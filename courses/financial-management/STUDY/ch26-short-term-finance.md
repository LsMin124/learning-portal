# Chapter 26: Short-Term Finance and Planning — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 26** (책 p.811~838).
> 26장은 *단기 재무 + 운전자본* — operating/cash cycle, 단기 정책, cash budget.

이 장의 *지적 무게중심*:
1. **Operating cycle / Cash cycle** — 자금이 묶이는 기간
2. **단기 재무정책** — flexible vs restrictive
3. **Carrying vs Shortage cost** — 최적 운전자본
4. **Cash budget** — 단기 현금 계획
5. **단기 차입** — line of credit, commercial paper

---

## §0 도입 — *사업을 굴리는 돈*

> **핵심 한 문장**: 장기 자본예산(2~13장)이 "어떤 자산을 살까"였다면, 26장은 그 사업을 *굴리는 동안* 묶이는 단기 자금 — 재고·매출채권에서 매입채무를 뺀 **cash cycle** — 을 관리한다. cash cycle 이 길수록 자금이 더 필요하고, 정책은 *안전과 수익* 을 맞바꾼다.

운전자본 관리는 네 질문으로 흐른다:

1. **돈은 얼마나 오래 묶이나** (§2): 재고를 사서(현금 유출) 팔고 대금을 받기까지가 *operating cycle*, 거기서 매입채무 유예를 뺀 게 *cash cycle*(figure 26.1) — 현금이 실제로 발이 묶이는 기간. Dell·Amazon 은 이걸 *음수* 로 만들어 공급업체 돈으로 영업한다.
2. **유동자산을 얼마나 들고 있을까** (§3–4): *flexible*(많이, 안전·수익↓)과 *restrictive*(적게, 수익↑·위험↑)의 trade-off. 최적은 *carrying cost(보유)* 와 *shortage cost(부족)* 의 합이 최소인 점(figure 26.2).
3. **그 자산을 무엇으로 조달하나** (§5): *maturity matching* — 영구 자산은 장기 자금, 계절 자산은 단기 자금(figure 26.3·26.4). flexible 은 거의 다 장기로(figure 26.5 의 Strategy F), restrictive 는 단기를 적극 쓴다(Strategy R).
4. **현금 타이밍을 어떻게 예측하나** (§6–7): *cash budget* 으로 월별 과부족을 내다보고, 부족분은 line of credit·commercial paper 로 메운다(compensating balance 가 실효이자를 올린다).

한 문장으로: **단기 재무는 "현금이 얼마나, 얼마나 오래 묶이고, 무엇으로 메우나"의 관리다.**

---

## §1 운전자본 (Working Capital) 기초

### §1.1 정의

> *Net working capital* = 유동자산 − 유동부채.

- 유동자산: 현금, 매출채권, 재고
- 유동부채: 매입채무, 단기차입
- *단기 = 1년 이내* (또는 영업주기 이내)

### §1.2 단기 재무의 핵심 질문

1. *얼마나* 유동자산 보유? (투자 수준)
2. *어떻게* 단기 자금 조달? (financing)
3. *현금흐름 타이밍* 관리

---

## §2 Operating Cycle & Cash Cycle

### §2.1 Operating Cycle (영업주기)

> 재고 매입 → 판매 → 대금 회수까지의 기간.

$$\text{Operating cycle} = \text{Inventory period} + \text{AR period}$$

- *Inventory period* — 재고 보유 기간
- *AR period* (매출채권 기간) — 외상 회수 기간

### §2.2 Cash Cycle (현금주기)

> 현금 *지출* → 현금 *회수*까지의 기간.

$$\text{Cash cycle} = \text{Operating cycle} - \text{AP period}$$

- *AP period* (매입채무 기간) — 외상 지급 유예
- = 현금이 *묶이는* 기간

### §2.3 각 기간 공식

| 기간 | 공식 |
|--|--|
| Inventory period | 365 / 재고회전율 = 365 × 평균재고/COGS |
| AR period | 365 / 매출채권회전율 = 365 × 평균AR/매출 |
| AP period | 365 × 평균AP/COGS |

### §2.4 직관

```
매입 ─── 판매 ─────── 회수
  │       │            │
  │←재고→│←─── AR ───→│
  │←──── Operating cycle ────→│
        │
  지급 ─┘
  │←AP→│
        │←──── Cash cycle ────→│
```

- *Cash cycle ↑* → 운전자본 투자 ↑ → 자금 필요 ↑
- *Cash cycle ↓* → 효율적 (Dell, Amazon: 음수 가능)

---

