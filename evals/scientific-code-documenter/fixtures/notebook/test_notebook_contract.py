from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

import validate_notebook_contract as validator


FIXTURE_ROOT = Path(__file__).resolve().parent


def load_contract(stem: str) -> dict:
    return json.loads((FIXTURE_ROOT / f"{stem}.contract.json").read_text(encoding="utf-8"))


def replace_value(data: bytes, path: tuple, value: object) -> bytes:
    text = data.decode("utf-8")
    spans = validator._SpanScanner(text).scan()
    start, end = spans[path]
    token = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (text[:start] + token + text[end:]).encode("utf-8")


def source_at(data: bytes, index: int) -> str:
    notebook = json.loads(data)
    source = notebook["cells"][index]["source"]
    return source if isinstance(source, str) else "".join(source)


class NotebookContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.editable = (FIXTURE_ROOT / "editable_scientific.ipynb").read_bytes()
        cls.editable_contract = load_contract("editable_scientific")
        cls.review = (FIXTURE_ROOT / "review_only_stale_claim.ipynb").read_bytes()
        cls.review_contract = load_contract("review_only_stale_claim")
        cls.over_commented = (FIXTURE_ROOT / "over_commented.ipynb").read_bytes()
        cls.over_commented_contract = load_contract("over_commented")
        cls.generated = (FIXTURE_ROOT / "generated_pipeline_report.ipynb").read_bytes()
        cls.generated_contract = load_contract("generated_pipeline_report")

    def assert_valid(self, result: dict) -> None:
        self.assertTrue(result["valid"], result["violations"])

    def assert_category(self, result: dict, category: str) -> None:
        categories = {item["category"] for item in result["violations"]}
        self.assertIn(category, categories, result)

    def documented_editable_candidate(self) -> bytes:
        markdown = (
            "# Scaling summary\n\n"
            "The transformation preserves input order and propagates missing values. "
            "The units and scientific meaning of `SCALE_FACTOR` are not documented."
        )
        candidate = replace_value(self.editable, ("cells", 0, "source"), markdown)
        code = source_at(candidate, 1).replace(
            "def notebook_contract_probe():\n",
            "def notebook_contract_probe():\n"
            "    \"\"\"Return ordered transformed values and their stable JSON form.\"\"\"\n"
            "    # Preserve missing values rather than applying the configured scale.\n",
        )
        return replace_value(candidate, ("cells", 1, "source"), code)

    def test_allowlisted_documentation_edit_passes_with_probe(self) -> None:
        result = validator.validate_bytes(
            self.editable,
            self.documented_editable_candidate(),
            self.editable_contract,
        )
        self.assert_valid(result)
        self.assertEqual(result["probe"]["status"], "pass")
        self.assertEqual(
            [item["cell_id"] for item in result["intended_source_changes"]],
            ["contract-overview", "transform-records"],
        )

    def test_comment_pruning_passes(self) -> None:
        markdown = "# Summary\n\nMissing values are omitted and the remaining values are sorted in ascending order."
        candidate = replace_value(self.over_commented, ("cells", 0, "source"), markdown)
        code = "".join(
            line
            for line in source_at(candidate, 1).splitlines(keepends=True)
            if not line.lstrip().startswith("#")
        )
        candidate = replace_value(candidate, ("cells", 1, "source"), code)
        result = validator.validate_bytes(
            self.over_commented,
            candidate,
            self.over_commented_contract,
        )
        self.assert_valid(result)

    def test_review_only_copy_is_byte_identical(self) -> None:
        self.assert_valid(
            validator.validate_bytes(self.review, self.review, self.review_contract)
        )

    def test_generated_copy_is_byte_identical(self) -> None:
        self.assert_valid(
            validator.validate_bytes(self.generated, self.generated, self.generated_contract)
        )

    def test_review_only_change_fails(self) -> None:
        candidate = self.review.replace(b"Signal preparation", b"Signal processing")
        result = validator.validate_bytes(self.review, candidate, self.review_contract)
        self.assert_category(result, "serialization-locality")

    def test_malformed_candidate_fails_closed(self) -> None:
        result = validator.validate_bytes(self.editable, b"{", self.editable_contract)
        self.assert_category(result, "parseability")

    def test_duplicate_candidate_key_fails_closed(self) -> None:
        candidate = self.editable.replace(
            b'"nbformat": 4,', b'"nbformat": 4,\n "nbformat": 4,', 1
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "parseability")

    def test_nonstandard_json_constant_fails_closed(self) -> None:
        candidate = self.editable.replace(
            b'"nbformat": 4,', b'"extension": NaN,\n "nbformat": 4,', 1
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "parseability")

    def test_top_level_format_change_is_structural(self) -> None:
        candidate = replace_value(self.editable, ("nbformat_minor",), 4)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "structural")

    def test_notebook_metadata_change_fails(self) -> None:
        candidate = replace_value(
            self.editable,
            ("metadata", "data_contract", "ordering"),
            "sorted order",
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "metadata")

    def test_cell_identifier_change_is_structural(self) -> None:
        candidate = replace_value(self.editable, ("cells", 1, "id"), "renamed")
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "structural")

    def test_cell_type_change_is_structural(self) -> None:
        candidate = replace_value(self.editable, ("cells", 3, "cell_type"), "markdown")
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "structural")

    def test_cell_order_change_is_structural(self) -> None:
        notebook = json.loads(self.editable)
        notebook["cells"][2], notebook["cells"][3] = notebook["cells"][3], notebook["cells"][2]
        candidate = replace_value(self.editable, ("cells",), notebook["cells"])
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "structural")

    def test_cell_count_change_is_structural(self) -> None:
        notebook = json.loads(self.editable)
        candidate = replace_value(self.editable, ("cells",), notebook["cells"][:-1])
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "structural")

    def test_cell_metadata_change_fails(self) -> None:
        candidate = replace_value(self.editable, ("cells", 1, "metadata", "collapsed"), True)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "metadata")

    def test_execution_count_change_fails(self) -> None:
        candidate = replace_value(self.editable, ("cells", 1, "execution_count"), 8)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "execution-count")

    def test_output_change_fails(self) -> None:
        candidate = replace_value(
            self.editable,
            ("cells", 1, "outputs", 0, "execution_count"),
            8,
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "output")

    def test_attachment_change_fails(self) -> None:
        candidate = replace_value(
            self.editable,
            ("cells", 2, "attachments", "scale-note.txt", "text/plain"),
            "changed",
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "attachment")

    def test_unknown_top_level_extension_is_protected(self) -> None:
        candidate = self.editable.replace(
            b' "nbformat": 4,', b' "custom_extension": {"enabled":true},\n "nbformat": 4,', 1
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "protected-field")

    def test_nonallowlisted_source_change_fails(self) -> None:
        candidate = replace_value(
            self.editable,
            ("cells", 2, "source"),
            "This unlisted cell changed.",
        )
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "unrelated-source")

    def test_source_container_representation_change_fails(self) -> None:
        source = source_at(self.editable, 0)
        candidate = replace_value(self.editable, ("cells", 0, "source"), [source])
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "serialization-locality")

    def test_whole_notebook_reserialization_fails_locality(self) -> None:
        candidate = json.dumps(json.loads(self.editable), separators=(",", ":")).encode("utf-8")
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "serialization-locality")

    def test_unchanged_source_with_different_escape_fails_locality(self) -> None:
        original_token = b'"# Scaling summary\\n\\nThe ordered records are transformed below."'
        replacement = b'"# Scaling summary\\u000a\\u000aThe ordered records are transformed below."'
        candidate = self.editable.replace(original_token, replacement, 1)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "serialization-locality")

    def test_source_edit_line_budget_is_enforced(self) -> None:
        markdown = source_at(self.editable, 0) + "\n" + "\n".join(f"extra {i}" for i in range(20))
        candidate = replace_value(self.editable, ("cells", 0, "source"), markdown)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "serialization-locality")

    def test_numerical_change_fails_ast_and_probe(self) -> None:
        code = source_at(self.editable, 1).replace("value * SCALE_FACTOR", "value + SCALE_FACTOR")
        candidate = replace_value(self.editable, ("cells", 1, "source"), code)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "protected-field")
        self.assert_category(result, "behavior")

    def test_call_order_change_fails_ast(self) -> None:
        code = source_at(self.editable, 1).replace(
            "json.dumps(rows, separators=(\",\", \":\"))",
            "json.dumps(rows, separators=(\",\", \":\"), sort_keys=True)",
        )
        candidate = replace_value(self.editable, ("cells", 1, "source"), code)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "protected-field")

    def test_probe_exception_fails(self) -> None:
        code = source_at(self.editable, 1).replace(
            "def notebook_contract_probe():\n",
            "def notebook_contract_probe():\n    raise RuntimeError(\"synthetic\")\n",
        )
        candidate = replace_value(self.editable, ("cells", 1, "source"), code)
        result = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_category(result, "behavior")

    def test_probe_timeout_fails(self) -> None:
        contract = copy.deepcopy(self.editable_contract)
        contract["behavior_probe"]["timeout_seconds"] = 0.1
        code = source_at(self.editable, 1).replace(
            "def notebook_contract_probe():\n",
            "def notebook_contract_probe():\n    while True:\n        pass\n",
        )
        candidate = replace_value(self.editable, ("cells", 1, "source"), code)
        result = validator.validate_bytes(self.editable, candidate, contract)
        self.assert_category(result, "behavior")

    def test_stale_original_hash_is_an_input_error(self) -> None:
        contract = copy.deepcopy(self.editable_contract)
        contract["original_sha256"] = "0" * 64
        with self.assertRaises(validator.InputError):
            validator.validate_bytes(self.editable, self.editable, contract)

    def test_stale_selector_is_an_input_error(self) -> None:
        contract = copy.deepcopy(self.editable_contract)
        contract["allowed_source_changes"][0]["cell_id"] = "stale-id"
        with self.assertRaises(validator.InputError):
            validator.validate_bytes(self.editable, self.editable, contract)

    def test_second_pass_byte_identity_is_enforced(self) -> None:
        candidate = self.documented_editable_candidate()
        first = validator.validate_bytes(self.editable, candidate, self.editable_contract)
        self.assert_valid(first)
        second_pass_contract = {
            "schema_version": 1,
            "original_sha256": hashlib.sha256(candidate).hexdigest(),
            "notebook_role": "source",
            "policy": "byte-identical",
            "allowed_source_changes": [],
        }
        second = validator.validate_bytes(candidate, candidate, second_pass_contract)
        self.assert_valid(second)


if __name__ == "__main__":
    unittest.main()
