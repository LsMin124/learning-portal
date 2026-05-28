# Ch 7 Risk Analysis, Real Options, Capital Budgeting — 퀴즈

> 10 문항 (개념 2 / 계산 4 / 디버그 3 / 면접 1).

### Q1. *Sensitivity / Scenario / Simulation* 차이?

각의 characteristic + use case?

<details><summary>답</summary>

| Method | 변수 | 분석 |
|--|--|--|
| Sensitivity | One input at a time | Tornado diagram |
| Scenario | Multi input simultaneous | Best/Base/Worst |
| Simulation (Monte Carlo) | Distribution + correlation | NPV distribution |

**Use cases**:
- Sensitivity: critical variable 식별
- Scenario: 경영진 결정 boundary
- Simulation: probability of loss, VaR

**Pros/Cons**:
| | Pros | Cons |
|--|--|--|
| Sensitivity | Simple | Multivariate 무시 |
| Scenario | 결정 친화 | 임의 scenario |
| Simulation | Distributional | Complex, assumption |

→ All 3 함께 → risk dashboard.

</details>

### Q2. *Real Options 5 종* — 예?

<details><summary>답</summary>

| Option | 예 |
|--|--|
| Expand | Disney Shanghai Phase 1 → 2, 3 |
| Abandon | Oil exploration — dry hole |
| Delay | Land development — wait market |
| Switch | Flex auto plant — sedan ↔ SUV |
| Stage | Pharma Phase I → II → III |

**추가 예**:
- Expand: AWS, Netflix DVD→Streaming, Tesla supercharger
- Abandon: GE lighting, IBM PC sale, failed movies
- Delay: Mining at low commodity, real estate recession
- Switch: Refinery crude grade, power plant fuel
- Stage: VC Series A→B→C, real estate phase

**핵심 insight**:
- Static DCF negative — option value 가 Go decision 만들 수 있음
- True business value

</details>

### Q3. 계산 — *3 종 Break-Even*

- Capex $500K (10 year, salvage $0)
- FC $80K/year, D $50K/year
- Price $50, VC $20, T_c = 0%, r = 10%

각 BE?

<details><summary>답</summary>

**Accounting BE**:
$$Q = \frac{80 + 50}{30} = \mathbf{4333\ units}$$

**Cash BE**:
$$Q = \frac{80}{30} = \mathbf{2667\ units}$$

**Financial BE**:
- EAC of $500K = $500K / 6.1446 = $81.36K
$$Q = \frac{80 + 81.36}{30} = \mathbf{5379\ units}$$

→ Financial > Accounting > Cash.

**경영 의미**:
- *Cash BE 2667*: 즉시 부도 회피
- *Accounting BE 4333*: paper profit
- *Financial BE 5379*: value creation

→ *Financial 만이 NPV 의미*.

</details>

### Q4. 계산 — *Decision Tree*

```
Phase II ($30M)
  ├─ Success (50%) → $200M
  └─ Failure (50%) → $0
```

(a) Phase II E[NPV]?
(b) Phase I cost $10M, 70% success → Phase II go: E[NPV]?
(c) Information value of Phase I?

<details><summary>답</summary>

**(a) Phase II**:
$$E[NPV] = 0.5 \times 200 - 30 = \$70M$$

**(b) Phase I + II**:
- Phase I success (70%) → Phase II ($70M)
- Phase I failure (30%) → abandon

$$E[NPV] = 0.7 \times 70 - 10 = \$39M$$

**(c) Information value**:

*Conditional update* — Phase I 통과 시 Phase II success rate 80% (예):
- E[Phase II | Phase I pass] = 0.8 × 200 - 30 = $130M
- Total = 0.7 × 130 - 10 = $81M

→ Without Phase I (직접 Phase II): $70M
→ With Phase I (information value): $81M
→ *Phase I value* = $11M

→ Phase I 가 *Phase II success rate* 의 *prediction 으로 value*.

</details>

### Q5. 디버그 — *Pharma static DCF*

