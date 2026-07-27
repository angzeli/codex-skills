# Codex skills collection

This repository is the editable source of truth for a growing collection of custom Codex skills. Each direct child of `skills/` is an independent runtime package; collection documentation, evaluation suites, and shared tooling stay outside those packages.

## Source and runtime installations

Edit skills in this repository. Runtime discovery uses one symbolic link per skill under `$HOME/.agents/skills/<name>`, pointing to `skills/<name>/`. Do not link or copy the repository root into the runtime skills directory.

```text
codex_skills/
├── skills/              # Independently installable runtime skills
├── evals/               # Prompts, fixtures, rubrics, and recorded-result templates
├── scripts/             # Shared collection management tools
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## Skill catalogue

No skill has been committed to the collection yet. New skills begin as experimental and graduate only after controlled evaluation and real-repository acceptance testing.

## Validate and install

The collection-level commands are designed to work from any checkout path once the shared tooling is present:

```sh
./scripts/check_skill.sh <name>
./scripts/check_all_skills.sh
./scripts/run_fixture_checks.sh <name>
./scripts/install_skill.sh <name>
./scripts/install_all_skills.sh
```

Installers derive the repository root from their own location and create individual links under `$HOME/.agents/skills`. They must preserve conflicting installations through a timestamped backup rather than deleting content silently.

## Invoke a skill

Invoke a skill explicitly by naming it in a prompt, for example `$<skill-name>`. Codex may also select a skill implicitly when a request closely matches the skill frontmatter description. Evaluation prompt matrices should test both paths as well as false triggers and ambiguous boundary cases.

## Add another skill

1. Create `skills/<name>/SKILL.md` using a kebab-case directory and matching frontmatter name.
2. Add only runtime-required references, scripts, templates, or assets beside the skill file.
3. Create `evals/<name>/` with trigger prompts, synthetic fixtures, a rubric, and result-recording instructions.
4. Run the shared validation and fixture checks.
5. Dry-run and then perform the individual installation.
6. Update this catalogue and `CHANGELOG.md`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete workflow.

## Evaluation and status

Structural validation proves that a skill can be discovered and parsed; it does not prove usefulness. Evaluate skills through controlled A/B runs from identical commits, using the same model and prompt in fresh sessions, then save diffs and validation logs and score both outputs manually. Include behavior-preservation, adversarial, false-trigger, and real-repository checks.

Unless a catalogue entry says otherwise, every skill is experimental. Do not describe a skill as stable or effective merely because installation and structural checks pass.

## Privacy and publication

Use synthetic, public-safe fixtures. Before sharing changes, inspect staged and tracked files for credentials, personal absolute paths, private server details, proprietary names, unpublished research, copied third-party code, and generated artifacts. Confirm publication rights separately from technical validation.

## Contributing and licence

Keep commits coherent and reviewable, preserve unrelated work, and update evaluations alongside behavior changes. This collection is available under the [MIT License](LICENSE).
