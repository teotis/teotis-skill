# Shared HTML Report Base

Common patterns for skills that generate interactive HTML analysis reports (abstraction-architect, analyze-success, renewal-architect).

Resolve this file relative to the calling SKILL.md's directory: `../shared/report_base.md`.

---

## 1. Mermaid Initialization

Place in `<head>`. Each skill should customize `themeVariables` colors to match its design tokens.

```html
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  themeVariables: {
    fontSize: '16px',
    primaryColor: 'var(--mermaid-primary, #334155)',
    primaryTextColor: 'var(--mermaid-text, #e2e8f0)',
    primaryBorderColor: 'var(--mermaid-border, #64748b)',
    lineColor: 'var(--mermaid-line, #94a3b8)',
    secondaryColor: 'var(--mermaid-secondary, #1e293b)',
    tertiaryColor: 'var(--mermaid-tertiary, #334155)',
    nodeBorder: 'var(--mermaid-node-border, #64748b)',
    clusterBkg: 'var(--mermaid-cluster-bg, #1e293b)',
    clusterBorder: 'var(--mermaid-cluster-border, #475569)',
    titleColor: 'var(--mermaid-title, #e2e8f0)',
    edgeLabelBackground: 'var(--mermaid-edge-label-bg, #1e293b)'
  }
});
</script>
```

### Compatibility Rules (all skills)

- Use `flowchart TB`, `flowchart LR`, or `flowchart TD`; never use `graph`.
- Do not use emoji inside Mermaid code. Node labels must be ASCII or plain text.
- Do not use `linkStyle` directives.
- Use `subgraph id["Display Label"]` formatting.
- Avoid complex punctuation and special path symbols inside node text.
- Do not add `%%{init:...}%%` blocks in individual diagrams.
- `.topology-diagram .mermaid` must have `min-height: 380px; width: 100%;`.
- If Mermaid CDN cannot load, display readable Mermaid source in `<pre>` blocks and disclose that rendering is unavailable.

---

## 2. Lightbox JavaScript

Identical across all three skills. Include once in a `<script>` block before `</body>`.

```javascript
document.querySelectorAll('.topology-diagram').forEach(diagram => {
  diagram.style.cursor = 'pointer';
  diagram.addEventListener('click', () => {
    const sourceSvg = diagram.querySelector('.mermaid svg');
    if (!sourceSvg) return;
    const svg = sourceSvg.cloneNode(true);
    const lb = document.createElement('div');
    lb.className = 'lightbox active';
    const wrapper = document.createElement('div');
    wrapper.className = 'mermaid';
    wrapper.appendChild(svg);
    lb.appendChild(wrapper);
    document.body.appendChild(lb);
    const close = () => lb.remove();
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', function onEsc(e) {
      if (e.key === 'Escape') {
        close();
        document.removeEventListener('keydown', onEsc);
      }
    });
  });
});
```

### Required CSS for Lightbox

```css
.lightbox { display: none; position: fixed; inset: 0; z-index: 9999; background: var(--lb-backdrop); cursor: pointer; }
.lightbox.active { display: flex; align-items: center; justify-content: center; }
.lightbox .mermaid { min-width: 700px; min-height: 500px; max-width: 94vw; max-height: 92vh; overflow: auto; background: var(--lb-content-bg); border-radius: 8px; padding: 24px; }
```

---

## 3. Topology Comparison CSS Skeleton

Each skill defines its own CSS variables and class names, but the layout skeleton is shared:

```css
.topology-compare { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 24px; }
.topology-diagram { flex: 1; min-width: 340px; cursor: pointer; }
.topology-diagram .mermaid { min-height: 380px; width: 100%; background: var(--topo-bg); }
.topology-diagram .label { font-size: 14px; font-weight: 600; margin-bottom: 8px; padding: 4px 12px; border-radius: 4px; display: inline-block; }
```

Each skill must define its own color variables and `.topology-diagram.<variant>` border/label styles.

---

## 4. Interactive Review System Pattern

Common to all three skills. Each skill customizes the status options and export directive text.

### Per-Card Review Controls

```html
<div class="review-controls" data-card-id="<unique-id>">
  <textarea class="review-text" placeholder="Review notes..."></textarea>
  <div class="review-actions">
    <select class="review-status">
      <!-- skill-specific options -->
    </select>
    <div class="star-rating">
      <!-- 1-5 stars -->
    </div>
  </div>
</div>
```

### localStorage Persistence

```javascript
(function() {
  const STORAGE_KEY = '<skill-specific-key>';

  function saveReview(cardId, data) {
    try {
      const all = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      all[cardId] = data;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
    } catch (e) { /* fall back to in-memory */ }
  }

  function loadReview(cardId) {
    try {
      const all = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      return all[cardId] || null;
    } catch (e) { return null; }
  }

  // Wire up all review cards on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.review-controls').forEach(ctrl => {
      const cardId = ctrl.dataset.cardId;
      const saved = loadReview(cardId);
      if (saved) {
        // restore textarea, select, stars from saved
      }
      // attach change listeners to save on input
    });
  });
})();
```

### Export FAB Pattern

```javascript
function exportReview() {
  const parts = [];
  document.querySelectorAll('.review-controls').forEach(ctrl => {
    const cardId = ctrl.dataset.cardId;
    const title = ctrl.closest('.card')?.querySelector('.card-title')?.textContent || cardId;
    const text = ctrl.querySelector('.review-text')?.value || '';
    const status = ctrl.querySelector('.review-status')?.value || '';
    const rating = ctrl.querySelector('.star-rating .active')?.dataset?.value || '';
    if (text || status || rating) {
      parts.push(`## ${title}\n- Rating: ${rating}/5\n- Status: ${status}\n- Notes: ${text}\n`);
    }
  });
  const markdown = parts.join('\n---\n') + '\n\n' + EXPORT_DIRECTIVE;
  navigator.clipboard.writeText(markdown).then(() => {
    // show toast
  }).catch(() => {
    // show fallback textarea for manual copy
  });
}
```

---

## 5. TOC Scroll Linkage

```javascript
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      document.querySelectorAll('.toc a').forEach(a => a.classList.remove('active'));
      const link = document.querySelector(`.toc a[href="#${entry.target.id}"]`);
      if (link) link.classList.add('active');
    }
  });
}, { rootMargin: '-10% 0px -80% 0px' });

document.querySelectorAll('section[id]').forEach(s => observer.observe(s));
```

---

## Usage in Skill SKILL.md

Replace the inline Mermaid init, CSS, lightbox JS, review system, and TOC code with:

> For Mermaid initialization, topology CSS skeleton, lightbox JavaScript, interactive review system, and TOC scroll linkage, use the shared patterns in `../shared/report_base.md` (resolved relative to this SKILL.md file's directory). Each skill must define its own CSS color variables and review status options; the shared file provides the structural skeleton.
