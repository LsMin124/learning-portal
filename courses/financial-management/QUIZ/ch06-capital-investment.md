# Ch 6 Making Capital Investment Decisions — 퀴즈

> 10 문항 (개념 2 / 계산 4 / 디버그 3 / 면접 1).

### Q1. *Incremental cash flow* — 어느 게 *포함*?

(a) 지난 분기 시장 조사비 $50K
(b) 회사 보유 토지 (시장 $200K) 위에 공장
(c) 새 product 가 기존 매출 $30K 잠식
(d) Allocated overhead $20K
(e) 새 product 가 매장 traffic ↑ → 다른 product +$10K

<details><summary>답</summary>

| | 포함? | 분류 |
|--|--|--|
| (a) | ✗ | Sunk cost |
| (b) | ✓ ($200K) | Opportunity cost |
| (c) | ✓ ($-30K) | Erosion |
| (d) | ✗ | Allocated (incremental 만 포함) |
| (e) | ✓ ($+10K) | Synergy |

</details>

### Q2. *OCF* 의 *3 가지 공식*

데이터:
- Sales $500K
- Cost $200K
- Depreciation $100K
- T_c = 25%

3 가지 방법으로 OCF?

<details><summary>답</summary>

**(1) Bottom-up**:
- EBIT = $200K, Tax = $50K, NI = $150K
- OCF = $150K + $100K = **$250K**

**(2) Top-down**:
- OCF = $500K − $200K − $50K = **$250K**

**(3) Tax shield**:
- OCF = ($500K − $200K)(0.75) + $100K(0.25)
- = $225K + $25K = **$250K**

→ 모두 동일.

**핵심 통찰**: Depreciation tax shield = $25K. MACRS / accelerated 가 *PV* 더 큼.

</details>

### Q3. 계산 — NPV with depreciation

Project:
- Capex: $500K (straight-line 5-year)
- Sales: $300K/year
- Cost: $150K/year
- T_c = 21%, r = 10%

NPV?

<details><summary>답</summary>

**Depreciation**: $500K / 5 = $100K/year

**Annual OCF**:
- EBIT = $50K, Tax = $10.5K, NI = $39.5K
- OCF = $39.5K + $100K = **$139.5K**

**NPV**:
$$NPV = -500 + 139.5 \times 3.7908 = \$28.8K$$

→ Accept.

**Bonus depreciation 100%** (Year 0 전체):
- Year 0: $-500K + $105K tax saving = $-395K
- Year 1-5 OCF: ($150K)(0.79) = $118.5K
- NPV = $-395K + $118.5K × 3.7908 = **$54.2K**

→ Bonus 의 *큰 차이* ($28.8K → $54.2K).

</details>

### Q4. 계산 — *MACRS* depreciation

같은 project (Q3), depreciation 만 *5-year MACRS*:
- Year 1: 20%, Y2: 32%, Y3: 19.2%, Y4: 11.52%, Y5: 11.52%

NPV?

<details><summary>답</summary>

**Annual OCF** = ($300K − $150K)(0.79) + D × 0.21

| Year | D | OCF |
|--|--|--|
| 1 | $100K | $118.5K + $21K = $139.5K |
| 2 | $160K | $118.5K + $33.6K = $152.1K |
| 3 | $96K | $118.5K + $20.16K = $138.66K |
| 4 | $57.6K | $118.5K + $12.1K = $130.6K |
| 5 | $57.6K | $118.5K + $12.1K = $130.6K |

**NPV**:
$$NPV = -500 + 126.8 + 125.7 + 104.2 + 89.2 + 81.1 = \$27K$$

**비교**:
- Straight-line: $28.8K
- MACRS: $27K (이 예제 Year 6 5.76% 무시)

→ Real MACRS (Year 6 포함) — *항상 우월*.

</details>

### Q5. 디버그 — Sunk cost

회사 — *new product*:
- R&D 의 지난 2년 $5M
- 추가 Capex: $10M
- Annual OCF: $3M (10 year)
- WACC = 12%

CEO: *"$5M 회수해야 — total $15M*". 옳은가?

<details><summary>답</summary>

**CEO 의 *실수***:

**Stand-alone**:
- Year 0: $-10M (R&D *sunk*, 무시)
- NPV = $-10M + $3M × 5.65 = **$6.95M positive**

→ ***Accept***.

**Famous sunk cost fallacy**:
- *Concorde* (1956-2003) — *돈 회수* 욕망 → 50년 운영 NPV negative
- *Boeing 747-8* (2011) — 브랜드 회수 → 단종
- *Vietnam War* (1965-1975) — *escalation*

**Behavioral root**:
- Loss aversion (Kahneman-Tversky)
- Commitment escalation (Staw)
- Public face — admit 실패 cost

**Solution**:
- Sunk cost 의 명시적 식별
- Future-only rule
- External advisor 의 objective view
- Decision tree (Ch 7) 의 stage 별 evaluation

</details>

### Q6. 디버그 — *NWC* 처리

회사 — e-commerce:
- A/R +$10K
- Inventory +$30K
- A/P +$50K

분석가: *"NWC 증가 $40K — outflow."* 맞나?

<details><summary>답</summary>

**잘못된 계산** — A/P 의 positive effect 무시.

**정확한 ΔNWC**:
$$\Delta NWC = (10 + 30) - 50 = \mathbf{-\$10K}$$

→ NWC negative change = cash inflow $10K.

**Amazon 의 negative NWC strategy**:
- Customer 즉시 결제
- Supplier 60-90 day 후 지불
- → *Supplier 가 funded*

