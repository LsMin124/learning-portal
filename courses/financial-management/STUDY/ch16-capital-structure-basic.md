# Chapter 16: Capital Structure — Basic Concepts — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 16** (책 p.504~533).
> 16장은 *Modigliani-Miller (MM)* — capital structure irrelevance + tax shield value. *재무의 가장 유명한 이론*.

이 장의 *지적 무게중심*:
1. **MM Prop I (no tax)** — capital structure irrelevant
2. **MM Prop II (no tax)** — cost of equity rises with leverage
3. **MM Prop I + Tax** — V_L = V_U + T_c × D
4. **MM Prop II + Tax** — cost of equity formula
5. **Pie Model**

---

## §1 The Capital Structure Question

### §1.1 Question

> *Does capital structure matter*?
> *Optimal D/E ratio*?

### §1.2 Two extreme views

**MM (1958)**: Irrelevant (no tax, frictions).
**Real**: Tax shield favors debt, bankruptcy cost limits — Trade-off (Ch 17).

### §1.3 Value of firm

$$V = E + D$$

---

## §2 MM Proposition I (No Tax)

### §2.1 Statement

$$V_L = V_U$$

→ *Firm value independent of capital structure*.

### §2.2 Arbitrage proof

**Setup**: Two firms identical operations, different structure.

**Case 1: V_L > V_U**:
- Sell L equity, buy U equity + personal borrow (homemade leverage)
- Same risk, lower cost → arbitrage

**Case 2: V_L < V_U**:
- Sell U equity, buy L equity + debt (homemade unlever)
- Arbitrage

→ Equilibrium V_L = V_U.

### §2.3 Strong Assumptions

1. No taxes
2. No transaction costs
3. No bankruptcy costs
4. Individuals borrow at firm rate
5. No info asymmetry
6. Cash flow unaffected by structure

### §2.4 Implications

- Capital structure doesn't matter
- WACC constant
- Risk shifted between equity + debt holders

---

## §3 MM Proposition II (No Tax)

### §3.1 Statement

$$R_E = R_0 + (R_0 - R_D) \frac{D}{E}$$

→ *Cost of equity rises with leverage*.

### §3.2 Derivation

From WACC = R_0:
$$R_0 = \frac{E}{V} R_E + \frac{D}{V} R_D$$

Solve for R_E.

### §3.3 Intuition

- More debt → equity 더 risky (residual claim)
- Higher equity risk → higher required return
- Total risk constant, only shifted

### §3.4 예

$R_0 = 12\%$, $R_D = 6\%$:

| D/E | R_E |
|--|--|
| 0 | 12% |
| 0.5 | 15% |
| 1.0 | 18% |
| 2.0 | 24% |
| 5.0 | 42% |

### §3.5 WACC constant

| D/E | E/V | D/V | R_E | R_D | WACC |
|--|--|--|--|--|--|
| 0 | 100% | 0% | 12% | — | 12% |
| 1 | 50% | 50% | 18% | 6% | 12% |
| 2 | 33% | 67% | 24% | 6% | 12% |

→ WACC = constant at R_0 ✓ MM I confirmed.

---

## §4 Pie Model (No Tax)

> Firm value = fixed pie. Capital structure = how to slice.

```
   ┌─────────┐
   │ Equity  │
V= │ ........│
   │ Debt    │
   └─────────┘
```

→ Slicing doesn't change total.

---

## §5 MM Proposition I (With Corporate Taxes)

### §5.1 Statement

$$V_L = V_U + T_c \times D$$

→ *Firm value increases with leverage due to tax shield*.

### §5.2 Why

- Interest tax-deductible
- Reduces tax → more cash to investors
- Equity + Debt holder total ↑
- Government 부담 ↓

### §5.3 Tax shield (perpetual debt)

- Annual: $D \times R_D \times T_c$
- PV (discount at R_D):

$$PV(TS) = \frac{D \times R_D \times T_c}{R_D} = T_c \times D$$

### §5.4 예

V_U = $1000M, D = $400M, T_c = 25%.

$$V_L = 1000 + 0.25 \times 400 = \$1100M$$

→ Leverage 가 $100M 가치 추가.

### §5.5 Implications

- More debt → more tax shield → more value
- Extreme: 100% debt = max value
- Real: bankruptcy cost limits (Ch 17)

