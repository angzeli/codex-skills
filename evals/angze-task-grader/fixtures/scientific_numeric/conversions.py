"""Synthetic numerical conversions with one seeded exponent defect."""

EV_TO_JOULE = 1.602176634e19


def ev_to_joule(energy_ev: float) -> float:
    """Convert an energy from electronvolts to joules."""
    return energy_ev * EV_TO_JOULE


def binding_energy(complex_energy: float, fragment_a: float, fragment_b: float) -> float:
    """Return E(complex) - E(fragment A) - E(fragment B)."""
    return complex_energy - fragment_a - fragment_b
