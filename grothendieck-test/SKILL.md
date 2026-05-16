---
name: grothendieck-test
description: >
  [TEST] Enhanced architecture analysis with Multi-Pass deep analysis, Motive Discovery protocol,
  and Grammar Invention. Uses Grothendieck's mathematical thinking framework to not just analyze
  but RECONSTRUCT architectural foundations.
  Produces a comprehensive HTML report with interactive review system.
  Use this skill whenever the user mentions architecture review, codebase analysis, system design evaluation,
  refactoring strategy, technical debt assessment, or wants to find non-incremental optimization opportunities
  in a codebase. Also trigger when the user asks "how to improve this project's architecture",
  "find major refactoring opportunities", or any request to deeply analyze a system's design quality.
  Even if the user just says "analyze this codebase" or "review the architecture", use this skill.
---

# Grothendieck Architecture Analysis (Enhanced)

Perform a comprehensive, exhaustive architectural analysis of the target project using **Grothendieck's mathematical thinking system**. The goal is not just to find problems, but to **discover the deeper structure** hidden beneath surface symptoms, then **reconstruct the foundation** so that many problems dissolve naturally. Do NOT modify any code — only produce analysis.

The final deliverable is an **HTML report** that opens automatically in the browser.

## Invocation

When the user invokes this skill:
1. Ask which codebase/directory to analyze (if not already specified)
2. **Determine the "Base Scheme"** — ask or infer the contextual parameters over which the analysis is relative:
   - **Team Scale**: Individual → Small team → Large org
   - **Codebase Maturity**: Prototype → Growth → Mature → Legacy
   - **Risk Tolerance**: High → Medium → Low
   - **Business Velocity**: Rapid iteration → Stable maintenance
   These parameters will shape ALL subsequent analysis — the same codebase under different bases yields different conclusions.
3. Explore the project structure to understand the codebase
4. Perform the full Grothendieck analysis (Multi-Pass, see Part 2)
5. Generate the HTML report
6. Open it in Chrome automatically

---

## Part 1: Analysis Methodology — Grothendieck's Thinking System

Grothendieck reshaped algebraic geometry through a universal methodology: **"make hard problems disappear by rebuilding the foundation."** The following 12 principles form an **organic whole**: the first 4 provide direction (how to see), the next 7 provide tools (how to act), and the 12th is the **generative principle** — it changes the language you use to describe the system itself.

For every finding, ask: **What would Grothendieck see here?**

### A. Philosophical Attitudes — Determining "What You See"

**1. The Rising Sea — Reject Local Hacks**

Facing a hard problem, ordinary engineers reach for hammers (patches, if/else, try/catch). Grothendieck's approach is to **raise the water level**: keep elevating the abstraction layer until the problem is naturally dissolved.

**Core insight**: When you find yourself "wrestling with code" — excessive special cases, unending bugs, everything coupled — this is a signal: **the abstraction level is too low**. The correct response is not to hack harder, but to **step back, elevate the abstraction dimension, and let the sea drown them**.

**Operational method** (how to actually raise the water level):
1. Identify the cluster of related problems and special cases
2. Ask: "At what abstraction level would these distinctions become irrelevant?"
3. Sketch that abstraction level — what are its primitives? What does it take for granted?
4. Verify: if this abstraction existed, would the original problems still require explicit handling?
5. If yes → go one level higher. If no → you found the right level.

**2. Finding Absolute Motives — Converge Polymorphic Appearances**

The same underlying thing appears in completely different "forms" across different contexts. Grothendieck's "motive" concept: cohomology, ℓ-adic cohomology, de Rham cohomology — these seemingly different theories are **projections of the same thing**.

**Core insight**: When you see N modules/state structures/data types that look "similar but different", don't just extract a common base class (that's syntax-level abstraction). Ask: **what deeper thing are they projections of?** Find that motive, and N appearances unify automatically.

**2.5. Motive Discovery Protocol — Operational Method (CRITICAL)**

This is NOT a high-level principle — it is a concrete, executable protocol. Before applying any other principles to specific findings, first perform a systematic Motive Discovery pass across the entire codebase:

**Step 1: Extract Structural Signatures**
Scan every module, data structure, state machine, and API surface. For each, extract its **structural signature** — a description that deliberately ignores naming:
- What shape does it have? (tree, graph, pipeline, state-machine, key-value, queue, observer...)
- What are its inputs and outputs? (types, cardinality, direction)
- What invariants does it appear to maintain?
- What other structures does it reference?

