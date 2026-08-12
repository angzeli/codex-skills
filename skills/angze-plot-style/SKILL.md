---
name: angze-plot-style
description: Apply Angze's evidence-backed Matplotlib scientific plotting conventions. Use when creating, restyling, reviewing, or exporting Python scientific figures for Angze, including manuscript/final figures, compact diagnostics, PDI compound comparisons, and plot-style decisions.
---

# Angze Plot Style

Apply Angze's established plotting language rather than a generic journal or
Matplotlib house style.

## Workflow

1. Identify the figure context before styling:
   - `base`: stable visual DNA for ordinary scientific plots.
   - `manuscript`: base DNA plus title-free, selective-legend, paired-export policy.
   - `diagnostic`: compact typography for working figures.
2. Read [references/style-profile.md](references/style-profile.md) for exact
   values and a minimal example.
3. Use [assets/angze_plot_style.py](assets/angze_plot_style.py) rather than
   retyping rcParams when writing Matplotlib code.
4. Apply layout and scientific formatting deliberately. Prefer a standalone
   `(8, 6)` figure; use panels only when the task requires a combined figure.
5. For final output, save PNG and PDF from one stem at 600 dpi with tight bounds
   and an opaque white background. Emit only one of those formats only when the
   user asks.

## Non-negotiable defaults

- Keep all four black 1.8 pt spines visible and keep the grid off.
- Use inward 1.8 pt by 4 pt major ticks on bottom and left only.
- Keep minor ticks off unless the scientific axis needs them.
- Use role-specific bold sizes: labels 22, ticks 14, titles 18, legends 10,
  annotations 9–10. Do not set a canonical global `font.size`.
- Support bold 18 pt titles, but leave the title absent by default. Keep a
  commented `# ax.set_title(...)` line in reusable examples.
- Add a framed, white, black-edged legend only when it carries scientific
  information. Try upper right, then upper center, then `best`, inside the axes.
- Use 2.0 pt data lines. Do not invent a universal scatter size or alpha.
- Use the PDI colour registry only for the exact PDI identities it names.

## Context and evidence

Read [references/exceptions.md](references/exceptions.md) before applying the
base mechanically to spectra, dense panels, diagnostics, or semantic markers.
Read [references/style-evidence.md](references/style-evidence.md) when reviewing
why a rule exists or when new mining evidence conflicts with the encoded style.
Explicit user decisions in that file take precedence over later statistical
re-mining until the user changes them.
