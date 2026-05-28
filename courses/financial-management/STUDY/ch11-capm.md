# Chapter 11: Return and Risk — CAPM — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 11** (책 p.353~390).
> 11장은 *Capital Asset Pricing Model (CAPM)* — equilibrium risk-return relationship. **Portfolio theory** (Markowitz), **Beta**, **SML**.

이 장의 *지적 무게중심*:
1. **Individual asset risk** — variance, std deviation
2. **Portfolio risk** — variance, correlation, diversification
3. **Systematic vs Unsystematic risk**
4. **CAPM**
5. **Beta**
6. **Security Market Line (SML)**

---

## §1 Individual Securities

### §1.1 Expected return

$$E[R] = \sum p_s R_s$$

### §1.2 Variance + Std

$$\sigma^2 = \sum p_s (R_s - E[R])^2$$

### §1.3 예

| State | P | R |
|--|--|--|
| Boom | 30% | 30% |
| Normal | 50% | 10% |
| Recession | 20% | -20% |

- E[R] = 0.3×30 + 0.5×10 + 0.2×(-20) = **10%**
- Variance: 0.3×400 + 0.5×0 + 0.2×900 = 300
- σ = √300 = **17.3%**

---

## §2 Portfolios

### §2.1 Portfolio Expected Return

$$E[R_P] = \sum w_i E[R_i]$$

### §2.2 Portfolio Variance — 2 assets

$$\sigma_P^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho \sigma_1 \sigma_2$$

### §2.3 Correlation range

| ρ | Meaning |
|--|--|
| +1 | Perfect positive |
| 0 | No correlation |
| -1 | Perfect negative |

### §2.4 Diversification core

> ρ < 1 → portfolio σ < weighted avg.

**예** — 2 assets, equal weight, σ = 20%:
- ρ = 1: σ_P = 20% (no diversification)
- ρ = 0: σ_P = 14.1% (decent)
- ρ = -1: σ_P = 0% (perfect hedge)

### §2.5 Portfolio Variance — N assets

$$\sigma_P^2 = \sum_i w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j Cov_{ij}$$

→ N variance + N(N-1) covariance terms. Large N: covariance dominant.

### §2.6 Equal-weight large portfolio

> N → ∞, equal weight, similar assets:

$$\sigma_P^2 \to \overline{Cov}$$

→ Individual variance N분의 1, covariance average 만 남음.

---

## §3 Systematic vs Unsystematic Risk

### §3.1 Total risk decomposition

**Systematic** (market): 모든 자산 영향, *diversification 불가*. GDP, rate, war.
**Unsystematic** (firm-specific): 특정 영향, *diversification 가능*. CEO, recall, lawsuit.

### §3.2 Diversification limit

```
Portfolio σ
  |\
  | \
  |  \____ Systematic risk (limit)
  |________________ N
       30-50
```

- N ~30: most unsystematic gone
- N → ∞: only systematic

### §3.3 Implications

- *Unsystematic non-priced* — 시장 compensate 안 함
- *Systematic priced* — Beta measure

---

## §4 Beta — Systematic Risk Measure

### §4.1 Definition

$$\beta_i = \frac{Cov(R_i, R_M)}{\sigma_M^2}$$

### §4.2 Interpretation

| β | Meaning |
|--|--|
| = 1 | Move with market |
| > 1 | Aggressive |
| < 1 | Defensive |
| = 0 | No correlation |
| < 0 | Counter-cyclical (gold) |

### §4.3 Industry betas (2024)

| Industry | β |
|--|--|
| Utility | 0.4-0.6 |
| Consumer staple | 0.6-0.8 |
| Healthcare | 0.7-0.9 |
| Industrial | 1.0-1.2 |
| Financial | 1.1-1.3 |
| Tech | 1.2-1.5 |
| Biotech | 1.5-2.0 |
| Crypto | 2.0-3.0 |

### §4.4 Portfolio beta

$$\beta_P = \sum w_i \beta_i$$

### §4.5 Estimation

**Regression**:
$$R_i - R_f = \alpha + \beta (R_M - R_f) + \epsilon$$

