# Changelog

All notable changes to this collection are documented here. No remote release has been published.

## Unreleased

### Added

- Experimental `angze-task-grader` v0.1.0rc1 runtime with T0-T4 execution contracts, validation floors and ceilings, scientific-computing overrides, scope-expansion gates, controlled JSON evaluation mode, and an explicit composition boundary for artifact/domain skills.
- Synthetic grading, routing, implementation, and one dual-skill composition case; eight public-safe fixture repositories; and a standard-library evaluation harness.
- Deterministic task-grader fixture validation in repository CI.

### Changed

- Defined independent authority for task-grader engineering effort and `angze-code-style` artifact preservation; stricter safety, preservation, and editability constraints win without translating or comparing numeric tiers.
- Limited overrides to the four declared categories and require them only when they materially alter the primary tier's normal execution contract.
- Tightened contract checks for allowed overrides, non-empty fields, actionable stop conditions, T3/T4 hard triggers, and proportional T0/T1 validation ceilings.

### Validated

- Historical original 25-case execution: 21/25 under the earlier override expectations.
- Retrospective rescore of those exact preserved contracts: 25/25 under corrected override semantics; this was not a new execution.
- Fresh final-runtime full execution: 25/25, with no hard-trigger undergrade and no evaluation-mode worktree mutation.
- Final dual-skill composition case: 1/1, with the generated notebook byte-identical, no tracked edit, an explicit preservation constraint, and no numeric-tier comparison.
- Full implicit-routing execution: 8/8 positive and 8/8 negative outcomes by observed task-grader `SKILL.md` reads, with no observed false positive or false negative.
- Existing six-case synthetic behavioral A/B plus focused iterations remains valid, with no observed correctness regression or speculative dependency/abstraction.

### Known limitations

- Synthetic evidence supports correctness and scope restraint but does not establish stable wall-time, command-count, or token savings.
- Routing evidence measures skill-file reads in the current Codex JSON event stream, not general production routing performance.
- The full routing execution spans a preserved five-prompt segment and an eleven-prompt resumed segment because the app was interrupted between prompts; every counted prompt has a completed raw event trace.
- The default Python lacks PyYAML for the optional skill-creator validator; repository-owned structural and deterministic validation passed.

## [0.4.0] - 2026-08-28

### Added

- Scientific and artifact contract inventory with `evidence-backed`, `observable-only`, and `unknown` classifications.
- Tier 0–3 risk grading and standardized review findings.
- First-class conservative Jupyter Notebook policy, role classification, and progressive references.
- Dependency-free notebook structural/locality validator, deterministic synthetic probe, four notebook fixtures, and hard-gate tests.
- Comment-pruning rules that consolidate real data contracts instead of adding narration or erasing useful context.
- Fresh-pass idempotence checks and dirty-target preservation.

### Changed

- Renamed the active skill from `scientific-code-documenter` to `angze-code-style` as a clean break; the old invocation is not retained as an alias.
- Runtime behavior now covers scientific contracts, notebook artifacts, pruning, and explicit preservation boundaries.
- Controlled A/B evaluation now includes notebooks plus Python, Shell, LaTeX, and HTML regressions.
- Historical v0.1–v0.3 results remain predecessor evidence rather than acceptance of the changed runtime.

### Validated

- Six editing fixtures averaged 17.5/18, with six skill wins and behavior preservation at 3/3 throughout.
- Editable, review-only, pruning, and generated notebook hard gates, including exact probe output and byte-level locality.
- Six accepted editing candidates remained byte-identical on fresh second passes.
- Positive implicit triggering at 10/10 and false triggering at 1/10.
- Full post-rename trigger rerun at 10/10 positives and 0/10 negatives, plus one renamed editable-notebook validation and byte-identical fresh second pass.
- Authorized immutable real tutorial-notebook acceptance: zero-edit review, controlled Markdown-only A/B, strict notebook validation, unchanged executable sources, and byte-identical fresh-session idempotence.

### Known limitations

- One notebook feature-development prompt falsely triggered the skill in the original matrix; the post-rename rerun did not reproduce it.
- Manual A/B scoring was not independently blind.
- ShellCheck and rendered LaTeX compilation were unavailable in the original local acceptance environment. Deterministic Shell contracts and static LaTeX contracts passed. ShellCheck subsequently ran and passed under the existing policy in remote CI on Ubuntu for Python 3.11 and 3.12; rendered LaTeX compilation remains a disclosed, non-blocking confidence-depth limitation.
- Deterministic fixtures and bounded Markdown-only real-notebook evidence do not prove general notebook equivalence or scientific correctness.
- Human scientific review remains required; the release remains experimental.

## [0.3.0] - 2026-07-29

### Added

- Real-repository ORCA Shell acceptance evidence.
- Multi-script Shell inventory and contract validation.
- Mock and dry-run preservation checks.
- Command, restart, failure, cleanup, and generated-input comparisons.

### Validated

- Production-style ORCA Shell scripts and review-only repository inspection.
- CLI, environment, exit-code, trap, cleanup, ordering, input-generation, and output-contract preservation.

### Known limitations

- No expensive production calculation was launched.
- Cluster-specific behavior remains outside the current acceptance scope.
- Human scientific review remains required.

## [0.2.0] - 2026-07-28

### Added

- Adversarial synthetic Shell, LaTeX, and HTML evaluation fixtures.
- Deterministic contracts for exit codes, manifests, rendering, labels, DOM behavior, CSV bytes, ordering, scaling, accessibility, and byte-fragile generated outputs.
- Language-specific explicit, implicit, negative, review-only, and generated-file trigger coverage.

### Changed

- Expanded tested language coverage and release evidence without changing the accepted v0.1.0 runtime instructions.

### Validated

- Shell aggregate-failure behavior, ORCA input preservation, manifest contracts, strict-mode restraint, and review-only behavior.
- LaTeX labels, macros, scientific values, conditional compilation, normalized rendered content, and fragile-template preservation.
- HTML DOM and accessibility contracts, CSV export, data ordering, display scaling, formatting, and generated-snapshot preservation.
- Cross-language trigger discovery, false-trigger, review-only, and generated-file boundaries.

### Known limitations

- Non-Python real-repository validation remains outstanding.
- Human review remains required before scientific documentation changes are merged.

## [0.1.0] - 2026-07-28

### Added

- Experimental `scientific-code-documenter` skill.
- Scientific documentation hierarchy and language-specific readability rules.
- Evidence-grounded guidance for units, shapes, conventions, and numerical context.
- Reusable validation, fixture-checking, discovery, and installation tooling.
- Controlled evaluation fixtures, prompt matrix, adversarial cases, and scoring rubric.

### Fixed

- Prevented unsupported inference of units, physical roles, correction meanings, and conversion semantics.
- Enforced review-only mode when a stale comment is identified instead of applying an unrequested edit.

### Validated

- Full five-fixture controlled A/B suite.
- Explicit and positive implicit trigger behavior.
- Negative false-trigger behavior.
- Review-only and explanation-only boundary scope adherence.
- Real-repository acceptance on a scientific Python XPS fitting workbench.

### Known limitations

- This first release remains experimental.
- The strongest real-repository evidence currently comes from Python; other supported languages have fixture-level coverage.
- Human scientific review remains required before merging generated documentation changes.
