---
name: html
description: >
  Automatically convert task output into HTML and open in the browser, solving the problem of poor readability
  and difficult interaction in terminal environments.
  Trigger this skill when task output is file-based (PDF, DOCX, DOC, PPT, PPTX, MD, images) or
  long-form text/analysis/reasoning/chart content, delivering results as visualized HTML.
  Trigger scenarios: user says "open with html", "generate html", "browser view", "html review";
  or the task produced a file (generated PDF/DOCX/PPT etc.) needing review;
  or the task produced long analysis text, architecture review, code analysis, data reports etc. needing visual presentation.
  Even if the user doesn't explicitly request HTML, proactively suggest using this skill when the output is complex
  (multi-page files, long analysis, multi-dimensional data).
---

# HTML Delivery Skill

Terminal environments are inherently ill-suited for reviewing visual output (PDF, DOCX, images) and reading long-form analysis text. The core idea of this skill:
after the task completes normally, additionally generate a self-contained HTML file and open it in the browser, giving the user a visual review experience.

## Output Classification

After completing the task, select a mode based on output type:

| Output Type | Mode | Key Features |
|-----------|------|---------|
| PDF, DOCX, DOC, PPT, PPTX | **File Review Mode** | Box/point annotation + coordinate mapping + feedback copy |
| Images (PNG, JPG, WEBP, SVG) | **File Review Mode** | Box/point annotation, no element mapping |
| Markdown (.md) | **File Review Mode** | Region annotation after HTML rendering |
| Long text (>500 chars), analysis reports | **Text Report Mode** | Dark theme + card layout + decision panel |
| Data tables, comparative analysis | **Text Report Mode** | Tables + metric panels + comparison cards |
| Code analysis, architecture review | **Text Report Mode** | Code highlighting + flow diagrams + TOC |
| Mixed (files + analysis) | **Dual Mode** | File preview + report side by side |

## Mode 1: File Review Mode

For scenarios requiring review of file outputs. Core capabilities: box/point annotation, smart annotation position recognition, one-click structured feedback copy.

### Workflow

1. **File Preprocessing** — Convert output to a browser-renderable format
2. **Generate Review HTML** — Generate self-contained HTML per `references/file_review_spec.md`
3. **Open Browser** — Open with `scripts/open_browser.py`
4. **Collect Feedback** — User pastes structured annotations back into the conversation via the "Copy Feedback" button

### File Preprocessing

Choose the preprocessing method based on file type:

**PDF files:**
```bash
python3 <skill-path>/scripts/pdf_to_pages.py <pdf_path> [--dpi 144] [--output <output.json>]
```
Output JSON: one base64 PNG data URL per page. Prefers pypdfium2, falls back to pdftoppm.

**DOCX/DOC/PPT/PPTX files:**
```bash
python3 <skill-path>/scripts/doc_to_pdf.py <input_path> [--output <output.pdf>]
```
Convert to PDF first (via LibreOffice soffice), then render page images with `pdf_to_pages.py`.

**Markdown files:**
Read file content directly, use inline markdown-to-HTML conversion in the HTML (Claude outputs pre-rendered HTML when generating).

**Image files:**
Read directly as base64 data URL and embed in HTML.

### Review HTML Structure

See `references/file_review_spec.md` for details. Key elements:

- **Top Bar**: filename + zoom controls + "Annotations" drawer button (with count) + "Copy Feedback" button
- **Main Area**: page image, supports box/point selection
- **Annotation Markers**: blue dot (point annotation) / blue semi-transparent rectangle (region annotation)
- **Side Drawer**: annotation list, editable/deletable
- **Feedback Format**: human-readable lines + machine-parseable JSON (wrapped in `---META---`)

### paper_worker Enhancement

When the current directory contains a `resume/` module and the output is DOCX, auto-enhance:

```python
# Check enhancement availability
try:
    from resume.review_element_registry import build_element_map
    from resume.parser import parse_layout_document
    ENHANCED = True
except ImportError:
    ENHANCED = False

if ENHANCED:
    # Build element_map and inject into HTML
    doc = parse_layout_document(docx_path)
    element_map = build_element_map(doc)
    # HTML auto-enables hover tooltips and coordinate mapping
```

When enhanced, annotations automatically show the element role under the cursor (e.g., "work experience body"), and feedback text automatically includes element identifiers.

## Mode 2: Text Report Mode

For long-form text, analysis results, data reports, etc. Core capabilities: dark-themed visual presentation, decision interaction, feedback export.

### Workflow

1. **Analyze Content Structure** — Identify heading hierarchy, data blocks, code blocks, comparison content
2. **Generate Report HTML** — Generate self-contained HTML per `references/text_report_spec.md`
3. **Open Browser** — Same as above

