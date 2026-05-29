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
