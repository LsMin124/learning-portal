# Chapter 18: Valuation and Capital Budgeting for the Levered Firm — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 18** (책 p.569~590).
> 18장은 *levered firm* 의 valuation 3 방법 — **APV**, **FTE**, **WACC**. Ch 16-17 의 capital structure 를 *valuation 에 적용*.

이 장의 *지적 무게중심*:
1. **APV (Adjusted Present Value)** — unlevered value + financing side effects
2. **FTE (Flow to Equity)** — equity cash flow at R_E
3. **WACC method** — unlevered cash flow at after-tax WACC
4. **3 방법의 *equivalence* + 선택 기준**
5. **Beta levering/unlevering** in practice
6. **APV for LBO / project financing**

---

## §0 도입 — 부채가 끼면 할인율이 흔들린다

Ch 16-17 은 자본구조가 기업가치를 *바꾼다*(세금방패만큼)고 했다. 그렇다면 부채로 일부를 조달하는 프로젝트의 NPV 는 어떻게 구하나? 핵심 골칫거리는 **할인율**이다. 전액 자기자본이면 $R_0$ 로 할인하면 끝이지만, 부채가 끼면 (i) 이자의 세금방패가 가치를 더하고 (ii) 자기자본의 위험(따라서 $R_E$)이 leverage 에 따라 커진다.

세 방법은 *이 financing 효과를 어디서 처리하느냐* 의 차이일 뿐이다:
- **APV** — 가치에서 *분리*: 전액자기자본 가치 $V_U$ 를 따로 구하고, 세금방패를 *별도 항목*으로 더한다.
- **FTE** — *현금흐름*에서 처리: 이자 차감 후 주주 몫(LCF)을 levered 위험률 $R_E$ 로 할인.
- **WACC** — *할인율*에서 처리: 세금방패를 $R_D(1-T_c)$ 항에 녹여 UCF 를 할인.

> **직관**: 같은 세금방패를 세 가지 회계처리로 나눠 본 것이므로, 일관된 가정 하에선 *반드시 같은 답*이 나온다(이 장 예제는 모두 $6.05M로 수렴). "무엇을 이미 어디에 반영했는가"만 헷갈리지 않으면 된다 — 그래서 §10 함정의 절반이 *이중 계산*이다.

---

## §1 세 가지 Valuation 방법 — 개요

> 같은 levered project 를 *3 가지 다른 경로*로 평가 — *이론적으로 동일한 답*.

| 방법 | Cash flow | Discount rate |
|--|--|--|
| **APV** | Unlevered FCF + tax shield 별도 | R_0 (unlevered) + R_D (shield) |
| **FTE** | *Equity* cash flow (after interest) | R_E (levered equity) |
| **WACC** | Unlevered FCF (UCF) | WACC (after-tax) |

→ 셋 다 *동일한 NPV* 산출 (일관 가정 하).

---

## §2 The Adjusted Present Value (APV) Approach

### §2.1 핵심 식

$$APV = NPV(\text{all-equity}) + NPV(\text{financing side effects})$$

$$APV = V_U + \sum \text{financing effects}$$

### §2.2 Financing side effects 4 가지

1. **Tax shield of debt** (가장 흔함, +)
2. **Cost of issuing new securities** (flotation cost, −)
3. **Cost of financial distress** (−)
4. **Subsidies to debt financing** (정부 보조 저리 대출, +)

### §2.3 기본 형태 (tax shield 만)

$$APV = \underbrace{-Cost + \sum \frac{UCF_t}{(1+R_0)^t}}_{\text{NPV unlevered}} + \underbrace{\sum \frac{T_c \cdot R_D \cdot D_t}{(1+R_D)^t}}_{\text{PV tax shield}}$$

- $UCF$ = unlevered cash flow = EBIT(1−T_c) + D&A − Capex − ΔNWC
- $R_0$ = unlevered cost of equity
- $T_c R_D D$ = annual tax shield

### §2.4 영구 debt 의 tax shield

$$PV(\text{Tax Shield}) = T_c \times D$$

(Ch 16 MM with tax 와 동일)

### §2.5 예제

