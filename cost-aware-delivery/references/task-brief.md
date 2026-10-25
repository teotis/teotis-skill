# Task brief and division calibration

Adapt to the task. The goal is a capable recipient delivering the required outcome at lower total cost, not mandatory fields or a new state system.

## What one brief should carry

- Goal/scope: final object, total scope, batch scope, completed engineering, and production still pending.
- Starting point: repository/data locations, verified entry points, procedures, reusable assets, and target baseline.
- Decisions: settled direction and reasons plus judgment left to the recipient.
- Method: actual commands/steps, input acquisition, why examples are acceptable, and common failure signals. Examples are not current execution evidence.
- Quality/closure: recipient-run checks, dimensions needing judgment, result destination, and evidence requirements. No automatic origin-model review.
- Failure: missing materials, conflict, authorization, and irreversible boundaries; isolate independent exceptions without inventing evidence.

## Budget, value, and evidence

Define a first visible result, relevant budget categories (source attempts, retries, time/tokens, receipts, or paid calls), task-specific soft limits, early stopping, and evidence locations. Numbers depend on platform and risk. Quality gates remain binding when budgets end: preserve evidence and report partial/blocked, impact, and next action.

Distinguish scope-accepted, first-value-landed, and integrated/published. Name a representative patch, usable page, or small accepted batch as first value; receiving work or generating candidates is not landed value. Complete-batch counts cannot replace early quality evidence.

Handoffs carry stable fields, evidence IDs, locations, state, remaining actions, permission boundaries, and next steps. Store long outputs/attempts in recoverable project locations rather than copying observations repeatedly. Missing detailed evidence is unknown/missing evidence.

For platform/batch comparisons, count accepted deliverable units that passed the actual quality gate. Optional metrics include first-value latency, time/tokens per accepted unit, rework, evidence recovery, and budget exhaustion. Self-reported completion counts are not evidence; absent telemetry cannot establish rankings.

Recipients may lack this conversation, tools, or filesystem. Prefer project-relative paths and native CLIs; mark unverified recipient prerequisites without blocking unrelated work. Resolve feasible integration gaps within existing authorization before handing over an unavailable branch. Document backup, checkpoint, and idempotency only where relevant. Semantic quality needs concrete good/bad criteria, not keywords, nonempty fields, or green tests alone. External startup prompts default to English with consistent scope and permissions.

## Executor capabilities and network

Delegation is optional and permitted only when the recipient environment and authorization support it. Missing concurrency does not prevent single-agent completion. Divide independent evidence, review, or edits by object/write boundary; give minimum inputs, destinations, and permissions. One integration owner handles shared assets that cannot be written concurrently. Workers cannot expand network/payment/edit permissions, and worker completion does not prove integration. Do not prescribe model brands, worker counts, or return-to-origin gates.

Verify only the required targets and recipient's current network configuration. Never copy a designer machine's proxy port as a universal default. A listening port is not evidence that the target can be reached through it. An optional bounded read-only HTTP proxy probe is:

```bash
curl --proxy '<EXECUTOR_PROXY_URL>' --noproxy '' --connect-timeout 10 --max-time 30 --fail --silent --show-error --output /dev/null 'https://TARGET_HOST/'
```

Use the verified protocol: SOCKS requires compatible socks5h configuration, not an HTTP address relabeled by port. Keep proxy environment changes process-local and preserve appropriate NO_PROXY for local/internal access. Distinguish proxy failure, permission, rate limiting, and content failure; follow retry budgets and continue independent work. Do not silently switch network routes or claim the recipient's connectivity from another machine's result.

## External resource lifecycle

Before issuing a batch brief, answer three questions: which persistent resources will this create or reuse; who owns final integration; and when may resources be released. A stateless small task may state that this section does not apply rather than inventing a control plane.

- Placement admission and capacity: before work starts, classify the output profile (cache, executable/runtime, media, or evidence), then state the destination volume, expected size, and final location. When a project read-only placement advisory exists, use its current output and preserve its explicit allow, blocked, and gray-zone decision. A blocked result means change the location or shrink the batch; the brief author must not relabel it as an exception. An old storage report is not current capacity evidence. Without such a check, record the capacity source and time and mark volume suitability unverified. Default admission puts regenerable small-file caches on a local APFS volume rather than exFAT, executable or load-intensive runtimes on the internal data volume, large media on the exchange volume, and canonical evidence in the project-authoritative location without leaving exFAT or sparse-bundle volumes as the only copy. Keep the rule focused on material usage: a small temporary output may exceptionally use a suboptimal volume only when the advisory explicitly permits that profile, its expected size stays within the configured gray-zone cap, gray use is explicitly enabled, and a removal or migration deadline is recorded. Do not make the gray zone a default production path or expand batch authorization because of one temporary file.
- Inventory and limits: name the worktrees, branches, runs/claims, batch directories, and evidence locations to create or reuse; audit similar leftovers first instead of defaulting to another fresh set per round. State task-specific workspace-count, evidence-size, and disk early-stop limits. Reuse existing sparse-checkout, deduplication, or archive mechanisms instead of copying the whole repository and duplicate evidence into every worker.
- Project-side gate pattern: projects creating batch worktrees or runs should follow the established vocab-run pattern: check destination free space and the existing worktree count before creating a worktree, exclude historical large objects from checkout by default, and release claims by owner after final integration or a zero-change receipt. Override gates require a recorded reason. The project, not a generic control plane, owns this lifecycle.
- Final path: workers may produce candidates, while one integration owner updates the formal library, ledger, and other shared assets. State whether final closure is a patch entering the target baseline, a zero-change receipt, or explicit abandonment of unreceived work. Zero change is valid closure and must not force cosmetic edits.
- Release and cleanup: active claims, locks, or shared reservations are released only after execution stops, evidence is preserved, and final integration or abandonment is recorded. Missing processes, old timestamps, or an absent worktree do not justify takeover; completed runs also must not block future task pools indefinitely. Cleanup is an explicitly authorized action, not an automatic ending.
- Preserve before removal: before deleting worktrees, branches, or run directories, preserve unmerged commits, tracked diffs, untracked evidence, and a verifiable manifest with a recovery path. Omit preservation only when those assets are already in the target baseline or explicitly abandoned; a missing process is not evidence.

## Calibration and counterexamples

For mechanical code updates, settle compatibility and transformations, validate risk points, then let a capable recipient perform repeated edits and native checks. For batch content problems, fix shared methods/tools and representative hard cases before delegating production; writing a prompt alone does not prove better output. Distinguish accessible, substantive, and accepted content rather than erasing quality differences with coverage counts.

A single wording change should usually be finished directly. A planning-only request should not become refactoring. No reusable engineering defect means the hard work may be a decision or sample, not code. If delegation cannot meet quality, reduce difficult judgments or explain the tradeoff; low cost is not a quality exemption. Delivering a brief does not authorize launching, reminders, polling, or mandatory return review.
