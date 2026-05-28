# Ch 9 Stock Valuation — 치트시트

> DDM / Gordon / Multi-stage / P/E / FCF.

## §1 DDM 기본

$$P_0 = \sum_{t=1}^{\infty} \frac{D_t}{(1+R)^t}$$

## §2 Return decomposition

$$R = \frac{D_1}{P_0} + g$$

= Dividend yield + Capital gain.

## §3 Zero growth (Perpetuity)

$$P_0 = \frac{D}{R}$$

→ Preferred stock.

## §4 Constant growth (Gordon)

$$P_0 = \frac{D_1}{R - g}, \quad R > g$$

## §5 Price trajectory

$$P_t = P_0 (1+g)^t$$

→ Price grows at g.

## §6 Sustainable growth

$$g = ROE \times b$$

- b = retention ratio (1 − payout)

## §7 Multi-stage 2-stage

$$P_0 = \sum_{t=1}^{T} \frac{D_t}{(1+R)^t} + \frac{D_{T+1}/(R-g_2)}{(1+R)^T}$$

## §8 Multi-stage 3-stage

```
Stage 1 (1-5): High (20-30%)
Stage 2 (6-10): Transition (declining)
Stage 3 (11+): Stable (3-5%)
```

## §9 R estimation 4 method

| Method | 공식 |
|--|--|
| CAPM | R_f + β(R_M - R_f) |
| DDM reversed | D_1/P_0 + g |
| Historical | Stock historical |
| Build-up | R_f + ERP + Size + Industry |

## §10 Implied growth (reverse DCF)

$$g_{implied} = R - D_1/P_0$$

→ 시장 implied — reality check.

## §11 P/E ratio

$$P/E = \frac{P}{EPS}$$

## §12 Justified P/E from Gordon

$$P/E = \frac{1-b}{R-g}$$

→ P/E ↑ when payout ↑, R ↓, g ↑.

## §13 PEG Ratio

$$PEG = \frac{P/E}{g}$$

- < 1: undervalued
- = 1: fair (Peter Lynch)
- > 1: overvalued

## §14 Multiples 비교

| Multiple | Use |
|--|--|
| P/E (trailing) | General |
| Forward P/E | Growth firm |
| PEG | Growth-adjusted |
| EV/EBITDA | Capital structure neutral |
| EV/Sales | Negative earnings |
| P/B | Bank, asset-heavy |
| P/S | Tech no earnings |

## §15 FCFE vs FCFF

| | 공식 |
|--|--|
| FCFE | NI + D&A - Capex - ΔNWC - net debt |
| FCFF | EBIT(1-T_c) + D&A - Capex - ΔNWC |

## §16 FCF valuation

| | 공식 |
|--|--|
| Equity (FCFE) | Σ FCFE/(1+R_e)^t |
| Firm (FCFF) | Σ FCFF/(1+WACC)^t |
| Equity from firm | Firm − Debt |

## §17 Common vs Preferred

| | Common | Preferred |
|--|--|--|
| Dividend | Variable | Fixed |
| Voting | Yes | No |
| Priority | Lowest | Above common |
| Volatility | High | Low |
| Convertible | No | Sometimes |

## §18 Total payout DDM

$$P = \frac{(D + Buyback) \times (1+g)}{R - g}$$

→ Apple 같은 buyback-heavy 적용.

## §19 Industry choice

| Industry | Primary |
|--|--|
| Mature dividend | DDM |
| Tech growth | FCFE / FCFF |
| Bank | P/B + ROE |
| Mining/Oil | NPV + commodity |
| Pharma | Multi-stage + decision tree |
| Startup | Revenue multiple, VC |

## §20 S&P 500 long-term avg

| Metric | Value |
|--|--|
| Trailing P/E | ~15-18 |
| Forward P/E | ~13-16 |
| Shiller (CAPE) | ~17 |
| Dividend yield | ~2% |
| Buyback yield | ~2% |

## §21 자주 함정

| 함정 | 정정 |
|--|--|
| Non-dividend = 0 | Future eventual payout |
| Gordon g ≥ R | Multi-stage |
| Single P/E | Industry + cycle + quality |
| Trailing only | Forward + cyclical |
| DDM only | Triangulation |
| Buyback 무시 | Total payout |
| Negative earnings P/E | EV/EBITDA, P/B, P/S |

## §22 Famous valuation cases

| Firm | 결과 |
|--|--|
| Microsoft 1986 IPO P/E 12 | $3T today |
| Cisco 2000 P/E 200 | -80% 5yr |
| Apple 2016 Buffett | 7x in 8yr |
| Tesla 2020-24 | $50→$1200→$250 wild |

## §23 핵심 mindmap

```
Stock Valuation
├── DDM
│   ├── Zero growth (perpetuity)
│   ├── Gordon constant g
│   └── Multi-stage (2-3)
├── FCF
│   ├── FCFE (equity)
│   └── FCFF (firm)
├── Multiples
│   ├── P/E, Forward, PEG
│   ├── EV/EBITDA
│   └── P/B, P/S
├── R estimation
│   ├── CAPM
│   ├── DDM reversed
│   ├── Historical
│   └── Build-up
└── Triangulation
    ├── Intrinsic (DCF)
    ├── Relative (multiples)
    ├── Transaction (M&A)
    └── Sensitivity + safety margin
```

## §24 1-line summary

> **Stock = PV of dividend (DDM). Zero = perpetuity, Constant = Gordon, Multi-stage = 2-3 stage. Return = dividend yield + g. *Sustainable g* = ROE × b. *P/E* = (1-b)/(R-g). *FCFE* (equity) vs *FCFF* (firm). *Triangulation* (DDM + FCF + P/E + comparable) modern best practice.**
