# File Review HTML Specification

This spec defines the HTML structure, styles, and interaction behavior for file review mode.

## Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review: {filename}</title>
  <style>/* Inline CSS */</style>
</head>
<body>
  <div class="toolbar">...</div>
  <div class="stage">
    <div class="page-shell" data-page="1">
      <img class="page-image" src="{data_url}" />
      <!-- Annotation markers dynamically inserted here -->
    </div>
  </div>
  <div class="drawer">...</div>
  <template id="popover-template">...</template>
  <script>/* Inline JS */</script>
</body>
</html>
```

## CSS Specification

### Theme Variables

```css
:root {
  --bg: #1a1a2e;
  --surface: #16213e;
  --border: #2a2a4a;
  --text: #e0e0e0;
  --text-dim: #8892a0;
  --accent: #4fc3f7;
  --accent-dim: rgba(79, 195, 247, 0.15);
  --danger: #ef5350;
  --success: #66bb6a;
  --warning: #ffa726;
  --pin-color: #4fc3f7;
  --region-color: rgba(79, 195, 247, 0.2);
  --selection-color: rgba(79, 195, 247, 0.3);
}
```

### Top Bar (.toolbar)

```css
.toolbar {
  position: fixed; top: 0; left: 0; right: 0;
  height: 48px; z-index: 100;
  background: var(--surface); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; padding: 0 16px; gap: 12px;
}
.toolbar .title { font-size: 14px; color: var(--text); flex: 1; }
.toolbar .btn {
  padding: 6px 14px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--surface); color: var(--text); cursor: pointer; font-size: 13px;
}
.toolbar .btn:hover { border-color: var(--accent); }
.toolbar .btn-primary {
  background: var(--accent); color: #000; border-color: var(--accent);
  font-weight: 600;
}
```

### Main Area (.stage)

```css
.stage {
  margin-top: 48px; padding: 24px;
  display: flex; flex-direction: column; align-items: center;
  min-height: calc(100vh - 48px);
}
.page-shell {
  position: relative; width: 100%; max-width: 900px;
  aspect-ratio: 0.707 / 1; /* A4 */
  background: #fff; box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  margin-bottom: 24px; overflow: hidden;
}
.page-image { width: 100%; height: 100%; object-fit: contain; pointer-events: none; }
```

### Annotation Markers

```css
.pin {
  position: absolute; width: 24px; height: 24px; border-radius: 50%;
  background: var(--pin-color); color: #000; font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  transform: translate(-50%, -50%); cursor: pointer; z-index: 10;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
.pin:hover { transform: translate(-50%, -50%) scale(1.15); }
.region {
  position: absolute; border: 2px solid var(--pin-color);
  background: var(--region-color); cursor: pointer; z-index: 10;
}
.region-label {
  position: absolute; top: -20px; left: 0;
  background: var(--pin-color); color: #000; font-size: 11px; font-weight: 700;
  padding: 1px 6px; border-radius: 3px;
}
.selection-box {
  position: absolute; border: 2px dashed var(--accent);
  background: var(--selection-color); z-index: 5; pointer-events: none;
}
```

### Side Drawer (.drawer)

```css
.drawer {
  position: fixed; top: 48px; right: -360px; width: 360px;
  height: calc(100vh - 48px); background: var(--surface);
  border-left: 1px solid var(--border); z-index: 90;
  transition: right 0.25s ease; overflow-y: auto; padding: 16px;
}
.drawer.open { right: 0; }
.drawer h3 { font-size: 15px; color: var(--text); margin-bottom: 12px; }
.annotation-item {
  padding: 10px; margin-bottom: 8px; border-radius: 6px;
  background: var(--bg); border: 1px solid var(--border); font-size: 13px;
}
.annotation-item .meta { color: var(--text-dim); font-size: 11px; margin-bottom: 4px; }
.annotation-item .text { color: var(--text); }
```

### Edit Popover (popover)

```css
.popover {
  position: fixed; z-index: 200; width: 320px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.popover textarea {
  width: 100%; min-height: 60px; resize: vertical;
  background: var(--bg); border: 1px solid var(--border); border-radius: 4px;
  color: var(--text); padding: 8px; font-size: 13px; font-family: inherit;
}
.popover .actions { display: flex; gap: 8px; margin-top: 8px; justify-content: flex-end; }
```

## Interaction Behavior

### Box/Point Annotation

Use Pointer Events for unified touch/mouse interaction:

1. **pointerdown**: record start coordinates (as percentage relative to `.page-shell`), capture pointer
2. **pointermove**: begin box selection once displacement exceeds 1.2% threshold, create/update `.selection-box`
3. **pointerup**:
   - No movement → point annotation (create `.pin` at that position)
   - Box area >= 2% x 1.2% → region annotation (create `.region`)
   - Box too small → fall back to point annotation

### Annotation Data Structure

```javascript
{
  id: timestamp + random,
  kind: "point" | "region",
  page: 1,
  x: percent,         // region: top-left X
  y: percent,         // region: top-left Y
  width: percent,     // region only
  height: percent,    // region only
  text: "user annotation text",
  elements: []        // optional, element map match results
}
```

### Persistence

- Store via `localStorage`, key is `review-annotations:{pathname}`
- Auto-save after each add/update/delete
- Auto-restore on page load

### Feedback Copy

The "Copy Feedback" button generates dual-format text:

**Human-readable format:**
```
#1 [Page 1 point 52%,17%] The font is too small here
#2 [Page 1 region 4%,50% - 99%,60%] Layout is too cramped
```

**Machine-parseable format:**
```
---META---
{"annotations": [...]}
---END---
```

When `element_map` exists, human-readable format automatically includes element role: `#1 [Page 1 point 52%,17%] {work experience body} Font too small`

### Element Hover Tooltip

When `window.__ELEMENT_MAP__` exists, `pointermove` events look up the element under the cursor in real time, showing a floating tooltip `role (section_id)`.

## Fallback Strategy

1. **No page images**: use iframe to embed PDF data URL, disable box annotation, prompt user "precise positioning not supported in current environment"
2. **Plain text/Markdown**: render as HTML content inside `.page-shell`, support region annotation
3. **Image files**: embed directly as `<img>`, support box/point annotation
