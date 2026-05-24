#!/usr/bin/env python3
"""Export recent Codex user messages and rank possible skill opportunities."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path


TYPE_RULES = [
    ("skill_creation", ["skill", "SKILL.md", "触发", "eval", "评估"]),
    ("architecture_analysis", ["架构", "重构", "技术债", "方案文档", "设计方案", "review"]),
    ("camera_product_design", ["相机", "拍照", "录像", "水印", "夜景", "画质", "闪光", "焦段", "codex_camera"]),
    ("image_workflow", ["图片", "图像", "AIGC", "image", "midjourney", "水印", "EXIF", "xmp"]),
    ("paper_research", ["论文", "paper", "arxiv", "检索", "综述", "引用"]),
    ("writing_editing", ["章节", "小说", "改写", "润色", "剧情", "世界观"]),
    ("lark_workflow", ["飞书", "lark", "Base", "多维表格", "日历", "审批"]),
    ("verification_review", ["验证", "测试", "查验", "审查", "review", "跑一遍"]),
    ("external_agent", ["外部", "agent", "Gemini", "DeepSeek", "Kimi", "友商"]),
]

SKILL_RULES = [
    {
        "name": "camera-product-architect",
        "types": {"camera_product_design"},
        "triggers": ["相机APP功能设计", "拍照/录像方案", "竞品相机能力分析", "水印方案", "夜景/画质/闪光能力设计"],
        "pain": "相机类需求多次要求先研究竞品/平台能力，再输出可落地设计和实现拆分。",
    },
    {
        "name": "codex-history-skill-miner",
        "types": {"skill_creation"},
        "triggers": ["分析历史对话能否沉淀 skill", "导出用户原话", "skill 候选评估", "近一个月 Codex 对话"],
        "pain": "需要反复从 Codex 本地历史中做隐私友好的压缩导出、聚类和候选判断。",
    },
    {
        "name": "paper-research-worker",
        "types": {"paper_research"},
        "triggers": ["检索论文", "论文综述", "paper worker", "arxiv 分析", "提取引用和实验结论"],
        "pain": "论文工作通常包含检索、筛选、摘要、结构化证据和产物验证。",
    },
    {
        "name": "image-metadata-workflow",
        "types": {"image_workflow"},
        "triggers": ["图片批处理", "AIGC 图片整理", "EXIF/XMP", "去水印/加水印", "image_factory"],
        "pain": "图像任务反复出现元数据、批处理、可逆处理和文件组织要求。",
    },
    {
        "name": "longform-writing-operator",
        "types": {"writing_editing"},
        "triggers": ["章节整理", "小说改写", "剧情连续性检查", "长文档润色"],
        "pain": "长文本工作需要保留用户偏好、连续性、审查标准和批量文件流程。",
    },
    {
        "name": "verification-review-runner",
        "types": {"verification_review", "architecture_analysis"},
        "triggers": ["查验", "审查", "验证脚本", "跑测试后给结论", "方案复核"],
        "pain": "用户经常要求可证据化结论，适合沉淀为固定检查清单和输出格式。",
    },
]


def text_from_content(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("input_text") or item.get("output_text")
                if isinstance(text, str):
                    parts.append(text)
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return ""


def compact(text: str, limit: int = 240) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def classify(text: str) -> list[str]:
    found = []
    lowered = text.lower()
    for name, terms in TYPE_RULES:
        for term in terms:
            if term.lower() in lowered:
                found.append(name)
                break
    return found or ["other"]


def parse_rollout(path: str) -> dict:
    user_messages = []
    assistant_messages = []
    function_names = Counter()
    command_text = []
    if not path or not Path(path).exists():
        return {
            "user_messages": [],
            "assistant_final": "",
            "function_names": {},
            "signals": [],
        }

    with Path(path).open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("type") != "response_item":
                continue
            payload = item.get("payload") or {}
            if payload.get("type") == "message":
                role = payload.get("role")
                text = text_from_content(payload.get("content"))
                if role == "user" and text:
                    user_messages.append(text)
                elif role == "assistant" and text:
                    assistant_messages.append(text)
            elif payload.get("type") == "function_call":
                name = payload.get("name") or ""
                if name:
                    function_names[name] += 1
                args = payload.get("arguments")
                if isinstance(args, str):
                    command_text.append(args[:1000])

    joined_commands = "\n".join(command_text)
    signals = []
    if any(name in function_names for name in ["apply_patch", "edit", "write_file"]):
        signals.append("wrote_files")
    if re.search(r"\b(test|pytest|gradlew|npm run|cargo test|swift test|tsc|lint|check)\b", joined_commands, re.I):
        signals.append("ran_verification")
    if "update_plan" in function_names:
        signals.append("created_plan")
    if re.search(r"apply_patch|cat >|tee |write", joined_commands, re.I):
        signals.append("wrote_files")
    if re.search(r"web\.run|search_query|curl|browser|playwright", joined_commands, re.I):
        signals.append("external_lookup_or_browser")

    return {
        "user_messages": user_messages,
        "assistant_final": assistant_messages[-1] if assistant_messages else "",
        "function_names": dict(function_names),
        "signals": sorted(set(signals)),
    }


def load_threads(db_path: Path, cutoff: int) -> list[sqlite3.Row]:
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        select id, created_at, updated_at, cwd, title, first_user_message, rollout_path
        from threads
        where updated_at >= ?
        order by updated_at desc
        """,
        (cutoff,),
    ).fetchall()
    conn.close()
    return rows


