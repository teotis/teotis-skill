# 文件审阅 HTML 规范

本规范定义文件审阅模式的 HTML 结构、样式和交互行为。

## 页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>审阅: {filename}</title>
  <style>/* 内联 CSS */</style>
</head>
<body>
  <div class="toolbar">...</div>
  <div class="stage">
    <div class="page-shell" data-page="1">
      <img class="page-image" src="{data_url}" />
      <!-- 批注标记动态插入此处 -->
    </div>
  </div>
  <div class="drawer">...</div>
  <template id="popover-template">...</template>
  <script>/* 内联 JS */</script>
</body>
</html>
```

## CSS 规范

### 主题变量

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

### 顶栏 (.toolbar)

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

### 主区域 (.stage)

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

### 批注标记

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

### 侧边抽屉 (.drawer)

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

### 编辑弹框 (popover)

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

## 交互行为

### 框选/点选批注

使用 Pointer Events 实现统一的触摸/鼠标交互：

1. **pointerdown**：记录起始坐标（相对于 `.page-shell` 的百分比），捕获指针
2. **pointermove**：位移超过 1.2% 阈值后开始框选，创建/更新 `.selection-box`
3. **pointerup**：
   - 未移动 → 点批注（在该位置创建 `.pin`）
   - 框选面积 >= 2% x 1.2% → 区域批注（创建 `.region`）
   - 框选太小 → 退化为点批注

### 批注数据结构

```javascript
{
  id: timestamp + random,
  kind: "point" | "region",
  page: 1,
  x: percent,         // 区域: 左上角 X
  y: percent,         // 区域: 左上角 Y
  width: percent,     // 仅 region
  height: percent,    // 仅 region
  text: "用户批注文案",
  elements: []        // 可选，元素映射匹配结果
}
```

### 持久化

- 使用 `localStorage` 存储，key 为 `review-annotations:{pathname}`
- 每次增删改后自动保存
- 页面加载时自动恢复

### 反馈复制

"复制反馈"按钮生成双格式文本：

**人读格式：**
```
#1 [第1页 点 52%,17%] 这里字体太小了
#2 [第1页 区域 4%,50% - 99%,60%] 排版太挤
```

**机器解析格式：**
```
---META---
{"annotations": [...]}
---END---
```

当存在 `element_map` 时，人读格式中自动包含元素角色：`#1 [第1页 点 52%,17%] {工作经历正文} 字体太小`

### 元素悬停提示

当 `window.__ELEMENT_MAP__` 存在时，`pointermove` 事件实时查找光标下的元素，显示浮层提示 `role (section_id)`。

## 降级策略

1. **无页面图片**：使用 iframe 嵌入 PDF data URL，禁用框选批注，提示用户"当前环境不支持精确定位"
2. **纯文本/Markdown**：渲染为 HTML 内容到 `.page-shell` 中，支持区域批注
3. **图片文件**：直接嵌入 `<img>`，支持框选/点选批注
