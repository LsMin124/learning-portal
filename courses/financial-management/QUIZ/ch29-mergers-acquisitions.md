# Ch 29 Mergers, Acquisitions, and Divestitures — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. 인수 *3 형태* + 분류?

<details><summary>답</summary>

**법적 3 형태**:
1. **Merger/Consolidation** — 흡수/신설합병, *주총 승인* 필요
2. **Acquisition of stock** — 주식 인수, *tender offer* (주총 불필요, 적대적 가능)
3. **Acquisition of assets** — 자산 인수 (소수주주 문제 회피, 부채 선별)

**경제적 분류**:
- *Horizontal* — 동종 (시장지배력)
- *Vertical* — 공급망 전후방
- *Conglomerate* — 무관 사업

</details>

### Q2. *시너지* 정의 + 4 원천?

<details><summary>답</summary>

**시너지**:
$$\text{Synergy} = V_{AB} - (V_A + V_B)$$

**4 원천**:
1. **Revenue enhancement** — 매출 증대 (시장지배력, 마케팅)
2. **Cost reduction** — 비용 절감 (규모의 경제) — *가장 신뢰*
3. **Tax gains** — 세금 (이월결손금, 부채여력)
4. **Lower cost of capital** — 자본비용 ↓ (발행비용)

**의심스러운 동기 (시너지 아님)**:
- 분산 (주주 직접 가능), EPS bootstrapping (착시), 제국 건설 (agency)

</details>

### Q3. M&A 실증 — 누가 이득 보나?

<details><summary>답</summary>

**실증 결과**:
- **Target 주주**: *큰 이득* (premium 20-40%)
- **Acquirer 주주**: 평균 *≈ 0* 또는 약간 음수

→ 시너지는 주로 *target 에게 이전*.

