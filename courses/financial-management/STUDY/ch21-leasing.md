# Chapter 21: Leasing — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 21** (책 p.667~690).
> 21장은 *리스* — Lease vs Buy 결정, 세금, NPV 분석, 회계.

이 장의 *지적 무게중심*:
1. **Lease 종류** — operating vs financial(capital)
2. **회계 처리** — ASC 842 / IFRS 16 (on-balance)
3. **Lease vs Buy NPV** — incremental analysis
4. **세금 효과** — depreciation tax shield vs lease deduction
5. **좋은/나쁜 리스 이유**

---

## §0 도입 — *빌리기는 변형된 빌림이다*

> **핵심 한 문장**: 리스는 "자산을 *살까 빌릴까*"처럼 보이지만 재무적으로는 **차입(debt)의 변형** — 그래서 lease vs buy 는 *투자결정이 아니라 조달결정* 이고, 진짜 승부는 세율 다른 두 당사자 간 *감가상각 방패의 이전(tax arbitrage)* 에서 난다.

핵심 그림은 단순하다(figure 21.1): *사면* Firm U 가 자산을 *소유 + 사용* 한다. *빌리면* lessor 가 *소유*, lessee(Firm U)가 *사용* — 소유와 사용이 갈린다. 이 분리가 만드는 세 가지 질문이 21장이다:

1. **무엇이 리스인가** (§1–2): operating(단기·취소가능, 위험은 lessor)과 financial(장기·사실상 구매)의 구분. 과거엔 operating 을 *장부 밖(off-balance)* 에 숨겼지만, ASC 842/IFRS 16(2019~)이 *대부분 on-balance* 로 끌어냈다(Enron 교훈).
2. **사는 게 싼가 빌리는 게 싼가** (§3): *NAL*(Net Advantage to Leasing)로 *증분 현금흐름* 만 비교한다 — 구매를 회피한 대가로 lease 료(세후)·*감가상각 방패*·잔존가치를 포기. lease 는 debt 의 대체라 *세후 차입비용* $R_D(1-T_c)$ 으로 할인한다.
3. **왜 리스가 존재하나** (§4–5): 진짜 이유는 *tax arbitrage* — *고세율 lessor* 가 감가상각 방패를 활용해 그 이득을 *저세율 lessee*(적자 스타트업 등)에게 lease 료 인하로 넘긴다. off-balance·"100% 금융" 같은 옛 명분은 환상.

한 문장으로: **리스는 debt 이고, lease-vs-buy 의 답은 세금에서 나온다.**

---

## §1 Lease 의 기본

### §1.1 정의

> *Lessee* (사용자) 가 *lessor* (소유자) 에게 *임차료* 지불하고 자산 사용.

- *자산 소유 없이 사용*
- *Capex 회피*

![Figure 21.1 — Buying versus Leasing. 교재 p.650](/courses/financial-management/figures/ch21/fig-21-1.png)

> **직관**: 리스의 *정의* 를 한 장에. *Buy*(왼쪽): Firm U 가 제조사에서 사서 *소유+사용* 하고, 자금은 주주·채권자가 댄다. *Lease*(오른쪽): lessor 가 사서 *소유*, Firm U(lessee)는 *사용만* 한다. 소유와 사용의 *분리* — 이 한 가지가 회계(§2)·세금(§4)·NAL(§3) 의 모든 차이를 낳는다.

### §1.2 종류

| 종류 | 특징 |
|--|--|
| **Operating lease** | 단기, 취소 가능, lessor 가 유지·위험 부담 |
| **Financial (capital) lease** | 장기, 취소 불가, 사실상 구매 (full payout) |
| **Sale and leaseback** | 자산 매각 후 재임차 (현금화) |
| **Leveraged lease** | Lessor 가 차입하여 구매 (3-party) |

### §1.3 Financial lease 의 4 기준 (구 회계)

다음 중 *하나라도* 충족 시 capital lease:
1. *소유권 이전* (만기)
2. *Bargain purchase option* (헐값 매수권)
3. *Lease term ≥ 75%* of 내용연수
4. *PV of payments ≥ 90%* of 자산 가치

---

## §2 회계 처리 — ASC 842 / IFRS 16

