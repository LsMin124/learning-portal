"""LLM 호출 공통 헬퍼.

Anthropic Claude API 호출 + 프롬프트 템플릿 로드.
study/quiz/cheatsheet 가 공유.

Phase 1: stub. Phase 2 에서 실제 anthropic SDK 호출로 교체.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# tools 디렉토리 import path
sys.path.insert(0, str(Path(__file__).parent.parent))

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(name: str) -> str:
    """tools/prompts/{name}.md 를 문자열로 로드.

    예: load_prompt("study") -> tools/prompts/study.md 의 내용.
    """
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"프롬프트 템플릿 없음: {path}")
    return path.read_text(encoding="utf-8")


def call_claude(system_prompt: str, user_input: str, *, max_tokens: int = 16000) -> str:
    """Claude API 호출 (Phase 2 구현 예정).

    Parameters
    ----------
    system_prompt : str
        프롬프트 템플릿 (역할·형식·길이 규약 등).
    user_input : str
        SourceBundle 의 본문 + 메타데이터.
    max_tokens : int
        출력 최대 토큰.

    Returns
    -------
    str
        Claude 의 응답 본문 (마크다운).
    """
    # ──────────────────────────────────────────────
    # Phase 2 에서 구현:
    #
    # from anthropic import Anthropic
    #
    # api_key = os.environ.get("ANTHROPIC_API_KEY")
    # if not api_key:
    #     raise RuntimeError("ANTHROPIC_API_KEY 환경변수 미설정. tools/.env.example 참고.")
    #
    # model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    # client = Anthropic(api_key=api_key)
    #
    # response = client.messages.create(
    #     model=model,
    #     max_tokens=max_tokens,
    #     system=system_prompt,
    #     messages=[{"role": "user", "content": user_input}],
    # )
    # return response.content[0].text
    # ──────────────────────────────────────────────

    raise NotImplementedError(
        "LLM 호출은 아직 stub. Phase 2 에서 anthropic SDK 로 구현.\n"
        "tools/README.md 의 'Phase 2' 섹션 참고."
    )


def render_user_input(bundle) -> str:
    """SourceBundle → LLM user 메시지 (공통 포맷).

    각 생성기가 자기 프롬프트와 함께 이 함수의 출력을 user 메시지로 전달.
    """
    parts = [
        f"# 자료 메타",
        f"- 제목: {bundle.title}",
        f"- 출처 타입: {bundle.source_type}",
        f"- 출처: {bundle.source_path}",
    ]
    if bundle.metadata:
        parts.append(f"- 메타데이터: {bundle.metadata}")
    if bundle.keywords:
        parts.append(f"- 핵심 키워드: {', '.join(bundle.keywords)}")

    if bundle.sections:
        parts.append("")
        parts.append("# 섹션 구조")
        for s in bundle.sections:
            parts.append(f"{'#' * (s.level + 1)} {s.title}" + (f"  (p.{s.page})" if s.page else ""))

    parts.append("")
    parts.append("# 본문")
    parts.append(bundle.plain_text)

    return "\n".join(parts)
