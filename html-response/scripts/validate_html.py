#!/usr/bin/env python3
"""Lightweight lint checks for HTML produced by Adaptive HTML Response.

Usage:
    python3 validate_html.py <html_path>

This is a fast structural/safety check, not a conformance or security certification.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_PATTERNS = {
    "doctype": r"<!doctype\s+html",
    "language": r"<html\b[^>]*\blang\s*=",
    "charset": r"<meta\b[^>]*charset\s*=",
    "viewport": r"<meta\b[^>]*name\s*=\s*[\"']viewport[\"']",
    "title": r"<title>\s*[^<\s][^<]*</title>",
    "main landmark": r"<main\b",
}
WARNING_PATTERNS = {
    "external dependency": r"(?:src|href)\s*=\s*[\"']https?://",
    "inline event handler": r"\son[a-z]+\s*=",
    "javascript URL": r"javascript\s*:",
    "eval usage": r"\beval\s*\(",
    "new Function usage": r"\bnew\s+Function\s*\(",
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_path")
    args = parser.parse_args()
    path = Path(args.html_path)
    if not path.exists():
        print(f"ERROR: not found: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()

    errors: list[str] = []
    warnings: list[str] = []
    for label, pattern in REQUIRED_PATTERNS.items():
        if not re.search(pattern, lower, flags=re.I | re.S):
            errors.append(f"missing {label}")
    if "content-security-policy" not in lower:
        warnings.append("missing Content Security Policy meta tag")
    if "prefers-reduced-motion" not in lower:
        warnings.append("no reduced-motion handling detected")
    if "skip-link" not in lower and "skip to" not in lower:
        warnings.append("no skip link detected")
    for label, pattern in WARNING_PATTERNS.items():
        if re.search(pattern, text, flags=re.I | re.S):
            warnings.append(f"detected {label}; review intent and safety")

    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        return 1
    print("PASS: required structural checks found")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
