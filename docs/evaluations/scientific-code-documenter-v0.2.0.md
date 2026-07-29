# scientific-code-documenter v0.2.0 validation

## Version status

- Version: `scientific-code-documenter` v0.2.0
- Release status: experimental release candidate
- Accepted runtime snapshot SHA-256: `3a58a55702bde8061fb3db226173da80e6f0336049ca679e4a70eb312069312e`
- Deterministic manifest SHA-256: `c55d3a7cb122b2b253f0d7c56edef349b13c75fdd08ffef1abd53f9563e79c4e`
- Runtime change from v0.1.0: none

v0.2.0 expands controlled language coverage and release evidence without changing the accepted v0.1.0 runtime instructions. The live runtime, immutable evaluation snapshot, and v0.1.0 runtime are byte-identical.

## Shell results

| Fixture | Baseline | Skill | Outcome |
| --- | ---: | ---: | --- |
| Editing: ORCA batch workflow | 24/27 | 27/27 | Skill win |
| Review: publishing workflow | 25/27 | 27/27 | Skill win |

Both candidates in both pairs passed independent Bash and behavior contracts. The editing pair preserved usage and error exit codes, aggregate-failure behavior, sorted processing, manifest headers and rows, status values, hashes, cleanup and `KEEP_TMP`, the dry-run formula, and the tested ORCA method, basis, solvent, directives, process count, and memory behavior. The skill candidate did not add blind `set -e`, `set -u`, or `pipefail` behavior.

The review-only skill candidate made no source change. It identified the unsupported unit-conversion claim, recommended neutral wording tied to the configured multiplication, and cautioned against strict-mode changes without an exit-semantics audit. The exact source hash, CSV bytes, configured scale behavior, manifest order, row counts, and hashes remained unchanged.

## LaTeX results

| Fixture | Baseline | Skill | Outcome |
| --- | ---: | ---: | --- |
| Editing: scientific report | 20/27 | 27/27 | Skill win |
| Review: fragile publisher template | 25/27 | 27/27 | Skill win |

Each candidate passed the independent LaTeX contract. The main fixture compiled twice without the conditional appendix and twice with it enabled. Both variants retained the expected two-page count, normalized visible-text hashes, labels and references, table rows and columns, macro values, scientific values, figure and table order, and negative-spacing workaround. The skill candidate improved source grouping and line breaking without changing rendered content or assigning a meaning to the configured shift.

The fragile template remained byte-identical in both review arms. Its one-page normalized visible output, publisher macro sequence and values, schema rows, and `\vspace{-0.4em}` workaround were preserved. The skill review did not infer physical meanings for `10^{-9}` or `0.037` and treated any future change as a coordinated contract migration.

## HTML results

| Fixture | Baseline | Skill | Outcome |
| --- | ---: | ---: | --- |
| Editing: XPS dashboard | 24/27 | 24/27 | Tie |
| Review: generated report snapshot | 27/27 | 27/27 | Tie |

Both dashboard candidates passed parsing and a dependency-free DOM execution harness. The checks retained required IDs, headers, filter values, accessible names, label associations and live-region behavior, seven raw rows and their order, `schemaVersion`, the public `window.__XPS_EXPORT__` shape, raw-intensity CSV export, exact header and row bytes, number formatting, the trailing newline, display scaling by `1e-3`, filter and reset behavior, component visibility, SVG point order, and the export filename.

The generated snapshot reviews made zero changes. Exact whitespace and element order, table values and `data-row-order` attributes, embedded JSON bytes, and schema version remained pinned by the source hash. Both reviews directed proposed improvements to the generator rather than reformatting the artifact.

## Cross-language aggregate

| Fixture | Baseline | Skill | Outcome |
| --- | ---: | ---: | --- |
| Shell editing | 24 | 27 | Skill win |
| Shell restraint | 25 | 27 | Skill win |
| LaTeX editing | 20 | 27 | Skill win |
| LaTeX restraint | 25 | 27 | Skill win |
| HTML editing | 24 | 24 | Tie |
| HTML restraint | 27 | 27 | Tie |
| **Total** | **145/162** | **159/162** | **4 wins, 2 ties, 0 losses** |

