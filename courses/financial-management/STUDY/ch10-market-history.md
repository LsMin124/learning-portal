# Chapter 10: Lessons from Market History — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 10** (책 p.321~352).
> 10장은 *risk and return* 의 *empirical foundation*. *Historical return*, *risk premium*, *normal distribution*, *EMH*.

이 장의 *지적 무게중심*:
1. **Historical returns** — US 1926-present
2. **Risk premium** — equity over bond
3. **Variance, std deviation**
4. **Arithmetic vs Geometric mean**
5. **Normal distribution**
6. **Efficient Market Hypothesis**

---

## §1 Returns

### §1.1 *Total return* 의 *2 source*

1. Income (dividend, interest)
2. Capital appreciation

$$Total\ Return = \frac{P_1 - P_0 + D_1}{P_0} = \frac{D_1}{P_0} + \frac{P_1-P_0}{P_0}$$

### §1.2 Holding period return

$$HPR = (1+R_1)(1+R_2)...(1+R_T) - 1$$

### §1.3 예

3 year: +20%, -10%, +15%
$$HPR = 1.20 \times 0.90 \times 1.15 - 1 = 24.2\%$$

Annualized = $1.242^{1/3} - 1 = 7.49%$.

---

## §2 Historical Returns (US 1926-2024)

### §2.1 *Average Annual*

| Asset | Return | Std Dev |
|--|--|--|
| Large stocks | 12.1% | 19.5% |
| Small stocks | 16.1% | 31.4% |
| LT corp bonds | 6.4% | 8.5% |
| LT gov bonds | 6.0% | 9.8% |
| T-bills | 3.4% | 3.0% |
| Inflation | 3.0% | 4.0% |

### §2.2 Risk Premium

$$Risk\ Premium = Asset\ Return - R_f$$

- Large stock ERP: 12.1% - 3.4% = **8.7%**

→ *Historical ERP ≈ 8-9%*.

### §2.3 Real Returns (after inflation)

| Asset | Nominal | Real |
|--|--|--|
| Stocks | 12.1% | ~9% |
| Bonds | 6.0% | ~3% |
| T-bills | 3.4% | ~0.4% |

→ T-bill real ≈ 0 — *purchasing power 만 보존*.

### §2.4 $1 → 2024

| Asset | 2024 Value |
|--|--|
| Small stocks | $40,000+ |
| Large stocks | $13,000+ |
| Corp bonds | $250 |
| Gov bonds | $200 |
| T-bills | $25 |
| CPI | $18 |

→ Stock long-term superiority + compounding power.

---

## §3 Variance and Standard Deviation

### §3.1 Definition

$$\sigma^2 = \frac{1}{N-1} \sum (R_i - \bar{R})^2, \quad \sigma = \sqrt{\sigma^2}$$

→ Risk measure (dispersion).

### §3.2 Risk-return relation

| Asset | Return | Std Dev |
|--|--|--|
| Small stocks | 16.1% | 31.4% |
| Large stocks | 12.1% | 19.5% |
| Long bonds | 6.0% | 9.8% |
| T-bills | 3.4% | 3.0% |

→ Higher return = Higher risk.

### §3.3 Coefficient of Variation

$$CV = \frac{\sigma}{\bar{R}}$$

| Asset | CV |
|--|--|
| Small stocks | 1.95 |
| Large stocks | 1.61 |
| T-bills | 0.88 |

---

## §4 Arithmetic vs Geometric Mean

### §4.1 Arithmetic

$$\bar{R}_A = \frac{1}{N} \sum R_i$$

→ Single period expected.

### §4.2 Geometric

$$\bar{R}_G = \left[\prod (1+R_i)\right]^{1/N} - 1$$

→ Multi-period compounded.

### §4.3 *왜 차이*

> Volatility 클수록 arithmetic > geometric.

**예** — 2 year: +100%, -50%

- Arithmetic: 25%
- Geometric: 0%

→ $1 → $2 → $1. 진짜 return 0.

### §4.4 Approximation

$$\bar{R}_G \approx \bar{R}_A - \frac{\sigma^2}{2}$$

→ *Volatility drag*.

**예** — S&P 500:
- Arithmetic 12.1%
- σ² = 0.038
- Geometric ≈ 10.2%

### §4.5 어떤 use

- Forward single period: Arithmetic
- Historical long-term, terminal wealth: Geometric
- DCF discount rate: Geometric (보통)

---

## §5 Normal Distribution

### §5.1 Approximate normality

> Stock return 은 *approximately normal*.

| Range | Probability |
|--|--|
| μ ± 1σ | 68% |
| μ ± 2σ | 95% |
| μ ± 3σ | 99.7% |

### §5.2 S&P 500 예 (μ=12%, σ=20%)

| Range | Probability |
|--|--|
| -8% ~ +32% | 68% |
| -28% ~ +52% | 95% |
| -48% ~ +72% | 99.7% |

### §5.3 Reality check

- 2008: -37% (3σ event, close)
- 1933: +54% (2σ event)
- 2020: -34% intra-year (2σ+)

### §5.4 Fat tails

> Extreme events 가 normal 예측보다 *훨씬 자주*.

**Examples**:
- 1987 crash: -22% in 1 day (normal: 10^-22, 실제 every 50 yr)
- 2008: 50%+ peak-to-trough
- 2020: COVID crash
- 2022 bond: -30% long Treasury

