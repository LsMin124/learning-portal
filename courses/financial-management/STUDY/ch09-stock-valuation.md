# Chapter 9: Stock Valuation — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 9** (책 p.284~320).
> 9장은 *Equity valuation* — *DDM* + *P/E* + *FCF*. *Multi-stage growth* + *return decomposition*.

이 장의 *지적 무게중심*:
1. **DDM** — Dividend Discount Model
2. **Constant growth** — Gordon Growth
3. **Multi-stage growth** — 2-stage, 3-stage
4. **Return decomposition** — dividend yield + capital gain
5. **P/E approach**
6. **Common vs Preferred stock**

---

## §1 The Present Value of Common Stocks

### §1.1 *기본 framework*

> Stock price = *모든 future dividend* 의 *현재 가치*.

$$P_0 = \sum_{t=1}^{\infty} \frac{D_t}{(1+R)^t}$$

### §1.2 *왜 dividend*

- Cash flow 의 *직접 measure*
- Earnings = accounting metric
- FCF = firm level, dividend = equity level

### §1.3 *Non-dividend firm*

> Amazon, Berkshire, Tesla — no dividend.

→ Eventually 모든 firm 은 dividend or buyback — infinite horizon.

### §1.4 Return decomposition

$$R = \frac{D_1}{P_0} + g$$

- Dividend yield + capital gain yield = total return.

---

## §2 Zero Growth Dividend

### §2.1 Setup

> $D_t = D$ (constant, perpetuity).

$$P_0 = \frac{D}{R}$$

### §2.2 Preferred stock model

- Fixed dividend, perpetual
- No voting
- Priority over common

**예** — Preferred $5/year, R = 8%:
$$P = \frac{5}{0.08} = \$62.50$$

---

## §3 Constant Growth (Gordon Growth Model)

### §3.1 Setup

> $D_t = D_0 (1+g)^t$.

$$P_0 = \frac{D_1}{R - g}\ (R > g)$$

### §3.2 *왜 R > g* 필요

- g ≥ R → infinite value (수학적 발산)
- 영원히 R 보다 빠른 성장 = 전체 경제 추월 불가능

### §3.3 예

$D_1 = $2, g = 5%, R = 12%:
$$P_0 = \frac{2}{0.07} = \$28.57$$

### §3.4 Year 1 price

$$P_1 = \frac{D_2}{R - g} = P_0(1+g) = \$30$$

→ Price grows at g.

### §3.5 Return decomposition

- Dividend yield: 2/28.57 = 7%
- Capital gain: g = 5%
- **Total R = 12%** ✓

### §3.6 Sustainable growth

$$g = ROE \times b$$

- b = retention ratio (1 − payout)
- ROE = Return on Equity

**Derivation**:
- Reinvestment = NI × b
- New equity = E_0 + NI × b
- Growth in equity = ROE × b

### §3.7 예

ROE 15%, b = 60%:
$$g = 0.15 \times 0.60 = 9\%$$

→ Sustainable growth 9% (외부 자금 없이).

### §3.8 Gordon Growth 의 한계

1. Single g 의 비현실
2. R, g, D_1 의 small change → 큰 가격 차이
3. Non-dividend firm 의 비적용
4. Negative growth firm 의 문제

→ Multi-stage 가 현실적.

---

## §4 Multi-Stage Growth

### §4.1 2-Stage

$$P_0 = \sum_{t=1}^{T} \frac{D_t}{(1+R)^t} + \frac{D_{T+1}/(R-g_2)}{(1+R)^T}$$

### §4.2 예

$D_0 = $2, g_1 = 20% (5 years), g_2 = 4%, R = 12%.

**Stage 1**:
- D_1 = 2.40, D_2 = 2.88, D_3 = 3.46, D_4 = 4.15, D_5 = 4.98

**Stage 2 (Gordon)**:
- D_6 = 5.18, P_5 = 5.18/0.08 = $64.75