All six pairs were valid and all 12 candidates passed independent contracts. Every skill behavior-preservation score was 3/3. Every skill restraint score was 3/3, and all three restraint sources were byte-identical. The three editing outcomes were two required wins plus one no-worse-than-tie, exceeded here by two additional skill wins on the restraint fixtures.

| Category average | Baseline | Skill |
| --- | ---: | ---: |
| Readability | 2.67 | 3.00 |
| Documentation and structural clarity | 2.33 | 2.83 |
| Scientific-context accuracy | 2.67 | 3.00 |
| Comment quality | 2.67 | 3.00 |
| Behavior preservation | 3.00 | 3.00 |
| Scope discipline | 2.83 | 3.00 |
| Language convention adherence | 2.50 | 2.83 |
| Restraint and operating mode | 3.00 | 3.00 |
| Maintainability and refactoring quality | 2.50 | 2.83 |

The first LaTeX editing attempt was excluded after the model stream disconnected after contract execution but before a final response. Both LaTeX arms were rerun from a new identical neutral commit; no interrupted candidate was reused.

## Trigger results

| Metric | Result | Gate |
| --- | ---: | ---: |
| Explicit invocation | 3/3 (100%) | 100% |
| Positive implicit triggering | 9/9 (100%) | at least 90% |
| Negative false triggers | 0/6 (0%) | at most 10% |
| Review/generated boundaries | 6/6 skill reads, 0 edits | zero material failures |

Shell, LaTeX, and HTML each recorded 3/3 positive implicit reads, 0/2 negative reads, and 2/2 boundary reads with zero edits. There were no invalid sessions or candidate commits. Generated-file recommendations were directed upstream, and no generated file was edited. Loading was determined from captured `SKILL.md` read events rather than response self-report.

## Previous validation retained

Because the runtime did not change, the accepted v0.1.0 evidence remains applicable:

- Five-fixture Python controlled A/B: 112/120 with the skill versus 94/120 baseline; four wins and one tie.
- The targeted semantic-restraint correction prevented unsupported units, physical roles, and correction meanings.
- Corrected review-only and explanation-only boundaries made zero source changes.
- Authorized scientific Python acceptance reviewed 47 files without review-mode edits; selected workflow and library edits scored 23/24 and 24/24 while preserving tested outputs, interfaces, and executable structure.

No new five-fixture Python A/B or real-repository acceptance run was required because the runtime hash remained unchanged.

## Methodology

The six controlled fixtures are synthetic and public-safe. Each pair started from one neutral commit and used fresh ephemeral sessions with the same model, reasoning effort, prompt body, sandbox, CLI, and independent post-run contract. The comparison differed only by explicit skill invocation. Skill arms used an immutable runtime snapshot and recorded a skill read; baseline and blind-judge conditions exposed no user skills. Candidate mappings were randomized and hidden until structured judge output passed validation.

Tracked materials include the [evaluation overview](../../evals/scientific-code-documenter/README.md), [prompt matrix](../../evals/scientific-code-documenter/prompts.yaml), [rubric](../../evals/scientific-code-documenter/rubric.md), [fixture contracts](../../evals/scientific-code-documenter/fixtures/cross-language-contracts.md), and [synthetic fixtures](../../evals/scientific-code-documenter/fixtures/). Raw model events, diffs, mappings, and generated outputs remain ignored local audit evidence.

## Limitations

- Shell, LaTeX, and HTML validation is synthetic and contract-based; it is not real-repository validation.
- Python remains the only language with completed real-repository acceptance for this runtime.
- PDF byte identity was not required because TeX metadata can be nondeterministic; normalized visible text, labels, structure, and page counts were compared instead.
- HTML behavior was exercised through the available dependency-free local DOM harness, not a complete cross-browser matrix.
- Trigger measurements cover the recorded prompt matrix and do not establish universal discovery behavior.
- Human review remains required before scientific or technical documentation edits are merged.
- v0.2.0 remains experimental and does not guarantee correctness in every project.
