---
name: angze-web-style
description: Apply Angze's evidence-backed personal web design system. Use when creating, modifying, reviewing, or refactoring HTML/CSS websites for Angze, including research sites, technical documentation, portfolios, personal writing archives, responsive layouts, and Day/Night theme support, or when a request mentions angze-web-style or matching Angze's existing websites.
---

# Angze Web Style

Reproduce the design language encoded in Angze's own websites. Treat the
existing implementations as evidence, preserve their information architecture,
and adapt their patterns to the page's purpose instead of applying a generic
visual preset.

## Work from evidence

1. Inspect the target site's HTML, CSS, assets, and behavior before editing.
2. Classify the page as technical/mapped, editorial/reading, or a deliberate
   combination with clearly separated regions.
3. Preserve the target's content, framework, routing, and accessibility
   contract unless the request changes them.
4. Reuse the matching source pattern and its token relationships. Do not invent
   a replacement palette, type system, spacing scale, component library, or
   theme mechanism for convenience.
5. Check the finished page at desktop and narrow widths, in Day and Night modes,
   with keyboard navigation.

## Preserve the design philosophy

- Make information hierarchy carry the design. Use typography, rules, spacing,
  and alignment before decoration.
- Give technical evidence a visible sequence: context, stage, purpose, detail,
  validation, and output.
- Give editorial prose a quiet reading measure with metadata subordinate to the
  title and body.
- Use the copper accent as a sparse semantic signal, not as ambient decoration.
- Prefer flat surfaces, fine rules, restrained state changes, and generous
  whitespace over ornamental cards, strong shadows, gradients without a source
  role, or motion-heavy interaction.
- Keep semantic HTML primary. Use JavaScript only for progressive enhancement,
  persisted theme choice, or a content-driven responsive control.

## Choose the appropriate variant

### Technical or mapped pages

Use the mono-led workflow language for research architecture, scientific
documentation, process maps, evidence pipelines, and pages whose structure is
the main explanatory device. Build semantic sections and articles, align
parallel branches with grids, and distinguish stages through labels, rules,
surface roles, and connectors.

### Editorial or reading pages

Use the serif-led archive language for portfolios, essays, posts, project
narratives, and pages optimized for sustained reading. Use a quiet site shell,
a bounded hero or page header, compact sans-serif metadata, narrow reading
columns, chronological lists, and restrained actions.

### Combined pages

Do not average the variants into an arbitrary hybrid. Let the page's dominant
purpose select the shell, then use the other variant only for a semantically
distinct region such as a technical evidence map within an editorial project
page.

## Implementation contract

- Use semantic landmarks, heading order, labeled navigation, real buttons for
  controls, visible focus states, and accessible state attributes.
- Define theme colors through custom properties. Keep component rules token
  based so Day and Night modes change relationships rather than structure.
- Respect the system preference, allow an explicit Day/Night selection, persist
  valid choices, synchronize control state, and update browser theme color.
- Collapse grids by information priority rather than shrinking dense desktop
  layouts. Preserve readable line lengths and touch targets.
- Preserve reduced-motion behavior where smooth scrolling or transitions exist.
- Keep output self-contained within the target project. Do not add a dependency
  on this skill directory.

## Load the relevant evidence

- Read [references/design-system.md](references/design-system.md) whenever color,
  surface, theme order, identity assets, or provenance matters.
- Read [references/typography.md](references/typography.md) when selecting or
  auditing type roles, font stacks, measures, or responsive type behavior.
- Read [references/layout-patterns.md](references/layout-patterns.md) when
  building or changing page structure, grids, reading shells, or responsive
  order.
- Read [references/components.md](references/components.md) only for the
  component families and interaction states present in the requested page.
- Read [references/implementation-notes.md](references/implementation-notes.md)
  when creating, refactoring, theme-wiring, or validating an implementation.

Treat the source keys in those files as the audit trail. Exact values belong to
their original technical or editorial variant; an inferred principle never
overrides an observed selector, token, structure, or behavior.

## Completion check

Confirm that the result retains the selected variant's hierarchy, token roles,
theme behavior, responsive reading order, and interaction accessibility. Remove
unrelated framework defaults and decorative additions that conflict with the
source-backed system.