**Total**:
$$P_0 = \sum \frac{D_t}{1.12^t} + \frac{64.75}{1.12^5}$$
$$= 12.37 + 36.74 = \$49.11$$

→ Terminal value PV ($36.74) = 전체 의 75%.

### §4.3 3-Stage Growth

> High → Transition → Stable.

**예** — Tech firm:
- Stage 1 (1-5): g = 30%
- Stage 2 (6-10): g declining 30% → 5%
- Stage 3 (11+): g = 5% perpetuity

### §4.4 Damodaran's 6-stage (complex firms)

1. High growth
2. Transition
3. Plateau
4. Mature
5. Decline
6. Terminal

---

## §5 Return Estimation 4 method

### §5.1 *CAPM*:
$$R = R_f + \beta(R_M - R_f)$$

### §5.2 *DDM rearranged*:
$$R = \frac{D_1}{P_0} + g$$

### §5.3 *Historical*: Stock historical return

### §5.4 *Build-up*:
$$R = R_f + ERP + Size + Industry + Firm$$

### §5.5 예 — IBM

| Method | R |
|--|--|
| CAPM | 9.4% |
| DDM | 7.8% |
| Historical | 10% |
| Build-up | 9% |

→ Range 7.8-10%. Triangulation importance.

### §5.6 Implied growth (reverse DCF)

$$g_{implied} = R - D_1/P_0$$

→ 시장 implied g — reality check.

---

## §6 P/E Ratio approach

### §6.1 정의

$$P/E = \frac{Price}{EPS}$$

### §6.2 Valuation

$$P = EPS \times Industry\ P/E$$

### §6.3 *Gordon Growth 연결*

$$P/E = \frac{1-b}{R-g}$$

→ P/E ↑ when:
- Payout ↑ (1-b)
- R ↓ (lower risk)
- g ↑ (higher growth)

### §6.4 Forward vs Trailing P/E

**S&P 500 long-term avg**:
- Trailing: ~15-18
- Forward: ~13-16
- Schiller (CAPE): ~17

### §6.5 PEG Ratio

$$PEG = \frac{P/E}{g}$$

- < 1: undervalued
- = 1: fair
- > 1: overvalued

**Peter Lynch**: "Fairly valued = P/E equal to growth rate."

### §6.6 P/E 한계

1. Negative earnings 무의미
2. Cyclical earnings swing
3. Accounting differences
4. Growth phase 의 high P/E justify
5. Quality 무시

→ EV/EBITDA, P/B, P/S 와 complementary.

---

## §7 Free Cash Flow Approach

### §7.1 FCFE vs FCFF

**FCFE** (Equity):
$$FCFE = NI + D\&A - Capex - \Delta NWC - Debt\ repay + Debt\ issue$$

**FCFF** (Firm):
$$FCFF = EBIT(1-T_c) + D\&A - Capex - \Delta NWC$$

### §7.2 Valuation

**Equity**:
$$Equity = \sum \frac{FCFE_t}{(1+R_e)^t}$$

**Firm**:
$$Firm = \sum \frac{FCFF_t}{(1+WACC)^t}$$
$$Equity = Firm - Debt$$

### §7.3 Tesla 예

- FCFF ~$5B, g = 10%, WACC = 10%
- → g = WACC, infinite (Gordon failure)
- Multi-stage required:
  - Stage 1 (5yr): g = 20%
  - Stage 2: g = 5%
  - → Firm $200-500B (market $700B+ premium 의문)

---

## §8 Common vs Preferred Stock

### §8.1 비교

| | Common | Preferred |
|--|--|--|
| Dividend | Variable | Fixed |
| Priority | Lowest | Above common |
| Voting | Yes | No |
| Convertible | No 보통 | Sometimes |
| Tax (corp recipient) | 50% exclusion | 50% exclusion |
| Volatility | High | Low |

