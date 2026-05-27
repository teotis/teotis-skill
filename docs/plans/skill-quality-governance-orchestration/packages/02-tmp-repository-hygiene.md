# 02-tmp-repository-hygiene

## Package ID

`02-tmp-repository-hygiene`

## Goal

Stop committing disposable `.tmp/` analysis artifacts while preserving the local files for the user.

## Context

- Confirmed finding: `.tmp/` is not ignored.
- Current tracked files include generated reports, data exports, Python cache files, and AppleDouble `._*` files under `.tmp/`.
- The fix should not delete local analysis history. It should remove `.tmp/` from the git index and ignore future `.tmp/` contents.

## File Ownership

- Owns: `.gitignore`
- Owns: git index entries under `.tmp/`
- Does not own file contents inside `.tmp/`

## Allowed Paths

- `.gitignore`
- `.tmp/**` only for `git rm --cached` / untracking from the index

## Forbidden Paths

- `skills/**`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `README.md`
- `README.zh-CN.md`
- `public/teotis-skills/**`
- physical deletion of `.tmp/` files unless the user separately authorizes it

## Dependencies

- Depends on: none

## Parallel Safety

- safe with caution
- Reason: this package edits `.gitignore` and git index only. Avoid running destructive file deletion.

## Implementation Scope

1. Add `.tmp/` to `.gitignore`.
2. Untrack currently tracked `.tmp` files without deleting local files:

   ```bash
   rtk git rm --cached -r .tmp
   ```

3. Confirm `.tmp/` is ignored and no `.tmp` path remains tracked.

Do not remove `.tmp/structural_abstraction_architect_report.html` from disk. It can remain available locally while no longer being committed.

## Acceptance Criteria

- `.gitignore` contains `.tmp/`.
- `rtk git ls-files .tmp` prints no tracked files.
- `rtk git check-ignore .tmp/probe-file` reports that `.tmp/` ignores future files.
- No local `.tmp` files are deleted by the package.
- `control/project.py check` still passes.

## Verification Commands

```bash
rtk git ls-files .tmp
rtk git check-ignore .tmp/probe-file
rtk python3 control/project.py check
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

