# Teotis Skills

Teotis 的公开 Codex skill 集合，当前聚焦结构性架构分析、可审阅技术报告和可复用 agent 规划工作流。

[English](README.md)

## Skills

### `abstraction-architect`

**效果：** 发现能删除整类重复模型、适配胶水、边界摩擦和分支复杂度的结构性抽象机会，并输出可审阅的 HTML 架构报告。  
**适配场景：** 适合重复领域表示、转换链过多、API 调用方持续补偿、边界越拆越乱、中心编排越来越重的系统。

### `reviewable-html-report`

**效果：** 为 Mermaid 图、拓扑对比、审阅卡片、本地反馈持久化和可导出的审阅备注提供可复用 HTML 报告机制。  
**适配场景：** 适合分析结论已由其他工作流负责，但需要浏览器可读、易检查、易批注、易交接的技术报告。

### `agent-handoff-planner`

**效果：** 把小型实现想法、外部 agent 发现和验收请求转成可直接执行的 Markdown 分包，适合 1-3 个手动 agent 窗口。  
**适配场景：** 适合轻量委派：先核验说法，再区分 Codex 保留判断和本地实现任务，并把验收标准写成可执行契约。

### `agent-orchestration-planner`

**效果：** 生成完整的多 agent 编排套件，包括分包文档、prompt、依赖图、状态账本和 Claude Code 后台 agent 启动流程。  
**适配场景：** 适合明确的中大型 agent 落地：需要分支/worktree 隔离、DAG 调度、尾部推进和最终集成收口。

## Self Assessment

| Skill | 专项能力 | 自评 | 说明 |
|---|---:|---:|---|
| `abstraction-architect` | 结构洞察与复杂度删除 | 94 / 100 | 强在发现缺失不变量和错误边界；不负责直接落地迁移。 |
| `reviewable-html-report` | 交互式技术报告基础设施 | 92 / 100 | 强在 Mermaid 兼容报告、审阅卡片、本地反馈状态和可导出审阅备注。 |
| `agent-handoff-planner` | 小型分包委派与验收契约 | 91 / 100 | 强在核验后的 1-3 个 agent 分包；刻意不负责批量派工和分支编排。 |
| `agent-orchestration-planner` | 多 agent 执行控制与收口 | 93 / 100 | 强在明确的编排套件；单点修改或轻量 handoff 时会显得过重。 |

## Design Philosophy

架构和报告技能围绕证据优先的协作方式设计：

- `abstraction-architect` 参考现代数学中寻找不变量、结构和统一表示的思维，用工程证据约束抽象，避免为了优雅而优雅。
- `reviewable-html-report` 通过稳定审阅卡片、可读图表和可导出反馈，让密集技术推理更容易检查和交接。

它们不模仿人物，也不把隐喻当结论。真正的标准只有一个：能否让工程判断更有证据、更可审阅、更能安全地转化为行动。

两个 planner skill 把同样的标准用于协作：让 agent 工作边界清楚、可验收、可恢复。轻量 planner 面向人手动控制的分包交接；orchestration planner 只在并发、依赖和集成收口值得单独建执行契约时使用。

## License

Apache License 2.0。详见 [LICENSE](LICENSE)。
