---
name: agent-orchestration-planner
description: 用于用户明确要求的中大型多 agent 落地、Claude Code Agents View、claude --bg 自动派工、任务尾部推进、DAG 调度、worktree/分支管理、状态账本和自动收口合并。Use for explicit multi-agent orchestration requests, background dispatch, tail-driven advancement, status ledgers, branch/worktree control, and finalize workflows.
---

# Agent Orchestration Planner

## Mission

Turn an explicit user request for medium/large multi-agent execution into a complete orchestration kit. The kit has two user entry paths:
- **Manual**: the user copies prompts from Markdown into any agent platform.
- **Script**: the user runs `bash launchers/orchestrate.sh start`; Claude Code background agents appear in Agents View.

The script is not a long-running central watcher. It is a start/advance/status/retry/finalize entrypoint. Initial `start` launches the first ready wave. Each package prompt ends by calling `orchestrate.sh advance --from <package-id>`, and `advance` is the only place that decides whether to launch downstream packages or `99-finalize`.

## When To Use

Use this skill only when the user explicitly asks for this skill or clearly asks for medium/large orchestration, such as:
- "agent-orchestration-planner"
- "orchestration skill"
- "多 agent 调度"
- "Agent View"
- "claude agents"
- "claude --bg"
- "自动派工"
- "状态账本"
- "十个线程"
- "10+ agents"
- "worktree 管理"
- "分支管理"
- "自动收口"
- "最终合并"

Do not infer this skill merely because a task is complex. If the user did not ask for orchestration or an equivalent multi-agent control plane, do normal work or use another explicitly requested skill. For lightweight one-to-three-window design handoff, use `agent-handoff-planner` only when the user requests it.

## Core Principle

An orchestration kit is a **tail-driven execution contract**. Package agents do the work, update their coordinator status, then call one shared advancement command. They do not implement scheduling logic themselves, and they do not decide what downstream work to start.

## Workflow

### 1. Inspect Or Create Package Materials

Before generating artifacts:
- Read the user request.
- Read existing plan/package docs if provided.
- Inspect enough local context to split work into concrete packages when package docs do not exist.
- Check current git status.
- Ensure every functional package has: Package ID, allowed/forbidden paths, dependencies, acceptance criteria, verification commands, expected evidence, branch/worktree policy, and unlock conditions.
- Run a capability preflight before finalizing the graph: for every package, verification command, and acceptance criterion, identify whether Claude Code can execute it autonomously in the planned environment. Anything requiring a physical device, human visual judgment, external account approval, credential entry, proprietary console access, paid service approval, remote hardware, or user-only decision must not be assigned to an auto-launched functional package.

### Capability Preflight

Prevent non-autonomous work from becoming a surprise blocker. For each candidate package and acceptance criterion, classify it as:

| Class | Meaning | Orchestration treatment |
|---|---|---|
| `autonomous` | Claude Code can execute it with local tools and allowed permissions. | Put it in a normal functional package. |
| `agent-verifiable substitute` | Claude cannot perform the final real-world check, but can produce meaningful evidence such as tests, builds, APKs, logs, screenshots, emulator checks, or checklists. | Put the substitute in an implementation package and state what remains externally unverified. |
| `external-assist` | Requires a human, Codex multimodal/device access, physical hardware, credentials, external approval, or a service console Claude cannot access. | Predeclare it in the INDEX as external assistance or a manual release gate; do not auto-launch it as Claude work. |

Examples of `external-assist`: real-device camera UI validation, hardware-in-the-loop checks, app-store release approval, CAPTCHA/account onboarding, entering private API keys, visual QA that needs user-owned media, and security approval outside the repository.

Design rules:
- Do not make downstream implementation waves depend on external-assist validation unless the user explicitly says it is a mandatory release gate.
- If external validation is required before release, model it as a known manual gate from the first output, with owner, exact commands/checklist, expected evidence, and how to report results back. The automation may stop at "ready for external QA"; it must not pretend the gate passed.
- If external validation is not required for implementation progress, keep it outside the package graph or as `manual=1` documentation that does not block autonomous implementation waves.
- For Android or camera work, package agents should produce APK paths, install commands, logs, emulator checks, and focused tests; real-device pass/fail remains external evidence unless the active environment actually provides that device workflow.

### 2. Generate Orchestration Kit

Create this structure under the plan directory:

```text
docs/plans/<plan-name>/
├── INDEX.md
├── packages/
│   ├── 01-<name>.md
│   ├── 02-<name>.md
│   └── 99-finalize.md
├── launchers/
│   ├── agent-prompts.md
│   ├── package-graph.tsv
│   └── orchestrate.sh
├── status/
│   ├── README.md
│   ├── state.tsv
│   ├── events.jsonl
│   ├── package-status-template.md
│   ├── <package-id>.md
│   └── 99-finalize.md
├── scratch/
│   └── .gitignore
└── FINAL_REPORT.md (created by 99-finalize)
```

`dispatch-claude-agents.sh` is no longer a primary generated entrypoint. If backward compatibility is useful, generate it only as a thin wrapper that calls `orchestrate.sh start`. Both scripts must compute `REPO_ROOT` with `git rev-parse --show-toplevel`, not hardcoded relative paths.

`launchers/orchestrate.sh` must be copied from `scripts/orchestrate-template.sh` (resolved relative to this SKILL.md file), then syntax-checked with `bash -n`. Do not recreate this script from memory or prose. The template is the tested runtime contract for launch handshakes, state mutation, repair, and retry behavior.

### 3. INDEX.md Required Sections

`INDEX.md` is the static execution contract. Dynamic status belongs in `status/`.

```markdown
# <Plan Title> - Orchestration Index

## Goal
<combined outcome>

## User Entry Points
- Manual: copy prompts from `launchers/agent-prompts.md` into any agent platform.
- Script: run `bash launchers/orchestrate.sh start`; view Claude Code agents with `claude agents`.
- Status: run `bash launchers/orchestrate.sh status`.
- Retry: run `bash launchers/orchestrate.sh retry <package-id>`.
- Manual advancement fallback: run `bash launchers/orchestrate.sh advance`.

## Repository And Branch Policy
- Main checkout: <absolute path>
- Coordinator plan root: <absolute path to docs/plans/<name>>
- Mainline branch: <branch>
- Integration branch: <branch created/updated by 99-finalize>
- Functional package branches: `agent/<plan>/<package-id>`
- Implementation isolation: one worktree per functional package unless explicitly excepted.
- Coordinator status/state files are not implementation artifacts and must not be committed on package branches unless explicitly requested.

## Authorization
Package agents are authorized to:
- Create or reuse only their assigned worktree and branch.
- Edit only allowed paths.
- Run listed verification commands.
- Commit local package changes.
- Write only their assigned coordinator status file.
- Update the state ledger only through `bash <plan-root>/launchers/orchestrate.sh mark-state ...`; do not edit `state.tsv` manually.
- Write temporary, non-sensitive shared working notes or intermediate artifacts only under their assigned scratch path from `bash <plan-root>/launchers/orchestrate.sh scratch-path <package-id>`.
- Call `bash <plan-root>/launchers/orchestrate.sh advance --from <package-id>` after recording final status.

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

## Dependency Graph
| Package | Depends On | Dependency Type | Unlock Condition | Wave |
|---|---|---|---|---|
| 01-xxx | none | status | completed | 1 |
| 02-xxx | none | status | completed | 1 |
| 03-xxx | 01-xxx, 02-xxx | code | upstream merged to integration branch or explicit branch base | 2 |
| 99-finalize | all functional packages | status+code | all functional packages completed | final |

## Merge Strategy
- Functional merge order: <ordered package IDs>
- Code dependency policy: <status dependency | merge-to-integration first | downstream bases on upstream branch>
- Conflict owner: `99-finalize`
- Mainline merge: local non-force merge after integration verification passes.
- Cleanup: delete only recorded local package worktrees/branches after all finalize steps succeed.

## Stop Conditions
- Any functional package is `blocked`, `stale`, or `invalid`.
- Graph has duplicate package IDs, missing dependencies, or cycles.
- Package evidence is incomplete.
- Package changed forbidden paths.
- Merge conflict or verification failure occurs.
- Status/state mismatch cannot be reconciled.

## Capability Preflight
| Package Or Gate | Class | Owner | Why Not Fully Autonomous | Autonomous Substitute | External Evidence Required | Blocks |
|---|---|---|---|---|---|---|
| 01-implementation | autonomous | Claude Code | n/a | tests/build | none | normal graph |
| real-device-qa | external-assist | user/Codex/device owner | requires physical device or human visual judgment | APK path, install command, logs, focused tests | checklist result, screenshot/video/log if available | release only, unless user says otherwise |
```

### 4. launchers/agent-prompts.md

