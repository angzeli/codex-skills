# Codex skills collection

This repository is the editable source of truth for a growing collection of custom Codex skills. Each direct child of `skills/` is an independent runtime package; collection documentation, evaluation suites, and shared tooling stay outside those packages.

New to Codex skills? Follow [Getting started](GETTING_STARTED.md) to install and use `angze-code-style`.

## Source and runtime installations

Edit skills in this repository. Runtime discovery uses one symbolic link per skill under `$HOME/.agents/skills/<name>`, pointing to `skills/<name>/`. Do not link or copy the repository root into the runtime skills directory.

```text
codex_skills/
├── skills/
│   ├── README.md
│   └── angze-code-style/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           ├── comment-examples.md
│           ├── jupyter-notebooks.md
│           └── scientific-contracts.md
├── evals/
│   ├── README.md
│   └── angze-code-style/
│       ├── fixtures/
│       ├── results/
│       ├── checks.sh
│       ├── prompts.yaml
│       └── rubric.md
├── scripts/             # Shared discovery, validation, fixture, and installation tools
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── GETTING_STARTED.md
├── LICENSE
└── README.md
```

## Skill catalogue

| Skill | Purpose | Status |
| --- | --- | --- |
| `angze-code-style` | Document and prune scientific code and Jupyter notebooks using explicit contract inventory, evidence classes, and risk grading | Experimental v0.4.0 release candidate; synthetic and authorized real-notebook acceptance plus controlled Python, Shell, LaTeX, HTML, trigger, restraint, and idempotence gates pass |
| `angze-task-grader` | Grade codebase and scientific-computing tasks and apply the minimum sufficient execution contract | Experimental v0.1.0rc1-ready; fresh 25/25 grading, 16/16 observed routing, dual-skill preservation, and deterministic CI gates pass, while stable speed and token savings remain unproven |

## Validate and install

The collection-level commands work from any checkout path:

```sh
./scripts/list_skills.sh
./scripts/check_skill.sh angze-code-style
./scripts/check_all_skills.sh
./scripts/run_fixture_checks.sh angze-code-style

./scripts/install_skill.sh --dry-run angze-code-style
./scripts/install_skill.sh angze-code-style
./scripts/install_all_skills.sh --dry-run
./scripts/install_all_skills.sh
```

Use placeholders for future skills:

```sh
./scripts/check_skill.sh <name>
./scripts/run_fixture_checks.sh <name>
./scripts/install_skill.sh <name>
```

Installers derive the repository root from their own location and create individual links under `$HOME/.agents/skills`. A conflicting file, directory, or link is moved to `<name>.backup-<timestamp>` before installation; it is never deleted silently. Open a new Codex session after the first installation so skill discovery refreshes, then check that the skill appears in `/skills`.

## Invoke a skill

Use `angze-code-style` for review-only documentation assessments, focused docstring and comment work, or behavior-preserving readability improvements. Invoke it explicitly for a review-only request:

```text
$angze-code-style
Review this file for readability and documentation quality. Do not modify it.
```

Codex may also select it implicitly for requests such as:

- “Add concise docstrings and document the units and NumPy array shapes without changing calculations.”
- “Replace these repetitive AI-like comments with explanations of the non-obvious data-ordering constraints.”
- “Clarify this Shell workflow's aggregate-error behavior without changing its exit codes.”
- “Organize these LaTeX macros while preserving labels, rendered content, and the template workaround.”
- “Make this scientific dashboard easier to maintain without changing its DOM or CSV contracts.”
- “Document this notebook's cell inputs, missing-value rules, ordering, and stored-output state without executing it.”
- “Prune syntax-narrating notebook comments while preserving outputs, metadata, execution counts, and cell identity.”

For an editing-mode request:

```text
$angze-code-style
Apply only high-confidence documentation and readability improvements to this file. Preserve calculations, public interfaces, file formats, and numerical behaviour.
```

