# Ch 2 Financial Statements and Cash Flow — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. 3 재무제표 의 *관계*

각 statement 의 역할 + 상호 연결?

<details><summary>답</summary>

| | 시간 | 답하는 질문 |
|--|--|--|
| **Balance Sheet** | 한 시점 (snapshot) | "지금 무엇을 보유하나?" |
| **Income Statement** | 기간 (year/quarter) | "이 기간 얼마 벌었나?" |
| **Cash Flow Statement** | 기간 | "이 기간 cash 어떻게 움직였나?" |

**연결**:
- I/S 의 *Net Income* → Retained Earnings (B/S equity)
- I/S 의 *Depreciation* → CF Statement 의 noncash adjustment
- B/S 의 *Capex* (Δ Fixed Asset) → CF Statement Investing
- B/S 의 *ΔWorking Capital* → CF Statement Operating
- B/S 의 *Δ Debt, Equity, Dividend* → CF Statement Financing

→ 3 statement 가 *self-consistent system*.

</details>

### Q2. Book value vs Market value

다음 시나리오 — book 과 market 의 차이?

(a) 30년 된 build (book $5M, 현재 fair value $50M)
(b) Software company 의 brand value
(c) IPO 첫날 market cap $10B, book equity $500M
(d) Bankruptcy 가까운 회사

<details><summary>답</summary>

**(a)**: Book $5M (historical cost − depreciation), Market $50M. *Under-valuation*.
**(b)**: Book ~$0 (internally generated intangible 불가), Market 수십억 (Coca-Cola brand ~$70B).
**(c)**: P/B = 20x (Premium for growth).
**(d)**: Book 양수, Market ~0 (equity 의 residual 이 debt 에 흡수).

**결론**:
- *Book* = conservative + historical
- *Market* = forward-looking + growth
- 의사 결정 = market. 회계 보고 = book.

</details>

### Q3. Cash Flow vs Net Income — *3 noncash items*

회사 Net Income $100. Cash flow 와 차이를 만드는 *3 noncash items* + 각 영향?

<details><summary>답</summary>

**1. Depreciation $50**:
- I/S: 비용 차감 (NI 감소)
- Cash: *이미 자산 매입 시 지출 완료*
- Reconciliation: NI 에 + $50

**2. Δ Accounts Receivable +$30** (매출 외상):
- I/S: 매출 $100 인식
- Cash: 실제 $70
- Reconciliation: NI 에서 − $30

**3. Δ Accounts Payable +$20** (구매 외상):
- I/S: 비용 $60
- Cash: 실제 $40
- Reconciliation: NI 에 + $20

**예제 계산**:

```
Net Income                $100
+ Depreciation            + $50
- ΔA/R (increase)         - $30
+ ΔA/P (increase)         + $20
─────────────
Operating Cash Flow       $140
```

→ NI $100 인데 OCF $140 — *cash 가 더 좋은* 케이스 (healthy).

**역 시나리오** (NI > OCF) — red flag.

</details>

### Q4. OCF 계산

다음 데이터:
- Sales $1000
- COGS $400
- SG&A $200
- Depreciation $100
- Interest $50
- Tax rate 21%

OCF 계산?

<details><summary>답</summary>

**Income Statement**:
```
Sales                  $1000
- COGS                  -400
- SG&A                  -200
- Depreciation          -100
─────────────
EBIT                    $300
- Interest               -50
─────────────
EBT                     $250
- Tax (21%)              -52.5
─────────────
Net Income              $197.5
```

**OCF**:
$$OCF = EBIT + Depreciation - Taxes = 300 + 100 - 52.5 = \$347.5$$

또는:
$$OCF = NI + Depreciation + Interest = 197.5 + 100 + 50 = \$347.5$$

**왜 interest 더하나**:
- OCF = *operating activity*, financing decision 무관
- Interest = financing
- FCFF (firm 가치) 시 interest 빼지 않음
- FCFE (equity 가치) 만 interest 차감

