---
name: grothendieck
description: >
  Complex engineering architecture analysis using Grothendieck's mathematical thinking framework.
  Produces a comprehensive HTML report with interactive review system.
  Use this skill whenever the user mentions architecture review, codebase analysis, system design evaluation,
  refactoring strategy, technical debt assessment, or wants to find non-incremental optimization opportunities
  in a codebase. Also trigger when the user asks "how to improve this project's architecture",
  "find major refactoring opportunities", or any request to deeply analyze a system's design quality.
  Even if the user just says "analyze this codebase" or "review the architecture", use this skill.
---

# Grothendieck Architecture Analysis

Perform a comprehensive, exhaustive architectural analysis of the target project using **Grothendieck's mathematical thinking system**. The goal is to identify directions with high potential for **non-incremental architectural optimization**. Do NOT modify any code — only produce analysis.

The final deliverable is an **HTML report** that opens automatically in the browser.

## Invocation

When the user invokes this skill:
1. Ask which codebase/directory to analyze (if not already specified)
2. Explore the project structure to understand the codebase
3. Perform the full Grothendieck analysis
4. Generate the HTML report
5. Open it in Chrome automatically

---

## Part 1: Analysis Methodology — Grothendieck's Thinking System

Grothendieck reshaped algebraic geometry through a universal methodology: **"make hard problems disappear by rebuilding the foundation."** The following 11 principles form an **organic whole**: the first 4 provide direction (how to see), the latter 7 provide tools (how to act).

For every finding, ask: **What would Grothendieck see here?**

### A. Philosophical Attitudes — Determining "What You See"

**1. The Rising Sea — Reject Local Hacks**

Facing a hard problem, ordinary engineers reach for hammers (patches, if/else, try/catch). Grothendieck's approach is to **raise the water level**: keep elevating the abstraction layer until the problem is naturally dissolved.

**Core insight**: When you find yourself "wrestling with code" — excessive special cases, unending bugs, everything coupled — this is a signal: **the abstraction level is too low**. The correct response is not to hack harder, but to **step back, elevate the abstraction dimension, and let the sea淹没 them**.

**2. Finding Absolute Motives — Converge Polymorphic Appearances**

The same underlying thing appears in completely different "forms" across different contexts. Grothendieck's "motive" concept: cohomology, ℓ-adic cohomology, de Rham cohomology — these seemingly different theories are **projections of the same thing**.

**Core insight**: When you see N modules/state structures/data types that look "similar but different", don't just extract a common base class (that's syntax-level abstraction). Ask: **what deeper thing are they projections of?** Find that motive, and N appearances unify automatically.

**3. Eliminate Artificial Boundaries — Melt Isolated Islands**

Most system coupling comes not from "functional complexity" but from **lines developers drew for convenience**: package boundaries, module boundaries, layer boundaries, process boundaries. Once drawn wrong, all subsequent code must spend effort **crossing these boundaries**, generating glue, adapters, conversion layers.

**Core insight**: Good boundaries should be **natural seams of the thing itself**, not arbitrary cuts. Ask: **if this line didn't exist, would the system be simpler or messier?** If simpler, the line is wrong.

**4. Childlike Simplicity — Naturally Falling Fruit**

When the foundation is right, proofs become "almost trivial." **Core insight**: if a feature requires "clever tricks", "experienced seniors to maintain", or long comments explaining "why we write it this way" — this isn't something to be proud of, it's a **symptom of wrong foundation**. Good architecture lets new features fall like ripe fruit, making the process of "implementing it" almost nonexistent.

### B. Operational Tools — Determining "How to Act"

**5. Relative Point of View**

Don't study "X" in isolation — study "X → S" (X relative to some base S). All properties are relative and **parameterized**.

**Core insight**: Analyzing a class in isolation is meaningless; analyze it **relative to what it depends on**. Optimization should target "families", not single points.

**6. Universal Property First**

Never "construct then define" — always first characterize what an object **should satisfy** via universal properties, then prove it exists.

**Core insight**: In engineering, this means **interface contracts and invariants precede implementation**. Modules where "implementation comes first, interface patched later" are almost destined to become mud balls.

**7. Functoriality**

Good constructions preserve structure under morphisms. **All operations should be functors** — they should automatically respect existing structure.

**Core insight**: Mode switching, config transformation, parameter passing, lifecycle transitions — if these "actions" are functors, you never need hand-written adaptation logic for each combination. If not, you'll forever write conversions and hit edge cases. Ask: **what does this transformation preserve? What does it break?**

**8. Sheaf / Local-to-Global**

The core of sheaf theory: **locally consistent data automatically composes into global objects** without a central coordinator.

**Core insight**: A healthy pipeline (e.g., Sensor→ISP→HAL→App) should not have a God Object mediating in the middle. Instead, adjacent segments should satisfy "local consistency conditions", and the whole should emerge automatically.

**9. Ruthless Generalization**

Don't solve 3 special cases — find the parent problem that contains them, making special cases **automatic corollaries**.

**Core insight**: But beware **false generalization** — abstraction for abstraction's sake that adds complexity without eliminating any special cases. The criterion for true Grothendieck-style generalization: **after abstraction, did the special-case code actually disappear?** If it just "moved elsewhere", that's false abstraction.

**10. Base Change**

The behavioral variation of the same structure across different "bases" should be unified by a **base change functor**, not N copies of divergent code.

**Core insight**: Environment, platform, or dependency variations should be abstracted as base change functors. Identify places where environmental differences cause code branching to膨胀, and propose explicitly parameterizing the "base."

**11. Yoneda Perspective**

