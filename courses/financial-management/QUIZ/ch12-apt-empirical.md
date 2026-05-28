# Ch 12 APT and Empirical Models — 퀴즈

> 10 문항 (개념 3 / 계산 3 / 디버그 3 / 면접 1).

### Q1. *APT vs CAPM*?

<details><summary>답</summary>

| | CAPM | APT |
|--|--|--|
| Factors | Market | Multiple |
| Foundation | Equilibrium | No-arbitrage |
| Assumptions | Strict | Weak |
| Factor spec | Market | Not specified |
| Test | Market observable | Factor arbitrary |

**APT strength**: Factor flexibility, robust, strong empirical.

**APT weakness**: Factor specification 모호, overfitting risk.

**No-arbitrage logic**:
- Same exposure → same return
- Otherwise arbitrage
- Equilibrium *no riskless profit*

</details>

### Q2. *Fama-French 5 Factor*?

<details><summary>답</summary>

| Factor | 명칭 | 의미 |
|--|--|--|
| Market | R_M - R_f | 시장 risk |
| SMB | Small Minus Big | Size |
| HML | High Minus Low B/M | Value |
| RMW | Robust Minus Weak | Profitability |
| CMA | Conservative Minus Aggressive | Investment |

**Carhart 4-factor**: + WML (Momentum)

**Origin**:
- Banz (1981): small-cap
- Stattman (1980): B/M
- Jegadeesh-Titman (1993): momentum
- Novy-Marx (2013): profitability

**Empirical**:
- 5-factor ~95% of variation
- Each positive premium historically
- Time-varying

**Critiques**: Multiple testing, replication crisis.

</details>

### Q3. *Chen-Roll-Ross macro factors*?

<details><summary>답</summary>

**5 macro factors (1986)**:

| Factor | Intuition |
|--|--|
| IP growth | Economic activity |
| Inflation | Purchasing power |
| Term spread | Future rate |
| Default spread | Recession risk |
| Oil price | Input cost |

**Modern macro factors**:
- Currency (FX)
- Carry (rate differential)
- Commodity
- Volatility (VIX)
- Liquidity (TED spread)
- Credit conditions
- Geopolitical (GPR)

**Use**:
- Hedge fund macro
- Asset allocation regime
- VaR by factor
- Stress test

</details>

### Q4. 계산 — APT pricing

- R_f = 4%
- λ_1 (market) = 6%, λ_2 (size) = 3%, λ_3 (value) = 4%
- β_1 = 1.2, β_2 = 0.5, β_3 = 0.3

E[R]?

<details><summary>답</summary>

$$E[R] = R_f + \beta_1 \lambda_1 + \beta_2 \lambda_2 + \beta_3 \lambda_3$$
$$= 4 + 1.2(6) + 0.5(3) + 0.3(4) = 13.9\%$$

**Decomposition**:
- Market: 7.2% (52%)
- Size: 1.5% (11%)
- Value: 1.2% (8%)
- Risk-free: 4% (29%)

→ CAPM only would be 4 + 1.2×6 = 11.2%. Multi-factor 13.9% — higher required.

</details>

### Q5. 계산 — Factor regression

| Period | R_stock | R_market | SMB | HML |
|--|--|--|--|--|
| Q1 | 5% | 3% | 1% | 2% |
| Q2 | 8% | 6% | 2% | -1% |
| Q3 | -2% | -1% | -3% | 1% |
| Q4 | 10% | 7% | 4% | 3% |

R_f = 2%/Q. β + α?

<details><summary>답</summary>

**Excess returns** (R - R_f):

| Period | Stock | Market |
|--|--|--|
| Q1 | 3% | 1% |
| Q2 | 6% | 4% |
| Q3 | -4% | -3% |
| Q4 | 8% | 5% |

**Approximate regression**:
- β_market ≈ 1.55
- β_SMB ≈ 0.45
- β_HML ≈ 0.85
- α ≈ 0.5%

