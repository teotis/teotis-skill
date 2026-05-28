# AGENTS.md

This file is the shared source of truth for AI coding agents working in this repository.

## Project overview

Codex 与 Claude Code 的私有技能工作区。技能覆盖工程、研究、学习、求职准备、可审阅交付物和可复用 agent 交接流程。公开发布内容放在独立嵌套仓库 `public/teotis-skills/` 中。

## How to work

- Read this file before making changes to skill layout, release guidance, or shared conventions.
- When `rtk` is available, prefix shell commands with `rtk` (see `~/.codex/RTK.md` for the token-optimized CLI proxy). When `rtk` is not installed, run commands directly — the `rtk` prefix is an optimization, not a requirement.
- Skill 正文使用英语编写（SKILL.md、脚本、prompt），可见介绍和 frontmatter 可使用中文。
- Skill frontmatter 必须包含 `name` 和 `description`，优先中文描述，必要时补充英文关键词。
- 共享工具放在 `skills/<skill>/scripts/` 或 `skills/<skill>/references/`。

### 公开发布模型

- 私有根仓库是个人工作流和实验的源。
- `public/teotis-skills/` 是独立的 Git 仓库。
- 公开技能手动选择发布，行为可能与私有版不同。
- 不要将私有笔记、本地路径、凭证、未发布 prompt 或敏感案例复制到公开仓库。
- 公开 README 需双语：`README.md`（英文）和 `README.zh-CN.md`（中文）。

### Git 提交规则

- 使用 conventional commit 格式，中文描述。
- 不 push 到远程，除非用户明确要求。
- commit subject 应指明受影响的技能、工作流或不变量，让 `git log` 自身可审查。
- 避免泛化 subject，例如 `chore: 更新 SKILL.md` 或 `chore: 更新 N 个文件`；这些 subject 无法传达改动意图。

示例：

- `docs: 为复杂技能补充 eval 行为契约`
- `fix: 停止跟踪 .tmp 分析产物`
- `chore: 同步 agent 入口文件`
- `feat: 增加 orchestration 状态账本规则`

## Validation

```bash
# 同步 agent 入口文件
rtk python3 control/project.py sync-agents

# 检查共享指导同步和技能布局
rtk python3 control/project.py check

# 同步私有技能到 Codex 和 Claude 用户级目录
rtk python3 control/project.py sync-user-skills

# 检查用户级技能同步
rtk python3 control/project.py check-user-skills
```

## Coding conventions

- Skill bodies in English.
- Skill introductions and frontmatter descriptions may use Chinese.
- Shared utilities go under `skills/<skill>/scripts/` or `skills/<skill>/references/`.

## Architecture notes

```
skills/<skill>/SKILL.md      — 私有技能入口
skills/<skill>/scripts/      — 技能共享脚本
skills/<skill>/references/   — 技能参考文件
public/teotis-skills/        — 嵌套公开仓库（本仓库忽略）
control/                     — 工程管理工具
```

## Generated files

- `CLAUDE.md` 和 `GEMINI.md` 由 `control/project.py sync-agents` 从本文件生成，作为薄适配器入口。
- 不要直接编辑 `CLAUDE.md` 或 `GEMINI.md`；修改共享规则时只改本文件。

## Security

- 本仓库是技能工作区，不含 API key 或凭证。
- 公开仓库 `public/teotis-skills/` 发布前须审计，排除私有路径、凭证和未发布内容。

## Agent-specific adapters

- Claude Code should read `CLAUDE.md`, which points back to this file. For Claude Code 2.x, verify official CLI reference and local version before generating launch commands; `claude --help` may omit supported flags. Multi-agent orchestration may use `claude --bg` to create background sessions that are visible in `claude agents` / Agents View.
- Gemini CLI should read `GEMINI.md`, which is generated from this file.
- Codex app should use this `AGENTS.md` as the shared project instruction file.
