@AGENTS.md

# Claude Code adapter

This repository uses AGENTS.md as the shared source of truth. See that file for all project rules, conventions, and validation commands.

## Claude Code Notes

- 修改共享规则后，运行 `rtk python3 control/project.py sync-agents`。
- 不要在本文件复制共享主规则；需要调整通用规则时只改 `AGENTS.md`。
- 当前 Claude Code 2.x 配置下，生成启动命令前先确认官方 CLI reference 和本机版本；`claude --help` 不一定列出全部 flag。
- 多 agent 编排可用 `claude --bg` 自动创建 background sessions，并通过 `claude agents` / Agents View 监控。
