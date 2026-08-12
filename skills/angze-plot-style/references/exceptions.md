# Exceptions and context boundaries

Apply the base as stable visual DNA, then yield to scientific meaning where the
following contexts require it.

## Scientific axes

- Set limits and padding from the measurement or model. Spectra may invert an
  axis, remove horizontal margins, or use specialized locator/formatter logic.
- Enable minor ticks only when they improve a quantitative axis. Their width and
  length are not canonical; set them explicitly in the calling figure.
- Enable top/right ticks only for a deliberate domain convention. Retain all
  four spines unless the plot itself is a specialized montage or schematic.
- Choose decimals, significant figures, and scientific notation from the data's
  precision. No global formatter is part of the skill.

## Composition and layout

- Use the base `(8, 6)` standalone figure unless the task requires panels.
- For dense or multipanel figures, choose dimensions from panel count and use
  constrained layout. Do not inherit the tiny montage typography automatically.
- Do not encode a broad presentation profile. A presentation figure should be a
  deliberate task-specific override until independent evidence supports one.
- Titles are useful in diagnostics and tutorials, but remain absent by default
  in final manuscript figures.

## Marks and colour

- Use `data_line_kwargs()` for the general filled circular PDI-derived marker.
- Use `experimental_errorbar_kwargs()` for PDI-like time-course means with
  uncertainty, `dense_marker_kwargs()` for dense traces, and
  `open_marker_kwargs()` for an explicitly open/control role.
- Choose stars, triangles, squares, diamonds, or other shapes only when they
  encode a scientific distinction. Do not use them as decorative variation.
- Keep scatter size, scatter alpha, and highlight geometry local to the figure.
- Use `PDI_COLOURS` only for exact `PDI-Me-COOH`, `PDI-H-COOH`, and
  `PDI-OMe-COOH` identities. Do not treat the registry as a universal palette.
- Reference lines are neutral and dashed when scientifically appropriate, but
  their width depends on emphasis.

## Legends and annotations

- Omit a legend when direct labels or a single series make it redundant.
- Keep legends inside the axes. Try upper right, then upper center, then `best`
  after checking collision with the data.
- Annotation position, arrows, and bounding boxes are context-specific. Use the
  bold 9–10 pt typography without imposing a universal placement.

## Export

- Final output is paired PNG/PDF by default. A user may request only one of
  those two formats.
- SVG, TIFF, transparent vector output, and 300 dpi are historical or
  task-specific exceptions, not defaults. Use them only on explicit request.

## Non-canonical mined contexts

Do not let these outliers redefine the skill: tiny montage text, 14 × 5 tutorial
canvases, 11 × 8.5 report pages, finance grids at 160 dpi, near-default quantum
chemistry utility plots, ASE tutorial styling, copied tutorial plots,
hidden-spine montages, XPS transparent-vector export, and the single XPS
presentation theme.
