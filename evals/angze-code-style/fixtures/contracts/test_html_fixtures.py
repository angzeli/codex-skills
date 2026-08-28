from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_SHA256 = "e158802dad213a33f35b4d060fa04558402d33bea98b470921ea1c1e655cb2c5"
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.ids: dict[str, dict[str, str | None]] = {}
        self.select_stack: list[str | None] = []
        self.options: dict[str, list[tuple[str | None, str]]] = {}
        self.option_value: str | None = None
        self.option_text: list[str] | None = None
        self.label_stack: list[set[str]] = []
        self.label_for: set[str] = set()
        self.nested_labels: set[str] = set()
        self.table_stack: list[str | None] = []
        self.th_text: list[str] | None = None
        self.headers: dict[str, list[str]] = {}
        self.text_by_id: dict[str, list[str]] = {}
        self.text_id_stack: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            require(element_id not in self.ids, f"duplicate id: {element_id}")
            self.ids[element_id] = attributes
            self.text_by_id[element_id] = []

        if tag not in VOID_ELEMENTS:
            self.stack.append(tag)
            self.text_id_stack.append(element_id)
        if tag == "label":
            self.label_stack.append(set())
            if attributes.get("for"):
                self.label_for.add(str(attributes["for"]))
        elif tag == "input" and self.label_stack and element_id:
            self.label_stack[-1].add(element_id)
        if tag == "select":
            self.select_stack.append(element_id)
            if element_id:
                self.options[element_id] = []
        elif tag == "option":
            self.option_value = attributes.get("value")
            self.option_text = []
        if tag == "table":
            self.table_stack.append(element_id)
            if element_id:
                self.headers[element_id] = []
        elif tag == "th" and self.table_stack:
            self.th_text = []

    def handle_endtag(self, tag: str) -> None:
        require(bool(self.stack) and self.stack[-1] == tag, f"unexpected closing tag: {tag}")
        self.stack.pop()
        if tag == "label":
            self.nested_labels.update(self.label_stack.pop())
        elif tag == "option":
            require(bool(self.select_stack) and self.select_stack[-1] is not None, "option outside identified select")
            self.options[str(self.select_stack[-1])].append(
                (self.option_value, "".join(self.option_text or []).strip())
            )
            self.option_value = None
            self.option_text = None
        elif tag == "select":
            self.select_stack.pop()
        elif tag == "th" and self.table_stack:
            table_id = self.table_stack[-1]
            if table_id:
                self.headers[table_id].append("".join(self.th_text or []).strip())
            self.th_text = None
        elif tag == "table":
            self.table_stack.pop()
        self.text_id_stack.pop()

    def handle_data(self, data: str) -> None:
        if self.option_text is not None:
            self.option_text.append(data)
        if self.th_text is not None:
            self.th_text.append(data)
        for element_id in reversed(self.text_id_stack):
            if element_id:
                self.text_by_id[element_id].append(data)
                break

    def close(self) -> None:
        super().close()
        require(not self.stack, f"unclosed tags: {self.stack}")


def parse_html(path: Path) -> tuple[str, ContractParser]:
    text = path.read_text(encoding="utf-8")
    parser = ContractParser()
    parser.feed(text)
    parser.close()
    return text, parser


def validate_main(path: Path) -> None:
    require(path.is_file(), f"missing fixture: {path}")
    text, parser = parse_html(path)
    required_ids = {
        "sample-filter",
        "region-filter",
        "show-components",
        "reset-button",
        "export-button",
        "row-count",
        "mean-intensity",
        "max-energy",
        "plot-status",
        "profile-plot",
        "results-table",
        "results-body",
    }
    require(required_ids <= parser.ids.keys(), "required DOM ID is missing")
    require(parser.options["sample-filter"] == [
        ("all", "All"),
        ("PDI-Me-COOH", "PDI-Me-COOH"),
        ("PDI-H-COOH", "PDI-H-COOH"),
        ("PDI-OMe-COOH", "PDI-OMe-COOH"),
    ], "sample filter options changed")
    require(parser.options["region-filter"] == [
        ("all", "All"),
        ("C1s", "C1s"),
        ("N1s", "N1s"),
        ("O1s", "O1s"),
    ], "region filter options changed")
    require(
        parser.headers["results-table"]
        == ["Sample", "Region", "BE / eV", "Scaled intensity", "Component"],
        "table header contract changed",
    )
    require({"sample-filter", "region-filter"} <= parser.label_for, "select label association changed")
    require("show-components" in parser.nested_labels or "show-components" in parser.label_for, "checkbox label association changed")
    require(parser.ids["profile-plot"].get("role") == "img", "plot role changed")
    require(
        parser.ids["profile-plot"].get("aria-label") == "Scaled XPS intensity profile",
        "plot accessible name changed",
    )
    require(parser.ids["plot-status"].get("aria-live") == "polite", "live-region behaviour changed")
    require("schema version 3" in text, "visible schema version changed")
    require(
        "sample,region,binding_energy_ev,intensity_cps,component" in text,
        "visible or executable CSV header changed",
    )

    node = shutil.which("node")
    require(bool(node), "Node.js is required for the dependency-free dashboard harness")
    harness = Path(__file__).with_name("xps_dashboard_harness.js")
    result = subprocess.run([str(node), str(harness), str(path)], check=False, capture_output=True, text=True)
    require(result.returncode == 0, f"dashboard behaviour harness failed:\n{result.stdout}{result.stderr}")
    require("PASS HTML dashboard behaviour contract" in result.stdout, "dashboard harness did not complete")
    print("PASS HTML main contract")


def validate_restraint(path: Path) -> None:
    require(path.is_file(), f"missing fixture: {path}")
    initial_bytes = path.read_bytes()
    require(hashlib.sha256(initial_bytes).hexdigest() == SNAPSHOT_SHA256, "generated snapshot bytes changed")
    text, parser = parse_html(path)
    require(parser.ids["generated-report"].get("data-schema-version") == "3", "snapshot schema attribute changed")
    require(parser.headers["summary-table"] == ["sample", "region", "value"], "snapshot headers changed")

    expected_rows = [
        ('0', 'PDI-Me-COOH', 'C1s', '179.4'),
        ('1', 'PDI-H-COOH', 'C1s', '225.1'),
        ('2', 'PDI-OMe-COOH', 'C1s', '243.4'),
    ]
    actual_rows = re.findall(
        r'<tr data-row-order="(\d+)"><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td></tr>',
        text,
    )
    require(actual_rows == expected_rows, "snapshot table row values or ordering changed")

    match = re.search(
        r'<script id="report-data" type="application/json">([^<]+)</script>',
        text,
    )
    require(bool(match), "embedded report JSON is missing")
    expected_json = (
        '{"schema_version":3,"columns":["sample","region","value"],'
        '"rows":[["PDI-Me-COOH","C1s",179.4],["PDI-H-COOH","C1s",225.1],'
        '["PDI-OMe-COOH","C1s",243.4]]}'
    )
    require(match.group(1) == expected_json, "embedded JSON bytes changed")
    require(json.loads(match.group(1))["schema_version"] == 3, "embedded schema version changed")
    require(path.read_bytes() == initial_bytes, "generated snapshot changed during validation")
    print("PASS HTML restraint contract")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    explicit_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    if mode in {"all", "main"}:
        validate_main(explicit_path or FIXTURE_ROOT / "html/cramped_xps_dashboard.html")
    if mode in {"all", "restraint"}:
        validate_restraint(explicit_path or FIXTURE_ROOT / "html/generated_report_snapshot.html")
    if mode not in {"all", "main", "restraint"}:
        raise SystemExit(f"unknown mode: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
