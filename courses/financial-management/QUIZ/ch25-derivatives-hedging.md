# Ch 25 Derivatives and Hedging — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *Forward vs Futures* 차이?

<details><summary>답</summary>

| | Forward | Futures |
|--|--|--|
| 거래 | OTC | 거래소 |
| 표준화 | 맞춤형 | 표준 (수량/만기) |
| 정산 | 만기만 | 일일 (mark-to-market) |
| Counterparty | 있음 | Clearinghouse (제거) |
| 유동성 | 낮음 | 높음 |
| 현금흐름 | 만기만 | 매일 |

**Mark-to-market**: futures 는 매일 손익을 margin account 로 정산 → margin call 가능 → 누적 부도 위험 ↓.

→ 이론 가격은 거의 같으나, 현금흐름 시점과 신용위험 구조가 다름.

</details>

### Q2. *Short hedge* vs *Long hedge*?

<details><summary>답</summary>

> Hedge = *기존 노출의 반대 포지션*.

**Short hedge** (futures 매도):
- 자산을 *보유* 또는 *생산* 예정
- 가격 *하락* 위험 방어
- 예: 농부(밀), 정유사(원유 재고), 광산

**Long hedge** (futures 매수):
- 미래 *매입* 예정
- 가격 *상승* 위험 방어
- 예: 항공사(연료), 제빵사(밀)

→ 보유/생산 = short, 매입 예정 = long.

</details>

### Q3. *왜 기업이 헤징* 하는가 (M&M 역설 포함)?

<details><summary>답</summary>

**M&M 역설**: 완전시장에서 헤징은 *무관* (주주가 직접 분산 가능). 그럼 왜?

**시장 불완전성 → 헤징 이유**:
1. **Financial distress 비용 ↓** — cash flow 안정 → 부도 확률 ↓ → distress 비용 회피
2. **Tax convexity** — 누진세, 이익 변동성 ↓ → 기대세금 ↓ (Jensen 부등식)
3. **부채여력 ↑** — 안정 cash flow → 더 많은 debt → tax shield ↑
4. **과소투자 회피** — 내부자금 확보 → NPV+ 투자 실행 (Froot-Scharfstein-Stein)
5. **경영진 위험회피** — 인적자본 집중 → 개인 위험 ↓

→ 핵심: 헤징은 *기대 cash flow* 가 아니라 *변동성*을 줄여 위 비용들을 절감.

</details>

### Q4. 계산 — Short hedge 손익

농부: 밀 10,000 부셸 보유. 현재 현물 $5.00/부셸. 밀 futures $5.20 에 *매도* (short hedge). 3개월 후 수확.

시나리오 A: 현물 $4.50, futures $4.60
시나리오 B: 현물 $5.80, futures $5.85

(a) 각 시나리오 순 실현가?

<details><summary>답</summary>

**Short hedge**: futures 매도 → 가격 하락 시 futures 이익.

**시나리오 A (가격 하락)**:
- 현물 매도: $4.50
- Futures 이익: $5.20 − $4.60 = $0.70 (매도 후 싸게 환매)
- 순 실현가: $4.50 + $0.70 = **$5.20/부셸**

**시나리오 B (가격 상승)**:
- 현물 매도: $5.80
- Futures 손실: $5.20 − $5.85 = −$0.65
- 순 실현가: $5.80 − $0.65 = **$5.15/부셸**

**해석**:
- 두 경우 모두 ≈ $5.15-5.20 (futures 가격 부근 *고정*)
- 차이 ($0.05) = *basis 변동* (basis risk)
- A: basis = 4.50−4.60 = −0.10, B: basis = 5.80−5.85 = −0.05
- → 가격은 고정했으나 basis risk 잔존

→ Short hedge 로 ≈ $5.20 고정, basis 변동만큼 오차.

</details>

### Q5. 계산 — Interest Rate Swap (comparative advantage)

| | A 기업 | B 기업 |
|--|--|--|
| 고정 차입 | 8% | 10% |
| 변동 차입 | LIBOR + 0.3% | LIBOR + 1% |

A는 변동 선호, B는 고정 선호. Swap 으로 총 이득?

<details><summary>답</summary>