Generate one self-contained prompt per package. Each prompt must end with the shared tail call.

````markdown
# Agent Prompts

## Package: <package-id> - <title>

Copy this prompt into an agent, or let `orchestrate.sh start/advance` launch it for Claude Code.

---

**Mode**: package executor
**INDEX**: <absolute-plan-dir>/INDEX.md
**Package doc**: <absolute-plan-dir>/packages/<package-id>.md
**Coordinator status**: <absolute-plan-dir>/status/<package-id>.md
**Coordinator state**: <absolute-plan-dir>/status/state.tsv
**Scratch path**: run `bash <absolute-plan-dir>/launchers/orchestrate.sh scratch-path <package-id>`
**Orchestrator**: <absolute-plan-dir>/launchers/orchestrate.sh

You may edit only the allowed paths in the package doc. Do not edit INDEX.md or another package status file. If you create/use an implementation worktree, do not rely on status files inside that worktree; write the coordinator status path above.

Use scratch only for temporary shared notes, inventories, command transcripts, draft diffs, or intermediate artifacts that help another package or finalizer inspect the work. Do not put credentials, tokens, private keys, `.env` files, hidden prompts, proprietary raw data, or authoritative completion evidence in scratch. Anything required for scheduling, completion, or final acceptance must be summarized into coordinator status through `mark-state` and the package status file.

Do not attempt external-assist work inside a Claude package. If you discover a package requires a physical device, user-owned account, secret, external approval, or human-only judgment that was not declared, mark the package `blocked` with a precise recovery hint instead of improvising or claiming completion.

Before calling `advance`, you must:
- Set coordinator status to `completed` or `blocked`.
- Fill evidence: worktree, branch, base commit, commit hash, changed files, verification commands/results, risks.
- If this package was retried or previously blocked, inspect `state.tsv`, the package status file, and `status/events.jsonl` before editing. Carry forward the recorded `last_error`, `failed_command`, `conflict_files`, `log_summary`, and `recovery_hint` into your diagnosis.
- Update the machine-readable state row only through the orchestrator; do not edit `state.tsv` manually:

```bash
bash <absolute-plan-dir>/launchers/orchestrate.sh mark-state <package-id> completed --commit <commit-sha> --verification "<command: result>"
```

For a blocker:

```bash
bash <absolute-plan-dir>/launchers/orchestrate.sh mark-state <package-id> blocked \
  --error "<specific blocker>" \
  --failed-command "<failed command, if any>" \
  --conflict-files "<comma-separated files, if any>" \
  --log-summary "<short log summary>" \
  --recovery-hint "<specific next action>"
```

Tail step:
```bash
bash <absolute-plan-dir>/launchers/orchestrate.sh advance --from <package-id>
```

If your agent platform cannot run local shell commands, report: "completed but advance not run", and tell the user to run:
```bash
bash <absolute-plan-dir>/launchers/orchestrate.sh advance
```
---
````

### 5. launchers/package-graph.tsv

Generate a machine-readable graph with a header:

```tsv
package_id	package_doc	status_file	dependencies	dependency_type	wave	branch	worktree	manual	finalize
01-xxx	packages/01-xxx.md	status/01-xxx.md		status	1	agent/<plan>/01-xxx	<worktree-path>	0	0
02-xxx	packages/02-xxx.md	status/02-xxx.md		status	1	agent/<plan>/02-xxx	<worktree-path>	0	0
03-xxx	packages/03-xxx.md	status/03-xxx.md	01-xxx,02-xxx	code	2	agent/<plan>/03-xxx	<worktree-path>	0	0
99-finalize	packages/99-finalize.md	status/99-finalize.md	01-xxx,02-xxx,03-xxx	status+code	final	agent/<plan>/99-finalize	<worktree-path>	0	1
```

Rules:
- Package IDs must be unique.
- Dependencies must reference existing package IDs.
- The graph must be acyclic.
- Functional packages are all rows where `finalize != 1`.
- `99-finalize` must be present exactly once.

### 6. status/state.tsv

Generate a machine-readable state ledger with a header:

```tsv
package_id	state	launched_at	completed_at	agent	branch	worktree	base_commit	commit_hash	verification	integration	cleanup	last_error	failed_command	conflict_files	log_summary	recovery_hint
01-xxx	pending	pending	pending	pending	agent/<plan>/01-xxx	<worktree-path>	pending	pending	pending	pending	pending	pending	pending	pending	pending	pending
```

