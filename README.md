# 학습 포털 — 멀티 코스 워크스페이스

다양한 학습자료 (강의·전공서·튜토리얼·블로그) 를 **STUDY/QUIZ/CHEATSHEETS 3 종 + ROADMAP** 으로 정형화하여 통합 뷰어 (`index.html`) 로 학습.

**Live**: https://learning-portal-psi.vercel.app/

## 디렉토리 구조

```
lecture_notes/
├── index.html               포털 (단일 페이지, manifest 동적 로드)
├── manifest.json            전체 코스 카탈로그 (5 카테고리)
│
├── courses/                 공개 학습 자료 (2차 가공)
│   └── ssafy-java/          현재 보유 코스
│       ├── course.json      코스 메타 + 강의 sections
│       ├── STUDY/           학습 노트 (단독 학습 가능)
│       ├── QUIZ/            14문항 (개념·적용·디버그·면접)
│       ├── CHEATSHEETS/     TL;DR + Quick Ref + Mind Map
│       └── ROADMAP.md       의존성·추천 학습 순서
│
├── _deploy/                 GitHub Pages 배포본 (별도 git repo)
└── _private/                비공개 원본·도구·credential
                             (.gitignore / .vercelignore 로 격리)
```

## 새 코스 추가 절차

1. 디렉토리 생성:
   ```bash
   mkdir -p courses/{course-id}/{STUDY,QUIZ,CHEATSHEETS}
   ```

2. `courses/{course-id}/course.json` 작성:
   ```json
   {
     "version": 1,
     "id": "course-id",
     "title": "코스 제목",
     "subtitle": "한 줄 설명",
     "tags": ["tag1", "tag2"],
     "sections": [
       {
         "title": "섹션 1",
         "items": [
           {"stem": "lesson-01", "pages": 30, "label": "01강 제목"}
         ]
       }
     ]
   }
   ```

3. 각 강의별 마크다운 작성:
   - `STUDY/{stem}.md` — 학습 노트 (단독 학습 가능, ~10KB)
   - `QUIZ/{stem}.md` — 14문항 (개념·적용·디버그·면접)
   - `CHEATSHEETS/{stem}.md` — 3 섹션 (TL;DR / Quick Ref / Mind Map)

4. `ROADMAP.md` — 의존성·추천 순서.

5. `manifest.json` 의 적절한 카테고리에 코스 등록:
   ```json
   {
     "id": "course-id",
     "title": "...",
     "subtitle": "...",
     "path": "courses/course-id",
     "tags": [...]
   }
   ```

6. 포털 새로고침. 사이드바 코스 셀렉터에서 선택 가능.

## 컨텐츠 가이드

### STUDY (학습 노트)
영상 강의 없이도 단독 학습 가능한 깊이. 함정·실무 맥락 포함. 분량은 강의 페이지 수 비례 (보통 10~30KB).

### QUIZ (퀴즈)
14문항이 표준 (가벼운 강의는 10문항). 4 카테고리 균형:
- **개념** (3~4): 정의·원리
- **적용** (4~5): 실제 코드 작성
- **디버그** (3~4): 함정·에러 해석
- **면접** (1~2): 한 줄 답변 형식

`<details><summary>정답</summary>...</details>` 토글 사용.

### CHEATSHEETS (치트시트)
3 섹션 통합:
1. **TL;DR** — 핵심 6줄 + 가장 중요한 코드 3개 + 면접 한 줄 답변
2. **Quick Reference** — 실무 복붙 (문법·명령어·비교표·함정)
3. **Mind Map** — 전체 토픽 트리 + 학습 진도 체크리스트

### ROADMAP
의존성·Phase·추천 학습 순서. 표·트리 사용. 강의 `stem` 만 적어두면 포털이 클릭 가능하게 변환.

## 로컬 실행

```bash
python3 -m http.server 8765 --bind 127.0.0.1
# http://127.0.0.1:8765/  (또는 /index.html)
```

## 배포

- **GitHub Pages** (현재): `_deploy/` 가 별도 git repo (LsMin124/Spring_edu) → main push → https://lsmin124.github.io/Spring_edu/
- **Vercel** (예정): lecture_notes 루트를 직접 연결. `.vercelignore` 가 `_private/`, `_deploy/` 제외.

## 비공개 자료 격리

`_private/` 안의 모든 자료는 **저작권 또는 보안 위험으로 외부 공개 금지**. `.gitignore` / `.vercelignore` 양쪽에 등록되어 배포 시 자동 제외. 상세는 `_private/README.md`.
