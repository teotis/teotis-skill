---
name: handoff
description: Write a project-local handoff that another session or agent can resume independently, preserving goals, verified state, authorization, unresolved work, validation, and the first action without starting execution.
---

# Handoff

Prepare work for a recipient who has not read this conversation. First check whether native resume/fork or an existing task document already closes the gap. Reference adequate existing assets rather than duplicating them. Write durable handoffs in the target project's repository, never in an unrelated skill repository or operating-system temporary directory.

## Intelligence Adaptation Contract

- **Hard invariants**: Separate verified facts, inference, unknowns, and pending work. A document does not expand authorization. Preserve privacy, rejected directions, actual file/branch state, failed checks, and unfinished verification. A commit or running process does not prove completion.
- **Mode contracts**: Native continuation needs only a reference; a single handoff needs one sufficient project-local document. Multiple packages or persistent coordination require demonstrated value and a separate workflow; do not create sessions, send messages, or start background work by default.
- **User value priors**: The recipient can start, verify facts, and locate the result with little background reconstruction. Default to English unless the user requests another language.
- **Adaptive heuristics**: Adapt sections, depth, filenames, and granularity to the target project. Steps guide judgment within the contract.
- **Examples and resources**: Read `references/handoff-contract.md` for complex recovery or cross-platform work. Existing issues, task packages, ledgers, and ADRs take precedence over new authorities.

## Capability Load

Use when cross-session continuation has an independent information gap. Self-probe: who receives the work, what comes next, which evidence is still valid, where may they write, and can the first action be executed? Skip|Delta for adequate existing continuation; Light for one short handoff; Full for conflicts, recovery, or multiple dependent boundaries. Read the bundled reference when uncertainty affects authorization, irreversibility, or truthfulness. Never fabricate missing facts or present machine-specific paths as universal prerequisites.

## Placement and Content

Read target-project instructions and document layout. Update an existing handoff/task location; otherwise a suggested location is a dated topic document under the project's docs/handoffs directory. Sensitive or scratch material stays in that project's ignored workspace. Never commit private handoffs to a public repository. Infer an already-established project rather than routinely asking for a path.

Preserve the goal and success evidence, trusted state and sources, finished and remaining work, allowed/prohibited changes, key decisions and reasons, first action, validation, result destination, and stop/report conditions. When Git matters, include repository, branch, commit, dirty baseline, and task-owned changes. Absolute paths are local source clues: also provide repository-relative locations and environment prerequisites. Do not copy credentials, account details, or full conversations.

Reference existing specs, ADRs, issues, code, and artifacts. Date changeable facts and explain revalidation. Only call a command runnable when currently verified; unknown tools or branches need verify-first actions. User reports are evidence of what was reported, not proof of implementation.

## Delivery Boundary

Check project placement, source locations, independently understandable next action, and validation. Report the document path and unfinished work. File existence proves the handoff was written, not that a recipient took over or completed the task. Follow project commit rules, stage only task-owned paths, and reuse existing authorization.
