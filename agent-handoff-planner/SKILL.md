---
name: agent-handoff-planner
description: >
  用于小型任务方案、外部 agent 反馈核验、1-3 个 Claude Code 窗口可手动执行的 Markdown 分包、Codex 保留项划分和交付验收。
  Use for lightweight handoff plans, direct-execution packages, and acceptance checks.
whenToUse: >
  当用户需要把一个请求拆成少量可手动执行的 agent 包、核验外部 agent 分析、规划 1-3 个窗口的协作、或做最终验收时使用。
  不用于用户明确要求中大型自动编排、Claude Agents View、claude --bg 自动派工、状态账本推进或自动合并的场景；这些应使用 agent-orchestration-planner。
---

# Agent Handoff Planner

## Mission

Turn broad requests, external-agent findings, and implementation ideas into lightweight, handoff-ready design packages for small execution runs. This skill is for plans that a user can execute by opening one to three Claude Code windows. Each package gets its own worktree and branch for clean isolation, using `using-git-worktrees` to create the worktrees. Preserve Codex for the parts that require deep local context, multimodal judgment, product taste, or final validation.

## When To Use

Use this skill for requests containing signals like:

- "external agent reviewed this; verify it"
- "output one or more Markdown plan documents"
- "send this to non-multimodal agents"
- "split this for one to three Claude Code windows"
- "you handle the hardest 10% / multimodal-only part"
- "after the other agent implements it, validate/acceptance test it"
- Chinese variants such as "外部 agent 审查", "核验", "方案文档", "转给其他非多模态 agent", "并行处理", "实现落地", "你验收"

Do not use it for a tiny single-edit request unless the user explicitly asks for handoff docs or validation.

Do not use it for medium or large orchestration: Agent View, background scripts, automatic dispatch, coordinator status ledgers, worktree/branch control, or roughly four or more concurrent packages. Use `agent-orchestration-planner` directly for those needs.

## Core Principle

A useful handoff document is not a brainstorm. It is a contract: what to inspect, what to change, what not to change, how to verify, and what evidence proves completion.

## Workflow

### 1. Establish The Request Shape

Identify which mode the user wants:

- **Verify and plan**: external report or user diagnosis may be wrong; inspect before accepting.
- **Research and plan**: current product or competitors inform the design; cite or summarize only decision-relevant findings.
- **Split and delegate lightly**: create one to three independent work packages for non-multimodal agents to run manually.
- **Validate delivered work**: compare another agent's implementation against the original plan.

If the mode is ambiguous, infer from the prompt and proceed. Ask only when the next action would be materially risky.

### 2. Inspect Before Planning

Read the smallest useful slice of local context:

- existing docs, AGENTS/CLAUDE instructions, README files;
- target files or modules named by the user;
- prior plan documents if the user references them;
- recent related task-package folders and plan docs in the project planning location, even when the user does not reference them explicitly;
- current git status, so unrelated changes are not overwritten.

Before designing a new package, check whether the project already has a recent related package folder, INDEX, handoff doc, status note, or design note. Search the local planning home first, such as `docs/plans/`, `codex/agent_plans/`, or the repository's documented planning location. Recent materials often explain the original requirement, failed assumptions, accepted tradeoffs, and the real blocker. Reuse or amend that context instead of starting from a blank plan.

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

### Optional Orchestration-Ready Fields

When a lightweight package might later be escalated to full orchestration, add these fields below the basic template. Keep them simple; this skill does not generate a dispatcher, status ledger, Agent View package list, or worktree control plane.

```markdown
## Package ID
<unique-id>

## File Ownership
- <package-id> owns: <file-or-glob>
- Other packages must not edit these files without coordination.

## Allowed Paths
- <path-or-glob>

## Forbidden Paths
- <path-or-glob>

## Dependencies
- Depends on: <package-id> | none

## Parallel Safety
- safe | caution | unsafe
- Reason: <brief explanation of conflict risk>

## Expected Evidence Pack
- [ ] working directory recorded
- [ ] branch name recorded if changed
- [ ] git status clean (or explanation)
- [ ] git diff --stat captured
- [ ] changed files listed
- [ ] verification commands run
- [ ] test results summarized
- [ ] commit hash / PR link
- [ ] unresolved risks noted
- [ ] only allowed paths touched (verified)
```

These fields are machine-readable enough for a future orchestration pass, but still hand-editable by a human.