### §2.1 변화 (2019~)

> 과거 *operating lease 는 off-balance* → 현재 *대부분 on-balance*.

| | 과거 | 현재 (842/16) |
|--|--|--|
| Operating lease | Off-balance (각주) | **On-balance** (ROU asset + lease liability) |
| Financial lease | On-balance | On-balance |

### §2.2 ROU (Right-of-Use) asset

- *Lease liability* = PV of lease payments
- *ROU asset* = lease liability + 초기 직접비
- *Balance sheet* 에 양변 계상

### §2.3 손익 처리 차이 (US GAAP)

| | Operating | Finance |
|--|--|--|
| 비용 인식 | 정액 (straight-line) | 이자 + 감가상각 (front-loaded) |
| Cash flow 분류 | Operating | Interest=operating, Principal=financing |

### §2.4 *왜 on-balance 로 바꿨나*

- *Off-balance debt* 숨김 방지 (Enron 교훈)
- *투명성* 향상
- *비교 가능성* (lease vs buy)
- *항공사, 소매* 큰 영향 (대규모 lease)

---

## §3 Lease vs Buy — NPV 분석

### §3.1 핵심 질문

> *리스* vs *차입 후 구매* — 어느 것이 더 싼가?

→ *Incremental cash flow* 비교 (lease 대신 buy 시 차이).

### §3.2 Lease 의 incremental cash flow (lease 관점)

**Lease 하면 (vs buy)**:
- (+) 초기 자산 구매 비용 회피 (+Cost)
- (−) Lease payment (after-tax): $-L(1-T_c)$
- (−) Depreciation tax shield 상실: $-T_c \times Dep$
- (−) Salvage value 포기 (만기)

### §3.3 NPV of Leasing (NAL — Net Advantage to Leasing)

$$NAL = Cost - \sum \frac{L(1-T_c) + T_c \cdot Dep_t}{(1+R_D(1-T_c))^t} - \frac{Salvage}{(1+r)^T}$$

- *NAL > 0* → 리스 유리
- *NAL < 0* → 구매 유리

### §3.4 Discount rate

> *After-tax cost of debt* $R_D(1-T_c)$ 사용.

- Lease = *debt 의 대체* (secured, low risk)
- Cash flow 가 *상대적으로 확실* → low discount rate

### §3.5 예제

자산 $100K, 5년, 정액 감가 $20K/year, lease $24K/year, T_c = 21%, R_D = 8%.

**After-tax discount rate**: 8% × 0.79 = 6.32%

**Lease 의 incremental (vs buy)**:
- 초기: +$100K (구매 회피)
- 매년: −$24K(0.79) − $20K(0.21) = −$18.96K − $4.2K = −$23.16K
- (lease payment after-tax + depreciation shield 상실)

**NAL**:
$$100 - 23.16 \times PVIFA(6.32\%, 5) = 100 - 23.16 \times 4.18 = 100 - 96.8 = \$3.2K$$

→ NAL > 0 → *리스 약간 유리* (이 가정 하).

---

## §4 세금 효과

### §4.1 Lessee 관점

- *Lease payment* = 전액 손비 인정 (operating)
- *구매 시*: depreciation tax shield + interest 손비
- → *세율 높은 lessee* 는 depreciation 가치 큼

### §4.2 Lessor 관점

- *Depreciation tax shield* 보유 (소유자)
- *Lease income* 과세
- → *세율 높은 lessor* 가 depreciation 활용 유리

### §4.3 Tax arbitrage (좋은 리스 이유)

> *세율 다른 두 당사자* 간 tax shield 이전.

- *Lessor* (고세율) — depreciation tax shield 활용
- *Lessee* (저세율, 또는 손실) — depreciation 활용 못 함
- → *Lessor 가 shield 가치를 lease 료 인하로 전가* → *win-win*

### §4.4 예시

- *스타트업* (적자, 세금 0) — depreciation 무용 → *lease 유리* (lessor 가 shield 활용)
- *고수익 대기업* — depreciation 가치 큼 → *buy* 고려

---

## §5 좋은 리스 vs 나쁜 리스 이유

### §5.1 좋은 이유 (real economic)

