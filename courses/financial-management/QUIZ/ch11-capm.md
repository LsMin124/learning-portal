# Ch 11 Return and Risk — CAPM — 퀴즈

> 10 문항 (개념 2 / 계산 5 / 디버그 2 / 면접 1).

### Q1. *Systematic vs Unsystematic risk*?

<details><summary>답</summary>

| | 의미 | 예 | Diversification |
|--|--|--|--|
| Systematic | Market-wide | GDP, rate, war | 불가 |
| Unsystematic | Firm-specific | CEO 사임, recall | 가능 |

**Total = Systematic + Unsystematic**.

**Diversification limit**:
- N ~30: 대부분 unsystematic 사라짐
- N → ∞: only systematic remains

**Implications**:
- Unsystematic = non-priced
- Systematic = priced (Beta)
- *Diversifiable risk* 의 *compensation 받을 자격 없음*

</details>

### Q2. *CAPM equation + assumptions*?

<details><summary>답</summary>

$$E[R_i] = R_f + \beta_i (E[R_M] - R_f)$$

**7 assumptions**:
1. Risk-averse + mean-variance optimizer
2. Homogeneous expectations
3. Risk-free borrow/lend
4. No transaction cost, tax
5. Single-period horizon
6. Frictionless markets
7. All hold market portfolio

**Empirical reality**:
- 대부분 가정 위반
- 그러나 first-order approximation 유용
- *Industry standard* DCF discount

**Critiques**:
- Roll (1977): market portfolio non-observable
- Fama-French (1992): size, value
- Behavioral: biases not captured

</details>

### Q3. 계산 — Portfolio return + risk

- A: E[R]=12%, σ=20%
- B: E[R]=8%, σ=10%
- ρ_AB=0.3, 60% A + 40% B

<details><summary>답</summary>

**E[R_P]**: 0.6(12) + 0.4(8) = **10.4%**

**Variance**:
$$\sigma_P^2 = (0.6)^2(0.2)^2 + (0.4)^2(0.1)^2 + 2(0.6)(0.4)(0.3)(0.2)(0.1)$$
$$= 0.0144 + 0.0016 + 0.00288 = 0.01888$$

**σ_P** = √0.01888 = **13.74%**

**Diversification benefit**:
- Weighted avg σ: 0.6(20) + 0.4(10) = 16%
- σ_P (13.74%) < 16%

**Sensitivity to ρ**:
- ρ=1: 16% (no benefit)
- ρ=0: 12.65%
- ρ=-1: 8% (large benefit)

</details>

### Q4. 계산 — Beta

| State | P | R_stock | R_market |
|--|--|--|--|
| Boom | 30% | 30% | 20% |
| Normal | 50% | 12% | 10% |
| Recession | 20% | -15% | -10% |

β?

<details><summary>답</summary>

**E[R]**:
- E[R_stock] = 12%
- E[R_M] = 9%

**Covariance**:

| State | (R_s-12)(R_M-9) | × P |
|--|--|--|
| Boom | 18×11=198 | 59.4 |
| Normal | 0×1=0 | 0 |
| Recession | -27×-19=513 | 102.6 |
| Sum | | 162 |

**σ_M²**:
- 0.3(11)² + 0.5(1)² + 0.2(-19)² = 36.3 + 0.5 + 72.2 = 109

**β** = 162/109 = **1.49**

**CAPM check** (R_f=4%):
- E[R] = 4 + 1.49(9-4) = 11.45%
- Actual E[R] = 12% → α = 0.55%

</details>

### Q5. 계산 — CAPM portfolio

- R_f = 5%, E[R_M] = 11%
- A β=0.8, B β=1.5

(a) A, B required return?
(b) 50/50 portfolio?
(c) Leveraged (50% A + 100% B − 50% R_f)?

<details><summary>답</summary>

**(a)**:
- A: 5 + 0.8(6) = **9.8%**
- B: 5 + 1.5(6) = **14%**

