"""Corporate Finance 12e figure 추출 러너.

장별 figs dict (0-based PDF page index) 를 누적 기록하고 extract_figures() 로
일괄 crop 한다. 페이지는 find_figures.py 로 먼저 탐색해 CHAPTERS 에 채운다.

  교재 인쇄 페이지 = PDF(1-based) − 33   (ch16 6개 figure 로 검증된 offset)

캡션은 Corporate Finance 12e 특성상 figure '위'에 있으므로 caption_pos="above".

멀티패널 figure (한 figure 가 세로로 쌓인 여러 차트 = GM/IBM/Kodak 식) 는
panel-anchor 로직이 첫 패널만 잡아 under-crop 된다. MULTIPANEL 에 등록하면
캡션 아래 region 의 모든 그래픽+이미지 합집합을 crop 하는 union 전략을 쓴다.

사용법:
    python tools/extract_finance.py 17                # ch17 → figures/ch17
    python tools/extract_finance.py 16 --out /tmp/x   # 출력 경로 지정(검증용)
"""
from __future__ import annotations

import os
import sys

import fitz  # PyMuPDF

from extract_figures import _find_caption, extract_figure, extract_figures  # tools/ 가 sys.path[0]

PDF = "tools/inbox/financial-management/Corporate Finance, 12th Twelfth edition.pdf"
OUT_BASE = "courses/financial-management/figures"

# chapter -> {figure 번호: 0-based PDF page index}.  find_figures.py 결과를 검토 후 등록.
CHAPTERS: dict[int, dict[str, int]] = {
    16: {"16.1": 520, "16.2": 523, "16.3": 529, "16.4": 536, "16.5": 539, "16.6": 541},
    17: {"17.1": 561, "17.2": 563, "17.3": 565, "17.4": 573, "17.5": 575, "17.6": 576},
}

# 멀티패널(세로로 쌓인 여러 차트) figure → union 전략. {chapter: {fnum, ...}}
MULTIPANEL: dict[int, set[str]] = {
    17: {"17.6"},
}


def _union_rect(page, caption_prefix: str, top_margin: float = 70, bot_margin: float = 55):
    """캡션 아래 region 의 모든 figure 그래픽(이미지+큰 벡터)+캡션 블록의 합집합 rect."""
    page_w, page_h = page.rect.width, page.rect.height
    rects = []
    for img in page.get_image_info():
        b = fitz.Rect(img["bbox"])
        if b.width >= 40 and b.height >= 40:
            rects.append(b)
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 6 or r.height < 6:
            continue
        if r.height < 1.5 and r.width > page_w * 0.7:   # 가로 rule/separator
            continue
        if r.y0 < top_margin or r.y1 > page_h - bot_margin:
            continue
        rects.append(r)
    if not rects:
        return None
    u = fitz.Rect(rects[0])
    for r in rects[1:]:
        u = u | r
    _, cap_block = _find_caption(page, caption_prefix)
    if cap_block is not None:
        u = u | cap_block
    return fitz.Rect(
        max(2, u.x0 - 6), max(2, u.y0 - 6),
        min(page_w - 2, u.x1 + 6), min(page_h - 2, u.y1 + 10),
    )


def _extract_union(pidx: int, fnum: str, out_path: str, dpi: float = 2.5) -> bool:
    doc = fitz.open(PDF)
    page = doc[pidx]
    rect = _union_rect(page, f"Figure {fnum}")
    if rect is None:
        doc.close()
        return False
    page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), clip=rect).save(out_path)
    doc.close()
    return True


def run(chapter: int, out: str | None = None) -> None:
    figs = CHAPTERS.get(chapter)
    if not figs:
        print(f"ch{chapter}: CHAPTERS 에 미등록 — find_figures.py 로 먼저 페이지 탐색")
        return
    out_dir = out or os.path.join(OUT_BASE, f"ch{chapter:02d}")
    os.makedirs(out_dir, exist_ok=True)
    multi = MULTIPANEL.get(chapter, set())
    print(f"ch{chapter}: {len(figs)}개 figure → {out_dir}  (멀티패널: {sorted(multi) or '없음'})")

    # 일반 figure 는 표준 extract_figures, 멀티패널은 union 전략.
    standard = {k: v for k, v in figs.items() if k not in multi}
    if standard:
        extract_figures(
            pdf=PDF, out_dir=out_dir, figs=standard,
            caption_format="Figure {num}", caption_pos="above",
        )
    for fnum in sorted(multi):
        out_path = os.path.join(out_dir, f"fig-{fnum.replace('.', '-')}.png")
        ok = _extract_union(figs[fnum], fnum, out_path)
        size = os.path.getsize(out_path) / 1024 if ok else 0
        print(f"{'OK  ' if ok else 'FAIL'} Fig {fnum} (union) -> {os.path.basename(out_path)}  ({size:.0f}KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    ch = int(sys.argv[1])
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    run(ch, out_path)