</details>

### Q5. FCF 계산

위 예제 + Capex $150, ΔNWC $30.

FCF + 분배 가능 cash?

<details><summary>답</summary>

$$FCF = OCF - \Delta NWC - Capex = 347.5 - 30 - 150 = \$167.5$$

**Distribution**:
- Debt: interest $50 + principal $20 = $70
- Equity: dividend $30 + buyback $50 = $80
- 남은 $17.5 — cash balance 증가

**FCF 의 의의**:
- *Valuation* (DCF, Ch 4) 의 input
- *Capital allocation* 의 evidence
- Growth firm = FCF 작음, mature = FCF 큼

</details>

### Q6. Net Working Capital 의 *good vs bad*

다음 회사 들의 NWC + 평가?

(a) Tesla: A/R $2B, inventory $13B, A/P $9B, short-term debt $1B
(b) Amazon: A/R $5B, inventory $15B, A/P $80B, short-term debt $10B
(c) Walmart: A/R $7B, inventory $55B, A/P $50B, short-term debt $5B

<details><summary>답</summary>

**Tesla**: NWC = (2+13) − (9+1) = $5B. Standard manufacturer.

**Amazon**: NWC = (5+15) − (80+10) = **−$70B**. *Negative* — supplier credit > customer credit. *Free working capital* — supplier 가 사실상 *무이자 융자*.

**Walmart**: NWC = (7+55) − (50+5) = $7B. Modest positive.

**Cash Conversion Cycle**:
$$CCC = DSO + DIO - DPO$$
- Amazon: ~-30 days (supplier 가 융자)
- Walmart: ~+5 days
- Tesla: ~+20 days

> *Negative NWC* = 위험 아닌 *효율*. Retail/marketplace 에서만 가능. *Amazon 의 비밀* = retail margin 보다 *NWC efficiency*.

</details>

### Q7. EBITDA 의 함정

스타트업 A, B. 같은 EBITDA $50M. 어느 회사의 *Equity value 더 큰가*?

| | A | B |
|--|--|--|
| EBITDA | $50M | $50M |
| Depreciation | $10M | $30M |
| Capex | $15M | $40M |
| ΔNWC | $5M | $20M |
| Debt | $100M | $200M |
| Interest | $5M | $15M |
| Tax rate | 21% | 21% |

<details><summary>답</summary>

**A**:
- EBIT = 50 − 10 = $40M
- NI = (40−5) × 0.79 = $27.65M
- OCF ≈ NI + D + Interest = 42.65M
- FCF = 42.65 − 5 − 15 = **$22.65M**

**B**:
- EBIT = 50 − 30 = $20M
- NI = (20−15) × 0.79 = $3.95M
- OCF = 3.95 + 30 + 15 = $48.95M
- FCF = 48.95 − 20 − 40 = **−$11.05M**

**같은 EBITDA, FCF 큰 차이**:
- A: $22.65M positive
- B: negative

**Lesson**:
- A = asset-light (cash 생성 우월)
- B = capital intensive (capex 가 cash 잡아먹음)

**EBITDA 한계**: capex, NWC, tax, interest 모두 무시. 

**Charlie Munger**: *"EBITDA = bullshit earnings."*

**Modern**:
- Capital-light (SaaS, asset management): EBITDA ≈ FCF
- Capital-heavy (telecom, utility, manufacturing): EBITDA >> FCF

</details>

### Q8. 디버그 — Cash flow red flag

5년 trend:

| Year | NI | OCF | Capex | D&A |
|--|--|--|--|--|
| 1 | $100 | $130 | $80 | $50 |
| 2 | $120 | $110 | $100 | $55 |
| 3 | $140 | $90 | $120 | $60 |
| 4 | $160 | $70 | $150 | $65 |
| 5 | $180 | $40 | $180 | $70 |

진단?

<details><summary>답</summary>

