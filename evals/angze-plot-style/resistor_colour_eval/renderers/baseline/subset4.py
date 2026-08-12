"""Condition A: non-contiguous four-series subset."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import matplotlib.pyplot as plt


EVAL_ROOT = Path(__file__).resolve().parents[2]
COMMON_SPEC = importlib.util.spec_from_file_location(
    "resistor_colour_eval_common", EVAL_ROOT / "common.py"
)
if COMMON_SPEC is None or COMMON_SPEC.loader is None:
    raise RuntimeError("Could not load shared evaluation semantics")
common = importlib.util.module_from_spec(COMMON_SPEC)
sys.modules[COMMON_SPEC.name] = common
COMMON_SPEC.loader.exec_module(common)


def main() -> None:
    dataset = common.load_dataset()
    views = common.scenario_views(dataset, "subset4")

    figure, axis = plt.subplots(figsize=(7.2, 4.8))
    for view in views:
        axis.plot(
            view.series.x,
            view.series.y,
            linewidth=1.5,
            marker="o",
            markersize=3.5,
            label=view.label,
        )
    axis.axhline(0.0, color="0.4", linestyle="--", linewidth=1.0, zorder=0)
    axis.set_xlabel(dataset.x_label)
    axis.set_ylabel(dataset.y_label)
    axis.legend(loc="best", frameon=False, ncol=2)
    figure.tight_layout()

    output = EVAL_ROOT / "outputs" / "A_baseline" / "subset4_A.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
