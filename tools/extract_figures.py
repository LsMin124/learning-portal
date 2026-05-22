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


def _figure_bbox(page, cap_bbox, cap_block_rect, margin_top=60, margin_bottom=50):
    """캡션 위쪽의 drawing 합집합 + 캡션 자체를 포함하는 figure bbox 추정."""
    page_h = page.rect.y1
    valid = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.y0 < margin_top or r.y1 > page_h - margin_bottom:
            continue
        if r.width < 0.5 or r.height < 0.5:
            continue
        # 캡션 아래의 drawing 은 제외 (figure 는 캡션 위 가정)
        if r.y0 > cap_bbox[3] + 2:
            continue
        valid.append(r)

    if not valid:
        return fitz.Rect(
            page.rect.x0 + 30,
            cap_bbox[1] - 200,
            page.rect.x1 - 30,
            cap_block_rect.y1 + 10,
        )

    fig_rect = valid[0]
    for r in valid[1:]:
        fig_rect = fig_rect | r
    fig_rect = fig_rect | cap_block_rect
    return fitz.Rect(
        fig_rect.x0 - 5,
        fig_rect.y0 - 5,
        fig_rect.x1 + 5,
        fig_rect.y1 + 10,
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
