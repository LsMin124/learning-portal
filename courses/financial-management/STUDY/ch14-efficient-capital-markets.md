# Chapter 14: Efficient Capital Markets and Behavioral Challenges — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 14** (책 p.428~466).
> 14장은 EMH deep dive + behavioral challenges. Ch 10 introduction 후 advanced.

이 장의 *지적 무게중심*:
1. **EMH** — 3 forms in depth
2. **Empirical evidence** — for and against
3. **Behavioral finance challenges**
4. **Anomalies**
5. **Implications for corporate finance**

---

## §0 도입 — 시장은 정말 효율적인가

*효율적 시장 가설(EMH)* 의 핵심 주장: 가격은 *이용 가능한 정보를 즉시·완전히* 반영한다. 따라서 새 정보가 나오면 가격은 *계단처럼 한 번에* 점프하고 그 뒤로는 표류하지 않는다.

![Figure 14.1 — Reaction of Stock Price to New Information in Efficient and Inefficient Markets. 교재 p.431](/courses/financial-management/figures/ch14/fig-14-1.png)

> **직관**: 효율적 시장(실선)은 발표일에 *즉시* 새 가치로 점프한다. *느린 반응*(점선)은 정보가 며칠에 걸쳐 스며들고(→ 사후 표류 = 수익 기회), *과잉반응*(파선)은 일단 튀었다가 되돌아온다(버블). 14장은 어느 쪽이 현실인지를 증거로 따진다.

---

## §1 EMH Deeper

### §1.1 3 forms revisited

**Weak**: Past prices no predictive. Random walk. Technical 무용.
**Semi-strong**: All public info reflected. Fundamental 무용 (after public).
**Strong**: Insider info also. Generally rejected.

![Figure 14.3 — Relationship among Three Different Information Sets. 교재 p.435](/courses/financial-management/figures/ch14/fig-14-3.png)

> **직관**: 세 정보집합은 *포함관계*다 — 과거가격 ⊂ 공개정보 ⊂ 모든정보. 그래서 strong 이 성립하면 semi-strong·weak 도 자동 성립한다. 효율성의 "강도"는 어느 집합까지 가격에 반영되느냐의 문제.

### §1.2 Random Walk

$$P_t = P_{t-1} + \epsilon_t$$

→ Best forecast = today's price.

![Figure 14.2 — Investor Behavior Tends to Eliminate Cyclical Patterns. 교재 p.434](/courses/financial-management/figures/ch14/fig-14-2.png)

> **직관**: 만약 주가에 *주기적 패턴*이 있다면, 투자자가 *저점 매수·고점 매도* 로 즉시 차익을 노려 그 패턴을 *스스로 소멸*시킨다. 남는 것은 예측 불가능한 random walk — weak form 효율성의 메커니즘.

![Figure 14.4 — Simulated and Actual Stock Price Movements. 교재 p.439](/courses/financial-management/figures/ch14/fig-14-4.png)

> **직관**: 위(A)는 *난수로 생성한* 가짜 시계열, 아래(B)는 The Gap 의 *실제* 주가다. 사람들은 둘 다에서 "패턴"을 보지만, 통계적으로 둘은 구분되지 않는다 — 패턴 인식은 대개 *착시*.

### §1.3 Statistical tests

- Autocorrelation ≈ 0 (weak)
- Run tests
- Variance ratio
- Filter rules — no profit after cost

---

## §2 Evidence for EMH

### §2.1 Event Studies

Method: Track abnormal return around event.
- Earnings, dividend, merger, split announcement

Findings:
- Quick adjustment (semi-strong)
- Limited drift after event
- Average abnormal converges to 0 days

![Figure 14.5 — Cumulative Abnormal Returns for Companies Announcing Dividend Omissions. 교재 p.440](/courses/financial-management/figures/ch14/fig-14-5.png)

> **직관**: 배당 *중단* 발표일(0일) *직전·당일* 에 누적초과수익(CAR)이 −5%까지 급락하고, 그 *이후엔 거의 평탄* 하다 — 나쁜 소식이 즉시 가격에 반영되고 표류가 없다는 semi-strong 효율성의 전형적 증거.

![Figure 14.15 — Stock Performance Prior to Forced Departures of Management. 교재 p.458](/courses/financial-management/figures/ch14/fig-14-15.png)

