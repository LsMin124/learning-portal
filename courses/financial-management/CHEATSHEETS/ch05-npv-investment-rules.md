# Ch 5 NPV and Other Investment Rules — 치트시트

> NPV / Payback / IRR / PI / MIRR / 실제 회사.

## §1 핵심 공식

| | 공식 |
|--|--|
| NPV | $-C_0 + \sum \frac{CF_t}{(1+r)^t}$ |
| IRR | NPV = 0 의 r |
| PI | PV future CF / |Initial| |
| Payback | 회수 까지 기간 |
| Discounted Payback | Payback + discount |
| MIRR | $(TV/|PV_{out}|)^{1/T} - 1$ |

## §2 Decision Rules

| Method | Accept |
|--|--|
| NPV | > 0 |
| IRR | > hurdle (investing); < hurdle (financing) |
| PI | > 1 |
| Payback | < cutoff |

## §3 NPV 의 5 우수성

1. Cash flow timing + magnitude
2. Risk via discount rate
3. Additive
4. Value creation 직접 측정
5. Mutual exclusive 명확

## §4 Payback 의 3 fatal flaw

1. Time value 무시
2. Post-payback 무시
3. 임의 cutoff

## §5 IRR 의 4 problem case

| # | Case | 해결 |
|--|--|--|
| 1 | Multiple IRR | NPV, MIRR |
| 2 | No IRR | NPV |
| 3 | Financing project | 역방향 rule |
| 4 | Mutually exclusive | Incremental IRR or NPV |

## §6 Conventional vs Non-conventional

| Pattern | Type |
|--|--|
| -, +, +, +, ... | Conventional |
| -, +, -, +, ... | Non-conventional (multiple IRR) |
| +, -, -, ... | Financing (reverse rule) |

## §7 NPV vs IRR — *crossover*

```
NPV
 |  \
 |   \   (B 가 NPV 우월)
 |    \
 |     X--- crossover rate
 |      \
 |________\______ r
           IRR(A) IRR(B)
```

→ r 이 *crossover 보다 작으면 B*, *크면 A*.

## §8 MIRR Steps

1. Outflow: PV at finance rate
2. Inflow: TV at reinvest rate
3. $(1+MIRR)^T = TV / |PV|$

## §9 Capital Rationing 의 PI

```
NPV-only:   largest project (E)
PI-ranked:  most efficient ($/$)
LP optimal: total NPV 최대 조합
```

→ *Restricted budget* 에서 *PI* 가 *NPV alone 보다 우월*.

## §10 실제 회사 (Graham-Harvey 2001)

| Method | Always/Often |
|--|--|
| IRR | 76% |
| NPV | 75% |
| Payback | 57% |
| Sensitivity | 52% |
| Discounted Payback | 30% |
| Accounting RoR | 20% |
| PI | 12% |

## §11 크기 별

| | Large | Small |
|--|--|--|
| NPV/IRR | Dominant | Sometimes |
| Payback | Suppl | Primary |
| Sensitivity | Standard | Rare |

## §12 산업별 primary

| Industry | Primary |
|--|--|
| Oil/Gas | NPV + scenario |
| Mining | NPV + real option |
| Real estate | IRR (convention) |
| Tech | NPV + scenario |
| Utility | NPV (regulated RoR) |
| Pharma | DCF + decision tree |
| PE | IRR + MOIC |

## §13 IRR 의 reinvestment assumption

| Method | Reinvestment rate |
|--|--|
| IRR | IRR 자체 (비현실) |
| NPV | WACC (현실적) |
| MIRR | Explicit (선택) |

## §14 PE IRR manipulation

| Trick | 영향 |
|--|--|
| Subscription line | IRR clock 늦게 |
| Early dist recycle | IRR 부풀림 |
| Mark-to-fantasy | Unrealized 부풀림 |
| Gross vs Net | Fee 후 큰 차이 |
| Selection bias | Winner only |

**Better metrics**: MOIC + DPI + TVPI + PME.

## §15 자주 빠지는 함정

| 함정 | 정정 |
|--|--|
| IRR 항상 NPV 일치 | 4 case 예외 |
| Payback high cutoff | 임의 + flaw |
| IRR reinvestment | IRR 자체 비현실 |
| Mutual exclusive IRR | Incremental IRR |
| Capital rationing NPV | PI 우월 |
| Multiple IRR panic | NPV 또는 MIRR |

## §16 Best practice — modern

1. NPV primary
2. IRR communication
3. Payback liquidity
4. Sensitivity — critical input
5. Real options — flexibility
6. Decision tree — conditional
7. Monte Carlo — uncertainty

## §17 PI vs NPV 우선

| 조건 | 우선 |
|--|--|
| Unrestricted | NPV |
| Capital rationing (single) | PI |
| Capital rationing (multi) | Integer LP |
| Mutually exclusive | NPV |
| Independent | NPV (모두 채택) |

## §18 Quotes

- *Brealey-Myers*: "NPV is the only criterion consistent with maximizing shareholder wealth."
- *Damodaran*: "NPV is right in theory; IRR is right in practice."
- *Buffett*: "I never look at IRR — I look at *what we paid* and *what we got back*."

## §19 핵심 mindmap

```
Investment Rules
├── NPV (gold standard)
│   ├── 5 우수성
│   └── Discount rate 의 주관 만 약점
├── Payback
│   ├── 3 fatal flaw
│   └── Liquidity / screening 보조
├── IRR
│   ├── Popular, % 직관
│   └── 4 problem case
│       ├── Multiple IRR
│       ├── No IRR
│       ├── Financing reverse
│       └── Mutual exclusive (scale, timing)
├── PI
│   ├── Capital rationing 우월
│   └── Independent 면 NPV
└── MIRR
    ├── IRR 일부 fix
    └── Reinvestment 명시
```

## §20 1-line summary

> **Capital budgeting *gold standard* = *NPV*. *Payback* (3 flaw, screen), *IRR* (4 problem, communication), *PI* (capital rationing 우월), *MIRR* (IRR fix). 실제 회사 = *NPV + IRR + Payback* 의 *3 종 병용*. *Sensitivity + real options* 가 modern 보완.**
