# abstraction-architect Detailed Method and Report Specification

# Part 1 — Structural Abstraction Method

The aim is not to maximize abstraction. The aim is to find abstractions that **delete repeated complexity while preserving meaningful differences**.

For open-ended architecture reviews, unclear pressure maps, or candidates that feel obvious but weak, read `references/discovery_patterns.md` before recommending a structural direction. Use it as a discovery aid, not as report filler.

For every candidate, ask:

> What recurring engineering burden exists, what hidden invariant might unify it, and what proof would demonstrate that the proposed abstraction is simpler in practice rather than merely more elegant on paper?

For candidates whose pain appears as a process rather than a thing, add:

> What static structural object would make the valid dynamic paths, local statuses, approvals, retries, reports, and environment variants natural projections or local sections of the same system?

### Entry Diagnostic: Question the Inherited Vocabulary

Before searching for structural pressure, ask a prior question: **is the current domain vocabulary, type enumeration, process vocabulary, or boundary naming itself misleading the system into false distinctions?**

Many structural problems begin not with wrong code but with wrong language — DTOs named after implementation concerns rather than domain invariants, status enums that split what is essentially one state, workflow stages named after tools rather than capabilities, boundary names that create artificial separations between coupled behaviors.

This diagnostic is not a finding. It is a **lens calibration step**: suspend trust in the inherited names long enough to see whether they faithfully represent the underlying structure. If the language is the cage, no amount of local refactoring inside it will suffice.

The Constraint Reality Filter (Part 3, Phase 1.5) is the parallel calibration for constraints: separating real contractual constraints from inertial ones. Together, these two steps ensure the analysis neither inherits false distinctions from vocabulary nor preserves false constraints from habit.

### Discovery Passes Before Commitment

Before committing to a high-leverage abstraction, probe the system from multiple directions:

- **Data lifecycle** — how one entity or event changes across storage, API, jobs, UI, reports, and tests.
- **Caller reality** — how consumers wrap, compensate for, or avoid the current API or boundary.
- **Failure and recovery** — what retries, incidents, repair scripts, manual steps, and status mismatches reveal.
- **Environmental variation** — how tenants, platforms, protocols, runners, permissions, and deployments deform the same behavior.

These passes are a candidate generator. They prevent the analysis from mistaking the first repeated code shape for the real invariant.

### Candidate Competition

For high-value pressure sites, generate at least two plausible structural explanations before recommending one. Compare them by evidence fit, complexity deletion, meaningful differences preserved, deformation power, transition seam, and disproof signal.

If candidates explain different burdens, report them separately. If one candidate is weaker, say why it is rejected, deferred, or scoped down. Do not present one elegant abstraction as inevitable merely because it is available.

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

### 6. Spatialize Dynamic Processes

When the pressure appears as a timeline, state machine, retry loop, approval chain, orchestration graph, queue, workflow, or environment-specific run path, do not start by merely splitting the orchestrator. First ask whether the system lacks a **canonical process object**.

Map the dynamic pressure into five structural pieces:

- **Base** — the context over which behavior varies: environment, tenant, platform, runner, permission mode, branch, capability class, release gate, user role, or operational policy.
- **Fibers / local instances** — the package, job, request, task, approval, session, screen flow, or lifecycle instance that lives over a particular base context.
- **Projections** — every artifact that shows or mutates part of the process: database rows, YAML, TSV, event logs, status Markdown, dashboards, CLI output, prompts, reports, checklists, alerts, or UI states.
- **Gluing conditions** — the exact local consistency rules that allow local evidence to compose into global completion, rollout, release, or user-visible state.
- **Deformations** — changes that should be cheap if the definition is right: adding a new status, runner, manual gate, failure class, package type, tenant, environment, verification mode, or reporting view.

**Engineering question:** Which observed dynamic paths would become ordinary projections of one structural object, and which artifacts would stop drifting because they are generated from or checked against the same definition?

**Caution:** Do not recommend a grand meta-model merely because a process is complicated. The proposal must name the projections it unifies, the drift it prevents, the local-to-global rule it enforces, and the concrete future deformation it makes cheaper.