Project: 초기 $-10M, UCF $1.8M/year 영구, R_0 = 12%, 영구 debt $5M, R_D = 8%, T_c = 21%.

**NPV (all-equity)**:
$$-10 + \frac{1.8}{0.12} = -10 + 15 = \$5M$$

**PV(Tax Shield)**:
$$T_c \times D = 0.21 \times 5 = \$1.05M$$

**APV**:
$$5 + 1.05 = \$6.05M$$

→ Financing (debt tax shield) 이 *$1.05M 가치 추가*.

---

## §3 The Flow to Equity (FTE) Approach

### §3.1 핵심

> *Levered cash flow* (equity holders 에게 가는 cash) 를 *R_E* 로 discount.

$$FTE: NPV = -(\text{Cost} - \text{Debt raised}) + \sum \frac{LCF_t}{(1+R_E)^t}$$

- $LCF$ = levered cash flow = UCF − after-tax interest
  $$LCF = (EBIT - R_D D)(1 - T_c) + D\&A - Capex - \Delta NWC$$
- 초기 투자에서 *debt 로 조달한 부분 차감* (equity 만 부담)

### §3.2 3 단계

1. **LCF 계산**: UCF − interest×(1−T_c)
2. **R_E 계산**: MM Prop II with tax (또는 CAPM levered β)
3. **Discount**: equity 초기 투자 대비 NPV

### §3.3 예제 (위와 동일 project)

- 초기 $-10M 중 debt $5M → equity 투자 $5M
- Annual interest: $5M × 8% = $0.4M
- LCF = $1.8M − $0.4M(1−0.21) = $1.8M − $0.316M = $1.484M
- E = V_L − D = $16.05M − $5M = $11.05M (V_L = V_U + tax shield = 15 + 1.05)

$$R_E = 0.12 + (0.12-0.08)(0.79)\frac{5}{11.05} = 0.12 + 0.0143 = 13.43\%$$

$$NPV_{FTE} = -5 + \frac{1.484}{0.1343} = -5 + 11.05 = \$6.05M$$

→ APV 와 *동일* ✓

---

## §4 The WACC Method

### §4.1 핵심

> *Unlevered cash flow (UCF)* 를 *WACC* 로 discount. Tax shield 는 *WACC 에 이미 반영*.

$$NPV_{WACC} = -Cost + \sum \frac{UCF_t}{(1+WACC)^t}$$

$$WACC = \frac{E}{V}R_E + \frac{D}{V}R_D(1-T_c)$$

### §4.2 예제 (동일)

- WACC = (11.05/16.05)(13.43%) + (5/16.05)(8%)(0.79)
- = 0.6885 × 13.43% + 0.3115 × 6.32%
- = 9.246% + 1.969% = 11.21%

$$NPV_{WACC} = -10 + \frac{1.8}{0.1121} = -10 + 16.06 = \$6.06M$$

→ APV, FTE 와 *동일* (rounding) ✓

### §4.3 WACC 방법의 *순환 문제*

- WACC 계산에 *E, D market value* 필요
- 그러나 V 가 *valuation 의 결과*
- → *iteration* 또는 *target D/V ratio* 가정 필요

---

## §5 세 방법의 비교 + 선택 기준

### §5.1 Equivalence 조건

> 세 방법은 *target debt-to-value ratio constant* 가정 하에서 *동일*.

WACC·FTE 는 $R_E$·WACC 가 *기간 내내 일정* 하다고 본다 — 이는 D/V 가 일정해야 성립한다(부채가 가치에 비례해 따라 움직인다는 가정). APV 는 그런 가정이 필요 없다: 각 연도의 부채 잔액에서 나오는 세금방패를 *직접* 더하므로, **부채 *금액*이 시간에 따라 변하는** 상황(LBO 의 paydown)에서도 정확하다. 그래서 §5.2 의 선택 기준이 갈린다 — *ratio 일정*이면 WACC, *level 변동*이면 APV.

### §5.2 언제 어느 방법

