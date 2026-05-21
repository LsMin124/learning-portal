# tools/ — 학습 자료 자동 처리

PDF/URL 한 챕터를 인박스에 던지면 STUDY/QUIZ/CHEATSHEETS 3종을 자동 생성.
**Anthropic API 키 불필요** — Claude Code 세션 자체가 Read/WebFetch 로 읽고 생성.

---

## 사용법

### 1. 인박스에 자료 드롭

```
tools/inbox/{course-id}/{stem}.{ext}
```

- `course-id`: `manifest.json` / `courses/` 의 디렉토리명 (없으면 신규 코스로 간주, 경고만 출력)
- `stem`: 출력 파일명 (예: `lesson-01-intro` → `courses/.../STUDY/lesson-01-intro.md`)
- `ext`: 아래 표 참고

예:
```bash
cp 로보틱스_1장_운동학.pdf tools/inbox/cs-robotics/lesson-01-kinematics.pdf
```

### 2. 트리거 (두 가지)

**A. 즉시 (수동)**
```
/process-inbox
```
Claude Code 세션에서 슬래시 명령 실행. `tools/SCHEDULE.md` 의 절차로 즉시 처리.

**B. 주기 (cron)**
```
/schedule
```
설정 시 프롬프트: `tools/SCHEDULE.md 의 절차대로 tools/inbox 를 처리해`

> ⚠ Claude Code 의 cron 은 **사용자가 세션을 켜둔 동안만 fire**. 백그라운드 데몬 X.

### 3. 결과

- `courses/{course-id}/STUDY/{stem}.md` (8~20KB)
- `courses/{course-id}/QUIZ/{stem}.md` (14문항, 6~12KB)
- `courses/{course-id}/CHEATSHEETS/{stem}.md` (TL;DR + Quick Ref + Mind Map)
- 원본 → `tools/processed/{course-id}/`
- `course.json` 마지막 섹션에 item 자동 append
- `manifest.json` 미등록 시 경고만 출력 (자동 등록 X)
- 자동 `git commit + push`

---

## 지원 입력

| 확장자 | 처리 도구 | 비고 |
|--|--|--|
| `.pdf` | Read | 10p 초과 시 `pages` 파라미터로 분할 읽기 |
| `.txt`, `.md` | Read | 직접 텍스트 |
| `.url` 또는 첫 줄 http인 `.txt` | WebFetch | 본문 추출 |
| `.youtube`, `.yt` | — | **Phase 3**, 지금은 스킵 + 경고 |

---

## 디렉토리

```
tools/
├── inbox/                  드롭 존 (course-id 별 하위 디렉토리)
│   └── .gitkeep
├── processed/              처리 완료 (원본 보관)
│   └── .gitkeep
├── prompts/                생성 시스템 프롬프트 (정형 규약)
│   ├── study.md
│   ├── quiz.md
│   └── cheatsheet.md
├── SCHEDULE.md             자동 처리 절차 (cron + 수동 트리거 공용)
└── README.md               이 문서
```

---

## 안전장치

- **덮어쓰기 금지**: 출력 3종 중 하나라도 이미 존재하면 그 파일 전체 스킵 + 경고
- **빈 인박스**: commit / push 안 함
- **PDF 분할 읽기**: 50p 초과 시 pages 파라미터로 나누어 읽고 컨텍스트에 결합
- **WebFetch 빈 결과**: 200자 미만이면 스킵

---

## 신규 코스 시작 절차

신규 `course-id` 의 자료를 처음 던질 때:

1. `tools/inbox/{course-id}/` 자동 생성 후 PDF 드롭
2. `/process-inbox`
3. 처리는 됨 (`courses/{course-id}/STUDY/...` 생성). 단:
   - ⚠ `course.json` 미생성 (마크다운만 생김)
   - ⚠ `manifest.json` 미등록
4. 결과 확인 후 사용자가 직접:
   - `courses/{course-id}/course.json` 작성 (title/subtitle/tags/sections)
   - `manifest.json` 의 적절한 카테고리에 코스 등록

이후 자료부터는 `course.json` 의 마지막 섹션에 item 자동 추가됨.

---

## 한계 및 추후 작업

- **YouTube 미지원**: Phase 3 에서 `youtube-transcript-api` 또는 `yt-dlp --write-auto-subs` 로 자막 추출 추가
- **다국어 자료**: 영어/일본어 등 → 프롬프트가 한국어 출력 강제. 원본 언어 그대로 두려면 프롬프트 수정 필요
- **이미지·다이어그램**: PDF 의 그림은 텍스트 추출 시 손실. 다이어그램 의존 자료는 STUDY 의 묘사가 약할 수 있음
