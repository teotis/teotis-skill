# 99-finalize

## Package ID

`99-finalize`

## Goal

Verify all functional packages, merge them in a safe local order, run final checks, and produce `FINAL_REPORT.md`.

## Context

This package is not a passive audit. It is the integration package for this orchestration. It may merge local package branches only after every functional package is complete and evidence is sufficient.

## File Ownership

- Owns: `docs/plans/skill-quality-governance-orchestration/status/99-finalize.md`
- Owns: `docs/plans/skill-quality-governance-orchestration/FINAL_REPORT.md`
- Owns: local integration branch `codex/skill-quality-governance-orchestration`
- Owns: cleanup of only local branches/worktrees created and recorded by this orchestration, after all finalize steps succeed

## Allowed Paths

- `docs/plans/skill-quality-governance-orchestration/status/99-finalize.md`
- `docs/plans/skill-quality-governance-orchestration/FINAL_REPORT.md`
- local git branches/worktrees created by this plan

## Forbidden Paths

- force-push
- hard reset
- remote branch deletion
- deleting unrecorded worktrees or branches
- editing functional package implementation files directly

## Dependencies

- Depends on: `01-complex-skill-evals`, `02-tmp-repository-hygiene`, `03-commit-message-guardrails`

## Implementation Scope

1. Read `INDEX.md`, `launchers/package-graph.tsv`, all package docs, all status files, and `status/state.tsv`.
2. Verify every functional package:
   - acceptance criteria addressed;
   - changed files are within allowed paths;
   - evidence pack complete;
   - branch, worktree, base commit, commit hash recorded if a commit was made;
   - verification commands passed or failures are justified.
3. Stop if any package is not `completed`.
4. Create or update `codex/skill-quality-governance-orchestration`.
5. Merge package branches in this order:
   - `01-complex-skill-evals`
   - `02-tmp-repository-hygiene`
   - `03-commit-message-guardrails`
6. Run final verification.
7. Merge integration branch back to `main` only after verification passes.
8. Write `FINAL_REPORT.md` and `status/99-finalize.md`.
9. Delete only recorded local package branches/worktrees after every prior step succeeds.

## Acceptance Criteria

- All functional package status files say `completed`.
- Final verification commands pass.
- `FINAL_REPORT.md` lists changes, verification, merge status, cleanup status, and residual risks.
- `status/state.tsv` marks `99-finalize` as `finalized` after success or `blocked` after failure.
- No unrecorded resources are deleted.

## Verification Commands

```bash
rtk python3 control/project.py check
rtk python3 control/project.py check-user-skills
rtk python3 -m json.tool skills/renewal-architect/evals/evals.json
rtk python3 -m json.tool skills/abstraction-architect/evals/evals.json
rtk python3 -m json.tool skills/agent-orchestration-planner/evals/evals.json
rtk python3 -m json.tool skills/html-response/evals/evals.json
rtk git ls-files .tmp
rtk git check-ignore .tmp/probe-file
rtk git status --short
```

## Failure Rules

- Any failure sets `99-finalize` to `blocked`.
- Record failure stage, command, branch, conflict files if any, and recovery suggestion.
- Preserve branches/worktrees on failure.
- Never force-push, hard reset, delete remote branches, or delete unrecorded local resources.

## Success Rules

- Mark `99-finalize` as `finalized`.
- Record integration branch, mainline merge commit, verification summary, and cleanup results.
- Re-running finalize after success must be idempotent and report `already finalized`.

