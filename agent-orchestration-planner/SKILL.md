---
name: agent-orchestration-planner
description: Use for explicit medium-to-large multi-agent execution requests, Claude Code Agents View, claude --bg background dispatch, tail-driven advancement, DAG scheduling, worktree/branch management, status ledgers, and final merge workflows.
---

# Agent Orchestration Planner

## Mission

Turn an explicit user request for medium/large multi-agent execution into a
complete orchestration kit. The kit has two user entry paths:
- **Manual**: the user copies package prompts from Markdown into any agent platform.
- **Script**: the user runs `bash launchers/orchestrate.sh start`; background agents are launched by the configured runner.

The script is not a long-running watcher. It is a
`start/advance/status/retry/finalize` entrypoint. Initial `start` launches the
first ready wave. Each package prompt ends by calling
`orchestrate.sh advance --from <package-id>`, and `advance` is the only place
that decides whether to launch downstream packages or `99-finalize`.
After the tail call returns, the package/finalize session must terminate immediately.
It must not emit another summary, ask for input, suggest a reply, or wait at an
interactive prompt; blocker and recovery details belong only in coordinator artifacts.

The generated template supports runner variation through `ORCHESTRATION_RUNNER`:
- `claude` (default): launches Claude Code background sessions with `claude --bg --name` and points users to `claude agents`.
- `codex`: launches local background `codex exec --json` processes from package worktrees, records `codex-thread:<thread-id>` when available, and points users to package JSONL logs. This is not a Claude Agents View clone.

## When To Use

Use this skill only when the user explicitly asks for this skill or clearly asks
for medium/large orchestration, such as:
- `agent-orchestration-planner`
- `orchestration skill`
- Multi-agent orchestration / automatic dispatch / 10+ agents
- Claude Code Agents View / `claude agents` / `claude --bg`
- Status ledger / DAG scheduling / worktree management / branch management / final merge

Do not infer this skill merely because a task is complex. If the user did not
ask for orchestration or an equivalent multi-agent control plane, do normal work
or use another explicitly requested skill. For lightweight one-to-three-window
manual execution, write compact packages containing the goal, owned and
forbidden paths, dependencies, acceptance criteria, verification commands,
expected evidence, and final status handoff instead of generating a full
orchestration kit.

## Core Contract

An orchestration kit is a **tail-driven execution contract**. Package agents do
the work, update their coordinator status, then call one shared advancement
command. They do not implement scheduling logic themselves, and they do not
decide what downstream work to start.

Context is loaded progressively by role and state:
- Functional package prompts use package-local context first: package doc,
  assigned status, graph/state rows, and relevant repository files.
- Read full INDEX, events, or failure-recovery details only when retry, policy
  conflict, fallback judgment, or capability uncertainty requires them.
- Functional package prompts do not copy global merge, fallback selection,
  cleanup, or task-level outcome logic; `99-finalize` owns those decisions.
- Background executors should not emit progress narration, task restatement, or
  intermediate summaries. They write durable evidence once to coordinator
  artifacts.
- The runtime keeps its full recovery surface, but user-facing chat exposes only
  the smallest command set needed for the current state.

Treat an orchestration as one execution contract with multiple projections:
- `INDEX.md` owns static human intent, authorization, policy, landing strategy, and capability gates.
- `launchers/package-graph.tsv` owns machine-readable package topology.
- `status/state.tsv` owns the current scheduler snapshot and is mutated only through `orchestrate.sh mark-state`.
- `status/events.jsonl` owns append-only audit history, retry accounting, and failure fingerprints.
- `status/<package-id>.md` owns human-readable package evidence and blocker diagnosis.
- `launchers/agent-prompts.md` owns local package execution contracts and tail-call instructions.
- `packages/99-finalize.md` and `FINAL_REPORT.md` own global verification, merge judgment, task outcome, and final narrative.
- `scratch/` is temporary, gitignored, non-authoritative exchange material.

When projections disagree, report the orchestration as invalid or blocked until
repaired. Do not infer success from the most optimistic artifact.

## Reference Map

Keep this `SKILL.md` as the operating kernel. Load references only when their
details are needed:

- Read `references/planning_contract.md` when splitting packages, assigning projection ownership, classifying capability gates, or defining landing/fallback behavior.
- Read `references/runtime_contract.md` before generating or modifying `package-graph.tsv`, `state.tsv`, `orchestrate.sh`, runner behavior, or dependency unlock rules.
- Read `references/failure_recovery.md` when handling `blocked`, `stale`, `invalid`, retry, doctor, logs, scratch, or non-landable plans.
- Read `references/artifact_templates.md` when producing `INDEX.md`, package prompts, `99-finalize`, or the final user-facing command summary.

`scripts/orchestrate-template.sh` is the tested runtime body. Copy it into the
generated kit as `launchers/orchestrate.sh` and run `bash -n`; do not recreate
the script from memory or prose.

## State Semantics

Allowed package states are:
`pending`, `ready`, `manual_required`, `launched`, `in_progress`, `completed`,
`blocked`, `stale`, `invalid`, `finalizing`, and `finalized`.

Do not add runner-specific state columns. Model Claude, Codex, manual execution,
CI runners, and other platforms as variations in launch mechanism, permission
mode, evidence channel, and verification ability over the same lifecycle.

Codex/runtime observations map onto the existing states:
- `pending_init` or `running`: active work; keep `launched`/`in_progress`.
- `interrupted`: usually retryable `stale` unless evidence proves a deliberate blocker.
- `completed`: package may become `completed` only after evidence is recorded and `mark-state completed` is called.
- `errored`: `blocked` or `invalid` with recovery context.
- `not_found`: `invalid` for missing launch identity, or `stale` for lost active sessions.
- `shutdown`: resource lifecycle only; not success by itself.

