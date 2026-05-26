@AGENTS.md

# Claude Code adapter

This repository uses AGENTS.md as the shared source of truth. See that file for all project rules, conventions, and validation commands.

## Claude Code Notes

- 修改共享规则后，运行 `rtk python3 control/project.py sync-agents`。
- 不要在本文件复制共享主规则；需要调整通用规则时只改 `AGENTS.md`。
- 当前 Claude Code 2.x 配置下，生成启动命令前先用 `claude --version` 和 `claude --help` 校验可用参数。
- 多 agent 编排优先使用 Agent View 和 `claude agents` 的默认模型、effort、permission 配置；不要继续生成过时的 `claude --bg` 命令，除非当前 CLI 帮助明确支持。
