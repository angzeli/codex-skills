# Contributing

Keep every contribution focused on one independently installable skill or one collection-level concern.

## Add a skill

1. Choose a unique kebab-case name.
2. Create `skills/<name>/SKILL.md` with valid frontmatter whose `name` matches the directory.
3. Add runtime references, scripts, templates, or assets only when the skill needs them during use.
4. Create the corresponding `evals/<name>/` directory.
5. Add positive, negative, and boundary trigger prompts.
6. Add synthetic, behavior-preserving fixtures when the skill edits code or artifacts.
7. Run `./scripts/check_skill.sh <name>`.
8. Run `./scripts/run_fixture_checks.sh <name>` when fixtures provide executable checks.
9. Dry-run with `./scripts/install_skill.sh --dry-run <name>`, then install with `./scripts/install_skill.sh <name>`.
10. Update the catalogue in `README.md` and the unreleased section in `CHANGELOG.md`.
11. Create coherent local commits with path-specific staging and reviewed staged diffs.
12. Review all tracked content for secrets, personal paths, private research, and publication rights before pushing or publishing.

Run `./scripts/check_all_skills.sh` and `./scripts/run_fixture_checks.sh` before sharing a collection-level change. State exactly which optional checks were unavailable.

## Change discipline

- Preserve existing skills and their public behavior.
- Keep runtime content out of `evals/` and collection infrastructure out of `skills/<name>/`.
- Do not commit generated evaluation runs.
- Do not claim trigger accuracy, behavior preservation, or effectiveness without recording the relevant evaluation.

## Evaluation gates for skill changes

- Add a focused synthetic regression whenever an observed failure leads to a runtime change.
- Rerun the directly affected fixture, trigger, or boundary gates after every runtime modification.
- Before a release, rerun collection validation, the skill's full fixture suite, and any real-repository gate whose accepted runtime snapshot changed.
- Record portable summaries of release evidence, but keep raw sessions, temporary repositories, and generated logs in ignored result directories.
