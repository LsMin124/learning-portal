# Ch 22 Options and Corporate Finance — 치트시트

> Call/Put / 6 요인 / Parity / Binomial / Black-Scholes / Equity as call.

## §1 기본 용어

| 용어 | 의미 |
|--|--|
| Call | 매수 권리 |
| Put | 매도 권리 |
| Strike K | 행사가 |
| American | 만기 전 행사 |
| European | 만기만 |

## §2 Payoff

| | 공식 |
|--|--|
| Call | $\max(S_T - K, 0)$ |
| Put | $\max(K - S_T, 0)$ |

## §3 4 기본 포지션

| 포지션 | 시각 | Max 손실 | Max 이익 |
|--|--|--|--|
| Long call | Bullish | Premium | 무한 |
| Short call | Bearish | 무한 | Premium |
| Long put | Bearish | Premium | K−P |
| Short put | Bullish | K−P | Premium |

## §4 6 가치 요인

| 요인 ↑ | Call | Put |
|--|--|--|
| 주가 S | ↑ | ↓ |
| Strike K | ↓ | ↑ |
| 변동성 σ | ↑ | ↑ |
| 만기 T | ↑ | ↑ |
| 무위험 r | ↑ | ↓ |
| 배당 | ↓ | ↑ |

→ 변동성 ↑ → call+put 둘 다 ↑.

## §5 Value 분해

$$\text{Option} = \text{Intrinsic} + \text{Time value}$$

- Intrinsic = $\max(S-K, 0)$ (call)
- Time value → 0 at expiration (theta decay)

## §6 Put-Call Parity

$$C + \frac{K}{(1+r)^T} = P + S$$

(연속: $C + Ke^{-rT} = P + S$)

- Synthetic stock = C − P + bond
- Synthetic call = P + S − bond

## §7 Binomial (1-period)

$$p = \frac{(1+r) - d}{u - d}$$

$$C = \frac{p C_u + (1-p) C_d}{1+r}$$

→ Risk-neutral probability (실제 확률 아님).

## §8 Replicating portfolio

$$\Delta = \frac{C_u - C_d}{uS - dS}$$

→ 주식 Δ주 + 차입 = call replicate.

## §9 Black-Scholes

$$C = S N(d_1) - Ke^{-rT}N(d_2)$$

$$d_1 = \frac{\ln(S/K) + (r+\sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

- $N(d_1)$ = delta
- $N(d_2)$ = risk-neutral 행사 확률

## §10 BS 가정

1. European
2. No dividends (기본)
3. Lognormal 주가
4. Constant σ, r
5. No transaction cost
6. Continuous trading

## §11 Greeks

| Greek | 의미 |
|--|--|
| Delta (Δ) | ∂C/∂S |
| Gamma (Γ) | ∂Δ/∂S |
| Vega | ∂C/∂σ |
| Theta (Θ) | ∂C/∂T (감소) |
| Rho (ρ) | ∂C/∂r |

## §12 Implied volatility

- 시장 가격 → σ 역산
- VIX = S&P 500 IV ("공포 지수")
- Volatility smile/skew (BS 가정 위배)

## §13 ATM 대략 추정

$$C_{ATM} \approx 0.4 \times S \times \sigma \times \sqrt{T}$$

## §14 Option Combinations

| 전략 | 구성 |
|--|--|
| Protective put | 주식 + put (보험) |
| Covered call | 주식 + short call (premium) |
| Straddle | call + put (변동성 베팅) |
| Bull spread | low K call 매수 + high K 매도 |

## §15 Equity as Call Option (Merton)

$$\text{Equity} = \max(V - D, 0)$$

- Strike = 부채 D
- Underlying = firm value V
- 채권자 = risk-free debt − put

## §16 옵션 함의 (capital structure)

| 현상 | 옵션 설명 |
|--|--|
| Asset substitution | σ↑ → equity(call)↑ |
| Debt overhang | deep OTM → 투자 유인 없음 |
| Default | put (주주 → 채권자) |
| Risk premium | 채권자 put 매도 |

## §17 Corporate securities = options

| 증권 | 옵션 분해 |
|--|--|
| Convertible bond | bond + call |
| Warrant | call (회사 발행) |
| Callable bond | bond − call |
| Putable bond | bond + put |
| Stock option | call on own stock |

## §18 Real options (Ch 7)

| Real option | 옵션 type |
|--|--|
| Expand | Call |
| Abandon | Put |
| Delay | American call |
| Switch | Option |

## §19 자주 함정

| 함정 | 정정 |
|--|--|
| σ↑ → call만 ↑ | 둘 다 ↑ |
| Value = intrinsic | + time value |
| Binomial 실제 확률 | Risk-neutral |
| BS = American | European 기본 |
| Equity ≠ option | Equity = call (Merton) |
| OTM = 가치 0 | Time value 존재 |
| 배당 무시 | 배당↑ → call↓ put↑ |

## §20 핵심 mindmap

```
Options
├── Payoff (call/put, 4 포지션)
├── 6 요인 (S/K/σ/T/r/div)
├── Parity (C + PV(K) = P + S)
├── Pricing
│   ├── Binomial (risk-neutral p)
│   └── Black-Scholes (N(d1), N(d2))
├── Greeks (Δ, Γ, Vega, Θ, ρ)
└── 기업 재무
    ├── Equity = call (Merton)
    ├── Corporate securities
    └── Real options
```

## §21 1-line summary

> **Options — *Call* $\max(S-K,0)$, *Put* $\max(K-S,0)$. *6 요인* (변동성이 핵심, call+put 둘 다 ↑). *Parity*: $C+PV(K)=P+S$. *Binomial* (risk-neutral p) + *Black-Scholes* ($SN(d_1)-Ke^{-rT}N(d_2)$). *Equity = call on firm value* (Merton) → asset substitution, debt overhang. *Convertible/warrant/real options* 모두 옵션 framework.**
