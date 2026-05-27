# Figures — Copyright Notice

이 디렉토리의 PNG 파일들은 **Designing Data-Intensive Applications** (Martin Kleppmann, O'Reilly Media, 2017) 책의 figure 들을 *학습 보조 목적*으로 PDF 에서 vector-aware crop 한 것입니다.

- **원저작권**: © 2017 Martin Kleppmann. All rights reserved.
- **출판사**: O'Reilly Media, Inc.
- **ISBN**: 978-1-449-37332-0
- **공식 사이트**: https://dataintensive.net/

본 자료는 *개인 학습용 노트* 로만 사용되며, 상업적 재배포·교재화·재출판은 *금지*. figure 가 책의 *맥락 인용* (fair use, 학습 노트에서 식별·해설) 범위를 벗어난다고 판단되면 즉시 제거.

## 추출 방법

`tools/extract_figures.py` 의 *vector-aware crop* — PDF 의 figure caption ("Figure X-Y.") bbox 를 찾고, 같은 페이지의 caption 위쪽 vector drawing 합집합 영역만 PNG 로 렌더. *페이지 전체 캡처가 아닌 figure 자체만*.

DPI 2.5 로 추출 (해상도와 파일 크기의 균형).