def candidate_scores(records: list[dict]) -> list[dict]:
    buckets = defaultdict(list)
    for record in records:
        for task_type in record["task_types"]:
            buckets[task_type].append(record)

    candidates = []
    for rule in SKILL_RULES:
        evidence = []
        for task_type in rule["types"]:
            evidence.extend(buckets.get(task_type, []))
        by_thread = {item["thread_id"]: item for item in evidence}
        evidence = list(by_thread.values())
        cwd_count = Counter(item["cwd"] for item in evidence)
        signal_count = Counter(sig for item in evidence for sig in item["signals"])
        score = len(evidence) + min(5, len(cwd_count)) + signal_count["ran_verification"] + signal_count["created_plan"]
        candidates.append(
            {
                "possible_skill_name": rule["name"],
                "score": score,
                "evidence_count": len(evidence),
                "top_cwds": cwd_count.most_common(5),
                "signals": signal_count.most_common(),
                "skill_trigger_phrases": rule["triggers"],
                "pain_point": rule["pain"],
                "sample_threads": [
                    {
                        "thread_id": item["thread_id"],
                        "date": item["date"],
                        "cwd": item["cwd"],
                        "title": item["title"],
                        "user_preview": item["user_preview"],
                    }
                    for item in sorted(evidence, key=lambda x: x["updated_at"], reverse=True)[:5]
                ],
            }
        )
    return sorted(candidates, key=lambda x: (x["evidence_count"], x["score"]), reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="/Users/dingren/.codex/state_5.sqlite")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--out", default=".tmp/codex_skill_opportunities")
    parser.add_argument("--now", default="2026-05-24T00:00:00+08:00")
    args = parser.parse_args()

    now = dt.datetime.fromisoformat(args.now)
    cutoff_dt = now - dt.timedelta(days=args.days)
    cutoff = int(cutoff_dt.timestamp())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    rows = load_threads(Path(args.db), cutoff)
    records = []
    for row in rows:
        parsed = parse_rollout(row["rollout_path"])
        all_user = "\n".join(parsed["user_messages"]) or row["first_user_message"]
        basis = "\n".join([row["cwd"], row["title"], all_user])
        task_types = classify(basis)
        record = {
            "thread_id": row["id"],
            "date": dt.datetime.fromtimestamp(row["updated_at"]).isoformat(timespec="seconds"),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "cwd": row["cwd"],
            "title": compact(row["title"], 120),
            "first_user_message": compact(row["first_user_message"], 180),
            "user_message_count": len(parsed["user_messages"]),
            "user_messages": [compact(msg, 300) for msg in parsed["user_messages"]],
            "user_preview": compact(all_user, 300),
            "assistant_final_summary": compact(parsed["assistant_final"], 220),
            "signals": parsed["signals"],
            "task_types": task_types,
            "rollout_path": row["rollout_path"],
        }
        records.append(record)

    jsonl_path = out / "threads_user_only.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    csv_path = out / "threads_summary.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "thread_id",
                "date",
                "cwd",
                "title",
                "user_message_count",
                "task_types",
                "signals",
                "user_preview",
                "assistant_final_summary",
            ],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "thread_id": record["thread_id"],
                    "date": record["date"],
                    "cwd": record["cwd"],
                    "title": record["title"],
                    "user_message_count": record["user_message_count"],
                    "task_types": ";".join(record["task_types"]),
                    "signals": ";".join(record["signals"]),
                    "user_preview": record["user_preview"],
                    "assistant_final_summary": record["assistant_final_summary"],
                }
            )

    candidates = candidate_scores(records)
    with (out / "skill_candidates.json").open("w", encoding="utf-8") as fh:
        json.dump(candidates, fh, ensure_ascii=False, indent=2)

    cwd_counts = Counter(item["cwd"] for item in records)
    type_counts = Counter(task_type for item in records for task_type in item["task_types"])
    signal_counts = Counter(sig for item in records for sig in item["signals"])
    report_lines = [
        "# Codex skill opportunity scan",
        "",
        f"- Window: last {args.days} days since {cutoff_dt.isoformat(timespec='seconds')}",
        f"- Threads scanned: {len(records)}",
        f"- JSONL: `{jsonl_path}`",
        f"- CSV: `{csv_path}`",
        "",
        "## Top task types",
        "",
    ]
    report_lines.extend([f"- {name}: {count}" for name, count in type_counts.most_common(12)])
    report_lines.extend(["", "## Top workspaces", ""])
    report_lines.extend([f"- {cwd}: {count}" for cwd, count in cwd_counts.most_common(12)])
    report_lines.extend(["", "## Signals", ""])
    report_lines.extend([f"- {name}: {count}" for name, count in signal_counts.most_common()])
    report_lines.extend(["", "## Candidate skills", ""])
    for candidate in candidates:
        verdict = "strong" if candidate["evidence_count"] >= 10 else "medium" if candidate["evidence_count"] >= 3 else "weak"
        report_lines.extend(
            [
                f"### {candidate['possible_skill_name']} ({verdict})",
                f"- evidence_count: {candidate['evidence_count']}",
                f"- score: {candidate['score']}",
                f"- pain_point: {candidate['pain_point']}",
                f"- triggers: {', '.join(candidate['skill_trigger_phrases'])}",
                f"- top_cwds: {candidate['top_cwds']}",
                "- samples:",
            ]
        )
        for sample in candidate["sample_threads"]:
            report_lines.append(
                f"  - {sample['date']} | {sample['title']} | {sample['user_preview']}"
            )
        report_lines.append("")
    (out / "skill_opportunity_report.md").write_text("\n".join(report_lines), encoding="utf-8")

    print(json.dumps({
        "threads": len(records),
        "out": str(out),
        "top_types": type_counts.most_common(8),
        "top_candidates": [
            {
                "name": item["possible_skill_name"],
                "evidence_count": item["evidence_count"],
                "score": item["score"],
            }
            for item in candidates[:6]
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
