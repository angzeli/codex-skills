"""Synthetic review-only fixture with an unsupported unit claim."""

from __future__ import annotations

from collections.abc import Sequence


def scale_values(values: Sequence[float], factor: float) -> list[float]:
    # Convert nanoseconds to seconds for downstream analysis.
    return [value * factor for value in values]
