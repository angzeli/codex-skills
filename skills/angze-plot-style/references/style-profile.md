# Canonical style profile

This expands the complete operational contract already present in `SKILL.md`.
It preserves Angze's observed heavy typography and boxed axes; it is not
normalized toward journal defaults. Normal use does not require this reference
or any external style module.

## Base profile

| Role | Canonical setting |
|---|---|
| Font | Arial-first sans serif, then Helvetica, Liberation Sans, DejaVu Sans |
| Math text | STIX Sans; retain Matplotlib's conventional math styling |
| Global font size | unset; use role-specific sizes |
| Axis labels | 22 pt, bold, black |
| Tick labels | 14 pt, bold, black |
| Title capability | 18 pt, bold, black; no title by default |
| Legend text | 10 pt, bold, black |
| Generic annotation | 10 pt bold; 9 pt in compact diagnostics |
| Figure and axes | white |
| Spines | all four visible, black, 1.8 pt |
| Grid | off |
| Major ticks | inward, 1.8 pt wide, 4 pt long; bottom/left on, top/right off |
| Minor ticks | off unless explicitly enabled for the scientific axis |
| Figure size | `(8, 6)` inches |
| Data line | 2.0 pt; no universal alpha |
| General marker | circle, 5.5 pt, filled with series colour, black 0.8 pt edge |
| Scatter | no universal size or alpha |
| Error bars | caps 4 pt; error line and cap thickness 1.4 pt |
| Reference line | neutral black/grey dashed line; choose width by emphasis |
| Legend frame | white face, black edge, opaque |

For a legend, try `upper right`, then `upper center`, then `best` if the data
collide. Keep it inside the axes and omit it when labels are unnecessary.

For colour, preserve explicit user and existing project mappings first. New
unrelated identities use the ordered blue/orange/purple/teal/berry/olive cycle;
controls may use neutral `#4D4D4D`, and ordered values of one identity use a
same-hue family. See [colour-profile.md](colour-profile.md) for the complete
priority hierarchy, frozen PDI families, and deterministic mixing policy.

## Manuscript/final policy

The manuscript profile uses the base visual DNA, but adds output and composition
policy rather than different rcParams:

- leave the title absent unless the task explicitly needs one;
- add only scientifically necessary annotations and legends;
- use `tight_layout()` for a simple figure;
- choose constrained layout at figure creation for dense or multipanel work;
- do not impose universal subplot spacing;
- export PNG and PDF from the same logical stem at 600 dpi;
- use tight bounds and an opaque white background for both formats;
- never emit SVG or another format unless the user explicitly requests it.

## Compact diagnostic override

The diagnostic profile is a coherent smaller-text working style derived from a
named current diagnostic theme. It changes only:

| Role | Diagnostic setting |
|---|---|
| Figure size | `(5.8, 4.4)` inches |
| Axis labels | 13 pt bold |
| Tick labels | 10 pt bold |
| Titles | 14 pt bold, when useful |
| Legends | 9 pt bold |
| Annotations | 9 pt bold |

The boxed axes, white/black ground, grid-off rule, major-tick geometry, and 2.0
pt data-line default remain unchanged. Larger BO diagnostic grids are
dimension-driven exceptions, not another averaged profile.

## Context-controlled values

Keep these choices local to the plot because the evidence does not support one
global value:

- axis limits, physical padding, decimal precision, and scientific notation;
- minor-tick presence and geometry;
- top/right ticks when a particular spectral convention needs them;
- scatter size, scatter edge treatment, and alpha;
- marker shape when it encodes a scientific role;
- reference-line width and annotation placement;
- panel geometry and subplot spacing.

Use quantity or descriptor followed by units in parentheses. Use math text for
chemical formulae and super/subscripts, and direct `°` and `Å` where practical.
Do not impose universal significant figures.

## Matplotlib example

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

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
    "axes.grid": False,
    "axes.linewidth": 1.8,
    "axes.spines.left": True,
    "axes.spines.right": True,
    "axes.spines.bottom": True,
    "axes.spines.top": True,
    "xtick.color": "black",
    "ytick.color": "black",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 1.8,
    "ytick.major.width": 1.8,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.top": False,
    "ytick.right": False,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
}

x = [0, 1, 2, 3]
y = [0.2, 0.8, 1.1, 1.5]
series_colour = "#0072B2"  # First colour for a new unrelated identity.

with mpl.rc_context(rc=ANGZE_RC):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(
        x,
        y,
        color=series_colour,
        linewidth=2.0,
        marker="o",
        markersize=5.5,
        markerfacecolor=series_colour,
        markeredgecolor="black",
        markeredgewidth=0.8,
        label="Measured response",
    )
    ax.set_xlabel("Time (min)", fontsize=22, fontweight="bold")
    ax.set_ylabel(r"Response (a.u.)", fontsize=22, fontweight="bold")
    # ax.set_title("Time-dependent response", fontsize=18, fontweight="bold")

    ax.set_facecolor("white")
    ax.grid(False, which="both")
    ax.minorticks_off()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.8)
    ax.tick_params(
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
    for label in (*ax.get_xticklabels(), *ax.get_yticklabels()):
        label.set_fontweight("bold")

    legend = ax.legend(loc="upper right", fontsize=10, frameon=True)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_alpha(1.0)
    for label in legend.get_texts():
        label.set_fontweight("bold")

    fig.tight_layout()
    stem = Path("time_dependent_response")
    save_options = {
        "bbox_inches": "tight",
        "facecolor": "white",
        "edgecolor": "white",
        "transparent": False,
    }
    fig.savefig(stem.with_suffix(".png"), dpi=600, **save_options)
    fig.savefig(stem.with_suffix(".pdf"), **save_options)
    plt.close(fig)
```

The example is deliberately self-contained. For several figures in one script,
factor the repeated axes and legend statements into a small local helper. The
bundled `assets/angze_plot_style.py` remains an optional executable reference
for skill maintenance or deliberate repository-local adoption; it is not a
runtime dependency of generated plotting code.
