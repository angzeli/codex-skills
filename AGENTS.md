# Repository instructions

- Preserve this repository as a collection of independently installable skills under `skills/<name>/`.
- Keep runtime files in each skill directory and evaluation material under the matching `evals/<name>/` directory.
- Determine repository paths dynamically; never hardcode personal absolute paths in committed files.
- Reuse collection-level scripts rather than adding skill-specific installation or validation machinery.
- Preserve existing skills and avoid broad formatting, migrations, or rewrites unrelated to the request.
- Use only synthetic, public-safe evaluation fixtures and examples.
- Validate `SKILL.md` frontmatter, including matching the declared name to its directory.
- Report only checks that were actually run and their real outcomes.
- Make coherent, atomic commits with path-specific staging.
- Do not push, publish, release, tag, or alter remotes unless the user explicitly requests it.
