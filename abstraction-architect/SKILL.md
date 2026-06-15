---
name: abstraction-architect
description: >
  Use for structural architecture analysis when complexity may come from missing invariants, duplicated domain representations, unstable boundaries, conversion glue, platform/configuration branching, or central orchestration bottlenecks.
  Grounds abstraction proposals in engineering evidence, counterexamples, migration seams, and falsifiable tests; produces paired Markdown and interactive HTML architecture reports.
  Trigger for architecture review, foundational redesign, domain unification, API/boundary redesign, platform/configuration generalization, repeated state/model representations, and non-incremental simplification opportunities.
  Do not use as the sole method for ordinary bug fixes, urgent incident recovery, small performance tuning, or delivery-risk-dominated debt prioritization.
---

# Structural Abstraction Architect

## Purpose

Analyze a software system for opportunities where a better structural model can eliminate entire families of special cases, adapters, branching logic, lifecycle inconsistencies, artificial boundaries, scattered process state, or user-facing workflow burden.

This skill is **inspired by structural and universal abstraction methods associated with Grothendieck**, but it is not a historical essay and does not imitate a personality. Mathematical metaphors are only useful when they yield verifiable engineering simplification.

The central advanced move is **process spatialization**: when complexity appears as time, sequence, status drift, retries, approvals, orchestration, or environment-dependent behavior, ask whether those dynamics should instead be represented by one canonical structural object whose documents, logs, UI states, ledgers, prompts, and reports are consistent projections.

The deliverable is a paired report set: a **Markdown source report** for efficient agent handoff and an **interactive HTML architecture report** for user review, comparison, and feedback. By default, this skill performs analysis only. It MUST NOT modify production code, tests, configuration, migrations, or infrastructure unless the user separately gives explicit authorization after reviewing a transition plan.

---

## Positioning: When to Use This Skill

### Strong fit

Use this skill when the system exhibits one or more of these structural signals:

- Many representations of what appears to be the same domain concept.
- Repeated adapters, conversions, schema mappers, mode switches, or platform branches.
- Boundaries that generate more glue than isolation value.
- A central orchestrator or God object coordinating logic that ought to compose locally.
- Workflow, orchestration, CI, approval, retry, or lifecycle state scattered across ledgers, logs, generated docs, dashboards, prompts, reports, or manual checklists.
- API pain revealed by many callers compensating for a provider's design.
- Similar workflows implemented separately across products, tenants, protocols, environments, or lifecycle stages.
- User workflows that require many commands, modes, handoffs, confirmations, training rules, or recovery loops because the system exposes controls rather than a task-level interaction model.
- A request for architecture review, domain unification, foundational refactoring, or non-incremental simplification.

### Weak fit or wrong first tool

Do not force this lens onto work whose primary constraint is operational urgency or implementation sequencing, such as:

- A production incident requiring immediate mitigation.
- A contained bug fix or localized performance bottleneck.
- A migration whose structural target is already known and whose remaining problem is rollout safety.
- Technical debt prioritization where ROI, blast radius, ownership, or delivery constraints dominate.

For these, use or hand off to **Pragmatic Renewal Architect**. The two skills are complements: this skill discovers higher-leverage structures; the pragmatic skill determines safe adoption paths.

---

## Invocation and Modes

When invoked:

1. Determine the target repository or directory if it is not already available.
2. Identify whether the request requires structural analysis, transition planning, or both.
3. Inspect the project only as deeply as evidence permits; clearly mark unavailable telemetry, history, runtime behavior, or business context.
4. Apply the Structural Abstraction method below.
5. Produce the report and optionally open it in a browser when the environment supports doing so.

### Operating modes

| Mode | Default trigger | Deliverable | Modification permission |
|---|---|---|---|
| Structural Scan | Broad architecture review, incomplete evidence | Candidate map and missing-evidence list | No code changes |
| Full Architecture Analysis | Repository available and structural issues evidenced | Markdown source report + interactive HTML report | No code changes |
| Transition Handoff | User accepts one or more structural directions | Migration hypotheses for pragmatic evaluation | No code changes |
| Authorized Implementation | User explicitly approves implementation after reviewing a plan | Scoped code changes with verification | Only within explicit authorization |

Never silently jump from analysis to implementation.

---

## Core Workflow

1. Establish the target repository, requested mode, and evidence limits.
2. Inspect enough code, docs, tests, runtime paths, and user-supplied context to build an evidence ledger.
3. Use the detailed structural method in `references/method_and_report_spec.md` when evaluating candidates, especially for process spatialization, admissibility, candidate competition, and report requirements.
4. Produce paired reports: first write `structural_abstraction_architect_report_{YYYYMMDD}_{HHMM}.md` as the agent-readable source of truth, then derive `structural_abstraction_architect_report_{YYYYMMDD}_{HHMM}.html` from the same evidence ledger, proposal IDs, and conclusions as the user-facing interactive review surface. Use `reviewable-html-report/references/report_base.md` for shared report mechanics instead of reimplementing HTML infrastructure. If that reference is unavailable, degrade to a self-contained static HTML report that preserves the core conclusion, TOC, stable section IDs, evidence appendix, and Mermaid source fallback.
5. If the user wants implementation after the report, switch only after explicit authorization and keep changes inside the accepted transition boundary.

## Report Delivery Contract

- **Markdown is the source report:** include the executive summary, evidence ledger, pressure map, candidate/proposal IDs, admissibility results, rejected/deferred abstractions, transition handoff, unknowns, and verification notes in a compact structure that another agent can reuse.
- **HTML is the interaction layer:** do not introduce conclusions absent from Markdown; use it for topology/process visuals, proposal cards, filters, expandable evidence, review/export controls, and user feedback.
- **Consistent naming:** formal reports use the same timestamp basename and deliver both `.md` and `.html`. If HTML cannot be generated or opened, still deliver Markdown and state the limitation.
- **Final response:** list both report paths, state whether HTML opened, summarize the highest-leverage structural opportunity in one sentence, and state that no code was modified.

## Resource Map

- `references/method_and_report_spec.md` — full structural method, admissibility gate, evidence rhythm, Markdown/HTML report schema, anti-goals, and execution flow.
- `references/discovery_patterns.md` — discovery prompts for unclear pressure maps or weak candidates.
- `../reviewable-html-report/references/report_base.md` — shared HTML report mechanics when an interactive report is required; if unavailable, use the static HTML fallback and do not block report delivery.

## Completion Standard

- Separate observed evidence, inference, and unknowns.
- Classify each proposal through the admissibility gate.
- Include rejected or deferred abstractions when relevant.
- Keep the Markdown source report and HTML interaction report aligned on the same evidence ledger, proposal IDs, and conclusions.
- Do not modify production code, tests, configuration, migrations, or infrastructure unless the user explicitly authorizes implementation after reviewing a transition plan.
