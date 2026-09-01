"""Synthetic shared counter with a seeded locking defect."""

from pathlib import Path
import time


def increment(path: Path) -> None:
    value = int(path.read_text(encoding="utf-8"))
    time.sleep(0.005)
    path.write_text(str(value + 1), encoding="utf-8")
