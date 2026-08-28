# Getting started

This guide shows how to install and use the `angze-code-style` skill in Codex. The skill helps review, document, and prune scientific code or Jupyter notebooks while preserving explicit scientific, data, interface, execution-state, and artifact contracts.

## What you need

- Codex Desktop, the Codex CLI, or the Codex IDE extension
- Access to this GitHub repository

If the repository is private, make sure your GitHub account or local Git setup can access it before installing.

## Install with Codex

Open a new Codex task and paste this prompt:

```text
$skill-installer
Install https://github.com/angzeli/codex-skills/tree/main/skills/angze-code-style
```

The skill should be available on your next turn. If it does not appear, start a new task or restart Codex.

## Try the skill

For a review that does not modify files:

```text
$angze-code-style
Review this file for readability and documentation quality. Do not modify it.
```

For focused documentation and readability improvements:

```text
$angze-code-style
Apply only high-confidence documentation and readability improvements to this file. Preserve calculations, public interfaces, file formats, and numerical behavior.
```

Attach the file, open its repository in Codex, or name the file path in the prompt. Codex may also select the skill automatically when a request clearly matches its purpose.

For a conservative notebook review:

```text
$angze-code-style
Review this notebook's role, scientific and data contracts, execution state, outputs, and documentation risks. Do not modify or execute it.
```

For an authorized notebook documentation edit, name the permitted cells or source fields and the protected state. The skill does not execute notebooks, clear outputs, add or reorder cells, or normalize notebook JSON by default.

Always review scientific edits before accepting them. The skill preserves behavior by design, but it cannot independently confirm undocumented scientific meaning, general notebook equivalence, stored-output validity, or every environment-specific interaction.

## Manual installation from a clone

This alternative is useful for contributors or anyone who wants updates in a local clone to become available immediately. It requires Git and a Bash-compatible shell.

```sh
git clone https://github.com/angzeli/codex-skills.git
cd codex-skills
./scripts/install_skill.sh angze-code-style
```

The script validates the skill and links it into `$HOME/.agents/skills`. Start a new Codex task after the first installation. To update later, pull the latest repository changes; the link will continue to use the checked-out skill.

## Troubleshooting

- **The skill is not listed:** Start a new task or restart Codex after installation.
- **GitHub access fails:** Confirm that you can open or clone the repository, especially if it is private.
- **The manual installer will not run:** From the repository root, try `bash ./scripts/install_skill.sh angze-code-style`.
- **You only want feedback:** Include `Do not modify files` in the prompt.

For maintainer commands, validation details, and evaluation status, see the main [README](README.md).
