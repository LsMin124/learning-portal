# Ch 9 Stock Valuation — 퀴즈

> 10 문항 (개념 2 / 계산 5 / 디버그 2 / 면접 1).

### Q1. *4 가지 valuation approach*?

<details><summary>답</summary>

| Method | 공식 | Use case |
|--|--|--|
| DDM | $\sum D_t/(1+R)^t$ | Mature dividend firm |
| FCFE | $\sum FCFE_t/(1+R_e)^t$ | Equity-level all firms |
| FCFF | $\sum FCFF_t/(1+WACC)^t$ | Capital structure agnostic |
| Multiples | P/E, EV/EBITDA, P/B | Quick comparable |

**Industry choice**:

| Industry | Primary |
|--|--|
| Mature dividend | DDM |
| Tech growth | FCFE / FCFF |
| Bank | P/B + ROE |
| Mining/Oil | NPV + commodity scenario |
| Pharma | Multi-stage FCF + decision tree |
| Startup | Revenue multiple, VC method |

**Triangulation**: 3-5 methods range + judgment integration.

</details>

### Q2. *Gordon Growth* 3 가정 + 위반 결과?

<details><summary>답</summary>

**3 가정**:
1. Constant growth g — 영원히 같은 rate
2. R > g — required > growth
3. Stable payout — dividend policy constant

**위반**:

**1. g 변동** → Multi-stage model (Apple 2010s, Tesla)
**2. R ≤ g** → 무한대, multi-stage with terminal g < R
**3. Payout 변동** → Total payout (D + Buyback)

**Real cases**:
- Apple (2012 first dividend) — 0% → 25%
- Microsoft (2003 first dividend)
- Amazon (2024 first dividend?)
- Tesla — no dividend
- Berkshire — Buffett "no dividend ever"

**Modern solution**:
- Multi-stage DDM
- FCFE (dividend independent)
- Total payout model
- Damodaran 6-stage

</details>

### Q3. 계산 — Gordon Growth

- $D_0 = $3.00, g = 6%, R = 13%$

(a) P_0?
(b) P_1?
(c) Total return 검증?

<details><summary>답</summary>

**(a)**: D_1 = 3.18
$$P_0 = \frac{3.18}{0.07} = \$45.43$$

**(b)**: D_2 = 3.37
$$P_1 = \frac{3.37}{0.07} = \$48.16$$

또는 P_0 × 1.06 = $48.16 ✓

**(c)**:
- Dividend yield: 3.18/45.43 = 7%
- Capital gain: (48.16-45.43)/45.43 = 6%
- **Total 13%** ✓

</details>

### Q4. 계산 — Multi-stage 2-stage

- $D_0 = $1.50$
- $g_1 = 25\%$ (3 years)
- $g_2 = 5\%$ (perpetual)
- $R = 14\%$

P_0?

<details><summary>답</summary>

**Stage 1**:
- D_1 = 1.875, D_2 = 2.344, D_3 = 2.930

**Stage 2**:
- D_4 = 3.076, P_3 = 3.076/0.09 = $34.18

**Discount**:
- PV(D_1) = 1.645
- PV(D_2) = 1.804
- PV(D_3) = 1.977
- PV(P_3) = 23.07

**P_0 = $28.50**

**해석**:
- Terminal PV ($23.07) = 81% of total
- Stage 1 explicit = 19%

**Sensitivity**:
- g_2 = 4%: $26.04
- g_2 = 6%: $31.55
- → ±1% → ~10% price change

</details>

### Q5. 계산 — Sustainable Growth

- ROE 18%, b = 40%
- D_0 = $2, R = 12%

(a) g?
(b) D_1?
(c) P_0?

<details><summary>답</summary>

**(a)**: g = 0.18 × 0.40 = **7.2%**

**(b)**: D_1 = 2 × 1.072 = $2.144

**(c)**: P_0 = 2.144/0.048 = **$44.67**

**Insight — ROE quality**:
- High ROE + retention = value creating
- Low ROE + retention = value destroying

**Value destroying example**:
- ROE 8% < R 12%, retain 60%
- g = 4.8%
- *Reinvested capital negative NPV*

**Buffett**:
> *"Only retain when each $ creates > $1 market value."*

