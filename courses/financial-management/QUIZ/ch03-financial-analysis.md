# Ch 3 Financial Statements Analysis — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. 5 ratio category

각 category 의 *measuring* 대상 + 대표 ratio?

<details><summary>답</summary>

| Category | Measures | 대표 |
|--|--|--|
| **Liquidity** | 단기 viability | Current, Quick, Cash |
| **Long-term solvency** | Default risk | D/E, TIE |
| **Asset turnover** | 효율 | Inventory T, AR T, TAT |
| **Profitability** | Margin | PM, ROA, ROE |
| **Market value** | Valuation | P/E, P/B, EV/EBITDA |

**Industry 별**:
- Software: 높은 PM, 낮은 turnover, 낮은 leverage
- Retail: 낮은 PM, 높은 turnover
- Bank: 매우 낮은 turnover, 매우 높은 leverage
- Utility: 중간 PM, 높은 leverage (debt 안정)

</details>

### Q2. DuPont — 3 component decomposition

식 + 각 의미 + 3 path 의 산업 예?

<details><summary>답</summary>

$$ROE = \frac{NI}{Sales} \times \frac{Sales}{Assets} \times \frac{Assets}{Equity}$$

= Profit Margin × Asset Turnover × Equity Multiplier

| Component | 의미 | Lever |
|--|--|--|
| PM | 판매당 이익 | Pricing power, cost efficiency |
| TAT | 자산당 매출 | Asset light, operational |
| EM | Leverage | Capital structure |

**3 path 의 ROE 20%**:

| | PM | TAT | EM | Example |
|--|--|--|--|--|
| Luxury | 25% | 0.8 | 1.0 | Hermès, LVMH |
| Retail | 2.5% | 2.5 | 3.2 | Walmart, Costco |
| Bank | 25% | 0.07 | 11.4 | JPMorgan |

→ 같은 ROE 도 *완전 다른 business model*.

</details>

### Q3. 디버그 — ROE 상승 의 원인

회사 A 의 5년 ROE:

| Year | ROE | PM | TAT | EM |
|--|--|--|--|--|
| 1 | 15% | 10% | 1.5 | 1.0 |
| 2 | 17% | 10% | 1.7 | 1.0 |
| 3 | 19% | 10% | 1.5 | 1.27 |
| 4 | 22% | 10% | 1.5 | 1.47 |
| 5 | 25% | 10% | 1.5 | 1.67 |

진단?

<details><summary>답</summary>

**관찰**:
- Year 1-2: TAT *operational improvement* (정상)
- Year 3-5: EM (leverage) 만 증가 — *debt 의존*

**Component 변화**:
- Y1→Y2: TAT +0.2 (operational)
- Y3→Y5: EM +0.67 (leverage)

**Diagnosis**:
- Year 3-5: *leverage 가 ROE 의 유일 driver* — 위험 신호
- EM 1.67 = D/E 0.67
- Interest expense ↑, default risk ↑
- Stress test 시 fragile

**미래**:
- 호황: 유지
- 침체: *interest + revenue ↓* → *negative ROE* 가능

**Strategic**: PM, TAT operational improvement 필요.

**Real**:
- **Sears** (2000s-2010s): leverage 기반 → 2018 파산
- **GE** (2000s-2017): financial services leverage → 2008 후 spin-off

→ DuPont 이 *ROE 의 quality* 드러냄.

</details>

### Q4. EFN 계산

회사: Sales $1000 (20% 성장), Assets $800, Liabilities $200 (모두 spontaneous), Equity $600, PM 10%, Payout 50%.

EFN?

<details><summary>답</summary>

**Step 1**: 새 Sales = $1200

**Step 2**: Δ Assets
- Asset / Sales = 0.8
- Year 2 Assets = $960
- Δ Assets = $160

**Step 3**: Δ Spontaneous L
- Spontaneous / Sales = 0.2
- Year 2 = $240
- Δ = $40

**Step 4**: Retained Earnings
- NI = $1200 × 10% = $120
- RE = $120 × 0.5 = $60

