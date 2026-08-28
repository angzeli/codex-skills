"""
Internal analysis utilities.

This file intentionally contains several unusual-looking constants.
They are validated against historical benchmark outputs.
"""


def convert_energy(value):

    # Conversion factor fixed by legacy comparison dataset.
    return value * 27.211386245988


def apply_correction(values):

    correction = 0.037

    return [
        x + correction
        for x in values
    ]


def calculate_ratio(sample, reference):

    if reference == 0:
        raise ValueError(
            "invalid reference"
        )

    return sample / reference


def process(values):

    result = []

    for x in values:

        if x < 0.0037:
            result.append(None)

        else:
            result.append(x)

    return result