### §8.2 Preferred valuation

$$P_{pref} = \frac{D_{pref}}{R_{pref}}$$

### §8.3 Cumulative vs Non-cumulative

- Cumulative: missed dividend accumulates
- Non-cumulative: missed = gone

### §8.4 Convertible preferred

> Conversion option into common.

- Dividend + upside potential
- VC startup 의 typical

---

## §9 Behavioral / Market Anomalies

### §9.1 Value vs Growth

- Value: low P/E, P/B
- Growth: high P/E, low/no dividend

**Fama-French (1992)**:
- Value premium: 4-5%/year historical
- 2000s 약화

### §9.2 Momentum

- Past 6-12 month winner continued
- Jegadeesh-Titman (1993)

### §9.3 Quality factor

- High ROE + low debt + stability
- Defensive in down market

### §9.4 Modern factor investing

- Fama-French 5 factor
- Carhart 4 factor
- AQR multi-factor

---

## §10 Real-world 예

### §10.1 Apple 2024

- EPS ~$6, Forward P/E ~28, Price ~$170
- Dividend $1 (~0.6% yield)
- ROE 150%+ (buyback)

**DDM challenge**:
- Dividend 작음 — DDM 부적합
- Buyback yield 4% — total payout 적용
- $P = (Dividend + Buyback) / (R - g)$

### §10.2 Berkshire Hathaway

- No dividend (Buffett policy)
- Buyback 가끔
- Book value growth
- Sum-of-parts + look-through earnings

### §10.3 Amazon (early 2000s)

- No dividend, negative NI (until ~2009)
- FCF positive but reinvested
- Valuation by growth + future profit

---

## §11 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Non-dividend firm = 0 value | Future eventual payout |
| 2 | Gordon g ≥ R | Multi-stage |
| 3 | Single P/E comparison | Industry + size + cycle |
| 4 | Trailing P/E only | Forward + cyclical |
| 5 | DDM 만 의존 | Triangulation |
| 6 | Buyback 무시 | Total payout = D + B |
| 7 | Negative earnings P/E | EV/EBITDA, P/B, P/S |
| 8 | Sustainable growth fix | ROE × b cycle change |
| 9 | Terminal value 비중 무시 | Sensitivity critical |
| 10 | Real options 무시 | Growth firm option value |

---

## §12 자가점검

1. *DDM framework*?
2. *Gordon Growth* 공식 + 조건?
3. *Sustainable growth* derivation?
4. *2-stage terminal value*?
5. *Return estimation* 4 method?
6. *P/E ↔ Gordon Growth* 연결?
7. *FCFE vs FCFF*?
8. *Common vs Preferred*?

<details><summary>해답</summary>

1. $P_0 = \sum D_t / (1+R)^t$.
2. $P_0 = D_1/(R-g)$, R > g.
3. Reinvestment = NI×b, equity growth = ROE×b.
4. $TV = D_{T+1}/(R-g_2)$, PV = TV/(1+R)^T.
5. CAPM, DDM rearranged, Historical, Build-up.
6. $P/E = (1-b)/(R-g)$.
7. FCFE (equity-level), FCFF (firm-level).
8. Common: variable, voting, low priority. Preferred: fixed, no voting, above.

</details>

---

## §13 다음 학습으로

- **Ch 10-12** — Risk and return — CAPM, APT
- **Ch 13** — WACC
- **Ch 16-17** — Capital structure
- **Ch 19** — Dividends

---

## §14 한 줄 요약

> **Stock valuation = PV of dividend (DDM). Zero growth = perpetuity, Constant g = Gordon, Multi-stage = 2-3 stage. Return = dividend yield + capital gain. *Sustainable growth* = ROE × b. *P/E approach* — P/E = (1-b)/(R-g). *FCFE* (equity) vs *FCFF* (firm). *Triangulation* (DDM, FCF, P/E, comparable) modern best practice.**