### 7. Context-Relative Analysis

A component cannot be judged in isolation. Its meaning depends on dependencies, callers, deployment environment, persistence guarantees, security boundaries, and operational expectations.

**Technique:** For a candidate component `X`, map `X relative to context S`: inputs, outputs, dependencies, callers, invariants, environmental variants, and failure modes.

### 8. Contract and Invariant First

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

### 9. Structure-Preserving Transformations

Transformations such as mapping, validation, configuration resolution, lifecycle transitions, serialization, and protocol conversion should preserve named structure instead of being reimplemented per case.

**Engineering question:** Which transformations are repeated because the system lacks a canonical intermediate representation or invariant-preserving operation?

### 10. Local Composition into Global Behavior

Prefer components that compose through stable local contracts over systems that require a central object to know every special case.

**Engineering question:** Can adjacent modules establish sufficient compatibility rules so that the global pipeline emerges without an expanding orchestrator?

**Caution:** Central coordination may still be necessary for transactions, security policy, rate limiting, or globally ordered workflows. State why decentralization is safe before recommending it.

### 11. Generalization Must Delete Exceptions

Generalization is legitimate only when it makes multiple existing implementations or branches unnecessary and does not erase meaningful domain distinctions.

**Technique:** Count before and after:

- number of representations;
- adapters and conversions;
- conditional branch families;
- duplicated tests;
- divergent configuration paths;
- ownership boundaries affected.

### 12. Parent Problem Search

When bottom-up unification from similar variants stalls — the variants resist a common kernel, or the proposed abstraction keeps leaking special cases — reverse direction. Ask whether the current pain point is a **projection of a larger problem** that the system has not yet named.

**Technique:** For a stubborn structural problem `P`, search upward:

> What larger contract, state machine, capability model, or canonical representation would make `P` a trivial projection or special case?

The parent problem is not an excuse for unbounded abstraction. It remains subject to the Admissibility Gate: it must have concrete evidence, a measurable complexity deletion claim, and a feasible transition seam.

**When to apply:** Use only after bottom-up generalization (Section A.2, Section B.11) has been attempted and the result is either too many preserved exceptions or an invariant too weak to delete complexity.

**When to stop:** If the parent problem cannot name eliminated code paths, it is philosophy, not engineering.

### 13. Parameterize Environmental Variation

Differences across platforms, tenants, protocols, deployment environments, feature sets, or dependency versions often create branch explosion.

**Engineering question:** Which environmental variation belongs in an explicit parameter, capability model, policy object, plugin boundary, or generated configuration rather than copied control flow?

### 14. Derive APIs from Caller Reality

An API is defined operationally by how consumers use, wrap, avoid, and compensate for it.

**Technique:** Sample call sites and identify caller-side workarounds, ordering assumptions, repeated conversion, defensive handling, and impossible states. Use this evidence to infer the true contract and boundary.

### 15. Interaction Flow as Architecture

Treat user workflows, control surfaces, and operational procedures as architectural structure. A better abstraction may delete user steps, modes, handoffs, training burden, and recovery paths, not only code branches or adapters.

**Engineering question:** Is the system exposing a command collection because it lacks a direct manipulation model, task object, stateful workspace, guided flow, or intent-level operation?

**Technique:** Map the user's intent to the current action sequence, visible controls, modes, confirmations, feedback delays, and recovery path. Then ask which interaction object or workflow state would make those commands natural operations rather than remembered procedures.

**Do not assume:** Cosmetic UI discomfort is structural pressure. Button color, spacing, and copy are weak signals unless paired with repeated workflow burden, mode confusion, control-surface sprawl, user errors, or recovery loops.

---

# Part 2 — The Abstraction Admissibility Gate

No proposal qualifies as a recommended structural direction until it passes this gate. A sophisticated abstraction without this validation belongs in the rejected or unproven section of the report.

## Mandatory proof obligations for each proposal

