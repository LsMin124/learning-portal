# Chapter 6: Making Capital Investment Decisions — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 6** (책 p.168~206).
> 6장은 *NPV 의 실제 적용*. **Incremental cash flow** 의 *정확한 식별* 이 핵심.

이 장의 *지적 무게중심*:
1. **Incremental cash flow** — *with vs without* project
2. **Sunk cost, opportunity cost, side effects**
3. **Depreciation** — *tax shield*
4. **MACRS** — 미국 의 *accelerated depreciation*
5. **Equivalent Annual Cost (EAC)** — *서로 다른 수명*

---

## §0 도입 — *어떤 현금흐름* 을 세느냐

> **핵심 한 문장**: NPV 의 식은 5장에서 끝났다. 6장은 그 식에 넣을 **올바른 현금흐름을 *세는* 기술** — *정확한 r 보다 정확한 CF 가 먼저*.

5장이 "규칙(NPV)" 이었다면, 6장은 그 규칙에 먹일 **현금흐름의 정의** 다. 핵심 원칙은 단 하나:

> **Incremental cash flow** — 프로젝트를 *하느냐 마느냐* 로 *달라지는* 현금흐름만 센다 (*with* − *without*).

이 한 줄에서 모든 함정이 갈린다:
- **Sunk cost** (이미 쓴 돈) — 무관, 무시
- **Opportunity cost** (다른 용도의 포기 가치) — 반드시 포함
- **Side effects** (erosion·synergy) — 포함
- **Allocated overhead** (배분된 간접비) — 증분이 아니면 제외

그리고 CF 를 셀 때 빠지기 쉬운 두 축이 **세금** (depreciation tax shield·MACRS — §3·§4) 과 **일관성** (명목/실질·NWC 회수·서로 다른 수명의 EAC). figure 6.1 은 그중 *명목 vs 실질* 의 직관을 잡아 준다.

---

## §1 Incremental Cash Flows

### §1.1 *Stand-alone* principle

> Project NPV = *incremental cash flow* 만으로 계산.

**Rule**: *CF with project* − *CF without project* = Incremental CF.

### §1.2 *4 가지 흔한 함정*

**1. Sunk costs**:
- 이미 지출 + 돌려받을 수 없음
- → **무시**
- 예: 시장 조사비, 실패한 R&D

**2. Opportunity costs**:
- Project 가 사용하는 자원 의 *대체 사용 가치*
- → **포함**
- 예: 회사 보유 토지 (시장 가격)

**3. Side effects**:
- *Synergy* (positive) — 새 제품 매장 traffic ↑
- *Erosion/cannibalization* (negative) — iPhone 14 가 iPhone 13 매출 잠식
- → **포함**

**4. Allocated overhead**:
- 기존 overhead share 무시, *추가* overhead 만 포함

---

## §2 *Cash Flow* 의 *4 components*

### §2.1 Initial outlay (Year 0)

$$Initial = -Capex - \Delta NWC + Salvage_{old} - Tax_{salvage}$$

### §2.2 Operating cash flow (Year 1 ~ T)

**3 가지 동일 공식**:

(1) Bottom-up: $OCF = NI + Depreciation$
(2) Top-down: $OCF = Sales - Cost - Tax$
(3) Tax shield: $OCF = (Sales - Cost)(1 - T_c) + Depreciation \times T_c$

→ 마지막이 *depreciation tax shield* 명확히 보임.

### §2.3 Terminal cash flow (Year T)

$$Terminal = Salvage - Tax_{salvage} + \Delta NWC_{recovery}$$

- Tax = (Salvage − Book Value) × T_c

### §2.4 *전체 NPV*

$$NPV = Initial + \sum_{t=1}^{T-1} \frac{OCF_t}{(1+r)^t} + \frac{OCF_T + Terminal}{(1+r)^T}$$

---

## §3 Depreciation 의 *tax shield*

### §3.1 Depreciation = noncash

- 회계상 비용, cash outflow 아님
- 그러나 *taxable income 감소* → tax 감소
- → *cash 효과* = *tax saving*

### §3.2 공식

$$Tax\ shield = Depreciation \times T_c$$

**예** — Depreciation $10,000, T_c = 21%:
$$Tax\ shield = 10000 \times 0.21 = \$2100$$

→ 매년 $2100 cash saving.

### §3.3 Method 별

