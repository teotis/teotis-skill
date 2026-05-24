# Codex Skill Collection

A compact collection of Codex and Claude Code skills for engineering workflows that need structured judgment, reviewable deliverables, and repeatable handoff patterns.

[中文版本](README.zh-CN.md)

## Skills

### `agent-handoff-planner` — Agent Handoff Planning

Use when a broad request needs to become executable work for one or more agents. It verifies external-agent findings before accepting them, separates high-context or multimodal work that Codex should retain from work that can be delegated, and produces Markdown implementation packages with scope, steps, acceptance criteria, and verification commands.

Best for:

- external agent review verification;
- Markdown handoff documents for non-multimodal agents;
- parallel implementation planning;
- final acceptance against the original plan.

### `html-response` — Adaptive HTML Response

Use when an answer, report, plan, artifact, or review would be easier to inspect in a browser than in plain chat. It selects the lightest useful HTML presentation mode, keeps simple answers in chat, and creates interactive review surfaces for dense analysis, comparisons, technical reviews, document/image previews, and structured feedback.

Best for:

- long-form reports and technical reviews;
- decision boards and action plans;
- artifact review for PDFs, documents, images, or rendered Markdown;
- feedback collection with stable review item IDs.

### `abstraction-architect` — Structural Abstraction Architect

Use for architecture analysis when complexity appears to come from missing invariants, duplicated domain representations, unstable boundaries, repeated adapters, platform branching, or orchestration bottlenecks. It looks for structural simplifications that can delete whole families of special cases, while requiring concrete code evidence, counterexamples, transition seams, and disproof tests.

Best for:

- foundational architecture review;
- domain model or API boundary redesign;
- identifying non-incremental simplification opportunities;
- deciding whether a proposed abstraction is valid or premature.

### `renewal-architect` — Pragmatic Renewal Architect

Use for legacy renewal and practical modernization under delivery, stability, organizational, and migration constraints. It focuses on measurable capability gains, dominant bottlenecks, rollback-safe pilots, coexistence strategies, and paths that can scale from a controlled experiment to broader engineering renewal.

Best for:

- technical debt governance;
- migration planning without stopping delivery;
- monolith decomposition or strangler/ACL boundary design;
- finding the most feasible first improvement in a complex system.

## Skill Map

| Need | Start With |
|---|---|
| Turn a request into agent-executable plans | `agent-handoff-planner` |
| Make a dense deliverable easier to review | `html-response` |
| Find a deeper structural simplification | `abstraction-architect` |
| Plan safe modernization in a legacy system | `renewal-architect` |

Each skill lives in its own directory with a `SKILL.md` entry point.
