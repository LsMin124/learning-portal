# Ch 22 Options and Corporate Finance — 퀴즈

> 10 문항 (개념 3 / 계산 5 / 디버그 1 / 면접 1).

### Q1. *Call / Put payoff* + 4 기본 포지션?

<details><summary>답</summary>

**Payoff**:
- Call: $\max(S_T - K, 0)$
- Put: $\max(K - S_T, 0)$

| 포지션 | 시각 | Max 손실 | Max 이익 |
|--|--|--|--|
| Long call | Bullish | Premium | 무한 |
| Short call | Bearish | 무한 | Premium |
| Long put | Bearish | Premium | K−Premium |
| Short put | Bullish | K−Premium | Premium |

**Moneyness**: ITM (S>K call), ATM (S=K), OTM (S<K call).

</details>

### Q2. *Option 가치 6 요인* + 방향?

<details><summary>답</summary>

| 요인 ↑ | Call | Put |
|--|--|--|
| 주가 S | ↑ | ↓ |
| Strike K | ↓ | ↑ |
| 변동성 σ | ↑ | ↑ |
| 만기 T | ↑ | ↑ |
| 무위험 r | ↑ | ↓ |
| 배당 | ↓ | ↑ |

**핵심**:
- 변동성 ↑ → call + put 둘 다 ↑ (asymmetric upside)
- Option = intrinsic + time value
- 변동성이 옵션 가치의 핵심 (BS 의 σ)

</details>

### Q3. *Equity as call option* (Merton)?

<details><summary>답</summary>

> 주주의 equity = firm value 에 대한 *call option*.

$$\text{Equity} = \max(V - D, 0)$$

- Strike = 부채 face value D
- Underlying = firm value V
- $V > D$: 부채 갚고 잔여 차지 (행사)
- $V < D$: default, firm 을 채권자에 (포기)

**채권자**: risky debt = risk-free debt − put.

**함의**:
1. Asset substitution — σ↑ → equity(call)↑ → 주주 risky 선호
2. Debt overhang — deep OTM call → 투자 유인 없음
3. Default premium — 채권자 put 매도

→ Ch 17 capital structure agency cost 와 직결.

</details>

### Q4. 계산 — Put-Call Parity

S = $80, K = $75, r = 4%, T = 1년, C = $12.

(a) Put 가격?
(b) Synthetic stock 구성?

<details><summary>답</summary>

**(a) Put-Call Parity**:
$$P = C + \frac{K}{1+r} - S = 12 + \frac{75}{1.04} - 80$$
$$= 12 + 72.12 - 80 = \$4.12$$

**(b) Synthetic stock**:
$$S = C - P + \frac{K}{1+r}$$
- Long call + Short put + Long bond (K의 PV)
- = $12 − $4.12 + $72.12 = $80 ✓

**검증 (만기 payoff)**:
- $S_T > K$: call $S_T−K$, put 0, bond K → 합 $S_T$ ✓
- $S_T < K$: call 0, short put −(K−S_T), bond K → 합 $S_T$ ✓

→ Synthetic stock = call − put + bond, 만기 payoff = $S_T$.

</details>

### Q5. 계산 — Binomial (1-period)

S = $50, u = 1.3, d = 0.7, K = $50, r = 6%.

(a) Risk-neutral probability?
(b) Call 가치?
(c) Put 가치 (parity)?

<details><summary>답</summary>

**(a) Risk-neutral probability**:
$$p = \frac{(1+r) - d}{u - d} = \frac{1.06 - 0.7}{1.3 - 0.7} = \frac{0.36}{0.6} = 0.6$$

**(b) Call**:
- $C_u = \max(65 - 50, 0) = 15$
- $C_d = \max(35 - 50, 0) = 0$
$$C = \frac{0.6 \times 15 + 0.4 \times 0}{1.06} = \frac{9}{1.06} = \$8.49$$

**(c) Put (parity)**:
$$P = C + \frac{K}{1+r} - S = 8.49 + \frac{50}{1.06} - 50$$
$$= 8.49 + 47.17 - 50 = \$5.66$$

