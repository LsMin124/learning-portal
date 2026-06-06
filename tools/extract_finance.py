"""Corporate Finance 12e figure 추출 러너.

장별 figs dict (0-based PDF page index) 를 누적 기록하고 extract_figures() 로
일괄 crop 한다. 페이지는 find_figures.py 로 먼저 탐색해 CHAPTERS 에 채운다.

  교재 인쇄 페이지 = PDF(1-based) − 33   (ch16 6개 figure 로 검증된 offset)

캡션은 Corporate Finance 12e 특성상 figure '위'에 있으므로 caption_pos="above".

추출 전략 3 종 (figure 별로 자동 선택):
- 기본: extract_figures (panel-anchor, 단일 figure 대부분)
- MULTIPANEL: 세로로 쌓인 여러 차트 → 캡션 영역 그래픽 합집합 union
- MANUAL: 기본/union 둘 다 실패(본문 혼입·잘림)하는 까다로운 figure →
          render_page.py 'rects' 로 차트 bbox 를 떠서 수동 좌표 지정.
          캡션 블록은 자동 union.

사용법:
    python tools/extract_finance.py 19                # ch19 → figures/ch19
    python tools/extract_finance.py 16 --out /tmp/x   # 출력 경로 지정(검증용)
"""
from __future__ import annotations

import os
import sys

import fitz  # PyMuPDF

from extract_figures import _find_caption, extract_figures  # tools/ 가 sys.path[0]

PDF = "tools/inbox/financial-management/Corporate Finance, 12th Twelfth edition.pdf"
OUT_BASE = "courses/financial-management/figures"

# chapter -> {figure 번호: 0-based PDF page index}.  find_figures.py 결과를 검토 후 등록.
CHAPTERS: dict[int, dict[str, int]] = {
    1: {"1.1": 34, "1.2": 35, "1.3": 40},   # 1.3 = period-prose 후보, QA 필수
    3: {"3.1": 100},
    4: {"4.1": 118, "4.2": 119, "4.3": 120, "4.4": 122, "4.5": 122, "4.6": 123,
        "4.7": 124, "4.8": 126, "4.9": 127, "4.10": 128, "4.11": 136, "4.12": 143},
    5: {"5.1": 168, "5.2": 172, "5.3": 173, "5.4": 174, "5.5": 176, "5.6": 183},
    6: {"6.1": 220},
    7: {"7.1": 242, "7.2": 244, "7.3": 247, "7.4": 249, "7.5": 251,
        "7.6": 252, "7.7": 254, "7.8": 255},   # 7.5 = 251 (250 은 prose 오탐)
    8: {"8.1": 268, "8.2": 272, "8.3": 283, "8.4": 284, "8.5": 289,
        "8.6": 290, "8.7": 292, "8.8": 293},   # 8.2 = 272 (find_figures 가 page 13 오탐)
    9: {"9.1": 304, "9.2": 306},
    10: {"10.1": 332, "10.2": 333, "10.3": 334, "10.4": 336, "10.5": 337,
         "10.6": 337, "10.7": 338, "10.8": 339, "10.9": 342, "10.10": 346,
         "10.11": 351, "10.12": 353},   # 10.1 = 332 (idx 12 는 prose 오탐)
    11: {"11.1": 365, "11.2": 370, "11.3": 371, "11.4": 373, "11.5": 374,
         "11.6": 375, "11.7": 380, "11.8": 383, "11.9": 384, "11.10": 387,
         "11.11": 390},   # alternate 다수(11.3/4/5/6/9/11) → 추출 후 QA 필수
    12: {"12.1": 407, "12.2": 410, "12.3": 411, "12.4": 413},
    13: {"13.1": 426, "13.2": 428, "13.3": 432, "13.4": 432, "13.5": 439},  # 13.3·13.4 동일 page 432
    14: {"14.1": 463, "14.2": 466, "14.3": 467, "14.4": 471, "14.5": 472,
         "14.6": 474, "14.7": 478, "14.8": 480, "14.9": 481, "14.10": 481,
         "14.11": 482, "14.12": 483, "14.13": 487, "14.14": 488, "14.15": 490},
    15: {"15.1": 513, "15.2": 514, "15.3": 515},
    16: {"16.1": 520, "16.2": 523, "16.3": 529, "16.4": 536, "16.5": 539, "16.6": 541},
    17: {"17.1": 561, "17.2": 563, "17.3": 565, "17.4": 573, "17.5": 575, "17.6": 576},
    19: {"19.1": 606, "19.2": 607, "19.3": 610, "19.4": 612,
         "19.5": 615, "19.6": 625, "19.7": 626, "19.8": 627},
    20: {"20.1": 646, "20.2": 646, "20.3": 647, "20.4": 648, "20.5": 650,
         "20.6": 659, "20.7": 660},   # 20.1·20.2 동일 page 646
    21: {"21.1": 682},
    22: {"22.1": 707, "22.2": 708, "22.3": 710, "22.4": 712, "22.5": 712,
         "22.6": 714, "22.7": 715, "22.8": 717, "22.9": 718, "22.10": 724,
         "22.11": 728, "22.12": 729},   # 22.4·22.5 동일 712; 22.10 캡션 미탐(QA)
    23: {"23.1": 758, "23.2": 760, "23.3": 766, "23.4": 768},
    24: {"24.1": 775, "24.2": 781, "24.3": 782},
    25: {"25.1": 804},
    26: {"26.1": 831, "26.2": 838, "26.3": 840, "26.4": 840, "26.5": 841},  # 26.3·26.4 동일 840
    27: {"27.1": 863, "27.2": 863, "27.3": 867, "27.4": 868, "27.5": 871, "27.6": 872},  # 27.1·27.2 동일 863
    28: {"28.1": 888, "28.2": 896, "28.3": 896, "28.4": 897, "28.5": 901},  # 28.2·28.3 동일 896
}

