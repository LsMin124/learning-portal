# Ch 8 Interest Rates and Bond Valuation — 퀴즈

> 10 문항 (개념 2 / 계산 4 / 디버그 3 / 면접 1).

### Q1. *Premium / Par / Discount* 조건?

<details><summary>답</summary>

| Condition | Price | YTM vs Coupon |
|--|--|--|
| Premium | > par | YTM < coupon |
| Par | = par | YTM = coupon |
| Discount | < par | YTM > coupon |

**직관**:
- YTM > coupon → 시장 더 높은 return 요구
- Price 낮춰 부족 보충 → Discount

**Bond lifecycle**:
- 발행 시 par (coupon = market YTM)
- 시간 + rate change → premium/discount 변동
- Maturity 가까워질수록 → par 수렴 (*pull to par*)

</details>

### Q2. *Interest rate risk* 2 dimensions?

<details><summary>답</summary>

**1. Maturity effect** — Longer → more sensitivity
**2. Coupon effect** — Lower → more sensitivity

**직관**:
- Maturity: Cash flow 멀리 → discount exponential 영향 ↑
- Coupon: Low coupon → 대부분 가치 maturity par → long horizon sensitivity ↑

**Duration**:
- Maturity-weighted average of CF
- Zero-coupon duration = maturity
- High coupon duration < maturity

**Real examples**:
- 2022 bond crash (Fed 인상): 30-year Treasury -30%
- SVB 2023: 30-year MBS unrealized loss → 부도

**Portfolio strategies**:
- Duration matching
- Barbell (short + long)
- Bullet (single maturity)

</details>

### Q3. 계산 — Bond pricing

- $1000 par, 8% coupon semi-annual
- 5 year, YTM 6%

Price?

<details><summary>답</summary>

- C = $40, T = 10, y = 3%
- PVIFA(3%, 10) = 8.5302
- PVIF(3%, 10) = 0.7441

$$P = 40 \times 8.5302 + 1000 \times 0.7441 = \$1085.30$$

→ **Premium** (price > par, YTM < coupon).

**1 year 후** (T = 8):
- PVIFA(3%, 8) = 7.0197
- PVIF(3%, 8) = 0.7894

$$P = 40 \times 7.0197 + 1000 \times 0.7894 = \$1070.20$$

→ Price 가 점차 par 수렴 ($1085 → $1070 → ... → $1000).

</details>

### Q4. 계산 — YTM

- $1000 par, 5% coupon annual
- 10 year, Current price $850

YTM?

<details><summary>답</summary>

**Trial and error**:

| y | Price |
|--|--|
| 6% | $926 |
| 7% | $858 |
| 7.07% | $852 |
| 7.10% | $849 |

→ **YTM ≈ 7.07%**.

**Approximation**:
$$YTM \approx \frac{C + (F-P)/T}{(F+P)/2} = \frac{50 + 15}{925} = 7.03\%$$

**Excel**:
```
=RATE(10, 50, -850, 1000) → 0.0707
```

</details>

### Q5. 계산 — Duration + Convexity

- Macaulay D = 7 year, YTM 6%, Convexity = 60

(a) Modified duration?
(b) Δy = +0.5%: ΔP/P?
(c) Δy = -1%: ΔP/P (duration only)?
(d) Δy = -1%: ΔP/P (with convexity)?

<details><summary>답</summary>

**(a)** D_mod = 7/1.06 = **6.60 year**

**(b)** ΔP/P ≈ -6.60 × 0.005 = **-3.30%**

**(c)** ΔP/P ≈ -6.60 × -0.01 = **+6.60%**

**(d)** ΔP/P ≈ -6.60 × -0.01 + 0.5 × 60 × 0.0001 = 6.60% + 0.30% = **+6.90%**

→ Convexity 효과 = 0.30%.

**큰 Δy 일수록 convexity 차이 ↑**:
- ±0.5%: 0.075%
- ±2%: 1.20%
- ±5%: 7.50%

