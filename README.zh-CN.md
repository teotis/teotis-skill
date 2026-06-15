# Teotis Skills

一组聚焦架构分析、工程更新、质量扫雷、可审阅报告和 agent 执行规划的公开 Codex skills。

[English](README.md)

## 技能

| Skill | 适用场景 |
|---|---|
| [`abstraction-architect`](abstraction-architect/) | 基于工程证据寻找能删除重复模型、转换链、边界摩擦和分支复杂度的结构性抽象，并交付一致的 Markdown 与交互式 HTML 报告。 |
| [`renewal-architect`](renewal-architect/) | 围绕主约束、稳定性护栏、采纳经济学和可衡量试点，设计可回滚的遗留系统更新路径，并交付一致的 Markdown 与交互式 HTML 报告。 |
| [`deep-flow-sweep`](deep-flow-sweep/) | 对主流程、稳定性、性能、测试、可观测性、安全、治理、近期改动和后续任务包做高预算、仅分析的质量扫雷。 |
| [`reviewable-html-report`](reviewable-html-report/) | 为浏览器可读的技术报告提供 Mermaid 图、审阅卡片、本地反馈和可导出备注。 |
| [`agent-orchestration-planner`](agent-orchestration-planner/) | 构建带依赖调度、状态跟踪、分支或 worktree 隔离及最终集成的多 agent 执行套件。 |

架构和扫雷技能默认只分析，不直接修改代码。轻量手动执行包使用仓库共享的
Task Package Contract；当并发和集成需要独立控制面时使用 orchestration planner。

## 安装

将所需技能目录复制到 Codex skills 目录，或使用你常用的 Codex skill
安装工具安装本仓库。

## 许可

Apache License 2.0。详见 [LICENSE](LICENSE)。
