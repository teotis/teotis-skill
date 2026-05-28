---
name: html-response
description: >
  用于将复杂回答、报告、计划、审查、对比、仪表盘、文档/图片/PDF 预览或结构化反馈转成更易阅读、审阅、比较和批注的自包含 HTML。
  每次输出较复杂内容时，都评估是否需要交互式 HTML 视图；简单回答仍保留在聊天中。
  Use for adaptive HTML response presentation, browser review, comparisons, feedback forms, visual material, and dense deliverables.
  Do not generate HTML for trivial acknowledgements, very short factual answers, or conversational exchanges unless the user asks for it.
---

# Adaptive HTML Response

## Mission

Transform an agent response into the **lowest-friction reading and feedback surface** appropriate to the task.
HTML is not decoration and not a mandatory duplicate of chat text. It is used when structure, visualization,
review, decision-making, annotation, or iterative feedback benefits from a browser-based surface.

This skill is capable of representing **any** response type. It must not blindly turn **every** response into an HTML file.
A two-sentence answer is usually easier to read in chat; a report, decision, plan, artifact review, or nuanced comparison is
usually easier to act on in adaptive HTML.

## Core Promise

Every generated HTML view must improve at least one of these outcomes:

1. **Orientation** — the user immediately knows the answer, state, or decision required.
2. **Comprehension** — the user reads less before understanding more.
3. **Inspection** — evidence, files, data, code, or diagrams are easier to examine.
4. **Actionability** — next actions, alternatives, and risks are easier to decide.
5. **Feedback** — the user can respond precisely without reconstructing context manually.

If none of the five improves, do not generate HTML unless explicitly requested.

---

## 1. Activation Policy: Universal Capability, Adaptive Use

Evaluate this skill for every substantive response. HTML generation is mandatory only when explicitly requested or when the
response is an artifact requiring visual review. Otherwise, silently score whether a view would help.

### 1.1 Mandatory Activation

Generate HTML when any of the following is true:

- The user asks for HTML, browser view, visual review, interactive review, an annotated preview, or a shareable report.
- The primary output is a visual/document artifact that needs review: PDF, DOCX/DOC, PPT/PPTX, image, rendered Markdown,
  layout-heavy file, or a mixed artifact plus explanatory report.
- The task-specific skill explicitly requires an HTML deliverable.

### 1.2 Adaptive Activation: Binary Decision

When 1.1 does not apply, ask two questions:

1. **Does the response need visual inspection?** Files, diagrams, charts, code diffs, topology, rendered pages, or layout review.
2. **Does the response need structured review?** Trade-offs with approvals, multi-step plans, multi-criterion evidence, or region-specific feedback.

Answer in chat only when both are false. Generate HTML when either is true and at least one of the five core outcomes (Orientation, Comprehension, Inspection, Actionability, Feedback) would clearly improve.

### 1.3 Anti-Overproduction Rule

Do **not** generate HTML merely because an answer is longer than an arbitrary character threshold. A long but simple answer can
remain readable in chat; a short but high-stakes comparison may benefit from a decision board.

Never mention the activation decision to the user.

---

## 2. Response Understanding Before Layout

Before generating HTML, derive a **comprehension contract**:

| Question | Required output |
|---|---|
| What does the user need to know first? | A one-screen conclusion or current state block |
| What can be hidden until needed? | Details/evidence placed in progressive disclosure sections |
| What is inspectable? | Evidence cards, files, code, charts, diagrams, citations, assumptions |
| What may the user disagree with? | Feedback controls attached to the relevant units |
| What action is expected next? | One explicit action zone; no silent action escalation |
| What is uncertain? | Visible uncertainty/assumption block, not buried in prose |

The opening viewport must deliver the answer or the review task, not an ornamental title page.

---

## 3. Presentation Modes

Choose one primary mode. Combine modes only when materially necessary.
Detailed structures are defined in `references/presentation_modes.md` (resolve relative to this SKILL.md).

