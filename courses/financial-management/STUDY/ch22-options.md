# Chapter 22: Options and Corporate Finance — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 22** (책 p.691~735).
> 22장은 *옵션* — Call/Put, payoff, put-call parity, Black-Scholes, binomial, 그리고 *기업 재무의 옵션 관점*.

이 장의 *지적 무게중심*:
1. **Call / Put** — payoff, profit
2. **Option 가치 결정 요인** — 6 factors
3. **Put-Call Parity**
4. **Binomial model** — risk-neutral valuation
5. **Black-Scholes**
6. **Equity as a call option** on firm value

---

## §1 Options 기본

### §1.1 정의

| 용어 | 의미 |
|--|--|
| **Call** | *매수* 권리 (strike K 에 살 권리) |
| **Put** | *매도* 권리 (strike K 에 팔 권리) |
| **Strike (exercise) price K** | 행사 가격 |
| **Expiration** | 만기 |
| **Premium** | 옵션 가격 |
| **American** | 만기 전 언제든 행사 |
| **European** | 만기에만 행사 |

### §1.2 Long vs Short

- *Long*: 옵션 매수 (권리 보유)
- *Short (writer)*: 옵션 매도 (의무 부담, premium 수취)

---

## §2 Payoff + Profit

### §2.1 Call payoff (만기)

$$\text{Call payoff} = \max(S_T - K, 0)$$

- $S_T$ = 만기 주가
- *In-the-money* (ITM): $S_T > K$
- *At-the-money* (ATM): $S_T = K$
- *Out-of-the-money* (OTM): $S_T < K$

### §2.2 Put payoff (만기)

$$\text{Put payoff} = \max(K - S_T, 0)$$

### §2.3 Profit (premium 차감)

- *Long call profit* = $\max(S_T - K, 0) - C$
- *Long put profit* = $\max(K - S_T, 0) - P$

### §2.4 Payoff diagram

```
Long Call:              Long Put:
profit                  profit
  |      /                |  \
  |     /                 |   \
0 |----/------ S_T      0 |----\------ S_T
  |__ /  K                |   K \___
   -C                      -P
```

### §2.5 4 기본 포지션

| 포지션 | 시각 | Max 손실 | Max 이익 |
|--|--|--|--|
| Long call | Bullish | Premium | 무한 |
| Short call | Bearish | 무한 | Premium |
| Long put | Bearish | Premium | K−Premium |
| Short put | Bullish | K−Premium | Premium |

---

## §3 Option Combinations

### §3.1 Protective put

- *주식 + put 매수* → downside 보호 (보험)
- "Portfolio insurance"

### §3.2 Covered call

- *주식 보유 + call 매도* → premium 수취, upside 제한

### §3.3 Straddle

- *Call + Put (같은 K)* → 변동성 베팅 (방향 무관)

### §3.4 Spread

- *Bull spread*: low K call 매수 + high K call 매도
- *Bear spread*: 반대
- *Butterfly*: 변동성 낮을 것 베팅

---

## §4 Option 가치 결정 6 요인

| 요인 | Call | Put |
|--|--|--|
| **주가 (S) ↑** | ↑ | ↓ |
| **Strike (K) ↑** | ↓ | ↑ |
| **변동성 (σ) ↑** | ↑ | ↑ |
| **만기 (T) ↑** | ↑ | ↑ (보통) |
| **무위험 이자율 (r) ↑** | ↑ | ↓ |
| **배당 ↑** | ↓ | ↑ |

### §4.1 핵심 직관

- **변동성 ↑** → call, put 모두 *↑* (asymmetric upside, 손실은 premium 한정)
- **시간 ↑** → 더 많은 기회 → 가치 ↑
- **변동성이 옵션 가치의 핵심** (Black-Scholes 의 σ)

### §4.2 Intrinsic value vs Time value

$$\text{Option value} = \text{Intrinsic value} + \text{Time value}$$

