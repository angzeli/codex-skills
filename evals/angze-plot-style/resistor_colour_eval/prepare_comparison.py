"""Collect the six primary PNGs in one local review directory."""

from __future__ import annotations

from pathlib import Path
import shutil


EVAL_ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = EVAL_ROOT / "outputs"

COPIES = {
    "A_baseline/categorical6_A.png": "comparison/categorical6_A.png",
    "B_skill/categorical6_B.png": "comparison/categorical6_B.png",
    "A_baseline/subset4_A.png": "comparison/subset4_A.png",
    "B_skill/subset4_B.png": "comparison/subset4_B.png",
    "A_baseline/ordered6_A.png": "comparison/ordered6_A.png",
    "B_skill/ordered6_B.png": "comparison/ordered6_B.png",
}


def main() -> None:
    for source_relative, target_relative in COPIES.items():
        source = OUTPUT_ROOT / source_relative
        target = OUTPUT_ROOT / target_relative
        if not source.is_file():
            raise FileNotFoundError(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


if __name__ == "__main__":
    main()