**Acquirer 실패 원인**:
1. 과도한 premium (winner's curse)
2. 시너지 과대평가
3. 통합 실패 (문화)
4. Hubris (Roll 1986, 경영진 자만)
5. Agency (제국 건설)

**시사점**: M&A 자체가 가치 파괴는 아니나, *acquirer 가 시너지를 다 지불* 하는 경향.

</details>

### Q4. 계산 — Cash 인수 NPV

기업 A (가치 $500M) 가 기업 B (독립가치 $100M) 인수. 시너지 $40M 예상. 현금 $130M 지급.

(a) Premium? (b) NPV to A? (c) 결합기업 가치?

<details><summary>답</summary>

**(a) Premium**:
$$= \text{현금} - V_B = 130 - 100 = \$30M$$

**(b) NPV to A**:
$$= \text{Synergy} - \text{Premium} = 40 - 30 = +\$10M$$

또는: 인수로 얻는 것 = $V_B$ + synergy = $140M, 지불 $130M → NPV = $10M.

**(c) 결합기업 가치**:
$$V_{AB} = V_A + V_B + \text{Synergy} - \text{현금지급}$$
$$= 500 + 100 + 40 - 130 = \$510M$$

(A 주주: 기존 $500M → $510M, +$10M = NPV ✓)

**해석**:
- 시너지 $40M 중 $30M 은 B 주주에 (premium), $10M 은 A 주주에
- Premium < synergy → A 도 이득

→ Premium $30M, NPV +$10M, 결합 $510M.

</details>

### Q5. 계산 — Stock 인수

기업 A (가치 $500M, 1,000만주, 주가 $50) 가 B ($100M) 인수. 시너지 $40M. 대가로 A 주식 *250만주* 발행.

(a) 결합가치? (b) A 가 B 주주에 준 지분율? (c) 실효 비용 + NPV?

<details><summary>답</summary>

**(a) 결합가치**:
$$V_{AB} = V_A + V_B + \text{Synergy} = 500 + 100 + 40 = \$640M$$

**(b) B 주주 지분율**:
- 신주 250만 / 총 (1,000만+250만) = 250/1,250 = **20%**

**(c) 실효 비용**:
$$= \alpha \times V_{AB} = 0.20 \times 640 = \$128M$$

**NPV to A**:
$$= (V_B + \text{Synergy}) - \text{실효비용} = 140 - 128 = +\$12M$$

또는: A 기존주주 가치 = 80% × $640M = $512M (기존 $500M, +$12M ✓)

**Cash 와 비교 (Q4)**:
- Cash $130M 지급 시 실효비용 $130M
- Stock 250만주 → 실효 $128M (시너지 공유로 차이)
- 시너지 클수록 stock 비용 ↑ (B 도 결합가치 share)

→ B 지분 20%, 실효비용 $128M, NPV +$12M.

</details>

### Q6. 계산 — EPS Bootstrapping 착시

A: EPS $4, 주가 $40 (P/E 10), 100만주. B: EPS $4, 주가 $20 (P/E 5), 100만주.
A 가 주식교환으로 B 인수 (B 주주에 50만주 발행, 시너지 0).

(a) 합병 후 EPS? (b) 가치 창출됐나?

<details><summary>답</summary>

**합병 전**:
- A 순이익 = $4 × 100만 = $400만
- B 순이익 = $4 × 100만 = $400만
- 합산 순이익 = $800만

**주식 발행** (B 주주에):
- B 가치 $20M / A 주가 $40 = 50만주 발행
- 합병 후 주식 = 100만 + 50만 = 150만주

**(a) 합병 후 EPS**:
$$= \frac{800만}{150만} = \$5.33$$

→ A 의 EPS $4 → $5.33 *증가*! (bootstrapping)

**(b) 가치 창출?**
- **NO. 회계 착시.**
- 시너지 0 → 실제 가치 불변 ($400만+$400만 = $800만)
- 합병 가치 = $40M + $20M = $60M
- 합병 후 주가 = $60M / 150만 = $40 (불변!)
- EPS ↑ 했지만 *P/E 하락* (10 → 7.5), 주가 불변

**함정**:
- 고 P/E 기업이 저 P/E 기업 인수 → EPS 자동 ↑
- 시장이 P/E 유지 *착각* 하면 주가 ↑ (일시적, sustainable 아님)
- "Chain letter / bootstrap game"

→ EPS $5.33 로 증가하나 *가치 창출 X* (P/E 하락, 주가 $40 불변). 회계 착시.

</details>

### Q7. 디버그 — 분산 시너지 주장

CEO: *"우리 경기민감 사업과 B 의 경기방어 사업을 합치면 현금흐름 변동성이 줄어든다. 이 분산 효과가 큰 시너지다!"*

비판?

<details><summary>답</summary>

**분산(diversification) "시너지" 의 오류**:

**1. 주주가 직접 분산 가능**:
- 투자자는 *포트폴리오*로 직접 분산 (저비용)
- 회사가 분산할 이유 없음 (M&M 정신)
- → 분산 자체는 *가치 추가 안 함*

**2. Conglomerate discount**:
- 실증: 복합기업은 *할인* 거래 (sum-of-parts 보다 낮음)
- 내부 자본시장 비효율, 투명성 ↓
- 행동주의 → 분할 압박 (focus)

**3. Coinsurance 효과 (채권자에게 이전)**:
- 분산 → 부도위험 ↓ → *채권자* 이득
- 주주는 오히려 *손해* (옵션 가치 ↓)

**4. 진짜 시너지와 구분**:
- 비용 절감, 매출 증대 = 진짜
- 단순 변동성 감소 = 가짜

**예외 (분산이 정당한 경우)**:
- Financial distress 비용 큼 → 안정화 가치
- 부채여력 ↑ (tax shield)
- 단 이건 *분산 자체*가 아니라 부수 효과

**유명**: 1960-70년대 conglomerate 붐 → 1980년대 해체 (LBO, bust-up). GE 의 장기 부진/분할.

→ 분산은 주주가 직접 가능 → 시너지 아님. Conglomerate discount, coinsurance(채권자 이전). 진짜 시너지(비용/매출)와 구분.

</details>

### Q8. 디버그 — Poison Pill 정당화

경영진: *"Poison pill 은 주주를 보호한다. 적대적 인수자로부터 회사를 지킨다!"*

다른 관점은?

<details><summary>답</summary>

**Poison pill 의 양면**:

**작동 방식**:
- 적대적 인수 시 *기존 주주*가 할인가 신주 매수권
- → 인수자 지분 *희석*, 인수 비용 ↑

**경영진 주장 (긍정)**:
1. 협상력 ↑ → *더 높은 premium* 유도
2. Lowball 입찰 방어
3. 시간 확보 (대안 모색)

**비판 (agency 관점)**:
1. **경영진 보호 (entrenchment)**:
- 무능 경영진이 *자리 보전*
- 인수 = 규율 메커니즘인데 차단
2. **주주 이익 침해**:
- 주주가 premium 받을 기회 박탈
- 경영진 vs 주주 이해 충돌
3. **실증 혼재**:
- Pill + staggered board → 기업가치 ↓ (일부 연구)
- 단독 pill 은 협상력 ↑ 효과도

**현대 추세**:
- 기관투자자/ISS 반대 (pill 폐지 압박)
- *Shadow pill* (필요시 즉시 도입)
- Dead-hand pill 등 극단형 → 법원 제동

**핵심 질문**: *누구를 위한 방어인가?*
- 주주 (협상력) vs 경영진 (자리 보전)
- 이사회 *신인의무* (fiduciary duty) 시험

→ Pill 은 협상력 ↑ (긍정) vs 경영진 entrenchment (agency). 실증 혼재. "누구를 위한 방어인가"가 핵심.

</details>

### Q9. 면접 — *왜 대부분 인수기업(acquirer)은 M&A 로 가치를 못 만드나*?

<details><summary>답</summary>

**Acquirer 가치 창출 실패의 구조적 이유**:

**1. Winner's curse (승자의 저주)**:
- 경매식 입찰 → 가장 *과대평가* 한 자가 낙찰
- 진짜 가치보다 높게 지불

**2. 시너지 과대평가**:
- 매출 시너지 = 특히 비현실적 (실현율 낮음)
- 통합 비용 과소평가
- "시너지" 가 deal 정당화 도구로 남용

**3. Premium 협상 구조**:
- Target 이사회 신인의무 → premium 극대화
- 경쟁 입찰 → premium ↑
- 시너지가 다 target 에 이전

**4. Hubris (Roll 1986)**:
- CEO 자만 → 가치 과신
- 대형 deal = CEO 명성/보상 (empire building)

**5. 통합 실패**:
- 문화 충돌 (Daimler-Chrysler)
- IT/프로세스 통합 비용
- 핵심 인재 이탈

**6. Agency**:
- 경영진 보상 = 규모 연동 → 과잉 인수
- Free cash flow 낭비 (Jensen)

**성공하는 경우**:
- *Cost 시너지* 명확 (중복 제거)
- *Tuck-in* 소규모 (통합 쉬움)
- *Serial acquirer* (Danaher, Constellation Software — 체계적)
- 적정 premium, 현금 deal (자신감)

**실증**:
- Target +20~40%, acquirer ≈ 0
- 주식 deal acquirer < 현금 deal (과대평가 신호)

> Acquirer 실패: winner's curse + 시너지 과대평가 + target 협상력(premium 다 이전) + hubris + 통합 실패 + agency. 성공: cost 시너지, tuck-in, serial acquirer, 적정 premium·현금.

</details>

### Q10. 면접 — *Spin-off 등 divestiture 가 어떻게 가치를 창출*하나?

<details><summary>답</summary>

**Divestiture 가치 창출 메커니즘**:

**1. Focus (집중)**:
- 핵심 사업 집중 → 경영 효율
- 자본배분 명확

**2. Conglomerate discount 해소**:
- 복합기업 = sum-of-parts 보다 할인
- 분할 → *순수 사업* 재평가 (re-rating)
- 투자자가 원하는 익스포저 선택

**3. 정보 비대칭 ↓**:
- 분리 → 각 사업 투명성 ↑
- Analyst coverage, 비교가능성

**4. 인센티브 정렬**:
- 분사 후 독립 경영진 보상 = 자기 사업 성과
- Entrepreneurial 동기

**5. 내부 자본시장 비효율 제거**:
- Cross-subsidization (좋은 사업이 나쁜 사업 보조) 중단
- Winner picking 실패 해소

**형태별**:
| 형태 | 현금유입 | 특징 |
|--|--|--|
| Sell-off | O | 매각 |
| Spin-off | X | 주주에 신주 (tax-free 가능) |
| Carve-out | O | 일부 IPO |
| Split-up | X | 완전 분할 |

**실증**:
- Spin-off 발표 시 *양(+) 주가 반응*
- 분리된 자회사 장기 outperform (일부)

**촉매**:
- 행동주의 (Icahn, Elliott) → 분할 압박
- 사례: eBay/PayPal, Abbott/AbbVie, GE 3분할

**주의 (가치 파괴 가능)**:
- Stranded cost (분리 후 중복 비용)
- 실제 시너지 있던 경우 손실
- Dis-synergy

> Divestiture 가치: focus, conglomerate discount 해소 (re-rating), 정보 투명성, 인센티브 정렬, 내부자본 비효율 제거. Spin-off (tax-free, 양 반응), carve-out (현금). 행동주의 촉매. 단 stranded cost·실제 시너지 손실 주의.

</details>
