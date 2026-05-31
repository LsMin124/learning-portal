# Chapter 17: Capital Structure — Limits to the Use of Debt — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 17** (책 p.528~559).
> 17장은 *Trade-off Theory* — bankruptcy + agency cost 가 debt 사용의 *upper limit*. MM 의 *real-world adjustment*.

이 장의 *지적 무게중심*:
1. **Costs of Financial Distress** — direct + indirect
2. **Agency Costs of Debt + Equity**
3. **Pecking Order Theory**
4. **Trade-off Theory** — optimal D/E
5. **Personal Taxes** (Miller 1977)
6. **Industry + Firm patterns**

---

## §0 도입 — MM 의 역설에서 Trade-off 로

Ch 16 의 결론(법인세를 넣은 MM)을 곧이곧대로 받으면 *기업은 100% 부채로 가야 한다*. 이자비용이 만드는 세금방패 $T_c B$ 가 부채에 비례해 무한히 커지기 때문이다. 그러나 현실의 어떤 건전한 기업도 그렇게 하지 않는다. **무엇이 부채의 상한을 만드는가?** 가 17장의 질문이다.

답은 *파이 모델(pie model)* 로 직관화된다. 기업가치라는 파이는 주주·채권자만 나눠 갖는 게 아니다. **세금(정부)·파산비용(변호사·회계사)·소송 청구권** 같은 *비시장 청구권(nonmarketed claims)* 에도 잘려 나간다.

![Figure 17.2 — The Pie Model with Real-World Factors. 교재 p.531](/courses/financial-management/figures/ch17/fig-17-2.png)

> **직관**: 부채를 늘리면 *세금 조각(정부 몫)* 은 줄어든다 — 이것이 세금방패의 이득이다. 그러나 동시에 *파산·distress 조각* 이 커진다. 주주와 채권자가 실제로 가져가는 *시장 청구권(marketed claims)* 의 합 $V_M = V_T - (\text{세금} + \text{distress})$ 을 **최대화**하는 D/E 가 최적이다. 곧, 부채의 한계이득(세금방패)과 한계비용(distress + agency)이 같아지는 지점이다.

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

![Figure 17.1 — The Optimal Amount of Debt and the Value of the Firm. 교재 p.529](/courses/financial-management/figures/ch17/fig-17-1.png)

직선 $V_L = V_U + T_C B$ 는 distress 비용이 없을 때의 MM(법인세) 가치선 — 부채에 비례해 끝없이 상승한다. 실제 기업가치 $V$ 는 이 직선에서 *재무위기 비용의 현재가치* 만큼 아래로 휜다. **순한계이득이 0** 이 되는 부채 $B^*$ 에서 $V$ 가 최대가 되고, 그 너머에서는 가치가 하락한다.

> **직관**: 처음 얼마간의 부채는 세금방패가 distress 위험을 압도해 가치를 키운다. 그러나 부채가 커질수록 파산확률이 가속적으로 오르고, $B^*$ 를 넘으면 추가 세금방패보다 늘어나는 distress·agency 비용이 더 커져 가치가 *하락* 한다. 이 $B^*$ 가 trade-off 이론이 말하는 최적 부채다.

### §4.3 Static vs Dynamic

**Static**: Single optimal D/E, cross-sectional.
**Dynamic**: Time-varying, adjustment costs, mean reversion.

![Figure 17.5 — Survey Results on the Use of Target Debt-Equity Ratios. 교재 p.543](/courses/financial-management/figures/ch17/fig-17-5.png)

설문(392 CFO)을 보면 대다수 기업이 *목표 D/E* 를 둔다 — "very strict"(10%) + "somewhat tight"(34%) + "flexible"(37%) = 81% 가 어떤 형태로든 목표를 운용하고, "목표 없음" 은 19% 뿐이다. 곧 현실의 재무담당자는 trade-off 가 시사하는 *최적 구간* 을 의식하되, 조정비용 때문에 *유연하게* 운영한다.

![Figure 17.6 — Leverage Ratios of General Motors, IBM, and Eastman Kodak over Time. 교재 p.544](/courses/financial-management/figures/ch17/fig-17-6.png)

> **직관**: 개별 기업의 leverage 는 수십 년에 걸쳐 *평균회귀(mean reversion)* 하면서도 주가 변동에 따라 출렁인다. GM·IBM·Kodak 모두 *book* 과 *market* leverage 가 장기적으로 같은 띠 안에서 움직인다 — 목표가 존재하되 즉각 조정되지는 않는다는 *dynamic* trade-off 의 증거다.

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

![Figure 17.3 — Stock Returns at the Time of Announcements of Exchange Offers. 교재 p.533](/courses/financial-management/figures/ch17/fig-17-3.png)

> **직관**: 교환오퍼(exchange offer)는 자본구조만 바꾸는 *깨끗한 실험* 이다. *부채를 늘리는*(leverage-increasing) 발표에는 주가가 **상승**, *부채를 줄이는*(leverage-decreasing) 발표에는 **하락** 한다. 부채 증가는 경영진이 미래 현금흐름에 자신 있다는 신호로, 자기자본 증가는 주식이 고평가됐다는 신호로 읽히기 때문 — signaling·pecking order 와 정합적이다.

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

![Figure 17.4 — Median Leverage Ratio of Sample Firms in 39 Different Countries (1991–2006). 교재 p.541](/courses/financial-management/figures/ch17/fig-17-4.png)

> **직관**: 국가별 median leverage 는 한국·인도네시아·브라질 등이 높고(은행 중심·관계금융), 미국·캐나다·호주가 낮다(자본시장 발달, 주식금융 용이). *법체계(La Porta)·세제·은행 vs 자본시장* 구조가 자본구조의 국가 간 차이를 만든다. 아래 Rajan-Zingales 표는 그중 G7 의 좁은 단면이다.

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
