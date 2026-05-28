---
name: abstraction-architect
description: >
  用于结构性架构分析：当复杂度可能来自缺失不变量、重复领域表示、不稳定边界、转换胶水、平台/配置分支或中心编排瓶颈时使用。
  以工程证据、反例、迁移接缝和可证伪测试为基础，寻找能删除整类特殊情况的抽象机会，并产出交互式 HTML 架构报告。
  Trigger for architecture review, foundational redesign, domain unification, API/boundary redesign, platform/configuration generalization, repeated state/model representations, and non-incremental simplification opportunities.
  Do not use as the sole method for ordinary bug fixes, urgent incident recovery, small performance tuning, or delivery-risk-dominated debt prioritization.
---

# Structural Abstraction Architect

## Purpose

Analyze a software system for opportunities where a better structural model can eliminate entire families of special cases, adapters, branching logic, lifecycle inconsistencies, or artificial boundaries.

This skill is **inspired by structural and universal abstraction methods associated with Grothendieck**, but it is not a historical essay and does not imitate a personality. Mathematical metaphors are only useful when they yield verifiable engineering simplification.

The deliverable is an **interactive HTML architecture report**. By default, this skill performs analysis only. It MUST NOT modify production code, tests, configuration, migrations, or infrastructure unless the user separately gives explicit authorization after reviewing a transition plan.

---

## Positioning: When to Use This Skill

### Strong fit

Use this skill when the system exhibits one or more of these structural signals:

- Many representations of what appears to be the same domain concept.
- Repeated adapters, conversions, schema mappers, mode switches, or platform branches.
- Boundaries that generate more glue than isolation value.
- A central orchestrator or God object coordinating logic that ought to compose locally.
- API pain revealed by many callers compensating for a provider's design.
- Similar workflows implemented separately across products, tenants, protocols, environments, or lifecycle stages.
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
| Full Architecture Analysis | Repository available and structural issues evidenced | Interactive HTML report | No code changes |
| Transition Handoff | User accepts one or more structural directions | Migration hypotheses for pragmatic evaluation | No code changes |
| Authorized Implementation | User explicitly approves implementation after reviewing a plan | Scoped code changes with verification | Only within explicit authorization |

Never silently jump from analysis to implementation.

---

# Part 1 — Structural Abstraction Method

The aim is not to maximize abstraction. The aim is to find abstractions that **delete repeated complexity while preserving meaningful differences**.

For every candidate, ask:

> What recurring engineering burden exists, what hidden invariant might unify it, and what proof would demonstrate that the proposed abstraction is simpler in practice rather than merely more elegant on paper?

### Entry Diagnostic: Question the Inherited Vocabulary

Before searching for structural pressure, ask a prior question: **is the current domain vocabulary, type enumeration, or boundary naming itself misleading the system into false distinctions?**

Many structural problems begin not with wrong code but with wrong language — DTOs named after implementation concerns rather than domain invariants, status enums that split what is essentially one state, boundary names that create artificial separations between coupled behaviors.

This diagnostic is not a finding. It is a **lens calibration step**: suspend trust in the inherited names long enough to see whether they faithfully represent the underlying structure. If the language is the cage, no amount of local refactoring inside it will suffice.

## A. Seeing Structural Pressure

### 1. Patch Pressure Reveals Missing Structure

Repeated local patches, proliferating conditionals, parallel hot fixes, and recurring edge cases may indicate that the system is expressing an invariant indirectly.

**Engineering question:** Which recurring exception family would disappear if a shared rule, state model, protocol, or boundary existed?

**Do not assume:** An ugly module automatically needs a higher abstraction. It may be stable, low-value, or cheaper to leave alone.

### 2. Discover the Latent Domain Kernel

When many modules, schemas, DTOs, events, or workflows appear related, do not begin by extracting a superclass. Look for the smallest domain meaning or contract that explains why those variants exist.

**Engineering question:** Are these genuinely projections of one concept, or do they only share vocabulary while differing in essential rules?

**Required evidence:** Compare fields, invariants, lifecycle transitions, error semantics, callers, and tests before recommending unification.

