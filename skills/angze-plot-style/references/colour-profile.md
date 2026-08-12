# Colour profile

This reference expands the operational colour contract in `SKILL.md`. The
skill remains sufficient for ordinary categorical selection without loading
this file.

## Priority and stable assignment

Resolve an identity in this order:

1. Preserve any explicit current user colour, palette, mapping, or order exactly.
2. Preserve a deliberate mapping already established by the project or task.
3. Apply an exact built-in semantic mapping, such as the PDI registry.
4. Reuse the identity mapping already established in the current workflow.
5. Assign a new unrelated identity from the ordered default cycle.
6. Use neutral grey for a scientifically appropriate control/reference role.

The canonical cycle is blue `#0072B2`, orange `#D55E00`, purple `#7A5195`,
teal `#009E73`, berry `#C23B70`, then olive `#7A8F00`. New categories `A–D`
therefore receive the first four; `A–F` receive all six. If a later plot shows
only `A, C, E, F`, retain blue, purple, berry, and olive. Colour follows identity,
not the number or order of visible series.

An explicit assignment always wins, including over semantic mappings. If the
user sets `A = #123456`, retain that exact value while assigning only the
unspecified identities normally. If the user requests green for `PDI-H-COOH`,
use green for that task rather than the built-in blue.

Use neutral `#4D4D4D` for a control, reference, literature benchmark, baseline,
or neutral comparison where appropriate. It does not consume the next cycle
slot and is not a seventh categorical colour. Black remains the canonical axes,
text, and spine colour.

## Exact PDI identities and rate families

The semantic identity mapping is fixed unless the user overrides it:

```python
PDI_COLOURS = {
    "PDI-Me-COOH": "#D55E00",
    "PDI-H-COOH": "#0072B2",
    "PDI-OMe-COOH": "#7A5195",
}
```

Use these frozen rate families only for the exact PDI identities and rate
levels shown:

```python
SAMPLE_RATE_COLOUR_MAPS = {
    "PDI-Me-COOH": {
        20.0: "#F6D2BD", 40.0: "#EEAE86", 60.0: "#E78A55",
        80.0: "#DF6A2B", 100.0: "#D55E00", 120.0: "#9B4100",
    },
    "PDI-H-COOH": {
        20.0: "#C5E1F0", 40.0: "#93C8E1", 60.0: "#5CAED2",
        80.0: "#2F94C3", 100.0: "#0072B2", 120.0: "#005681",
    },
    "PDI-OMe-COOH": {
        20.0: "#D8C9E2", 40.0: "#BFA6CE", 60.0: "#A881BC",
        80.0: "#8D63A7", 100.0: "#7A5195", 120.0: "#58346F",
    },
}
```

Each 100-level anchor is the exact semantic base. Lower levels become lighter;
120 is darker. Do not generalize these exact shades to unrelated identities.

## Generic ordered families

When ordered scalar values belong to one non-PDI identity, generate a task-local
same-hue family from its assigned base. For six levels, mix RGB colour values as
follows; percentages are colour mixing, never transparency:

| Level | Transformation |
|---|---|
| 1 | base mixed 75% toward white |
| 2 | base mixed 55% toward white |
| 3 | base mixed 35% toward white |
| 4 | base mixed 18% toward white |
| 5 | exact base colour |
| 6 | base mixed 25% toward black |

For another number of levels, interpolate monotonically across the same
light-to-dark progression. Preserve the exact base at a natural nominal or
reference level when one exists; otherwise sample the full progression. Do not
switch hue or use alpha over a white background.

Generated families remain task-local. Freeze one into this skill only after a
separate explicit approval or repeated intentional adoption; do not precompute
six families of six shades.

## Crowded categorical comparisons

With more than six unrelated unmapped categories, do not extend the cycle,
switch palettes, use rainbow/jet, or recycle hues ambiguously. Consider grouping,
faceting, separate standalone figures, direct labels, or scientifically
meaningful line/marker redundancy. Introduce more hues only when genuinely
required or explicitly supplied by the user.