**Step 2: Cluster by Structural Signature**
Group entities by structural similarity, NOT by naming similarity. Two classes named `UserManager` and `OrderProcessor` may be the same motive if both are: "receives event → validates → delegates to handler → emits result". Two modules both named `*Service` may be completely different motives.

**Step 3: Name the Underlying Thing**
For each cluster, answer: **"these are all projections of WHAT?"** Invent a name for the underlying thing. The name should capture its essential nature, not what it happens to be used for in any specific case.

Example: if you find 5 modules that all follow the pattern "receive input → transform → validate → persist → notify", the motive might be **"Staged Transaction Pipeline"** — the fact that one handles users and another handles orders is just a projection onto different domains.

**Step 4: Validate the Motive**
Test your candidate motive name against every member of the cluster:
- Does the motive explain WHY each variant has the structure it has?
- Are the differences between variants EXPLAINABLE as projections? (different domains, different constraints)
- Are there any variants that DON'T fit? If so, either adjust the motive or split the cluster.

**Step 5: Assign a Mathematical Category**
Classify each discovered motive into its mathematical nature. This categorization will guide the reconstruction:
- **Set-like**: CRUD entities, repositories, collections
- **Graph-like**: Dependency trees, routing, relationships, hierarchies
- **Transform-like**: Functions, mappings, pipelines, converters
- **State-machine-like**: Workflows, lifecycles, status transitions
- **Sheaf-like**: Locally-consistent data that glues together globally
- **Functor-like**: Structure-preserving mappings between categories

**Output of Motive Discovery**: A catalog of discovered motives, each with: name, definition, member count, code locations, mathematical category. This catalog becomes the FOUNDATION for all subsequent analysis — every Grothendieck principle will be applied relative to these discovered motives.

**3. Eliminate Artificial Boundaries — Melt Isolated Islands**

Most system coupling comes not from "functional complexity" but from **lines developers drew for convenience**: package boundaries, module boundaries, layer boundaries, process boundaries. Once drawn wrong, all subsequent code must spend effort **crossing these boundaries**, generating glue, adapters, conversion layers.

**Core insight**: Good boundaries should be **natural seams of the thing itself**, not arbitrary cuts. Ask: **if this line didn't exist, would the system be simpler or messier?** If simpler, the line is wrong.

**Operational method**:
1. Map every boundary in the system (package, module, layer, process)
2. For each boundary, quantify the "boundary tax": how many adapters, converters, facades, and glue classes exist solely to cross it?
3. Boundary tax > 20% of the code on either side → the boundary is likely artificial and should be reconsidered

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

**Core insight**: Environment, platform, or dependency variations should be abstracted as base change functors. Identify places where environmental differences cause code branching to proliferate, and propose explicitly parameterizing the "base."

**11. Yoneda Perspective**

Yoneda lemma (roughly): **an object is completely determined by "all morphisms pointing to it"** — i.e., "how it's used" completely determines "what it is."

**Core insight**: APIs should not be designed from the implementer's perspective. They should be **reverse-engineered from caller usage patterns**. Find APIs designed from "implementer self-indulgence" that cause extreme pain for "callers", and reverse-engineer their true abstraction boundaries from usage patterns.

### C. The Generative Principle — Changing the Language

**12. Grammar Invention — Create New Concepts**

Grothendieck didn't just solve problems in algebraic geometry — he **invented a new language** (schemes, topoi, motives, étale cohomology) that made the old problems unaskable. Before him, no one had the concept of a "scheme"; after him, algebraic geometry was unthinkable without it.

**Core insight**: When you find yourself using the same few words ("service", "manager", "handler", "controller", "util") to describe fundamentally different things, the language is too poor to capture the architecture's actual structure. Good architecture requires **good names** — and sometimes the right names don't exist yet.

**Grammar Invention Protocol**:

1. **Identify unnamed concepts**: During Motive Discovery and cross-illumination, note structures that lack a precise, agreed-upon name in the codebase. These are things developers describe with long phrases ("the thing that takes the request and figures out which downstream services to call") or overloaded terms ("the handler").