Allowed states:
- `pending`
- `ready`
- `manual_required`
- `launched`
- `in_progress`
- `completed`
- `blocked`
- `stale`
- `invalid`
- `finalizing`
- `finalized`

Markdown status is for humans. `state.tsv` is the scheduler source of truth. If Markdown status and `state.tsv` disagree, `orchestrate.sh status` reports `invalid` and does not unlock downstream packages.

Failure recovery context is part of the scheduler ledger, not an informal chat note. For merge conflicts, failed tests, launch failures, or verification failures, write:
- `last_error`: concise failure statement.
- `failed_command`: exact command or operation that failed, such as `git merge agent/...` or `./gradlew test`.
- `conflict_files`: comma-separated conflicted or suspect files, or empty when none.
- `log_summary`: short summary of the decisive log lines; keep raw logs in `status/` or scratch when needed.
- `recovery_hint`: the next action a downstream retry or repair agent should try first.

Do not blindly retry a blocked package. A retry must preserve the prior recovery context long enough for the relaunched package agent to inspect it, and repeated identical fingerprints must trip the retry breaker.

### 7. launchers/orchestrate.sh

Generate one script with these subcommands:

```bash
bash launchers/orchestrate.sh start
bash launchers/orchestrate.sh advance [--from <package-id>]
bash launchers/orchestrate.sh status
bash launchers/orchestrate.sh retry <package-id>
bash launchers/orchestrate.sh finalize
bash launchers/orchestrate.sh mark-state <package-id> <state> [--base <sha>] [--commit <sha>] [--verification <text>] [--integration <text>] [--cleanup <text>] [--error <text>] [--failed-command <text>] [--conflict-files <text>] [--log-summary <text>] [--recovery-hint <text>]
bash launchers/orchestrate.sh repair-state
bash launchers/orchestrate.sh doctor [--environment]
bash launchers/orchestrate.sh verify-package <package-id>
bash launchers/orchestrate.sh verify-finalize
bash launchers/orchestrate.sh scratch-path <package-id>
```

Required behavior:
- `start`: preflight the graph, acquire lock, launch all currently ready functional packages up to `ORCHESTRATION_MAX_PARALLEL`, then exit.
- `advance`: acquire lock, re-read graph/status/state, validate dependencies, stop on blocked/stale/invalid, launch newly ready functional packages, or launch `99-finalize` when all functional packages are completed.
- `status`: print a concise table of package state, branch, worktree, verification, integration, last error, failed command, and recovery hint.
- `retry <package-id>`: only reset `blocked`, `stale`, or `invalid` packages after reporting prior recovery context. It must not retry already launched or completed packages unless the user explicitly changes state. If the same package hits the same terminal failure fingerprint three times, block further retry and require human diagnosis.
- `finalize`: run or re-run the `99-finalize` package idempotently.
- `mark-state`: the only supported way for package agents to mutate `state.tsv`; it also keeps Markdown status in sync.
- `repair-state`: rebuild `state.tsv` from graph and Markdown status when a ledger is empty or malformed.
- `doctor`: run preflight and consistency checks without launching work.
- `doctor --environment`: report repo root, plan root, Claude CLI path/version, `claude agents --help` availability, permission mode, and setting sources so users can tell whether Codex/rtk and macOS Terminal are using the same Claude environment.
- `verify-package` / `verify-finalize`: verify package evidence before integration, including completed state, branch, commit hash, commit existence, and clean package worktree when present.
- `scratch-path <package-id>`: create `scratch/.gitignore`, create the package-local scratch directory, print its absolute path, and record the request in `events.jsonl`.

