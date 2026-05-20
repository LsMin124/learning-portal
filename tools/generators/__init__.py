"""LLM 생성기.

각 모듈은 단일 함수 `generate(bundle: SourceBundle) -> str` 을 노출.
반환은 마크다운 본문 (파일에 그대로 write).

규약:
- prompts/{name}.md 의 템플릿을 로드 + bundle 값 치환 후 LLM 호출.
- 출력은 항상 마크다운. 따옴표 / 코드블록 / details 토글 포함 OK.
- 결과 검증 (길이 / 헤더 구조 / 필수 섹션) 은 호출자가 처리.
"""
