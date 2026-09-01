import csv
from pathlib import Path
import tempfile
import unittest

from migrate import migrate_v1_to_v2, read_v1


class MigrationTests(unittest.TestCase):
    def test_read_v1_remains_supported(self):
        rows = read_v1(Path("data_v1.csv"))
        self.assertEqual(rows[0], {"label": "alpha", "value": "-1.25"})

    def test_migration_preserves_rows_and_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "data_v2.csv"
            migrate_v1_to_v2(Path("data_v1.csv"), destination)
            with destination.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(
            rows,
            [
                {"sample_id": "row-001", "label": "alpha", "value_ev": "-1.25"},
                {"sample_id": "row-002", "label": "beta", "value_ev": "2.50"},
            ],
        )

    def test_malformed_source_does_not_touch_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "bad.csv"
            destination = Path(tmp) / "output.csv"
            source.write_text("label,value\nalpha\n", encoding="utf-8")
            destination.write_text("keep me\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                migrate_v1_to_v2(source, destination)
            self.assertEqual(destination.read_text(encoding="utf-8"), "keep me\n")


if __name__ == "__main__":
    unittest.main()
