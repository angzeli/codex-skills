from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parents[1]
FRAGILE_SHA256 = "5f2934fccb73798192ebe1af68f19176ef46a9c0ac42122693bade22c99b4841"
MAIN_TEXT_SHA256 = "ae3e3ede94c0851308ffea5d2b7fc47550ceb2fd5c96c1fee2f7c233e3c3e9a3"
APPENDIX_TEXT_SHA256 = "c8c90612c87cc75c4a595162e82779b3912b0c303dce092f269cad43be55401d"
FRAGILE_TEXT_SHA256 = "9d1d0da91711ee17b1c302bdb8c26f6d5449ed3510fa3448c3ad980aec539377"
MAIN_LABELS = {
    "sec:workflow",
    "fig:workflow",
    "eq:response",
    "sec:descriptors",
    "tab:descriptors",
    "sec:electrochem",
    "tab:electrochem",
    "fig:comparison",
    "sec:reproducibility",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_source(text: str) -> str:
    return " ".join(text.split())


def compile_tex(source: Path, appendix: bool, expected_pages: int) -> tuple[Path, Path, str, tempfile.TemporaryDirectory[str]]:
    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        raise RuntimeError("pdflatex is unavailable")
    temporary = tempfile.TemporaryDirectory(prefix="scd-latex-contract-")
    output_dir = Path(temporary.name)
    job_name = "with_appendix" if appendix else "without_appendix"
    if appendix:
        source_argument = rf"\def\SHOWAPPENDIX{{1}}\input{{{source}}}"
    else:
        source_argument = str(source)
    command = [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-jobname={job_name}",
        "-output-directory",
        str(output_dir),
        source_argument,
    ]
    last_output = ""
    for _ in range(2):
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        last_output = result.stdout + result.stderr
        require(result.returncode == 0, f"pdflatex failed for {source.name}:\n{last_output}")
    require("undefined references" not in last_output.lower(), "references remain undefined after two passes")

    pdf_path = output_dir / f"{job_name}.pdf"
    aux_path = output_dir / f"{job_name}.aux"
    require(pdf_path.is_file() and aux_path.is_file(), "pdflatex outputs are missing")
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        info = subprocess.run([pdfinfo, str(pdf_path)], check=True, capture_output=True, text=True).stdout
        match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
        require(bool(match), "pdfinfo did not report a page count")
        require(int(match.group(1)) == expected_pages, f"page count changed: {match.group(1)}")
    else:
        require(f"({expected_pages} pages" in last_output or f"({expected_pages} page" in last_output, "compile log page count changed")
    return pdf_path, aux_path, last_output, temporary


def extract_normalized_text(pdf_path: Path) -> str | None:
    ghostscript = shutil.which("gs")
    if not ghostscript:
        return None
    result = subprocess.run(
        [ghostscript, "-q", "-sDEVICE=txtwrite", "-o", "-", str(pdf_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return " ".join(result.stdout.split())


def labels_from_aux(aux_path: Path) -> set[str]:
    return set(re.findall(r"\\newlabel\{([^}]+)\}", aux_path.read_text(encoding="utf-8")))


def validate_main(source: Path, *, compile_output: bool = True) -> None:
    require(source.is_file(), f"missing fixture: {source}")
    text = source.read_text(encoding="utf-8")
    compact = normalized_source(text)
    require(r"\documentclass[10pt]{article}" in text, "document class contract changed")

    macro_values = {
        "SampleMe": r"\textsc{PDI-Me-COOH}",
        "SampleH": r"\textsc{PDI-H-COOH}",
        "SampleOMe": r"\textsc{PDI-OMe-COOH}",
        "configuredshift": "0.037",
        "orbitaliso": "0.030",
        "densityiso": "0.002",
        "energyunit": r"\ensuremath{\mathrm{E_h}}",
        "dipoleunit": "D",
    }
    for name, value in macro_values.items():
        require(rf"\newcommand{{\{name}}}{{{value}}}" in text, f"macro changed: {name}")
    require(r"\setlength{\panelwidth}{0.295\linewidth}" in text, "panel width changed")
    require(r"\vspace{-0.6em}" in text, "negative figure-spacing workaround changed")
    require(r"\ifdefined\SHOWAPPENDIX" in text and r"\fi" in text, "appendix conditional changed")

    source_labels = set(re.findall(r"\\label\{([^}]+)\}", text))
    require(source_labels == MAIN_LABELS | {"sec:appendix"}, "source labels changed")
    references = set(re.findall(r"\\ref\{([^}]+)\}", text))
    require(references == MAIN_LABELS - {"sec:workflow", "sec:descriptors", "sec:electrochem", "sec:reproducibility"}, "reference targets changed")

    descriptor_rows = [
        r"\SampleMe & -4089.158196 & 9.274 & \orbitaliso & \densityiso \\",
        r"\SampleH & -4010.441141 & 7.861 & \orbitaliso & \densityiso \\",
        r"\SampleOMe & -4239.641138 & 3.778 & \orbitaliso & \densityiso \\",
    ]
    electrochemical_rows = [
        r"\SampleMe & 0.510 & -0.383 & 18.6 & 179.4 & 0.669 \\",
        r"\SampleH & 0.398 & -0.220 & 18.3 & 225.1 & 0.781 \\",
        r"\SampleOMe & 0.414 & -0.185 & 13.2 & 243.4 & 0.768 \\",
    ]
    last_index = -1
    for row in descriptor_rows + electrochemical_rows:
        index = compact.find(normalized_source(row))
        require(index > last_index, f"table value or row order changed: {row}")
        last_index = index
    require("Sample & Energy & Dipole & Orbital surface & Density surface" in compact, "descriptor columns changed")
    require(r"Sample & $E_{\mathrm{pa}}$ & $E_{\mathrm{pc}}$ & $R_{\mathrm{s}}$ & $R_{\mathrm{ct}}$ & $n$" in compact, "electrochemical columns changed")

    if not compile_output:
        print("PASS LaTeX main static contract")
        return

    pdf, aux, _, temporary = compile_tex(source, appendix=False, expected_pages=2)
    try:
        require(labels_from_aux(aux) == MAIN_LABELS, "non-appendix AUX labels changed")
        visible = extract_normalized_text(pdf)
        if visible is not None:
            require("Conditional appendix" not in visible, "appendix is visible without SHOWAPPENDIX")
            require(sha256_bytes(visible.encode()) == MAIN_TEXT_SHA256, "non-appendix visible text changed")
    finally:
        temporary.cleanup()

    pdf, aux, _, temporary = compile_tex(source, appendix=True, expected_pages=2)
    try:
        require(labels_from_aux(aux) == MAIN_LABELS | {"sec:appendix"}, "appendix AUX labels changed")
        visible = extract_normalized_text(pdf)
        if visible is not None:
            require("Conditional appendix" in visible, "appendix is missing with SHOWAPPENDIX")
            require(sha256_bytes(visible.encode()) == APPENDIX_TEXT_SHA256, "appendix visible text changed")
    finally:
        temporary.cleanup()

    print("PASS LaTeX main contract")


def validate_restraint(source: Path, *, compile_output: bool = True) -> None:
    require(source.is_file(), f"missing fixture: {source}")
    initial_bytes = source.read_bytes()
    require(sha256_bytes(initial_bytes) == FRAGILE_SHA256, "fragile source hash changed")
    text = initial_bytes.decode("utf-8")
    compact = normalized_source(text)

    macros = [
        r"\newcommand{\ManuscriptType}{Research Article}",
        r"\newcommand{\JournalSection}{Photochemistry}",
        r"\newcommand{\SchemaVersion}{3}",
        r"\newcommand{\ConfiguredFactor}{10^{-9}}",
        r"\newcommand{\UnknownCorrection}{0.037}",
    ]
    positions = [text.find(macro) for macro in macros]
    require(all(position >= 0 for position in positions), "publisher macro or value changed")
    require(positions == sorted(positions), "publisher macro order changed")
    require("Field & Type & Required" in compact, "schema table columns changed")
    schema_rows = ["sample & string & yes", "region & string & yes", "value & number & yes"]
    row_positions = [compact.find(row) for row in schema_rows]
    require(all(position >= 0 for position in row_positions), "schema row changed")
    require(row_positions == sorted(row_positions), "schema row order changed")
    require(r"\vspace{-0.4em}" in text, "publisher spacing workaround changed")
    require("source and target units are not established" in compact, "factor ambiguity warning changed")
    require("physical interpretation is deliberately unspecified" in compact, "correction ambiguity warning changed")

    if not compile_output:
        require(source.read_bytes() == initial_bytes, "fragile source changed during validation")
        print("PASS LaTeX restraint static contract")
        return

    pdf, _, _, temporary = compile_tex(source, appendix=False, expected_pages=1)
    try:
        visible = extract_normalized_text(pdf)
        if visible is not None:
            require(sha256_bytes(visible.encode()) == FRAGILE_TEXT_SHA256, "fragile visible text changed")
    finally:
        temporary.cleanup()
    require(source.read_bytes() == initial_bytes, "fragile source changed during validation")
    print("PASS LaTeX restraint contract")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    explicit_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    compile_output = mode != "static"
    if mode in {"all", "main", "static"}:
        validate_main(
            explicit_path or FIXTURE_ROOT / "latex/crowded_scientific_report.tex",
            compile_output=compile_output,
        )
    if mode in {"all", "restraint", "static"}:
        validate_restraint(
            explicit_path or FIXTURE_ROOT / "latex/fragile_template_snippet.tex",
            compile_output=compile_output,
        )
    if mode not in {"all", "main", "restraint", "static"}:
        raise SystemExit(f"unknown mode: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