2. **Invent new terms**: For each unnamed concept, invent a precise term. Criteria for a good term:
   - It captures the ESSENCE, not the implementation
   - It distinguishes this concept from all others in the codebase
   - It is short enough to use in conversation (1-3 words)
   - It suggests the right analogies (mathematical, physical, or domain-specific)

3. **Write definitions**: Each new term gets a formal one-sentence definition. The definition should allow someone to decide, for any piece of code, whether it IS or IS NOT an instance of this concept.

4. **Build a Concept Lexicon**: Assemble all invented terms + all discovered motives into a single "Concept Lexicon." This is a dictionary translating between:
   - **Current terms** (what the codebase calls it now — often inconsistent)
   - **Proposed terms** (the precise, invented vocabulary)
   - **Definition** (what distinguishes this concept)
   - **Structural signature** (the motive pattern it embodies)

5. **Re-describe the system**: Take one or two key architectural areas and re-describe them using ONLY the new vocabulary. If the description is significantly simpler and more precise than the original, the grammar invention is successful.

**The test of good grammar**: After introducing the new concepts, can a newcomer understand the architecture's essential structure in 10 minutes? If the old vocabulary required weeks of onboarding, and the new vocabulary enables rapid comprehension, you've achieved a genuine "grammar change."

> **Meta-principle**: These 12 principles are not a checklist, but **thinking prisms**. The same code viewed through different prisms reveals different problems. For key architectural points, use **multi-prism cross-illumination** — at least 3 principles must converge on each Major Finding. The interaction between principles is as important as the principles themselves.

---

## Part 2: Multi-Pass Deep Analysis (CRITICAL — Follow This Structure)

The analysis is NOT a linear scan through principles. It is a **5-Pass structure** where each pass deepens and refines the previous one. Early passes are broad and exhaustive; later passes are focused on the most critical findings.

### Pass 1: Territory Mapping

**Goal**: Build a comprehensive map of the codebase's structure. No judgment yet — just observation.

**Method**:
- Map the module/call graph: what depends on what?
- Trace data-flow paths end-to-end for 2-3 key user scenarios
- Identify all external boundaries (APIs, databases, services, filesystem)
- Count: modules, files, classes, interfaces, significant functions
- Note surface-level symptoms: large files, deep inheritance, many dependencies, frequent change hotspots

**Output**: A module dependency graph (use Mermaid in your mental model), a list of surface symptoms, and a rough size/complexity heatmap.

**Duration guidance**: ~20% of total analysis effort.

### Pass 2: Motive Discovery

**Goal**: Find the deeper structural patterns beneath surface differences. This is the CRITICAL pass — it provides the foundation for everything that follows.

**Method**: Execute the full **Motive Discovery Protocol** (Part 1, Section 2.5):
1. Extract structural signatures (ignore naming)
2. Cluster by structural similarity
3. Name the underlying thing (the "motive")
4. Validate against all cluster members
5. Assign mathematical categories

**Output**: A **Motive Catalog** listing every discovered motive with name, definition, member count, locations, and category.

**Duration guidance**: ~25% of total analysis effort. This is the most important pass — do not rush it.

### Pass 3: Cross-Illumination

**Goal**: Apply multiple Grothendieck principles simultaneously to each Major Finding. The interaction between principles reveals what any single principle misses.

**Method**:
- Select the top 5-8 most significant findings from Pass 1+2
- For EACH Major Finding, view it through at least 3 different principles. Example combinations:
  - Finding: "5 modules each have their own validation logic" → Rising Sea + Motive + Functoriality
  - Finding: "Every new feature requires changes in 8+ files" → Artificial Boundaries + Sheaf + Base Change
  - Finding: "The API was designed around internal implementation" → Yoneda + Universal Property + Grammar Invention
- For each combination, ask: "What does Principle A reveal that Principle B misses? And what does their INTERSECTION reveal?"
- Document the interplay — the most profound insights come from the tension between principles

**Output**: A set of Cross-Illuminated Findings, each with ≥3 principle perspectives and their interactions documented.

**Duration guidance**: ~25% of total analysis effort.

### Pass 4: Root Cause Synthesis

**Goal**: Trace all findings and symptoms back to a SMALL NUMBER of fundamental architectural errors. The 15 problems you found are manifestations of 2-3 wrong foundational choices.

