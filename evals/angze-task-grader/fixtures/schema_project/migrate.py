"""Synthetic CSV schema migration."""

import csv
from pathlib import Path


def read_v1(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def migrate_v1_to_v2(source: Path, destination: Path) -> None:
    """Migrate the documented schema without overwriting malformed input."""
    raise NotImplementedError("seeded migration task")
