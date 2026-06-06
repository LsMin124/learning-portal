# Chapter 23: Options and Corporate Finance — Extensions and Applications — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 23** (책 p.736~759).
> 23장은 *옵션의 기업 응용* — Executive stock options, Startup valuation, Real options (확장), 위험 채권의 옵션 분해.

이 장의 *지적 무게중심*:
1. **Executive Stock Options (ESO)** — valuation, incentive, 논란
2. **Startup as options** — 단계적 투자
3. **Real options 심화** — timing, expansion, abandonment
4. **Decision tree vs Real options**
5. **Mergers as options**

---

## §0 도입 — *기업 도처의 옵션*

> **핵심 한 문장**: 22장이 *거래소 옵션* 의 가격을 다뤘다면, 23장은 그 렌즈를 **기업 안** 으로 돌린다 — 경영진 보상(ESO), 스타트업의 단계 투자, 광산·R&D 의 유연성, 위험 채권까지 모두 *옵션* 으로 보고 같은 이항트리·risk-neutral 기법으로 값을 매긴다.

22장의 결론("주식 = call")을 받아, 23장은 다섯 갈래로 확장한다:

1. **경영진 옵션 (ESO)** (§1): 사실상 회사 주식 call — 2004년 FASB 가 ATM 도 *fair value 비용* 으로 인식하게 강제하기 전까진 "공짜 보상"처럼 보였다. repricing·backdating 논란의 뿌리.
2. **스타트업·R&D = compound option** (§2): 적자 기업도 *높은 변동성* 이 곧 가치 — 각 투자 라운드가 *다음 라운드에 대한 옵션* 이라 DCF 음수도 정당화될 수 있다(남용 주의).
3. **real options 심화** (§3): expand(call)·abandon(put)·delay(American call)·switch. 값은 *binomial tree* 로 — figure 23.1(2시점)·23.2(3시점)이 그 골격.
4. **decision tree vs real option** (§4): 둘 다 미래 분기를 다루지만 decision tree 는 *실제 확률 + 위험조정 할인율*, real option 은 *risk-neutral 확률 + 무위험율* 을 쓴다. 기초자산이 거래되면 후자가 무차익으로 더 정확.
5. **위험 채권 = 무위험채권 − put** (§6): credit spread 가 곧 그 put 의 가격. 광산 같은 자원 사업(figure 23.3 의 금 이항트리·23.4 의 시뮬 경로)이 이 모든 기법의 결정판이다.

관통하는 명제: **유연성과 조건부 결정은 모두 옵션이고, 옵션은 변동성을 먹고 산다.**

---

## §1 Executive Stock Options (ESO)

### §1.1 정의

> 경영진에게 부여하는 *회사 주식 call option*.

- *Strike* = 부여 시 주가 (보통 ATM)
- *Vesting* (보통 3-4년)
- *Expiration* (보통 10년)
- *Non-transferable*

### §1.2 목적

1. **Incentive alignment** — 주가 ↑ 유인
2. **Talent retention** — vesting 으로 묶음
3. **Cash 절약** — 현금 대신 (스타트업)
4. **Tax** — 일부 우대 (ISO)

### §1.3 ESO 의 *과대평가 문제*

- *과거*: ATM option 은 회계상 비용 0 (intrinsic 0)
- *FASB 2004 (ASC 718)*: *fair value 비용 처리* 강제
- → ESO 의 진짜 비용 (Black-Scholes) 인식

### §1.4 ESO valuation 의 특수성

- *Non-transferable* → 조기 행사 경향 (Black-Scholes 과대)
- *Vesting* 위험 (퇴사 시 소멸)
- *Dilution* (신주 발행)
- → *조정 Black-Scholes* 또는 *binomial*

### §1.5 논란

- **Repricing** — 주가 하락 시 strike 인하 ("heads I win, tails I reprice")
- **Backdating** — 부여일 조작 (2006 스캔들)
- **Excessive comp** — CEO-직원 격차
- **Short-termism** — 단기 주가 유인

---

## §2 Startup / Equity as Option

### §2.1 적자 스타트업 valuation

> 전통 DCF 어려움 (현금흐름 음수, 높은 불확실성).

- *Equity = call option* on 미래 가치
- *높은 변동성* → option 가치 ↑
- → DCF 가 음수여도 *option value* 로 정당화 가능 (단, 남용 주의)

### §2.2 Staged investment = compound option

- 각 라운드 = *다음 라운드에 대한 옵션*
- Series A = option on Series B = option on ...
- *VC staged financing* (Ch 20) 의 옵션 해석

