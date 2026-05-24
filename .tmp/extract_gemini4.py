#!/usr/bin/env python3
"""Extract user messages from Gemini Takeout HTML - improved parser."""

import re

HTML_PATH = "/Volumes/Extreme_SSD/工作数据/AI对话/gemini_web/Takeout/我的活动/Gemini Apps/我的活动记录.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find body content
body_start = content.find('<body')
body = content[body_start:]

# Split by outer-cell divs
entries = re.split(r'<div class="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp">', body)

# Let's look at the first entry in detail to understand structure
if len(entries) > 1:
    entry = entries[1]
    # Print first 3000 chars of first entry
    print("=== FIRST ENTRY (3000 chars) ===")
    print(entry[:3000])
    print("\n=== END FIRST ENTRY ===\n")

# Now let's look at a few more entries
for i in range(2, min(4, len(entries))):
    entry = entries[i]
    print(f"\n=== ENTRY {i} (2000 chars) ===")
    print(entry[:2000])
    print("=== END ===")
