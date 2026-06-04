---
name: reviewable-html-report
description: >
  用于生成、改造或审查可交互评审的 HTML 报告基础设施。
  Use whenever a skill or workflow needs a browser-readable technical report with Mermaid diagrams, topology comparisons, review cards, local feedback persistence, and exportable review notes.
whenToUse: >
  当任务需要构建或审查 HTML 报告基础设施、Mermaid 图、拓扑对比、评审卡、反馈持久化、导出评审笔记或可交互技术报告模板时使用。
  不用于一次性普通 HTML 回答、简单报告排版、或只需要选择是否生成 HTML 的场景；这些应使用 html-response。
---

# Reviewable HTML Report

## Mission

Build the reusable presentation layer for dense technical reports. This skill does not perform the domain analysis itself; it turns an already-formed analysis, plan, audit, comparison, or artifact review into a self-contained HTML report that is easy to read, inspect, annotate, and hand back to another agent.

Use it as the report companion for skills such as `abstraction-architect`, `renewal-architect`, and `analyze-success` when they need interactive HTML output.

## When To Use

Use this skill when the user asks for, or another skill requires:

- an interactive HTML report;
- Mermaid topology diagrams with readable fallbacks;
- review cards, star ratings, status fields, comments, or exportable feedback;
- a visual technical report for architecture, renewal, success-pattern analysis, product review, or implementation planning;
- a shared report scaffold instead of each skill reimplementing CSS, lightbox, review persistence, and export logic.

Do not use this skill to decide the report's domain conclusions. The calling skill owns the analysis, evidence, recommendations, and acceptance criteria.

## Core Boundary

The calling skill owns meaning. This skill owns report mechanics.

| Layer | Owner |
|---|---|
| Domain evidence, findings, recommendation logic, scoring criteria | Calling skill |
| Section order and reviewable item IDs | Calling skill, using this skill's conventions |
| Mermaid import rules, lightbox behavior, review controls, feedback export, accessibility basics | `reviewable-html-report` |
| Final verification that the report renders and remains readable | Calling skill plus this skill's checklist |

## Workflow

1. Identify the report mode: architecture review, renewal plan, success-pattern analysis, product review, artifact review, or generic technical review.
2. Ask the calling skill for the stable reviewable units: finding IDs, proposal IDs, recommendation IDs, artifact page IDs, or decision IDs.
3. Load `references/report_base.md` only when you need concrete CSS, JavaScript, Mermaid rules, or review-control snippets.
4. Generate a self-contained HTML file unless the report is too large; for large reports, create a local bundle with sibling assets and an obvious index.
5. Preserve all high-stakes conclusions in the chat or source Markdown as well. The HTML can improve review, but it must not be the only place where the conclusion exists.
6. Verify the report before delivering it:
   - the opening viewport contains the answer or review task;
   - Mermaid source is readable even if CDN loading fails;
   - topology diagrams have enough space and can open in a lightbox;
   - review controls have stable IDs and do not depend on hidden state;
   - localStorage and clipboard operations have fallbacks;
   - feedback export contains enough context for a follow-up agent.

## Required Report Features

- Use semantic sections and headings. Avoid decorative title-only first screens.
- Every reviewable card must have a stable `data-card-id` or equivalent ID.
- Persist review state locally when useful, but wrap localStorage access in `try/catch`.
- Export feedback as Markdown or JSON that names the report, item IDs, rating/status/comment fields, and a next-action note.
- For Mermaid diagrams, follow the compatibility rules in `references/report_base.md`.
- Provide readable Mermaid source or explanatory fallback text when remote CDN loading is unavailable.

## Resource Map

All paths below are relative to this SKILL.md file's directory.

- `references/report_base.md` — shared Mermaid initialization, topology CSS skeleton, lightbox JavaScript, review controls, localStorage pattern, export pattern, and TOC linkage.

## Migration Guidance For Calling Skills

When migrating an existing analysis skill:

1. Keep the skill's domain method and report schema in that skill.
2. Replace inline report infrastructure prose with: "Use `reviewable-html-report/references/report_base.md` for shared report mechanics."
3. Keep skill-specific colors, terminology, statuses, and export directives local to the calling skill.
4. Do not merge analysis skills merely because they share this report layer.