| Obligation | What the report must show |
|---|---|
| Concrete symptom | Specific files, modules, call sites, schemas, tests, or dependency edges exhibiting the burden. |
| Hidden invariant hypothesis | The exact common rule or domain meaning believed to unify the symptom family. |
| Process-to-space map | For workflow, lifecycle, orchestration, or stateful interaction candidates: the canonical process object, its base contexts, local instances, projections, and gluing conditions. |
| Projection consistency | For projection-based candidates: which artifacts are projections of the same object, which invariant each projection owns or reflects, and how drift between them is detected or eliminated. |
| Base-change behavior | When variation exists: which environmental, platform, tenant, permission, runner, or capability differences are explicit base parameters, and which core rules remain invariant across bases. |
| Difference preservation | Cases that look similar but must remain distinct, and how the design preserves them. |
| Exception classification | Which exception families would be absorbed by the new structure, which must remain as real differences, and which are false alarms unrelated to this pressure. |
| Complexity deletion | Named branches, adapters, duplicate models, coordinators, or workflow copies removed or made unnecessary. |
| Definition power | What future changes, feature additions, or variant introductions become trivial projections or special cases of this definition. |
| Deformation test | For non-incremental proposals: a concrete new state, environment, gate, failure class, package type, representation, or caller that should be addable with bounded, predictable changes if the abstraction is real. |
| Interaction simplification | For interaction-flow proposals, which user steps, modes, decisions, confirmations, training instructions, or recovery paths disappear or become unnecessary. |
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
- It merely collects process artifacts under a new name without specifying projection consistency, gluing rules, and drift detection.
- It requires a broad rewrite without a transition seam or rollback mechanism.
- It assumes runtime pain, business benefit, or developer friction not evidenced by available data.
- It turns cosmetic UI polish into an architecture proposal without evidence of workflow burden, control-surface sprawl, or interaction-state complexity.
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
- process projection surfaces such as ledgers, event streams, generated docs, dashboards, prompts, reports, manual checklists, CLI output, and status files;
- user task flows, screen flows, command sequences, modes, confirmations, and recovery paths when user interaction is part of the pressure;
- tests describing invariants and edge cases.

When available, also gather:

- churn and repeated modifications;
- issue/incident references;
- performance profiles or SLO evidence;
- UX telemetry such as time-to-complete, backtrack rate, abandonment, error recovery, support tickets, or repeated training instructions;
- deployment boundaries and ownership information.

Do not claim telemetry-based findings when telemetry is unavailable.

## Phase 1.5: Constraint Reality Filter

Before mapping structural pressure, separate real constraints from inertia. This prevents the analysis from over-respecting constraints that do not actually exist, and from dismissing constraints that are genuine and must be honored by any viable proposal.

### Purpose

Every system has constraints it *feels* bound by. Some are real — backed by contracts, data, users, or compliance. Others are inertia — backed by habit, fear of large diffs, or the weight of existing implementation shape. A structural proposal that treats inertia as immutable will be too conservative to solve the problem. A proposal that ignores real constraints will be unimplementable.

This filter runs after the system survey and before the structural pressure map. It is not a finding — it is a **lens calibration step**, parallel to the Entry Diagnostic (which questions inherited vocabulary). The Entry Diagnostic asks "are the names lying to us?"; this filter asks "are the constraints real or are we just afraid?"

### Filter taxonomy

| Constraint source | Nature | Judgment criteria |
|---------|------|---------|
| Public API / SDK contract | **Real constraint** | External callers depend on this behavior; breaking it causes production incidents |
| Persistent data format / schema | **Real constraint** | Production data depends on this structure; requires migration strategy, not dismissal |
| Documented integration interface | **Real constraint** | External systems depend on this protocol; changes require coordination |
| User-visible behavior commitment | **Real constraint** | User workflows depend on this interaction model; changes require migration guidance |
| Deployment / operations constraint | **Real constraint** | Hard requirements: CI pipeline, infra, SLO, etc. |
| Compliance / security requirement | **Real constraint** | Mandated by legal or security policy; non-negotiable |
| Internal callers (same repo) | **Inertia constraint** | Can be updated in a single refactoring pass; should not constrain the target model |
| Legacy naming / package structure | **Inertia constraint** | Should not dictate the shape of the target architecture |
| Existing partial implementation | **Inertia constraint** | Sunk cost; should not distort the target model to preserve partial work |
| "The diff will be too large" | **Inertia constraint** | Migration cost should be assessed separately; must not pollute the target model |
| Organizational habit / "we've always done it this way" | **Inertia constraint** | Not an architecture constraint; belongs to the domain of change management |

