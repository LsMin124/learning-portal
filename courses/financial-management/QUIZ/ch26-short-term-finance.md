# Ch 26 Short-Term Finance and Planning — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *Operating cycle* vs *Cash cycle*?

<details><summary>답</summary>

**Operating cycle** (영업주기):
$$= \text{Inventory period} + \text{AR period}$$
- 재고 매입 → 판매 → 회수까지

**Cash cycle** (현금주기):
$$= \text{Operating cycle} - \text{AP period}$$
- 현금 *지출* → 현금 *회수*까지 (현금 묶이는 기간)

**핵심**:
- AP period (매입채무 유예) 가 길수록 cash cycle ↓
- Cash cycle ↑ → 운전자본 투자 ↑ → 자금 필요 ↑
- Dell/Amazon: cash cycle *음수* (선수금 + AP 연장)

</details>

### Q2. *Flexible* vs *Restrictive* 단기 정책?

<details><summary>답</summary>

| | Flexible (보수적) | Restrictive (공격적) |
|--|--|--|
| 유동자산 | 多 | 少 |
| 현금/재고 | 高 | 低 |
| 신용 | 관대 | 엄격 |
| 단기차입 | 少 (장기 충당) | 多 |
| 위험 | 낮음 | 높음 |
| 수익성 | 낮음 | 높음 |

**Trade-off**:
- Flexible: 안전 (품절·부도 위험↓) but 유휴자산 → 수익성 ↓
- Restrictive: 수익성 ↑ but shortage 위험 ↑

→ 최적은 carrying cost = shortage cost 균형점.

</details>

### Q3. *Carrying cost* vs *Shortage cost*?

<details><summary>답</summary>

**Carrying cost (보유비용)**:
- 유동자산 보유 비용 (자본 기회비용, 보관, 진부화)
- 유동자산 ↑ → carrying ↑

**Shortage cost (부족비용)**:
- 유동자산 부족 비용
- *Order cost* (긴급 조달), *safety reserve cost* (품절, 거래중단, 신용상실)
- 유동자산 ↓ → shortage ↑

**최적**:
$$\text{Total} = \text{Carrying} + \text{Shortage} \to \min$$

- Flexible 정책 = carrying > shortage (보수적)
- Restrictive 정책 = shortage > carrying (공격적)

</details>

### Q4. 계산 — Operating / Cash Cycle

평균 재고 $50,000, COGS $300,000. 평균 AR $40,000, 매출 $400,000. 평균 AP $30,000.

(a) Inventory period? (b) AR period? (c) AP period? (d) Operating/Cash cycle?

<details><summary>답</summary>

**(a) Inventory period**:
$$= \frac{365 \times \text{평균재고}}{\text{COGS}} = \frac{365 \times 50,000}{300,000} = 60.8 \text{일}$$

**(b) AR period**:
$$= \frac{365 \times \text{평균AR}}{\text{매출}} = \frac{365 \times 40,000}{400,000} = 36.5 \text{일}$$

**(c) AP period**:
$$= \frac{365 \times \text{평균AP}}{\text{COGS}} = \frac{365 \times 30,000}{300,000} = 36.5 \text{일}$$

**(d) Cycles**:
- Operating cycle = 60.8 + 36.5 = **97.3 일**
- Cash cycle = 97.3 − 36.5 = **60.8 일**

**해석**: 현금이 약 61일간 묶임. 단축하려면 재고 회전↑, AR 회수↑, AP 유예↑.

</details>

### Q5. 계산 — Cash Budget

분기 초 현금 $20,000. 최소 유지 $10,000.
- Q1 매출 회수 $100,000, 지출 $130,000
- Q2 매출 회수 $150,000, 지출 $120,000

각 분기 말 현금 + 차입/상환 필요액?

<details><summary>답</summary>

**Q1**:
- 기초 $20,000 + 회수 $100,000 − 지출 $130,000 = **−$10,000**
- 최소 $10,000 유지 위해 차입: $10,000 − (−$10,000) = **$20,000 차입**
- Q1말 현금: $10,000 (최소)

