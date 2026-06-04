# Chapter 5: Net Present Value and Other Investment Rules — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 5** (책 p.133~167).
> 5장은 *Capital Budgeting* 의 *결정 규칙*. **NPV** 가 *gold standard*. 다른 규칙 (Payback, IRR, PI) 의 *각 약점* + *NPV 와 충돌* 의 학습.

이 장의 *지적 무게중심*:
1. **NPV Rule** — *유일 sound criterion*
2. **Payback Period** — 단순 + 결함
3. **Internal Rate of Return (IRR)** — popular but flawed
4. **Profitability Index** — capital rationing
5. **The Practice of Capital Budgeting** — 실제 회사

---

## §0 도입 — *결정 규칙* 들의 경연

> **핵심 한 문장**: 좋은 투자 규칙은 *(1) 돈의 시간가치, (2) 위험, (3) 가치의 가산성* 을 모두 반영해야 한다 — 이 셋을 다 갖춘 건 **NPV 뿐**.

4장이 "미래 현금흐름을 현재가치로 바꾸는 *기계*" 였다면, 5장은 그 기계로 "*이 프로젝트를 할까 말까*" 를 정하는 **규칙들의 비교** 다. 후보는 넷:

| 규칙 | 한 줄 | 평가 |
|--|--|--|
| **NPV** | 미래 CF 의 PV 합 − 투자 | *gold standard* |
| **Payback** | 원금 회수 기간 | 시간가치·후속 CF 무시 |
| **IRR** | NPV=0 의 수익률 | 직관적·인기, *4가지 함정* |
| **PI** | PV / 투자 | capital rationing 에서만 우위 |

이 장의 드라마는 대부분 **IRR 이 NPV 와 충돌하는 순간** 에 있다 (multiple IRR / financing 역방향 / scale / timing — §4). figure 5.4~5.6 의 ***NPV profile*** (discount rate 를 x축, NPV 를 y축에 그린 곡선) 이 그 충돌을 시각적으로 푼다:

> **곡선이 x축을 만나는 점 = IRR**, **세로선 r=hurdle 에서의 곡선 높이 = NPV**.

둘이 *언제 일치하고 언제 갈라지는지* 가 5장의 전부다.

---

## §1 The Net Present Value Rule

### §1.1 NPV 의 정의

$$NPV = -C_0 + \sum_{t=1}^{T} \frac{CF_t}{(1+r)^t}$$

**Decision rule**:
- NPV > 0 → **accept**
- NPV < 0 → **reject**
- NPV = 0 → indifferent

![Figure 5.1 — Cash Flows of an Investment Project. 교재 p.136](/courses/financial-management/figures/ch05/fig-5-1.png)

> **직관**: 4장의 timeline 이 그대로 capital budgeting 으로 넘어온다. 지금 $50,000 을 쓰고(−$50,000) 1·2·3년 후 $30k·$20k·$10k 를 받는다. NPV 는 이 미래 화살표 셋을 *모두 현재로 discount* 한 뒤 −$50,000 과 더한 값. 양수면 *가치 창출* → 채택.

### §1.2 *왜 NPV* 가 *gold standard*

1. **Cash flow** 의 *timing* + *magnitude* 반영
2. **Discount rate** 가 *risk* 의 정량적 표현
3. **Additive** — NPV(A+B) = NPV(A) + NPV(B)
4. **Value creation** 직접 측정 — shareholder wealth 증분
5. **Mutual exclusivity** 에서 명확한 결정

### §1.3 NPV 의 *경제적 해석*

**예** — Project: $-100 today, $130 in 1 year, r = 10%.

$$NPV = -100 + \frac{130}{1.10} = -100 + 118.18 = \$18.18$$

- *Project value* = $118.18 (PV of future CF)
- *Cost* = $100
- *Value created* = $18.18

→ 채택 시 *shareholder wealth* $18.18 증가.

---

## §2 The Payback Period Method

### §2.1 정의

> *초기 투자* 회수 까지 *기간*.

**예**:
- Initial: -$10,000
- Year 1: $3,000
- Year 2: $4,000
- Year 3: $5,000

Payback = 2 + 3000/5000 = **2.6 years**