Yoneda lemma (roughly): **an object is completely determined by "all morphisms pointing to it"** — i.e., "how it's used" completely determines "what it is."

**Core insight**: APIs should not be designed from the implementer's perspective. They should be **reverse-engineered from caller usage patterns**. Find APIs designed from "implementer self-indulgence" that cause extreme pain for "callers", and reverse-engineer their true abstraction boundaries from usage patterns.

> **Meta-principle**: These 11 principles are not a checklist, but **thinking prisms**. The same code viewed through different prisms reveals different problems. For key architectural points, use **multi-prism cross-illumination**.

---

## Part 2: Suggested Analysis Rhythm (Flexible)

- **Survey before deconstructing**: Roughly map module/call graphs, then annotate problem points on the graph.
- **Evidence before assertion**: Each optimization suggestion should reference specific file/class/method paths.
- **Counterexamples before generalization**: Before proposing a general solution, ask "under what conditions would this fail?"
- **Combine large and small slices**: Provide both long-term vision (foundation rebuild) and immediately verifiable最小 slices.
- **Self-assessment at the end**: Honestly list blind spots and uncertainties in the analysis.

---

## Part 3: Anti-Goals (What NOT to Produce)

- Unsupported vague assertions
- Pure academic abstraction disconnected from business scenarios
- "Silver bullet" suggestions未经 counterexample检验
- Criticism that only指出 problems without any落地 path
- Disguising "moved special cases" as "generalization"

---

## Part 4: HTML Report Specification

### Visual & Layout

- **Dark theme by default** (background `#1a1a1a` or similar, soft foreground, avoid pure black/white contrast)
- Modern typography: clear hierarchy, comfortable line-height (1.6+), reasonable whitespace
- Key content presented as **cards** with subtle borders/shadows
- **High-contrast color badges** (danger red, optimization green, concept blue) for important attributes
- **Multi-column tables** for multi-dimensional comparison
- Mermaid.js Integration (CRITICAL):
  The HTML <head> MUST include the following script to render topology diagrams:

  <script type="module">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs'; mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>

### Report Structure

- **Sticky TOC** (left or right side), auto-highlights current section on scroll (IntersectionObserver)
- **Opening: Global Overview Matrix** — Use CSS Grid or inline SVG to draw a **[Benefit × Refactoring Cost] 2×2 matrix** (scatter plot concept), plotting all optimization suggestions
- **Core: Detailed Suggestion Cards** — Each suggestion is an independent block containing:
  - Quantized badges: `Difficulty⚙️` `Benefit📈` `Risk⚠️` `Confidence🎯`
  - **Grothendieck principle traceability badge** (which of the 11 principles it's based on)
  - **"Current vs Improved" dual-column comparison card** (red left, green right)
  - Long code sketches wrapped in `<details>` collapsible sections
  - Topological Evolution Diagrams (Inside the comparison card): You MUST generate two Mermaid.js graphs (using `graph TD` or `LR` inside `<div class="mermaid">` tags) to visually demonstrate the architecture's shape.
    - 'Current Topology' (Left/Red): Visually depict the "bad shape" (e.g., spaghetti coupling, M×N cross-connections, missing abstraction). Use red stroke/color for problematic links.
    - 'Elevated Topology' (Right/Green): Visually depict the Grothendieck "elegant shape" (e.g., funneling through a Functor, strict layer Sheaves, clear Base Change parameterization). Use thicker/green lines for the new clean pathways. Long code sketches wrapped in <details> collapsible sections

### Interactive Review System (Must implement in vanilla JS)

1. **At the bottom of each suggestion card, render:**
   - A `<textarea>` for review comments
   - A **5-star rating widget** for acceptance scoring (1-5 stars)
   - **Status tag selector**: `[Agree] [Doubtful] [Already Exists / False Positive] [Not Applicable to Business]`
   - All persisted with `localStorage`, survives page refresh
   - Topology Zoom/Lightbox Feature: Add simple JS so clicking any rendered Mermaid diagram expands it to full screen (or a large modal) for easy viewing.
2. **Export Feedback FAB**: Fixed floating button in bottom-right corner "Export Feedback"
   - On click, JS must execute the following:
     1. Iterate over all cards with feedback and concatenate their title/rating/tag/text into a formatted Markdown string.
     2. IMPORTANT: Append the following exact text at the very end of the generated Markdown string:
   
        "[Next Action Directive] Temporarily set aside Grothendieck's purely abstract perspective and return to the pragmatic engineering perspective of a frontline senior architect. Based on my review feedback above, please comprehensively evaluate these refactoring directions considering their 'short, medium, and long-term ROI', 'implementation risks and costs', and 'architectural impact on existing business'. Help me identify the most practical and cost-effective entry points for implementation. Once a smooth transitional refactoring plan is formulated, please proceed directly to executing the concrete code modifications."
     3. Write the final concatenated string to the clipboard using navigator.clipboard.writeText.
   - Show native `alert` or friendly Toast: "Copied successfully, can paste directly to AI for next deep-dive round"
3. **TOC scroll linkage**: Current section highlighted in TOC

### Delivery

- After generating HTML, **auto-open in Chrome**:
  - macOS: `open -a "Google Chrome" <path>`
  - Linux: `google-chrome <path>`
  - Windows: `start chrome <path>`

---

## Execution Flow

1. Explore the target codebase structure (use Glob, Grep, Read)
2. Build a mental model of the module/call graph
3. Apply each of the 11 Grothendieck principles systematically
4. For each finding: gather evidence (file paths, code snippets), assess impact, trace to principles
5. Generate the complete HTML report following the spec above
6. Write the HTML to a temp file and open in Chrome
7. Inform the user the report is ready for interactive review
