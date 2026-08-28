#!/usr/bin/env python3
"""Validate a release manifest, frozen runtime, and public release surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


class IntegrityError(RuntimeError):
    """Raised when a release-integrity contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegrityError(message)


def safe_repo_path(repo_root: Path, raw_path: str) -> Path:
    posix_path = PurePosixPath(raw_path)
    require(
        raw_path == posix_path.as_posix()
        and not posix_path.is_absolute()
        and ".." not in posix_path.parts,
        f"manifest path is not a safe repository-relative path: {raw_path!r}",
    )
    return repo_root.joinpath(*posix_path.parts)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tracked_paths(repo_root: Path, pathspec: str) -> set[str]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--", pathspec], cwd=repo_root
    )
    return {path for path in output.decode().split("\0") if path}


def validate_file_records(
    repo_root: Path, records: object, label: str
) -> list[tuple[str, str]]:
    require(isinstance(records, list) and records, f"{label} files must be a non-empty list")

    validated: list[tuple[str, str]] = []
    seen: set[str] = set()
    for record in records:
        require(isinstance(record, dict), f"{label} file record must be an object")
        raw_path = record.get("path")
        expected_hash = record.get("sha256")
        expected_size = record.get("bytes")
        require(isinstance(raw_path, str), f"{label} file path must be a string")
        require(raw_path not in seen, f"duplicate {label} file path: {raw_path}")
        require(
            isinstance(expected_hash, str)
            and re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None,
            f"invalid SHA-256 for {raw_path}",
        )
        require(
            isinstance(expected_size, int) and expected_size >= 0,
            f"invalid byte size for {raw_path}",
        )

        path = safe_repo_path(repo_root, raw_path)
        require(path.is_file() and not path.is_symlink(), f"missing regular file: {raw_path}")
        data = path.read_bytes()
        actual_hash = sha256_bytes(data)
        require(actual_hash == expected_hash, f"SHA-256 mismatch: {raw_path}")
        require(len(data) == expected_size, f"byte-size mismatch: {raw_path}")
        seen.add(raw_path)
        validated.append((raw_path, actual_hash))

    require(
        [path for path, _ in validated] == sorted(path for path, _ in validated),
        f"{label} file records must be C-sorted by path",
    )
    return validated


