# Ch 10 Lessons from Market History — 치트시트

> Historical returns / Risk / Mean / Normal / EMH / Behavioral.

## §1 Total Return

$$R = \frac{D_1}{P_0} + \frac{P_1-P_0}{P_0}$$

## §2 HPR

$$HPR = \prod (1+R_t) - 1$$

Annualized geometric: $(1+HPR)^{1/N} - 1$.

## §3 US Historical (1926-2024)

| Asset | Return | Std Dev | Real |
|--|--|--|--|
| Small stocks | 16.1% | 31.4% | ~13% |
| Large stocks | 12.1% | 19.5% | ~9% |
| LT corp bonds | 6.4% | 8.5% | ~3.4% |
| LT gov bonds | 6.0% | 9.8% | ~3% |
| T-bills | 3.4% | 3.0% | ~0.4% |
| Inflation | 3.0% | 4.0% | — |

## §4 $1 in 1926 → 2024

| Asset | 2024 |
|--|--|
| Small | $40K+ |
| Large | $13K+ |
| Corp bonds | $250 |
| Gov bonds | $200 |
| T-bills | $25 |
| CPI | $18 |

## §5 Risk Premium

$$RP = Asset - R_f$$

- Historical ERP: ~8-9%
- Forward ERP (2024): ~4-5%

## §6 Variance + Std

$$\sigma^2 = \frac{1}{N-1} \sum (R_i - \bar{R})^2$$

## §7 CV

$$CV = \sigma / \bar{R}$$

## §8 Sharpe Ratio

$$Sharpe = \frac{R - R_f}{\sigma}$$

| Sharpe | 평가 |
|--|--|
| > 1.0 | Excellent |
| 0.5-1.0 | Good |
| 0.0-0.5 | Acceptable |
| < 0 | Poor |

## §9 Arithmetic vs Geometric

| | Use |
|--|--|
| Arithmetic | Single forward |
| Geometric | Multi-period, terminal |

$\bar{R}_G \approx \bar{R}_A - \sigma^2/2$ (volatility drag).

## §10 Normal Distribution

| Range | Probability |
|--|--|
| μ ± 1σ | 68% |
| μ ± 2σ | 95% |
| μ ± 3σ | 99.7% |

## §11 Fat tails (실제 events)

| 연도 | S&P |
|--|--|
| 1931 | -43.8% |
| 1937 | -34.7% |
| 1974 | -25.9% |
| 1987 | -22% (1day) |
| 2002 | -22.1% |
| 2008 | -37.0% |
| 2020 | -34% intra |

→ 100yr 의 4-5 (vs Gaussian 1).

## §12 EMH 3 forms

| Form | Info | Implication |
|--|--|--|
| Weak | Past prices | Technical 무용 |
| Semi-strong | Public | Fundamental 무용 |
| Strong | All | 모든 무용 |

## §13 Anomalies

- Value premium
- Size, Momentum
- Calendar (January)
- Post-earnings drift
- Bubbles + crashes

## §14 Famous bubbles

| 연도 | Bubble | Crash |
|--|--|--|
| 1637 | Tulip | -99% |
| 1720 | South Sea | -84% |
| 1929 | US | -89% |
| 1989 | Japan | -82% |
| 2000 | Dot-com | -78% |
| 2008 | US housing | -57% |
| 2017 | Crypto | -84% |
| 2021 | SPAC meme | -90% |

## §15 Behavioral biases

| Bias | 영향 |
|--|--|
| Overconfidence | Over-trading |
| Anchoring | Initial sticky |
| Loss aversion | 손실 회피 |
| Mental accounting | Use-specific |
| Herding | 군중 따라 |
| Recency | 최근 over-weight |
| Hindsight | "그럴 줄 알았다" |

## §16 AMH (Lo 2004)

- EMH 동적
- Anomaly → exploit → fade
- Bubble → crash → learning
- Behavioral pattern systematic

## §17 12 Lessons

1. Compounding power
2. Equity long-term superior
3. Diversification reduces risk
4. Cost matters
5. Time > Timing
6. Risk tolerance ≠ capacity
7. Fat tails real
8. Mean reversion
9. Behavioral biases hurt
10. Asset allocation > Stock picking
11. Sequence risk
12. Adaptive markets

## §18 Survivorship bias

- Fund failures excluded
- True underperformance under-estimated
- Active fund net alpha ~ 0

## §19 자주 함정

| 함정 | 정정 |
|--|--|
| Past = future | Baseline only |
| Arith = compound | Geometric for long |
| Normal = reality | Fat tail |
| EMH 강신뢰 | Adaptive |
| Recent over-weight | Mean revert |
| Stock 항상 win | Japan 1989-2024 |
| Risk = volatility | Permanent loss |
| Diversification 충분 | Crisis correlation ↑ |

## §20 Quotes

- *Buffett*: "Fearful when greedy."
- *Bogle*: "Time is friend; impulse enemy."
- *Munger*: "Big money in waiting."
- *Taleb*: "Don't be fooled by randomness."

## §21 핵심 mindmap

```
Market History
├── Returns (US 1926-2024)
├── Risk (Var, Std, Sharpe)
├── Mean (Arith vs Geom)
├── Distribution
│   ├── Normal approximate
│   └── Fat tails real
├── EMH
│   ├── Weak/Semi/Strong
│   └── Adaptive (Lo)
└── Behavioral
    ├── Biases
    ├── Bubbles
    └── 12 lessons
```

## §22 1-line summary

> **Market history = empirical foundation. Stock long-term outperform (real ~7%), ERP ~8% historical, ~4-5% forward. Arithmetic vs geometric — volatility drag. Normal approximate, fat tail real. EMH 3 forms — adaptive markets. Behavioral biases + bubbles recurring. Compounding + diversification + cost + long horizon = long-term wealth.**
