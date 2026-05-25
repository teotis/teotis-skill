# Codex Skill Collection

A compact collection of Codex and Claude Code skills for engineering, research, learning, career preparation, reviewable deliverables, and repeatable handoff workflows.

[中文版本](README.zh-CN.md)

## Repository Model

This repository is the private workspace for personal skills, experiments, and
release preparation. Public release content lives in a separate nested Git
repository at `public/teotis-skills/`.

- Private skills live under `skills/<skill>/`.
- Shared agent guidance lives in `AGENTS.md`; `CLAUDE.md` and `GEMINI.md`
  are generated thin entry points.
- Private skills can include personal workflows, Chinese-facing notes, and
  unpublished behavior.
- Public skills are selected manually and may intentionally differ from their
  private counterparts.
- Skill bodies stay in English. The visible introduction and frontmatter
  description may use Chinese so invocation context is easier to recognize.
- The public repository provides both `README.md` and `README.zh-CN.md`.

## Skills

### `model-capability-cost-research` — Model Capability And Cost Research

Use when selecting AI models, vendors, or access routes for real workflows. It compares current model capability, pricing, cached-token behavior, multimodal support, coding-agent fit, and cost-performance trade-offs using fresh evidence and normalized assumptions.

Best for:

- Codex, Claude Code, Gemini CLI, OpenCode, or API backend choices;
- comparing GPT, Claude, Gemini, Qwen, DeepSeek, Kimi, Mimo, Qianfan, and similar models;
- token pricing, cached input pricing, output pricing, and reseller-package normalization;
- multimodal, Chinese UI/document, long-context, and large-repo coding-agent decisions.

### `android-career-interview-coach` — Android Career Interview Coach

Use when preparing for Android, mobile, camera-app, client-side, AI-app, or robotics Android interviews. It turns fundamentals and project experience into interview-ready explanations, 90-second answers, technical breakdowns, mock Q&A, and job-fit strategy.

Best for:

- Android/Kotlin/Java/C++/JNI/NDK/OS/performance interview prep;
- camera app, device adaptation, client architecture, and stability questions;
- Alibaba Qwen/Quark, Xiaomi-style camera, robotics Android, and AI-app client roles;
- resume-to-role matching, likely interview questions, and company targeting.

### `math-tutor` — Math Tutor

Use when learning mathematics, understanding formulas, proofs, theorems, calculus, linear algebra, probability, functions, operators, symmetry, or math screenshots. It combines low-barrier explanation, rigorous derivation, and optional Grothendieck-style structural insight.

Best for:

- "I don't understand" repair explanations;
- rigorous proofs and step-by-step derivations;
- formula or exercise explanations from text or screenshots;
- structural or essence-focused interpretations of mathematical ideas.

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
| Compare current AI models, prices, and agent backend fit | `model-capability-cost-research` |
| Prepare Android/mobile/camera interview answers and job strategy | `android-career-interview-coach` |
| Learn math concepts, proofs, formulas, or mathematical essence | `math-tutor` |
| Turn a request into agent-executable plans | `agent-handoff-planner` |
| Make a dense deliverable easier to review | `html-response` |
| Find a deeper structural simplification | `abstraction-architect` |
| Plan safe modernization in a legacy system | `renewal-architect` |

Each private skill lives in `skills/<skill>/` with a `SKILL.md` entry point.

## Guidance Sync

When shared repository rules change, edit `AGENTS.md` and run:

```bash
python3 control/project.py sync-agents
python3 control/project.py check
```

`make sync-agents` and `make check` provide the same shortcuts.