- Phase III $500M
- 30% approval → $5B
- 70% failure → $0
- r = 15%

(a) Static NPV?
(b) Real option value (interim abandon)?

<details><summary>답</summary>

**(a) Static naive**:
- E[NPV] = -$500M + 0.3 × $5000M = $1000M
- *naive* — risk-adjusted discount 부족

**(b) Real option — staged**:

Phase III split:
- $200M initial
- Interim 50% positive → spend $300M more
- Interim 50% negative → abandon

```
Phase III ($200M)
  ├─ Interim positive (50%) → continue ($300M)
  │                            ├─ Final success (60%) → $5B
  │                            └─ Final failure (40%) → $0
  └─ Interim negative (50%) → abandon
```

**Expected NPV**:
- Positive proceed: $5B × 0.5 × 0.6 - $300M × 0.5 = $1350M
- Saved (abandon): +$150M
- Minus $200M initial
- = $1300M

→ Higher than naive — *abandon option* value.

**Pharma reality**:
- Adaptive trial — interim 결정 보편화
- Bayesian update
- FDA Breakthrough designation
- Real option valuation standard

**Famous cases**:
- Pfizer Lipitor (1996) — Phase III interim positive surprise
- Merck Vioxx (2004) — Phase IV abandon (CV risk)
- mRNA COVID (2020) — Operation Warp Speed parallel staging

</details>

### Q6. 디버그 — *Real option over-application*

Tech CEO: *"NPV negative $50M, but real option (expansion + acquihire + pivot) = $200M, true NPV $150M."*

Critique?

<details><summary>답</summary>

**함정**:

**1. Over-application** — 모든 가능성 의 hand-wave
**2. Identifiable + exercisable 기준 부족**
**3. Pivot ≠ option** (strategy change, not contingent claim)
**4. Acquihire = acquirer option**, 우리 의 권한 없음
**5. Volatility false precision** — startup σ proxy 없음
**6. Double-counting** of mutually exclusive

**Real-world cases**:
- WeWork (2019) — "Tech firm" branding 의 fake. IPO 취소.
- Theranos (2014-2018) — expansion fiction
- SoftBank Vision Fund — wild claims

**Sober *real option valuation***:

1. Single, specific, exercisable 만
2. Underlying asset market proxy
3. Probability robustness
4. Static + option value 명시
5. Skeptical review

**Damodaran**:
> *"Real options useful — specific, exercisable, measurable. 아니면 over-engineering."*

</details>

### Q7. 디버그 — *Monte Carlo* 함정

Analyst — 10,000 iteration:
- Mean NPV $50M, Std $30M, P(NPV<0) 5%
- 결론: *95% probability of value creation*.

Critique?

<details><summary>답</summary>

**5 함정**:

**1. Distribution assumption** — normal 의 fat tail 무시
**2. Correlation among input** — independent draw 가정
**3. Input parameter uncertainty** — mean/std 자체 estimate
**4. Garbage in, garbage out** — historical forward-looking limit
**5. False precision** — statistical vs practical significance

**Famous failures**:
- **LTCM (1998)** — VaR Monte Carlo, Gaussian, correlation breakdown, $4.6B loss
- **2008 Subprime** — housing regional independence 가정, $trillions loss
- **VW emission (2015)** — model risk

**Best practice**:
1. Multiple distributions
2. Stress test — extreme
3. Correlation — copula
4. Bayesian update — learning
5. Decision-relevant range
6. Robustness

**Tools**:
- Crystal Ball (Oracle), @Risk (Palisade)
- Python: NumPy, SciPy, PyMC

→ Monte Carlo useful but careful. *Interpretation humility*.

</details>

### Q8. 디버그 — *Sensitivity vs Scenario* 혼동

Analyst: *"Sales -10% NPV $50K, Cost +10% NPV $30K. Worst NPV ≈ sum gap = $-20K."*

Critique?

<details><summary>답</summary>

**함정** — Sensitivity 의 naive 합산.

**왜**:
1. 각 sensitivity = single change
2. Multi-input simultaneous = scenario
3. Non-linearity interaction
4. Correlation 무시

