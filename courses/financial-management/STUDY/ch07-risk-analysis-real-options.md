# Chapter 7: Risk Analysis, Real Options, and Capital Budgeting — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 7** (책 p.207~240).
> 7장은 *Capital budgeting* 의 *risk* + *flexibility* 측면. **Sensitivity / Scenario / Simulation / Decision Tree / Real Options**.

이 장의 *지적 무게중심*:
1. **Sensitivity, Scenario, Simulation** — risk quantification 3 방법
2. **Break-even analysis** — 3 종
3. **Decision Tree** — 조건부 의사 결정
4. **Real Options** — 전통 DCF 의 *static 한계 보완*
5. **Real options 5 종**

---

## §1 Risk Analysis Tools — 3 종

### §1.1 Sensitivity Analysis

> *한 가지 input* 의 *NPV* 영향.

**예**:

| Variable | -10% | Base | +10% |
|--|--|--|--|
| Sales price | $50K | $100K | $150K |
| Sales volume | $80K | $100K | $120K |
| Variable cost | $115K | $100K | $85K |
| Fixed cost | $103K | $100K | $97K |

→ Sales price 가 가장 sensitive.

**Tornado diagram**: NPV impact 의 bar chart, 큰 → 작은 정렬.

### §1.2 Scenario Analysis

> *복수 input* 의 *동시 변화*.

**Best/Base/Worst + probability-weighted**:

| | Prob | NPV | Expected |
|--|--|--|--|
| Best | 25% | $200K | $50K |
| Base | 50% | $100K | $50K |
| Worst | 25% | -$50K | -$12.5K |
| **E[NPV]** | | | **$87.5K** |

### §1.3 Monte Carlo Simulation

> 각 input 의 *probability distribution*, *수천 iteration* 의 NPV.

**Steps**:
1. Each input distribution
2. Correlation 사이 input
3. Random draw — N = 10,000
4. NPV distribution mean, std, percentile

**Output**: Mean, Std, P(NPV<0), VaR, Tornado.

**Python 예**:

```python
import numpy as np

n = 10000
sales = np.random.normal(1000, 100, n)
cost = np.random.normal(500, 50, n)
r = 0.10
T = 5

cf = (sales - cost) * 0.79
npv = -1000 + sum(cf / (1 + r)**t for t in range(1, T+1))

print(f"Mean: {npv.mean():.1f}")
print(f"P(NPV<0): {(npv < 0).mean()*100:.1f}%")
```

### §1.4 비교

| Method | Pros | Cons |
|--|--|--|
| Sensitivity | Simple | Multivariate 무시 |
| Scenario | 결정 친화 | 임의 scenario |
| Monte Carlo | Distributional | Complex |

---

## §2 Break-Even Analysis

### §2.1 *3 종*

**Accounting BE** (NI = 0):
$$Q = \frac{FC + D}{P - VC}$$

**Cash BE** (OCF = 0):
$$Q = \frac{FC}{P - VC}$$

**Financial BE** (NPV = 0) — true economic:
$$Q = \frac{FC + EAC}{P - VC}$$

### §2.2 예 + 비교

- Capex $300K (5 year)
- FC $50K, D $60K
- Price $100, VC $40, r = 10%, T_c = 0

- Accounting: (50+60)/60 = **1833 units**
- Cash: 50/60 = **833 units**
- Financial: EAC of $300K = $79.1K. (50+79.1)/60 = **2152 units**

→ *Financial > Accounting > Cash*.

### §2.3 경영 의미

- *Cash BE* — 즉시 부도 회피
- *Accounting BE* — paper profit
- *Financial BE* — *value creation* threshold

→ *Financial 만이 NPV 의미*.

---

## §3 Decision Tree

### §3.1 동기 — 조건부 의사 결정

> Project stage + node 에서 *information* 의 resolution.

### §3.2 Pharma R&D 예

```
        ┌──── Success (60%) ──── Launch ($100M)
Phase II ┤
        └──── Failure (40%) ──── Abandon ($0)
```

Phase II cost: $20M

$$E[NPV] = 0.6 \times 100 + 0.4 \times 0 - 20 = \$40M$$

→ Phase II go.

### §3.3 복수 stage

```
Phase I ($5M)
  ├─ Success (80%) → Phase II ($20M)
  │                   ├─ Success (60%) → Launch ($100M)
  │                   └─ Failure (40%) → Abandon
  └─ Failure (20%) → Abandon
```

Phase II expected = $40M.

$$E[NPV] = 0.8 \times 40 + 0.2 \times 0 - 5 = \$27M$$

### §3.4 *Decision Tree 의 power*

- Conditional decision
- Optimal stopping — unsuccessful 의 early abandon
- Information value

### §3.5 Information Value

> Perfect 정보 의 가치?

**예**:
- No info: E[NPV] = $40M
- Perfect info: $48M
- *Value of info* = $8M

→ *Market research, prototype* 의 *WTP* 한계.

---

## §4 Real Options — 전통 DCF 한계

### §4.1 전통 DCF 의 *static 가정*

- 한 번 결정, unchanging
- 수정 불가
- Information arrival 무시

### §4.2 현실 — 경영자의 flexibility

- Expand / Abandon / Delay / Switch / Stage

### §4.3 가치

$$NPV_{real\ option} = NPV_{static} + Option\ Value$$

