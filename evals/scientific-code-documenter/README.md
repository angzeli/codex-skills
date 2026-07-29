# Scientific Code Documenter evaluation

This suite tests whether the skill improves documentation and readability without changing behavior or expanding scope. Tracked fixtures are synthetic and contain no unpublished research or third-party project code. Authorized real-repository runs retain raw source, diffs, and logs only in ignored local result directories; tracked summaries are sanitized.

## Evaluation layers

1. Run collection structural validation to check frontmatter, naming, references, and portable runtime content.
2. Use `prompts.yaml` to test explicit invocation, positive implicit triggering, false triggers, and boundary decisions in fresh sessions.
3. Run `./scripts/run_fixture_checks.sh scientific-code-documenter` before and after each fixture edit.
4. Compare baseline and skill-assisted diffs from identical starting commits using the same model and prompt.
5. Score both outputs with `rubric.md`; preserve raw diffs and command logs under `results/`.
6. Exercise adversarial fixtures to confirm that unknown meaning is not invented and generated or vendored files remain untouched.
7. After synthetic acceptance, repeat review-only and limited-edit prompts on real repositories whose owners permit the work.

Structural success is necessary but does not establish trigger accuracy or effectiveness. Record those claims only after the full prompt matrix and controlled comparisons have been completed.

## Fixtures

- `python/`: a numerical spectrum transformation with mixed calculation and presentation concerns, unclear units, and protected output tests.
- `html/`: an intentionally over-nested report with weak names, inline styling, and an unlabeled control; the validator checks syntax and preserves the intended challenge.
- `shell/`: a valid workflow with quoting and working-directory issues plus a long scientific-computing command.
- `latex/`: a compilable report with scattered macros, long lines, inconsistent float structure, and an unexplained workaround.
- `adversarial/`: trivial code, unknown scientific meaning, a protected unusual threshold, and generated or vendored files that must not be edited.

Baseline fixtures are intentionally imperfect. A good edit may change their style defects but must keep executable checks and protected outputs passing.

## Controlled A/B outline

- Create sibling worktrees outside the main checkout at the same starting commit.
- Start fresh Codex sessions with the same model and prompt.
- Run the baseline without explicit invocation and the comparison with `$scientific-code-documenter`.
- Save each diff and validation log, then score both independently.
- Record the model, date, commit, fixture, trigger result, scores, validation outcome, strengths, regressions, and follow-up work.

Exact repository-specific commands are maintained in the root `README.md` after the shared scripts and commits exist.

## Real-repository acceptance

Completed acceptance now covers an authorized scientific Python repository and a production-style ORCA Shell workflow repository. The ORCA run reviewed nine scripts, exercised three controlled edit pairs with isolated mocks and dry runs, and preserved generated calculation inputs and workflow contracts without launching an expensive calculation. See the [v0.3.0 sanitized summary](../../docs/evaluations/scientific-code-documenter-v0.3.0.md).

Future acceptance should add an authorized HTML/reporting or scientific-document repository and broader scheduler or cluster environments. Use the reusable prompts in `prompts.yaml`; do not use private code without authorization.
