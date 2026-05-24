# Skill opportunity recommendation

Scan window: 2026-04-24 to 2026-05-24.

Data used: 245 non-subagent Codex App threads from `state_5.sqlite`; rollout JSONL was parsed for user messages only, plus short final assistant summary and coarse action signals.

## Output artifacts

- `threads_user_only.jsonl`: one compact JSON object per thread.
- `threads_summary.csv`: spreadsheet-friendly thread summary.
- `skill_candidates.json`: heuristic candidate scores.
- `skill_opportunity_report.md`: raw grouped report.

## Strongest recommendation

Build a new skill tentatively named `agent-handoff-planner`.

Why:

- Direct evidence appears in 33 threads with phrases like "输出一份或多份 md 格式的方案文档", "转给其他非多模态 agent", "并行处理", and "实现落地".
- It appears together with adjacent repeated patterns: validation/acceptance in 34 threads, external-agent review/checking in 22 threads, competitor or internet research in 27 threads, and multimodal gating in 45 threads.
- The workflow is stable across different projects: inspect context, verify external claims, identify parts that require Codex/multimodal judgment, split the rest into handoff-ready implementation docs, then later validate the result.
- This is more reusable than a narrow camera or image skill because it captures the user's preferred orchestration style.

Suggested triggers:

- "输出 md 方案文档给其他 agent"
- "非多模态 agent 并行处理"
- "你负责最难的 10% / 多模态限定部分"
- "外部 agent 审查结论，核验后拆方案"
- "交付其他 agent 实现落地，你验收"

Expected behavior:

1. Read local context and existing docs before proposing work.
2. Separate user-visible goal, known evidence, assumptions, and unresolved risks.
3. Verify external-agent claims before accepting them.
4. Identify work that needs multimodal or high-context judgment and keep that with Codex.
5. Split remaining work into one or more self-contained Markdown handoff docs.
6. Each handoff doc should include scope, files to inspect, implementation steps, acceptance criteria, and verification commands.
7. If asked to验收, compare implementation against the original handoff doc and report gaps first.

Historical eval prompts:

1. "该项目中，外部agent审查，认为存在如下问题。你核验一下，如果认可，则分析设计执行方案，输出一份或多份 md 格式的方案文档，以便直接转给其他一个或多个非多模态 agent 处理，实现落地。"
2. "根据过往会话纪录，总结用户需求和项目定位，然后针对任务全面审查完整度，分析设计执行方案。你负责最有难度的 10% 和多模态限定工作，剩余部分按领域输出多份 md 方案文档给其他 agent 并行处理。"
3. "需求单：当前还没有实现横竖模式的恰当切换。可以参考 Apple/Oppo/Vivo 的成熟处理。分析设计执行方案，输出 md 文档，交付其他 agent 实现落地，之后你验收。"

## Other viable candidates

`camera-product-architect`: strong domain evidence, especially in `codex_camera` with 68 classified threads. Good if you expect the camera project to continue. It should encode Apple/Vivo/Oppo comparison, Android feasibility, mode-level UX, and implementation handoff.

`image-prompt-factory`: 50 threads matched image-generation/prompt-document workflows, mostly in `image_factory` and Study/Image contexts. Worth building if the desired workflow is stable enough around character realism, prompt docs, batch generation, and quality review.

`codex-history-skill-miner`: useful, but only 2 direct recent requests plus related history-analysis patterns. Build it if this local-history mining becomes a recurring maintenance task; otherwise keep the current script as a lightweight tool.

## Recommendation

Create `agent-handoff-planner` first. It gives the broadest reuse and would also improve future camera, image, paper, and architecture tasks. Then use the three historical prompts above as the first eval set.
