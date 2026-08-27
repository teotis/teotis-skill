# abstraction-architect Detailed Method and Report Specification

# Part 1 — Structural Abstraction Method

The aim is not to maximize abstraction. The aim is to find abstractions that **delete repeated complexity while preserving meaningful differences**.

For open-ended architecture reviews, unclear pressure maps, or candidates that feel obvious but weak, read `references/discovery_patterns.md` before recommending a structural direction. Use it as a discovery aid, not as report filler.

For every candidate, ask:

> What recurring engineering burden exists, what hidden invariant might unify it, and what proof would demonstrate that the proposed abstraction is simpler in practice rather than merely more elegant on paper?

For candidates whose pain appears as a process rather than a thing, add:

> What static structural object would make the valid dynamic paths, local statuses, approvals, retries, reports, and environment variants natural projections or local sections of the same system?

### Entry Diagnostic: Question the Inherited Vocabulary

When naming drift, duplicated translations, or contradictory boundaries provide evidence that vocabulary may be part of the pressure, ask: **is the current domain vocabulary, type enumeration, process vocabulary, or boundary naming misleading the system into false distinctions?**

Many structural problems begin not with wrong code but with wrong language — DTOs named after implementation concerns rather than domain invariants, status enums that split what is essentially one state, workflow stages named after tools rather than capabilities, boundary names that create artificial separations between coupled behaviors.

This diagnostic is not a mandatory preflight or a finding. Treat inherited names as provisional only when concrete mismatches make the question informative; otherwise preserve shared language and spend the evidence budget elsewhere.

The Constraint Reality Filter (Part 3, Phase 1.5) is the parallel calibration for constraints: separating real contractual constraints from inertial ones. Together, these two steps ensure the analysis neither inherits false distinctions from vocabulary nor preserves false constraints from habit.

### Discovery Passes Before Commitment

Before committing to a high-leverage abstraction, choose the probes with the highest expected information gain. Useful directions may include:

- **Data lifecycle** — how one entity or event changes across storage, API, jobs, UI, reports, and tests.
- **Caller reality** — how consumers wrap, compensate for, or avoid the current API or boundary.
- **Failure and recovery** — what retries, incidents, repair scripts, manual steps, and status mismatches reveal.
- **Environmental variation** — how tenants, platforms, protocols, runners, permissions, and deployments deform the same behavior.
- **Observational probes** — whether callers, tests, queries, telemetry, reports, policy checks, and recovery paths can distinguish rival structural explanations.

These passes are a candidate generator, not a coverage quota. Stop when additional passes are unlikely to change the recommendation or claim permission, and record material gaps instead of performing every pass.

### Candidate Competition

For ambiguous or high-consequence pressure sites, compare the leading explanation with at least one *real* rival, which may be local deletion, boundary repair, status quo, or a different structure. When evidence makes one path plainly dominant, state why rival generation would add no decision value instead of inventing a second abstraction.

If candidates explain different burdens, report them separately. If one candidate is weaker, say why it is rejected, deferred, or scoped down. Do not present one elegant abstraction as inevitable merely because it is available.

### Candidate Proof Route

Before recommending a structural rewrite, canonical model, or process-spatialization proposal, turn the candidate into a short proof route. The proof route is not a mathematical performance; it is a practical chain showing why this abstraction is justified by the current system.

Useful proof-route dimensions, selected in proportion to the strength and consequence of the recommendation:

| Step | Question |
|---|---|
| **Family proof** | Why do these concrete examples belong to the same exception family, pressure pattern, or workflow burden? |
| **Difference proof** | Which differences are projection differences, parameter differences, or local policy differences, and which are semantic differences that must remain visible? |
| **Preservation proof** | How would the proposed structure generate, preserve, or safely translate the old behaviors users, callers, data, or operations still depend on? |
| **Future deformation proof** | Which future change becomes a bounded deformation rather than a new branch family, adapter set, manual workflow, or report drift? |
| **Falsifier** | What observation, counterexample, caller behavior, production constraint, or migration result would prove the abstraction wrong or premature? |

A strong rewrite or canonical-model recommendation should close the decision-relevant parts of this route well enough for another engineer to test or attack it. A preliminary direction may omit unavailable dimensions if it is clearly labeled as a hypothesis, names the missing evidence, and does not claim rewrite readiness. Never manufacture future-deformation value or a token falsifier merely to complete the table.

