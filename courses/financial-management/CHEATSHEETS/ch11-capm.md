# Ch 11 CAPM — 치트시트

> Risk decomposition / Beta / CAPM / SML / Markowitz.

## §1 Expected + Variance (single)

$$E[R] = \sum p_s R_s$$
$$\sigma^2 = \sum p_s (R_s - E[R])^2$$

## §2 Portfolio Expected Return

$$E[R_P] = \sum w_i E[R_i]$$

## §3 Portfolio Variance (2-asset)

$$\sigma_P^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho \sigma_1 \sigma_2$$

## §4 Correlation

| ρ | Diversification |
|--|--|
| +1 | None |
| 0 | Moderate |
| -1 | Perfect hedge |

## §5 Risk Decomposition

$$Total = Systematic + Unsystematic$$

| | 의미 | Diversifiable |
|--|--|--|
| Systematic | Market-wide | No |
| Unsystematic | Firm-specific | Yes (N~30) |

## §6 Diversification limit

```
σ_P
  |\
  | \____ Systematic floor
  |______________ N
       30-50
```

## §7 Beta

$$\beta_i = \frac{Cov(R_i, R_M)}{\sigma_M^2}$$

| β | Meaning |
|--|--|
| = 1 | Move with market |
| > 1 | Aggressive |
| < 1 | Defensive |
| = 0 | No correlation |
| < 0 | Counter-cyclical |

## §8 Industry betas (2024)

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

## §9 Portfolio Beta

$$\beta_P = \sum w_i \beta_i$$

## §10 CAPM

$$E[R_i] = R_f + \beta_i (E[R_M] - R_f) = R_f + \beta_i \times ERP$$

## §11 CAPM Assumptions (7)

1. Risk-averse + mean-variance
2. Homogeneous expectations
3. Risk-free borrow/lend
4. No tx cost, tax
5. Single-period
6. Frictionless
7. All hold market portfolio

## §12 SML

```
E[R]
  ^
  |    . Above (under-priced)
  |   .
  |  .  Slope = ERP
  R_f___________ β
              1
```

| Position | Action |
|--|--|
| On SML | Fair |
| Above | Under-priced (buy) |
| Below | Over-priced (sell) |

## §13 SML vs CML

| | SML | CML |
|--|--|--|
| X-axis | Beta | Std dev |
| Use | Individual | Efficient portfolio |
| Risk | Systematic | Total |

## §14 Markowitz Frontier

```
E[R]
  |     *
  |    *
  |   *
  |  * Efficient
  | *
  |* Min variance
  |__________ σ
```

## §15 Two-fund theorem

> All hold *same risky portfolio*, vary R_f weight.

- Lending: conservative
- Borrowing: aggressive
- All on CML

## §16 β Estimation

$$R_i - R_f = \alpha + \beta(R_M - R_f) + \epsilon$$

- Slope = β
- Intercept = α
- R² = explained

**Common**: 5yr monthly, S&P 500.

## §17 β Smoothing

$$\beta_{adj} = 0.66 \beta_{raw} + 0.33 \times 1$$

→ Shrinks toward 1.

## §18 Bottom-up β

$$\beta_L = \beta_U [1 + (1-T_c) D/E]$$

→ Industry unlevered + capital structure.

## §19 CAPM Failures

| Anomaly | Effect |
|--|--|
| Low β | Outperform high β |
| Size | Small > Large |
| Value | Value > Growth |
| Momentum | Past winner |
| Quality | High ROE + low debt |

## §20 Modern Factor Models

| Model | Factors |
|--|--|
| FF 3 (1992) | Market, SMB, HML |
| Carhart 4 (1997) | + WML (momentum) |
| FF 5 (2015) | + RMW + CMA |
| q-factor (2015) | Market, size, invest, profit |
| APT (1976) | Multiple macro |

## §21 자주 함정

| 함정 | 정정 |
|--|--|
| High return = high σ | Systematic만 priced |
| Diversification 무한 | Floor |
| β = volatility | β systematic, σ total |
| CAPM accurate empirical | Anomalies |
| Market = S&P 500 | Theoretical broader |
| β 안정 | Time-varying |
| Single-factor sufficient | Multi-factor |

## §22 Performance

| Ratio | 공식 |
|--|--|
| Sharpe | (R-R_f)/σ |
| Treynor | (R-R_f)/β |
| Jensen's α | R - CAPM 예측 |
| Information | α / tracking error |

## §23 Quotes

- *Buffett*: "Beta = volatility, not real risk."
- *Damodaran*: "CAPM oversimplification, abandon 어려움."
- *Markowitz*: "Diversification = only free lunch."

## §24 핵심 mindmap

```
CAPM
├── Risk decomposition
│   ├── Systematic
│   └── Unsystematic
├── Beta
│   ├── Cov/σ²_M
│   ├── Estimation
│   └── Smoothing
├── CAPM
│   ├── E[R] = R_f + β·ERP
│   ├── 7 assumptions
│   └── SML
├── Portfolio Theory
│   ├── Markowitz frontier
│   ├── Two-fund theorem
│   ├── CML
│   └── Market portfolio
└── Empirical
    ├── Failures
    ├── Multi-factor
    └── Behavioral
```

## §25 1-line summary

> **Risk = systematic + unsystematic. Diversification 의 unsystematic 제거, systematic floor. *Beta* = systematic measure. CAPM: $E[R] = R_f + \beta \cdot ERP$. SML equilibrium. Markowitz frontier + CML. Empirical failures (low β, size, value, mom). Multi-factor (FF) modern extension.**
