# Chapter 11: Return and Risk — CAPM — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 11** (책 p.353~390).
> 11장은 *Capital Asset Pricing Model (CAPM)* — equilibrium risk-return relationship. **Portfolio theory** (Markowitz), **Beta**, **SML**.

이 장의 *지적 무게중심*:
1. **Individual asset risk** — variance, std deviation
2. **Portfolio risk** — variance, correlation, diversification
3. **Systematic vs Unsystematic risk**
4. **CAPM**
5. **Beta**
6. **Security Market Line (SML)**

---

## §0 도입 — *위험에 가격표를 붙이다*

> **핵심 한 문장**: 10장이 "주식은 변동성이 크다"는 *사실* 을 보여줬다면, 11장은 그 위험을 *분산으로 없앨 수 있는 부분과 없앨 수 없는 부분* 으로 쪼개고 — **시장은 후자(systematic=β)에만 값을 치른다**는 균형 이론(CAPM)을 세운다.

논리는 네 걸음으로 이어진다:

1. **포트폴리오 위험은 *공분산* 이 지배한다** (§2). 두 자산을 섞으면 분산은 가중평균보다 *작다* — 상관 ρ<1 이면(figure 11.1) 서로 상쇄되기 때문. 자산 수 N 이 커지면 개별 분산은 1/N 로 사라지고 *평균 공분산만 남는다*.
2. **그래서 위험은 둘로 갈린다** (§3) — *unsystematic*(분산으로 제거 가능)과 *systematic*(시장 전체 충격, 제거 불가, figure 11.7). 공짜로 없앨 수 있는 위험에 시장이 프리미엄을 줄 리 없다.
3. **systematic 위험의 측정자 = β** (§4). $\beta_i = Cov(R_i,R_M)/\sigma_M^2$ — 시장이 1% 움직일 때 자산이 몇 % 움직이나(figure 11.10 의 회귀 기울기).
4. **CAPM 이 기대수익을 β 로 가격한다** (§5–6): $E[R_i] = R_f + \beta_i\,[E[R_M]-R_f]$. 이 직선이 *SML*(figure 11.11) — 모든 자산이 그 위에 놓이도록 차익거래가 가격을 조정한다.

Markowitz 의 *efficient frontier*(figure 11.6)와 무위험자산을 더한 *CML*(figure 11.8·11.9)이 그 배경 기하학이다. 한 문장으로: **"보상받는 위험은 β 뿐이다."**

---

## §1 Individual Securities

### §1.1 Expected return

$$E[R] = \sum p_s R_s$$

### §1.2 Variance + Std

$$\sigma^2 = \sum p_s (R_s - E[R])^2$$

### §1.3 예

| State | P | R |
|--|--|--|
| Boom | 30% | 30% |
| Normal | 50% | 10% |
| Recession | 20% | -20% |

- E[R] = 0.3×30 + 0.5×10 + 0.2×(-20) = **10%**
- Variance: 0.3×400 + 0.5×0 + 0.2×900 = 300
- σ = √300 = **17.3%**

---

## §2 Portfolios

### §2.1 Portfolio Expected Return

$$E[R_P] = \sum w_i E[R_i]$$

![Figure 11.2 — Expected Returns and Standard Deviations for Supertech, Slowpoke, and a 60/40 Portfolio. 교재 p.338](/courses/financial-management/figures/ch11/fig-11-2.png)

> **직관**: Supertech(고수익·고위험)과 Slowpoke(저수익·저위험), 그리고 60/40 포트폴리오(□)를 *기대수익–표준편차* 평면에 찍은 점. 포트폴리오 σ(15.44%)가 두 자산 σ의 단순 가중평균보다 *왼쪽으로 당겨진* 것이 분산효과의 첫 증거다.

### §2.2 Portfolio Variance — 2 assets

$$\sigma_P^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho \sigma_1 \sigma_2$$

### §2.3 Correlation range

| ρ | Meaning |
|--|--|
| +1 | Perfect positive |
| 0 | No correlation |
| -1 | Perfect negative |

![Figure 11.1 — Examples of Different Correlation Coefficients. 교재 p.333](/courses/financial-management/figures/ch11/fig-11-1.png)

> **직관**: 세 패널이 ρ의 의미를 시각화한다. *완전 양(+1)* — A·B가 같은 시점에 함께 오르내려 섞어도 위험은 그대로. *완전 음(−1)* — 정확히 반대로 움직여 섞으면 *완벽 헤지*. *무상관(0)* — 제각각. 분산효과는 바로 이 ρ가 1 미만일 때 생긴다.

### §2.4 Diversification core

> ρ < 1 → portfolio σ < weighted avg.