### Abstraction Fitness Score

Use this score as a decision aid inside candidate competition. It is not a hard gate, not a total order, and not a reason to manufacture evidence. A candidate may be strong with an uneven score when the missing dimensions are irrelevant to the user's decision.

| Dimension | What to look for | Use in decision |
|---|---|---|
| **Clear examples** | Can the abstraction immediately explain three real examples from the current system without hand-waving? | Raises confidence that the definition names a real pattern. |
| **Tool yield** | Does the definition produce checks, migrations, generators, validators, debugging probes, projection registries, or review tools? | Favors abstractions that become useful operations, not just vocabulary. |
| **Cross-context link** | Does it connect previously separated modules, workflows, artifacts, reports, ledgers, or user scenarios? | Helps detect whether the abstraction has reach beyond one local cleanup. |
| **Practical sufficiency** | Under bounded evidence, migration capacity, rollback ability, and maintainer cognition, is this model good enough to use now? | Prevents the most elegant abstraction from crowding out the most usable one. |
| **Hot path value** | Does it touch frequent change paths, high-risk judgment paths, manual coordination loops, release/claim gates, or user-trust paths? | Pulls structural judgment back toward user and engineering value. |
| **Tiny complete loop** | Is there a small pilot, check, fixture, adapter seam, or report projection that can validate the structure before broad migration? | Improves transition safety and user confidence. |

Default report expression should not expose a noisy spreadsheet first. Show the recommended decision, key evidence, main risk, and why rivals lost; keep the fitness details in proposal cards, expandable sections, or appendices.

### Baseline Before Abstraction / Decision Triage

Before escalating a pressure site to a new abstraction, compare it with any **no new abstraction** alternatives that are plausible for the observed burden:

- delete obsolete branches, dead modes, stale compatibility paths, or abandoned workflow steps;
- merge local duplication without creating a new cross-system concept;
- repair a boundary, ownership split, adapter/API contract, or conversion path without naming a new canonical object;
- improve interaction copy, labels, empty states, confirmations, or recovery text when the burden is user confusion rather than structural workflow state;
- keep the status quo with evidence when the code is ugly but stable, low-value, or protected by real constraints.

The following dispositions are useful shorthand when they clarify the decision; mixed or staged outcomes are allowed:

- `local deletion wins`: the concrete symptom disappears without introducing a new invariant, projection registry, framework, DSL, coordination layer, or migration surface.
- `boundary repair wins`: the symptom is real, but the right response is to shrink or clarify an existing boundary rather than promote a new structural model.
- `structural candidate worth testing`: lower-abstraction paths fail to explain the recurring exception family, projection drift, caller compensation, lifecycle inconsistency, or workflow burden.

State the level of intervention and deciding evidence in plain language. The labels are optional, and an outcome may combine local deletion now with a structural experiment later.

### Anti-Beauty Gate

Structural candidates often become attractive because they are unified, elegant, general, or conceptually beautiful. That is not enough. Downgrade the candidate to `interesting but not actionable` unless it can show at least one concrete value path:

- deletes a current burden in a hot path;
- reduces a maintenance, user, or recovery operation the team actually performs;
- protects a real contract or removes caller compensation;
- creates a small validation loop that can disprove the structure before broad migration.

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

For a consequential unification proposal, classify the exception families that could change the decision. The following categories are prompts, not an exhaustive or mutually exclusive ontology:

| Category | Meaning | Action |
|---|---|---|
| **Absorbable by new structure** | The exception exists only because the current model is too narrow. A better invariant or canonical representation would make it a natural case, not an exception. | Candidate for unification. |
| **Must remain as real difference** | The exception carries genuinely distinct business rules, failure semantics, lifecycle transitions, or ownership. Erasing it would create bugs. | Preserve explicitly in the proposed design. |
| **False alarm** | The exception looks like a variant of the pressure pattern but actually belongs to a different concern entirely. | Exclude from this structural analysis. |

Allow `mixed`, `context-dependent`, and `unknown pending evidence` when a case changes category by observer, migration phase, or operating mode. A strong unification claim still has to show that meaningful differences will not be erased; it does not have to force every case into a clean bucket.

## B. Constructing Better Structures

