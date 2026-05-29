# Ch 18 Levered Firm Valuation — 치트시트

> APV / FTE / WACC / Beta levering / LBO.

## §1 세 방법 비교

| 방법 | Cash flow | Discount rate |
|--|--|--|
| APV | UCF + tax shield 별도 | R_0 + R_D |
| FTE | LCF (equity) | R_E |
| WACC | UCF | After-tax WACC |

→ Target D/V constant 하 *동일*.

## §2 APV 식

$$APV = V_U + \sum \text{financing effects}$$

$$= V_U + PV(TS) - Flotation - PV(Distress) + Subsidy$$

## §3 PV of Tax Shield

| Debt 형태 | PV(TS) |
|--|--|
| 영구 (perpetual) | $T_c \times D$ |
| 변동 (schedule) | $\sum \frac{T_c R_D D_t}{(1+R_D)^t}$ |

## §4 FTE

$$NPV = -(Cost - Debt) + \sum \frac{LCF_t}{(1+R_E)^t}$$

$$LCF = (EBIT - R_D D)(1-T_c) + D\&A - Capex - \Delta NWC$$

= UCF − interest×(1−T_c).

## §5 WACC method

$$NPV = -Cost + \sum \frac{UCF_t}{(1+WACC)^t}$$

$$WACC = \frac{E}{V}R_E + \frac{D}{V}R_D(1-T_c)$$

→ UCF 사용, tax shield 이미 WACC 에 반영.

## §6 UCF vs LCF

| | 정의 |
|--|--|
| UCF | EBIT(1−T_c) + D&A − Capex − ΔNWC |
| LCF | UCF − interest(1−T_c) |

## §7 R_E (MM Prop II with tax)

$$R_E = R_0 + (R_0 - R_D)(1-T_c)\frac{D}{E}$$

## §8 Hamada (Beta levering)

$$\beta_L = \beta_U[1 + (1-T_c)\frac{D}{E}]$$

$$\beta_U = \frac{\beta_L}{1 + (1-T_c)\frac{D}{E}}$$

## §9 Pure-play 절차

1. Peers 식별
2. β_L 관측
3. Unlever → β_U
4. 평균 β_U
5. Target D/E 로 re-lever
6. CAPM → R_E

## §10 방법 선택

| 상황 | 방법 |
|--|--|
| Target D/V ratio 일정 | WACC / FTE |
| Debt level 고정/변동 | APV |
| LBO (debt paydown) | APV |
| Going-concern 단순 | WACC |
| Different project risk | APV / pure-play |

## §11 LBO APV

$$APV_{LBO} = V_U + \sum \frac{T_c R_D D_t}{(1+R_D)^t} + \frac{TV}{(1+R_0)^T}$$

→ Debt 매년 감소 → tax shield 매년 다름.

## §12 LBO value creation 3 source

1. Leverage / Tax shield
2. Operational improvement (margin, efficiency)
3. Multiple expansion (entry vs exit EV/EBITDA)

## §13 LBO mechanics

- Sources & Uses
- Debt waterfall (senior → mezz → equity)
- Cash sweep (excess FCF → 상환)
- IRR / MOIC (exit, target 20-25%)

## §14 유명 LBO

| Deal | 연도 | 규모 |
|--|--|--|
| RJR Nabisco | 1989 | $25B |
| TXU | 2007 | $45B (2014 파산) |
| Hilton | 2007 | $26B (큰 수익) |
| Dell | 2013 | $24B |
| Twitter | 2022 | $44B |

## §15 Flotation / Subsidy

| Effect | APV 부호 |
|--|--|
| Flotation cost | − |
| Subsidized loan | + (market rate 대비 절감 PV) |

## §16 WACC 순환 문제

- WACC 에 E, D market value 필요
- V 가 valuation 결과
- → iteration 또는 target ratio 가정

## §17 자주 함정

| 함정 | 정정 |
|--|--|
| 세 방법 답 다름 | 일관 가정 하 동일 |
| WACC 에 tax shield 또 더함 | 이미 반영, 이중 금지 |
| FTE debt 미차감 | 초기투자 = equity분만 |
| APV 에 LCF 사용 | APV/WACC = UCF |
| LBO 에 WACC | Debt 변동 → APV |
| β unlever 없이 사용 | Leverage 제각각 → unlever 필수 |
| Flotation/subsidy 무시 | APV 항목 |

## §18 실무 선호

| 주체 | 방법 |
|--|--|
| Investment banking | WACC (target structure) |
| Private equity / LBO | APV (debt schedule) |
| Corporate project | WACC (same risk) / APV (diff) |
| Real estate | APV (고정 mortgage) |

## §19 핵심 mindmap

```
Levered Firm Valuation
├── APV (V_U + financing effects)
│   ├── Tax shield (+)
│   ├── Flotation (−)
│   ├── Distress (−)
│   └── Subsidy (+)
├── FTE (LCF at R_E)
│   └── 초기투자 = equity분
├── WACC (UCF at WACC)
│   └── tax shield 이미 반영
├── Beta levering (Hamada)
│   └── Pure-play 절차
└── LBO
    ├── APV (debt paydown)
    └── 3 value source
```

## §20 1-line summary

> **3 valuation 방법 — *APV* ($V_U$ + tax shield $T_c D$ 별도), *FTE* (LCF at R_E, equity분만), *WACC* (UCF at after-tax WACC, shield 내장). *Target D/V constant* 하 동일. *Debt level 변동* (LBO) = APV, *ratio 일정* = WACC/FTE. *Hamada* β unlever/re-lever, *pure-play*. LBO value = tax shield + operational + multiple expansion.**
