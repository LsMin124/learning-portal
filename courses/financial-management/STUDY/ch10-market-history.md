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

## §0 도입 — *이론 이전의 경험적 기록*

> **핵심 한 문장**: 11~13장이 "위험과 수익은 *어떻게 연결돼야 하는가*"를 이론으로 묻기 전에, 10장은 "*실제로 무슨 일이 있었나*"를 100년 데이터로 답한다 — 모든 위험 모형(CAPM·APT·WACC)의 *경험적 닻*.

재무이론은 미래의 위험·수익을 가정에서 연역하지만, 그 가정이 터무니없지 않다는 보증은 *역사* 뿐이다. 10장의 메시지는 세 겹이다:

1. **수익은 둘로 쪼개진다** — *income(배당·이자) + capital gain(가격변동)*. figure 10.1·10.2 가 이 분해를 달러·퍼센트로 보여준다.
2. **더 높은 수익엔 더 높은 위험이 붙는다** — 1926년 이후 미국 실측:

| 자산 | 평균수익 | 표준편차 | $1 → 2024 |
|--|--|--|--|
| Small stocks | 16.1% | 31.4% | $40,000+ |
| Large stocks | 12.1% | 19.5% | $13,000+ |
| LT gov bonds | 6.0% | 9.8% | $200 |
| T-bills | 3.4% | 3.0% | $25 |
| Inflation | 3.0% | 4.0% | $18 |

   주식 risk premium ≈ **8%**, 그러나 변동성도 ~6배. figure 10.4(부의 지수)·10.5~10.8(연도별 수익)이 이 trade-off 의 그림.
3. **수익은 *근사적으로* 정규분포지만 꼬리가 두껍다** — figure 10.9(히스토그램)·10.10(종형곡선)이 ±1σ=68% 규칙을, figure 10.12(2008)가 그 규칙이 깨지는 순간을 보여준다.

여기에 *arithmetic vs geometric mean*(변동성 drag, §4)과 *EMH*(가격은 정보를 즉시 반영, §6)가 더해져, 10장은 "*과거는 미래의 보장이 아니라 baseline*"이라는 겸손을 가르친다.

---

## §1 Returns

### §1.1 *Total return* 의 *2 source*

1. Income (dividend, interest)
2. Capital appreciation

$$Total\ Return = \frac{P_1 - P_0 + D_1}{P_0} = \frac{D_1}{P_0} + \frac{P_1-P_0}{P_0}$$

![Figure 10.1 — Dollar Returns. 교재 p.300](/courses/financial-management/figures/ch10/fig-10-1.png)

> **직관**: 총수익을 *달러* 로 분해한 타임라인. $3,700 을 넣으면(아래 outflow) 1년 뒤 배당 $185 + 기말가치 $4,033 = **$4,218** 이 돌아온다(위 inflow). 곧 *수익 = income(배당) + capital gain(가격변동)* — 우측 괄호가 그 두 조각을 묶는다.

![Figure 10.2 — Percentage Returns. 교재 p.301](/courses/financial-management/figures/ch10/fig-10-2.png)

> **직관**: 같은 분해를 *주당·퍼센트* 로. 주가 $37 → 배당 $1.85(5%) + 기말 $40.33 → 총 $42.18. 달러 *크기* 를 지워야 자산 간 비교가 되므로, 이 퍼센트가 §2 역사적 수익률의 단위가 된다.

### §1.2 Holding period return

$$HPR = (1+R_1)(1+R_2)...(1+R_T) - 1$$

![Figure 10.3 — Cash Flow: An Investment Example. 교재 p.302](/courses/financial-management/figures/ch10/fig-10-3.png)

> **직관**: 단일기간 수익의 골격 — $25 투자 → 배당 $2 + 기말주가 $35 = $37 회수, $R = (2+10)/25 = 48\%$. HPR 은 바로 이런 단일기간 $(1+R)$ 을 여러 해 *곱한* 것: 복리는 더하기가 아니라 곱하기다.

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

![Figure 10.5 — Year-by-Year Total Returns on Large-Company Common Stocks. 교재 p.305](/courses/financial-management/figures/ch10/fig-10-5.png)

> **직관**: 위 표의 *평균 12.1%* 뒤에 숨은 raw data. 막대가 0 위(파랑)·아래(빨강)로 춤춘다 — +54%(1933)에서 −43%(1931)·−37%(2008)까지. *평균은 어느 해에도 실현되지 않는다*; 변동성이 본질이다.

![Figure 10.6 — Year-by-Year Total Returns on Small-Company Stocks. 교재 p.305](/courses/financial-management/figures/ch10/fig-10-6.png)

