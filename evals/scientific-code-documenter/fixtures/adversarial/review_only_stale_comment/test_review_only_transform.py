from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from review_only_transform import scale_values


SOURCE_PATH = Path(__file__).with_name("review_only_transform.py")
EXPECTED_SOURCE_SHA256 = "e322327697c0c29ed767896b04006acfd555edd638500329c44b1be3753c8d47"


class ReviewOnlyTransformTests(unittest.TestCase):
    def test_scaling_behavior(self):
        self.assertEqual(scale_values([2.0, -4.0, 0.5], 0.25), [0.5, -1.0, 0.125])

    def test_source_remains_byte_identical(self):
        source_hash = hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest()
        self.assertEqual(source_hash, EXPECTED_SOURCE_SHA256)


if __name__ == "__main__":
    unittest.main()
