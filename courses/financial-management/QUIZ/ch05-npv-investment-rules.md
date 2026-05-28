# Ch 5 NPV and Other Investment Rules — 퀴즈

> 10 문항 (개념 2 / 계산 4 / 디버그 3 / 면접 1).

### Q1. *5 method* — 각 의 *primary flaw*?

NPV, Payback, Discounted Payback, IRR, PI?

<details><summary>답</summary>

| Method | Primary flaw |
|--|--|
| **NPV** | (gold standard) Discount rate 추정 의 *주관* |
| **Payback** | Time value 무시, post-payback 무시, 임의 cutoff |
| **Discounted Payback** | Post-payback 무시, 임의 cutoff |
| **IRR** | Multiple IRR, no IRR, financing reverse, scale/timing |
| **PI** | Mutual exclusive 의 scale |

**Modern best practice**:
- *NPV* = primary
- *IRR + Payback* = communication
- *Sensitivity + scenario + Monte Carlo* = risk
- *Real options* = flexibility

</details>

### Q2. *Conventional vs Non-conventional*

(a) -$100, $30, $30, $30, $30, $30
(b) -$100, $50, $50, $50, -$30
(c) -$200, -$100, $50, $50, $200
(d) $1000, -$1100 (loan)

어느 게 *non-conventional* + *왜*?

<details><summary>답</summary>

| | Sign | Conventional? |
|--|--|--|
| (a) | -, +, +, +, +, + | ✓ |
| (b) | -, +, +, +, - | ✗ (2 sign change) |
| (c) | -, -, +, +, + | ✓ (1 sign change) |
| (d) | +, - | *Financing*, 역방향 |

**Implications**:
- (a), (c): IRR 1 개
- (b): Multiple IRR 가능 (strip mine)
- (d): IRR > hurdle → ***reject***

**Real non-conventional examples**:
- Strip mining cleanup
- Nuclear plant decommissioning
- Pharma late R&D milestone
- Real estate renovation 중간

</details>

### Q3. 계산 — NPV/IRR/PI/Payback

Project:
- Initial: $-100K
- Year 1-3: $40K each
- Year 4: $30K
- r = 12%

각 method 계산?

<details><summary>답</summary>

**(a) NPV**:
$$NPV = -100 + \frac{40}{1.12} + \frac{40}{1.12^2} + \frac{40}{1.12^3} + \frac{30}{1.12^4}$$
$$= -100 + 35.71 + 31.89 + 28.47 + 19.07 = \$15.14K$$

**(b) IRR**:
- At 17%: NPV ≈ $1.5K
- At 18%: NPV ≈ $-0.5K
- → IRR ≈ **17.75%**

**(c) PI**:
$$PI = \frac{115.14}{100} = 1.15$$

**(d) Payback**:
- Year 1-2 cumul: $80K
- Year 3 needed: $20K of $40K
- Payback = **2.5 years**

**(e) Discounted Payback** at 12%:
- Year 3 cumul PV: $96.07
- Year 4 needed: $3.93 of $19.07
- Discounted Payback = **3.21 years**

**Decision (all)**: Accept (NPV > 0, IRR > 12%, PI > 1, fast payback).

</details>

### Q4. 디버그 — *Multiple IRR* 의 결정

Strip mining:
- Year 0: $-1000
- Year 1: $6000
- Year 2: $-11,000
- Year 3: $6000

(a) IRR?
(b) Hurdle 10%, 20%, 30% 의 결정?

<details><summary>답</summary>

**(a) IRR**:
해: **IRR_1 ≈ 0%, IRR_2 ≈ 100%** 부근.

**NPV at 다양한 r**:

| r | NPV |
|--|--|
| 0% | $0 |
| 10% | $63 |
| 50% | $130 |
| 100% | $0 |
| 200% | -$222 |

→ *Dome-shaped*. IRR 두 곳.

**(b) Decision**:

| Hurdle | NPV | Decision |
|--|--|--|
| 10% | $63 | Accept |
| 20% | $90 | Accept |
| 50% | $130 | Accept |
| 100% | $0 | Indifferent |
| 200% | -$222 | Reject |

