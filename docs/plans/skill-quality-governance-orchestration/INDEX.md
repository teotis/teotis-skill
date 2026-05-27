# Skill Quality Governance - Orchestration Index

## Goal

Turn the confirmed structural findings into safe, parallel implementation work:

- add regression eval coverage for the four complex skills that currently lack `evals/evals.json`;
- stop tracking disposable `.tmp/` analysis artifacts and ignore future ones;
- tighten future commit-message guidance so useful skill history is easier to review.

This plan does not rewrite git history and does not publish or push anything.

## User Entry Points

- Manual: copy prompts from `launchers/agent-prompts.md` into any agent platform.
- Script: run `bash launchers/orchestrate.sh start`; view Claude Code agents with `claude agents`.
- Status: run `bash launchers/orchestrate.sh status`.
- Retry: run `bash launchers/orchestrate.sh retry <package-id>`.
- Manual advancement fallback: run `bash launchers/orchestrate.sh advance`.

## Repository And Branch Policy

- Main checkout: `/Volumes/Extreme_SSD/project/teotis_skill`
- Coordinator plan root: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration`
- Mainline branch: `main`
- Integration branch: `codex/skill-quality-governance-orchestration`
- Functional package branches: `agent/skill-quality-governance-orchestration/<package-id>`
- Implementation isolation: one worktree per functional package unless the package explicitly says direct-checkout execution is acceptable.
- Coordinator status/state files are not implementation artifacts and must not be committed on package branches unless explicitly requested.

## Authorization

Package agents are authorized to:

- Create or reuse only their assigned worktree and branch.
- Edit only allowed paths.
- Run listed verification commands.
- Commit local package changes.
- Write only their assigned coordinator status file and state row.
- Call `bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance --from <package-id>` after recording final status.

`99-finalize` is authorized by default to perform incremental orchestration operations for this plan:

- Inspect package docs, status files, state, branches, commits, and diffs.
- Create/update the integration branch.
- Merge package branches into the integration branch according to Merge Strategy.
- Run integration verification.
- Merge the verified integration branch back to mainline.
- Write `FINAL_REPORT.md` and `status/99-finalize.md`.
- Delete only local branches/worktrees created and recorded by this orchestration after every finalize step succeeds.

Forbidden without explicit user approval:

- force-push
- hard reset
- delete branches/worktrees not recorded as created by this orchestration
- delete remote branches
- add secrets or credentials
- edit outside allowed paths
- rewrite existing git history to fix old commit messages

## Dependency Graph

| Package | Depends On | Dependency Type | Unlock Condition | Wave |
|---|---|---|---|---|
| 01-complex-skill-evals | none | status | completed | 1 |
| 02-tmp-repository-hygiene | none | status | completed | 1 |
| 03-commit-message-guardrails | none | status | completed | 1 |
| 99-finalize | all functional packages | status+code | all functional packages completed | final |

## Merge Strategy

- Functional merge order: `01-complex-skill-evals`, `02-tmp-repository-hygiene`, `03-commit-message-guardrails`.
- Code dependency policy: status dependency only; packages own disjoint paths.
- Conflict owner: `99-finalize`.
- Mainline merge: local non-force merge after integration verification passes.
- Cleanup: delete only recorded local package worktrees/branches after all finalize steps succeed.

## Stop Conditions

- Any functional package is `blocked`, `stale`, or `invalid`.
- Graph has duplicate package IDs, missing dependencies, or cycles.
- Package evidence is incomplete.
- Package changed forbidden paths.
- Merge conflict or verification failure occurs.
- Status/state mismatch cannot be reconciled.
- A package discovers that an apparent hygiene change would remove user-authored analysis material rather than only untracking generated artifacts.

## Package Summary

| Package | Allowed Paths | Purpose |
|---|---|---|
| `01-complex-skill-evals` | `skills/renewal-architect/evals/evals.json`, `skills/abstraction-architect/evals/evals.json`, `skills/agent-orchestration-planner/evals/evals.json`, `skills/html-response/evals/evals.json` | Add regression anchors for complex skill behavior and safety boundaries. |
| `02-tmp-repository-hygiene` | `.gitignore`, git index entries under `.tmp/` | Ignore `.tmp/` and untrack existing `.tmp` artifacts without deleting local files. |
| `03-commit-message-guardrails` | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, optional `README.md`, optional `README.zh-CN.md` | Clarify future commit-message rules; do not rewrite history. |
| `99-finalize` | plan status files, `FINAL_REPORT.md`, git branches/worktrees created by this plan | Validate, merge, run checks, and report final state. |

## Verification Baseline

Run from `/Volumes/Extreme_SSD/project/teotis_skill`:

```bash
rtk python3 control/project.py check
rtk python3 control/project.py check-user-skills
rtk git status --short
```

Package-specific verification commands are listed in each package.

