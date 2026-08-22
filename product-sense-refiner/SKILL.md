---
name: product-sense-refiner
description: Use when a technically plausible design, workflow, report, scoring system, agent tool, or interaction needs sharper product fit, clearer defaults, decision-useful output, better recommendation framing, or fewer misleading incentives.
---

# Product Sense Refiner

## Mission

Refine a technically plausible design into a decision-useful product experience.

The core move:

> Start from the user's actual benefit, then the decision and default answer, and work backward to the internal model.

Use this skill when a solution is reasonable but still feels generic, over-mechanized, too internally focused, too verbose by default, hard to operate, or not sharp enough for the user's real choice.

## Use When

Use this skill when:

- a feature, report, workflow, scoring system, agent tool, or architecture plan is technically valid but not product-sharp;
- the user asks for deeper insight, better optimization, product sense, or why a design lacks fit;
- a design exposes many mechanisms but does not make the user's next decision obvious;
- default output is too detailed, vague, or not action-oriented;
- a metric, ranking, or evaluation could reward the wrong behavior;
- multiple valid strategies exist and the design must decide what should be default, hidden, optional, or unsupported.

Do not use it for narrow bug fixes, emergency recovery, purely mechanical implementation, math tutoring, career interview preparation, or already approved specs where product framing is intentionally fixed.

## Capability Load (Pilot)

Separate **task fit** from **load depth** (project contract: Skill Intelligence Adaptation v2).

**Task fit:** if this run would not add a relevant user decision/intent, Human Terminal Fit, reward-alignment, or default-answer judgment, do not run the full skill. A bounded companion delta remains valid when one concrete product risk is already visible.

**Self-probe** before Light / Skip|Delta (escalate to **Full** when uncertainty materially affects authorization, a strong recommendation, or user trust; record ordinary unknowns and continue):

1. What is the actual benefit to the user?
2. Can you name the user's next decision?
3. What is the shortest honest default answer?
4. Is there at least one Human Terminal Fit or reward-misalignment finding?
5. What fails if you skip the full lens (false certainty, bad default, skewed incentives)?

| State | When | Load |
|---|---|---|
| **Skip \| Delta** | Probe passes; only one default/copy/incentive fix | Hard bounds + minimal delta |
| **Light** | Product judgment needed but narrow | Decision + default answer + one keep/change/remove + one risk |
| **Full** | Weak path, multi-candidate, probe fails, or full refinement requested | Full affordance menu and optional references |

**Hard gate (always, before finish):** when a user choice is central, the decision or intent is named; fact / judgment / expression are not mixed; recommendation does not invent false certainty or reward clearly wrong behavior. On failure, escalate, soften the claim, or state that no product change is justified. `No change` is a valid result.

## Workflow

### 1. Name The User Decision

State the decision the user is trying to make. Do not start by describing the feature.

Before that, identify the user's actual benefit. For learning, growth, creative, or interest-building tasks, an appropriately deeper explanation, a higher-order way of analyzing the problem, a reveal of its essence, transferable judgment, or a demonstration of taste may help more than a short answer. For shallow tasks, solve quickly instead. Depth is chosen by which treatment best improves the user's current state without excessive cost—not by intrinsic problem difficulty alone. A master perspective is an adaptive heuristic for confusion, a faulty frame, undeveloped interest, or high-transfer open problems; it is not a fixed role-play template.

Weak:

```text
This tool scores AI agents.
```

Better:

```text
This tool helps the user decide which agent is suitable for which class of real engineering task.
```

If a user choice is central and the decision cannot be named, clarify it. Exploratory, creative, educational, or support tasks may have an intent or desired outcome rather than one discrete decision.

### 2. Write The Default Answer First

Before refining internals, draft what the user should see by default. A good default answer is short, decision-oriented, and safe from false certainty.

Example:

```text
87 / 100
Suitable for low-risk implementation and existing-plan execution.
Not the first choice for open-ended architecture exploration.
Confidence: high.
```

If the default answer is not useful, the internal model is probably solving the wrong problem.

### 3. Check Human Terminal Fit

Assume the user has limited attention, memory, patience, and trust budget. Check:

- **Entry:** can the user find the right entry without remembering hidden rules?
- **Default path:** does the default action match the user's likely intent?
- **Operation count:** how many clicks, commands, choices, confirmations, or transfers are required?
- **Context load:** what must the user keep in working memory between steps?
- **Recovery:** when the path fails, can the user understand and recover?
- **Capability reachability:** is the strongest useful capability reachable from the default path?

Prefer removing a step, decision, or context reconstruction over adding explanatory text.

### 4. Separate Fact, Judgment, And Expression

Classify each major element:

| Layer | Meaning | Examples |
|---|---|---|
| Fact | Raw observable material | diff, logs, tests, user input, timestamps, artifacts |
| Judgment | System interpretation | score, tier, rank, confidence, risk, incomparable reason |
| Expression | User-facing output | recommendation sentence, report row, dashboard summary |

Do not leak every internal judgment into the default expression. Do not treat expression as evidence.

### 5. Pressure-Test Extreme Archetypes

Test the design against cases that expose product weakness:

- stable but mediocre performer;
- high-upside but inconsistent performer;
- verbose self-reporter with weak evidence;
- small safe fix versus broad risky redesign;
- result that solves the task but creates future maintenance cost;
- result that reframes the problem and improves future work;
- two results that are genuinely incomparable;
- ambiguous task where user intent changes the ranking.

Ask whether the current default answer would mislead the user.

### 6. Find Reward Misalignment

Identify what the design might accidentally reward:

- verbosity instead of evidence;
- effort instead of outcome;
- novelty instead of usefulness;
- low-risk conservatism when exploration is needed;
- impressive framing without solving the core problem;
- forced rankings where the honest answer is incomparable;
- historical anchors that freeze bias;
- metrics that are easy to optimize but not decision-useful.

For each issue, remove the metric, cap it, make it internal-only, or expose it with caveats.

### 7. Decide What Stays Internal

Mark each detail as:

- `default`: shown in the normal answer;
- `detail`: available on request or in detailed mode;
- `audit`: persisted for traceability but hidden unless debugging;
- `discard`: not useful or incentive-warping.

The default answer should usually contain only what the user needs for the next decision.

### 8. Turn Descriptions Into Recommendations

Replace adjective-only praise with fit guidance.

Weak:

```text
This result is excellent and well structured.
```

Better:

```text
Best suited for ambiguous refactoring tasks where structural insight matters more than first-pass predictability.
```

A recommendation sentence should include fit and non-fit when relevant.

## Output Format

Return the smallest decision-useful refinement surface. The following sections are a menu, not a required template; use only what changes the recommendation:

```markdown
## Product Frame
<User decision and corrected product purpose>

## Default Answer
<Recommended default output shape or example>

## Human Terminal Fit
<Entry, default path, operation count, context load, recovery, capability reachability>

## Keep
<Parts of the current design that serve the user decision>

## Change
<Internal model or workflow changes that improve product fit>

## Remove
<Metrics, outputs, or mechanisms that create bad incentives or false clarity>

## Keep Internal
<Analysis that should remain available but hidden by default>

## Recommendation Wording
<Actionable user-facing sentences>

## Risks
<Ways the refined design could still mislead users>
```

For small tasks, compress the sections but preserve the logic: decision, default answer, fit, changes, removals, and recommendation.

## Completion Check

Before finishing, verify that the user decision is explicit, the default answer is short and actionable, human terminal fit was checked, facts and judgments were separated from expression, at least one edge archetype was pressure-tested, bad incentives were removed or contained, and the recommendation says what the result is suitable and unsuitable for when that matters.
