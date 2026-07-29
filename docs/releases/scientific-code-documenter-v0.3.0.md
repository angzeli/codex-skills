# scientific-code-documenter v0.3.0

Release date: 2026-07-29

This experimental release candidate adds the first real-repository Shell acceptance for `scientific-code-documenter`. It validates the unchanged v0.2.0 runtime on production-style ORCA workflows while preserving calculation inputs and Shell workflow contracts.

Accepted runtime snapshot SHA-256: `3a58a55702bde8061fb3db226173da80e6f0336049ca679e4a70eb312069312e`

Deterministic manifest SHA-256: `c55d3a7cb122b2b253f0d7c56edef349b13c75fdd08ffef1abd53f9563e79c4e`

## Added and validated

- Real-repository review of nine production-style ORCA Shell scripts totaling 4,319 lines.
- Three controlled A/B edits spanning multi-stage calculation orchestration, shared failure/restart helpers, and parallel cube post-processing.
- Skill aggregate of 89/90 versus 80/90 baseline, with three wins and no ties or losses.
- Zero-edit review-only repository inspection.
- Preservation checks for CLI and environment contracts, exit codes, traps, cleanup, command order, parallelism, restart behavior, failure aggregation, logs, filenames, generated inputs, and output trees.
- Deterministic mock success, failure, process-count fallback, resume, skip-existing, publication, and cleanup scenarios.

No runtime rule changed. v0.3.0 is an expansion of real-repository validation evidence, not a runtime improvement.

## Installation

From the collection checkout:

```sh
./scripts/install_skill.sh scientific-code-documenter --dry-run
./scripts/install_skill.sh scientific-code-documenter
```

The installer links only `skills/scientific-code-documenter/` into the per-user skills directory.

## Compatibility and retained evidence

The runtime files and modes are unchanged from v0.2.0. Existing scientific Python real-repository acceptance and controlled Shell, LaTeX, HTML, CSS, JavaScript, trigger, and boundary evidence remain applicable. No invocation syntax, installation path, or public skill packaging changed.

See the [sanitized v0.3.0 evaluation summary](../evaluations/scientific-code-documenter-v0.3.0.md) for the per-script scores, methodology, preserved contracts, and limitations.

## Limitations

- No expensive production calculation was launched.
- Mock and dry-run validation cannot cover every cluster, scheduler, MPI, or operating-system interaction.
- Real Shell acceptance currently covers one ORCA-oriented source tree.
- Human scientific and maintainer review remains required.
- The skill remains experimental.