**Practitioner**:
- Small (< 25bp): Duration만 OK
- Medium (25-100bp): + Convexity
- Large (> 100bp): Full repricing

**Portfolio**:
- Duration target — 부채 일치
- Convexity max — *option-like value*
- Callable — *negative convexity* 위험

</details>

### Q6. 디버그 — Inverted yield curve

2024:
- 3-month: 5.3%
- 2-year: 4.8%
- 10-year: 4.4%
- 30-year: 4.6%

Signal?

<details><summary>답</summary>

**Inverted curve** (Short > Long, 3mo 0.9% inversion).

**3 theories**:
1. *Expectations*: Future short rate fall → recession
2. *Liquidity preference*: Strong demand for long bond
3. *Market segmentation*: Pension long, bank short

**미국 historical**:

| 연도 | Inversion | Recession |
|--|--|--|
| 1989 | Yes | 1990 |
| 2000 | Yes | 2001 |
| 2006 | Yes | 2008 |
| 2019 | Yes | 2020 COVID |
| 2022 | Yes | 2024? |

→ 모든 recession 전 ~6-18 month inversion.
False positive: 1966, 1998.

**Mechanism**:
- Fed short rate 인상 (인플레 통제)
- Long rate — future low rate expectation
- → Curve invert

**Modern complications**:
- QT (quantitative tightening) — Fed balance sheet
- Foreign demand
- Term premium

**Investor response**:
- Defensive: cash, short, high-quality
- Aggressive: long-duration (rate 하락)
- Hedge: gold, defensive stocks

→ Inverted = *probability ↑*, not certainty. *Diversified caution*.

</details>

### Q7. 디버그 — *SVB 2023*

- Deposit (short liability) $200B
- Bond portfolio (long MBS) $100B, duration ~10 year
- 2022 Fed +5% hike

무슨 일?

<details><summary>답</summary>

**Setup**:
- Asset duration: 10 year
- Liability duration: ~0
- Duration gap: 10 year

**Asset value loss**:
- ΔP/P ≈ -10 × 5% = **-50%**
- $100B → $50B
- *Unrealized loss*: $50B

**Crisis trigger**:
- 2023 March: deposit run (SNS 확산)
- 24 hours: $42B withdrawal
- Forced sale → realized loss
- *Equity wipeout*
- FDIC takeover

**Root cause** — Duration mismatch:
1. Short funding (demand deposit)
2. Long asset (10-year MBS)
3. Asymmetric mark-to-market (HTM hides loss)
4. No interest rate hedge

**Hedge tools** (SVB 안 함):
- Interest rate swap
- Treasury futures (short)
- Cap/floor

**Lessons**:
1. ALM (Asset-Liability Management) fundamental
2. Duration gap active management
3. Stress test
4. Bank regulation — Dodd-Frank reduce after 2018
5. HTM accounting loophole

**Other 2023 failures**: Signature Bank, First Republic, Credit Suisse.

**Modern bank**:
- Duration matching (자산-부채 차이 < 1 year)
- Daily VaR monitoring
- Stress test — +500bp scenario

</details>

### Q8. 디버그 — Credit spread

회사 X — 5 year bond:
- 2019: yield 3.5%, T 1.8% → spread 1.7%
- 2020 March: yield 8.5%, T 0.5% → spread 8.0%
- 2021: yield 3.0%, T 1.5% → spread 1.5%

해석?

<details><summary>답</summary>

**왜 *COVID spread 8.0%***:
1. Default risk uncertainty
2. Liquidity dry-up
3. Flight to quality (Treasury 만 수요)
4. Forced selling (fund redemption)

**Fed intervention 2020**:
- QE — Treasury + MBS 매입
- PMCCF, SMCCF — *최초 corporate bond facility*
- Liquidity facilities
- → Spread narrow back

**해석 — Credit cycle**:
- Normal: 1-2%
- Stress: 3-5%
- Crisis: > 5%

**Investor behavior**:
- Spread widening — recession fear
- Spread narrowing — risk appetite return
- Carry trade — short Treasury, long corp

