"""Synthetic baseline fixture for documentation and readability evaluation."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable, Sequence


def transform(x, y, ref, threshold=0.073):
    if len(x) != len(y) or len(y) != len(ref):
        raise ValueError("length mismatch")
    if len(x) < 3:
        raise ValueError("not enough points")
    vals = []
    for i in range(len(y)):
        if ref[i] <= 0 or y[i] <= 0:
            raise ValueError("bad intensity")
        v = -math.log10(y[i] / ref[i])
        if abs(v) < threshold:
            v = 0.0
        vals.append(v)
    base = (vals[0] + vals[1] + vals[2]) / 3.0
    vals = [v - base for v in vals]
    return [(x[i] * 1e-9, vals[i]) for i in range(len(x))]


def rows_to_text(rows):
    out = ["wavelength_m,corrected_absorbance"]
    for x, y in rows:
        out.append(f"{x:.12e},{y:.9f}")
    return "\n".join(out) + "\n"


def write_results(path, rows):
    Path(path).write_text(rows_to_text(rows), encoding="utf-8")


def load_csv(path):
    xs = []
    ys = []
    refs = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            xs.append(float(row["wavelength_nm"]))
            ys.append(float(row["sample_counts"]))
            refs.append(float(row["reference_counts"]))
    return xs, ys, refs


def ascii_plot(rows: Sequence[tuple[float, float]], width: int = 20) -> str:
    biggest = max(abs(value) for _, value in rows) or 1.0
    lines = []
    for location, value in rows:
        count = round(abs(value) / biggest * width)
        direction = "+" if value >= 0 else "-"
        lines.append(f"{location:.3e} {direction}{'#' * count}")
    return "\n".join(lines)


def process_file(source, destination):
    x, y, ref = load_csv(source)
    rows = transform(x, y, ref)
    write_results(destination, rows)
    return ascii_plot(rows)


def mean_signal(values: Iterable[float]) -> float:
    collected = list(values)
    if not collected:
        raise ValueError("empty values")
    return sum(collected) / len(collected)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()
    print(process_file(args.source, args.destination))
