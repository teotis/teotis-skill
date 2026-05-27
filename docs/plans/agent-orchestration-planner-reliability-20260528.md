# Agent Orchestration Planner Reliability Repair Plan

Date: 2026-05-28
Scope: `skills/agent-orchestration-planner`

## Problem Statement

Recent orchestration kits are useful when they reach execution, but script-triggered execution is too fragile. The observed failure rate is high because generated launchers currently treat `claude --bg` process creation as enough evidence that a package is executing, while the real success boundary is later: a background session must be reachable, have a package worktree/branch, write coordinator evidence, and update state consistently.

## Evidence From Recent Runs

- 2026-05-26, old `dispatch-claude-agents.sh`: Claude Code 2.1.142 permission behavior changed. Passing or omitting permission mode had subtle effects, and `set -u` plus an empty `CLAUDE_PERMISSION_ARGS[@]` array caused launch scripts to fail before any agent was created.
- 2026-05-27, `paper_worker` `orchestrate.sh`: `retry` reported a backgrounded Claude session, but there was no package branch, worktree, commit, or evidence. The coordinator had to mark the package `stale`.
- 2026-05-27, same kit: `state.tsv` was previously empty or malformed enough that status handling had to be hardened with schema validation, `repair-state`, and `mark-state`.
- 2026-05-27, `open_camera` UX regression orchestration: a package status said `blocked` for test failures, but the underlying worktree also contained unrelated dirty changes. Verifying the exact package commit in a clean worktree was required to distinguish stale ledger state, package failure, and accidental uncommitted repairs.

## Root Cause

This is not one shell bug. The root cause is that the skill specifies an orchestration contract but does not yet provide a tested orchestration runtime. Each kit is generated as bespoke shell, so small differences in launch, state mutation, lock handling, TSV parsing, permission flags, and post-launch checks reintroduce failures.

The most important missing invariant:

> A package is not `launched` merely because `claude --bg` printed `backgrounded`. It is launched only after the script records the session id, captures launch logs, verifies the intended branch/worktree exists or was created, and can inspect the background session enough to keep or downgrade the state.

## Repair Strategy

### Phase 1 - Stabilize The Runtime Contract

Move the launcher from "prose-generated shell" to a reusable runtime template under:

- `skills/agent-orchestration-planner/scripts/orchestrate-template.sh`
- optional renderer/helper: `skills/agent-orchestration-planner/scripts/render_orchestration_kit.py`

Every generated `launchers/orchestrate.sh` should be derived from the same template and parameterized by `package-graph.tsv`, `state.tsv`, and plan metadata.

Required runtime commands:

- `start`
- `advance [--from <package-id>]`
- `status`
- `retry <package-id>`
- `finalize`
- `mark-state <package-id> <state> [--base ...] [--commit ...] [--verification ...] [--integration ...] [--cleanup ...] [--error ...]`
- `repair-state`
- `doctor`

### Phase 2 - Make State Mutation Script-Owned

Package prompts must stop telling agents to hand-edit `state.tsv`.

They should say:

```bash
bash <plan>/launchers/orchestrate.sh mark-state <package-id> completed --commit <sha> --verification "<command: result>"
```

The script must validate:

- exact graph header and 10 fields per graph row
- exact state header and 13 fields per state row
- one and only one finalize row
- no duplicate package ids
- no missing dependency ids
- no blocked/stale/invalid package before unlock
- Markdown status and `state.tsv` are consistent

### Phase 3 - Treat Launch As A Two-Step Handshake

Before launch:

- compute repo root with `git rev-parse --show-toplevel`
- verify `claude` exists and record `claude --version`
- pre-create or verify the assigned worktree and branch, then launch the agent from that worktree
- write `status/launch-<package-id>.log`

After launch:

- parse and record the background session id in the `agent` column
- run a short postflight check: `claude logs <session-id>` or equivalent
- if launch output has no session id, mark `invalid`
- if logs are unreadable or the session exits immediately, mark `stale`
- never unlock downstream packages from a plain `launched` state

### Phase 4 - Harden Finalization

`99-finalize` must verify each package from immutable evidence, not from trust in a status sentence.

For every package:

- confirm branch exists
- confirm commit hash exists
- confirm changed files are within allowed paths
- confirm worktree is clean or explicitly record dirty state as blocker
- verify package commit in a clean detached worktree when status and current workspace disagree
- merge only recorded package branches into an integration branch
- never mix coordinator ledger commits with unrelated orchestration docs or concurrent mainline edits

### Phase 5 - Add Failure-Focused Evals

Current evals check that the kit exists, but not that it survives known failure modes. Add evals for:

- empty `CLAUDE_PERMISSION_MODE` under `set -u` does not produce an unbound variable
- `claude --bg` returns `backgrounded <id>` but `claude logs <id>` fails, so package becomes `stale`
- missing or empty `state.tsv` causes `status` to fail with a repair instruction
- malformed TSV row width blocks `start` and `advance`
- `retry` only works for `blocked`, `stale`, and `invalid`
- concurrent `advance` calls cannot double-launch a package
- Markdown status and `state.tsv` mismatch reports `invalid`
- downstream packages do not unlock from `launched`
- package prompt uses `mark-state`, not manual `state.tsv` editing
- finalize refuses dirty package worktrees and unrecorded branches

## Acceptance Criteria

- New orchestration kits use the shared runtime template.
- `bash -n` passes for generated scripts.
- A fake `claude` test harness covers launch success, launch failure, unreadable logs, missing session id, and permission-mode inheritance.
- `control/project.py check` passes.
- `control/project.py sync-user-skills` and `check-user-skills` pass after the skill update.
- A dry-run generated kit can pass `status`, `start` with fake Claude, `mark-state`, `advance`, `retry`, `repair-state`, and `finalize` state transitions without manual TSV edits.

## Suggested Implementation Split

1. Runtime template and prompt contract: extract a single robust `orchestrate-template.sh`, add `mark-state`, `repair-state`, `doctor`, launch logs, session id capture, state schema validation.
2. Launch/worktree hardening: make package worktree/branch creation script-owned and launch agents from the assigned worktree.
3. Finalize evidence hardening: verify commit hashes, allowed paths, dirty worktrees, integration branch merge order, and mainline drift.
4. Eval/test coverage: add fake-Claude tests and eval cases for all failure modes above.
5. Existing kit migration note: document that old `dispatch-claude-agents.sh` and early `orchestrate.sh` kits may need regeneration or a one-time launcher upgrade.