| Mode | Use for | Primary feedback affordance |
|---|---|---|
| **Brief View** | Explicit HTML request for a short answer, status, confirmation, or definition | “Helpful / Need detail” plus comment |
| **Guided Explanation** | Educational explanations, summaries, research synthesis, policy/technical interpretation | Mark unclear section, ask follow-up, comment |
| **Decision Board** | Recommendations, alternatives, trade-offs, prioritization, approvals | Choose/accept/defer/reject each option with rationale |
| **Action Plan** | Roadmaps, migration sequences, checklists, project plans | Edit step, flag blocker, mark dependency, approve phase |
| **Evidence Dashboard** | Metrics, comparisons, evaluations, data-derived findings | Dispute evidence, request source/detail, rate confidence |
| **Technical Review** | Code review, architecture review, incident analysis, refactoring analysis | Comment per finding/code block/diagram; severity/status |
| **Artifact Review** | PDF, DOCX/PPT rendered pages, images, layout outputs | Point/region annotation plus structured export |
| **Mixed Workspace** | Artifact plus analysis or proposed changes | Shared annotations and decision cards |

A response about an error or troubleshooting procedure generally uses **Guided Explanation** or **Action Plan**, not a new visual style.

---

## 4. Content Shaping Principles

### 4.1 Answer First

The first screen contains, in this order when relevant:

1. concise answer / recommendation / task state;
2. critical caveat or blocker;
3. primary next action;
4. navigation to evidence or details.

### 4.2 Progressive Disclosure

- Keep essential conclusions visible.
- Place supporting evidence, alternatives, long code, complete tables, appendices, and raw logs in expandable sections.
- Do not hide safety warnings, material uncertainty, destructive impacts, deadlines, or decision-critical trade-offs.

### 4.3 Match Interaction to Task

Do not apply generic `Accept / Consider / Reject` buttons to every response. Feedback controls must reflect what the user is
actually reviewing: choosing, prioritizing, annotating, correcting, asking for explanation, or approving a phase.

### 4.4 Preserve Traceability

Every reviewable card receives a stable `data-item-id`, a title, a type, and optional source/evidence reference. Feedback exports
must preserve these IDs so the next agent turn can map comments to the correct content.

### 4.5 Chat Still Matters

When delivering HTML, provide a concise chat message with the conclusion, the HTML link/path, and one sentence describing how to
use the review controls. The HTML must not be the only place where a high-stakes conclusion appears.

---

## 5. Generation Pipeline

1. **Classify the response** using the activation policy and select the primary mode.
2. **Extract structure**: conclusion, sections, evidence, decisions, uncertainty, next actions, reviewable units.
3. **Choose packaging profile**:
   - `single-file-portable`: text, small images, compact artifacts; CSS/JS/data embedded inline.
   - `local-review-bundle`: large page-rendered artifacts or large datasets; HTML plus sibling asset/data files to avoid an unusably huge HTML file.
4. **Render semantic HTML** according to `references/html_system_spec.md` (resolve relative to this SKILL.md).
5. **Add mode-specific feedback** according to `references/feedback_spec.md`.
6. **Render artifact previews**, if needed, according to `references/artifact_review_spec.md`.
7. **Validate quality and safety** with `references/quality_checklist.md`; use `scripts/validate_html.py` when available.
8. **Open the local HTML** with `scripts/open_browser.py` when browser launch is appropriate and allowed by the execution environment.
9. **Deliver in chat** with a direct link/path and concise instructions for feedback export.

---

## 6. Packaging and Dependency Policy

### 6.1 Offline-First Default

Default output must work without network access. Inline the page CSS and the interaction JavaScript. Use local data/assets or
embedded data URLs according to the chosen packaging profile.

### 6.2 Diagram and External Asset Policy

Default output uses inline SVG or CSS-only diagrams for true offline use.

When a task-specific skill mandates Mermaid diagrams (e.g., abstraction-architect, renewal-architect, analyze-success), CDN-loaded Mermaid is permitted. In these cases:
- Mark the document as network-dependent with a visible note.
- Provide readable Mermaid source in `<pre>` blocks as a fallback in case CDN loading fails.
- The Mermaid global initialization block (from the calling skill) serves as the declaration that CDN is required.

Do not load fonts, syntax highlighters, or other CDN assets beyond what the calling skill's spec requires.

### 6.3 Portable vs Large Review Outputs

Embedding all rendered pages as base64 in one HTML file is useful for small documents but wasteful for large ones. By default:

- up to 12 rendered pages or approximately 20 MB embedded payload: `single-file-portable` is acceptable;
- beyond that: use `local-review-bundle`, lazy page loading, thumbnails, and a visible portability note;
- for very large artifacts, render an initial review subset or index and state what is not yet rendered.

Do not ask for confirmation merely because a file is large when an indexed or partial preview is sufficient to proceed.