**예** — 2 assets, equal weight, σ = 20%:
- ρ = 1: σ_P = 20% (no diversification)
- ρ = 0: σ_P = 14.1% (decent)
- ρ = -1: σ_P = 0% (perfect hedge)

![Figure 11.3 — Set of Portfolios Composed of Holdings in Supertech and Slowpoke (correlation −0.1639). 교재 p.339](/courses/financial-management/figures/ch11/fig-11-3.png)

> **직관**: 두 자산의 비중을 0→100%로 바꾸며 그린 *기회집합*. 직선이 아니라 *왼쪽으로 휜 곡선* 인 게 핵심 — ρ=−0.1639<1 이라 섞을수록 σ가 줄어 MV(최소분산점)에서 가장 왼쪽이 된다. 위쪽 가지만 효율적(같은 σ에 더 높은 수익).

![Figure 11.4 — Opportunity Sets Composed of Holdings in Supertech and Slowpoke. 교재 p.341](/courses/financial-management/figures/ch11/fig-11-4.png)

> **직관**: 같은 두 자산이라도 ρ가 작을수록 곡선이 더 *왼쪽으로 휜다*. ρ=1(직선, 분산효과 0)→0.5→0→−0.1639→−1(거의 꼭짓점). *낮은 상관 = 강한 분산효과* 를 한 그림에 겹쳐 보여준다.

![Figure 11.5 — Return/Risk Trade-off for World Stocks: Portfolio of U.S. and Foreign Stocks. 교재 p.342](/courses/financial-management/figures/ch11/fig-11-5.png)

> **직관**: 이론이 아닌 실제 데이터 — 미국·해외 주식 비중을 바꾼 *국제 분산*. 100% 미국에서 해외를 섞기 시작하면 *수익은 오르고 위험은 오히려 줄어* 곡선이 좌상향한다. 최소분산점이 해외 비중이 꽤 높은 쪽이라는 게 자국편향(home bias)의 반례.

### §2.5 Portfolio Variance — N assets

$$\sigma_P^2 = \sum_i w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j Cov_{ij}$$

→ N variance + N(N-1) covariance terms. Large N: covariance dominant.

### §2.6 Equal-weight large portfolio

> N → ∞, equal weight, similar assets:

$$\sigma_P^2 \to \overline{Cov}$$

→ Individual variance N분의 1, covariance average 만 남음.

---

## §3 Systematic vs Unsystematic Risk

### §3.1 Total risk decomposition

**Systematic** (market): 모든 자산 영향, *diversification 불가*. GDP, rate, war.
**Unsystematic** (firm-specific): 특정 영향, *diversification 가능*. CEO, recall, lawsuit.

### §3.2 Diversification limit

```
Portfolio σ
  |\
  | \
  |  \____ Systematic risk (limit)
  |________________ N
       30-50
```

- N ~30: most unsystematic gone
- N → ∞: only systematic

![Figure 11.7 — Portfolio Diversification. 교재 p.348](/courses/financial-management/figures/ch11/fig-11-7.png)

> **직관**: 분산투자의 *한계* 를 보여준다. 1종목 σ 49.2%에서 종목을 늘리면 급격히 떨어지지만 ~19.2%에서 *바닥* 을 친다. 위쪽 줄어드는 부분이 *diversifiable(unsystematic)*, 바닥의 평평한 부분이 *nondiversifiable(systematic)*. 시장이 보상하는 건 후자뿐이다.

### §3.3 Implications

- *Unsystematic non-priced* — 시장 compensate 안 함
- *Systematic priced* — Beta measure

---

## §4 Beta — Systematic Risk Measure

### §4.1 Definition

$$\beta_i = \frac{Cov(R_i, R_M)}{\sigma_M^2}$$

![Figure 11.10 — Performance of Jelco, Inc., and the Market Portfolio. 교재 p.355](/courses/financial-management/figures/ch11/fig-11-10.png)

> **직관**: β의 *그림 정의*. 가로축은 시장수익, 세로축은 Jelco 수익. 점들에 회귀선(characteristic line)을 그으면 *기울기 = β = 1.5* — 시장이 1% 오를 때 Jelco는 1.5% 오른다. β는 곧 *시장 민감도의 회귀 기울기* 다.

### §4.2 Interpretation

| β | Meaning |
|--|--|
| = 1 | Move with market |
| > 1 | Aggressive |
| < 1 | Defensive |
| = 0 | No correlation |
| < 0 | Counter-cyclical (gold) |

### §4.3 Industry betas (2024)

