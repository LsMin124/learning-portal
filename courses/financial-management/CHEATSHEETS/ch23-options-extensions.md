# Ch 23 Options Extensions — 치트시트

> ESO / Startup option / Real options 심화 / Risky debt.

## §1 Executive Stock Options (ESO)

| 속성 | 값 |
|--|--|
| Strike | 부여 시 주가 (ATM) |
| Vesting | 3-4년 |
| Expiration | 10년 |
| Transferable | No |

**목적**: incentive alignment, retention, cash 절약, tax (ISO).

## §2 ESO 회계 (FASB 2004 / ASC 718)

- 과거: ATM 비용 0 (intrinsic)
- 현재: *fair value 비용 처리* (Black-Scholes)

## §3 ESO 논란

| 논란 | 의미 |
|--|--|
| Repricing | 주가 하락 시 strike 인하 |
| Backdating | 부여일 조작 (2006) |
| Excessive comp | CEO-직원 격차 |
| Short-termism | 단기 주가 유인 |

## §4 ESO valuation 조정

- Non-transferable → 조기 행사 (BS 과대)
- Vesting 위험
- Dilution
- → 조정 BS / binomial

## §5 Startup / R&D as Option

| 대상 | 옵션 |
|--|--|
| 적자 스타트업 equity | Call on 미래 가치 |
| Staged investment | Compound option |
| R&D | Call on 제품 |
| Pharma Phase | 단계적 compound |

## §6 Real Options 4종

| Option | Type |
|--|--|
| Expand | Call (pilot → full) |
| Abandon | Put (salvage strike) |
| Delay | American call (timing) |
| Switch | Option (input/output) |

## §7 Real option valuation

1. Black-Scholes (단순)
2. Binomial (단계적, American)
3. Monte Carlo (path-dependent)
4. Decision tree (이산)

## §8 Decision Tree vs Real Option

| | Decision tree | Real option |
|--|--|--|
| 확률 | 실제 | Risk-neutral |
| Discount | Risk-adjusted | Risk-free |
| 적합 | Non-traded, 주관적 | Traded, replicable |

## §9 Option to Delay 가치

- 대기 = downside 제한 + upside 유지
- Asymmetry 가 가치
- 단, *preemption* (경쟁자 진입) 위험

## §10 Risky Debt 옵션 분해

$$\text{Risky debt} = \text{Risk-free debt} - \text{Put on V}$$

- 채권자 = put 매도
- Default = 주주 limited liability

## §11 Credit spread

- = Put option 가치
- 변동성 ↑ → put ↑ → spread ↑

## §12 Merton model

$$E = V N(d_1) - De^{-rT}N(d_2)$$

(Equity = call on firm value)

## §13 Distance-to-Default

$$DD \approx \frac{V - D}{\sigma_V \times V}$$

- 낮을수록 default 확률 ↑
- → EDF (KMV/Moody's)

## §14 Structural credit models

| Model | 특징 |
|--|--|
| Merton (1974) | Equity = call |
| KMV/Moody's | Distance-to-default → EDF |
| Reduced-form | Default intensity (Jarrow-Turnbull) |
| CDS | Put on credit |

## §15 Mergers as options

| 구조 | 옵션 |
|--|--|
| Toehold | Option on full acquisition |
| Staged | Compound option |
| Collar | Floor + cap (put + call) |
| Earnout | Option on target performance |

## §16 실무 응용

| 분야 | 옵션 |
|--|--|
| 유전/광산 | Option on commodity (Brennan-Schwartz) |
| 부동산 | Land = timing option |
| 특허 | Option on commercialization |
| Insurance/Guarantee | Put 매도 (FDIC, PBGC) |

## §17 Real option 3 조건 (남용 방지)

1. **Identifiable** — 구체적 trigger
2. **Exercisable** — 실제 행사 권한
3. **Measurable** — value + volatility 추정

## §18 자주 함정

| 함정 | 정정 |
|--|--|
| ESO 비용 0 | FASB 2004 fair value |
| ESO = BS 그대로 | Non-transferable 조정 |
| Real option 으로 모든 것 | 3 조건 충족 시만 |
| Decision tree = real option | 확률·rate 다름 |
| Risky debt 옵션 무시 | = risk-free − put |
| Negative NPV = 거부 | Real option 고려 (남용 주의) |
| Repricing 정당 | Incentive 왜곡 |

## §19 핵심 mindmap

```
Options Extensions
├── ESO (incentive, FASB 2004, repricing 논란)
├── Startup/R&D = option (compound)
├── Real options 심화
│   ├── Expand/Abandon/Delay/Switch
│   └── 3 조건 (identifiable/exercisable/measurable)
├── Decision tree vs Real option
└── Risky debt
    ├── = risk-free − put
    ├── Merton model
    └── Distance-to-default (KMV)
```

## §20 1-line summary

> **Options 응용 — *ESO* (FASB 2004 fair value, repricing/backdating 논란). *Startup/R&D = option* (compound, 변동성 가치). *Real options 심화* (expand/abandon/delay/switch), 단 *identifiable+exercisable+measurable* 일 때만. *Decision tree* (이산, 실제 확률) vs *real option* (risk-neutral). *Risky debt = risk-free − put* (Merton, distance-to-default, KMV).**
