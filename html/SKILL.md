---
name: html
description: >
  将当前任务的产出物自动转化为 HTML 并在浏览器中打开，解决终端环境交互困难、阅读视觉不佳的问题。
  当任务完成后的产出物是文件类（PDF、DOCX、DOC、PPT、PPTX、MD、图片）或大段文本/分析/推理/图表类内容时，
  触发此技能将结果以可视化 HTML 形式交付。
  触发场景：用户说"用 html 打开"、"生成 html"、"浏览器查看"、"html 审阅"；
  或任务产出了文件（生成了 PDF/DOCX/PPT 等）需要审阅；
  或任务产出了大段分析文本、架构评审、代码分析、数据报告等需要可视化展示。
  即使用户没有明确要求 HTML，当产出物复杂度较高（多页文件、长篇分析、多维度数据）时也应主动建议使用。
---

# HTML 交付 Skill

终端环境天然不适合审阅视觉化产出物（PDF、DOCX、图片）和阅读大段分析文本。本 skill 的核心思路是：
在任务正常完成后，额外生成一份自包含的 HTML 文件并在浏览器中打开，让用户获得可视化审阅体验。

## 产出物分类

完成任务后，根据产出物类型选择模式：

| 产出物类型 | 模式 | 关键特征 |
|-----------|------|---------|
| PDF, DOCX, DOC, PPT, PPTX | **文件审阅模式** | 框选/点选批注 + 坐标映射 + 反馈复制 |
| 图片 (PNG, JPG, WEBP, SVG) | **文件审阅模式** | 框选/点选批注，无元素映射 |
| Markdown (.md) | **文件审阅模式** | 渲染为 HTML 后支持区域批注 |
| 长篇文本 (>500字)、分析报告 | **文本报告模式** | 暗色主题 + 卡片布局 + 决策面板 |
| 数据表格、对比分析 | **文本报告模式** | 表格 + 指标面板 + 对比卡 |
| 代码分析、架构评审 | **文本报告模式** | 代码高亮 + 流程图 + TOC |
| 混合型（文件+分析） | **双模式** | 文件预览 + 报告并列 |

## 模式一：文件审阅模式

适用于需要审阅文件产出物的场景。核心能力：框选/点选添加批注、智能识别批注位置、一键复制结构化反馈。

### 工作流

1. **文件预处理** — 将产出物转为可在浏览器中渲染的格式
2. **生成审阅 HTML** — 按 `references/file_review_spec.md` 规范生成自包含 HTML
3. **打开浏览器** — 用 `scripts/open_browser.py` 打开
4. **收集反馈** — 用户通过"复制反馈"按钮将结构化批注粘贴回对话

### 文件预处理

根据文件类型选择预处理方式：

**PDF 文件：**
```bash
python3 <skill-path>/scripts/pdf_to_pages.py <pdf_path> [--dpi 144] [--output <output.json>]
```
输出 JSON：每页一个 base64 PNG data URL。优先使用 pypdfium2，降级到 pdftoppm。

**DOCX/DOC/PPT/PPTX 文件：**
```bash
python3 <skill-path>/scripts/doc_to_pdf.py <input_path> [--output <output.pdf>]
```
先转为 PDF（通过 LibreOffice soffice），再用 `pdf_to_pages.py` 渲染页面图片。

**Markdown 文件：**
直接读取文件内容，在 HTML 中用内联 markdown-to-HTML 转换（Claude 生成时直接输出渲染后的 HTML）。

**图片文件：**
直接读取为 base64 data URL 嵌入 HTML。

### 审阅 HTML 结构

详见 `references/file_review_spec.md`。关键要素：

- **顶栏**：文件名 + 缩放控制 + "批注" 抽屉按钮（含计数）+ "复制反馈" 按钮
- **主区域**：页面图片，支持框选/点选
- **批注标记**：蓝色圆点（点批注）/ 蓝色半透明矩形（区域批注）
- **侧边抽屉**：批注列表，可编辑/删除
- **反馈格式**：人读行 + 机器解析 JSON（`---META---` 包裹）

### paper_worker 增强

当检测到当前目录包含 `resume/` 模块且产出物是 DOCX 时，自动增强：

