# Teotis Skills

A public Codex skill collection by Teotis, currently focused on structural
architecture analysis, reviewable technical reports, and reusable agent
planning workflows.

[中文版本](README.zh-CN.md)

## Skills

### `abstraction-architect`

**Effect:** Finds structural abstraction opportunities that can remove whole
families of duplicated models, adapters, boundary friction, and branching
complexity, then produces a reviewable HTML architecture report.  
**Best fit:** Systems with repeated domain representations, excessive
conversion chains, caller-side API workarounds, collapsing boundaries, or
growing central orchestration.

### `reviewable-html-report`

**Effect:** Provides the reusable HTML report mechanics for Mermaid diagrams,
topology comparisons, review cards, local feedback persistence, and exportable
review notes.  
**Best fit:** Workflows that already own the analysis but need a browser-readable
technical report that is easier to inspect, annotate, and hand back to another
agent.

### `agent-handoff-planner`

**Effect:** Turns small implementation ideas, external-agent findings, and
validation requests into concrete Markdown handoff packages for one to three
manual agent windows.  
**Best fit:** Lightweight delegation where the important work is verifying
claims, separating Codex-retained judgment from local implementation, and
making acceptance criteria executable.

### `agent-orchestration-planner`

**Effect:** Builds a complete multi-agent orchestration kit with package docs,
prompts, dependency graph, status ledger, and Claude Code background-agent
launcher workflow.  
**Best fit:** Explicit medium or large agent execution where branch/worktree
isolation, DAG scheduling, tail-driven advancement, and final integration need
a written control plane.

## Self Assessment

| Skill | Specialist strength | Score | Note |
|---|---:|---:|---|
| `abstraction-architect` | Structural insight and complexity deletion | 94 / 100 | Strong at missing invariants and wrong boundaries; intentionally does not own rollout planning. |
| `reviewable-html-report` | Interactive technical report infrastructure | 92 / 100 | Strong for Mermaid-safe reports, review cards, local feedback state, and exportable review notes. |
| `agent-handoff-planner` | Small-package delegation and acceptance contracts | 91 / 100 | Strong for verified 1-3 agent handoffs; intentionally avoids batch dispatch and branch orchestration. |
| `agent-orchestration-planner` | Multi-agent execution control and finalization | 93 / 100 | Strong for explicit orchestration kits; overkill when a single local edit or lightweight handoff is enough. |

## Design Philosophy

The architecture and reporting skills are designed around evidence-first
collaboration:

- `abstraction-architect` draws from modern mathematics: the search for
invariants, structures, and unifying representations, constrained here by
engineering evidence so abstraction does not become elegance for its own sake.
- `reviewable-html-report` makes dense technical reasoning inspectable through
stable review cards, readable diagrams, and exportable feedback.

They do not imitate people, and metaphor is never treated as proof. The only
standard is whether the skill makes engineering judgment more evidence-based,
more reviewable, and safer to turn into action.

The two planner skills apply the same standard to collaboration: they make
agent work explicit, bounded, verifiable, and easier to resume. The lightweight
planner is optimized for human-controlled handoff; the orchestration planner is
reserved for cases where concurrency, dependencies, and integration deserve
their own execution contract.

## License

Apache License 2.0. See [LICENSE](LICENSE).
