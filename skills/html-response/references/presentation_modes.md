# Presentation Modes

## Selection Rule

Select the smallest mode that makes the user's job meaningfully easier. Do not use dashboards or complex controls when a clear
page and one feedback box are sufficient.

## Mode Matrix

| Mode | Opening viewport | Main units | Interaction | Avoid |
|---|---|---|---|---|
| Brief View | Direct answer and one next step | One compact card | Helpful / Need detail, optional note | TOC, dashboards, decorative metrics |
| Guided Explanation | Summary + key terms / takeaway | Sections, examples, evidence, questions | Mark unclear, ask detail, comment on section | Treating explanation as approval workflow |
| Decision Board | Recommendation + pending decisions | Options, trade-offs, risks, evidence | Select, rank, defer, comment | Hiding decisive risks in details |
| Action Plan | Goal + immediate phase | Steps, owners if known, dependencies, checkpoints | Approve/revise/block step; dependency notes | Presenting unverified execution as committed |
| Evidence Dashboard | Key findings + source status | Metrics, tables, comparisons, assumptions | Challenge evidence, rate confidence, comment | Charts without underlying values |
| Technical Review | Highest-leverage findings | Finding cards, affected areas, code/diagram details | Status, severity, rationale, note per finding | Generic feedback detached from findings |
| Artifact Review | What to inspect and how | Rendered pages/images and annotations | Point/region comment, export | Pixel annotation when semantic comment suffices |
| Mixed Workspace | Artifact + recommendation summary | Preview pane plus review cards | Combined annotations and decisions | Uncoordinated duplicate export channels |

## Shared Section Ordering

For modes with multiple sections, prefer:

1. `Summary` — answer or review objective.
2. `What matters most` — critical decisions/findings/risks.
3. `Evidence or detail` — traceable supporting material.
4. `Next action` — what the user can do or decide.
5. `Feedback` — controls attached to the relevant unit plus export.
6. `Appendix` — raw material, detailed code, large tables, full citations.

## Content Mapping

| Source content | Render as |
|---|---|
| Final answer or recommendation | Prominent summary card, not a banner only |
| Material caution/blocker | Visible warning card near summary |
| Assumptions/unknowns | Explicit assumption list with confidence/status |
| Alternatives | Comparable option cards with aligned criteria |
| Roadmap | Ordered phases with gates, outcomes, rollback/decision points |
| Code/snippets | `<pre><code>` with copy button and explanation outside code |
| Tables | Real HTML table with mobile overflow and plain-language takeaway |
| Citations/source evidence | Source list or evidence references mapped to claims |
| Diagrams | Inline SVG/CSS plus textual explanation/table fallback |
| Very long supporting content | `<details>` with descriptive summary |

## Mode-Specific Feedback Vocabulary

- Brief View: `Helpful`, `Need more detail`, `Incorrect`.
- Guided Explanation: `Clear`, `Unclear`, `Challenge claim`, `Ask follow-up`.
- Decision Board: `Prefer`, `Accept`, `Defer`, `Reject`, `Need evidence`.
- Action Plan: `Approve phase`, `Revise`, `Blocked`, `Dependency missing`, `Risk too high`.
- Evidence Dashboard: `Trust`, `Question source`, `Question method`, `Need breakdown`.
- Technical Review: `Agree`, `False positive`, `Defer`, `Need proof`, `Ready for planning`.
- Artifact Review: free annotation plus optional `Change`, `Question`, `Approve`.

Use only the vocabulary that helps the current review. Avoid forcing every control into every page.
