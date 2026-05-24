#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "control" / "contract.md"
NOTICE = "<!-- Generated from control/contract.md. Do not edit directly. -->"


@dataclass
class Result:
    issues: list[str] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def render_agents() -> str:
    return f"""# Repository Instructions

{NOTICE}

Shared skill workspace rules are in:

`control/contract.md`

Codex should read this file before changing skill layout, release guidance, or
shared repository conventions.

## Codex Notes

- After modifying shared rules, run `python3 control/project.py sync-agents`.
- Run `python3 control/project.py check` before finishing guidance changes.
- `AGENTS.md` is the Codex entry point; do not copy shared rules into this file.
"""


def render_claude() -> str:
    return f"""# Claude Code Entry

{NOTICE}

Shared skill workspace rules are in:

@./control/contract.md

## Claude Code Notes

- After modifying shared rules, run `python3 control/project.py sync-agents`.
- Run `python3 control/project.py check` before finishing guidance changes.
- Do not copy shared rules into this file.
"""


def render_gemini() -> str:
    return f"""# Gemini CLI Entry

{NOTICE}

Shared skill workspace rules are in:

@./control/contract.md

## Gemini CLI Notes

- After modifying shared rules, run `python3 control/project.py sync-agents` and reload context in Gemini CLI.
- Run `python3 control/project.py check` before finishing guidance changes.
- Do not copy shared rules into this file.
"""


def expected_agent_files() -> dict[Path, str]:
    return {
        ROOT / "AGENTS.md": render_agents(),
        ROOT / "CLAUDE.md": render_claude(),
        ROOT / "GEMINI.md": render_gemini(),
    }


def sync_agents() -> int:
    if not CONTRACT.exists():
        print("missing control/contract.md", file=sys.stderr)
        return 1
    for path, content in expected_agent_files().items():
        path.write_text(content, encoding="utf-8")
    print("Synced AGENTS.md, CLAUDE.md, and GEMINI.md.")
    return 0


def check_agent_sync(result: Result) -> None:
    if not CONTRACT.exists():
        result.issues.append("missing control/contract.md")
        return
    for path, expected in expected_agent_files().items():
        if not path.exists():
            result.issues.append(f"missing {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            result.issues.append(f"{path.relative_to(ROOT)} is not in sync with control/contract.md")
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
    sub.add_parser("sync-agents", help="regenerate agent entry files")
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
