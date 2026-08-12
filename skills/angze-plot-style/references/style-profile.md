# Canonical style profile

This is the Phase-2 operational specification. It preserves Angze's observed
heavy typography and boxed axes; it is not normalized toward journal defaults.

## Base profile

| Role | Canonical setting |
|---|---|
| Font | Arial-first sans serif, then Helvetica, Liberation Sans, DejaVu Sans |
| Math text | STIX Sans, regular math default |
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

import matplotlib.pyplot as plt

from angze_plot_style import (
    PDI_COLOURS,
    angze_plot_context,
    data_line_kwargs,
    save_figure_bundle,
    style_axes,
    style_legend,
)

with angze_plot_context("manuscript"):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(
        x,
        y,
        label="PDI-H-COOH",
        **data_line_kwargs(PDI_COLOURS["PDI-H-COOH"]),
    )
    ax.set_xlabel("Time (min)")
    ax.set_ylabel(r"Concentration ($\mathrm{mmol\,L^{-1}}$)")
    # ax.set_title("Time-dependent response")
    style_axes(ax, profile="manuscript")
    style_legend(ax.legend(loc="upper right"), profile="manuscript")
    fig.tight_layout()
    save_figure_bundle(fig, Path("time_dependent_response"))
    plt.close(fig)
```

Add the skill's `assets/` directory to `sys.path`, or copy/import the module in
the consuming project according to that project's packaging convention.
