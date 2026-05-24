# Project Contract

This file is the single source of shared rules for this private Codex skill
workspace. `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are generated entry points
that only point back to this contract.

## Project Structure

Private skills live under `skills/`. Each skill lives in its own directory with
a `SKILL.md` as entry point:

- `skills/<skill>/SKILL.md` - private or incubation skill entry point.
- `skills/<skill>/scripts/` - shared scripts for that skill.
- `skills/<skill>/references/` - supporting references for that skill.
- `public/teotis-skills/` - nested public repository for selected release-ready
  skills; ignored by this private repository.

## Skill Conventions

- Skill bodies are implemented in English (`SKILL.md`, scripts, prompts).
- Skill introductions can use Chinese so the visible skill description is easy
  to recognize during invocation.
- Skill frontmatter must include `name` and `description`. Prefer
  Chinese-first descriptions with concise English keywords when helpful.
- Shared utilities go under `skills/<skill>/scripts/` or
  `skills/<skill>/references/`.

## Public Release Model

- The private root repository is the source for personal workflows and
  experiments.
- `public/teotis-skills/` is a separate Git repository named `teotis-skills`.
- Public skills are selected manually and may behave differently from private
  skills.
- Do not copy private notes, local paths, credentials, unpublished prompts, or
  sensitive cases into the public repository.
- Public README files should be bilingual: `README.md` in English and
  `README.zh-CN.md` in Chinese.

## Agent Entry Sync

- Edit shared guidance in `control/contract.md`, not in `AGENTS.md`,
  `CLAUDE.md`, or `GEMINI.md`.
- After modifying shared rules, run `python3 control/project.py sync-agents`.
- Run `python3 control/project.py check` before finishing documentation or layout
  changes that affect shared guidance.

## Git

- Use conventional commits with Chinese descriptions.
- Never push to remote unless explicitly requested.
