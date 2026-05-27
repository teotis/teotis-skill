# Orchestration Status

`state.tsv` is the scheduler source of truth. Markdown status files are the human evidence log.

Package agents must update only their assigned status file and row. If a package uses an implementation worktree, it must still write status to this coordinator directory:

`/Volumes/Extreme_SSD/project/teotis_skill/docs/plans/skill-quality-governance-orchestration/status`

Allowed terminal states:

- `completed`
- `blocked`

Intermediate states are managed by `launchers/orchestrate.sh`.

