# Implementation notes

Use this file when creating a page, refactoring an existing site, or auditing
whether an implementation follows the skill. Source keys refer to
[design-system.md](design-system.md).

- [Forensic workflow](#forensic-workflow)
- [Structure before styling](#structure-before-styling)
- [CSS organization and naming](#css-organization-and-naming)
- [Theme implementation](#theme-implementation)
- [Refactoring an existing site](#refactoring-an-existing-site)
- [Verification](#verification)

## Forensic workflow

Before changing a target site:

1. Locate the rendered entry points, templates/layouts, active stylesheets,
   theme script, and locally used assets. Ignore generated copies when an
   editable source exists.
2. Extract custom properties, font stacks, shell widths, major component
   selectors, interaction states, and every media query. Record selector or
   file evidence beside each conclusion.
3. Separate observations from inferences. Treat a declared-but-unused variable,
   hidden placeholder, or one-off content class as evidence of existence—not a
   universal rule.
4. Identify conflicts with the target's current system. Preserve deliberate
   project semantics and explicit user instructions; use this skill to restyle
   only the authorized surface.
5. Select the technical or editorial variant by content function. List the
   components actually needed before writing CSS.

Do not infer a token from an image sample when the active CSS can be inspected.
Do not copy generated site output back over editable templates.

## Structure before styling

For a technical architecture page, preserve this semantic order when the
content supports it: `[W-HTML]`

```html
<a class="skip-link" href="#main-content">...</a>
<main class="site-main" id="main-content">
  <section class="hero" aria-labelledby="page-title">...</section>
  <section class="workflow-board" aria-labelledby="workflow-title">
    <div class="section-intro">...</div>
    <div class="workflow-grid">
      <section class="stage-row stage-row--paired">...</section>
      <section class="stage-row stage-row--shared">...</section>
    </div>
  </section>
</main>
<footer class="site-footer">...</footer>
```

Use `article` for self-contained stage nodes, `section` for labeled groups,
`aside` for companion context, `ul` for evidence sets, and `dl` for named
strategies. Connector elements remain presentational and hidden from assistive
technology.

For an editorial site, preserve a reusable shell and reading article:
`[B-HTML]`

```html
<header class="site-header">...</header>
<main class="site-main">
  <article class="post-shell">
    <header class="post-header">...</header>
    <div class="post-content">...</div>
    <nav class="post-navigation" aria-label="...">...</nav>
  </article>
</main>
<footer class="site-footer">...</footer>
```

For home or portfolio pages, exchange the article for a labeled `.home-hero`
and one or more narrow semantic sections. Keep metadata before titles in list
items and keep actions subordinate to the page thesis.

## CSS organization and naming

Follow the source cascade order where possible: `[W-CSS] [B-CSS]`

1. theme-independent custom properties and default theme values;
2. system-preference theme override;
3. explicit `html[data-theme="light|dark"]` overrides;
4. box sizing and element foundations;
5. shared shell and global interactions;
6. page regions and components in document order;
7. responsive blocks from wider to narrower thresholds;
8. reduced-motion override where motion exists.

Use role-led class names already established by the sources:

- shell: `site-*`;
- major regions: `hero-*`, `section-*`, `page-*`, `post-*`;
- technical structure: `stage-*`, `node-*`, `tool-*`, `connector-*`;
- base plus modifier: `.stage-row.stage-row--paired`,
  `.detail-list.detail-list--two`;
- behavior hooks: `data-theme-choice`, `data-view`, `data-branch`, and
  `data-workflow-board` rather than style-dependent JavaScript selectors.

Keep component declarations token-based. Scope a second variant to a semantic
region rather than redefining global variables halfway through a page without a
clear boundary.

## Theme implementation

Both sources implement the same behavioral contract with small cascade-order
differences. `[W-CSS] [W-HTML] [W-JS] [B-CSS] [B-HTML] [B-JS]`

1. Define complete Day and Night custom-property sets in CSS and retain a
   `prefers-color-scheme` fallback.
2. Run a small head bootstrap before the stylesheet paints. Read only `light`
   or `dark` from storage; otherwise resolve the system preference.
3. Apply the resolved value through `document.documentElement.dataset.theme`
   when the source variant requires an explicit attribute, and set
   `color-scheme` consistently.
4. Build the visible control from two buttons using `data-theme-choice`,
   `.is-active`, and synchronized `aria-pressed` values.
5. Persist a manual choice. Catch storage read/write errors so the selected
   theme still applies for the current page.
6. Follow system preference changes only while no saved manual choice exists.
7. Update browser theme-color metadata to the active page ground. Use the
   selected variant's extracted pair: technical `#f2efe8 / #11181d` or
   editorial `#f5efe4 / #11181d`.

Preserve an existing storage key. For a new site, choose one stable key scoped
to that project; do not couple unrelated sites through a shared arbitrary key.
Keep labels as Day/Night or a faithful localization. Do not replace the control
with an unrelated switch design unless requested.

## Refactoring an existing site

- Map old selectors to semantic roles before renaming or deleting them.
- Introduce the selected source token names, then replace raw literals only when
  their role is proven. Do not bulk-map colors by visual similarity.
- Preserve framework behavior, templates, routes, content data, form semantics,
  and application logic.
- Remove conflicting framework decoration only inside the authorized page or
  component scope.
- Retain deliberate project assets. Use the archive mark only for the same
  identity or when explicitly requested.
- Keep content-specific technical connectors and archive filters out of pages
  that do not express those relationships.

## Verification

Check the result against the actual target and the selected reference variant:

- no new color literal lacks a documented role or explicit user instruction;
- every theme token resolves in both Day and Night modes;
- system default, manual choice, reload persistence, system-change behavior,
  invalid/missing storage, and storage failure degrade correctly;
- keyboard focus is visible, controls use real buttons, pressed state is
  announced, heading order is coherent, and presentational connectors are
  hidden from assistive technology;
- technical layouts are inspected across `1000px`, `820px`, `700px`, and
  `460px` behavior changes; editorial layouts are inspected across `700px`;
- no-JavaScript content remains complete, especially both workflow branches;
- long titles, long tool names, CJK text, list density, and figures do not
  overflow their measures;
- reduced-motion preference suppresses nonessential motion where transitions or
  smooth scrolling are present;
- the final diff contains only the requested site scope and no dependency on the
  skill bundle.