> **직관**: 강제 해임된 경영진의 회사는 발표 *수개월 전부터* 누적 예측오차가 −40~−50%로 미끄러진다 — 시장이 부진을 먼저 반영하고, 이사회의 해임은 *뒤늦은* 대응임을 보여준다.

### §2.2 Mutual Fund Performance

- Active avg underperforms after fees
- Survivorship-adjusted: more underperformance
- Carhart (1997): persistent winners rare
- SPIVA: 80%+ underperform 10-year

![Figure 14.6 — Percentage of Managed Equity Funds Beating the Vanguard 500 Index Fund, One-Year Returns. 교재 p.442](/courses/financial-management/figures/ch14/fig-14-6.png)

> **직관**: 단일 연도에 인덱스를 이기는 액티브 펀드 비율이 대부분 *50% 미만* 이다 — 매년 절반 이상이 패시브에 진다. 누적하면(여러 해 연속 승리) 극소수만 살아남아, 강형 효율성에 가까운 그림.

### §2.3 Quick news reaction

- News fully reflected seconds (HFT)

### §2.4 Random walk

- Daily returns ~0 autocorrelation
- Long-horizon slight mean reversion

---

## §3 Evidence Against EMH

### §3.1 Size effect (Banz 1981)

- Small-cap outperforms after β
- 3-5% extra annual
- Weakened post-1980s

![Figure 14.10 — Annual Stock Returns on Portfolios Sorted by Size (Market Capitalization), 1926–2013. 교재 p.449](/courses/financial-management/figures/ch14/fig-14-10.png)

> **직관**: 소형(Small) 13.4% → 대형(Large) 9.3% 로 *크기가 작을수록 수익률이 높다*. CAPM 이 설명 못 하는 초과수익 — 대표적 이상현상(단, 1980년대 이후 약화).

### §3.2 Value effect (Fama-French 1992)

- High B/M > Low B/M
- 4-5% annual historical
- 2010-2020 weakened, 2021- revival

![Figure 14.11 — Monthly Return Difference between High Book-to-Price (value) and Low Book-to-Price (growth) Stocks around the World. 교재 p.450](/courses/financial-management/figures/ch14/fig-14-11.png)

> **직관**: value−growth 월간 초과수익(.33~.62%)이 *전 지역에서 양(+)* 이다 — value premium 이 미국만의 우연이 아니라 글로벌하게 나타나는 강건한 이상현상임을 보여준다.

### §3.3 Momentum (Jegadeesh-Titman 1993)

- Past 6-12 month winners
- 8% annual historical
- Persists countries, asset classes

### §3.4 Calendar Effects

- January effect (small-cap)
- Weekend (Monday underperform)
- Holiday (pre-holiday outperform)

### §3.5 Post-earnings drift

- Positive surprise → continued 60-90 days
- Behavioral underreaction

![Figure 14.9 — Returns on Two Investment Strategies Based on Earnings Surprise. 교재 p.449](/courses/financial-management/figures/ch14/fig-14-9.png)

> **직관**: *극단적 양(+) 어닝서프라이즈* 포트폴리오는 발표 후 275일까지 +3.25% 더 오르고, *음(−)* 포트폴리오는 −3.94%로 더 빠진다 — 정보가 *서서히* 반영되는 underreaction(PEAD), semi-strong 효율성에 반하는 증거.

### §3.6 IPO underperformance

- First-day +15% underpricing
- 3-5 year underperform
- Loughran-Ritter

![Figure 14.14 — Returns on Initial Public Offerings (IPOs) and Seasoned Equity Offerings (SEOs) in Years Following Issue. 교재 p.456](/courses/financial-management/figures/ch14/fig-14-14.png)

> **직관**: IPO·SEO 발행기업(파랑)이 발행 후 여러 해 동안 *style-matched 비발행기업(주황)* 보다 낮은 수익률을 낸다 — "신주 발행 퍼즐(new issues puzzle)". 경영진이 *고평가 시점에 발행*한다는 market-timing 해석.

### §3.7 Bubbles/Crashes

- Tulip 1637, 1929, Japan 1989, Dot-com 2000, 2008, Crypto, SPAC 2021
- Recurring behavioral

![Figure 14.12 — Value of Index of Internet Stocks. 교재 p.451](/courses/financial-management/figures/ch14/fig-14-12.png)

