#!/usr/bin/env python3
"""Extract user messages from Gemini Takeout HTML."""

import re
from datetime import datetime

HTML_PATH = "/Volumes/Extreme_SSD/工作数据/AI对话/gemini_web/Takeout/我的活动/Gemini Apps/我的活动记录.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find body content
body_start = content.find('<body')
body = content[body_start:]

# Split by outer-cell divs - each represents one conversation
entries = re.split(r'<div class="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp">', body)

results = []
for i, entry in enumerate(entries[1:], 1):  # skip first (before any entry)
    # Extract header (title/date)
    header_match = re.search(r'<div class="header-cell mdl-cell mdl-cell--12-col">\s*<div class="mdl-typography--title">(.*?)</div>', entry, re.DOTALL)
    header = header_match.group(1).strip() if header_match else "unknown"

    # Extract all content cells
    content_cells = re.findall(r'<div class="content-cell mdl-cell mdl-cell--\d+-col[^"]*">(.*?)</div>', entry, re.DOTALL)

    # Clean HTML tags from content
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

    user_msg = ""
    model_msg = ""
    metadata = ""

    for cell in content_cells:
        cleaned = clean_html(cell)
        if not cleaned:
            continue
        # The first content cell is usually user's prompt
        # The second is usually model's response
        # The caption cell is metadata
        if "mdl-typography--caption" in entry:
            pass
        if not user_msg:
            user_msg = cleaned
        elif not model_msg:
            model_msg = cleaned
        else:
            metadata = cleaned

    # Parse date from header
    date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', header)
    date_str = ""
    if date_match:
        y, m, d = date_match.groups()
        date_str = f"{y}-{int(m):02d}-{int(d):02d}"

    results.append({
        'index': i,
        'date': date_str,
        'header': header,
        'user_msg': user_msg[:500],  # truncate
        'model_msg': model_msg[:100],  # compress model response
        'metadata': metadata[:200],
    })

# Filter to last 2 months (March-May 2026)
cutoff = "2026-03-01"
recent = [r for r in results if r['date'] >= cutoff]

print(f"Total entries: {len(results)}")
print(f"Entries since {cutoff}: {len(recent)}")
print(f"\n{'='*80}")

# Sort by date
recent.sort(key=lambda x: x['date'])

for r in recent:
    print(f"\n--- [{r['date']}] Entry #{r['index']} ---")
    print(f"Header: {r['header']}")
    print(f"User: {r['user_msg'][:300]}")
    if r['model_msg']:
        print(f"Model (compressed): {r['model_msg'][:100]}")
    print()

# Also show all dates for overview
print(f"\n{'='*80}")
print("All entry dates:")
for r in sorted(results, key=lambda x: x['date']):
    print(f"  {r['date']}  #{r['index']:2d}  {r['header'][:60]}")
