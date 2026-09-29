"""Xuat docs/mau3_draft.md ra PDF (khong page-break cung truoc moi muc).

Dung markdown -> HTML -> Edge headless --print-to-pdf. Khong can pandoc/LibreOffice.
Chay: python scripts/build_pdf.py [input.md] [output.pdf]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import markdown

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
body{font-family:'Times New Roman',serif;font-size:12pt;line-height:1.4;margin:18px}
h1{font-size:17pt;margin:0 0 8px}
h2{font-size:14pt;margin:14px 0 6px}   /* KHONG page-break cung */
h3{font-size:12.5pt;margin:10px 0 4px}
table{border-collapse:collapse;width:100%;font-size:9.5pt;margin:6px 0}
tr{page-break-inside:avoid}
td,th{border:1px solid #999;padding:3px 5px}
code{font-size:9.5pt}
p,li{margin:3px 0}
"""


def find_edge() -> str:
    for p in EDGE_CANDIDATES:
        if Path(p).exists():
            return p
    raise SystemExit("Khong tim thay msedge.exe")


def main() -> int:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/mau3_draft.md")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "mau3_draft.pdf")
    html_path = out.with_suffix(".html")

    md = src.read_text(encoding="utf-8")
    body = markdown.markdown(md, extensions=["tables", "fenced_code"])
    html_path.write_text(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style>'
        f"</head><body>{body}</body></html>",
        encoding="utf-8",
    )

    edge = find_edge()
    subprocess.run([
        edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={out.resolve()}", html_path.resolve().as_uri(),
    ], check=True, timeout=120)
    html_path.unlink(missing_ok=True)

    try:
        from pypdf import PdfReader
        n = len(PdfReader(str(out)).pages)
        print(f"PDF: {out} | SO TRANG: {n}")
    except Exception as e:  # noqa: BLE001
        print(f"PDF: {out} (khong dem duoc trang: {e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