> **직관**: 소형주는 같은 그림의 *증폭판*. y축이 −100~+200% (대형주는 −60~+60). +143%(1933) 같은 폭등과 더 깊은 골 — 높은 평균수익(16.1%)의 대가가 이 진폭(σ 31.4%)이다.

![Figure 10.7 — Year-by-Year Total Returns on Long-term Government Bonds and U.S. Treasury Bills. 교재 p.306](/courses/financial-management/figures/ch10/fig-10-7.png)

> **직관**: 위 패널(장기국채)은 주식보다 *좁게* 출렁이고, 아래(T-bill)는 거의 0 위에만 머문다 — *거의 무위험*. 단 1970~80년대 인플레기에 T-bill 이 15%까지 치솟은 것은 "명목 ≠ 실질"(§2.3)을 예고한다.

### §2.2 Risk Premium

$$Risk\ Premium = Asset\ Return - R_f$$

- Large stock ERP: 12.1% - 3.4% = **8.7%**

→ *Historical ERP ≈ 8-9%*.

![Figure 10.11 — Stock Market Risk Premiums for 17 Countries, 1900–2010. 교재 p.319](/courses/financial-management/figures/ch10/fig-10-11.png)

> **직관**: 미국의 8% ERP 가 우연 아닌가? 17개국 1900~2010 평균은 6.9%이고 *모두 양(+)* — 어디서나 주식이 안전자산을 이겼다. 미국(7.2%)은 중간일 뿐. survivorship bias 를 감안해도 *주식 위험 프리미엄은 보편적* 현상이다.

### §2.3 Real Returns (after inflation)

| Asset | Nominal | Real |
|--|--|--|
| Stocks | 12.1% | ~9% |
| Bonds | 6.0% | ~3% |
| T-bills | 3.4% | ~0.4% |

→ T-bill real ≈ 0 — *purchasing power 만 보존*.

![Figure 10.8 — Year-by-Year Inflation. 교재 p.307](/courses/financial-management/figures/ch10/fig-10-8.png)

> **직관**: 인플레이션 자체도 출렁인다 — 1940년대·1970~80년대 급등(18%), 1930년대엔 *디플레*(−10%). 명목수익에서 이 막대를 빼야 *실질* 수익이 남는다. T-bill 의 명목 3.4% 가 인플레 3.0% 와 거의 같아 *실질수익 ≈ 0* 인 것이 이 그림의 결론.

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

![Figure 10.4 — Wealth Indexes of Investments in the U.S. Capital Markets (Year-End 1925 = $1.00). 교재 p.304](/courses/financial-management/figures/ch10/fig-10-4.png)

> **직관**: 10장에서 가장 유명한 그림. 1925년 $1 을 넣었다면 2017년 small stock $36,931 vs T-bill $20.78 — 약 *1,800배* 차이다. *로그 스케일* 이라 완만해 보이지만 한 칸이 10배임에 주의. 주식의 장기 우위 + 복리의 위력과, 동시에 1930년대·2008년의 깊은 골(위험)을 한 장에 담았다.

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

![Figure 10.10 — The Normal Distribution. 교재 p.314](/courses/financial-management/figures/ch10/fig-10-10.png)

> **직관**: 정규분포의 ±1/2/3σ 규칙을 주식수익(μ=12.1%, σ=19.8%)에 입힌 그림. 해의 *68%* 는 −7.7%~+31.9% 안에 든다. 단 하나의 모수 σ 로 위험 전체를 요약한다는 이 *단순화* 가 §3 표준편차와 11장 이후 모든 위험 모형의 출발 가정이다.

![Figure 10.9 — Histogram of Returns on Large-Company Stocks: 1926–2017. 교재 p.310](/courses/financial-management/figures/ch10/fig-10-9.png)

> **직관**: 각 연도를 수익 구간(10%폭)에 벽돌처럼 쌓은 *경험적 분포*. 0~20% 근처가 가장 높고 양극단으로 갈수록 낮아져 위 종형(정규)에 *근사* 한다. 다만 −40%대(1931·2008)와 +50%대(1933·1954)에 막대가 남아 있는 것이 §5.4 의 *fat tail* — 정규가 "거의 불가능"이라던 사건이 실제로 일어났다.

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

![Figure 10.12 — S&P 500 Monthly Returns, 2008. 교재 p.321](/courses/financial-management/figures/ch10/fig-10-12.png)

> **직관**: 정규분포가 깨지는 순간을 클로즈업. 2008년 *월별* 수익에서 10월 −16.8% 는 정규 가정상 수만 년에 한 번꼴 사건이다. 이런 *fat tail* 이 현실에선 10년마다 찾아온다 — Gaussian VaR 의 과소추정과 스트레스 테스트가 필요한 이유(§5.4).

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