**Method**:
- Take all findings from Pass 2 (motives) and Pass 3 (cross-illuminated findings)
- Build a causal graph: which findings are root causes, and which are downstream symptoms?
- Ask: "If we fixed THIS one thing, how many other problems would dissolve naturally?"
- Iteratively prune the causal graph until you arrive at the 2-4 most fundamental issues
- For each root cause, identify: what was the original design decision that led here? What was the (possibly reasonable) assumption that turned out to be wrong?

**Output**: A Root Cause Map showing 2-4 fundamental issues, each with its causal downstream effects, and the original design assumption that created it.

**Duration guidance**: ~15% of total analysis effort.

### Pass 5: Reconstruction Design

**Goal**: Design what the architecture SHOULD look like — the elevated foundation that dissolves the root causes.

**Method**:
- **Rising Sea elevation**: For each root cause, find the abstraction level where it naturally dissolves
- **Motive-based redesign**: Redraw the architecture around the discovered motives — each motive becomes a first-class architectural element
- **Grammar Invention**: Execute the full Grammar Invention Protocol (Part 1, Section C). Create the new vocabulary that makes the redesigned architecture simple to describe.
- **Sheaf gluing**: Design the local consistency conditions that allow components to compose without central coordination
- **Base parameterization**: Explicitly parameterize the parts that vary across environments/platforms/contexts
- Draw the "Elevated Topology" — the new architecture diagram showing how components relate

**Output**: A Reconstruction Blueprint containing: the elevated topology diagram, the Concept Lexicon, a Redesign Rationale (why this design dissolves the root causes), and a Migration Pathway (how to get from here to there in concrete steps).

**Duration guidance**: ~15% of total analysis effort.

---

## Part 3: Anti-Goals (What NOT to Produce)

- Unsupported vague assertions
- Pure academic abstraction disconnected from business scenarios
- "Silver bullet" suggestions not tested against counterexamples
- Criticism that only identifies problems without any actionable path
- Disguising "moved special cases" as "generalization"
- A list of 20 independent problems without a Root Cause synthesis
- New terminology that is more confusing than the original (Grammar Invention must SIMPLIFY)
- Motives that are just renamed common base classes (true motives capture deeper structure)

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

  <script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    themeVariables: {
      fontSize: '16px',
      primaryColor: '#334155',
      primaryTextColor: '#e2e8f0',
      primaryBorderColor: '#64748b',
      lineColor: '#94a3b8',
      secondaryColor: '#1e293b',
      tertiaryColor: '#334155',
      nodeBorder: '#64748b',
      clusterBkg: '#1e293b',
      clusterBorder: '#475569',
      titleColor: '#e2e8f0',
      edgeLabelBackground: '#1e293b'
    }
  });
  </script>

### Report Structure

- **Sticky TOC** (left or right side), auto-highlights current section on scroll (IntersectionObserver)
- **Opening: Base Parameters & Global Overview**:
  - Display the "Base Scheme" parameters (Team Scale, Maturity, Risk Tolerance, Velocity) as metric badges
  - Use CSS Grid or inline SVG to draw a **[Benefit × Refactoring Cost] 2×2 matrix** (scatter plot concept), plotting all optimization suggestions
  - Color-code points by which root cause they trace to
- **Section 1: Territory Map** — Module dependency graph (Mermaid), size/complexity heatmap, surface symptoms table
- **Section 2: Motive Catalog** (NEW — CRITICAL) — For each discovered motive:
  - Name, definition, mathematical category badge, member count, key locations
  - Mermaid diagram showing the motive's structural signature
  - A "Current vs. If Unified" comparison: what happens if this motive is recognized as a first-class concept?
- **Section 3: Cross-Illuminated Findings** — Each Major Finding as a detailed suggestion card containing:
  - Quantized badges: `Difficulty⚙️` `Benefit📈` `Risk⚠️` `Confidence🎯`
  - **Grothendieck principle traceability badge** — which principles were cross-illuminated (at least 3)
  - **"Current vs Improved" dual-column comparison card** (red left, green right)
  - Long code sketches wrapped in `<details>` collapsible sections
  - **Topological Evolution Diagrams** — Current Topology (red) vs Elevated Topology (green)
