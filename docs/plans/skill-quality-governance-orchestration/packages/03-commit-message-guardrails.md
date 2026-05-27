# 03-commit-message-guardrails

## Package ID

`03-commit-message-guardrails`

## Goal

Prevent future low-information commit messages such as `chore: update SKILL.md` from erasing useful project history.

## Context

- Confirmed finding: recent history contains many generic `chore: 更新 SKILL.md` and `chore: 更新 N 个文件` commits.
- Existing rule already says conventional commits are required, but it does not define what good skill-repo commit subjects should contain.
- This package must not rewrite old commits. It only improves future guidance.

## File Ownership

- Owns: `AGENTS.md`
- Owns: `CLAUDE.md` and `GEMINI.md` only as generated outputs from `rtk python3 control/project.py sync-agents`
- May update README commit guidance if there is already a nearby validation or workflow section.

## Allowed Paths

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `README.md`
- `README.zh-CN.md`

## Forbidden Paths

- `skills/**`
- `.gitignore`
- `.tmp/**`
- `public/teotis-skills/**`
- `control/project.py` unless the package explicitly proves a deterministic check is worth adding
- any git history rewrite command

## Dependencies

- Depends on: none

## Parallel Safety

- safe with caution
- Reason: this package owns shared docs only. It may overlap with generated adapters if another package runs `sync-agents`, so coordinate before committing if adapters change unexpectedly.

## Implementation Scope

1. Refine the existing Git commit rule in `AGENTS.md`.
2. Keep conventional commit format and Chinese descriptions.
3. Add examples that encode user-visible or maintenance-visible intent:

   - `docs: 为复杂技能补充 eval 行为契约`
   - `fix: 停止跟踪 .tmp 分析产物`
   - `chore: 同步 agent 入口文件`
   - `feat: 增加 orchestration 状态账本规则`

4. Explicitly discourage generic subjects:

   - `chore: 更新 SKILL.md`
   - `chore: 更新 N 个文件`

5. Run `rtk python3 control/project.py sync-agents` after editing `AGENTS.md`.

Do not add a hard git-log check for old commits. Historical commits already exist and should not become a failing gate.

## Acceptance Criteria

- `AGENTS.md` explains that commit subjects should name the affected skill, workflow, or invariant.
- `AGENTS.md` says generic "update file count" subjects should be avoided.
- `CLAUDE.md` and `GEMINI.md` are regenerated if `AGENTS.md` changed.
- `control/project.py check` passes.
- No git history is rewritten.

## Verification Commands

```bash
rtk python3 control/project.py sync-agents
rtk python3 control/project.py check
rtk git diff -- AGENTS.md CLAUDE.md GEMINI.md README.md README.zh-CN.md
rtk git status --short
```

## Expected Evidence Pack

- [ ] working directory recorded
- [ ] branch name recorded if changed
- [ ] git status clean or explained
- [ ] git diff --stat captured
- [ ] changed files listed
- [ ] verification commands run
- [ ] test results summarized
- [ ] commit hash recorded if committed
- [ ] unresolved risks noted
- [ ] only allowed paths touched

