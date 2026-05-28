# Chapter 17: Capital Structure — Limits to the Use of Debt — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 17** (책 p.534~568).
> 17장은 *Trade-off Theory* — bankruptcy + agency cost 가 debt 사용의 *upper limit*. MM 의 *real-world adjustment*.

이 장의 *지적 무게중심*:
1. **Costs of Financial Distress** — direct + indirect
2. **Agency Costs of Debt + Equity**
3. **Pecking Order Theory**
4. **Trade-off Theory** — optimal D/E
5. **Personal Taxes** (Miller 1977)
6. **Industry + Firm patterns**

---

## §1 Costs of Financial Distress

### §1.1 Direct costs

- Legal fees, court, accountants, advisors, restructuring
- Typical: **3-5% of asset value**

### §1.2 Indirect costs (much larger)

- Customer loss, employee departure, supplier credit
- Lost growth, management distraction, brand damage
- Typical: **10-25% of firm value**

### §1.3 Financial distress vs Bankruptcy

- *Financial distress*: difficulty meeting obligations
- *Bankruptcy*: formal proceedings
  - Chapter 7: Liquidation
  - Chapter 11: Reorganization

### §1.4 Famous examples

- Enron 2001: $66B → bankruptcy, $1B legal
- Lehman 2008: $639B assets, longest bankruptcy
- Hertz 2020: $19B debt, COVID
- Toys R Us 2017: PE leverage + Amazon
- Boeing 737 MAX 2019: $20B+ crisis cost

---

## §2 Agency Costs of Debt

### §2.1 Debt Overhang (Myers 1977)

> Excessive debt prevents positive NPV investments.

**Mechanism**:
- Positive NPV → benefits bondholders first
- Equity holders don't see upside
- Refuse to fund
- Under-investment

**예**:
- Debt $100M, project NPV $20M, equity $50M
- Most goes to bondholders (priority)
- Equity refuses

### §2.2 Asset Substitution (Risk Shifting)

> Equity holders prefer risky projects — option value.

**Mechanism**:
- Equity = option on firm value
- Higher volatility → higher option value
- Bondholders bear downside
- Equity shifts to risky

**예**:
- Debt $80M, Safe project $100M certain
- Risky: 50%×$50M + 50%×$150M = $100M expected
- Same E[V], risky preferred by equity

### §2.3 Shareholder Wealth Transfer

- Asset sale → equity
- Surprise dividend → debt loses
- LBO leverage increase → existing debt deteriorates

### §2.4 Bond Covenants

**Negative**: D/E limit, dividend restriction, asset sale, M&A approval.
**Positive**: Reporting, maintain ratios.

---

## §3 Agency Costs of Equity (Jensen 1986)

### §3.1 Free Cash Flow Hypothesis

> Excessive FCF → manager empire building.

**Mechanism**:
- Manager private benefits (perks, comp, prestige)
- Empire building (negative NPV M&A)
- Reluctance to return cash

### §3.2 Debt as discipline

- Forces cash distribution
- Reduces FCF
- Limits manager discretion
- Disciplines spending

**Examples**: LBO operational efficiency, activist push for buyback.

### §3.3 Stock-based compensation

- Align manager + shareholder
- Tech firm dominant
- Stock option, RSU

---

## §4 Trade-off Theory

### §4.1 Statement

> Optimal D/E balances tax shield + bankruptcy + agency cost.

$$V_L = V_U + PV(TS) - PV(Distress) - PV(Agency)$$

### §4.2 Optimal D/E

> Marginal tax shield = Marginal distress + agency cost.

```
V_L
  |                  ⌒  Maximum
  |               /     \
  |            /         \
  V_U-/                    \
  |                          \
  |________________________ D/E
              Optimal
```

### §4.3 Static vs Dynamic

**Static**: Single optimal D/E, cross-sectional.
**Dynamic**: Time-varying, adjustment costs, mean reversion.

### §4.4 Industry patterns

| Industry | D/E | Rationale |
|--|--|--|
| Utility | High | Stable, low distress cost |
| Bank | Very high | Regulated, deposit funding |
| Tech | Low | Growth, intangible assets |
| Pharma | Low-Mid | R&D risk, volatile |
| Real estate | High | Tangible collateral |
| Mining | Mid | Cyclical, commodity risk |

---

## §5 Pecking Order Theory (Myers-Majluf 1984)

### §5.1 Statement

> Financing preference:
> 1. Internal funds
> 2. Debt
> 3. Equity

### §5.2 Why

**Info asymmetry**: Manager has private info, investor doesn't.

**Equity signal**: Issue when overvalued → negative signal → stock falls ~3%.

**Debt signal**: Less sensitive to mispricing.

**Internal**: No signal.

### §5.3 Empirical evidence

- Profitable firms use less debt (counter trade-off)
- External financing follows bad earnings
- Equity issues depress stock ~3%

### §5.4 Pecking Order vs Trade-off

| | Trade-off | Pecking Order |
|--|--|--|
| Optimal D/E | Yes (specific) | No (path-dependent) |
| Profitability + debt | Positive | Negative |
| Empirical fit | Cross-sectional | Time-series |

