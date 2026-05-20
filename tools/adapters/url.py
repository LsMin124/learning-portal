"""URL 어댑터.

Phase 1: 골격만. Phase 2 에서 실제 구현.

추천 구현:
- requests + readability-lxml: 본문 추출 (광고·메뉴 제거)
- 대안: trafilatura (더 정확함)
- HTML -> 마크다운 변환: markdownify
- H1/H2 태그를 Section 으로 묶기
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from source_bundle import SourceBundle


def extract(source: str) -> SourceBundle:
    """URL 의 본문을 SourceBundle 로 변환.

    Parameters
    ----------
    source : str
        HTTP(S) URL.

    Returns
    -------
    SourceBundle
        - source_type = "url"
        - sections: HTML H1/H2 기반
        - metadata: {"author", "published", "site", "url_canonical"}
    """
    # ──────────────────────────────────────────────
    # Phase 2 에서 구현:
    #
    # import requests
    # import trafilatura
    #
    # resp = requests.get(source, timeout=15, headers={"User-Agent": "..."})
    # resp.raise_for_status()
    #
    # # 본문 + 메타데이터 추출
    # extracted = trafilatura.bare_extraction(resp.text, with_metadata=True)
    # text = extracted["text"]
    # title = extracted["title"]
    # author = extracted.get("author")
    # published = extracted.get("date")
    #
    # # 섹션 분할 (h1/h2 기반)
    # sections = parse_sections_from_html(resp.text)
    #
    # return SourceBundle(
    #     title=title,
    #     source_type="url",
    #     source_path=source,
    #     plain_text=text,
    #     sections=sections,
    #     keywords=extracted.get("tags", []),
    #     metadata={
    #         "author": author,
    #         "published": published,
    #         "site": extracted.get("sitename"),
    #     },
    # )
    # ──────────────────────────────────────────────

    raise NotImplementedError(
        f"URL 어댑터는 아직 stub. Phase 2 에서 구현. ({source})\n"
        "구현 시 trafilatura 또는 readability-lxml 사용. tools/README.md 참고."
    )
