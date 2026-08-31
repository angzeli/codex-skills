# Grading rubric

Use one primary tier and only necessary risk overrides. Prefer hard-trigger rules to numerical scoring.

## Decision sequence

1. Determine whether the request modifies or validates a codebase. If not, do not apply this skill.
2. Identify explicit acceptance criteria, repository-mandated checks, side effects, and reversibility.
3. Start with the smallest tier matching the requested surface.
4. Apply hard triggers that raise the tier or validation depth.
5. Freeze an execution contract and revise it only when new evidence changes risk.

Evaluate surface area, behavioral impact, data and side-effect risk, scientific or numerical risk, compatibility, uncertainty, and reversibility. Do not average them into a false-precision score.

## T0 — Mechanical

Use when the requested outcome is obvious, non-behavioral, and target-local.

Typical work:

- Correct a typo, label, comment, or wording.
- Remove an unused import proven unused.
- Apply requested mechanical formatting.
- Correct one obvious metadata value that does not alter runtime behavior.

Contract:

- Inspect the named target only.
- Make the smallest visible diff.
- Add no abstraction, dependency, test framework, or unrelated cleanup.
- Validate text, syntax, or the focused diff only.
- Stop immediately when correct.

Escalate if the apparent text or metadata is executable, generated, public-interface-defining, release-identifying, schema-defining, or scientifically meaningful.

## T1 — Localized Patch

Use for a known, low-risk root cause with a narrow behavior surface.

Typical work:

- Fix one helper, parser edge case, argument-handling bug, or localized notebook problem.
- Add a regression test for one bounded defect.
- Repair a narrow CI command when the cause is known.

Contract:

- Inspect the target and direct call sites.
- Normally change no more than about three production files.
- Preserve architecture and public contracts outside the requested behavior.
- Run the focused regression plus directly relevant static validation.
- Do not run the full suite without evidence or a mandatory instruction.
- Use at most one coherent commit when requested.

Escalate if inspection reveals persistence, broad API impact, concurrency, cross-platform semantics, scientific meaning, uncertain blast radius, or non-revertible side effects.

## T2 — Bounded Feature or Subsystem Audit

Use for one complete capability or one clearly bounded subsystem.

Typical work:

- Add one CLI subcommand, parser, report, workflow, or tutorial.
- Audit one affected subsystem.
- Change several related modules under one acceptance contract.

Contract:

- Inspect only the affected subsystem and freeze scope.
- Add abstractions only for demonstrated current consumers.
- Run targeted unit tests and one relevant integration or smoke check.
- Update affected user-facing documentation only.
- Perform one focused diff review.
- Report unrelated findings without fixing them.

Escalate if the capability mutates persistent user data, crosses compatibility boundaries, changes scientific defaults, or exposes an uncertain broad blast radius.

## T3 — High-Risk Change

Use when correctness cannot be protected by localized software checks alone.

Hard triggers:

- Scientific or numerical semantics that could silently alter results or conclusions.
- Persistent schema or data-format changes.
- Public API behavior or backward compatibility.
- Concurrency, file locking, or atomicity.
- Cross-platform filesystem, process, encoding, or numerical behavior.
- Nontrivial user-data mutation.
- Calculation defaults, charge, spin, multiplicity, units, signs, thresholds, restart, path, or provenance semantics.
- Uncertain root cause with a broad plausible blast radius.

Contract:

- Inspect dependencies and state a short plan when useful.
- Keep the implementation bounded.
- Add focused regression and relevant integration checks.
- Validate scientific invariants, compatibility, migration safety, or data preservation as applicable.
- Run only the broader relevant suite justified by the affected surface.
- Do not add release-grade processes unless publication or distribution is in scope.

## T4 — Release, Destructive, or Critical

Use when failure may escape the repository, become hard to reverse, or cross a security or publication boundary.

Hard triggers:

- Release candidate, package publication, tag or release identity, or public distribution.
- Destructive migration or restore.
- Irreversible external write or high data-loss risk.
- Security, credential, signing, or trust boundary.
- Broad backward-compatibility migration.
- Explicit release-quality validation.

Contract:

- Derive the full relevant quality gate from the explicit release request, project configuration, and repository checklist. It may include full tests, lint, formatting, typing, build, clean install, compatibility matrix, migration fixtures, restore rehearsal, hostile review, and release-identity checks only when those gates apply.
- Run each applicable gate once after the final change. Do not inspect Git history or tags, repeat identity searches, or add generic release ceremony when tag creation, history, remote identity, or publication is outside the request.
- When a full required test gate already covers an identity or regression test, do not run the subset separately unless it is needed to diagnose a failure. Read the checklist and package configuration directly; stop searching once they establish the release surface.
- Resolve targets and obtain authorization before destructive or external actions.
- Keep irrelevant release ceremony out of non-release work.

Repository size, maturity, or a desire for reassurance is not a T4 trigger.

## Risk overrides

Use an override only when it materially changes the normal execution contract implied by the primary tier. Do not emit overrides decoratively or duplicate the primary tier rationale in override form.

- `scientific/numerical`: Validate units, signs, tolerances, invariants, convergence, and provenance. A tiny patch may be `T1 with scientific/numerical override`.
- `data/destructive`: Validate preservation, migration, backups, rollback, and target identity. Escalate to T4 if effects are destructive or irreversible.
- `compatibility/cross-platform`: Validate the affected versions, operating systems, schemas, or legacy formats. Do not create a full matrix without evidence.
- `uncertainty`: Expand inspection until the root cause and blast radius are established, then regrade. Do not confuse uncertainty with permission for broad implementation.

## Audit-only tasks

Grade audits by the surface that must be inspected and the consequence of a missed finding, not by expected diff size.

- A named-file audit is usually T1.
- An affected-subsystem audit is usually T2.
- A scientific-correctness, data-safety, compatibility, or security audit is usually T3 or T4.
- Review-only language prohibits fixes. Report findings and proportional evidence only.

## Ambiguity rules

- If requirements are underspecified but a narrow reversible assumption preserves intent, proceed at the smallest safe tier and state the assumption.
- If different reasonable interpretations materially change public behavior, scientific meaning, persistent data, or destructive scope, request clarification.
- Treat generated files as outputs unless repository instructions identify them as sources.
- Treat notebook Markdown-only edits as T0 or T1 when cell identity, metadata, outputs, and execution state remain untouched; raise the tier for code, outputs, environment, or scientific semantics.
- Treat parser changes as T1 when they add one proven edge-case regression; use T2 for a bounded grammar or report capability; raise to T3 for persistent formats, scientific semantics, or broad compatibility.
- Treat CI repairs as T1 when the failure and fix are local; use T2 for a bounded workflow redesign; use T3 or T4 for publishing, credentials, signing, or release gates.

## Scope expansion gate

Classify every adjacent issue:

- `blocking`: the requested result cannot be correct without it; include and regrade if needed.
- `materially coupled`: correctness requires treating it together; include with a concise explanation.
- `unrelated`: do not fix; report only if material.

An observed nearby defect is not automatically part of the task.

## Escalation and de-escalation

Escalate only on new material evidence. State the old tier, new tier, evidence, and changed validation plan when the change is meaningful. De-escalate when evidence proves the task smaller than expected.

Examples:

- Escalate T1 to T3 when a parser field controls persisted scientific provenance.
- Escalate T2 to T4 when a packaging task becomes public publication.
- De-escalate T2 to T0 when the failure is one documentation typo.
- De-escalate T3 to T1 when a suspected migration is only a display-label defect.

## Completion rule

Stop when acceptance criteria are satisfied, proportional validation has passed, and no blocker remains. Do not continue for completeness, reassurance, future-proofing, cleanup, or additional documentation.
