# Codex skills collection

This repository is the editable source of truth for a growing collection of custom Codex skills. Each direct child of `skills/` is an independent runtime package; collection documentation, evaluation suites, and shared tooling stay outside those packages.

## Source and runtime installations

Edit skills in this repository. Runtime discovery uses one symbolic link per skill under `$HOME/.agents/skills/<name>`, pointing to `skills/<name>/`. Do not link or copy the repository root into the runtime skills directory.

```text
codex_skills/
├── skills/
│   ├── README.md
│   └── scientific-code-documenter/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/comment-examples.md
├── evals/
│   ├── README.md
│   └── scientific-code-documenter/
│       ├── fixtures/
│       ├── results/
│       ├── checks.sh
│       ├── prompts.yaml
│       └── rubric.md
├── scripts/             # Shared discovery, validation, fixture, and installation tools
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Skill catalogue

| Skill | Purpose | Status |
| --- | --- | --- |
| `scientific-code-documenter` | Improve scientific and technical code documentation and readability while preserving behavior | Experimental v0.1.0; validated with controlled synthetic, trigger, boundary, and scientific Python acceptance tests |

## Validate and install

The collection-level commands work from any checkout path:

```sh
./scripts/list_skills.sh
./scripts/check_skill.sh scientific-code-documenter
./scripts/check_all_skills.sh
./scripts/run_fixture_checks.sh scientific-code-documenter

./scripts/install_skill.sh --dry-run scientific-code-documenter
./scripts/install_skill.sh scientific-code-documenter
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

Use `scientific-code-documenter` for review-only documentation assessments, focused docstring and comment work, or behavior-preserving readability improvements. Invoke it explicitly for a review-only request:

```text
$scientific-code-documenter
Review this file for readability and documentation quality. Do not modify it.
```

Codex may also select it implicitly for requests such as:

- “Add concise docstrings and document the units and NumPy array shapes without changing calculations.”
- “Replace these repetitive AI-like comments with explanations of the non-obvious data-ordering constraints.”

For an editing-mode request:

```text
$scientific-code-documenter
Apply only high-confidence documentation and readability improvements to this file. Preserve calculations, public interfaces, file formats, and numerical behaviour.
```

Units, shapes, conventions, physical roles, and numerical context should be documented only when supported by code, tests, configuration, repository documentation, or user-provided evidence. Uncertainty should be stated rather than converted into scientific fact. A review-only or “do not edit” instruction takes precedence over opportunities to fix stale comments or improve code.

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

`scientific-code-documenter` v0.1.0 passed its five-fixture controlled A/B suite (112/120 versus 94/120), tested explicit and implicit trigger gates, corrected review-only boundary regressions, and passed acceptance on a scientific Python repository without changing reviewed files or tested behavior. The strongest real-repository evidence is currently Python; other supported languages remain fixture-validated. See the [sanitized v0.1.0 evaluation summary](docs/evaluations/scientific-code-documenter-v0.1.0.md) for methods, exact results, and limitations. The skill remains experimental and scientific edits still require human review.

## Privacy and publication

Use synthetic, public-safe fixtures. Before sharing changes, inspect staged and tracked files for credentials, personal absolute paths, private server details, proprietary names, unpublished research, copied third-party code, and generated artifacts. Confirm publication rights separately from technical validation.

## Contributing and licence

Keep commits coherent and reviewable, preserve unrelated work, and update evaluations alongside behavior changes. This collection is available under the [MIT License](LICENSE).