Units, shapes, conventions, physical roles, and numerical context should be documented precisely only when supported by code, tests, configuration, repository documentation, or user-provided evidence. Directly observable operations may be described neutrally; unknown scientific meaning stays unresolved. A review-only or “do not edit” instruction takes precedence over opportunities to fix stale comments or improve code.

Jupyter notebooks are treated as structured artifacts. The skill classifies notebook role and risk before editing, preserves cell identity, metadata, execution counts, attachments, and stored outputs by default, and does not execute notebooks merely to refresh state. Generated, unknown-role, and protected analysis notebooks normally remain review-only.

Ordinary debugging, dependency upgrades, test execution, and unrelated feature work should not trigger the skill merely because code is present.

## Add another skill

1. Create `skills/<name>/SKILL.md` using a kebab-case directory and matching frontmatter name.
2. Add only runtime-required references, scripts, templates, or assets beside the skill file.
3. Create `evals/<name>/` with trigger prompts, synthetic fixtures, a rubric, and result-recording instructions.
4. Add an executable `evals/<name>/checks.sh` when fixtures support deterministic checks.
5. Run the shared validation and fixture checks.
6. Dry-run and then perform the individual installation.
7. Update this catalogue and `CHANGELOG.md`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete workflow.

## Evaluation and status

Structural validation proves that a skill can be discovered and parsed; it does not prove usefulness. Evaluation therefore combines controlled A/B runs, trigger and scope-boundary measurements, independent behavior checks, adversarial fixtures, and authorized real-repository acceptance.

`angze-code-style` v0.4.0 changes runtime behavior and completes a clean-break rename from `scientific-code-documenter`. It adds scientific/artifact contract inventory, `evidence-backed` / `observable-only` / `unknown` classification, Tier 0–3 risk grading, structured review findings, conservative notebook policy, comment pruning, and repeated-pass stability.

Controlled synthetic evaluation covered an editable notebook, review-only stale claim, over-commented notebook, generated notebook, and representative Python, Shell, LaTeX, and HTML fixtures. The accepted skill candidates averaged 17.5/18, won all six editing comparisons, passed every behavior and notebook hard gate, and were byte-stable on fresh second passes. The initial trigger matrix scored 10/10 positives with one false trigger; the full post-rename rerun scored 10/10 positives and 0/10 negatives. A separately authorized real tutorial-notebook snapshot passed zero-edit review, controlled A/B editing, strict preservation validation, behavior-preservation, and fresh-session idempotence. Scoring was manual rather than independently blind. ShellCheck and `pdflatex` were unavailable in the original local acceptance environment, so Shell syntax/dynamic contracts and static LaTeX contracts were used. ShellCheck subsequently ran and passed under the existing policy in remote CI on Ubuntu for Python 3.11 and 3.12; rendered `pdflatex` compilation remains unavailable. See the [sanitized v0.4.0 evaluation summary](docs/evaluations/angze-code-style-v0.4.0.md), [real-notebook acceptance record](docs/evaluations/angze-code-style-v0.4.0-real-notebook.md), and [integrity manifest](docs/evaluations/angze-code-style-v0.4.0.manifest.json).

Historical v0.1–v0.3 scientific Python and ORCA Shell evidence remains useful predecessor evidence, but it is not accepted as proof for the changed v0.4 runtime. The real-notebook acceptance established bounded Markdown-only preservation, not general notebook equivalence or scientific correctness. The skill remains experimental, and human scientific review remains mandatory.

## Privacy and publication

Use synthetic, public-safe fixtures. Before sharing changes, inspect staged and tracked files for credentials, personal absolute paths, private server details, proprietary names, unpublished research, copied third-party code, and generated artifacts. Confirm publication rights separately from technical validation.

## Contributing and licence

Keep commits coherent and reviewable, preserve unrelated work, and update evaluations alongside behavior changes. This collection is available under the [MIT License](LICENSE).
