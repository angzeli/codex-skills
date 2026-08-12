"""Optional executable reference for Angze's evidence-backed plotting style.

The skill generates self-contained Matplotlib code for normal use. This module
is a reference implementation and validation fixture, not a required runtime
dependency for consuming repositories.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Mapping, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend

DEFAULT_FIGSIZE = (8.0, 6.0)
DIAGNOSTIC_FIGSIZE = (5.8, 4.4)

AXIS_LABEL_SIZE = 22.0
TICK_LABEL_SIZE = 14.0
TITLE_SIZE = 18.0
LEGEND_SIZE = 10.0
ANNOTATION_SIZE = 10.0

DIAGNOSTIC_AXIS_LABEL_SIZE = 13.0
DIAGNOSTIC_TICK_LABEL_SIZE = 10.0
DIAGNOSTIC_TITLE_SIZE = 14.0
DIAGNOSTIC_LEGEND_SIZE = 9.0
DIAGNOSTIC_ANNOTATION_SIZE = 9.0

SPINE_WIDTH = 1.8
MAJOR_TICK_WIDTH = 1.8
MAJOR_TICK_LENGTH = 4.0
DATA_LINE_WIDTH = 2.0

DEFAULT_MARKER = "o"
DEFAULT_MARKER_SIZE = 5.5
DEFAULT_MARKER_EDGE_COLOR = "black"
DEFAULT_MARKER_EDGE_WIDTH = 0.8

ERRORBAR_CAPSIZE = 4.0
ERRORBAR_LINE_WIDTH = 1.4

PDI_COLOURS = {
    "PDI-Me-COOH": "#D55E00",
    "PDI-H-COOH": "#0072B2",
    "PDI-OMe-COOH": "#7A5195",
}

BASE_RCPARAMS: dict[str, object] = {
    "figure.figsize": DEFAULT_FIGSIZE,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "legend.facecolor": "white",
    "legend.edgecolor": "black",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "mathtext.fontset": "stixsans",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "text.color": "black",
    "axes.edgecolor": "black",
    "axes.labelcolor": "black",
    "axes.labelsize": AXIS_LABEL_SIZE,
    "axes.labelweight": "bold",
    "axes.titlesize": TITLE_SIZE,
    "axes.titleweight": "bold",
    "axes.linewidth": SPINE_WIDTH,
    "axes.grid": False,
    "axes.spines.left": True,
    "axes.spines.right": True,
    "axes.spines.bottom": True,
    "axes.spines.top": True,
    "xtick.color": "black",
    "ytick.color": "black",
    "xtick.labelsize": TICK_LABEL_SIZE,
    "ytick.labelsize": TICK_LABEL_SIZE,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": MAJOR_TICK_WIDTH,
    "ytick.major.width": MAJOR_TICK_WIDTH,
    "xtick.major.size": MAJOR_TICK_LENGTH,
    "ytick.major.size": MAJOR_TICK_LENGTH,
    "xtick.bottom": True,
    "ytick.left": True,
    "xtick.top": False,
    "ytick.right": False,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
    "lines.linewidth": DATA_LINE_WIDTH,
    "legend.fontsize": LEGEND_SIZE,
    "legend.frameon": True,
    "legend.fancybox": False,
    "legend.framealpha": 1.0,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.edgecolor": "white",
    "savefig.transparent": False,
}

DIAGNOSTIC_RCPARAM_OVERRIDES: dict[str, object] = {
    "figure.figsize": DIAGNOSTIC_FIGSIZE,
    "axes.labelsize": DIAGNOSTIC_AXIS_LABEL_SIZE,
    "axes.titlesize": DIAGNOSTIC_TITLE_SIZE,
    "xtick.labelsize": DIAGNOSTIC_TICK_LABEL_SIZE,
    "ytick.labelsize": DIAGNOSTIC_TICK_LABEL_SIZE,
    "legend.fontsize": DIAGNOSTIC_LEGEND_SIZE,
}

SUPPORTED_PROFILES = ("base", "manuscript", "diagnostic")


def _validate_profile(profile: str) -> str:
    if profile not in SUPPORTED_PROFILES:
        choices = ", ".join(SUPPORTED_PROFILES)
        raise ValueError(f"Unknown profile {profile!r}; choose one of: {choices}")
    return profile


def rc_params(profile: str = "base") -> dict[str, object]:
    """Return a fresh rcParams mapping for an Angze style profile.

    ``manuscript`` deliberately shares the base rcParams. Its distinct rules
    concern title, legend, layout, and export policy rather than typography.
    """

    _validate_profile(profile)
    params = dict(BASE_RCPARAMS)
    params["font.sans-serif"] = list(BASE_RCPARAMS["font.sans-serif"])
    if profile == "diagnostic":
        params.update(DIAGNOSTIC_RCPARAM_OVERRIDES)
    return params


@contextmanager
def angze_plot_context(
    profile: str = "base",
    *,
    overrides: Mapping[str, object] | None = None,
) -> Iterator[None]:
    """Apply a profile temporarily and restore all global rcParams afterward."""

    params = rc_params(profile)
    if overrides:
        params.update(overrides)
    with mpl.rc_context(rc=params):
        yield


def apply_angze_plot_style(
    profile: str = "base",
    *,
    overrides: Mapping[str, object] | None = None,
) -> None:
    """Apply a profile globally when an explicit persistent change is wanted."""

    params = rc_params(profile)
    if overrides:
        params.update(overrides)
    mpl.rcParams.update(params)


def _profile_typography(profile: str) -> dict[str, float]:
    _validate_profile(profile)
    if profile == "diagnostic":
        return {
            "axis_label": DIAGNOSTIC_AXIS_LABEL_SIZE,
            "tick_label": DIAGNOSTIC_TICK_LABEL_SIZE,
            "title": DIAGNOSTIC_TITLE_SIZE,
            "legend": DIAGNOSTIC_LEGEND_SIZE,
            "annotation": DIAGNOSTIC_ANNOTATION_SIZE,
        }
    return {
        "axis_label": AXIS_LABEL_SIZE,
        "tick_label": TICK_LABEL_SIZE,
        "title": TITLE_SIZE,
        "legend": LEGEND_SIZE,
        "annotation": ANNOTATION_SIZE,
    }


def style_axes(
    ax: Axes,
    *,
    profile: str = "base",
    xlabel: str | None = None,
    ylabel: str | None = None,
    minor_ticks: bool = False,
    top_ticks: bool = False,
    right_ticks: bool = False,
    grid: bool = False,
) -> Axes:
    """Apply boxed axes and role-specific typography to one axes object."""

    sizes = _profile_typography(profile)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    ax.figure.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(grid, which="both")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(SPINE_WIDTH)

    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        width=MAJOR_TICK_WIDTH,
        length=MAJOR_TICK_LENGTH,
        colors="black",
        labelsize=sizes["tick_label"],
        bottom=True,
        left=True,
        top=top_ticks,
        right=right_ticks,
    )
    if minor_ticks:
        ax.minorticks_on()
        ax.tick_params(
            axis="both",
            which="minor",
            direction="in",
            colors="black",
            bottom=True,
            left=True,
            top=top_ticks,
            right=right_ticks,
        )
    else:
        ax.minorticks_off()
        ax.tick_params(
            axis="both",
            which="minor",
            bottom=False,
            left=False,
            top=False,
            right=False,
        )

    for label in (ax.xaxis.label, ax.yaxis.label):
        label.set_color("black")
        label.set_fontsize(sizes["axis_label"])
        label.set_fontweight("bold")
    for label in (*ax.get_xticklabels(), *ax.get_yticklabels()):
        label.set_fontweight("bold")
    for offset_text in (ax.xaxis.get_offset_text(), ax.yaxis.get_offset_text()):
        offset_text.set_color("black")
        offset_text.set_fontsize(sizes["tick_label"])
        offset_text.set_fontweight("bold")
    title_artists = (
        ax.title,
        getattr(ax, "_left_title", None),
        getattr(ax, "_right_title", None),
    )
    for title in title_artists:
        if title is not None and title.get_text():
            title.set_color("black")
            title.set_fontsize(sizes["title"])
            title.set_fontweight("bold")
    return ax


def style_legend(legend: Legend | None, *, profile: str = "base") -> Legend | None:
    """Style an existing legend; return ``None`` unchanged when absent."""

    if legend is None:
        return None
    sizes = _profile_typography(profile)
    legend.set_frame_on(True)
    frame = legend.get_frame()
    frame.set_facecolor("white")
    frame.set_edgecolor("black")
    frame.set_linewidth(1.0)
    frame.set_alpha(1.0)
    for label in legend.get_texts():
        label.set_color("black")
        label.set_fontsize(sizes["legend"])
        label.set_fontweight("bold")
    return legend


def data_line_kwargs(color: str | None = None, **overrides: object) -> dict[str, object]:
    """Return the general line and PDI-derived filled-circle marker geometry."""

    values: dict[str, object] = {
        "linewidth": DATA_LINE_WIDTH,
        "marker": DEFAULT_MARKER,
        "markersize": DEFAULT_MARKER_SIZE,
        "markeredgecolor": DEFAULT_MARKER_EDGE_COLOR,
        "markeredgewidth": DEFAULT_MARKER_EDGE_WIDTH,
    }
    if color is not None:
        values.update(color=color, markerfacecolor=color)
    values.update(overrides)
    return values


def experimental_errorbar_kwargs(
    color: str | None = None,
    **overrides: object,
) -> dict[str, object]:
    """Return the PDI time-course error-bar role with filled, white-edged points."""

    values: dict[str, object] = {
        "linewidth": DATA_LINE_WIDTH,
        "marker": "o",
        "markersize": 6.5,
        "markeredgecolor": "white",
        "markeredgewidth": 0.7,
        "capsize": ERRORBAR_CAPSIZE,
        "elinewidth": ERRORBAR_LINE_WIDTH,
        "capthick": ERRORBAR_LINE_WIDTH,
    }
    if color is not None:
        values.update(color=color, markerfacecolor=color)
    values.update(overrides)
    return values


def dense_marker_kwargs(color: str | None = None, **overrides: object) -> dict[str, object]:
    """Return the compact circular marker used for dense electrochemical traces."""

    values: dict[str, object] = {
        "linestyle": "none",
        "marker": "o",
        "markersize": 4.5,
        "markeredgecolor": "white",
        "markeredgewidth": 0.45,
    }
    if color is not None:
        values.update(color=color, markerfacecolor=color)
    values.update(overrides)
    return values


def open_marker_kwargs(color: str, **overrides: object) -> dict[str, object]:
    """Return the open-circle role used for explicitly distinct/control series."""

    values: dict[str, object] = {
        "linestyle": "none",
        "color": color,
        "marker": "o",
        "markersize": 7.0,
        "markerfacecolor": "white",
        "markeredgecolor": color,
        "markeredgewidth": 1.8,
    }
    values.update(overrides)
    return values


@contextmanager
def create_figure(
    *,
    profile: str = "base",
    figsize: tuple[float, float] | None = None,
    constrained_layout: bool = False,
    **subplot_kwargs: object,
) -> Iterator[tuple[Figure, Axes]]:
    """Create one styled axes while isolating the profile's global rcParams."""

    _validate_profile(profile)
    default_size = DIAGNOSTIC_FIGSIZE if profile == "diagnostic" else DEFAULT_FIGSIZE
    with angze_plot_context(profile):
        fig, ax = plt.subplots(
            figsize=figsize or default_size,
            constrained_layout=constrained_layout,
            **subplot_kwargs,
        )
        style_axes(ax, profile=profile)
        yield fig, ax