### Application rule

Each candidate abstraction, before entering the Admissibility Gate, must answer:

1. **Which real constraints does it respect?** Name the specific contract, data dependency, user promise, or compliance requirement, and how the proposal honors it.
2. **Which inertia constraints is it ignoring?** State explicitly which internal names, package layouts, partial implementations, or diff-size concerns the proposal deliberately overrides.
3. **If the proposal preserves a compatibility shim for an inertia constraint**, it must name the concrete reason (e.g., staged rollout to reduce risk, not "compatibility is good").

A proposal that respects all real constraints while ignoring inertia is not reckless — it is correctly calibrated. A proposal that preserves shims for inertia without naming a concrete reason is over-fitted to the current implementation.

### Interaction with the Admissibility Gate

The constraint reality classification feeds directly into the Admissibility Gate's Hard Rejection Rules:

- A proposal that violates a **real constraint** without a transition seam is **inadmissible** (fails "It requires a broad rewrite without a transition seam or rollback mechanism").
- A proposal that preserves complexity solely to satisfy an **inertia constraint** is a **False Abstraction Risk** (fails "It has no specific code evidence" when the kept complexity has no named contract).

### Output note

The constraint classification is an internal analysis artifact, not a standalone report section. Its results surface in:
- The Structural Pressure Map (pressure signals are filtered: only pressure against real constraints plus pressure from missing invariants)
- The Proposal Card's evidence section (which constraints does this proposal navigate?)
- The Admissibility Gate classification (is a proposal rejected because it ignores a real constraint, or because it preserves inertia?)

## Phase 2: Structural pressure map

Identify recurring forms of pressure:

| Pressure signal | Typical structural hypothesis | Minimum evidence |
|---|---|---|
| Many similar models | Latent canonical domain model | Side-by-side schema and invariant comparison |
| Adapter/conversion explosion | Missing canonical representation or boundary | Multiple concrete conversion paths |
| Mode/platform branching | Unparameterized environmental variation | Branch families and variant rules |
| God coordinator | Local composition failure | Coordination responsibilities and callers |
| Scattered process state | Missing canonical process object with consistent projections | Same lifecycle or workflow represented in multiple artifacts that can drift |
| Painful API | Boundary designed away from caller reality | Multiple caller workarounds |
| Caller compensation / workaround accumulation | Missing transformation protocol or canonical intermediate representation | Multiple callers implementing identical pre-processing, post-processing, or format adaptation |
| Repeated lifecycle bugs | Missing explicit state machine/invariant | Transitions, tests, incident or bug evidence |
| Environment-specific workflow copies | Missing base-change model for capability, platform, runner, tenant, or permission variation | Duplicated status, recovery, verification, or reporting logic across environments |
| Control surface sprawl | Missing direct manipulation model, task object, or intent-level operation | Repeated command sequences, many visible controls, training burden, user errors, or support evidence |
| Mode choreography | Missing task-level interaction state model | Users must remember mode order, switch context repeatedly, or recover from wrong-mode actions |
| Repeated recovery loops | Interaction state machine does not absorb real user behavior | Undo/retry/backtrack paths, abandoned flows, incident/support evidence, or observed task failures |
| Indirect intent mapping | Users translate goals into low-level commands manually | Gap between user intent and action sequence, repeated confirmations, defensive checks, or manual procedures |

## Phase 3: Candidate construction and falsification

For every high-value structural hypothesis:

1. Formulate the proposed invariant or canonical abstraction.
2. Run discovery passes when the invariant is not obvious: data lifecycle, caller reality, failure/recovery, and environmental variation.
3. Generate competing structural explanations for high-leverage pressure sites and compare them before choosing one.
4. For dynamic workflow, lifecycle, orchestration, or interaction-state pressure, run the process spatialization pass: name the base, local instances, projections, gluing rules, and deformation tests.
5. Locate concrete affected paths.
6. Find at least one near-counterexample or meaningful difference.
7. Estimate what complexity disappears and what new complexity is introduced.
8. Define a transition seam, even though this skill does not execute it.
9. For interaction-flow candidates, estimate deleted user steps, modes, decisions, training rules, and recovery paths as well as introduced discoverability or accessibility risks.
10. Classify confidence and state missing evidence.

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

Generate an HTML report named `structural_abstraction_architect_report_{YYYYMMDD}_{HHMM}.html` (e.g. `structural_abstraction_architect_report_20260608_1432.html`). Include timestamp to prevent overwrites across multiple runs. The report contains analysis, not code modifications. If HTML generation or automatic browser launch is not feasible, provide the same content as Markdown and clearly state the limitation.

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
   - Representation duplication, conversion glue, boundary friction, transformation branching, orchestration hotspots, process projection drift, caller pain, and interaction-flow pressure when relevant.

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
   - **Candidate competition matrix** — for high-leverage pressure sites, compare plausible structural explanations and explain why the recommended candidate wins or why no winner is proven.
   - **Projection registry** — for process-spatialization proposals, list each projection artifact, its source of truth relationship, owned/reflected invariants, drift risks, and reconciliation rule.
   - **Complexity deletion scorecard** — before/after counts of representations, adapters, branch families, duplicated tests, and divergent configuration paths, so the team can track whether the abstraction actually simplified the system.
   - **Interaction simplification scorecard** — before/after counts of user steps, modes, visible controls, confirmations, required training rules, and recovery paths for proposals that redesign user workflow structure.
   - **Subsequent eval cases** — concrete scenarios the team can test after refactoring to verify the structure has not regressed (e.g., "add a new payment method without touching the order lifecycle"; "add a manual approval gate without editing unrelated status projections").
   - **Definition quality checklist** — self-check questions derived from this analysis: does the new definition make future variants trivial projections? Does it preserve all meaningful differences? Can a new team member explain the structure in under 5 minutes?

## Proposal card schema

Every proposal card MUST contain:

- Title and classification.
- Quantized badges: `Structural Leverage`, `Transition Burden`, `Risk`, `Confidence`.
- Lens traceability: which structural lens or lenses support the proposal.
- Concrete evidence with file/symbol references.
- Current symptom versus proposed structure.
- Competing structural explanations considered, when the proposal is high leverage or non-obvious.
- Hidden invariant hypothesis.
- **Spatialization Map** (include for proposals whose value depends on turning dynamic workflow, lifecycle, orchestration, approval, retry, or environment-variant behavior into structure):
  - *Canonical process object* — the named object that replaces scattered process fragments.
  - *Base contexts* — environments, platforms, tenants, runners, permissions, branches, gates, or capability classes over which behavior varies.
  - *Local instances* — jobs, packages, sessions, approvals, requests, screens, or lifecycle entities living over those contexts.
  - *Projection artifacts* — files, tables, logs, events, docs, dashboards, prompts, reports, checklists, or UI states that expose the object.
  - *Gluing conditions* — local consistency rules required before global completion, release, rollout, or visible state can be claimed.
  - *Deformation tests* — new states, gates, environments, failure classes, package types, or reporting views that should become cheap changes.