**(b)** 50/50:
- β_P = 0.5(0.8) + 0.5(1.5) = 1.15
- E[R_P] = 5 + 1.15(6) = **11.9%**

**(c)** Leverage:
- β_P = 0.5(0.8) + 1(1.5) + (-0.5)(0) = 1.9
- E[R_P] = 5 + 1.9(6) = **16.4%**

**해석**:
- Leverage → β ↑, R ↑
- Cost: σ ↑ also
- Sharpe ratio same (theoretical)

**Real leverage**:
- Hedge fund 2-5x
- LTCM 30x (collapsed)
- Banks 10x typical
- TQQQ 3x

</details>

### Q6. 계산 — Diversification limit

Each σ=30%, avg covariance=100 (ρ=0.11).

(a) N=1 σ_P?
(b) N=30?
(c) N→∞?

<details><summary>답</summary>

**Formula**: 
$$\sigma_P^2 = \frac{\sigma^2}{N} + \left(1 - \frac{1}{N}\right) \overline{Cov}$$

**(a) N=1**: 30%

**(b) N=30**:
- σ_P² = (900/30) + (29/30)(100) = 30 + 96.67 = 126.67
- σ_P = **11.25%**

**(c) N→∞**:
- σ_P² → 100
- σ_P → **10%**

**Implications**:
- N=1: 30%
- N=30: 11.25% (close to limit)
- N→∞: 10% (systematic only)

→ 30 stocks captures most diversification.

**Modern view**:
- S&P 500: over-diversification (marginal)
- International — additional via different dynamics
- Multi-asset — beyond stock
- *Correlation increasing globally*
- Crisis correlation ↑ all → 1

</details>

### Q7. 디버그 — Low beta anomaly

CAPM 예측: low β → low return. 실증: low β → *higher* return.

원인?

<details><summary>답</summary>

**Frazzini-Pedersen (2014) — Betting Against Beta**:

**Causes**:

**1. Leverage constraints**:
- 많은 투자자 (pension, mutual fund) leverage 불가
- → Demand for high β (achieve return without leverage)
- → High β over-priced, low β under-priced

**2. Behavioral**:
- Lottery-like preference (high β upside)
- Over-confidence stock picking
- Herding popular stocks

**3. Agency problem**:
- Manager — track index, over-weight high β bull
- Career risk — fear of underperform
- → High β bid up

**4. Defensive demand**:
- Pension, insurance — limited risk tolerance
- Risk parity weights 1/β
- → Low β additional demand

**Empirical robust**:
- Across countries
- Across asset class (stock, bond, futures, currency, commodity)
- Pre-1960s also

**Strategy**:
- BAB factor: Long low β, short high β
- Beta-neutral: leverage low β
- Risk parity

**Practitioners**:
- AQR — BAB
- Bridgewater — risk parity
- Buffett — quality at fair (low β + quality)

→ CAPM fundamental failure. Multi-factor model necessity.

</details>

### Q8. 디버그 — Tech bubble 2000

1999-2000 dot-com:
- Tech β ~2-3
- 2000-2002 return -78%

CAPM 실패?

<details><summary>답</summary>

**CAPM = *expected*, *realized 가 아님***:

**1. E[R] = long-run avg**:
- Single period realization 의 deviation
- Bubble + crash = equilibrium deviation

**2. Bubble dynamics**:
- Disequilibrium, expectation-driven
- Fundamental decoupling
- Mean reversion eventually

**3. β estimation error**:
- Pre-bubble β measured during bull
- Time-varying β

**4. Behavioral bubble**:
- Overconfidence, FOMO, herding
- EMH 위반

**5. ERP shift**:
- Tech ERP during bubble — abnormally low
- Bursting → normalization → crash

**Interpretation**:

**Long-run (1990-2010 avg)**: Tech ~7%/year, CAPM 17%, underperformance.

**Short-run (1999-2000)**: +50%, large positive α.

**Crash (2000-2002)**: -78%, huge negative α.

