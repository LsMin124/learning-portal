# Chapter 12: APT and Empirical Models — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 12** (책 p.391~415).
> 12장은 *Arbitrage Pricing Theory* + *empirical multi-factor models*. CAPM 의 single-factor 한계 보완.

이 장의 *지적 무게중심*:
1. **Factor Models**
2. **APT** — no-arbitrage derivation
3. **Multi-factor** — Fama-French, Carhart
4. **APT vs CAPM**
5. **Macroeconomic factors** — Chen-Roll-Ross
6. **Risk decomposition**

---

## §1 Factor Models

### §1.1 Single-factor

$$R_i = \alpha_i + \beta_i F + \epsilon_i$$

### §1.2 Multi-factor

$$R_i = \alpha_i + \beta_{i1} F_1 + \beta_{i2} F_2 + ... + \beta_{iK} F_K + \epsilon_i$$

### §1.3 Factor types

| Type | 예 |
|--|--|
| Macroeconomic | GDP, inflation, rate, oil |
| Fundamental | Size, value, profitability |
| Statistical | PCA derived |

### §1.4 Why multi-factor

- Single factor (CAPM) insufficient
- Multiple risk sources
- Better empirical fit
- Anomaly explanation

---

## §2 APT

### §2.1 Stephen Ross (1976)

> APT = *no-arbitrage* equilibrium pricing.

### §2.2 Core insight

> Diversified portfolio expected return = factor exposure weighted sum.

$$E[R_i] = R_f + \beta_{i1} \lambda_1 + ... + \beta_{iK} \lambda_K$$

- $\lambda_k$ = risk premium for factor k

### §2.3 APT vs CAPM

| | CAPM | APT |
|--|--|--|
| Factors | Market only | Multiple |
| Foundation | Equilibrium | No-arbitrage |
| Assumptions | Strict | Weak |
| Factor specification | Market portfolio | Not specified |
| Test | Market observable | Factor choice arbitrary |

### §2.4 No-arbitrage logic

If two portfolios:
- Same factor exposures
- Different expected returns
→ Arbitrage — buy higher, sell lower
→ Equilibrium — same exposure same return

### §2.5 APT flexibility

- Factor choice — researcher decides
- Robust to variations
- Strong empirical support

### §2.6 APT weakness

- Factor specification — no theory
- Risk premium estimation — empirical fit
- Endless models possibility

---

## §3 Macroeconomic Factor Models

### §3.1 Chen-Roll-Ross (1986)

**5 factors**:
1. Industrial production growth
2. Inflation (expected + unexpected)
3. Term spread (long - short)
4. Default spread (junk - Treasury)
5. Oil price

### §3.2 Intuition

- GDP, IP — economic activity
- Inflation — purchasing power
- Rate — discount rate, opportunity cost
- Default spread — recession indicator
- Oil — input cost, geopolitical

### §3.3 Practical use

- Hedge fund — macro long/short
- Asset allocation — economic regime
- Risk management — VaR by factor

---

## §4 Fama-French Models

### §4.1 3 Factor (1992)

$$R_i - R_f = \alpha + \beta_M(R_M-R_f) + \beta_{SMB}SMB + \beta_{HML}HML + \epsilon$$

- Market (R_M - R_f)
- SMB = Small Minus Big (size)
- HML = High Minus Low B/M (value)

### §4.2 Motivation

- Banz (1981): small-cap outperforms
- Stattman (1980): B/M predicts return

→ CAPM anomalies → factor 표현.

### §4.3 SMB + HML construction

**SMB**: Long small, short big.
**HML**: Long high B/M (value), short low (growth).

### §4.4 Empirical findings

- Market β significant
- SMB positive
- HML positive
- 3-factor explains ~90% of variation

### §4.5 Carhart 4 Factor (1997)

> + WML (Winners Minus Losers) = Momentum.

Jegadeesh-Titman (1993): Past 12-month winners outperform.

→ Behavioral or risk? — debate.

### §4.6 Fama-French 5 Factor (2015)

> + RMW (profitability) + CMA (investment).

- RMW = Robust Minus Weak
- CMA = Conservative Minus Aggressive

→ q-theory + DDM 기반.

### §4.7 Modern factors (2020s+)

- Quality (Asness-Frazzini-Pedersen)
- Low volatility / Low beta
- Investment intensity
- Earnings quality
- ESG factor

---

## §5 Risk Premium Estimates

### §5.1 Historical (US 1926-2024)

| Factor | Annual Premium |
|--|--|
| Market | ~8% |
| SMB (size) | ~3% |
| HML (value) | ~4% |
| WML (momentum) | ~8% |
| RMW (profitability) | ~3% |
| CMA (investment) | ~3% |

### §5.2 Time-varying

