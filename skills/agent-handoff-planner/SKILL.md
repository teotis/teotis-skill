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
- target files or modules named by the user;
- prior plan documents if the user references them;
- current git status, so unrelated changes are not overwritten.

When an external agent claim is provided, treat it as untrusted input. Verify it against code, docs, or reproducible commands before endorsing it.

### 3. Separate Work By Capability

Classify each part:

- **Codex-retained work**: multimodal inspection, screenshots/images, high-uncertainty architecture calls, final acceptance, and anything requiring broad context synthesis.
- **Delegable work**: localized implementation, tests, straightforward refactors, documentation updates, deterministic scripts.
- **Blocked work**: missing requirements, unsafe assumptions, unavailable dependencies, or changes that would require product approval.

Prefer fewer, cleaner handoff docs over many tiny fragments. Split only when work can proceed independently without shared-state conflicts.

### 4. Produce Handoff-Ready Markdown

When asked to create docs, write files under a project-appropriate planning location. If no convention exists, use `docs/plans/`.

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

For multiple agents, create an INDEX document that ties packages together. Every INDEX must include the four authorization sections below so external agents know exactly what they can do without asking, when they must stop, how to finish, and what prompt the user should copy to start them.

````markdown
# [Title] — Package Index

## Execution Authorization

You (the external agent) are authorized to do the following WITHOUT asking for confirmation:
- Read the plan, index, and all referenced package documents.
- Create or reuse an isolated git worktree for implementation.
- Make scope-bounded edits, add/update tests, and update docs as described in each package.
- Run the listed verification commands.
- Commit locally within the worktree branch.
- Merge, push, or create PRs for worktree branches (incremental, non-destructive operations).

## Stop Gates — Must Ask

STOP and ask the user before:
- Crossing Stage boundaries or making architectural decisions beyond scope.
- Product-level decisions where requirements are genuinely ambiguous.
- Destructive git operations: force-push, hard reset, deleting branches/worktrees.
- Network access, external API calls, or adding secrets/credentials.
- Overwriting unrelated dirty changes outside this package.
- Fixing verification failures when the fix expands scope beyond this package.

## Completion Policy

After completing all packages:
- Merge, push, or create a PR as the final step — no need to ask.
- Report: what changed, test results, merge/PR status, and branch/worktree path.
- Do NOT delete the worktree unless explicitly instructed.

## Package Documents
| Work Package | Target Agent | Dependency | Purpose |
|---|---|---|---|
| [01-package-name.md] | implementation agent | none | [...] |
| [02-package-name.md] | implementation agent | after 01 | [...] |
| [XX-codex-validation.md] | Codex retained | after implementation | [...] |

## Recommended Execution Order
1. ...
2. ...
3. Return to Codex for validation.

## Launch Prompt

Copy this exact message to start an external Claude Code agent:

```
/using-superpowers
执行授权：你可以在本任务范围内自行创建/使用隔离 worktree，读取方案，实施 scope 内修复，更新必要测试/文档，运行列出的验证命令，在 worktree 分支内本地提交，并在完成后自行 merge/push/PR；不要为这些常规步骤询问确认。不要 force-push、hard reset、删除 worktree。只有遇到 Stop Gates 才停下询问。
核查现状，并恰当落地如下优化方案：<PLAN_PATH>
```
````

The authorization sections eliminate unnecessary confirmation prompts (worktree creation, merge asking, cleanup) while keeping the human safety gates intact.

### 5. Keep The Handoff Executable

Each document should name concrete files, modules, commands, or search terms. Avoid vague instructions like "improve architecture" unless paired with exact boundaries and acceptance criteria.

If the user wants non-multimodal agents to implement, explicitly remove multimodal tasks from their package and reserve them for Codex.

### 6. Validate Later Deliveries

When the user asks for acceptance or validation:

1. Re-open the original handoff document and user request.
2. Check git status and diff.
3. Compare delivered changes against each acceptance criterion.
4. Run the listed verification commands when feasible.
5. Report findings first: missing work, regressions, unverified claims, or mismatches.
6. Only then summarize what is complete.

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
- Producing an INDEX.md without execution authorization, stop gates, completion policy, or launch prompt — this causes external agents to interrupt the human with unnecessary confirmation prompts for worktree creation, merging, and cleanup.
