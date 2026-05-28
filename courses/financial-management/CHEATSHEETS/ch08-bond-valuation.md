# Ch 8 Bond Valuation — 치트시트

> Bond pricing / YTM / Duration / Term structure / Yield determinants.

## §1 Bond 핵심 용어

| | 의미 |
|--|--|
| Par (face) | 만기 상환 ($1000 US) |
| Coupon rate | 연간 이자 / par |
| Coupon | 매 기간 이자 |
| Maturity | 만기 기간 |
| YTM | Required return |

## §2 Bond Pricing

$$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}$$

= Annuity + Single (face).

## §3 Premium / Par / Discount

| | Price | YTM vs Coupon |
|--|--|--|
| Premium | > par | YTM < coupon |
| Par | = par | YTM = coupon |
| Discount | < par | YTM > coupon |

→ Pull to par as maturity approaches.

## §4 Interest Rate Risk 2 dimensions

| Dimension | Effect |
|--|--|
| Maturity | Longer → 더 sensitive |
| Coupon | Lower → 더 sensitive |

## §5 Duration

**Macaulay**:
$$D = \sum_t t \times \frac{PV(CF_t)}{P}$$

**Modified**:
$$D_{mod} = \frac{D}{1+y}$$

**Price change**:
$$\frac{\Delta P}{P} \approx -D_{mod} \times \Delta y$$

## §6 Convexity correction

$$\frac{\Delta P}{P} \approx -D_{mod} \Delta y + \frac{1}{2} C (\Delta y)^2$$

→ Large Δy 에서 중요.

## §7 Yield 측정 3 종

| | 의미 |
|--|--|
| YTM | Bond IRR (total) |
| Current Yield | C / P (coupon only) |
| YTC | Yield to call date |

→ Yield to worst = min(YTM, YTC).

## §8 Bond ratings

| Rating | Moody's | S&P |
|--|--|--|
| Highest | Aaa | AAA |
| Investment | Aa-Baa | AA-BBB |
| Speculative | Ba-B | BB-B |
| Distressed | Caa-C | CCC-C |
| Default | D | D |

## §9 Bond types (담보)

| | 담보 |
|--|--|
| Debenture | Unsecured |
| Mortgage bond | Real estate |
| Collateral trust | Securities |
| Equipment trust | Specific |

## §10 Treasury securities

| | 만기 |
|--|--|
| T-bill | < 1년, discount |
| T-note | 2-10년, coupon |
| T-bond | 10-30년, coupon |
| TIPS | 5-30년, inflation-protected |

## §11 Fisher Equation

$$(1+r_n) = (1+r_r)(1+\pi)$$

근사: $r_n \approx r_r + \pi$.

## §12 TIPS mechanism

```
Principal × CPI = Adjusted Principal
Coupon = Adjusted Principal × real coupon
```

→ Real return 보장.

## §13 BEI

$$BEI = Nominal\ Yield - TIPS\ Yield$$

→ 시장 implied inflation.

## §14 Yield Curve 3 shape

| Shape | 의미 |
|--|--|
| Upward (normal) | Future rate up |
| Flat | Uncertainty |
| Inverted | Recession signal |

## §15 Inverted curve history

| 연도 | Inversion | Recession |
|--|--|--|
| 1989 | Yes | 1990 |
| 2000 | Yes | 2001 |
| 2006 | Yes | 2008 |
| 2019 | Yes | 2020 COVID |
| 2022 | Yes | 2024? |

→ 모든 recession 전 ~6-18 month.

## §16 Term structure 3 theories

| Theory | 설명 |
|--|--|
| Expectations | Long = avg future short |
| Liquidity preference | Long premium |
| Market segmentation | Maturity-specific demand |

## §17 Yield determinants (6)

1. Real rate
2. Inflation premium
3. Interest rate risk
4. Default risk (credit spread)
5. Taxability (muni exemption)
6. Liquidity premium

## §18 Credit spread

| Quality | Normal |
|--|--|
| AA | 50-100 bp |
| BBB | 100-200 bp |
| BB (junk) | 300-500 bp |
| B | 500-800 bp |
| CCC | 800+ bp |

→ Crisis widening: 2008 6%+ junk, 2020 COVID temporary.

## §19 Muni equivalent

$$Equiv = \frac{Muni\ Yield}{1 - Tax\ Rate}$$

예: 3% / 0.65 = 4.62% (35% bracket).

## §20 Strategy by environment

| Environment | Strategy |
|--|--|
| Rising rate | Shorter, FRN, cash |
| Falling rate | Long duration |
| Inflation | TIPS |
| Crisis | Treasury, high-quality |
| Spread tight | Junk, EM |

## §21 자주 함정

| 함정 | 정정 |
|--|--|
| YTM = CY | YTM total, CY coupon only |
| Long bond safer | IR risk higher |
| High coupon better | YTM 결정 |
| Inverted = recession | Probability ↑ |
| Duration linear | Convexity 2nd-order |
| Callable same | YTC higher |

## §22 핵심 mindmap

```
Bond Valuation
├── Pricing
│   ├── P = Σ C/(1+y)^t + F/(1+y)^T
│   └── Premium/Par/Discount
├── Yield
│   ├── YTM
│   ├── Current yield
│   └── YTC
├── Risk
│   ├── Maturity effect
│   ├── Coupon effect
│   ├── Duration
│   └── Convexity
├── Term structure
│   ├── Upward/Flat/Inverted
│   └── 3 theories
├── Determinants (6)
└── Special
    ├── TIPS
    ├── Muni
    └── Zero-coupon
```

## §23 1-line summary

> **Bond valuation = PV of CF. YTM = bond IRR. *Price-yield 역관계*, *maturity + coupon effect*. *Duration* 정량화 + *convexity*. *Term structure* — inverted = recession. *6 yield factors*. *TIPS + muni + zero-coupon* special. Active strategy 의 rate environment 별.**