For small multi-window execution, create an INDEX document that ties packages together. Every INDEX must include the four authorization sections below so external agents know exactly what they can do without asking, when they must stop, how to finish, and what prompt the user should copy to start them.

````markdown
# [Title] — Package Index

## Execution Authorization

You (the external agent) are authorized to do the following WITHOUT asking for confirmation:
- Read the plan, index, and all referenced package documents.
- Create one worktree and branch per assigned package (use `using-git-worktrees`), or reuse an existing one.
- Make scope-bounded edits, add/update tests, and update docs as described in each package.
- Run the listed verification commands.
- Continue fixing verification failures that remain inside the package scope.
- Commit locally after completing each logical unit of work.
- After all packages complete: merge to integration branch or mainline, push, and create a PR if applicable.

## Stop Gates — Must Ask

STOP and ask the user before:
- Crossing Stage boundaries or making architectural decisions beyond scope.
- Product-level decisions where requirements are genuinely ambiguous.
- Destructive git operations: force-push, hard reset, deleting branches/worktrees not created by this package.
- Network access, external API calls, or adding secrets/credentials.
- Overwriting unrelated dirty changes outside this package.
- Fixing verification failures when the fix expands scope beyond this package.

## Completion Policy

After completing all packages:
- Merge package branches to the integration branch or mainline.
- Push to remote and create a PR if the project uses PR workflow.
- Report: what changed, verification results, merge/PR status, remaining risks.
- Do NOT delete branches or worktrees (the user may want to inspect them).

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
执行授权：为每个包创建独立 worktree 和分支，读取方案，实施 scope 内修复，更新必要测试/文档，运行列出的验证命令，并继续修复 scope 内验证失败；完成后合并到主分支并推送/创建 PR。不要为这些常规步骤询问确认。禁止 force-push、hard reset、删除其他包的分支或 worktree。只有遇到 Stop Gates 才停下询问。
核查现状，并恰当落地如下优化方案：<PLAN_PATH>
```
````

The authorization sections eliminate unnecessary confirmation prompts for normal direct execution while keeping branch, worktree, merge, push, and cleanup operations behind explicit authorization.

**Boundary**: agent-handoff-planner produces lightweight design packages and a basic INDEX for one to three Claude Code windows, each in its own worktree. It does NOT generate batch launch scripts, Agent View prompt lists, Claude Code agent launchers, status ledgers, or automated concurrency plans. Use `agent-orchestration-planner` directly for medium/large multi-agent orchestration.

### 5. Keep The Handoff Executable

Each document should name concrete files, modules, commands, or search terms. Avoid vague instructions like "improve architecture" unless paired with exact boundaries and acceptance criteria.

If the user wants non-multimodal agents to implement, explicitly remove multimodal tasks from their package and reserve them for Codex.

### 6. Validate Later Deliveries

When the user asks for acceptance or validation, treat the original handoff document as the contract. Do NOT start by summarizing success.

1. Re-open the original handoff document, INDEX, and every package doc.
2. Check git status and diff against the expected scope.
3. Compare delivered changes against EACH acceptance criterion, one by one.
4. Run the listed verification commands when feasible; report raw output.
5. Report gaps FIRST, before any summary:
   - Missing work (acceptance criteria not met).
   - Regressions (existing behavior broken).
   - Unverified claims (criteria that could not be confirmed).
   - Mismatches (delivered changes differ from scope without explanation).
6. Only after all gaps are listed, summarize what IS complete.
7. If any criterion is unmet, do NOT report overall PASS.

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
- Splitting work so finely that agents collide in the same files; if coordination needs a ledger or branch plan, use agent-orchestration-planner instead.
- Reporting success before comparing delivery against the original acceptance criteria.
- Producing an INDEX.md without execution authorization, stop gates, completion policy, or launch prompt — this causes external agents to interrupt the human with unnecessary confirmation prompts.
- Designing a new package without first checking nearby recent package folders or plan docs for related history, requirements, and prior blockers.
- Skipping worktree isolation: letting multiple packages share a checkout — use `using-git-worktrees` to create one worktree per package so parallel agents never collide on dirty state.
- Reporting validation success before listing every unmet acceptance criterion.
- Adding batch-launch scripts, Agent View prompts, status ledgers, or worktree/branch orchestration to INDEX — those belong to agent-orchestration-planner, not handoff-planner.