**Comparative advantage 분석**:
- 고정 차이: 10% − 8% = 2%
- 변동 차이: (LIBOR+1%) − (LIBOR+0.3%) = 0.7%
- **총 이득 = 2% − 0.7% = 1.3%**

**A의 우위**: 고정에서 2% 우위 (변동 0.7%보다 큼) → A는 *고정*에 비교우위.

**구조**:
- A: 고정 8% 차입 (자신의 강점) → 변동 원함
- B: 변동 LIBOR+1% 차입 → 고정 원함
- Swap: A↔B 이자 교환

**배분 (1.3% 균등 가정, 각 0.65%)**:
- A 목표: 변동, 시장 직접이면 LIBOR+0.3% → swap 으로 LIBOR−0.35%
- B 목표: 고정, 직접이면 10% → swap 으로 9.35%
- 은행 개입 시 spread 차감

→ 총 1.3% 이득을 나눔 (comparative advantage). 원금 교환 없이 이자만 차액 정산.

</details>

### Q6. 계산 — Duration Hedging (immunization)

은행: 자산 $100M (duration 5년), 부채 $90M (duration 2년).

(a) Duration gap?
(b) 금리 1%p 상승 시 순자산 변화 (근사)?
(c) 면역 방법?

<details><summary>답</summary>

**(a) Duration gap**:
$$DG = D_A - D_L \times \frac{L}{A} = 5 - 2 \times \frac{90}{100} = 5 - 1.8 = 3.2 \text{년}$$

**(b) 금리 1%p 상승 (Δy = +0.01)**:
- 자산 변화: −5 × $100M × 0.01 = −$5M
- 부채 변화: −2 × $90M × 0.01 = −$1.8M
- 순자산 변화: −$5M − (−$1.8M) = **−$3.2M**

→ 금리 상승 시 순자산 *감소* (자산이 더 민감).

**(c) 면역 방법**:
1. 자산 duration ↓ (단기 자산으로)
2. 부채 duration ↑ (장기 차입)
3. *Interest rate futures 매도* (금리 상승 시 이익으로 상쇄)
4. *Pay-fixed swap* (고정 지급/변동 수취)
- 목표: duration gap = 0 (immunization)

→ DG = 3.2년, 금리↑ 시 −$3.2M. Futures 매도/swap 으로 면역.

</details>

### Q7. 계산 — Cap (금리 상한)

차입자: 변동금리 $10M 대출 (LIBOR 연동). 금리 상승 우려 → strike 5% interest rate cap 매수 (premium $50,000).

LIBOR 가 (a) 4% (b) 7% 일 때 cap payoff + 실효금리?

<details><summary>답</summary>

**Cap = 금리 call 매수** (LIBOR > strike 시 차액 수취).

**(a) LIBOR 4% (< 5% strike)**:
- Cap payoff: $0 (OTM, 행사 안 함)
- 이자: 4% × $10M = $400,000
- + premium $50,000
- 실효: ($400,000 + $50,000) / $10M = **4.5%**

**(b) LIBOR 7% (> 5% strike)**:
- Cap payoff: (7% − 5%) × $10M = $200,000
- 이자: 7% × $10M = $700,000
- 순 이자: $700,000 − $200,000 = $500,000 (= 5% 상한)
- + premium $50,000
- 실효: ($500,000 + $50,000) / $10M = **5.5%**

**해석**:
- Cap 이 금리를 *5% 상한*으로 고정 (premium 비용 추가)
- 금리 하락 시 (a) 낮은 금리 *유지* (옵션의 비대칭)
- → futures 와 달리 *downside 차단 + upside 유지*

→ Cap = 금리 상한 보험. 실효금리 = min(LIBOR, 5%) + premium.

</details>

### Q8. 디버그 — "헤징은 항상 주주에게 이득"

CFO: *"우리가 원자재 가격을 헤지하면 cash flow 가 안정되니 주주 가치가 항상 올라간다!"*

오류?

<details><summary>답</summary>

**오류 — M&M 역설 무시**:

**1. 완전시장에서 헤징 무관**:
- 주주는 *직접 포트폴리오 분산* 가능
- 체계적 위험은 헤지해도 주주가 이미 분산
- → 기업 헤징이 *가치 추가 안 함*

**2. 헤징이 가치 있는 *조건* (시장 불완전성)**:
- Financial distress 비용 존재
- 세금 convexity
- 과소투자 문제
- → 이게 *없으면* 헤징 무의미

