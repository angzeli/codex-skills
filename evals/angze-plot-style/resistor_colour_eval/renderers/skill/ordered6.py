"""Condition B: six ordered levels using a same-hue family from SKILL.md."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


EVAL_ROOT = Path(__file__).resolve().parents[2]
COMMON_SPEC = importlib.util.spec_from_file_location(
    "resistor_colour_eval_common", EVAL_ROOT / "common.py"
)
if COMMON_SPEC is None or COMMON_SPEC.loader is None:
    raise RuntimeError("Could not load shared evaluation semantics")
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
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "lines.linewidth": 2.0,
    "legend.fontsize": 10,
    "legend.frameon": True,
    "legend.framealpha": 1.0,
}


def ordered_colours() -> tuple[object, ...]:
    base_colour = "#0072B2"
    family = LinearSegmentedColormap.from_list(
        "ordered_identity",
        [(0.0, "white"), (0.8, base_colour), (1.0, "black")],
    )
    return tuple(family(position) for position in (0.18, 0.34, 0.50, 0.66, 0.80, 0.94))


def style_axes(axis) -> None:
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
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_alpha(1.0)
    for label in legend.get_texts():
        label.set_fontsize(10)
        label.set_fontweight("bold")


def main() -> None:
    dataset = common.load_dataset()
    views = common.scenario_views(dataset, "ordered6")

    with mpl.rc_context(rc=ANGZE_RC):
        figure, axis = plt.subplots(figsize=(8, 6))
        for view, colour in zip(views, ordered_colours(), strict=True):
            axis.plot(
                view.series.x,
                view.series.y,
                color=colour,
                linewidth=2.0,
                marker="o",
                markersize=5.5,
                markerfacecolor=colour,
                markeredgecolor="black",
                markeredgewidth=0.8,
                label=view.label,
            )
        axis.axhline(
            0.0, color="#4D4D4D", linestyle="--", linewidth=1.2, zorder=0
        )
        axis.set_xlabel(dataset.x_label, fontsize=22, fontweight="bold")
        axis.set_ylabel(dataset.y_label, fontsize=22, fontweight="bold")
        # axis.set_title("...", fontsize=18, fontweight="bold")
        style_axes(axis)
        legend = axis.legend(loc="upper center", ncol=2, frameon=True)
        style_legend(legend)
        figure.tight_layout()

        output_stem = EVAL_ROOT / "outputs" / "B_skill" / "ordered6_B"
        output_stem.parent.mkdir(parents=True, exist_ok=True)
        save_options = {
            "bbox_inches": "tight",
            "facecolor": "white",
            "edgecolor": "white",
            "transparent": False,
        }
        figure.savefig(output_stem.with_suffix(".png"), dpi=600, **save_options)
        figure.savefig(output_stem.with_suffix(".pdf"), dpi=600, **save_options)
        plt.close(figure)


if __name__ == "__main__":
    main()