- *Intrinsic*: $\max(S-K, 0)$ (call) — 즉시 행사 가치
- *Time value*: 나머지 (변동성 + 시간 premium)

---

## §5 Put-Call Parity

### §5.1 공식

$$C + \frac{K}{(1+r)^T} = P + S$$

또는 (연속복리):
$$C + Ke^{-rT} = P + S$$

### §5.2 직관

- *왼쪽*: Call + 무위험채권 (K 의 PV)
- *오른쪽*: Put + 주식
- → *동일 payoff* (만기 둘 다 $\max(S_T, K)$)

### §5.3 차익거래

- Parity 깨지면 *arbitrage*
- *Synthetic position* 구성 가능:
  - Synthetic call = Put + Stock − Bond
  - Synthetic stock = Call − Put + Bond

### §5.4 예제

S = $50, K = $50, r = 5%, T = 1년, C = $6.

$$P = C + \frac{K}{1+r} - S = 6 + \frac{50}{1.05} - 50 = 6 + 47.62 - 50 = \$3.62$$

---

## §6 Binomial Option Pricing

### §6.1 1-period model

**Setup**: 주가 S, 1기간 후 *up (uS)* 또는 *down (dS)*.

**Risk-neutral probability**:
$$p = \frac{(1+r) - d}{u - d}$$

**Call value**:
$$C = \frac{p \cdot C_u + (1-p) \cdot C_d}{1+r}$$

- $C_u = \max(uS - K, 0)$, $C_d = \max(dS - K, 0)$

### §6.2 Risk-neutral valuation 직관

- *실제 확률* 불필요 → *risk-neutral probability* 사용
- *No-arbitrage* 로부터 도출
- *Replicating portfolio* (주식 Δ + 차입) 와 동일

### §6.3 예제

S = $100, u = 1.2, d = 0.8, K = $100, r = 5%.

- $C_u = \max(120 - 100, 0) = 20$
- $C_d = \max(80 - 100, 0) = 0$
- $p = (1.05 - 0.8)/(1.2 - 0.8) = 0.25/0.4 = 0.625$
- $C = (0.625 \times 20 + 0.375 \times 0)/1.05 = 12.5/1.05 = \$11.90$

### §6.4 Replicating portfolio (delta hedging)

- *Δ (hedge ratio)* = $(C_u - C_d)/(uS - dS)$
- 위 예: Δ = 20/40 = 0.5 (주식 0.5주 매수 + 차입)
- *Multi-period* → 더 정밀 (CRR model)

---

## §7 Black-Scholes Model

### §7.1 공식

$$C = S \cdot N(d_1) - K e^{-rT} N(d_2)$$

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$$

$$d_2 = d_1 - \sigma\sqrt{T}$$

- $N(\cdot)$ = 표준정규 누적분포

### §7.2 가정

1. *European* option (만기 행사)
2. *No dividends* (기본형)
3. *Lognormal* 주가 분포
4. *Constant σ, r*
5. *No transaction costs*
6. *Continuous trading*

### §7.3 직관

- $N(d_1)$ = delta (hedge ratio)
- $N(d_2)$ = risk-neutral 행사 확률
- *Continuous-time* binomial 의 극한

### §7.4 Put (parity 로부터)

$$P = Ke^{-rT}N(-d_2) - S N(-d_1)$$

### §7.5 Greeks

| Greek | 의미 |
|--|--|
| **Delta (Δ)** | ∂C/∂S (주가 민감도) |
| **Gamma (Γ)** | ∂Δ/∂S (delta 변화) |
| **Vega** | ∂C/∂σ (변동성 민감도) |
| **Theta (Θ)** | ∂C/∂T (시간 감소) |
| **Rho (ρ)** | ∂C/∂r (금리 민감도) |

### §7.6 Implied volatility

- *시장 가격* → σ 역산
- *VIX* = S&P 500 implied volatility ("공포 지수")
- *Volatility smile/skew* (실제 ≠ Black-Scholes 가정)