**Python**:
```python
from sklearn.linear_model import LinearRegression
X = [[1,1,2],[4,2,-1],[-3,-3,1],[5,4,3]]
y = [3, 6, -4, 8]
model = LinearRegression().fit(X, y)
```

**Reality**:
- 4 periods 너무 적음
- Standard: 5 year monthly (60 obs)
- Newey-West robust std error

</details>

### Q6. 계산 — Multi-factor required + Alpha

Stock A:
- β_M = 1.0, β_SMB = 0.8, β_HML = 0.5
- Premia: 6%, 3%, 4%, R_f 4%
- Realized R = 16%, σ = 25%

(a) CAPM required?
(b) 3-factor required?
(c) Sharpe?
(d) Multi-factor alpha?

<details><summary>답</summary>

**(a) CAPM**: 4 + 1.0(6) = **10%**

**(b) 3-factor**: 4 + 1.0(6) + 0.8(3) + 0.5(4) = **14.4%**

**(c) Sharpe**: (16-4)/25 = **0.48**

**(d) Alpha**:
- CAPM α = 16-10 = **6%**
- 3-factor α = 16-14.4 = **1.6%**

→ CAPM alpha 6% 의 대부분이 factor exposure 로 explained.

**Implication**:
- True skill α = 1.6% (small)
- CAPM under-estimates risk premium
- Many "successful manager α" disappears with multi-factor
- Smart beta revolution justification

</details>

### Q7. 디버그 — Factor Death (2010-2020)

Value premium negative. *Value is dead*?

<details><summary>답</summary>

**Decade (2010-2020)**:
- Value: -5% to 0% premium (vs historical 4-5%)
- Growth outperformance (FAANG bubble)
- Multiple expansion in growth
- Low rate — value의 cheap funding 무용

**왜 *Death debate***:

**1. Structural**:
- Intangibles not in book value
- Asset-light businesses
- Network effects (winner-takes-all)

**2. Crowding**:
- Many funds same metric
- Smart beta proliferation
- Arbitrage away

**3. Monetary**:
- Low rates favor growth
- QE inflated growth assets

**Counter-argument — *Value alive***:

**1. Cyclical** — historical 7-10 year cycles
**2. 2021-2023 revival** — rate increase
**3. International strong** — less crowded
**4. Modified value** — EV/EBITDA, FCF yield

**Modern response**:
1. Multi-factor — single cyclicality 완화
2. Quality factor — sustainable value
3. Defensive value (low vol + value)
4. International diversification
5. ESG overlay

**Practitioners**:
- Fama-French 2020: "Long-term value 인정, recent negative"
- AQR (Asness 2020): "Temporary underperformance"
- Buffett: "Quality + Value" evolution

→ Factor cyclicality. Single-factor risk. Multi-factor judgment.

</details>

### Q8. 디버그 — Factor Zoo + Replication Crisis

Researcher: *"100 factors significant. Profitable strategy?"*

<details><summary>답</summary>

**Multiple testing bias**:
- p<0.05 가정 — random data 도 *20번에 1번* significant
- 100 factors → ~5 expected false positive
- Bonferroni correction: p<0.0005

**Data mining**:
- In-sample over-fitting
- Out-of-sample test critical
- Long historical + international replication

**Hou-Xue-Zhang (2020)**:
- Replicate 452 factors
- 65% fail
- Surviving: market, value, profitability, investment

**Harvey-Liu-Zhu (2016)**:
- Multiple testing adjustment
- Only 5-10 robust factors
- Most published — false positives

**Implications**:

1. **Skepticism** — replication
2. **Robustness** — OOS, international, period
3. **Implementable** — cost, capacity, lag, tax

**Modern best practice**:
1. Theoretical motivation
2. Long historical replication
3. Multiple geography
4. Multiple time periods
5. Implementable cost reality
6. Capacity considerations
7. OOS verification
8. Multiple testing correction