# union 전략 대상 → {chapter: {fnum, ...}}. 세로 누적 멀티패널 등.
MULTIPANEL: dict[int, set[str]] = {
    17: {"17.6"},
}

# 캡션 union 을 끌 figure → {chapter: {fnum, ...}}.
# EXAMPLE 박스 안의 figure 처럼 캡션 '위' prose 가 같은 figure 번호를 언급("…displayed
# in Figure 4.10.")하면 _find_caption 이 그 prose 를 캡션으로 잡아 box 를 위로 늘린다.
# 이 경우 MANUAL box 에 실제 캡션을 직접 포함시키고 자동 union 은 끈다.
NO_CAPTION_UNION: dict[int, set[str]] = {
    4: {"4.2", "4.3", "4.7", "4.9", "4.10"},
    5: {"5.5", "5.6"},
    6: {"6.1"},
    7: {"7.1", "7.4", "7.5", "7.6", "7.7"},
    8: {"8.2", "8.7"},
    9: {"9.1", "9.2"},
    10: {"10.1", "10.2", "10.5", "10.10", "10.11", "10.12"},
    11: {"11.4", "11.8", "11.9", "11.11"},
    12: {"12.1", "12.4"},
    13: {"13.1"},
    20: {"20.2", "20.5"},
    22: {"22.7", "22.8", "22.10", "22.11", "22.12"},
    23: {"23.1", "23.2", "23.3", "23.4"},
    24: {"24.3"},
    26: {"26.1", "26.2", "26.3", "26.5"},
    27: {"27.3", "27.4", "27.6"},
    28: {"28.1", "28.5"},
}

