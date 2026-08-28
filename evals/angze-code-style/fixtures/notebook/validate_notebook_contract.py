#!/usr/bin/env python3
"""Validate narrowly allowlisted edits to a Jupyter notebook.

The optional behavior probe executes only trusted synthetic fixture code. It is
not a security sandbox and does not establish general notebook equivalence.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


class InputError(Exception):
    """Raised when the original notebook or contract is invalid or ambiguous."""


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _parse_json(data: bytes, *, label: str) -> tuple[Any, str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} is not valid UTF-8: {exc}") from exc

    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{label} is not strict JSON: {exc}") from exc
    return value, text


def _notebook_shape_error(notebook: Any) -> str | None:
    if not isinstance(notebook, dict):
        return "notebook root must be an object"
    if not isinstance(notebook.get("cells"), list):
        return "notebook cells must be an array"
    for index, cell in enumerate(notebook["cells"]):
        if not isinstance(cell, dict):
            return f"cells[{index}] must be an object"
        if not isinstance(cell.get("id"), str) or not cell["id"]:
            return f"cells[{index}].id must be a non-empty string"
        if cell.get("cell_type") not in {"code", "markdown", "raw"}:
            return f"cells[{index}].cell_type is invalid"
        source = cell.get("source")
        if not isinstance(source, (str, list)):
            return f"cells[{index}].source must be a string or string array"
        if isinstance(source, list) and not all(isinstance(line, str) for line in source):
            return f"cells[{index}].source contains a non-string value"
    return None


class _SpanScanner:
    """Collect raw JSON value spans by structural path."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.decoder = json.JSONDecoder()
        self.spans: dict[tuple[Any, ...], tuple[int, int]] = {}

    def scan(self) -> dict[tuple[Any, ...], tuple[int, int]]:
        end = self._value(self._space(0), ())
        if self._space(end) != len(self.text):
            raise ValueError("unexpected content after JSON document")
        return self.spans

    def _space(self, index: int) -> int:
        while index < len(self.text) and self.text[index] in " \t\r\n":
            index += 1
        return index

    def _value(self, index: int, path: tuple[Any, ...]) -> int:
        index = self._space(index)
        start = index
        if index >= len(self.text):
            raise ValueError("unexpected end of JSON document")
        if self.text[index] == "{":
            end = self._object(index, path)
        elif self.text[index] == "[":
            end = self._array(index, path)
        else:
            _, end = self.decoder.raw_decode(self.text, index)
        self.spans[path] = (start, end)
        return end

    def _object(self, index: int, path: tuple[Any, ...]) -> int:
        index = self._space(index + 1)
        if index < len(self.text) and self.text[index] == "}":
            return index + 1
        while True:
            key, end = self.decoder.raw_decode(self.text, index)
            if not isinstance(key, str):
                raise ValueError("object key is not a string")
            index = self._space(end)
            if index >= len(self.text) or self.text[index] != ":":
                raise ValueError("missing colon after object key")
            index = self._value(index + 1, path + (key,))
            index = self._space(index)
            if index >= len(self.text):
                raise ValueError("unterminated object")
            if self.text[index] == "}":
                return index + 1
            if self.text[index] != ",":
                raise ValueError("missing comma in object")
            index = self._space(index + 1)

    def _array(self, index: int, path: tuple[Any, ...]) -> int:
        index = self._space(index + 1)
        if index < len(self.text) and self.text[index] == "]":
            return index + 1
        item_index = 0
        while True:
            index = self._value(index, path + (item_index,))
            item_index += 1
            index = self._space(index)
            if index >= len(self.text):
                raise ValueError("unterminated array")
            if self.text[index] == "]":
                return index + 1
            if self.text[index] != ",":
                raise ValueError("missing comma in array")
            index = self._space(index + 1)


def _source_text(source: str | list[str]) -> str:
    return source if isinstance(source, str) else "".join(source)


def _changed_line_count(before: str, after: str) -> int:
    matcher = difflib.SequenceMatcher(a=before.splitlines(), b=after.splitlines())
    return sum(
        max(old_end - old_start, new_end - new_start)
        for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes()
        if tag != "equal"
    )


