# Ch 17 Capital Structure Limits — 퀴즈

> 10 문항 (개념 4 / 분석 3 / 디버그 2 / 면접 1).

### Q1. *Direct vs Indirect* bankruptcy costs?

<details><summary>답</summary>

**Direct** (3-5% of assets):
- Legal fees, court, advisors, restructuring

**Indirect** (10-25% of firm value — much larger):
- Customer loss, employee departure, supplier credit
- Lost growth, management distraction, brand damage

**Famous**:
- Enron 2001: $1B legal fees
- Lehman 2008: longest bankruptcy
- Toys R Us 2017: PE leverage + Amazon
- Boeing 737 MAX 2019: $20B+ crisis

</details>

### Q2. *Agency costs of debt* (3 types)?

<details><summary>답</summary>

**1. Debt Overhang** (Myers 1977):
- Positive NPV → bondholders first
- Equity refuses → under-investment

**2. Asset Substitution**:
- Equity = option on firm value
- Higher volatility → option value ↑
- Equity shifts to risky

**3. Wealth Transfer**:
- Asset sale → equity
- Surprise dividend → debt loses
- LBO leverage → existing debt deteriorates

**Mitigation**: Bond covenants (negative + positive).

</details>

### Q3. *Jensen's Free Cash Flow*?

<details><summary>답</summary>

> Excessive FCF → manager empire building.

**Mechanism**:
- Manager private benefits
- Empire building (negative NPV M&A)
- Reluctance to return cash

**Debt as discipline**:
- Forces cash distribution
- Reduces FCF
- Limits manager discretion

**Examples**: LBO efficiency, activist push for buyback.

**Real-world**: Apple, Microsoft large buyback programs.

</details>

### Q4. *Pecking Order vs Trade-off*?

<details><summary>답</summary>

| | Trade-off | Pecking Order |
|--|--|--|
| Optimal D/E | Yes | No (path-dependent) |
| Profitability + debt | Positive | Negative |
| Empirical fit | Cross-sectional | Time-series |
| Source | Tax vs distress | Info asymmetry |
| Author | Various | Myers-Majluf 1984 |

**Pecking order**: Internal → Debt → Equity.

**Why**:
- Equity issue signal (overvalued?)
- Debt less sensitive
- Internal no signal

**Modern view**: Both partial. Trade-off long-run cross-sectional. Pecking short-run.

</details>

### Q5. 분석 — Debt overhang

회사 X:
- Existing debt $200M
- New project: NPV $30M, $80M equity
- Firm value (no project): $250M

(a) Equity fund?
(b) Bondholder enforce?

<details><summary>답</summary>

**(a) Calculation**:
- Without project: Firm $250M, Equity $50M
- With project: Firm $280M, Equity $80M
- Equity gain: $30M
- But equity invests $80M → net loss $50M
- → **Refuse to fund**

**Bondholder gain**: $30M NPV improves repayment probability.

**(b) Bondholder enforcement**:
1. Debt forgiveness
2. New investor (equity issue, dilution)
3. Acquisition
4. Bankruptcy restructuring

**Modern**:
- Distressed exchange
- Activist debt holders
- DIP financing

**Famous**: GM 2009 bondholder haircut, Greek 2012 75% haircut, Evergrande 2021-22.

</details>

### Q6. 분석 — Asset substitution

회사 Y:
- Firm $100M, debt $80M (face)
- Equity $20M

(a) Safe ($100M certain) vs Risky (50%×$50M + 50%×$150M)?
(b) Equity preference?

<details><summary>답</summary>

**(a)**:

**Safe**: Firm $100M → Debt $80M, Equity $20M.

**Risky**:
- 50% × $50M: Firm $50M < Debt → Equity $0, default
- 50% × $150M: Firm $150M → Equity $70M
- E[Equity] = 0.5 × $70M = $35M
- E[Firm] = $100M (same!)
- E[Debt] = 0.5 × $50M + 0.5 × $80M = $65M

| | Safe | Risky |
|--|--|--|
| E[Firm] | $100M | $100M |
| E[Equity] | $20M | $35M |
| E[Debt] | $80M | $65M |

**(b) Equity prefers Risky** ($35M > $20M).

→ Same E[firm], but volatility shift wealth equity ↑, debt ↓.

**Mitigation**: Covenants, collateral, monitoring.

**Famous**:
- S&L crisis 1980s
- AIG 2008 derivatives
- Distressed firms gamble for resurrection

</details>

### Q7. 분석 — Miller personal tax

T_c = 25%, T_B = 40%, T_E = 15%.

(a) Net tax advantage?
(b) Effective shield?

<details><summary>답</summary>

**(a)**:
$$1 - \frac{(0.75)(0.85)}{0.60} = 1 - 1.0625 = \mathbf{-6.25\%}$$

→ **Negative** advantage. Debt *not preferred*.

**(b)**:
- Pure corporate: T_c = 25%
- With personal: -6.25%

**Why negative**:
- Equity gain heavily favored (15%)
- Interest fully taxed (40%)
- Net: debt more taxed overall

**Implications**:
- Miller's view: capital structure partially irrelevant
- Equilibrium: debt supply meets demand
- Investor heterogeneity

**Reality (US 2024)**:
- T_c = 21%, T_B = 37%, LTCG = 20%
- Net: -0.3% (near zero)

→ Pure MM over-states benefit. Real net smaller.

**Practical**:
- Trade-off still valid
- Marginal tax shield lower
- Optimal D/E lower
- Industry variation explains rest

**Historical**:
- Pre-1986 US: T_B higher → debt less
- 2017 TCJA: T_c 35→21% → less benefit
- OECD Pillar 2: 15% min → reduce variation