---

## §8 Equity as a Call Option (기업 재무 핵심)

### §8.1 통찰 (Merton)

> *주주의 equity* = *firm value 에 대한 call option*.

- *Strike* = 부채 face value (D)
- *Underlying* = firm value (V)
- 만기 (부채 만기) 에:
  - $V > D$: 주주가 부채 갚고 잔여 ($V - D$) 차지 → call 행사
  - $V < D$: 주주가 *default*, firm 을 채권자에 넘김 → call 포기

$$\text{Equity} = \max(V - D, 0)$$

### §8.2 채권자 관점

> *Risky debt* = *risk-free debt − put option*.

- 채권자 = firm 매수 + put 매도 (주주에게)
- *Put* = default option (주주의 limited liability)

### §8.3 함의

**1. Asset substitution (Ch 17 연결)**:
- *변동성 ↑* → equity (call) 가치 ↑
- 주주가 *risky project* 선호
- 채권자 손해

**2. Debt overhang**:
- Deep OTM call (V << D) → 주주 투자 유인 없음

**3. 부채 = 옵션 매도**:
- 채권자는 *put 매도* → default risk premium 요구

### §8.4 Real options 연결 (Ch 7)

- *Option to expand* = call
- *Option to abandon* = put
- *Option to delay* = American call
- 기업 의사결정 전반에 옵션 framework

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 변동성 ↑ → call만 ↑ | Call + Put 둘 다 ↑ |
| 2 | Option value = intrinsic | + time value |
| 3 | Put-call parity 무시 | C + PV(K) = P + S |
| 4 | Binomial 에 실제 확률 | Risk-neutral probability |
| 5 | Black-Scholes = American | European 기본 (배당 시 조정) |
| 6 | Equity ≠ option | Equity = call on firm value (Merton) |
| 7 | 배당 무시 | 배당 ↑ → call ↓, put ↑ |
| 8 | OTM = 가치 0 | Time value 존재 (만기 전) |

---

## §10 자가점검

1. *Call / Put payoff*?
2. *Option 6 요인* + 방향?
3. *Put-Call Parity*?
4. *Binomial* risk-neutral probability?
5. *Black-Scholes* 공식 + 가정?
6. *Equity as call option* (Merton)?

<details><summary>해답</summary>

1. Call: $\max(S_T-K,0)$. Put: $\max(K-S_T,0)$.
2. S↑(C↑P↓), K↑(C↓P↑), σ↑(둘다↑), T↑(둘다↑), r↑(C↑P↓), 배당↑(C↓P↑).
3. $C + K/(1+r)^T = P + S$ (또는 $Ke^{-rT}$).
4. $p = ((1+r)-d)/(u-d)$, $C = [pC_u + (1-p)C_d]/(1+r)$.
5. $C = S N(d_1) - Ke^{-rT}N(d_2)$. 가정: European, no dividend, lognormal, constant σ/r, no tx cost, continuous trading.
6. Equity = $\max(V-D, 0)$ = call on firm value, strike = 부채 D. 채권자 = risk-free debt − put.

</details>

---

## §11 다음 학습으로

- **Ch 23** — Options extensions (employee options, real options)
- **Ch 24** — Warrants and convertibles
- **Ch 25** — Derivatives and hedging
- **Ch 7** — Real options (recap)

---

## §12 한 줄 요약

> **Options — *Call* $\max(S-K,0)$, *Put* $\max(K-S,0)$. *6 요인* (S, K, σ, T, r, 배당). *변동성이 핵심* (call+put 모두 ↑). *Put-call parity*: $C + PV(K) = P + S$. *Binomial* (risk-neutral prob) + *Black-Scholes* ($C = SN(d_1) - Ke^{-rT}N(d_2)$). *Equity = call option on firm value* (Merton), 채권자 = risk-free debt − put → asset substitution, debt overhang 설명.**
