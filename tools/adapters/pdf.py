"""PDF 어댑터.

Phase 1: 골격만. Phase 2 에서 실제 구현.

추천 구현:
- pypdfium2 또는 pdfplumber: 텍스트 PDF 추출
- 텍스트 추출 실패 시 (스캔 이미지) → macOS Vision OCR fallback (_private/tools/ocr_all.py 의 패턴 재사용)
- 페이지별로 분리해서 Section 으로 묶기 + H1/H2 후보 휴리스틱 (큰 글꼴 / 굵게 / 짧은 줄)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from source_bundle import SourceBundle, Section


def extract(source: str) -> SourceBundle:
    """PDF 파일을 SourceBundle 로 변환.

    Parameters
    ----------
    source : str
        PDF 파일 경로.

    Returns
    -------
    SourceBundle
        - source_type = "pdf"
        - sections: 페이지 또는 챕터 단위 (휴리스틱)
        - metadata["pages"]: 총 페이지 수
    """
    path = Path(source).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    # ──────────────────────────────────────────────
    # Phase 2 에서 구현:
    #
    # import pypdfium2 as pdfium
    # pdf = pdfium.PdfDocument(path)
    # pages = []
    # for i, page in enumerate(pdf, start=1):
    #     text = page.get_textpage().get_text_range()
    #     if not text.strip():
    #         # OCR fallback
    #         text = run_vision_ocr(page)
    #     pages.append((i, text))
    #
    # # 섹션 휴리스틱: 큰 글꼴 / 굵게 / "Chapter N" 패턴
    # sections = detect_sections(pages)
    #
    # return SourceBundle(
    #     title=path.stem,
    #     source_type="pdf",
    #     source_path=str(path),
    #     plain_text="\n\n".join(t for _, t in pages),
    #     sections=sections,
    #     keywords=extract_keywords(pages),     # TF-IDF 또는 간단한 빈도
    #     metadata={"pages": len(pages)},
    # )
    # ──────────────────────────────────────────────

    raise NotImplementedError(
        f"PDF 어댑터는 아직 stub. Phase 2 에서 구현. ({path})\n"
        "구현 시 pypdfium2 또는 pdfplumber 사용. tools/README.md 참고."
    )
