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
| `scientific-code-documenter` | Improve scientific and technical code documentation and readability while preserving behavior | Experimental v0.2.0; validated with controlled Python, Shell, LaTeX, HTML/CSS/JavaScript, trigger, boundary, and scientific Python acceptance tests |

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
- “Clarify this Shell workflow's aggregate-error behavior without changing its exit codes.”
- “Organize these LaTeX macros while preserving labels, rendered content, and the template workaround.”
- “Make this scientific dashboard easier to maintain without changing its DOM or CSV contracts.”

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

`scientific-code-documenter` v0.2.0 retains the accepted v0.1.0 runtime unchanged. Its new six-fixture controlled suite scored 159/162 with the skill versus 145/162 baseline: four wins, two ties, and no losses. Contract checks covered Shell aggregate failure, exit codes, manifests, ORCA inputs, and review-only restraint; LaTeX compilation, labels, macros, conditional content, rendered text, and fragile templates; and HTML DOM, accessibility, CSV bytes, ordering, scaling, and generated snapshots. Cross-language trigger checks passed explicit invocation, implicit discovery, negative, and zero-edit boundary gates.

Scientific Python remains the only completed real-repository acceptance. Shell, LaTeX, and HTML/CSS/JavaScript evidence is synthetic and contract-based, including generated- and fragile-file restraint; it must not be described as real-repository validation. See the [sanitized v0.2.0 evaluation summary](docs/evaluations/scientific-code-documenter-v0.2.0.md) for exact results and limitations. The skill remains experimental and scientific edits still require human review.

## Privacy and publication

Use synthetic, public-safe fixtures. Before sharing changes, inspect staged and tracked files for credentials, personal absolute paths, private server details, proprietary names, unpublished research, copied third-party code, and generated artifacts. Confirm publication rights separately from technical validation.

## Contributing and licence

Keep commits coherent and reviewable, preserve unrelated work, and update evaluations alongside behavior changes. This collection is available under the [MIT License](LICENSE).