> **직관**: AMEX 인터넷 지수(올리브)가 1999–2000 에 *S&P 500(빨강)* 과 완전히 괴리되며 10배 넘게 폭등했다가 폭락 — dot-com 버블의 교과서적 그림. 펀더멘털과 무관한 가격 급등의 전형.

---

## §4 Behavioral Finance

### §4.1 Foundations

- Kahneman-Tversky (1979): Prospect Theory
- Thaler: Mental accounting
- Shiller (2000): Irrational Exuberance
- Lo (2004): AMH

### §4.2 Cognitive biases (8)

| Bias | 의미 |
|--|--|
| Overconfidence | Skill over-estimation |
| Anchoring | Initial estimate sticky |
| Loss aversion | Loss 2-2.5x more painful |
| Mental accounting | Use-specific money |
| Herding | 군중 따라 |
| Confirmation | Beliefs 확인만 |
| Hindsight | "그럴 줄 알았다" |
| Recency | 최근 over-weight |

**Real impact**:
- Barber-Odean (2000): 6.5% annual cost from over-trading

### §4.3 Limits to Arbitrage

> Rational arbitrageurs cannot quickly correct mispricing.

**Reasons** (Shleifer-Vishny 1997):
1. Fundamental risk
2. Noise trader risk
3. Implementation costs
4. Career concerns

![Figure 14.7 — Deviations of the Ratio of the Market Value of Royal Dutch to the Market Value of Shell from Parity. 교재 p.446](/courses/financial-management/figures/ch14/fig-14-7.png)

> **직관**: Royal Dutch 와 Shell 은 *같은 현금흐름을 60:40으로 나누는* 쌍둥이 주식이라 가격비가 항상 0(parity)이어야 하는데, 실제로는 ±40%까지 벗어났다 — 차익거래가 *오랫동안 못 메운다*(limits to arbitrage)는 결정적 증거.

![Figure 14.8 — The Percentage Difference between One Share of 3Com and One and One-Half Shares of Palm. 교재 p.448](/courses/financial-management/figures/ch14/fig-14-8.png)

> **직관**: 3Com 이 자회사 Palm 지분을 보유해 *3Com ≥ 1.5×Palm* 이어야 하는데, 한동안 그 차이가 *마이너스*(Palm 이 모회사보다 비쌈)였다 — 명백한 mispricing 이 공매도 제약 등으로 즉시 교정되지 못한 사례.

### §4.4 Adaptive Markets Hypothesis (Lo 2004)

- EMH dynamic
- Anomalies emerge → exploited → fade
- Behavioral biases evolving
- Markets learn

---

## §5 Corporate Finance Implications

### §5.1 Stock Price as Fair Value

- EMH: market = fair value
- DCF target should match
- Discrepancy = opportunity or model error

### §5.2 IPO + SEO

- IPO underpricing ~15% (Loughran-Ritter)
- SEO ~3-5%
- Behavioral — sentiment

![Figure 14.13 — Three Stock Price Adjustments after Issuing Equity. 교재 p.455](/courses/financial-management/figures/ch14/fig-14-13.png)

> **직관**: 신주 발행 후 주가 경로 3가지 — 경영진이 *타이밍 능력 없음*(즉시 반영, 점선 상향은 inferior), *효율적 시장*(평탄, 실선), *우월한 타이밍*(하락, 파선). 발행 후 평균적으로 *하락* 한다면 경영진이 고점에 발행했다는 뜻(market timing).

### §5.3 Capital Structure

- Market timing
- Pecking order (Ch 16)
- Behavioral on financing

### §5.4 Dividend Policy

- Signaling
- Bird-in-hand fallacy (Gordon-Lintner)
- Behavioral preference

### §5.5 M&A

- Acquirer's curse — over-pay
- Hubris hypothesis (Roll 1986)
- Method of payment signal
- Long-run underperformance

### §5.6 Stock Splits + Buybacks

- Stock split positive signal
- Buyback under-valuation signal
- Positive empirical return

---

## §6 Famous Studies

### §6.1 Fama-Bondt (1985) — Overreaction

- 3-year losers > 3-year winners
- Mean reversion

### §6.2 Daniel-Hirshleifer-Subrahmanyam (1998)

- Overconfidence + biased self-attribution
- Momentum (short) + reversal (long)