**Q2**:
- 기초 $10,000 + 회수 $150,000 − 지출 $120,000 = $40,000
- 최소 $10,000 초과분 $30,000
- Q1 차입 $20,000 상환 → **$20,000 상환**
- Q2말 현금: $40,000 − $20,000 = $20,000

**해석**:
- 계절성 → Q1 차입, Q2 상환 (cash budget 의 핵심 용도)
- 누적 현금 부족 시점 미리 파악 → line of credit 준비

→ Q1: $20,000 차입. Q2: $20,000 상환.

</details>

### Q6. 계산 — Compensating Balance 실효이자

$100,000 대출, 명목 8%. 은행이 *compensating balance 20%* 요구 (대출금의 20% 예치).

실효이자율?

<details><summary>답</summary>

**실제 사용 가능액**:
- 대출 $100,000 − compensating balance $20,000 = **$80,000**

**이자 (전액 기준)**:
- $100,000 × 8% = $8,000

**실효이자율**:
$$= \frac{8,000}{80,000} = 10\%$$

**해석**:
- 명목 8% 지만 실효 *10%* (compensating balance 가 비용 ↑)
- 묶인 $20,000 은 사용 못 하나 이자는 전액 부담

**변형 — discount loan** (선이자):
- 이자 선공제 → 실제 수령 $92,000 → 실효 = 8,000/92,000 = 8.7%
- Compensating + discount 동시면 더 높음

→ Compensating balance 20% → 실효 10% (명목 8%보다 높음).

</details>

### Q7. 디버그 — "Cash cycle 은 무조건 짧게"

CFO: *"Cash cycle 을 최대한 0 이하로 만들자! 재고 최소, AR 즉시 회수, AP 최대 연장!"*

문제점?

<details><summary>답</summary>

**과도한 cash cycle 단축의 문제**:

**1. 재고 최소 → 품절 위험**:
- Stockout → 매출 상실, 고객 이탈
- Shortage cost ↑ (just-in-time 의 공급망 위험)

**2. AR 즉시 회수 → 매출 감소**:
- 엄격한 신용 → 고객 이탈 (경쟁사로)
- 신용 판매가 매출 driver (Ch 28)

**3. AP 최대 연장 → 관계 훼손 + 할인 포기**:
- 공급업체 관계 악화, 향후 조건 불리
- *Cash discount 포기* 비용 (2/10 net 30 → 연 37% 비용!)
- 신용등급 하락

**올바른 관점**:
- Cash cycle 단축은 *carrying vs shortage trade-off* 내에서
- 효율 (Dell) vs 관계·매출 균형
- 음수 cash cycle 은 *협상력* 있는 기업만 (Walmart, Amazon)

**유명**: Dell (음수 cash cycle, 주문생산) — 단 강한 brand/협상력 전제. 무리한 모방은 역효과.

→ 무조건 단축 X. Shortage cost, 매출 상실, 공급망·할인 비용 고려.

</details>

### Q8. 디버그 — 만기 매칭 오류

회사가 *영구 운전자본* (항상 필요한 재고)을 *30일 commercial paper* 로 계속 roll-over 조달.

위험은?

<details><summary>답</summary>

**Maturity mismatch 위험**:

**1. Rollover (차환) 위험**:
- 영구 자산을 단기 부채로 → 매 30일 차환
- 신용시장 경색 시 *차환 불가* → 유동성 위기

**2. 금리 위험**:
- 단기금리 급등 시 조달비용 ↑
- 영구 자산 수익은 고정 → 마진 압박

**3. 2008/SVB(2023) 교훈**:
- 단기 조달 + 장기 자산 = bank run 취약
- CP 시장 동결 (2008) → 차환 의존 기업 위기

**올바른 매칭 (maturity matching)**:
- *영구 운전자본* → *장기 자금* (장기부채/자본)
- *계절 운전자본* → *단기 자금* (CP, line of credit)

