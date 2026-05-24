#!/usr/bin/env python3
"""Extract user messages from Gemini Takeout HTML activity record."""

import re

HTML_PATH = "/Volumes/Extreme_SSD/工作数据/AI对话/gemini_web/Takeout/我的活动/Gemini Apps/我的活动记录.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total size: {len(content)} chars")

# Skip CSS - find where actual HTML body starts
body_start = content.find('<body')
if body_start == -1:
    body_start = content.find('<main')
print(f"Body starts at char {body_start}")

# Look at content after CSS (skip first ~50KB which is likely CSS)
chunk = content[50000:55000]
print(f"\n--- Content around char 50000 ---")
print(chunk[:3000])

# Search for div class patterns that might indicate conversation entries
print("\n--- Searching for class patterns in body ---")
body_content = content[body_start:] if body_start > 0 else content[50000:]

# Find all unique class names
classes = re.findall(r'class="([^"]+)"', body_content[:200000])
unique_classes = {}
for c in classes:
    if c not in unique_classes:
        unique_classes[c] = 0
    unique_classes[c] += 1

# Sort by frequency
for cls, count in sorted(unique_classes.items(), key=lambda x: -x[1])[:30]:
    print(f"  {count:4d}x  {cls}")
