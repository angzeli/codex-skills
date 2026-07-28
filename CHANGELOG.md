# Changelog

All notable changes to this collection are documented here. No remote release has been published.

## Unreleased

No changes yet.

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
