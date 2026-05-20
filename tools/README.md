# `tools/` — 학습 자료 자동 생성 파이프라인

다양한 입력 (PDF · URL · YouTube 영상) 을 받아 **STUDY / QUIZ / CHEATSHEETS** 마크다운을 자동 생성하는 Python CLI.

> **상태**: Phase 1 (설계 + 골격). LLM 호출 코드는 stub. Anthropic API 키 준비 후 Phase 2 에서 실제 구현.

## 파이프라인

```
[입력 어댑터]              [공통 중간 표현]              [LLM 생성기]              [출력]
PDF       ─┐                                                                ┌─ courses/{id}/STUDY/{stem}.md
URL       ─┼─→ adapters/  ─→  SourceBundle    ─→  generators/  ─→ Claude ─┼─ courses/{id}/QUIZ/{stem}.md
YouTube   ─┘   (입력 정규화)   (dataclass)        (프롬프트+API)            └─ courses/{id}/CHEATSHEETS/{stem}.md

                                                                              + course.json sections 자동 갱신 제안
                                                                              + ROADMAP.md 항목 추가 제안
```

**핵심 설계**: 어떤 입력이든 `SourceBundle` 로 정규화 → LLM 프롬프트는 항상 동일. 새 입력 종류 추가 시 어댑터만 1개 작성.

## 사용 예

```bash
# PDF
python tools/ingest.py \
    _private/raw/pdf/cs-os-chapter-01.pdf \
    --course cs-os \
    --stem chapter-01-intro \
    --label "01강 운영체제 개요" \
    --section "Part 1: 기초"

# URL
python tools/ingest.py \
    https://example.com/article \
    --course tutorials \
    --stem article-slug \
    --label "글 제목"

# YouTube
python tools/ingest.py \
    https://www.youtube.com/watch?v=XXXXXX \
    --course youtube-courses \
    --stem video-slug \
    --label "영상 제목"

# Dry-run (LLM 호출 없이 SourceBundle 만 확인)
python tools/ingest.py file.pdf --course cs-os --stem test --dry-run

# 일부 산출물만 (예: QUIZ 만 재생성)
python tools/ingest.py file.pdf --course cs-os --stem test --only quiz
```

## SourceBundle 스키마

```python
@dataclass
class SourceBundle:
    title: str                    # 자료 제목 (LLM 이 본문에서 추출)
    source_type: str              # "pdf" | "url" | "youtube"
    source_path: str              # 원본 경로/URL
    plain_text: str               # 추출된 본문 (마크다운 친화)
    sections: list[Section]       # 챕터·섹션 구조 (있으면)
    keywords: list[str]           # 핵심 키워드 (어댑터가 추출)
    metadata: dict                # 페이지 수, 길이, 저자, 게시일 등 자유
```

## 디렉토리 구조

```
tools/
├── README.md                 (이 파일)
├── requirements.txt          (Python 의존성)
├── .env.example              (API 키 안내)
├── ingest.py                 (CLI 진입점)
├── source_bundle.py          (공통 중간 표현 dataclass)
│
├── adapters/                 (입력 -> SourceBundle)
│   ├── __init__.py
│   ├── pdf.py                (pypdfium2 + macOS Vision OCR)
│   ├── url.py                (requests + readability-lxml)
│   └── youtube.py            (youtube-transcript-api)
│
├── generators/               (SourceBundle -> 마크다운)
│   ├── __init__.py
│   ├── study.py              (학습 노트 생성)
│   ├── quiz.py               (14문항 퀴즈 생성)
│   └── cheatsheet.py         (3섹션 치트시트 생성)
│
└── prompts/                  (LLM 프롬프트 템플릿)
    ├── study.md              (STUDY 형식·톤·길이 가이드)
    ├── quiz.md               (개념·적용·디버그·면접 카테고리)
    └── cheatsheet.md         (TL;DR + Quick Ref + Mind Map)
```

## 환경 변수

`.env` 파일에 (또는 shell export):

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
ANTHROPIC_MODEL=claude-sonnet-4-6        # 또는 claude-opus-4-7 (고품질)
```

`.env.example` 참고. 절대 commit X (`.gitignore` 에 등록).

## 비용 추정 (Claude Sonnet 4.6 기준)

| 강의 1개 (PDF 30p) | Input | Output | 비용 |
|--|--|--|--|
| STUDY 생성 | 15K tok | 10K tok | $0.20 |
| QUIZ 생성 | 15K tok | 8K tok  | $0.17 |
| CHEAT 생성 | 15K tok | 12K tok | $0.22 |
| **합계** | | | **~$0.59/강** |

30강 코스 1개 ≈ $18. Opus 4.7 사용 시 약 5배 ($90).

## 새 입력 종류 추가하는 법

예: Jupyter Notebook (.ipynb) 지원 추가

1. `tools/adapters/notebook.py` 작성:
   ```python
   def extract(path: Path) -> SourceBundle:
       # ipynb -> markdown cells + code cells 결합
       return SourceBundle(...)
   ```

2. `ingest.py` 의 dispatch 에 등록:
   ```python
   ADAPTERS["notebook"] = notebook.extract
   ```

3. CLI 확장자/스킴 인식 로직에 `.ipynb` 추가.

LLM 프롬프트는 건드릴 필요 없음 (SourceBundle 만 잘 채우면 됨).

## 정형 가이드 (생성기가 따르는 규약)

새 자료 추가 시 출력물이 기존 자료와 일관되도록 `prompts/*.md` 에 다음을 명시:

### STUDY
- 영상 강의 없이도 단독 학습 가능한 깊이
- 함정·실무 맥락 포함
- 분량 8~20KB (자료 크기 비례)
- H2 섹션은 자료의 자연스러운 챕터 따라감

### QUIZ
- 14문항 (가벼운 자료는 10)
- 4 카테고리 균형: 개념(3-4) · 적용(4-5) · 디버그(3-4) · 면접(1-2)
- `<details><summary>정답</summary>...</details>` 토글

### CHEATSHEETS
- 3 섹션 통합: TL;DR (5분 요약) + Quick Reference (실무 복붙) + Mind Map (학습 체크리스트)
- TL;DR 의 "핵심 6줄" + "가장 중요한 코드 3개" + "면접 한 줄 답변" 포맷

## 다음 단계 (Phase 2)

1. Anthropic API 키 발급 (`.env` 설정)
2. `pip install -r tools/requirements.txt`
3. `adapters/pdf.py` 의 `extract()` 실제 구현 (현재 stub)
4. `generators/*.py` 의 `generate()` 실제 구현 (Anthropic SDK 호출)
5. 짧은 PDF 로 첫 시도 → 결과 검토 → 프롬프트 튜닝 루프
