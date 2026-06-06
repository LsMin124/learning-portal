# Chapter 24: Warrants and Convertibles — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 24** (책 p.760~780).
> 24장은 *워런트 + 전환사채* — 옵션이 결합된 기업 증권.

이 장의 *지적 무게중심*:
1. **Warrants** — call option (회사 발행), dilution
2. **Convertible bonds** — bond + conversion option
3. **Warrant vs Call** — dilution 차이
4. **Convertible valuation** — straight bond + conversion
5. **왜 발행하는가** — backdoor equity, agency

---

## §0 도입 — *옵션이 박힌 증권*

> **핵심 한 문장**: 워런트와 전환사채는 *옵션이 박힌 기업 증권* — 워런트는 회사가 발행한 **call**(행사 시 신주 *dilution*), 전환사채는 **채권 + 전환 call**. 둘 다 "공짜 점심"이 아니라 옵션 가치만큼 대가를 치르는, 정보 비대칭 시대의 *뒷문 주식 발행(backdoor equity)*.

22장의 옵션 가격이론을 *실제 발행 증권* 에 입히면:

1. **워런트 = 회사가 쓴 call** (§1): 거래소 call 과 달리 행사하면 *신주가 새로 발행* 돼 주식 수가 늘어난다 — 그래서 같은 조건이라도 dilution factor $n/(n+n_w)$ 만큼 call 보다 싸다(figure 24.1 의 AIG 워런트, 상·하한 사이 곡선).
2. **전환사채 = 채권 + 전환권** (§2–3): 가치는 *세 조각* 으로 읽는다 — straight bond floor(하한), conversion value(=비율×주가), 그 위의 option premium. 주가가 낮으면 채권처럼, 높으면 주식처럼 움직인다(figure 24.2 의 floor, 24.3 의 합성 곡선).
3. **왜 발행하나** (§4): "싼 coupon" 은 환상이고(전환권이 그 대가), 진짜 이유는 *backdoor equity*·agency 완화·cash 절약 — 고성장·고위험 기업(Tesla·Netflix)이 단골이다.
4. **forced conversion·CoCo·차익거래** (§5–7): callable 전환사채로 부채를 자본으로 강제 전환하고, 은행은 CoCo 로 규제자본을 만들며, 헤지펀드는 convertible 매수+주식 공매도로 옵션을 포착한다.

한 문장으로: **이 증권들의 값은 "채권 + 옵션"으로 분해되고, 그 옵션은 dilution 을 빼고 변동성을 더해 매겨진다.**

---

## §1 Warrants

### §1.1 정의

> *회사가 발행하는 long-term call option*.

- *Strike (exercise price)* 에 신주 매수권
- 보통 *bond/preferred 와 함께* (sweetener)
- *만기 길다* (수년)
- 행사 시 *신주 발행* (회사가 cash 받음)

### §1.2 Warrant vs Call option

| | Call option | Warrant |
|--|--|--|
| 발행자 | 거래소/투자자 | 회사 |
| 행사 시 | 기존 주식 이전 | *신주 발행* (dilution) |
| 회사 cash | 무관 | 행사가 수취 |
| 만기 | 단기 | 장기 |

### §1.3 Dilution 효과

> 행사 시 *신주 발행* → 주식 수 증가 → *희석*.

**Warrant value (dilution 반영)**:
$$W = \frac{n}{n + n_w} \times \text{Call value (on diluted firm)}$$

- n = 기존 주식, n_w = warrant 주식
- *Dilution factor* = $\frac{n}{n + n_w}$

![Figure 24.1 — AIG Warrants on December 1, 2017. 교재 p.743](/courses/financial-management/figures/ch24/fig-24-1.png)

> **직관**: 워런트 가치의 *띠*. *상한* = 주식 가치(1:1, 위 직선), *하한* = 내재가치(주가−행사가, 아래 직선). 실제 워런트 값은 그 사이 *완만한 곡선*(점선). AIG 워런트는 행사가 $45, 주가 $59.88 일 때 $17.95 — 내재가치($14.88)보다 비싼 만큼이 time value. (call 과 달리 행사 시 dilution 반영)

### §1.4 직관