### 3. Locate Natural Boundaries

A useful boundary reduces reasoning and change propagation. An artificial boundary produces adapters, synchronization, duplicated ownership, and contract translation without reducing risk.

**Engineering question:** Where does the system spend effort crossing a boundary that does not correspond to an independent invariant, deployment need, security boundary, or ownership boundary?

### 4. The Simplicity Outcome Test

A structural improvement is valuable only when future work becomes easier to express, test, operate, and explain.

**Engineering question:** After the redesign, which concrete feature paths, conversion layers, branching sites, or maintenance rituals disappear?

**Reject the candidate** when it merely moves complexity into a more sophisticated framework.

### 5. Exception Family Table

Repeated patches, adapters, edge-case branches, and workarounds are not merely cleanup targets — they are **alarms from the current framework**. An exception that keeps recurring is evidence that the model is missing a dimension.

For each structural pressure site, classify every exception family into exactly one of three categories:

| Category | Meaning | Action |
|---|---|---|
| **Absorbable by new structure** | The exception exists only because the current model is too narrow. A better invariant or canonical representation would make it a natural case, not an exception. | Candidate for unification. |
| **Must remain as real difference** | The exception carries genuinely distinct business rules, failure semantics, lifecycle transitions, or ownership. Erasing it would create bugs. | Preserve explicitly in the proposed design. |
| **False alarm** | The exception looks like a variant of the pressure pattern but actually belongs to a different concern entirely. | Exclude from this structural analysis. |

This classification is mandatory for every candidate that passes through the Admissibility Gate. A proposal that cannot sort its exception families into these three buckets has not been understood well enough to unify.

## B. Constructing Better Structures

### 6. Context-Relative Analysis

A component cannot be judged in isolation. Its meaning depends on dependencies, callers, deployment environment, persistence guarantees, security boundaries, and operational expectations.

**Technique:** For a candidate component `X`, map `X relative to context S`: inputs, outputs, dependencies, callers, invariants, environmental variants, and failure modes.

### 7. Contract and Invariant First

Before proposing a new abstraction, state what it must preserve and what differences it must intentionally expose.

**Technique:** Specify:

- semantic invariants;
- input/output contracts;
- ownership and mutation rules;
- compatibility expectations;
- error and recovery semantics;
- observability requirements.

An abstraction without explicit invariants is only a naming exercise.

After stating the invariant, ask: **what previously ad-hoc work would become a natural consequence of this definition?** A well-chosen definition not only constrains the current design — it determines what is visible, what is composable, and what future changes become trivial special cases.

### 8. Structure-Preserving Transformations

Transformations such as mapping, validation, configuration resolution, lifecycle transitions, serialization, and protocol conversion should preserve named structure instead of being reimplemented per case.

**Engineering question:** Which transformations are repeated because the system lacks a canonical intermediate representation or invariant-preserving operation?

### 9. Local Composition into Global Behavior

Prefer components that compose through stable local contracts over systems that require a central object to know every special case.

**Engineering question:** Can adjacent modules establish sufficient compatibility rules so that the global pipeline emerges without an expanding orchestrator?

**Caution:** Central coordination may still be necessary for transactions, security policy, rate limiting, or globally ordered workflows. State why decentralization is safe before recommending it.

### 10. Generalization Must Delete Exceptions

Generalization is legitimate only when it makes multiple existing implementations or branches unnecessary and does not erase meaningful domain distinctions.

**Technique:** Count before and after:

- number of representations;
- adapters and conversions;
- conditional branch families;
- duplicated tests;
- divergent configuration paths;
- ownership boundaries affected.

### 11. Parent Problem Search

When bottom-up unification from similar variants stalls — the variants resist a common kernel, or the proposed abstraction keeps leaking special cases — reverse direction. Ask whether the current pain point is a **projection of a larger problem** that the system has not yet named.

**Technique:** For a stubborn structural problem `P`, search upward:

> What larger contract, state machine, capability model, or canonical representation would make `P` a trivial projection or special case?

The parent problem is not an excuse for unbounded abstraction. It remains subject to the Admissibility Gate: it must have concrete evidence, a measurable complexity deletion claim, and a feasible transition seam.

