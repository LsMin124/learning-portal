# Ch 1 Introduction to Corporate Finance — 퀴즈

> 10 문항 (개념 4 / 계산 1 / 디버그 2 / 면접 3).

### Q1. 재무의 3 가지 질문

각 질문 + 해당하는 책의 *Part*?

<details><summary>답</summary>

1. **Capital budgeting** — "어떤 long-term asset 에 투자?" → Part II (Ch 4-9)
2. **Capital structure** — "Debt vs equity 비율?" → Part IV (Ch 14-19)
3. **Working capital management** — "단기 cash 관리?" → Part VII (Ch 26-28)

이 책 전체가 이 3 질문 의 *deep dive*.

</details>

### Q2. Corporation vs Partnership

같은 회사를 corporation 으로 vs partnership 으로 — *5 가지 차이*?

<details><summary>답</summary>

| | Partnership | Corporation |
|--|--|--|
| Liability | Unlimited (general) | Limited (주식 가격) |
| Life | 파트너 의존 | Perpetual |
| Tax | Pass-through (personal) | 이중 과세 |
| Transfer | 어려움 | 주식 양도 자유 |
| Capital | 파트너 자산 합 | 무제한 (시장) |

**왜 corporation 이 지배적**: *capital 조달 무제한* + *limited liability* + *perpetual life*. 대가는 *이중 과세* + *agency cost*.

</details>

### Q3. Cash flow vs Accounting income

다음 각각이 *cash flow* 인가 *accounting only* 인가?

| 항목 | Cash? Accounting? |
|--|--|
| 매출 1000, 외상 500 | ? |
| 감가상각비 200 | ? |
| 이자 지급 50 | ? |
| 자산 매입 (capex) 800 | ? |
| 배당 지급 100 | ? |

<details><summary>답</summary>

| 항목 | Cash? | 설명 |
|--|--|--|
| 매출 1000, 외상 500 | Cash 500 (현금 매출만) | 외상은 수금 시 cash |
| 감가상각비 200 | Cash X | 이미 자산 매입 시 cash 지출 |
| 이자 지급 50 | Cash 50 outflow | Financing activity |
| Capex 800 | Cash 800 outflow | Investing activity |
| 배당 100 | Cash 100 outflow | Financing activity |

> Cash is fact. Profit is opinion.

</details>

### Q4. Cash flow 의 3 요소

A, B 두 투자 — 어느 게 더 가치 큰가?

| | A | B |
|--|--|--|
| 1년 후 cash flow | $1100 확실 | $1500 (50% $2000, 50% $1000) |
| Required return | 10% | ? |

<details><summary>답</summary>

**A 의 PV**: $1100 / 1.10 = $1000

**B 의 expected value**: 0.5 × $2000 + 0.5 × $1000 = $1500

**B 가 risky** → required return > 10% (예: 20%):
- $1500 / 1.20 = $1250

**비교**: A $1000 vs B $1250. B 우세 (가정 하).

**핵심 원리**:
1. *Identification* — A, B 모두 cash flow
2. *Timing* — 같은 1 년 후
3. *Risk* — A 확실, B 위험 → 다른 discount rate

→ *Risk-adjusted PV* 가 정답.

</details>

### Q5. 디버그 — Agency cost 진단

CEO 가 $500M 으로 *underperforming firm* 인수. 인수 후 firm size 2배, CEO 보수 30% 인상. 그러나 *combined firm stock price* 발표 후 *15% 하락*.

이 결정의 *agency cost* + monitoring 방법?

<details><summary>답</summary>

**Agency cost 의 classic — Empire building**:
- CEO 가 *주주 부 하락에도 본인 이익* (compensation, power, prestige)
- *Negative NPV merger* 의 흔한 동기

**Monitoring 메커니즘**:
1. **Board** — Independent director 비율 ↑, merger 의 *independent valuation*
2. **Compensation** — Stock option / RSU, performance metric, clawback
3. **Activism** — Carl Icahn 같은 *board seat* 요구
4. **Takeover threat** — 주가 하락 시 hostile takeover
5. **Disclosure** — Merger rationale, fairness opinion

**Modern trends**:
- *Stewardship* — BlackRock, Vanguard 의 engagement
- *ESG ratings* 의 압력
- *Activist + social media*

</details>

### Q6. 디버그 — IPO 시점

스타트업 founder, Series D ($10B valuation). IPO 시점?

<details><summary>답</summary>

**옵션 별 trade-off**:

**A — 지금 IPO**:
- Pro: liquidity, brand 신뢰, M&A currency
- Con: SOX cost, quarterly pressure, short-termism

**B — 1년 후 IPO**:
- Pro: 더 큰 valuation, operating maturity
- Con: market window 닫힐 위험

**C — Private 유지**:
- Pro: SOX 회피, long-term, founder control
- Con: liquidity 한계

