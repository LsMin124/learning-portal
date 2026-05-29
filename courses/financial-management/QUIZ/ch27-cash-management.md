# Ch 27 Cash Management — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. 현금 보유 *3 동기* + 비용?

<details><summary>답</summary>

**Keynes 3 동기**:
1. **Transaction** — 일상 결제 (급여, 매입, 운영)
2. **Precautionary** — 예비 (불확실 현금흐름 대비)
3. **Speculative** — 기회 포착 (인수, 저가 매입)

**추가**: compensating balance (은행 요구), 세금 (해외 현금).

**보유 비용**:
- *기회비용* — 현금은 낮은 수익 (유휴자산)
- → 보유 ↑ (안전, 기회비용↑) vs 보유 ↓ (거래비용↑, shortage)
- 최적 = 목표 현금잔액 모형 (Baumol/Miller-Orr)

</details>

### Q2. *Float* 정의 + collection vs disbursement?

<details><summary>답</summary>

**Float** = 은행 가용잔액 − 장부잔액 (수표 처리 시차).

**Disbursement float (+, 유리)**:
- 우리가 수표 발행 → 아직 미인출
- 장부 < 은행 → 자금 더 오래 보유
- 목표: *늘리기* (지급 지연)

**Collection float (−, 불리)**:
- 우리가 수표 수취 → 아직 미입금
- 장부 > 은행 → 자금 못 씀
- 목표: *줄이기* (수금 가속)

**Net float** = disbursement − collection. → 극대화가 목표.

</details>

### Q3. *Baumol* vs *Miller-Orr* 차이?

<details><summary>답</summary>

| | Baumol | Miller-Orr |
|--|--|--|
| 현금흐름 | 일정 유출 (확정) | 랜덤 (불확실) |
| 기반 | EOQ | 통제 한계 |
| 결과 | 최적 거래규모 C* | 상한 H, 하한 L, 목표 Z |
| 공식 | C*=√(2TF/K) | Z*=∛(3Fσ²/4K)+L |

**Baumol**: 현금 일정 소진 → C* 만큼 보충. 평균 = C*/2.

**Miller-Orr**: 현금 랜덤 변동 → 상한 도달 시 증권 매입, 하한 시 매도, 범위 내 방치. H=3Z−2L.

→ Baumol 은 비현실적 (일정 유출), Miller-Orr 이 변동성 반영.

</details>

### Q4. 계산 — Baumol Model

연간 현금 수요 $1,200,000. 증권 매도 거래비용 $50/회. 기회비용 (이자율) 6%.

(a) 최적 거래규모 C*? (b) 평균 현금잔액? (c) 연간 거래 횟수?

<details><summary>답</summary>

**(a) C*** (Baumol):
$$C^* = \sqrt{\frac{2TF}{K}} = \sqrt{\frac{2 \times 1,200,000 \times 50}{0.06}}$$
$$= \sqrt{\frac{120,000,000}{0.06}} = \sqrt{2,000,000,000} \approx \$44,721$$

**(b) 평균 현금잔액**:
$$= \frac{C^*}{2} = \frac{44,721}{2} \approx \$22,361$$

**(c) 거래 횟수**:
$$= \frac{T}{C^*} = \frac{1,200,000}{44,721} \approx 26.8 \text{회/년}$$

**검증 (총비용)**:
- 거래비용: 26.8 × $50 = $1,342
- 기회비용: $22,361 × 0.06 = $1,342
- → 두 비용 같음 (EOQ 최적 조건) ✓

→ C* ≈ $44,721, 평균 ≈ $22,361, 약 27회.

</details>

### Q5. 계산 — Miller-Orr Model

일일 현금흐름 분산 σ² = $1,000,000 ($1,000 표준편차). 거래비용 F = $40. 일일 기회비용 K = 0.025% (0.00025). 하한 L = $5,000.

(a) 목표잔액 Z*? (b) 상한 H*? (c) 평균 현금?

<details><summary>답</summary>

