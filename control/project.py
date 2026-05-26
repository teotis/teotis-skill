#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "AGENTS.md"
NOTICE = "<!-- Generated from AGENTS.md. Do not edit directly. -->"


@dataclass
class Result:
    issues: list[str] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def render_claude() -> str:
    return f"""@AGENTS.md

# Claude Code adapter

This repository uses AGENTS.md as the shared source of truth. See that file for all project rules, conventions, and validation commands.

## Claude Code Notes

- 修改共享规则后，运行 `rtk python3 control/project.py sync-agents`。
- 不要在本文件复制共享主规则；需要调整通用规则时只改 `AGENTS.md`。
- 当前 Claude Code 2.x 配置下，生成启动命令前先用 `claude --version` 和 `claude --help` 校验可用参数。
- 多 agent 编排优先使用 Agent View 和 `claude agents` 的默认模型、effort、permission 配置；不要继续生成过时的 `claude --bg` 命令，除非当前 CLI 帮助明确支持。
"""


def render_gemini() -> str:
    return f"""# Gemini CLI Entry

{NOTICE}

Shared skill workspace rules are in:

@./AGENTS.md

## Gemini CLI Notes

- 修改 `AGENTS.md` 后，使用 `/memory reload` 重新加载上下文。
- 运行 `rtk python3 control/project.py check` 检查同步状态。
- 不要在本文件复制共享主规则；需要调整通用规则时只改 `AGENTS.md`。
"""


def expected_agent_files() -> dict[Path, str]:
    return {
        ROOT / "CLAUDE.md": render_claude(),
        ROOT / "GEMINI.md": render_gemini(),
    }


def sync_agents() -> int:
    if not AGENTS_PATH.exists():
        print("missing AGENTS.md", file=sys.stderr)
        return 1
    for path, content in expected_agent_files().items():
        path.write_text(content, encoding="utf-8")
    print("Synced CLAUDE.md and GEMINI.md.")
    return 0


def check_agent_sync(result: Result) -> None:
    if not AGENTS_PATH.exists():
        result.issues.append("missing AGENTS.md")
        return
    for path, expected in expected_agent_files().items():
        if not path.exists():
            result.issues.append(f"missing {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            result.issues.append(f"{path.relative_to(ROOT)} is not in sync with AGENTS.md")
    if not result.issues:
        result.notices.append("agent entry files are synced")


def check_private_skill_layout(result: Result) -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        result.issues.append("missing skills/ directory")
        return

    root_skill_files = [
        path for path in ROOT.glob("*/SKILL.md")
        if path.parts[-2] not in {"skills", "public"}
    ]
    if root_skill_files:
        for path in root_skill_files:
            result.issues.append(f"private skill outside skills/: {path.relative_to(ROOT)}")

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        result.issues.append("no private skills found under skills/")
    else:
        result.notices.append(f"private skills under skills/: {len(skill_files)}")


def check() -> int:
    result = Result()
    check_agent_sync(result)
    check_private_skill_layout(result)

    for notice in result.notices:
        print(f"OK: {notice}")
    for issue in result.issues:
        print(f"ERROR: {issue}", file=sys.stderr)
    return 0 if result.ok else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sync-agents", help="regenerate agent entry files from AGENTS.md")
    sub.add_parser("check", help="check shared guidance sync and skill layout")
    args = parser.parse_args()

    if args.command == "sync-agents":
        return sync_agents()
    if args.command == "check":
        return check()
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
