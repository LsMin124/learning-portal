---
description: tools/inbox 의 자료를 STUDY/QUIZ/CHEATSHEETS 3종으로 자동 처리하고 commit + push
---

`tools/SCHEDULE.md` 의 절차를 그대로 따라 `tools/inbox/` 의 자료를 처리하세요.

요약:
1. `tools/inbox/*/` 스캔 (각 하위 디렉토리 = `course-id`, `.gitkeep` 무시)
2. 비어있으면 "처리할 자료 없음" 출력 후 즉시 종료 (commit 도 X)
3. 각 파일에 대해 SCHEDULE.md 의 절차 수행:
   - 확장자별 도구로 컨텐츠 추출 (PDF→Read, URL→WebFetch, YouTube→스킵)
   - 출력 파일 충돌 검사 (이미 존재하면 스킵)
   - `tools/prompts/{study|quiz|cheatsheet}.md` 를 system 으로 적용하여 3종 생성
   - 원본을 `tools/processed/{course}/` 로 mv
   - `courses/{course}/course.json` 의 마지막 섹션에 item append
4. 생성된 파일이 1개 이상이면 `git add -A && git commit && git push origin main`
5. SCHEDULE.md 6 절의 형식으로 요약 출력

신규 코스 (manifest.json 미등록, course.json 부재) 는 마크다운만 생성하고 경고만 출력 — 자동 등록 X.