- *Call*: 행사해도 firm 가치 불변 (기존 주식 이전)
- *Warrant*: 행사 시 *cash 유입* + *신주* → firm 가치 ↑ but 주식 ↑
- → *순 효과는 dilution 으로 call 보다 가치 ↓*

---

## §2 Convertible Bonds

### §2.1 정의

> *전환권* 이 붙은 채권 (bond → 주식 전환).

- *Conversion ratio* — 채권당 전환 주식 수
- *Conversion price* = par / conversion ratio
- *Conversion value* = ratio × 주가
- 보통 *낮은 coupon* (전환권 가치만큼)

### §2.2 핵심 가치 (3 floor)

**1. Straight bond value (bond floor)**:
- 전환 무시한 순수 채권 가치
- *하한* (downside 보호)

**2. Conversion value**:
- = conversion ratio × 주가
- 즉시 전환 시 가치

**3. Convertible value**:
$$\text{Convertible} = \max(\text{Bond floor}, \text{Conversion value}) + \text{Option premium}$$

![Figure 24.2 — Minimum Value of a Convertible Bond versus the Value of the Stock for a Given Interest Rate. 교재 p.749](/courses/financial-management/figures/ch24/fig-24-2.png)

> **직관**: 전환사채의 *바닥*. 두 하한이 만난다 — 수평의 *straight bond value*(주가 무관, 채권으로서 최소가치)와 우상향의 *conversion value*(=전환비율×주가, 기울기=전환비율). 전환사채는 이 둘 중 *높은 쪽* 아래로는 결코 안 내려간다.

### §2.3 가치 다이어그램

```
Convertible
value
  |              / (conversion value)
  |            /
  |     ______/  ← convertible (option premium)
  |    /  bond floor
  |___/____________ 주가
```

- *낮은 주가*: bond floor 근처 (채권처럼)
- *높은 주가*: conversion value 근처 (주식처럼)
- *중간*: option premium (둘 다 보다 높음)

![Figure 24.3 — Value of a Convertible Bond versus the Value of the Stock for a Given Interest Rate. 교재 p.750](/courses/financial-management/figures/ch24/fig-24-3.png)

> **직관**: 그 바닥 *위* 의 진짜 가치. 낮은 주가에선 bond floor 에 붙고(채권처럼), 높은 주가에선 conversion value 에 수렴(주식처럼), 중간에선 둘보다 위로 *부푼다* — 그 봉긋한 차이가 *option value*. 곧 전환사채 = max(floor, conversion) + 전환옵션.

### §2.4 Conversion premium

$$\text{Conversion premium} = \frac{\text{Convertible price} - \text{Conversion value}}{\text{Conversion value}}$$

- 전환가치 대비 *얼마나 비싼지*

---

## §3 Convertible = Bond + Call

### §3.1 분해

$$\text{Convertible bond} = \text{Straight bond} + \text{Call option (on stock)}$$

- *Straight bond*: 채권 가치 (bond floor)
- *Call*: 전환권 (warrant 유사, dilution)

### §3.2 가치 평가

1. *Straight bond value* (comparable yield 로)
2. *Conversion option value* (Black-Scholes/binomial, dilution 조정)
3. 합산

### §3.3 Callable convertible

- 대부분 convertible 은 *callable* (회사 조기상환권)
- 회사가 *forced conversion* 유도 (call 위협)
- *Call protection* 기간 존재

---

## §4 왜 Convertible / Warrant 발행?

### §4.1 잘못된 이유 (free lunch 환상)

- ~~"낮은 coupon 으로 싸게 차입"~~ — 전환권 대가
- ~~"높은 가격에 주식 발행"~~ — 불확실
- → *Free lunch 없음* (옵션 가치만큼 대가)

### §4.2 올바른 이유

**1. Backdoor equity (지연된 주식 발행)**:
- *직접 SEO 어려운* 성장기업
- 주가 상승 시 자동 전환 → equity
- *Pecking order* (Ch 17) 우회

**2. Agency cost 완화**:
- *Risk-shifting* 완화 (채권자도 upside 참여)
- *Asset substitution* 문제 감소

**3. Information asymmetry**:
- *불확실한 위험* 의 기업
- 채권자-주주 valuation 차이 좁힘
- "Backdoor equity" — 정보 비대칭 신호 완화

**4. Cash flow 절약**:
- *낮은 coupon* (성장기 cash 부족)
- 스타트업, 고성장 기업

