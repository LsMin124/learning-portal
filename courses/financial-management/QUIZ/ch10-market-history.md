# Ch 10 Lessons from Market History — 퀴즈

> 10 문항 (개념 2 / 계산 4 / 디버그 3 / 면접 1).

### Q1. *Historical returns* US 1926-2024?

<details><summary>답</summary>

| Asset | Return | Std Dev | Real |
|--|--|--|--|
| Small stocks | 16.1% | 31.4% | ~13% |
| Large stocks | 12.1% | 19.5% | ~9% |
| LT corp bonds | 6.4% | 8.5% | ~3.4% |
| LT gov bonds | 6.0% | 9.8% | ~3% |
| T-bills | 3.4% | 3.0% | ~0.4% |
| Inflation | 3.0% | 4.0% | — |

**Risk-return**: Higher return = Higher risk.

**$1 → 2024**:
- Small $40K+, Large $13K+, Bonds $200-250, T-bills $25, CPI $18

</details>

### Q2. EMH 3 forms + evidence?

<details><summary>답</summary>

| Form | Info | Implication |
|--|--|--|
| Weak | Past prices | Technical 무용 |
| Semi-strong | All public | Fundamental 무용 |
| Strong | All info | 모든 무용 |

**Evidence for**:
- Random walk short-term
- Mutual fund underperformance avg
- Quick news incorporation

**Anomalies (against)**:
- Value premium (Fama-French)
- Size, Momentum, Calendar
- Post-earnings drift
- Bubbles + crashes

**Behavioral**:
- Over/under-reaction
- Herding, loss aversion
- Limits to arbitrage

**Modern AMH** (Lo 2004):
- EMH 동적, adapting
- Anomaly → exploit → fade
- Strong EMH not believed

</details>

### Q3. 계산 — HPR + Annualized

5 year: +15%, -10%, +25%, +5%, -8%

<details><summary>답</summary>

**HPR**:
$$HPR = 1.15 \times 0.90 \times 1.25 \times 1.05 \times 0.92 - 1 = 24.9\%$$

**Geometric**:
$$\bar{R}_G = 1.249^{1/5} - 1 = 4.54\%$$

**Arithmetic**:
$$\bar{R}_A = (15-10+25+5-8)/5 = 5.4\%$$

→ Arithmetic > Geometric (volatility drag).

</details>

### Q4. 계산 — Variance + Std

5 yr returns: 10%, 15%, -5%, 20%, 8%

<details><summary>답</summary>

**Mean**: 9.6%

**Variance**:
| R_i | Diff | Diff² |
|--|--|--|
| 10 | 0.4 | 0.16 |
| 15 | 5.4 | 29.16 |
| -5 | -14.6 | 213.16 |
| 20 | 10.4 | 108.16 |
| 8 | -1.6 | 2.56 |
| Sum | | 353.20 |

$\sigma^2 = 353.20/4 = 88.30$
$\sigma = 9.40\%$

**CV**: 9.40/9.6 = 0.98

**Reference**:
- S&P 500 (1990-2020): μ ~10%, σ ~17%, CV 1.7
- Russell 2000: μ ~12%, σ ~22%, CV 1.8

</details>

### Q5. 계산 — Sharpe Ratio

2024: Stock 12% (σ=18%), T-bill 4%, Inflation 3%

(a) Risk premium?
(b) Sharpe?
(c) Real risk premium?

<details><summary>답</summary>

**(a)** RP = 12% - 4% = **8%**

**(b)** Sharpe = 8%/18% = **0.44**

**(c)** Real RP:
- Real stock: (1.12/1.03)-1 = 8.74%
- Real T-bill: (1.04/1.03)-1 = 0.97%
- Real RP = **7.77%** (≈ nominal RP)

**Sharpe benchmark**:
- > 1.0: Excellent
- 0.5-1.0: Good
- 0.0-0.5: Acceptable
- < 0: Poor

**Historical**:
- S&P 500: ~0.4-0.5
- Hedge fund avg: ~0.5-0.7
- Top: ~1-2
- Berkshire (1965-2009): ~0.76

**Other risk-adjusted**:
- Sortino (downside only)
- Treynor (beta-based)
- Information ratio (vs benchmark)
- Jensen's alpha (CAPM)

</details>

### Q6. 디버그 — Past 5 yr return = future?

투자자: "*S&P past 5 yr* = 15%/year. *Next 5 yr 도 15%*?"

<details><summary>답</summary>

**문제**:

1. **Recency bias** — past over-weight
2. **Mean reversion** — high → low tendency
3. **Forward indicators**:
   - Dividend yield + g = current 6%
   - CAPE inverse
   - ERP estimate
4. **Period specifics**: 2019-2024 post-COVID + Fed stimulus
5. **Survivorship bias** — only successful funds visible

**Damodaran's forward ERP (2024)**:
- ~4-5% (vs historical 8%)
- Driver: low rate, high valuations, tax change

**Realistic forward 5-yr**:
- Historical baseline 10%
- Valuation adjustment -2% ~ -3%
- Range: 4-8% (much lower than 15%)

**Famous forecasting failures**:
- 2000: dot-com → -10%/year 2000-2010
- 2008: pre-crisis bullishness
- 2021: post-COVID exuberance → 2022 bear

**Buffett (2020)**:
> "Future returns much lower. Get used to 4-6% nominal."