| 상황 | 추천 방법 | 이유 |
|--|--|--|
| **Target D/V constant** | WACC 또는 FTE | WACC 가장 간단 |
| **Debt level 이 *고정 금액*** (LBO) | **APV** | Tax shield 명확히 별도 |
| **Debt 이 시간에 따라 변화** | **APV** | 각 연도 tax shield 명시 |
| **Project 가 firm 과 다른 risk** | APV 또는 FTE | Pure-play β |
| **간단한 going-concern** | WACC | 실무 표준 |

### §5.3 Rule of thumb

- **WACC + FTE**: debt *비율(ratio)* 이 일정할 때
- **APV**: debt *수준(level)* 이 일정하거나 변동 — *LBO, project finance*

### §5.4 실무 선호

- *대부분 기업 valuation*: **WACC** (간단, target ratio)
- *LBO, leveraged recap*: **APV** (debt paydown schedule)
- *Investment banking*: 상황별 혼용

---

## §6 Beta Levering / Unlevering (실무 핵심)

### §6.1 Hamada equation (Ch 16 recap)

$$\beta_L = \beta_U[1 + (1-T_c)\frac{D}{E}]$$

$$\beta_U = \frac{\beta_L}{1 + (1-T_c)\frac{D}{E}}$$

### §6.2 Pure-play 방법 절차

1. *비교 가능 상장사(peers)* 식별
2. 각 peer 의 *β_L* (관측)
3. 각 peer 를 *unlever* → β_U
4. *평균 β_U* (business risk)
5. 우리 회사 *target D/E 로 re-lever* → β_L
6. *CAPM* 으로 R_E

### §6.3 예제

Peers β_U 평균 = 1.0. 우리 회사 target D/E = 0.5, T_c = 21%.

$$\beta_L = 1.0 \times [1 + 0.79 \times 0.5] = 1.395$$

R_f = 4%, ERP = 6%:
$$R_E = 4\% + 1.395 \times 6\% = 12.37\%$$

### §6.4 왜 unlever 가 필요한가

- Peer 들의 *leverage 가 제각각*
- *Business risk (β_U)* 만 비교 가능
- 우리 회사 *자체 capital structure* 로 re-lever

---

## §7 APV for LBO (Leveraged Buyout)

### §7.1 LBO 의 특징

- *높은 debt* (보통 60-90%)
- *Debt paydown* 매년 (FCF 로 상환)
- *Debt level 이 시간에 따라 감소* → **APV 가 적합**

### §7.2 APV 구조

$$APV_{LBO} = V_U + \sum_{t=1}^{T} \frac{T_c \cdot R_D \cdot D_t}{(1+R_D)^t} + \frac{TV}{(1+R_0)^T}$$

- $D_t$ = 각 연도 *감소하는* debt balance
- Tax shield 가 *매년 다름* (debt 감소)
- Terminal value (exit) 별도

### §7.3 LBO 의 value creation 3 source

1. **Leverage / Tax shield** — debt tax 절감
2. **Operational improvement** — margin, efficiency
3. **Multiple expansion** — entry vs exit EV/EBITDA

### §7.4 유명 LBO

| Deal | 연도 | 규모 |
|--|--|--|
| RJR Nabisco | 1989 | $25B (당시 최대, "Barbarians at the Gate") |
| TXU Energy | 2007 | $45B (역대 최대, 2014 파산) |
| Hilton (Blackstone) | 2007 | $26B (위기 생존, 큰 수익) |
| Dell | 2013 | $24B (Michael Dell + Silver Lake) |
| Twitter (Musk) | 2022 | $44B (high leverage, 논란) |

---

## §8 Flotation Costs + Subsidized Financing

### §8.1 Flotation cost in APV

$$APV = V_U + PV(TS) - \text{Flotation Cost}$$

- *Issuance cost* (IPO 6-7%, bond 1-2%, Ch 15)
- *즉시 차감* 또는 *amortize over debt life* (세금 효과)

### §8.2 Subsidized loan

> 정부/지자체의 *시장 이하 금리* 대출.

$$NPV(\text{Subsidy}) = \text{Loan} - \sum \frac{\text{After-tax payments}}{(1+R_D^{market})^t}$$