→ Static NPV 가 negative 라도 option value 때문에 positive 가능.

---

## §5 Real Options — 5 종

### §5.1 Option to Expand

> *Initial small* + *성공 시 scale up*.

**예** — Disney Shanghai (2016):
- 초기 $5.5B park
- 성공 시 Phase 2, 3 expand
- *Static DCF* 만 보면 NPV ~0 → option value 가 Go decision

**Black-Scholes 적용**:
- S = PV of expansion CF
- K = expansion cost
- T = decision horizon
- σ = uncertainty
- r = risk-free

### §5.2 Option to Abandon

> Failure 시 abandon.

**예** — Oil exploration:
- Initial drill $10M
- Discovery → production
- Dry hole → abandon

**Salvage value** = abandon option 의 strike.

### §5.3 Option to Delay (Wait)

> 지금 결정 vs 1년 후.

**예** — Land development:
- 지금 capex → NPV $-5M
- 1년 후 + info → 50% NPV $20M / 50% NPV $-5M
- Delay option: 0.5 × $20M = $10M (1 year discount → $9M)

→ Delay 가 더 valuable.

**조건**:
- Information arrival in delay
- Holding cost 작음
- Irreversibility 큼

### §5.4 Option to Switch

> Output, input, technology 변경.

**예 — Flexible manufacturing**:
- Auto plant — sedan + SUV
- 시장 변화 시 production mix 조정
- → Single-product 보다 option value 높음

**Input switch**:
- Refinery — crude grade flexible
- Power plant — gas/coal/oil switching

### §5.5 Option to Stage

> Modular invest — go/no-go at each stage.

**예** — Pharma:
- Phase I → II → III → Commercialize
- 각 stage go/no-go
- Failure 의 일찍 cut

---

## §6 Real Options Valuation Methods

### §6.1 Binomial tree

**Cox-Ross-Rubinstein**:
- Up (u) / down (d)
- Recursive valuation
- Backward induction

### §6.2 Black-Scholes

$$C = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)$$

- $d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma \sqrt{T}}$
- $d_2 = d_1 - \sigma \sqrt{T}$

### §6.3 Monte Carlo

> American-style, path-dependent.

### §6.4 비교

| Method | Pros | Cons |
|--|--|--|
| Binomial | Intuitive, American | Step 계산 |
| Black-Scholes | Closed-form, fast | European only |
| Monte Carlo | Flexible, path-dep | Computational cost |

---

## §7 Real options 의 industry usage

### §7.1 Oil & Gas — *the canonical*

- Exploration: drill option
- Development: stage option
- Production: switching
- Abandonment: decommissioning

### §7.2 Pharma

- R&D stage: 각 phase go/no-go
- Patent: temporal monopoly

### §7.3 Mining

- Open pit start: delay (price waiting)
- Production switching: copper arb

### §7.4 Real estate

- Land development: delay
- Phase development: stage

### §7.5 Tech

- R&D platform: expand
- Acqui-hire: scale option

---

## §8 Real options 의 한계

### §8.1 Underlying asset 의 non-traded

- Project value 의 market price 없음
- → Volatility estimation 어려움
- Proxy — comparable, historical, simulation

### §8.2 Exercise discretion constraint

- 노동 계약, 환경 규제, internal politics
- Theoretical > practical

### §8.3 Path dependency

- Real = operating CF path + terminal
- Monte Carlo 필요

### §8.4 Behavioral

- 경영진 commitment
- Sunk cost fallacy
- Systematic 어려움

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | DCF 만 | Real options flexibility |
| 2 | Sensitivity 만 | Scenario + simulation |
| 3 | Worst > base 무시 | Asymmetric upside |
| 4 | Decision tree probability subjective | Sensitivity of prob |
| 5 | Option value false precision | Range robust |
| 6 | Black-Scholes European limit | American = binomial/MC |
| 7 | Real options over-application | Identifiable + exercisable |
| 8 | Volatility = historical | Forward-looking |

---

## §10 자가점검

1. *Sensitivity / Scenario / Simulation* 차이?
2. *3 종 break-even* 공식?
3. *Decision tree information value*?
4. *Real options 5 종*?
5. *Black-Scholes 5 input* — real option 대응?
6. *Real options 3 한계*?

<details><summary>해답</summary>

1. Sensitivity = one input, Scenario = multi, Simulation = distribution + 수천 iteration.
2. Accounting: (FC+D)/(P-VC), Cash: FC/(P-VC), Financial: (FC+EAC)/(P-VC).
3. E[NPV with info] − E[NPV without]. WTP for test/research.
4. Expand, Abandon, Delay, Switch, Stage.
5. S = PV CF, K = invest cost, T = horizon, σ = uncertainty, r = risk-free.
6. Non-traded asset, Exercise constraint, Path dependency.

</details>

---

## §11 다음 학습으로

- **Ch 8** — Bond valuation
- **Ch 22** — Options advanced
- **Ch 23** — Real options extensions

---

## §12 한 줄 요약

> **Capital budgeting risk + flexibility. *Sensitivity / Scenario / Simulation* 의 3 method. *Break-even* 3 종 — financial 만 NPV 의미. *Decision tree* 의 conditional decision + information value. *Real options* 5 종 (expand/abandon/delay/switch/stage). *Industry-specific* — Oil&Gas, Pharma, Mining, Real estate, Tech.**
