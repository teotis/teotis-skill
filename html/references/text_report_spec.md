# Text Report HTML Specification

This spec defines the HTML structure, styles, and interaction behavior for text report mode.

## Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Report Title}</title>
  <style>/* Inline CSS */</style>
</head>
<body>
  <nav class="toc">...</nav>
  <main class="container">
    <header class="report-header">
      <h1>{Title}</h1>
      <p class="subtitle">{Summary}</p>
    </header>
    <!-- Content organized by Phase -->
    <section id="p1">...</section>
    <section id="p2">...</section>
    ...
  </main>
  <div class="decision-panel">...</div>
  <div class="toast" id="toast"></div>
  <script>/* Inline JS */</script>
</body>
</html>
```

## CSS Specification

### Theme Variables

```css
:root {
  --bg: #0b0f14;
  --surface: #131820;
  --border: #21262d;
  --text: #c9d1d9;
  --text-dim: #6e7681;
  --accent: #5b9bd5;
  --red: #f85149;
  --yellow: #d2991d;
  --green: #3fb950;
  --purple: #a371f7;
  --blue: #58a6ff;
}
```

### Typography

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  font-size: 15px; line-height: 1.7; color: var(--text);
  background: var(--bg); margin: 0; padding: 0;
}
code, pre {
  font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace;
}
```

### Container & Layout

```css
.container { max-width: 1020px; margin: 0 auto; padding: 40px 24px 120px; }
h1 { font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 8px; }
h2 { font-size: 22px; font-weight: 600; color: #fff; margin-top: 48px; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
h3 { font-size: 18px; font-weight: 600; color: var(--text); margin-top: 32px; margin-bottom: 12px; }
p { margin: 0 0 16px; color: var(--text-dim); }
```

### Card System

```css
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 6px; padding: 20px; margin-bottom: 16px;
  border-left: 3px solid var(--accent);
}
.card.info { border-left-color: var(--accent); }
.card.fracture { border-left-color: var(--red); }
.card.rfc { border-left-color: var(--green); }
.card.motif { border-left-color: var(--purple); }
.card.warning { border-left-color: var(--yellow); }
```

### Tags

```css
.tag {
  display: inline-block; padding: 2px 8px; border-radius: 12px;
  font-size: 12px; font-weight: 600; margin-right: 4px;
}
.tag-r { background: rgba(248,81,73,0.15); color: var(--red); }
.tag-g { background: rgba(63,185,80,0.15); color: var(--green); }
.tag-b { background: rgba(88,166,255,0.15); color: var(--blue); }
.tag-p { background: rgba(163,113,247,0.15); color: var(--purple); }
.tag-y { background: rgba(210,153,29,0.15); color: var(--yellow); }
```

### Comparison Cards

```css
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.compare-old {
  background: rgba(248,81,73,0.06); border: 1px solid rgba(248,81,73,0.2);
  border-radius: 6px; padding: 16px;
}
.compare-new {
  background: rgba(63,185,80,0.06); border: 1px solid rgba(63,185,80,0.2);
  border-radius: 6px; padding: 16px;
}
```

### Metric Panel

```css
.metric-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.metric {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 6px; padding: 16px 20px; min-width: 120px; text-align: center;
}
.metric .num { font-size: 32px; font-weight: 700; color: var(--accent); }
.metric .label { font-size: 12px; color: var(--text-dim); margin-top: 4px; }
```

### Blockquote

```css
.motif-quote {
  border-left: 3px solid var(--purple); padding: 12px 20px;
  background: rgba(163,113,247,0.04); font-style: italic;
  color: var(--text); margin-bottom: 24px; border-radius: 0 6px 6px 0;
}
```

### Code Blocks

```css
pre {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 16px; overflow-x: auto;
  font-size: 13px; line-height: 1.5; margin-bottom: 16px;
}
code { font-size: 13px; }
pre code { background: none; border: none; padding: 0; }
code:not(pre code) {
  background: rgba(88,166,255,0.1); padding: 2px 6px;
  border-radius: 3px; font-size: 13px;
}
.kw { color: var(--purple); } .ty { color: var(--accent); }
.fn { color: var(--green); } .str { color: var(--yellow); }
.cm { color: var(--text-dim); font-style: italic; }
```

### Flow Diagram

```css
.flow { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.flow .box {
  background: var(--surface); border: 1px solid var(--border);
  padding: 8px 14px; border-radius: 6px; font-size: 13px; color: var(--text);
}
.flow .arrow { color: var(--text-dim); font-size: 18px; }
```