**Investor robust**:
- Lower expected return (5-7%)
- Higher saving rate
- Diversification
- Long-term horizon
- Sequence of return risk

</details>

### Q7. 디버그 — Normal distribution 2008 적용

S&P 2008: -37%. Normal (μ=10%, σ=20%): P ~ 1%. *Every 100 yr* or *more frequent*?

<details><summary>답</summary>

**Normal frequency**: 100 year 의 ~1 회.

**실제 historical**:

| 연도 | S&P return |
|--|--|
| 1931 | -43.8% |
| 1937 | -34.7% |
| 1974 | -25.9% |
| 2002 | -22.1% |
| 2008 | -37.0% |
| 2020 | -34% intra |

→ 100 yr 의 4-5 event (vs 1 예측).

**Fat tail evidence**:
- Excess kurtosis (4-5x more tail)
- Negative skew (extreme losses > gains)

**Better distributions**:
- Log-normal (price)
- Student-t (df 3-5)
- Generalized Pareto (tails)
- Levy stable (power-law)

**Implications**:

1. **VaR underestimation** — 3-5x more frequent
2. **Stress testing** — beyond Gaussian
3. **Portfolio insurance** — tail risk hedge
4. **Black Swan** (Taleb) — unexpected

**Famous Gaussian failures**:
- LTCM 1998
- 2008 housing
- 2020 COVID

→ *Normal = useful baseline, not reality*.

</details>

### Q8. 디버그 — Survivorship bias

뮤추얼 active fund avg 10 yr = 8% (vs S&P 10%). *Active underperform 2%*?

<details><summary>답</summary>

**True underperformance** (survivorship correction):

- Survivors only: 8%
- Including failures (30-40% death rate): 6-7%
- *True underperformance*: ~3-4% (vs 2% reported)

**Studies**:
- Carhart 1997: After cost — alpha ~ 0
- Fama-French 2010: Median underperform 0.5-1%
- SPIVA: 80%+ underperform 10-year benchmark

**왜 Survivorship**:
1. Fund failures → liquidation → no record
2. Mergers — bad absorbed
3. Strategy changes
4. Backtest survivor only sample

**General survivorship**:
- Hedge fund 심함
- Startup success rate
- Historical stock indices

**Implications**:
- Active underperformance under-estimated
- Index fund preference strengthened
- Past performance skepticism

**Modern corrections**:
- CRSP, Morningstar — survivorship-free
- Backtest forward verification

**Bogle's index argument**:
> *Average active expense + transaction + tax = long-term underperformance*. *Index = mathematical superiority*.

</details>

### Q9. 디버그 — ERP forward vs historical

Historical (1926-2024) = 8%. *Forward (2024)*?

<details><summary>답</summary>

**Methods**:

**1. Historical extrapolation** (naive) — 8%

**2. Implied ERP (reverse DCF)**:
- S&P div yield 1.5% + buyback 2% + g 5% = 8.5% return
- Minus 10-yr Treasury 4.5%
- *Implied ERP ~4%*

**3. Damodaran (2024)**: ~4-5%

**4. Surveys**:
- CFO (Graham-Harvey): 3-5%
- Academic (Welch): 4-5%
- Practitioner: 4-7%

**5. Country**:
- US: 4-5%
- Emerging: 6-9%
- Frontier: 9-12%

**왜 Forward < Historical**:

1. **Valuations higher** (CAPE 30 vs 17)
2. **Lower rate environment** (real rate 1.5%)
3. **Higher passive allocation**
4. **Globalization** (info advantage 감소)

**Implications**:

| Use | Forward ERP |
|--|--|
| Capital budgeting | 4-5% |
| Portfolio expected | 4-6% real |
| Retirement planning | 5-7% nominal |
| WACC | 4-5% |

**Robust expectation**:
- Long-term real: 5-7% (vs 9% historical)
- Bond real: 1-2% (vs 3%)
- 60/40: 3-4% real

**Pension crisis**:
- Assumed 7-8% returns
- Realistic 4-5%
- Funding gap

</details>

### Q10. 면접 — Practical investment principles?

<details><summary>답</summary>

**12 Lessons**:

**1. Compounding power** — $1 → $13K over 100 years
**2. Equity long-term superior** — real 7% > 3% > 0.4%
**3. Diversification reduces risk** — MPT, 60/40
**4. Cost matters** — 0.5% × 30 yr = 15% wealth loss
**5. Time > Timing** — missing 10 best days halves return
**6. Risk tolerance ≠ capacity** — match to horizon
**7. Fat tails real** — 1987, 2000, 2008, 2020
**8. Mean reversion** — Japan 1989-2024 extreme
**9. Behavioral biases hurt** — Dalbar 4-5% gap
**10. Asset allocation > Stock picking** — Brinson 90%
**11. Sequence of return risk** — retirement early loss
**12. Adaptive markets** — humility, continuous learning

**Wisdoms**:
- Buffett: "Fearful when greedy, greedy when fearful."
- Bogle: "Time is your friend; impulse is your enemy."
- Munger: "Big money in waiting."
- Taleb: "Don't be fooled by randomness."

**Evidence-based portfolio**:
1. Index funds (broad)
2. Diversified across asset class + geography
3. Low cost (< 0.3%)
4. Long-term hold (10+ year)
5. Tax-efficient
6. Rebalance annually
7. Lifecycle adjust
8. Tail risk insurance (if affordable)

> *Time + discipline + low cost + diversification + patience* = long-term wealth.

</details>
