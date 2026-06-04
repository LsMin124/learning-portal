"""Corporate Finance 12e figure 추출 러너.

장별 figs dict (0-based PDF page index) 를 누적 기록하고 extract_figures() 로
일괄 crop 한다. 페이지는 find_figures.py 로 먼저 탐색해 CHAPTERS 에 채운다.

  교재 인쇄 페이지 = PDF(1-based) − 33   (ch16 6개 figure 로 검증된 offset)

캡션은 Corporate Finance 12e 특성상 figure '위'에 있으므로 caption_pos="above".

추출 전략 3 종 (figure 별로 자동 선택):
- 기본: extract_figures (panel-anchor, 단일 figure 대부분)
- MULTIPANEL: 세로로 쌓인 여러 차트 → 캡션 영역 그래픽 합집합 union
- MANUAL: 기본/union 둘 다 실패(본문 혼입·잘림)하는 까다로운 figure →
          render_page.py 'rects' 로 차트 bbox 를 떠서 수동 좌표 지정.
          캡션 블록은 자동 union.

사용법:
    python tools/extract_finance.py 19                # ch19 → figures/ch19
    python tools/extract_finance.py 16 --out /tmp/x   # 출력 경로 지정(검증용)
"""
from __future__ import annotations

import os
import sys

import fitz  # PyMuPDF

from extract_figures import _find_caption, extract_figures  # tools/ 가 sys.path[0]

PDF = "tools/inbox/financial-management/Corporate Finance, 12th Twelfth edition.pdf"
OUT_BASE = "courses/financial-management/figures"

# chapter -> {figure 번호: 0-based PDF page index}.  find_figures.py 결과를 검토 후 등록.
CHAPTERS: dict[int, dict[str, int]] = {
    1: {"1.1": 34, "1.2": 35, "1.3": 40},   # 1.3 = period-prose 후보, QA 필수
    3: {"3.1": 100},
    4: {"4.1": 118, "4.2": 119, "4.3": 120, "4.4": 122, "4.5": 122, "4.6": 123,
        "4.7": 124, "4.8": 126, "4.9": 127, "4.10": 128, "4.11": 136, "4.12": 143},
    14: {"14.1": 463, "14.2": 466, "14.3": 467, "14.4": 471, "14.5": 472,
         "14.6": 474, "14.7": 478, "14.8": 480, "14.9": 481, "14.10": 481,
         "14.11": 482, "14.12": 483, "14.13": 487, "14.14": 488, "14.15": 490},
    15: {"15.1": 513, "15.2": 514, "15.3": 515},
    16: {"16.1": 520, "16.2": 523, "16.3": 529, "16.4": 536, "16.5": 539, "16.6": 541},
    17: {"17.1": 561, "17.2": 563, "17.3": 565, "17.4": 573, "17.5": 575, "17.6": 576},
    19: {"19.1": 606, "19.2": 607, "19.3": 610, "19.4": 612,
         "19.5": 615, "19.6": 625, "19.7": 626, "19.8": 627},
}

# union 전략 대상 → {chapter: {fnum, ...}}. 세로 누적 멀티패널 등.
MULTIPANEL: dict[int, set[str]] = {
    17: {"17.6"},
}

# 캡션 union 을 끌 figure → {chapter: {fnum, ...}}.
# EXAMPLE 박스 안의 figure 처럼 캡션 '위' prose 가 같은 figure 번호를 언급("…displayed
# in Figure 4.10.")하면 _find_caption 이 그 prose 를 캡션으로 잡아 box 를 위로 늘린다.
# 이 경우 MANUAL box 에 실제 캡션을 직접 포함시키고 자동 union 은 끈다.
NO_CAPTION_UNION: dict[int, set[str]] = {
    4: {"4.2", "4.3", "4.7", "4.9", "4.10"},
}

