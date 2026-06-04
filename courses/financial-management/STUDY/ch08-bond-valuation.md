# Chapter 8: Interest Rates and Bond Valuation — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 8** (책 p.241~283).
> 8장은 *Fixed income securities* 의 *valuation*. **Bond price** 과 **interest rate** 의 *역관계*, **yield curve**, **duration**, **inflation**.

이 장의 *지적 무게중심*:
1. **Bond features** — coupon, par, maturity
2. **Bond valuation** — PV of cash flow
3. **Yield to Maturity (YTM)** — *bond 의 IRR*
4. **Interest rate risk** — duration, convexity
5. **Term structure** — yield curve
6. **Inflation, default, taxability** — yield 결정 요인

---

## §0 도입 — *채권 = 정해진 현금흐름*

> **핵심 한 문장**: 채권은 4장 PV 기계의 *가장 깨끗한 응용* — 현금흐름(coupon + face value)이 *계약으로 고정*돼 있어, 가치는 오직 **할인율(yield)** 하나로 움직인다.

주식과 달리 채권의 CF 는 미리 정해져 있다. 그래서 8장은 *PV 식의 변주* 다:
- **Price ↔ Yield 는 역관계** (§2) — 한쪽을 알면 다른 쪽이 나온다. yield 가 오르면 price 하락.
- **YTM** = 그 채권을 만기까지 들고 갈 때의 *IRR* (§3).
- **위험 측정** — 같은 yield 변화에도 *만기 길수록·coupon 낮을수록* 가격이 더 출렁인다 (duration, §2).
- **Yield 의 분해** (§7~8) — 시장 yield = 실질금리 + 인플레 프리미엄 + 만기위험 + 부도위험 + 세금 + 유동성.

figure 들이 이 골격을 따라간다: 8.1(채권 CF) → 8.2(만기와 금리위험) → 8.3·8.4(실제 시세) → 8.5·8.6(인플레·금리 역사) → 8.7·8.8(term structure / yield curve).

---

## §1 Bonds and Bond Valuation

### §1.1 Bond 의 *기본 특징*

| 용어 | 의미 |
|--|--|
| Par value (face value) | 만기 상환 금액 (US: $1,000) |
| Coupon rate | 연간 이자 / par value |
| Coupon payment | 매 기간 (semi-annual common) 의 이자 |
| Maturity | 만기 기간 |
| Yield to Maturity (YTM) | Bond 의 *required return* |

**예** — 10-year, 6% coupon, $1000 par, semi-annual:
- Coupon: $1000 × 6%/2 = $30/6mo
- 20 periods
- Par at maturity: $1000

### §1.2 Bond Pricing

$$Price = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}$$

= *annuity (coupons)* + *single payment (face)*.

### §1.3 예

10-year, 6% coupon semi-annual, $1000 par. YTM = 8%.

- C = $30, F = $1000, T = 20, y = 4% (semi-annual)

$$Price = 30 \times 13.5903 + 1000 \times 0.4564 = \$864.10$$

→ *Discount bond* (price < par because YTM > coupon).

![Figure 8.1 — Cash Flows for Xanth Co. Bond. 교재 p.236](/courses/financial-management/figures/ch08/fig-8-1.png)

> **직관**: 채권의 현금흐름은 *계약으로 고정*. Xanth 채권 = 매년 coupon $80 (10년) + 만기에 face value $1,000. 가치 평가는 이 *정해진 화살표들* 을 yield 로 discount 한 PV 일 뿐 — 4장 timeline 의 가장 깨끗한 사례. 불확실한 건 *할인율* 뿐.

### §1.4 *Premium vs Par vs Discount*

| Condition | Price vs Par |
|--|--|
| YTM > coupon | Discount (< par) |
| YTM = coupon | Par |
| YTM < coupon | Premium (> par) |

**직관**: YTM > coupon → 시장이 *더 높은 return* 요구 → price 낮춰 equalize.

---

## §2 Interest Rate Risk

### §2.1 Price-Yield 역관계

10-year, 6% coupon:
- YTM 8% → $864
- YTM 6% → $1000 (par)
- YTM 4% → $1166 (premium)

### §2.2 *2 dimensions*

**1. Maturity effect**: Longer → more sensitivity.
**2. Coupon effect**: Lower → more sensitivity.

### §2.3 Maturity 예

6% coupon, YTM 8% → 4%:

| | 10-year | 30-year |
|--|--|--|
| YTM 8% | $864 | $774 |
| YTM 4% | $1166 | $1346 |
| Change | +35% | +74% |

