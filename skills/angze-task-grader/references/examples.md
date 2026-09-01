# Grading examples

Use these examples only to resolve boundaries. `Forbidden` names the most likely overengineering failure.

| # | Task | Tier | Overrides | Inspection | Validation | Forbidden |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Correct one README typo | T0 | None | Named paragraph | Read text and diff | Docs build or nearby rewriting |
| 2 | Remove a proven unused import | T0 | None | Target file | Syntax/import check and diff | Full suite or refactor |
| 3 | Correct a non-executable comment | T0 | None | Target lines | Textual review | New documentation section |
| 4 | Fix one obvious display label | T0 | None | Target template | Focused render/text check | Component redesign |
| 5 | Repair localized CLI handling of zero | T1 | None | CLI function and direct tests | Focused CLI regression | New argument framework |
| 6 | Fix a parser trailing-empty-field edge case | T1 | None | Parser and callers | Edge fixture plus parser tests | Parser rewrite |
| 7 | Correct one helper's off-by-one loop | T1 | None | Helper and call sites | Focused regression | Generic iteration library |
| 8 | Repair a known CI test path | T1 | None | Workflow and named command | Reproduce relevant command | CI redesign or full matrix |
| 9 | Correct one notebook Markdown instruction | T1 | None | Target cell and notebook contract | Structural/locality check | Notebook execution |
| 10 | Fix a two-line unit conversion | T1 | scientific/numerical | Function, uses, unit evidence | Hand-computable values, units, tolerance | Broad module refactor |
| 11 | Fix an adsorption-energy sign equation | T1 | scientific/numerical | Equation, references, callers | Sign-sensitive synthetic invariant | Renaming all energy APIs |
| 12 | Add one report output to an existing parser | T2 | None | Parser subsystem | Unit tests plus end-to-end report smoke | Reporting framework |
| 13 | Add one complete CLI subcommand | T2 | None | CLI subsystem and reused services | Units plus command smoke | Plugin architecture |
| 14 | Build one bounded CSV importer | T2 | None | Import subsystem | Fixture units plus import smoke | Generic ETL framework |
| 15 | Audit one caching subsystem without edits | T2 | None | Affected subsystem | Evidence-backed read-only checks | Fixing adjacent defects |
| 16 | Add one tutorial notebook | T2 | None | Tutorial conventions and linked helper | Structural check plus safe fresh-copy execution | Project-wide notebook validation |
| 17 | Refactor one related module cluster behind existing tests | T2 | None | Affected subsystem | Targeted units plus representative integration | Architecture migration |
| 18 | Fix ORCA normal-termination parsing | T3 | None | Parser, attempt identity, consumers | Truncated/restart/convergence fixtures | Running production ORCA |
| 19 | Change a VASP default affecting results | T3 | compatibility/cross-platform | Default precedence and resolved inputs | Input snapshots and scientific review | Production calculation without approval |
| 20 | Change a persistent CSV schema | T3 | None | Readers, writers, migration path | Old/new round trip and preservation | Silent rewrite of real data |
| 21 | Repair file locking around shared state | T3 | None | Critical section and failure paths | Deterministic contention test | Broad concurrency framework |
| 22 | Fix cross-platform path normalization | T3 | None | Path boundary and supported platforms | Focused platform cases | Unrelated portability cleanup |
| 23 | Diagnose a broad failure with unknown root cause | T3 | uncertainty | Dependency-aware until cause is bounded | Reproducer then regrade | Implementing speculative fixes |
| 24 | Change geometry-frame rotation semantics | T3 | None | Transform, frame consumers, provenance | Distance, orientation, round-trip invariants | Visual-only validation |
| 25 | Prepare a package release candidate | T4 | None | Release surface and identity | Declared full gate, build, clean install | Skipping mandatory release checks |
| 26 | Publish a package and tag | T4 | None | Release config, artifacts, remote identity | Full release and publication verification | Acting without explicit authorization |
| 27 | Perform a destructive database migration | T4 | None | Exact targets, migration, backup, rollback | Disposable rehearsal and recovery checks | Applying to live data first |
| 28 | Restore files over an existing workspace | T4 | None | Exact source/target and recoverability | Disposable restore rehearsal and integrity | Broad unresolved deletion or overwrite |
| 29 | Audit credential handling before distribution | T4 | None | Security and release boundary | Hostile review and required security gate | Publishing before blockers resolve |
| 30 | Explain Python dataclasses conceptually | No trigger | None | None | None | Creating an execution contract |
| 31 | Compare ORCA and CP2K conceptually | No trigger | None | None | None | Inspecting repositories |
| 32 | Draft an email about a bug | No trigger | None | None | None | Treating prose as a code task |

## Escalation examples

- Regrade a localized parser patch from T1 to T3 when the parsed field controls scientific provenance; add lineage and scientific validation while keeping the patch small.
- Regrade a bounded packaging change from T2 to T4 when the user requests public publication; add release identity, artifact, and clean-install gates.
- Regrade a CLI feature from T2 to T3 when it overwrites persistent user data; add data-safety and rollback checks.

## De-escalation examples

- Regrade a suspected subsystem bug from T2 to T0 after reproducing it as a README typo; edit only the text.
- Regrade a suspected schema migration from T3 to T1 when stored data is correct and only a UI label is wrong; test only the display path.
- Regrade an uncertain CI failure from T3 to T1 after identifying one missing test-only path; repair and rerun that job.