- Value: 1926-2000 strong, 2000-2020 weak, 2021- revival
- Size: weakened since 1980s
- Momentum: still positive but volatile

### §5.3 International

- Most factors robust across countries
- Stronger in emerging
- Weaker in others

---

## §6 Statistical Factor Models

### §6.1 PCA

> Statistical extraction from return correlations.

- Factor 1: market (largest eigenvalue)
- Factor 2: size or sector
- Factor 3+: smaller

### §6.2 비교

| | Macro | Fundamental | Statistical |
|--|--|--|--|
| Source | Theory | Firm char | Data |
| Interpretation | Clear | Clear | Often unclear |
| Estimation | Easy | Standard | Complex |
| Robustness | High | High | Sample-dep |

---

## §7 Behavioral vs Rational Factor Interpretation

### §7.1 Rational view

- Factors = priced risks
- Risk premium = compensation
- Value, size, momentum = macro risk exposure

### §7.2 Behavioral view

- Factors = mispricing
- Limits to arbitrage
- Behavioral biases (over/under-reaction)
- Lakonishok-Shleifer-Vishny (1994): value = mispricing

### §7.3 Empirical debate

- Risk: factor return varies with conditions
- Behavioral: non-economic timing alpha
- Hybrid: both contribute

---

## §8 Implementation — Factor Investing

### §8.1 Active managers

- Stock selection by factor exposure
- Quant funds (AQR, DFA, Two Sigma)
- Hedge fund multi-factor long/short

### §8.2 Passive / Smart Beta

- Factor ETFs (single or combined)
- Value: IWN, IVE, DFLVX
- Size: IWM, IJR
- Momentum: MTUM, PMOM
- Quality: QUAL
- Low vol: USMV, SPLV

### §8.3 Multi-factor

- AQR — Style premia
- BlackRock — Factor ETFs combined
- Vanguard — Multi-factor fund (2018)
- DFA — Multi-factor mutual fund

### §8.4 Performance reality

- Factors cyclical
- 2010-2020: value underperform — factor death debate
- 2021-2023: value strong revival
- Single factor: high tracking error
- Multi-factor: smoother

---

## §9 Modern Challenges

### §9.1 Factor Zoo (Cochrane 2011)

- Hundreds of factors proposed
- Multiple testing bias
- Data mining
- Out-of-sample failure

### §9.2 Replication crisis

- Many factors fail OOS
- Hou-Xue-Zhang (2020): 65% fail replication
- Harvey-Liu-Zhu (2016): only 5-10 robust

### §9.3 Machine Learning

- Kelly-Pruitt-Su (2020): ML factor models
- Gu-Kelly-Xiu (2020): 30 ML factors
- OOS improvement
- Interpretation challenge

### §9.4 Modern best practice

1. Theoretically motivated
2. OOS test
3. International replication
4. Multiple testing correction
5. Economic significance
6. Implementable (transaction cost, capacity)

---

## §10 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | More factors = better | Multiple testing, robustness |
| 2 | Historical = future | Time-varying, cyclical |
| 3 | Factor = priced risk | Behavioral 가능성도 |
| 4 | Single factor sufficient | Multi-factor empirical |
| 5 | Factor stable | Time-varying premium |
| 6 | APT = CAPM | Different foundation |
| 7 | Easy factor ID | Factor zoo 함정 |
| 8 | Factor 항상 positive | Sample-period dependent |

---

## §11 자가점검

1. *Single vs Multi-factor model*?
2. *APT vs CAPM*?
3. *Fama-French 5 factor*?
4. *Chen-Roll-Ross macro factors*?
5. *Value premium rational vs behavioral*?
6. *Factor Zoo + Replication crisis*?

<details><summary>해답</summary>

1. Single (CAPM) = market only. Multi = multiple systematic factors.
2. APT = no-arbitrage, factors flexible. CAPM = equilibrium, market portfolio. APT 더 flexible.
3. Market + SMB + HML + RMW + CMA (Carhart's WML optional).
4. IP growth, inflation, term spread, default spread, oil.
5. Rational = risk premium. Behavioral = mispricing (glamour vs neglected).
6. Factor Zoo (Cochrane) = hundreds proposed. Replication crisis — 65% fail OOS.

</details>

---

## §12 다음 학습으로

- **Ch 13** — WACC — *실제 cost of capital*
- **Ch 16-17** — Capital structure

---

## §13 한 줄 요약

> **APT (Ross 1976) = *no-arbitrage multi-factor* pricing — CAPM single-factor extension. *Fama-French 3 / Carhart 4 / FF 5* models. *Macroeconomic* (Chen-Roll-Ross) + *fundamental* (size, value) + *statistical* (PCA) factors. *Risk vs behavioral* interpretation. *Factor Zoo + replication crisis* modern challenges. *Multi-factor portfolio + factor ETF* industry adoption.**
