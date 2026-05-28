# Chapter 13: Risk, Cost of Capital, and Valuation — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 13** (책 p.416~449).
> 13장은 *WACC (Weighted Average Cost of Capital)* — Capital budgeting + Valuation 의 결정적 input.

이 장의 *지적 무게중심*:
1. **Cost of Equity** — CAPM, DDM, Build-up
2. **Cost of Debt** — YTM
3. **WACC**
4. **Capital structure weights** — book vs market
5. **Tax shield on debt**
6. **Project-specific vs Firm WACC**

---

## §1 Cost of Equity

### §1.1 3 estimation methods

**1. CAPM**:
$$R_E = R_f + \beta(R_M - R_f)$$

**2. DDM rearranged**:
$$R_E = \frac{D_1}{P_0} + g$$

**3. Build-up**:
$$R_E = R_f + ERP + Size + Industry + Firm$$

### §1.2 예 — IBM

- R_f = 4%, β = 0.9, ERP = 6%
- D_1 = $5, P_0 = $130, g = 4%

| Method | R_E |
|--|--|
| CAPM | 9.4% |
| DDM | 7.85% |
| Build-up | 9% |

→ Range 7.85-9.4%. Triangulation.

### §1.3 Best practice

- Multiple methods triangulation
- Industry benchmark 비교
- Sensitivity range

---

## §2 Cost of Debt

### §2.1 YTM

> Bond market YTM = cost of debt.

$$R_D = YTM$$

### §2.2 Why YTM not coupon

- Coupon = historical (issue 시 rate)
- YTM = current market required return
- Refinance basis

### §2.3 Multiple debt

$$R_D = \sum w_i YTM_i$$

→ Market value weighted.

### §2.4 After-tax cost

> Interest tax-deductible.

$$R_D^{after-tax} = R_D \times (1 - T_c)$$

**예**: R_D 6%, T_c 21% → 4.74%.

### §2.5 Non-traded debt

- Comparable (same rating)
- Synthetic rating (ratios → rating → spread)
- Recent borrowing rate

---

## §3 WACC

### §3.1 Formula

$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1 - T_c)$$

V = E + D (firm value).

### §3.2 예

- E = $600M, D = $400M
- R_E = 12%, R_D = 6%, T_c = 21%

$$WACC = 0.6(12) + 0.4(6)(0.79) = 7.2 + 1.896 = 9.1\%$$

### §3.3 3 인 형태 (preferred 포함)

$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1 - T_c) + \frac{P}{V} R_P$$

### §3.4 왜 weighted average

- Capital provider mix (equity + debt holders)
- 각 required return
- Firm 전체 blended cost

---

## §4 Capital Structure Weights — Book vs Market

### §4.1 Book value

- Accounting equity, debt
- Historical, outdated
- 부정확

### §4.2 Market value

- Current market price
- True economic value
- Future opportunity 반영

### §4.3 Practice — Market 사용

**왜**:
- Forward-looking
- Investor expectation 반영
- DCF target consistent

**예외**:
- Private firm — market 추정 어려움
- Distressed — abnormal market

### §4.4 예

| | Book | Market |
|--|--|--|
| Equity | $500M | $1000M |
| Debt | $300M | $320M |
| E/V | 62.5% | 75.8% |
| D/V | 37.5% | 24.2% |

---

## §5 Tax Shield on Debt

### §5.1 Origin

> Interest tax-deductible (US corporate tax).

- Pre-tax $100 interest
- Tax saving (21%): $21
- After-tax: $79

### §5.2 Annual tax shield

$$TS_t = D \times R_D \times T_c$$

### §5.3 PV of tax shield (perpetuity, MM)

$$PV(TS) = T_c \times D$$

→ Ch 16 Modigliani-Miller value component.

### §5.4 Other countries

- 대부분 interest deductible
- Thin capitalization rules (excessive debt)
- BEPS (OECD) — 30% EBITDA limit

### §5.5 Practical impact

- Debt cheaper than equity (tax saving)
- Capital structure decision (Ch 16)
- Optimal D/E tax-driven

---

## §6 Project-Specific vs Firm WACC

### §6.1 Firm WACC 한계

- Firm WACC = average of existing
- 새 project 다른 risk면 부적합

### §6.2 Project-specific Methods

**1. Pure-play firm**:
- Same business publicly traded
- 그 firm의 β 사용
- Industry analog

**2. Divisional WACC**:
- Multi-division firm
- 각 division own WACC
- 예: GE industrial vs financial

