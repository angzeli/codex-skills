import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from cli import main
from records import parse_records, summary_report


class RecordTests(unittest.TestCase):
    def test_parse_records(self):
        self.assertEqual(parse_records("a,1\nb,2.5\n"), [("a", 1.0), ("b", 2.5)])

    def test_summary_report(self):
        self.assertEqual(summary_report("a,1\n\nb,2.5\n"), "records=2 total=3.50")

    def test_cli_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.csv"
            path.write_text("a,1\nb,2.5\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["summary", str(path)]), 0)
        self.assertEqual(output.getvalue(), "records=2 total=3.50\n")


if __name__ == "__main__":
    unittest.main()