# 수동 좌표(PDF pt, 차트 본체 bbox) → {chapter: {fnum: (x0, y0, x1, y1)}}.
# 페이지 인덱스는 CHAPTERS 에서 가져오고, 캡션 블록은 자동 union 한다.
MANUAL: dict[int, dict[str, tuple[float, float, float, float]]] = {
    1: {
        "1.2": (198.0, 258.0, 578.0, 709.0),   # 긴 조직도(y260~706)
        "1.3": (68.0, 466.0, 548.0, 713.0),    # 페이지 하단 그림 + 좌측 캡션(상단 prose 제외)
    },
    # ch04: text-block 좌표로 검증(render_page rects + get_text blocks). 캡션은 좌측 여백.
    4: {
        "4.1":  (250.0,  92.0, 472.0, 190.0),  # 상단 timeline — 우측 $11,424 잘림 복구(좌측 캡션 union)
        "4.2":  (200.0,  92.0, 512.0, 242.0),  # 캡션+패널만, 하단 'Suppose, instead…'(y247) 제외 (union OFF)
        "4.3":  (175.0, 164.0, 485.0, 303.0),  # 캡션+패널만, 하단 prose 제외 (union OFF)
        "4.4":  ( 84.0,  92.0, 534.0, 336.0),  # 막대+note. x0=84 로 우측정렬 캡션 'Compound Interest'(x86.7) 포함
        "4.7":  (170.0, 162.0, 548.0, 306.0),  # 캡션+패널만, 하단 'The ratio…'(y309) 제외 (union OFF)
        "4.8":  (190.0,  92.0, 528.0, 351.0),  # 차트+우측라벨+하단 note (우측 라벨은 x487 까지)
        "4.9":  (200.0, 227.0, 552.0, 390.0),  # 캡션+2패널. 위 'Figure 4.9 illustrates…'·아래 prose 제외 (union OFF)
        "4.10": (172.0, 174.0, 485.0, 316.0),  # 캡션+패널만, 위 prose·아래 ratio 제외 (union OFF)
    },
    5: {
        "5.5": ( 72.0,  95.0, 550.0, 325.0),   # 3패널+내부 note, 하단 'Consider…'(y330) 제외 (union OFF)
        "5.6": (115.0, 511.0, 580.0, 709.0),   # 좌측 5줄 캡션 + 패널(x축 'Discount rate' y688·Project B 라벨까지) (union OFF)
    },
    6: {
        "6.1": ( 85.0,  92.0, 551.0, 255.0),   # 좌측 2줄 캡션 + 패널 전체(내부 note 'Hamburgers…' y236 포함), 하단 본문 제외 (union OFF)
    },
    7: {  # decision tree·break-even — 좌측 멀티라인 캡션 + 패널 전체(내부 note 포함), 본문 트림. 전부 union OFF
        "7.1": ( 88.0, 455.0, 533.0, 707.0),   # break-even 차트 + 내부 note 'The pretax…'(패널 하단)
        "7.4": ( 88.0,  92.0, 535.0, 312.0),   # Monte Carlo 분포 + 내부 note, 'STEP 4' 본문(y319) 제외
        "7.5": ( 88.0,  92.0, 511.0, 226.0),   # Ice Hotel 의사결정나무 (page 251 상단 패널)
        "7.6": ( 80.0,  92.0, 551.0, 330.0),   # Abandonment 영화 나무 + 내부 note
        "7.7": ( 90.0,  92.0, 532.0, 251.0),   # Vacant Land 나무 (기본추출이 일부만 잡던 것 전체 복구)
    },
    8: {  # 좌측 멀티라인 캡션 + 패널 전체. union OFF
        "8.2": ( 76.0,  92.0, 551.0, 447.0),   # interest rate risk 차트 (하단 x축까지, 패널 y443)
        "8.7": ( 82.0,  92.0, 551.0, 487.0),   # term structure 2-패널(A 상향+B 하향), 우측 'Nominal interest rate' 라벨 포함
    },
    9: {  # union OFF
        "9.1": ( 88.0,  92.0, 502.0, 420.0),   # growth pattern 차트 + 내부 공식(Zero/Constant/Differential), 'The general model' 본문(y460) 제외
        "9.2": (206.0, 369.0, 511.0, 637.0),   # Elixir 배당성장 차트(가로 캡션 y371 + 패널), 'displays' 본문(y639) 제외
    },
    10: {  # 좌측/상단 캡션 포함, 본문·인접 figure 캡션 트림. 전부 union OFF
        "10.1":  (100.0,  90.0, 466.0, 263.0),  # 좌측 캡션 + Dollar Returns 타임라인(우측 TOTAL/Dividends/Ending mv 라벨 포함), 본문(y268) 제외
        "10.2":  (110.0, 458.0, 534.0, 617.0),  # 좌측 캡션 + Percentage Returns 다이어그램, 하단 percentage-return 공식 본문(y619) 제외
        "10.5":  (150.0,  93.0, 577.0, 395.0),  # 상단 캡션 + large-stock 차트 + SOURCE, 하단 10.6 캡션(y401) 제외
        "10.10": (100.0, 402.0, 550.0, 581.0),  # 좌측 캡션 + 종형곡선 + σ축 라벨 + 'Return on stocks', 본문(y584) 제외
        "10.11": (100.0,  92.0, 577.0, 360.0),  # 좌측 캡션 + 17개국 막대 + 국가명 + 'Country' + SOURCE, 본문(y379) 제외
        "10.12": (100.0,  92.0, 577.0, 315.0),  # 좌측 캡션 + S&P500 월별 차트 + 월 라벨, 하단 본문(y349) 제외
    },
    11: {  # 내부 note 포함/본문·footnote·요약표 트림. 전부 union OFF
        "11.4":  (110.0,  92.0, 548.0, 370.0),  # 좌측 캡션 + ρ별 opportunity set 차트 + 내부 note('Each curve…'), 본문(y393) 제외
        "11.8":  (228.0,  94.0, 548.0, 370.0),  # 상단 캡션 + riskless+risky 차트, 하단 본문(y379) 제외(+4px 마진 고려해 370)
        "11.9":  ( 76.0,  90.0, 518.0, 363.0),  # 좌측 캡션 + CML 차트 + 내부 note('Portfolio Q…'), 본문(y378)·요약표 제외
        "11.11": ( 84.0, 440.0, 546.0, 683.0),  # 좌측 캡션 + SML 차트 + 내부 note, 하단 footnote(y688) 제외
    },
    12: {  # union OFF
        "12.1": (110.0, 408.0, 556.0, 700.0),  # 좌측 캡션 + One-Factor 차트 + 내부 note('Each line…' y668), 상단 본문(y386) 제외
        "12.4": (100.0,  90.0, 526.0, 289.0),  # 좌측 캡션 + SML(market) 차트 전체(우측 'Security market line' x502·Beta축·내부 note 포함), 본문(y302) 제외
    },
    13: {  # union OFF
        "13.1": ( 88.0,  92.0, 489.0, 290.0),  # 좌측 캡션 + extra-cash 다이어그램(아래 화살표) + 내부 note('Investors want…' y238), 본문(y299) 제외
    },
    # ch14: 표준 추출이 하단 라벨/노트/x축·우측 라벨을 잘라 → render_page rects 기반 수동 box
    14: {
        "14.1":  (196.0, 382.0, 641.0, 736.0),   # 하단 라벨 + 우측 라벨
        "14.2":  (193.0,  90.0, 625.0, 334.0),   # 하단/우측 Buy 라벨
        "14.4":  (233.0,  92.0, 542.0, 456.0),   # 2-그래프(A 시뮬·B Gap) 멀티패널
        "14.7":  (167.0, 411.0, 560.0, 706.0),   # 하단 x축
        "14.9":  (188.0,  90.0, 625.0, 450.0),   # 하단 x축 라벨(14.10 위, y<472)
        "14.11": (188.0,  90.0, 568.0, 384.0),   # 하단 설명 note
        "14.13": (193.0,  90.0, 643.0, 400.0),   # 우측 라벨(페이지 끝까지)
        "14.14": (190.0,  90.0, 625.0, 614.0),   # 하단 note + 우측 라벨
    },
    # 19.7: 같은 페이지 본문이 union 에 혼입 → 차트 img(171,94.7,546,299)+SOURCE 까지만
    19: {"19.7": (171.0, 92.0, 547.0, 309.0)},
    20: {  # union OFF
        "20.2": ( 78.0, 363.0, 550.0, 572.0),  # 좌측 캡션 + Exit Funnel 파이 + 'Known Failed 18%' 라벨 + SOURCE, 본문(y583) 제외
        "20.5": ( 92.0,  92.0, 533.0, 726.0),  # 좌측 캡션 + 전체 tombstone 광고(세로 긴 단일 이미지 y95-723)
    },
    22: {  # union OFF. 옵션 payoff/Black-Scholes — 우측 라벨·내부 note·하단 x축 잘림 복구
        "22.7":  (104.0, 505.0, 526.0, 708.0),  # 페이지 하단 figure. 좌측 캡션 + upper/lower bound 차트 + 우측 'Lower bound=Price−Exercise' 라벨 + 내부 note(table 22.x 는 제외)
        "22.8":  (110.0,  92.0, 524.0, 313.0),  # 좌측 캡션 + American call 차트 + 우측 'Min value of call' + 내부 note, 본문(y353)·Table 22.2 제외
        "22.10": (170.0, 490.0, 492.0, 698.0),  # 'Table 22.10' 누적확률 종형곡선(N(d), 캡션='Figure 22.10' prose). 본문(y487) 제외
        "22.11": ( 80.0,  92.0, 506.0, 292.0),  # 좌측 캡션 + Popov 주주 cash flow 차트 + 내부 note, 본문(y308) 제외
        "22.12": (108.0,  92.0, 505.0, 311.0),  # 좌측 캡션 + Popov 채권자 cash flow 차트 + 내부 note, 본문(y328) 제외
    },
    23: {  # union OFF. 이항트리/시뮬 경로 — 우측 라벨·내부 note·전체 트리 복구
        "23.1": ( 78.0,  90.0, 504.0, 303.0),  # 좌측 캡션 + 2-date 트리 + 우측 '$2.74($.64=…)' 라벨 + 내부 note, 본문(y305) 제외
        "23.2": ( 78.0,  90.0, 505.0, 400.0),  # 좌측 캡션 + 3-date 트리 + 우측 '$3.13($1.03=…)' + 내부 note, 본문(y410) 제외
        "23.3": ( 82.0, 310.0, 540.0, 700.0),  # 페이지 하단 figure. 좌측 캡션 + 전체 gold 이항트리(좌하단까지) + x축 + 내부 note
        "23.4": ( 82.0,  90.0, 540.0, 430.0),  # 좌측 캡션 + gold 시뮬 경로 + 광산 open/close 주석 + 내부 note, 본문(y451) 제외
    },
    24: {  # union OFF
        "24.3": ( 82.0, 384.0, 515.0, 645.0),  # 페이지 하단 figure. 좌측 캡션 + convertible bond 가치 차트 + 내부 note('As shown…'), footnote(y663) 제외
    },
    26: {  # union OFF. operating-cycle/정책 다이어그램 — 내부 note·하단 라벨 잘림 복구
        "26.1": (104.0,  92.0, 578.0, 322.0),  # 좌측 캡션 + cash-cycle 타임라인 + 'Operating cycle' 화살표 + 내부 note, 본문(y356) 제외
        "26.2": ( 82.0,  91.0, 550.0, 692.0),  # 좌측 캡션 + 3패널(optimal/flexible/restrictive, 세로 긴 y93-701) + 내부 note
        "26.3": ( 80.0,  92.0, 550.0, 282.0),  # 좌측 캡션 + ideal-economy sawtooth + '0 1 2 3 4' 축 + 내부 note, 본문(y319) 제외
        "26.5": ( 90.0,  92.0, 578.0, 465.0),  # 좌측 캡션 + Strategy F/R 2패널 + 내부 note('Strategy F always…'), 본문(y487) 제외
    },
    27: {  # union OFF. cash-management flowchart/차트 — 우측·하단 잘림 복구
        "27.3": (104.0,  92.0, 578.0, 445.0),  # 좌측 캡션 + lockbox flowchart 전체(4개 Customer 박스 우측까지) + 내부 note, 본문(y476) 제외
        "27.4": ( 76.0,  92.0, 550.0, 455.0),  # 좌측 캡션 + concentration flowchart 전체(하단 박스행까지), 본문(y488)·여백노트 제외
        "27.6": (100.0, 454.0, 550.0, 692.0),  # 페이지 하단 figure. 좌측 캡션 + seasonal 차트(우측 'Total financing needs') + 내부 note
    },
    28: {  # union OFF
        "28.1": ( 98.0, 451.0, 528.0, 688.0),  # 페이지 하단 figure. 좌측 캡션 + credit cost 차트 + 내부 note('Carrying costs are…'). y0=451(−4px 마진 고려, 상단 본문 'opportunities.' 제외)
        "28.5": (100.0,  92.0, 578.0, 698.0),  # 좌측 캡션 + safety/reorder 3패널(A/B/C, 세로 긴 y94-705) + 각 패널 note
    },
}


