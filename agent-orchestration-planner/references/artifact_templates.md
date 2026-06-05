# Artifact Templates

This reference owns long generated Markdown templates and final user output
shape. Read it when producing `INDEX.md`, `agent-prompts.md`, `99-finalize.md`,
or the final chat instructions after creating an orchestration kit.

### 3. INDEX.md Required Sections

`INDEX.md` is the static execution contract. Dynamic status belongs in `status/`.

```markdown
# <Plan Title> - Orchestration Index

## Goal
<combined outcome>

## Projection Ownership
- `INDEX.md` owns static human intent, policy, authorization, landing strategy, capability gates, and the intended dependency contract.
- `launchers/package-graph.tsv` owns machine-readable dispatch topology. It must match the dependency intent in this INDEX.
- `status/state.tsv` owns current scheduler state. It must not be edited manually.
- `status/events.jsonl` owns append-only event history, retry accounting, and failure fingerprints.
- `status/<package-id>.md` owns human-readable evidence, risks, verification details, and blocker diagnosis.
- `scratch/` is temporary and non-authoritative; it cannot unlock dependencies or satisfy acceptance criteria by itself.
- If these projections disagree, treat the orchestration as invalid or blocked until repaired; do not infer success from one artifact alone.

## User Entry Points
- Manual: copy prompts from `launchers/agent-prompts.md` into any agent platform.
- Script: run `bash launchers/orchestrate.sh start`; by default view Claude Code agents with `claude agents`. For Codex, run with `ORCHESTRATION_RUNNER=codex` and inspect `status/launch-<package-id>.log`.
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

## Landing Strategy
- Primary landing path: <what must be true for the main plan to count as landed>
- Preapproved fallback paths, in order: <fallback id, trigger, acceptance criteria, verification, and whether it may merge to mainline>
- Unacceptable degradation: <shortcuts or partial states that must not be shipped>
- Abort conditions: <conditions that end this orchestration as failed instead of retrying>
- Independent merge candidates if main plan fails: <package ids or "none"; for each, explain independence, standalone acceptance, and standalone verification>

Allowed task-level outcomes:
- `landed`: primary path landed and verification passed.
- `landed-with-approved-fallback`: a preapproved fallback landed and verification passed.
- `ready-for-external-gate`: autonomous work is complete but a declared release-blocking external gate is still pending.
- `failed-no-merge`: the main plan failed, no fallback is approved, and nothing may be merged.
- `failed-with-candidate-independent-fixes`: the main plan failed, but predeclared independent fixes are available for separate review.

## Stop Conditions
- Any functional package is `blocked`, `stale`, or `invalid`.
- Graph has duplicate package IDs, missing dependencies, or cycles.
- Package evidence is incomplete.
- Package changed forbidden paths.
- Merge conflict or verification failure occurs.
- Status/state mismatch cannot be reconciled.
- Abort condition in Landing Strategy is met.
- A package identifies the main plan as non-landable and no preapproved fallback applies.

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

## Package Execution Authorization

The INDEX authorizes this package to perform the routine operations needed to complete its assigned scope. Do not pause for confirmation before these in-scope actions:
- Read the INDEX, package doc, assigned status file, package graph, state ledger, events log, and relevant repository files.
- Create or reuse only this package's assigned worktree and branch.
- Edit only the allowed paths named by this package.
- Run the package's listed verification commands and focused follow-up commands needed to diagnose in-scope failures.
- Continue fixing verification failures that remain inside this package's allowed scope.
- Commit local package changes to this package's branch.
- Write evidence and blocker diagnosis only to this package's coordinator status file.
- Use the orchestrator commands listed in this prompt: `scratch-path`, `mark-state`, and the final `advance --from <package-id>` tail call.

Do not wait for an interactive approval inside background execution. If the runner, sandbox, subscription, permission mode, credential boundary, network policy, or missing external capability prevents an in-scope command from running, record a blocker instead of hanging, retrying blindly, or claiming completion. Use `mark-state blocked` with:
- `--error`: the concrete authorization or capability blocker.
- `--failed-command`: the command or operation that was refused.
- `--log-summary`: the decisive refusal message, such as an approval-policy, subscription, sandbox, credential, or permission-mode error.
- `--recovery-hint`: the exact user or coordinator action needed, such as "rerun with approved permission mode", "provide manual external evidence", "mark package manual=1", or "retry after fixing runner authentication".

Forbidden without explicit user approval from the INDEX or chat:
- force-push, hard reset, or destructive git cleanup
- deleting branches/worktrees not assigned to this package
- editing outside allowed paths
- adding secrets, credentials, or private tokens
- accessing external accounts, paid services, physical devices, or human-only review gates
- changing global orchestration policy, dependency graph, or another package's status

You may edit only the allowed paths in the package doc. Do not edit INDEX.md or another package status file. If you create/use an implementation worktree, do not rely on status files inside that worktree; write the coordinator status path above.

Use scratch only for temporary shared notes, inventories, command transcripts, draft diffs, or intermediate artifacts that help another package or finalizer inspect the work. Do not put credentials, tokens, private keys, `.env` files, hidden prompts, proprietary raw data, or authoritative completion evidence in scratch. Anything required for scheduling, completion, or final acceptance must be summarized into coordinator status through `mark-state` and the package status file.

Respect projection ownership: write scheduler state only through `mark-state`, write human-readable evidence and risks in your package status file, leave static policy in INDEX, and never treat scratch or chat text as dependency-unlock evidence.

Do not attempt external-assist work inside a Claude package. If you discover a package requires a physical device, user-owned account, secret, external approval, or human-only judgment that was not declared, mark the package `blocked` with a precise recovery hint instead of improvising or claiming completion.

Do not invent an unapproved fallback. If the primary package path cannot land, classify why, identify whether an INDEX-declared fallback applies, and record whether the situation should retry, investigate, ask the user, switch to a named fallback, or abort the orchestration. If your package might be an independent merge candidate, state why it is independent and provide standalone verification; otherwise say it should be discarded if the main plan fails.

Before calling `advance`, you must:
- Set coordinator status to `completed` or `blocked`.
- Fill evidence: worktree, branch, base commit, commit hash, changed files, verification commands/results, risks.
- For blockers, classify the failure as one of: `capability-gap`, `invalid-requirement`, `external-dependency`, `verification-failure`, `merge-conflict`, `design-invalid`, `cost-out-of-scope`, or `unknown-needs-investigation`.
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
4. Check projection consistency across INDEX, graph, state, package status, and events before treating any package as globally complete.
5. Check the Capability Preflight section. If an external-assist gate is release-blocking and evidence is absent, stop with "ready for external QA" or "waiting for external gate"; do not claim overall PASS.
6. Check Landing Strategy. Decide task-level outcome before any mainline merge: `landed`, `landed-with-approved-fallback`, `ready-for-external-gate`, `failed-no-merge`, or `failed-with-candidate-independent-fixes`.
7. Decide whether merging is allowed.
8. Create or update the integration branch.
9. Merge functional package branches in Merge Strategy order.
10. Stop and record conflicts without cleaning anything.
11. Run integration verification.
12. Merge integration branch back to mainline only after verification passes and release-blocking external gates are satisfied or explicitly deferred by the user.
13. Write `FINAL_REPORT.md` and `status/99-finalize.md` for both success and failure.
14. Delete only local package branches/worktrees recorded by this orchestration after every prior step succeeds.

Failure rules:
- Any failure sets `99-finalize` to `blocked`.
- Record failure stage, command, branch, conflict files if any, log summary, and recovery suggestion in `status/99-finalize.md`.
- Also update the coordinator ledger with `mark-state 99-finalize blocked --error ... --failed-command ... --conflict-files ... --log-summary ... --recovery-hint ...`; do not leave merge/test failures only in prose.
- Check `status/events.jsonl` when explaining repeated failures; do not keep retrying the same fingerprint after the retry breaker opens.
- If the primary plan is non-landable, write a failure analysis that separates: observed facts, failed assumptions, failure category, attempted or rejected fallback paths, whether the user must decide, and the recommended next orchestration or abort action.
- Default to no merge when the task outcome is `failed-no-merge`.
- For `failed-with-candidate-independent-fixes`, list candidate package ids, recorded commits, allowed paths, standalone verification, and why each candidate is independent from the failed main plan. Do not merge a candidate unless it was predeclared in Landing Strategy and passes standalone verification.
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
- Landing strategy summary: primary landing path, preapproved fallbacks, abort conditions, and independent merge candidates if the main plan fails.

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

If the user chooses the Codex runner, include the explicit runner variable:

```bash
cd "<repo-root>"
ORCHESTRATION_RUNNER=codex bash "<absolute-plan-dir>/launchers/orchestrate.sh" start
```

Also include status and recovery commands:

```bash
bash "<absolute-plan-dir>/launchers/orchestrate.sh" status
bash "<absolute-plan-dir>/launchers/orchestrate.sh" advance
bash "<absolute-plan-dir>/launchers/orchestrate.sh" retry <package-id>
bash "<absolute-plan-dir>/launchers/orchestrate.sh" finalize
bash "<absolute-plan-dir>/launchers/orchestrate.sh" doctor --environment
bash "<absolute-plan-dir>/launchers/orchestrate.sh" collect-logs <package-id>
bash "<absolute-plan-dir>/launchers/orchestrate.sh" verify-finalize
bash "<absolute-plan-dir>/launchers/orchestrate.sh" scratch-path <package-id>
claude agents --cwd "<repo-root>"
```

For Codex runner status inspection, include:

```bash
ORCHESTRATION_RUNNER=codex bash "<absolute-plan-dir>/launchers/orchestrate.sh" doctor --environment
tail -f "<absolute-plan-dir>/status/launch-<package-id>.log"
codex resume <thread-id>
```

If a command contains placeholders such as `<package-id>`, explicitly say which concrete package IDs are valid recovery targets. Do not leave the user to infer them from the docs.

Do not present `/batch`, `dispatch-claude-agents.sh`, or a separate audit prompt as peer user entrypoints.
