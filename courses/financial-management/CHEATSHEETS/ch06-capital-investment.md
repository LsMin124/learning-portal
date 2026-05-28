# Ch 6 Making Capital Investment Decisions — 치트시트

> Incremental CF / Depreciation / MACRS / EAC / Sensitivity.

## §1 Stand-alone principle

> Project NPV = *incremental CF* (with project − without).

## §2 4 가지 함정

| | 처리 |
|--|--|
| Sunk cost | 무시 |
| Opportunity cost | 포함 |
| Side effects (synergy/erosion) | 포함 |
| Allocated overhead | Incremental 만 |

## §3 Cash Flow 의 4 components

| | 공식 |
|--|--|
| Initial | $-Capex - \Delta NWC + Salvage_{old} - Tax_{salvage}$ |
| OCF | $(Sales-Cost)(1-T_c) + D \times T_c$ |
| Terminal | $Salvage - Tax_{salvage} + \Delta NWC_{recovery}$ |

## §4 OCF 의 3 공식 (모두 동일)

| | 공식 |
|--|--|
| Bottom-up | NI + Depreciation |
| Top-down | Sales - Cost - Tax |
| Tax shield | (Sales-Cost)(1-T_c) + D × T_c |

## §5 Depreciation Tax Shield

$$Tax\ shield = D \times T_c$$

→ *Cash 효과* 는 *tax saving* 만.

## §6 MACRS 5-year %

| Year | % |
|--|--|
| 1 | 20.00 |
| 2 | 32.00 |
| 3 | 19.20 |
| 4 | 11.52 |
| 5 | 11.52 |
| 6 | 5.76 |

→ Half-year convention.

## §7 MACRS class

| Class | 자산 |
|--|--|
| 3-year | Research equipment |
| 5-year | Computer, auto |
| 7-year | Industrial equipment |
| 10-year | Manufacturing |
| 15-year | Land improvement |
| 27.5-year | Residential rental |
| 39-year | Commercial real estate |

## §8 Bonus depreciation phase-out

| Year | % |
|--|--|
| 2017-2022 | 100% |
| 2023 | 80% |
| 2024 | 60% |
| 2025 | 40% |
| 2026 | 20% |
| 2027+ | 0% |

## §9 Salvage value tax

```
Sale price − Book Value = Gain (or Loss)
Tax = Gain × T_c
After-tax salvage = Sale price − Tax
```

→ Loss 면 tax saving (after-tax > sale).

## §10 NWC

```
ΔNWC = ΔA/R + ΔInventory − ΔA/P
```

- Increase → outflow
- Decrease → inflow
- Year 0: outflow, Year T: recovery (inflow)

## §11 EAC 공식

$$EAC = \frac{PV\ of\ cost}{PVIFA(r, T)}$$

→ Unequal life 의 *gold standard*.

## §12 EAC use cases

- Equipment 교체
- Maintenance vs replacement
- Different-life project 비교
- Optimal replacement timing

## §13 Inflation consistency

| | Both? |
|--|--|
| CF nominal + r nominal | ✓ |
| CF real + r real | ✓ |
| CF nominal + r real | ✗ (NPV 과대) |
| CF real + r nominal | ✗ (NPV 과소) |

**Fisher**: $(1+r_n) = (1+r_r)(1+\pi)$

## §14 Break-even 3 종

| Type | 조건 |
|--|--|
| Accounting | NI = 0 |
| Cash | OCF = 0 |
| Financial | NPV = 0 |

## §15 Sensitivity vs Scenario

| | 변수 |
|--|--|
| Sensitivity | One input |
| Scenario | Multiple input simultaneous |
| Monte Carlo | Probability distribution |
| Decision tree | Conditional path |

## §16 Cash conversion cycle

$$CCC = DSO + DIO - DPO$$

| Firm | CCC |
|--|--|
| Amazon | ~-30 day |
| Apple | ~-30 day |
| Walmart | ~+5 day |
| Tesla | ~+20 day |

→ Negative CCC = *supplier-funded growth*.

## §17 흔한 함정

| 함정 | 정정 |
|--|--|
| Sunk cost 포함 | 무시 |
| Opportunity cost 누락 | 포함 |
| Erosion 무시 | 포함 |
| Depreciation = cash | Tax shield 만 |
| Nominal+real 혼합 | Consistency |
| NWC 무시 | Year 0+T 포함 |
| Salvage tax 무시 | (Sale − BV) × T_c |
| Different life 직접 비교 | EAC |

## §18 Famous post-audit lessons

| Project | 결과 |
|--|--|
| Disney Eurodisney 1992 | Cultural error |
| Daimler-Chrysler 1998 | $36B → $7B |
| HP-Compaq 2002 | Synergy → negative |
| AOL-Time Warner 2000 | $99B write-off |
| Boeing 747-8 2011 | 단종 |

## §19 핵심 mindmap

```
Capital Investment
├── Incremental CF
│   ├── Sunk 무시
│   ├── Opportunity 포함
│   ├── Side effects 포함
│   └── Allocated incremental 만
├── Cash flow
│   ├── Initial
│   ├── OCF = (S-C)(1-T_c) + D × T_c
│   └── Terminal
├── Depreciation
│   ├── Tax shield = D × T_c
│   ├── MACRS (accelerated)
│   ├── Bonus (phase-out)
│   └── Straight-line
├── EAC
│   ├── Unequal life
│   └── Optimal replacement
└── Risk
    ├── Sensitivity
    ├── Scenario
    ├── Break-even
    └── Monte Carlo
```

## §20 1-line summary

> **NPV 의 실제 적용. *Incremental CF* (with − without) — *sunk 무시, opportunity + side effects 포함*. *OCF* = (S-C)(1-T_c) + D×T_c. *Depreciation tax shield* + *MACRS* 가 accelerated. *EAC* 가 unequal life. *Sensitivity + scenario + break-even*. *Post-audit* 가 long-term capital allocation 의 best practice.**
