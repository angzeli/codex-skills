# Runtime skills

Each direct child directory represents one independently installable Codex skill and must contain a valid `SKILL.md`.

- Use kebab-case directory names.
- Set the frontmatter `name` to exactly the directory name.
- Keep only runtime-required references, scripts, templates, and assets inside the skill directory.
- Keep repository-level evaluation, validation, installation, and contribution infrastructure outside runtime directories.
- Preserve each skill as an independent package that can be linked to `$HOME/.agents/skills/<name>`.
