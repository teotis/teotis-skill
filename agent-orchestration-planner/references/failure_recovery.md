# Failure Recovery

This reference owns terminal failure handling, retry policy, doctor/log
reconciliation, scratch handling, and non-landable plan reporting. Read it when
a package is `blocked`, `stale`, `invalid`, when retrying work, or when
generating/validating `doctor`, `collect-logs`, `verify-package`, and
`verify-finalize` behavior.

## Failure States

- `blocked`: the package ran and found a real product, code, dependency, merge,
  or verification blocker.
- `stale`: the package was launched or active, but the runner/session cannot be
  trusted anymore, such as unreadable logs, interrupted execution, or lost
  background process.
- `invalid`: the coordinator cannot trust the launch or ledger shape, such as a
  missing session id, malformed state row, duplicate package id, missing
  dependency, forbidden transition, or execution-platform mismatch.

## Retry Rules

- Retry only `blocked`, `stale`, or `invalid` packages.
- Preserve prior `last_error`, `failed_command`, `conflict_files`,
  `log_summary`, and `recovery_hint` long enough for the retried package to
  inspect them.
- Record terminal failures in `events.jsonl` with a normalized fingerprint.
- After the same package hits the same normalized terminal failure fingerprint
  three times, stop retry and require human diagnosis.
- Do not retry a package that is `launched`, `in_progress`, `completed`,
  `finalizing`, or `finalized` unless the user explicitly changes state.
- Treat an execution-platform mismatch as a plan-level stop, not a package
  retry. Preserve the existing `status/execution-platform` record and require a
  new plan or explicit user-authorized rebind before continuing.

## Recovery Decision

Every terminal execution attempt should receive one named recovery action:

`resume | retry-same | repair-runtime | split | investigate | approved-handoff | await-user | abort`

`retry-same` is only for a classified transient runner failure and must carry
an attempt budget. Promotion from `blocked`, `stale`, or `invalid` to a success
state requires `mark-state --recovery-action <action>` so the event ledger
records why the recovery was accepted. Repeated identical failures require a
new action or a user decision; they must not silently become another retry.

`status/attempts.jsonl` is the attempt history. Package `state.tsv` remains the
dependency truth, while attempt records preserve session identity, activity,
checkpoint and termination evidence.

## Handoff

Cross-platform continuation is explicit. Create a versioned Handoff Envelope,
validate it on the target platform, and write an Accept Receipt. The source
attempt is not `transferred` until the receipt is accepted. Handoff artifacts
do not unlock downstream packages and do not authorize credentials, devices,
force-pushes or other external side effects.

## Doctor And Logs

- `doctor` runs preflight and consistency checks without launching new work.
- For active Claude sessions, `doctor` reconciles session ids and log
  readability. Unreadable or missing logs for an active session should mark the
  package `stale`, write recovery context, and emit `agent_lost` or
  `agent_logs_unreadable`.
- `doctor --environment` reports repository root, plan root, runner, CLI
  version/capability, permission mode, setting sources, and template version
  drift, plus the bound execution platform and whether continuation is
  same-platform/manual.
- `collect-logs <package-id>` writes runner logs to
  `status/logs/<package-id>.log`; logs are evidence for review, not scheduler
  truth by themselves.

## Scratch Rules

- `scratch/` is plan-local, gitignored, temporary, and non-authoritative.
- Package agents must request scratch paths through
  `orchestrate.sh scratch-path <package-id>`.
- Scratch may hold non-sensitive notes, command transcripts, inventories, draft
  diffs, or intermediate artifacts.
- Scratch must not hold credentials, secrets, private keys, `.env` files,
  hidden prompts, proprietary raw data, scheduler truth, dependency unlocks, or
  final acceptance evidence.

## Non-Landable Plans

- A package that discovers a false plan assumption should mark itself
  `blocked`, classify the failure, and say whether to retry, investigate, ask
  the user, switch to a named fallback, or abort.
- `99-finalize` must decide the task-level outcome before merging:
  `landed`, `landed-with-approved-fallback`, `ready-for-external-gate`,
  `failed-no-merge`, or `failed-with-candidate-independent-fixes`.
- When the main plan fails, default to no merge unless the INDEX predeclared
  independent merge candidates and their standalone verification passes.
