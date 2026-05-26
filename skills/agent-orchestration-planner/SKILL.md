---
name: agent-orchestration-planner
description: 用于中大型多 agent 落地、Claude Code Agents View、claude --bg 自动派工、10+ 线程分批调度、worktree/分支管理、状态账本和最终集成验收。Use for multi-agent orchestration, background dispatch, status ledgers, branch/worktree control, and integration audit workflows.
---

# Agent Orchestration Planner

## Mission

Turn medium and large implementation needs into an executable multi-agent orchestration kit. This skill can start from an existing handoff package set, or directly from a user request when the work clearly needs Agent View, background sessions, automated dispatch, coordinator status, and branch/worktree control:
- Decide whether to use Agent View with `claude --bg` and `claude agents`, `/batch`, agent team, or a staged orchestration plan.
- Create orchestration-ready package docs when they do not already exist.
- Generate launch prompts automatically.
- Generate optional shell dispatch scripts that are idempotent and dependency-aware.
- Define package ownership and concurrency groups.
- Prevent file conflicts.
- Require evidence packs.
- Define worktree, branch, integration, and coordinator-status policies.
- Provide integration audit and final validation entrypoints.

## When To Use

Use this skill when the request contains signals like:
- "多 agent"
- "并行落地"
- "分包执行"
- "Agent View"
- "claude agents"
- "claude --bg"
- "/batch"
- "批量执行"
- "自动派工"
- "状态账本"
- "多个 Claude Code 窗口"
- "十个线程"
- "10+ agents"
- "worktree 管理"
- "分支管理"
- "Codex 负责验收"
- "生成启动 prompt"
- "生成 dispatch script"

Do not use it for one tiny implementation package, or for a lightweight design that the user can run in one to three Claude Code windows in the current checkout. Use `agent-handoff-planner` for that smaller mode.

## Core Principle

An orchestration kit is a **machine-readable execution contract**, not a brainstorming document. Every agent must know exactly what to do, what not to touch, how to report, and when to stop.

## Workflow

### 1. Inspect Or Create Package Materials

Before generating any orchestration artifacts, verify that the work is executable. If package docs already exist, inspect them. If they do not exist, create orchestration-ready package docs directly from the user request and local context.