**3. Subjective approach**:
- Above-avg risk: WACC + 2-5%
- Below-avg risk: WACC - 2-5%
- Average: firm WACC

### §6.3 예

Conglomerate X:
- Firm WACC: 10%
- Tech div WACC: 13% (β=1.5)
- Retail div WACC: 8% (β=0.8)

→ Tech project에 10% 적용 → under-discount → 위험.

### §6.4 Bottom-up β (Damodaran)

1. Industry peers identify
2. 각 β_L 계산
3. Unlever: $\beta_U = \beta_L / [1 + (1-T_c) D/E]$
4. Average β_U
5. Re-lever target structure

---

## §7 International + Emerging Market

### §7.1 Country risk premium

$$R_E = R_f + \beta(R_M - R_f) + CRP$$

**Damodaran**:
- Sovereign default spread vs US Treasury
- × Relative volatility (stock/bond)
- Country-specific

### §7.2 Currency

- Local vs USD WACC
- Forward exchange rate
- Inflation differential

### §7.3 Country premia

| Country | CRP |
|--|--|
| US | 0% |
| Korea (AA-) | 0.5% |
| Brazil (BB) | 3-4% |
| Argentina (CCC) | 8-10% |
| Venezuela (D) | 15%+ |

---

## §8 WACC Practical Issues

### §8.1 β estimation

- 5 year monthly 표준
- Bayesian smoothing (Bloomberg)
- Industry β (Damodaran)
- Sensitivity

### §8.2 ERP estimation

- Historical: ~8% (US 1926-)
- Forward (implied): ~4-5% (2024)
- Survey: ~5-7%
- Country-specific

### §8.3 Capital structure target

- Current market weights
- Target (firm's plan)
- Industry average

### §8.4 Cyclical adjustments

- Recession: WACC ↑
- Boom: WACC ↓
- Crisis: extreme deviations

### §8.5 Long-term vs Short-term

- Project lifecycle long-term WACC
- R_f: 10-year Treasury (long project)
- T-bill: short only

---

## §9 WACC Applications

### §9.1 Capital budgeting

- NPV discount rate = WACC
- Accept/reject

### §9.2 Valuation (DCF)

- FCFF discount = WACC
- Firm value = Σ FCFF / WACC

### §9.3 Performance metrics

**EVA**:
$$EVA = NOPAT - WACC \times Invested\ Capital$$

- > 0: value creation
- < 0: value destruction

### §9.4 Capital structure optimization (Ch 16)

- WACC minimization → optimal D/E
- Trade-off theory (tax shield vs distress)

---

## §10 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Book weights | Market weights |
| 2 | Coupon rate as cost of debt | YTM (current) |
| 3 | Single β | Bayesian smooth, industry |
| 4 | Firm WACC for all | Project-specific |
| 5 | Tax shield 무시 | After-tax debt |
| 6 | Historical ERP only | Forward + range |
| 7 | No country risk | EM premium |
| 8 | WACC unchanging | Time-varying |
| 9 | T-bill for long project | LT Treasury |
| 10 | Pre-tax debt cost | After-tax: R_D(1-T_c) |

---

## §11 자가점검

1. *Cost of equity 3 methods*?
2. *WACC formula*?
3. *Why market weights*?
4. *After-tax cost of debt*?
5. *PV of tax shield* (perpetuity)?
6. *Project-specific WACC* methods?
7. *Bottom-up β* steps?
8. *Country risk premium*?

<details><summary>해답</summary>

1. CAPM, DDM rearranged, Build-up.
2. $WACC = (E/V)R_E + (D/V)R_D(1-T_c)$.
3. Forward-looking, investor expectation, DCF consistent.
4. $R_D \times (1 - T_c)$.
5. $T_c \times D$.
6. Pure-play, Divisional, Subjective.
7. Peers → β_L → unlever → avg → re-lever target.
8. Sovereign default spread × relative volatility (Damodaran).

</details>

---

## §12 다음 학습으로

- **Ch 16-17** — Capital structure (D/E optimization)
- **Ch 18** — APV
- **Ch 19** — Dividends

---

## §13 한 줄 요약

> **WACC = *capital budgeting + valuation* 의 *결정 input*. *Cost of equity* (CAPM, DDM, build-up) + *cost of debt* (YTM after-tax). *Market weights* (book 아님). *Tax shield* = $T_c \times D$. *Project-specific* — pure-play, divisional, subjective. *Country risk premium* — emerging market. *β estimation, ERP* — practical critical.**
