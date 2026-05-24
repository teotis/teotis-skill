# Codex Skill Collection

A private Codex and Claude Code skill workspace for personal use, incubation,
and selective public release.

## Project Structure

Private skills live in this repository root. Each skill lives in its own
directory with a `SKILL.md` as entry point:

- `<skill>/SKILL.md` — private or incubation skill entry point
- `<skill>/scripts/` — shared scripts for that skill
- `<skill>/references/` — supporting references for that skill
- `public/teotis-skills/` — nested public repository for selected release-ready
  skills; ignored by this private repository

## Skill Conventions

- Skill bodies are implemented in **English** (SKILL.md, scripts, prompts).
- Skill introduction can use **Chinese** so the visible skill description is
  easy to recognize during invocation.
- Skill frontmatter: `name`, `description` (used for trigger matching). Prefer
  Chinese-first descriptions with concise English keywords when helpful.
- Shared utilities go under `<skill>/scripts/` or `<skill>/references/`

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

## Git

- Conventional commits, Chinese descriptions
- Never push to remote unless explicitly requested
