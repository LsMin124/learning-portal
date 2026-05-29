# Ch 28 Credit and Inventory Management — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. 신용정책 *3 요소* + trade credit 이유?

<details><summary>답</summary>

**신용정책 3 요소**:
1. **Terms of sale** — 신용기간, cash discount, 결제수단
2. **Credit analysis** — 고객 신용도 평가 (5 Cs)
3. **Collection policy** — 회수 노력

**Trade credit (외상매출) 이유**:
- *매출 증대* (구매 편의 제공)
- *가격 차별* (실질 할인/유예로 고객별 차등)
- *정보 우위* (공급업체가 고객 신용 파악)
- *경쟁* (업계 관행)

</details>

### Q2. *5 Cs* of Credit?

<details><summary>답</summary>

| C | 의미 |
|--|--|
| **Character** | 상환 *의지* (신용 이력, 평판) |
| **Capacity** | 상환 *능력* (현금흐름) |
| **Capital** | 재무 건전성 (자기자본) |
| **Collateral** | 담보 |
| **Conditions** | 경제·산업 상황 |

**Credit scoring**:
- Altman Z-score (부도 예측): Z = 1.2X₁+1.4X₂+3.3X₃+0.6X₄+1.0X₅
- Z < 1.81 위험, Z > 2.99 안전
- 현대: ML, FICO

</details>

### Q3. *EOQ* 모델 + Baumol 과의 관계?

<details><summary>답</summary>

**EOQ (경제적 주문량)**:
$$Q^* = \sqrt{\frac{2DF}{CC}}$$
- D = 연간 수요, F = 주문비용, CC = 단위 보유비용
- 평균 재고 = Q*/2, 주문 횟수 = D/Q*

**Baumol (현금)** 과 동일 형태:
$$C^* = \sqrt{\frac{2TF}{K}}$$

→ *같은 trade-off 구조*: 거래비용(주문/매매) vs 보유비용(carrying/기회).
→ 현금 = "재고로서의 현금" (Baumol 이 EOQ 를 현금에 적용).

**최적 조건**: 총 주문비용 = 총 보유비용.

</details>

### Q4. 계산 — 할인 포기 비용

다음 신용조건의 할인 포기 실효 연이자율:
(a) 2/10 net 30
(b) 1/15 net 45
(c) 3/10 net 60

<details><summary>답</summary>

**공식**:
$$\text{실효} = \left(1 + \frac{d}{1-d}\right)^{\frac{365}{N-D}} - 1$$

**(a) 2/10 net 30** (N−D = 20):
$$= \left(1 + \frac{0.02}{0.98}\right)^{365/20} - 1 = (1.0204)^{18.25} - 1 \approx 44.6\%$$

**(b) 1/15 net 45** (N−D = 30):
$$= \left(1 + \frac{0.01}{0.99}\right)^{365/30} - 1 = (1.0101)^{12.17} - 1 \approx 13.0\%$$

**(c) 3/10 net 60** (N−D = 50):
$$= \left(1 + \frac{0.03}{0.97}\right)^{365/50} - 1 = (1.0309)^{7.3} - 1 \approx 25.0\%$$

**해석**:
- (a) 가장 비쌈 (44.6%) → 할인 꼭 받기
- (b) 13% → 차입비용보다 높으면 할인
- 할인율 ↑, (N−D) ↓ → 포기 비용 ↑

→ 할인 포기 = 비싼 차입. 차입비용과 비교해 결정.

</details>

### Q5. 계산 — EOQ

연간 수요 D = 10,000 단위. 주문당 비용 F = $50. 단위당 연간 보유비용 CC = $4.

(a) EOQ? (b) 평균 재고? (c) 주문 횟수? (d) 총 재고비용?

<details><summary>답</summary>

**(a) EOQ**:
$$Q^* = \sqrt{\frac{2DF}{CC}} = \sqrt{\frac{2 \times 10,000 \times 50}{4}} = \sqrt{250,000} = 500 \text{단위}$$

**(b) 평균 재고**:
$$= \frac{Q^*}{2} = \frac{500}{2} = 250 \text{단위}$$

**(c) 주문 횟수**:
$$= \frac{D}{Q^*} = \frac{10,000}{500} = 20 \text{회/년}$$

