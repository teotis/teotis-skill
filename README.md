# Codex Skill Collection

A curated set of Claude Code skills for enhanced engineering workflows.

[中文版本](README.zh-CN.md)

## Skills

### `agent-handoff-planner` — Agent Handoff Planning

Verifies external-agent findings, separates Codex-retained work from delegable work, and turns broad requests into Markdown implementation packages that other agents can execute. Useful when a task needs non-multimodal agents, parallel implementation, handoff docs, or later acceptance against the original plan.

### `html` — Visual Output Delivery

Turns any task output into a polished, interactive HTML page that opens in your browser. Instead of squinting at raw text in the terminal or downloading files one by one, you get a proper visual review experience: annotate directly on rendered pages, rate results with stars, and copy structured feedback back to Claude in one click. Works with PDF, DOCX, PPT, images, markdown, and long-form analysis text.

### `grothendieck` — Architecture Deep Analysis

Analyzes your codebase through 11 mathematical thinking principles and produces an interactive review report. You get a global overview matrix of all optimization opportunities (plotted by benefit vs. cost), detailed suggestion cards with before/after architecture diagrams, and a full review system to evaluate each finding. The report finds **non-incremental** improvements — not "extract this method," but "the abstraction level is wrong, and raising it dissolves dozens of special cases."

### `skill-creator` — Build & Iterate on Skills (by Anthropic)

Created by Anthropic, the company behind Claude. A complete toolkit for building, testing, and refining Claude Code skills. Takes you through the full loop: draft a skill → run it against test cases → compare with-skill vs. without-skill results → review outputs side-by-side in a browser → improve based on feedback → repeat. Includes quantitative benchmarking and trigger description optimization so your skill fires reliably in real-world use.
