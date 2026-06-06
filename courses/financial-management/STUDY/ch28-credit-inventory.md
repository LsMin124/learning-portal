# Chapter 28: Credit and Inventory Management — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 28** (책 p.863~894).
> 28장은 *신용 + 재고 관리* — 신용정책, 5 Cs, EOQ, JIT.

이 장의 *지적 무게중심*:
1. **Credit policy** — terms, analysis, collection
2. **Cash discount** — 할인 포기 비용
3. **신용 의사결정** — NPV of granting credit
4. **5 Cs** — 신용 분석
5. **Inventory** — EOQ, reorder, JIT

---

## §0 도입 — *외상과 재고, 묶인 현금의 두 얼굴*

> **핵심 한 문장**: 매출채권(외상)과 재고는 둘 다 *현금을 묶어두는 유동자산 투자* — 26장의 *carrying ↔ shortage* 트레이드오프가 그대로 적용된다. 외상엔 "*할인 포기 = 연 44% 차입*"이라는 숨은 비용이, 재고엔 *EOQ* 라는 최적 주문량이 핵심.

28장은 두 자산을 나란히 다룬다:

1. **신용(외상) 정책** (§1–5): terms of sale + 신용분석 + 회수. *2/10 net 30* 에서 할인을 포기하면 연 **44.6%** 짜리 차입과 같다 — 그래서 보통 할인을 받는다. 신용을 *줄지 말지* 는 매출 증가 마진과 부도·회수 비용을 견주는 NPV 문제이고(figure 28.1 의 비용 트레이드오프), 상대의 신용도는 *5 Cs* 로 가린다.
2. **재고 관리** (§6–8): 재고도 *carrying(보유)* 과 *restocking/shortage(주문·부족)* 의 합이 최소인 점이 최적 — 그게 *EOQ* $Q^*=\sqrt{2DF/CC}$(figure 28.3). 재고는 톱니처럼 소진·재주문되며 평균은 $Q/2$(figure 28.4), 불확실성엔 *reorder point + safety stock* 으로 대비한다(figure 28.5). 가치별 *ABC*(figure 28.2)와 *JIT* 가 현대 기법.

관통하는 명제: **외상도 재고도 "더 들면 carrying, 덜 들면 shortage" — 최적은 둘의 합이 최소인 지점이다.**

---

## §1 신용정책 (Credit Policy)

### §1.1 세 요소

| 요소 | 내용 |
|--|--|
| *Terms of sale* | 신용기간, 할인, 수단 |
| *Credit analysis* | 신용도 평가 |
| *Collection policy* | 회수 노력 |

### §1.2 외상매출 (Trade credit) 이유

- *매출 증대* (구매 편의)
- *가격 차별* (실질 할인/유예)
- *정보* (공급업체가 고객 신용 파악)
- *재고 관리* (소매에 위험 전가)

---

## §2 Terms of Sale + Cash Discount

### §2.1 표기

> *2/10 net 30* = 10일 내 2% 할인, 아니면 30일 내 전액.

- *Cash discount* — 조기 결제 할인 (2%)
- *Discount period* — 할인 기간 (10일)
- *Credit period* — 신용 기간 (30일)

### §2.2 할인 포기 비용 (핵심)

> 할인을 *포기*하면 = 비싼 차입.

$$\text{실효 연이자} = \left(1 + \frac{d}{1-d}\right)^{\frac{365}{N-D}} - 1$$

- d = 할인율, N = credit period, D = discount period

**2/10 net 30 예시**:
- $\left(1 + \frac{0.02}{0.98}\right)^{365/20} - 1 \approx 44.6\%$
- *단순 근사*: $\frac{0.02}{0.98} \times \frac{365}{20} \approx 37.2\%$

→ 할인 포기 = 연 *44.6%* 차입 → 매우 비쌈, 할인 받아야.

### §2.3 직관

- 할인 포기 비용 > 차입비용 → *할인 받기* (필요시 차입)
- 할인 포기 비용 < 차입비용 → 포기 (드뭄)

---

## §3 신용 공여 의사결정 (NPV)

### §3.1 신용 정책 변경 NPV

> 현금판매 → 신용판매 전환의 가치.