### §6.3 Hong-Stein (1999)

- Underreaction + delayed overreaction

### §6.4 Lakonishok-Shleifer-Vishny (1994)

- Glamour stocks underperform
- Behavioral over-extrapolation

### §6.5 Modern asset pricing

- Cochrane (2011): Factor Zoo
- Harvey-Liu-Zhu (2016): most fail replication
- Hou-Xue-Zhang (2020): 65% factor failure

---

## §7 Bubbles and Crashes

### §7.1 Pattern (5 stages)

1. Displacement (new tech)
2. Boom
3. Euphoria
4. Profit taking (smart money exits)
5. Panic + Crash

### §7.2 Behavioral drivers

- FOMO
- Herding + social proof
- Recency
- Greater fool theory
- Easy credit + leverage

### §7.3 Historical

| 연도 | Bubble | Crash |
|--|--|--|
| 1637 | Tulip | -99% |
| 1720 | South Sea | -84% |
| 1929 | US | -89% |
| 1989 | Japan | -82% |
| 2000 | Dot-com | -78% |
| 2008 | Housing | -57% |
| 2017 | BTC | -84% |
| 2021 | SPAC/meme | -90% |

### §7.4 Recognizing

- CAPE > 30
- Margin debt peak
- IPO frenzy
- Mainstream attention
- Speculation > fundamentals

---

## §8 Modern Market Structure

### §8.1 HFT

- Microsecond decisions
- 60% US equity volume
- Liquidity provider
- Flash crash risk

### §8.2 Algorithmic + Passive

- Index dominance > 50% AUM
- Crowding
- Correlation increase
- Price discovery 한계

### §8.3 Crypto

- Volatility 10x stocks
- Behavioral driven
- Limited fundamental anchor
- Regulatory uncertainty

### §8.4 Social Media

- Meme stocks (GameStop 2021)
- Reddit WSB
- Coordinated retail
- Short squeeze

---

## §9 Synthesis

### §9.1 Adaptive Markets

- EMH mostly applies, mostly of time
- Behavioral creates temporary inefficiency
- Arbitrageurs limit
- Markets evolve

### §9.2 Investor practical

**Passive (EMH belief)**: Index, low cost, diversification.
**Active (behavioral exploit)**: Value, momentum, factor tilts.
**Hybrid**: Core (passive) + satellite (factor).

### §9.3 Corporate manager practical

- Don't time market
- Long-term fundamentals dominate
- Behavioral of investor — signaling
- Capital structure timing limited

---

## §10 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | EMH 강 신뢰 | Anomalies evidence |
| 2 | EMH 완전 거부 | Active failure |
| 3 | Anomaly = arbitrage | Limits |
| 4 | Single anomaly portfolio | Multi-factor |
| 5 | Past = future | Adaptive |
| 6 | Bubble 식별 쉬움 | Hindsight |
| 7 | Behavioral avoidable | Systematic costly |
| 8 | Manager hubris | Acquirer's curse |

---

## §11 자가점검

1. *EMH 3 forms + evidence*?
2. *Anomalies* (size, value, momentum)?
3. *Behavioral biases 8*?
4. *Limits to Arbitrage* 4?
5. *AMH*?
6. *Bubble pattern 5 stages*?

<details><summary>해답</summary>

1. Weak (past), Semi-strong (public), Strong (insider). Event studies, mutual fund evidence.
2. Banz (size), FF (value), Jegadeesh-Titman (momentum).
3. Overconfidence, anchoring, loss aversion, mental accounting, herding, confirmation, hindsight, recency.
4. Fundamental risk, noise trader, implementation, career.
5. EMH dynamic, anomalies emerge → exploited → fade.
6. Displacement → Boom → Euphoria → Profit taking → Panic.

</details>

---

## §12 다음 학습으로

- **Ch 15** — Long-term financing
- **Ch 16-17** — Capital structure
- **Ch 19** — Dividends

---

## §13 한 줄 요약

> **EMH 3 forms. Event studies + mutual fund underperformance evidence. *Anomalies* (size, value, momentum) + *behavioral biases* — EMH challenges. *Limits of Arbitrage* prevent quick correction. *AMH* (Lo) synthesizes. *Bubble pattern* recurring. *Modern market structure* (HFT, passive, crypto, social media) evolution.**
