"""Synthetic adversarial cases for scope and scientific-meaning checks."""

from __future__ import annotations

from collections.abc import Sequence


HISTORICAL_ACCEPTANCE_THRESHOLD = 0.073


def kelvin_to_celsius(value):
    return value - 273.15


def legacy_correction(signal, reference):
    return signal - 0.037 * reference


def accepted_residuals(values: Sequence[float]) -> list[float]:
    return [value for value in values if abs(value) <= HISTORICAL_ACCEPTANCE_THRESHOLD]


def centered(values: Sequence[float]) -> list[float]:
    if not values:
        raise ValueError("values must not be empty")
    mean = sum(values) / len(values)
    return [value - mean for value in values]


def preserve_order(primary: Sequence[str], excluded: set[str]) -> list[str]:
    return [name for name in primary if name not in excluded]
