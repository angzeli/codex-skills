---
name: angze-plot-style
description: Apply Angze's evidence-backed Matplotlib scientific plotting conventions. Use when creating, restyling, reviewing, or exporting Python scientific figures for Angze, including manuscript/final figures, compact diagnostics, PDI compound comparisons, and plot-style decisions.
---

# Angze Plot Style

Generate ordinary, self-contained Matplotlib code in Angze's established
plotting language. Treat this skill as the runtime specification: normal output
must not import, copy, install, or add a path for the bundled Python helper.

## Usage model

1. Identify the figure context before styling:
   - `base`: stable visual DNA for ordinary scientific plots.
   - `manuscript`: base DNA plus title-free, selective-legend, paired-export policy.
   - `diagnostic`: compact typography for working figures.
2. Write self-contained Matplotlib. For several related figures in one script,
   define a small local `style_axes(ax)` helper rather than depending on a
   personal external module.
3. Prefer one standalone `(8, 6)` scientific figure per logical result rather
   than combining unrelated plots into one giant panel. Use panels when the
   scientific comparison genuinely requires them.

## Base contract

Use `figsize=(8, 6)`, a white ground, black foreground, Arial-first sans serif,
and STIX Sans math. Apply at least these rcParams; do not set a global
`font.size` or force `mathtext.default`:

```python
{
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
```

For every ordinary axes:

- keep all four spines visible, black, and 1.8 pt wide;
- disable both major and minor grids, then call `ax.minorticks_off()`;
- use inward major ticks 1.8 pt wide and 4 pt long, with bottom/left ticks on
  and top/right ticks off while retaining their spines;
- make every tick label 14 pt bold;
- use 22 pt bold axis labels and 10 pt bold annotations;
- draw data lines at 2.0 pt;
- use the general marker `"o"`, 5.5 pt, filled with the series colour, with a
  black 0.8 pt edge;
- leave scatter size, scatter alpha, and semantic marker shapes task-specific.

Support an 18 pt bold title but do not display one by default. In reusable
plotting code, provide a convenient commented line:

```python
# ax.set_title("...", fontsize=18, fontweight="bold")
```

## Legend, layout, and export

Add a legend only when it communicates scientific information. Make it 10 pt
bold with an opaque white frame and black edge, keep it inside the axes, and try
`upper right`, then `upper center`, then `best` when collision requires it. Do
not default to an outside legend.

Use `fig.tight_layout()` for an ordinary figure. Use constrained layout for a
genuinely dense or multipanel composition; do not impose universal subplot
spacing.

For final output, save only `<stem>.png` and `<stem>.pdf` by default. Save the
PNG at 600 dpi and both with `bbox_inches="tight"`, `facecolor="white"`, and
`transparent=False`. Do not emit SVG, EPS, TIFF, JPEG, or another format unless
the user explicitly requests it.

## Context and optional resources

Use quantity or descriptor plus units in parentheses; keep axis limits,
scientific notation, decimal precision, significant figures, physical padding,
annotation placement, scatter geometry, and reference-line width specific to
the science. Use the exact PDI registry only for those identities:
`PDI-Me-COOH: #D55E00`, `PDI-H-COOH: #0072B2`, and
`PDI-OMe-COOH: #7A5195`.

Use the compact diagnostic override only for working figures: `(5.8, 4.4)`,
13 pt bold labels, 10 pt bold ticks, 14 pt bold titles, and 9 pt bold legends
and annotations. Retain the base axes geometry.

Consult [references/style-profile.md](references/style-profile.md) for expanded
detail and a self-contained example. Consult
[references/exceptions.md](references/exceptions.md) only when spectra, dense
panels, diagnostics, or another special context may justify an override.
Consult [references/style-evidence.md](references/style-evidence.md) for
provenance or future conflict review; explicit user decisions there override
later mining until the user changes them.

Treat [assets/angze_plot_style.py](assets/angze_plot_style.py) only as an
optional reference implementation, executable specification, and validation
fixture. Reuse it only when the user explicitly asks, a repository already
vendors it deliberately, or the task is maintaining this skill.
