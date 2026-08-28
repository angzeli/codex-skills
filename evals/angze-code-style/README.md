# Angze Code Style evaluation

This suite tests whether the skill improves documentation and readability without changing behavior or expanding scope. It includes contract-aware Jupyter Notebook cases without treating notebook JSON as ordinary text. Tracked fixtures are synthetic and contain no unpublished research or third-party project code. Authorized real-repository runs retain raw source, diffs, and logs only in ignored local result directories; tracked summaries are sanitized.

## Evaluation layers

1. Run collection structural validation to check frontmatter, naming, references, and portable runtime content.
2. Use `prompts.yaml` to test explicit invocation, positive implicit triggering, false triggers, and boundary decisions in fresh sessions.
3. Run `./scripts/run_fixture_checks.sh angze-code-style` before and after each fixture edit. Notebook candidates must also pass their fixture-specific contract file.
4. Compare baseline and skill-assisted diffs from identical starting commits using the same model and prompt.
5. Score both outputs with `rubric.md`; preserve raw diffs and command logs under `results/`.
6. Exercise adversarial and notebook fixtures to confirm that unknown meaning is not invented and generated, review-only, or protected notebook state remains untouched.
7. Rerun the same skill prompt against every accepted editing candidate. The second pass must create no tracked diff; notebook bytes must be identical to pass 1.
8. After synthetic acceptance, repeat review-only and limited-edit prompts on real repositories whose owners explicitly permit the work.

Structural success is necessary but does not establish trigger accuracy or effectiveness. Record those claims only after the full prompt matrix and controlled comparisons have been completed.

## Fixtures

- `python/`: a numerical spectrum transformation with mixed calculation and presentation concerns, unclear units, and protected output tests.
- `html/`: an intentionally over-nested report with weak names, inline styling, and an unlabeled control; the validator checks syntax and preserves the intended challenge.
- `shell/`: a valid workflow with quoting and working-directory issues plus a long scientific-computing command.
- `latex/`: a compilable report with scattered macros, long lines, inconsistent float structure, and an unexplained workaround.
- `adversarial/`: trivial code, unknown scientific meaning, a protected unusual threshold, and generated or vendored files that must not be edited.
- `notebook/`: editable, review-only, over-commented, and generated notebooks plus a dependency-free structural/locality validator and a narrow isolated synthetic probe.

Baseline fixtures are intentionally imperfect. A good edit may change their style defects but must keep executable checks and protected outputs passing.

## Controlled A/B outline

- Create sibling worktrees outside the main checkout at the same starting commit.
- Start fresh Codex sessions with the same model and prompt.
- Run the baseline without explicit invocation and the comparison with `$angze-code-style`.
- Compare the four notebook cases and representative Python, Shell, LaTeX, and HTML cases. Count the 75% win threshold across editing fixtures; both notebook editing fixtures must beat baseline.
- Use write-enabled workspaces for review-only and generated pairs so restraint is demonstrated rather than enforced by permissions. These cases may tie, but the skill must not lose or modify a byte.
- Save each diff and validation log, then score both independently.
- Validate every accepted skill editing candidate again after a fresh second pass; retain the pass-2 raw log and zero-diff evidence.
- Record the model, date, commit, fixture, trigger result, scores, validation outcome, strengths, regressions, and follow-up work.

Notebook candidates are invalid before qualitative scoring if any protected field, output, attachment, execution count, non-allowlisted source, or byte outside an allowlisted source value changes. Validator errors and ambiguous comparisons also fail closed. The deterministic fixture probe executes only selected trusted synthetic code cells in isolated Python processes. It does not run a notebook, provide a security sandbox, or prove general notebook equivalence.

Exact repository-specific commands are maintained in the root `README.md` after the shared scripts and commits exist.

## Real-repository acceptance

Historical acceptance covers an authorized scientific Python repository and a production-style ORCA Shell workflow repository. The ORCA run reviewed nine scripts, exercised three controlled edit pairs with isolated mocks and dry runs, and preserved generated calculation inputs and workflow contracts without launching an expensive calculation. See the [v0.3.0 sanitized summary](../../docs/evaluations/scientific-code-documenter-v0.3.0.md). Those runs remain evidence for the predecessor runtime, not acceptance of the contract-aware v0.4 runtime.

Real-notebook acceptance for v0.4 remains pending until a notebook owner explicitly authorizes an immutable review and controlled edit candidate. Do not substitute a personal or research notebook merely because it is locally available.

Run real-repository candidates only from immutable snapshots, never from the live source tree. Protect and restore tracked source state, and determine validity from the frozen runtime, source inputs, prompts, harnesses, and captured outputs. Ignored calculation outputs and filesystem metadata remain outside that boundary unless explicitly frozen; record concurrent external activity separately without treating live-source quiescence as an evaluation gate.

Future acceptance should add an authorized HTML/reporting or scientific-document repository and broader scheduler or cluster environments. Use the reusable prompts in `prompts.yaml`; do not use private code without authorization.