- Read the original user request.
- Read INDEX.md and ALL package docs when they exist.
- If no package docs exist, inspect enough local context to split the work into concrete packages.
- Check that every package has concrete acceptance criteria and verification commands.
- Check current git status.
- If package docs lack the [orchestration-ready fields](`) (Package ID, File Ownership, Allowed Paths, Forbidden Paths, Dependencies, Parallel Safety, Expected Evidence Pack), either:
  - Fill in the missing fields yourself if the information is obvious from the package content, OR
  - Create new orchestration package docs with those fields.

### 2. Select Execution Mode

Analyze the packages and automatically select the best mode. Document your choice and the rejected alternatives in INDEX.md.

| Mode | When To Use | Max Packages | Key Trait |
|---|---|---|---|
| `SINGLE_AGENT` | 1–2 packages, tightly coupled files, low concurrency benefit | 1–2 | Simplest; one agent does everything in sequence |
| `AGENT_VIEW` | 2–10 relatively independent packages, user wants manual Agents View control | 2–10 | User pastes prompts into Claude Code Agent View; each agent uses its assigned branch/worktree policy |
| `BACKGROUND_AGENT_SCRIPT` | User wants automatic task creation for independently launchable packages | 2–20 | Generated `dispatch-claude-agents.sh` launches one `claude --bg --name` background session per ready package, then opens or points to `claude agents` |
| `BATCH` | Repo-wide mechanical migration, lint/type rule rollout, test migration | Any (single command) | Output one `/batch` instruction, not N package prompts |
| `AGENT_TEAM` | Research, review, multi-hypothesis debugging, cross-layer exploration only | 2–5 | Experimental; higher token cost; NOT for direct implementation of risky changes |
| `CODEX_RETAINED_REVIEW` | Final acceptance, multimodal judgment, product taste, cross-package consistency audit | 1 (Codex) | Codex does NOT do grunt implementation; it validates deliverables |

**Decision rules**:
- If all packages touch the same 1–3 files → `SINGLE_AGENT`, or recommend `agent-handoff-planner` if no orchestration is needed.
- If packages are file-disjoint and 2–10 → `AGENT_VIEW` (manual default).
- If user says "自动" or "批量启动" → `BACKGROUND_AGENT_SCRIPT`.
- If packages have ordered dependencies, still use `BACKGROUND_AGENT_SCRIPT` when automation is useful, but make the script dependency-aware instead of launching every package unconditionally.
- If there are more than 10 implementation packages, use staged waves and an integration branch policy; do not start all agents at once unless file ownership and validation capacity are clearly safe.
- If the task is a mechanical transform across the whole repo → `BATCH`.
- If the user explicitly asks for research/review by multiple agents → `AGENT_TEAM` (warn about token cost).
- Always reserve `CODEX_RETAINED_REVIEW` for final integration audit.
- Before writing any Claude launch command, check the official CLI reference and local version. Do not rely only on `claude --help`, because it may omit supported flags.

### 3. Generate Orchestration Kit

Create the following directory structure under the plan directory:

```
docs/plans/<plan-name>/
├── INDEX.md
├── packages/
│   ├── 01-<name>.md
│   ├── 02-<name>.md
│   └── 99-integration-audit.md
├── launchers/
│   ├── agent-view-prompts.md
│   ├── package-graph.tsv
│   └── dispatch-claude-agents.sh
├── status/
│   ├── README.md
│   ├── package-status-template.md
│   └── <package-id>.md (one per package, initially empty)
└── validation/
    └── final-audit-prompt.md
```

### 4. INDEX.md Required Sections

INDEX.md is the master control document. It MUST contain every section below.

```markdown
# <Plan Title> — Orchestration Index

## Goal
[One paragraph describing the combined outcome of all packages.]

## Execution Mode Recommendation
- Recommended mode: <SINGLE_AGENT | AGENT_VIEW | BACKGROUND_AGENT_SCRIPT | BATCH | AGENT_TEAM | CODEX_RETAINED_REVIEW>
- Why: <1–2 sentence justification>
- Alternatives rejected: <mode — reason>
- Max parallel agents: <N>
- Codex-retained work: <what only Codex should do>

## Repository And Branch Policy
- Main checkout: <absolute path to coordinator checkout>
- Coordinator plan root: <absolute path to docs/plans/<name>>
- Implementation isolation: <worktree per package | shared worktree per wave | explicit no-worktree exception>
- Branch naming: <branch prefix and package-id format>
- Integration branch: <branch name | manual merge only>
- Package agents must commit only implementation files, tests, and package-owned docs; coordinator status files are external coordination state and must not be included in implementation commits unless explicitly requested.

## Execution Authorization

You (the external agent) are authorized to do the following WITHOUT asking for confirmation:
- Read the plan, index, and all referenced package documents.
- Create or reuse an isolated git worktree for implementation.
- Make scope-bounded edits, add/update tests, and update docs as described in your assigned package.
- Run the listed verification commands.
- Commit locally within the worktree branch.
- Merge, push, or create PRs for worktree branches (incremental, non-destructive operations).
- Write to ONLY the assigned coordinator status file at the absolute path given in the prompt — never edit INDEX.md or another package's status file.
- Mark that coordinator status file `in_progress` when starting, then `completed` or `blocked` when finishing.
- If you work in an isolated git worktree, do NOT rely on the worktree copy of `status/<package-id>.md`; the dispatcher only reads the coordinator status file under the original plan directory.

## Stop Gates — Must Ask

STOP and ask the user before:
- Crossing Stage boundaries or making architectural decisions beyond scope.
- Product-level decisions where requirements are genuinely ambiguous.
- Destructive git operations: force-push, hard reset, deleting branches/worktrees.
- Network access, external API calls, or adding secrets/credentials.
- Overwriting unrelated dirty changes outside your assigned Allowed Paths.
- Fixing verification failures when the fix expands scope beyond your package.

## Completion Policy

After completing your assigned package:
- Write your evidence pack to the coordinator status file and set `Status` to `completed`, or `blocked` if acceptance criteria cannot be met — do NOT edit INDEX.md.
- If sandbox permissions prevent writing the coordinator status file directly, write the evidence to your worktree copy and report the exact source path plus the required sync command; do NOT claim the package is dependency-unlocking until the coordinator status file is updated.
- Merge, push, or create a PR as the final step — no need to ask.
- Report: what changed, test results, merge/PR status, and branch/worktree path.
- Do NOT delete the worktree unless explicitly instructed.

## Concurrency Plan
| Group | Packages | Can Run In Parallel | Must Wait For | Conflict Risk |
|---|---|---|---|---|
| G1 | 01-xxx | yes (with G2) | none | safe — disjoint files |
| G2 | 02-xxx | yes (with G1) | none | safe — disjoint files |
| G3 | 03-xxx | no | G1, G2 | caution — reads files G1 writes |

## Dependency Graph
| Package | Depends On | Unlocks | Ready When | Notes |
|---|---|---|---|---|
| 01-xxx | none | 03-xxx | immediately | can launch in first wave |
| 02-xxx | none | 03-xxx | immediately | can launch in first wave |
| 03-xxx | 01-xxx, 02-xxx | 99-audit | both dependency status files show completed | integration package |
| 99-audit | all implementation packages | none | all package status files show completed | Codex retained |

## File Ownership Map
| Path / Glob | Owner Package | Other Packages Must Not Edit |
|---|---|---|
| src/auth/** | 01-auth-refactor | 02, 03 |
| src/logging/** | 02-logging-opt | 01, 03 |
| src/shared/types.ts | 01-auth-refactor | 02 must coordinate before editing |

## Agent Budget
- Recommended Claude Code agents: <N>
- Max parallel agents: <N>
- Codex usage: <final audit only | multimodal tasks | etc.>
- When to pause: <condition that should stop all agents>

## Dispatch Plan
| Package | Mode | Agent Name | Prompt File | Status File | Depends On | Auto-Dispatch Rule |
|---|---|---|---|---|---|---|
| 01-xxx | agent-view | agent-01-xxx | launchers/agent-view-prompts.md#pkg-01 | status/01-xxx.md | none | ready immediately |
| 02-xxx | agent-view | agent-02-xxx | launchers/agent-view-prompts.md#pkg-02 | status/02-xxx.md | none | ready immediately |
| 03-xxx | agent-view | agent-03-xxx | launchers/agent-view-prompts.md#pkg-03 | status/03-xxx.md | 01-xxx, 02-xxx | launch when dependencies are completed |
| 99-audit | codex | — | validation/final-audit-prompt.md | status/99-audit.md | all implementation packages | manual Codex audit unless explicitly automated |

## Status Ledger
| Package | Agent | Status | Worktree | Commit/PR | Verification | Evidence |
|---|---|---|---|---|---|---|
| 01-xxx | — | pending | — | — | — | — |
| 02-xxx | — | pending | — | — | — | — |
| 99-audit | — | pending | — | — | — | — |

## Merge Strategy
- Merge order: <e.g., 01 → 02 → 03, or any order then integration rebase>
- Code dependency policy: <downstream starts only after upstream commit is merged to integration branch | downstream may base on upstream branch | status-only dependency>
- Rebase policy: <rebase on latest main before PR | merge as-is>
- Conflict owner: <which package resolves conflicts if two packages touch adjacent code>
- Final integration agent: <Codex | specific package agent>
- Do not delete worktrees until: <final audit passes | user confirms>

## Evidence Pack Required From Each Agent

Each agent MUST write to its own `status/<package-id>.md` file after completion.
Do NOT edit INDEX.md directly — that causes concurrent-write conflicts.

Evidence pack must include:
- [ ] worktree path
- [ ] branch name
- [ ] base commit
- [ ] git status
- [ ] git diff --stat
- [ ] changed files (full list)
- [ ] commands run (verification commands + output summary)
- [ ] test result summary (pass/fail counts)
- [ ] commit hash / PR link
- [ ] merge/integration status
- [ ] unresolved risks (if any)
- [ ] whether it touched only allowed paths (self-certify)

## Package Documents
| Work Package | Target Agent | Dependency | Parallel Safety | Purpose |
|---|---|---|---|---|
| [01-xxx.md] | implementation agent | none | safe | [...] |
| [02-xxx.md] | implementation agent | none | safe | [...] |
| [99-integration-audit.md] | Codex retained | after all packages | — | [...] |

## Recommended Execution Order
1. Launch G1 packages in parallel.
2. Launch G2 packages after G1 completes.
3. Run integration audit after all packages complete.

## Launch Options
- **Option A**: Agent View manual dispatch — copy prompts from `launchers/agent-view-prompts.md`.
- **Option B**: background agent script — run `bash launchers/dispatch-claude-agents.sh` to create background sessions and view them in `claude agents`.
- **Option C**: `/batch` — use the batch instruction in `launchers/batch-instruction.md`.
- **Option D**: Final integration audit — give `validation/final-audit-prompt.md` to Codex.
```

### 5. launchers/agent-view-prompts.md

Generate one prompt per package. Each prompt must be self-contained enough for a Claude Code agent to start work, but reference INDEX and package doc for full detail.

Format:

```markdown
# Agent View Prompts

## Package: <package-id> — <title>

Copy the block below into Claude Code Agent View.

---

**Mode**: package executor
**INDEX**: <repo-root>/docs/plans/<name>/INDEX.md
**Package doc**: <repo-root>/docs/plans/<name>/packages/<package-id>-<name>.md
**Status file**: <repo-root>/docs/plans/<name>/status/<package-id>.md

**File ownership**: you may edit <allowed-paths>. Do NOT touch <forbidden-paths>.
**Dependencies**: <none | wait for package X to complete first>. If dependencies exist, start only after the dependency status files show `completed`.
**Status updates**: the status file above is the coordinator status file, even if you create a separate implementation worktree. Immediately set that exact file to `in_progress`; when finished, set that exact file to `completed` or `blocked` and include the evidence pack. Do not only update a same-path copy inside your implementation worktree.

**Stop gates**: force-push, hard reset, delete worktree, expand scope, touch forbidden paths → stop and ask.

**Evidence pack**: when done, write completion evidence to your status file (not INDEX.md). Include worktree path, branch, git diff --stat, changed files, commands run, test results, commit/PR, unresolved risks, and a self-certification that you only touched allowed paths.

---

<repeat for each package>
```

### 6. launchers/dispatch-claude-agents.sh

Generate an executable dispatch script. Default to NOT running it automatically — the user decides.

The script MUST be idempotent and dependency-aware:
- Read `launchers/package-graph.tsv` to discover packages, package docs, status files, and dependencies.
- Launch only packages whose dependencies are completed.
- Skip packages that are already `completed`, `in_progress`, or already listed as launched in `status/.dispatch-state.tsv`.
- Print blocked packages with the specific dependency statuses that prevent launch.
- Support repeated manual runs: after upstream agents finish and write `completed`, running the same script again launches newly-ready downstream packages.
- Support optional watch mode (`ORCHESTRATION_WATCH=1`) that polls status files and launches newly-ready packages until all non-manual packages are complete.
- Do NOT make package agents recursively invoke the dispatcher from inside their own task. Centralized watch mode is safer and easier to audit than agent self-triggering.
- Treat `99-integration-audit` as manual by default unless the user explicitly asks to automate the final audit.

Generate `launchers/package-graph.tsv` with a header and one row per package:

```tsv
package_id	package_doc	status_file	dependencies	manual
01-xxx	packages/01-xxx.md	status/01-xxx.md		0
02-xxx	packages/02-xxx.md	status/02-xxx.md		0
03-xxx	packages/03-xxx.md	status/03-xxx.md	01-xxx,02-xxx	0
99-integration-audit	packages/99-integration-audit.md	status/99-integration-audit.md	01-xxx,02-xxx,03-xxx	1
```

For more than 10 packages, generate waves in the graph and cap concurrent launches with `ORCHESTRATION_MAX_PARALLEL`. Do not dispatch every package at once just because it is dependency-ready.

The script launches one Claude Code background session per ready package with `claude --bg --name`, then prints the `claude agents` command. Do not open Agents View by default, because users may run several dispatch scripts from one terminal.

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PLAN_DIR="$REPO_ROOT/docs/plans/<plan-name>"
GRAPH_FILE="$PLAN_DIR/launchers/package-graph.tsv"
DISPATCH_STATE="$PLAN_DIR/status/.dispatch-state.tsv"

cd "$REPO_ROOT"

# Pre-flight checks
command -v claude >/dev/null 2>&1 || { echo "ERROR: claude CLI not found"; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "ERROR: not a git repository"; exit 1; }
[ -f "$PLAN_DIR/INDEX.md" ] || { echo "ERROR: INDEX.md not found at $PLAN_DIR/INDEX.md"; exit 1; }
[ -f "$GRAPH_FILE" ] || { echo "ERROR: package graph not found at $GRAPH_FILE"; exit 1; }
CLAUDE_VERSION="$(claude --version || true)"
CLAUDE_MODEL="${CLAUDE_MODEL:-sonnet}"
CLAUDE_EFFORT="${CLAUDE_EFFORT:-xhigh}"
CLAUDE_PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-}"
CLAUDE_SETTING_SOURCES="${CLAUDE_SETTING_SOURCES:-user,project,local}"
CLAUDE_OPEN_AGENT_VIEW="${CLAUDE_OPEN_AGENT_VIEW:-0}"
ORCHESTRATION_WATCH="${ORCHESTRATION_WATCH:-0}"
ORCHESTRATION_INCLUDE_MANUAL="${ORCHESTRATION_INCLUDE_MANUAL:-0}"
ORCHESTRATION_POLL_SECONDS="${ORCHESTRATION_POLL_SECONDS:-30}"
ORCHESTRATION_MAX_PARALLEL="${ORCHESTRATION_MAX_PARALLEL:-10}"

echo "=== Claude Code ==="
echo "$CLAUDE_VERSION"
echo
echo "=== Dependency-aware dispatch ==="

mkdir -p "$PLAN_DIR/status"
touch "$DISPATCH_STATE"

status_of() {
  local status_file="$1"
  if [ ! -f "$status_file" ]; then
    echo "pending"
    return
  fi
  local status_line
  status_line="$(grep -Eim1 '^- \*\*Status\*\*:' "$status_file" || true)"
  if [ -z "$status_line" ]; then
    echo "pending"
    return
  fi
  local parsed_status
  parsed_status="$(echo "$status_line" | sed -E 's/.*Status\*\*: *//; s/[ <>]//g' | tr '[:upper:]' '[:lower:]')"
  case "$parsed_status" in
    pending|in_progress|completed|blocked) echo "$parsed_status" ;;
    *) echo "pending" ;;
  esac
}

