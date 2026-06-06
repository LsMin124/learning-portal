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

## §0 도입 — *비대칭이 만드는 가치*

> **핵심 한 문장**: 옵션은 *권리지 의무가 아니라서* payoff 가 한쪽으로만 꺾인다(hockey stick) — 이 **비대칭** 이 "변동성이 클수록 가치가 크다"는 반직관을 낳고, 끝내 *부채 있는 기업의 주식 자체가 firm value 에 대한 call option*(Merton)이라는 통찰로 이어진다.

22장은 네 층으로 쌓인다:

1. **payoff 의 기하학** (§2–3): call 은 $\max(S-K,0)$(figure 22.1), put 은 $\max(K-S,0)$(figure 22.2) — 손실은 premium 으로 한정되고 이익만 열려 있다. 이 조각들을 더하면 *protective put*(figure 22.4)·*covered call*(figure 22.6) 같은 구조화 포지션이 나온다.
2. **무엇이 옵션을 비싸게 하나** (§4): 6 요인 중 *변동성* 이 왕이다 — 손실은 막혀 있으니 더 출렁일수록(figure 22.9 의 넓은 분포 B) 위쪽 가능성만 커진다. 가치는 항상 상·하한 사이에 갇힌다(figure 22.7·22.8).
3. **가격을 어떻게 매기나** (§5–7): *put-call parity* $C+PV(K)=P+S$(figure 22.5)가 네 자산을 묶고, *binomial*(risk-neutral 확률)과 그 극한인 *Black-Scholes* $C=SN(d_1)-Ke^{-rT}N(d_2)$ 가 값을 준다. $N(d)$ 는 누적정규확률(figure 22.10).
4. **기업 = 옵션** (§8): 부채 만기에 주주는 $V>D$ 면 빚을 갚고 잔여를 갖고, $V<D$ 면 walk away — 곧 *주식 = call*(figure 22.11), *채권 = 무위험채권 − put*(figure 22.12). 여기서 asset substitution·debt overhang 이 따라 나온다.

관통하는 한 단어는 **비대칭**: 꺾인 payoff 가 변동성을 *자산* 으로 바꾸고, 유한책임이 주식을 *옵션* 으로 바꾼다.

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

![Figure 22.1 — The Value of a Call Option on the Expiration Date. 교재 p.675](/courses/financial-management/figures/ch22/fig-22-1.png)

> **직관**: call payoff 의 *하키스틱*. 만기 주가가 행사가(100) 아래면 가치 0(왼쪽 평평), 위면 $S-K$ 만큼 1:1 상승(오른쪽 45°). 손실은 0 에서 멈추고 이익만 열린 *비대칭* — 옵션의 모든 직관이 이 꺾임에서 나온다.

### §2.2 Put payoff (만기)

$$\text{Put payoff} = \max(K - S_T, 0)$$

![Figure 22.2 — The Value of a Put Option on the Expiration Date. 교재 p.676](/courses/financial-management/figures/ch22/fig-22-2.png)

> **직관**: put 은 call 의 거울상. 주가가 행사가(50) 위면 가치 0, 아래로 갈수록 $K-S$ 만큼 가치 상승(최대 $K$, 주가 0 일 때). 하락에 베팅하되 손실은 premium 한정.

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

![Figure 22.3 — The Payoffs to Sellers of Calls and Puts and to Buyers of Common Stock. 교재 p.678](/courses/financial-management/figures/ch22/fig-22-3.png)

> **직관**: *매도자(writer)* 의 payoff — 매수자를 위아래로 뒤집은 것. *Sell a call*: 주가 오르면 손실 무한(우하향). *Sell a put*: 주가 폭락 시 손실(좌하향). *Buy stock*: 그냥 45° 직선. 옵션은 *zero-sum* — 매수자 이익 = 매도자 손실.

---

## §3 Option Combinations

### §3.1 Protective put

- *주식 + put 매수* → downside 보호 (보험)
- "Portfolio insurance"

![Figure 22.4 — Payoff to the Combination of Buying a Put and Buying the Underlying Stock. 교재 p.680](/courses/financial-management/figures/ch22/fig-22-4.png)

> **직관**: *protective put* = 주식 + put. 주식의 우상향(왼쪽)에 put 의 좌상향(가운데)을 더하면 — 하단이 $K$ 에서 *평평하게 막힌* L자 곡선(오른쪽). 주가가 아무리 떨어져도 $K$ 는 보장되는 *포트폴리오 보험*.

### §3.2 Covered call

- *주식 보유 + call 매도* → premium 수취, upside 제한

