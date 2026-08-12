"""Neutral CSV parsing and scientific semantics shared by A and B."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parent
DATA_ROOT = EVAL_ROOT / "data"


@dataclass(frozen=True)
class DatasetSpec:
    """Scientific interpretation fixed before either rendering condition."""

    key: str
    filename: str
    series_names: tuple[str, str, str]
    x_label: str
    y_label: str
    reverse_x: bool


@dataclass(frozen=True)
class SeriesData:
    name: str
    x: tuple[float, ...]
    y: tuple[float, ...]


@dataclass(frozen=True)
class Dataset:
    spec: DatasetSpec
    series: tuple[SeriesData, ...]


DATASETS = {
    "ir": DatasetSpec(
        key="ir",
        filename="ir.csv",
        series_names=("PDI-H-COOH", "PDI-Me-COOH", "PDI-OMe-COOH"),
        x_label="Wavenumber",
        y_label="Intensity",
        reverse_x=True,
    ),
    "uv_vis": DatasetSpec(
        key="uv_vis",
        filename="uv_vis.csv",
        series_names=("PDI-Me-COOH", "PDI-OMe-COOH", "PDI-H-COOH"),
        x_label="Wavelength",
        y_label="Absorbance",
        reverse_x=False,
    ),
    "xrd": DatasetSpec(
        key="xrd",
        filename="xrd.csv",
        series_names=("PDI-H-COOH", "PDI-Me-COOH", "PDI-OMe-COOH"),
        x_label="Angle",
        y_label="Intensity",
        reverse_x=False,
    ),
}


def load_dataset(key: str) -> Dataset:
    """Load and validate the three x/y series for one fixture."""

    spec = DATASETS[key]
    path = DATA_ROOT / spec.filename
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    if len(rows) < 3:
        raise ValueError(f"{path} has no numeric data rows")
    compound_headers = tuple(value for value in rows[0] if value.strip())
    if compound_headers != spec.series_names:
        raise ValueError(
            f"{path} compound order {compound_headers!r} does not match "
            f"{spec.series_names!r}"
        )
    if len(rows[1]) != 6:
        raise ValueError(f"{path} must contain three x/y column pairs")

    series: list[SeriesData] = []
    for pair_index, name in enumerate(spec.series_names):
        x_column = 2 * pair_index
        y_column = x_column + 1
        x_values: list[float] = []
        y_values: list[float] = []
        for row_number, row in enumerate(rows[2:], start=3):
            if len(row) != 6:
                raise ValueError(f"{path}:{row_number} has {len(row)} columns, expected 6")
            try:
                x_values.append(float(row[x_column]))
                y_values.append(float(row[y_column]))
            except ValueError as error:
                raise ValueError(f"{path}:{row_number} contains non-numeric data") from error
        series.append(SeriesData(name=name, x=tuple(x_values), y=tuple(y_values)))

    reference_x = series[0].x
    if any(item.x != reference_x for item in series[1:]):
        raise ValueError(f"{path} series do not share the same x coordinates")
    return Dataset(spec=spec, series=tuple(series))


def load_all() -> dict[str, Dataset]:
    """Load all fixtures using the frozen shared scientific interpretation."""

    return {key: load_dataset(key) for key in DATASETS}