1. **Tax arbitrage** — 세율 차이 활용
2. **Reduced uncertainty** — 잔존가치 위험 이전 (operating)
3. **Lower transaction cost** — 반복 사용 자산
4. **Specialized lessor** — 유지·재판매 전문성 (항공기, 차량)
5. **Flexibility** — 단기 사용, 기술 노후화 위험 회피

### §5.2 나쁜 이유 (illusory)

1. ~~Off-balance financing~~ — 이제 on-balance (842/16)
2. ~~"100% financing"~~ — debt capacity 소모
3. ~~회계 이익 조작~~ — 투명성 강화로 약화
4. ~~"리스는 더 싸다" 막연한 믿음~~ — NAL 계산 필요

### §5.3 산업별 lease 활용

| 산업 | Lease 자산 |
|--|--|
| 항공 | 항공기 (operating lease 흔함) |
| 소매 | 매장 (real estate) |
| 운송 | 트럭, 컨테이너 |
| IT | 서버, 장비 (기술 노후화) |
| 의료 | 고가 장비 (MRI 등) |

---

## §6 Lease vs Buy 의사결정 절차

### §6.1 5 단계

1. *자산 NPV* 가 positive 인지 (먼저 투자 자체 결정)
2. *Lease 의 incremental cash flow* 계산
3. *After-tax cost of debt* 로 discount
4. *NAL* 계산
5. *NAL + 정성 요인* (flexibility, 위험) 종합

### §6.2 주의

- *투자 결정(NPV)* 과 *조달 결정(lease vs buy)* 분리
- Lease 는 *financing* 결정 (debt 대체)
- *자산 NPV negative* 면 lease 여부 무관 (안 함)

---

## §7 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Operating lease 는 off-balance | ASC 842/IFRS 16 — on-balance |
| 2 | Lease = 항상 싸다 | NAL 계산 필요 |
| 3 | "100% financing" 이득 | Debt capacity 소모 |
| 4 | Lease discount = WACC | After-tax cost of debt |
| 5 | 투자결정 = 조달결정 | 분리 (NPV vs NAL) |
| 6 | 모든 lessee 에 유리 | 세율 차이가 핵심 |
| 7 | Salvage 무시 | Buy 시 잔존가치 고려 |
| 8 | Depreciation shield 무시 | 구매의 핵심 이점 |

---

## §8 자가점검

1. *Operating vs Financial lease*?
2. *ASC 842/IFRS 16* 변화?
3. *NAL* 의 incremental cash flow?
4. *Lease discount rate*?
5. *Tax arbitrage* (좋은 리스 이유)?
6. *나쁜 리스 이유*?

<details><summary>해답</summary>

1. Operating: 단기, 취소가능, lessor 위험 부담. Financial: 장기, 취소불가, 사실상 구매.
2. 과거 operating off-balance → 현재 on-balance (ROU asset + lease liability).
3. (+)구매 회피, (−)lease payment after-tax, (−)depreciation shield 상실, (−)salvage 포기.
4. After-tax cost of debt $R_D(1−T_c)$ (lease = debt 대체, 확실 cash flow).
5. 세율 다른 당사자 간 tax shield 이전 — 고세율 lessor 가 shield 활용, 저세율 lessee 에 lease료 인하 전가.
6. Off-balance(이제 on), "100% financing"(debt 소모), 회계 조작(투명성 강화), 막연한 "싸다".

</details>

---

## §9 다음 학습으로

- **Ch 6** — Capital investment (depreciation tax shield)
- **Ch 16-17** — Capital structure (lease = debt)
- **Ch 18** — APV (subsidized financing 유사)

---

## §10 한 줄 요약

> **Leasing — *operating* (단기, 취소가능) vs *financial* (장기, 사실상 구매). *ASC 842/IFRS 16*: 대부분 on-balance (ROU asset + lease liability). *Lease vs Buy* = NAL (incremental: 구매 회피 + lease payment − depreciation shield − salvage). *After-tax cost of debt* 로 discount. *좋은 이유* = tax arbitrage (세율 차이), 위험 이전, 전문성, flexibility. *나쁜 이유* = off-balance(이제 무효), "100% financing" 환상.**