# 수동 좌표(PDF pt, 차트 본체 bbox) → {chapter: {fnum: (x0, y0, x1, y1)}}.
# 페이지 인덱스는 CHAPTERS 에서 가져오고, 캡션 블록은 자동 union 한다.
MANUAL: dict[int, dict[str, tuple[float, float, float, float]]] = {
    1: {
        "1.2": (198.0, 258.0, 578.0, 709.0),   # 긴 조직도(y260~706)
        "1.3": (68.0, 466.0, 548.0, 713.0),    # 페이지 하단 그림 + 좌측 캡션(상단 prose 제외)
    },
    # ch04: text-block 좌표로 검증(render_page rects + get_text blocks). 캡션은 좌측 여백.
    4: {
        "4.1":  (250.0,  92.0, 472.0, 190.0),  # 상단 timeline — 우측 $11,424 잘림 복구(좌측 캡션 union)
        "4.2":  (200.0,  92.0, 512.0, 242.0),  # 캡션+패널만, 하단 'Suppose, instead…'(y247) 제외 (union OFF)
        "4.3":  (175.0, 164.0, 485.0, 303.0),  # 캡션+패널만, 하단 prose 제외 (union OFF)
        "4.4":  ( 84.0,  92.0, 534.0, 336.0),  # 막대+note. x0=84 로 우측정렬 캡션 'Compound Interest'(x86.7) 포함
        "4.7":  (170.0, 162.0, 548.0, 306.0),  # 캡션+패널만, 하단 'The ratio…'(y309) 제외 (union OFF)
        "4.8":  (190.0,  92.0, 528.0, 351.0),  # 차트+우측라벨+하단 note (우측 라벨은 x487 까지)
        "4.9":  (200.0, 227.0, 552.0, 390.0),  # 캡션+2패널. 위 'Figure 4.9 illustrates…'·아래 prose 제외 (union OFF)
        "4.10": (172.0, 174.0, 485.0, 316.0),  # 캡션+패널만, 위 prose·아래 ratio 제외 (union OFF)
    },
    # ch14: 표준 추출이 하단 라벨/노트/x축·우측 라벨을 잘라 → render_page rects 기반 수동 box
    14: {
        "14.1":  (196.0, 382.0, 641.0, 736.0),   # 하단 라벨 + 우측 라벨
        "14.2":  (193.0,  90.0, 625.0, 334.0),   # 하단/우측 Buy 라벨
        "14.4":  (233.0,  92.0, 542.0, 456.0),   # 2-그래프(A 시뮬·B Gap) 멀티패널
        "14.7":  (167.0, 411.0, 560.0, 706.0),   # 하단 x축
        "14.9":  (188.0,  90.0, 625.0, 450.0),   # 하단 x축 라벨(14.10 위, y<472)
        "14.11": (188.0,  90.0, 568.0, 384.0),   # 하단 설명 note
        "14.13": (193.0,  90.0, 643.0, 400.0),   # 우측 라벨(페이지 끝까지)
        "14.14": (190.0,  90.0, 625.0, 614.0),   # 하단 note + 우측 라벨
    },
    # 19.7: 같은 페이지 본문이 union 에 혼입 → 차트 img(171,94.7,546,299)+SOURCE 까지만
    19: {"19.7": (171.0, 92.0, 547.0, 309.0)},
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
        if r.width > page_w * 0.92 and r.height > page_h * 0.92:  # 페이지 전체 배경/테두리
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


def _crop(page, rect, out_path: str, dpi: float = 2.5) -> None:
    page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), clip=rect).save(out_path)


def _extract_union(pidx: int, fnum: str, out_path: str) -> bool:
    doc = fitz.open(PDF)
    page = doc[pidx]
    rect = _union_rect(page, f"Figure {fnum}")
    ok = rect is not None
    if ok:
        _crop(page, rect, out_path)
    doc.close()
    return ok


def _extract_manual(pidx: int, fnum: str, box: tuple, out_path: str,
                    union_caption: bool = True) -> bool:
    """수동 차트 bbox + (자동 탐지) 캡션 블록 union 으로 crop.

    union_caption=False 면 box 를 그대로 쓴다 (캡션 '위' prose 가 같은 figure
    번호를 언급해 _find_caption 이 prose 를 잡는 EXAMPLE 박스용 — NO_CAPTION_UNION).
    """
    doc = fitz.open(PDF)
    page = doc[pidx]
    rect = fitz.Rect(*box)
    if union_caption:
        _, cap_block = _find_caption(page, f"Figure {fnum}")
        # 캡션 블록은 box 와 *세로로 근접* 할 때만 union — 같은 페이지의 멀리 떨어진
        # prose("Figure 1.3. The arrows…")가 잡혀 box 를 본문까지 늘리는 것 방지.
        if cap_block is not None and cap_block.y1 >= box[1] - 50 and cap_block.y0 <= box[3] + 50:
            rect = rect | cap_block
    rect = fitz.Rect(rect.x0 - 4, rect.y0 - 4, rect.x1 + 4, rect.y1 + 4)
    _crop(page, rect, out_path)
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
    manual = MANUAL.get(chapter, {})
    no_union = NO_CAPTION_UNION.get(chapter, set())
    special = multi | set(manual)
    print(f"ch{chapter}: {len(figs)}개 figure → {out_dir}  "
          f"(union: {sorted(multi) or '-'}, manual: {sorted(manual) or '-'})")

    standard = {k: v for k, v in figs.items() if k not in special}
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
    for fnum, box in sorted(manual.items()):
        out_path = os.path.join(out_dir, f"fig-{fnum.replace('.', '-')}.png")
        _extract_manual(figs[fnum], fnum, box, out_path, union_caption=fnum not in no_union)
        tag = "manual" if fnum not in no_union else "manual,no-cap-union"
        size = os.path.getsize(out_path) / 1024
        print(f"OK   Fig {fnum} ({tag}) -> {os.path.basename(out_path)}  ({size:.0f}KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    ch = int(sys.argv[1])
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    run(ch, out_path)