### §2.2 *Payback 의 *3 가지 fatal flaw**

1. **Time value of money 무시** — $1 today + $1 tomorrow 동등
2. **Cash flow after payback 무시** — Long-term project 차별
3. **임의의 cutoff** — *근거 없는* 선택

### §2.3 Payback 의 *valid use*

- *Simple* (calculator 불필요)
- *Quick screening*
- *Liquidity-focused* (small firm, distressed)
- *High-uncertainty* (emerging market, R&D)
- *Capital-constrained*

→ *Primary tool* 아닌 *supplementary screen*.

### §2.4 Discounted Payback Period

> Payback + *discounting*.

**위 예** at r = 10%:
- Year 1 PV: $3000/1.1 = $2727
- Year 2 PV: $4000/1.21 = $3306
- Year 3 PV: $5000/1.331 = $3757

누적: $2727, $6033, $9790, ...

→ Discounted payback > 3 year.

Flaw 2, 3 여전히 존재. *NPV 가 더 우수*.

---

## §3 The Internal Rate of Return (IRR)

### §3.1 정의

> IRR = *NPV = 0* 으로 만드는 discount rate.

$$0 = -C_0 + \sum_{t=1}^{T} \frac{CF_t}{(1 + IRR)^t}$$

![Figure 5.2 — Cash Flows for a Simple Project. 교재 p.140](/courses/financial-management/figures/ch05/fig-5-2.png)

> **직관**: 가장 단순한 프로젝트 — 지금 $100, 1년 후 $110. 이 *한 번의 sign change*(−→+) 가 IRR 을 *유일하게* 보장한다. NPV=0 으로 만드는 r = 10% 가 IRR. 부호 변화 1번 = IRR 1개의 보증수표.

### §3.2 Decision rule

- IRR > required rate → accept
- IRR < required rate → reject

### §3.3 IRR 의 *직관*

> IRR = *project 의 yield*.

**예** — $-100 today, $130 in 1 year:
$$0 = -100 + \frac{130}{1 + IRR} \Rightarrow IRR = 30\%$$

→ 만약 *required* 10% 면 *30% > 10%* → accept.

![Figure 5.3 — Cash Flows for a More Complex Project. 교재 p.141](/courses/financial-management/figures/ch05/fig-5-3.png)

> **직관**: 다기간 버전 — −$200 뒤 3년간 $100 씩. IRR 은 $0 = -200 + \sum 100/(1+IRR)^t$ 를 푸는 r 인데 손으로는 안 풀려 *시행착오/계산기* 가 필요하다. 그 해가 아래 그림(5.4)의 곡선이 0 을 지나는 지점.

![Figure 5.4 — NPV Profile for a More Complex Project. 교재 p.142](/courses/financial-management/figures/ch05/fig-5-4.png)

> **직관**: 위 5.3 프로젝트의 ***NPV profile*** — discount rate 를 x축, NPV 를 y축에 그린 곡선. r=0 이면 NPV=$100(현금 합−투자), r 이 오를수록 NPV 하락, **23.38% 에서 0 을 통과**(=IRR). NPV rule(세로선 r=hurdle 의 높이)과 IRR rule(곡선이 x축 닿는 점)이 *왜 보통 같은 답* 을 주는지 한눈에 보인다.

### §3.4 NPV vs IRR — *agreement* 의 조건

**Conventional project** (-, +, +, +, ...) + *single sign change*:
- NPV 와 IRR 가 *같은 결정*

---

## §4 IRR 의 4 가지 문제

![Figure 5.5 — NPV Profile for Projects A, B, and C. 교재 p.144](/courses/financial-management/figures/ch05/fig-5-5.png)

> **직관**: IRR 이 무너지는 *세 가지 곡선 모양*. **A**(−,+): 우하향 — 정상, IRR 1개. **B**(+,−): 우상향 — *financing* 이라 규칙이 뒤집힌다(§4.3). **C**(−,+,−): 부호 변화 2번 — 봉우리 모양이라 x축을 *두 번* 만나 IRR 2개(§4.1), r→∞ 면 −100 으로 수렴. *부호 변화 횟수 = IRR 개수의 상한*.

