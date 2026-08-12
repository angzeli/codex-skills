"""Neutral data parsing and scenario semantics for the resistor colour A/B test."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parent
CSV_PATH = EVAL_ROOT.parent / "data" / "resistor_repeats5_20260122_201801.csv"


@dataclass(frozen=True)
class Series:
    identity: str
    source_header: str
    display_label: str
    x: tuple[float, ...]
    y: tuple[float, ...]


@dataclass(frozen=True)
class Dataset:
    x_label: str
    y_label: str
    series: tuple[Series, ...]


@dataclass(frozen=True)
class SeriesView:
    series: Series
    label: str


SERIES_DEFINITIONS = (
    ("S1", "Current_run1 (mA)", "Run 1"),
    ("S2", "Current_run2 (mA)", "Run 2"),
    ("S3", "Current_run3 (mA)", "Run 3"),
    ("S4", "Current_run4 (mA)", "Run 4"),
    ("S5", "Current_run5 (mA)", "Run 5"),
    ("S6", "Current_avg (mA)", "Average"),
)
SUBSET_IDENTITIES = ("S1", "S3", "S5", "S6")
ORDERED_LABELS = tuple(f"Level {index}" for index in range(1, 7))


def load_dataset() -> Dataset:
    """Load the shared voltage domain and six source-ordered current series."""

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    expected_header = ("Voltage (V)",) + tuple(
        source_header for _identity, source_header, _label in SERIES_DEFINITIONS
    )
    if not rows or tuple(rows[0]) != expected_header:
        raise ValueError(f"Unexpected CSV header in {CSV_PATH}")
    if len(rows) < 2 or any(len(row) != 7 for row in rows[1:]):
        raise ValueError(f"{CSV_PATH} must contain seven-column numeric rows")

    try:
        x_values = tuple(float(row[0]) for row in rows[1:])
        y_columns = tuple(
            tuple(float(row[column]) for row in rows[1:])
            for column in range(1, 7)
        )
    except ValueError as error:
        raise ValueError(f"{CSV_PATH} contains non-numeric data") from error

    if any(left >= right for left, right in zip(x_values, x_values[1:])):
        raise ValueError("Voltage values must be strictly increasing")

    series = tuple(
        Series(
            identity=identity,
            source_header=source_header,
            display_label=display_label,
            x=x_values,
            y=y_values,
        )
        for (identity, source_header, display_label), y_values in zip(
            SERIES_DEFINITIONS, y_columns, strict=True
        )
    )
    return Dataset(x_label="Voltage (V)", y_label="Current (mA)", series=series)


def scenario_views(dataset: Dataset, scenario: str) -> tuple[SeriesView, ...]:
    """Return stable source identities and labels for one evaluation scenario."""

    if scenario == "categorical6":
        return tuple(SeriesView(item, item.display_label) for item in dataset.series)
    if scenario == "subset4":
        by_identity = {item.identity: item for item in dataset.series}
        return tuple(
            SeriesView(by_identity[identity], by_identity[identity].display_label)
            for identity in SUBSET_IDENTITIES
        )
    if scenario == "ordered6":
        return tuple(
            SeriesView(item, label)
            for item, label in zip(dataset.series, ORDERED_LABELS, strict=True)
        )
    raise ValueError(f"Unknown scenario: {scenario}")