**Cash conversion cycle**:
$$CCC = DSO + DIO - DPO$$

| Firm | CCC |
|--|--|
| Amazon | ~-30 day |
| Walmart | ~+5 day |
| Tesla | ~+20 day |
| Apple | ~-30 day |

**Negative NWC 의 strategic value**:
- Free working capital
- Compounding growth — sales 증가 시 cash 자동 ↑
- Negotiating power 의 결과

</details>

### Q7. 디버그 — *Salvage value tax*

- Capex: $100K (5-year MACRS)
- Year 5 sell: $40K
- T_c = 21%

After-tax salvage?

<details><summary>답</summary>

**Step 1: Year 5 Book Value**:
- MACRS 누적: 94.24%
- BV = $100K × 5.76% = **$5,760**

**Step 2: Gain**:
- $40K − $5,760 = **$34,240**

**Step 3: Tax**:
- $34,240 × 21% = **$7,190**

**Step 4: After-tax salvage**:
- $40K − $7,190 = **$32,810**

**Loss scenario** (sell at $3K):
- Loss: $-2,760
- Tax saving: $-580
- After-tax: $3K + $580 = $3,580

**Pedagogical**:
- Gain = tax 지불, after-tax < sale
- Loss = tax saving, after-tax > sale

**Real estate** (commercial) — *Section 1250 depreciation recapture* — complex.

</details>

### Q8. 디버그 — *Inflation* consistency

- Year 1 nominal CF $100, growing 5% nominal
- Discount rate 12% real (inflation 3%)
- 10 year

NPV correctness?

<details><summary>답</summary>

**불일치**:
- CF: nominal (5% growth)
- r: real (12%)

**Fix 1 — both nominal**:
- r nominal: $(1.12)(1.03) - 1 = 15.36\%$
- Year 5 CF: $100 × 1.05^4 = $121.55

**Fix 2 — both real**:
- CF real growth: $(1.05)/(1.03) - 1 = 1.94\%$
- Year 5 real: $100 × 1.0194^4 = $108

**Year 5 PV comparison**:
- *Both nominal*: $121.55 / 1.1536^5 = $74.4
- *Both real*: $108 / 1.12^5 = $61.3
- *Mixed (wrong)*: $121.55 / 1.12^5 = $69 (incorrect)

→ Mixed = NPV 과대.

**Famous distortion**:
- 1970s 미국 (15% 인플레) — capital budgeting 의 *대규모 mis-investment*
- Argentina (50%+ 인플레) — *daily price update*

**Modern practice**:
- Nominal forecast + nominal WACC
- Sensitivity 의 inflation scenario
- Local currency 의 country cost of capital

</details>

### Q9. 디버그 — *Equipment replacement*

기존 — 5 year old, 5 year remaining, $2K/year operating
- Sell now: $5K, BV: $4K
- T_c = 21%

새 — 10 year life, $1K/year operating
- Cost: $20K (5-year MACRS, salvage $0)
- r = 10%

Replace?

<details><summary>답</summary>

**Old machine EAC** ≈ $1.58K (after-tax op) + $1.26K (opportunity from sale) = **$2.84K/year**

**New machine EAC** ≈ $20K / 6.1446 − $0.05K = **$3.21K/year**

→ Old EAC < New EAC → ***replace 안 함***.

**Caveat — quality, reliability, environmental**:
- Old breakdown 위험 증가
- New technology improvement
- Regulation (emission standard)

**Real example**:
- FedEx fleet replacement — 8-10 year cycle
- Solar panel — 25-year warranty + degradation 0.5%/year, replacement unlikely

**Lesson**: EAC 가 unequal life 의 gold standard. Technology + regulation 고려.

</details>

### Q10. 면접 — *Post-audit* 의 value?

"Project 1년 후 *actual vs forecast NPV* — 비교 의 value?"

<details><summary>답</summary>

**Post-audit** — *흔히 빠뜨림*, *큰 value*.

**Why**:

1. **Forecasting accuracy** measurement
2. **Bias correction** — optimism, anchoring
3. **Learning** — assumption 의 *off*
4. **Discipline** — future propose 의 honesty
5. **Manager compensation alignment**

**Common biases**:

| Bias | 영향 |
|--|--|
| Optimism | Sales overestimate |
| Empire building | Cost underestimate |
| Anchoring | Benchmark prior |
| Information asymmetry | Manager private info |
| Capital rationing game | Inflated NPV to win |

**Challenges**:
1. Attribution — *project CF* 의 isolation 어려움
2. Externality — *외부 환경*
3. Manager 이동
4. Cost — audit resource
5. Behavioral resistance

**Famous post-audit lessons**:
- *Disney Eurodisney* (1992) — attendance forecast 의 50% — cultural error
- *Daimler-Chrysler* (1998-2007) — $36B → $7B — synergy overestimate
- *HP-Compaq* (2002) — forecast $2.5B synergy → negative
- *AOL-Time Warner* (2000) — $164B → $99B write-off

**Modern best practice**:
1. Standardized post-audit
2. Variance analysis (line item)
3. Root cause
4. Knowledge management
5. Track record
6. Bias correction adjustment

**Industry practice**:
- Oil/gas: production curve 비교
- Manufacturing: quarterly variance vs plan
- Tech startup: cohort analysis
- PE: deal post-mortem

**Buffett**:
> *"Capital allocation 의 quality 가 CEO 의 가장 중요한 기능."*

> Post-audit + learning = long-term advantage.

</details>
