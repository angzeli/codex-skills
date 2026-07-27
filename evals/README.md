# Skill evaluations

Use a one-to-one convention: `skills/<name>/` corresponds to `evals/<name>/`.

Evaluation material remains separate so runtime installations contain only the instructions and resources Codex needs while using a skill. A useful suite contains:

- a prompt matrix covering positive implicit triggers, explicit invocation, negative prompts, and boundary cases;
- synthetic fixtures that expose the behavior the skill should improve without including private or proprietary content;
- executable behavior-preservation or artifact-validation checks where practical;
- a manual scoring rubric for properties that scripts cannot judge reliably;
- controlled A/B instructions using identical starting commits, models, prompts, and fresh sessions;
- result-recording templates for diffs, validation logs, scores, trigger outcomes, strengths, and regressions.

Generated evaluation runs belong under `evals/<name>/results/` and are ignored by default except for committed directory markers and templates.

Each suite may provide `evals/<name>/checks.sh`. Run one suite with `./scripts/run_fixture_checks.sh <name>` or all available suites with `./scripts/run_fixture_checks.sh`. A missing optional tool should produce a clear skip; a detected regression must produce a non-zero exit.
