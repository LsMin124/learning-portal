# Ch 13 Cost of Capital — 치트시트

> R_E / R_D / WACC / Project-specific / Country risk.

## §1 Cost of Equity — 3 methods

| Method | 공식 |
|--|--|
| CAPM | $R_f + \beta(R_M-R_f)$ |
| DDM | $D_1/P_0 + g$ |
| Build-up | $R_f + ERP + Size + Industry + Firm$ |

## §2 Cost of Debt

$$R_D = YTM$$

→ Current market, not coupon.

## §3 After-tax R_D

$$R_D^{after-tax} = R_D (1 - T_c)$$

## §4 WACC

$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1 - T_c)$$

## §5 With Preferred

$$+ \frac{P}{V} R_P$$

## §6 Book vs Market

| | Book | Market |
|--|--|--|
| Source | Accounting | Current price |
| Forward | No | Yes |
| Practice | Avoid | Standard |

## §7 Tax Shield

$$Annual: D \times R_D \times T_c$$

$$PV(perpetuity): T_c \times D$$

## §8 Project-specific methods

| Method | When |
|--|--|
| Pure-play | Industry analog |
| Divisional | Multi-segment |
| Subjective | Above/below avg ±2-5% |
| Bottom-up β | Industry peer |

## §9 Bottom-up β (Damodaran)

1. Peers identify
2. β_L 계산
3. Unlever: $\beta_U = \beta_L / [1 + (1-T_c) D/E]$
4. Average β_U
5. Re-lever target

## §10 Country Risk Premium

$$CRP = Sovereign\ Spread \times \frac{\sigma_{stocks}}{\sigma_{bonds}}$$

$$R_E = R_f + \beta(ERP) + CRP$$

## §11 Country premia (S&P)

| Rating | CRP |
|--|--|
| AAA | 0% |
| AA | 0.5% |
| A | 1.0% |
| BBB | 2.0% |
| BB | 3.5% |
| B | 5% |
| CCC | 8% |
| D | 15%+ |

## §12 β estimation

| Approach | Method |
|--|--|
| Standard | 5yr monthly regression |
| Bloomberg | Bayesian smooth |
| Industry | Damodaran |
| Bottom-up | Peers + capital structure |

## §13 ERP

| Method | Value (2024) |
|--|--|
| Historical | ~8% |
| Implied | ~4-5% |
| Survey | ~5-7% |

## §14 Industry WACC (2024)

| Industry | WACC |
|--|--|
| Utility | 5-7% |
| Mature tech | 8-10% |
| Industrial | 9-12% |
| Growth tech | 11-14% |
| Pharma | 9-12% |
| Bank | 8-11% |
| EM | 12-20% |

## §15 EVA

$$EVA = NOPAT - WACC \times IC$$

## §16 자주 함정

| 함정 | 정정 |
|--|--|
| Book weights | Market |
| Coupon = R_D | YTM |
| Single β | Bayesian smooth |
| Firm WACC all | Project-specific |
| Tax shield 무시 | After-tax R_D |
| Historical ERP only | Forward + range |
| No country risk | EM CRP |
| WACC unchanging | Time-varying |
| T-bill for long | LT Treasury |

## §17 Modern best practice (10)

1. Multiple methods R_E
2. Bottom-up β
3. Implied ERP forward
4. Market weights
5. Project-specific
6. Country risk EM
7. Sensitivity range
8. Annual reassessment
9. Post-audit feedback
10. Real options + multi-factor

## §18 Applications

| App | Use |
|--|--|
| Capital budgeting | NPV discount |
| DCF valuation | FCFF discount |
| EVA | Performance |
| Capital structure | WACC minimization |

## §19 Sensitivity report

```
Base: 10%
Low: 9% (lower β, ERP)
High: 11% (higher β, ERP)
NPV at each: range
```

## §20 Quotes

- *Damodaran*: "WACC at best estimate."
- *Buffett*: "I don't use WACC. I use opportunity cost."
- *Munger*: "Hurdle rate = best alternative."

## §21 핵심 mindmap

```
Cost of Capital
├── Cost of Equity (CAPM/DDM/Build-up)
├── Cost of Debt (YTM after-tax)
├── Weights (Market preferred)
├── WACC formula + tax shield
├── Project-specific
│   ├── Pure-play
│   ├── Divisional
│   ├── Subjective
│   └── Bottom-up β
├── International (CRP, currency)
└── Modern (sensitivity, real options, AI)
```

## §22 1-line summary

> **WACC = *capital budgeting + valuation* 결정 input. *Cost of equity* (CAPM/DDM/build-up) + *cost of debt* (YTM after-tax). *Market weights*. *Tax shield* = $T_c \times D$. *Project-specific* — pure-play, divisional, subjective, bottom-up. *Country risk* — EM. *β, ERP* critical. *Sensitivity range* mandatory.**