| Method | Pattern | PV of tax shield |
|--|--|--|
| Straight-line | Equal | 낮음 |
| Double declining | Early heavy | 높음 |
| MACRS | Mixed | 높음 |

→ *Accelerated* 가 *higher PV* — 항상 선호.

---

## §4 MACRS

### §4.1 미국 표준 감가상각

> *1986 Tax Reform Act* 이후 — federal income tax 의 *required*.

### §4.2 *Asset class*

| Class | 자산 |
|--|--|
| 3-year | Research equipment |
| 5-year | Computer, auto |
| 7-year | Industrial equipment |
| 10-year | Manufacturing |
| 15-year | Land improvement |
| 20-year | Long utility |
| 27.5-year | Residential rental |
| 39-year | Commercial real estate |

### §4.3 *5-year MACRS %*

| Year | % |
|--|--|
| 1 | 20.00 |
| 2 | 32.00 |
| 3 | 19.20 |
| 4 | 11.52 |
| 5 | 11.52 |
| 6 | 5.76 |

→ *Half-year convention* — Year 1 의 50% 만, 6 년에 걸침.

### §4.4 *Bonus depreciation*

- *2017 TCJA* — 100% 즉시 expense
- 2023 부터 phase out (80%, 60%, ...)
- 2027 부터 0% (현재 debate)

→ Capital-intensive firm 에 큰 tax saving.

---

## §5 *NWC* 의 cash flow

### §5.1 *Project 의 NWC 영향*

- Increase NWC → cash outflow
- Decrease NWC → cash inflow

### §5.2 *Initial vs Terminal*

- Year 0: Increase NWC (outflow)
- Year T: Recover NWC (inflow)

### §5.3 *왜 important*

- Growth firm: NWC 상당 증가 → cash drag
- Mature firm: 안정
- Amazon (negative NWC) — cash boost

---

## §6 Project Evaluation — 예제

### §6.1 *Setup*

- Capex: $300K (5-year MACRS)
- Sales: $200K/year
- Cost: $80K/year
- T_c = 21%
- NWC: $20K Year 0, recover Year 5
- Salvage Year 5: $30K
- WACC = 12%

### §6.2 Year 별 cash flow

**Year 0**:
- Capex: $-300K
- NWC: $-20K
- **Total: $-320K**

**Year 1**:
- Sales: $200K
- Cost: $-80K
- Depreciation: $300K × 20% = $60K
- EBIT: $60K
- Tax: $12.6K
- NI: $47.4K
- **OCF**: $47.4K + $60K = **$107.4K**

### §6.3 *Book Value of Year 5*

- 5-year MACRS Year 5 BV = $300K × 5.76% = $17,280
- Salvage: $30K
- Tax on gain: ($30K - $17,280) × 21% = $2,671
- *After-tax salvage*: $27,329

### §6.4 Terminal (Year 5)

- OCF Year 5
- + After-tax salvage: $27,329
- + NWC recovery: $20K
- = Year 5 total

---

## §7 Equivalent Annual Cost (EAC)

### §7.1 동기 — 서로 다른 수명

| | Machine A | Machine B |
|--|--|--|
| Cost | $10K | $12K |
| Life | 5 year | 8 year |

→ *NPV* 직접 비교 *부적절*.

### §7.2 EAC 정의

$$EAC = \frac{NPV}{PVIFA(r, T)}$$

### §7.3 예

At r = 10%:

$$EAC_A = \frac{10000}{3.7908} = \$2638$$
$$EAC_B = \frac{12000}{5.3349} = \$2249$$

→ Machine B 가 cheaper/year → **Machine B**.

### §7.4 Use cases

- Equipment 교체
- Maintenance vs replacement
- Different life project 비교

---

## §8 Inflation

### §8.1 Nominal vs Real

> 일관성:
> *Nominal CF* + *nominal r*  OR  *Real CF* + *real r*

![Figure 6.1 — Calculation of Real Rate of Interest. 교재 p.188](/courses/financial-management/figures/ch06/fig-6-1.png)

> **직관**: *명목 vs 실질* 을 햄버거로. 은행에 $1,000(=햄버거 1,000개) 넣고 명목 10% 로 1년 후 $1,100. 그런데 물가가 6% 올라 햄버거가 $1.06 → $1,100 으로 *1,038개* 만 산다. 즉 *구매력* 은 3.8% 만 늘었다 = **실질이자율**. 근사로 $real \approx nominal - inflation$ (10−6=4%), 정확히는 Fisher: $1 + r_{real} = \frac{1.10}{1.06}$ → 3.8%. *명목 CF 는 명목 r 로, 실질 CF 는 실질 r 로* 맞춰 discount 해야 하는 이유.