already_launched() {
  local package_id="$1"
  grep -Eq "^${package_id}[[:space:]]" "$DISPATCH_STATE"
}

dependencies_ready() {
  local deps="$1"
  local dep dep_status dep_status_file
  [ -z "$deps" ] && return 0
  IFS=',' read -ra dep_array <<<"$deps"
  for dep in "${dep_array[@]}"; do
    dep="${dep// /}"
    dep_status_file="$(awk -F '\t' -v id="$dep" 'NR > 1 && $1 == id { print $3 }' "$GRAPH_FILE")"
    if [ -z "$dep_status_file" ]; then
      echo "unknown dependency $dep"
      return 1
    fi
    dep_status="$(status_of "$PLAN_DIR/$dep_status_file")"
    if [ "$dep_status" != "completed" ]; then
      echo "$dep=$dep_status"
      return 1
    fi
  done
  return 0
}

all_launchable_complete() {
  local package_id package_doc status_file dependencies manual current_status
  while IFS=$'\t' read -r package_id package_doc status_file dependencies manual; do
    [ "$package_id" = "package_id" ] && continue
    [ -z "$package_id" ] && continue
    [ "$manual" = "1" ] && [ "$ORCHESTRATION_INCLUDE_MANUAL" != "1" ] && continue
    current_status="$(status_of "$PLAN_DIR/$status_file")"
    [ "$current_status" = "completed" ] || return 1
  done < "$GRAPH_FILE"
  return 0
}

