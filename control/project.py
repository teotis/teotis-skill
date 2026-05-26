#!/usr/bin/env python3
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "AGENTS.md"
SKILLS_DIR = ROOT / "skills"
USER_SKILL_TARGETS = {
    "codex": Path.home() / ".codex" / "skills",
    "claude": Path.home() / ".claude" / "skills",
}
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
- 当前 Claude Code 2.x 配置下，生成启动命令前先确认官方 CLI reference 和本机版本；`claude --help` 不一定列出全部 flag。
- 多 agent 编排可用 `claude --bg` 自动创建 background sessions，并通过 `claude agents` / Agents View 监控。
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


def private_skill_dirs() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(path for path in SKILLS_DIR.iterdir() if (path / "SKILL.md").is_file())


def selected_skill_targets(target: str) -> dict[str, Path]:
    if target == "all":
        return USER_SKILL_TARGETS
    return {target: USER_SKILL_TARGETS[target]}


def replace_tree(src: Path, dest: Path) -> None:
    if dest.exists() or dest.is_symlink():
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)
    shutil.copytree(src, dest)


def sync_user_skills(target: str, dry_run: bool) -> int:
    skills = private_skill_dirs()
    if not skills:
        print("missing private skills under skills/", file=sys.stderr)
        return 1

    for target_name, target_dir in selected_skill_targets(target).items():
        print(f"{'Would sync' if dry_run else 'Syncing'} {len(skills)} skills to {target_name}: {target_dir}")
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
        for src in skills:
            dest = target_dir / src.name
            if dry_run:
                print(f"  {src.relative_to(ROOT)} -> {dest}")
            else:
                replace_tree(src, dest)
                print(f"  synced {src.name}")
    return 0


def compare_dirs(src: Path, dest: Path, result: Result, label: str) -> None:
    if not dest.exists():
        result.issues.append(f"{label} missing target directory: {dest}")
        return
    comparison = filecmp.dircmp(src, dest)
    for name in comparison.left_only:
        result.issues.append(f"{label} missing {src.name}/{name}")
    for name in comparison.right_only:
        result.issues.append(f"{label} extra {src.name}/{name}")
    for name in comparison.diff_files:
        result.issues.append(f"{label} differs {src.name}/{name}")
    for name in comparison.common_funny:
        result.issues.append(f"{label} cannot compare {src.name}/{name}")
    for subdir in comparison.common_dirs:
        compare_dirs(src / subdir, dest / subdir, result, label)


def check_user_skills_for_target(result: Result, target_name: str, target_dir: Path) -> None:
    skills = private_skill_dirs()
    if not skills:
        result.issues.append("missing private skills under skills/")
        return
    for src in skills:
        dest = target_dir / src.name
        if not dest.exists():
            result.issues.append(f"{target_name} missing skill: {src.name}")
            continue
        compare_dirs(src, dest, result, target_name)
    if not result.issues:
        result.notices.append(f"{target_name} user skills are synced")


def check_user_skills(target: str) -> int:
    result = Result()
    for target_name, target_dir in selected_skill_targets(target).items():
        check_user_skills_for_target(result, target_name, target_dir)

    for notice in result.notices:
        print(f"OK: {notice}")
    for issue in result.issues:
        print(f"ERROR: {issue}", file=sys.stderr)
    return 0 if result.ok else 1


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
    if not SKILLS_DIR.is_dir():
        result.issues.append("missing skills/ directory")
        return

    root_skill_files = [
        path for path in ROOT.glob("*/SKILL.md")
        if path.parts[-2] not in {"skills", "public"}
    ]
    if root_skill_files:
        for path in root_skill_files:
            result.issues.append(f"private skill outside skills/: {path.relative_to(ROOT)}")

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
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
    sync_user = sub.add_parser("sync-user-skills", help="sync private skills to user-level Codex and Claude skill directories")
    sync_user.add_argument("--target", choices=["all", "codex", "claude"], default="all")
    sync_user.add_argument("--dry-run", action="store_true")
    check_user = sub.add_parser("check-user-skills", help="check user-level Codex and Claude skills against this workspace")
    check_user.add_argument("--target", choices=["all", "codex", "claude"], default="all")
    args = parser.parse_args()

    if args.command == "sync-agents":
        return sync_agents()
    if args.command == "check":
        return check()
    if args.command == "sync-user-skills":
        return sync_user_skills(args.target, args.dry_run)
    if args.command == "check-user-skills":
        return check_user_skills(args.target)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