![Figure 26.1 — Cash Flow Time Line and the Short-Term Operating Activities of a Typical Manufacturing Firm. 교재 p.799](/courses/financial-management/figures/ch26/fig-26-1.png)

> **직관**: *cash cycle* 을 타임라인으로. 재고 매입(현금 유출)부터 판매까지가 *inventory period*, 판매부터 대금 회수까지가 *AR period* — 둘을 합치면 *operating cycle*. 그런데 매입대금은 나중에 내므로(*AP period*), 현금이 실제 묶이는 *cash cycle* = operating − AP. 이 기간만큼 운전자본 자금이 필요하다.

---

## §3 단기 재무정책

### §3.1 두 차원

**1. 유동자산 투자 규모**:
- *Flexible (보수적)*: 유동자산 多 (현금, 재고, 관대한 신용)
- *Restrictive (공격적)*: 유동자산 少

**2. 단기 부채 사용 정도**:
- *Flexible*: 장기 자금으로 충당 (단기차입 少)
- *Restrictive*: 단기차입 多

### §3.2 Flexible vs Restrictive

| | Flexible | Restrictive |
|--|--|--|
| 유동자산 | 多 | 少 |
| 현금/재고 | 高 | 低 |
| 신용 정책 | 관대 | 엄격 |
| 위험 | 낮음 | 높음 |
| 수익성 | 낮음 | 높음 |

### §3.3 Trade-off

- *Flexible*: 안전 but 수익성 ↓ (유휴 자산)
- *Restrictive*: 수익성 ↑ but 위험 ↑ (품절, 부도)

---

## §4 Carrying Cost vs Shortage Cost

### §4.1 두 비용

**Carrying cost (보유비용)**:
- 유동자산 보유 비용 (기회비용, 보관)
- 자산 ↑ → carrying cost ↑

**Shortage cost (부족비용)**:
- 유동자산 부족 비용 (품절, 거래중단, 긴급조달)
- 자산 ↓ → shortage cost ↑

### §4.2 최적 운전자본

$$\text{Total cost} = \text{Carrying} + \text{Shortage} \to \min$$

- 두 비용 합 최소화 지점
- *Flexible* = carrying > shortage
- *Restrictive* = shortage > carrying

### §4.3 그래프

```
비용
  │ \  Carrying    / Total
  │  \           /
  │   \        /
  │    \     /  ← 최적
  │     \  /
  │      \/  Shortage
  │___________________ 유동자산
```

---

![Figure 26.2 — Carrying Costs and Shortage Costs. 교재 p.806](/courses/financial-management/figures/ch26/fig-26-2.png)

> **직관**: 유동자산을 얼마나 들지 결정하는 *비용 트레이드오프*. *carrying cost*(보유비용, 우상향)와 *shortage cost*(부족비용, 우하향)의 합인 total cost 가 최소가 되는 CA* 가 최적. 아래 두 패널처럼 *flexible*(carrying 우세)·*restrictive*(shortage 우세) 정책에 따라 최적점이 옮겨간다.

---

## §5 자금 조달 — 만기 매칭

### §5.1 Maturity Matching (만기 대응)

> *자산 수명 = 부채 만기* 매칭 (헤징 접근).

- 장기 자산 → 장기 자금
- 단기/계절 자산 → 단기 자금

![Figure 26.3 — Financing Policy for an Ideal Economy. 교재 p.808](/courses/financial-management/figures/ch26/fig-26-3.png)

> **직관**: *이상적 경제* 의 만기매칭. 고정자산(장기 부채로 조달, 우상향 직선)과 계절적 유동자산(톱니, 단기 부채로 조달)이 정확히 매칭돼 *순운전자본이 항상 0*. 단기 자산은 단기 부채로, 장기 자산은 장기 자본으로 — 헤징 접근의 교과서적 그림.

### §5.2 세 가지 전략

| 전략 | 영구 자산 | 계절 자산 |
|--|--|--|
| Maturity matching | 장기 | 단기 |
| Flexible (보수적) | 장기 | 장기 (잉여 → 단기투자) |
| Restrictive (공격적) | 단기+장기 | 단기 |

![Figure 26.5 — Alternative Asset Financing Policies. 교재 p.809](/courses/financial-management/figures/ch26/fig-26-5.png)

> **직관**: 두 극단 전략. *Strategy F*(flexible): 장기 자금을 *총자산 수요의 정점 위* 로 잡아 평소엔 잉여를 marketable securities 로 굴린다(안전, 수익↓). *Strategy R*(restrictive): 장기 자금을 낮게 잡고 부족분을 *단기 차입* 으로 메운다(수익↑, 위험↑). 둘 사이가 maturity matching.

### §5.3 누적 자금 수요