launch_agent() {
  local package_id="$1"
  local package_doc="$2"
  local status_file="$3"
  local name="agent-${package_id}"
  local prompt
  prompt="Read $PLAN_DIR/INDEX.md and $package_doc. Implement package $package_id. Treat $status_file as the coordinator status file outside any implementation worktree. Immediately mark that exact file Status as in_progress. When done, set that exact file Status to completed or blocked and write the evidence pack there. Do NOT only update a same-path copy inside your worktree. Do NOT edit INDEX.md or other status files."
  echo "Launching $name"
  set +e
  if [ -n "$CLAUDE_PERMISSION_MODE" ]; then
    output="$(claude \
      --bg \
      --name "$name" \
      --model "$CLAUDE_MODEL" \
      --effort "$CLAUDE_EFFORT" \
      --permission-mode "$CLAUDE_PERMISSION_MODE" \
      --setting-sources "$CLAUDE_SETTING_SOURCES" \
      "$prompt" 2>&1)"
  else
    output="$(claude \
      --bg \
      --name "$name" \
      --model "$CLAUDE_MODEL" \
      --effort "$CLAUDE_EFFORT" \
      --setting-sources "$CLAUDE_SETTING_SOURCES" \
      "$prompt" 2>&1)"
  fi
  status=$?
  set -e
  if [ "$status" -ne 0 ]; then
    echo "$output" >&2
    if [ "$CLAUDE_PERMISSION_MODE" = "auto" ] && grep -qi "requires opting in" <<<"$output"; then
      echo >&2
      echo "ERROR: Claude Code requires one interactive auto-mode opt-in before --bg can use --permission-mode auto." >&2
      echo "Run once interactively: claude --permission-mode auto" >&2
      echo "Or rerun this script without auto mode: CLAUDE_PERMISSION_MODE=default bash launchers/dispatch-claude-agents.sh" >&2
    fi
    return "$status"
  fi
  echo "$output"
  printf "%s\t%s\t%s\n" "$package_id" "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$DISPATCH_STATE"
}

