# Synthetic behavioral A/B smoke report

## Scope

The main smoke used six synthetic fixtures: T0 README typo, T1 CLI zero handling, T1 scientific unit conversion, T2 parser summary, T3 CSV migration, and T4 release-candidate preparation. Every baseline and treatment arm ran in a fresh temporary Git repository from the same canonical fixture bytes. Treatment installed the skill only under the disposable repository and invoked it explicitly.

The first six-case pass exposed excess treatment inspection and validation. The runtime was tightened, then the affected T0, scientific T1, and T4 pairs were rerun. A final scientific pair verified that validation left no `__pycache__` artifact.

## Correctness and scope

- All observed baseline and treatment arms passed their independent fixture acceptance command.
- No treatment correctness regression occurred.
- Treatment never increased unrelated-file changes in the accepted final pairs.
- Changed-file counts were equal in the final T0, scientific T1, and T4 comparisons.
- Human diff review found no speculative dependency, module, factory, interface, configuration framework, or unrelated cleanup in treatment.
- The T3 treatment added focused migration failure-path tests within the allowed case scope; this was judged useful rather than speculative.

## Final affected-pair observations

Skill-loading reads are excluded from task-command counts but remain included in wall time and token totals. Validation counts represent detected operations inside compound shell commands, not only outer shell invocations.

| Case | Correct baseline/treatment | Changed files B/T | Validation operations B/T | Task commands B/T | Wall seconds B/T | Input tokens B/T |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| T0 docs typo | yes / yes | 1 / 1 | 1 / 1 | 3 / 2 | 30.1 / 31.8 | 132,790 / 151,154 |
| T1 scientific units, final repeat | yes / yes | 1 / 1 | 3 / 3 | 3 / 4 | 43.1 / 62.3 | 136,186 / 227,133 |
| T4 release RC, final repeat | yes / yes | 3 / 3 | 7 / 4 | 9 / 9 | 84.6 / 78.1 | 253,593 / 244,181 |

The scientific pair varied across repeats: one prior post-refinement treatment used fewer task commands, less wall time, and fewer input tokens than its baseline, while the final artifact-preservation repeat was slower and larger. This does not establish stable speed or token savings.

## Interpretation

The controlled evidence supports correctness, scope restraint, proportional changed-file counts, and equal-or-lower final validation-operation counts for the sampled T0/T1 pairs. It does not support a general claim that the skill reduces wall time, command count, or token usage. The skill itself adds context and loading cost, and model-run variance was material.

Other globally installed skills remained available to Codex. `graphify` loaded in some baseline arms and in the positive routing probe, so the comparison isolates absence versus explicit presence of `angze-task-grader`, not a completely skill-free baseline.

No token-savings claim is made. Token values above were genuinely present in the Codex JSON event stream and are reported only as observations from these runs.

Synthetic evaluation establishes controlled behavioral evidence, not proof of performance on every real repository.