def save_figure_bundle(
    figure: Figure,
    path_without_suffix: str | Path,
    *,
    formats: Sequence[str] = ("png", "pdf"),
    dpi: int = 600,
) -> tuple[Path, ...]:
    """Save PNG/PDF outputs from one stem with tight, opaque white bounds."""

    stem = Path(path_without_suffix)
    if stem.suffix:
        raise ValueError("path_without_suffix must be a logical stem without an extension")
    normalized: list[str] = []
    for item in formats:
        file_format = str(item).lower().lstrip(".")
        if file_format not in {"png", "pdf"}:
            raise ValueError("formats may contain only 'png' and 'pdf'")
        if file_format not in normalized:
            normalized.append(file_format)
    if not normalized:
        raise ValueError("formats must contain at least one of 'png' or 'pdf'")

    stem.parent.mkdir(parents=True, exist_ok=True)
    common: dict[str, object] = {
        "bbox_inches": "tight",
        "facecolor": "white",
        "edgecolor": "white",
        "transparent": False,
    }
    outputs: list[Path] = []
    for file_format in normalized:
        output = stem.with_suffix(f".{file_format}")
        kwargs = dict(common)
        kwargs["dpi"] = dpi
        figure.savefig(output, format=file_format, **kwargs)
        outputs.append(output)
    return tuple(outputs)
