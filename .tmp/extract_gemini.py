#!/usr/bin/env python3
"""Extract user messages from Gemini Takeout HTML activity record."""

import re
import sys
from html.parser import HTMLParser
from datetime import datetime

HTML_PATH = "/Volumes/Extreme_SSD/工作数据/AI对话/gemini_web/Takeout/我的活动/Gemini Apps/我的活动记录.html"

class GeminiActivityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.current_entry = {}
        self.in_header = False
        self.in_content = False
        self.capture_text = False
        self.current_text = []
        self.tag_stack = []
        self.div_depth = 0

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')

        if tag == 'div':
            self.div_depth += 1

    def handle_endtag(self, tag):
        if self.tag_stack:
            self.tag_stack.pop()
        if tag == 'div':
            self.div_depth -= 1

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        self.current_text.append(data)

def parse_html_simple(filepath):
    """Simple approach: find patterns in the HTML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"HTML file size: {len(content)} chars")
    print(f"First 2000 chars:\n{content[:2000]}")
    print(f"\n--- Looking for patterns ---")

    # Look for common Gemini Takeout patterns
    # Try to find conversation entries
    patterns = [
        r'class="[^"]*conversation[^"]*"',
        r'class="[^"]*prompt[^"]*"',
        r'class="[^"]*response[^"]*"',
        r'class="[^"]*user[^"]*"',
        r'class="[^"]*message[^"]*"',
        r'class="[^"]*activity[^"]*"',
        r'class="[^"]*content[^"]*"',
        r'class="[^"]*entry[^"]*"',
    ]

    for p in patterns:
        matches = re.findall(p, content[:50000])
        if matches:
            unique = list(set(matches))[:5]
            print(f"  {p}: {len(matches)} matches, e.g.: {unique}")

    # Look for date patterns
    date_patterns = [
        r'\d{4}年\d{1,2}月\d{1,2}日',
        r'\d{4}-\d{2}-\d{2}',
        r'\d{4}/\d{2}/\d{2}',
    ]
    for p in date_patterns:
        matches = re.findall(p, content[:50000])
        if matches:
            print(f"  Date pattern {p}: {matches[:5]}")

if __name__ == '__main__':
    parse_html_simple(HTML_PATH)