### 6. Spatialize Dynamic Processes

When pressure appears as a timeline, state machine, retry loop, approval chain, orchestration graph, queue, workflow, or environment-specific run path, consider whether a **canonical process object** would explain observed projection drift. Treat it as one hypothesis alongside local state repair, clearer ownership, a smaller orchestrator, or an explicit protocol.

If process spatialization is the leading hypothesis and the detail changes the decision, map the relevant pieces:

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

When a proposal claims that two representations are equivalent, make that
claim relative to an explicit observer, operation, or context. Record which
differences are intentionally ignored, which must remain visible, what
information a transformation loses, and whether that loss is allowed,
traceable, or recoverable.

Do not infer domain identity from matching fields, serialization, or current
tests alone. Identify a **separating probe** capable of exposing differences in
lifecycle, ownership, ordering, failure, security, or recovery semantics. If
the available probes cannot distinguish rival candidates, preserve the
uncertainty and classify the conclusion as unproven.

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

For high-consequence proposals that rely on local facts composing into a global release, authorization, money, security, or consistency claim, provide a **Local-to-Global Certificate**. For ordinary internal composition, use only the subset needed to expose a realistic failure:

- name the local units and their overlap domains;
- define the compatibility predicate on each overlap;
- state which component owns truth at the boundary;
- explain how conflicts are detected and arbitrated;
- check whether compatible local states produce an existing global state;
- check whether that global state is unique for the claimed invariant;
- identify ordering, transaction, security, quota, or policy constraints that
  are invisible to pairwise checks.

Pairwise compatibility is not sufficient evidence of global composition.

When local checks close but the global claim remains doubtful, run a
**Residual Obstruction Test**:

1. Define the allowed operations, such as transitions, approvals,
   compensations, projection updates, adapter conversions, and recovery steps.
2. Define the obligations those operations are expected to discharge, such as
   dependencies, evidence, ownership, consistency, and pending responsibility.
3. Check whether the observed global state can be legally generated,
   explained, eliminated, and recovered using those operations.
4. Trace complete cycles and round trips, not only adjacent pairs.
5. Classify any residual as evidence of a missing canonical object, incomplete
   state space, wrong boundary, hidden global coordination requirement, or a
   meaningful difference that must remain.

Do not introduce homology terminology or require a mathematical chain complex.
This is an engineering falsification test for claims of natural composition.

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

No strong rewrite or canonical-model claim qualifies as a recommended structural direction until the decision-relevant parts of this gate are satisfied. A proportional exploratory direction may remain a clearly labeled hypothesis with missing evidence and a next probe; do not force it into a false validated/unproven binary.

## Proportionate proof obligations

| Obligation | What the report must show |
|---|---|
| Concrete symptom | Specific files, modules, call sites, schemas, tests, or dependency edges exhibiting the burden. |
| Hidden invariant hypothesis | The exact common rule or domain meaning believed to unify the symptom family. |
| Candidate proof route | The family proof, difference proof, preservation proof, future deformation proof, and falsifier for a strong structural rewrite or canonical-model claim; select only the dimensions that change a lighter recommendation. |
| Abstraction fitness | Non-gating assessment of clear examples, tool yield, cross-context link, practical sufficiency, hot path value, and tiny complete loop. |
| Process-to-space map | For workflow, lifecycle, orchestration, or stateful interaction candidates when this map changes the decision; do not require a canonical process object as a default answer. |
| Projection consistency | For projection-based candidates: which artifacts are projections of the same object, which invariant each projection owns or reflects, and how drift between them is detected or eliminated. |
| Observational adequacy | Which callers, tests, queries, telemetry, reports, policy checks, or recovery paths support the candidate; which observation blind spots remain; and which separating probe distinguishes it from the nearest rival. |
| Local-to-global certificate | For consequential composition claims where pairwise checks could hide a global failure; use a smaller compatibility check for ordinary internal composition. |
| Residual obstruction | When local checks appear valid: whether the claimed global state can be legally generated, explained, eliminated, and recovered through allowed operations, including full-cycle and round-trip behavior. |
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

Classify each consequential candidate as one of the following, while allowing mixed or pending states when evidence spans categories:

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
- It chooses between rival candidates when current observations cannot distinguish them and names no separating probe.
- It treats pairwise compatibility as proof of a valid global state without checking global constraints or full-cycle residuals.
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

