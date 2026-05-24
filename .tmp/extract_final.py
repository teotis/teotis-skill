#!/usr/bin/env python3
"""Extract and analyze user messages from Gemini Takeout HTML."""

import re
import json

HTML_PATH = "/Volumes/Extreme_SSD/工作数据/AI对话/gemini_web/Takeout/我的活动/Gemini Apps/我的活动记录.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

body_start = content.find('<body')
body = content[body_start:]
entries = re.split(r'<div class="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp">', body)

def clean_html(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

results = []
for i, entry in enumerate(entries[1:], 1):
    # Find the main content cell
    content_match = re.search(
        r'<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.*?)</div>',
        entry, re.DOTALL
    )
    if not content_match:
        continue

    raw = content_match.group(1)

    # Extract user message: between "Prompted" and the date
    user_match = re.search(r'Prompted\s+(.*?)\s*\d{4}年\d{1,2}月\d{1,2}日', raw, re.DOTALL)
    if not user_match:
        # Try alternative: maybe just "Prompted" with content
        user_match = re.search(r'Prompted\s+(.*?)(?:<br|\n)', raw, re.DOTALL)

    user_msg = ""
    if user_match:
        user_msg = clean_html(user_match.group(1))

    # Extract date
    date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2}):(\d{2})', raw)
    date_str = ""
    time_str = ""
    if date_match:
        y, m, d, h, mi, s = date_match.groups()
        date_str = f"{y}-{int(m):02d}-{int(d):02d}"
        time_str = f"{int(h):02d}:{int(mi):02d}"

    # Extract model response (after date, before end of content cell)
    # Response starts after the date line
    if date_match:
        resp_start = date_match.end()
        resp_raw = raw[resp_start:]
        model_msg = clean_html(resp_raw)[:150]  # compressed to 150 chars
    else:
        model_msg = ""

    if user_msg:
        results.append({
            'index': i,
            'date': date_str,
            'time': time_str,
            'user_msg': user_msg,
            'model_msg_preview': model_msg,
        })

# Filter to last 2 months (March-May 2026)
cutoff = "2026-03-20"
recent = [r for r in results if r['date'] >= cutoff]
recent.sort(key=lambda x: (x['date'], x['time']))

print(f"Total entries with user messages: {len(results)}")
print(f"Entries since {cutoff}: {len(recent)}")
print(f"\n{'='*80}")

# Print all recent entries with full user messages
for r in recent:
    print(f"\n[{r['date']} {r['time']}]")
    print(f"用户: {r['user_msg']}")
    print(f"模型摘要: {r['model_msg_preview'][:80]}...")
    print()

# Save to JSON for further analysis
output = []
for r in recent:
    output.append({
        'date': r['date'],
        'time': r['time'],
        'user_message': r['user_msg'],
        'model_preview': r['model_msg_preview'][:100],
    })

with open('/tmp/gemini_user_messages.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(output)} entries to /tmp/gemini_user_messages.json")
