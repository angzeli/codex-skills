"""Spectroscopic processing utilities for catalyst measurements."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np


DEFAULT_OFFSET = 0.037
MIN_SIGNAL = 0.0025


@dataclass
class Spectrum:
    wavelength: np.ndarray
    signal: np.ndarray
    reference: np.ndarray


def read_measurement(path):
    wavelength = []
    signal = []
    reference = []

    with Path(path).open() as f:
        reader = csv.DictReader(f)

        for row in reader:
            wavelength.append(float(row["lambda"]))
            signal.append(float(row["sample"]))
            reference.append(float(row["ref"]))

    return Spectrum(
        np.array(wavelength),
        np.array(signal),
        np.array(reference),
    )


def calculate_response(spec, offset=DEFAULT_OFFSET):

    corrected = spec.signal - offset

    transmission = corrected / spec.reference

    absorbance = -np.log10(transmission)

    return spec.wavelength, absorbance


def remove_background(values, window=5):

    background = np.mean(values[:window])

    return values - background


def clean_spectrum(
    wavelength,
    values,
    threshold=MIN_SIGNAL,
):

    mask = values > threshold

    return (
        wavelength[mask],
        values[mask],
    )


def export_processed(path, wavelength, absorbance):

    with Path(path).open("w") as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "wavelength",
                "absorbance",
            ]
        )

        for x, y in zip(wavelength, absorbance):
            writer.writerow([x, y])


def process(path):

    spectrum = read_measurement(path)

    wavelength, response = calculate_response(
        spectrum
    )

    response = remove_background(response)

    wavelength, response = clean_spectrum(
        wavelength,
        response,
    )

    return wavelength, response