**Sustainable g limit**:
- Long-term: 5-10% max
- Mature firm: 3-5%
- Mature industry: 2-3%

</details>

### Q6. 계산 — P/E approach

- EPS_0 = $5, Industry P/E = 18
- Forward EPS growth = 8%
- R_f = 4%, ERP = 6%, β = 1.2

(a) Trailing valuation?
(b) Forward P/E?
(c) Justified P/E from Gordon?

<details><summary>답</summary>

**(a) Trailing**: P = 5 × 18 = **$90**

**(b) Forward**:
- EPS_1 = 5.40
- Forward P/E = 90/5.40 = **16.67**

**(c) Justified P/E**:
- R = 4% + 1.2 × 6% = 11.2%
- Payout 50%:
$$P/E = \frac{0.5}{0.112 - 0.08} = 15.6$$

→ Justified 15.6 < Industry 18 — industry overvalued or our risk lower?

**β = 0.9 (lower risk)**:
- R = 9.4%
- Justified P/E = 0.5/0.014 = 35.7
- P/E 18 = significant undervaluation!

**β = 1.2 (equal risk)**:
- Justified 15.6 vs 18 = ~6% overvaluation

**Apple real example (2024)**:
- EPS forward $6, P/E 28 → $168
- Justified (R=10%, g=8%, b=0.7): P/E = 15
- *큰 차이* — quality + brand premium

</details>

### Q7. 계산 — Implied growth (Reverse DCF)

Tesla 2024:
- Price $250, D_0 = $0
- Earnings $4/share
- R = 12% (β = 2.2)

*Implied perpetual earnings growth*?

<details><summary>답</summary>

**Multi-stage assumption**:

Stage 1 (10 yr) high growth, Stage 2 stable 4% payout 80%.

**For P_0 = $250**:
- 10 years 후 EPS = 4 × (1+g_1)^10
- P_10 = EPS_10 × 0.8 / (0.12 - 0.04) = EPS_10 × 10
- P_0 = P_10 / 1.12^10 = P_10 / 3.106
- 250 = EPS_10 × 10 / 3.106 → EPS_10 = 77.65
- 4 × (1+g_1)^10 = 77.65 → **g_1 = 34%/year**

→ Implied 34% EPS growth for 10 years.

**Reality check**:
- Tesla EPS 2019-2024: $-0.98 → $4.30 — CAGR ~30%
- Continuation 10 more years?
- Mature auto industry: 2-5%
- EV + storage growth?

**Buffett critique**:
- 34% for 10 years = 19x EPS by Year 10
- Heroic assumption
- Margin of safety 부족

**Damodaran**:
- Tesla over-valued (반복)
- Implied growth historically rare

→ Reverse DCF = market expectation transparency.

</details>

### Q8. 디버그 — Apple DDM 실패

Apple 2024:
- Dividend $1/year (~0.6% yield at $170)
- DDM: P = $1/(0.10-0.04) = $16.67
- Market: $170

DDM 10x error 원인?

<details><summary>답</summary>

**4 원인**:

**1. Buyback dominant**:
- Annual buyback ~$90B
- Dividend ~$15B
- Total payout ~$105B = ~$6/share (4% yield)
- *Total payout DDM*: $6/0.06 = $100 (가까움)

**2. Buyback boost g**:
- Share count ↓ → per-share g 의 artificial inflation
- Adjusted g (excl buyback) ≈ 4%
- With buyback per-share g ≈ 8%

**3. Brand + ecosystem premium**:
- Switching cost (iOS lock-in)
- Brand value
- Recurring (Services growth)

**4. Future option value**:
- Vision Pro, Apple AI
- Optionality valuation

**Correct framework**:

$$P = \frac{Total\ Payout \times (1+g_1)}{R - g_2}$$ (multi-stage)

또는 FCF:
- Apple FCF ~$100B/year, g 6%
- Firm value: $100B × 1.06 / 0.03 = $3.5T
- Per share (16B): $220 — 더 가까움

**Lesson**:
- Pure DDM — dividend-only firm
- Total payout 더 정확
- FCF approach 가장 flexible
- Multiple methods triangulation

**Buffett's evolution**:
- Old: DDM, low P/E, value
- Apple 2016: quality + moat + buyback
- 현재 Berkshire 최대 holding (~50%)