### §4.3 발행 기업 특성

- *고성장 + 고위험* (변동성 ↑ → 전환권 가치)
- *Tesla, Twitter, Netflix* — convertible 발행
- *스타트업 / mezzanine*

---

## §5 Forced Conversion

### §5.1 메커니즘

- Convertible 이 *callable* 일 때
- 주가 ↑ → conversion value > call price
- 회사가 *call 행사 위협* → bondholder 전환 강제
- → *equity 로 전환* (부채 → 자본)

### §5.2 왜 forced conversion

- *부채 → 자본* (leverage 감소)
- *Coupon 부담 제거*
- *Capital structure 조정*

### §5.3 타이밍

- *최적 call 시점* 논쟁 (이론 vs 실무)
- *이론*: conversion value = call price 즉시
- *실무*: 지연 (safety margin, signaling)

---

## §6 Mandatory Convertibles + 기타

### §6.1 Mandatory convertible

- *만기에 강제 전환* (선택권 없음)
- *Equity-like* (회계상 자본 가까움)
- 높은 배당, 전환 상한/하한

### §6.2 Contingent convertible (CoCo)

- *조건부 전환* (자본비율 하락 시)
- *은행 규제 자본* (Basel III)
- *Bail-in* 메커니즘

### §6.3 Convertible preferred

- *VC 표준* (Ch 15, 20)
- Liquidation preference + 전환권
- Downside 보호 + upside

---

## §7 Convertible Arbitrage

### §7.1 전략

- *Convertible 매수 + 주식 공매도* (delta hedge)
- *Option 가치* 포착 (저평가 시)
- *Hedge fund* 흔한 전략

### §7.2 위험

- *Credit risk* (issuer 부도)
- *Liquidity* (convertible 시장 얇음)
- *2008 위기*: convertible arb 펀드 큰 손실 (deleveraging)

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Warrant = call 과 동일 | Dilution (신주 발행) |
| 2 | Convertible = 싼 차입 (free lunch) | 전환권 대가 |
| 3 | Convertible value = bond floor | + option premium |
| 4 | Convertible = bond floor or conversion 중 하나 | max + premium |
| 5 | 전환권 무시 valuation | bond + call 분해 |
| 6 | Forced conversion 즉시 | 실무 지연 (safety margin) |
| 7 | 낮은 coupon = 이득 | 전환권 가치 반영 |
| 8 | Dilution 무시 (warrant) | n/(n+n_w) factor |

---

## §9 자가점검

1. *Warrant vs Call* 차이?
2. *Convertible* 의 3 가치 (floor)?
3. *Convertible = ?* (분해)?
4. *왜 convertible 발행* (올바른 이유)?
5. *Forced conversion* 메커니즘?
6. *Convertible arbitrage*?

<details><summary>해답</summary>

1. Warrant: 회사 발행, 행사 시 신주 (dilution), cash 유입, 장기. Call: 거래소, 기존 주식 이전.
2. Bond floor (straight bond, 하한), conversion value (ratio × 주가), convertible = max + option premium.
3. Convertible = straight bond + call option (on stock, dilution 조정).
4. Backdoor equity (지연 주식 발행), agency cost 완화 (risk-shifting), info asymmetry, cash 절약 (낮은 coupon).
5. Callable convertible + 주가 ↑ → 회사 call 위협 → bondholder 전환 강제 → 부채→자본.
6. Convertible 매수 + 주식 공매도 (delta hedge), option 가치 포착. 위험: credit, liquidity (2008 손실).

</details>

---

## §10 다음 학습으로

- **Ch 25** — Derivatives and hedging
- **Ch 22** — Options 기본 (recap)
- **Ch 15, 20** — Convertible preferred (VC)

---

## §11 한 줄 요약

> **Warrants = 회사 발행 long-term call (행사 시 *신주 dilution*, n/(n+n_w) factor). *Convertible bond* = straight bond + conversion option. *3 가치*: bond floor (하한), conversion value (ratio × 주가), convertible = max + option premium. *왜 발행*: backdoor equity + agency 완화 + cash 절약 (free lunch 아님, 전환권 대가). *Forced conversion* (callable + 주가↑ → 강제 전환). *Convertible arbitrage* (매수 + 공매도 delta hedge).**
