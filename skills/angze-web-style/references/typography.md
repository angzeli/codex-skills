# Typography

Use the typography variant selected by the page's information task. Source keys
refer to the ledger in [design-system.md](design-system.md).

## Technical / mapped typography

Use the mono system when labels, stages, tools, and aligned evidence must read as
one technical architecture. `[W-CSS]`

```css
--font-mono: "IBM Plex Mono", SFMono-Regular, "SF Mono", Menlo, Monaco,
  Consolas, "Liberation Mono", monospace;
```

The source does not load a webfont. Keep this fallback stack unless the target
already supplies IBM Plex Mono deliberately; do not add a font service merely
to force the first face.

| Role | Extracted contract | Evidence selector |
|---|---|---|
| body | `15px`, `1.68`, `0.01em` tracking | `body` |
| hero title | `clamp(3.5rem, 6.5vw, 4.5rem)`, 500, `0.98`, `-0.055em`, uppercase, max `18ch` | `.hero h1` |
| hero subtitle | `clamp(0.96rem, 1.7vw, 1.08rem)`, `1.75`, max `760px` | `.hero-subtitle` |
| eyebrow | `0.66rem`, 700, `0.145em`, uppercase | `.eyebrow` plus shared label rule |
| stage/section labels | `0.72rem`, 700, `0.145em`, `1.45`, uppercase | grouped label selectors |
| section title | `clamp(1.8rem, 3.2vw, 2.65rem)`, 500, `-0.04em`, `1.16`, uppercase | `.section-intro h2` |
| branch title | `clamp(1.4rem, 2.5vw, 1.8rem)`, 600, `-0.025em`, uppercase | `.column-heading h3` |
| stage title | `clamp(1.45rem, 2.5vw, 1.75rem)`, 600, `-0.025em`, uppercase | `.stage-title` |
| application name | `clamp(2rem, 3.1vw, 2.125rem)`, 650, `-0.035em`, uppercase | `.app-name` |
| tool name | `clamp(1.25rem, 2vw, 1.42rem)`, 600, `-0.02em` | `.tool-name` |
| node purpose | `0.92rem`, `1.58`, muted | `.node-purpose` |
| compact detail | `0.88rem`, `1.52`, muted | `.detail-list` |

Use uppercase and tracking for taxonomy, sequence, and application identities;
use sentence case and longer leading for explanation. Keep purpose text quieter
than tool names and stage labels. `[W-CSS] [W-HTML]`

At 700px, reduce body text to `14px`; at 460px, cap key titles with the source's
explicit `.hero h1`, `.section-intro h2`, `.stage-title`, and `.app-name`
overrides. Do not scale every text role uniformly. `[W-CSS: responsive blocks]`

## Editorial / reading typography

Use a CJK-aware serif for identity, titles, and prose; use the system sans stack
for navigation, metadata, controls, captions, and archive labels. `[B-CSS]`

```css
--font-serif: "Songti TC", "Songti SC", "STSongti-TC-Regular", "STSong",
  "PMingLiU", "MingLiU", serif;
--font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

| Role | Extracted contract | Evidence selector |
|---|---|---|
| body | `18px`, `1.9`, `0.02em`, serif | `body` |
| site identity | `1.04rem`, 500, `0.06em`, serif | `.site-mark` |
| navigation | `0.92rem`, `0.04em`, sans | `.site-nav` |
| hero label | `0.68rem`, 650, `0.18em`, uppercase, sans | `.archive-label`, `.section-kicker` |
| home title | `clamp(3.3rem, 11vw, 8.6rem)`, 500, `1.05`, max `11ch` | `.home-hero h1` |
| home subtitle | `clamp(1.08rem, 2vw, 1.34rem)`, `1.8`, max `680px` | `.home-subtitle` |
| section title | `clamp(1.8rem, 5vw, 3rem)`, 500, `1.2` | `.section-heading h2` |
| page title | `clamp(2.35rem, 7vw, 4.8rem)`, 500, `1.2` | `.page-header h1` |
| post title | `clamp(2.55rem, 7vw, 5rem)`, `1.12`, max `9em` | `.post-title` |
| post body | `clamp(1.03rem, 2vw, 1.12rem)` within the 720px shell | `.post-content`, `.post-shell` |
| metadata | `0.76rem`, `0.08em`, `1.5`, uppercase, sans | `.post-meta` |
| caption | `0.86rem`, `0.02em`, `1.7`, centered, sans | `figcaption` |

Keep weight restrained—typically 500 for major serif headings. Create hierarchy
through scale, measure, color role, and whitespace instead of heavy bold text.
Use manual no-wrap title lines only when content metadata explicitly supplies
them; the default title remains naturally wrapping. `[B-HTML: post layout]`

At 700px, reduce the body to `16px` with `1.85` line-height and remove restrictive
title widths. `[B-CSS: responsive block]`

## Combination rule

Do not set editorial prose in the workflow mono face or technical stage maps in
the archive serif merely to make a page look more unified. If a narrative page
contains a technical map, keep the editorial shell and give the map a locally
scoped technical type system. The scope boundary must follow a semantic region,
not an arbitrary mix of headings.
