# Ch 23 Options — Extensions and Applications — 퀴즈

> 10 문항 (개념 4 / 분석 3 / 디버그 2 / 면접 1).

### Q1. *ESO* 목적 + FASB 2004?

<details><summary>답</summary>

**ESO** = 경영진 회사 주식 call option (ATM strike, vesting 3-4년, expiration 10년, non-transferable).

**목적**:
1. Incentive alignment (주가 ↑ 유인)
2. Talent retention (vesting)
3. Cash 절약 (스타트업)
4. Tax (ISO 우대)

**FASB 2004 (ASC 718)**:
- 과거: ATM option 회계 비용 0 (intrinsic 0)
- 현재: *fair value 비용 처리* 강제 (Black-Scholes)

**논란**: repricing, backdating (2006 스캔들), excessive comp, short-termism.

</details>

### Q2. *Startup / R&D 가 옵션* 인 이유?

<details><summary>답</summary>

**Equity = call on 미래 가치**:
- 적자 스타트업 → DCF 음수
- 높은 변동성 → option 가치 ↑

**Staged investment = compound option**:
- Series A = option on B = option on C...

**R&D = call on 제품**:
- Pharma: Phase I = option on II = ... = launch
- 높은 실패율 + 큰 성공 = 옵션 성격

→ VC staged financing (Ch 20) 의 옵션 해석.

</details>

### Q3. *Real options 4종* + valuation 방법?

<details><summary>답</summary>

| Real option | 옵션 type |
|--|--|
| Expand | Call (pilot → full) |
| Abandon | Put (salvage = strike) |
| Delay | American call (timing) |
| Switch | Option (input/output) |

**Valuation**:
1. Black-Scholes (단순)
2. Binomial tree (단계적, American)
3. Monte Carlo (path-dependent)
4. Decision tree (이산)

**Delay 주의**: 대기 가치 vs *경쟁자 진입* (preemption).

</details>

### Q4. *Risky debt 옵션 분해*?

<details><summary>답</summary>

$$\text{Risky debt} = \text{Risk-free debt} - \text{Put on firm value}$$

- 채권자 = put 매도 (주주에게)
- Default option = 주주 limited liability

**Credit spread = put value**:
- 변동성 ↑ → put ↑ → spread ↑
- Merton model → 신용위험 정량화

**Structural credit models**:
- Merton (1974): equity = call, debt = risk-free − put
- KMV/Moody's: distance-to-default = (V−D)/σ_V
- CDS: 명시적 put on credit

</details>

### Q5. 분석 — Decision tree vs Real option

- Decision tree: 실제 확률 50%, risk-adjusted 20%
- Real option: risk-neutral prob, risk-free 5%

왜 다르고 어느 게 맞나?

<details><summary>답</summary>

**차이 — discount rate + probability**:

**Decision tree**: 실제 확률, risk-adjusted rate, 주관적 확률 가능.
**Real option**: risk-neutral prob (no-arbitrage), risk-free rate, traded 가정.

**어느 게 맞나**:

**Real option 우월**: underlying traded/replicable → no-arbitrage 정확 (oil, 금융자산).

**Decision tree 우월**: non-traded, 주관적 확률 (R&D 성공률, 규제 승인).

**핵심 함정**:
- Decision tree 의 *단일 risk-adjusted rate* 가 옵션 (asymmetric) cash flow 에 부적절
- Risk 가 매 node 변함 → 단일 rate 부정확
- → Real option (risk-neutral) 이 회피

**실무**: Traded → real option (BS). Non-traded → decision tree + sensitivity. Hybrid → Monte Carlo.

→ Traded 면 real option (no-arbitrage). 옵션의 변하는 risk 를 단일 rate 로 못 잡는 게 decision tree 한계.

</details>

### Q6. 분석 — Option to Delay

토지: 지금 개발 NPV +$2M. 1년 대기:
- 50% 호황 → +$8M
- 50% 불황 → −$1M (개발 안 함 → $0)

r = 10%. 대기 가치?

<details><summary>답</summary>

**지금 개발**: +$2M

**1년 대기**:
- 호황 (50%): +$8M
- 불황 (50%): $0 (abandon)
- 기대값: 0.5 × $8M + 0.5 × $0 = $4M
- 현재가치: $4M / 1.10 = **$3.64M**

**비교**: 지금 $2M < 대기 $3.64M → **대기 유리**.

**Option value of waiting** = $3.64M − $2M = **$1.64M**.
- 불황 시 손실 회피 (downside 제한) + 호황 시 큰 이익
- *Asymmetry* 가 가치

**전제**: 대기 비용 작음, 경쟁자 진입 (preemption) 없음, information 도착.

**Preemption 위험**: 경쟁자 선점 → 기회 상실 → 대기 가치 감소. First-mover vs option value trade-off.

→ Delay option value $1.64M. Asymmetry 핵심. 단 preemption 고려.

</details>

### Q7. 분석 — Distance to Default

V = $120M, σ_V = 25%, D = $100M (1년).

(a) Distance-to-default?
(b) Equity 옵션?

<details><summary>답</summary>

