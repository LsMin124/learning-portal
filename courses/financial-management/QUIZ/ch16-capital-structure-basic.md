# Ch 16 Capital Structure: Basic — 퀴즈

> 10 문항 (개념 3 / 계산 5 / 디버그 1 / 면접 1).

### Q1. *MM Prop I* (no tax)?

<details><summary>답</summary>

$$V_L = V_U$$

**Proof** (arbitrage):
- V_L > V_U: homemade leverage → arbitrage
- V_L < V_U: homemade unlever → arbitrage
- Equilibrium

**Assumptions** (strong):
1. No taxes
2. No transaction costs
3. No bankruptcy
4. Individual borrow at firm rate
5. No info asymmetry
6. Cash flow unaffected

**Implications**:
- WACC constant
- Risk shifted
- Capital structure doesn't matter

</details>

### Q2. *MM Prop II* (no tax)?

<details><summary>답</summary>

$$R_E = R_0 + (R_0 - R_D) \frac{D}{E}$$

**Intuition**:
- More debt → equity riskier
- Higher return required
- Total risk constant, shifted

**WACC = constant** at R_0.

</details>

### Q3. *MM with tax*?

<details><summary>답</summary>

**Prop I**:
$$V_L = V_U + T_c \times D$$

**Tax shield**:
- Annual: D × R_D × T_c
- PV (perpetuity): T_c × D

**Prop II**:
$$R_E = R_0 + (R_0 - R_D)(1-T_c) \frac{D}{E}$$

**WACC**:
$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1-T_c)$$

→ WACC ↓ with leverage.

**Pure MM tax**: 100% debt = max value.
**Real**: bankruptcy + agency limits.

</details>

### Q4. 계산 — MM Prop II (no tax)

$R_0 = 14\%$, $R_D = 7\%$.

D/E별 R_E?

<details><summary>답</summary>

$$R_E = 14 + 7 \times D/E$$

| D/E | R_E |
|--|--|
| 0 | 14% |
| 0.5 | 17.5% |
| 1 | 21% |
| 2 | 28% |
| 5 | 49% |

**WACC** (D/E=1): 0.5(21) + 0.5(7) = 14% = R_0 ✓

</details>

### Q5. 계산 — V_L with tax

V_U = $800M, D = $300M, T_c = 21%.

<details><summary>답</summary>

**Tax shield**: 0.21 × 300 = **$63M**

**V_L**: 800 + 63 = **$863M**

**Equity**: 863 - 300 = **$563M**

**Comparison**:
- Unlevered: $800M (all equity)
- Levered: $863M = $300M debt + $563M equity
- *Tax shield $63M → equity holders*

**Equity perspective**:
- Unlevered: $800M (own all)
- Levered: $563M (own less, levered)
- Net gain: $63M from tax shield

</details>

### Q6. 계산 — MM Prop II (with tax)

$R_0 = 14\%$, $R_D = 7\%$, T_c = 21%.

D/E별 R_E, WACC?

<details><summary>답</summary>

$$R_E = 14 + 7 \times 0.79 \times D/E$$

| D/E | R_E | After-tax R_D | E/V | D/V | WACC |
|--|--|--|--|--|--|
| 0 | 14% | — | 100% | 0% | 14% |
| 0.5 | 16.77% | 5.53% | 67% | 33% | 12.99% |
| 1 | 19.53% | 5.53% | 50% | 50% | 12.53% |
| 2 | 25.06% | 5.53% | 33% | 67% | 12.05% |
| 5 | 41.65% | 5.53% | 17% | 83% | 11.66% |

→ WACC ↓ with leverage. Pure MM tax: 100% debt = lowest.

**Real**: Bankruptcy + agency cap (Ch 17).

</details>

### Q7. 계산 — Levered vs Unlevered β

β_L = 1.8, D/E = 0.6, T_c = 21%.

(a) β_U?
(b) D/E target = 1 의 β_L?
(c) WACC (R_f = 4%, ERP = 6%, R_D = 6%)?

<details><summary>답</summary>

**(a)** $\beta_U = 1.8 / (1 + 0.79 \times 0.6) = 1.8/1.474 = \mathbf{1.22}$

**(b)** β_L (D/E=1) = 1.22 × (1 + 0.79 × 1) = 1.22 × 1.79 = **2.18**

**(c)** WACC:
- R_E = 4 + 2.18(6) = 17.08%
- E/V = 50%, D/V = 50%
- WACC = 0.5(17.08) + 0.5(6)(0.79) = **10.91%**