**(d) 총 재고비용**:
- 주문비용: 20 × $50 = $1,000
- 보유비용: 250 × $4 = $1,000
- 총: **$2,000** (두 비용 같음 = EOQ 최적 ✓)

→ EOQ 500, 평균 250, 20회, 총비용 $2,000.

</details>

### Q6. 계산 — 신용 정책 변경 NPV

현재 현금판매 100단위/월. 신용판매 전환 시 110단위/월 예상. 가격 $50, 단위 변동비 $30. 월 할인율 1%. (부도·회수비용 무시 가정)

신용 전환 가치?

<details><summary>답</summary>

**현금판매 → 신용판매 (한 달 회수 지연 가정)**:

**초기 비용 (전환 시점)**:
- 기존 고객 매출 회수 지연: 현금 못 받음 → $PQ = 50 × 100 = $5,000$
- 신규 판매 변동비: $v(Q'-Q) = 30 × (110-100) = $300$
- 총 초기 비용: $5,000 + $300 = $5,300

**영구 추가 현금흐름 (매월)**:
- 신용판매 마진: $(P-v)Q' = (50-30) × 110 = $2,200/월$

**NPV**:
$$NPV = -5,300 + \frac{2,200}{0.01} = -5,300 + 220,000 = +\$214,700$$

**해석**:
- NPV ≫ 0 → 신용 전환 *유리*
- 단 부도율, 회수비용 차감 필요 (여기선 무시)
- 핵심: 매출 증가 마진의 영구 가치 vs 회수 지연 일회성 비용

→ NPV ≈ +$214,700 (부도 무시 시). 신용 전환.

</details>

### Q7. 디버그 — 할인 포기 결정

구매팀: *"2/10 net 30 조건인데, 우리는 현금이 부족하니 할인 포기하고 30일에 결제하자. 2% 아끼려고 빚낼 필요 없잖아."*

문제점?

<details><summary>답</summary>

**오류 — 할인 포기 비용 = 연 44.6%**:

**1. 2% 의 진짜 비용**:
- 할인 포기 = 20일 더 쓰는 대가로 2%
- 연율 환산: (1+0.02/0.98)^(365/20)−1 ≈ **44.6%**
- → 사실상 연 44.6% 이자로 차입하는 셈

**2. 차입과 비교**:
- 은행 단기차입 ≈ 6-10%
- 44.6% ≫ 10% → *차입해서라도 할인 받는 게 유리*

**3. 올바른 결정**:
- 현금 부족 → *은행 차입 (10%)* → 할인 받기 (44.6% 절감)
- 순이득 = 44.6% − 10% ≈ 34.6%

**4. 예외 (할인 포기가 맞는 경우)**:
- 차입 불가 (신용 한도 소진)
- 차입비용 > 44.6% (극단적 부실)
- 공급업체가 연체 묵인 (실질 기간 연장)

**현실**: "stretching payables" (연체)는 관계·신용 훼손.

→ 할인 포기 = 연 44.6% 차입. 은행차입(10%)해서 할인 받는 게 유리. "2%만 아낀다"는 착각.

</details>

### Q8. 디버그 — JIT 맹신

운영팀: *"JIT 로 재고를 거의 0 으로 줄였다. Carrying cost 제로! 완벽한 효율!"*

위험은?

<details><summary>답</summary>

**JIT 의 숨은 위험 (carrying cost 만 본 오류)**:

**1. Shortage cost 증가**:
- 재고 0 → *품절* 위험 ↑
- 공급 차질 → 생산 중단, 매출 상실
- EOQ: carrying ↓ 했지만 shortage/ordering ↑

**2. 공급망 위험 (2020 교훈)**:
- 코로나/반도체 부족 → JIT 기업 생산 마비
- 단일 공급처 의존 → fragility
- 자연재해, 지정학 (수에즈 운하, 우크라이나)

**3. 협상력·물량 할인 상실**:
- 소량 빈번 주문 → 단가 ↑, 물량 할인 ↓
- 주문 비용 (F) ↑

**4. 품질·리드타임 의존**:
- 공급업체 품질·납기에 완전 의존
- 한 곳 실패 → 전체 중단

**재평가 (현대)**:
- JIT → *JIC (Just-In-Case)* 일부 회귀
- *Resilience* vs efficiency trade-off
- 핵심 부품 buffer stock, 공급처 다변화 (China+1)

**올바른 관점**:
- JIT 는 *안정 공급망* 전제 (Toyota 의 협력사 생태계)
- Carrying cost 절감 ↔ shortage/공급망 위험 trade-off

→ Carrying cost만 봄. Shortage·공급망 위험 (2020 코로나) 무시. JIT는 안정 공급망 전제, resilience trade-off.

</details>

### Q9. 면접 — *외상매출(AR)이 너무 많을 때 어떻게 진단·개선*?

<details><summary>답</summary>

**진단 (AR 과다 분석)**:

**1. 지표 측정**:
- *ACP* (= AR/일평균매출) — 업계 평균 대비
- *DSO* 추세 (악화 여부)
- *Aging schedule* — 연체 비중 (60일+ 급증?)

**2. 원인 규명**:
- 신용정책 too loose (관대한 terms)
- Credit analysis 부실 (5 Cs 평가 미흡)
- Collection 노력 부족
- 매출 압박 (영업이 신용 남발)
- 고객 부실 (경기·산업)

**개선 방안**:

**A. Terms 조정**:
- Cash discount 도입/강화 (2/10 net 30)
- 신용기간 단축

**B. Credit analysis 강화**:
- 5 Cs, credit scoring
- 신용한도 설정, 모니터링

**C. Collection 개선**:
- Aging 기반 체계적 독촉
- Collection agency, factoring (즉시 현금화)

**D. 구조적**:
- AR financing (담보 차입)
- Trade credit insurance
- 영업 인센티브를 *회수* 까지 연동

**Trade-off (과도 긴축 주의)**:
- 너무 엄격 → *매출 상실* (고객 이탈)
- 최적 = 추가 마진 vs 부도·회수비용 (Ch 28 NPV)

**사례**: PE 인수 후 AR 최적화 (DSO 단축 → cash release).

> AR 과다 진단: ACP/DSO/aging (업계 대비). 원인: terms 관대, credit analysis 부실, collection 약함. 개선: cash discount, 5 Cs 강화, aging 독촉, factoring. 단 과도 긴축 = 매출 상실 (마진 vs 부도비용 trade-off).

</details>

### Q10. 면접 — *운전자본 3대 항목(현금·AR·재고) 관리의 공통 원리*?

<details><summary>답</summary>

**공통 원리 — 모두 *carrying vs shortage(거래) trade-off***:

| 항목 | Carrying cost | Shortage/거래 cost | 모델 |
|--|--|--|--|
| 현금 | 기회비용 | 거래비용 (증권 매매) | Baumol/Miller-Orr |
| 재고 | 보관·진부화 | 품절·주문 | EOQ |
| AR | 자본묶임·부도 | 매출 상실 | 신용정책 NPV |

**1. 동일한 최적화 구조**:
- 보유 ↑ → carrying ↑, shortage ↓
- 보유 ↓ → carrying ↓, shortage ↑
- 최적 = 총비용 최소 (한계비용 균형)

**2. 같은 수학 (EOQ/Baumol)**:
- Q* = √(2DF/CC), C* = √(2TF/K) — 동일 형태
- "lumpy" 보충의 trade-off

**3. 공통 목표**:
- *유동성 확보* vs *기회비용 최소화*
- Cash cycle 단축 (Ch 26) — 세 항목 통합

**4. 공통 함정**:
- 한 비용만 보기 (carrying 만, 또는 shortage 만)
- 불확실성 무시 (safety stock/buffer 필요)
- 과도 최적화 → 매출·공급 차질

**5. 통합 관점 (운전자본)**:
- $\Delta NWC$ → FCF 영향
- CCC = DSO + DIO − DPO
- 세 항목 동시 관리 (TMS, ERP)

**현대 진화**:
- AI 수요예측 → safety stock 최적화
- 실시간 visibility (통합 dashboard)
- 공급망 resilience (JIT → JIC)

> 현금·AR·재고 = 동일한 carrying vs shortage trade-off. EOQ/Baumol 같은 수학 (√2·거래량·고정비/보유비). 공통 목표: 유동성 vs 기회비용. 함정: 한 비용만 보기, 불확실성 무시. 통합: CCC 단축, ΔNWC→FCF.

</details>
