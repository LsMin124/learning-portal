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

try:
    import numpy as np
    from scipy.ndimage import binary_closing, label as _cc_label
    _HAS_PIXEL = True
except ImportError:
    _HAS_PIXEL = False


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


def _figure_bbox_from_image(page, cap_block_rect, page_top_margin=60, min_image_dim_pt=20):
    """페이지의 embedded raster image bbox 중 caption 의 figure 인 것의 합집합 반환.

    선별 휴리스틱:
      - region: (이전 caption bottom, 현재 caption top) 사이
      - caption width 의 50% 미만 폭의 image 는 *decoration* 으로 간주 (예: chapter
        시작 페이지의 작은 logo, page header 의 아이콘)
      - region 안 *가장 큰* image 를 anchor 로, 그것과 비슷한 폭 (≥ 60%) 의 image
        만 함께 클러스터 (서로 다른 figure 가 한 페이지에 작은+큰 image 로 섞여
        있어도 큰 게 caption 의 figure 일 가능성 압도적)
    """
    all_caps = _find_all_caption_blocks(page)
    cur_idx = next(
        (i for i, r in enumerate(all_caps)
         if abs(r.y0 - cap_block_rect.y0) < 1 and abs(r.y1 - cap_block_rect.y1) < 1),
        None,
    )
    region_top = (
        all_caps[cur_idx - 1].y1 + 2
        if cur_idx is not None and cur_idx > 0
        else page_top_margin
    )
    region_bot = cap_block_rect.y0 - 1

    cap_w = cap_block_rect.width
    min_useful_w = max(min_image_dim_pt, cap_w * 0.5)

    candidates = []
    for img in page.get_image_info():
        b = fitz.Rect(img["bbox"])
        if b.width < min_useful_w or b.height < min_image_dim_pt:
            continue
        if b.y1 <= region_top + 2 or b.y0 >= region_bot - 2:
            continue
        candidates.append(b)

    if not candidates:
        return None

    # 가장 큰 image 가 anchor, 그것과 폭이 비슷한 것 (≥ 60% anchor width) 만 합침
    candidates.sort(key=lambda r: -(r.width * r.height))
    anchor = candidates[0]
    fig = anchor
    for r in candidates[1:]:
        if r.width < anchor.width * 0.6:
            continue
        fig = fig | r
    fig = fig | cap_block_rect

    page_h = page.rect.y1
    return fitz.Rect(
        max(page.rect.x0 + 2, fig.x0 - 3),
        max(page_top_margin - 5, fig.y0 - 3),
        min(page.rect.x1 - 2, fig.x1 + 3),
        min(page_h - 45, fig.y1 + 6),
    )


