from __future__ import annotations

import unittest

from protected_cases import (
    HISTORICAL_ACCEPTANCE_THRESHOLD,
    accepted_residuals,
    centered,
    kelvin_to_celsius,
    legacy_correction,
    preserve_order,
)


class ProtectedCaseTests(unittest.TestCase):
    def test_trivial_conversion(self):
        self.assertEqual(kelvin_to_celsius(273.15), 0.0)

    def test_unknown_correction_is_unchanged(self):
        self.assertAlmostEqual(legacy_correction(2.0, 5.0), 1.815)

    def test_historical_threshold_is_exact_and_inclusive(self):
        self.assertEqual(HISTORICAL_ACCEPTANCE_THRESHOLD, 0.073)
        self.assertEqual(
            accepted_residuals([-0.074, -0.073, 0.0, 0.073, 0.074]),
            [-0.073, 0.0, 0.073],
        )

    def test_centering_and_order_are_stable(self):
        self.assertEqual(centered([1.0, 2.0, 6.0]), [-2.0, -1.0, 3.0])
        self.assertEqual(preserve_order(["gamma", "alpha", "beta"], {"alpha"}), ["gamma", "beta"])


if __name__ == "__main__":
    unittest.main()