dispatch_ready_once() {
  local launched_any=0
  local launch_count=0
  while IFS=$'\t' read -r package_id package_doc status_file dependencies manual; do
    [ "$package_id" = "package_id" ] && continue
    [ -z "$package_id" ] && continue

    local abs_package_doc="$PLAN_DIR/$package_doc"
    local abs_status_file="$PLAN_DIR/$status_file"
    [ -f "$abs_package_doc" ] || { echo "ERROR: missing package doc $abs_package_doc"; exit 1; }

    local current_status
    current_status="$(status_of "$abs_status_file")"
    if [ "$current_status" = "completed" ]; then
      echo "SKIP $package_id: completed"
      continue
    fi
    if [ "$current_status" = "in_progress" ] || already_launched "$package_id"; then
      echo "SKIP $package_id: already launched or in progress"
      continue
    fi
    if [ "$manual" = "1" ] && [ "$ORCHESTRATION_INCLUDE_MANUAL" != "1" ]; then
      echo "SKIP $package_id: manual package"
      continue
    fi

    local blocked_reason
    if ! blocked_reason="$(dependencies_ready "$dependencies")"; then
      echo "BLOCKED $package_id: waiting for $blocked_reason"
      continue
    fi

    if [ "$launch_count" -ge "$ORCHESTRATION_MAX_PARALLEL" ]; then
      echo "PAUSE $package_id: max launches reached for this pass ($ORCHESTRATION_MAX_PARALLEL)"
      continue
    fi

    launch_agent "$package_id" "$abs_package_doc" "$abs_status_file"
    launch_count=$((launch_count + 1))
    launched_any=1
  done < "$GRAPH_FILE"

  return "$launched_any"
}