### §2.3 R&D as option

- *R&D 투자* = 미래 제품에 대한 call
- *Pharma*: Phase I = option on Phase II = ... = option on launch
- *높은 실패율 + 큰 성공* = 옵션 성격

---

## §3 Real Options — 심화 (Ch 7 확장)

### §3.1 Option to Expand

- *Pilot project* = option on full-scale
- 성공 시 *확장* (call 행사)
- *Negative NPV pilot* 도 option value 로 정당화

### §3.2 Option to Abandon

- *Failure 시 청산* (put)
- *Salvage value* = put strike
- *Flexibility* 가치

### §3.3 Option to Delay (Timing)

- *지금 vs 나중* 투자
- *Information 도착* 대기
- *American call* (조기 행사 가능)
- 단, *경쟁자 진입* 위험 (preemption)

### §3.4 Option to Contract / Switch

- *생산 축소* (put-like)
- *Input/output 전환* (flexible manufacturing)

### §3.5 Real option valuation 방법

1. **Black-Scholes** — 단순 case
2. **Binomial tree** — 단계적, American
3. **Monte Carlo** — 복잡, path-dependent
4. **Decision tree** — 이산 결정

---

![Figure 23.1 — Movement of Heating Oil Prices from September 1 to December 1 in a Two-Date Example. 교재 p.726](/courses/financial-management/figures/ch23/fig-23-1.png)

> **직관**: real option 을 *이항트리* 로 푸는 가장 단순한 예. 9월 1일 heating oil $2.00 이 12월 1일 $2.74(↑) 또는 $1.46(↓). 행사가 $2.10 call 은 위에서 $0.64, 아래서 $0. risk-neutral 확률로 두 결과를 가중·할인하면 옵션 값 — *실제 확률은 필요 없다*.

![Figure 23.2 — Movement of Heating Oil Prices in a Three-Date Model. 교재 p.728](/courses/financial-management/figures/ch23/fig-23-2.png)

> **직관**: 같은 논리를 *3시점* 으로. 단계마다 ×1.25 / ×0.80 로 갈라져 12월 1일엔 세 결과($3.13/$2.00/$1.28). 끝에서부터 *역진(backward)* 으로 각 노드의 옵션 값을 채워 현재로 접는다 — multi-period binomial 의 전형.

---

## §4 Decision Tree vs Real Options

### §4.1 Decision Tree (Ch 7 recap)

- *이산적* 결정 node + chance node
- *Backward induction*
- *실제 확률* 사용 → discount at risk-adjusted rate

### §4.2 Real Options

- *연속적* 또는 옵션 framework
- *Risk-neutral* valuation
- *Volatility* 기반

### §4.3 언제 어느 것

| 상황 | 방법 |
|--|--|
| 이산 결정 (go/no-go) | Decision tree |
| 연속 가치 변동 | Real option (BS) |
| Traded underlying | Real option (risk-neutral) |
| 주관적 확률 | Decision tree |
| Path-dependent | Monte Carlo |

### §4.4 두 방법의 차이 (discount rate)

- *Decision tree*: 실제 확률 + risk-adjusted rate
- *Real option*: risk-neutral prob + risk-free rate
- → *Traded asset* 면 real option 이 더 정확 (no-arbitrage)

---

## §5 Mergers and Options

### §5.1 M&A 의 옵션 성격

- *Toehold* = option on full acquisition
- *Staged acquisition* = compound option
- *Termination fee* = option premium 유사

### §5.2 Collar (M&A 에서)

- 주식 인수 시 *교환 비율 조정*
- *Floor + cap* (collar) → put + call 조합
- 인수가 변동 위험 hedge

### §5.3 Earnout

- *성과 조건부 추가 지급*
- = *option on target performance*
- 정보 비대칭 해소

---

## §6 위험 채권의 옵션 분해 (Ch 22 심화)

### §6.1 Risky debt = Risk-free − Put

$$\text{Risky debt} = \text{Risk-free debt} - \text{Put on firm value}$$

- 채권자가 *put 매도* (주주에게)
- *Default option* = 주주의 limited liability

### §6.2 Credit spread = Put value

- *Credit spread* (yield 차이) = put option 가치 반영
- *변동성 ↑* → put ↑ → spread ↑
- *Merton model* → 신용위험 정량화

### §6.3 Structural credit models

- **Merton (1974)**: equity = call, debt = risk-free − put
- **KMV / Moody's**: distance-to-default
- **CDS**: 명시적 default protection (put on credit)

