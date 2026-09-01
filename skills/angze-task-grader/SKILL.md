---
name: angze-task-grader
description: Grade codebase and scientific-computing tasks before execution to select the minimum sufficient inspection, patch scope, abstraction, validation, documentation, review, subagent, and commit effort. Use for code edits, bug fixes, repository audits, CI/build failures, bounded features, refactors, CLI or parser changes, notebook edits, migrations, releases, packaging, and scientific workflow changes. Do not use for pure conceptual Q&A, general explanations, prose or email writing, brainstorming, ordinary conversation, or requests that neither modify nor validate a codebase.
---

# Angze Task Grader

Apply the least engineering work sufficient for the actual risk of the requested task. Act as a lightweight execution governor; do not replace user, system, developer, repository, directory-specific, or domain-skill instructions.

## Compose with artifact and domain skills

User, system, safety, repository, and explicit task constraints remain highest authority. This skill controls engineering-process effort: inspection and patch scope, abstraction, validation, documentation, review, commits, and stopping. A domain skill such as `angze-code-style` controls artifact preservation, scientific and data contracts, notebook handling, editability, review-only boundaries, and representation-sensitive constraints.

When both apply, satisfy both sets of constraints; the stricter safety, preservation, or editability constraint wins. Never translate, compare, rank, or equate their numeric tier labels. A low task-grader tier does not permit an edit that the domain skill makes review-only, and a high preservation tier in another skill does not by itself require release-grade validation here.

## Grade before executing

1. Identify the requested outcome, acceptance criteria, explicit constraints, and applicable repository instructions.
2. Assign one provisional tier using hard triggers rather than a weighted score:
   - `T0 Mechanical`: non-behavioral, obvious, target-local work.
   - `T1 Localized Patch`: known, low-risk behavior change with a narrow affected surface.
   - `T2 Bounded Feature or Subsystem Audit`: one complete bounded capability or affected-subsystem review.
   - `T3 High-Risk Change`: scientific, numerical, persistent-data, public-interface, concurrency, compatibility, restart/provenance, or broad-uncertainty risk.
   - `T4 Release, Destructive, or Critical`: publication, irreversible external effects, destructive migration or restore, security boundary, data-loss risk, or release-quality validation.
3. Add only necessary named overrides that materially change the normal contract for the primary tier: `scientific/numerical`, `data/destructive`, `compatibility/cross-platform`, or `uncertainty`. Do not restate the reason for the tier as an override.
4. Establish an internal execution contract: tier, material reasons, inspection budget, patch budget, abstraction budget, validation floor and ceiling, documentation budget, review requirement, subagent policy, commit strategy, stop condition, and escalation triggers.
5. Execute within the contract. Use the defaults below without loading references for clear cases. Read [references/grading-rubric.md](references/grading-rubric.md) only for a genuine tier boundary or ambiguity, and [references/validation-matrix.md](references/validation-matrix.md) only when the validation floor or ceiling is unclear.

Keep the contract internal for T0-T1. For T2, state at most one short tier line when useful. For T3-T4, briefly state the tier and the reason for stronger validation. Do not emit a rubric unless asked.

## Apply the default contracts

### T0 — Mechanical

- Inspect only the target.
- Make the minimal mechanical diff with no abstraction, dependency, or cleanup.
- Validate text, syntax, or the focused diff only; never run the full suite.
- Stop as soon as the requested correction is visibly correct.

### T1 — Localized Patch

- Inspect the target and direct call sites; normally keep production changes within about three files.
- Treat a known one-line repair to executable CI or workflow configuration as T1, not T0.
- Stay within the existing architecture and prohibit speculative abstraction.
- Run targeted tests and the directly relevant lint, type, import, or static check.
- Do not run the full suite without new evidence or a mandatory repository instruction.
- Use at most one coherent commit when a commit is requested; otherwise do not commit.
- Stop after the acceptance criteria and proportional validation pass.

### T2 — Bounded Feature or Subsystem Audit

- Inspect the affected subsystem and freeze scope before implementation.
- Add an abstraction only for a demonstrated current need.
- Run targeted unit tests plus one relevant integration or smoke check.
- Update only affected user-facing documentation and perform one focused diff review.
- Report unrelated findings without fixing them.
- Stop when the bounded acceptance criteria pass.

### T3 — High-Risk Change

- Inspect dependencies and state a short plan before editing when useful.
- Keep patch scope bounded even when validation depth is high.
- Run focused regression and relevant integration checks; add scientific, numerical, compatibility, or data-safety validation as applicable.
- Run a broader relevant suite only when the affected surface or repository policy justifies it.
- Do not add clean-room installs or release matrices unless the task requires them.

### T4 — Release, Destructive, or Critical