def _figure_bbox_pixel(page, cap_block_rect, page_top_margin=60, page_bot_margin=50, raster_dpi=2.0):
    """픽셀 기반 connected-component 로 figure 영역 정밀 검출.

    bbox 합집합보다 정확. raster render → non-white mask → morphological closing →
    connected components → caption 바로 위의 *주 cluster* 의 시각적 경계 추출.

    page 안 다른 figure caption / body paragraph 위치를 미리 매핑하여
    region 의 위·아래 경계를 *시각적이 아닌 의미적* 으로 제한.
    """
    if not _HAS_PIXEL:
        return None

    page_h = page.rect.y1
    page_w = page.rect.x1

    # 1. 페이지 내 caption block 위치
    all_caps = _find_all_caption_blocks(page)
    cur_idx = next(
        (i for i, r in enumerate(all_caps)
         if abs(r.y0 - cap_block_rect.y0) < 1 and abs(r.y1 - cap_block_rect.y1) < 1),
        None,
    )
    prev_cap_bottom = (
        all_caps[cur_idx - 1].y1 + 2
        if cur_idx is not None and cur_idx > 0
        else page_top_margin
    )

    # 2. body paragraph 가 region 위에 있으면 region top 을 그 아래로 조정
    region_top_pt = prev_cap_bottom
    region_bot_pt = cap_block_rect.y0 - 1
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        br = fitz.Rect(blk["bbox"])
        if br.y1 <= region_top_pt or br.y0 >= region_bot_pt:
            continue
        if abs(br.y0 - cap_block_rect.y0) < 1:
            continue
        # body paragraph 휴리스틱: 폭 >= 60% column AND 높이 >= 25pt
        if br.width >= page_w * 0.55 and br.height >= 25:
            if br.y1 > region_top_pt and br.y1 < region_bot_pt - 10:
                region_top_pt = br.y1 + 3

    if region_bot_pt - region_top_pt < 10:
        return None

    # 3. raster render 전체 페이지
    mat = fitz.Matrix(raster_dpi, raster_dpi)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n >= 3:
        gray = img[..., :3].mean(axis=2)
    else:
        gray = img.squeeze()

    # 4. non-white mask
    mask = gray < 245

    # 5. ROI crop in pixel coord
    y0_px = int(region_top_pt * raster_dpi)
    y1_px = int(region_bot_pt * raster_dpi)
    if y1_px - y0_px < 5:
        return None
    roi = mask[y0_px:y1_px, :]

    if roi.sum() < 50:
        return None

    # 6. morphological closing — 화살표·라벨 등 작은 element 연결
    closing_size = max(2, int(raster_dpi * 4))
    closed = binary_closing(roi, iterations=closing_size)

    # 7. connected component labeling
    labels, n_comp = _cc_label(closed)
    if n_comp == 0:
        return None

    # 8. component 별 bbox + area
    candidates = []
    min_area_px = max(150, int(raster_dpi * raster_dpi * 30))
    for cid in range(1, n_comp + 1):
        ys, xs = np.where(labels == cid)
        if len(ys) < min_area_px:
            continue
        candidates.append({
            "bbox": (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())),
            "area": int(len(ys)),
        })

    if not candidates:
        return None

    # 9. 가장 큰 component 를 anchor, 나머지 큰 cluster (>= 5% anchor) 들도 합침
    candidates.sort(key=lambda c: -c["area"])
    anchor = candidates[0]
    union = list(anchor["bbox"])
    anchor_area = anchor["area"]
    merge_gap_pt = 35
    for c in candidates[1:]:
        if c["area"] < anchor_area * 0.05:
            break
        b = c["bbox"]
        gap_y_px = max(0, max(b[1] - union[3], union[1] - b[3]))
        gap_x_px = max(0, max(b[0] - union[2], union[0] - b[0]))
        if gap_y_px > raster_dpi * merge_gap_pt:
            continue
        if gap_x_px > raster_dpi * merge_gap_pt:
            continue
        union[0] = min(union[0], b[0])
        union[1] = min(union[1], b[1])
        union[2] = max(union[2], b[2])
        union[3] = max(union[3], b[3])

    # 10. px → pt + ROI offset 보정
    fig_rect_pt = fitz.Rect(
        union[0] / raster_dpi,
        (y0_px + union[1]) / raster_dpi,
        union[2] / raster_dpi,
        (y0_px + union[3]) / raster_dpi,
    )
    fig_rect_pt = fig_rect_pt | cap_block_rect

    # 11. 페이지 경계 clamp + 약간 padding
    return fitz.Rect(
        max(page.rect.x0 + 2, fig_rect_pt.x0 - 3),
        max(page_top_margin - 5, fig_rect_pt.y0 - 3),
        min(page.rect.x1 - 2, fig_rect_pt.x1 + 3),
        min(page_h - page_bot_margin + 5, fig_rect_pt.y1 + 6),
    )


def extract_figure(page, caption_prefix, out_path, dpi=2.5, precision="pixel"):
    """단일 figure 추출. 성공하면 True 반환.

    precision:
        "pixel" — 3-tier 우선순위:
            (1) embedded raster image bbox (책의 figure 가 image 인 경우 정확)
            (2) pixel connected-component (vector graphic)
            (3) vector/text bbox 합집합 (fallback)
        "bbox"  — vector/text bbox 합집합만 (빠름, 약간 부정확)
    """
    cap_bbox, cap_block_rect = _find_caption(page, caption_prefix)
    if cap_bbox is None:
        return False

    fig_rect = None
    if precision == "pixel":
        fig_rect = _figure_bbox_from_image(page, cap_block_rect)
        if fig_rect is None and _HAS_PIXEL:
            fig_rect = _figure_bbox_pixel(page, cap_block_rect)

    if fig_rect is None:
        fig_rect = _figure_bbox(page, cap_bbox, cap_block_rect)

    pix = page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), clip=fig_rect)
    pix.save(out_path)
    return True


def extract_figures(pdf, out_dir, figs, dpi=2.5, caption_format="Figure {num}:", precision="pixel"):
    """
    여러 figure 일괄 추출.

    Args:
        pdf: PDF 파일 경로
        out_dir: PNG 출력 디렉토리 (없으면 생성)
        figs: {"2.1": 29, "2.2": 30, ...}  — figure 번호 → 0-based PDF page index
        dpi: pixmap 의 매트릭스 스케일 (2.5 = 2.5x, ~180dpi 효과)
        caption_format: 캡션 prefix 템플릿 (`{num}` 자리표시자)
        precision: "pixel" (정밀, 느림) 또는 "bbox" (빠름)

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
            precision=precision,
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