**검증 (put 직접 계산)**:
- $P_u = \max(50-65, 0) = 0$, $P_d = \max(50-35, 0) = 15$
- $P = (0.6 \times 0 + 0.4 \times 15)/1.06 = 6/1.06 = \$5.66$ ✓

</details>

### Q6. 계산 — Replicating portfolio (delta)

위 Q5 (S=$50, u=1.3, d=0.7, K=$50, r=6%).

(a) Hedge ratio (delta)?
(b) Replicating portfolio (주식 + 차입)?

<details><summary>답</summary>

**(a) Delta (hedge ratio)**:
$$\Delta = \frac{C_u - C_d}{uS - dS} = \frac{15 - 0}{65 - 35} = \frac{15}{30} = 0.5$$

→ 주식 0.5주 보유.

**(b) Replicating portfolio**:
- 주식 0.5주 매수 + 차입 B
- 만기 up: 0.5 × 65 − B(1.06) = 15 → 32.5 − 1.06B = 15 → B = $16.51
- 만기 down: 0.5 × 35 − 16.51 × 1.06 = 17.5 − 17.5 = 0 ✓

**Portfolio 비용 (= call 가격)**:
- 0.5 × $50 − $16.51 = $25 − $16.51 = **$8.49** ✓ (Q5 와 일치)

**해석**:
- Call = *주식 0.5주 매수 + $16.51 차입*
- Delta hedging: call 매도 시 0.5주 매수로 hedge
- *No-arbitrage* → replicating portfolio 비용 = option 가격

</details>

### Q7. 계산 — Protective put + Covered call

주식 $100 보유.

(a) Protective put (K=$95, P=$3): 만기 $80, $110 시 가치?
(b) Covered call (K=$110, C=$4): 만기 $80, $130 시 가치?

<details><summary>답</summary>

**(a) Protective put** (주식 + put $95):

| 만기 S_T | 주식 | Put payoff | 합 (−$3 premium) |
|--|--|--|--|
| $80 | $80 | $15 | $95 − $3 = **$92** |
| $110 | $110 | $0 | $110 − $3 = **$107** |

→ Downside $92 로 보호 (floor), upside 유지. "보험".

**(b) Covered call** (주식 + short call $110):

| 만기 S_T | 주식 | Short call | 합 (+$4 premium) |
|--|--|--|--|
| $80 | $80 | $0 | $80 + $4 = **$84** |
| $130 | $130 | −$20 | $130 − $20 + $4 = **$114** |

→ Upside $114 로 제한 (cap), premium 수취. 횡보장 유리.

**비교**:
- Protective put: downside 보호, premium 지불
- Covered call: upside 제한, premium 수취
- *반대 방향* 전략

</details>

### Q8. 계산 — Black-Scholes 직관 (정성)

회사 A 와 B, 동일 S=$50, K=$50, T=1년, r=5%.
- A: σ = 20%
- B: σ = 50%

어느 call 이 더 비싼가? 정량 직관?

<details><summary>답</summary>

**B 가 더 비쌈** (σ 50% > 20%).

**이유 (변동성 효과)**:
- *Call payoff* = $\max(S_T - K, 0)$ — *asymmetric*
- 변동성 ↑ → 큰 상승 가능성 ↑ (큰 이익)
- 큰 하락은 *손실이 0 에서 멈춤* (downside 제한)
- → *변동성이 클수록 call 가치 ↑*

**Black-Scholes 직관**:
- $d_1, d_2$ 의 σ 항
- *Vega > 0* (변동성 민감도 양수)

**대략 추정** (ATM, BS):
- ATM call ≈ $0.4 \times S \times \sigma \times \sqrt{T}$
- A: $0.4 \times 50 \times 0.20 \times 1 = \$4.0$
- B: $0.4 \times 50 \times 0.50 \times 1 = \$10.0$
- → B 가 약 2.5배 비쌈

