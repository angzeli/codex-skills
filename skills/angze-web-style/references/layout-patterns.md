# Layout and structural patterns

Use these patterns to preserve information order while adapting content. Source
keys refer to [design-system.md](design-system.md).

## Shared shell

- Keep the outer shell at `1120px` maximum with `40px` total horizontal
  subtraction on larger screens and `28px` below 700px. The technical source
  expresses this through `--page-width`; the editorial source uses the literal
  maximum. `[W-CSS: .site-main, .site-footer]` `[B-CSS: shell group]`
- Center shells with `margin-inline: auto` and retain a `min-width: 280px` guard
  on the technical page. `[W-CSS] [B-CSS]`
- Narrow sustained reading and compact output independently of the outer shell.
  The editorial reading shell is `720px`; the technical shared/output nodes are
  `900px` or `920px`. `[W-CSS] [B-CSS]`

## Technical architecture page

Build the page as a semantic sequence. `[W-HTML]`

1. Use one `main` landmark with a skip link and a labeled hero section.
2. Put identity and the theme control in a ruled topline.
3. Pair an uppercase title, quiet subtitle, and compact metadata in the hero.
4. Introduce the architecture with a two-column section heading: thesis on the
   left, explanatory paragraph on the right.
5. Represent parallel evidence branches as paired semantic sections/articles,
   then merge into shared stages only when the content truly converges.
6. Use heading order, lists, definition lists, and asides to encode the evidence
   relationships independently of the CSS connector lines.
7. Finish with validated results, common analysis, and output rather than a
   decorative call-to-action.

Extracted dimensions and grid behavior: `[W-CSS]`

| Pattern | Contract |
|---|---|
| hero | `30px 0 64px`; content begins after a `68px` top offset |
| section intro | columns `1.12fr / 0.88fr`, minimum right column `280px`, `64px` gap |
| parallel branch rows | two equal `minmax(0, 1fr)` columns, `48px` gap |
| stage node | `28px 29px 30px`, `1px` rule, `2px` radius, full row height |
| shared node | max `920px`, `35px 38px 38px`, copper-tinted top emphasis |
| output/shared analysis | max `900px` |
| internal capability grids | usually two equal columns separated by soft rules |

Connectors are structural annotations, not decoration. Use paired, merge, split,
shared, or mini connectors only when the semantic sequence contains that
relationship. Mark purely visual connector elements `aria-hidden="true"`.
`[W-HTML: connector elements]` `[W-CSS: connector selectors]`

### Technical responsive sequence

- At `1000px`, reduce paired gaps and node padding; collapse dense two-column
  detail/foundation grids where needed. `[W-CSS]`
- At `820px`, stack the two workflow branches, flatten merge/split connectors to
  one vertical line, and expose the three-option branch selector only when the
  `.js` enhancement class is present. `[W-CSS] [W-JS]`
- Keep all branches visible without JavaScript. With JavaScript, filter only at
  the narrow breakpoint and announce the visible state through an `aria-live`
  status. `[W-HTML] [W-JS]`
- At `700px`, reduce outer gutters and node padding; at `460px`, collapse dense
  internal grids and companion-tool layouts to one column. `[W-CSS]`

## Editorial archive and portfolio

Build a stable site shell from reusable header, main, and footer landmarks.
`[B-HTML: default layout and includes]`

- Use a header with one identity mark, a short navigation group, and the theme
  control. Keep it horizontally distributed on wide screens and stacked at
  `700px`. `[B-HTML: header include]` `[B-CSS: .site-header]`
- Use the home hero at max `960px`, with `88px auto 78px` outer spacing and
  `70px min(8vw, 78px) 72px` inner spacing. Bound it with a strong top rule and
  quiet bottom rule rather than treating it as a floating card. `[B-CSS]`
- Use max `720px` for latest posts, pages, and posts. Apply `74px 0 84px` to page
  and post shells, and separate the header from content with one rule. `[B-CSS]`
- Represent latest posts as a semantic article list with metadata before title
  and excerpt. Represent archives as a date column plus content column.
  `[B-HTML: home/category layouts]`
- Keep figures in the reading column, use one fine border and small radius on
  images, and place muted sans-serif captions below. `[B-CSS: post content]`
- Keep previous/next navigation after the article and switch it from a row to a
  left-aligned grid below `700px`. `[B-HTML: post layout]` `[B-CSS]`

At `700px`, use `42px 24px` hero padding, stack the site header, remove archive
date columns, and allow titles to use the full width. `[B-CSS: responsive block]`

## Adaptation rules

- Preserve the target framework's native templating and components. Translate
  these semantic patterns instead of replacing Jekyll, static HTML, React, or
  another existing architecture.
- Preserve existing content order unless the task explicitly authorizes
  editorial restructuring.
- Create a new component only when the content has a new semantic role. Do not
  turn every paragraph into a card or every section into a two-column grid.
- Use CSS Grid for aligned evidence relationships and Flexbox for one-dimensional
  navigation, metadata, and action groups, matching the source division.