---

## §6 MM Proposition II (With Taxes)

### §6.1 Cost of equity

$$R_E = R_0 + (R_0 - R_D)(1 - T_c) \frac{D}{E}$$

→ Tax shield reduces rate of increase.

### §6.2 WACC

$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1 - T_c)$$

→ After-tax R_D.

### §6.3 WACC decreases with leverage

| D/E | E/V | D/V | R_E | After-tax R_D | WACC |
|--|--|--|--|--|--|
| 0 | 100% | 0% | 12% | — | 12% |
| 1 | 50% | 50% | 16.5% | 4.5% | 10.5% |
| 2 | 33% | 67% | 21% | 4.5% | 10% |
| 5 | 17% | 83% | 39% | 4.5% | ~10% asymp |

→ WACC ↓ with leverage (tax benefit).

### §6.4 Optimal

- Pure MM tax: 100% debt = lowest WACC
- Real world: trade-off with bankruptcy (Ch 17)

---

## §7 Pie Model (With Taxes)

> Tax = government slice. More debt → smaller gov slice.

```
No leverage:                With leverage:
┌──────────┐                ┌──────────┐
│ Equity   │                │ Equity   │
│ 75%      │                │ 60%      │
│ ........ │                │ ........ │
│ Tax 25%  │                │ Debt 30% │
└──────────┘                │ Tax 10%  │
                            └──────────┘
```

---

## §8 Levered vs Unlevered β

### §8.1 Levered β

> Observed equity β.

$$\beta_L$$

### §8.2 Unlevered β (Asset β)

> Business risk only, no leverage.

$$\beta_U = \frac{\beta_L}{1 + (1 - T_c) D/E}$$

### §8.3 Re-lever

$$\beta_L = \beta_U [1 + (1 - T_c) D/E]$$

### §8.4 Use case — Bottom-up β

1. Industry peers β_L
2. Unlever each → β_U
3. Average β_U
4. Re-lever for target D/E

---

## §9 MM Contributions

### §9.1 Nobel Prize

- Modigliani (1985) — economics
- Miller (1990) — finance

### §9.2 Why important

- First rigorous theory
- Identifies frictions
- Benchmark for real-world

### §9.3 Real-world deviations

- Tax shield
- Bankruptcy cost (Ch 17)
- Agency cost (Ch 17)
- Info asymmetry (Pecking order)
- Behavioral

### §9.4 MM as null hypothesis

> *Any capital structure effect* must violate one of MM assumptions.

→ Identifies *where* friction matters.

---

## §10 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | MM = always true | Strong assumptions |
| 2 | Capital structure irrelevant | Only without frictions |
| 3 | Debt 항상 cheaper | After-tax only |
| 4 | More debt = more value | Bankruptcy limits (Ch 17) |
| 5 | WACC unchanging | Only without frictions |
| 6 | Equity cost constant | Rises (Prop II) |
| 7 | 100% debt optimal | Pure MM tax only |
| 8 | Pie size constant | Tax shield grows |

---

## §11 자가점검

1. *MM Prop I (no tax)*?
2. *MM Prop II (no tax)*?
3. *MM with tax* — firm value?
4. *WACC with leverage* (with tax)?
5. *Levered vs Unlevered β*?
6. *MM benchmark*?

<details><summary>해답</summary>

1. $V_L = V_U$.
2. $R_E = R_0 + (R_0 - R_D) D/E$.
3. $V_L = V_U + T_c D$.
4. WACC ↓ with leverage. Pure MM 100% debt = lowest.
5. $\beta_U = \beta_L / [1 + (1-T_c) D/E]$.
6. Null hypothesis. Any effect must violate MM. Identifies where friction matters.

</details>

---

## §12 다음 학습으로

- **Ch 17** — Capital structure limits
- **Ch 18** — APV
- **Ch 19** — Dividends

---

## §13 한 줄 요약

> **Modigliani-Miller — capital structure irrelevance (Prop I, no tax). Cost of equity rises with leverage (Prop II). MM with corporate tax — $V_L = V_U + T_c \times D$ — tax shield adds value. *WACC decreases with leverage* (tax benefit). *Levered vs unlevered β*. *MM as benchmark*. *Real deviations* — tax, bankruptcy, agency, info, behavioral.**
