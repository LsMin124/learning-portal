# Ch 4 Discounted Cash Flow Valuation — 치트시트

> Time value / PV-FV / Annuity-Perpetuity / Compounding / DCF.

## §1 핵심 공식

| | 공식 |
|--|--|
| FV | $PV(1+r)^T$ |
| PV | $FV / (1+r)^T$ |
| NPV | $-Cost + PV(future\ CF)$ |
| EAR | $(1+APR/m)^m - 1$ |
| Continuous | $e^{rT}$ |

## §2 PV/FV 의 *Rule of 72*

> *원금 2배* 시간 ≈ 72 / rate (%)

| Rate | Time to double |
|--|--|
| 4% | 18 year |
| 6% | 12 year |
| 8% | 9 year |
| 10% | 7.2 year |
| 12% | 6 year |
| 24% | 3 year |

## §3 Annuity 의 4 종류

| | 공식 | 의미 |
|--|--|--|
| Ordinary Annuity | $C \times \frac{1-(1+r)^{-T}}{r}$ | 기말 지불 |
| Annuity Due | Ordinary × (1+r) | 기초 지불 |
| Perpetuity | $C/r$ | 영구 |
| Growing Perpetuity | $C_1 / (r-g)$ | 영구 + 성장 (r>g) |
| Growing Annuity | $\frac{C_1}{r-g}[1 - (\frac{1+g}{1+r})^T]$ | 한정 + 성장 |

## §4 Compounding 빈도의 EAR (APR 12%)

| Frequency | EAR |
|--|--|
| Annual (m=1) | 12.00% |
| Semi-annual (m=2) | 12.36% |
| Quarterly (m=4) | 12.55% |
| Monthly (m=12) | 12.68% |
| Daily (m=365) | 12.747% |
| Continuous | 12.750% |

## §5 Fisher Equation

$$1 + r_{nominal} = (1 + r_{real}) \times (1 + \pi)$$

근사:
$$r_{nominal} \approx r_{real} + \pi$$

## §6 Loan Types

| | 만기 지불 | 매 기간 |
|--|--|--|
| Pure discount | Principal | 0 |
| Interest-only | Principal | Interest |
| Amortizing | 0 | Principal + Interest |
| Balloon | Large | Partial |

## §7 Mortgage Math

$$PMT = \frac{PV \times r}{1 - (1+r)^{-T}}$$

**30yr $400K, APR 6% example**:
- PMT = $2398/month
- Total: $863K
- Interest: $463K (원금보다 많음)

## §8 Front-loaded interest

| Year | Principal % of payment |
|--|--|
| 1 | ~17% |
| 10 | ~30% |
| 20 | ~57% |
| 30 | ~99% |

→ *초기에 거의 이자만*.

## §9 DCF 의 기본

$$V_0 = \sum_{t=1}^{T} \frac{CF_t}{(1+r)^t} + \frac{TV}{(1+r)^T}$$

## §10 Terminal Value 2 방법

| | 공식 |
|--|--|
| Gordon Growth | $CF_{T+1} / (r-g)$ |
| Exit Multiple | $EBITDA_T \times Multiple$ |

## §11 TV 의 *dominance*

| Forecast horizon | TV % of total |
|--|--|
| 5 year | ~75-85% |
| 10 year | ~60-75% |
| 15 year | ~45-60% |
| 20 year | ~30-45% |

## §12 *Real options* (Ch 7, 22)

- Option to expand / abandon / delay / switch

→ 전통 DCF 의 *static* 한계 보완.

## §13 산업별 valuation 의 weight

| Industry | Primary method |
|--|--|
| Mature firm | DCF |
| Tech startup | Revenue multiple |
| Bank | P/B, ROE |
| Real estate | NOI / Cap rate |
| Oil/Mining | NPV + commodity scenario |
| Distressed | Liquidation + going-concern |
| M&A | Precedent transaction |

## §14 Famous DCF cases

| Firm | Year | DCF assumed | 결과 |
|--|--|--|--|
| AOL Time Warner | 2000 | Perpetual high g | $99B write-off |
| Yahoo | 2008 | Reject Microsoft $44B | 2017 $4.5B sold |
| Nortel | 2000 | Telecom growth | 2009 파산 |
| Tesla | 2020s | $1T+ | Justification 의문 |
| WeWork | 2019 | $47B | $9B, IPO 취소 |

## §15 자주 빠지는 함정

| 함정 | 정정 |
|--|--|
| Nominal CF + real r 혼합 | Consistency |
| APR = EAR | Compounding 횟수 확인 |
| g ≥ r perpetuity | 무한대, multi-stage |
| TV 가 전체의 90% | Sensitivity 검토 |
| 같은 single g 영원히 | Stage 분리 |
| Annuity vs Annuity Due | Due 는 (1+r)x |

## §16 Damodaran 의 best practice

1. Multiple methods (3-5 triangulation)
2. Sensitivity (grid)
3. Reverse DCF (market implied)
4. Margin of safety (Buffett's 30%)
5. Living model (continuous update)
6. Pre-mortem (failure analysis)

## §17 Stage 분리 예 (multi-stage DCF)

```
Stage 1 (Year 1-5)   : High growth (예: 20%)
Stage 2 (Year 6-10)  : Transition (10% → 5%)
Stage 3 (Year 11+)   : Stable (3%) → Terminal Value
```

## §18 Damodaran's 6 inputs to DCF

1. Cash flow 추정
2. Growth rate
3. Length of high growth
4. Risk (discount rate)
5. Reinvestment 가정
6. Terminal Value 가정

→ 각 input 의 *judgment + sensitivity*.

## §19 핵심 mindmap

```
DCF Valuation
├── Time value of money
│   ├── FV = PV(1+r)^T
│   ├── PV = FV/(1+r)^T
│   └── Rule of 72
├── Compounding (APR vs EAR, continuous)
├── Closed forms
│   ├── Perpetuity (C/r)
│   ├── Growing perp (C/(r-g))
│   ├── Annuity (factor)
│   └── Growing annuity
├── Loan types
└── Firm valuation
    ├── DCF = Σ CF/(1+r)^t + TV
    ├── TV = Gordon Growth or Exit Multiple
    └── TV dominance 60-80%, sensitivity critical
```

## §20 1-line summary

> **Time value. *FV/PV* 의 compounding/discounting. Closed forms (perpetuity, growing perpetuity, annuity, growing annuity). *APR* vs *EAR*. *DCF* = Σ FCF/(1+r)^t + TV. *Terminal Value* 가 *60-80% dominance*. *Triangulation* + *sensitivity* + *reverse DCF*.**
