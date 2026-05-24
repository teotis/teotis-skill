# Teotis Skills

A public Codex skill collection for selected release-ready skills.

## Repository Scope

- This repository contains only skills intentionally selected for public release.
- Public skills may behave differently from private versions.
- Do not include private notes, local paths, credentials, unpublished prompts,
  sensitive examples, or user-specific workflow assumptions.

## Skill Conventions

- Skill bodies are written in **English**.
- The visible skill introduction may use **Chinese** so the skill is easy to
  recognize during invocation.
- `SKILL.md` frontmatter must include `name` and `description`.
- Prefer Chinese-first `description` values with concise English keywords when
  useful for matching.
- Shared utilities belong under `<skill>/scripts/` or `<skill>/references/`.

## README

- `README.md` is the English public entry point.
- `README.zh-CN.md` is the Chinese public entry point.
- Keep both files aligned when adding, renaming, or removing public skills.

## Git

- Use conventional commits with Chinese descriptions.
- Never push to remote unless explicitly requested.

