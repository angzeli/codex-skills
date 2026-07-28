# scientific-code-documenter v0.1.0

This is the first experimental release of the scientific code readability and documentation skill. It is intended for focused review, documentation, comment cleanup, and readability improvements that preserve calculations, interfaces, file formats, and numerical behavior.

Accepted runtime snapshot SHA-256: `3a58a55702bde8061fb3db226173da80e6f0336049ca679e4a70eb312069312e`

## Key capabilities

- Review scientific and technical code without editing it.
- Add concise, language-appropriate function and interface documentation.
- Explain supported units, shapes, conventions, assumptions, safeguards, and numerical context.
- Improve names, structure, and comments while preserving behavior and limiting scope.
- Refuse to promote plausible but unsupported scientific interpretations into documentation.

## Installation

From the collection checkout:

```sh
./scripts/install_skill.sh --dry-run scientific-code-documenter
./scripts/install_skill.sh scientific-code-documenter
```

The installer links only `skills/scientific-code-documenter/` into `$HOME/.agents/skills/scientific-code-documenter`.

## Invocation

```text
$scientific-code-documenter
Review this file for readability and documentation quality. Do not modify it. Identify the five highest-value improvements.
```

For editing mode, replace the second line with a focused request that explicitly permits documentation and readability changes while preserving calculations, public interfaces, file formats, and numerical behavior. A no-edit instruction always takes precedence.

## Validation evidence

- Five-fixture controlled A/B evaluation: 112/120 with the skill versus 94/120 baseline; 4 wins, 1 tie, 0 losses.
- Explicit invocation: 5/5; positive implicit triggering: 10/10; negative false-trigger rate: 0% across valid runs.
- Corrected review-only boundary suite: 8/8 valid sessions stayed within scope with zero source changes for review/explanation cases.
- Scientific Python acceptance: 47 files reviewed with zero review-mode changes; selected workflow and library edits scored 23/24 and 24/24 while preserving their tested behavior.

See the [sanitized evaluation summary](../evaluations/scientific-code-documenter-v0.1.0.md) for the methodology and complete release evidence.

## Known limitations

- v0.1.0 remains experimental and does not guarantee scientific correctness.
- The strongest real-repository validation currently covers scientific Python; other supported languages have fixture-level coverage.
- Documentation may remain intentionally concise when evidence is incomplete.
- Human scientific review is required before merging edits.
- One full-suite test launcher failure was environment-dependent and reproduced on untouched source; all 120 tests passed when the source was exposed explicitly.

## Upgrade notes

There are no breaking changes: this is the first versioned release and the repository has no earlier release tag. Existing local source installations can be refreshed with the same individual-skill installer command above.