- Apply the full quality gate actually required by the release or critical risk.
- Include build, clean-install, compatibility, migration, restore, hostile-review, publication-identity, or external-user checks only when applicable.
- Resolve exact targets before destructive or irreversible actions and obtain any required authorization.
- Do not assign T4 merely because a repository is large or mature.

## Enforce proportionality

Treat these as invariants:

> Validation effort must be proportional to change risk, not repository size.

> Additional validation requires evidence, not anxiety.

Define a validation floor and ceiling before running checks. Repository-mandated checks and explicit user requirements take precedence. If a required check is unavailable, report the limitation and strongest substitute; never claim it passed.

Run one check per distinct risk. Use a repository-documented or evidently supported command directly; do not probe equivalent interpreter, test-runner, or command aliases. For Python, use the interpreter named by repository commands; if none is named, use `python3` once rather than probing `python`. If the selected executable is unavailable, switch once to the supported alternative, then run that validation purpose only once. Do not repeat a passing check after unchanged code. When a broader required gate includes a focused check, run only the broader gate after the final change unless the focused check is needed first to diagnose a failure.

Keep validation from adding unrelated artifacts. For focused Python checks in a clean or restricted worktree, set `PYTHONDONTWRITEBYTECODE=1` or redirect bytecode to a temporary location; do not create repository `__pycache__` directories and then clean them up as an extra step.

Stop investigating once the root cause and affected surface are sufficiently established. Do not reread unchanged files, repeat searches, inspect unrelated modules, use history or blame, or broaden architecture analysis unless new evidence could change correctness or scope.

For a self-contained task that names the target and focused tests, inspect those files directly. Perform at most one bounded search for applicable repository instructions when their location is unknown; do not precede a localized task with generic file inventories, repository-wide content searches, or redundant status probes.

For release work, derive the file set and gates from the explicit checklist and package configuration. Once those sources identify the release surface, stop inventorying. Do not delete caches that were redirected outside the worktree or never created.

## Prevent overengineering and scope creep

- Prefer the smallest correct implementation.
- Add no speculative abstraction, dependency, module, extension point, factory with one backend, interface with one implementation, configuration framework for a few constants, or generic framework for one demonstrated case.
- Perform no opportunistic improvements, unrelated cleanup, architecture migration, broad documentation, or multiple commits for a trivial patch.
- Before adding architecture, ask whether fewer moving parts implement the current requirement correctly. If yes, choose the smaller design.
- Classify adjacent findings as `blocking`, `materially coupled`, or `unrelated`. Include only blocking or materially coupled work; report material unrelated findings without fixing them.

Use subagents proportionally: none for T0-T1; only clearly independent, time-saving work for T2; independent exploration, compatibility analysis, testing, or review for T3-T4 when it genuinely helps. Applicable system or developer restrictions on delegation still control.

## Handle scientific and numerical work

Read [references/scientific-computing.md](references/scientific-computing.md) whenever scientific results, numerical semantics, structures, units, energies, convergence, provenance, or expensive calculations may be affected.

Scientific risk can raise validation depth without increasing patch size. A two-line correction may remain a T1-sized patch while requiring T3-style scientific validation. Never launch an expensive calculation without explicit authorization; prefer minimized or synthetic fixtures. A plausible-looking numerical value is not evidence of correctness.

## Escalate only on evidence

Treat the initial grade as provisional. Escalate when inspection reveals a materially higher-risk surface, and de-escalate when evidence proves the task smaller. For a meaningful escalation, briefly state the old tier, new tier, new evidence, and changed validation plan. Do not silently expand a localized task into high-risk work.

Before any extra work, ask:

1. Are the requested acceptance criteria satisfied?
2. Has proportional validation passed?
3. Is any blocker unresolved?

If the answers are yes, yes, and no, stop.

## Use controlled evaluation mode

When the exact phrase `TASK-GRADER EVAL MODE` appears, do not modify files, execute the requested task, or run validation. Output only one valid JSON object with exactly these keys and compatible value types:

```json
{
  "tier": "T1",
  "tier_name": "Localized Patch",
  "risk_overrides": [],
  "reasons": [],
  "inspection_budget": [],
  "patch_budget": {
    "expected_scope": "",
    "file_guidance": ""
  },
  "abstraction_budget": "",
  "validation_floor": [],
  "validation_ceiling": [],
  "documentation_budget": "",
  "review_requirement": "",
  "subagent_policy": "",
  "commit_strategy": "",
  "stop_condition": "",
  "escalation_triggers": []
}
```

Return plain JSON without Markdown fences or commentary. Grade the described task without performing it. Do not mention evaluation mode during ordinary tasks.

## Finish concisely

Report what changed, which proportional validation ran, and any material limitation or deferred unrelated finding. Do not explain the grading framework unless asked. Consult [references/examples.md](references/examples.md) only when a boundary case needs comparison.
