"""Render Condition B from angze-plot-style/SKILL.md only."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import matplotlib as mpl
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


ANGZE_RC = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "legend.facecolor": "white",
    "legend.edgecolor": "black",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "mathtext.fontset": "stixsans",
    "text.color": "black",
    "axes.edgecolor": "black",
    "axes.labelcolor": "black",
    "axes.labelsize": 22,
    "axes.labelweight": "bold",
    "axes.titlesize": 18,
    "axes.titleweight": "bold",
    "axes.linewidth": 1.8,
    "axes.grid": False,
    "axes.spines.left": True,
    "axes.spines.right": True,
    "axes.spines.bottom": True,
    "axes.spines.top": True,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "xtick.color": "black",
    "ytick.color": "black",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 1.8,
    "ytick.major.width": 1.8,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.bottom": True,
    "ytick.left": True,
    "xtick.top": False,
    "ytick.right": False,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
    "lines.linewidth": 2.0,
    "legend.fontsize": 10,
    "legend.frameon": True,
    "legend.framealpha": 1.0,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.edgecolor": "white",
    "savefig.transparent": False,
}

PDI_COLOURS = {
    "PDI-Me-COOH": "#D55E00",
    "PDI-H-COOH": "#0072B2",
    "PDI-OMe-COOH": "#7A5195",
}


def style_axes(axis) -> None:
    """Apply the SKILL.md axes contract locally within this renderer."""

    axis.figure.patch.set_facecolor("white")
    axis.set_facecolor("white")
    axis.grid(False, which="both")
    axis.minorticks_off()
    for spine in axis.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.8)
    axis.tick_params(
        axis="both",
        which="major",
        direction="in",
        width=1.8,
        length=4,
        colors="black",
        labelsize=14,
        bottom=True,
        left=True,
        top=False,
        right=False,
    )
    for label in (*axis.get_xticklabels(), *axis.get_yticklabels()):
        label.set_fontweight("bold")


def style_legend(legend) -> None:
    """Apply the SKILL.md inside-axes legend contract."""

    legend.set_frame_on(True)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_alpha(1.0)
    for label in legend.get_texts():
        label.set_fontsize(10)
        label.set_fontweight("bold")


def render_dataset(dataset) -> tuple[Path, Path]:
    """Create a standalone treatment figure without external style imports."""

    with mpl.rc_context(rc=ANGZE_RC):
        figure, axis = plt.subplots(figsize=(8, 6))
        for series in dataset.series:
            axis.plot(
                series.x,
                series.y,
                color=PDI_COLOURS[series.name],
                linewidth=2.0,
                label=series.name,
            )

        axis.set_xlabel(dataset.spec.x_label, fontsize=22, fontweight="bold")
        axis.set_ylabel(dataset.spec.y_label, fontsize=22, fontweight="bold")
        # axis.set_title("...", fontsize=18, fontweight="bold")
        if dataset.spec.reverse_x:
            axis.invert_xaxis()
        style_axes(axis)
        legend = axis.legend(loc="upper right", fontsize=10, frameon=True)
        style_legend(legend)
        figure.tight_layout()

        output_dir = EVAL_ROOT / "outputs" / "B_skill"
        output_dir.mkdir(parents=True, exist_ok=True)
        stem = output_dir / f"{dataset.spec.key}_B"
        save_options = {
            "bbox_inches": "tight",
            "facecolor": "white",
            "edgecolor": "white",
            "transparent": False,
        }
        png = stem.with_suffix(".png")
        pdf = stem.with_suffix(".pdf")
        figure.savefig(png, dpi=600, **save_options)
        figure.savefig(pdf, dpi=600, **save_options)
        plt.close(figure)
        return png, pdf


def main() -> None:
    for dataset in common.load_all().values():
        render_dataset(dataset)


if __name__ == "__main__":
    main()