| Industry | β |
|--|--|
| Utility | 0.4-0.6 |
| Consumer staple | 0.6-0.8 |
| Healthcare | 0.7-0.9 |
| Industrial | 1.0-1.2 |
| Financial | 1.1-1.3 |
| Tech | 1.2-1.5 |
| Biotech | 1.5-2.0 |
| Crypto | 2.0-3.0 |

### §4.4 Portfolio beta

$$\beta_P = \sum w_i \beta_i$$

### §4.5 Estimation

**Regression**:
$$R_i - R_f = \alpha + \beta (R_M - R_f) + \epsilon$$

- Slope = β
- Intercept = α (Jensen's alpha)
- R² = explained variance

**Common**: 5 year monthly, S&P 500 proxy, 3-mo T-bill R_f.

### §4.6 Beta instability

- Time-varying
- Industry restructuring
- Recession 시 ↑ (correlation 증가)
- Bayesian shrinkage toward 1

---

## §5 CAPM

### §5.1 Equation

$$E[R_i] = R_f + \beta_i (E[R_M] - R_f)$$

= R_f + β × ERP.

### §5.2 Assumptions

1. Risk-averse + mean-variance optimizer
2. Homogeneous expectations
3. Risk-free borrow/lend
4. No transaction cost, tax
5. Single-period horizon
6. Frictionless markets
7. All hold market portfolio

### §5.3 예 — IBM

- R_f = 4%, ERP = 6%, β = 0.9
$$E[R] = 4\% + 0.9 \times 6\% = 9.4\%$$

### §5.4 왜 CAPM

- Single-factor simple
- Equilibrium derived
- Industry standard
- DCF discount rate

---

## §6 Security Market Line (SML)

### §6.1 Graphical CAPM

```
E[R]
  ^
  |       . Asset A (above = under-priced)
  |    .
  |  .  
  |.    Slope = ERP
  R_f___________ β
              1
```

- Slope = ERP, Intercept = R_f
- On SML: fairly priced
- Above: under-priced
- Below: over-priced

![Figure 11.11 — Relationship between Expected Return on an Individual Security and Beta. 교재 p.358](/courses/financial-management/figures/ch11/fig-11-11.png)

> **직관**: CAPM의 그래프 = *SML*. 가로축이 σ가 아니라 **β** 임에 주의 — 개별 자산의 *systematic* 위험만 본다. 직선 $R_F + \beta(\bar R_M - R_F)$ 위에 있으면 적정가격. S(아래)는 *고평가*(같은 β에 수익 부족), T(위)는 *저평가*. 차익거래가 모두를 선 위로 끌어당긴다.

### §6.2 SML vs CML

| | SML | CML |
|--|--|--|
| X-axis | Beta | Std dev |
| Y-axis | E[R] | E[R] |
| Use | Individual asset | Efficient portfolio |
| Risk | Systematic | Total |

### §6.3 Mispricing

- Above → buy → price ↑ → SML 수렴
- Below → sell → price ↓ → SML 수렴

→ Arbitrage mechanism.

---

## §7 Markowitz Portfolio Theory

### §7.1 Efficient Frontier

```
E[R]
  |     *   Maximum
  |    *
  |   *
  |  * Efficient frontier
  | *
  |* Min variance
  |____________________ σ
```

![Figure 11.6 — The Feasible Set of Portfolios Constructed from Many Securities. 교재 p.343](/courses/financial-management/figures/ch11/fig-11-6.png)

> **직관**: 여러 종목으로 만들 수 있는 모든 포트폴리오의 집합(*feasible set*). 왼쪽 경계 MV~X의 *위쪽 가지* 가 **efficient frontier** — 주어진 위험에 최대 수익. 내부 점(1·2·3·W)은 모두 비효율(같은 σ에 더 나은 점이 위에 있다).

### §7.2 Optimal Portfolio

- Risk-free + risky 의 combination
- Tangent of CML and frontier = *Market portfolio*
- Two-fund theorem — all hold same risky, vary R_f weight

![Figure 11.9 — Relationship between Expected Return and Standard Deviation for a Combination of Risky Securities and the Riskless Asset. 교재 p.352](/courses/financial-management/figures/ch11/fig-11-9.png)

> **직관**: 무위험자산 + *효율적 위험포트폴리오 Q* 의 결합. R_F에서 Q의 효율집합에 *접하는* 직선 II 가 **CML** — 가능한 모든 직선 중 가장 가파르다(최고 Sharpe). 점1(70% 무위험)·점3(140% 주식, 차입)처럼 *한 위험포트폴리오 Q + 무위험 비중* 만으로 모두 도달한다(two-fund 정리).

### §7.3 Risk-free addition

- Lending (positive R_f) — conservative
- Borrowing (negative R_f, leverage) — aggressive
- All optimal on CML

![Figure 11.8 — Relationship between Expected Return and Risk for Portfolios Composed of the Riskless Asset and One Risky Asset. 교재 p.351](/courses/financial-management/figures/ch11/fig-11-8.png)

> **직관**: 무위험자산을 *하나의 위험자산*(Merville)과 섞으면 둘을 잇는 *직선* 이 된다. R_F(10%)에서 출발해 35/65 같은 *대출(lending)* 점, Merville을 지나 120/−20 같은 *차입(borrowing) 레버리지* 점까지. 위험–수익이 선형으로 늘어나는 게 CML의 씨앗.

### §7.4 Market portfolio

> Theoretically: all risky, market cap weighted.

- S&P 500 common proxy
- Total stock market broader
- Global multi-asset true theoretical

---

## §8 CAPM Empirical Evidence

### §8.1 Tests

**Fama-MacBeth (1973)** — two-pass regression.

**Findings**:
- Beta-return relationship exists
- Slope < ERP (weak)
- Size, value 등 significant

### §8.2 Known failures

**1. Low beta anomaly** (Frazzini-Pedersen 2014): Low β stocks outperform.
**2. Size effect**: Small > Large after β.
**3. Value effect**: Value > Growth after β.
**4. Momentum**: Past winner outperforms (12 month).

### §8.3 Critiques

- *Roll critique (1977)*: Market portfolio non-observable
- Empirical failures
- Behavioral biases not captured
- Single-period unrealistic
- Homogeneous expectations unrealistic

### §8.4 Modern alternatives

- Fama-French 3 factor: market + size + value (1992)
- Carhart 4 factor: + momentum (1997)
- Fama-French 5 factor: + profitability + investment (2015)
- APT (Ross 1976) — multiple factors
- q-factor (Hou-Xue-Zhang)

---

## §9 CAPM Practical Use

### §9.1 Capital budgeting

> Project β → required return → WACC.

### §9.2 Portfolio management

- Active: alpha search
- Passive: β = 1 (index)
- Smart beta: factor tilts

### §9.3 Performance evaluation

- Jensen's alpha: portfolio return − CAPM predicted
- Treynor: excess / β
- Information ratio: alpha / tracking error

### §9.4 Risk management

- Portfolio β monitoring
- Beta hedging
- Stress test (β change in crisis)

---

## §10 International CAPM

### §10.1 International

$$E[R] = R_f + \beta_w (E[R_w] - R_f)$$

### §10.2 Country β

- Developed: 1.0 baseline
- Emerging: 1.5-2.0
- Country risk premium (Damodaran)

### §10.3 Cross-border

- Adler-Dumas — segmented
- Solnik — integrated
- Modern — partial integration

---

## §11 자주 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | High return = high σ | Systematic 만 priced |
| 2 | Diversification 무한 | Systematic floor |
| 3 | β = volatility | β = systematic, σ = total |
| 4 | CAPM empirical 정확 | Multiple anomalies |
| 5 | Market = S&P 500 | Theoretical broader |
| 6 | β 안정 | Time-varying |
| 7 | Single-factor sufficient | Multi-factor modern |
| 8 | Negative β impossible | Gold rare 가능 |

---

## §12 자가점검

1. *Portfolio variance* 2-asset?
2. *Diversification limit*?
3. *Systematic vs Unsystematic*?
4. *Beta* 정의?
5. *CAPM equation + assumptions*?
6. *SML 위/아래*?
7. *Empirical failures*?

<details><summary>해답</summary>

1. $\sigma_P^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho\sigma_1\sigma_2$.
2. Unsystematic 사라짐, systematic floor.
3. Systematic = market-wide undiversifiable. Unsystematic = firm-specific diversifiable.
4. $\beta = Cov(R_i, R_M)/\sigma_M^2$.
5. $E[R] = R_f + \beta(E[R_M]-R_f)$. Risk-averse, mean-variance, homogeneous, R_f borrow/lend, frictionless.
6. Above SML = under-priced (buy), below = over-priced (sell).
7. Low beta anomaly, size, value, momentum. Roll critique.

</details>

---

## §13 다음 학습으로

- **Ch 12** — APT, multi-factor
- **Ch 13** — WACC

---

## §14 한 줄 요약

> **Risk = systematic + unsystematic. Diversification 의 unsystematic 제거, systematic floor. *Beta* = systematic measure. *CAPM*: $E[R] = R_f + \beta \cdot ERP$. *SML* equilibrium pricing. *Markowitz* + *CML*. *CAPM empirical limit* — low beta, size, value, momentum anomalies. *Multi-factor* (Fama-French) modern extension.**