- Slope = β
- Intercept = α (Jensen's alpha)
- R² = explained variance

**Common**: 5 year monthly, S&P 500 proxy, 3-mo T-bill R_f.

### §4.6 Beta instability

- Time-varying
- Industry restructuring
- Recession 시 ↑ (correlation 증가)
- Bayesian shrinkage toward 1

---

## §5 CAPM

### §5.1 Equation

$$E[R_i] = R_f + \beta_i (E[R_M] - R_f)$$

= R_f + β × ERP.

### §5.2 Assumptions

1. Risk-averse + mean-variance optimizer
2. Homogeneous expectations
3. Risk-free borrow/lend
4. No transaction cost, tax
5. Single-period horizon
6. Frictionless markets
7. All hold market portfolio

### §5.3 예 — IBM

- R_f = 4%, ERP = 6%, β = 0.9
$$E[R] = 4\% + 0.9 \times 6\% = 9.4\%$$

### §5.4 왜 CAPM

- Single-factor simple
- Equilibrium derived
- Industry standard
- DCF discount rate

---

## §6 Security Market Line (SML)

### §6.1 Graphical CAPM

```
E[R]
  ^
  |       . Asset A (above = under-priced)
  |    .
  |  .  
  |.    Slope = ERP
  R_f___________ β
              1
```

- Slope = ERP, Intercept = R_f
- On SML: fairly priced
- Above: under-priced
- Below: over-priced

### §6.2 SML vs CML

| | SML | CML |
|--|--|--|
| X-axis | Beta | Std dev |
| Y-axis | E[R] | E[R] |
| Use | Individual asset | Efficient portfolio |
| Risk | Systematic | Total |

### §6.3 Mispricing

- Above → buy → price ↑ → SML 수렴
- Below → sell → price ↓ → SML 수렴

→ Arbitrage mechanism.

---

## §7 Markowitz Portfolio Theory

### §7.1 Efficient Frontier

```
E[R]
  |     *   Maximum
  |    *
  |   *
  |  * Efficient frontier
  | *
  |* Min variance
  |____________________ σ
```

### §7.2 Optimal Portfolio

- Risk-free + risky 의 combination
- Tangent of CML and frontier = *Market portfolio*
- Two-fund theorem — all hold same risky, vary R_f weight

### §7.3 Risk-free addition

- Lending (positive R_f) — conservative
- Borrowing (negative R_f, leverage) — aggressive
- All optimal on CML

### §7.4 Market portfolio

> Theoretically: all risky, market cap weighted.

- S&P 500 common proxy
- Total stock market broader
- Global multi-asset true theoretical

---

## §8 CAPM Empirical Evidence

### §8.1 Tests

**Fama-MacBeth (1973)** — two-pass regression.

**Findings**:
- Beta-return relationship exists
- Slope < ERP (weak)
- Size, value 등 significant

### §8.2 Known failures

**1. Low beta anomaly** (Frazzini-Pedersen 2014): Low β stocks outperform.
**2. Size effect**: Small > Large after β.
**3. Value effect**: Value > Growth after β.
**4. Momentum**: Past winner outperforms (12 month).

### §8.3 Critiques

- *Roll critique (1977)*: Market portfolio non-observable
- Empirical failures
- Behavioral biases not captured
- Single-period unrealistic
- Homogeneous expectations unrealistic

### §8.4 Modern alternatives

- Fama-French 3 factor: market + size + value (1992)
- Carhart 4 factor: + momentum (1997)
- Fama-French 5 factor: + profitability + investment (2015)
- APT (Ross 1976) — multiple factors
- q-factor (Hou-Xue-Zhang)

---

## §9 CAPM Practical Use

### §9.1 Capital budgeting

> Project β → required return → WACC.

### §9.2 Portfolio management

- Active: alpha search
- Passive: β = 1 (index)
- Smart beta: factor tilts

### §9.3 Performance evaluation

- Jensen's alpha: portfolio return − CAPM predicted
- Treynor: excess / β
- Information ratio: alpha / tracking error

### §9.4 Risk management

- Portfolio β monitoring
- Beta hedging
- Stress test (β change in crisis)

---

## §10 International CAPM

### §10.1 International

$$E[R] = R_f + \beta_w (E[R_w] - R_f)$$

### §10.2 Country β

- Developed: 1.0 baseline
- Emerging: 1.5-2.0
- Country risk premium (Damodaran)

### §10.3 Cross-border

- Adler-Dumas — segmented
- Solnik — integrated
- Modern — partial integration

---

## §11 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | High return = high σ | Systematic 만 priced |
| 2 | Diversification 무한 | Systematic floor |
| 3 | β = volatility | β = systematic, σ = total |
| 4 | CAPM empirical 정확 | Multiple anomalies |
| 5 | Market = S&P 500 | Theoretical broader |
| 6 | β 안정 | Time-varying |
| 7 | Single-factor sufficient | Multi-factor modern |
| 8 | Negative β impossible | Gold rare 가능 |

---

## §12 자가점검

1. *Portfolio variance* 2-asset?
2. *Diversification limit*?
3. *Systematic vs Unsystematic*?
4. *Beta* 정의?
5. *CAPM equation + assumptions*?
6. *SML 위/아래*?
7. *Empirical failures*?

<details><summary>해답</summary>

1. $\sigma_P^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho\sigma_1\sigma_2$.
2. Unsystematic 사라짐, systematic floor.
3. Systematic = market-wide undiversifiable. Unsystematic = firm-specific diversifiable.
4. $\beta = Cov(R_i, R_M)/\sigma_M^2$.
5. $E[R] = R_f + \beta(E[R_M]-R_f)$. Risk-averse, mean-variance, homogeneous, R_f borrow/lend, frictionless.
6. Above SML = under-priced (buy), below = over-priced (sell).
7. Low beta anomaly, size, value, momentum. Roll critique.

</details>

---

## §13 다음 학습으로

- **Ch 12** — APT, multi-factor
- **Ch 13** — WACC

---

## §14 한 줄 요약

> **Risk = systematic + unsystematic. Diversification 의 unsystematic 제거, systematic floor. *Beta* = systematic measure. *CAPM*: $E[R] = R_f + \beta \cdot ERP$. *SML* equilibrium pricing. *Markowitz* + *CML*. *CAPM empirical limit* — low beta, size, value, momentum anomalies. *Multi-factor* (Fama-French) modern extension.**