- *영구 운전자본* — 항상 필요 (장기 조달)
- *계절 운전자본* — 변동 (단기 조달)

---

![Figure 26.4 — The Total Asset Requirement over Time. 교재 p.808](/courses/financial-management/figures/ch26/fig-26-4.png)

> **직관**: 현실의 *총자산 수요*. 고정자산+영구 운전자본이 *꾸준히 성장*(직선)하는 위에 *계절 변동*(물결)이 얹힌다. 직선 부분은 장기 자금으로, 물결 부분은 단기 자금으로 대는 게 maturity matching — §5.2 전략들의 출발점.

---

## §6 Cash Budget (현금예산)

### §6.1 정의

> 단기 *현금 유입·유출* 예측 → 자금 과부족 파악.

### §6.2 구성

1. *Cash inflows* — 현금 매출 + 매출채권 회수
2. *Cash outflows* — 매입, 인건비, 세금, 자본지출
3. *Net cash flow* = 유입 − 유출
4. *Cumulative cash* — 누적 → 차입/투자 결정

### §6.3 활용

- *현금 부족* → 단기차입 계획
- *현금 잉여* → 단기투자 (Ch 27)
- *계절성* 파악

---

## §7 단기 차입

### §7.1 무담보 대출 (Unsecured)

**Line of credit (신용한도)**:
- *Committed* — 수수료 지급, 보장
- *Uncommitted* — 비공식
- *Compensating balance* — 보상예금 (실효이자 ↑)
- *Cleanup* — 연중 일정기간 상환 요구

### §7.2 담보 대출 (Secured)

- *AR financing* — 매출채권 담보 (assigning / factoring)
- *Inventory financing* — 재고 담보 (blanket lien, trust receipt, warehouse)

### §7.3 Commercial Paper (CP)

- *대기업* 단기 무담보 어음
- 만기 < 270일
- 은행 대출보다 *저렴*
- 신용등급 우량 기업만

### §7.4 실효이자율

> Compensating balance / discount → 실효이자 ↑.

$$\text{실효이자} = \frac{\text{이자}}{\text{실제 사용가능 금액}}$$

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Operating cycle = cash cycle | Cash = operating − AP |
| 2 | Cash cycle 짧을수록 무조건 좋음 | 너무 짧으면 공급 차질 |
| 3 | Flexible = 항상 우월 | 수익성 ↓ (trade-off) |
| 4 | Carrying cost 만 고려 | + shortage cost |
| 5 | 단기차입 = 항상 위험 | 만기매칭이 핵심 |
| 6 | Compensating balance 무시 | 실효이자 ↑ |
| 7 | AP 연장 = 항상 이득 | 할인 포기 비용 (Ch 28) |

---

## §9 자가점검

1. *Operating cycle* vs *Cash cycle* 공식?
2. *Flexible vs Restrictive* 정책 차이?
3. *Carrying vs Shortage cost* 와 최적?
4. *Maturity matching* 이란?
5. *Cash budget* 구성?
6. *Line of credit / Commercial paper*?

<details><summary>해답</summary>

1. Operating = inventory period + AR period. Cash = operating − AP period (현금 묶이는 기간).
2. Flexible: 유동자산 多 (안전, 수익성↓). Restrictive: 유동자산 少 (수익성↑, 위험↑).
3. Carrying (보유비용, 자산↑→↑) vs shortage (부족비용, 자산↓→↑). Total = carrying + shortage 최소.
4. 자산 수명 = 부채 만기 매칭 (장기자산→장기자금, 계절자산→단기자금).
5. Cash inflows (매출+AR 회수) − outflows (매입/인건비/세금) = net → cumulative → 차입/투자.
6. Line of credit: 신용한도 (committed/uncommitted, compensating balance). CP: 대기업 단기 무담보 어음 (<270일, 저렴).

</details>

---

## §10 다음 학습으로

- **Ch 27** — Cash management (현금 자체 관리)
- **Ch 28** — Credit and inventory (AR/재고 정책)
- **Ch 2** — 재무제표 (운전자본 항목)

---

## §11 한 줄 요약

> **단기 재무 = 운전자본 관리. *Operating cycle* = inventory period + AR period. *Cash cycle* = operating − AP period (현금 묶이는 기간, 짧을수록 효율 but 한계). *정책*: flexible (유동자산 多, 안전·수익↓) vs restrictive (少, 수익↑·위험↑). *최적* = carrying cost + shortage cost 최소. *Maturity matching* (자산수명=부채만기). *Cash budget* (유입−유출→차입/투자). *단기차입*: line of credit (compensating balance→실효이자↑), commercial paper (대기업, 저렴).**
