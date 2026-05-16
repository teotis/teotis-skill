#!/usr/bin/env python3
"""PDF → 页面 PNG base64 data URL JSON。

用法:
    python3 pdf_to_pages.py <pdf_path> [--dpi 144] [--output <output.json>]

输出 JSON 格式:
    [{"page": 1, "data_url": "data:image/png;base64,..."}, ...]

优先使用 pypdfium2，降级到 pdftoppm CLI。
"""
import argparse
import base64
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def render_with_pypdfium2(pdf_path: str, dpi: int) -> list[dict]:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(pdf_path)
    scale = dpi / 72.0
    pages = []

    for i in range(len(doc)):
        page = doc[i]
        bitmap = page.render(scale=scale)
        image = bitmap.to_pil()
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        pages.append({"page": i + 1, "data_url": f"data:image/png;base64,{b64}"})

    doc.close()
    return pages


def render_with_pdftoppm(pdf_path: str, dpi: int) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = Path(tmpdir) / "page"
        result = subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), pdf_path, str(prefix)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"pdftoppm failed: {result.stderr}")

        pages = []
        for img_path in sorted(Path(tmpdir).glob("page-*.png")):
            b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
            # Extract page number from filename like "page-01.png"
            num = int(img_path.stem.split("-")[-1])
            pages.append({"page": num, "data_url": f"data:image/png;base64,{b64}"})

        return pages


def main():
    parser = argparse.ArgumentParser(description="PDF → 页面 PNG data URL JSON")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("--dpi", type=int, default=144, help="渲染 DPI (默认 144)")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径 (默认 stdout)")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not Path(pdf_path).exists():
        print(f"错误: 文件不存在: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    try:
        pages = render_with_pypdfium2(pdf_path, args.dpi)
    except ImportError:
        print("pypdfium2 不可用，降级到 pdftoppm...", file=sys.stderr)
        try:
            pages = render_with_pdftoppm(pdf_path, args.dpi)
        except (RuntimeError, FileNotFoundError) as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    output_json = json.dumps(pages, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"已输出 {len(pages)} 页到 {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