**Step 5**: EFN
$$EFN = 160 - 40 - 60 = \$60$$

→ *$60 external financing* 필요.

**Sensitivity**:
- Growth ↑ → EFN ↑
- Profit margin ↑ → EFN ↓
- Payout ↓ → EFN ↓

</details>

### Q5. SGR 계산

위 회사의 SGR + IGR?

<details><summary>답</summary>

- ROA = $100 / $800 = 12.5%
- ROE = $100 / $600 = 16.7%
- $b$ = 0.5

**IGR**:
$$IGR = \frac{0.125 \times 0.5}{1 - 0.125 \times 0.5} = 6.67\%$$

**SGR**:
$$SGR = \frac{0.167 \times 0.5}{1 - 0.167 \times 0.5} = 9.1\%$$

**해석**:
- 외부 financing 0: 6.67%
- Capital structure 유지: 9.1%
- 목표 20% > SGR 9.1% → *equity issue* 또는 *leverage 증가*

**Strategic**:
- *Bezos Amazon* — 수년간 SGR 초과 → external + debt
- *Buffett Berkshire* — *no dividend* → SGR ↑

</details>

### Q6. 디버그 — 인플레이션 의 *ratio distortion*

A 회사 inventory $10M (LIFO). 인플레이션 10%/year. 5년 후 LIFO vs FIFO 의 *PM 차이*?

<details><summary>답</summary>

**Setup**: 인플레이션 → 최근 구매가 가장 비쌈.
- *LIFO*: 최근 = COGS, 옛것 = inventory
- *FIFO*: 옛것 = COGS, 최근 = inventory

**Year 5 (price = $14.64)**:
- Buy 100 @ $14.64
- Sell 100 → revenue $2200
- *LIFO COGS*: $1464 → NI $736 → PM 33.5%
- *FIFO COGS*: $1000 → NI $1200 → PM 54.5%

**Tax + Cash Flow**:
- LIFO: tax 적음 → cash flow 더 좋음
- *LIFO reserve* = FIFO inventory − LIFO inventory

**IFRS vs GAAP**:
- US GAAP: LIFO 허용
- IFRS: **금지**
- → 국제 비교 시 *LIFO distortion*

**현실**:
- 미국 manufacturer (steel, oil): LIFO
- Retail (Walmart, Amazon): FIFO

→ *Accounting method* 확인 필수.

</details>

### Q7. 디버그 — 산업 비교의 함정

A는 software, B는 manufacturer. ROE 둘 다 20%. 어느 게 우월?

<details><summary>답</summary>

**DuPont 분해**:

| | A (Software) | B (Manufacturer) |
|--|--|--|
| PM | 25% | 8% |
| TAT | 0.8 | 1.5 |
| EM | 1.0 | 1.67 |
| ROE | 20% | 20% |

**같은 ROE, 다른 character**:

**A (Software)**:
- 높은 PM = pricing power (SaaS subscription)
- 낮은 TAT = intangible-heavy
- Low leverage = self-funded
- 특징: high gross margin, recurring, scalable

**B (Manufacturer)**:
- 낮은 PM = commodity competition
- 높은 TAT = physical asset
- High leverage = debt-funded
- 특징: capital intensive, cyclical

**미래 sustainability**:
- A: low capital intensity, network effect, recurring revenue
- B: commodity price fluctuation, cyclical demand, capex burden

**Valuation**:
- A: EV/EBITDA 20-30x
- B: EV/EBITDA 6-10x

→ 일반적으로 *A 우월* (quality, risk, growth, valuation).

</details>

### Q8. 디버그 — Window dressing

분기말: Current ratio 3.0, Quick ratio 2.5, 매출 +30%.
다음 분기 시작: Current ratio 1.5, Quick ratio 1.0, 매출 −20%.

진단?

<details><summary>답</summary>

**Window dressing patterns**:
- *Short-term debt repayment* 직전, 재대출 직후
- *Inventory transfer* (consignment)
- *Pre-billing* customers
- *A/P delay*
- *Channel stuffing* (소매 inventory dump)
- *Bill and hold*
- *Sales discount* 분기 말 push