When constraint assumptions materially affect the target or recommendation, separate hard constraints, migration/feasibility constraints, and unsupported habit. This prevents both over-respecting assumptions and dismissing costs that make an otherwise elegant target unusable.

### Purpose

Every system has constraints it *feels* bound by. Some are real — backed by contracts, data, users, or compliance. Others are inertia — backed by habit, fear of large diffs, or the weight of existing implementation shape. A structural proposal that treats inertia as immutable will be too conservative to solve the problem. A proposal that ignores real constraints will be unimplementable.

This filter is a lens, not a mandatory phase. Apply it where the classification changes the decision, and preserve uncertainty when the available evidence cannot distinguish a hard constraint from a costly but negotiable one.

### Filter taxonomy

| Constraint source | Nature | Judgment criteria |
|---------|------|---------|
| Public API / SDK contract | **Real constraint** | External callers depend on this behavior; breaking it causes production incidents |
| Persistent data format / schema | **Real constraint** | Production data depends on this structure; requires migration strategy, not dismissal |
| Documented integration interface | **Real constraint** | External systems depend on this protocol; changes require coordination |
| User-visible behavior commitment | **Real constraint** | User workflows depend on this interaction model; changes require migration guidance |
| Deployment / operations constraint | **Real constraint** | Hard requirements: CI pipeline, infrastructure, SLO, and similar constraints |
| Compliance / security requirement | **Real constraint** | Mandated by legal or security policy; non-negotiable |
| Internal callers in the same repository | **Context-dependent** | Often changeable, but volume, ownership, generated clients, release coupling, or rollback needs may make them a real migration constraint |
| Legacy naming / package structure | **Usually soft** | Should not dictate the target alone, but shared language and tooling compatibility can carry real coordination value |
| Existing partial implementation | **Context-dependent** | Sunk cost alone is not a reason to preserve it; validated behavior, delivery timing, and recovery value still matter |
| "The diff will be too large" | **Feasibility signal** | Diff size is not an architectural invariant, but reviewability, rollout capacity, and rollback risk can change the viable target or staging |
| Organizational habit / "we've always done it this way" | **Weak evidence** | Habit alone is not binding; ownership, training, incident response, and coordinated change capacity may still be relevant constraints |

### Application rule

Before making a high-consequence recommendation, answer the decision-relevant subset:

1. **Which real constraints does it respect?** Name the specific contract, data dependency, user promise, or compliance requirement, and how the proposal honors it.
2. **Which constraints are negotiable, and on what evidence?** Do not infer negotiability merely from being internal.
3. **If the proposal preserves a compatibility shim or migration stage**, name the concrete value it protects, such as rollback, coordinated release, or bounded operational risk.

A proposal is calibrated when it distinguishes target-shape constraints from transition constraints without pretending the latter are free. A shim without a concrete value is suspect; a staged seam with real rollback or coordination value is not mere inertia.

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
| Artifact or report synchronization drift | Missing intermediate representation, projection registry, or transformation protocol rather than a final domain model | Multiple reports, ledgers, prompts, exports, status files, or dashboards restating the same fact with drift |
| Repeated lifecycle bugs | Missing explicit state machine/invariant | Transitions, tests, incident or bug evidence |
| Environment-specific workflow copies | Missing base-change model for capability, platform, runner, tenant, or permission variation | Duplicated status, recovery, verification, or reporting logic across environments |
| Control surface sprawl | Missing direct manipulation model, task object, or intent-level operation | Repeated command sequences, many visible controls, training burden, user errors, or support evidence |
| Mode choreography | Missing task-level interaction state model | Users must remember mode order, switch context repeatedly, or recover from wrong-mode actions |
| Repeated recovery loops | Interaction state machine does not absorb real user behavior | Undo/retry/backtrack paths, abandoned flows, incident/support evidence, or observed task failures |
| Indirect intent mapping | Users translate goals into low-level commands manually | Gap between user intent and action sequence, repeated confirmations, defensive checks, or manual procedures |

## Phase 3: Candidate construction and falsification

For a high-value structural hypothesis, select the steps that can change the recommendation or claim permission:

1. Compare plausible no-new-abstraction alternatives before escalating; skip alternatives contradicted by current evidence.
2. Run the discovery passes with the highest information gain when the invariant is not obvious.
3. Compare a real rival for ambiguous or high-consequence sites; do not invent candidate count.
4. When pressure crosses reports, ledgers, generated docs, prompts, exports, dashboards, callers, or workflow artifacts, run the **IR vs domain model fork**: ask whether the system needs a stable intermediate representation, projection registry, or transformation protocol before it needs a final domain model.
5. Test whether current probes can distinguish the nearest candidates; if not, name a separating probe and keep the conclusion unproven.
6. For dynamic pressure, run process spatialization only when a canonical process object is a leading, decision-relevant hypothesis.
7. Use a Local-to-Global Certificate or Residual Obstruction Test only when pairwise checks could hide a consequential global contradiction.
8. Locate concrete affected paths.
9. Look for a near-counterexample or meaningful difference when it can separate the leading explanations.
10. Match proof-route depth to recommendation strength. An exploratory recommendation may remain explicitly partial; a rewrite-ready claim may not.
11. Score candidate fitness as a non-gating comparison aid: clear examples, tool yield, cross-context link, practical sufficiency, hot path value, and tiny complete loop.
12. Estimate what complexity disappears and what new complexity is introduced.
13. Define a transition seam, even though this skill does not execute it. Prefer a tiny complete loop when one can validate the structure before broad migration.
14. For interaction-flow candidates, estimate deleted user steps, modes, decisions, training rules, and recovery paths as well as introduced discoverability or accessibility risks.
15. Classify confidence and state missing evidence.

## Phase 4: Handoff boundary

When the user wants implementation planning, or the accepted direction crosses a consequential production, data, API, deployment, security, or ownership boundary, produce a proportionate handoff brief. Useful fields include:

- accepted target structure;
- unchanged invariants;
- candidate pilot boundary;
- required compatibility or adaptation seam;
- evidence still needed before implementation;
- explicit statement that code changes require user authorization.

---

# Part 4 — Report Specification

## Deliverable

The default deliverable is the smallest form that preserves the decision, evidence, uncertainty, and next step. This may be a direct chat answer, a short Markdown note, or a durable report; one screen is a preference, not a truncation rule.

HTML is an optional review surface, not proof of deep analysis. Generate it only when interactivity materially lowers review cost:

- more than three candidates or pressure sites need comparison, filtering, or comments;
- evidence ledger, proposal cards, review comments, or feedback export will change the next decision;
- the user explicitly asks for a formal report or interactive review surface;
- long-term archival, team review, public-release audit, or agent handoff needs a durable review artifact.

When generated, the HTML report is named:

- `structural_abstraction_architect_report_{YYYYMMDD}_{HHMM}.html`

Markdown is the default durable source when a file artifact is useful. HTML may be generated from the same evidence when the review gate is met:

- `structural_abstraction_architect_report_{YYYYMMDD}_{HHMM}.md`

When both are produced, keep conclusions and evidence IDs aligned. A failed optional HTML upgrade does not block delivery of a complete Markdown or chat result.

When a Markdown source report is produced, HTML and Markdown must share the same evidence ledger, proposal IDs, admissibility classifications, and conclusions. HTML may add visualizations, filters, and review controls; it must not introduce conclusions absent from the underlying analysis or Markdown source.

When HTML is generated, implement the section index as the left collapsible scroll-spy TOC sidebar (shared contract: `html-response/references/html_system_spec.md` §3.1); the bundled `references/fallback.html` already follows it.

## Adaptive report elements

Include only elements that preserve evidence, distinguish candidates, or support the next decision. A short analysis need not instantiate every section below.

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
   - Include when plausible rivals or rejected abstractions would otherwise be mistaken for omissions.

7. **Transition Handoff Brief**
   - Include only for user-relevant accepted candidates.
   - Frame work for later pragmatic planning, not automatic implementation.

8. **Uncertainties and Missing Evidence**
   - Explicit limitations and what further inspection would change confidence.