**함의 (기업 재무)**:
- *Equity = call* (Merton)
- 변동성 ↑ → equity 가치 ↑
- → *Asset substitution*: 주주가 risky project 선호, 채권자 희생
- *고변동성 산업* (biotech, 스타트업) 의 equity = 옵션 성격 강함

</details>

### Q9. 디버그 — "OTM 옵션은 가치 0"

투자자: *"이 call 은 OTM (S=$40, K=$50) 이니 가치 0, 안 사겠다."*

오류?

<details><summary>답</summary>

**오류 — Time value 무시**:

**Option value = Intrinsic + Time value**:
- *Intrinsic* (OTM call) = $\max(40-50, 0) = 0$
- *Time value* = *나머지* (변동성 + 시간 premium)
- → *총 가치 > 0* (만기 전이면)

**왜 OTM 도 가치 있나**:
1. 만기까지 시간 — 주가가 $50 넘을 가능성
2. 변동성 — 큰 상승 가능
3. Asymmetric — 상승 이익 무한, 하락 손실 premium 한정

**예시**:
- S=$40, K=$50, T=1년, σ=40% → call ≈ $2-3 (intrinsic 0 이지만 time value)
- 만기 임박할수록 time value → 0 (theta decay)

**함정의 위험**:
- *OTM 옵션 매도* (naked) → "공짜 premium" 착각
- 그러나 *tail risk* (급등) → 큰 손실 가능
- *변동성 매도* 위험 (LTCM, 2018 volpocalypse)

**Deep OTM 특수**:
- *Lottery ticket* 성격 (낮은 확률, 큰 보상)
- *Behavioral* — 과대평가 경향 (lottery preference)

**시간 가치 소멸 (theta)**:
- 만기 가까울수록 time value 급감
- ATM 옵션의 theta 가 가장 큼
- 옵션 매수자의 적 = 시간

→ OTM ≠ 가치 0. Time value 존재. 변동성 + 시간이 가치 부여.

</details>

### Q10. 면접 — *옵션 framework 가 기업 재무에서 왜 강력*?

<details><summary>답</summary>

**응용**:

**1. Equity = Call on firm value (Merton)**:
- 주주 = $\max(V-D, 0)$, 부채 = strike
- Limited liability 의 옵션 성격

**2. Capital structure (Ch 16-17)**:
- Asset substitution (σ↑ → equity↑ → 주주 risky 선호)
- Debt overhang (deep OTM → 투자 유인 없음)
- Risky debt = risk-free − put

**3. Real options (Ch 7)**:
- Expand = call, Abandon = put, Delay = American call, Switch = option
- 전통 DCF 가 놓치는 flexibility value

**4. Corporate securities**:
- Convertible bond = bond + call (Ch 24)
- Warrant = call (회사 발행)
- Callable bond = bond − call
- Putable bond = bond + put

**5. Executive compensation**:
- Stock option = call on own stock
- Incentive alignment + risk-taking 유인

**6. Insurance / Guarantees**:
- Deposit insurance (FDIC) = put
- Loan guarantee = put
- Pension PBGC = put

**7. Capital budgeting**:
- Staged investment = compound option
- R&D = call on future product
- Natural resource = option on commodity

**왜 강력**:
1. Asymmetry 포착 (전통 NPV 는 expected)
2. Volatility 가치 (불확실성이 가치)
3. Dynamic decision (정보 도착 시 재결정)
4. 통합 framework (equity, debt, real assets)

**한계**:
- Non-traded underlying → volatility 추정 어려움
- Exercise complexity
- Over-application 위험

**유명**:
- Merton (1974): structural credit model → KMV, Moody's
- Black-Scholes (1973): Nobel 1997
- Real options (Dixit-Pindyck, Trigeorgis)

**현대**: CDS (put on credit), VIX, structured products, crypto options.

> 옵션 framework = asymmetry + volatility value + dynamic decision. Equity = call (Merton), real options, corporate securities. 전통 DCF 가 놓치는 유연성·비대칭성. 단, non-traded volatility 추정 + over-application 주의.

</details>