**(a) Distance-to-default** (간이):
$$DD \approx \frac{V - D}{\sigma_V \times V} = \frac{20}{0.25 \times 120} = \frac{20}{30} = 0.67$$

**해석**: 0.67σ 거리. 낮을수록 default 확률 ↑. ~25% default (대략).

**(b) Equity as call**:
- Equity = $\max(V−D, 0)$ = call, strike $100M
- Intrinsic = $20M + time value (변동성)
- 채권자 = risk-free − put

**함의**:
- σ_V ↑ → DD ↓ → default ↑ → spread ↑
- V ↓ 또는 D ↑ (leverage) → DD ↓

**실무 (KMV)**: DD → Expected Default Frequency (EDF). Equity 변동성 → asset 변동성 역산.

→ DD = (V−D)/(σ_V×V). Equity = call (Merton).

</details>

### Q8. 디버그 — Real option 남용

CEO: *"DCF −$50M 이지만 option to expand + pivot + acquire = $200M, 가치 +$150M!"*

비판?

<details><summary>답</summary>

**Real option 남용 (over-application)**:

**1. Identifiable 안 함**: "option to pivot" 구체적 trigger 없음.
**2. Exercisable 안 함**: pivot = strategy change, contingent claim 아님.
**3. Measurable 안 함**: underlying value, volatility 추정 불가.
**4. Double counting**: 여러 옵션 합산 중복.
**5. Volatility garbage in**: 높은 σ → 큰 value (자의적).

**올바른 3 조건**:
1. Identifiable (구체적 trigger)
2. Exercisable (실제 행사 권한)
3. Measurable (value + volatility 추정)

**정당한 예**: 광산 (commodity = traded), Pharma Phase (go/no-go), pilot.
**부당한 예**: "option to pivot", "option to dominate", "synergy option".

**유명 남용**: Dot-com 2000, WeWork, SPAC projection.

**Damodaran**: *"Specific, exercisable, measurable 일 때만. 아니면 over-engineering."*

→ 막연한 옵션 $200M = 남용. 3 조건 미충족.

</details>

### Q9. 디버그 — ESO repricing

주가 $100 → $40. ESO strike $100 (deep OTM). 이사회: *"strike $40 로 인하."*

문제점?

<details><summary>답</summary>

**ESO repricing 문제**:

**1. Incentive 왜곡**: "Heads I win, tails I reprice" — downside 제거, moral hazard.
**2. 주주-경영진 불일치**: 주주 −60% 손실, 경영진 strike 인하로 회피.
**3. Risk-taking 왜곡**: repricing 기대 → 과도한 위험.
**4. 회계**: ASC 718 modification → 추가 비용 인식.
**5. 주주 승인**: 거래소 투표 요구, proxy advisor (ISS) 반대.

**대안**:
1. 새 option 부여 (dilution)
2. 6-and-1 exchange (가치 중립)
3. Performance-based
4. RSU 전환 (덜 binary)
5. Indexed options (시장 상대)

**역사**: dot-com 붕괴 (2000-02) repricing 급증 → 주주 반발.

**현대**: repricing 회피, RSU 선호, performance shares (TSR/ROIC), clawback.

**옳은 관점**: ESO = 위험 공유. 주가 하락 = 경영진도 손실 (정상). Repricing = 위험 공유 파괴.

→ "Heads I win, tails I reprice" — incentive 왜곡. RSU/performance-based 대안.

</details>

### Q10. 면접 — *위험 채권을 옵션으로 보는 실무 가치*?

<details><summary>답</summary>

**Risky debt = Risk-free − Put 응용**:

**1. 신용위험 정량화 (Merton/KMV)**:
- Equity 변동성 → asset 변동성 역산
- Distance-to-default = (V−D)/σ_V → EDF
- 신용평가 보완 (Moody's KMV)

**2. Credit spread 분해**: spread = put value (변동성, leverage, 만기 함수).

**3. CDS pricing**: CDS = put on credit, structural model.

**4. 신용위험 hedge**: equity put 으로 credit hedge, capital structure arbitrage.

**5. 부실기업 분석**: distressed debt, equity = OTM call (option value).

**6. Bank capital (Basel)**: loan = put 매도 집합, expected loss = put value.

**Merton model**:
- $E = V N(d_1) - De^{-rT}N(d_2)$ (equity = call)
- Debt = V − E

**실무 한계**:
- V 직접 관측 불가 (equity 역산)
- σ_V 추정 어려움
- 단순 capital structure 가정
- Jump risk 무시

**발전 모델**: KMV, reduced-form (Jarrow-Turnbull), CreditMetrics, jump-diffusion.

**유명**: 2008 위기 — Merton correlation 한계, CDO mispricing.

**투자 전략**: capital structure arbitrage (equity put vs CDS), distressed, convertible arb.

> 위험 채권 = risk-free − put 가치: 신용위험 정량화 (Merton/KMV, DD), credit spread 분해, CDS pricing, hedge, 부실 분석, bank capital. 단 V·σ_V 추정 한계, 2008 correlation 교훈.

</details>