**일회성 (one-shot) 효과**:
- 매출 증가 (Q → Q')
- 추가 마진: $(P - v)(Q' - Q)$
- 비용: 회수 지연, 부도, 회수비용

![Figure 28.1 — The Costs of Granting Credit. 교재 p.856](/courses/financial-management/figures/ch28/fig-28-1.png)

> **직관**: 신용을 *얼마나 줄까* 의 비용 곡선. 외상을 늘리면 *carrying cost*(자금이 묶이는 비용, 우상향)가 늘고, 줄이면 *opportunity cost*(놓친 매출, 우하향)가 는다. 둘의 합 total cost 가 최소인 지점이 *최적 신용 규모* — 신용정책도 결국 carrying↔shortage 최적화.

### §3.2 NPV 공식 (단순화)

$$NPV = -\underbrace{[PQ + v(Q'-Q)]}_{\text{초기 비용}} + \frac{(P-v)Q'}{r}$$

- P = 가격, v = 단위 변동비, Q/Q' = 기존/신규 판매량
- r = 기간 할인율

### §3.3 고려 요소

- *Default 확률* (부도율)
- *회수 기간* (ACP)
- *회수 비용*
- *반복 거래* (장기 관계)

---

## §4 신용 분석 — 5 Cs

### §4.1 5 Cs of Credit

| C | 의미 |
|--|--|
| *Character* | 상환 의지 (신용 이력) |
| *Capacity* | 상환 능력 (현금흐름) |
| *Capital* | 재무 건전성 (자본) |
| *Collateral* | 담보 |
| *Conditions* | 경제·산업 상황 |

### §4.2 Credit Scoring

- *통계적 신용평점* (다변량)
- *Altman Z-score* (부도 예측):
$$Z = 1.2X_1 + 1.4X_2 + 3.3X_3 + 0.6X_4 + 1.0X_5$$
- Z < 1.81 → 위험, Z > 2.99 → 안전
- 현대: ML 신용평가, FICO

### §4.3 정보원

- 재무제표, 신용평가기관 (D&B, Moody's)
- 은행, 거래 이력

---

## §5 회수 정책 (Collection)

### §5.1 모니터링 도구

**Average Collection Period (ACP)**:
- = AR / 일평균 매출 (회수까지 평균 일수)

**Aging schedule (연령분석표)**:
- AR 을 경과 기간별 분류 (0-30, 31-60, 61-90...)
- 연체 파악

### §5.2 회수 노력 단계

1. 독촉장
2. 전화
3. 회수 대행사 (collection agency)
4. 법적 조치

### §5.3 Trade-off

- 강한 회수 → 부도 ↓ but 비용·고객관계 ↓
- 약한 회수 → 부도 ↑

---

## §6 재고 관리 (Inventory)

### §6.1 재고 종류

| 종류 | 의미 |
|--|--|
| *Raw materials* | 원자재 |
| *Work-in-progress* | 재공품 |
| *Finished goods* | 완제품 |

### §6.2 재고 비용

**Carrying cost (보유비용)**:
- 보관, 보험, 진부화, 자본 기회비용
- 재고 ↑ → carrying ↑

**Shortage/order cost (부족·주문비용)**:
- *Restocking cost* — 주문 비용
- *Safety reserve* — 품절 비용
- 재고 ↓ → shortage ↑

---

## §7 EOQ Model (경제적 주문량)

### §7.1 공식

$$Q^* = \sqrt{\frac{2 \times D \times F}{CC}}$$

- D = 연간 수요 (판매량)
- F = 주문당 고정비용
- CC = 단위당 연간 보유비용

![Figure 28.3 — Costs of Holding Inventory. 교재 p.864](/courses/financial-management/figures/ch28/fig-28-3.png)

> **직관**: 재고의 *EOQ* 그림. 주문량 Q 를 키우면 *carrying cost*(보유, 우상향)는 늘고 *restocking cost*(주문 횟수↓, 우하향)는 준다. 둘의 합 total cost 가 최소인 *Q\** 가 경제적 주문량 — 26장 운전자본 그래프와 같은 U자 트레이드오프.

### §7.2 관련 지표

| 지표 | 공식 |
|--|--|
| 평균 재고 | Q*/2 |
| 주문 횟수 | D/Q* |
| 총비용 (최적) | 거래비용 = 보유비용 |

![Figure 28.4 — Inventory Holdings for the Eyssell Corporation. 교재 p.864](/courses/financial-management/figures/ch28/fig-28-4.png)

> **직관**: *평균 재고 = Q/2* 의 시각화. Eyssell 사는 3,600단위로 시작해 4주에 걸쳐 0 까지 *직선으로 소진*하고 다시 채운다. 톱니의 평균 높이가 Q/2 = 1,800 — EOQ 의 '평균재고 Q/2' 가정이 이 그림.

### §7.3 Reorder Point + Safety Stock

- *Reorder point* = 리드타임 × 일수요 (+ safety stock)
- *Safety stock* — 불확실 대비 여유 재고

---

![Figure 28.5 — Safety Stocks and Reorder Points. 교재 p.869](/courses/financial-management/figures/ch28/fig-28-5.png)

> **직관**: 불확실성에 대비하는 두 장치. *A. safety stock*: 최소재고선 위에 *완충 재고* 를 깔아 품절을 막는다. *B. reorder point*: 배송 리드타임을 감안해 *재고가 일정선에 닿으면 미리 주문*. *C. 둘의 결합*: reorder point 와 safety stock 을 함께 써 예측 못 한 수요·지연에 모두 대비한다.

## §8 현대 재고 기법

### §8.1 ABC 분석

- 재고를 *중요도(가치)* 로 A/B/C 분류
- A (고가치 소수) → 집중 관리

![Figure 28.2 — ABC Inventory Analysis. 교재 p.864](/courses/financial-management/figures/ch28/fig-28-2.png)

> **직관**: *ABC 분석* — 재고를 가치로 차등 관리. A 그룹은 *품목 수로는 10%* 인데 *가치로는 57%*(위 막대 대비 아래 막대), C 그룹은 반대로 품목 50%·가치 16%. 소수의 고가치 A 품목에 관리를 집중하라는 파레토 원리.

### §8.2 Just-In-Time (JIT)

- *재고 최소화* (필요시 조달)
- Toyota — kanban
- → carrying cost ↓ but 공급망 위험 ↑

### §8.3 MRP / DRP

- *Materials Requirement Planning* — 수요 기반 자재 계획
- 컴퓨터 기반 재고·생산 통합

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 할인 포기 = 공짜 유예 | 연 44.6% 차입 (비쌈) |
| 2 | 2/10 net 30 → 2% 비용 | 연율 환산 (≈37-45%) |
| 3 | 신용 = 항상 매출↑ 이득 | 부도·회수·지연 비용 |
| 4 | EOQ = Baumol 무관 | 같은 형태 (√2DF/CC) |
| 5 | JIT = 항상 우월 | 공급망 위험 (2020 교훈) |
| 6 | 재고 많을수록 안전 | Carrying cost |
| 7 | 5 Cs 중 character 무시 | 상환 의지 핵심 |

---

## §10 자가점검

1. 신용정책 *3 요소*?
2. *2/10 net 30* 할인 포기 비용?
3. 신용 공여 NPV 고려 요소?
4. *5 Cs* of credit?
5. ACP / aging schedule?
6. *EOQ* 공식 + JIT?

<details><summary>해답</summary>

1. Terms of sale (할인/기간), credit analysis (신용평가), collection policy (회수).
2. 할인 포기 = (1+0.02/0.98)^(365/20)−1 ≈ 44.6% (단순 근사 37.2%). 매우 비싼 차입 → 할인 받아야.
3. 매출 증가 마진 vs 부도율, 회수기간(ACP), 회수비용, 반복거래.
4. Character (의지), Capacity (능력), Capital (자본), Collateral (담보), Conditions (경제상황).
5. ACP = AR/일평균매출 (회수 평균 일수). Aging = 경과기간별 AR 분류 (연체 파악).
6. Q* = √(2DF/CC). 평균재고 Q*/2. JIT: 재고 최소 (carrying↓, 공급망 위험↑).

</details>

---

## §11 다음 학습으로

- **Ch 26** — 단기 재무 (운전자본, cash cycle)
- **Ch 27** — Cash management (Baumol = EOQ 형태)
- **Ch 29** — M&A (다음 Part)

---

## §12 한 줄 요약

> **신용 + 재고 관리. *신용정책* = terms(2/10 net 30) + analysis(5 Cs) + collection. *할인 포기 비용* = (1+d/(1−d))^(365/(N−D))−1 ≈ 44.6% (매우 비쌈→할인 받기). *신용 공여 NPV*: 매출↑ 마진 vs 부도·회수·지연. *5 Cs*: Character/Capacity/Capital/Collateral/Conditions (+Altman Z). *회수*: ACP, aging schedule. *재고*: EOQ Q*=√(2DF/CC) (평균 Q*/2), reorder point + safety stock, JIT(carrying↓·공급망 위험↑), ABC.**