**Correct — scenario**:

| | Sales | Cost | NPV |
|--|--|--|--|
| Base | $1000K | $500K | $100K |
| Both adverse | $900K | $550K | $? |

**Calculation**:
- Base: (1000-500)(0.79) × 5 - 1000 = $975K
- Sales -10%: $580K
- Cost +10%: $777.5K
- Both: (900-550)(0.79) × 5 - 1000 = $382.5K

Sum of gaps: $395K + $197.5K = $592.5K
Both: $975K - $382.5K = $592.5K → 동일 (linear 예)

→ *Linear simple*: addition OK. *Non-linear* (tax bracket, step cost): 부정확.

**Lesson**:
- Sensitivity = individual factor
- Scenario = joint behavior
- Simulation = correlation + distribution

</details>

### Q9. 디버그 — *Probability subjectivity*

Pharma — Phase II success rate: *60%* (analyst), *80%* (CEO), *40%* (skeptic).

NPV range?

<details><summary>답</summary>

**Probability sensitivity**:

Phase II $30M, success → $200M.

| Prob | E[NPV] |
|--|--|
| 40% (skeptic) | $50M |
| 60% (analyst) | $90M |
| 80% (CEO) | $130M |

→ Range $50M-$130M (160% range).

**해결**:

1. **Probability range explicit reporting** — Best/Base/Worst
2. **Bayesian update** — Phase I data
3. **Industry data**:

**Pharma success rate** (BIO 2014):
- Phase I → approval: 9.6%
- Phase II → approval: 15.3%
- Phase III → approval: 49.6%
- Oncology Phase II: 5.1%
- Hematology Phase II: 26.1%

**Best practice**:
1. External benchmark — historical industry
2. Molecule-specific adjustment
3. Sensitivity range
4. Multiple analysts triangulation
5. Expert panel

**Behavioral biases**:
- Optimism (CEO 80% — empire building)
- Anchoring (60% prior report)
- Risk aversion (skeptic 40% — cover behind)
- Information asymmetry (private info)

**Decision under uncertainty**:
- Min-max regret
- Bayesian decision
- Real option staged

</details>

### Q10. 면접 — *Modern framework*?

"Traditional NPV 외 의 modern tools?"

<details><summary>답</summary>

**Multi-layered framework**:

**Layer 1 — Static DCF**: NPV, IRR, payback

**Layer 2 — Risk Analysis** (Ch 7):
- Sensitivity, Scenario, Simulation
- Break-even (3 types)

**Layer 3 — Real Options** (Ch 7):
- 5 종, Binomial/Black-Scholes/MC valuation
- Static + option value

**Layer 4 — Decision Tree** (Ch 7):
- Conditional path
- Information value
- Optimal stopping

**Layer 5 — Behavioral / Strategic**:
- Pre-mortem
- Devil's advocate
- Reference class forecasting (Kahneman)
- Outside view
- Robust decision-making (RAND)

**Layer 6 — AI / ML**:
- Reinforcement learning
- Neural net forecasting
- Bayesian net
- Causal inference (Pearl)

**Industry adoption**:

| Industry | Primary |
|--|--|
| Oil/Gas | Real options + MC |
| Pharma | Decision tree + adaptive |
| Mining | Real options + commodity scenario |
| Real estate | DCF + delay option |
| Tech | VC method + option |
| Bank | VaR + stress test |

**Kahneman-Tversky lessons**:
1. Loss aversion
2. Reference dependence
3. Probability weighting

**Modern best practice integrated**:
1. NPV (base)
2. Sensitivity + scenario + simulation
3. Real options
4. Decision tree
5. Pre-mortem
6. Outside view
7. Robustness
8. Post-audit (learning)

**Buffett**:
> *"Be approximately right rather than precisely wrong."*

**Munger**:
> *"All I want to know is where I'm going to die, so I'll never go there."* — worst case avoidance.

→ Modern finance = modeling sophistication + behavioral wisdom combination.

</details>
