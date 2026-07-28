# scientific-code-documenter v0.1.0 validation

## Version and status

- Version: `scientific-code-documenter` v0.1.0
- Release status: experimental first release
- Accepted runtime snapshot SHA-256: `3a58a55702bde8061fb3db226173da80e6f0336049ca679e4a70eb312069312e`
- Deterministic manifest SHA-256: `c55d3a7cb122b2b253f0d7c56edef349b13c75fdd08ffef1abd53f9563e79c4e`

The release runtime is byte-identical to the immutable snapshot used for the passing real-repository acceptance test.

## Synthetic controlled A/B evaluation

Five synthetic fixtures compared baseline and skill-assisted edits from identical starting states:

| Fixture | Baseline | Skill | Outcome |
| --- | ---: | ---: | --- |
| Documentation | 21 | 23 | Skill win |
| Photocatalysis | 17 | 22 | Skill win |
| Quantum | 21 | 21 | Tie |
| Cramped | 16 | 22 | Skill win |
| Restraint | 19 | 24 | Skill win |
| **Total** | **94/120** | **112/120** | **4 wins, 1 tie, 0 losses** |

All skill candidates passed their independent behavior checks and received the maximum behavior-preservation score. The main gains were in function documentation, evidence-grounded scientific context, readability, and focused refactoring quality.

An earlier photocatalysis run exposed semantic overconfidence: plausible units, physical roles, correction meanings, and conversion semantics were documented without sufficient evidence. The evidence-before-interpretation correction passed the targeted regression. The final five-fixture run contained no unsupported scientific interpretation and retained useful documentation where units and conventions were supported.

## Trigger and boundary evaluation

- Explicit invocation: 5/5 (100%).
- Positive implicit triggering: 10/10 (100%).
- Negative false triggers: 0/9 valid runs (0%); one invalid run was excluded because an unrelated native browser event broke the isolation condition.
- Original boundary matrix after correction: 6/6 passed.
- Additional review-only and explanation-only regressions: 2/2 passed with byte-identical source files.
- Across all eight valid boundary sessions, material scope failures and unsupported scientific interpretations were both zero.
- The stale-comment case reported the issue and proposed neutral wording without editing the file.
- Documentation and photocatalysis edit-mode smoke checks each changed one intended file, passed all four behavior tests, and were judged useful. The photocatalysis smoke check also passed 100 exact differential input sets.

These results support the tested trigger and scope boundaries; they do not establish universal trigger behavior.

## Real-repository acceptance

Acceptance used an immutable, remote-free snapshot of a scientific Python XPS fitting workbench:

- 47 Python files reviewed; review-only mode made zero changes.
- Workflow script edit: 23/24.
- Library module edit: 24/24.
- Workflow behavior checks matched an exact 21-file manifest, normalized workflow JSON, three CSV files, and six PNG files.
- The library module preserved its public interface and had an equivalent executable AST after removing documentation-only nodes.
- Syntax, repository-wide lint and formatting checks, configured type checks, targeted tests, and import smoke checks passed for the relevant candidates.
- Raw full-suite execution produced 119 passes and one identical launcher failure on untouched and edited snapshots; exposing the source explicitly produced 120/120 passes for all three snapshots. The launcher failure was therefore classified as a pre-existing environment limitation.

The skill source, target source, global skill state, and prior evaluation evidence were preserved by the acceptance run.

## Methodology

Evaluation used neutral repositories and public-safe synthetic fixtures, fresh ephemeral candidate sessions, isolated skill discovery, and identical controlled A/B prompts except for explicit skill invocation. Outputs were judged blind to condition, and behavior was checked independently of qualitative scoring. Real-repository candidates came from immutable, remote-free source and skill snapshots so acceptance could be tied to one exact runtime hash.

Tracked materials are available in the [evaluation overview](../../evals/scientific-code-documenter/README.md), [prompt matrix](../../evals/scientific-code-documenter/prompts.yaml), [scoring rubric](../../evals/scientific-code-documenter/rubric.md), and [synthetic fixtures](../../evals/scientific-code-documenter/fixtures/). Detailed raw runs remain local, ignored audit evidence and are not part of the release.

## Known limitations

- Coverage is substantial but not universal, and v0.1.0 is not a guarantee of correctness.
- The strongest real-repository evidence is currently for scientific Python.
- Other supported languages have fixture-level rather than real-repository validation.
- Documentation helpers may intentionally remain concise when the source does not support more detail.
- One raw `pytest` launcher failure was environment-dependent and reproduced on untouched source.
- Users should review scientific documentation edits before merging them.