class _DocstringStripper(ast.NodeTransformer):
    def _strip(self, node: ast.AST) -> ast.AST:
        body = getattr(node, "body", None)
        if (
            isinstance(body, list)
            and body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            node.body = body[1:]
        return self.generic_visit(node)

    visit_Module = _strip
    visit_FunctionDef = _strip
    visit_AsyncFunctionDef = _strip
    visit_ClassDef = _strip


def _python_semantics(source: str) -> str:
    tree = ast.parse(source)
    stripped = _DocstringStripper().visit(tree)
    ast.fix_missing_locations(stripped)
    return ast.dump(stripped, include_attributes=False)


def _mask_spans(
    text: str,
    spans: dict[tuple[Any, ...], tuple[int, int]],
    paths: set[tuple[Any, ...]],
) -> str:
    replacements = []
    for path in paths:
        if path not in spans:
            raise ValueError(f"missing raw JSON span for {path}")
        start, end = spans[path]
        replacements.append((start, end))
    for start, end in sorted(replacements, reverse=True):
        text = text[:start] + '"__ALLOWLISTED_SOURCE__"' + text[end:]
    return text


def _violation(category: str, path: str, message: str) -> dict[str, str]:
    return {"category": category, "path": path, "message": message}


def _validate_contract(contract: Any, original: dict[str, Any], original_data: bytes) -> None:
    if not isinstance(contract, dict):
        raise InputError("contract root must be an object")
    if contract.get("schema_version") != 1:
        raise InputError("contract schema_version must be 1")
    if contract.get("policy") not in {"allowlisted-source-edits", "byte-identical"}:
        raise InputError("contract policy is invalid")
    expected_hash = contract.get("original_sha256")
    actual_hash = hashlib.sha256(original_data).hexdigest()
    if expected_hash != actual_hash:
        raise InputError("contract original_sha256 does not match the original notebook")
    if contract.get("notebook_role") not in {
        "source",
        "tutorial",
        "analysis artifact",
        "generated",
        "unknown",
    }:
        raise InputError("contract notebook_role is invalid")
    allowed = contract.get("allowed_source_changes")
    if not isinstance(allowed, list):
        raise InputError("allowed_source_changes must be an array")
    seen: set[int] = set()
    for selector in allowed:
        if not isinstance(selector, dict):
            raise InputError("each source selector must be an object")
        index = selector.get("cell_index")
        if not isinstance(index, int) or isinstance(index, bool):
            raise InputError("source selector cell_index must be an integer")
        if index in seen:
            raise InputError(f"duplicate source selector for cells[{index}]")
        seen.add(index)
        if index < 0 or index >= len(original["cells"]):
            raise InputError(f"source selector cells[{index}] is out of range")
        cell = original["cells"][index]
        if selector.get("cell_id") != cell.get("id"):
            raise InputError(f"source selector cells[{index}] has a stale cell_id")
        if selector.get("cell_type") != cell.get("cell_type"):
            raise InputError(f"source selector cells[{index}] has a stale cell_type")
        if selector.get("edit_kind") not in {"markdown", "python-comments-docstrings"}:
            raise InputError(f"source selector cells[{index}] has an invalid edit_kind")
        maximum = selector.get("max_changed_lines")
        if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < 0:
            raise InputError(f"source selector cells[{index}] has an invalid line limit")
    if contract["policy"] == "byte-identical" and allowed:
        raise InputError("byte-identical contracts cannot allow source changes")


def _run_probe(
    notebook: dict[str, Any], probe: dict[str, Any], *, label: str
) -> tuple[Any | None, str | None]:
    selectors = probe.get("selected_code_cells")
    callable_name = probe.get("callable")
    timeout = probe.get("timeout_seconds", 5)
    if not isinstance(selectors, list) or not selectors:
        return None, "selected_code_cells must be a non-empty array"
    if not isinstance(callable_name, str) or not callable_name.isidentifier():
        return None, "probe callable must be a Python identifier"
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
        return None, "probe timeout_seconds must be positive"

    sources = []
    for selector in selectors:
        if not isinstance(selector, dict) or not isinstance(selector.get("cell_index"), int):
            return None, "probe selector is malformed"
        index = selector["cell_index"]
        if index < 0 or index >= len(notebook["cells"]):
            return None, f"probe selector cells[{index}] is out of range"
        cell = notebook["cells"][index]
        if cell.get("id") != selector.get("cell_id") or cell.get("cell_type") != "code":
            return None, f"probe selector cells[{index}] does not match a code cell"
        sources.append(_source_text(cell["source"]))

    wrapper = (
        "\n\n".join(sources)
        + "\n\nimport json as __probe_json\n"
        + f"__probe_value = {callable_name}()\n"
        + "print('__NOTEBOOK_PROBE__' + __probe_json.dumps("
        + "__probe_value, ensure_ascii=False, sort_keys=True, separators=(',', ':')))\n"
    )
    environment = {
        "LC_ALL": "C",
        "PATH": os.environ.get("PATH", ""),
        "PYTHONIOENCODING": "utf-8",
    }
    try:
        with tempfile.TemporaryDirectory(prefix="notebook-contract-probe-") as workdir:
            completed = subprocess.run(
                [sys.executable, "-I", "-c", wrapper],
                cwd=workdir,
                env=environment,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
    except subprocess.TimeoutExpired:
        return None, f"{label} probe timed out"
    if completed.returncode != 0:
        return None, f"{label} probe raised an exception"
    marker = "__NOTEBOOK_PROBE__"
    lines = completed.stdout.splitlines()
    if len(lines) != 1 or not lines[0].startswith(marker) or completed.stderr:
        return None, f"{label} probe produced unexpected stdout or stderr"
    try:
        return json.loads(lines[0][len(marker) :]), None
    except json.JSONDecodeError:
        return None, f"{label} probe returned invalid JSON"


def validate_bytes(
    original_data: bytes, candidate_data: bytes, contract: dict[str, Any]
) -> dict[str, Any]:
    """Return a deterministic validation record for two notebook byte streams."""

    try:
        original, original_text = _parse_json(original_data, label="original notebook")
    except ValueError as exc:
        raise InputError(str(exc)) from exc
    shape_error = _notebook_shape_error(original)
    if shape_error:
        raise InputError(f"original notebook: {shape_error}")
    _validate_contract(contract, original, original_data)

    violations: list[dict[str, str]] = []
    try:
        candidate, candidate_text = _parse_json(candidate_data, label="candidate notebook")
    except ValueError as exc:
        return {
            "valid": False,
            "policy": contract["policy"],
            "notebook_role": contract["notebook_role"],
            "intended_source_changes": [],
            "violations": [_violation("parseability", "$", str(exc))],
            "probe": {"status": "not-run"},
        }
    shape_error = _notebook_shape_error(candidate)
    if shape_error:
        violations.append(_violation("parseability", "$", shape_error))
        return {
            "valid": False,
            "policy": contract["policy"],
            "notebook_role": contract["notebook_role"],
            "intended_source_changes": [],
            "violations": violations,
            "probe": {"status": "not-run"},
        }

    if contract["policy"] == "byte-identical":
        if original_data != candidate_data:
            violations.append(
                _violation(
                    "serialization-locality",
                    "$",
                    "byte-identical notebook changed",
                )
            )
        return {
            "valid": not violations,
            "policy": contract["policy"],
            "notebook_role": contract["notebook_role"],
            "intended_source_changes": [],
            "violations": violations,
            "probe": {"status": "not-applicable"},
        }

    allowed = {entry["cell_index"]: entry for entry in contract["allowed_source_changes"]}
    original_cells = original["cells"]
    candidate_cells = candidate["cells"]
    if len(original_cells) != len(candidate_cells):
        violations.append(_violation("structural", "$.cells", "cell count changed"))

    original_identity = [(cell.get("id"), cell.get("cell_type")) for cell in original_cells]
    candidate_identity = [(cell.get("id"), cell.get("cell_type")) for cell in candidate_cells]
    if original_identity != candidate_identity:
        violations.append(
            _violation("structural", "$.cells", "cell order, IDs, or types changed")
        )

    for key in sorted(set(original) | set(candidate)):
        if key == "cells":
            continue
        if original.get(key) == candidate.get(key) and (key in original) == (key in candidate):
            continue
        category = "metadata" if key == "metadata" else "structural" if key in {"nbformat", "nbformat_minor"} else "protected-field"
        violations.append(_violation(category, f"$.{key}", "protected top-level field changed"))

    intended: list[dict[str, Any]] = []
    mask_paths: set[tuple[Any, ...]] = set()
    total_changed_lines = 0
    for index in range(min(len(original_cells), len(candidate_cells))):
        before = original_cells[index]
        after = candidate_cells[index]
        for key in sorted(set(before) | set(after)):
            path = f"$.cells[{index}].{key}"
            if key == "source":
                if before.get(key) == after.get(key) and (key in before) == (key in after):
                    continue
                selector = allowed.get(index)
                if selector is None:
                    violations.append(_violation("unrelated-source", path, "non-allowlisted source changed"))
                    continue
                if type(before.get(key)) is not type(after.get(key)):
                    violations.append(
                        _violation("serialization-locality", path, "source container representation changed")
                    )
                    continue
                before_text = _source_text(before[key])
                after_text = _source_text(after[key])
                changed_lines = _changed_line_count(before_text, after_text)
                total_changed_lines += changed_lines
                if changed_lines > selector["max_changed_lines"]:
                    violations.append(
                        _violation("serialization-locality", path, "source edit exceeds its changed-line limit")
                    )
                if selector["edit_kind"] == "markdown" and before.get("cell_type") != "markdown":
                    violations.append(_violation("protected-field", path, "markdown edit targets a non-Markdown cell"))
                if selector["edit_kind"] == "python-comments-docstrings":
                    try:
                        before_ast = _python_semantics(before_text)
                        after_ast = _python_semantics(after_text)
                    except SyntaxError:
                        violations.append(_violation("parseability", path, "Python source does not parse"))
                    else:
                        if before_ast != after_ast:
                            violations.append(
                                _violation("protected-field", path, "Python executable AST changed")
                            )
                intended.append(
                    {
                        "cell_id": before.get("id"),
                        "cell_index": index,
                        "changed_lines": changed_lines,
                        "edit_kind": selector["edit_kind"],
                    }
                )
                mask_paths.add(("cells", index, "source"))
                continue
            if before.get(key) == after.get(key) and (key in before) == (key in after):
                continue
            category = {
                "attachments": "attachment",
                "execution_count": "execution-count",
                "metadata": "metadata",
                "outputs": "output",
            }.get(key, "structural" if key in {"cell_type", "id"} else "protected-field")
            violations.append(_violation(category, path, "protected cell field changed"))

    locality = contract.get("locality", {})
    maximum_total = locality.get("max_changed_lines_total")
    if not isinstance(maximum_total, int) or isinstance(maximum_total, bool) or maximum_total < 0:
        raise InputError("locality.max_changed_lines_total must be a non-negative integer")
    if total_changed_lines > maximum_total:
        violations.append(
            _violation("serialization-locality", "$.cells", "source edits exceed the total changed-line limit")
        )

    try:
        original_spans = _SpanScanner(original_text).scan()
        candidate_spans = _SpanScanner(candidate_text).scan()
        masked_original = _mask_spans(original_text, original_spans, mask_paths)
        masked_candidate = _mask_spans(candidate_text, candidate_spans, mask_paths)
    except (json.JSONDecodeError, ValueError) as exc:
        raise InputError(f"raw JSON span analysis failed: {exc}") from exc
    if masked_original != masked_candidate:
        violations.append(
            _violation(
                "serialization-locality",
                "$",
                "bytes outside intentionally changed source values differ",
            )
        )

    probe_record: dict[str, Any] = {"status": "not-applicable"}
    probe = contract.get("behavior_probe")
    if probe is not None:
        if not isinstance(probe, dict) or "expected_json" not in probe:
            raise InputError("behavior_probe is malformed")
        original_result, original_error = _run_probe(original, probe, label="original")
        candidate_result, candidate_error = _run_probe(candidate, probe, label="candidate")
        expected = probe["expected_json"]
        if original_error or candidate_error:
            message = original_error or candidate_error or "probe failed"
            violations.append(_violation("behavior", "$.behavior_probe", message))
            probe_record = {"status": "fail", "message": message}
        elif original_result != expected or candidate_result != expected or original_result != candidate_result:
            message = "original, candidate, and expected probe results are not identical"
            violations.append(_violation("behavior", "$.behavior_probe", message))
            probe_record = {"status": "fail", "message": message}
        else:
            probe_record = {"status": "pass", "result": expected}

    violations.sort(key=lambda item: (item["category"], item["path"], item["message"]))
    intended.sort(key=lambda item: item["cell_index"])
    return {
        "valid": not violations,
        "policy": contract["policy"],
        "notebook_role": contract["notebook_role"],
        "intended_source_changes": intended,
        "violations": violations,
        "probe": probe_record,
    }


def validate_paths(original: Path, candidate: Path, contract_path: Path) -> dict[str, Any]:
    original_data = original.read_bytes()
    candidate_data = candidate.read_bytes()
    try:
        contract, _ = _parse_json(contract_path.read_bytes(), label="contract")
    except ValueError as exc:
        raise InputError(str(exc)) from exc
    return validate_bytes(original_data, candidate_data, contract)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        result = validate_paths(args.original, args.candidate, args.contract)
    except (InputError, OSError) as exc:
        print(f"VALIDATOR ERROR: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    else:
        print("PASS" if result["valid"] else "FAIL")
        for violation in result["violations"]:
            print(f"{violation['category']}: {violation['path']}: {violation['message']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