if [ "$ORCHESTRATION_WATCH" = "1" ]; then
  while true; do
    if all_launchable_complete; then
      echo "All launchable packages are completed."
      break
    fi
    set +e
    dispatch_ready_once
    launched=$?
    set -e
    if [ "$launched" -eq 0 ]; then
      sleep "$ORCHESTRATION_POLL_SECONDS"
    else
      sleep 5
    fi
  done
else
  dispatch_ready_once || true
fi

echo
echo "=== Dispatch pass complete ==="
echo "View them with:"
if [ -n "$CLAUDE_PERMISSION_MODE" ]; then
  echo "  claude agents --cwd \"$REPO_ROOT\" --model \"$CLAUDE_MODEL\" --effort \"$CLAUDE_EFFORT\" --permission-mode \"$CLAUDE_PERMISSION_MODE\" --setting-sources \"$CLAUDE_SETTING_SOURCES\""
else
  echo "  claude agents --cwd \"$REPO_ROOT\" --model \"$CLAUDE_MODEL\" --effort \"$CLAUDE_EFFORT\" --setting-sources \"$CLAUDE_SETTING_SOURCES\""
fi
echo
echo "Rerun this script after upstream packages complete to launch newly-ready downstream packages."
echo "For continuous dependency dispatch: ORCHESTRATION_WATCH=1 bash launchers/dispatch-claude-agents.sh"
echo "After all implementation packages complete, run the integration audit."