- 예: 산업단지 유치 저리 대출, 그린에너지 보조
- *Market rate 대비 절감액의 PV*

### §8.3 예제

$10M 대출, subsidized 3% vs market 8%, 5년 만기, T_c = 21%.
- *각 연도 이자 절감* × (1−T_c) 의 PV = subsidy value
- APV 에 *+* 항목으로 추가

---

## §9 실무 적용 정리

### §9.1 Investment banking DCF

- 보통 **WACC method** (target capital structure)
- *Terminal value* (Gordon 또는 exit multiple)
- *Sensitivity* (WACC ±, growth ±)

### §9.2 Private equity / LBO

- **APV** 또는 *LBO model* (debt schedule)
- *IRR target* (보통 20-25%)
- *Exit assumption* critical

### §9.3 Corporate project

- *Same risk as firm*: WACC
- *Different risk*: pure-play β → project WACC 또는 APV

### §9.4 Real estate

- *고정 mortgage* → APV 자연스러움
- *Cap rate* 와 연결

---

## §10 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 세 방법 답이 다르다 | 일관 가정 하 *동일* |
| 2 | WACC 에 tax shield 또 더함 | WACC 에 *이미 반영*, 이중 계산 금지 |
| 3 | FTE 에서 debt 조달분 미차감 | 초기 투자 = *equity 부담분만* |
| 4 | APV 에서 UCF 대신 LCF 사용 | APV/WACC 는 *UCF*, FTE 만 *LCF* |
| 5 | LBO 에 WACC 사용 | Debt 변동 → *APV* 적합 |
| 6 | β unlever 없이 peer β 직접 사용 | Leverage 제각각 → unlever 필수 |
| 7 | Tax shield discount rate 혼동 | 보통 R_D (debt risk), 일부 R_0 |
| 8 | Flotation cost 무시 | APV 에서 *차감* |
| 9 | 순환 문제 무시 (WACC) | Target ratio 또는 iteration |
| 10 | Subsidy 무시 | APV *+* 항목 |

---

## §11 자가점검

1. *APV* 의 기본 식?
2. *FTE* 의 LCF 정의 + discount rate?
3. *WACC method* 가 tax shield 를 어떻게 반영?
4. 세 방법이 *동일* 한 조건?
5. *LBO* 에 APV 가 적합한 이유?
6. *Hamada equation* (unlever/re-lever)?
7. *Pure-play* 절차?

<details><summary>해답</summary>

1. $APV = V_U + \sum$ financing effects (주로 tax shield $T_c D$).
2. LCF = UCF − after-tax interest = $(EBIT−R_D D)(1−T_c)$+D&A−Capex−ΔNWC. Discount at R_E. 초기투자는 equity 부담분만.
3. WACC 의 after-tax R_D 항 $R_D(1−T_c)$ 에 *tax shield 이미 반영*. UCF 사용, 별도 tax shield 더하지 않음.
4. *Target D/V ratio constant* 가정 하 동일.
5. LBO 는 *debt level 이 매년 감소* → tax shield 가 매년 다름 → APV 가 각 연도 명시.
6. $\beta_L = \beta_U[1+(1−T_c)D/E]$, $\beta_U = \beta_L / [1+(1−T_c)D/E]$.
7. Peers 식별 → β_L 관측 → unlever → 평균 β_U → target D/E 로 re-lever → CAPM.

</details>

---

## §12 다음 학습으로

- **Ch 19** — Dividends and payouts
- **Ch 20** — Raising capital (IPO)
- **Ch 29** — M&A (APV/LBO 응용)

---

## §13 한 줄 요약

> **Levered firm valuation 3 방법 — *APV* ($V_U$ + financing side effects, 주로 tax shield $T_c D$), *FTE* (LCF at R_E, 초기투자는 equity분만), *WACC* (UCF at after-tax WACC). 셋 다 *target D/V constant* 하 *동일*. *Debt level 고정/변동* (LBO) 이면 **APV**, *ratio 일정* 이면 **WACC/FTE**. *Hamada* 로 β unlever/re-lever, *pure-play* 절차. *Flotation cost*(−), *subsidy*(+) 도 APV 항목.**