**Quote**:
- Cochrane (2011): "Factor zoo의 cleaning out 우선"
- Harvey (2017): "Most published research findings likely false"

**Robust universe** (~5-8):
1. Market, 2. Size, 3. Value, 4. Momentum
5. Profitability, 6. Investment, 7. Low beta, 8. Carry

→ Hundreds others의 *cautious skepticism*.

</details>

### Q9. 디버그 — *ML factor models*

ML model — *OOS Sharpe 2.0* claim. Believable?

<details><summary>답</summary>

**ML promise**:
- Nonlinear relationships
- High-dimensional features
- Interaction effects
- OOS improvement (some papers)

**Peril**:

**1. Over-fitting** — deep nets, sample-specific
**2. Look-ahead bias** — feature engineering using future
**3. Implementation gap** — capacity, latency, borrow, tax
**4. Survivorship** — failed models unpublished
**5. Snapshot vs Evolution** — regime changes

**Kelly-Pruitt-Su (2020)**:
- Linear ML (instrumented PCA)
- Interpretability
- OOS valid
- Modest gains (Sharpe 0.5 → 1.0)

**Gu-Kelly-Xiu (2020)**:
- 30 ML factors
- OOS Sharpe 0.4 → 0.8

**Why *Sharpe 2.0 suspicious***:
- Buffett Berkshire: 0.76 lifetime
- Renaissance Medallion: 2-3 (legendary)
- Most ML papers: 0.5-1.0 realistic
- 2.0 = outlier even for top quant

**Red flags**:
1. No transaction cost
2. Recent data only
3. Single asset class
4. No documentation
5. Cherry-picked metrics

**Lopez de Prado (2018)**: *"Most ML finance = over-fitting + leakage + survivorship"*.

**Modern best practice**:
1. Linear baseline
2. ML as supplement (interpretable)
3. OOS years (multiple)
4. Implementation cost reality
5. Capacity test
6. Cross-team replication

→ ML = useful supplement, not magic. *Skeptical evaluation*.

</details>

### Q10. 면접 — *Factor investing future + challenges*?

<details><summary>답</summary>

**Evolution**:

| Phase | Period | Characterization |
|--|--|--|
| 1 | 1992-2010 | Academic discovery |
| 2 | 2010-2020 | Smart beta boom |
| 3 | 2020- | Multi-factor + AI |
| 4 | 2025-? | Personalized + ESG + crypto |

**Challenges**:

1. **Crowding** — $1T+ smart beta AUM, premium decay
2. **Implementation cost** — turnover, spread, tax
3. **Factor cyclicality** — 2010-2020 value drought
4. **ESG complications** — traditional factor disruption
5. **AI / ML disruption** — quant arms race

**Future trends**:

1. **Multi-factor dominant** — single factor 의 high tracking error
2. **Macro overlay** — regime-conditional weights
3. **Alternative data** — satellite, credit card, social media
4. **Personalized** — tax, ESG, lifecycle
5. **Crypto factor** — Bitcoin, Ethereum
6. **Real-time tactical** — daily rebalancing

**Industry consolidation**:
- Active fund decline
- Passive + Smart beta growth
- Hedge fund fee compression
- Robo-advisor democratization

**Quotes**:
- Bogle: *"Smart beta = active의 마지막 진화"*
- Marks (Oaktree): *"Markets still inefficient, just less so"*
- Asness (AQR): *"Multi-factor long-term success"*

**Investor strategy**:

1. Diversified multi-factor foundation
2. Low cost implementation
3. Long-term horizon (factor cycles)
4. International exposure
5. Alternative assets
6. Periodic rebalancing
7. Tax efficiency
8. ESG integration (if aligned)

**Core portfolio**:
- Core (60%): broad index
- Factor tilt (20%): multi-factor smart beta
- Bonds (15%): duration + credit
- Alternatives (5%): gold, REIT, commodity

> Factor investing = *evolving discipline*. *Multi-factor + low cost + long-term* core principles persist.

</details>