### Report HTML Structure

See `references/text_report_spec.md` for details. Key elements:

- **Dark Theme**: background `#0b0f14`, cards `#131820`, text `#c9d1d9`
- **Card Layout**: `.card` base class + left border color differentiation (blue=info, red=issue, green=solution, purple=concept)
- **TOC Navigation**: fixed top-right, scroll-linked highlight
- **Decision Panel**: fixed bottom-right, three buttons (Accept/Consider/Reject), click to copy preset feedback to clipboard
- **Feedback Export**: iterate all comment areas, concatenate as Markdown

### Content Mapping Rules

| Raw Content | HTML Component |
|---------|----------|
| Headings/sections | h2/h3 + card container |
| Long analysis text | `.card.info` card |
| Issues/risks | `.card.fracture` red left border |
| Solutions/suggestions | `.card.rfc` green left border |
| Concepts/theory | `.card.motif` purple left border |
| Data tables | `<table>` + highlighted rows |
| Comparison content | `.grid2` dual-column + `.compare-old`/`.compare-new` |
| Code blocks | `<pre>` + syntax highlighting spans |
| Simple linear flow (3-5 steps) | `.flow` CSS flexbox flow diagram |
| Architecture/topology/data-flow overview | Mermaid `.topology-diagram.single` + lightbox zoom |
| Before/after architecture comparison | `.topology-compare` with `.topology-diagram.current` + `.topology-diagram.elevated` (Mermaid) |
| Statistics | `.metric-row` metric panel |

## Mixed Mode Handling

When output includes both files and analysis text (e.g., "generated a PDF with modification suggestions"), generate dual-panel HTML:

- Left: file preview area (box/point annotation)
- Right: analysis text area (card layout + decision panel)
- Shared feedback export across both sides

## Execution Steps

### 1. Determine Mode

```python
# Pseudocode — Claude determines based on context during execution
if output_is_file(pdf, docx, ppt, md, image):
    mode = "file_review"
elif output_is_long_text(>500 chars) or output_is_analysis:
    mode = "text_report"
elif output_is_mixed:
    mode = "dual"
```

### 2. Preprocess (File Mode)

```bash
# PDF -> page image JSON
python3 <skill>/scripts/pdf_to_pages.py output/report.pdf --dpi 144

# DOCX -> PDF -> page images
python3 <skill>/scripts/doc_to_pdf.py output/report.docx
python3 <skill>/scripts/pdf_to_pages.py output/report.pdf
```

### 3. Generate HTML

Claude generates a complete self-contained HTML file following the specs in `references/`, written to the same directory as the output.

File naming:
- File review: `<original_filename>_review.html`
- Text report: `<task_topic>_report.html`
- Dual mode: `<task_topic>_review.html`

### Diagram Decision (before generating HTML)

Before writing the HTML, classify every diagram or structural visualization in the content:

| Content pattern | Use |
|---------|------|
| 3-5 step linear pipeline or sequence | `.flow` CSS flexbox — lightweight, no CDN needed |
| Any architecture diagram, topology map, or data flow with more than 5 nodes | Mermaid `.topology-diagram.single` in a blue card — requires Mermaid CDN + lightbox JS |
| "Current vs Proposed" architecture comparison | `.topology-compare` with two Mermaid diagrams (`.current` red + `.elevated` green) — requires Mermaid CDN + lightbox JS |
| Entity-relationship or sequence diagrams | Mermaid `.topology-diagram.single` with `erDiagram` or `sequenceDiagram` syntax |

**Rule of thumb**: If it has more than 5 nodes, branches, or bidirectional edges, use Mermaid. Only use `.flow` for simple, linear, one-direction sequences.

If Mermaid is used at all, the HTML MUST include:
1. The Mermaid CDN `<script type="module">` in `<head>` (with themeVariables matching the report's dark theme)
2. The lightbox `<script>` before `</body>`

### 4. Open Browser

```bash
python3 <skill>/scripts/open_browser.py <html_path>
```

Cross-platform: macOS `open`, Linux `xdg-open`, Windows `start`.

### 5. Feedback Collection

Tell the user:
- File mode: click/box-select on pages to add annotations, then click "Copy Feedback" to paste back
- Text mode: click buttons in the decision panel, or fill in comment areas, then click "Export Feedback" to paste back

## Notes

- All HTML must be **self-contained** (CSS/JS inline, no external dependencies), openable offline
- File preprocessing scripts output to a temp directory or the output directory, without polluting source files
- Browser opening uses the `open` command and does not block the Claude session
- When soffice is unavailable, DOCX preprocessing will fail; fall back to text report mode to display file content
- For large files (>50 page PDF), prompt the user whether to continue rendering to avoid long waits