def _union_rect(page, caption_prefix: str, top_margin: float = 70, bot_margin: float = 55):
    """캡션 아래 region 의 모든 figure 그래픽(이미지+큰 벡터)+캡션 블록의 합집합 rect."""
    page_w, page_h = page.rect.width, page.rect.height
    rects = []
    for img in page.get_image_info():
        b = fitz.Rect(img["bbox"])
        if b.width >= 40 and b.height >= 40:
            rects.append(b)
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 6 or r.height < 6:
            continue
        if r.width > page_w * 0.92 and r.height > page_h * 0.92:  # 페이지 전체 배경/테두리
            continue
        if r.height < 1.5 and r.width > page_w * 0.7:   # 가로 rule/separator
            continue
        if r.y0 < top_margin or r.y1 > page_h - bot_margin:
            continue
        rects.append(r)
    if not rects:
        return None
    u = fitz.Rect(rects[0])
    for r in rects[1:]:
        u = u | r
    _, cap_block = _find_caption(page, caption_prefix)
    if cap_block is not None:
        u = u | cap_block
    return fitz.Rect(
        max(2, u.x0 - 6), max(2, u.y0 - 6),
        min(page_w - 2, u.x1 + 6), min(page_h - 2, u.y1 + 10),
    )


def _crop(page, rect, out_path: str, dpi: float = 2.5) -> None:
    page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), clip=rect).save(out_path)


