"""Render Condition A with ordinary Matplotlib and no plotting skill."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import matplotlib.pyplot as plt


EVAL_ROOT = Path(__file__).resolve().parents[2]
COMMON_SPEC = importlib.util.spec_from_file_location(
    "angze_plot_eval_common",
    EVAL_ROOT / "common.py",
)
if COMMON_SPEC is None or COMMON_SPEC.loader is None:
    raise RuntimeError("Could not load the neutral evaluation semantics")
common = importlib.util.module_from_spec(COMMON_SPEC)
sys.modules[COMMON_SPEC.name] = common
COMMON_SPEC.loader.exec_module(common)


def render_dataset(dataset) -> Path:
    """Create a clear standalone research figure using baseline judgment."""

    figure, axis = plt.subplots(figsize=(7.2, 4.6))
    for series in dataset.series:
        axis.plot(series.x, series.y, linewidth=1.4, label=series.name)

    axis.set_xlabel(dataset.spec.x_label)
    axis.set_ylabel(dataset.spec.y_label)
    if dataset.spec.reverse_x:
        axis.invert_xaxis()
    axis.legend(loc="best", frameon=False)
    figure.tight_layout()

    output_dir = EVAL_ROOT / "outputs" / "A_baseline"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{dataset.spec.key}_A.png"
    figure.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(figure)
    return output


def main() -> None:
    for dataset in common.load_all().values():
        render_dataset(dataset)


if __name__ == "__main__":
    main()