**(a) 목표잔액 Z*** (return point):
$$Z^* = \sqrt[3]{\frac{3F\sigma^2}{4K}} + L = \sqrt[3]{\frac{3 \times 40 \times 1,000,000}{4 \times 0.00025}} + 5,000$$
$$= \sqrt[3]{\frac{120,000,000}{0.001}} + 5,000 = \sqrt[3]{1.2 \times 10^{11}} + 5,000$$
$$\approx 4,932 + 5,000 = \$9,932$$

**(b) 상한 H***:
$$H^* = 3Z^* - 2L = 3(9,932) - 2(5,000) = 29,796 - 10,000 = \$19,796$$

**(c) 평균 현금**:
$$= \frac{4Z^* - L}{3} = \frac{4(9,932) - 5,000}{3} = \frac{34,728}{3} \approx \$11,576$$

**해석**:
- 현금이 $19,796 도달 → ($19,796−$9,932)=$9,864 증권 매입
- $5,000 도달 → ($9,932−$5,000)=$4,932 증권 매도
- 범위 내 방치

→ Z* ≈ $9,932, H* ≈ $19,796, 평균 ≈ $11,576.

</details>

### Q6. 계산 — Lockbox 의사결정

Lockbox 도입 → 수금 float *3일* 단축. 일평균 수금 $200,000. 연 이자율 5%. Lockbox 연간 비용 $15,000.

도입할까?

<details><summary>답</summary>

**Float 단축으로 확보 자금**:
- 3일 × $200,000/일 = **$600,000** (조기 가용)

**연간 이자 절감 (편익)**:
- $600,000 × 5% = **$30,000/년**

**비용**: $15,000/년

**순편익**:
- $30,000 − $15,000 = **+$15,000/년**

**결정**: 순편익 양수 → **Lockbox 도입**.

**손익분기 (BEP)**:
- 비용 = 편익: $15,000 = (3 × $200,000) × r → r = 2.5%
- 또는 일평균 수금 $100,000 이면 편익 $15,000 = 비용 (무차별)

→ 순편익 +$15,000 → 도입. (Float × 이자율 > 비용 일 때)

</details>

### Q7. 디버그 — Disbursement float 극대화 전략

재무팀: *"멀리 떨어진 은행에서 수표 발행해서 결제를 최대한 늦추자. Float 로 며칠 더 이자 벌 수 있다!"*

문제점?

<details><summary>답</summary>

**과도한 disbursement float (playing the float) 문제**:

**1. 전자결제로 float 소멸**:
- *Check 21 Act* (2004) → 수표 전자 이미지 처리
- ACH/wire → float ≈ 0
- 원거리 은행 전략 효과 미미

**2. 윤리·관계 문제**:
- 공급업체 지급 의도적 지연 → 관계 악화
- 신용등급, 향후 거래조건 불리

**3. 규제 위험**:
- Remote disbursement = 규제 당국 주시
- 일부는 기만적 관행으로 간주

**4. 비용 대비 편익 미미**:
- 며칠 float × 낮은 금리 = 작은 이득
- 관리비용, 관계비용 > 이득

**올바른 관점**:
- Float 관리는 *정당한 수금 가속* (lockbox) 에 집중
- 지급은 *예정대로* (관계 유지) + ZBA 로 유휴현금만 최소화
- 현대: float 게임보다 *전자결제 효율*

→ 전자결제로 float 소멸 + 윤리·관계·규제 비용. 며칠 이자 < 비용.

</details>

### Q8. 디버그 — Baumol 모델 오적용

스타트업 CFO: *"우리 현금흐름은 매출이 들쭉날쭉하지만 Baumol 모델로 C*=√(2TF/K) 계산해서 목표 현금 정했다."*

문제점?

<details><summary>답</summary>

**Baumol 모델 가정 위반**:

**1. Baumol 핵심 가정**: *일정한(확정적) 현금 유출*
- 매출이 들쭉날쭉 = *불확실(랜덤)* 현금흐름
- → Baumol 부적합

**2. 올바른 모델: Miller-Orr**
- 랜덤 현금흐름 → 상한/하한/목표 (Z*=∛(3Fσ²/4K)+L)
- 변동성 σ² 반영