</details>

### Q9. 디버그 — High P/E justification

회사 X tech:
- EPS_0 = $1, Forward P/E = 60

영원히 성장? Justification?

<details><summary>답</summary>

**P/E 60 implied (Gordon)**:

R = 10%, b = 50%:
- 0.5/(0.10-g) = 60 → g = 9.17% perpetual

→ 영원히 9-10% growth. 불가능 (long-term).

**Multi-stage interpretation**:

10 years high (예: 20%) → stable 5%:
- EPS_10 = $6.19
- P_10 = (6.19 × 1.05 × 0.5) / 0.05 = $65
- P_0 = $25 → Forward P/E = 25 (not 60)

→ Market 60 implies more aggressive — 15-20% 영원히 or 25% for 15 year.

**Justified scenarios**:
1. Network effect (Facebook, Google early)
2. Switching cost lock-in
3. Mega-trend (AI, EV, cloud)
4. Disruptive innovation
5. Real options (platform)

**Bubble history**:
- Nifty Fifty (1972) — P/E 50-90, 10yr stagnation
- Dot-com 1999 — P/E 100+, Cisco P/E 200 → -80% 5yr
- 2021 SPAC — Lordstown, Lucid
- 2024 AI — Nvidia P/E 60+

**Investor decision**:
- Believer: thesis, long hold
- Skeptic: margin of safety, mean reversion
- Hybrid: some exposure (10-15%), stop loss

**Damodaran**:
> *"High P/E justify 는 specific growth narrative + constraint understanding."*

</details>

### 10. 면접 — *Modern equity valuation framework*?

<details><summary>답</summary>

**Multi-layered framework**:

**Layer 1 — Intrinsic methods**:
- DDM, FCFE, FCFF, RI, APV

**Layer 2 — Relative multiples**:
- P/E, Forward P/E, PEG, EV/EBITDA, EV/Sales, P/B, P/S, EV/EBIT

**Layer 3 — Comparable**:
- Trading, Transaction, Sum-of-parts

**Layer 4 — Special**:

| Situation | Method |
|--|--|
| Distressed | Liquidation, restructuring |
| Cyclical | Normalized, mid-cycle |
| Pre-revenue | VC, real options |
| Bank | Excess return, ROE-justified P/B |
| REIT | NAV, FFO |
| Mining | NPV + commodity |
| Pharma | Risk-adjusted NPV, decision tree |

**Layer 5 — Factor**:
- Fama-French 5 factor
- Momentum, Quality, Volatility

**Layer 6 — Behavioral / Sentiment**:
- CAPE Shiller, Buffett indicator, VIX, P/C ratio

**Layer 7 — AI/ML**:
- NLP (earnings call)
- Alternative data (satellite, credit card)
- RL trading
- Knowledge graph
- Causal inference

**Triangulation**:

```
1. DCF intrinsic
2. Trading multiples
3. Transaction multiples
4. Sum-of-parts (if applicable)
5. Sensitivity + scenario
6. Behavioral overlay
7. Margin of safety
```

**Industry primary**:

| Industry | Top 3 |
|--|--|
| Tech (mature) | DCF, P/E, EV/EBITDA |
| Tech (growth) | DCF multi, P/Sales, engagement |
| Bank | P/B, RI, ROE-justified |
| Real estate | NAV, FFO, DCF |
| Mining/Oil | NPV, EV/Reserves |
| Pharma | DCF, EV/Sales, decision tree NPV |
| Retail | EV/EBITDA, P/E, store NPV |

**Famous cases**:
- Microsoft 1986 IPO P/E 12 → $3T today
- Cisco 2000 P/E 200, 2000 peak still unsurpassed
- Apple 2016 Buffett $1B P/E 12 → 7x in 8 years
- Tesla 2020-24 $50→$1200→$250 wild swing

**Wisdoms**:
- *Buffett*: "Price is what you pay, value is what you get."
- *Munger*: "Big money in waiting."
- *Damodaran*: "Valuation = craft, quantitative + qualitative."

> Modern valuation = *range with confidence*. *Multiple methods + scenario + behavioral + AI*. *Margin of safety + patience*.

</details>