**Lessons**:
1. CAPM = equilibrium, not crystal ball
2. Bubble outside equilibrium
3. Behavioral + AMH supplements
4. β instability extreme periods
5. Multi-factor + real options + scenario

**Modern response**:
- Diversification
- Value + quality factor
- Mean reversion expectation
- Position sizing — small in bubble assets

</details>

### Q9. 디버그 — β time-varying

회사 X β:
- 2018: 0.9
- 2020 COVID: 1.5
- 2022 recovery: 1.1
- 2024: 0.95

WACC 어떤 β?

<details><summary>답</summary>

**β 변화 이유**:

1. Business change (product launch β ↑, mature mix β ↓)
2. Macro environment (crisis 모두 ↑)
3. Estimation issue (sample, outlier, window)
4. Real time-variation (leverage, operating leverage)

**Best practice**:

**1. Smoothed β (Bayesian)**:
$$\beta_{adj} = 0.66 \beta_{raw} + 0.33 \times 1$$

**2. Industry β** — peer average

**3. Forward adjustment** — strategy change anticipate

**4. Bottom-up β (Damodaran)**:
- Unleveraged β
- Re-leverage with target structure
$$\beta_L = \beta_U [1 + (1-T_c) D/E]$$

**5. Rolling estimation** — 5-year, monthly

**Recommendation by use**:

| Use | β choice |
|--|--|
| Long-term WACC | 5-yr rolling, Bayesian smooth |
| Short-term sensitivity | Recent 1-2 yr |
| Crisis valuation | Pre-crisis baseline |
| Forward project | Industry β + adjustment |
| M&A target | Bottom-up + capital structure |

**Tools**:
- Bloomberg β (2yr weekly, adjusted)
- Damodaran database (industry, unlevered)
- Capital IQ (multiple windows)
- Fama-French (factor exposure)

**Famous controversies**:
- Apple 2010-20: β 0.8 → 1.3 (tech-or-consumer)
- Tesla 2020-23: β 1.5 → 2.5 (auto vs tech)
- Bank 2008: β 1.2 → 2.0 → 1.5 (systemic)

</details>

### Q10. 면접 — *CAPM relevance + modern alternatives*?

<details><summary>답</summary>

**CAPM relevance**:

1. *Educational baseline* — single-factor simple
2. *Industry practice* — WACC dominant
3. *Limitations acknowledged*

**Modern alternatives**:

| Model | Factors |
|--|--|
| FF 3 (1992) | Market + size + value |
| Carhart 4 (1997) | + momentum |
| FF 5 (2015) | + profitability + investment |
| q-factor (Hou-Xue-Zhang 2015) | Market + size + invest + profit |
| APT (Ross 1976) | Multiple macro |
| Barra | Risk model |

**Industry practice (2024)**:

| Use | Method |
|--|--|
| Textbook teaching | CAPM |
| WACC (DCF) | CAPM (still dominant) |
| Equity research | CAPM + qualitative |
| Active risk model | Multi-factor Barra |
| Smart beta passive | FF 5 or simplified |
| Academic | FF 5 + q-factor |
| Hedge fund | Macro + statistical |

**Damodaran**:
> *"CAPM sin = oversimplification. Practical abandon 어려움. *Caveat + judgment* 의 application."*

**AI-augmented**:
- ML factor discovery (kitchen sink)
- NLP earnings call sentiment
- Alternative data (satellite, credit card, social)
- Network effects (supply chain)
- Causal ML (Pearl)

**Behavioral overlay**:
- Investor sentiment
- Limits of arbitrage
- Crowding + correlation breakdown

**Buffett**:
> *"Beta = volatility, not real risk. True risk = permanent loss of capital."*

**Modern best practice**:
1. CAPM baseline (WACC)
2. Sensitivity (β range)
3. Multi-factor comparison
4. Bottom-up β
5. Industry adjustment
6. Forward-looking
7. Behavioral overlay
8. Stress test

> CAPM single-factor limitation + multi-method + judgment = modern approach.

</details>
