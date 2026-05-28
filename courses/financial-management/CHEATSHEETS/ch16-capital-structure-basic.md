# Ch 16 Capital Structure: Basic — 치트시트

> MM Theorem / Tax shield / Pie Model / β.

## §1 MM Prop I (no tax)

$$V_L = V_U$$

## §2 MM Prop II (no tax)

$$R_E = R_0 + (R_0 - R_D) \frac{D}{E}$$

## §3 WACC (no tax)

$$WACC = (E/V) R_E + (D/V) R_D = R_0$$

→ Constant.

## §4 MM Assumptions

1. No taxes
2. No transaction costs
3. No bankruptcy
4. Individual borrow at firm rate
5. No info asymmetry
6. Cash flow unaffected

## §5 MM Prop I (with tax)

$$V_L = V_U + T_c \times D$$

## §6 Tax Shield

| | 공식 |
|--|--|
| Annual | $D \times R_D \times T_c$ |
| PV (perpetuity) | $T_c \times D$ |

## §7 MM Prop II (with tax)

$$R_E = R_0 + (R_0 - R_D)(1 - T_c) \frac{D}{E}$$

## §8 WACC (with tax)

$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1 - T_c)$$

→ ↓ with leverage.

## §9 Pure MM Tax Optimal

- 100% debt = lowest WACC
- Real: bankruptcy + agency limits

## §10 β

$$\beta_U = \frac{\beta_L}{1 + (1 - T_c) D/E}$$

$$\beta_L = \beta_U [1 + (1 - T_c) D/E]$$

## §11 Bottom-up β

1. Industry peers β_L
2. Each unlever → β_U
3. Average β_U
4. Re-lever target

## §12 Pie Model

```
No tax: fixed pie
With tax: pie grows (less gov slice)
```

## §13 Real-world Deviations

| Friction | Effect |
|--|--|
| Tax shield | V ↑ with debt |
| Bankruptcy (Ch 17) | V ↓ high leverage |
| Agency | Debt overhang, asset sub |
| Info (Pecking order) | Internal > Debt > Equity |
| Personal tax (Miller) | Reduces shield |
| Behavioral | Overconfidence |

## §14 Industry D/E

| Industry | D/E |
|--|--|
| Tech | 0-0.5 |
| Pharma | 0.3-0.8 |
| Utility | 1.5-2.5 |
| Real estate | 2-4 |
| Bank | 10+ (regulated) |

## §15 Trade-off Theory (Ch 17)

- Optimal D/E: marginal tax shield = marginal bankruptcy
- Industry + firm + cycle specific

## §16 Pecking Order (Myers-Majluf 1984)

1. Internal first
2. Debt next
3. Equity last

## §17 Empirical

- Frank-Goyal (2009): industry, profitability, tangibility, size
- DeAngelo (2006): trade-off poor explanatory
- Strebulaev (2007): dynamic mean reversion

## §18 Famous bad leverage

| Firm | Year | Result |
|--|--|--|
| LTCM | 1998 | 30x → $4.6B loss |
| Lehman | 2008 | 30x → bankruptcy |
| LBOs | 1980s-2000s | Distress |
| Boeing | 2020-22 | $50B+ COVID debt |

## §19 자주 함정

| 함정 | 정정 |
|--|--|
| MM = always true | Strong assumptions |
| Capital structure irrelevant | Only without frictions |
| Debt 항상 cheaper | After-tax only |
| More debt = more value | Bankruptcy limits |
| WACC unchanging | Only without frictions |
| Equity cost constant | Rises |
| 100% debt optimal | Pure MM only |
| Pie size constant | Tax shield grows |

## §20 Quotes

- *Buffett*: "Leverage is dangerous. Don't use much."
- *Miller*: "Pie size grows with tax"
- *Damodaran*: "MM = null hypothesis, not destination"

## §21 핵심 mindmap

```
Capital Structure: Basic (MM)
├── MM Prop I + II (no tax)
├── MM with tax (V_L = V_U + T_c D)
├── WACC formula
├── Pie Model
├── β (levered/unlevered, bottom-up)
└── Real deviations
```

## §22 1-line summary

> **MM Theorem — capital structure irrelevance (Prop I, no tax). Cost of equity rises with leverage (Prop II). MM with tax — $V_L = V_U + T_c D$. WACC decreases with leverage. Levered/unlevered β. Real deviations — tax, bankruptcy, agency, info, behavioral.**
