import contextlib
import io
import unittest

from tiny_cli import main, render_greetings


class TinyCliTests(unittest.TestCase):
    def test_default_count(self):
        self.assertEqual(render_greetings("Ada", 1), ["hello Ada"])

    def test_zero_count(self):
        self.assertEqual(render_greetings("Ada", 0), [])

    def test_cli_zero_is_silent(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["Ada", "--count", "0"]), 0)
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