def validate_markdown_links(repo_root: Path, files: list[Path]) -> int:
    link_count = 0
    for source in files:
        for match in re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
            link_count += 1
            reference = match.strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not reference or reference.startswith(
                ("#", "http://", "https://", "mailto:", "skill://", "$")
            ):
                continue
            target = (source.parent / reference).resolve()
            try:
                target.relative_to(repo_root)
            except ValueError as error:
                raise IntegrityError(
                    f"relative link escapes repository in {source.relative_to(repo_root)}: {reference}"
                ) from error
            require(
                target.exists(),
                f"broken relative link in {source.relative_to(repo_root)}: {reference}",
            )
    return link_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--expected-runtime-sha", required=True)
    parser.add_argument("--expected-skill", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--forbid-invocation", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = args.manifest
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path
    manifest_path = manifest_path.resolve()
    try:
        manifest_path.relative_to(repo_root)
    except ValueError as error:
        raise IntegrityError("manifest must be inside the repository") from error

    require(
        re.fullmatch(r"[0-9a-f]{64}", args.expected_runtime_sha) is not None,
        "expected runtime SHA-256 must be 64 lowercase hexadecimal characters",
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("schema_version") == 1, "unsupported manifest schema")
    require(manifest.get("skill") == args.expected_skill, "manifest skill mismatch")
    require(manifest.get("version") == args.expected_version, "manifest version mismatch")

    runtime = manifest.get("runtime_snapshot")
    require(isinstance(runtime, dict), "missing runtime_snapshot object")
    require(
        runtime.get("sha256") == args.expected_runtime_sha,
        "manifest runtime SHA-256 does not match the accepted release hash",
    )
    runtime_records = validate_file_records(
        repo_root, runtime.get("files"), "runtime snapshot"
    )

    runtime_root = f"skills/{args.expected_skill}"
    listed_runtime_paths = {path for path, _ in runtime_records}
    require(
        listed_runtime_paths == tracked_paths(repo_root, runtime_root),
        "manifest runtime file set does not match tracked runtime files",
    )
    aggregate_records = []
    for raw_path, digest in runtime_records:
        runtime_relative = PurePosixPath(raw_path).relative_to(runtime_root).as_posix()
        aggregate_records.append(f"{digest}  {runtime_relative}")
    actual_runtime_sha = sha256_bytes(
        ("\n".join(aggregate_records) + "\n").encode()
    )
    require(
        actual_runtime_sha == args.expected_runtime_sha,
        "tracked runtime aggregate SHA-256 mismatch",
    )

    notebook_section = manifest.get("notebook_acceptance_fixtures")
    require(isinstance(notebook_section, dict), "missing notebook fixture section")
    notebook_records = validate_file_records(
        repo_root, notebook_section.get("files"), "notebook acceptance fixture"
    )
    recorded_notebooks = {
        path for path, _ in notebook_records if PurePosixPath(path).suffix == ".ipynb"
    }
    tracked_eval_paths = tracked_paths(repo_root, f"evals/{args.expected_skill}")
    tracked_notebooks = {
        path for path in tracked_eval_paths if PurePosixPath(path).suffix == ".ipynb"
    }
    require(
        tracked_notebooks == recorded_notebooks,
        "tracked notebooks do not match the synthetic notebooks in the manifest",
    )
    raw_log_paths = {
        path
        for path in tracked_eval_paths
        if PurePosixPath(path).suffix in {".jsonl", ".log"}
    }
    require(not raw_log_paths, "raw evaluation logs are tracked")
    allowed_result_paths = {
        f"evals/{args.expected_skill}/results/.gitkeep",
        f"evals/{args.expected_skill}/results/result.template.md",
    }
    require(
        tracked_paths(repo_root, f"evals/{args.expected_skill}/results")
        <= allowed_result_paths,
        "unexpected raw result artifacts are tracked",
    )

    version_label = f"v{args.expected_version}"
    release_path = repo_root / f"docs/releases/{args.expected_skill}-{version_label}.md"
    evaluation_path = (
        repo_root / f"docs/evaluations/{args.expected_skill}-{version_label}.md"
    )
    acceptance_path = repo_root / (
        f"docs/evaluations/{args.expected_skill}-{version_label}-real-notebook.md"
    )
    current_surfaces = [
        repo_root / "README.md",
        repo_root / "GETTING_STARTED.md",
        repo_root / "CHANGELOG.md",
        release_path,
        evaluation_path,
        acceptance_path,
        repo_root / f"evals/{args.expected_skill}/README.md",
        repo_root / f"evals/{args.expected_skill}/prompts.yaml",
        repo_root / runtime_root / "SKILL.md",
        repo_root / runtime_root / "agents/openai.yaml",
    ]
    for path in current_surfaces:
        require(path.is_file(), f"missing current release surface: {path.relative_to(repo_root)}")

    invocation = f"${args.expected_skill}"
    skill_text = (repo_root / runtime_root / "SKILL.md").read_text(encoding="utf-8")
    require(
        re.search(rf"(?m)^name:\s*{re.escape(args.expected_skill)}\s*$", skill_text)
        is not None,
        "SKILL.md frontmatter name mismatch",
    )
    agent_text = (repo_root / runtime_root / "agents/openai.yaml").read_text(
        encoding="utf-8"
    )
    prompts_text = (repo_root / f"evals/{args.expected_skill}/prompts.yaml").read_text(
        encoding="utf-8"
    )
    require(invocation in agent_text, "agent metadata lacks the current invocation")
    require(
        re.search(rf"(?m)^skill:\s*{re.escape(args.expected_skill)}\s*$", prompts_text)
        is not None
        and invocation in prompts_text,
        "evaluation prompts lack the current skill identity or invocation",
    )
    require(
        f"{args.expected_skill} {version_label}" in release_path.read_text(encoding="utf-8")
        and f"{args.expected_skill} {version_label}"
        in evaluation_path.read_text(encoding="utf-8"),
        "current release documents have inconsistent identity",
    )
    require(
        "experimental" in release_path.read_text(encoding="utf-8").lower(),
        "release note does not state experimental status",
    )
    require(
        "REAL-NOTEBOOK ACCEPTANCE PASSED"
        in acceptance_path.read_text(encoding="utf-8"),
        "real-notebook acceptance is not recorded as passed",
    )
    controlled_results = manifest.get("controlled_results")
    require(isinstance(controlled_results, dict), "missing controlled_results object")
    real_acceptance = controlled_results.get("real_notebook_acceptance")
    require(
        isinstance(real_acceptance, dict) and real_acceptance.get("status") == "pass",
        "manifest real-notebook acceptance is not passed",
    )

    combined_current_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace") for path in current_surfaces
    )
    for forbidden in args.forbid_invocation:
        require(
            forbidden not in combined_current_text,
            f"forbidden current-facing invocation found: {forbidden}",
        )
    require(
        re.search(
            r"REAL-NOTEBOOK ACCEPTANCE PENDING|PARTIALLY READY|"
            r"real-notebook acceptance[^.]*pending",
            combined_current_text,
            flags=re.IGNORECASE,
        )
        is None,
        "current release surfaces still describe real-notebook acceptance as pending",
    )

    personal_path_pattern = re.compile(
        rb"/Users/[^/$\s]+/|/home/[^/$\s]+/|[A-Za-z]:\\Users\\[^\\]+\\"
    )
    privacy_paths = {
        path for path, _ in runtime_records + notebook_records
    } | {str(path.relative_to(repo_root)) for path in current_surfaces}
    for raw_path in sorted(privacy_paths):
        require(
            personal_path_pattern.search((repo_root / raw_path).read_bytes()) is None,
            f"personal absolute path found: {raw_path}",
        )

    markdown_surfaces = [path for path in current_surfaces if path.suffix == ".md"]
    link_count = validate_markdown_links(repo_root, markdown_surfaces)

    print(f"PASS release identity: {args.expected_skill} {version_label} ({invocation})")
    print(f"PASS runtime files: {len(runtime_records)}")
    print(f"PASS runtime SHA-256: {actual_runtime_sha}")
    print(f"PASS notebook fixture records: {len(notebook_records)}")
    print(f"PASS current release links: {link_count}")
    print("PASS tracked evidence and path sanitation")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IntegrityError, json.JSONDecodeError, OSError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
