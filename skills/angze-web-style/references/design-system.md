# Design system and provenance

Use this file to select exact color and surface roles. Do not normalize the two
source variants into one token set: their relationships are shared, but several
Day values intentionally differ.

- [Source ledger](#source-ledger)
- [Shared visual grammar](#shared-visual-grammar)
- [Core palette correspondence](#core-palette-correspondence)
- [Technical token contract](#technical-token-contract)
- [Editorial token contract](#editorial-token-contract)
- [Asset boundary](#asset-boundary)

## Source ledger

- `[W-CSS]` `computational-modelling-workflow/docs/website/assets/css/workflow.css`
- `[W-HTML]` `computational-modelling-workflow/docs/website/index.html`
- `[W-JS]` `computational-modelling-workflow/docs/website/assets/js/workflow.js`
- `[B-CSS]` `blogger/assets/css/style.css`
- `[B-HTML]` `blogger/_layouts/*.html` and `blogger/_includes/*.html`
- `[B-JS]` `blogger/assets/js/theme-toggle.js`
- `[B-ASSET]` `blogger/assets/logo-mark.svg` and `blogger/assets/favicon.svg`

The CSS files are authoritative for values and responsive rules. HTML proves
structural use; JavaScript proves interaction behavior; SVG proves only the
existing mark treatment. Source keys below identify the inspected evidence.

## Shared visual grammar

Observed in both variants:

- Pair a warm Day ground with cool dark text and a blue-black Night ground with
  warm light text. `[W-CSS: :root, theme overrides]` `[B-CSS: :root, theme overrides]`
- Use copper for labels, active states, and editorial emphasis; do not flood
  large surfaces with it. `[W-CSS: --accent, label selectors]`
  `[B-CSS: --copper, metadata and state selectors]`
- Separate hierarchy with one-pixel rules, occasional two-pixel emphasis, and
  surface changes before using depth effects. `[W-CSS: section and node rules]`
  `[B-CSS: header, hero, list, and content rules]`
- Keep the outer content measure at 1120px and narrow prose-heavy regions
  further. `[W-CSS: --page-width]` `[B-CSS: shell widths]`
- Express Day/Night changes through custom properties rather than duplicate
  component rules. `[W-CSS: theme blocks]` `[B-CSS: theme blocks]`

Inferred principle: the identity comes from warm/cool contrast, disciplined
hierarchy, and sparse emphasis—not from making every page share one font or one
card layout.

## Core palette correspondence

These are extracted values, not replacement recommendations.

| Role | Technical Day / Night | Editorial Day / Night | Evidence |
|---|---|---|---|
| page ground | `--canvas: #f2efe8 / #11181d` | `--paper: #f5efe4 / #11181d` | `[W-CSS] [B-CSS]` |
| defined soft surface | `--surface: #f8f5ef / #172027` | `--paper-soft: #f8f1e7 / #172027` (currently unused) | `[W-CSS] [B-CSS]` |
| body text | `--text: #292d2f / #e8dfd1` | `--ink: #1f2528 / #e8dfd1` | `[W-CSS] [B-CSS]` |
| cool heading text | `--text-cool: #263746 / #d7e0e7` | `--night-blue: #263746 / #d7e0e7` | `[W-CSS] [B-CSS]` |
| muted text | `--muted: #686967 / #a99f92` | `--muted: #6f7477 / #a99f92` | `[W-CSS] [B-CSS]` |
| base rule | `--line: #c9c2b8 / #34424b` | `--line: #d6c8b8 / #34424b` | `[W-CSS] [B-CSS]` |
| copper accent | `--accent: #b96f45 / #c9855c` | `--copper: #b96f45 / #c9855c` | `[W-CSS] [B-CSS]` |
| soft copper | `--accent-soft: #a65f3c / #d0936d` | `--copper-soft: #a76643 / #d0936d` | `[W-CSS] [B-CSS]` |

Preserve the selected variant's exact Day values. Do not “correct” the small
differences between the technical and editorial systems.

## Technical token contract

Use the workflow token names for process maps, research architecture, and dense
technical documentation. `[W-CSS: lines beginning at :root]`

| Token | Day | Night | Role |
|---|---|---|---|
| `--canvas` | `#f2efe8` | `#11181d` | page ground |
| `--surface` | `#f8f5ef` | `#172027` | ordinary stage node |
| `--surface-strong` | `#ece8df` | `#1b252c` | calculation/engine emphasis |
| `--surface-subtle` | `#eeebe4` | `#141c21` | preparation/result support |
| `--text` | `#292d2f` | `#e8dfd1` | body copy |
| `--text-cool` | `#263746` | `#d7e0e7` | headings and primary names |
| `--muted` | `#686967` | `#a99f92` | supporting explanation |
| `--muted-cool` | `#62717a` | `#9aa8b0` | metadata and stage labels |
| `--line` | `#c9c2b8` | `#34424b` | ordinary rules |
| `--line-soft` | `rgba(187, 178, 166, 0.72)` | `rgba(52, 66, 75, 0.7)` | internal rules |
| `--rule-strong` | `rgba(38, 55, 70, 0.58)` | `rgba(215, 224, 231, 0.5)` | two-pixel structural emphasis |
| `--accent` | `#b96f45` | `#c9855c` | semantic emphasis |
| `--accent-soft` | `#a65f3c` | `#d0936d` | active/large accent text |
| `--accent-faint` | `rgba(185, 111, 69, 0.055)` | `rgba(201, 133, 92, 0.075)` | shared-node wash |

Keep `--page-width: 1120px`. Keep the extracted mono stack documented in
[typography.md](typography.md). The source is dark-first: unqualified `:root`
contains Night values, a light system preference applies Day values only when
`data-theme` is absent, and explicit `html[data-theme]` blocks win.

## Editorial token contract

Use the archive token names for portfolios, essays, posts, and narrative project
pages. `[B-CSS: :root and theme overrides]`

Core roles are in the correspondence table. Preserve these exact supporting
tokens:

| Token | Day | Night |
|---|---|---|
| `--paper-wash-start` | `rgba(248, 241, 231, 0.76)` | `rgba(23, 32, 39, 0.78)` |
| `--paper-wash-end` | `rgba(245, 239, 228, 0)` | `rgba(17, 24, 29, 0)` |
| `--link-underline` | `rgba(185, 111, 69, 0.46)` | `rgba(201, 133, 92, 0.58)` |
| `--header-line` | `rgba(214, 200, 184, 0.58)` | `rgba(52, 66, 75, 0.72)` |
| `--nav-ink` | `rgba(38, 55, 70, 0.74)` | `rgba(215, 224, 231, 0.72)` |
| `--footer-line` | `rgba(216, 202, 187, 0.64)` | `rgba(52, 66, 75, 0.72)` |
| `--hero-wash-start` | `rgba(248, 241, 231, 0.48)` | `rgba(23, 32, 39, 0.62)` |
| `--hero-wash-end` | `rgba(245, 239, 228, 0.16)` | `rgba(17, 24, 29, 0.24)` |
| `--hero-rule` | `rgba(38, 55, 70, 0.76)` | `rgba(215, 224, 231, 0.56)` |
| `--hero-line` | `rgba(214, 200, 184, 0.68)` | `rgba(52, 66, 75, 0.74)` |
| `--hero-inset` | `rgba(255, 255, 255, 0.28)` | `rgba(232, 223, 209, 0.08)` |
| `--section-line` | `rgba(214, 200, 184, 0.76)` | `rgba(52, 66, 75, 0.78)` |
| `--item-line` | `rgba(216, 202, 187, 0.84)` | `rgba(52, 66, 75, 0.7)` |
| `--theme-toggle-rule` | `rgba(216, 202, 187, 0.72)` | `rgba(52, 66, 75, 0.84)` |
| `--theme-toggle-hover` | `rgba(185, 111, 69, 0.16)` | `rgba(201, 133, 92, 0.18)` |

Button values are component-specific; load [components.md](components.md) when
buttons are present. `--paper-soft` and `--shadow` are defined in the source but
not consumed by current selectors. Do not infer an active card-shadow or
secondary-surface rule from those unused declarations.

The editorial source is light-first, with a dark system-preference override and
explicit `html[data-theme="light"]` / `html[data-theme="dark"]` blocks. Preserve
that order when modifying the existing archive; either source ordering is valid
for a new page if its cascade and no-script fallback remain equivalent.

## Asset boundary

The editorial SVG mark uses the same cool/copper Day pair and switches its mark
colors through `prefers-color-scheme`. `[B-ASSET]` Reuse it only when the target
is the same writing identity or the user asks for that mark. Do not treat the
shape as a universal logo or redraw a new logo from the palette.
