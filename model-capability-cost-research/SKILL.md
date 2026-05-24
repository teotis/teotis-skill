---
name: model-capability-cost-research
description: 用于比较 AI 模型、厂商、API 路线、coding-agent 后端、多模态能力、token 价格、缓存折扣、榜单排名、模型命名和性价比；覆盖 Codex、Claude Code、Gemini CLI、OpenCode、Qwen、DeepSeek、Kimi、Mimo、GPT、Anthropic、百度千帆等。Use for current model capability, pricing, and cost-performance research.
---

# Model Capability Cost Research

## Mission

Help the user choose AI models and vendors for real workflows by comparing capability, reliability, integration fit, and normalized cost. Treat model information as time-sensitive: verify current facts before making recommendations.

This skill is for practical selection, not leaderboard theater. A good answer tells the user which option to use for a specific job, what evidence supports it, what is uncertain, and what would change the recommendation.

## When To Use

Use this skill for requests involving:

- model comparisons such as GPT, Claude, Gemini, Qwen, DeepSeek, Kimi, Mimo, GLM, Qianfan, or router platforms;
- Claude Code, Codex App, Gemini CLI, OpenCode, Cursor, or agent backend choices;
- coding ability, large-repo reasoning, tool use, Chinese UI/document understanding, multimodal perception, image/PPT/layout review, or long-context work;
- token pricing, cached input pricing, output pricing, exchange rates, reseller packages, subscription plans, or cost-performance rankings;
- "latest", "current", "authoritative benchmark", "ranking", "calling model name", or "which is best value".

Do not use this skill for a simple explanation of what a model is unless the user asks for a decision or comparison.

## Research Discipline

Model names, prices, context windows, benchmarks, and product availability change quickly. Browse or otherwise verify current information before answering when the request depends on any of these facts.

Prefer primary and recent sources:

- official pricing pages, model cards, API docs, changelogs, and release notes;
- respected benchmark projects with dated methodology;
- public eval reports that describe task setup clearly;
- the user's own logs, bills, prompts, and workflow constraints.

Treat social posts, reseller claims, and benchmark charts without methodology as weak evidence. Use them only as leads or market signals.

## Workflow

### 1. Define the decision

Extract:

- target workflow: coding agent, UI review, document reading, image understanding, search/research, translation, writing, or mixed work;
- environment: Codex App, Claude Code, Gemini CLI, OpenCode, direct API, router, or web app;
- constraints: budget, speed, privacy, quota, region, language, multimodal need, long context, tool support, and tolerance for setup friction;
- candidate models and any user-supplied pricing assumptions.

If the user gives partial pricing such as "8 RMB for 700M tokens", preserve it as a user-supplied assumption and normalize it separately from official prices.

### 2. Verify current facts

For each serious candidate, collect:

- exact model name or API identifier;
- release or documentation date when available;
- context length and modality support;
- input, cached input, and output prices;
- important usage limits, routing caveats, or subscription restrictions;
- benchmark evidence relevant to the user's workflow.

When facts conflict, show the conflict and favor the source with clearer provenance.

### 3. Normalize costs

Convert costs to the same unit before comparing. Use:

- per 1M input tokens;
- per 1M cached input tokens when the provider distinguishes cache hits;
- per 1M output tokens;
- blended scenario costs for the user's workload.

For agentic coding, include at least two scenario baskets when data allows:

| Scenario | Typical shape |
|---|---|
| Cache-heavy repo iteration | large repeated input, high cache hit rate, moderate output |
| Fresh research or one-shot analysis | uncached input, more browsing/synthesis, moderate output |
| Long implementation loop | repeated repo context plus long tool transcripts and patches |

Do not collapse everything into one "cheap/expensive" label when cached input and output prices point in different directions.

### 4. Compare capabilities by workflow

Rank only on dimensions that matter for the user:

- coding-agent reliability: instruction following, tool use, large diff discipline, test/debug loops;
- large-repo reasoning: architecture understanding, long-context use, avoiding shallow edits;
- multimodal: Chinese UI screenshots, document images, PPT/layout judgment, chart/table reading;
- Chinese technical understanding: terminology, mixed Chinese-English prompts, local ecosystem knowledge;
- latency and stability: speed, outages, rate limits, retry behavior;
- integration fit: whether the model is actually usable in the named app or CLI.

Avoid saying a model is "best" globally. State "best for this scenario".

### 5. Produce a decision report

Use this structure unless the user asks for another format:

```markdown
## Recommendation
[Top 1-3 choices with when to use each.]

## Assumptions
[User-supplied prices, exchange rate, workload shape, missing facts.]

## Evidence Table
| Model | Access route | Current price | Relevant capability evidence | Caveats |

## Cost Normalization
| Scenario | Model A | Model B | Model C | Notes |

## Workflow Fit
[Short comparison by coding, multimodal, Chinese UI/docs, long context, reliability.]

## Decision
[Practical choice, fallback choice, and what would change the recommendation.]
```

For high-uncertainty answers, add "What I would verify next" rather than overstating confidence.

## Common Mistakes

- Using an old benchmark or price table without checking dates.
- Comparing only input token price while ignoring output and cached-input pricing.
- Recommending a model that is strong in chat but not available or stable in the user's actual agent environment.
- Treating reseller token packages as equivalent to official API access without noting routing, account, quota, and reliability risk.
- Ranking by aggregate benchmark score when the user needs a narrower workflow such as Chinese UI screenshot review or large Android repo editing.
