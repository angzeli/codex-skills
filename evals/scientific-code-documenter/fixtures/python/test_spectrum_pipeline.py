from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from spectrum_pipeline import ascii_plot, process_file, rows_to_text, transform


class SpectrumPipelineTests(unittest.TestCase):
    def setUp(self):
        self.wavelength = [400.0, 500.0, 600.0, 700.0]
        self.sample = [80.0, 50.0, 25.0, 10.0]
        self.reference = [100.0, 100.0, 100.0, 100.0]

    def test_transform_preserves_protected_numerical_output(self):
        rows = transform(self.wavelength, self.sample, self.reference)

        expected_wavelengths = [4e-7, 5e-7, 6e-7, 7e-7]
        for (actual, _), wanted in zip(rows, expected_wavelengths):
            self.assertAlmostEqual(actual, wanted, places=18)
        expected = [-0.236423320, -0.032303338, 0.268726658, 0.666666667]
        for (_, actual), wanted in zip(rows, expected):
            self.assertAlmostEqual(actual, wanted, places=8)

    def test_values_below_threshold_are_zeroed(self):
        sample = [100.0, 100.0, 10 ** -0.072 * 100.0]
        rows = transform([400.0, 500.0, 600.0], sample, [100.0] * 3)
        self.assertEqual([value for _, value in rows], [0.0, 0.0, 0.0])

    def test_values_above_threshold_are_retained(self):
        sample = [100.0, 100.0, 10 ** -0.074 * 100.0]
        rows = transform([400.0, 500.0, 600.0], sample, [100.0] * 3)
        self.assertAlmostEqual(rows[-1][1], 0.074 - 0.074 / 3, places=12)

    def test_rejects_shape_and_domain_errors(self):
        with self.assertRaisesRegex(ValueError, "length mismatch"):
            transform([1.0], [1.0, 2.0], [1.0])
        with self.assertRaisesRegex(ValueError, "bad intensity"):
            transform([1.0, 2.0, 3.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0])

    def test_serialization_and_ascii_plot_are_stable(self):
        rows = [(4e-7, -0.25), (5e-7, 0.5)]
        self.assertEqual(
            rows_to_text(rows),
            "wavelength_m,corrected_absorbance\n4.000000000000e-07,-0.250000000\n5.000000000000e-07,0.500000000\n",
        )
        self.assertEqual(ascii_plot(rows, width=4), "4.000e-07 -##\n5.000e-07 +####")

    def test_process_file_keeps_cli_file_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir, "input.csv")
            destination = Path(temp_dir, "output.csv")
            source.write_text(
                "wavelength_nm,sample_counts,reference_counts\n"
                "400,80,100\n500,50,100\n600,25,100\n700,10,100\n",
                encoding="utf-8",
            )
            plot = process_file(source, destination)
            self.assertTrue(destination.read_text(encoding="utf-8").startswith("wavelength_m,"))
            self.assertEqual(len(plot.splitlines()), 4)


if __name__ == "__main__":
    unittest.main()
