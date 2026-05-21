# 인박스 → STUDY/QUIZ/CHEATSHEETS 자동 처리 절차

이 문서는 두 트리거의 **공통 진입 프롬프트**.

- 수동: `/process-inbox` 슬래시 명령 (`.claude/commands/process-inbox.md` 가 이 문서를 가리킴)
- 주기: `/schedule` cron — fire 시 "tools/SCHEDULE.md 의 절차대로 인박스 처리" 형식의 프롬프트로 진입

> Claude Code 의 cron 은 **사용자 세션이 켜져 있는 동안만 fire** 됨. 자고 일어나서 자동 처리는 안 됨.

---

## 절차 (이 순서대로 정확히 수행)

### 1. 인박스 스캔

- `ls tools/inbox/*/` 로 하위 디렉토리 (각 디렉토리명 = `course-id`) 안의 파일 확인
- `.gitkeep` 은 무시
- 처리할 파일이 0개면 **"처리할 자료 없음"** 출력 후 종료 (commit 도 X)
- 처리 대상 목록 한 줄로 출력 (`{course}/{file}` 형식)

### 2. 각 파일 순회 처리

파일명에서 stem 추출: `lesson-01-intro.pdf` → stem=`lesson-01-intro`.

#### 2-1. 컨텐츠 추출

| 입력 | 도구 | 비고 |
|--|--|--|
| `.pdf` | Read | 10p 초과 시 `pages: "1-10"`, `"11-20"`, ... 로 분할 읽기 후 결합 |
| `.txt`, `.md` | Read | 직접 텍스트 |
| `.url` 또는 첫 줄이 `http(s)://` 인 `.txt` | WebFetch | 본문 추출 (스크립트/광고 제거된 결과 신뢰) |
| `.youtube`, `.yt` | — | **스킵 + 경고 출력** ("YouTube 는 Phase 3"). 이동도 X. |

추출 텍스트가 빈 문자열이거나 200자 미만이면 → 해당 파일 스킵 + 경고.

#### 2-2. 출력 파일 충돌 검사

다음 3개 경로가 이미 존재하면 **해당 파일 전체를 스킵 + 경고**:
- `courses/{course-id}/STUDY/{stem}.md`
- `courses/{course-id}/QUIZ/{stem}.md`
- `courses/{course-id}/CHEATSHEETS/{stem}.md`

(덮어쓰기 금지. 재생성 의도라면 사용자가 기존 파일을 먼저 삭제해야 함.)

#### 2-3. 3종 생성

각 종마다 다음을 수행:

1. `tools/prompts/{study|quiz|cheatsheet}.md` 를 Read 로 읽어 **system 지시**로 적용
2. **user 입력**: 추출한 컨텐츠 + 한 줄 헤더 (`# {stem} - 원본 발췌`)
3. 자기 자신 (Claude Code) 이 생성한 마크다운을 Write 로 저장:
   - STUDY → `courses/{course-id}/STUDY/{stem}.md`
   - QUIZ → `courses/{course-id}/QUIZ/{stem}.md`
   - CHEAT → `courses/{course-id}/CHEATSHEETS/{stem}.md`

분량 가이드는 각 프롬프트에 명시. STUDY 8~20KB, QUIZ 6~12KB, CHEAT 10~22KB.

#### 2-4. 원본 이동

처리 성공 시 `tools/inbox/{course}/{file}` → `tools/processed/{course}/{file}` (mkdir -p 후 mv).
스킵된 파일은 그대로 둠 (다음 트리거에서 재시도 또는 사용자 정리).

### 3. course.json 갱신

`courses/{course-id}/course.json` 이:

- **존재** → `sections` 의 **마지막 섹션** 의 `items` 끝에 `{"stem": "{stem}", "label": "{본문에서 추출한 사람-읽기-좋은 제목}"}` 추가. `pages` 는 PDF 메타에서 알면 추가, 모르면 생략.
- **존재하지만 sections 가 비어있음** → `sections: [{"title": "신규 추가", "items": [...]}]` 로 채움
- **부재** → 생성하지 않음. 마지막 요약에 경고: "`courses/{course-id}/course.json` 없음 → 직접 작성 필요"

JSON 갱신은 한 번에 Read → 파싱 → 객체 갱신 → Write.

### 4. manifest.json 확인

`manifest.json` 의 어느 카테고리에도 `path: "courses/{course-id}"` 가 없으면 → 요약에 경고: "manifest.json 에 {course-id} 미등록 → 카테고리·태그 직접 추가 필요". 자동 등록 X (카테고리 선택은 사용자 의도).

### 5. 커밋 + 푸시

생성된 파일이 1개 이상이면:

```bash
git add -A
git commit -m "feat({course-id}): 자동 처리 - {stem-list-comma}"
git push origin main
```

여러 코스를 동시에 처리했다면 코스별로 별도 커밋 또는 다중 코스 한 커밋 (`feat(auto): cs-robotics(lesson-01), cs-os(lesson-03)`).

생성된 파일이 0개면 commit X.

### 6. 요약 출력

마지막에 반드시 다음 형태로 보고:

```
✓ 처리 완료: N 파일
  - cs-robotics/lesson-01-intro.pdf → STUDY/QUIZ/CHEATSHEETS
  - cs-robotics/lesson-02-kinematics.pdf → STUDY/QUIZ/CHEATSHEETS

⚠ 스킵: M 파일
  - cs-os/lecture-99.youtube (YouTube 미지원)
  - cs-robotics/lesson-01-intro.pdf (출력 이미 존재)

⚠ 경고:
  - manifest.json 에 cs-robotics 미등록
  - course.json sections 비어있어서 "신규 추가" 섹션 생성됨

커밋: feat(cs-robotics): 자동 처리 - lesson-01-intro, lesson-02-kinematics
푸시: ✓ origin/main
```

---

## 안전장치

- 출력 파일 덮어쓰기 금지 (이미 있으면 스킵)
- 인박스 비면 commit / push 안 함
- PDF 가 너무 크면 분할 읽고 결합 (단일 prompt 호출에 다 넣되 토큰 한도 주의 — 한 챕터 50p 정도까지 한 번에 OK)
- WebFetch 본문이 너무 짧거나 비면 스킵 + 경고
- 사용자 입력 없이 자율 진행 가능 (오류 시에는 출력에 경고 남기고 다음 파일로)

## 로보틱스 첫 시도 시 체크

사용자가 `tools/inbox/cs-robotics/{stem}.pdf` 를 드롭한다고 가정:

1. `manifest.json` 에 `cs-robotics` 없음 → 카테고리 미정. 첫 시도에서는 경고만 출력, 마크다운은 정상 생성.
2. `courses/cs-robotics/` 디렉토리도 없음 → STUDY/QUIZ/CHEATSHEETS 하위 디렉토리 생성 (`mkdir -p`).
3. `course.json` 도 없음 → 경고. 마크다운만 생성하고 사용자가 나중에 작성.
4. 결과 확인 후 사용자가 `manifest.json` + `course.json` 수동 등록 → 포털에서 보임.
