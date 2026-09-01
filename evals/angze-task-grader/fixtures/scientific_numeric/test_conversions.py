import math
import unittest

from conversions import EV_TO_JOULE, binding_energy, ev_to_joule


class ConversionTests(unittest.TestCase):
    def test_documented_constant(self):
        self.assertEqual(EV_TO_JOULE, 1.602176634e-19)

    def test_one_electronvolt(self):
        self.assertTrue(math.isclose(ev_to_joule(1.0), 1.602176634e-19, rel_tol=1e-15))

    def test_sign_is_preserved(self):
        self.assertLess(ev_to_joule(-2.0), 0.0)

    def test_binding_energy_convention_is_unchanged(self):
        self.assertEqual(binding_energy(-12.0, -5.0, -6.0), -1.0)


if __name__ == "__main__":
    unittest.main()