**Modern trend** — *staying private longer*:
- IPO age 1999 ~4년 → 2020s ~10년
- *Stripe, OpenAI, SpaceX* 수십 billion valuation 의 private

**결정 핵심**:
- Capital needs, liquidity needs, strategic timing, market conditions, founder control

**Dual-class stock** 의 *founder control* 보존.

</details>

### Q7. 면접 — *왜 corporation 의 이중 과세에도 dominant*?

"이중 과세가 비용인데 왜 LLC 가 대체 안?"

<details><summary>답</summary>

LLC 의 *limitation*:

1. **Capital raising scale**: LLC publicly trade 불가, IPO 위해 전환 필요
2. **Investor preference**: 기관 투자자가 stock 보유 표준
3. **M&A currency**: stock 으로 지불 — corporation 의 도구
4. **Employee stock option**: ISO tax benefit — corporation only
5. **Going public**: IPO 가 founder/VC exit 표준
6. **Brand + signaling**: "Inc." 의 credibility

**현실의 distribution**:
- Small: LLC dominant
- Large + growth: C-Corp
- Public: 100% C-Corp

**이중 과세 *완화***:
- Retained earnings (배당 안 함)
- Buyback (capital gain)
- S-Corp (100 shareholder 이하 pass-through)

> *이중 과세 는 비용*. 그러나 *대규모 capital + M&A + employee stock + IPO* 의 가치가 더 큼.

</details>

### Q8. 면접 — *ESG investing 의 valuation 영향*?

"ESG 가 *부 극대화* 와 충돌 아닌가?"

<details><summary>답</summary>

**Friedman (1970)** view: *Business 의 사회적 책임 = 이익 극대화*.

**현대 view**: *Long-term shareholder value* = *stakeholder 보호* 와 결국 일치.

**Cost side**:
- Carbon tax, litigation risk, brand damage, regulation, stranded assets

**Benefit side**:
- Lower cost of capital (green finance), talent retention, customer loyalty, risk mitigation

**Academic evidence**:
- Friede et al. 2015 — *non-negative* ESG-performance 관계
- Edmans 2011 — *employee satisfaction* → 4% annual alpha

**산업**:
- BlackRock 2018 — ESG integration
- Business Roundtable 2019 — stakeholder capitalism
- 2022~ anti-ESG backlash (Florida, Texas)

> ESG = *long-term shareholder value 의 일부*. *Materiality* (어떤 ESG가 어떤 industry 의 cash flow 영향) 가 핵심.

</details>

### Q9. 면접 — *Tech 회사의 dual-class stock*?

"Founder 가 10x voting power — agency problem 강화?"

<details><summary>답</summary>

**Dual-class structure**:
- Class A (founder): 10 vote/share
- Class B (public): 1 vote/share

**예**: Google (2004), Facebook (2012), Snap (2017, 0 vote public).

**찬성**:
- Long-term vision (Bezos, Musk)
- Hostile takeover 방어
- Founder skill 보존

**반대**:
- Agency problem 극단
- No accountability
- Entrenchment

**실제 사례**:
- *Success*: Google, Facebook
- *Failure*: WeWork (Adam Neumann), Snap (-50% 5년)

**Index inclusion**:
- S&P 500 2017 부터 *new dual-class 차단*

**Sunset clause** — 시간 제한 (Pinterest 20년), ownership-based, event-based.

> *Founder vision* 가치 + *agency cost* trade-off. *Sunset clause* 가 modern best practice.

</details>

### Q10. 면접 — *SOX 의 *실제* effectiveness*?

"SOX 후에도 Theranos, FTX — 효과?"

<details><summary>답</summary>

**SOX 의 핵심**:
1. CEO/CFO personal certification
2. Internal control documentation + audit
3. Independent audit committee
4. PCAOB

**Effectiveness — 정량적**:
- 2003-2010: restatement 점진 감소
- Material weakness disclosure 의 deterrence

**SOX 의 *scope 한계***:
- **Theranos** (2018) — *Private company* — SOX 적용 X
- **FTX** (2022) — *Crypto* — regulatory gap
- **Wirecard** (2020) — *Germany* — SOX jurisdiction 외

**SOX 의 *implementation 한계***:
- *Check-box compliance* vs *substantive*
- *Auditor independence* — Big 4 의 consulting 회피 부족
- *Section 404 cost* — small company 부담

**Modern 보완**:
- *Dodd-Frank* — whistleblower bounty
- *Cyber security disclosure* (SEC 2023)
- *Crypto framework* — 진화 중

> SOX 는 *fraud zero* 의 *불가능 목표* 가 아닌, *baseline accountability* 의 *raise*. *Theranos, FTX* 는 *scope 밖*. *Enforcement + whistleblower + 새 영역 framework* 가 *extension*.

</details>