9. **Reusable Analysis Artifacts** (include when the analysis yields artifacts the team can reuse independently)
   - **Counterexample catalog** — cases that look structurally similar to a recommended unification but must remain distinct, with the specific rule or invariant that distinguishes them.
   - **Candidate competition matrix** — for high-leverage pressure sites, compare plausible structural explanations and explain why the recommended candidate wins or why no winner is proven.
   - **Abstraction fitness scorecard** — a non-gating comparison of clear examples, tool yield, cross-context link, practical sufficiency, hot path value, and tiny complete loop.
   - **Projection registry** — for process-spatialization proposals, list each projection artifact, its source of truth relationship, owned/reflected invariants, drift risks, and reconciliation rule.
   - **Complexity deletion scorecard** — before/after counts of representations, adapters, branch families, duplicated tests, and divergent configuration paths, so the team can track whether the abstraction actually simplified the system.
   - **Interaction simplification scorecard** — before/after counts of user steps, modes, visible controls, confirmations, required training rules, and recovery paths for proposals that redesign user workflow structure.
   - **Subsequent eval cases** — concrete scenarios the team can test after refactoring to verify the structure has not regressed (e.g., "add a new payment method without touching the order lifecycle"; "add a manual approval gate without editing unrelated status projections").
   - **Definition quality checklist** — self-check questions derived from this analysis: does the new definition make future variants trivial projections? Does it preserve all meaningful differences? Can a new team member explain the structure in under 5 minutes?

## Proposal card schema

Proposal cards are optional. When they help comparison, include the subset below that changes the decision; do not manufacture scores, rivals, maps, or proof fields to fill a schema:

- Title and classification.
- Quantized badges: `Structural Leverage`, `Transition Burden`, `Risk`, `Confidence`.
- Lens traceability: which structural lens or lenses support the proposal.
- Concrete evidence with file/symbol references.
- Current symptom versus proposed structure.
- Competing structural explanations considered, when the proposal is high leverage or non-obvious.
- Hidden invariant hypothesis.
- Candidate proof route: family proof, difference proof, preservation proof, future deformation proof, and falsifier.
- Abstraction fitness score: clear examples, tool yield, cross-context link, practical sufficiency, hot path value, and tiny complete loop. Keep this as decision support, not a pass/fail gate.
- IR vs domain model note when the proposal touches multiple artifacts, reports, ledgers, workflows, callers, or projection surfaces.
- Tiny complete loop or pilot seam when a small validation path exists before broad migration.
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

When a before/after comparison materially improves understanding, one or two diagrams may be rendered beneath the relevant analysis:

- `Current Topology`: observed structural pressure.
- `Proposed Structural Topology`: candidate invariant, boundary, canonical model, or composition path.

For interaction-flow proposals, these diagrams may instead be labeled `Current Interaction Flow` and `Proposed Interaction Model`.

### Mermaid compatibility guidance

- Include Mermaid 10 via a module import and initialize globally with a dark theme.
- Use `flowchart TB`, `flowchart TD`, or `flowchart LR`; never use `graph` syntax.
- Use ASCII-only node and edge labels inside Mermaid blocks.
- Do not use emoji or `linkStyle` directives inside Mermaid code.
- Use `subgraph id["Label"]` form.
- Sanitize labels and avoid markdown/path punctuation likely to break parsing.
- Choose dimensions that remain readable at the target viewport; fixed `380px` height and lightbox behavior are optional implementation details.
- Avoid duplicated initialization when multiple diagrams share a page.
- Add a lightbox only when the diagrams are too dense to inspect inline.
- If Mermaid cannot load in the target environment, retain readable Mermaid source and disclose that rendering is unavailable; do not claim that diagrams rendered successfully.

### Optional Mermaid initialization example

Use the Mermaid initialization pattern provided by the `reviewable-html-report` capability. In this repository, `skills/reviewable-html-report/references/report_base.md` is an optional reference, not a standalone dependency. This skill's theme uses:

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

Follow the Mermaid compatibility rules from the `reviewable-html-report` capability when available; otherwise preserve readable Mermaid source and disclose the rendering limitation.

### Optional CSS example for topology comparison and lightbox

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

Use the lightbox behavior from the `reviewable-html-report` capability when available. Otherwise provide a self-contained static fallback without making browser-only behavior a completion requirement.

## Optional interactive review system

Add review controls only when the user or review workflow needs persistent item-level decisions. Choose storage deliberately: `localStorage` is acceptable for local, non-sensitive review state but is not a default requirement.

Possible controls include:

- review textarea;
- 1–5 star confidence/acceptance rating;
- status selector with: `[Structurally Sound] [Needs More Evidence] [Too Abstract] [Send to Transition Planning] [Reject]`;
- optional reviewer note about a missing counterexample or operational constraint.

## Feedback export

When exported feedback is part of the requested workflow, provide a clearly labeled export action in a location appropriate to the interface.

Export the fields needed for the selected handoff. A next-action directive may summarize authorization and evidence boundaries, but fixed wording or automatic routing to another skill is not required.

```text
[Next Action Directive] Treat the structural recommendations above as hypotheses that must be translated into safe engineering work. For items marked "Send to Transition Planning", evaluate transition burden, business relevance, compatibility boundaries, rollout controls, rollback strategy, ownership, and short, medium, and long-term ROI using the Pragmatic Renewal Architect approach. Do not modify code unless I explicitly authorize implementation after reviewing the proposed transition plan.
```

Clipboard copy and a success notification are optional interface conveniences; provide a visible downloadable/static fallback when browser APIs are unavailable.

---

# Part 5 — Relationship to Pragmatic Renewal Architect

The two skills address different failure modes:

| Skill | Primary question | Prevents |
|---|---|---|
| Structural Abstraction Architect | What deeper structure can eliminate recurring complexity? | Endless patches, duplicated representations, artificial boundaries, abstraction blindness |
| Pragmatic Renewal Architect | What safe, worthwhile step can move the system forward now? | Grand rewrites, rollout failure, ROI blindness, unmanaged transition debt |

## Proportionate handoff rule

A structural proposal that materially affects production architecture, persistence, public APIs, deployment topology, security, or multiple team boundaries should receive proportionate transition evaluation before implementation. This may be a compact implementation plan for a small reversible change or a dedicated renewal workflow for broad, coupled migration; the skill name is not the gate.

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
- a fitness score table that overwhelms the user, creates false precision, or replaces the admissibility gate;
- a recommended structural rewrite whose proof route does not close;
- report polish that begins before evidence, candidate competition, and admissibility classification are complete;
- direct code modification instructions presented as already approved work;
- historical or philosophical exposition unrelated to the engineering decision.

---

# Execution Flow

1. Confirm the target codebase or inspect the supplied project context.
2. Determine whether this skill is the right first lens or whether the task should be routed to pragmatic transition analysis.
3. Survey the evidence faces likely to change the decision. Question inherited vocabulary only when concrete drift or translation pressure makes it suspect.
4. Apply the Constraint Reality Filter where constraint classification matters; distinguish hard, feasibility/migration, soft, and unknown constraints rather than forcing real/inertia binaries.
5. Build the structural pressure map and evidence ledger.
6. For open-ended or non-obvious pressure sites, use `references/discovery_patterns.md` to run discovery passes, observational probe analysis, and candidate competition before selecting a direction.
7. For dynamic workflow or orchestration pressure, compare the relevant lower-cost paths and consider whether `local deletion wins`, `boundary repair wins`, or a structural candidate best explains the evidence. Run process spatialization only when its detail changes the recommendation: identify the relevant base contexts, local instances, projection artifacts, gluing conditions, and deformation tests.
8. For equivalence claims, state the observer or context and material blind spots. Require a Local-to-Global Certificate or full-cycle residual inspection only for consequential composition claims.
9. For artifact/report/workflow synchronization pressure, decide whether the right candidate is a stable IR, projection registry, or transformation protocol rather than a final domain model.
10. Construct candidates and test them proportionally against decision-relevant counterexamples and constraints; preserve unknown or mixed classifications.
11. Match proof-route and fitness detail to recommendation strength; do not force a rival, score, or completed proof for a clearly labeled exploratory direction.
12. Classify validated opportunities, unproven hypotheses, false abstractions, and pragmatic sequencing problems.
13. Deliver the smallest complete decision surface. Use Markdown when a durable artifact helps; add HTML only after structural conclusions are formed and interactivity materially helps review.
14. If a report is generated, provide the saved report path and a clickable `file://` URL. Open the report only when the user requests a preview or the environment explicitly supports interactive preview without CI, SSH, or headless side effects.
15. Produce a transition handoff only when the user wants implementation planning or the change consequences warrant it. Do not execute code changes without explicit authorization.