---

## 7. Accessibility, Readability, and Interaction Requirements

Every HTML output must satisfy the following engineering requirements:

- Semantic landmarks: `<header>`, `<main>`, `<nav>`, `<section>`, `<aside>`, `<footer>` as appropriate.
- A descriptive `<title>`, correct `lang`, viewport metadata, visible page purpose, and meaningful heading order.
- Keyboard-operable controls; visible focus indicators; no feedback function dependent only on dragging.
- Provide button alternatives for region navigation/selection when annotation uses pointer gestures.
- Touch targets at least `24 × 24 CSS px`; prefer larger controls for primary actions.
- Text should be chunked, scannable, and use whitespace; avoid dense unbroken prose.
- Respect `prefers-reduced-motion`; animation must never be needed to understand content.
- Charts and diagrams must have a text summary or table alternative.
- Sticky controls must not obscure focused elements or critical content.
- Support narrow screens; switch side-by-side panels to stacked layouts below the configured breakpoint.
- Include print styles for reports and plans; suppress interactive chrome in printed output.

Do not claim formal accessibility conformance unless it has actually been tested. These are required implementation safeguards.

---

## 8. Safety and Data Handling

### 8.1 Safe Rendering

- Treat user-provided and tool-derived content as untrusted text unless deliberately authored HTML is required.
- Escape inserted text and attribute values; never concatenate untrusted input into executable script or raw HTML.
- Do not use `eval`, `new Function`, inline event attributes, or uncontrolled URL navigation.
- Prefer a restrictive Content Security Policy meta tag for standalone outputs; adjust only for declared bundled/online resources.
- Never silently embed credentials, tokens, hidden prompts, or sensitive raw source data that is unnecessary for review.

### 8.2 Feedback Storage and Export

- Store feedback locally only when useful, with a document-specific key and a visible “Clear feedback” action.
- `localStorage` operations must be protected by `try/catch` and fall back to in-memory state.
- Clipboard writes must occur only after a user action and provide a textarea/manual-copy fallback when clipboard access fails.
- Export both readable Markdown and structured JSON metadata when precise continuation is required.

### 8.3 No Execution Escalation

Exported feedback may request revision, deeper analysis, or a proposed action plan. It must **not** instruct the next agent to send,
delete, deploy, purchase, modify code, or alter user data without explicit user authorization.

---

## 9. File and Artifact Review

For PDF, document, slide, image, or layout-heavy output, use **Artifact Review** or **Mixed Workspace**.

- PDFs: render pages for precise annotation when feasible using `scripts/pdf_to_pages.py`.
- DOCX/DOC/PPT/PPTX: convert a review copy to PDF using `scripts/doc_to_pdf.py`, then render pages. Do not modify the source artifact merely to preview it.
- Images: embed directly or reference local sibling assets; support point/region annotations.
- Markdown or HTML drafts: render semantically; allow section-level comments rather than pixel-only annotations when possible.
- Large artifacts: prefer bundle packaging with lazy page loading and explicit page counts.

Detailed behavior is in `references/artifact_review_spec.md`.

---

## 10. Delivery Contract

When HTML is produced, the chat response should include:

- the main conclusion or the state of the requested task;
- a link/path to the generated HTML;
- the selected purpose, such as “review decisions”, “annotate pages”, or “compare options”;
- one instruction for exporting feedback back to the agent.

Do not merely say “opened in browser”; the user needs a durable link and enough context even when browser opening fails.

---

## 11. Reference Files

All paths below are relative to this SKILL.md file's directory. When reading or executing them, resolve against the skill directory, not the current working directory.

- `references/presentation_modes.md` — selection and structure of each response mode.
- `references/html_system_spec.md` — shared shell, layout, responsive, accessibility, offline, and security requirements.
- `references/feedback_spec.md` — interactive feedback model and export schema.
- `references/artifact_review_spec.md` — page/image review and annotation behavior.
- `references/quality_checklist.md` — final validation checklist.
- `scripts/pdf_to_pages.py` — PDF page rendering helper.
- `scripts/doc_to_pdf.py` — office document preview conversion helper.
- `scripts/open_browser.py` — local browser opening helper.
- `scripts/validate_html.py` — lightweight structural and safety checks for generated output.
- `templates/interactive_response_base.html` — accessible offline-first starting shell for interactive text/review modes.
- `references/dependencies.md` — external system and Python package dependencies required by scripts.