def _extract_union(pidx: int, fnum: str, out_path: str) -> bool:
    doc = fitz.open(PDF)
    page = doc[pidx]
    rect = _union_rect(page, f"Figure {fnum}")
    ok = rect is not None
    if ok:
        _crop(page, rect, out_path)
    doc.close()
    return ok


def _extract_manual(pidx: int, fnum: str, box: tuple, out_path: str,
                    union_caption: bool = True) -> bool:
    """수동 차트 bbox + (자동 탐지) 캡션 블록 union 으로 crop.

    union_caption=False 면 box 를 그대로 쓴다 (캡션 '위' prose 가 같은 figure
    번호를 언급해 _find_caption 이 prose 를 잡는 EXAMPLE 박스용 — NO_CAPTION_UNION).
    """
    doc = fitz.open(PDF)
    page = doc[pidx]
    rect = fitz.Rect(*box)
    if union_caption:
        _, cap_block = _find_caption(page, f"Figure {fnum}")
        # 캡션 블록은 box 와 *세로로 근접* 할 때만 union — 같은 페이지의 멀리 떨어진
        # prose("Figure 1.3. The arrows…")가 잡혀 box 를 본문까지 늘리는 것 방지.
        if cap_block is not None and cap_block.y1 >= box[1] - 50 and cap_block.y0 <= box[3] + 50:
            rect = rect | cap_block
    rect = fitz.Rect(rect.x0 - 4, rect.y0 - 4, rect.x1 + 4, rect.y1 + 4)
    _crop(page, rect, out_path)
    doc.close()
    return True