**Bottom-up approach**:
1. Industry peers β_L
2. Each unlever → β_U
3. Average
4. Re-lever for target

</details>

### Q8. 계산 — Maximum firm value

V_U = $500M, T_c = 21%.

(a) D = 0?
(b) D = $200M?
(c) D = $500M?
(d) Optimal?

<details><summary>답</summary>

| D | V_L | Increase |
|--|--|--|
| 0 | 500 | 0 |
| 200 | 542 | +8.4% |
| 500 | 605 | +21% |

**Pure MM tax**: 100% debt = max.

**Real-world limits**:

**1. Bankruptcy cost**: 10-25% of firm value.
**2. Agency cost**: Debt overhang, asset substitution.
**3. Personal taxes** (Miller 1977): Reduces effective shield.
**4. Info asymmetry**: Pecking order.

**Industry typical D/E**:
- Utility: 1.5-2.5
- Bank: 10+ (regulated)
- Tech: 0-0.5
- Real estate: 2-4
- Pharma: 0.3-0.8

**Trade-off Theory**: Marginal tax shield = Marginal bankruptcy cost.

</details>

### Q9. 디버그 — MM real-world break down

회사 A — D/E = 5:
- MM 예측: WACC 매우 낮음, value 높음
- 실제: 부도 직전, spread 8%, 주가 -50%

원인?

<details><summary>답</summary>

**Causes**:

**1. Bankruptcy cost**:
- Direct (법률, 회계) 3-5%
- Indirect (customer, employee, supplier) 10-25%

**2. Agency cost of debt**:
- Debt overhang (Myers 1977) — under-investment
- Asset substitution — risk shifting
- Wealth transfer

**3. Personal taxes** (Miller 1977):
- Interest fully taxed
- Equity preferential
- Reduces effective tax shield

**4. Info asymmetry** (Myers-Majluf):
- Highly leveraged signal
- *Can't issue equity*

**5. Operating effects**:
- Strict covenants limit
- Customer fear
- Supplier credit tightening
- Talent retention difficulty

**6. Market timing**:
- Vulnerable to downturn
- Refinance difficulty

**Real failures**:
- LTCM (1998): 30x leverage, Russia → $4.6B loss
- Lehman (2008): 30x → bankruptcy
- Many LBOs 1980s-2000s
- GE 2018 complexity
- Boeing 2020-22: $50B+ COVID

**Buffett**: *"Leverage is dangerous. Don't use much."*

</details>

### Q10. 면접 — MM practical relevance?

<details><summary>답</summary>

**Contributions**:

**1. Framework**: Null hypothesis, identifies frictions.

**2. Tax shield value**: V_L = V_U + T_c D — analyst standard.

**3. APV** (Ch 18): V_L = V_U + PV(Tax) - PV(Distress).

**4. WACC**: Formula derived from MM, levered/unlevered β.

**5. Capital structure decisions**: Trade-off, Pecking order, Market timing.

**Real-world modifications**:

**Tax**:
- Personal taxes (Miller 1977)
- Tax shield uncertainty (profitability)
- NOL lost shield

**Bankruptcy**:
- Direct 3-5%
- Indirect 10-25%
- Industry-specific

**Agency**:
- Debt overhang
- Asset substitution
- Free cash flow (Jensen 1986)

**Info**:
- Pecking order

**Behavioral**:
- Overconfidence
- Catering

**Industry dominant theory**:

| Industry | Theory |
|--|--|
| Mature stable | Trade-off |
| Growth tech | Pecking order |
| Distressed | Debt overhang |
| Cyclical | Market timing |
| Bank | Regulatory |

**Modern determinants**:
- Profitability (Pecking order: more profit → less debt)
- Asset tangibility
- Growth opportunities
- Size
- Volatility

**Macro**:
- Interest rate
- Equity valuation
- Tax policy

**Famous decisions**:
- Apple 2013+: leverage for buyback
- Tesla 2017-22: equity vs debt
- Boeing 2020-22: COVID debt
- Berkshire: minimal debt

**Modern issues**:
1. Stock-based comp
2. Hybrid securities
3. Operating leases
4. Pension obligations
5. Climate-linked

**Empirical**:
- Frank-Goyal (2009): industry, profitability, tangibility, size
- DeAngelo-DeAngelo (2006): trade-off poor explanatory
- Strebulaev (2007): dynamic mean reversion

> MM = foundation, not destination. *Trade-off + Pecking + Timing + Behavioral* combined. *Industry + firm + cycle* adjustment. *Buffett conservative*: don't push to optimum. *Margin of safety*.

</details>
