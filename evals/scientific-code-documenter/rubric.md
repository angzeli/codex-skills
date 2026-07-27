# Manual scoring rubric

Score each category from 0 to 3. Record evidence from the diff and validation log rather than inferring intent.

| Category | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Readability | Harder to scan or substantially churned | Minor cosmetic gains; major density remains | Clearer structure with a few avoidable issues | Focused structure, names, spacing, and flow materially improve scanning |
| Function documentation | Missing, misleading, or mechanical | Some non-trivial interfaces documented poorly | Important interfaces documented with small omissions | Concise, language-appropriate contracts cover purpose and meaningful failures |
| Scientific context | Invented or materially wrong | Key units, shapes, or conventions remain ambiguous | Most relevant context is explicit without guessing | Units, shapes, domains, assumptions, and distinctions are precise and evidence-based |
| Comment quality | Narrates syntax or uses repetitive AI-like phrasing | Too sparse, verbose, or generic | Mostly useful with limited redundancy | Human-sounding comments explain only intent, constraints, conventions, or safeguards |
| Behavior preservation | Any syntax, API, format, test, or numerical regression | No detected regression but validation is inadequate | Checks pass but material behavior remains unprotected | All relevant checks pass and public, numerical, ordering, and file-format behavior is preserved |
| Scope discipline | Unrequested rewrite or generated/vendor edits | Significant unrelated formatting or risky refactor | Mostly focused with small avoidable churn | Minimal, reviewable diff; risky or suspicious logic is reported rather than changed |

## Acceptance criteria

- Average score: at least 15 out of 18.
- Per-fixture score: at least 13 out of 18.
- Behavior preservation: exactly 3 for every accepted fixture.
- Skill output clearly outperforms baseline in at least 75% of scored fixtures.
- No syntax, API, file-format, test, or numerical regression.
- Positive implicit-trigger accuracy: at least 90% across the recorded matrix.
- False-trigger rate: no higher than 10% across negative prompts.

Do not average away a behavior regression. A fixture that scores below any mandatory criterion fails even if the overall mean passes.

## Result record

For each run, capture:

- model and interface;
- date and starting commit;
- fixture and exact prompt ID;
- whether implicit or explicit triggering occurred;
- baseline and skill scores by category;
- validation commands and exit status;
- saved diff and log paths;
- observed strengths and regressions;
- follow-up changes or unresolved ambiguity.
