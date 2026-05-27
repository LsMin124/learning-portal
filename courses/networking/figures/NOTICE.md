# Figures — Copyright Notice

이 디렉토리의 PNG 파일들은 **Computer Networking: A Top-Down Approach** (James F. Kurose & Keith W. Ross, 8th Global Edition, Pearson 2021) 책의 figure 들을 *학습 보조 목적* 으로 PDF 에서 vector-aware crop 한 것입니다.

- **원저작권**: © 2021 James F. Kurose, Keith W. Ross
- **출판사**: Pearson Education
- **ISBN-13** (Global Edition): 978-1-292-40546-9
- **공식 사이트**: https://gaia.cs.umass.edu/kurose_ross/

본 자료는 *개인 학습용 노트* 로만 사용. 상업적 재배포·교재화 금지. fair use (학습 노트에서 식별·해설) 범위를 벗어난다고 판단되면 즉시 제거.

## 추출 방법

`tools/extract_figures.py` 의 *3-tier 정밀 알고리즘*:
1. Embedded raster image bbox (caption width ≥ 50% filter)
2. Pixel connected-component (raster + non-white mask + morphological closing)
3. Vector/text bbox 합집합 (fallback)

Caption pattern: `Figure {num} ♦` (Kurose 책의 다이아몬드 marker). 공백 정규화 regex 로 tab·multi-space 변동 처리.

DPI 2.5 로 추출 (해상도와 파일 크기의 균형).
