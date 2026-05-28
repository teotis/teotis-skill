# 01-complex-skill-evals

## Package ID

`01-complex-skill-evals`

## Goal

Add `evals/evals.json` coverage for the four complex skills that currently lack it:

- `renewal-architect`
- `abstraction-architect`
- `agent-orchestration-planner`
- `html-response`

The evals should act as behavior contracts, not decorative examples.

## Context

- Confirmed finding: only three skills currently have tracked evals: `agent-handoff-planner`, `android-career-interview-coach`, and `math-tutor`.
- Missing coverage is highest-risk for the long and rule-heavy skills.
- Existing eval format uses a JSON object with `skill_name` and an `evals` array. Use the existing style in `skills/math-tutor/evals/evals.json` and `skills/agent-handoff-planner/evals/evals.json` as local precedent.

## File Ownership

- Owns: `skills/renewal-architect/evals/evals.json`
- Owns: `skills/abstraction-architect/evals/evals.json`
- Owns: `skills/agent-orchestration-planner/evals/evals.json`
- Owns: `skills/html-response/evals/evals.json`
- Must not edit any `SKILL.md` unless a syntax or naming mismatch makes the eval impossible to express.

## Allowed Paths

- `skills/renewal-architect/evals/evals.json`
- `skills/abstraction-architect/evals/evals.json`
- `skills/agent-orchestration-planner/evals/evals.json`
- `skills/html-response/evals/evals.json`

## Forbidden Paths

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.gitignore`
- `.tmp/**`
- `public/teotis-skills/**`
- existing eval files for other skills

## Dependencies

- Depends on: none

## Parallel Safety

- safe
- Reason: this package only creates eval files under four skill-specific directories.

## Implementation Scope

Create one eval file per missing skill. Each file should contain 3 to 5 cases:

- one core positive flow;
- one boundary or non-trigger case;
- one safety or authorization case;
- one output-contract case;
- for `html-response`, one simple-answer case where HTML should not be generated.

Recommended coverage:

### renewal-architect

- Legacy modernization analysis produces evidence ledger, capability bottlenecks, pilot recommendation, guardrails, rollback, and owners.
- Rejects grand rewrite when evidence and rollback are absent.
- Separates business capability bottlenecks from architecture narratives.

### abstraction-architect

- Produces analysis only and does not modify code without explicit authorization.
- Requires concrete evidence, counterexamples, transition seam, and disproof signals before calling a proposal validated.
- Rejects false abstraction that only unifies names.

### agent-orchestration-planner

- Triggers only on explicit multi-agent orchestration request.
- Generates a plan with INDEX, packages, graph, state ledger, prompts, `orchestrate.sh`, and `99-finalize`.
- Enforces tail-driven execution, coordinator status outside worktrees, and safe finalize cleanup.
- Does not present `dispatch-claude-agents.sh` as a primary entrypoint.

### html-response

- Keeps trivial responses in chat.
- Generates HTML for dense report/review cases with exportable feedback.
- Requires CSP, accessibility basics, safe localStorage/clipboard fallbacks, stable review IDs, and no unauthorized next-action directive.
- Uses local bundles or partial previews for large artifacts instead of huge single-file embeds.

## Acceptance Criteria

- Four new valid JSON files exist under the four missing skill directories.
- Every file has `skill_name` matching the directory name.
- Every eval includes `prompt`, `expected_output`, `files`, and `assertions`.
- Assertions are specific enough to detect trigger drift, boundary drift, output-contract drift, or authorization drift.
- No existing skill body or existing eval file is modified.

## Verification Commands

```bash
rtk python3 -m json.tool skills/renewal-architect/evals/evals.json
rtk python3 -m json.tool skills/abstraction-architect/evals/evals.json
rtk python3 -m json.tool skills/agent-orchestration-planner/evals/evals.json
rtk python3 -m json.tool skills/html-response/evals/evals.json
rtk python3 control/project.py check
rtk git status --short
```

## Expected Evidence Pack

- [ ] working directory recorded
- [ ] branch name recorded if changed
- [ ] git status clean or explained
- [ ] git diff --stat captured
- [ ] changed files listed
- [ ] verification commands run
- [ ] test results summarized
- [ ] commit hash recorded if committed
- [ ] unresolved risks noted
- [ ] only allowed paths touched

