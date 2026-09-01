# Validation matrix

Use the minimum check that can demonstrate the requested behavior and the maximum normally justified check absent new evidence. Explicit user and repository requirements override the ceiling.

| Category | Likely tier | Minimum validation | Maximum normally justified | Escalate when |
| --- | --- | --- | --- | --- |
| Docs-only | T0 | Read changed text and focused diff; check links only if changed | Targeted docs build or link check | Text is executable, generated, release-identifying, schema-defining, or scientifically normative |
| Localized Python patch | T1 | Focused regression plus syntax/import or directly relevant lint/type check | Affected module tests | Public API, persistence, scientific results, broad call graph, or uncertain root cause appears |
| Parser edge case | T1 | One regression fixture and parser unit tests | Parser subsystem integration test | Grammar changes broadly, input is persistent, compatibility-sensitive, or scientific |
| Bounded parser feature | T2 | Targeted units plus one end-to-end parse smoke | Affected parser subsystem | Schema migration, backward compatibility, provenance, or broad ambiguity appears |
| CLI | T1-T2 | Direct command behavior and focused tests | CLI integration/smoke suite | Command mutates data, changes public contracts, crosses platforms, or publishes artifacts |
| Notebook | T0-T2 | Structural/locality check; relevant cell logic test without re-execution unless requested | Fresh-copy execution of the bounded tutorial when safe and required | Scientific logic, stored outputs, metadata, execution state, environment, or expensive work changes |
| Persistent data schema | T3 | Old/new fixtures, migration and round-trip tests, preservation assertions | Relevant integration plus rollback/compatibility checks | Migration is destructive, irreversible, broad, or externally applied |
| Packaging | T2-T4 | Metadata consistency and targeted build/import checks | Build, clean install, package tests, artifact inspection | RC/publication, signing, tag identity, supported-version matrix, or public distribution is requested |
| CI/build failure | T1-T3 | Reproduce the failing job or closest local command and verify the focused fix | Affected workflow matrix | Credentials, publication, signing, cross-platform behavior, or unclear broad coupling appears |
| Migration | T3 | Forward migration, preservation, failure-path, and rollback fixture | Representative compatibility/data-safety suite | Destructive or irreversible effects, real external data, or broad compatibility migration appears |
| Release | T4 | Explicit repository release checklist and required configured gates, each run once | Full declared release matrix, clean install, artifact and identity checks only when applicable | Missing authorization, unavailable mandatory gate, signing/credential issue, or artifact mismatch blocks release |
| Scientific numerical core | T1-sized patch with T3 validation or T3 | Focused regression with units, signs, invariants, tolerances, and provenance | Relevant scientific integration and comparison to authoritative synthetic/reference values | Defaults, algorithms, convergence, expensive calculations, or conclusions may change |
| ORCA/Multiwfn workflow | T3 | Minimized public-safe outputs, parser/workflow fixtures, termination/convergence and provenance checks | Relevant synthetic workflow integration | Real calculations, licensed/private data, restart state, paths, charge/spin, or destructive replacement is involved |
| Cross-platform behavior | T3 | Focused tests on affected platform semantics or deterministic emulation | Relevant supported-platform matrix | Public API, filesystem semantics, packaging, or broad supported versions are affected |
| Concurrency/file locking | T3 | Deterministic contention regression and failure-path checks | Relevant stress/integration test | Data loss, deadlock, cross-platform locking, or external shared state is plausible |
| Destructive restore | T4 | Exact-target resolution, disposable restore rehearsal, integrity and rollback checks | Full authorized recovery procedure | Target identity, backup validity, credentials, or reversibility is uncertain |

## Selection rules

- Count each check by the distinct risk it covers; do not rerun equivalent checks.
- Use documented or evidently supported commands directly; do not probe command aliases merely to discover the interpreter or runner.
- Prefer focused behavior checks over full suites for T0-T2.
- Use a broader suite only when the patch crosses modules, repository policy requires it, or targeted failures reveal coupling.
- Do not install or upgrade dependencies merely to increase apparent coverage unless the task requires that environment.
- Do not launch a persistent server, watcher, external write, migration, or expensive calculation without task-specific need and authorization.
- If a check cannot run, record the exact limitation and strongest substitute.