**IRR 의 결정 불가** — 두 IRR 모두 발생.

**Solution**:
- *NPV* 가 *명확*
- *MIRR* (single value)

**Famous case**:
- Nuclear power plant — initial + operating + decommissioning
- Mining — initial + extraction + reclamation
- Oil offshore — drilling + production + abandonment

→ *Cleanup cost* 가 *non-conventional* 만듦.

</details>

### Q5. 디버그 — *Mutually Exclusive scale problem*

| | A | B |
|--|--|--|
| Initial | $-10K | $-100K |
| Year 1 | $20K | $150K |
| IRR | 100% | 50% |
| NPV (r=10%) | $8.2K | $36.4K |

(a) IRR vs NPV ranking?
(b) Correct decision?
(c) Incremental IRR?

<details><summary>답</summary>

**(a) Ranking**:
- IRR: A (100%) > B (50%)
- NPV: B ($36.4K) > A ($8.2K)

**(b) B 채택**.

**이유**:
- NPV = *shareholder wealth 증분*
- IRR 100% 의 *small project* < IRR 50% 의 *large project*
- *Magnitude* 가 중요

**Analogy**:
- $10 saving 의 50% return ($5) vs $1000 saving 의 20% return ($200)
- *Dollar* 가 *percentage* 보다 중요

**(c) Incremental IRR**:

Incremental cash flow (B - A):
- Year 0: $-90K
- Year 1: $130K

Incremental IRR = $130/90 - 1 = **44.4%**

→ Incremental IRR (44.4%) > hurdle (10%) → ***B 채택*** (NPV 일치).

**Lesson**:
- *Mutually exclusive* 에서 *IRR ranking 무시*
- *NPV* 또는 *Incremental IRR* 사용

</details>

### Q6. 디버그 — *Loan IRR* 의 *reverse*

회사 *short-term loan*:
- Year 0: +$10,000
- Year 1: -$10,500
- Year 2: -$1000

(a) IRR?
(b) Hurdle 5%, 10%, 15% 의 결정?

<details><summary>답</summary>

**(a) IRR**:
$$0 = 10000 - \frac{10500}{1+r} - \frac{1000}{(1+r)^2}$$
→ **IRR ≈ 9.7%**

**(b) Decision** — *Financing reverse*:

| Hurdle | NPV | Decision (financing) |
|--|--|--|
| 5% | -$907 | Reject |
| 10% | $74 | Accept |
| 15% | $850 | Accept |

**왜 *역전***:
- *Investing*: 우리가 *cash 제공*. IRR = *받는 yield*
- *Financing*: 우리가 *cash 받음*. IRR = *우리 cost*

→ Financing 에서 *cost < hurdle* 면 *유리*.

**현실의 *typical***:
- Corporate borrowing — effective interest < market rate 면 유리
- Bond issue — coupon < required yield 면 유리

**Lesson**:
- *IRR rule* 의 *direction sensitivity*
- *NPV rule* 의 *direction agnostic*

</details>

### Q7. 계산 — *Capital Rationing PI*

Budget $200M:

| | Cost | NPV | PI |
|--|--|--|--|
| A | $50M | $30M | 1.6 |
| B | $80M | $40M | 1.5 |
| C | $40M | $35M | 1.875 |
| D | $30M | $25M | 1.833 |
| E | $100M | $60M | 1.6 |

(a) NPV-only ranking?
(b) PI ranking + budget 최적?

<details><summary>답</summary>

**(a) NPV ranking**: E > B > C > A > D

**(b) PI ranking**: C > D > A = E > B

**Budget $200M optimal**:
- *C + D + A + B* = $200M, **NPV $130M** ★

**대안**:
- *C + E + A* = $190M, NPV $125M
- *C + E + D* = $170M, NPV $120M

**Optimization**:
- *Linear programming* — exact
- *Integer programming* — discrete
- *Heuristic* — PI ranking + adjustment

**기업 예**:
- 일반 *capital allocation committee* — PI + strategic fit
- *Berkshire* — *opportunistic* (cash patient)
- *PE firm* — IRR 목표 (15-25%)

