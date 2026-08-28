# Manual scoring rubric

Score each category from 0 to 3. Record evidence from the diff and validation log rather than inferring intent.

| Category | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Readability | Harder to scan or substantially churned | Minor cosmetic gains; major density remains | Clearer structure with a few avoidable issues | Focused structure, names, spacing, and flow materially improve scanning |
| Function documentation | Missing, misleading, or mechanical | Some non-trivial interfaces or cell inputs/outputs documented poorly | Important interfaces and notebook flow documented with small omissions | Concise, language-appropriate contracts cover purpose, cell inputs/outputs, and meaningful failures |
| Scientific context | Invented or materially wrong | Key units, shapes, conventions, or evidence limits remain ambiguous | Most relevant context and uncertainty are explicit without guessing | Contracts are precise, evidence-classified, and preserve unknown scientific meaning |
| Comment quality | Narrates syntax, duplicates Markdown, or uses repetitive AI-like phrasing | Too sparse, verbose, generic, or reluctant to prune | Mostly useful with limited redundancy | Human-sounding comments explain only real contracts; obvious or duplicate commentary is removed or consolidated |
| Behavior preservation | Any syntax, API, format, test, or numerical regression | No detected regression but validation is inadequate | Checks pass but material behavior remains unprotected | All relevant checks pass and public, numerical, ordering, and file-format behavior is preserved |
| Scope discipline | Unrequested rewrite or generated/vendor edits | Significant unrelated formatting, notebook churn, or risky refactor | Mostly focused with small avoidable churn | Minimal, reviewable diff; role and risk are classified, and Tier-3 or suspicious work is reported rather than changed |

## Acceptance criteria

The quantitative score and comparative-win criteria in this section apply to controlled synthetic scored fixtures. Authorized real-notebook field acceptance uses the separate safety and restraint rule below.

- Average score: at least 15 out of 18.
- Per-fixture score: at least 13 out of 18.
- Behavior preservation: exactly 3 for every accepted fixture.
- Skill output clearly outperforms baseline in at least 75% of scored fixtures.
- No syntax, API, file-format, test, or numerical regression.
- Positive implicit-trigger accuracy: at least 90% across the recorded matrix.
- False-trigger rate: no higher than 10% across negative prompts.

Do not average away a behavior regression. A fixture that scores below any mandatory criterion fails even if the overall mean passes.

## Notebook hard gates

Evaluate these gates before qualitative scoring. Every applicable gate must pass.

| Gate | Required result |
| --- | --- |
| Original identity | Contract SHA-256 matches the exact immutable starting notebook |
| Protected structure | 100% preservation of formats, cells, order, IDs, types, metadata, attachments, execution counts, and outputs |
| Source allowlist | Zero changes outside explicitly permitted cell source fields |
| Textual locality | Zero byte changes outside intentionally changed allowlisted source values |
| Review/generated restraint | Review-only and generated notebooks remain byte-identical |
| Behavioral probe | Exact numerical values, missing-value behavior, and serialized order for applicable trusted synthetic fixtures |
| Idempotence | Fresh second skill pass creates zero tracked diff; notebook bytes remain identical to pass 1 |
| Validator health | Zero parse ambiguities, internal errors, timeouts, or unexplained changes |

### Synthetic scored editing fixtures

For controlled synthetic editing fixtures used to establish skill-added value, every notebook editing candidate must beat its baseline and the aggregate editing win threshold still applies. Review-only and generated restraint candidates may tie, but they must not lose or change a byte.

### Authorized real-notebook acceptance

The separately authorized real-notebook field acceptance tests safety and restraint rather than adding another synthetic skill-value benchmark. The skill candidate must not lose to baseline; an honest tie is acceptable only when the documentation task is legitimate rather than manufactured through under-editing and every applicable notebook hard gate passes.

## Result record

For each run, capture:

- model and interface;
- date and starting commit;
- fixture and exact prompt ID;
- whether implicit or explicit triggering occurred;
- baseline and skill scores by category;
- validation commands and exit status;
- saved diff and log paths;
- notebook role, risk tier and reasons, evidence classes, allowlisted source fields, validator report, and hard-gate outcomes;
- second-pass prompt, raw log, diff, and byte-identity result for accepted editing candidates;
- observed strengths and regressions;
- follow-up changes or unresolved ambiguity.
