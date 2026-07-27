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
| `scientific-code-documenter` | Improve scientific and technical code documentation and readability while preserving behavior | Experimental; structurally and synthetically checked, not yet A/B or real-repository validated |

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

Invoke the current skill explicitly:

```text
$scientific-code-documenter
Review this file for readability and documentation quality. Do not modify it.
```

Codex may also select it implicitly for requests such as:

- “Add concise docstrings and document the units and NumPy array shapes without changing calculations.”
- “Replace these repetitive AI-like comments with explanations of the non-obvious data-ordering constraints.”

Ordinary debugging, dependency upgrades, test execution, and unrelated feature work should not trigger it merely because code is present.

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

Structural validation proves that a skill can be discovered and parsed; it does not prove usefulness. Evaluate skills through controlled A/B runs from identical commits, using the same model and prompt in fresh sessions, then save diffs and validation logs and score both outputs manually. Include behavior-preservation, adversarial, false-trigger, and real-repository checks.

The current fixture suite checks Python numerical outputs and file formatting, HTML/CSS integrity, shell syntax, adversarial constants and ordering, and LaTeX compilation when available. It does not automate subjective rubric scoring or measure implicit-trigger accuracy.

### Controlled A/B procedure

The initial evaluation base is commit `16552f9c065b6d02bbd2c40b1e7018ff7cc6e20e` on `main`. Create sibling worktrees outside the main checkout:

```sh
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_PARENT=$(dirname "$REPO_ROOT")
EVAL_BASE=16552f9c065b6d02bbd2c40b1e7018ff7cc6e20e
BASELINE_WT="$REPO_PARENT/codex-skills-ab-baseline"
SKILL_WT="$REPO_PARENT/codex-skills-ab-skill"

git worktree add --detach "$BASELINE_WT" "$EVAL_BASE"
git worktree add --detach "$SKILL_WT" "$EVAL_BASE"
```

Independent Codex sessions are not launched by repository tooling. Open two fresh tasks manually, select the same model, and use one worktree per task. Give the baseline task this prompt:

```text
Apply only high-confidence documentation and readability improvements to evals/scientific-code-documenter/fixtures/python/spectrum_pipeline.py. Preserve calculations, public interfaces, file formats, and numerical behaviour.
```

Give the skill task the same request, preceded only by the explicit invocation:

```text
$scientific-code-documenter
Apply only high-confidence documentation and readability improvements to evals/scientific-code-documenter/fixtures/python/spectrum_pipeline.py. Preserve calculations, public interfaces, file formats, and numerical behaviour.
```

Save diffs and validation logs back to the ignored results directory:

```sh
git -C "$BASELINE_WT" diff -- evals/scientific-code-documenter/fixtures/python/spectrum_pipeline.py > "$REPO_ROOT/evals/scientific-code-documenter/results/baseline.diff"
git -C "$SKILL_WT" diff -- evals/scientific-code-documenter/fixtures/python/spectrum_pipeline.py > "$REPO_ROOT/evals/scientific-code-documenter/results/skill.diff"

"$BASELINE_WT/scripts/run_fixture_checks.sh" scientific-code-documenter > "$REPO_ROOT/evals/scientific-code-documenter/results/baseline-validation.log" 2>&1
"$SKILL_WT/scripts/run_fixture_checks.sh" scientific-code-documenter > "$REPO_ROOT/evals/scientific-code-documenter/results/skill-validation.log" 2>&1

cp "$REPO_ROOT/evals/scientific-code-documenter/results/result.template.md" "$REPO_ROOT/evals/scientific-code-documenter/results/initial-python-ab.md"
```

Fill in the copied result record and score both diffs with `evals/scientific-code-documenter/rubric.md`. Do not reuse a session, change models, or carry context from one run to the other. After saving all results, clean worktrees only with ordinary `git worktree remove <path>` commands; never use destructive resets.

### Real-repository acceptance prompts

Run these later on one authorized medium-complexity file from a scientific Python repository, a computational workflow repository, and an HTML/reporting/scientific-document repository:

```text
$scientific-code-documenter
Review this file for readability and documentation quality. Do not modify it. Identify the five highest-value improvements.
```

```text
$scientific-code-documenter
Apply only high-confidence documentation and readability improvements to this file. Preserve calculations, public interfaces, file formats, and numerical behaviour.
```

```text
$scientific-code-documenter
Implement the requested function using this repository's conventions. Document its units, array shapes, assumptions, failure modes, and return values without over-commenting it.
```

Unless a catalogue entry says otherwise, every skill is experimental. `scientific-code-documenter` is ready for experimental local use, but controlled A/B comparison, trigger-rate measurement, and real-repository acceptance remain outstanding.

## Privacy and publication

Use synthetic, public-safe fixtures. Before sharing changes, inspect staged and tracked files for credentials, personal absolute paths, private server details, proprietary names, unpublished research, copied third-party code, and generated artifacts. Confirm publication rights separately from technical validation.

## Contributing and licence

Keep commits coherent and reviewable, preserve unrelated work, and update evaluations alongside behavior changes. This collection is available under the [MIT License](LICENSE).