![Figure 22.6 — Payoff to the Combination of Buying a Stock and Selling a Call. 교재 p.682](/courses/financial-management/figures/ch22/fig-22-6.png)

> **직관**: *covered call* = 주식 + call 매도. 주식 우상향(왼쪽)에 call 매도의 우하향(가운데)을 더하면 — 위쪽이 $K$ 에서 *천장에 막힌* 곡선(오른쪽). upside 를 포기하는 대가로 premium 을 받는다.

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

![Figure 22.9 — Distribution of Common Stock Price at Expiration for Both Security A and Security B. 교재 p.686](/courses/financial-management/figures/ch22/fig-22-9.png)

> **직관**: 왜 *변동성* 이 옵션 가치의 핵심인가. 같은 행사가에 두 주식 — A(좁은 분포)와 B(넓은 분포). 손실은 어차피 premium 으로 막혀 있으니, B 의 *더 두꺼운 오른쪽 꼬리*(큰 상승 가능성)만 옵션 가치에 더해진다. 그래서 σ↑ → call·put 모두 ↑.

### §4.2 Intrinsic value vs Time value

$$\text{Option value} = \text{Intrinsic value} + \text{Time value}$$

- *Intrinsic*: $\max(S-K, 0)$ (call) — 즉시 행사 가치
- *Time value*: 나머지 (변동성 + 시간 premium)

![Figure 22.7 — The Upper and Lower Boundaries of Call Option Values. 교재 p.683](/courses/financial-management/figures/ch22/fig-22-7.png)

> **직관**: 옵션 가치가 갇히는 *띠*. *상한* = 주가 자체(call 이 주식보다 비쌀 순 없다). *하한* = 주가 − 행사가(내재가치). 실제 call 값은 이 두 경계 사이 색칠된 영역 안에 — 만기 전엔 항상 *하한보다 위*(time value).

![Figure 22.8 — Value of an American Call as a Function of Stock Price. 교재 p.685](/courses/financial-management/figures/ch22/fig-22-8.png)

> **직관**: 그 띠 안에서 실제 call 값은 *완만한 곡선*(점선). 깊은 OTM 에선 0 에 붙고, 깊은 ITM 에선 하한선(주가−K)에 수렴. 곡선과 하한의 *간격 = time value*, ATM 부근에서 가장 크다.

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

![Figure 22.5 — Payoff to the Combination of Buying a Call and Buying a Zero Coupon Bond. 교재 p.680](/courses/financial-management/figures/ch22/fig-22-5.png)

> **직관**: put-call parity 의 그림. *call + 무위험채권(K)* 의 payoff(오른쪽)가 figure 22.4 의 *put + 주식* 과 똑같다 — 둘 다 $\max(S,K)$. 그래서 $C+PV(K)=P+S$. 네 자산 중 셋을 알면 넷째는 복제(synthetic)된다.

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

![Figure 22.10 — Graph of Cumulative Probability (N(d)). 교재 p.692](/courses/financial-management/figures/ch22/fig-22-10.png)

> **직관**: Black-Scholes 의 $N(d)$ 가 무엇인가 — 표준정규분포의 *누적확률*. 종형곡선에서 $d$(여기 .3742) 왼쪽 면적이 $N(.3742)=.6459$. $N(d_1)$=delta(헤지비율), $N(d_2)$=risk-neutral 행사확률. (책 라벨은 Table 22.10)

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

![Figure 22.11 — Cash Flow to Stockholders of Popov Company as a Function of Cash Flow to the Firm. 교재 p.696](/courses/financial-management/figures/ch22/fig-22-11.png)

> **직관**: *주식 = firm 에 대한 call*. 가로축 firm 현금흐름, 세로축 주주 몫. 부채 $800 이하면 주주는 0(채권자에 넘김), 초과분만 45° 로 가져간다 — 정확히 행사가 $800 짜리 call payoff. 유한책임이 주식을 옵션으로 만든다.

### §8.2 채권자 관점

> *Risky debt* = *risk-free debt − put option*.

- 채권자 = firm 매수 + put 매도 (주주에게)
- *Put* = default option (주주의 limited liability)

![Figure 22.12 — Cash Flow to Bondholders of Popov Company as a Function of Cash Flow to the Firm. 교재 p.697](/courses/financial-management/figures/ch22/fig-22-12.png)

> **직관**: *채권 = 무위험채권 − put*. 채권자는 firm 현금흐름이 $800 미만이면 그 전부를(우상향), 초과하면 $800 에서 *천장에 막힘*. 즉 채권자는 firm 을 소유하되 주주에게 call 을 *매도* 한 것 — default risk premium 의 정체.

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