Implementation rules:
- Use `scripts/orchestrate-template.sh` (resolved relative to this SKILL.md file) as the script body.
- Compute `REPO_ROOT` dynamically with `git rev-parse --show-toplevel` from the script's directory. Never use hardcoded relative path traversal like `../../..` — the plan directory depth from repo root varies per project.
- When awk processes the same TSV file twice (e.g. `awk '...' "$GRAPH" "$GRAPH"`), use `FNR == 1` to skip each file's header, not `NR == 1` which only skips the first file's header.
- Use a lock such as `status/.orchestrate.lock` so concurrent `advance` calls cannot double-launch packages.
- Never trust `--from`; it is only a hint for logging. Always compute readiness from coordinator status/state.
- Every package can be launched at most once unless `retry` explicitly resets it.
- Launch Claude Code background agents with `claude --bg --name` from the package's assigned worktree.
- Parse Claude Code session ids from both observed output formats: `backgrounded <id>` and `backgrounded · <id>`. Never record punctuation such as `·` as the session id.
- Do not silently grant elevated permission modes. Default to no explicit `--permission-mode`; `CLAUDE_PERMISSION_MODE=auto` requires `CLAUDE_AUTO_MODE_OPTED_IN=1` after an interactive opt-in, and `CLAUDE_PERMISSION_MODE=bypassPermissions` requires `CLAUDE_BYPASS_PERMISSIONS_APPROVED=1`.
- Before launch, create or verify the recorded package worktree and branch.
- If a graph row has `manual=1`, never auto-launch it. When its dependencies are satisfied, mark it `manual_required` and print the package id for manual execution.
- Capability preflight is mandatory before graph creation. Auto-launched packages may contain only `autonomous` or `agent-verifiable substitute` work. `external-assist` checks must be predeclared in the INDEX and kept out of autonomous package execution unless the active environment truly provides that capability.
- Maintain `status/events.jsonl` as an append-only audit log. Record at minimum: `launch_requested`, `launch_succeeded`, `state_changed`, `terminal_failure`, `retry_requested`, `retry_blocked`, and `scratch_path_requested` with timestamp, package id, state transition or session id, path, and error fingerprint where relevant.
- On terminal package failures (`blocked`, `stale`, or `invalid` with `--error`), record recovery context in both `state.tsv` and `events.jsonl`: error, failed command, conflict files, log summary, and recovery hint. Sanitize tabs/newlines before writing TSV.
- Treat `events.jsonl` as the source for retry loop accounting. If `terminal_failure` records show the same package and normalized error fingerprint three times, `retry` must stop before relaunching and print the package id, failure count, and fingerprint.
- Maintain `scratch/` as a plan-local, gitignored, non-authoritative exchange area. Runtime commands must create `scratch/.gitignore` with ignored contents, and package prompts must direct agents to request their package path through `scratch-path`. Scratch contents must never unlock dependencies, satisfy acceptance criteria by themselves, or replace status/evidence fields.
- Write raw launch output to `status/launch-<package-id>.log`.
- Parse and record the background session id in the `agent` column.
- After launch, run a short `claude logs <session-id>` postflight. If the session id is missing, mark the package `invalid`. If logs are not readable or the session exits immediately, mark it `stale`.
- Never unlock downstream packages from `launched`, `in_progress`, or `finalizing`; downstream unlock requires `completed` or `finalized`.
- Default `ORCHESTRATION_MAX_PARALLEL=10`.
- Print the `claude agents` command after launching agents.
- Do not run as a permanent watcher. Tail calls and manual `advance` drive progression.

### 8. packages/99-finalize.md

Generate a finalize package, not a passive audit-only prompt.

`99-finalize` must:
1. Read INDEX, graph, all package docs, all status files, and `state.tsv`.
2. Run `bash launchers/orchestrate.sh verify-finalize` before merging.
3. Verify every functional package:
   - acceptance criteria addressed
   - changed files are within allowed paths
   - evidence pack complete
   - branch, worktree, base commit, commit hash recorded
   - verification commands passed or failure is explicitly justified
   - package branch exists
   - package commit hash exists
   - package changed files are within allowed paths
   - package worktree is clean, or dirty state is recorded as a blocker
4. Check the Capability Preflight section. If an external-assist gate is release-blocking and evidence is absent, stop with "ready for external QA" or "waiting for external gate"; do not claim overall PASS.
5. Decide whether merging is allowed.
6. Create or update the integration branch.
7. Merge functional package branches in Merge Strategy order.
8. Stop and record conflicts without cleaning anything.
9. Run integration verification.
10. Merge integration branch back to mainline only after verification passes and release-blocking external gates are satisfied or explicitly deferred by the user.
11. Write `FINAL_REPORT.md` and `status/99-finalize.md` for both success and failure.
12. Delete only local package branches/worktrees recorded by this orchestration after every prior step succeeds.

Failure rules:
- Any failure sets `99-finalize` to `blocked`.
- Record failure stage, command, branch, conflict files if any, log summary, and recovery suggestion in `status/99-finalize.md`.
- Also update the coordinator ledger with `mark-state 99-finalize blocked --error ... --failed-command ... --conflict-files ... --log-summary ... --recovery-hint ...`; do not leave merge/test failures only in prose.
- Check `status/events.jsonl` when explaining repeated failures; do not keep retrying the same fingerprint after the retry breaker opens.
- Preserve branches/worktrees on failure.
- If package status and current workspace disagree, verify the recorded package commit in a clean detached worktree before changing state.
- Never force-push, hard reset, delete remote branches, or delete unrecorded local resources.
- Never mix coordinator ledger/final-report commits with unrelated orchestration documents or concurrent mainline edits.

