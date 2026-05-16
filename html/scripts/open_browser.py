#!/usr/bin/env python3
"""跨平台打开浏览器。

用法:
    python3 open_browser.py <html_path>

支持 macOS (open)、Linux (xdg-open)、Windows (start)。
"""
import platform
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("用法: python3 open_browser.py <html_path>", file=sys.stderr)
        sys.exit(1)

    html_path = sys.argv[1]
    if not Path(html_path).exists():
        print(f"错误: 文件不存在: {html_path}", file=sys.stderr)
        sys.exit(1)

    abs_path = str(Path(html_path).resolve())
    system = platform.system()

    if system == "Darwin":
        subprocess.Popen(["open", abs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system == "Linux":
        subprocess.Popen(["xdg-open", abs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system == "Windows":
        subprocess.Popen(["start", abs_path], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f"不支持的平台: {system}", file=sys.stderr)
        print(f"请手动打开: file://{abs_path}")
        sys.exit(1)

    print(f"已在浏览器中打开: {abs_path}")


if __name__ == "__main__":
    main()