- **Section 4: Root Cause Map** — Causal graph (Mermaid flowchart) showing how 2-4 root causes cascade into all symptoms. Each root cause labeled with the original design assumption.
- **Section 5: Reconstruction Blueprint** — The elevated architecture:
  - Elevated Topology diagram (full-width Mermaid)
  - **Concept Lexicon** (NEW — CRITICAL): A table mapping Current Terms → Proposed Terms → Definition → Motive Pattern. This is the "grammar change" made concrete.
  - Redesign Rationale: for each root cause, explain why the new design dissolves it
  - **Rising Sea Elevation Map** (NEW): A Mermaid diagram or table showing: Current Abstraction Level → Problem → Elevated Abstraction Level → Why It Dissolves
- **Section 6: Research Directions** (NEW) — Open questions and conjectures:
  - "Open Problems": what we DON'T yet know about this architecture
  - "If We Changed X...": thought experiments exploring hypothetical reconstruction paths
  - "Next Investigation": what to look at next, what evidence is still missing
  - This section explicitly positions the analysis as the START of a research program, not its conclusion
- **Self-Assessment**: Honestly list blind spots, uncertainties, and limitations of the analysis

### Topological Evolution Diagrams (CRITICAL)

Each Major Finding card (Section 3) and the Reconstruction Blueprint (Section 5) MUST include topology diagrams rendered as Mermaid.js graphs. Follow these specifications exactly:

- You MUST generate two Mermaid.js graphs to visually demonstrate the architecture's shape.
- Place them in a dedicated `<div class="topology-compare">` that spans the full card width.
- Each diagram gets its own `<div class="topology-diagram">` with a label (`Current Topology` / `Elevated Topology`).
- **Sizing (IMPORTANT)**: Each `.topology-diagram .mermaid` container MUST have `min-height: 380px` and `width: 100%`. Do NOT add `%%{init:...}%%` blocks to individual Mermaid diagrams — the global `<script>` initialization in `<head>` already sets `theme: 'dark'` and all `themeVariables` (fontSize, colors). Adding a local init overrides the global dark theme without declaring `theme`, causing Mermaid to fall back to light theme defaults while text remains light-colored, making labels invisible. Never let Mermaid diagrams render at the tiny default size — they must be large enough that node labels and edge annotations are clearly legible.
- 'Current Topology' (Red): Visually depict the "bad shape" (e.g., spaghetti coupling, M×N cross-connections, missing abstraction). Use red-tinted borders and red stroke colors for problematic links.
- 'Elevated Topology' (Green): Visually depict the Grothendieck "elegant shape" (e.g., funneling through a Functor, strict layer Sheaves, clear Base Change parameterization). Use green-tinted borders and thicker/green lines for the new clean pathways.
- **Lightbox Zoom**: Clicking any topology diagram opens it in a full-screen lightbox overlay (dark backdrop, centered image, close on click/ESC). This is mandatory — the inline diagram provides the overview, the lightbox provides the detailed inspection.
- Required CSS for diagrams:
  ```css
  /* Topology diagram theme variables (dark by default, light mode override) */
  :root {
    --topo-bg: #1a1a1a;
    --topo-current-label-bg: rgba(248,81,73,0.15);
    --topo-current-label-color: #f85149;
    --topo-current-border: rgba(248,81,73,0.2);
    --topo-elevated-label-bg: rgba(63,185,80,0.15);
    --topo-elevated-label-color: #3fb950;
    --topo-elevated-border: rgba(63,185,80,0.2);
    --lb-backdrop: rgba(0,0,0,0.85);
    --lb-content-bg: #1a1a1a;
  }
  @media (prefers-color-scheme: light) {
    :root {
      --topo-bg: #f0f0f0;
      --topo-current-label-bg: rgba(220,53,69,0.1);
      --topo-current-label-color: #dc3545;
      --topo-current-border: rgba(220,53,69,0.15);
      --topo-elevated-label-bg: rgba(25,135,84,0.1);
      --topo-elevated-label-color: #198754;
      --topo-elevated-border: rgba(25,135,84,0.15);
      --lb-backdrop: rgba(255,255,255,0.92);
      --lb-content-bg: #ffffff;
    }
  }
  .topology-compare { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 24px; }
  .topology-diagram { flex: 1; min-width: 340px; }
  .topology-diagram .mermaid { min-height: 380px; width: 100%; background: var(--topo-bg); }
  .topology-diagram .label { font-size: 14px; font-weight: 600; margin-bottom: 8px; padding: 4px 12px; border-radius: 4px; display: inline-block; }
  .topology-diagram.current .label { background: var(--topo-current-label-bg); color: var(--topo-current-label-color); }
  .topology-diagram.current .mermaid { border: 2px solid var(--topo-current-border); border-radius: 8px; padding: 16px; }
  .topology-diagram.elevated .label { background: var(--topo-elevated-label-bg); color: var(--topo-elevated-label-color); }
  .topology-diagram.elevated .mermaid { border: 2px solid var(--topo-elevated-border); border-radius: 8px; padding: 16px; }
  /* Lightbox */
  .lightbox { display: none; position: fixed; inset: 0; z-index: 9999; background: var(--lb-backdrop); cursor: pointer; }
  .lightbox.active { display: flex; align-items: center; justify-content: center; }
  .lightbox .mermaid { min-width: 700px; min-height: 500px; background: var(--lb-content-bg); border-radius: 8px; padding: 24px; }
  ```