### §8.2 흔한 실수

- *Real CF* + *Nominal r* → NPV 과대
- → *Both nominal* 일관

### §8.3 Inflation pass-through

- Commodity: 부분
- Brand: 거의 100% (Coca-Cola)
- Regulated: regulator approval

---

## §9 Investments of Unequal Lives

### §9.1 Methods 3

1. **EAC method**
2. **Common life** — LCM of lives, 반복
3. **NPV of perpetual replacement**

### §9.2 Replacement chain 예

Machine A (5) vs B (8) — LCM 40 year, A 반복 8 회, B 반복 5 회.

→ 보통 *EAC* 가 간단.

### §9.3 Optimal replacement

- Equipment operating cost 점차 증가
- *어느 해* 교체? → *EAC 최소* 시점

---

## §10 Sensitivity + Scenario + Break-even

### §10.1 Sensitivity

> *한 가지 input* 의 NPV 영향.

### §10.2 Scenario

| | Sales | Cost | NPV |
|--|--|--|--|
| Best | +20% | -10% | $200K |
| Base | 0 | 0 | $100K |
| Worst | -20% | +10% | $-50K |

### §10.3 Break-even

**Accounting break-even** (NI = 0):
$$Q_{BE} = \frac{FC + D}{P - VC}$$

**Cash break-even** (OCF = 0):
$$Q_{BE} = \frac{FC}{P - VC}$$

**Financial break-even** (NPV = 0) — true economic.

---

## §11 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Sunk cost 포함 | 무시 |
| 2 | Opportunity cost 누락 | 포함 |
| 3 | Erosion 무시 | 포함 |
| 4 | Allocated overhead 포함 | Incremental 만 |
| 5 | Depreciation = cash | Tax shield 만 |
| 6 | Nominal CF + Real r | Consistency |
| 7 | NWC 무시 | Initial outflow + terminal recovery |
| 8 | Salvage tax 무시 | (Salvage − BV) × T_c |
| 9 | Different life 직접 비교 | EAC |
| 10 | Short horizon | Full life cycle |

---

## §12 Real-world 예

### §12.1 Tesla Gigafactory (2014~)

- Incremental CF — Nevada/Shanghai/Berlin
- Side effects — Solar synergy, brand
- Erosion — Roadster → S/X
- Bonus depreciation

### §12.2 Pharma R&D

- Sunk — Phase I, II 이미 spent
- Opportunity — Capital + scientist alternative
- Side effects — off-label, related product

### §12.3 Real estate development

- Capex — 토지 + 건축
- NWC — minimal
- Depreciation — 39-year MACRS (commercial)
- Salvage — terminal value

---

## §13 자가점검

1. *Incremental cash flow* 의 *stand-alone* 원리?
2. *Sunk, opportunity, side effects*?
3. *OCF* 의 *3 가지 동일 공식*?
4. *Depreciation tax shield* 공식?
5. *MACRS half-year convention*?
6. *EAC* 공식 + use case?
7. *Inflation consistency rule*?
8. *Sensitivity vs Scenario vs Break-even*?

<details><summary>해답</summary>

1. *With* − *without* = Incremental.
2. Sunk 무시, Opportunity 포함, Side effects 포함.
3. NI+D, S−C−T, (S−C)(1−T_c) + D×T_c.
4. Depreciation × T_c.
5. Year 1, T 의 50%, 6 년에 걸침.
6. NPV/PVIFA(r,T). Unequal life 비교.
7. Both nominal 또는 both real.
8. Sensitivity = single, Scenario = multi, Break-even = NPV/NI/OCF = 0.

</details>

---

## §14 다음 학습으로

- **Ch 7** — Risk analysis + real options
- **Ch 13** — WACC
- **Ch 22** — Real options advanced

---

## §15 한 줄 요약

> **NPV 의 실제 적용. *Incremental CF* 의 *with vs without*. *Sunk 무시, opportunity 포함, side effects 포함, allocated overhead 만 incremental*. *Depreciation tax shield* 가 cash 효과. *MACRS + bonus* 가 accelerated. *EAC* 가 unequal life 비교. *Sensitivity + scenario + break-even* 의 risk 보완.**
