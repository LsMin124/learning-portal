# Ch 21 Leasing — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *Operating vs Financial lease*?

<details><summary>답</summary>

| | Operating | Financial (capital) |
|--|--|--|
| 기간 | 단기 | 장기 |
| 취소 | 가능 | 불가 |
| 위험 | Lessor 부담 | Lessee 부담 |
| 본질 | 임차 | 사실상 구매 |

**Financial lease 4 기준** (하나라도 충족):
1. 소유권 이전
2. Bargain purchase option
3. Lease term ≥ 75% 내용연수
4. PV payments ≥ 90% 자산가치

**기타**: Sale-leaseback (현금화), leveraged lease (3-party).

</details>

### Q2. *ASC 842 / IFRS 16* 변화?

<details><summary>답</summary>

**핵심**: 과거 operating lease 는 *off-balance* → 현재 *on-balance*.

| | 과거 | 현재 |
|--|--|--|
| Operating | Off-balance (각주) | On-balance (ROU + liability) |
| Financial | On-balance | On-balance |

**ROU asset**:
- Lease liability = PV of payments
- ROU asset = liability + 초기 직접비

**왜 변경**:
- Off-balance debt 숨김 방지 (Enron 교훈)
- 투명성, 비교 가능성
- 항공/소매 큰 영향

</details>

### Q3. *Tax arbitrage* (좋은 리스 이유)?

<details><summary>답</summary>

> 세율 다른 두 당사자 간 *tax shield 이전*.

**메커니즘**:
- *Lessor* (고세율) — depreciation tax shield 활용
- *Lessee* (저세율/적자) — depreciation 무용
- → Lessor 가 shield 가치를 *lease료 인하* 로 전가
- → **win-win**

**예**:
- 스타트업 (적자, 세금 0) — depreciation 무용 → *lease 유리*
- 고수익 대기업 — depreciation 가치 큼 → buy 고려

**기타 좋은 이유**:
- 잔존가치 위험 이전 (operating)
- 전문 lessor (항공기, 차량)
- Flexibility (기술 노후화)

</details>

### Q4. 계산 — NAL (Net Advantage to Leasing)

자산 $60K, 3년, 정액 감가 $20K/year (salvage $0), lease $22K/year, T_c = 25%, R_D = 8%.

NAL?

<details><summary>답</summary>

**After-tax discount rate**: 8% × 0.75 = 6%

**Lease incremental cash flow (vs buy)**:
- 초기 (Year 0): +$60K (구매 회피)
- 매년 (1-3):
  - −Lease after-tax: −$22K × 0.75 = −$16.5K
  - −Depreciation shield 상실: −$20K × 0.25 = −$5K
  - = −$21.5K/year

**NAL**:
$$NAL = 60 - 21.5 \times PVIFA(6\%, 3)$$

PVIFA(6%, 3) = 2.673

$$= 60 - 21.5 \times 2.673 = 60 - 57.47 = \$2.53K$$

→ NAL > 0 → *리스 유리* ($2.53K).

**해석**: 리스가 구매보다 *$2.53K 저렴* (이 가정 하). 단, salvage·flexibility 정성 요인 추가 고려.

</details>

### Q5. 계산 — Lessee vs Lessor 세율 차이

자산 $100K, 5년, 정액 감가 $20K, lease $25K/year.
- Lessee: T_c = 0% (적자)
- Lessor: T_c = 30%

(a) Lessee 의 lease 비용 (after-tax)?
(b) Lessor 의 depreciation shield?
(c) 왜 win-win?

<details><summary>답</summary>

**(a) Lessee (T_c = 0%)**:
- Lease payment 손비 효과 없음 (세금 0)
- After-tax 비용 = $25K (full)
- Depreciation 보유해도 무용 → lease 자연스러움

**(b) Lessor (T_c = 30%)**:
- Depreciation shield = $20K × 30% = **$6K/year**
- Lease income 과세: $25K × 30% = $7.5K
- Lessor 가 depreciation 활용 (lessee 는 못 함)

**(c) Win-win**:
- Lessor 가 *연 $6K shield* 확보 → 일부를 *lease료 인하* 전가
- 예: $25K → $23K
- Lessee: 저렴한 사용
- Lessor: shield 차익
- → *tax arbitrage* 양측 이익

**핵심**: 세율 차이 클수록 lease economic 가치 ↑. 동일 세율이면 (perfect) 이점 미미.

</details>

### Q6. 계산 — Sale and Leaseback

회사: 본사 건물 (book $50M, 시장가 $80M). 매각 후 재임차.

(a) 즉시 현금?
(b) 매각 차익?
(c) 왜 하는가?

<details><summary>답</summary>

**(a) 즉시 현금**: $80M (시장가)

**(b) 매각 차익**: $80M − $50M = **$30M** (capital gain, 과세)

**(c) 이유**:

1. **현금화**: 묶인 자산 → $80M cash (운영, 부채상환, 투자)
2. **Balance sheet** (과거, 이제 약화): ROA 개선 (단 ASC 842 로 다시 on-balance)
3. **Tax**: lease 손비 (단 $30M capital gain 과세)
4. **부동산 위험 분리**: core business 집중

**유명 사례**:
- 소매업체 매장 sale-leaseback
- Macy's, Sears — 부동산 현금화 (생존 자금)

**주의**:
- 고금리 implicit (lease료 내재)
- Flexibility 상실 (장기 임차)
- Distress signal 가능

</details>

### Q7. 디버그 — "100% financing 이라 좋다"

CFO: *"리스는 자기자본 0% 로 자산 사용! 100% financing 무조건 유리!"*

반박?

<details><summary>답</summary>

**오해 — "100% financing" 환상**:

**1. Debt capacity 소모**:
- Lease = debt 대체 (사실상 borrowing)
- ASC 842: on-balance lease liability
- → 다른 차입 여력 감소

**2. Implicit interest rate**:
- Lease료에 내재 이자율
- 직접 차입보다 높을 수 있음 (lessor margin)
- NAL 로 확인 필요

**3. 진짜 비교 대상**:
- Lease vs *차입 후 구매* (둘 다 100% financing)
- 자기자본 비교 아님
- → NAL 이 정답

**4. 회계 변화**:
- 과거 off-balance 환상 (항공사)
- 현재 ASC 842/IFRS 16 on-balance

**올바른 framework**:
1. 자산 NPV positive?
2. Lease vs Buy → NAL
3. NAL > 0 면 lease
4. 정성 요인 추가

**진짜 lease 이점**: tax arbitrage, 위험 이전, 전문성, flexibility.

→ "100% financing" 은 환상. Lease 도 debt capacity 소모. NAL 로 판단.

</details>

### Q8. 디버그 — 투자결정 vs 조달결정 혼동

분석가: *"기계 NPV −$5K 인데, 리스 NAL +$3K 라서 리스로 도입!"*

오류?

<details><summary>답</summary>

**근본 오류 — 두 결정 혼동**:

**1. 투자 결정 (먼저)**:
- 기계 NPV = −$5K (negative)
- → 애초에 도입하면 안 됨
- Lease 든 buy 든 자산 자체가 가치 파괴

**2. 조달 결정 (NPV positive 일 때만)**:
- NAL +$3K = 리스가 구매보다 $3K 저렴
- 조달 방식 비교일 뿐

**올바른 계산**:
- Lease 도입 총 가치 = NPV + NAL = −$5K + $3K = **−$2K**
- 여전히 negative → 도입 안 함

**분리 원칙**:
- 투자 결정 (NPV): 자산 가치 있는가?
- 조달 결정 (NAL): 어떻게 자금?
- 순서: NPV 먼저, positive 면 NAL

**예외 (드묾)**:
- NAL 이 매우 커서 NPV + NAL > 0 가능
- 여기선 −$5K 가 너무 큼

**실무 함정**:
- Lease 매력에 현혹 → 나쁜 자산 도입
- Vendor financing 유혹
- Subsidized lease 가 negative NPV 정당화 X

→ 투자(NPV)와 조달(NAL) 분리. NPV negative 면 lease 무관 (NAL 이 상쇄할 만큼 크지 않은 한 도입 안 함).

</details>

### Q9. 면접 — *왜 항공사는 항공기를 리스*?

<details><summary>답</summary>

**항공사 lease 이유**:

**1. 자본 집약 + 고가**: 대당 $100M-$400M, capex 회피, 노선 확장 유연.

**2. 잔존가치 위험 이전**: 잔존가치 변동 큼 (연료 효율, 노후화), lessor 부담 (operating).

**3. Fleet flexibility**: 수요 변동 (계절, 경기), 단기 lease 로 capacity 조정.

**4. 전문 lessor**: AerCap, Air Lease Corp — 재판매·유지·재배치 규모의 경제.

**5. Tax arbitrage**: lessor 가 depreciation 활용, 저수익 항공사 유리.

**6. Off-balance (과거)**: ASC 842 전 부채 숨김 (현재 on-balance).

**통계**:
- 글로벌 항공기 ~50% lease (operating)
- AerCap 세계 최대 lessor

**Buy 하는 경우**: 대형 안정 항공사 (Delta, Lufthansa) core fleet 일부 소유. Mix 전략.

**COVID 교훈 (2020)**:
- 수요 급감 → lease flexibility 가치 입증
- 일부 lessor 위기 (lessee 파산)

**유사 산업**: 해운 (선박 charter), 운송 (트럭), 건설 (중장비), IT (노후화).

> 항공사 lease = 고가 자본집약 + 잔존가치 위험 이전 + fleet flexibility + 전문 lessor + tax arbitrage.

</details>

### Q10. 면접 — *Lease vs Buy framework*?

<details><summary>답</summary>

**완전한 framework**:

**Step 1 — 투자 결정 (NPV)**: 자산 가치 창출? NPV > 0 면 진행.

**Step 2 — 조달 옵션**: Lease (operating/financial) vs Buy (현금/차입), 둘 다 financing.

**Step 3 — NAL 계산**:
$$NAL = Cost - \sum \frac{L(1-T_c) + T_c Dep}{(1+R_D(1-T_c))^t} - \frac{Salvage}{(1+r)^T}$$
- After-tax cost of debt discount
- NAL > 0 → lease

**Step 4 — 정량 요인**: 세율 차이, salvage 불확실, maintenance, residual risk.

**Step 5 — 정성 요인**: Flexibility, 전문성, off-balance (약화), covenant, control.

**의사결정 매트릭스**:

| 상황 | 추천 |
|--|--|
| Lessee 적자/저세율 | Lease (tax arbitrage) |
| 잔존가치 위험 큼 | Lease (operating) |
| 기술 노후화 빠름 | Lease (flexibility) |
| Core long-term | Buy |
| 고수익 (depreciation 가치) | Buy |
| 전문 유지 필요 | Lease |

**산업별**:
- 항공: lease (잔존 위험, flexibility)
- 소매: 매장 lease
- 제조: core 설비 buy
- IT: 장비 lease

**흔한 실수**:
1. 투자 ↔ 조달 혼동
2. "100% financing" 환상
3. WACC discount (after-tax debt 써야)
4. 세율 차이 무시
5. Salvage 무시

> Lease vs Buy = 2단계 분리 (투자 NPV → 조달 NAL) + 세율 차이 + 정성 요인. After-tax cost of debt discount.

</details>