**Use of spread**:
- Recession predictor (6-12 month lead)
- Default probability (Merton model)
- Investment ranking
- Equity risk premium base

**Spread products**:
- CDS — pure default risk
- iTraxx, CDX indices
- VCSH (short), HYG (junk) ETF

**Famous spread events**:
- 1998 LTCM, 2008 Lehman, 2011 Eurozone, 2020 COVID, 2022-23 SVB

</details>

### Q9. 디버그 — TIPS vs Nominal

2024:
- 10-year Treasury: 4.5%
- 10-year TIPS: 2.1%
- BEI: 2.4%

A — TIPS, B — Nominal — 결정 logic?

<details><summary>답</summary>

**BEI 의미**: 시장 implied inflation.

**투자자 결정 — *inflation expectation* 의존**:

| Scenario | Nominal (4.5%) | TIPS (2.1% real) |
|--|--|--|
| Inflation 1% | 3.5% real | 2.1% real |
| Inflation 2.4% | 2.1% real | 2.1% (equal) |
| Inflation 5% | -0.5% real | 2.1% real |

→ Higher inflation → TIPS 우위.

**TIPS pros**:
- Real return 보장
- Inflation shock 보호
- Long-term retirement 적합

**TIPS cons**:
- Tax on imputed inflation (annual, no cash)
- Lower liquidity
- Deflation period no benefit (floor at par)

**Use cases**:

| Investor | Best |
|--|--|
| Retiree (real income) | TIPS |
| Bank/insurance | Nominal |
| Speculator | Either (inflation view) |
| Foreign | Nominal (USD exposure) |
| Tax-deferred | TIPS |
| Taxable | Nominal (simpler) |

**Modern complications**:
- Deflation floor (par minimum)
- Negative real yield 2020-22
- Foreign TIPS-like: 영국 Gilts, 캐나다 RRB

**Famous TIPS moments**:
- 1997 introduction
- 2008-2009 — deflation, floor 활용
- 2022 — inflation surge, outperform
- 2024 — normalization

</details>

### Q10. 면접 — *Bond strategy in rising rate*?

<details><summary>답</summary>

**6 framework**:

**1. Shorten duration** — Long → Short, FRN
**2. Floating rate exposure** — bank loans, FRN, ARM
**3. Credit quality up** — Junk → Investment grade
**4. TIPS** — inflation protection
**5. Active hedging** — futures, swap, cap, bear ETF
**6. Cash allocation** — money market, T-bill

**Specific tactics**:
- Barbell — short + long, middle skip
- Bullet — single maturity
- Ladder — equal portion 각 maturity

**Risk management**:

| Risk | Hedge |
|--|--|
| Interest rate | Duration short, futures |
| Credit | Quality up, CDS |
| Inflation | TIPS, commodities |
| Currency | Forward, hedge ETF |
| Liquidity | Treasury, large issues |

**ETF tools**:

| ETF | Strategy |
|--|--|
| SHY | Short Treasury |
| TLT | Long Treasury |
| LQD | Investment grade corp |
| HYG | High yield |
| TIP | TIPS |
| FLOT | Floating rate |
| TBT | -2x Treasury bear |

**Famous rising rate periods**:
- 1979-1981 Volcker — 9% → 20%, 1980 -8% nominal
- 1994 Greenspan surprise — Long T -8%
- 2004-2006 — 1% → 5.25%
- 2022 — 7 hike year, Long T -30%

**Lessons 2022**:
- 60/40 둘 다 negative
- Duration risk underestimated
- TIPS outperform
- Cash king — T-bill popularity

**Conservative** (rising rate):
1. Shorter (2-5yr)
2. Higher quality (AA+)
3. Floating (20-30%)
4. TIPS (10-15%)
5. Cash (10%)

**Aggressive opportunistic**:
1. Long-duration after peak (cut expected)
2. Distressed credit (after spread widen)
3. Foreign currency bond (USD weakness)

> Rising rate = defense + opportunistic combination. Active management outperformance potential.

</details>