</details>

### Q8. 디버그 — Industry D/E

- Utility: 2.0
- Bank: 10+
- Tech: 0.3
- Pharma: 0.5
- Real estate: 3.0

각 logic?

<details><summary>답</summary>

**Utility (2.0)**: Stable cash flow, low distress, tangible assets, long-term steady, regulator allows.

**Bank (10+)**: Regulatory min capital (Basel), deposit funding cheap, asset-liability matching, trading book, higher ROE.

**Tech (0.3)**: Intangible assets, high growth (Pecking order), volatile earnings, sufficient internal funds, no collateral.

**Pharma (0.5)**: R&D risk (Phase failure), volatile cash flow, patent cliff, long cycles.

**Real estate (3.0)**: Tangible collateral, stable rental, tax shield critical, REITs.

**Trade-off logic**:

**High D/E**: Tax shield > Distress, tangible collateral, stable cash flow, agency discipline.

**Low D/E**: Distress > Tax shield, intangible, volatile, growth (Pecking).

**Cyclical**:
- Boom: D/E rises
- Bust: deleverage forced
- 2008 financial crisis: Bank D/E 20+ → 12 (Dodd-Frank)
- COVID 2020: many firms increase debt for survival

**Modern trends**:
- Tech: high cash + buyback
- Bank: stricter Basel III/IV
- Real estate: REIT leverage steady
- Pharma: more M&A debt
- Crypto: experimental

</details>

### Q9. 디버그 — Distressed decisions

회사 Z — spread 8% (junk), $200M debt maturity 1년.

4 options: Sell assets / Issue equity / Restructure / Continue normal.

추천?

<details><summary>답</summary>

**Decision framework**:

**A. Asset sale**:
- Pros: Quick liquidity
- Cons: Below-market (distress discount), permanent loss
- Best: Asset sufficient + non-core

**B. Equity issue**:
- Pros: De-leverage, future flexibility
- Cons: 30% dilution (discounted), bad timing, negative signal
- Best: Equity market receptive, long-term

**C. Debt restructuring**:
- Pros: Reduce debt burden, preserve firm
- Cons: Credit rating destroyed, legal complexity
- Best: Debt holders cooperative

**D. Continue normal**:
- Pros: Preserve options
- Cons: Default risk at maturity, deteriorating credit
- Best: Strong recovery expected, short timeline

**Decision tree**:
1. Cash flow projection — recover?
   - Yes → A or D
   - No → B or C
2. Asset quality — sellable?
   - Yes → A
   - No → C
3. Market conditions — equity feasible?
   - Yes → B
   - No → C

**Best**: Often combination.

**Famous**:
- Chrysler 2009: Bailout + bankruptcy + Fiat
- GM 2009: Conservatorship → restructured
- Westinghouse: Toshiba subsidiary, $9B losses
- WeWork: SoftBank rescue + IPO failure
- Hertz 2020: COVID bankruptcy → emerged 2021

**Lessons**:
1. Early action > waiting
2. Multi-track exploration
3. Experienced advisor
4. Stakeholder management
5. Preserve value of viable
6. Cut losses of non-viable

**Modern tools**: Distressed exchange, DIP financing, pre-pack bankruptcy, Section 363, plan support agreement.

</details>

### Q10. 면접 — Modern optimal capital structure framework?

<details><summary>답</summary>

**Multi-theory framework**:

**1. Trade-off** (Static): Tax shield vs Distress + Agency.
**2. Pecking Order** (Dynamic): Info asymmetry, internal→debt→equity.
**3. Market Timing**: Issue equity overvalued, debt at low rates.
**4. Agency (Jensen)**: Debt as discipline for FCF.
**5. Behavioral**: Overconfidence, catering.
**6. Macro/Regime**: Rate, recession risk.

**Practical steps**:

1. **Industry benchmark** — peer, mean reversion
2. **Firm adjustment** — profitability, tangibility, growth, volatility, tax shield
3. **Strategic** — M&A, activist defense, signaling
4. **Sensitivity + stress** — recession, rate change, refinancing
5. **Implementation** — target D/E, refinancing schedule, buyback

**Industry primary**:

| Industry | Theory |
|--|--|
| Utility | Trade-off |
| Tech growth | Pecking order |
| Mature stable | Trade-off + agency |
| Distressed | Debt overhang |
| Cyclical | Market timing |
| Bank | Regulatory |
| Real estate | Trade-off + tax (REIT) |
| PE | High leverage exit |

**Modern issues**:
1. SBC dilution
2. Hybrid securities
3. Operating leases (ASC 842)
4. Pension obligations
5. Climate / ESG
6. Crypto / digital

**Behavioral**:
- Overconfidence
- Anchoring
- Loss aversion
- Catering

**Industry leaders**:
- Apple: net cash, buyback for tax efficiency
- Tesla: equity + convertibles (Pecking when cash-burning)
- Berkshire: minimal debt (Buffett)

**Quotes**:
- *Buffett*: "Leverage dangerous. Don't use much."
- *Damodaran*: "Optimal = range, not point. Sensitivity essential."

**Best practice (10)**:
1. Industry benchmark
2. Firm-specific adjustment
3. Multiple theories integration
4. Sensitivity + stress
5. Strategic flexibility
6. Cyclical adjustment
7. Behavioral discipline
8. Modern issues (SBC, ESG)
9. Tax efficiency
10. Conservative bias (margin of safety)

> Optimal capital structure = *art + science*. Multi-theory + firm-specific + cyclical + flexibility + margin of safety. Single point = false precision. Range with sensitivity = realistic.

</details>