`launched`, `in_progress`, and `finalizing` must never unlock downstream
packages, start `99-finalize`, or satisfy acceptance criteria. Dependency
checks unlock only from `completed` or `finalized`.

## Workflow

### 1. Inspect Or Create Package Materials

Before generating artifacts:
- Read the user request and existing plan/package docs if provided.
- Search the project's documented planning home, such as `docs/plans/`, `codex/agent_plans/`, or paths named by AGENTS/CLAUDE/project docs.
- Inspect enough local context to split work into concrete packages.
- Check current git status.
- Ensure every functional package has package id, allowed/forbidden paths, dependencies, acceptance criteria, verification commands, expected evidence, branch/worktree policy, and unlock conditions.
- Run capability preflight: classify each package or gate as `autonomous`, `agent-verifiable substitute`, or `external-assist`.
- Default to task packages that agents can complete by themselves. If real-device QA, human visual acceptance, external approval, credential entry, or another `external-assist` item is essential, cannot be ignored, and has no agent-verifiable substitute, stop before generating the kit and ask the user to approve the gate, change scope, or abort the orchestration.
- Define landing strategy before launch: primary path, preapproved fallbacks, explicit non-goals, abort conditions, and independent merge candidates.

Use `references/planning_contract.md` for the detailed projection, capability,
and landing/failure planning rules.

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
└── FINAL_REPORT.md
```

Read `references/runtime_contract.md` for exact graph/state headers, runtime
commands, runner behavior, and no-`launched`-unlock rules. Read
`references/artifact_templates.md` for the long Markdown templates and final
chat output shape.

### 3. Required Script Commands

Generated `launchers/orchestrate.sh` must expose:

```bash
start
advance [--from <package-id>]
status
retry <package-id>
finalize
cleanup --mainline <branch>
mark-state <package-id> <state> [fields...]
repair-state
doctor [--environment]
collect-logs <package-id>
verify-package <package-id>
verify-finalize
scratch-path <package-id>
```

Core behavior:
- `start` and `advance` acquire a lock, validate graph/state, compute readiness, and launch only eligible packages.
- The ready-package queue must use a dedicated file descriptor, not the dispatch loop's stdin; runner launch, log postflight, or health-check subprocesses must not be able to consume later package IDs from the same wave.
- Package agents mutate `state.tsv` only through `mark-state`.
- `retry` accepts only `blocked`, `stale`, or `invalid`, preserves prior recovery context, and obeys the three-strike fingerprint breaker.
- `doctor` checks consistency and runner/session health without launching work.
- `99-finalize` runs only when all functional packages are `completed`, then verifies evidence, merges conservatively, reports outcome, and calls `cleanup --mainline <branch>` only after success. Cleanup must finish before `99-finalize` may be marked `finalized`.

### 4. Output To User

After generating the kit, show only immediately actionable entry paths:
- Plan directory path.
- Mainline branch, integration branch, max parallel agents.
- First wave packages and final package `99-finalize`.
- Manual path: copy prompts from `launchers/agent-prompts.md`.
- Script path: absolute `cd`, `bash <plan>/launchers/orchestrate.sh start`,
  `bash <plan>/launchers/orchestrate.sh status`, and `claude agents --cwd
  <repo-root>` commands.
- Default user chat shows only `start`, `status`, and `claude agents`.
- Recovery commands are shown only when the current state requires them:
  `retry <package-id>` for `blocked`/`stale`/`invalid`, `doctor --environment`
  for runner setup, `collect-logs <package-id>` for diagnosis, `advance` for a
  shell-less manual tail-call gap, `verify-finalize`/`finalize` for finalize
  recovery, and `scratch-path <package-id>` only for declared exchange needs.
- External-assist gates, owners, whether they block release, and exact evidence expected.
- Landing strategy summary.

For Codex runner, include `ORCHESTRATION_RUNNER=codex` in script commands and
describe evidence as JSONL logs plus recorded thread/process identifiers, not
Claude Agents View.

## Guardrails

- Do NOT use this skill unless the user explicitly asks for orchestration.
- Do NOT make `orchestrate.sh` a long-running watcher.
- Do NOT duplicate scheduling logic in package prompts; prompts only call `advance`.
- Do NOT let package agents edit `INDEX.md`, another package status file, or `state.tsv` manually.
- Do NOT use worktree-local status as coordinator truth.
- Do NOT launch downstream packages from a package agent directly.
- Do NOT assign non-autonomous work such as real-device QA, external approvals, credential entry, or human-only visual judgment to auto-launched packages.
- Do NOT hide external-assist requirements inside acceptance criteria.
- Do NOT output a full kit with a blocking external-assist gate before the user has approved that gate, owner, expected evidence, and blocking scope.
- Do NOT invent fallback paths during failure handling unless the INDEX preapproved them or the user explicitly approves them.
- Do NOT merge anything after the main plan fails unless it is a predeclared independent merge candidate with standalone verification.
- Do NOT add `state.tsv` columns for narrative evidence, retry history, QA links, release tickets, or reviewer comments.
- Do NOT copy separate lifecycle states or finalize logic for each runner or agent platform.
- Do NOT resolve projection drift by trusting the most optimistic artifact.
- Do NOT treat `scratch/` files as scheduler truth, final evidence, or a place for secrets.
- Do NOT clean up branches/worktrees unless finalize fully succeeds.
- Do NOT delete resources not recorded as created by this orchestration.

## Relationship With Lightweight Manual Packages

When the user only needs one to three manually executed packages, do not generate
the full orchestration kit. Use the shared Task Package Contract to capture
scope, acceptance criteria, and verification commands. Use
`agent-orchestration-planner` when the user asks for a multi-agent orchestration
control plane with durable state, dependency scheduling, recovery, and finalize
behavior.