### §6.4 함의

- *Distance-to-default* = (V − D) / σ_V
- *낮을수록* default 확률 ↑
- *Volatility* 가 핵심 입력

---

## §7 실무 응용

### §7.1 자원 산업 (oil, mining)

- *유전/광산* = option on commodity price
- *낮은 가격* → 생산 중단 (abandon option)
- *높은 가격* → 확장 (expand)
- *Brennan-Schwartz* model

![Figure 23.3 — A Binomial Tree for Gold Prices. 교재 p.734](/courses/financial-management/figures/ch23/fig-23-3.png)

> **직관**: 광산이라는 real option 의 무대 — 금값의 6개월 간격 *이항트리*(Now $1,300 → 18개월 후 $2,209~$765). 각 노드에서 *채굴할까 멈출까* 를 결정할 수 있어 광산은 금값에 대한 *일련의 옵션* 이 된다. expand/abandon 이 트리 위에서 행사된다.

![Figure 23.4 — A Possible Path for the Price of Gold. 교재 p.736](/courses/financial-management/figures/ch23/fig-23-4.png)

> **직관**: 그 트리에서 뽑은 *하나의 시뮬 경로*. 가격이 $2,209 에 닿으면 광산을 *열고*(−$20M), $1,089 로 떨어지면 *닫는다*(−$10M). 각 시점 현금흐름 = 25,000oz × (금값−$1,400). 이런 경로 5,000개의 평균 PV 가 광산 가치 — Monte Carlo real option 의 그림.

### §7.2 부동산 개발

- *토지* = option on development
- *Timing option* (언제 개발)
- *Vacant land* 가 옵션 가치

### §7.3 IP / Patent

- *특허* = option on commercialization
- *License* = option transfer

### §7.4 Insurance

- *Guarantee* = put 매도
- *Deposit insurance* (FDIC)
- *Pension guarantee* (PBGC)

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | ESO 비용 0 (ATM) | FASB 2004 — fair value 비용 처리 |
| 2 | ESO = Black-Scholes 그대로 | Non-transferable, vesting 조정 |
| 3 | Real option 으로 모든 것 정당화 | Identifiable + exercisable + measurable |
| 4 | Decision tree = real option | 확률·discount rate 다름 |
| 5 | Risky debt 옵션 무시 | = risk-free − put |
| 6 | Negative NPV = 거부 | Real option value 고려 (단 남용 주의) |
| 7 | Timing option 무시 | Delay 가치 (단, preemption 위험) |
| 8 | Volatility 추정 쉬움 | Non-traded → 어려움 |

---

## §9 자가점검

1. *ESO* 목적 + FASB 2004 변화?
2. *Startup / R&D 가 옵션* 인 이유?
3. *Real options 4종* (Ch 7) + valuation 방법?
4. *Decision tree vs Real option* 차이?
5. *Risky debt 옵션 분해*?
6. *자원 산업 옵션* 응용?

<details><summary>해답</summary>

1. Incentive alignment + retention + cash 절약. FASB 2004 (ASC 718): ATM 도 fair value 비용 처리 강제.
2. Equity = call on 미래 가치. 높은 변동성 → option ↑. Staged = compound option. R&D = call on 제품.
3. Expand (call), Abandon (put), Delay (American call), Switch. Valuation: BS, binomial, MC, decision tree.
4. Decision tree: 이산, 실제 확률, risk-adjusted rate. Real option: 연속, risk-neutral prob, risk-free rate.
5. Risky debt = risk-free debt − put on firm value. Credit spread = put 가치. Merton model.
6. 유전/광산 = option on commodity price. 낮은 가격 → abandon, 높은 가격 → expand.

</details>

---

## §10 다음 학습으로

- **Ch 24** — Warrants and convertibles
- **Ch 25** — Derivatives and hedging
- **Ch 22** — Options 기본 (recap)
- **Ch 7** — Real options (recap)

---

## §11 한 줄 요약

> **Options 응용 — *ESO* (incentive, FASB 2004 fair value 비용, repricing/backdating 논란). *Startup/R&D = option* (변동성 가치, staged = compound). *Real options 심화* (expand/abandon/delay/switch). *Decision tree* (이산, 실제 확률) vs *Real option* (연속, risk-neutral). *Risky debt = risk-free − put* (Merton, credit spread = put 가치). *자원/부동산/IP* 모두 옵션. 단 *identifiable + exercisable + measurable* 일 때만 적용.**
