# Shared HTML System Specification

## 1. Base Document

Every generated page must include:

```html
<!doctype html>
<html lang="<response-language>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'none'; img-src data: blob:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; font-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <title><specific descriptive title></title>
  <style>/* Inline CSS */</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="page-header">...</header>
  <div class="layout">
    <nav class="toc" aria-label="Sections">...</nav><!-- only when useful -->
    <main id="main">...</main>
    <aside class="review-panel" aria-label="Review controls">...</aside><!-- only when useful -->
  </div>
  <div class="toast" role="status" aria-live="polite" hidden></div>
  <script>/* Inline, no untrusted code interpolation */</script>
</body>
</html>
```

If an explicitly approved online-enhanced document needs external libraries, declare the dependencies visibly and adjust CSP only
for those named assets. Do not call such an output offline/self-contained.

## 2. Visual Tokens

Use a restrained design system rather than task-specific one-off styling:

```css
:root {
  --bg: #f6f7f9; --surface: #ffffff; --surface-2: #f0f3f6;
  --text: #16202a; --muted: #52606d; --border: #d7dee6;
  --accent: #1267d6; --positive: #087443; --warning: #9a5700; --danger: #b42318;
  --shadow: 0 1px 3px rgba(16,24,40,.08), 0 8px 20px rgba(16,24,40,.04);
  --radius: 12px; --measure: 74ch;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0c1117; --surface: #141b23; --surface-2: #1c2631;
    --text: #e6edf3; --muted: #9ba9b7; --border: #2c3845;
    --accent: #69a6ff; --positive: #4bd08b; --warning: #f2bb5d; --danger: #ff7b72;
    --shadow: none;
  }
}
```

- Body text: comfortable line height (`1.55–1.7`) and readable measure.
- Cards: use border and spacing before color; never communicate state through color alone.
- Avoid defaulting every page to a dense dark dashboard. Follow color scheme and content needs.

## 3. Layout Rules

- `main` content is the reading priority and remains readable without JavaScript.
- Use a table of contents only for four or more meaningful sections or long documents.
- Use side panels only when persistent review controls improve the task; collapse them below content on narrow screens.
- The summary card is always visible near the top and should not be hidden behind controls.
- Use `<details>` for secondary detail, with clear summaries that explain what is inside.

Suggested breakpoints:

```css
.layout { display:grid; grid-template-columns:minmax(0, 1fr); gap:1rem; }
@media (min-width: 960px) {
  .layout.has-toc { grid-template-columns: 220px minmax(0, 1fr); }
  .layout.has-review { grid-template-columns: minmax(0, 1fr) 300px; }
  .layout.has-toc.has-review { grid-template-columns: 210px minmax(0, 1fr) 290px; }
  .toc, .review-panel { position:sticky; top:1rem; align-self:start; }
}
```

## 4. Readability and Cognitive Load

- A page starts with a concise conclusion, objective, or review instruction.
- Use short blocks and descriptive headings; do not transform prose into dozens of visual cards without reason.
- Show one primary action at a time. Secondary operations should be visually subordinate.
- Use aligned comparison tables/cards so differences are inspectable without searching across paragraphs.
- Use labels such as `Fact`, `Inference`, `Assumption`, `Risk`, and `Decision needed` when these distinctions matter.

## 5. Interaction and Accessibility

- All controls use semantic buttons, inputs, labels, and fieldsets.
- Keyboard focus is visible and not hidden under sticky bars.
- Every pointer-driven function has a keyboard/single-click alternative.
- For annotation regions, offer a list-based comment action in addition to drawing a rectangle.
- Minimum target size is `24px × 24px`; use `40px+` for primary buttons where practical.
- Use `aria-live="polite"` for copy/save notifications.
- Respect reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; animation: none !important; }
}
```

## 6. Diagram Policy

Use the smallest reliable representation:

| Structure | Default representation |
|---|---|
| Up to five linear steps | CSS step flow with text list fallback |
| Comparison of before/after pathways | Inline SVG or aligned node lists with arrows |
| Larger topology or dependency view | Inline SVG with zoom and adjacent text summary |
| Metrics/trends | HTML table first; optional inline SVG visualization |

Do not require a CDN renderer for a page that promises offline operation. Every visual needs a short text interpretation and any
critical values in accessible text or table form.

## 7. Safe Content Insertion

- Insert content through escaped text nodes whenever possible.
- If generated markup is assembled programmatically, provide an `escapeHtml()` utility for all untrusted strings.
- Structured feedback JSON must be serialized safely; escape `<` in JSON inserted into `<script type="application/json">`.
- Links must be explicit and validated; do not create clickable `javascript:` or untrusted external URLs.

## 8. Printing and Sharing

Provide print support for explanation, decision, plan, evidence, and technical review pages:

```css
@media print {
  .toc, .review-panel, .feedback-controls, .toast, button { display:none !important; }
  body { background:#fff; color:#111; }
  .card, details { break-inside:avoid; box-shadow:none; }
  details > * { display:block; }
}
```

Artifact annotation pages need not be optimized for printing unless the user requests a printable review export.