![Figure 8.2 — Interest Rate Risk and Time to Maturity. 교재 p.240](/courses/financial-management/figures/ch08/fig-8-2.png)

> **직관**: 같은 금리 변화에도 *만기가 길수록 가격이 더 출렁인다*. 30년 채권(파란 곡선)은 금리 5%→20% 에 $1,768.62→$502.11 로 급락하지만, 1년 채권(갈색)은 $1,047.62→$916.67 로 거의 평평. 둘 다 10% 에서 par($1,000) 교차. 먼 미래 CF 일수록 할인의 *복리 효과* 가 커서 — 이것이 duration 의 직관.

### §2.4 Coupon 예

10-year, YTM 8% → 4%:

| Coupon | YTM 8% | YTM 4% | Change |
|--|--|--|--|
| 0% (zero) | $456 | $676 | +48% |
| 6% | $864 | $1166 | +35% |
| 12% | $1272 | $1655 | +30% |

### §2.5 Duration — sensitivity 정량

**Macaulay**:
$$D = \sum_{t=1}^{T} t \times \frac{PV(CF_t)}{Price}$$

**Modified**:
$$D_{mod} = \frac{D}{1 + y}$$

**Price change**:
$$\frac{\Delta P}{P} \approx -D_{mod} \times \Delta y$$

**예** — Duration 7.5, Δy = +1%:
$$\Delta P / P \approx -7.5\% \times 1\% = -7.5\%$$

### §2.6 Convexity — 2nd-order

$$\frac{\Delta P}{P} \approx -D_{mod} \times \Delta y + \frac{1}{2} \times Convexity \times (\Delta y)^2$$

→ Bond price-yield curve 의 *convex shape*. Duration 만 = large change underestimate.

---

## §3 YTM 와 yield 측정

### §3.1 YTM

> Bond IRR — *PV of CF = current price* 의 yield.

위 $864 bond → trial and error → YTM = 8%.

### §3.2 Current Yield

$$CY = \frac{Annual\ Coupon}{Price}$$

위 예: $60 / $864 = 6.94% (capital gain/loss 무시).

### §3.3 Yield to Call (YTC)

> Callable bond 의 — call date 까지 yield.

*Yield to worst* = min(YTM, YTC) — bondholder 보수적.

### §3.4 Spot/forward rate

$$(1 + spot_T)^T = (1 + spot_1)(1 + fwd_{1,2})...(1 + fwd_{T-1,T})$$

---

## §4 Bond Features 상세

### §4.1 Bond Indenture

> Legal agreement issuer ↔ bondholder.

- Terms, covenants, trustee

### §4.2 Security (담보)

| Type | 의미 |
|--|--|
| Debenture | Unsecured |
| Mortgage bond | Real estate collateral |
| Collateral trust | Securities collateral |
| Equipment trust | Specific equipment |

### §4.3 Seniority

Senior > Subordinate > Junior.

### §4.4 Covenants

- Negative — 제한 (D/E ≤ 2)
- Positive — 의무 (재무제표)

### §4.5 Bond ratings

| Rating | Moody's | S&P |
|--|--|--|
| Investment | Aaa | AAA |
| | Aa | AA |
| | A | A |
| | Baa | BBB |
| Junk | Ba | BB |
| | B | B |
| | Caa | CCC |
| | C | C |
| Default | D | D |

→ Top 4 = investment grade.

---

## §5 Bond Markets

### §5.1 Primary vs Secondary

Primary = issuance. Secondary = trading.

### §5.2 Clean vs Dirty

- Clean = 인용가
- Dirty = Clean + accrued interest

$$Dirty = Clean + Accrued$$

### §5.3 Quote convention

- US Treasury: 32 분의 1
- Corporate: percentage

![Figure 8.3 — Sample TRACE Bond Quotations. 교재 p.251](/courses/financial-management/figures/ch08/fig-8-3.png)