### §4.1 *Multiple IRRs*

**Cash flow 가 *sign change 여러 번***:

**예** — Strip mine:
- Year 0: $-100
- Year 1: $230
- Year 2: $-132

→ NPV = 0 의 *해 2 개*:
- IRR_1 = 10%
- IRR_2 = 20%

→ *어떤 IRR* 사용? *Both valid mathematically*.

**Solution**: **Modified IRR (MIRR)** 또는 *NPV 만 사용*.

### §4.2 *No IRR*

**Cash flow 가 *NPV positive 영원히***:
- Year 0: $-100
- Year 1: $1000
- Year 2: $-50

→ NPV 가 모든 r 에서 양수. *No IRR* 존재.

### §4.3 *Investing vs Financing* 의 *역방향*

**Investing project** (-, +, +, ...) — IRR > hurdle → accept

**Financing project** (+, -, -, ...) — IRR > hurdle → ***REJECT***

**예 — Loan**:
- Year 0: +$1000 (loan 받음)
- Year 1: -$1200 (상환)

→ IRR = 20%. Cost of capital 10% < IRR → *NPV는 negative*.

→ *Financing project 에서는 IRR < required* 면 accept.

### §4.4 *Mutually Exclusive Project* — *scale + timing*

**Scale problem**:

| | Project A | Project B |
|--|--|--|
| Initial | $-100 | $-10,000 |
| Year 1 | $200 | $15,000 |
| IRR | 100% | 50% |
| NPV (r=10%) | $82 | $3636 |

→ IRR 은 A 선호, NPV 는 B 선호. *NPV correct* (B 가 *더 많은 가치 생성*).

**Solution**: *Incremental IRR*.

**Timing problem**:

| | Project A | Project B |
|--|--|--|
| Initial | $-100 | $-100 |
| Year 1 | $130 | $0 |
| Year 3 | $0 | $180 |
| IRR | 30% | 21.6% |

**At r = 10%**:
- NPV(A) = $18.18
- NPV(B) = $35.24

→ IRR 은 A, NPV 는 B. *Discount rate 의 *crossover***.

![Figure 5.6 — Net Present Value and the Internal Rate of Return for Mutually Exclusive Projects. 교재 p.151](/courses/financial-management/figures/ch05/fig-5-6.png)

> **직관**: 상호배타 A·B 의 NPV profile 이 *교차*(crossover, ≈12.94%). 교차점 *왼쪽*(낮은 r)에선 B 우월(NPV_B>NPV_A), *오른쪽*에선 A 우월. IRR(곡선이 x축 닿는 점)만 보면 늘 한쪽이지만, *실제 r 이 교차점보다 낮으면 다른 쪽이 정답* — 이것이 mutually exclusive 에서 IRR 이 틀리고 NPV 가 맞는 이유. crossover 는 *증분 현금흐름의 IRR* 로 찾는다.

---

## §5 Modified IRR (MIRR)

### §5.1 동기

> Multiple IRR + reinvestment assumption 문제 fix.

### §5.2 Method

1. Outflow → *initial* 로 *discount* (at finance rate)
2. Inflow → *terminal* 로 *compound* (at reinvest rate)
3. $(1 + MIRR)^T = \frac{TV}{|PV\ of\ outflow|}$

### §5.3 예

- Year 0: $-100
- Year 1-3: $50 each

At r = 10%:
$$TV = 50 \times 1.1^2 + 50 \times 1.1 + 50 = 165.5$$
$$(1 + MIRR)^3 = 1.655 \Rightarrow MIRR = 18.3\%$$

### §5.4 *MIRR 의 *남은 한계***

- Reinvestment rate *주관적*
- Mutually exclusive 의 *scale problem* 여전
- *NPV 가 여전히 우수*

---

## §6 The Profitability Index (PI)

### §6.1 정의

$$PI = \frac{PV\ of\ future\ cash\ flow}{|Initial\ investment|}$$

### §6.2 Decision rule

- PI > 1 → accept (NPV > 0 과 동일)
- PI < 1 → reject

### §6.3 *Capital rationing*

> 제한된 budget 에서 *여러 project* 선택.

**예** — Budget $100M:

| | Cost | NPV | PI |
|--|--|--|--|
| A | $20M | $30M | 2.5 |
| B | $50M | $40M | 1.8 |
| C | $30M | $50M | 2.67 |
| D | $100M | $90M | 1.9 |

**Pure NPV** — D ($90M).

**PI ranking** — C, A, B (총 $100M, NPV $120M).

→ *Capital rationing 에서 *PI 가 NPV 보다 우월** — 한정 자본 의 *효율 사용*.

### §6.4 PI 의 한계

- *Mutually exclusive* 에서 NPV 와 충돌 (scale)
- *Capital rationing 없으면* NPV 와 동일 결정

---

## §7 The Practice of Capital Budgeting

### §7.1 *실제 회사* 의 *method 사용 빈도*

(Graham + Harvey 2001 survey, US 대기업):

| Method | Always/Often |
|--|--|
| NPV | 75% |
| IRR | 76% |
| Payback | 57% |
| Discounted Payback | 30% |
| PI | 12% |
| Accounting RoR | 20% |
| Sensitivity analysis | 52% |

### §7.2 *회사 크기*

| | Large Firm | Small Firm |
|--|--|--|
| NPV/IRR | Dominant | Sometimes |
| Payback | Supplementary | Primary |
| Sensitivity | Standard | Rare |

### §7.3 *국가별 차이*

- 미국, 영국: NPV+IRR dominant
- 일본, 한국: Payback 더 흔함 (전통)
- 유럽: IRR 선호
- Emerging market: Payback 흔함 (uncertainty)

### §7.4 산업 별

| Industry | Primary method |
|--|--|
| Oil/Gas | NPV with scenario |
| Mining | NPV + Real options |
| Real estate | IRR (industry convention) |
| Tech | NPV + Scenario |
| Utility | NPV (regulated RoR) |
| Pharma | DCF + Decision tree (FDA approval) |

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | IRR 항상 NPV 와 일치 | Multiple IRR, financing, scale, timing 4 case |
| 2 | Payback 의 high cutoff | *Cutoff 의 임의성* + flaw |
| 3 | IRR 의 *yield 의미* | *Reinvestment at IRR* 가정 의 *비현실* |
| 4 | Mutual exclusive 의 IRR | *Incremental IRR* 또는 *NPV* 사용 |
| 5 | Capital rationing 에서 NPV | PI 가 *더 우월* (효율) |
| 6 | NPV = 0 무시 | Indifference 이나 *boundary 정보* |
| 7 | Multiple IRR 의 panic | MIRR 또는 NPV |
| 8 | IRR > 100% 가 *항상 좋음* | Small project 의 *scale* 무시 |

---

## §9 자가점검

1. *NPV* 의 *5 가지 우수성*?
2. *Payback* 의 *3 가지 fatal flaw*?
3. *IRR* 의 *4 가지 문제 case*?
4. *MIRR* 의 *step* 3 개?
5. *PI* 가 *NPV 보다 우월* 한 경우?
6. *실제 회사* 의 *method 사용 빈도*?

<details><summary>해답</summary>

1. Timing+magnitude, risk via r, additive, value 직접, mutual exclusivity 명확.
2. Time value 무시, post-payback 무시, 임의 cutoff.
3. Multiple IRR, no IRR, financing reverse, mutual exclusive (scale, timing).
4. (i) Outflow → PV. (ii) Inflow → TV. (iii) (1+MIRR)^T = TV / |PV outflow|.
5. *Capital rationing*.
6. NPV 76%, IRR 76%, Payback 57%, sensitivity 52%.

</details>

---

## §10 다음 학습으로

- **Ch 6** — Capital investment decisions — incremental CF, depreciation
- **Ch 7** — Risk analysis, real options
- **Ch 13** — WACC — *어떤 r*

---

## §11 한 줄 요약

> **Capital budgeting 의 *gold standard* = *NPV*. *Payback* (3 flaw), *IRR* (4 problem case), *PI* (capital rationing 에서 우월). *MIRR* 가 IRR 의 일부 fix. *실제 회사* 는 NPV + IRR + Payback 의 *3 종 병용*. *Sensitivity* 가 *위험 인식 의 보조*.**
