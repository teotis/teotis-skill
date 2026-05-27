# Agent Prompts

## Package: 01-complex-skill-evals - Add eval contracts for complex skills

Copy this prompt into an agent, or let `orchestrate.sh start/advance` launch it for Claude Code.

---

**Mode**: package executor
**INDEX**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/INDEX.md`
**Package doc**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/packages/01-complex-skill-evals.md`
**Coordinator status**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/01-complex-skill-evals.md`
**Coordinator state**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/state.tsv`
**Orchestrator**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh`

You are executing package `01-complex-skill-evals`. Read the INDEX and package doc before changing files. You may edit only the allowed paths in the package doc. Do not edit INDEX.md or another package status file. If you create/use an implementation worktree, do not rely on status files inside that worktree; write the coordinator status path above.

Before calling `advance`, you must:
- Set coordinator status to `completed` or `blocked`.
- Fill evidence: worktree, branch, base commit, commit hash if committed, changed files, verification commands/results, risks.
- Update the machine-readable state row consistently.

Tail step:

```bash
bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance --from 01-complex-skill-evals
```

If your agent platform cannot run local shell commands, report: "completed but advance not run", and tell the user to run:

```bash
bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance
```

---

## Package: 02-tmp-repository-hygiene - Ignore and untrack tmp artifacts

Copy this prompt into an agent, or let `orchestrate.sh start/advance` launch it for Claude Code.

---

**Mode**: package executor
**INDEX**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/INDEX.md`
**Package doc**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/packages/02-tmp-repository-hygiene.md`
**Coordinator status**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/02-tmp-repository-hygiene.md`
**Coordinator state**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/state.tsv`
**Orchestrator**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh`

You are executing package `02-tmp-repository-hygiene`. Read the INDEX and package doc before changing files. You may edit only the allowed paths in the package doc. Do not delete local `.tmp` files; use index-only untracking as directed. Do not edit INDEX.md or another package status file.

Before calling `advance`, you must:
- Set coordinator status to `completed` or `blocked`.
- Fill evidence: worktree, branch, base commit, commit hash if committed, changed files, verification commands/results, risks.
- Update the machine-readable state row consistently.

Tail step:

```bash
bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance --from 02-tmp-repository-hygiene
```

If your agent platform cannot run local shell commands, report: "completed but advance not run", and tell the user to run:

```bash
bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance
```

---

## Package: 03-commit-message-guardrails - Clarify future commit subjects

Copy this prompt into an agent, or let `orchestrate.sh start/advance` launch it for Claude Code.

---

**Mode**: package executor
**INDEX**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/INDEX.md`
**Package doc**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/packages/03-commit-message-guardrails.md`
**Coordinator status**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/03-commit-message-guardrails.md`
**Coordinator state**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/state.tsv`
**Orchestrator**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh`

You are executing package `03-commit-message-guardrails`. Read the INDEX and package doc before changing files. You may edit only the allowed paths in the package doc. Do not rewrite git history. Do not edit INDEX.md or another package status file.

Before calling `advance`, you must:
- Set coordinator status to `completed` or `blocked`.
- Fill evidence: worktree, branch, base commit, commit hash if committed, changed files, verification commands/results, risks.
- Update the machine-readable state row consistently.

Tail step:

```bash
bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance --from 03-commit-message-guardrails
```

If your agent platform cannot run local shell commands, report: "completed but advance not run", and tell the user to run:

```bash
bash /Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh advance
```

---

## Package: 99-finalize - Integrate and verify all packages

Copy this prompt into an agent only after all functional packages are completed, or let `orchestrate.sh advance` launch it after the graph unlocks.

---

**Mode**: package executor
**INDEX**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/INDEX.md`
**Package doc**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/packages/99-finalize.md`
**Coordinator status**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/99-finalize.md`
**Coordinator state**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status/state.tsv`
**Orchestrator**: `/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/launchers/orchestrate.sh`

You are executing package `99-finalize`. Read the INDEX, graph, every package doc, every status file, and `state.tsv`. Do not run finalize if any functional package is not `completed`. Merge only local branches created and recorded by this orchestration, then run the final verification commands in the package doc. Preserve branches/worktrees on failure. Do not force-push, hard reset, delete remote branches, or delete unrecorded local resources.

Before finishing, you must:
- Set coordinator status to `finalized` or `blocked`.
- Fill evidence: integration branch, mainline merge commit if created, verification summary, cleanup results, risks.
- Update the machine-readable state row consistently.
- Write `FINAL_REPORT.md`.

---

