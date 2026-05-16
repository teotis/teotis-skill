#!/usr/bin/env python3
"""DOCX/DOC/PPT/PPTX → PDF (via LibreOffice soffice)。

用法:
    python3 doc_to_pdf.py <input_path> [--output <output.pdf>]

依赖 LibreOffice soffice。如果不可用，报错退出。
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_soffice() -> str:
    """查找 soffice 可执行文件。"""
    # 直接在 PATH 中查找
    soffice = shutil.which("soffice")
    if soffice:
        return soffice

    # macOS 默认安装路径
    mac_paths = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        os.path.expanduser("~/Applications/LibreOffice.app/Contents/MacOS/soffice"),
    ]
    for p in mac_paths:
        if Path(p).exists():
            return p

    return ""


def convert_to_pdf(input_path: str, output_dir: str) -> str:
    """使用 soffice 将文件转为 PDF，返回生成的 PDF 路径。"""
    soffice = find_soffice()
    if not soffice:
        print("错误: 未找到 LibreOffice soffice，请安装 LibreOffice", file=sys.stderr)
        sys.exit(1)

    # 使用独立 profile 避免锁冲突
    with tempfile.TemporaryDirectory() as profile_dir:
        cmd = [
            soffice,
            "-env:UserInstallation=file://" + profile_dir,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"soffice 转换失败: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    # 找到输出的 PDF
    input_stem = Path(input_path).stem
    pdf_path = Path(output_dir) / f"{input_stem}.pdf"
    if not pdf_path.exists():
        # 尝试查找任何生成的 PDF
        pdfs = list(Path(output_dir).glob("*.pdf"))
        if pdfs:
            pdf_path = pdfs[0]
        else:
            print(f"错误: soffice 未生成 PDF 文件", file=sys.stderr)
            sys.exit(1)

    return str(pdf_path)


def main():
    parser = argparse.ArgumentParser(description="DOCX/DOC/PPT/PPTX → PDF")
    parser.add_argument("input_path", help="输入文件路径")
    parser.add_argument("--output", "-o", help="输出 PDF 路径 (默认与输入同目录)")
    args = parser.parse_args()

    input_path = args.input_path
    if not Path(input_path).exists():
        print(f"错误: 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = str(Path(args.output).parent) if args.output else str(Path(input_path).parent)
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = convert_to_pdf(input_path, output_dir)

    if args.output and pdf_path != args.output:
        shutil.move(pdf_path, args.output)
        pdf_path = args.output

    print(pdf_path)


if __name__ == "__main__":
    main()
