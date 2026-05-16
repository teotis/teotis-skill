# Codex Skill Collection

A curated set of Claude Code skills for enhanced engineering workflows.

## Skills

### `html` — Visual Output Delivery

Transforms terminal-unfriendly task outputs (PDF, DOCX, PPT, images, markdown, long-form analysis) into self-contained, dark-themed HTML reports that open automatically in the browser. Supports two modes:

- **File Review Mode** — box/point annotation on rendered pages with coordinate-mapped feedback copy, powered by pointer events and localStorage persistence
- **Text Report Mode** — card-based layout with TOC navigation, decision panel (Accept/Consider/Reject), and structured feedback export

The highlight: turns the terminal's "read a wall of text or download a file" experience into an interactive visual review — annotations, star ratings, one-click feedback back to Claude.

### `grothendieck` — Architecture Deep Analysis

Applies Grothendieck's 11-principle mathematical thinking framework (Rising Sea, Absolute Motives, Functoriality, Sheaf Theory, Yoneda Perspective, etc.) to codebase architecture. Produces an interactive HTML report with:

- Benefit × Cost scatter matrix for all optimization suggestions
- Detailed suggestion cards with principle traceability badges and before/after topology diagrams (Mermaid.js)
- Full interactive review system with ratings, status tags, and structured feedback export

The highlight: finds **non-incremental** optimization opportunities — not "extract this method," but "the abstraction level is fundamentally wrong, and 40 special cases dissolve when you raise it."

### `skill-creator` — Build & Iterate on Skills (by Anthropic)

Created by Anthropic (Claude Code's parent company). An end-to-end toolkit for creating, testing, benchmarking, and optimizing Claude Code skills. Covers the full lifecycle:

- Draft SKILL.md with progressive disclosure (metadata → body → bundled resources)
- Parallel test runs (with-skill vs baseline) with quantitative assertion grading
- Browser-based eval viewer for side-by-side output comparison with feedback collection
- Blind A/B comparison for rigorous quality assessment
- Trigger description optimization via iterative eval loop

The highlight: a disciplined "draft → test → review → improve → repeat" loop with quantitative benchmarks, ensuring skills generalize beyond a few hand-picked examples.

---

## Structure

Each skill follows the standard layout:

```
skill-name/
├── SKILL.md          # YAML frontmatter + markdown instructions
├── scripts/          # Executable helpers (Python)
├── references/       # Design specs loaded on demand
└── assets/           # Templates and static resources
```
