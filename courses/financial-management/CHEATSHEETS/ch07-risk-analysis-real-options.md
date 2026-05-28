# Ch 7 Risk Analysis, Real Options — 치트시트

> Sensitivity / Scenario / Simulation / Break-even / Decision Tree / Real Options.

## §1 Risk Analysis 3 Methods

| | 변수 | 분석 |
|--|--|--|
| Sensitivity | One input | Tornado |
| Scenario | Multi simultaneous | Best/Base/Worst |
| Simulation (MC) | Distribution + corr | NPV distribution |

## §2 Sensitivity Tornado

```
Sales price ████████████  (가장 sensitive)
Volume     ██████
Var cost   █████
Fixed cost ██
```

## §3 Scenario Probability-Weighted

| | Prob | NPV | E[NPV] |
|--|--|--|--|
| Best | 25% | $200K | $50K |
| Base | 50% | $100K | $50K |
| Worst | 25% | -$50K | -$12.5K |
| **Total** | | | **$87.5K** |

## §4 Monte Carlo Output

| Metric | 의미 |
|--|--|
| Mean | 기대값 |
| Std | 변동성 |
| P(NPV<0) | Probability of loss |
| VaR | 95% worst |
| Tornado | Input sensitivity |

## §5 Break-Even 3 종

| Type | 조건 | 공식 |
|--|--|--|
| Accounting | NI = 0 | (FC+D)/(P-VC) |
| Cash | OCF = 0 | FC/(P-VC) |
| Financial | NPV = 0 | (FC+EAC)/(P-VC) |

→ *Financial > Accounting > Cash*.

## §6 Break-Even 의미

| BE | 의미 |
|--|--|
| Cash | 부도 회피 minimum |
| Accounting | Paper profit |
| Financial | True value creation |

## §7 Decision Tree 의 4 step

1. Node — decision or chance
2. Branch — outcome or alternative
3. Backward induction — terminal → start
4. Expected value at each node

## §8 Information Value

$$IV = E[NPV\ with\ info] - E[NPV\ without\ info]$$

→ Market research, prototype, pilot 의 WTP.

## §9 Real Options 5 종

| Option | 예 | Trigger |
|--|--|--|
| Expand | Disney Shanghai | Success |
| Abandon | Oil dry hole | Failure |
| Delay | Real estate wait | Info arrival |
| Switch | Flex auto plant | Market change |
| Stage | Pharma R&D | Sequential learning |

## §10 Black-Scholes input mapping

| Financial | Real Option |
|--|--|
| Stock price S | PV of project CF |
| Strike K | Investment cost |
| Time T | Decision horizon |
| Volatility σ | CF uncertainty |
| Risk-free r | Risk-free rate |
| Dividend yield | Cost of delay |

## §11 Real Options Valuation

| Method | Pros | Cons |
|--|--|--|
| Binomial | Intuitive, American | Step 계산 |
| Black-Scholes | Closed-form | European only |
| Monte Carlo | Flexible, path-dep | Computation |

## §12 Industry usage

| Industry | Primary |
|--|--|
| Oil/Gas | Real options + MC |
| Pharma | Decision tree |
| Mining | Real options + commodity |
| Real estate | DCF + delay option |
| Tech | VC + option |
| Bank | VaR + stress |

## §13 Real options 한계

| 한계 | 정정 |
|--|--|
| Non-traded asset | Proxy volatility |
| Exercise constraint | Political/regulatory |
| Path dependency | Monte Carlo |
| Behavioral | Sunk cost, commitment |

## §14 NPV = Static + Option

$$NPV_{total} = NPV_{static\ DCF} + Option\ Value$$

→ Static negative + option positive = total positive 가능.

## §15 자주 함정

| 함정 | 정정 |
|--|--|
| DCF 만 | Real options |
| Sensitivity 만 | Multi-factor |
| Real options over-app | Identifiable + exercisable |
| Black-Scholes for American | Binomial |
| Volatility historical | Forward-looking |
| Probability subjective | Industry benchmark |
| Monte Carlo precision | Distribution assumption |

## §16 Pharma success rate (BIO 2014)

| Phase | → Approval |
|--|--|
| I | 9.6% |
| II | 15.3% |
| III | 49.6% |
| Oncology II | 5.1% |
| Hematology II | 26.1% |

## §17 Famous failures

| Project | 실수 | 영향 |
|--|--|--|
| LTCM 1998 | Gaussian, correlation | $4.6B loss |
| 2008 subprime | Regional independence | $trillions |
| Concorde | Sunk cost | 50yr unprofitable |
| WeWork 2019 | Real option over-claim | IPO 취소 |

## §18 Behavioral biases

| Bias | 영향 |
|--|--|
| Optimism | NPV inflation |
| Anchoring | Initial estimate |
| Loss aversion | Conservative |
| Sunk cost | Continue losing |
| Commitment escalation | Ego defense |
| Confirmation | Selective evidence |

## §19 Modern best practice (multi-layered)

1. NPV (base)
2. Sensitivity + scenario + simulation
3. Real options
4. Decision tree
5. Pre-mortem
6. Outside view (Kahneman)
7. Robustness check
8. Post-audit (learning)

## §20 핵심 mindmap

```
Risk Analysis + Real Options
├── Risk methods
│   ├── Sensitivity (one)
│   ├── Scenario (multi)
│   └── Monte Carlo
├── Break-even
│   ├── Accounting (NI=0)
│   ├── Cash (OCF=0)
│   └── Financial (NPV=0)
├── Decision tree
│   ├── Conditional
│   ├── Optimal stopping
│   └── Information value
└── Real Options
    ├── 5 종 (Expand/Abandon/Delay/Switch/Stage)
    ├── BS / Binomial / MC valuation
    └── Limitations
```

## §21 1-line summary

> **Capital budgeting risk + flexibility. *Sensitivity / Scenario / Simulation* 의 3 method. *Break-even* 3 종 — Financial 만 NPV 의미. *Decision tree* conditional + information value. *Real options* 5 종. *Industry-specific*. *Behavioral + post-audit* = modern integrated framework.**