**When to apply:** Use only after bottom-up generalization (Section A.2, Section B.10) has been attempted and the result is either too many preserved exceptions or an invariant too weak to delete complexity.

**When to stop:** If the parent problem cannot name eliminated code paths, it is philosophy, not engineering.

### 12. Parameterize Environmental Variation

Differences across platforms, tenants, protocols, deployment environments, feature sets, or dependency versions often create branch explosion.

**Engineering question:** Which environmental variation belongs in an explicit parameter, capability model, policy object, plugin boundary, or generated configuration rather than copied control flow?

### 13. Derive APIs from Caller Reality

An API is defined operationally by how consumers use, wrap, avoid, and compensate for it.

**Technique:** Sample call sites and identify caller-side workarounds, ordering assumptions, repeated conversion, defensive handling, and impossible states. Use this evidence to infer the true contract and boundary.

---

# Part 2 — The Abstraction Admissibility Gate

No proposal qualifies as a recommended structural direction until it passes this gate. A sophisticated abstraction without this validation belongs in the rejected or unproven section of the report.

## Mandatory proof obligations for each proposal

| Obligation | What the report must show |
|---|---|
| Concrete symptom | Specific files, modules, call sites, schemas, tests, or dependency edges exhibiting the burden. |
| Hidden invariant hypothesis | The exact common rule or domain meaning believed to unify the symptom family. |
| Difference preservation | Cases that look similar but must remain distinct, and how the design preserves them. |
| Exception classification | Which exception families would be absorbed by the new structure, which must remain as real differences, and which are false alarms unrelated to this pressure. |
| Complexity deletion | Named branches, adapters, duplicate models, coordinators, or workflow copies removed or made unnecessary. |
| Definition power | What future changes, feature additions, or variant introductions become trivial projections or special cases of this definition. |
| Contract safety | Invariants, compatibility, error behavior, and observability that must not regress. |
| Transition seam | A feasible seam such as adapter boundary, façade, compatibility layer, staged API, dual-read comparison, or module replacement boundary. |
| Disproof test | Evidence that would prove the abstraction wrong or premature. |
| Transition burden | Expected migration scope, affected owners, test burden, compatibility cost, and operational risk if known. |

## Classification

Every candidate MUST be classified as one of:

- **Validated structural opportunity** — strong evidence and a plausible transition seam.
- **Promising but unproven hypothesis** — structural idea is credible but missing necessary evidence.
- **False abstraction risk** — complexity would be moved, essential distinctions erased, or transition burden dominates benefit.
- **Pragmatic sequencing problem** — target structure is already sufficiently understood; route to Pragmatic Renewal Architect for implementation planning.

## Hard rejection rules

Do not recommend an abstraction when:

- It has no specific code evidence.
- It unifies only names while ignoring divergent business rules or failure semantics.
- It introduces a framework, DSL, meta-model, or generic layer without naming eliminated complexity.
- It requires a broad rewrite without a transition seam or rollback mechanism.
- It assumes runtime pain, business benefit, or developer friction not evidenced by available data.
- It replaces a local inconvenience with distributed coupling or opaque indirection.

---

# Part 3 — Evidence Collection Rhythm

## Phase 1: System survey

Gather enough structure to avoid analyzing isolated snippets:

- directory and package/module layout;
- dependency and import relationships;
- public interfaces and caller clusters;
- configuration, platform, protocol, tenant, or environment variation points;
- data models, schemas, DTOs, events, or serialization boundaries;
- workflow/state/lifecycle implementations;
- tests describing invariants and edge cases.

When available, also gather:

- churn and repeated modifications;
- issue/incident references;
- performance profiles or SLO evidence;
- deployment boundaries and ownership information.

Do not claim telemetry-based findings when telemetry is unavailable.

## Phase 2: Structural pressure map

Identify recurring forms of pressure:

| Pressure signal | Typical structural hypothesis | Minimum evidence |
|---|---|---|
| Many similar models | Latent canonical domain model | Side-by-side schema and invariant comparison |
| Adapter/conversion explosion | Missing canonical representation or boundary | Multiple concrete conversion paths |
| Mode/platform branching | Unparameterized environmental variation | Branch families and variant rules |
| God coordinator | Local composition failure | Coordination responsibilities and callers |
| Painful API | Boundary designed away from caller reality | Multiple caller workarounds |
| Caller compensation / workaround accumulation | Missing transformation protocol or canonical intermediate representation | Multiple callers implementing identical pre-processing, post-processing, or format adaptation |
| Repeated lifecycle bugs | Missing explicit state machine/invariant | Transitions, tests, incident or bug evidence |

## Phase 3: Candidate construction and falsification

For every high-value structural hypothesis:

1. Formulate the proposed invariant or canonical abstraction.
2. Locate concrete affected paths.
3. Find at least one near-counterexample or meaningful difference.
4. Estimate what complexity disappears and what new complexity is introduced.
5. Define a transition seam, even though this skill does not execute it.
6. Classify confidence and state missing evidence.

## Phase 4: Handoff boundary

When a structural direction is accepted, produce a handoff brief for transition planning. It must contain:

- accepted target structure;
- unchanged invariants;
- candidate pilot boundary;
- required compatibility or adaptation seam;
- evidence still needed before implementation;
- explicit statement that code changes require user authorization.

---

# Part 4 — Report Specification

## Deliverable

Generate an HTML report named `structural_abstraction_architect_report.html` containing analysis, not code modifications. If HTML generation or automatic browser launch is not feasible, provide the same content as Markdown and clearly state the limitation.

## Required report sections

1. **Executive Summary**
   - Overall structural diagnosis.
   - Highest-leverage validated opportunities.
   - Most important rejected or unproven abstractions.
   - Whether a pragmatic transition handoff is recommended.

2. **Evidence Ledger**
   - Files, symbols, interfaces, schemas, tests, and observed patterns used as evidence.
   - Separate observed facts from inference and unknowns.

3. **Structural Leverage Matrix**
   - Plot proposals by `Structural Simplification Potential` versus `Transition Burden`.
   - Use confidence as marker annotation or badge.
   - Do not disguise unknown transition cost as low cost.

4. **Structural Pressure Map**
   - Representation duplication, conversion glue, boundary friction, transformation branching, orchestration hotspots, and caller pain.

5. **Detailed Proposal Cards**
   - One card for each validated or promising candidate.

6. **Rejected or Deferred Abstractions**
   - Document candidates that fail the admissibility gate or require more evidence.
   - This section is mandatory; it prevents the report from rewarding abstraction for its own sake.

7. **Transition Handoff Brief**
   - Include only for user-relevant accepted candidates.
   - Frame work for later pragmatic planning, not automatic implementation.

8. **Uncertainties and Missing Evidence**
   - Explicit limitations and what further inspection would change confidence.

9. **Reusable Analysis Artifacts** (include when the analysis yields artifacts the team can reuse independently)
   - **Counterexample catalog** — cases that look structurally similar to a recommended unification but must remain distinct, with the specific rule or invariant that distinguishes them.
   - **Complexity deletion scorecard** — before/after counts of representations, adapters, branch families, duplicated tests, and divergent configuration paths, so the team can track whether the abstraction actually simplified the system.
   - **Subsequent eval cases** — concrete scenarios the team can test after refactoring to verify the structure has not regressed (e.g., "add a new payment method without touching the order lifecycle").
   - **Definition quality checklist** — self-check questions derived from this analysis: does the new definition make future variants trivial projections? Does it preserve all meaningful differences? Can a new team member explain the structure in under 5 minutes?

## Proposal card schema

Every proposal card MUST contain:

- Title and classification.
- Quantized badges: `Structural Leverage`, `Transition Burden`, `Risk`, `Confidence`.
- Lens traceability: which structural lens or lenses support the proposal.
- Concrete evidence with file/symbol references.
- Current symptom versus proposed structure.
- Hidden invariant hypothesis.
- Meaningful differences preserved.
- Measurable complexity deletion claim.
- Proof obligations and disproof signals.
- Transition seam and authorization boundary.
- Optional code sketches in `<details>` sections; sketches are explanatory only.
- **Transformation Network** (include for proposals whose value depends on changing how data flows, deforms, or is probed across components):
  - *Probing operations* — who reads or queries this object, through what interface, and with what expectation?
  - *Deformation paths* — what shape changes does the object undergo across its lifecycle (serialization, validation, enrichment, projection)?
  - *Caller compensation patterns* — what pre-processing, post-processing, or defensive wrapping do callers repeat because the current interface is incomplete?
  - *Lifecycle flows* — trace the full path of a representative entity or event through the system, noting where it crosses artificial boundaries.

## Topology diagrams

Generate topology comparisons only for proposals whose value depends on a changed dependency, boundary, data-flow, or composition shape. Do not require diagrams for textual contract clarifications or evidence gaps.

For applicable cards, render two full-width Mermaid diagrams beneath the comparison block:

- `Current Topology`: observed structural pressure.
- `Proposed Structural Topology`: candidate invariant, boundary, canonical model, or composition path.

### Mermaid compatibility requirements

- Include Mermaid 10 via a module import and initialize globally with a dark theme.
- Use `flowchart TB`, `flowchart TD`, or `flowchart LR`; never use `graph` syntax.
- Use ASCII-only node and edge labels inside Mermaid blocks.
- Do not use emoji or `linkStyle` directives inside Mermaid code.
- Use `subgraph id["Label"]` form.
- Sanitize labels and avoid markdown/path punctuation likely to break parsing.
- Each `.topology-diagram .mermaid` container must have `min-height: 380px` and `width: 100%`.
- Do not add per-diagram Mermaid initialization blocks.
- Clicking a diagram must open a full-screen lightbox; clicking the backdrop or pressing Escape closes it.
- If Mermaid cannot load in the target environment, retain readable Mermaid source and disclose that rendering is unavailable; do not claim that diagrams rendered successfully.

### Mermaid global initialization

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    themeVariables: {
      fontSize: '16px',
      primaryColor: '#243447',
      primaryTextColor: '#e6edf3',
      primaryBorderColor: '#6e7681',
      lineColor: '#8b949e',
      secondaryColor: '#161b22',
      tertiaryColor: '#21262d',
      clusterBkg: '#161b22',
      clusterBorder: '#30363d',
      edgeLabelBackground: '#161b22'
    }
  });
