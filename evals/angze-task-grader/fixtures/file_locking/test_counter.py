import inspect
import multiprocessing
from pathlib import Path
import tempfile
import unittest

import counter


def run_increments(path_text: str, count: int) -> None:
    path = Path(path_text)
    for _ in range(count):
        counter.increment(path)


class CounterTests(unittest.TestCase):
    def test_critical_section_uses_a_file_lock(self):
        self.assertIn("flock", inspect.getsource(counter.increment))

    def test_concurrent_updates_are_not_lost(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "counter.txt"
            path.write_text("0", encoding="utf-8")
            workers = [multiprocessing.Process(target=run_increments, args=(str(path), 8)) for _ in range(4)]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(timeout=10)
                self.assertEqual(worker.exitcode, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), "32")


if __name__ == "__main__":
    unittest.main()