if [ "$CLAUDE_OPEN_AGENT_VIEW" = "1" ] && [ -t 1 ]; then
  if [ -n "$CLAUDE_PERMISSION_MODE" ]; then
    claude agents \
      --cwd "$REPO_ROOT" \
      --model "$CLAUDE_MODEL" \
      --effort "$CLAUDE_EFFORT" \
      --permission-mode "$CLAUDE_PERMISSION_MODE" \
      --setting-sources "$CLAUDE_SETTING_SOURCES"
  else
    claude agents \
      --cwd "$REPO_ROOT" \
      --model "$CLAUDE_MODEL" \
      --effort "$CLAUDE_EFFORT" \
      --setting-sources "$CLAUDE_SETTING_SOURCES"
  fi
fi
```

**Script rules**:
- `set -euo pipefail` at the top.
- `cd` to repo root.
- Check that `claude` CLI exists.
- Check that it's a git repo.
- Check that plan files and `launchers/package-graph.tsv` exist before launching.
- Launch one background session per ready package with `claude --bg --name`.
- Never launch a package whose dependencies are not completed.
- Read status only from the coordinator plan directory (`$PLAN_DIR/status/...`), not from implementation worktree copies.
- Never launch a package that is already completed, in progress, or recorded in `status/.dispatch-state.tsv`.
- Print exact blocked dependency statuses for ordered work packages.
- Include optional watch mode with `ORCHESTRATION_WATCH=1`; keep it off by default.
- Cap each dispatch pass with `ORCHESTRATION_MAX_PARALLEL`; default to 10 for large plans.
- Keep final integration audit manual by default unless the user explicitly requests full automation.
- To retry a launched package that never writes completion evidence, the user may remove that package's row from `status/.dispatch-state.tsv` after inspecting the failure.
- Default generated scripts to inherit the user's configured Claude Code permission mode by omitting `--permission-mode`; set `CLAUDE_PERMISSION_MODE=bypassPermissions`, `auto`, `default`, or another supported mode only when an explicit override is needed.
- For users who set `permissions.defaultMode` to `bypassPermissions` in `~/.claude/settings.json`, the generated background sessions will start in bypass mode without the script hard-coding it.
- If `--permission-mode auto` fails with the opt-in error, print the exact interactive opt-in command and a `CLAUDE_PERMISSION_MODE=default` fallback.
- Print `claude agents --cwd "$REPO_ROOT"` after dispatch.
- Do not open Agents View by default; open it only when `CLAUDE_OPEN_AGENT_VIEW=1`.
- Never use `--dangerously-skip-permissions`.
- Never delete worktrees.
- Never force-push or hard reset.

### 7. Status Files Instead of Shared Ledger Writes

To prevent concurrent-write conflicts, package executors MUST NOT edit INDEX.md directly. Status files are coordination files in the original plan directory, not implementation files owned by a worktree branch.

- Each agent writes ONLY to its assigned coordinator status file at the absolute path given in the prompt.
- The status file uses the `package-status-template.md` format.
- The dispatch script may write only `status/.dispatch-state.tsv` for launched-session bookkeeping.
- The integration auditor (Codex or final agent) reads all `status/*.md` files and summarizes into INDEX or a `FINAL_REPORT.md`.
- If an implementation worktree also contains a stale copy of `docs/plans/.../status/<package-id>.md`, ignore it unless it has been explicitly synchronized back to the coordinator status path.

**status/README.md**:

```markdown
# Status Files

Each package executor writes to its own coordinator status file in this plan directory. Do NOT edit INDEX.md.

## How to use
1. Copy `package-status-template.md` to `<package-id>.md`.
2. Set `Status` to `in_progress` in this coordinator file when starting.
3. Set `Status` to `completed` in this coordinator file when done, or `blocked` if acceptance criteria cannot be met.
4. Fill in each evidence section as you complete the package.
5. Do not rely on a status-file copy inside an implementation worktree; dependency dispatch reads this coordinator file only.
6. Do not edit other packages' status files.
```

**status/package-status-template.md**:

```markdown
# Package Status: <package-id>

- **Agent**: <agent name / Claude Code window>
- **Status**: <pending | in_progress | completed | blocked>
- **Started**: <timestamp>
- **Completed**: <timestamp>

## Worktree
- Path:
- Branch:
- Base commit:

## Changes
- git status:
- git diff --stat:
- Changed files:

## Verification
- Commands run:
- Test results:

## Delivery
- Commit hash:
- PR link:
- Integration status:

## Self-Certification
- [ ] Only touched allowed paths
- [ ] Did not edit forbidden paths
- [ ] Did not edit INDEX.md or other status files

## Unresolved Risks
- <none | list>
```

### 8. Integration Audit

Generate `packages/99-integration-audit.md` and `validation/final-audit-prompt.md`.

The audit task MUST:

1. Re-read the original INDEX and all package docs.
2. Re-read all `status/*.md` files.
3. Check git status, diff, commits/PRs.
4. Compare delivery against EACH acceptance criterion from each package.
5. Check for cross-package duplication, conflicts, or file ownership violations.
6. Run final integration verification commands.
7. Fix only scope-contained, low-risk, obvious omissions — do NOT expand scope.
8. Output one of: **PASS** | **PARTIAL** (list unmet criteria) | **FAIL** (blocking issues).

**validation/final-audit-prompt.md**:

```markdown
# Final Integration Audit

## Context
- INDEX: <path>
- Packages: <list>
- Status files: <glob>

## Audit Steps
1. Read INDEX.md and all package docs.
2. Read all status/<package-id>.md files.
3. Run: git status; git diff --stat; git log --oneline (recent).
4. For each package, check every acceptance criterion.
5. Run integration-level verification:
   ```bash
   # <integration test commands>
   ```
6. Check for cross-package conflicts:
   - Did any agent edit a file it wasn't supposed to?
   - Are there duplicate implementations of the same thing?
   - Do changes in different packages conflict semantically?
7. Report: PASS / PARTIAL / FAIL with specific evidence for each gap.

## Evidence Required
- Per-package acceptance criteria status (met / unmet / unverifiable).
- Integration test results.
- Cross-package conflict report.
- Final recommendation (merge / fix-then-merge / do-not-merge).
```

### 9. Output Style

After generating the orchestration kit, report concisely in chat:

- **Recommended mode**: <mode>
- **Dependency order**: <which packages run first, which packages wait, and what unlocks them>
- **Generated files**: <count and key paths>
- **How to run**:
  - Agent View: paste prompts from `launchers/agent-view-prompts.md`
  - Background script one pass: `bash launchers/dispatch-claude-agents.sh`
  - Background script continuous dependency dispatch: `ORCHESTRATION_WATCH=1 bash launchers/dispatch-claude-agents.sh`
  - Batch: see `launchers/batch-instruction.md`
- **What not to do**: force-push, hard reset, delete worktrees, edit INDEX.md from package agents
- **Where final audit starts**: `validation/final-audit-prompt.md`

## Guardrails

- Do NOT stuff all launch prompts into a monolithic INDEX.
- Do NOT require the user to manually write three launch modes.
- Do NOT let multiple agents write to INDEX.md concurrently.
- Do NOT default to AGENT_TEAM for implementation tasks.
- Do NOT default to BATCH for non-mechanical tasks.
- Do NOT delete worktrees.
- Do NOT force-push or hard reset.
- Do NOT assign Codex to low-value grunt implementation.
- Do NOT dispatch multi-agent work without acceptance criteria in every package.
- Do NOT generate the orchestration kit if the input packages lack executable acceptance criteria — fix them first or ask the user to re-run `agent-handoff-planner`.

## Relationship With agent-handoff-planner

| Concern | agent-handoff-planner | agent-orchestration-planner |
|---|---|---|
| Verify external claims | Yes | No |
| Write package docs with acceptance criteria | Yes | No (reads them) |
| Add orchestration-ready fields | Yes (when asked) | Fills gaps if missing |
| Select execution mode | No | Yes |
| Generate Agent View prompts | No | Yes |
| Generate dispatch scripts | No | Yes |
| Generate status templates | No | Yes |
| Create concurrency plan | No | Yes |
| Create file ownership map | No | Yes |
| Integration audit | Basic validation | Full cross-package audit |
| Basic INDEX with auth sections | Yes | No (reads it) |
| Full orchestration INDEX | No | Yes |

Use `agent-handoff-planner` for small design packages that the user will run manually in one to three Claude Code windows, usually in the current checkout. Use `agent-orchestration-planner` directly for medium or large multi-agent execution, Agent View, background dispatch scripts, coordinator status, worktrees, branches, staged waves, and final integration audit. Chaining the two skills is optional, not required.
