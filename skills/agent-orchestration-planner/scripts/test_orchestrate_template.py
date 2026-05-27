#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE = SCRIPT_DIR / "orchestrate-template.sh"


class OrchestrateTemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="orchestrate-template-test-"))
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        self.run_cmd(["git", "init"], cwd=self.repo)
        self.run_cmd(["git", "config", "user.email", "test@example.com"], cwd=self.repo)
        self.run_cmd(["git", "config", "user.name", "Test User"], cwd=self.repo)
        (self.repo / ".gitignore").write_text(".worktrees/\n", encoding="utf-8")
        (self.repo / "README.md").write_text("test repo\n", encoding="utf-8")
        self.run_cmd(["git", "add", ".gitignore", "README.md"], cwd=self.repo)
        self.run_cmd(["git", "commit", "-m", "init"], cwd=self.repo)

        self.plan = self.repo / "docs" / "plans" / "sample-orchestration"
        (self.plan / "launchers").mkdir(parents=True)
        (self.plan / "packages").mkdir()
        (self.plan / "status").mkdir()
        shutil.copy2(TEMPLATE, self.plan / "launchers" / "orchestrate.sh")
        self.make_kit()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def run_cmd(
        self,
        args: list[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        result = subprocess.run(
            args,
            cwd=cwd,
            env=merged_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if check and result.returncode != 0:
            self.fail(
                f"command failed: {args}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def make_kit(self) -> None:
        (self.plan / "INDEX.md").write_text("# Sample\n", encoding="utf-8")
        (self.plan / "packages" / "01-alpha.md").write_text("# Alpha\n", encoding="utf-8")
        (self.plan / "packages" / "02-beta.md").write_text("# Beta\n", encoding="utf-8")
        (self.plan / "packages" / "99-finalize.md").write_text("# Finalize\n", encoding="utf-8")
        for package_id in ("01-alpha", "02-beta", "99-finalize"):
            (self.plan / "status" / f"{package_id}.md").write_text(
                f"# {package_id} Status\n\n## State\n\n`pending`\n",
                encoding="utf-8",
            )
        worktree_base = self.repo / ".worktrees" / "sample-orchestration"
        (self.plan / "launchers" / "package-graph.tsv").write_text(
            "\n".join(
                [
                    "package_id\tpackage_doc\tstatus_file\tdependencies\tdependency_type\twave\tbranch\tworktree\tmanual\tfinalize",
                    f"01-alpha\tpackages/01-alpha.md\tstatus/01-alpha.md\t\tstatus\t1\tagent/sample/01-alpha\t{worktree_base / '01-alpha'}\t0\t0",
                    f"02-beta\tpackages/02-beta.md\tstatus/02-beta.md\t01-alpha\tstatus\t2\tagent/sample/02-beta\t{worktree_base / '02-beta'}\t0\t0",
                    f"99-finalize\tpackages/99-finalize.md\tstatus/99-finalize.md\t01-alpha,02-beta\tstatus+code\tfinal\tagent/sample/99-finalize\t{worktree_base / '99-finalize'}\t0\t1",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (self.plan / "status" / "state.tsv").write_text(
            "\n".join(
                [
                    "package_id\tstate\tlaunched_at\tcompleted_at\tagent\tbranch\tworktree\tbase_commit\tcommit_hash\tverification\tintegration\tcleanup\tlast_error",
                    f"01-alpha\tpending\t\t\t\tagent/sample/01-alpha\t{worktree_base / '01-alpha'}\t\t\tpending\tpending\tpending\t",
                    f"02-beta\tpending\t\t\t\tagent/sample/02-beta\t{worktree_base / '02-beta'}\t\t\tpending\tpending\tpending\t",
                    f"99-finalize\tpending\t\t\t\tagent/sample/99-finalize\t{worktree_base / '99-finalize'}\t\t\tpending\tpending\tpending\t",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (self.plan / "launchers" / "agent-prompts.md").write_text(
            textwrap.dedent(
                f"""
                # Agent Prompts

                ## Package: 01-alpha - Alpha

                Run alpha.

                ## Package: 02-beta - Beta

                Run beta.

                ## Package: 99-finalize - Finalize

                Run finalize.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

    def fake_claude(self, *, logs_ok: bool = True, omit_session: bool = False) -> dict[str, str]:
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir(exist_ok=True)
        script = bin_dir / "claude"
        script.write_text(
            textwrap.dedent(
                f"""\
                #!/usr/bin/env bash
                set -euo pipefail
                case "${{1:-}}" in
                  --version)
                    echo "2.1.142 (fake)"
                    ;;
                  logs)
                    if [ "{'1' if logs_ok else '0'}" = "1" ]; then
                      echo "fake logs for $2"
                    else
                      echo "job not found" >&2
                      exit 1
                    fi
                    ;;
                  --bg)
                    if [ "{'1' if omit_session else '0'}" = "1" ]; then
                      echo "backgrounded"
                    else
                      echo "backgrounded fake-session-123"
                    fi
                    ;;
                  *)
                    echo "unexpected claude args: $*" >&2
                    exit 2
                    ;;
                esac
                """
            ),
            encoding="utf-8",
        )
        script.chmod(script.stat().st_mode | stat.S_IEXEC)
        return {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}

    def orchestrate(self, *args: str, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.run_cmd(
            ["bash", str(self.plan / "launchers" / "orchestrate.sh"), *args],
            cwd=self.repo,
            env=env,
            check=check,
        )

    def test_status_rejects_malformed_state(self) -> None:
        (self.plan / "status" / "state.tsv").write_text(
            "package_id\tstate\n01-alpha\tpending\n",
            encoding="utf-8",
        )
        result = self.orchestrate("status", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid state header", result.stderr)

    def test_start_records_session_id_and_creates_worktree(self) -> None:
        result = self.orchestrate("start", env=self.fake_claude())
        self.assertEqual(result.returncode, 0)
        self.assertIn("fake-session-123", (self.plan / "status" / "state.tsv").read_text())
        self.assertTrue((self.repo / ".worktrees" / "sample-orchestration" / "01-alpha").exists())
        self.assertTrue((self.plan / "status" / "launch-01-alpha.log").exists())

    def test_unreadable_logs_mark_package_stale(self) -> None:
        result = self.orchestrate("start", env=self.fake_claude(logs_ok=False), check=False)
        self.assertNotEqual(result.returncode, 0)
        state = (self.plan / "status" / "state.tsv").read_text(encoding="utf-8")
        self.assertIn("01-alpha\tstale\t", state)
        self.assertIn("logs are not readable", state)

    def test_missing_session_id_marks_package_invalid(self) -> None:
        result = self.orchestrate("start", env=self.fake_claude(omit_session=True), check=False)
        self.assertNotEqual(result.returncode, 0)
        state = (self.plan / "status" / "state.tsv").read_text(encoding="utf-8")
        self.assertIn("01-alpha\tinvalid\t", state)
        self.assertIn("missing background session id", state)

    def test_mark_state_unlocks_downstream_only_after_completed(self) -> None:
        self.orchestrate("mark-state", "01-alpha", "completed", "--commit", "abc123", "--verification", "unit: pass")
        result = self.orchestrate("advance", env=self.fake_claude())
        self.assertEqual(result.returncode, 0)
        state = (self.plan / "status" / "state.tsv").read_text(encoding="utf-8")
        self.assertIn("02-beta\tlaunched\t", state)

    def test_retry_only_accepts_bad_terminal_states(self) -> None:
        result = self.orchestrate("retry", "01-alpha", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("retry only supports", result.stderr)
        self.orchestrate("mark-state", "01-alpha", "blocked", "--error", "test blocker")
        result = self.orchestrate("retry", "01-alpha", env=self.fake_claude())
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
