# Teotis Skills

给需要先判断、再行动的 coding agents 使用的架构与执行技能集。

这套 skills 面向的不是“直接改一行代码”的场景，而是那些贸然动手会出事的工程任务：架构压力、遗留系统更新、发布前风险扫雷、密集技术报告、多 agent 执行规划。它们帮助 agent 把混乱代码库转化为证据、选择、报告和可控下一步。

[English](README.md)

## 一句话版本

当你希望 agent 做这些事时，可以使用 Teotis Skills：

- 找到真实结构压力，而不是套一个流行模式名；
- 区分“代码难看”和“业务兼容性真的不能破”；
- 在决定修什么之前，先扫主流程和发布风险；
- 交付人能审阅的报告，而不是一大段 chat 文本；
- 用 ledger、任务包边界和最终验证来协调多 agent 工作。

默认立场很保守：先分析再修改，先证据再结论，先交接边界再执行。

## 为什么需要这些 skills

Coding agents 做局部修改很快，这很有用，但也会放大几类失败：

| 失败模式 | 常见问题 | Teotis 的回应 |
|---|---|---|
| 架构诊断太浅 | agent 看到重复代码就发明抽象，还没证明真正的不变量。 | `abstraction-architect` 强制先比较“无需新抽象”的基线，再做候选竞争、反例和证据支撑。 |
| 遗留系统现代化变成表演 | agent 提迁移路线，却没有证明采纳成本、回滚路径和稳定性底线。 | `renewal-architect` 把现代化落到可回滚试点和决策门。 |
| 发布风险藏在真实流程里 | agent 看了文件，但漏掉主流程失败、陈旧测试、可观测性缺口和历史闭环。 | `deep-flow-sweep` 先建立流程、风险、证据和后续任务包，再谈修复。 |
| 报告难审阅 | 结论困在长聊天记录或扁平 Markdown 里。 | `reviewable-html-report` 提供浏览器可读报告机制：目录、图示、卡片、反馈和导出。 |
| 多 agent 工作失控 | 后台 agent 各说各的完成，没有一个 artifact 拥有真实状态。 | `agent-orchestration-planner` 生成任务包、DAG 状态、事件 ledger 和最终集成契约。 |

## 技能组合

### [`abstraction-architect`](abstraction-architect/)

用于结构性架构分析：当复杂度可能来自缺失不变量、重复领域模型、不稳定边界、转换链、平台分支或分散流程状态。

- **设计目标：** 发现能删除整类 adapter、mode、projection 和流程漂移的结构模型。
- **预期效果：** 交付可审阅架构报告，包含压力地图、proposal ID、准入检查、被拒候选、未知项和迁移交接。
- **适合时机：** 你怀疑代码库真正缺的是不变量，而不只是局部清理。

### [`renewal-architect`](renewal-architect/)

用于遗留系统和长期技术债：难点不只是目标设计，而是在业务不能停的情况下如何演进。

- **设计目标：** 找出主约束，并设计可回滚的第一个突破口。
- **预期效果：** 交付 renewal decision report，包含事实账本、稳定性底线、采纳经济学、保护/实验/延后拆分和试点决策契约。
- **适合时机：** 现代化、兼容、owner、交付压力和回滚需要同时考虑。

### [`deep-flow-sweep`](deep-flow-sweep/)

用于对主流程、发布面、稳定性、测试、可观测性、安全、治理、历史和后续任务包做高预算、仅分析的质量扫雷。

- **设计目标：** 在决定修什么之前，先找到项目在真实使用中会在哪里失败。
- **预期效果：** 产出风险地图、证据、严重度、覆盖债、历史闭环、验证缺口和后续任务包。
- **适合时机：** 发布前、大合并前、bug bash 前、架构推进前，或需要判断“先修什么”。

### [`reviewable-html-report`](reviewable-html-report/)

用于把已经形成的分析转成浏览器可读的 artifact。

- **设计目标：** 为密集技术报告提供可复用的 HTML 机制。
- **预期效果：** 产出稳定章节、Mermaid fallback、审阅卡片、本地反馈和导出机制。
- **适合时机：** 分析已经有了，但需要从 chat 变成可审阅界面。

### [`agent-orchestration-planner`](agent-orchestration-planner/)

用于明确的中大型多 agent 执行请求：并发和集成需要自己的控制面。

- **设计目标：** 把多 agent 工作转成任务边界、DAG 状态、事件 ledger 和收尾规则。
- **预期效果：** 产出任务 prompts、状态文件、重试/收尾行为和可合入证据。
- **适合时机：** 多个后台 agent、worktree、依赖关系和最终集成都必须被有意识地协调。

## 理念

**证据优先于优雅。** 说不出支持文件、流程、测试、日志或约束的设计，只能算假设，不能算建议。

**好架构经常是删除工作。** 任何新抽象的第一个竞争者都是“不新增抽象”：删掉过时分支、合并局部重复、改善文案，或在证据表明稳定时保持现状。

**遗留系统携带真实契约。** 老代码不天然错误。关键是分清什么必须保护，什么可以安全实验，什么要等试点产出缺失事实再决定。

**报告应该降低理解成本。** 密集分析应该先给答案，再用可导航结构展开证据、图示、权衡、未知项和审阅控件。

**编排需要真实账本。** 多 agent 同时工作时，状态必须落在显式 artifact 里，而不是靠乐观总结。

## 快速开始

1. 选择你需要的 skill 目录。
2. 将该目录复制到你的 agent skills 目录，或用支持 GitHub skill source 的安装器安装本仓库。
3. 在 agent 会话中按名称调用 skill。

示例：

```text
Use abstraction-architect on this repo. I want an architecture report, not code changes yet.
```

```text
Run deep-flow-sweep for the release-critical flows and package the top follow-up tasks.
```

```text
Use agent-orchestration-planner to split this migration into background agent packages.
```

每个 skill 的 `SKILL.md` 都是自包含入口。公开包里的 `references/` 和 `scripts/` 只在该 skill 需要它们维持 Portable Core 时才随包发布。

## 一次好的运行应该长什么样

| 输出 | 你应该看到什么 |
|---|---|
| 架构或 renewal 报告 | 保存的 HTML 路径、可点击 `file://` URL、命名证据、显式未知项；除非再次授权，不改代码。 |
| Deep sweep | 带覆盖说明的 findings、风险/严重度、验证缺口，以及适合后续 agent 执行的任务包。 |
| 可审阅 HTML | 自包含 HTML、稳定 section ID、可读图示 fallback、反馈/导出机制。 |
| 编排套件 | `INDEX.md`、任务包 prompts、`package-graph.tsv`、`state.tsv`、`events.jsonl`、包状态文件和最终收尾契约。 |

## 自我评估

**擅长：**

- evidence-first 架构分析；
- 把模糊工程不安转成可审阅 artifact；
- 区分分析、试点设计、执行和 handoff；
- 在 agent-heavy 工作中保留人的控制权；
- 产出比原始 chat 更容易检查的报告。

**不适合：**

- 一行能修的小 bug；
- 下一步实现已经非常明确的任务；
- 替代项目自己的测试、遥测或产品判断；
- 用自信措辞掩盖不确定性。

**成熟度说明：** 这些 skills 是强观点、实用取向的工程纪律，但仍在演进。最好的使用方式是把它们当作可复用方法，批判性检查输出，并按你自己团队的词汇继续改造。

## 许可

Apache License 2.0。详见 [LICENSE](LICENSE)。
