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


def dump_rects(idx: int, top: int = 12) -> None:
    """페이지의 큰 drawing/image rect 를 면적 순으로 출력 (수동 crop 좌표용)."""
    doc = fitz.open(PDF)
    page = doc[idx]
    print(f"# PDF p.{idx + 1} (교재 p.{idx + 1 - 33}), page rect = {page.rect}")
    items = []
    for d in page.get_drawings():
        r = d["rect"]
        items.append(("draw", r))
    for im in page.get_image_info():
        items.append(("img", fitz.Rect(im["bbox"])))
    items.sort(key=lambda t: t[1].width * t[1].height, reverse=True)
    for kind, r in items[:top]:
        print(f"  {kind:4} x0={r.x0:6.1f} y0={r.y0:6.1f} x1={r.x1:6.1f} y1={r.y1:6.1f}  "
              f"(w={r.width:5.1f} h={r.height:5.1f})")
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    if sys.argv[1] == "rects":
        dump_rects(int(sys.argv[2]))
    else:
        render([int(a) for a in sys.argv[1:]])