**Distributions**:
- Normal: thin tails
- Log-normal: positive skew (prices)
- Student-t, Pareto: fat tails

**Implication**:
- VaR underestimate (Gaussian)
- Stress testing importance
- Risk parity 의 failure modes

---

## §6 Efficient Market Hypothesis

### §6.1 *3 forms*

| Form | Info set | Implication |
|--|--|--|
| Weak | Past prices | Technical 무용 |
| Semi-strong | All public | Fundamental 무용 |
| Strong | All info (insider) | 모든 무용 |

### §6.2 Implications

**Weak**:
- Random walk
- Technical (charts) 무용

**Semi-strong**:
- News 즉시 반영
- Fundamental 무용 (after public)

**Strong**:
- Insider 도 무용
- Generally not believed

### §6.3 Evidence for

- Random walk short-term
- Mutual fund underperformance (avg)
- Quick news incorporation
- Liquid market efficiency

### §6.4 Evidence against

**Anomalies**:
- Value premium (Fama-French)
- Size effect
- Momentum (Jegadeesh-Titman)
- Calendar effect (January)
- Post-earnings drift
- Bubbles + crashes

**Behavioral**:
- Over/under-reaction
- Herding
- Loss aversion
- Anchoring
- Limits to arbitrage

### §6.5 Modern view — *Adaptive Markets Hypothesis*

> EMH 가 *동적*. 시장은 learning, adapting.

- Anomaly 발견 → exploit → fade
- Bubble → crash → learning
- Behavioral bias → systematic patterns

Lo (2004): AMH.

---

## §7 Behavioral Finance

### §7.1 Cognitive biases

| Bias | Description |
|--|--|
| Overconfidence | 본인 정보 over-valuation |
| Anchoring | Initial estimate sticky |
| Loss aversion | 손실 회피 > 이익 추구 |
| Mental accounting | Use-specific accounting |
| Herding | 군중 따라가기 |
| Recency | 최근 사건 over-weight |
| Hindsight | "그럴 줄 알았다" |

### §7.2 Market anomalies

- January effect — small-cap January
- Monday effect
- Holiday effect
- Weather effect

### §7.3 Famous bubbles

| 연도 | Bubble | Peak/Crash |
|--|--|--|
| 1637 | Tulip | 5000% → -99% |
| 1720 | South Sea | 10x → -84% |
| 1929 | US stock | -89% |
| 1989 | Japan | Nikkei -82% |
| 2000 | Dot-com | NASDAQ -78% |
| 2008 | US housing | S&P -57% |
| 2017 | Crypto | BTC -84% |
| 2021 | SPAC meme | -90% |

---

## §8 Portfolio implication

### §8.1 Diversification

- 비상관 assets 의 risk reduction
- 60/40 standard
- Modern multi-asset (alts, EM, factor)

### §8.2 Asset allocation

- Long horizon: equity-heavy (60-90%)
- Short horizon: bond-heavy
- Lifecycle funds (target-date)

### §8.3 Rebalancing

- Drift after time
- Rebalance = systematic buy low sell high
- Threshold (10%) vs time-based (annual)

### §8.4 Cost matters

- Index fund vs active: 0.05% vs 1%+
- 30 year compounding 큰 차이
- Bogle/Vanguard low-cost revolution

---

## §9 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Past = future | Historical baseline only |
| 2 | Arithmetic = compound | Geometric for long-term |
| 3 | Normal = reality | Fat tail real |
| 4 | EMH 강신뢰 | Adaptive, anomalies |
| 5 | Recent past over-weight | Long-term mean reversion |
| 6 | Stock 항상 win | Period-dependent (Japan 1989-2024) |
| 7 | Risk = volatility | Permanent loss 진정 risk |
| 8 | Diversification 충분 | Tail correlation crisis ↑ |

---

## §10 자가점검

1. *Total return* 2 source?
2. *Historical ERP*?
3. *Arithmetic vs Geometric*?
4. *Normal distribution* 3 properties?
5. *EMH* 3 forms?
6. *Bubble* examples?
7. *Behavioral biases*?

<details><summary>해답</summary>

1. Income + Capital appreciation.
2. ~8-9% historical US.
3. Arith = single forward, Geom = multi-period compound (terminal wealth).
4. Symmetric, ±1σ=68%, ±2σ=95%, ±3σ=99.7%.
5. Weak (past), Semi-strong (public), Strong (all).
6. Tulip 1637, South Sea 1720, 1929, Japan 1989, Dot-com 2000, 2008, Crypto 2017/21.
7. Overconfidence, anchoring, loss aversion, herding, recency, hindsight, mental accounting.

</details>

---

## §11 다음 학습으로

- **Ch 11** — CAPM, Beta
- **Ch 12** — APT, Multi-factor
- **Ch 13** — WACC

---

## §12 한 줄 요약

> **Market history = *risk + return* empirical. *Stock long-term outperform* (real ~7%), *ERP ~8%*. *Arithmetic vs geometric* — volatility drag. *Normal approximate, fat tail real*. *EMH 3 forms* — adaptive markets. *Behavioral biases + bubble recurring*. *Diversification + cost + long horizon* portfolio implication.**
