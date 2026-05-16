# 文本报告 HTML 规范

本规范定义文本报告模式的 HTML 结构、样式和交互行为。

## 页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{报告标题}</title>
  <style>/* 内联 CSS */</style>
</head>
<body>
  <nav class="toc">...</nav>
  <main class="container">
    <header class="report-header">
      <h1>{标题}</h1>
      <p class="subtitle">{摘要}</p>
    </header>
    <!-- 按 Phase 组织的内容区 -->
    <section id="p1">...</section>
    <section id="p2">...</section>
    ...
  </main>
  <div class="decision-panel">...</div>
  <div class="toast" id="toast"></div>
  <script>/* 内联 JS */</script>
</body>
</html>
```

## CSS 规范

### 主题变量

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

### 字体

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

### 容器与排版

```css
.container { max-width: 1020px; margin: 0 auto; padding: 40px 24px 120px; }
h1 { font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 8px; }
h2 { font-size: 22px; font-weight: 600; color: #fff; margin-top: 48px; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
h3 { font-size: 18px; font-weight: 600; color: var(--text); margin-top: 32px; margin-bottom: 12px; }
p { margin: 0 0 16px; color: var(--text-dim); }
```

### 卡片系统

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

### 标签

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

### 对比卡

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

### 指标面板

```css
.metric-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.metric {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 6px; padding: 16px 20px; min-width: 120px; text-align: center;
}
.metric .num { font-size: 32px; font-weight: 700; color: var(--accent); }
.metric .label { font-size: 12px; color: var(--text-dim); margin-top: 4px; }
```

### 引言

```css
.motif-quote {
  border-left: 3px solid var(--purple); padding: 12px 20px;
  background: rgba(163,113,247,0.04); font-style: italic;
  color: var(--text); margin-bottom: 24px; border-radius: 0 6px 6px 0;
}
```

### 代码块

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

### 流程图

```css
.flow { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.flow .box {
  background: var(--surface); border: 1px solid var(--border);
  padding: 8px 14px; border-radius: 6px; font-size: 13px; color: var(--text);
}
.flow .arrow { color: var(--text-dim); font-size: 18px; }
```

### 表格

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

### TOC 导航

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

### 决策面板

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

### Toast 通知

```css
.toast {
  position: fixed; bottom: 90px; right: 24px; z-index: 100;
  background: var(--green); color: #000; padding: 10px 20px;
  border-radius: 8px; font-size: 14px; font-weight: 600;
  opacity: 0; transition: opacity 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; }
```

### 反馈评论区（可选）

每个卡片底部可添加评论区：

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

## 交互行为

### 决策面板

三个按钮，点击后将预设反馈文本复制到剪贴板并显示 toast：

- **采纳** (go)："整体方案认可，建议执行。"
- **思考** (think)："需要进一步分析以下方面：..."
- **驳回** (stop)："方案存在以下问题，需要重新评估：..."

### TOC 滚动联动

使用 `IntersectionObserver` 监听各 section 的可见性，自动高亮当前阅读位置对应的 TOC 条目。

### 反馈导出

页面底部的"导出反馈"按钮，遍历所有 `.card-feedback` 中的评论和评分，拼接为 Markdown：

```markdown
## 反馈汇总

### {卡片标题}
- 评分：★★★★☆
- 评论：{用户输入的评论}

### {下一个卡片标题}
...
```

复制到剪贴板并显示 toast。

## 内容组织原则

### 章节结构

标准三段式（可扩展）：
1. **概览/扫描** — 核心发现、关键指标、整体洞察
2. **问题诊断** — 具体问题、风险、痛点
3. **方案建议** — 解决方案、执行路径、优先级

### 卡片分类指南

| 内容性质 | 卡片类型 | 左边框颜色 | 典型场景 |
|---------|---------|-----------|---------|
| 信息/事实 | `.card.info` | 蓝色 | 背景说明、现状描述 |
| 问题/风险 | `.card.fracture` | 红色 | Bug、性能问题、安全隐患 |
| 方案/建议 | `.card.rfc` | 绿色 | 重构方案、优化建议 |
| 概念/理论 | `.card.motif` | 紫色 | 架构原则、设计模式 |
| 警告/注意 | `.card.warning` | 黄色 | 兼容性风险、迁移注意事项 |

### 标签使用

- 优先级：`P0`→红、`P1`→黄、`P2`→蓝
- 类型：`问题`→红、`优化`→绿、`概念`→紫、`信息`→蓝
- 可组合：`<span class="tag tag-r">P0</span> <span class="tag tag-r">问题</span>`
