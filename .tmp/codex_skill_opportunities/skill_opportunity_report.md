# Codex skill opportunity scan

- Window: last 30 days since 2026-04-24T00:00:00+08:00
- Threads scanned: 303
- JSONL: `.tmp/codex_skill_opportunities/threads_user_only.jsonl`
- CSV: `.tmp/codex_skill_opportunities/threads_summary.csv`

## Top task types

- external_agent: 300
- verification_review: 248
- architecture_analysis: 210
- lark_workflow: 191
- image_workflow: 175
- skill_creation: 151
- paper_research: 112
- camera_product_design: 103
- writing_editing: 98
- other: 1

## Top workspaces

- /Volumes/Extreme_SSD/project/codex_camera: 87
- /Volumes/Extreme SSD/codex/image_factory: 40
- /Volumes/Extreme_SSD/codex/image_factory: 29
- /Volumes/Extreme_SSD/project/paper_worker: 23
- /Volumes/Extreme SSD/codex/Study_codex: 22
- /Volumes/Extreme SSD/codex/Thought_codex: 20
- /Volumes/Extreme SSD/codex/JN_codex: 17
- /Volumes/Extreme_SSD/codex/paper_worker: 16
- /Volumes/Extreme SSD/Study_codex: 13
- /Volumes/Extreme_SSD/codex/Study_codex: 8
- /Volumes/Extreme_SSD/codex/New_Camera: 7
- /Volumes/Extreme_SSD/codex/agent_project_seed: 7

## Signals

- ran_verification: 107
- created_plan: 54
- wrote_files: 29
- external_lookup_or_browser: 13

## Candidate skills

