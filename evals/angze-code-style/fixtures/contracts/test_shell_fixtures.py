from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_HEADER = (
    "name\tmode\tatoms\tstatus\tenergy_hartree\tinput_sha256\toutput_sha256\n"
)
REVIEW_SHA256 = "8396763f8384bd910b1299bbb969d2d840745e93a93032948ad2c4466a4de69e"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(
    script: Path, *arguments: str, environment: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if environment:
        env.update(environment)
    return subprocess.run(
        ["bash", str(script), *arguments],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_xyz(path: Path, atom_count: str) -> None:
    path.write_text(f"{atom_count}\nsynthetic\nH 0 0 0\n", encoding="utf-8")


def validate_main(script: Path) -> None:
    require(script.is_file(), f"missing fixture: {script}")
    syntax = subprocess.run(["bash", "-n", str(script)], check=False)
    require(syntax.returncode == 0, "main shell fixture fails bash -n")

    usage = run_script(script)
    require(usage.returncode == 64, f"usage exit code changed: {usage.returncode}")
    require(usage.stderr.startswith("usage:"), "usage diagnostic changed")

    with tempfile.TemporaryDirectory(prefix="scd-shell-errors-") as raw_tmp:
        root = Path(raw_tmp)
        missing = run_script(script, str(root / "missing"), str(root / "output"))
        require(missing.returncode == 66, "missing-source exit code changed")

        source = root / "source"
        source.mkdir()
        invalid_mode = run_script(script, str(source), str(root / "bad-mode"), "freq")
        require(invalid_mode.returncode == 64, "invalid-mode exit code changed")
        require(invalid_mode.stderr == "bad mode: freq\n", "invalid-mode diagnostic changed")

        no_match_output = root / "no-match"
        no_match = run_script(script, str(source), str(no_match_output), "opt", "*.xyz")
        require(no_match.returncode == 3, "no-matching-files exit code changed")
        require(no_match.stderr == "no matching structures\n", "no-match diagnostic changed")
        require(
            (no_match_output / "manifest.tsv").read_text(encoding="utf-8")
            == MANIFEST_HEADER,
            "empty-run manifest header changed",
        )

    with tempfile.TemporaryDirectory(prefix="scd-shell-valid-") as raw_tmp:
        root = Path(raw_tmp)
        source = root / "source"
        output = root / "output"
        scratch = root / "scratch"
        source.mkdir()
        scratch.mkdir()
        write_xyz(source / "b.xyz", "3")
        write_xyz(source / "a.xyz", "2")

        result = run_script(
            script,
            str(source),
            str(output),
            "opt",
            "*.xyz",
            environment={
                "DRY_RUN": "1",
                "METHOD": "PBE0",
                "BASIS": "def2-SVP",
                "SOLVENT": "Acetonitrile",
                "NPROCS": "4",
                "MAXCORE_MB": "999",
                "TMPDIR": str(scratch),
            },
        )
        require(result.returncode == 0, f"valid dry run failed: {result.stderr}")
        require(result.stdout == "processed 2 structure(s)\n", "success summary changed")
        manifest = (output / "manifest.tsv").read_text(encoding="utf-8")
        rows = manifest.splitlines()
        require(rows[0] + "\n" == MANIFEST_HEADER, "manifest header changed")
        require([row.split("\t")[0] for row in rows[1:]] == ["a", "b"], "sort order changed")

        expected_energies = {"a": "-100.246912000000", "b": "-100.370368000000"}
        for row in rows[1:]:
            name, mode, atoms, status, energy, input_hash, output_hash = row.split("\t")
            require(mode == "opt" and status == "ok", f"status changed for {name}")
            require(energy == expected_energies[name], f"dry-run energy changed for {name}")
            input_path = output / "inputs" / f"{name}.inp"
            output_path = output / "outputs" / f"{name}.out"
            require(input_hash == sha256(input_path), f"input hash changed for {name}")
            require(output_hash == sha256(output_path), f"output hash changed for {name}")
            input_text = input_path.read_text(encoding="utf-8")
            require(
                "! PBE0 def2-SVP TightSCF RIJCOSX NoSym SMD(Acetonitrile) Opt TightOpt"
                in input_text,
                "ORCA method, basis, solvent, directives, or opt mode changed",
            )
            require("%pal\n  nprocs 4\nend" in input_text, "nprocs behaviour changed")
            require("%maxcore 999" in input_text, "maxcore behaviour changed")
            require("Print[P_Basis] 2" in input_text, "ORCA output directive changed")
            require(f"* xyzfile 0 1 {source / (name + '.xyz')}" in input_text, "XYZ directive changed")
            require(atoms in {"2", "3"}, "atom count changed")
        require(not list(scratch.glob("orca-batch.*")), "default cleanup left temporary data")

    with tempfile.TemporaryDirectory(prefix="scd-shell-mixed-") as raw_tmp:
        root = Path(raw_tmp)
        source = root / "source"
        output = root / "output"
        scratch = root / "scratch"
        source.mkdir()
        scratch.mkdir()
        write_xyz(source / "a_bad.xyz", "unknown")
        write_xyz(source / "z_good.xyz", "4")
        result = run_script(
            script,
            str(source),
            str(output),
            "sp",
            environment={"DRY_RUN": "1", "TMPDIR": str(scratch)},
        )
        require(result.returncode == 2, "mixed-input aggregate failure exit code changed")
        require("invalid atom count:" in result.stderr, "invalid XYZ diagnostic missing")
        require("1 calculation(s) failed validation" in result.stderr, "aggregate diagnostic missing")
        rows = (output / "manifest.tsv").read_text(encoding="utf-8").splitlines()
        require([row.split("\t")[0] for row in rows[1:]] == ["a_bad", "z_good"], "mixed row order changed")
        bad_fields = rows[1].split("\t")
        good_fields = rows[2].split("\t")
        require(bad_fields[2:] == ["-", "invalid_xyz", "-", "-", "-"], "invalid status row changed")
        require(good_fields[1:5] == ["sp", "4", "ok", "-100.493824000000"], "valid mixed row changed")
        require("Opt TightOpt" not in (output / "inputs/z_good.inp").read_text(encoding="utf-8"), "sp mode gained optimization directives")
        require(good_fields[5] == sha256(output / "inputs/z_good.inp"), "mixed input hash changed")
        require(good_fields[6] == sha256(output / "outputs/z_good.out"), "mixed output hash changed")
        require(not list(scratch.glob("orca-batch.*")), "mixed-run cleanup left temporary data")

    with tempfile.TemporaryDirectory(prefix="scd-shell-keep-") as raw_tmp:
        root = Path(raw_tmp)
        source = root / "source"
        output = root / "output"
        scratch = root / "scratch"
        source.mkdir()
        scratch.mkdir()
        write_xyz(source / "one.xyz", "1")
        result = run_script(
            script,
            str(source),
            str(output),
            "sp",
            environment={"DRY_RUN": "1", "KEEP_TMP": "1", "TMPDIR": str(scratch)},
        )
        require(result.returncode == 0, "KEEP_TMP smoke run failed")
        kept = list(scratch.glob("orca-batch.*"))
        require(len(kept) == 1, "KEEP_TMP no longer preserves exactly one scratch directory")
        shutil.rmtree(kept[0])

    print("PASS shell main contract")


def validate_restraint(script: Path) -> None:
    require(script.is_file(), f"missing fixture: {script}")
    initial_hash = sha256(script)
    require(initial_hash == REVIEW_SHA256, "review-only shell source hash changed")
    syntax = subprocess.run(["bash", "-n", str(script)], check=False)
    require(syntax.returncode == 0, "review-only shell fixture fails bash -n")

    with tempfile.TemporaryDirectory(prefix="scd-shell-review-") as raw_tmp:
        root = Path(raw_tmp)
        source = root / "source"
        publish = root / "publish"
        source.mkdir()
        (source / "b.csv").write_text("delay,signal\n5,30\n", encoding="utf-8")
        (source / "a.csv").write_text("delay,signal\n1.5,10\n2,20\n", encoding="utf-8")
        result = run_script(
            script,
            str(source),
            str(publish),
            environment={"PUBLISH_SCALE": "2"},
        )
        require(result.returncode == 0, f"review-only smoke run failed: {result.stderr}")
        require((publish / "a.csv").read_text(encoding="utf-8") == "delay,signal\n3,10\n4,20\n", "configured scale or CSV formatting changed")
        require((publish / "b.csv").read_text(encoding="utf-8") == "delay,signal\n10,30\n", "configured scale changed")
        rows = (publish / "manifest.tsv").read_text(encoding="utf-8").splitlines()
        require(rows[0] == "file\trows\tsha256", "publish manifest header changed")
        require([row.split("\t")[0] for row in rows[1:]] == ["a.csv", "b.csv"], "publish manifest ordering changed")
        require([row.split("\t")[1] for row in rows[1:]] == ["2", "1"], "publish row counts changed")
        for row in rows[1:]:
            name, _, checksum = row.split("\t")
            require(checksum == sha256(publish / name), f"publish hash changed for {name}")

    require(sha256(script) == initial_hash, "review-only shell fixture changed during smoke test")
    print("PASS shell restraint contract")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    explicit_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    if mode in {"all", "main"}:
        validate_main(explicit_path or FIXTURE_ROOT / "shell/cramped_orca_batch.sh")
    if mode in {"all", "restraint"}:
        validate_restraint(explicit_path or FIXTURE_ROOT / "shell/review_only_publish.sh")
    if mode not in {"all", "main", "restraint"}:
        raise SystemExit(f"unknown mode: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