- Required JS for lightbox:
  ```javascript
  // Lightbox: click any topology diagram to zoom full-screen
  document.querySelectorAll('.topology-diagram').forEach(diagram => {
    diagram.style.cursor = 'pointer';
    diagram.addEventListener('click', () => {
      const svg = diagram.querySelector('.mermaid svg').cloneNode(true);
      const lb = document.createElement('div');
      lb.className = 'lightbox active';
      const wrapper = document.createElement('div');
      wrapper.className = 'mermaid';
      wrapper.style.cssText = 'min-width:700px;min-height:500px;';
      wrapper.appendChild(svg);
      lb.appendChild(wrapper);
      document.body.appendChild(lb);
      const close = () => { lb.remove(); };
      lb.addEventListener('click', close);
      document.addEventListener('keydown', function onEsc(e) {
        if (e.key === 'Escape') { close(); document.removeEventListener('keydown', onEsc); }
      });
    });
  });
  ```

### Interactive Review System (Must implement in vanilla JS)

1. **At the bottom of each suggestion card (Section 3), render:**
   - A `<textarea>` for review comments
   - A **5-star rating widget** for acceptance scoring (1-5 stars)
   - **Status tag selector**: `[Agree] [Doubtful] [Already Exists / False Positive] [Not Applicable to Business]`
   - All persisted with `localStorage`, survives page refresh
   - **Topology Zoom/Lightbox** (MANDATORY): Every Mermaid diagram MUST be clickable to open a full-screen lightbox for detailed inspection. Implementation:
     - On page load, wrap each `.mermaid` element's parent `.topology-diagram` with a click handler.
     - When clicked: clone the inner SVG into a `.lightbox` div, add `.active` class, append to `<body>`.
     - The lightbox centers the diagram at large size (min 700x500px) on an opaque dark backdrop.
     - Click the backdrop or press ESC to close and remove the lightbox element.
     - This is essential — the inline diagram shows the big picture, the lightbox lets you read every label.
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

1. Determine the Base Scheme parameters (ask or infer)
2. Explore the target codebase structure (use Glob, Grep, Read) — **Pass 1: Territory Mapping**
3. Execute systematic Motive Discovery across the entire codebase — **Pass 2**
4. Select top 5-8 Major Findings and cross-illuminate each with ≥3 principles — **Pass 3**
5. Build causal graph, trace all findings to 2-4 root causes — **Pass 4**
6. Design the elevated architecture: Rising Sea elevation, Motive-based redesign, Grammar Invention — **Pass 5**
7. Assemble all findings into the complete HTML report following the spec above (7 sections)
8. Write the HTML to a temp file and open in Chrome
9. Inform the user the report is ready for interactive review

## Critical Rules

- **No `%%{init}%%` in individual Mermaid diagrams** — the global `<script>` initialization already sets `theme: 'dark'` and all `themeVariables`. Adding a local init overrides the global dark theme, causing Mermaid to fall back to light defaults with light text, making labels invisible.
- **Each Major Finding MUST reference specific file/class/method paths** — no vague assertions
- **Motive Discovery MUST be exhaustive** — scan the entire codebase, not just a few files
- **Grammar Invention MUST produce names that are SIMPLER than what they replace** — if the new vocabulary is more confusing, it's false abstraction
- **The Root Cause Map MUST converge to ≤4 root causes** — if you have more than 4, you haven't found the real roots yet
