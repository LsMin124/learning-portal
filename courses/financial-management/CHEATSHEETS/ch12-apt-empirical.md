# Ch 12 APT and Empirical — 치트시트

> APT / Multi-factor / Fama-French / Macro / Empirical.

## §1 Multi-factor model

$$R_i = \alpha_i + \beta_{i1} F_1 + ... + \beta_{iK} F_K + \epsilon_i$$

## §2 APT (Ross 1976)

$$E[R_i] = R_f + \beta_{i1} \lambda_1 + ... + \beta_{iK} \lambda_K$$

No-arbitrage equilibrium.

## §3 APT vs CAPM

| | CAPM | APT |
|--|--|--|
| Factors | Market only | Multiple |
| Foundation | Equilibrium | No-arbitrage |
| Assumptions | Strict | Weak |
| Factor spec | Market | Not specified |

## §4 Factor types

| Type | 예 |
|--|--|
| Macro | GDP, inflation, rate, oil |
| Fundamental | Size, value, profitability |
| Statistical | PCA |

## §5 Fama-French 3 Factor (1992)

$$R - R_f = \alpha + \beta_M(R_M-R_f) + \beta_{SMB}SMB + \beta_{HML}HML$$

## §6 Carhart 4 Factor (1997)

> + WML (Winners Minus Losers) = Momentum

## §7 Fama-French 5 Factor (2015)

> + RMW (profitability) + CMA (investment)

| Factor | 의미 |
|--|--|
| Market | 시장 risk |
| SMB | Size |
| HML | Value |
| RMW | Profitability |
| CMA | Investment |

## §8 Chen-Roll-Ross Macro (1986)

1. IP growth
2. Inflation
3. Term spread
4. Default spread
5. Oil price

## §9 Risk Premia (US 1926-2024)

| Factor | Annual |
|--|--|
| Market | ~8% |
| SMB | ~3% |
| HML | ~4% |
| WML | ~8% |
| RMW | ~3% |
| CMA | ~3% |

## §10 Factor cyclicality

| Period | Value |
|--|--|
| 1926-2000 | Strong + |
| 2000-2020 | Weak/- |
| 2021- | Revival |

## §11 Factor Zoo (Cochrane 2011)

- Hundreds proposed
- Multiple testing bias
- Data mining
- OOS failure

## §12 Replication Crisis

- Hou-Xue-Zhang (2020): 65% fail OOS
- Harvey-Liu-Zhu (2016): 5-10 robust

## §13 Robust universe (~8)

1. Market
2. Size
3. Value
4. Momentum
5. Profitability/Quality
6. Investment
7. Low beta
8. Carry

## §14 Behavioral vs Rational

| | Rational | Behavioral |
|--|--|--|
| Source | Risk premium | Mispricing |
| Example | Macro risk | Glamour neglect |

## §15 Smart beta ETFs

| ETF | Factor |
|--|--|
| IWN | Value |
| IWM | Size |
| MTUM | Momentum |
| QUAL | Quality |
| USMV | Low vol |

## §16 ML factor models

| Study | Finding |
|--|--|
| Kelly-Pruitt-Su 2020 | Linear ML 0.5→1.0 Sharpe |
| Gu-Kelly-Xiu 2020 | 30 ML factors 0.4→0.8 |
| Lopez de Prado | "Most = over-fitting" |

## §17 자주 함정

| 함정 | 정정 |
|--|--|
| More = better | Multiple testing |
| Historical = future | Time-varying |
| Factor = risk | Behavioral possible |
| Single factor 충분 | Multi-factor |
| Factor stable | Time-varying premium |
| APT = CAPM | Different foundation |
| Easy ID | Factor zoo |

## §18 Modern best practice

1. Theoretical motivation
2. OOS test
3. International replication
4. Multiple testing correction
5. Economic significance
6. Implementable cost
7. Capacity
8. Cross-team replication

## §19 Industry adoption (2024)

| Use | Method |
|--|--|
| Textbook | CAPM |
| WACC | CAPM dominant |
| Equity research | CAPM + qualitative |
| Active risk | Barra |
| Smart beta | FF 5 / simplified |
| Academic | FF 5 + q-factor |
| Hedge fund | Macro + statistical + ML |

## §20 핵심 mindmap

```
APT + Multi-factor
├── APT
│   ├── No-arbitrage
│   ├── Multi-factor
│   └── vs CAPM
├── Fama-French (3, 4, 5)
├── Macro (Chen-Roll-Ross)
├── Statistical (PCA)
└── Modern
    ├── Factor Zoo
    ├── Replication crisis
    ├── ML
    └── Smart beta
```

## §21 1-line summary

> **APT (Ross 1976) = no-arbitrage multi-factor pricing. CAPM single-factor extension. Fama-French 3/4/5 models. Macro (Chen-Roll-Ross) + fundamental + statistical (PCA). Risk vs behavioral interpretation. Factor Zoo + replication crisis challenges. Multi-factor portfolio + ETF industry adoption.**