Success rules:
- Mark `99-finalize` as `finalized`.
- Record integration branch, mainline merge commit, verification summary, and cleanup results.
- Re-running finalize after success must be idempotent and report `already finalized`.

### 9. Output Style

After generating the kit, chat output must be immediately actionable and must show only the two primary user entry paths plus status/recovery commands.

Always include this information:
- Plan directory path.
- Mainline branch.
- Integration branch.
- Max parallel agents.
- First wave packages.
- Final package: `99-finalize`.
- A statement that downstream dispatch is triggered by package tail calls to `advance`.
- Any external-assist gates, their owners, whether they block release or only final confidence, and the exact evidence expected.

For the **Manual** path, include a package table so the user can decide which prompts to copy first:

| Package | Prompt Location | Can Start Now | Must Wait For | Dependency Type | Notes |
|---|---|---|---|---|---|
| 01-xxx | `<plan>/launchers/agent-prompts.md#01-xxx` | yes | none | status | first wave |
| 02-xxx | `<plan>/launchers/agent-prompts.md#02-xxx` | yes | none | status | first wave |
| 03-xxx | `<plan>/launchers/agent-prompts.md#03-xxx` | no | 01-xxx, 02-xxx | code | started by `advance` |
| 99-finalize | `<plan>/launchers/agent-prompts.md#99-finalize` | no | all functional packages | status+code | auto final package |

The Manual section must say:
- Copy prompts from `<plan>/launchers/agent-prompts.md`.
- Start every row where `Can Start Now = yes` in any agent platform.
- Later packages should not be manually started unless their dependencies are satisfied or the user intentionally overrides automation.
- If an agent platform cannot run local shell commands, the user may manually run `advance`.

For the **Script** path, include complete copy-paste commands for a new macOS Terminal. Commands must use absolute paths and avoid assuming the user's current directory.

```bash
cd "<repo-root>"
bash "<absolute-plan-dir>/launchers/orchestrate.sh" start
```

Also include status and recovery commands:

```bash
bash "<absolute-plan-dir>/launchers/orchestrate.sh" status
bash "<absolute-plan-dir>/launchers/orchestrate.sh" advance
bash "<absolute-plan-dir>/launchers/orchestrate.sh" retry <package-id>
bash "<absolute-plan-dir>/launchers/orchestrate.sh" finalize
bash "<absolute-plan-dir>/launchers/orchestrate.sh" doctor --environment
bash "<absolute-plan-dir>/launchers/orchestrate.sh" verify-finalize
bash "<absolute-plan-dir>/launchers/orchestrate.sh" scratch-path <package-id>
claude agents --cwd "<repo-root>"
```

If a command contains placeholders such as `<package-id>`, explicitly say which concrete package IDs are valid recovery targets. Do not leave the user to infer them from the docs.

Do not present `/batch`, `dispatch-claude-agents.sh`, or a separate audit prompt as peer user entrypoints.

## Guardrails

- Do NOT use this skill unless the user explicitly asks for orchestration.
- Do NOT make `orchestrate.sh` a long-running watcher by default.
- Do NOT duplicate scheduling logic in package prompts; prompts only call `advance`.
- Do NOT let package agents edit INDEX.
- Do NOT use worktree-local status as coordinator truth.
- Do NOT launch downstream packages from a package agent directly.
- Do NOT assign non-autonomous work such as real-device QA, external approvals, credential entry, or human-only visual judgment to auto-launched Claude packages.
- Do NOT hide external-assist requirements inside acceptance criteria; predeclare them in the INDEX before launching agents.
- Do NOT run `99-finalize` if any functional package is not `completed`.
- Do NOT treat scratch files as scheduler truth, final evidence, or a place for secrets.
- Do NOT clean up branches/worktrees unless finalize fully succeeds.
- Do NOT delete resources not recorded as created by this orchestration.

## Relationship With agent-handoff-planner

Use `agent-handoff-planner` only when the user asks for small handoff plans that they will run manually in one to three windows. Use `agent-orchestration-planner` only when the user asks for a multi-agent orchestration control plane. Chaining the two skills is optional, not required.