def run(chapter: int, out: str | None = None) -> None:
    figs = CHAPTERS.get(chapter)
    if not figs:
        print(f"ch{chapter}: CHAPTERS 에 미등록 — find_figures.py 로 먼저 페이지 탐색")
        return
    out_dir = out or os.path.join(OUT_BASE, f"ch{chapter:02d}")
    os.makedirs(out_dir, exist_ok=True)
    multi = MULTIPANEL.get(chapter, set())
    manual = MANUAL.get(chapter, {})
    no_union = NO_CAPTION_UNION.get(chapter, set())
    special = multi | set(manual)
    print(f"ch{chapter}: {len(figs)}개 figure → {out_dir}  "
          f"(union: {sorted(multi) or '-'}, manual: {sorted(manual) or '-'})")

    standard = {k: v for k, v in figs.items() if k not in special}
    if standard:
        extract_figures(
            pdf=PDF, out_dir=out_dir, figs=standard,
            caption_format="Figure {num}", caption_pos="above",
        )
    for fnum in sorted(multi):
        out_path = os.path.join(out_dir, f"fig-{fnum.replace('.', '-')}.png")
        ok = _extract_union(figs[fnum], fnum, out_path)
        size = os.path.getsize(out_path) / 1024 if ok else 0
        print(f"{'OK  ' if ok else 'FAIL'} Fig {fnum} (union) -> {os.path.basename(out_path)}  ({size:.0f}KB)")
    for fnum, box in sorted(manual.items()):
        out_path = os.path.join(out_dir, f"fig-{fnum.replace('.', '-')}.png")
        _extract_manual(figs[fnum], fnum, box, out_path, union_caption=fnum not in no_union)
        tag = "manual" if fnum not in no_union else "manual,no-cap-union"
        size = os.path.getsize(out_path) / 1024
        print(f"OK   Fig {fnum} ({tag}) -> {os.path.basename(out_path)}  ({size:.0f}KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    ch = int(sys.argv[1])
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    run(ch, out_path)
