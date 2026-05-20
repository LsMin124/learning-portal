"""공통 중간 표현.

입력 (PDF/URL/YouTube) 이 무엇이든 어댑터가 SourceBundle 로 정규화해서
넘기면, 생성기 (study/quiz/cheatsheet) 는 항상 같은 형식으로 LLM 을 호출.

새 입력 종류를 지원하려면 어댑터 1개만 추가하면 됨.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Literal


SourceType = Literal["pdf", "url", "youtube"]


@dataclass
class Section:
    """원본 자료의 챕터·섹션 구조.

    LLM 이 학습 노트의 H2 섹션을 자료의 자연스러운 흐름에 맞추도록
    어댑터가 가능한 채워둠. 추출이 어려운 경우 빈 리스트 OK.
    """

    level: int          # 1=H1, 2=H2, 3=H3, ...
    title: str          # "1.1 운영체제란 무엇인가"
    content: str        # 섹션 본문 (마크다운 친화)
    page: int | None = None    # PDF 의 페이지 번호 (있으면)


@dataclass
class SourceBundle:
    """입력 → LLM 사이의 공통 표현.

    어댑터 출력 / 생성기 입력 양쪽의 계약.

    Attributes
    ----------
    title : str
        자료 제목. 어댑터가 추출하거나 사용자가 --label 로 override.
    source_type : SourceType
        "pdf" | "url" | "youtube". dispatch 와 metadata 표시용.
    source_path : str
        원본 경로 또는 URL. 결과물의 footer 인용에 사용.
    plain_text : str
        본문 전체. 섹션 구조가 약하더라도 이 필드는 반드시 채움.
        LLM 의 메인 입력.
    sections : list[Section]
        구조가 명확한 자료 (책 PDF, 잘 정리된 글) 에서만 채워짐.
        영상/짧은 글은 빈 리스트.
    keywords : list[str]
        본문에서 추출한 핵심 키워드. 프롬프트에 힌트로 전달.
        어댑터가 채우거나 LLM 의 첫 단계에서 채울 수 있음.
    metadata : dict
        자유. 페이지 수·저자·게시일·총 길이·언어 등.
        예: {"pages": 32, "author": "...", "language": "ko"}
    """

    title: str
    source_type: SourceType
    source_path: str
    plain_text: str
    sections: list[Section] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """디버그·로깅·dry-run 출력용."""
        return asdict(self)

    def estimated_input_tokens(self) -> int:
        """LLM 비용 추정용. 영어/한글 모두 대략 1 token = 3.5 chars."""
        return max(1, len(self.plain_text) // 3)