**Trend**:
- NI: +80% ↑
- OCF: **-70% ↓**
- Capex: +125% ↑
- *FCF*: Y1 $50, Y5 **−$140** — cash burn

**Red flag**:
1. NI ↑, OCF ↓ — *aggressive revenue recognition* 가능
2. Capex 의 *aggressive 증가* — hyper-growth or asset depletion 회피
3. *FCF negative* — external financing 의존

**Possible**:
- (a) Hyper-growth (Uber, Tesla 의 early) — *intentional*
- (b) Working capital deterioration — A/R, inventory quality 문제
- (c) Earnings management — Enron, Wirecard 같은 fraud sign

**확인 방법**:
- DSO trend
- Inventory days
- Accrual ratio = (NI - OCF) / Assets
- Reverse engineer revenue
- Industry comparison

**Famous examples**:
- **Enron** (2001): NI ↑ + OCF 정체
- **Wirecard** (2020): A/R phantom
- **WeWork** (2019): Adjusted EBITDA creative

→ NI vs OCF *지속적 divergence* = 대표적 red flag.

</details>

### Q9. 디버그 — Negative FCF 의 *evaluation*

회사 A — 5년 연속 *negative FCF* $-50M/year. 인수 검토?

<details><summary>답</summary>

**Negative FCF 가 *항상 bad* 는 아님**:

**Good negative FCF**:
- Early-stage growth (Amazon 1995-2001, Tesla 2003-2019)
- High ROIC reinvestment
- Industry growth phase

**Bad negative FCF**:
- Mature firm, capex 가 maintenance 만
- Working capital deterioration
- Operating loss + capex 동시

**평가 framework**:

| 질문 | Good FCF- | Bad FCF- |
|--|--|--|
| Capex 의 ROIC? | > Cost of capital | < Cost of capital |
| Revenue growth? | High | Low |
| Margin expansion? | Yes | No |
| Cash runway? | Sufficient | Approaching zero |
| External financing 접근? | 쉬움 (VC, debt) | 어려움 |

**Real cases**:
- **Tesla**: 2013 인수 talks (Apple, Google) — eventually independent, vindicated
- **Twitter**: Elon 2022 $44B — FCF 의문 + non-monetary
- **Slack**: Salesforce 2020 $27B — growth + synergy

> Context (industry phase, capex ROIC, path to profitability) 가 결정. *Future expected FCF* 의 *PV* 가 *current FCF* 보다 중요.

</details>

### Q10. 면접 — *EBITDA 의 *valid* use*?

"EBITDA 가 나쁘면 왜 산업 표준?"

<details><summary>답</summary>

**EBITDA 가 *useful***:

1. **Acquisition valuation** — EV/EBITDA multiple, capital structure + tax neutral
2. **Capital structure 비교** — debt-heavy vs equity-heavy 의 operating quality
3. **International** — different tax + depreciation methods
4. **Bond covenant** — DSCR, Net Debt / EBITDA
5. **Industry benchmark** — peer 의 unified metric

**EBITDA 가 *invalid***:

1. *Capital-intensive* (telecom, utility) — capex 가 EBITDA 의 대부분
2. *Distressed* — restructuring 의 빈번
3. *Hyper-growth* — aggressive revenue recognition
4. *EBITDA 의 cousin* — Adjusted EBITDA, EBITDAR, EBITDA pre-SBC — 비교 어려움

**Modern best practice**:
1. EBITDA = starting point
2. Adjusted EBITDA 면 adjustment list critical examination
3. EBITDA → FCF bridge (capex, NWC, tax, interest)
4. Multiple metrics
5. Industry-specific

**Buffett's *Owner Earnings***:
- = NI + D&A − maintenance capex − ΔWC
- *진짜 FCF*

> EBITDA = imperfect but useful. *Capital structure + international + acquisition* 에 valid. 그러나 *FCF 의 대체 아닌 starting point*.

</details>
