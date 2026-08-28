# angze-code-style v0.4.0 real-notebook acceptance

## Scope

- Sanitized notebook identifier: `part-5-worked-tutorial-01`
- Role: tutorial
- Immutable snapshot SHA-256: `e160f1ac42055375c6d498957d64538fff4f76694ac26e4374074a2831721395`
- Size and structure: 527,494 bytes; 44 cells (30 Markdown, 14 code); notebook format 4.5
- Stored state: nine output items, 14 execution counts, 44 cell IDs, and no attachments
- Original integrity: unchanged at the final check

The original notebook was not executed, cleared, regenerated, normalized, or modified. Raw snapshots, candidates, prompts, logs, and private paths remain in an ignored local evidence bundle and are not tracked.

## Zero-edit review

A fresh `$angze-code-style` review-only session changed zero bytes. It reported six finding categories: public/tutorial interface, reproducibility and execution state, shapes/order/missing-value contracts, stored-output provenance, scientific interpretation, and navigation/readability.

The review identified a stale interface description that required expert confirmation. That item was excluded from editing rather than guessed.

## Controlled task and A/B

The bounded task appended at most 12 lines to one existing Markdown cell to document only observable input/output shapes, append ordering, terminal-candidate state, missing/non-finite validation boundaries, and unspecified units. It prohibited code changes, cell operations, output or metadata changes, execution, and normalization.

Fresh baseline and skill sessions began from the exact snapshot hash. Both produced a legitimate eight-line Markdown change, introduced no unsupported scientific claims, and passed the same strict contract validator. Side-by-side review found equivalent correctness, restraint, locality, contract awareness, and notebook safety: **tie**. The skill therefore did not lose to baseline.

## Hard gates and behavior evidence

| Gate | Unexpected changes |
| --- | ---: |
| Structure, order, IDs, and cell types | 0 |
| Notebook and cell metadata | 0 |
| Outputs and execution counts | 0 |
| Attachments | 0 |
| Non-allowlisted source | 0 |
| Bytes outside the intended source value | 0 |
| Serialization locality | 0 |

All 14 code-cell source values were exactly equal to the immutable snapshot; their aggregate source hash was `451a689da8f62471cb24943fb4c44a5974fde48f91b56717f520b417762f3402`. This establishes behavior-preservation evidence for a Markdown-only edit. It does not claim general notebook equivalence.

## Idempotence and runtime integrity

The accepted skill candidate SHA-256 was `19e0bec2539426c7d25f5f74f4b3562300daa184f475cccf1a37ca72cb0b5ee3`. A fresh session repeated the exact request and changed zero bytes; the second-pass hash was identical and the strict validator again reported zero failures.

An initial harness check misclassified the saved session's frozen reference read because it followed a runtime-snapshot path rather than the detector's expected direct path. The detector was corrected over the retained JSONL; the model session was not rerun or replaced, and every substantive idempotence gate had already passed.

The tracked runtime SHA-256 before and after acceptance was `7f79b22c4694717963966132967b1a03b4cf5790529e6c229ef2ef31920fad84`. Acceptance added evidence only; it did not mutate the frozen runtime.

Verdict: **REAL-NOTEBOOK ACCEPTANCE PASSED**.
