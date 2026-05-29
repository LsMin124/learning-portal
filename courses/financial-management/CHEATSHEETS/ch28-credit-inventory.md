# Ch 28 Credit and Inventory — 치트시트

> 신용정책 / 할인 포기 / 5 Cs / EOQ / JIT.

## §1 신용정책 3 요소

| 요소 | 내용 |
|--|--|
| Terms of sale | 기간/할인 |
| Credit analysis | 신용평가 (5 Cs) |
| Collection | 회수 |

## §2 Terms 표기

> 2/10 net 30 = 10일내 2% 할인, 아니면 30일 전액.

## §3 할인 포기 비용 (핵심)

$$\left(1 + \frac{d}{1-d}\right)^{\frac{365}{N-D}} - 1$$

- 2/10 net 30 → ≈ 44.6%
- 단순 근사: (d/(1−d))×(365/(N−D)) ≈ 37.2%

## §4 할인 결정

- 포기 비용 > 차입비용 → 할인 받기
- 보통 44.6% ≫ 차입 → 받아야

## §5 신용 공여 NPV

$$NPV = -[PQ + v(Q'-Q)] + \frac{(P-v)Q'}{r}$$

(매출↑ 마진 vs 회수지연·부도)

## §6 5 Cs

| C | 의미 |
|--|--|
| Character | 의지 |
| Capacity | 능력 (현금흐름) |
| Capital | 자본 |
| Collateral | 담보 |
| Conditions | 경제상황 |

## §7 Credit Scoring

$$Z = 1.2X_1 + 1.4X_2 + 3.3X_3 + 0.6X_4 + 1.0X_5$$

- Altman Z < 1.81 위험, > 2.99 안전

## §8 회수 모니터링

| 도구 | 내용 |
|--|--|
| ACP | AR / 일평균매출 |
| Aging schedule | 경과기간별 AR |

## §9 재고 종류

- Raw materials (원자재)
- Work-in-progress (재공품)
- Finished goods (완제품)

## §10 재고 비용

| 비용 | 재고↑ |
|--|--|
| Carrying (보관/진부화/기회) | ↑ |
| Shortage/order | ↓ |

## §11 EOQ

$$Q^* = \sqrt{\frac{2DF}{CC}}$$

- D=수요, F=주문비용, CC=단위 보유비용
- 평균 = Q*/2, 횟수 = D/Q*

## §12 EOQ = Baumol

| | 공식 |
|--|--|
| EOQ (재고) | √(2DF/CC) |
| Baumol (현금) | √(2TF/K) |

→ 동일 trade-off 구조.

## §13 Reorder + Safety

- Reorder point = 리드타임 × 일수요 (+ safety)
- Safety stock = 불확실 대비

## §14 현대 재고 기법

| 기법 | 특징 |
|--|--|
| ABC | 가치별 A/B/C |
| JIT | 재고 최소 (Toyota) |
| MRP | 수요기반 자재계획 |

## §15 JIT trade-off

- Carrying ↓ but shortage·공급망 위험 ↑
- 2020 코로나 → JIC 회귀

## §16 운전자본 3대 통합

| 항목 | 모델 |
|--|--|
| 현금 | Baumol/Miller-Orr |
| 재고 | EOQ |
| AR | 신용 NPV |

→ 모두 carrying vs shortage. CCC = DSO+DIO−DPO.

## §17 자주 함정

| 함정 | 정정 |
|--|--|
| 할인 포기 = 공짜 | 연 44.6% |
| 2/10 net 30 = 2% | 연율 환산 |
| 신용 = 항상 이득 | 부도·회수 비용 |
| JIT 항상 우월 | 공급망 위험 |
| 재고 많을수록 안전 | Carrying cost |

## §18 핵심 mindmap

```
Credit & Inventory
├── 신용정책 (terms/analysis/collection)
├── 할인 포기 (44.6%, 받아야)
├── 5 Cs + Altman Z
├── 신용 NPV (마진 vs 부도)
├── EOQ √(2DF/CC) = Baumol
└── JIT (carrying↓·공급망 위험↑)
```

## §19 1-line summary

> **신용+재고. 신용정책 = terms(2/10 net 30) + 5 Cs analysis + collection. *할인 포기* = (1+d/(1−d))^(365/(N−D))−1 ≈ 44.6% (받아야). *5 Cs*: Character/Capacity/Capital/Collateral/Conditions (+Altman Z<1.81 위험). 회수: ACP, aging. *재고*: EOQ Q*=√(2DF/CC) (=Baumol 형태), reorder+safety stock, JIT(carrying↓·공급망 위험↑, 2020→JIC). 현금·AR·재고 모두 carrying vs shortage, CCC=DSO+DIO−DPO.**
