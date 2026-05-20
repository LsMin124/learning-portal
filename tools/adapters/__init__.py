"""입력 어댑터.

각 모듈은 단일 함수 `extract(source: str) -> SourceBundle` 을 노출.

규약:
- source 는 파일 경로 (PDF) 또는 URL (URL/YouTube).
- 실패 시 적절한 예외 (FileNotFoundError, ValueError, requests.HTTPError 등).
- LLM 비용을 줄이려면 plain_text 를 너무 길게 만들지 말 것.
  너무 긴 자료는 chunking 전략을 별도 모듈에서 다룸 (Phase 3 예정).
"""
