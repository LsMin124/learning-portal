"""PDF 페이지를 통째로 렌더한다 (figure 레이아웃 육안 QA 용, repo 밖 /tmp 출력).

사용법:
    python tools/render_page.py 562 563 564   # 0-based 페이지 인덱스
"""
from __future__ import annotations

import sys

import fitz  # PyMuPDF

PDF = "tools/inbox/financial-management/Corporate Finance, 12th Twelfth edition.pdf"


def render(indices: list[int], scale: float = 1.6) -> None:
    doc = fitz.open(PDF)
    for i in indices:
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(scale, scale))
        out = f"/tmp/page-{i}.png"
        pix.save(out)
        print(f"{out}  (PDF p.{i + 1}, 교재 p.{i + 1 - 33})")
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    render([int(a) for a in sys.argv[1:]])