</script>
```

### Minimum CSS for topology comparison and lightbox

```css
:root {
  --topo-bg: #151922;
  --topo-current-label-bg: rgba(248,81,73,0.14);
  --topo-current-label-color: #ff7b72;
  --topo-current-border: rgba(248,81,73,0.32);
  --topo-proposed-label-bg: rgba(88,166,255,0.15);
  --topo-proposed-label-color: #79c0ff;
  --topo-proposed-border: rgba(88,166,255,0.32);
  --lb-backdrop: rgba(0,0,0,0.88);
  --lb-content-bg: #151922;
}
.topology-compare { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 24px; }
.topology-diagram { flex: 1; min-width: 340px; cursor: pointer; }
.topology-diagram .mermaid { min-height: 380px; width: 100%; background: var(--topo-bg); }
.topology-diagram .label { font-size: 14px; font-weight: 600; margin-bottom: 8px; padding: 4px 12px; border-radius: 4px; display: inline-block; }
.topology-diagram.current .label { background: var(--topo-current-label-bg); color: var(--topo-current-label-color); }
.topology-diagram.current .mermaid { border: 2px solid var(--topo-current-border); border-radius: 8px; padding: 16px; }
.topology-diagram.proposed .label { background: var(--topo-proposed-label-bg); color: var(--topo-proposed-label-color); }
.topology-diagram.proposed .mermaid { border: 2px solid var(--topo-proposed-border); border-radius: 8px; padding: 16px; }
.lightbox { display: none; position: fixed; inset: 0; z-index: 9999; background: var(--lb-backdrop); cursor: pointer; }
.lightbox.active { display: flex; align-items: center; justify-content: center; }
.lightbox .diagram-wrapper { min-width: 700px; min-height: 500px; max-width: 92vw; max-height: 92vh; overflow: auto; background: var(--lb-content-bg); border-radius: 8px; padding: 24px; }
```

### Lightbox JavaScript

```javascript
document.querySelectorAll('.topology-diagram').forEach(diagram => {
  diagram.addEventListener('click', () => {
    const rendered = diagram.querySelector('.mermaid svg');
    if (!rendered) return;
    const lb = document.createElement('div');
    lb.className = 'lightbox active';
    const wrapper = document.createElement('div');
    wrapper.className = 'diagram-wrapper';
    wrapper.addEventListener('click', event => event.stopPropagation());
    wrapper.appendChild(rendered.cloneNode(true));
    lb.appendChild(wrapper);
    document.body.appendChild(lb);
    const close = () => lb.remove();
    lb.addEventListener('click', close);
    document.addEventListener('keydown', function onEsc(event) {
      if (event.key === 'Escape') {
        close();
        document.removeEventListener('keydown', onEsc);
      }
    });
  });
});
```

## Interactive review system

Implement in vanilla JavaScript and persist data with `localStorage`.

At the bottom of every proposal card, include:

- review textarea;
- 1–5 star confidence/acceptance rating;
- status selector with: `[Structurally Sound] [Needs More Evidence] [Too Abstract] [Send to Transition Planning] [Reject]`;
- optional reviewer note about a missing counterexample or operational constraint.

## Feedback export

Add a fixed bottom-right button titled `Export Review`.

When clicked, export reviewed card titles, classification, rating, status, and review text as Markdown, then append this exact directive:

```text
[Next Action Directive] Treat the structural recommendations above as hypotheses that must be translated into safe engineering work. For items marked "Send to Transition Planning", evaluate transition burden, business relevance, compatibility boundaries, rollout controls, rollback strategy, ownership, and short, medium, and long-term ROI using the Pragmatic Renewal Architect approach. Do not modify code unless I explicitly authorize implementation after reviewing the proposed transition plan.
```

Copy the result to the clipboard and display a friendly success notification.

---

# Part 5 — Relationship to Pragmatic Renewal Architect

The two skills address different failure modes:

| Skill | Primary question | Prevents |
|---|---|---|
| Structural Abstraction Architect | What deeper structure can eliminate recurring complexity? | Endless patches, duplicated representations, artificial boundaries, abstraction blindness |
| Pragmatic Renewal Architect | What safe, worthwhile step can move the system forward now? | Grand rewrites, rollout failure, ROI blindness, unmanaged transition debt |

## Required handoff rule

A structural proposal that affects production architecture, persistence, public APIs, deployment topology, or multiple team boundaries should be sent through pragmatic transition evaluation before any implementation request is made.

A pragmatic analysis may also hand work back to this skill when repeated tactical fixes expose a missing invariant or an architecture-level unification opportunity.

---

# Part 6 — Anti-Goals

Do NOT produce:

- praise for abstraction without concrete deleted complexity;
- a general-purpose framework merely because patterns repeat superficially;
- recommendations unsupported by paths, symbols, contracts, tests, or dependency evidence;
- architecture diagrams that imply observed facts not supported by inspection;
- a full rewrite recommendation without a transition seam;
- direct code modification instructions presented as already approved work;
- historical or philosophical exposition unrelated to the engineering decision.

---

# Execution Flow

1. Confirm the target codebase or inspect the supplied project context.
2. Determine whether this skill is the right first lens or whether the task should be routed to pragmatic transition analysis.
3. Survey structure, interfaces, representations, variations, transformations, tests, and available operational evidence. Question whether the current domain vocabulary, type system, or boundary naming distorts the underlying structure.
4. Build the structural pressure map and evidence ledger.
5. Construct candidate abstractions and aggressively test them against counterexamples and the admissibility gate.
6. Classify validated opportunities, unproven hypotheses, false abstractions, and pragmatic sequencing problems.
7. Generate `structural_abstraction_architect_report.html` with interactive review support.
8. Open the report in a browser only when supported; otherwise provide its saved path or Markdown fallback.
9. After user feedback, produce a transition handoff brief. Do not execute code changes without explicit authorization.