**Famous cases**:
- **Sunbeam** (1990s): bill and hold, channel stuffing. Al Dunlap 해고, 파산.
- **Computer Associates** (2000s): 35-day month. SEC charge.
- **HealthSouth** (2003): $2.7B fictitious. Richard Scrushy 기소.

**Detection**:
1. *Quarterly trend* — Q4 disproportionate
2. *A/R quality* — DSO 의 분기별 변동
3. *Cash conversion* — OCF/NI ratio
4. *Channel inventory*
5. *Peer comparison*

**Modern detection**:
- Benford's Law (digit distribution)
- Machine learning fraud pattern
- Short seller report (Hindenburg)
- Whistleblower (Dodd-Frank bounty)

→ *Trend + cash flow quality + peer* 가 detection 도구.

</details>

### Q9. 면접 — *SGR 의 *strategic implication*?*

"SGR 이 회사 성장의 상한?"

<details><summary>답</summary>

**SGR**:
- *현재 capital structure 유지하면서* 가능한 *internal growth*
- *외부 equity 없이*, *현재 leverage* 의 maximum

**상한 *아닌* 이유**:

1. **External financing**: New equity (IPO, secondary), more debt, convertible
2. **Operational improvement**: PM ↑, TAT ↑ → SGR 자체가 ↑
3. **Retention ratio ↑**: Dividend 줄임 → SGR ↑

**SGR 이 *상한* 인 경우**:
- *Bond covenant* — D/E 한계
- *Credit rating* (예: investment grade 유지)
- *Equity issue cost* — dilution, signaling, underpricing
- *Strategic preference* (founder control)

**Strategic dialogue**:
- CEO 의 *30% growth* 약속 vs CFO SGR 9.1%
- *어떻게 financing*?
- *Dilution* 주주 opinion
- *Risk* trade-off
- *Sustainability* (1년 vs 5년)

**Real**:
- **Amazon (1997-2010)**: SGR 초과 → external + debt, *negative NWC* 의 creative
- **Walmart (1970s-1990s)**: SGR 수준 disciplined
- **Tesla (2010s)**: hyper-growth → equity raise + debt

> SGR = *constraint with trade-off*, not 상한. 더 빠른 성장 = financing 또는 operational.

</details>

### Q10. 면접 — *Financial modeling 의 limitations*?

"빈틈없이 모델링했어도 예측 실패 흔한 이유?"

<details><summary>답</summary>

**Fundamental limitations**:

1. **Linear extrapolation** — percentage of sales 의 *linear*. 현실 *step functions*, *nonlinear scaling*.
2. **Unknown unknowns** — Black swan (2008, COVID, war), disruptive (Kodak digital, taxi Uber).
3. **Behavioral biases** — anchoring, optimism, confirmation, sunk cost.
4. **Model risk** — spreadsheet errors (London Whale의 JPMorgan $6B), circular reference, stale data.
5. **Complexity vs Accuracy** — 과도한 detail 의 false precision. Occam's razor.
6. **Strategic vs Tactical** — model = output, strategy = cause. Flawed assumption.

**Best practice**:
1. *Multiple scenarios* — Base/Bull/Bear/Stress, probability-weighted
2. *Sensitivity analysis* — Tornado diagram
3. *Monte Carlo* (Ch 7) — multiple uncertain inputs
4. *Reverse DCF* — "이 주가가 의미하는 growth rate?"
5. *Pre-mortem* — *failure 의 분석*
6. *Living model* — continuous update, variance analysis

**Famous failures**:
- **LTCM (1998)** — Nobel quant model + Russia default + correlated positions. $4.6B 손실.
- **2008 Crisis** — VaR 의 Gaussian assumption + housing correlation under-estimation.
- **WeWork (2019)** — Adjusted EBITDA creative, IPO 취소.

> Model = useful but limited. *Linear, behavioral, model risk*. *Multiple scenarios + sensitivity + reverse DCF + pre-mortem* 이 modern best practice.

</details>
