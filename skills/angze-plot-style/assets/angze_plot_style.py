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
from matplotlib.colors import to_hex, to_rgb
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

DEFAULT_COLOUR_CYCLE = [
    "#0072B2",
    "#D55E00",
    "#7A5195",
    "#009E73",
    "#C23B70",
    "#7A8F00",
]
NEUTRAL_COLOUR = "#4D4D4D"

PDI_COLOURS = {
    "PDI-Me-COOH": "#D55E00",
    "PDI-H-COOH": "#0072B2",
    "PDI-OMe-COOH": "#7A5195",
}

SAMPLE_RATE_COLOUR_MAPS = {
    "PDI-Me-COOH": {
        20.0: "#F6D2BD",
        40.0: "#EEAE86",
        60.0: "#E78A55",
        80.0: "#DF6A2B",
        100.0: "#D55E00",
        120.0: "#9B4100",
    },
    "PDI-H-COOH": {
        20.0: "#C5E1F0",
        40.0: "#93C8E1",
        60.0: "#5CAED2",
        80.0: "#2F94C3",
        100.0: "#0072B2",
        120.0: "#005681",
    },
    "PDI-OMe-COOH": {
        20.0: "#D8C9E2",
        40.0: "#BFA6CE",
        60.0: "#A881BC",
        80.0: "#8D63A7",
        100.0: "#7A5195",
        120.0: "#58346F",
    },
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
    "axes.prop_cycle": mpl.cycler(color=DEFAULT_COLOUR_CYCLE),
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


def assign_categorical_colours(
    identities: Sequence[str],
    *,
    user_colours: Mapping[str, object] | None = None,
    project_colours: Mapping[str, object] | None = None,
    established_colours: Mapping[str, object] | None = None,
    neutral_identities: Sequence[str] = (),
) -> dict[str, object]:
    """Assign stable colours while preserving the documented priority order.

    Explicit user assignments outrank project mappings, the PDI registry, and
    established workflow mappings. Neutral identities do not consume a
    categorical slot. More than six unresolved identities requires an explicit
    design decision rather than automatic palette expansion or recycling.
    """

    user = user_colours or {}
    project = project_colours or {}
    established = established_colours or {}
    neutral = set(neutral_identities)
    ordered_identities = tuple(dict.fromkeys(identities))
    assigned: dict[str, object] = {}
    unresolved: list[str] = []

    for identity in ordered_identities:
        if identity in user:
            assigned[identity] = user[identity]
        elif identity in project:
            assigned[identity] = project[identity]
        elif identity in PDI_COLOURS:
            assigned[identity] = PDI_COLOURS[identity]
        elif identity in established:
            assigned[identity] = established[identity]
        elif identity in neutral:
            assigned[identity] = NEUTRAL_COLOUR
        else:
            unresolved.append(identity)

    used_cycle_colours: set[str] = set()
    for colour in assigned.values():
        try:
            used_cycle_colours.add(to_hex(colour, keep_alpha=False).upper())
        except (TypeError, ValueError):
            continue
    available = [
        colour for colour in DEFAULT_COLOUR_CYCLE if colour not in used_cycle_colours
    ]
    if len(unresolved) > len(available):
        raise ValueError(
            "More than six unmapped categorical identities require an explicit "
            "mapping, grouping, faceting, or redundant encoding"
        )
    assigned.update(zip(unresolved, available[: len(unresolved)], strict=True))
    return assigned


_FAMILY_MIX_WEIGHTS = (0.75, 0.55, 0.35, 0.18, 0.0, -0.25)


def _interpolated_mix_weight(position: float) -> float:
    lower = min(int(position), len(_FAMILY_MIX_WEIGHTS) - 1)
    upper = min(lower + 1, len(_FAMILY_MIX_WEIGHTS) - 1)
    fraction = position - lower
    return (
        _FAMILY_MIX_WEIGHTS[lower] * (1.0 - fraction)
        + _FAMILY_MIX_WEIGHTS[upper] * fraction
    )


def generate_colour_family(
    base_colour: object,
    levels: int = 6,
    *,
    anchor_index: int | None = None,
) -> list[str]:
    """Generate a deterministic light-to-dark family from one base colour.

    The six-level default mixes 75%, 55%, 35%, and 18% toward white, uses the
    exact base, then mixes 25% toward black. For another level count, sample the
    same progression. Supply ``anchor_index`` when a natural nominal/reference
    level must remain the exact base colour.
    """

    if levels < 1:
        raise ValueError("levels must be at least 1")
    if anchor_index is not None and not 0 <= anchor_index < levels:
        raise ValueError("anchor_index must identify one generated level")

    base_rgb = to_rgb(base_colour)
    base_hex = to_hex(base_rgb).upper()
    if levels == 1:
        return [base_hex]

    if anchor_index is None:
        weights = [
            _interpolated_mix_weight(index * 5.0 / (levels - 1))
            for index in range(levels)
        ]
    elif levels == 6 and anchor_index == 4:
        weights = list(_FAMILY_MIX_WEIGHTS)
    else:
        weights = []
        for index in range(levels):
            if index < anchor_index:
                weight = 0.75 * (anchor_index - index) / anchor_index
            elif index == anchor_index:
                weight = 0.0
            else:
                darker_steps = levels - 1 - anchor_index
                weight = -0.25 * (index - anchor_index) / darker_steps
            weights.append(weight)

    colours: list[str] = []
    for weight in weights:
        target = (1.0, 1.0, 1.0) if weight >= 0.0 else (0.0, 0.0, 0.0)
        amount = abs(weight)
        mixed = tuple(
            channel * (1.0 - amount) + target_channel * amount
            for channel, target_channel in zip(base_rgb, target, strict=True)
        )
        colours.append(to_hex(mixed).upper())
    return colours


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
