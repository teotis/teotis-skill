# Codex Skill 合集

一组面向 Codex 和 Claude Code 的技能，覆盖工程、研究、学习、求职准备、可审阅交付物，以及可复用的 agent 交接流程。

[English](README.md)

## 仓库模型

本仓库是私有工作区，用于自用技能、实验内容和公开发布前的孵化。限制性对外发布内容放在独立的嵌套 Git 仓库 `public/teotis-skills/` 中。

- 私有技能统一放在 `skills/<skill>/` 下。
- 共享 agent 指导规则统一放在 `AGENTS.md`；`CLAUDE.md`、`GEMINI.md` 是生成出来的薄入口。
- 私有技能可以包含个人工作流、中文说明、未发布行为和本地上下文。
- 公开技能只手动选择一部分发布，且行为可以与私有版不同。
- skill 正文继续使用英语；可见介绍和 frontmatter `description` 可以使用中文，方便调用时识别。
- 公共仓库提供 `README.md` 与 `README.zh-CN.md` 两个版本。

## 技能列表

### `android-career-interview-coach` — Android 求职面试教练

用于准备 Android、移动端、相机 App、客户端、AI 应用或机器人 Android 岗位面试。它会把基础概念和项目经历转成可面试表达的一句话介绍、90 秒回答、技术拆解、模拟问答和岗位匹配策略。

适合：

- Android/Kotlin/Java/C++/JNI/NDK/操作系统/性能面试准备；
- 相机 App、机型适配、客户端架构和稳定性问题；
- 阿里千问/夸克、小米相机、机器人 Android、AI 应用客户端岗位；
- 简历与岗位匹配、可能面试题、公司投递目标分析。

### `math-tutor` — 数学学习助手

用于学习数学、理解公式、证明、定理、微积分、线性代数、概率、函数、算子、对称性或数学截图。它会把低门槛讲解、严谨推导和可选的格罗滕迪克式结构洞察结合起来。

适合：

- “看不懂”“不理解”后的换路讲解；
- 严谨证明和逐步推导；
- 文本或截图中的公式、习题讲解；
- 对数学概念进行本质化、结构化理解。

### `agent-handoff-planner` — Agent 交接方案规划

用于把宽泛需求拆成一个或多个 agent 可以执行的工作包。它会先核验外部 agent 的结论，再区分应由 Codex 保留的高上下文/多模态工作与可委托工作，并输出包含范围、步骤、验收标准和验证命令的 Markdown 实施方案。

适合：

- 核验外部 agent 审查结论；
- 为非多模态 agent 准备 Markdown 交接文档；
- 拆分并行实现任务；
- 按原始方案进行最终验收。

### `html-response` — 自适应 HTML 交付

用于把复杂回答、报告、计划、产物或审查结果转成更适合浏览器阅读和反馈的 HTML。它会选择最低成本但有帮助的展示模式，简单回答仍保留在聊天中；复杂分析、对比、技术审查、文档/图片预览和结构化反馈则生成交互式审阅界面。

适合：

- 长篇报告和技术审查；
- 决策看板和行动计划；
- PDF、文档、图片、渲染 Markdown 等产物审阅；
- 使用稳定条目 ID 收集结构化反馈。

### `abstraction-architect` — 结构抽象架构分析

用于分析复杂度是否来自缺失的不变量、重复的领域表示、不稳定边界、反复出现的适配层、平台分支或中心化编排瓶颈。它关注能够删除整类特殊情况的结构性简化，同时要求代码证据、反例、迁移接缝和可证伪测试。

适合：

- 基础架构审查；
- 领域模型或 API 边界重设计；
- 寻找非增量式的复杂度消除机会；
- 判断某个抽象方案是有效、过早，还是会制造新复杂度。

### `renewal-architect` — 务实演进架构分析

用于在交付、稳定性、组织协作和迁移约束下推进遗留系统更新。它关注可衡量的能力提升、真正限制演进的主瓶颈、可回滚试点、共存迁移策略，以及从小范围验证扩展到系统级更新的路径。

适合：

- 技术债治理；
- 不暂停业务交付的迁移规划；
- 单体拆分、Strangler 或 ACL 边界设计；
- 在复杂系统中寻找最可行的第一个突破点。

## 选择指南

| 需求 | 优先使用 |
|---|---|
| 准备 Android/移动端/相机面试回答和求职策略 | `android-career-interview-coach` |
| 学习数学概念、证明、公式或数学本质 | `math-tutor` |
| 把需求变成可交给 agent 执行的方案 | `agent-handoff-planner` |
| 让复杂交付物更易审阅和反馈 | `html-response` |
| 寻找更深层的结构性简化 | `abstraction-architect` |
| 为遗留系统设计安全演进路径 | `renewal-architect` |

每个私有技能都位于 `skills/<skill>/` 独立目录中，并以 `SKILL.md` 作为入口。

## 指导文件同步

共享仓库规则变化时，只编辑 `AGENTS.md`，然后运行：

```bash
rtk python3 control/project.py sync-agents
rtk python3 control/project.py check
```

私有技能变化后，同步到 Codex 和 Claude 的用户级技能目录：

```bash
rtk python3 control/project.py sync-user-skills
rtk python3 control/project.py check-user-skills
```

也可以使用 `make sync-agents`、`make check`、`make sync-user-skills` 和 `make check-user-skills`。