### verification-review-runner (strong)
- evidence_count: 249
- score: 382
- pain_point: 用户经常要求可证据化结论，适合沉淀为固定检查清单和输出格式。
- triggers: 查验, 审查, 验证脚本, 跑测试后给结论, 方案复核
- top_cwds: [('/Volumes/Extreme_SSD/project/codex_camera', 86), ('/Volumes/Extreme_SSD/codex/image_factory', 29), ('/Volumes/Extreme_SSD/project/paper_worker', 23), ('/Volumes/Extreme SSD/codex/Study_codex', 20), ('/Volumes/Extreme SSD/codex/Thought_codex', 20)]
- samples:
  - 2026-05-24T11:30:20 | 基于codex app中近一个月内的历史对话信息，用于分析是否可以构建新的skill。如下是友商推荐的流程，我的要求是注意节省token，因为近一个月内的数据可能比较大，重点是用户说了什么，模型回复是比较次要的，甚至前一百字这样的压缩也许… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/skill <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Skill Collection A curated set of Codex skills for enhanced engineering workflows. ## Project Structure Each skill lives in its own directory with a `SKILL.md`…
  - 2026-05-24T11:18:10 | 我希望将codex app中近一个月内的历史对话信息的用户说话导出，用于分析是否可以构建新的skill。该如何处理 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:52:16 | 研究可去水印功能的实现方案。我的初步想法是，写一段脚本处理，前提是在jpg中添加关于水印位置，水印区域原图（稍大）的数据（在xmp，或者别的什么地方），需要去水印时恰当覆盖即可。你也可以参考apple，vivo之类的实现，或者你是否更好的… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:50:07 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:48:21 | [$superpowers:using-superpowers](/Users/dingren/.codex/.tmp/plugins/plugins/superpowers/skills/using-superpowers/SKILL.… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…

### image-metadata-workflow (strong)
- evidence_count: 175
- score: 268
- pain_point: 图像任务反复出现元数据、批处理、可逆处理和文件组织要求。
- triggers: 图片批处理, AIGC 图片整理, EXIF/XMP, 去水印/加水印, image_factory
- top_cwds: [('/Volumes/Extreme SSD/codex/image_factory', 40), ('/Volumes/Extreme_SSD/project/codex_camera', 34), ('/Volumes/Extreme_SSD/codex/image_factory', 29), ('/Volumes/Extreme_SSD/project/paper_worker', 23), ('/Volumes/Extreme_SSD/codex/paper_worker', 16)]
- samples:
  - 2026-05-24T10:52:16 | 研究可去水印功能的实现方案。我的初步想法是，写一段脚本处理，前提是在jpg中添加关于水印位置，水印区域原图（稍大）的数据（在xmp，或者别的什么地方），需要去水印时恰当覆盖即可。你也可以参考apple，vivo之类的实现，或者你是否更好的… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:50:07 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T04:32:23 | 设计多种水印方案 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T04:03:43 | 实现拍照录像与模式优化 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T03:56:46 | 检索互联网，根据apple，vivo，oppo顶配旗舰机型的相机APP功能设计，分析当前该项目中，各个模式应增加的功能和能力（重点考虑可行性，用户价值） | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…

### codex-history-skill-miner (strong)
- evidence_count: 151
- score: 235
- pain_point: 需要反复从 Codex 本地历史中做隐私友好的压缩导出、聚类和候选判断。
- triggers: 分析历史对话能否沉淀 skill, 导出用户原话, skill 候选评估, 近一个月 Codex 对话
- top_cwds: [('/Volumes/Extreme_SSD/project/codex_camera', 35), ('/Volumes/Extreme_SSD/project/paper_worker', 23), ('/Volumes/Extreme SSD/codex/Study_codex', 20), ('/Volumes/Extreme SSD/codex/Thought_codex', 19), ('/Volumes/Extreme SSD/codex/JN_codex', 17)]
- samples:
  - 2026-05-24T11:30:20 | 基于codex app中近一个月内的历史对话信息，用于分析是否可以构建新的skill。如下是友商推荐的流程，我的要求是注意节省token，因为近一个月内的数据可能比较大，重点是用户说了什么，模型回复是比较次要的，甚至前一百字这样的压缩也许… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/skill <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Skill Collection A curated set of Codex skills for enhanced engineering workflows. ## Project Structure Each skill lives in its own directory with a `SKILL.md`…
  - 2026-05-24T11:18:10 | 我希望将codex app中近一个月内的历史对话信息的用户说话导出，用于分析是否可以构建新的skill。该如何处理 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:50:07 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:48:21 | [$superpowers:using-superpowers](/Users/dingren/.codex/.tmp/plugins/plugins/superpowers/skills/using-superpowers/SKILL.… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T04:32:23 | 设计多种水印方案 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…

### paper-research-worker (strong)
- evidence_count: 112
- score: 174
- pain_point: 论文工作通常包含检索、筛选、摘要、结构化证据和产物验证。
- triggers: 检索论文, 论文综述, paper worker, arxiv 分析, 提取引用和实验结论
- top_cwds: [('/Volumes/Extreme_SSD/project/paper_worker', 23), ('/Volumes/Extreme SSD/codex/JN_codex', 17), ('/Volumes/Extreme_SSD/codex/paper_worker', 16), ('/Volumes/Extreme_SSD/project/codex_camera', 15), ('/Volumes/Extreme SSD/codex/Study_codex', 14)]
- samples:
  - 2026-05-24T03:56:46 | 检索互联网，根据apple，vivo，oppo顶配旗舰机型的相机APP功能设计，分析当前该项目中，各个模式应增加的功能和能力（重点考虑可行性，用户价值） | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-23T10:24:31 | 该项目中，外部agent审查，认为存在如下问题。你核验一下，如果认可，则分析设计优化方案，输出一份或多份的md格式的方案文档，以便直接转给其他一个或多个非多模态的 agent 处理，实现具体落地。外部agent审查结论：MainActiv… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-23T10:23:54 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-23T10:23:38 | 该项目中，外部agent审查，认为存在如下问题。你核验一下，如果认可，则分析设计优化方案，输出一份或多份的md格式的方案文档，以便直接转给其他一个或多个非多模态的 agent 处理，实现具体落地。外部agent审查结论：Effect-De… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-23T10:22:24 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…

### camera-product-architect (strong)
- evidence_count: 103
- score: 172
- pain_point: 相机类需求多次要求先研究竞品/平台能力，再输出可落地设计和实现拆分。
- triggers: 相机APP功能设计, 拍照/录像方案, 竞品相机能力分析, 水印方案, 夜景/画质/闪光能力设计
- top_cwds: [('/Volumes/Extreme_SSD/project/codex_camera', 87), ('/Volumes/Extreme_SSD/codex/paper_worker', 5), ('/Volumes/Extreme_SSD/codex/image_factory', 4), ('/Volumes/Extreme_SSD/project/paper_worker', 2), ('/Volumes/Extreme_SSD/codex/New_Camera', 2)]
- samples:
  - 2026-05-24T11:18:10 | 我希望将codex app中近一个月内的历史对话信息的用户说话导出，用于分析是否可以构建新的skill。该如何处理 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:52:16 | 研究可去水印功能的实现方案。我的初步想法是，写一段脚本处理，前提是在jpg中添加关于水印位置，水印区域原图（稍大）的数据（在xmp，或者别的什么地方），需要去水印时恰当覆盖即可。你也可以参考apple，vivo之类的实现，或者你是否更好的… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:50:07 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T10:48:21 | [$superpowers:using-superpowers](/Users/dingren/.codex/.tmp/plugins/plugins/superpowers/skills/using-superpowers/SKILL.… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-24T04:32:23 | 设计多种水印方案 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…

### longform-writing-operator (strong)
- evidence_count: 98
- score: 150
- pain_point: 长文本工作需要保留用户偏好、连续性、审查标准和批量文件流程。
- triggers: 章节整理, 小说改写, 剧情连续性检查, 长文档润色
- top_cwds: [('/Volumes/Extreme_SSD/project/paper_worker', 23), ('/Volumes/Extreme SSD/codex/Thought_codex', 20), ('/Volumes/Extreme SSD/codex/JN_codex', 17), ('/Volumes/Extreme_SSD/codex/paper_worker', 15), ('/Volumes/Extreme_SSD/codex/image_factory', 5)]
- samples:
  - 2026-05-22T17:35:10 | 优化项目相关简历文案 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/paper_worker <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # AGENTS.md This file provides guidance to Codex (Codex.ai/code) when working with code in this repository. ## 项目概述 paper_worker — 文件处理助手，当前聚焦简历管理。解析现有简历（.docx/…
  - 2026-05-22T07:56:56 | 最新版apk真机实测发现的问题。1，拍照以后，缩略图无水印跳变有水印，应当一开始就有水印。2，横屏未适配（我建议UI布局不变，按钮/文字旋转，预览框横屏化）。3，构图网格效果不佳，包括UI显示效果，包括线条分布效果（针对实际成像的预览区域… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/codex_camera <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # Codex Initialization This repository is an Android/Kotlin camera project named `OpenCamera`. Treat it as a Claude Code project that has been initialized for C…
  - 2026-05-22T00:04:52 | 介绍你自己 | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/paper_worker <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # AGENTS.md This file provides guidance to Codex (Codex.ai/code) when working with code in this repository. ## 项目概述 paper_worker — 文件处理助手，当前聚焦简历管理。解析现有简历（.docx/…
  - 2026-05-21T13:34:26 | [$superpowers:systematic-debugging](/Users/dingren/.codex/.tmp/plugins/plugins/superpowers/skills/systematic-debugging/… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/paper_worker <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # AGENTS.md This file provides guidance to Codex (Codex.ai/code) when working with code in this repository. ## 项目概述 paper_worker — 文件处理助手，当前聚焦简历管理。解析现有简历（.docx/…
  - 2026-05-21T13:33:51 | The following is the Codex agent history whose request action you are assessing. Treat the transcript, tool call argume… | # AGENTS.md instructions for /Volumes/Extreme_SSD/project/paper_worker <INSTRUCTIONS> 更新 @/Users/dingren/.codex/RTK.md --- project-doc --- # AGENTS.md This file provides guidance to Codex (Codex.ai/code) when working with code in this repository. ## 项目概述 paper_worker — 文件处理助手，当前聚焦简历管理。解析现有简历（.docx/…
