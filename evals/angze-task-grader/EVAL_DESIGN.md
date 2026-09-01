# Evaluation design

## Questions

1. Does controlled evaluation mode produce the stable contract schema and an acceptable tier?
2. Does the skill avoid undergrading canonical scientific, destructive-data, and release cases?
3. Does treatment preserve correctness while reducing or matching scope and validation effort on low-risk work?
4. Does implicit routing cover execution tasks without activating on conceptual, prose, or ordinary prompts?
5. When both task-grader and code-style apply, does artifact preservation remain authoritative over a low-effort engineering grade?

## Isolation

- Use only fixtures in this directory.
- Copy every arm into a new temporary directory.
- Initialize Git only inside the disposable copy and commit the starting fixture.
- Install the treatment skill only inside the copy at `.agents/skills/angze-task-grader`.
- Install both skills only inside the disposable copy for the one composition case.
- Never modify canonical fixtures during an arm.
- Require no network for fixture behavior or deterministic checks.
- Store raw generated results under ignored `results/`.

The baseline and treatment use the same fixture bytes, task text, Codex executable, model setting, inherited reasoning/speed configuration, sandbox, approval policy, and environmental limits. The only intentional differences are treatment's repo-scoped skill and explicit invocation.

## Grading acceptance

- Require at least 90% exact or explicitly acceptable-adjacent agreement.
- Forbid any tier below expected on canonical T4 cases.
- Forbid any tier below T3 on canonical scientific or data-destructive T3 cases.
- Require the exact JSON key set and value types.
- Reject unknown override names, empty required content, and non-actionable stop conditions.
- Reject affirmative release-grade validation ceilings in canonical T0/T1 cases.
- Require named overrides only when they materially extend the primary tier; do not require an override that merely restates the tier's defining hard trigger.
- Bind expected overrides to the expected primary tier; an explicitly acceptable higher adjacent tier is judged against its own base contract rather than inheriting a lower tier's override.
- Compare repeated runs when consistency evidence is requested; do not infer stability from one run.

## Behavioral metrics

Record deterministic or event-supported signals:

- acceptance-command result;
- changed-file count and diff;
- production lines added and removed;
- unrelated files or cleanup;
- added modules and dependencies;
- commands and repeated commands when emitted;
- targeted versus broad validation operations, counting compound shell segments rather than treating a wrapper invocation as one check;
- wall time, exit status, and final response;
- token usage only when genuinely emitted.

Automated heuristics flag full-suite commands, repeated commands, dependency additions, and changed files outside each case's allowed paths. Human review scores unnecessary abstraction, scope creep, disproportionate validation, documentation usefulness, maintainability, and correctness concerns. Subjective overengineering is not treated as perfectly machine-detectable.

## Composition acceptance

The single composition case reuses the synthetic generated-notebook fixture from `angze-code-style`, introduces one heading typo only in a disposable copy, and explicitly invokes both skills. It passes only when the task-grader identifies the requested correction as T0 or T1, the generated notebook remains byte-identical and the worktree stays clean, the response identifies the preservation or editability constraint, and the two skills' numeric tiers are not compared or translated.

## Human-review template

For each arm record:

- Correctness concerns: none / minor / material, with evidence.
- Unnecessary abstraction: none / suspected / present, with file and reason.
- Scope creep: none / suspected / present, with unrelated paths or behavior.
- Validation proportionality: insufficient / proportional / excessive, with command evidence.
- Documentation: useful / neutral / unnecessary, with examples.
- Maintainability: improved / unchanged / worsened, with reason.
- Overall decision: baseline / tie / treatment / invalid comparison.

## Routing evidence

Prefer direct skill-loading events from Codex JSON. If unavailable, record manual inspection or a response-shape behavioral proxy and label it explicitly. Do not fabricate activation rates.

## Operational bounds

- Run all deterministic checks and the 25 grading cases for a release decision.
- Run the one dual-skill composition case and all 16 routing prompts for the v0.1.0rc1 decision.
- Limit implementation A/B smoke to approximately four to six cases during normal development.
- Do not run the full behavioral matrix without explicit authorization.
- Abort and document the blocker when Codex is unavailable, unauthenticated, or unable to isolate disposable repositories.
- Do not claim production effectiveness or token savings from synthetic results alone.
