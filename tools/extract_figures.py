#!/usr/bin/env python3
"""
PDF 의 vector figure 만 정확히 추출하는 도구.

PyMuPDF (fitz) 로 figure caption ("Figure X.Y:") 의 bbox 를 찾고,
같은 페이지에서 *캡션 위쪽* 의 모든 vector drawing 영역의 합집합을
clip 으로 잡아 그 영역만 PNG 로 렌더한다. 페이지 전체 캡처가 아닌
*figure 자체만* 추출.

사용 예 (Modern Robotics Ch 2):

    from extract_figures import extract_figures
    extract_figures(
        pdf="tools/inbox/modern-robotics/MR.pdf",
        out_dir="courses/modern-robotics/figures/ch02",
        figs={
            "2.1":  29,  # PDF page index (0-based, == PDF page number - 1)
            "2.2":  30,
            "2.3":  33,
            # ...
        },
        dpi=2.5,
    )

기본 가정:
  - figure 가 캡션 *위* 에 위치 (학술 PDF 의 표준)
  - 캡션 텍스트가 "Figure {num}:" 형태로 시작
  - 페이지 상/하 60pt / 50pt 마진의 drawing 은 헤더·푸터로 간주, 제외
"""

import os
import fitz


def _find_caption(page, caption_prefix):
    """페이지 안에서 caption_prefix 로 시작하는 line 의 (bbox, block_rect) 반환."""
    for blk in page.get_text("dict")["blocks"]:
        for line in blk.get("lines", []):
            txt = "".join(s["text"] for s in line["spans"])
            if txt.startswith(caption_prefix):
                return line["bbox"], fitz.Rect(blk["bbox"])
    return None, None


def _find_all_caption_blocks(page, caption_marker="Figure "):
    """페이지의 모든 figure caption block rect 를 위→아래 순으로 반환.

    같은 페이지에 figure 가 여러 개일 때 각 figure 의 영역을 *상하 분리* 하기 위함.
    """
    blocks = []
    for blk in page.get_text("dict")["blocks"]:
        for line in blk.get("lines", []):
            txt = "".join(s["text"] for s in line["spans"])
            if txt.startswith(caption_marker) and "." in txt[:20]:
                blocks.append(fitz.Rect(blk["bbox"]))
                break
    blocks.sort(key=lambda r: r.y0)
    return blocks


def _content_in_band(page, y_top, y_bot, x_inset=10):
    """[y_top, y_bot] 세로 band 안의 vector drawing + text block bbox 들 반환.

    figure 의 vector 본체뿐 아니라 *축 라벨·legend* 같은 text block 도 포함하여
    under-crop 을 막는다.
    """
    rects = []
    page_w = page.rect.x1
    min_dim = 0.5
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < min_dim or r.height < min_dim:
            continue
        if r.y0 < y_top - 1 or r.y1 > y_bot + 1:
            continue
        # 페이지 가로 전체에 걸친 *얇은* 선 (header/footer rule, separator) 제외
        if r.height < 1.0 and r.width > page_w * 0.7:
            continue
        rects.append(r)

    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        br = fitz.Rect(blk["bbox"])
        if br.width < 1 or br.height < 1:
            continue
        if br.y0 < y_top - 1 or br.y1 > y_bot + 1:
            continue
        # caption 이외의 *큰 본문 paragraph* 는 제외 — 너무 폭이 넓고 키도 크면 본문 가능성
        if br.width > page_w - 2 * x_inset - 5 and br.height > 30:
            continue
        rects.append(br)
    return rects


def _figure_bbox(page, cap_bbox, cap_block_rect, page_top_margin=60, page_bot_margin=50):
    """캡션 위의 figure 영역 bbox 추정.

    페이지 내 *모든 caption* 을 찾아, 현재 caption 의 figure region 을
    (이전 caption block 의 bottom, 현재 caption block 의 top) 사이로 제한.
    이 영역 안의 vector drawing + text block 의 합집합 + caption block 자체.
    """
    page_h = page.rect.y1
    all_caps = _find_all_caption_blocks(page)
    cur_idx = None
    for i, r in enumerate(all_caps):
        if abs(r.y0 - cap_block_rect.y0) < 1 and abs(r.y1 - cap_block_rect.y1) < 1:
            cur_idx = i
            break

    if cur_idx is not None and cur_idx > 0:
        region_top = all_caps[cur_idx - 1].y1 + 2
    else:
        region_top = page_top_margin
    region_bot = cap_block_rect.y0 - 1

    if region_bot - region_top < 10:
        region_top = max(page_top_margin, cap_bbox[1] - 350)
        region_bot = cap_block_rect.y0 - 1

    rects = _content_in_band(page, region_top, region_bot)

    if not rects:
        return fitz.Rect(
            page.rect.x0 + 30,
            max(page_top_margin, cap_bbox[1] - 300),
            page.rect.x1 - 30,
            cap_block_rect.y1 + 10,
        )

    fig_rect = rects[0]
    for r in rects[1:]:
        fig_rect = fig_rect | r
    fig_rect = fig_rect | cap_block_rect

    return fitz.Rect(
        max(page.rect.x0 + 2, fig_rect.x0 - 6),
        max(page_top_margin - 5, fig_rect.y0 - 6),
        min(page.rect.x1 - 2, fig_rect.x1 + 6),
        min(page_h - page_bot_margin + 5, fig_rect.y1 + 10),
    )


def extract_figure(page, caption_prefix, out_path, dpi=2.5):
    """단일 figure 추출. 성공하면 True 반환."""
    cap_bbox, cap_block_rect = _find_caption(page, caption_prefix)
    if cap_bbox is None:
        return False
    fig_rect = _figure_bbox(page, cap_bbox, cap_block_rect)
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), clip=fig_rect)
    pix.save(out_path)
    return True


def extract_figures(pdf, out_dir, figs, dpi=2.5, caption_format="Figure {num}:"):
    """
    여러 figure 일괄 추출.

    Args:
        pdf: PDF 파일 경로
        out_dir: PNG 출력 디렉토리 (없으면 생성)
        figs: {"2.1": 29, "2.2": 30, ...}  — figure 번호 → 0-based PDF page index
        dpi: pixmap 의 매트릭스 스케일 (2.5 = 2.5x, ~180dpi 효과)
        caption_format: 캡션 prefix 템플릿 (`{num}` 자리표시자)

    Returns:
        성공한 figure 의 dict {fig_num: out_path}
    """
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf)
    result = {}
    for fnum, pidx in figs.items():
        out = os.path.join(out_dir, f"fig-{fnum.replace('.', '-')}.png")
        ok = extract_figure(
            doc[pidx],
            caption_format.format(num=fnum),
            out,
            dpi=dpi,
        )
        if ok:
            result[fnum] = out
            print(f"OK   Fig {fnum} -> {os.path.basename(out)}  "
                  f"({os.path.getsize(out)/1024:.0f}KB)")
        else:
            print(f"FAIL Fig {fnum}  (caption not found on page {pidx+1})")
    doc.close()
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "mr-ch2":
        extract_figures(
            pdf="tools/inbox/modern-robotics/MR.pdf",
            out_dir="courses/modern-robotics/figures/ch02",
            figs={
                "2.1":  29, "2.2":  30, "2.3":  33, "2.4":  35,
                "2.5":  36, "2.7":  38, "2.9":  41, "2.10": 46,
                "2.11": 48, "2.12": 50,
            },
        )
    else:
        print(__doc__)