**Lesson**:
- *Unrestricted*: NPV
- *Restricted*: PI + LP

</details>

### Q8. 디버그 — *Reinvestment assumption*

5 year project, IRR 30%. 정말 *연간 30% return* 으로 *reinvest 가능*?

<details><summary>답</summary>

**IRR 의 *implicit assumption***:

> 모든 *interim cash flow* 가 *IRR 자체* 로 *reinvest*.

**현실**:
- *Hurdle rate* 가 10% — *30% 의 평균 reinvest 불가*
- *Limit* 의 *cash 잡을 능력*

**NPV 의 *implicit assumption***:

> Interim cash flow → *discount rate (WACC)* 으로 reinvest.

- WACC = *firm average* — *지속 가능*
- → NPV 의 *reinvestment* 가 *more reasonable*

**MIRR 의 *해결***:
- *Explicit reinvestment rate* (보통 WACC)
- → MIRR < IRR

**예** — IRR 30% project at WACC 10%:
- *MIRR* = *18-22%* 부근
- → *real-world expected return*

**Buffett's view**:
- *IRR obsession* 의 함정
- *NPV* + *quality* + *durable competitive advantage*
- *PE firm IRR target* 의 *creative engineering*

</details>

### Q9. 디버그 — *PE firm IRR 의 manipulation*

PE — Reported IRR 30% (5 years). *진짜* 30%?

<details><summary>답</summary>

**PE IRR 의 *common manipulation 5***:

**1. Subscription line / Capital call timing** — IRR clock 늦게 시작 → 부풀림
**2. Early distribution recycling** — Quick exit, 재 commit → IRR 부풀림
**3. Mark-to-fantasy valuation** — Unrealized IRR optimistic
**4. Fund vs deal-level** — Gross > Net (fee 후)
**5. Selection bias** — Winner only, loser quiet write-off

**Better metrics**:

| Metric | 의미 |
|--|--|
| *MOIC* | Multiple on Invested Capital |
| *DPI* | Distribution to Paid-In (realized) |
| *TVPI* | Total Value to Paid-In |
| *PME* | Public Market Equivalent (S&P 500 비교) |

**Modern best practice**:
- *IRR + MOIC* 병기
- *PME* (Kaplan-Schoar) alpha 측정
- *ILPA template* 의 standardization

**Famous critique**:
- *Kaplan-Schoar (2005)*: PE 의 *median alpha 후 fee ≈ zero*
- *Phalippou (2020)*: "PE net return ≈ S&P 500, fee 훨씬 높음"

> *IRR* = useful but manipulable. *Multiple metrics + DD* 가 defense.

</details>

### Q10. 면접 — *Why NPV despite IRR popularity*?

"IRR 이 더 popular 한데, *왜 academic 은 NPV*?"

<details><summary>답</summary>

**IRR popularity**:

1. **Percentage** — 직관, 의사 소통 쉬움
2. **No need for r** — discount rate 불필요
3. **Hurdle comparison** — simple rule
4. **Industry convention** — RE, PE 의 standard

**NPV academic preference**:

1. **Dollar value** — *shareholder wealth* 직접
2. **Additive** — projects 합산
3. **Mutual exclusive** — correct ranking
4. **Conventional + non-conventional** robust
5. **Reinvestment at WACC** — 현실적
6. **Financing direction** agnostic

**Modern compromise**:

- *NPV + IRR + Payback* 의 *3 종 dashboard*
- *Sensitivity analysis*
- *Real options* (Ch 22)
- *Decision tree*

**Industry primary**:

| Industry | Primary |
|--|--|
| Real estate | IRR (convention) |
| Private equity | IRR + MOIC |
| Public corporate | NPV + IRR |
| Pharma | DCF + decision tree |
| Mining | NPV + real option |
| Tech VC | Revenue multiple |

**Quotes**:
- *Brealey-Myers*: *"NPV is the only criterion that is consistent with maximizing shareholder wealth."*
- *Damodaran*: *"NPV is right in theory; IRR is right in practice."*

**Bottom line**:
- *Theory*: NPV
- *Practice*: NPV + IRR
- *Best*: Multiple + sensitivity + judgment

</details>
