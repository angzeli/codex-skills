from pathlib import Path
import sys
import tomllib
import unittest


sys.path.insert(0, str(Path("src").resolve()))
import tiny_release  # noqa: E402


class ReleaseTests(unittest.TestCase):
    def test_version_identity_is_synchronized(self):
        metadata = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(metadata["project"]["version"], "0.1.1rc1")
        self.assertEqual(tiny_release.__version__, "0.1.1rc1")
        self.assertEqual(tiny_release.identity(), "tiny-release 0.1.1rc1")

    def test_local_checklist_is_complete(self):
        checklist = Path("RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertNotIn("- [ ]", checklist)
        self.assertIn("No publication, tag, or network action was performed.", checklist)


if __name__ == "__main__":
    unittest.main()