### Tables

```css
table {
  width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 14px;
}
th {
  background: rgba(88,166,255,0.08); text-align: left;
  padding: 10px 12px; border-bottom: 2px solid var(--border); color: var(--text);
}
td { padding: 8px 12px; border-bottom: 1px solid var(--border); color: var(--text-dim); }
tr.high td { background: rgba(248,81,73,0.06); }
tr.del td { background: rgba(63,185,80,0.06); }
```

### TOC Navigation

```css
.toc {
  position: fixed; top: 20px; right: 20px; width: 200px; z-index: 100;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 12px;
}
.toc a {
  display: block; padding: 4px 8px; color: var(--text-dim);
  text-decoration: none; font-size: 13px; border-radius: 4px;
  border-left: 2px solid transparent;
}
.toc a:hover, .toc a.active { color: var(--accent); border-left-color: var(--accent); }
@media (max-width: 700px) { .toc { display: none; } }
```

### Decision Panel

```css
.decision-panel {
  position: fixed; bottom: 24px; right: 24px; z-index: 100;
  display: flex; flex-direction: column; gap: 8px;
}
.decision-panel button {
  padding: 10px 20px; border-radius: 8px; border: none;
  font-size: 14px; font-weight: 600; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3); min-width: 120px;
}
.decision-panel .go { background: var(--green); color: #000; }
.decision-panel .think { background: var(--accent); color: #000; }
.decision-panel .stop { background: var(--red); color: #fff; }
```

### Toast Notification

```css
.toast {
  position: fixed; bottom: 90px; right: 24px; z-index: 100;
  background: var(--green); color: #000; padding: 10px 20px;
  border-radius: 8px; font-size: 14px; font-weight: 600;
  opacity: 0; transition: opacity 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; }
```

### Feedback Comment Area (Optional)

An optional comment area can be added at the bottom of each card:

```css
.card-feedback { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); }
.card-feedback textarea {
  width: 100%; min-height: 40px; resize: vertical;
  background: var(--bg); border: 1px solid var(--border); border-radius: 4px;
  color: var(--text); padding: 8px; font-size: 12px; font-family: inherit;
}
.card-feedback .rating { margin-top: 6px; }
.card-feedback .star { cursor: pointer; font-size: 18px; color: var(--border); }
.card-feedback .star.active { color: var(--yellow); }
```

## Interaction Behavior

### Decision Panel

Three buttons that copy preset feedback text to the clipboard and show a toast:

- **Accept** (go): "Overall plan accepted, recommend proceeding."
- **Consider** (think): "Needs further analysis on the following aspects: ..."
- **Reject** (stop): "Plan has the following issues, needs re-evaluation: ..."

### TOC Scroll Linkage

Use `IntersectionObserver` to monitor section visibility, automatically highlighting the TOC entry corresponding to the current reading position.

### Feedback Export

The "Export Feedback" button at the bottom of the page iterates all `.card-feedback` comments and ratings, concatenating them as Markdown:

```markdown
## Feedback Summary

### {Card Title}
- Rating: ★★★★☆
- Comment: {user's comment}

### {Next Card Title}
...
```

Copy to clipboard and show toast.

## Content Organization Principles

### Section Structure

Standard three-part structure (extensible):
1. **Overview/Scan** — Key findings, critical metrics, overall insights
2. **Problem Diagnosis** — Specific issues, risks, pain points
3. **Solution Proposals** — Solutions, execution paths, priorities

### Card Classification Guide

| Content Nature | Card Type | Left Border Color | Typical Scenario |
|---------|---------|-----------|---------|
| Info/Facts | `.card.info` | Blue | Background explanation, current state |
| Issues/Risks | `.card.fracture` | Red | Bugs, performance issues, security concerns |
| Solutions/Suggestions | `.card.rfc` | Green | Refactoring plans, optimization suggestions |
| Concepts/Theory | `.card.motif` | Purple | Architecture principles, design patterns |
| Warnings/Cautions | `.card.warning` | Yellow | Compatibility risks, migration notes |

### Tag Usage

- Priority: `P0`→Red, `P1`→Yellow, `P2`→Blue
- Type: `Issue`→Red, `Optimization`→Green, `Concept`→Purple, `Info`→Blue
- Can be combined: `<span class="tag tag-r">P0</span> <span class="tag tag-r">Issue</span>`