**Trade-off**:
- 단기 조달이 *싸다* (정상 yield curve) → 유혹
- 하지만 rollover/금리 위험 = restrictive 정책의 대가

→ 영구 자산을 단기 CP 로 = rollover + 금리 위험. 만기 매칭 위반.

</details>

### Q9. 면접 — *왜 음수 cash cycle 이 가능*하고 누가 달성하나?

<details><summary>답</summary>

**음수 cash cycle = 현금 회수 < 현금 지급** (공급업체 돈으로 운영):

**조건**:
1. **빠른 재고 회전** — JIT, 주문생산 (재고 period 짧음)
2. **즉시/선수금 회수** — 현금/카드 판매 (AR period ≈ 0)
3. **긴 AP 유예** — 협상력으로 공급업체 지급 연장

**달성 기업**:
- *Amazon* — 고객 즉시 결제, 공급업체 60일+ 후 지급
- *Dell* (전성기) — 주문생산, 부품은 외상
- *Walmart* — 회전 빠름 + 공급업체 협상력
- *Apple* — 선주문, 공급업체 장기 유예

**효과**:
- 운전자본이 *자금 공급원* (negative working capital)
- 성장이 현금 *창출* (성장할수록 공급업체 외상 ↑)
- 무이자 자금 → ROIC ↑

**전제 조건**:
- *협상력* (대형 구매자) — 공급업체에 조건 강제
- *브랜드/수요* — 선수금 가능
- 무리한 모방 → 공급망 악화, 품절

**위험**:
- 성장 둔화 시 운전자본 *역전* (현금 유출)
- 공급업체 부실화 (지나친 압박)

**철학**: 음수 cash cycle = 비즈니스 모델 + 협상력의 *결과*지, 목표 자체가 아님.

> 음수 cash cycle = 빠른 회전 + 선수금 회수 + 긴 AP. Amazon/Dell/Walmart (협상력·브랜드 전제). 공급업체 자금으로 운영, 성장이 현금 창출. 단 협상력 없으면 모방 불가, 성장둔화 시 역전 위험.

</details>

### Q10. 면접 — *운전자본 관리가 기업가치에 미치는 영향*?

<details><summary>답</summary>

**운전자본 → 기업가치 경로**:

**1. FCF 직접 영향**:
- $FCF = EBIT(1-t) + D\&A - CapEx - \Delta NWC$
- 운전자본 *증가* = 현금 유출 (FCF ↓)
- 효율적 관리 → ΔNWC ↓ → FCF ↑ → 가치 ↑

**2. ROIC 영향**:
- Invested capital = 고정자산 + 운전자본
- 운전자본 ↓ → invested capital ↓ → ROIC ↑

**3. 성장 자금**:
- 효율적 운전자본 → 내부 현금 → 성장 자금 (외부조달 ↓)
- 음수 cash cycle → 성장이 현금 창출

**4. 재무 위험**:
- 과도한 단기 조달 → rollover 위험
- 만기 매칭 → 유동성 안정

**실무 지표 (cash conversion 개선)**:
1. *DSO* (Days Sales Outstanding) ↓ — AR 회수 가속
2. *DIO* (Days Inventory Outstanding) ↓ — 재고 효율
3. *DPO* (Days Payable Outstanding) ↑ — AP 유예
4. CCC = DSO + DIO − DPO

**Trade-off (과도 최적화 위험)**:
- AR 너무 엄격 → 매출 ↓
- 재고 너무 적음 → 품절
- AP 너무 길게 → 공급업체 관계/할인

**사례**:
- PE 인수 후 *운전자본 최적화* (cash release)
- CFO KPI 에 CCC 포함

**거시**: 경기침체 시 운전자본 = 유동성 buffer (cash is king).

> 운전자본 관리 → FCF (ΔNWC), ROIC (invested capital), 성장자금, 재무위험. 개선: DSO↓/DIO↓/DPO↑ (CCC 단축). 단 매출·품절·공급업체 trade-off. PE 가 가치창출 lever 로 활용.

</details>
