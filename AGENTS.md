# Codex Skill Collection

A curated set of Codex skills for enhanced engineering workflows.

## Project Structure

Each skill lives in its own directory with a `SKILL.md` as entry point:

- `html/` — Visual output delivery, converts task output to interactive HTML
- `grothendieck/` — Architecture deep analysis with mathematical thinking framework
- `grothendieck-test/` — Enhanced version of grothendieck with multi-pass analysis
- `skill-creator/` — Build, test, and iterate on skills (by Anthropic)

## Skill Conventions

- Skills are implemented in **English** (SKILL.md, scripts, prompts)
- Skill frontmatter: `name`, `description` (used for trigger matching)
- Shared utilities go under `<skill>/scripts/` or `<skill>/references/`

## Git

- Conventional commits, Chinese descriptions
- Never push to remote unless explicitly requested