> **직관**: 실제 회사채 시세(FINRA TRACE). 각 행 = Coupon·Maturity·신용등급(Moody's/S&P)·High/Low/Last 가격·Change·**Yield%**. 가격은 par 100 기준 percentage 로 호가 — 예: Last 100.08 = par 의 100.08%. 가격과 yield 가 *한 줄에 같이* 표시되는 게 §2 의 역관계가 시장에서 실현된 모습.

### §5.4 Treasury types

| | 만기 | 특징 |
|--|--|--|
| T-bill | < 1년 | Discount, no coupon |
| T-note | 2-10년 | Semi-annual coupon |
| T-bond | 10-30년 | Semi-annual coupon |
| TIPS | 5-30년 | Inflation-protected |

![Figure 8.4 — Sample Wall Street Journal U.S. Treasury Bond Prices. 교재 p.252](/courses/financial-management/figures/ch08/fig-8-4.png)

> **직관**: 미국 국채 시세표 — Maturity·Coupon·**Bid/Asked**(매수/매도 호가)·Chg·Asked Yield. Treasury 는 전통적으로 *32분의 1* 단위로 호가(예: Asked 100:08 = 100 + 8/32). 만기·coupon 별로 빼곡한 이 표가 §7 yield curve 의 *원자료* — 각 만기의 yield 를 모으면 곡선이 된다.

---

## §6 Inflation 과 Interest Rate

### §6.1 Fisher Effect

$$(1 + r_n) = (1 + r_r) \times (1 + \pi)$$

근사: $r_n \approx r_r + \pi$.

![Figure 8.5 — Annualized One-Month Treasury Bill Returns and Inflation. 교재 p.257](/courses/financial-management/figures/ch08/fig-8-5.png)

> **직관**: Fisher 효과의 *실증*. 명목 단기금리(파란 T-bill)와 인플레이션(주황)이 1950~2016 내내 *함께 움직인다* — 명목금리가 인플레를 따라가며 실질금리를 대체로 보존한다는 Fisher 식 $r_n \approx r_r + \pi$ 의 그림. 1970~80년대 고인플레 구간에서 둘이 같이 치솟는 게 특히 뚜렷.

### §6.2 TIPS

> Principal 이 *CPI 에 따라 조정*.

**예**:
- $1000 TIPS, 2% real coupon
- CPI 3%
- Adjusted principal: $1030
- Coupon: $1030 × 2% = $20.60

→ Real rate 보존, 인플레 위험 회피.

### §6.3 Breakeven Inflation Rate

$$BEI = Treasury\ Yield - TIPS\ Yield$$

**Example (2024)**:
- 10-year Treasury: 4.5%
- 10-year TIPS: 2.1%
- BEI: 2.4%

→ 시장의 implied inflation.

---

## §7 Term Structure of Interest Rates

### §7.1 Yield Curve

> Maturity vs Yield plot.

![Figure 8.8 — The Treasury Yield Curve: February 2018. 교재 p.261](/courses/financial-management/figures/ch08/fig-8-8.png)

> **직관**: yield curve = *만기(x)별 yield(y)* 를 점으로 잇는 곡선. 2018년 2월 곡선은 *우상향(normal)* — 1MO 약 1.4% 에서 30YR 약 3.0% 로. 위쪽 nominal, 아래쪽 real(TIPS) 곡선의 간격이 곧 *기대 인플레*. §5.4 의 국채 시세표를 만기순으로 줄 세운 결과.

### §7.2 Shape — 3 종

| Shape | 의미 |
|--|--|
| Upward (normal) | Long > Short — 미래 rate 상승 expectation |
| Flat | 모든 maturity 비슷 — uncertainty |
| Inverted | Short > Long — recession indicator |

![Figure 8.7 — The Term Structure of Interest Rates. 교재 p.260](/courses/financial-management/figures/ch08/fig-8-7.png)

> **직관**: 명목 금리를 *세 겹* 으로 분해. **Real rate**(바닥) + **Inflation premium**(가운데) + **Interest rate risk premium**(위, 만기 길수록 커짐) = Nominal interest rate. **A. 우상향**은 만기위험 프리미엄이 쌓여 곡선이 오르는 정상 형태, **B. 우하향(inverted)**은 *인플레 premium 이 만기 갈수록 줄어들* 때 — 미래 금리 하락(=경기 둔화) 기대를 반영.

### §7.3 Inverted = recession signal

**미국 역사**:
- 모든 recession 전 ~6-18 month inversion
- 2019 → 2020 COVID
- 2022-2023 → 2024-?

**Mechanism**:
- Fed short rate 인상 (inflation 통제)
- Long rate — future low rate expectation
- → Curve invert

### §7.4 *3 theories*

**1. Expectations**: Long rate = expected future short rate average.

**2. Liquidity preference**: 투자자 short 선호 → long 에 liquidity premium → upward bias.

**3. Market segmentation**: Maturity 별 demand/supply (pension long, bank short).

---

## §8 Determinants of Bond Yields

### §8.1 *6 factors*

1. Real rate
2. Inflation premium
3. Interest rate risk premium
4. Default risk premium
5. Taxability premium
6. Liquidity premium

![Figure 8.6 — U.S. Interest Rates: 1800–2016. 교재 p.258](/courses/financial-management/figures/ch08/fig-8-6.png)

> **직관**: 이 6 요인의 *합* 이 시대마다 어떻게 움직였나 — 200년치 미국 장기(주황)·단기(파랑) 금리. 1800~1960 은 대체로 2~6% 박스권, 1980년 전후 고인플레로 *14% 이상* 까지 치솟았다가 이후 장기 하락. 금리는 고정 상수가 아니라 *인플레·정책·위험* 이 만드는 시계열임을 보여 준다.

### §8.2 *Yield 분해 예*

**10-year IBM bond**:
- Real: 1.5% / Inflation: 2.5% / IR risk: 0.5%
- Default (AA): 0.5% / Liquidity: 0.1%
- **Total: 5.1%**

**10-year Treasury**:
- Real + Inflation + IR risk = 4.5%
- Default + Liquidity = 0% (risk-free)
- **Total: 4.5%**

→ *Credit spread* = 0.6%.

### §8.3 Credit spread

> Corporate yield − Treasury = default premium.

**Crisis widening**:
- 2008: spread 6%+ (junk)
- 2020 COVID: temporary

**Normal**:
- AA: 50-100 bp
- BBB: 100-200 bp
- Junk: 300-800 bp

---

## §9 Municipal Bonds

### §9.1 Tax advantage

> Interest *tax-exempt* (federal, often state).

**Equivalent taxable**:
$$Equiv = \frac{Muni\ Yield}{1 - Tax\ Rate}$$

**예** — Muni 3%, fed tax 35%:
$$Equiv = 3\% / 0.65 = 4.62\%$$

### §9.2 Use case

- 고소득자 (high marginal tax)
- Pension/401k — 이미 tax-deferred, no benefit

---

## §10 Zero-Coupon Bonds

### §10.1 Structure

- No coupon
- Discount price (예: $300 for $1000)
- Return = capital appreciation

$$P = \frac{F}{(1+y)^T}$$

### §10.2 Duration = maturity

→ Highest interest rate sensitivity.

### §10.3 Tax issue

> *Imputed interest* — annual accrual 과세 (US).

Pension, IRA → tax-deferred 시 idea.

### §10.4 Use case

- Strip Treasury
- College savings
- Speculative leverage on IR

---

## §11 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | YTM = current yield | YTM total return, CY = coupon only |
| 2 | Price = par 항상 | YTM ≠ coupon 이면 ≠ par |
| 3 | Duration linear | Convexity 의 2nd-order |
| 4 | Long bond safer | IR risk 가 higher |
| 5 | High coupon better | YTM 결정 |
| 6 | Junk bond = loss | Risk-adjusted return |
| 7 | Inflation = nominal | Fisher 의 분해 |
| 8 | Inverted curve = recession | Probability ↑, not certainty |
| 9 | Muni 항상 우월 | Marginal tax + AMT |
| 10 | Callable = same risk | YTC — higher risk |

---

## §12 자가점검

1. *Bond pricing* 공식?
2. *YTM* vs *CY* vs *YTC*?
3. *Maturity + coupon effect*?
4. *Duration* 공식 + *price change*?
5. *Fisher equation*?
6. *Yield curve* 3 shape?
7. *Yield 6 factors*?
8. *Muni equivalent taxable*?

<details><summary>해답</summary>

1. Price = Σ C/(1+y)^t + F/(1+y)^T.
2. YTM = total, CY = coupon/price, YTC = to call.
3. Longer + lower coupon → higher sensitivity.
4. D = Σ t × PV(CF)/Price. D_mod = D/(1+y). ΔP/P ≈ −D_mod × Δy.
5. (1+r_n) = (1+r_r)(1+π).
6. Upward = up expectation, Flat = uncertainty, Inverted = recession.
7. Real, inflation, IR risk, default, taxability, liquidity.
8. Equiv = Muni / (1 − tax).

</details>

---

## §13 다음 학습으로

- **Ch 9** — Stock valuation
- **Ch 13** — WACC
- **Ch 22-25** — Options, derivatives

---

## §14 한 줄 요약

> **Bond valuation = *PV of CF*. *YTM* = bond IRR. *Price-yield 역관계*, *maturity + coupon effect*. *Duration* 정량화. *Term structure* 3 shape — inverted = recession signal. *6 factors* (real, inflation, IR risk, default, taxability, liquidity). *TIPS + muni + zero-coupon* 의 special structure.**
