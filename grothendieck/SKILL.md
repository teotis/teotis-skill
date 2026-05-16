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

**Core insight**: When you find yourself "wrestling with code" — excessive special cases, unending bugs, everything coupled — this is a signal: **the abstraction level is too low**. The correct response is not to hack harder, but to **step back, elevate the abstraction dimension, and let the sea drown them**.

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

**Core insight**: Environment, platform, or dependency variations should be abstracted as base change functors. Identify places where environmental differences cause code branching to proliferate, and propose explicitly parameterizing the "base."

**11. Yoneda Perspective**

Yoneda lemma (roughly): **an object is completely determined by "all morphisms pointing to it"** — i.e., "how it's used" completely determines "what it is."

**Core insight**: APIs should not be designed from the implementer's perspective. They should be **reverse-engineered from caller usage patterns**. Find APIs designed from "implementer self-indulgence" that cause extreme pain for "callers", and reverse-engineer their true abstraction boundaries from usage patterns.

> **Meta-principle**: These 11 principles are not a checklist, but **thinking prisms**. The same code viewed through different prisms reveals different problems. For key architectural points, use **multi-prism cross-illumination**.

---

## Part 2: Suggested Analysis Rhythm (Flexible)

- **Survey before deconstructing**: Roughly map module/call graphs, then annotate problem points on the graph.
- **Evidence before assertion**: Each optimization suggestion should reference specific file/class/method paths.
- **Counterexamples before generalization**: Before proposing a general solution, ask "under what conditions would this fail?"
- **Combine large and small slices**: Provide both long-term vision (foundation rebuild) and immediately verifiable minimal slices.
- **Self-assessment at the end**: Honestly list blind spots and uncertainties in the analysis.

---

## Part 3: Anti-Goals (What NOT to Produce)

- Unsupported vague assertions
- Pure academic abstraction disconnected from business scenarios
- "Silver bullet" suggestions not tested against counterexamples
- Criticism that only identifies problems without any actionable path
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

  <script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    themeVariables: {
      fontSize: '16px',
      primaryColor: '#2d3748',
      primaryTextColor: '#e2e8f0',
      primaryBorderColor: '#4a5568',
      lineColor: '#718096',
      secondaryColor: '#1a202c',
      tertiaryColor: '#2d3748',
      nodeBorder: '#4a5568',
      clusterBkg: '#1a202c',
      clusterBorder: '#4a5568',
      titleColor: '#e2e8f0',
      edgeLabelBackground: '#1a202c'
    }
  });
  </script>

### Report Structure

- **Sticky TOC** (left or right side), auto-highlights current section on scroll (IntersectionObserver)
- **Opening: Global Overview Matrix** — Use CSS Grid or inline SVG to draw a **[Benefit × Refactoring Cost] 2×2 matrix** (scatter plot concept), plotting all optimization suggestions
- **Core: Detailed Suggestion Cards** — Each suggestion is an independent block containing:
  - Quantized badges: `Difficulty⚙️` `Benefit📈` `Risk⚠️` `Confidence🎯`
  - **Grothendieck principle traceability badge** (which of the 11 principles it's based on)
  - **"Current vs Improved" dual-column comparison card** (red left, green right)
  - Long code sketches wrapped in `<details>` collapsible sections
  - **Topological Evolution Diagrams** (CRITICAL — render full-width BELOW the comparison card, NOT inside the cramped 2-column grid):
    - You MUST generate two Mermaid.js graphs to visually demonstrate the architecture's shape.
    - Place them in a dedicated `<div class="topology-compare">` that spans the full card width.
    - Each diagram gets its own `<div class="topology-diagram">` with a label (`Current Topology` / `Elevated Topology`).
    - **Sizing (IMPORTANT)**: Each `.topology-diagram .mermaid` container MUST have `min-height: 380px` and `width: 100%`. Use `%%{init: {'themeVariables': { 'fontSize': '16px', 'primaryColor': '#2d3748', 'primaryTextColor': '#e2e8f0', 'primaryBorderColor': '#4a5568', 'lineColor': '#718096', 'nodeBorder': '#4a5568' }}}%%` in Mermaid to ensure readable text and dark-background-compatible node colors. Never let Mermaid diagrams render at the tiny default size — they must be large enough that node labels and edge annotations are clearly legible.
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

1. **At the bottom of each suggestion card, render:**
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

1. Explore the target codebase structure (use Glob, Grep, Read)
2. Build a mental model of the module/call graph
3. Apply each of the 11 Grothendieck principles systematically
4. For each finding: gather evidence (file paths, code snippets), assess impact, trace to principles
5. Generate the complete HTML report following the spec above
6. Write the HTML to a temp file and open in Chrome
7. Inform the user the report is ready for interactive review
