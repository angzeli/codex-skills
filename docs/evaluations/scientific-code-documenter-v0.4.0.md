# scientific-code-documenter v0.4.0 validation

## Version status

- Version: `scientific-code-documenter` v0.4.0, before the final `angze-code-style` migration
- Release status: experimental local release candidate
- Runtime behavior changed from v0.3.0: yes
- Real-notebook acceptance: pending explicit authorization
- Provisional verdict: **PARTIALLY READY — REAL-NOTEBOOK ACCEPTANCE PENDING**

## Methodology

The controlled comparison used fresh ephemeral Codex CLI sessions with `gpt-5.6-terra`, medium reasoning, workspace-write sandboxes, identical synthetic starting files, and a zero-user-skill baseline. Candidate sessions exposed one frozen runtime snapshot and explicitly invoked the skill for A/B editing and restraint runs. Independent fixture validators ran after every candidate.

The eight pairs covered editable notebook documentation, notebook review restraint, notebook comment pruning, generated-notebook restraint, Python, Shell, LaTeX, and HTML. Fresh second sessions repeated the same skill prompt against all six accepted editing candidates. Raw prompts, event logs, diffs, responses, validation records, failed attempts, and second-pass evidence remain in the ignored local result bundle.

Scoring was a manual evidence-based side-by-side review of saved diffs and validation results. It was not randomized or independently blind; this limits the strength of comparative claims.

## A/B result

| Fixture | Baseline | Skill | Outcome |
| --- | ---: | ---: | --- |
| Editable notebook | 17/18 | 18/18 | Skill win |
| Notebook pruning | 14/18 | 17/18 | Skill win |
| Python | 14/18 | 17/18 | Skill win |
| Shell | 16/18 | 17/18 | Skill win |
| LaTeX | 16/18 | 18/18 | Skill win |
| HTML | 15/18 | 18/18 | Skill win |
| **Average** | **15.3/18** | **17.5/18** | **6 wins, 0 ties, 0 losses** |

Every accepted skill fixture scored at least 17/18 and behavior preservation was 3/3 throughout. Review-only and generated notebooks were unscored byte-identical ties.

The baseline Python candidate added public annotations and asserted more scientific interpretation than the repository established. The accepted skill candidate retained public signatures and described the threshold neutrally. The skill notebook candidate explicitly kept the scale factor's units and scientific meaning unknown. The pruning candidate consolidated visible `None` filtering and ascending ordering once while deleting syntax narration. Shell, LaTeX, and HTML candidates documented concrete contracts more locally and concisely.

## Notebook hard gates

| Gate | Result |
| --- | --- |
| Protected notebook structure | 100% preserved |
| Unexpected output, metadata, attachment, cell-ID, or execution-count changes | 0 |
| Non-allowlisted source changes | 0 |
| Bytes outside intended source values | 0 changes |
| Review-only and generated notebooks | 0 changed bytes |
| Deterministic numerical, missing-value, and ordering probe | Exact pass |
| Fresh second-pass idempotence | 6/6 editing candidates byte-identical |
| Accepted-candidate validator failures | 0 |

The validator uses strict standard-library JSON parsing, exact original hashes, explicit source selectors, protected-field comparison, raw JSON span masking, line budgets, Python AST comparison for comment/docstring-only edits, and an optional trusted synthetic probe. It fails closed on malformed input, stale selectors, ambiguity, serialization churn, or internal error.

## Trigger result

Ten positive implicit prompts covered Python, Shell, LaTeX, HTML, notebook documentation, notebook readability, data contracts, and comment pruning. All ten activated or read the skill. Ten negative prompts covered debugging, dependencies, tests, performance, data analysis, notebook execution, crashes, methodology, and features. One notebook feature prompt read the skill, for a 10% false-trigger rate.

Thus positive accuracy was 100% and false triggering was 10%, meeting the release thresholds. The feature false positive is retained as a known limitation.

## Retained failed attempts

- One orchestration attempt used incompatible current CLI flags and exited before model launch; no candidate changed.
- Initial Python, Shell, and HTML candidates drifted on a second pass. The runtime added an explicit dirty-target preservation boundary, and all affected reruns became byte-identical.
- Deletion-only notebook-pruning attempts tied the baseline. The runtime's evidence-class wording was reconciled so visible missing-value and ordering operations are documented neutrally without inventing scientific purpose; the final retained candidate passed and won.

These attempts remain in the local result bundle and were not removed or scored as accepted outputs.

## Existing evidence and limitations

Historical v0.1–v0.3 scientific Python and ORCA Shell acceptance remains predecessor evidence only because v0.4 changes runtime instructions.

No notebook owner explicitly authorized a real immutable notebook snapshot. Per the release boundary, no arbitrary personal or research notebook was substituted. Real-notebook zero-edit review and controlled baseline-versus-skill editing remain pending.

ShellCheck and `pdflatex` were unavailable. Required Shell syntax and dynamic contract checks passed; LaTeX static contracts passed, but rendered compilation did not run. The deterministic notebook probe is limited fixture evidence, not general equivalence or scientific validation. Human scientific review remains mandatory.
