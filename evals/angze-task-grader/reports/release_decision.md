# v0.1.0rc1 release decision

Decision: ready for experimental v0.1.0rc1 use. Synthetic evaluation does not establish production-wide effectiveness.

## Composition authority

`angze-task-grader` controls engineering-process effort: inspection, patch scope, abstraction, validation, documentation, review, commits, and stopping. Artifact or domain skills such as `angze-code-style` control preservation, scientific and data contracts, notebook handling, editability, review-only boundaries, and representation-sensitive constraints. User, system, safety, repository, and explicit task constraints remain higher authority.

When both skills apply, both contracts must be satisfied and the stricter safety, preservation, or editability constraint wins. Their numeric tier labels are never translated, compared, ranked, or equated. A low task-grader tier cannot authorize an edit that code-style makes review-only, while a high code-style preservation tier does not itself require release-grade task-grader validation.

The final composition execution, `composition-20260831T134448Z`, passed 1/1. The task-grader identified the requested typo correction as T0, but the generated and non-editable notebook remained byte-identical and the worktree stayed clean. The response identified the unavailable upstream generator and review-only constraint; no numeric-tier comparison was detected.

## Controlled grading evidence

Three evidence generations remain distinct:

1. **Historical original execution — 21/25.** `grading-20260828T103916Z` scored 21/25 under earlier override expectations. It had no T3/T4 hard-gate failure and made no evaluation-mode worktree change.
2. **Historical retrospective rescore — 25/25.** The exact preserved contracts from that run rescore 25/25 under the corrected override semantics. This is not a new runtime execution.
3. **Fresh final-runtime full execution — 25/25.** `grading-20260831T131351Z` ran all 25 cases anew against the final runtime and validator. It achieved 25/25, with no hard-gate failure, failed Codex invocation, or evaluation-mode worktree mutation.

Intermediate RC-cleanup runs and the rejected structured-output transport attempt remain preserved under ignored `results/`; they were diagnostic evidence, not substituted for the definitive fresh run.

## Override and contract checks

The allowed override vocabulary is exactly `scientific/numerical`, `data/destructive`, `compatibility/cross-platform`, and `uncertainty`. An override is required only when it materially changes the normal contract implied by the chosen primary tier; it is not required to repeat that tier's defining reason. Accepted adjacent tiers are evaluated against their own base contract rather than inheriting an override from another primary tier.

Deterministic checks reject unknown or duplicate overrides, empty required content, non-actionable stop conditions, canonical T3/T4 undergrading, and affirmative release-grade validation ceilings in canonical T0/T1 cases. Negated limits such as “do not run the full suite” remain valid.

## Routing evidence

The earlier routing evidence executed only one positive and one negative prompt. The final evaluation executed all 16 current prompts against the final discovery configuration:

- positives: 8/8 showed a direct task-grader `SKILL.md` read;
- negatives: 8/8 showed no task-grader `SKILL.md` read;
- observed false negatives: 0;
- observed false positives: 0.

An app interruption occurred after the first five positive prompts completed. Their event traces remain in `routing-20260831T134744Z`; the remaining three positives and all eight negatives completed in `routing-20260901T030809Z`, whose summary is 11/11. The aggregate is therefore 16/16 across two preserved run segments. This measures presence or absence of a task-grader skill-file read in the current Codex JSON command stream, not general production routing accuracy.

## Deterministic validation and CI

Repository structural validation passed for all four skills. `./scripts/run_fixture_checks.sh angze-task-grader` passed case schemas and tier distribution, all eight deliberately failing synthetic seeds, contract vocabulary and content checks, stop and ceiling assertions, T3/T4 hard gates, and deterministic composition assumptions. Repository CI now runs that same offline, credential-free command.

The optional skill-creator `quick_validate.py` could not run because the default Python does not provide PyYAML. The repository-owned structural validator passed; no dependency was installed solely for this optional check.

## Existing behavioral A/B evidence

The existing six-case synthetic A/B evidence remains applicable because the RC changes clarified governance, evaluation semantics, and composition without changing the implementation fixtures' acceptance behavior. No treatment correctness regression was observed. Timing, command count, and token effects were mixed, so no speed, token-savings, or real-world productivity improvement is claimed.

## Safety and limitations

- All model-backed runs used synthetic fixtures in disposable repositories.
- No real task, private-task replay, real research repository, production system, expensive scientific calculation, publication, or external write was used.
- No user-scope skill installation or symlink state was modified.
- Ignored historical evidence was neither rewritten nor deleted.
- No push, tag, publication, or remote mutation occurred.

Synthetic evaluation establishes controlled behavioral evidence, not proof of performance on every real repository.
