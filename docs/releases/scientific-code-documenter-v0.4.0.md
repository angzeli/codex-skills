# scientific-code-documenter v0.4.0

Release preparation date: 2026-08-28

This experimental release candidate changes runtime behavior. It upgrades scientific documentation from style guidance to contract-aware, risk-graded work and adds conservative first-class support for Jupyter Notebook artifacts.

The final v0.4 package will be renamed to `angze-code-style` after the pre-rename implementation, evaluation, and local release preparation are stable. Final renamed runtime and manifest hashes will be recorded after that migration.

## Added

- A pre-edit inventory of scientific meaning, units, shapes, schemas, ordering, missing values, state dependencies, interfaces, outputs, and artifact structure.
- Explicit `evidence-backed`, `observable-only`, and `unknown` classifications.
- Tier 0 review through Tier 3 protected-risk decisions, with standardized finding fields and reason labels.
- Notebook role classification: source, tutorial, analysis artifact, generated, or unknown.
- Structured notebook preservation for formats, cells, IDs, types, metadata, attachments, execution counts, outputs, untouched source, and serialization locality.
- Comment pruning that removes syntax narration while retaining concise observable data contracts.
- A standard-library notebook validator and isolated deterministic fixture probe.
- Four public-safe notebook fixtures plus Python, Shell, LaTeX, and HTML regression coverage.

## Evaluation result

Six editing comparisons averaged 17.5/18, with a minimum of 17/18, behavior preservation at 3/3 for every accepted fixture, and six skill wins. Review-only and generated notebooks were byte-identical ties. All notebook hard gates passed, including the exact numerical/missing-value/ordering probe and fresh-pass idempotence.

Positive implicit triggering was 10/10. One of ten negative prompts—a notebook feature request—falsely triggered, meeting but not exceeding the 10% limit.

## Notebook safety boundary

Notebooks are not executed, cleared, regenerated, reordered, or normalized by default. Source edits are restricted to explicit cells or fields and require structural plus textual-locality validation. Stored outputs remain stored outputs; their presence does not imply recomputation after a source edit.

The deterministic probe executes only selected trusted synthetic fixture code in isolated Python processes. It is not a security sandbox, notebook execution engine, or proof of general notebook equivalence.

## Limitations and release status

- No real notebook was supplied with explicit authorization. Required real-notebook review and controlled-edit acceptance remain pending.
- Scoring was manual side-by-side review, not an independent blind judge.
- ShellCheck and `pdflatex` were unavailable. Shell behavior contracts and static LaTeX contracts passed, but rendered LaTeX validation did not run.
- One notebook feature prompt falsely triggered the skill.
- Notebook structure preservation does not establish scientific correctness, output freshness, provenance completeness, or hidden-state safety.
- Jupyter is the only newly supported environment; R, MATLAB, Julia, and Fortran remain out of scope.
- Human scientific and maintainer review remains mandatory.
- The release remains experimental.

Provisional verdict: **PARTIALLY READY — REAL-NOTEBOOK ACCEPTANCE PENDING**.
