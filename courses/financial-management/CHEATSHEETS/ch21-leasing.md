# Ch 21 Leasing — 치트시트

> Lease 종류 / 회계 / NAL / Tax arbitrage.

## §1 Lease 종류

| 종류 | 특징 |
|--|--|
| Operating | 단기, 취소가능, lessor 위험 |
| Financial (capital) | 장기, 취소불가, 사실상 구매 |
| Sale-leaseback | 매각 후 재임차 (현금화) |
| Leveraged | Lessor 차입 (3-party) |

## §2 Financial lease 4 기준

(하나라도 충족 시):
1. 소유권 이전
2. Bargain purchase option
3. Term ≥ 75% 내용연수
4. PV ≥ 90% 자산가치

## §3 회계 — ASC 842 / IFRS 16

| | 과거 | 현재 |
|--|--|--|
| Operating | Off-balance | On-balance |
| Financial | On-balance | On-balance |

→ ROU asset + lease liability.

## §4 손익 처리 (US GAAP)

| | Operating | Finance |
|--|--|--|
| 비용 | 정액 | 이자+감가 (front-loaded) |
| CF 분류 | Operating | Int=op, Principal=fin |

## §5 NAL (Net Advantage to Leasing)

$$NAL = Cost - \sum \frac{L(1-T_c) + T_c Dep_t}{(1+R_D(1-T_c))^t} - \frac{Salvage}{(1+r)^T}$$

- NAL > 0 → lease
- NAL < 0 → buy

## §6 Lease incremental cash flow (vs buy)

| 항목 | 부호 |
|--|--|
| 구매 비용 회피 | + |
| Lease payment (after-tax) | − |
| Depreciation shield 상실 | − |
| Salvage 포기 | − |

## §7 Discount rate

> *After-tax cost of debt* $R_D(1-T_c)$.

→ Lease = debt 대체, 확실 cash flow → low rate.

## §8 Tax Arbitrage

> 세율 다른 당사자 간 tax shield 이전.

- Lessor (고세율): depreciation 활용
- Lessee (저세율/적자): 무용
- → lease료 인하 전가 (win-win)

## §9 세율별 lease 유불리

| Lessee | 결정 |
|--|--|
| 적자/저세율 | Lease (lessor shield 활용) |
| 고수익/고세율 | Buy (depreciation 가치) |

## §10 좋은 리스 이유

1. Tax arbitrage (세율 차이)
2. 잔존가치 위험 이전
3. Transaction cost 절감
4. 전문 lessor (재판매, 유지)
5. Flexibility (노후화)

## §11 나쁜 리스 이유 (환상)

1. ~~Off-balance~~ (이제 on)
2. ~~"100% financing"~~ (debt 소모)
3. ~~회계 조작~~ (투명성)
4. ~~"막연히 싸다"~~ (NAL 필요)

## §12 의사결정 2단계

```
Step 1: 투자 결정 (NPV > 0?)
Step 2: 조달 결정 (NAL > 0?)
→ NPV negative 면 lease 무관
```

## §13 산업별 lease

| 산업 | 자산 |
|--|--|
| 항공 | 항공기 (~50% lease) |
| 소매 | 매장 |
| 운송 | 트럭, 컨테이너 |
| IT | 서버 (노후화) |
| 의료 | 고가 장비 |

## §14 Sale-leaseback

- 즉시 현금화 (자산 시장가)
- Capital gain 과세
- Core business 집중
- 단, flexibility 상실 + distress signal 가능

## §15 항공사 lease 이유

1. 자본 집약 + 고가
2. 잔존가치 위험 이전
3. Fleet flexibility
4. 전문 lessor (AerCap)
5. Tax arbitrage

## §16 자주 함정

| 함정 | 정정 |
|--|--|
| Operating off-balance | ASC 842 on-balance |
| Lease 항상 싸다 | NAL 계산 |
| "100% financing" | Debt capacity 소모 |
| WACC discount | After-tax cost of debt |
| 투자=조달 결정 | 분리 (NPV vs NAL) |
| 모든 lessee 유리 | 세율 차이 핵심 |
| Salvage 무시 | Buy 시 고려 |

## §17 핵심 공식 요약

| | 공식 |
|--|--|
| Lease liability | PV of lease payments |
| ROU asset | liability + 직접비 |
| Discount rate | $R_D(1-T_c)$ |
| Tax shield (buy) | $T_c \times Dep$ |

## §18 핵심 mindmap

```
Leasing
├── 종류 (operating/financial/sale-leaseback/leveraged)
├── 회계 (ASC 842/IFRS 16 — on-balance)
├── Lease vs Buy
│   ├── NAL 공식
│   ├── After-tax cost of debt
│   └── 투자/조달 결정 분리
├── Tax arbitrage (세율 차이)
└── 좋은/나쁜 이유
```

## §19 좋은 vs 나쁜 (요약)

| 좋은 (real) | 나쁜 (환상) |
|--|--|
| Tax arbitrage | Off-balance (무효) |
| 위험 이전 | "100% financing" |
| 전문성 | 회계 조작 |
| Flexibility | "막연히 싸다" |

## §20 1-line summary

> **Leasing — *operating* (단기, 취소가능) vs *financial* (사실상 구매). *ASC 842/IFRS 16*: on-balance (ROU + liability). *Lease vs Buy* = NAL (구매 회피 − lease after-tax − depreciation shield − salvage), *after-tax cost of debt* discount. *좋은 이유* = tax arbitrage (세율 차이) + 위험 이전 + 전문성 + flexibility. *나쁜 이유* = off-balance(무효) + "100% financing" 환상. 투자(NPV)/조달(NAL) 결정 분리.**