- Meaningful differences preserved.
- Measurable complexity deletion claim.
- Proof obligations and disproof signals.
- Transition seam and authorization boundary.
- Optional code sketches in `<details>` sections; sketches are explanatory only.
- **Interaction Flow Map** (include for proposals whose value depends on changing user workflow structure):
  - *User intent* — what the user is trying to accomplish in domain terms.
  - *Current action sequence* — commands, screens, modes, confirmations, and recovery paths required today.
  - *Current control surface* — visible controls, hidden rules, ordering assumptions, and training burden.
  - *Proposed interaction object or model* — direct manipulation surface, task object, guided state machine, workspace, or intent-level operation.
  - *Deleted workflow complexity* — steps, modes, decisions, confirmations, training instructions, and recovery loops made unnecessary.
  - *New risks* — discoverability, accessibility, expert-user efficiency, migration, and instrumentation needed to prove the new flow works.
- **Transformation Network** (include for proposals whose value depends on changing how data flows, deforms, or is probed across components):
  - *Probing operations* — who reads or queries this object, through what interface, and with what expectation?
  - *Deformation paths* — what shape changes does the object undergo across its lifecycle (serialization, validation, enrichment, projection)?
  - *Caller compensation patterns* — what pre-processing, post-processing, or defensive wrapping do callers repeat because the current interface is incomplete?
  - *Lifecycle flows* — trace the full path of a representative entity or event through the system, noting where it crosses artificial boundaries.

## Topology diagrams

Generate topology comparisons only for proposals whose value depends on a changed dependency, boundary, data-flow, composition shape, or interaction-flow structure. Do not require diagrams for textual contract clarifications or evidence gaps.

For applicable cards, render two full-width Mermaid diagrams beneath the comparison block:

- `Current Topology`: observed structural pressure.
- `Proposed Structural Topology`: candidate invariant, boundary, canonical model, or composition path.

For interaction-flow proposals, these diagrams may instead be labeled `Current Interaction Flow` and `Proposed Interaction Model`.

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

Use the Mermaid initialization pattern from `../reviewable-html-report/references/report_base.md` (resolved relative to this SKILL.md). This skill's theme uses:

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

Mermaid compatibility rules are in `../reviewable-html-report/references/report_base.md`.

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

Use the lightbox JavaScript from `../reviewable-html-report/references/report_base.md` (resolved relative to this SKILL.md). The code is identical across all report skills.

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
- a static artifact dump that renames a workflow but does not enforce projection consistency, local-to-global gluing, or cheap deformation;
- a single elegant candidate for a high-leverage problem without considering plausible rival explanations;
- report polish that begins before evidence, candidate competition, and admissibility classification are complete;
- direct code modification instructions presented as already approved work;
- historical or philosophical exposition unrelated to the engineering decision.

---

# Execution Flow

1. Confirm the target codebase or inspect the supplied project context.
2. Determine whether this skill is the right first lens or whether the task should be routed to pragmatic transition analysis.
3. Survey structure, interfaces, representations, variations, transformations, tests, process projection surfaces, user/task flows when relevant, and available operational evidence. Question whether the current domain vocabulary, type system, process vocabulary, boundary naming, or interaction vocabulary distorts the underlying structure.
4. Run the Constraint Reality Filter (Phase 1.5): list the constraints the system appears bound by, classify each as real or inertia, and carry only real constraints into the pressure map.
5. Build the structural pressure map and evidence ledger.
6. For open-ended or non-obvious pressure sites, use `references/discovery_patterns.md` to run discovery passes and candidate competition before selecting a direction.
7. For dynamic workflow or orchestration pressure, run process spatialization before proposing a decomposition: identify base contexts, local instances, projection artifacts, gluing conditions, and deformation tests.
8. Construct candidate abstractions and aggressively test them against counterexamples and the admissibility gate. Ensure each candidate's constraint classification (which real constraints it respects, which inertia constraints it ignores) is explicit before classification.
9. Classify validated opportunities, unproven hypotheses, false abstractions, and pragmatic sequencing problems.
10. Generate `structural_abstraction_architect_report_{YYYYMMDD}_{HHMM}.html` with interactive review support only after the structural conclusions are formed.
11. Open the report in a browser only when supported; otherwise provide its saved path or Markdown fallback.
12. After user feedback, produce a transition handoff brief. Do not execute code changes without explicit authorization.
