#!/usr/bin/env python3
"""Tests for control/project.py — core project management tooling.

Run from repo root: python3 control/tests/test_project.py
Run via rtk: rtk python3 control/tests/test_project.py
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add repo root for imports
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "control"))

import project


class TestResult(unittest.TestCase):
    def test_empty_result_is_ok(self):
        r = project.Result()
        self.assertTrue(r.ok)
        self.assertEqual(r.issues, [])
        self.assertEqual(r.notices, [])

    def test_result_with_issues_is_not_ok(self):
        r = project.Result(issues=["error"])
        self.assertFalse(r.ok)

    def test_result_only_notices_is_ok(self):
        r = project.Result(notices=["info"])
        self.assertTrue(r.ok)


class TestRenderFunctions(unittest.TestCase):
    def test_render_claude_contains_expected_content(self):
        output = project.render_claude()
        self.assertIn("@AGENTS.md", output)
        self.assertIn("Claude Code adapter", output)
        self.assertIn("rtk python3 control/project.py sync-agents", output)

    def test_render_claude_does_not_contain_notice(self):
        output = project.render_claude()
        self.assertNotIn(project.NOTICE, output)

    def test_render_gemini_contains_notice(self):
        output = project.render_gemini()
        self.assertIn(project.NOTICE, output)
        self.assertIn("@./AGENTS.md", output)
        self.assertIn("Gemini CLI Notes", output)


class TestPrivateSkillDirs(unittest.TestCase):
    def test_real_skills_dir_exists(self):
        skills = project.private_skill_dirs()
        self.assertGreater(len(skills), 0)
        for d in skills:
            self.assertTrue((d / "SKILL.md").is_file())


class TestCompareDirs(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="project_test_"))
        self.src = self.tmp / "src"
        self.dest = self.tmp / "dest"
    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _make_skill_like(self, base: Path, name: str, extra_file: str | None = None):
        skill_dir = base / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"# {name}")
        if extra_file:
            extra_path = skill_dir / extra_file
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text("extra")

    def test_missing_dest_reports_issue(self):
        self._make_skill_like(self.src, "test-skill")
        result = project.Result()
        project.compare_dirs(self.src / "test-skill", self.dest / "test-skill", result, "test")
        self.assertFalse(result.ok)
        self.assertIn("missing target directory", str(result.issues))

    def test_identical_dirs_are_ok(self):
        self._make_skill_like(self.src, "test-skill")
        shutil.copytree(self.src, self.dest)
        result = project.Result()
        project.compare_dirs(self.src / "test-skill", self.dest / "test-skill", result, "test")
        self.assertTrue(result.ok)

    def test_extra_file_in_dest_reported(self):
        self._make_skill_like(self.src, "test-skill")
        self._make_skill_like(self.dest, "test-skill", "extra_file.md")
        result = project.Result()
        project.compare_dirs(self.src / "test-skill", self.dest / "test-skill", result, "test")
        self.assertFalse(result.ok)
        self.assertTrue(any("extra" in i for i in result.issues))

    def test_missing_file_in_dest_reported(self):
        self._make_skill_like(self.src, "test-skill", "references/data.md")
        self._make_skill_like(self.dest, "test-skill")
        result = project.Result()
        project.compare_dirs(self.src / "test-skill", self.dest / "test-skill", result, "test")
        self.assertFalse(result.ok)
        self.assertTrue(any("missing" in i for i in result.issues))

    def test_differing_file_reported(self):
        self._make_skill_like(self.src, "test-skill")
        self._make_skill_like(self.dest, "test-skill")
        (self.dest / "test-skill" / "SKILL.md").write_text("# modified")
        result = project.Result()
        project.compare_dirs(self.src / "test-skill", self.dest / "test-skill", result, "test")
        self.assertFalse(result.ok)
        self.assertTrue(any("differs" in i for i in result.issues))


class TestReplaceTree(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="project_test_"))
        self.src = self.tmp / "src"
        self.dest = self.tmp / "dest"
    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_replace_creates_dest_when_missing(self):
        self.src.mkdir()
        (self.src / "file.txt").write_text("hello")
        project.replace_tree(self.src, self.dest)
        self.assertTrue(self.dest.is_dir())
        self.assertTrue((self.dest / "file.txt").is_file())

    def test_replace_overwrites_existing_dest(self):
        self.src.mkdir()
        (self.src / "file.txt").write_text("new")
        self.dest.mkdir()
        (self.dest / "old.txt").write_text("old")
        project.replace_tree(self.src, self.dest)
        self.assertTrue((self.dest / "file.txt").is_file())
        self.assertFalse((self.dest / "old.txt").exists())

    def test_replace_overwrites_existing_file_with_dir(self):
        self.src.mkdir()
        (self.src / "nested").mkdir()
        self.dest.write_text("i am a file")
        project.replace_tree(self.src, self.dest)
        self.assertTrue(self.dest.is_dir())
        self.assertTrue((self.dest / "nested").is_dir())


class TestSyncAgents(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="project_test_"))
        self.original_agents = project.AGENTS_PATH
        self.original_root = project.ROOT
        project.ROOT = self.tmp
        project.AGENTS_PATH = self.tmp / "AGENTS.md"

    def tearDown(self):
        project.ROOT = self.original_root
        project.AGENTS_PATH = self.original_agents
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_sync_agents_fails_without_agents_md(self):
        rc = project.sync_agents()
        self.assertEqual(rc, 1)

    def test_sync_agents_writes_expected_files(self):
        project.AGENTS_PATH.write_text("# AGENTS test", encoding="utf-8")
        rc = project.sync_agents()
        self.assertEqual(rc, 0)
        self.assertTrue((self.tmp / "CLAUDE.md").is_file())
        self.assertTrue((self.tmp / "GEMINI.md").is_file())
        claude_content = (self.tmp / "CLAUDE.md").read_text()
        self.assertIn("@AGENTS.md", claude_content)


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="project_test_"))
        self.original_root = project.ROOT
        self.original_agents = project.AGENTS_PATH
        self.original_skills = project.SKILLS_DIR
        project.ROOT = self.tmp
        project.AGENTS_PATH = self.tmp / "AGENTS.md"
        project.SKILLS_DIR = self.tmp / "skills"

    def tearDown(self):
        project.ROOT = self.original_root
        project.AGENTS_PATH = self.original_agents
        project.SKILLS_DIR = self.original_skills
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _setup_minimal_valid(self):
        project.AGENTS_PATH.write_text("# Test AGENTS", encoding="utf-8")
        project.sync_agents()
        (project.SKILLS_DIR / "test-skill").mkdir(parents=True)
        (project.SKILLS_DIR / "test-skill" / "SKILL.md").write_text("# test")

    def test_check_passes_with_valid_state(self):
        self._setup_minimal_valid()
        result = project.Result()
        project.check_agent_sync(result)
        project.check_private_skill_layout(result)
        self.assertTrue(result.ok)

    def test_check_detects_missing_skills_dir(self):
        project.AGENTS_PATH.write_text("# Test", encoding="utf-8")
        project.sync_agents()
        result = project.Result()
        project.check_private_skill_layout(result)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing skills/" in i for i in result.issues))

    def test_check_detects_skill_outside_skills_dir(self):
        (project.SKILLS_DIR).mkdir(parents=True)
        (project.SKILLS_DIR / "legit-skill").mkdir()
        (project.SKILLS_DIR / "legit-skill" / "SKILL.md").write_text("# legit")
        (self.tmp / "rogue-skill").mkdir()
        (self.tmp / "rogue-skill" / "SKILL.md").write_text("# rogue")
        result = project.Result()
        project.check_private_skill_layout(result)
        self.assertFalse(result.ok)
        self.assertTrue(any("outside skills/" in i for i in result.issues))

    def test_check_detects_unsynced_agent_file(self):
        project.AGENTS_PATH.write_text("# Test", encoding="utf-8")
        (self.tmp / "CLAUDE.md").write_text("# stale content")
        result = project.Result()
        project.check_agent_sync(result)
        self.assertFalse(result.ok)
        self.assertTrue(any("not in sync" in i for i in result.issues))

    def test_check_detects_missing_agent_file(self):
        project.AGENTS_PATH.write_text("# Test", encoding="utf-8")
        result = project.Result()
        project.check_agent_sync(result)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing" in i for i in result.issues))


class TestExpectedAgentFiles(unittest.TestCase):
    def test_expected_files_has_claude_and_gemini(self):
        expected = project.expected_agent_files()
        self.assertIn(project.ROOT / "CLAUDE.md", expected)
        self.assertIn(project.ROOT / "GEMINI.md", expected)
        self.assertEqual(len(expected), 2)

    def test_claude_content_differs_from_gemini(self):
        expected = project.expected_agent_files()
        claude = expected[project.ROOT / "CLAUDE.md"]
        gemini = expected[project.ROOT / "GEMINI.md"]
        self.assertNotEqual(claude, gemini)


class TestSelectedSkillTargets(unittest.TestCase):
    def test_all_returns_all_targets(self):
        result = project.selected_skill_targets("all")
        self.assertEqual(set(result.keys()), {"codex", "claude"})

    def test_single_target(self):
        result = project.selected_skill_targets("claude")
        self.assertEqual(list(result.keys()), ["claude"])

    def test_unknown_target_raises(self):
        with self.assertRaises(KeyError):
            project.selected_skill_targets("nonexistent")


class TestSyncUserSkills(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="project_test_"))
        self.original_root = project.ROOT
        self.original_skills = project.SKILLS_DIR
        project.ROOT = self.tmp
        project.SKILLS_DIR = self.tmp / "skills"
        (project.SKILLS_DIR / "test-skill").mkdir(parents=True)
        (project.SKILLS_DIR / "test-skill" / "SKILL.md").write_text("# test")

    def tearDown(self):
        project.ROOT = self.original_root
        project.SKILLS_DIR = self.original_skills
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dry_run_does_not_create_files(self):
        target_dir = self.tmp / "user-skills"
        # Temporarily override the target
        original_targets = project.USER_SKILL_TARGETS
        project.USER_SKILL_TARGETS = {"test": target_dir}
        try:
            rc = project.sync_user_skills("test", dry_run=True)
            self.assertEqual(rc, 0)
            self.assertFalse(target_dir.exists())
        finally:
            project.USER_SKILL_TARGETS = original_targets

    def test_sync_creates_target_directory(self):
        target_dir = self.tmp / "user-skills"
        original_targets = project.USER_SKILL_TARGETS
        project.USER_SKILL_TARGETS = {"test": target_dir}
        try:
            rc = project.sync_user_skills("test", dry_run=False)
            self.assertEqual(rc, 0)
            self.assertTrue(target_dir.is_dir())
            self.assertTrue((target_dir / "test-skill" / "SKILL.md").is_file())
        finally:
            project.USER_SKILL_TARGETS = original_targets

    def test_sync_fails_when_no_skills_exist(self):
        shutil.rmtree(project.SKILLS_DIR)
        target_dir = self.tmp / "user-skills"
        original_targets = project.USER_SKILL_TARGETS
        project.USER_SKILL_TARGETS = {"test": target_dir}
        try:
            rc = project.sync_user_skills("test", dry_run=False)
            self.assertEqual(rc, 1)
        finally:
            project.USER_SKILL_TARGETS = original_targets


if __name__ == "__main__":
    unittest.main(verbosity=2)
