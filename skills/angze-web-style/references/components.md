# Components and interaction states

Load only the component families present in the requested page. Source keys
refer to [design-system.md](design-system.md).

- [Shared primitives](#shared-primitives)
- [Technical component families](#technical-component-families)
- [Editorial component families](#editorial-component-families)
- [Motion and transitions](#motion-and-transitions)

## Shared primitives

### Theme control

Use two real buttons inside a labeled group, with a separator hidden from the
accessibility tree. Use `data-theme-choice="light|dark"`, update
`aria-pressed`, and mark the active option with `.is-active`. Keep a transparent,
square-edged control with an underline state rather than a pill switch.
`[W-HTML: .theme-toggle]` `[B-HTML: header include]` `[W-CSS] [B-CSS]`

Minimum extracted sizes differ by context:

- technical: option `40px` minimum width, `30px` minimum height, uppercase mono;
- editorial: option `30px` minimum width, `32px` minimum height, system sans.

### Links and focus

- Retain one-pixel underlines with a generous text offset for inline links.
  Hover/focus changes to copper or soft copper. `[W-CSS: a]` `[B-CSS: a]`
- Use a one-pixel copper focus outline with `4px` offset for controls. The
  technical source uses `:focus-visible`; the editorial source also keeps
  link-level `:focus` feedback. `[W-CSS] [B-CSS]`
- Do not remove focus indicators or use color alone to show a pressed theme
  state; the underline and `aria-pressed` remain. `[W-HTML] [B-HTML]`

## Technical component families

### Hero and section intro

Use `.hero-topline` for identity plus theme controls, `.hero-content` for the
main title/subtitle/metadata group, and `.section-intro` for section thesis plus
explanation. Rules, not background decoration, separate these regions.
`[W-HTML] [W-CSS]`

### Stage nodes

Start with `.stage-node`, then add a role modifier proven by the content:

| Role | Extracted treatment | Evidence |
|---|---|---|
| preparation | subtle surface | `.preparation-step` |
| reference | transparent ground, two-pixel strong left rule | `.reference-node` |
| shared abstraction | centered, max `920px`, copper-tinted rule/wash | `.shared-node` |
| validation gate | dashed border, transparent ground | `.gate-node` |
| calculation engine | strong surface and two-pixel top rule | `.engine-node` |
| validated result | subtle surface and two-pixel top rule | `.result-node` |
| scientific output | transparent ground, max `900px` | `.output-node` |

Use `.node-stage` for stage taxonomy, `.stage-title` or `.app-name` for identity,
`.node-purpose` / `.app-purpose` for meaning, and semantic lists or definition
lists for evidence. `[W-HTML] [W-CSS]`

### Evidence grids and lists

Use `.detail-list` for compact evidence with an em-dash pseudo-marker; use the
two-column modifier only when items remain legible. Use `.capability-grid`,
`.production-grid`, or `.method-strategy` only for their matching content shape:
capability groups, production branches, or term/definition method strategy.
`[W-HTML] [W-CSS]`

### Responsive branch selector

Hide `.view-selector` by default. Display it only at the narrow workflow
breakpoint and only under `.js`; without scripting, keep both branches visible.
The three options are `Both`, the first branch, and the second branch, with
pressed state and an `aria-live` status. `[W-HTML] [W-CSS] [W-JS]`

## Editorial component families

### Site identity and navigation

Use `.site-mark` as an unadorned identity link containing the existing mark and
title. Use a short `.site-nav`; do not introduce a large navigation system for a
small archive. The mark is a 24px asset on desktop and 22px below 700px.
`[B-HTML: header include]` `[B-CSS]` `[B-ASSET]`

### Editorial hero

Use `.home-hero` as a bounded editorial field with a paper wash, two-pixel top
rule, one-pixel bottom rule, and subtle inset line. The extracted hero has no
rounded card edge and no drop shadow. `[B-CSS]`

### Actions

Use `.button` with `42px` minimum height, `9px 16px` padding, one-pixel border,
and `4px` radius. Preserve the exact component tokens: `[B-CSS]`

| Token | Day | Night |
|---|---|---|
| `--button-border` | `rgba(185, 111, 69, 0.3)` | `rgba(201, 133, 92, 0.34)` |
| `--button-primary-bg` | `rgba(38, 55, 70, 0.06)` | `rgba(215, 224, 231, 0.08)` |
| `--button-primary-border` | `rgba(38, 55, 70, 0.34)` | `rgba(215, 224, 231, 0.28)` |
| `--button-primary-bg-hover` | `rgba(38, 55, 70, 0.1)` | `rgba(215, 224, 231, 0.12)` |
| `--button-primary-border-hover` | `rgba(38, 55, 70, 0.48)` | `rgba(215, 224, 231, 0.42)` |
| `--button-secondary-bg` | `rgba(185, 111, 69, 0.035)` | `rgba(201, 133, 92, 0.08)` |
| `--button-secondary-text` | `#8f5538` | `#d39a76` |
| `--button-secondary-bg-hover` | `rgba(185, 111, 69, 0.08)` | `rgba(201, 133, 92, 0.13)` |
| `--button-secondary-border-hover` | `rgba(185, 111, 69, 0.42)` | `rgba(201, 133, 92, 0.48)` |
| `--button-secondary-text-hover` | `#824d34` | `#e0aa88` |

Keep primary actions cool-blue and secondary actions copper; do not add filled
brand buttons without a new user decision.

### Lists, metadata, and content

- Use `.post-meta` for category and date, `.post-preview` for latest entries,
  and `.archive-item` for dated archive entries. Fine bottom rules provide the
  grouping. `[B-HTML] [B-CSS]`
- Use `.page-header` / `.post-header` for title and optional subtitle/excerpt,
  followed by `.page-content` / `.post-content`. `[B-HTML] [B-CSS]`
- Use `.category-filter` as compact outlined rounded tags only for real category
  filtering. Do not generalize the `999px` radius to buttons or cards. `[B-CSS]`
- Use `figure`, `img`, and `figcaption` semantically. Keep image radius at
  `0.35rem`; captions remain muted, sans, and centered. `[B-CSS]`

## Motion and transitions

The technical source transitions page background and text for `140ms ease` and
disables meaningful transition/animation duration under
`prefers-reduced-motion: reduce`. It also disables smooth scrolling on narrow
screens. `[W-CSS]` Do not add entrance animations, parallax, or animated card
effects; no source component establishes those behaviors.