### §5.5 Modern view

- Both theories partial explanation
- Trade-off: long-run cross-sectional
- Pecking order: short-run decision
- Behavioral + market timing additional

---

## §6 Personal Taxes (Miller 1977)

### §6.1 Critique

> Personal taxes on interest reduce effective shield.

**Logic**:
- Interest fully taxed (personal income)
- Equity returns preferential (capital gain)
- Net debt advantage smaller

### §6.2 Miller's formula

$$Net\ Advantage = 1 - \frac{(1 - T_c)(1 - T_E)}{(1 - T_B)}$$

**Example**:
- T_c = 21%, T_B = 37%, T_E = 20%
- Net advantage: 1 - (0.79 × 0.80)/0.63 = 1 - 1.003 = -0.3%

→ Almost zero in some cases.

### §6.3 Reality (2024)

- Top T_B ~37%
- T_c ~21%
- LTCG ~20%
- Net advantage ~5-10% (still positive)

---

## §7 Industry + Firm Patterns

### §7.1 Determinants

**Firm-specific**:
- Profitability (Pecking: more profit → less debt)
- Asset tangibility (collateral → more debt)
- Growth (less debt for growth)
- Size (large → more debt access)
- Volatility (less debt if volatile)
- Non-debt tax shields (depreciation, R&D)

**Industry**: Asset specificity, cyclicality, regulatory.

**Country**: Legal system (La Porta), tax, bank vs capital market, cultural.

### §7.2 Frank-Goyal (2009) findings

Most reliable determinants:
1. Industry median (mean reversion)
2. Tangibility
3. Profitability
4. Firm size
5. Expected inflation
6. Market-to-book

### §7.3 Cyclical

- Boom: more debt (asset value, low cost)
- Bust: deleverage (covenants, refinancing)

### §7.4 Country differences (Rajan-Zingales 1995)

| Country | Mean Debt Ratio |
|--|--|
| US | 0.27 |
| Japan | 0.29 |
| Germany | 0.16 |
| France | 0.18 |
| Italy | 0.27 |
| UK | 0.18 |
| Canada | 0.32 |

---

## §8 Modern Issues

### §8.1 Stock-based compensation

- Dilution concern
- Buyback offset (Apple $90B/year)
- Accounting complexity

### §8.2 Hybrid securities

- Convertible bonds
- Mezzanine debt
- Preferred stock
- Subordinated debentures

### §8.3 Operating leases (post-ASC 842, 2019)

- On balance sheet (US GAAP)
- Debt-like
- Higher reported leverage

### §8.4 Pension obligations

- Defined benefit long-term debt-like
- Underfunded — corporate liability
- PBGC (US) insurance

### §8.5 Climate transition

- Stranded assets (fossil fuel)
- Green bonds
- Transition risk — covenant impact

### §8.6 Behavioral

- Managerial overconfidence — too much debt
- Catering — investor preferences
- Market timing — exploit mispricing

---

## §9 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | More debt = more value | Bankruptcy limits |
| 2 | Pecking = trade-off equivalent | Different theory |
| 3 | Bankruptcy = direct only | Indirect 10-25% larger |
| 4 | Free cash flow good | Jensen — discipline 부족 |
| 5 | Debt overhang theoretical | Empirically significant |
| 6 | Single optimal D/E | Industry + firm + cycle |
| 7 | Personal taxes 무시 | Miller — reduces shield |
| 8 | Static analysis | Dynamic mean reversion |

---

## §10 자가점검

1. *Direct vs Indirect* bankruptcy?
2. *Debt overhang + Asset substitution*?
3. *Jensen's free cash flow*?
4. *Trade-off equation*?
5. *Pecking Order + order*?
6. *Miller's personal tax*?
7. *Industry patterns*?

<details><summary>해답</summary>

1. Direct 3-5%, Indirect 10-25%.
2. Debt overhang: under-investment. Asset substitution: equity risk shifting.
3. Excessive FCF → empire building. Debt as discipline.
4. $V_L = V_U + PV(TS) - PV(Distress) - PV(Agency)$.
5. Internal → Debt → Equity. Info asymmetry.
6. Personal interest tax reduces effective shield.
7. Utility/Bank/Real estate high (stable, collateral). Tech/Pharma low (growth, intangible).

</details>

---

## §11 다음 학습으로

- **Ch 18** — APV
- **Ch 19** — Dividends
- **Ch 20** — Raising capital

---

## §12 한 줄 요약

> **Trade-off Theory: optimal D/E balances *tax shield* + *bankruptcy + agency cost*. *Direct* 3-5%, *indirect* 10-25%. *Debt overhang* + *asset substitution* + *free cash flow* (Jensen) — agency. *Pecking Order* (Myers-Majluf): internal → debt → equity, info asymmetry. *Miller* — personal tax reduces shield. *Industry + firm + cycle* specific. *Modern* — SBC, hybrids, leases, pensions, climate, behavioral.**