**3. 스타트업 특수성**:
- 현금흐름 변동성 *매우 큼*
- *Burn rate*, runway 관리가 핵심
- Precautionary 동기 ↑ (예비현금 多)

**4. 모델의 현실 한계**:
- Baumol/Miller-Orr 모두 단순화 (현실은 cash budget + 시나리오)
- 실무: 13주 cash flow forecast, 시나리오 분석

**올바른 접근**:
- 변동성 큼 → Miller-Orr (또는 더 보수적 buffer)
- 스타트업: runway 기준 (months of cash)
- Cash budget (Ch 26) + 시나리오

→ Baumol 은 일정 유출 가정. 변동 현금흐름 = Miller-Orr 또는 runway 관리.

</details>

### Q9. 면접 — *왜 Apple 같은 기업이 거액 현금을 쌓아두나*?

<details><summary>답</summary>

**거액 현금 보유 이유 (Apple $200B+ 시기)**:

**1. Speculative/전략 동기**:
- 인수 기회, R&D, 신사업 (옵션 가치)

**2. Precautionary**:
- 경기·공급망 충격 buffer
- 사업 변동성 대비

**3. 세금 (과거 핵심)**:
- 해외 이익 → 미국 송금 시 과세 (TCJA 2017 이전)
- → 해외 현금 *trapped* (송금 회피)
- 2018 이후 본국 송환 + buyback 급증

**4. 협상력/신용**:
- 강한 대차대조표 → 낮은 조달비용, 신뢰

**비판 (agency)**:
- *유휴 현금 = 낮은 수익* (주주 기회비용)
- Free cash flow 문제 (Jensen) — 과잉 현금 → 낭비 투자 유인
- 행동주의 (Icahn vs Apple) → 배당/buyback 압박

**해결**:
- 영구 잉여 → 배당/buyback (Apple 대규모 환원)
- 임시 잉여만 money market 보유

**Trade-off**:
- 유연성·옵션 가치 vs 기회비용·agency

> Apple 현금: speculative(M&A)+precautionary+세금(해외 trapped, TCJA 전)+협상력. 비판: 기회비용·agency(Jensen FCF). 해결: 영구잉여는 배당/buyback 환원. 유연성 vs 기회비용 trade-off.

</details>

### Q10. 면접 — *전자결제 시대에 cash management 가 어떻게 변했나*?

<details><summary>답</summary>

**전통 → 현대 cash management 진화**:

**Float 관리의 쇠퇴**:
- *Check 21 Act* (2004) → 수표 전자처리, float ↓
- ACH, wire, 실시간 결제 (RTP, FedNow) → float ≈ 0
- "Playing the float" 전략 무의미화

**새로운 도구**:
1. *Treasury management system (TMS)* — 통합 자금관리
2. *Real-time payments* (RTP, FedNow 2023) — 즉시 결제
3. *Virtual accounts* — 가상계좌 자동 분류
4. *Cash pooling* (notional/physical) — 글로벌 자금 통합
5. *AI 현금흐름 예측* — ML 기반 forecast

**글로벌화**:
- *Multi-currency* 관리 (Ch 31 환위험)
- *In-house bank* (대기업 사내은행)
- 규제 (Basel, 자금세탁 AML)

**유휴현금 투자 진화**:
- MMF (2a-7 규제, 2016 개혁)
- 단기 ETF, 직접 운용
- 2008/2020 MMF "break the buck" 위험 인식

**핵심 가치 불변**:
- 유동성 확보, 기회비용 최소화 (목표잔액 개념)
- Precautionary buffer (2020 코로나 → 현금 중요성 재확인)

**미래**:
- 실시간 visibility + AI 예측
- 디지털 통화 (CBDC) 가능성
- API 기반 임베디드 금융

> Float 게임은 전자결제(Check 21, RTP, FedNow)로 소멸. 현대: TMS, cash pooling, 실시간 결제, AI 예측, 글로벌 multi-currency. 단 목표잔액·precautionary buffer 개념은 불변 (2020 코로나로 현금 중요성 재확인).

</details>
