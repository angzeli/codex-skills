"""Collect the six rendered PNGs in one local comparison directory."""

from __future__ import annotations

from pathlib import Path
import shutil


EVAL_ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = EVAL_ROOT / "outputs"

COPIES = {
    "A_baseline/ir_A.png": "comparison/ir_A.png",
    "B_skill/ir_B.png": "comparison/ir_B.png",
    "A_baseline/uv_vis_A.png": "comparison/uv_vis_A.png",
    "B_skill/uv_vis_B.png": "comparison/uv_vis_B.png",
    "A_baseline/xrd_A.png": "comparison/xrd_A.png",
    "B_skill/xrd_B.png": "comparison/xrd_B.png",
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
