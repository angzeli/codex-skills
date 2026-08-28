# angze-code-style v0.4.0 validation

## Version status

- Version: `angze-code-style` v0.4.0
- Migration: clean-break rename from `scientific-code-documenter`; no compatibility alias
- Release status: experimental local release candidate
- Runtime behavior changed from v0.3.0: yes
- Real-notebook acceptance: passed
- Verdict: **READY FOR LOCAL REVIEW**
- Tracked runtime snapshot SHA-256: `7f79b22c4694717963966132967b1a03b4cf5790529e6c229ef2ef31920fad84`
- Integrity manifest: [`angze-code-style-v0.4.0.manifest.json`](angze-code-style-v0.4.0.manifest.json)
- Real-notebook record: [`angze-code-style-v0.4.0-real-notebook.md`](angze-code-style-v0.4.0-real-notebook.md)

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

After the clean-break rename, the same full 20-prompt matrix was rerun in fresh isolated sessions. All twenty sessions were valid: positives were 10/10 and negative activations were 0/10. The global skill inventory matched exactly after restoration. An initial path-sensitive detector undercount was corrected over the saved JSONL because the CLI resolved the isolated symlink to `runtime-snapshot/SKILL.md`; no session was rerun or replaced.

## Post-rename representative check

One explicit `$angze-code-style` editable-notebook run changed only the allowlisted source values and passed the strict notebook contract validator. A fresh second session read the same frozen runtime and left the first candidate byte-identical; the validator passed again. This is a rename-sensitive synthetic migration check, not real-notebook acceptance.

## Authorized real-notebook acceptance

An immutable snapshot of one authorized real tutorial notebook was accepted without exposing its personal path or substantive research content in tracked evidence. The snapshot contained 44 cells (30 Markdown and 14 code), nine stored outputs, no attachments, and notebook format 4.5.

Review-only inspection changed zero bytes and reported six categories of documentation or contract findings. A bounded task added a concise observable data/history contract to one existing Markdown cell. Baseline and skill candidates began from the same snapshot; both passed the strict validator and the honest human comparison was a tie. The skill introduced no unsupported scientific claims and was not materially worse than baseline.

For the skill candidate, protected-structure, metadata, output, attachment, execution-count, cell-ID, non-allowlisted-source, and serialization-locality violations were all zero. All 14 executable source values remained exactly equal to the snapshot. A fresh second skill session changed zero bytes and passed the validator again. The original notebook was unchanged and was not executed. This is bounded Markdown-only preservation evidence; general notebook equivalence is not claimed. Full sanitized details are in the [real-notebook acceptance record](angze-code-style-v0.4.0-real-notebook.md).

## Retained failed attempts

- One orchestration attempt used incompatible current CLI flags and exited before model launch; no candidate changed.
- Initial Python, Shell, and HTML candidates drifted on a second pass. The runtime added an explicit dirty-target preservation boundary, and all affected reruns became byte-identical.
- Deletion-only notebook-pruning attempts tied the baseline. The runtime's evidence-class wording was reconciled so visible missing-value and ordering operations are documented neutrally without inventing scientific purpose; the final retained candidate passed and won.

These attempts remain in the local result bundle and were not removed or scored as accepted outputs.

## Existing evidence and limitations

Historical v0.1–v0.3 scientific Python and ORCA Shell acceptance remains predecessor evidence only because v0.4 changes runtime instructions.

ShellCheck and `pdflatex` were unavailable. Required Shell syntax and dynamic contract checks passed; LaTeX static contracts passed, but rendered compilation did not run. Manual A/B scoring was not independently blind. The deterministic probe and bounded real-notebook acceptance are limited evidence, not general equivalence or scientific validation. Human scientific review remains mandatory.
