"""Synthetic release package."""

__version__ = "0.1.0"


def identity() -> str:
    return f"tiny-release {__version__}"