```python
# 检测增强可用性
try:
    from resume.review_element_registry import build_element_map
    from resume.parser import parse_layout_document
    ENHANCED = True
except ImportError:
    ENHANCED = False

if ENHANCED:
    # 构建 element_map，注入到 HTML 中
    doc = parse_layout_document(docx_path)
    element_map = build_element_map(doc)
    # HTML 中自动启用悬停提示和坐标映射
```

增强后，批注时自动显示鼠标下方的元素角色（如"工作经历正文"），反馈文案自动包含元素标识。

## 模式二：文本报告模式

适用于大段文字、分析结果、数据报告等场景。核心能力：暗色主题美化展示、决策交互、反馈导出。

### 工作流

1. **分析内容结构** — 识别标题层级、数据块、代码块、对比内容
2. **生成报告 HTML** — 按 `references/text_report_spec.md` 规范生成自包含 HTML
3. **打开浏览器** — 同上

### 报告 HTML 结构

详见 `references/text_report_spec.md`。关键要素：

- **暗色主题**：背景 `#0b0f14`，卡片 `#131820`，文字 `#c9d1d9`
- **卡片布局**：`.card` 基类 + 左边框颜色区分类型（蓝=信息、红=问题、绿=方案、紫=概念）
- **TOC 导航**：固定右上角，滚动联动高亮
- **决策面板**：固定右下角，三个按钮（采纳/思考/驳回），点击复制预设反馈到剪贴板
- **反馈导出**：遍历所有评论区，拼接为 Markdown 格式

### 内容映射规则

| 原始内容 | HTML 组件 |
|---------|----------|
| 标题/章节 | h2/h3 + 卡片容器 |
| 大段分析文字 | `.card.info` 卡片 |
| 问题/风险 | `.card.fracture` 红色左边框 |
| 方案/建议 | `.card.rfc` 绿色左边框 |
| 概念/理论 | `.card.motif` 紫色左边框 |
| 数据表格 | `<table>` + 高亮行 |
| 对比内容 | `.grid2` 双列 + `.compare-old`/`.compare-new` |
| 代码块 | `<pre>` + 语法高亮 span |
| 流程/拓扑 | `.flow` CSS flexbox 流程图 |
| 统计数据 | `.metric-row` 指标面板 |

## 混合型处理

当产出物同时包含文件和分析文本时（如"生成了 PDF 并给出了修改建议"），生成双面板 HTML：

- 左侧：文件预览区（框选/点选批注）
- 右侧：分析文本区（卡片布局 + 决策面板）
- 两侧共享反馈导出

## 执行步骤

### 1. 判断模式

```python
# 伪代码 — Claude 实际执行时根据上下文判断
if output_is_file(pdf, docx, ppt, md, image):
    mode = "file_review"
elif output_is_long_text(>500 chars) or output_is_analysis:
    mode = "text_report"
elif output_is_mixed:
    mode = "dual"
```

### 2. 预处理（文件模式）

```bash
# PDF → 页面图片 JSON
python3 <skill>/scripts/pdf_to_pages.py output/report.pdf --dpi 144

# DOCX → PDF → 页面图片
python3 <skill>/scripts/doc_to_pdf.py output/report.docx
python3 <skill>/scripts/pdf_to_pages.py output/report.pdf
```

### 3. 生成 HTML

Claude 根据 `references/` 中的规范生成完整自包含 HTML 文件，写入产出物同目录。

文件命名：
- 文件审阅：`<原文件名>_review.html`
- 文本报告：`<任务主题>_report.html`
- 双模式：`<任务主题>_review.html`

### 4. 打开浏览器

```bash
python3 <skill>/scripts/open_browser.py <html_path>
```

跨平台支持：macOS `open`、Linux `xdg-open`、Windows `start`。

### 5. 反馈收集

告知用户：
- 文件模式：在页面上点击/框选添加批注，完成后点击"复制反馈"粘贴回来
- 文本模式：在决策面板点击按钮，或在评论区填写反馈，点击"导出反馈"粘贴回来

## 注意事项

- 所有 HTML 必须**自包含**（CSS/JS 内联，无外部依赖），可离线打开
- 文件预处理脚本输出到临时目录或产出物同目录，不污染源文件
- 浏览器打开是 `open` 命令，不阻塞 Claude 会话
- 当 soffice 不可用时，DOCX 预处理会失败，应降级为文本报告模式展示文件内容
- 大文件（>50 页 PDF）应提示用户是否继续渲染，避免长时间等待