**3. 헤징 비용**:
- 거래비용, premium, basis risk, 관리비용
- 비용 > 편익이면 가치 파괴

**4. 투기 변질 위험**:
- "헤지" 명목 과도한 포지션 → 손실 (Barings, P&G)

**올바른 관점**:
- 헤징은 *변동성*만 줄임 (기대 cash flow 불변)
- 위 불완전성이 *클 때만* 가치 창출
- 무조건 ↑ 아님

→ M&M: 완전시장 헤징 무관. distress/tax/과소투자 있을 때만 가치. 비용·투기변질 주의.

</details>

### Q9. 디버그 — Metallgesellschaft 사례

MG: 고객에 *장기* 고정가 석유 공급 계약 → 헤지로 *단기* futures *매수* (long), 만기마다 *roll-over*. 1993 유가 하락 → 대규모 margin call → $1.3B 손실 후 청산.

무엇이 문제였나?

<details><summary>답</summary>

**Metallgesellschaft 의 헤징 실패**:

**1. Maturity mismatch (핵심)**:
- 노출: *장기* (10년 공급 계약)
- 헤지: *단기* futures (rolling stack hedge)
- → 만기 불일치 = basis risk

**2. Cash flow 시점 불일치**:
- 단기 futures: 유가 하락 → *즉시* margin call (현금 유출)
- 장기 계약 이익: *미래* 실현 (현금 유입 지연)
- → 이론상 헤지됐어도 *유동성 위기*

**3. Mark-to-market 의 함정**:
- Futures 손실은 매일 현금 정산
- 상쇄되는 계약 이익은 회계상 미실현
- → $1.3B margin 조달 불가

**4. 조기 청산 (최악)**:
- 모회사가 포지션 강제 청산
- 유가 *반등* 시 손실 확정 (헤지 효과 상실)

**교훈**:
- *Funding liquidity risk* (헤지해도 현금 부족)
- Maturity matching 중요
- Mark-to-market 현금흐름 관리
- 헤지 손실의 *회계 vs 경제* 괴리

→ Maturity mismatch + 단기 margin call 유동성 위기 + 조기 청산. "이론 헤지 ≠ 현금흐름 헤지".

</details>

### Q10. 면접 — *기업이 어떤 위험을 헤지하고 어떤 위험은 안 하는가*?

<details><summary>답</summary>

**헤지하는 위험 (비체계적/사업 외 위험)**:
1. **상품가격** (원자재, 연료) — 항공사, 정유, 제조
2. **환위험** (FX) — 다국적, 수출입
3. **금리위험** — 금융기관, 부채 많은 기업
4. **신용위험** — CDS

**헤지 안 하는 (또는 신중) 위험**:
1. **핵심 사업 위험** — 회사의 *존재 이유* (제약사 R&D, 기술 혁신)
2. **체계적 위험** — 주주가 이미 분산
3. **헤지 비용 > 편익**

**헤징 결정 프레임워크**:
- *Comparative advantage*: 회사가 시장보다 잘 아는 위험만 부담, 나머지 헤지
- 항공사: 항공 서비스가 본업 → *연료가격* 헤지 (본업 아님)
- 석유 회사: 유가가 본업 → *부분만* 헤지 (정보 우위)

**실무 고려**:
1. *Selective hedging* (시장 view 반영) — 투기 변질 위험
2. *Hedge ratio* (full vs partial)
3. *Natural hedge* (수익-비용 같은 통화)
4. 회계 (hedge accounting, ASC 815)
5. 경쟁사 헤징 (상대적 위치)

**이론 vs 실무**:
- 이론 (M&M): distress/tax/과소투자 있을 때만
- 실무: 경영진 위험회피, earnings smoothing (논란), covenant

**유명**: Southwest Airlines (연료 헤지로 2000년대 우위), 반대로 Delta 정유소 인수 (수직통합 헤지).

> 헤지 대상: 본업 외 위험 (상품/FX/금리), 비교우위 없는 위험. 헤지 제외: 핵심 사업 위험 (존재 이유), 체계적 위험 (주주 분산). 핵심: comparative advantage + M&M 불완전성. 단 selective hedging 은 투기 변질 주의.

</details>
