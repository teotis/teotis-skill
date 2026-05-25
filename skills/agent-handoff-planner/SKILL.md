---
name: agent-handoff-planner
description: 用于把复杂需求拆成可交给其他 agent 执行的 Markdown 实施包，核验外部 agent 反馈，区分应由 Codex 保留的高上下文/多模态任务，并在交付后按原计划验收。Use for external agent review, handoff plans, parallel work packages, and acceptance checks.
---

# Agent Handoff Planner

## Mission

Turn broad requests, external-agent findings, and implementation ideas into handoff-ready work packages that other agents can execute safely. Preserve Codex for the parts that require deep local context, multimodal judgment, product taste, or final validation.

## When To Use

Use this skill for requests containing signals like:

- "external agent reviewed this; verify it"
- "output one or more Markdown plan documents"
- "send this to non-multimodal agents"
- "split this for multiple agents to implement in parallel"
- "you handle the hardest 10% / multimodal-only part"
- "after the other agent implements it, validate/acceptance test it"
- Chinese variants such as "外部 agent 审查", "核验", "方案文档", "转给其他非多模态 agent", "并行处理", "实现落地", "你验收"

Do not use it for a tiny single-edit request unless the user explicitly asks for handoff docs or validation.

## Core Principle

A useful handoff document is not a brainstorm. It is a contract: what to inspect, what to change, what not to change, how to verify, and what evidence proves completion.

Every project should also have one stable planning home. Once you choose where handoff documents live for a project, record that location in the project's planning index so future agents can find it. For a specific multi-document handoff round, maintain a separate handoff package index as the round's top-level file.

## Workflow

### 1. Establish The Request Shape

Identify which mode the user wants:

- **Verify and plan**: external report or user diagnosis may be wrong; inspect before accepting.
- **Research and plan**: current product or competitors inform the design; cite or summarize only decision-relevant findings.
- **Split and delegate**: create multiple independent work packages for non-multimodal agents.
- **Validate delivered work**: compare another agent's implementation against the original plan.

If the mode is ambiguous, infer from the prompt and proceed. Ask only when the next action would be materially risky.

### 2. Inspect Before Planning

Read the smallest useful slice of local context:

- existing docs, AGENTS/CLAUDE instructions, README files;
- known planning indexes or planning-location conventions;
- target files or modules named by the user;
- prior plan documents if the user references them;
- current git status, so unrelated changes are not overwritten.

When an external agent claim is provided, treat it as untrusted input. Verify it against code, docs, or reproducible commands before endorsing it.

### 3. Resolve The Project Planning Location

Before writing handoff documents, find or create a stable planning location for the current project:

1. Prefer an existing planning index if present, such as `docs/plans/INDEX.md`, `docs/agent-plans/INDEX.md`, `.agents/plans/INDEX.md`, or another clearly named project planning index.
2. If no convention exists, use `docs/plans/` and create `docs/plans/INDEX.md`.
3. Record the chosen location near the top of the index so future agents reuse it instead of scattering plans across the repository.
4. When the chosen location differs from the default, mention it in the final response and link to the index.

Use the project planning index as the discovery surface for generated handoff docs and package indexes. At minimum, keep entries with:

- plan title and link;
- owner or target agent type, if known;
- status: `planned`, `in_progress`, `implemented`, `validated`, `blocked`, or `superseded`;
- creation date or last update date;
- one-line outcome or next action.

### 4. Review Recent Related Plans

Before creating a new handoff plan, check the resolved planning location for related work from the last 7 days. Use this as a reference layer, not as unquestioned truth.

Look in:

- the planning index for recently created or updated entries;
- Markdown files in the planning location whose filename, title, relevant files, modules, commands, or keywords overlap with the current request;
- nearby status notes for plans marked `implemented`, `validated`, `blocked`, or `superseded`.

When related recent plans exist:

- reuse verified context, file lists, verification commands, constraints, and known risks when still applicable;
- avoid duplicating a plan that is already active unless the new request materially changes scope;
- record dependencies, supersession, or follow-up relationships in the new package index, and add a short cross-reference in the project planning index when useful;
- cite the referenced plan documents in the new handoff document's Context or Risks And Notes section.

When no related recent plans exist, proceed normally and do not invent a reference.

### 5. Separate Work By Capability

Classify each part:

- **Codex-retained work**: multimodal inspection, screenshots/images, high-uncertainty architecture calls, final acceptance, and anything requiring broad context synthesis.
- **Delegable work**: localized implementation, tests, straightforward refactors, documentation updates, deterministic scripts.
- **Blocked work**: missing requirements, unsafe assumptions, unavailable dependencies, or changes that would require product approval.

Prefer fewer, cleaner handoff docs over many tiny fragments. Split only when work can proceed independently without shared-state conflicts.

### 6. Produce Handoff-Ready Markdown

When asked to create docs, write files under the resolved project planning location.

Use this structure for each handoff document:

````markdown
# [Specific Work Package Title]

## Goal
[One paragraph describing user-visible outcome.]

## Context
- User request:
- Verified facts:
- Relevant files:
- Non-goals:

## Implementation Scope
- [Concrete change 1]
- [Concrete change 2]

## Steps
1. Inspect ...
2. Change ...
3. Add/update tests ...
4. Run verification ...

## Acceptance Criteria
- [Observable criterion]
- [Regression criterion]
- [User experience criterion, if relevant]

## Verification Commands
```bash
[exact command]
```

## Risks And Notes
- [Known risk or dependency]
````

For multiple agents or multi-document handoffs, add a handoff package index for this round. This is the top-level file for the current plan package, distinct from the project planning index. It should list:

- package goal and user request;
- package documents and ownership;
- dependencies and recommended execution order;
- related recent plans used as references;
- status for each work package;
- final conclusions, completion notes, validation evidence, and follow-up items after work lands.

After writing or updating handoff documents, update the handoff package index in the same turn. Also update the project planning index only as the directory-level registry: point it to the package index, record the top-level status, and keep the canonical planning location discoverable.

### 7. Keep The Handoff Executable

Each document should name concrete files, modules, commands, or search terms. Avoid vague instructions like "improve architecture" unless paired with exact boundaries and acceptance criteria.

If the user wants non-multimodal agents to implement, explicitly remove multimodal tasks from their package and reserve them for Codex.

### 8. Validate Later Deliveries

When the user asks for acceptance or validation:

1. Re-open the original handoff document and user request.
2. Check git status and diff.
3. Compare delivered changes against each acceptance criterion.
4. Run the listed verification commands when feasible.
5. Report findings first: missing work, regressions, unverified claims, or mismatches.
6. Update the handoff package index with the validation result, completion status, important conclusions, and any follow-up work. Update the project planning index only with the package-level status or link changes needed for discovery.
7. Only then summarize what is complete.

If you personally execute the plan instead of delegating it, still update the handoff package index after implementation lands. Include what changed, what verification passed or was not run, and whether the plan is now `implemented`, `validated`, `blocked`, or `superseded`.

## Output Style

Lead with the decision:

- "The claim is valid; I wrote 2 handoff docs."
- "The claim is partly valid; I split only the confirmed work."
- "I would not delegate this yet; these blockers need resolution."
- "Validation found gaps; here are the failing criteria."

Then provide links to generated docs or cite exact files inspected. Keep chat concise; let the Markdown handoff carry the operational detail.

## Common Mistakes

- Accepting an external agent's conclusion without checking the code.
- Creating a plan that says what to do but not how to verify it.
- Giving non-multimodal agents screenshot/image tasks they cannot perform.
- Splitting work so finely that agents collide in the same files.
- Reporting success before comparing delivery against the original acceptance criteria.
