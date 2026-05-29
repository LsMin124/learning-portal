# Ch 24 Warrants and Convertibles — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *Warrant vs Call option*?

<details><summary>답</summary>

| | Call | Warrant |
|--|--|--|
| 발행자 | 거래소/투자자 | 회사 |
| 행사 시 | 기존 주식 이전 | 신주 발행 (dilution) |
| 회사 cash | 무관 | 행사가 수취 |
| 만기 | 단기 | 장기 |

**Dilution value**:
$$W = \frac{n}{n + n_w} \times \text{Call value (diluted firm)}$$

→ Warrant 는 dilution 때문에 동일 조건 call 보다 가치 ↓.

</details>

### Q2. *Convertible* 의 3 가치 (floor)?

<details><summary>답</summary>

1. **Bond floor** (straight bond value) — 하한, downside 보호
2. **Conversion value** = conversion ratio × 주가
3. **Convertible value** = max(bond floor, conversion value) + option premium

**다이어그램**:
- 낮은 주가: bond floor 근처 (채권처럼)
- 높은 주가: conversion value 근처 (주식처럼)
- 중간: option premium

</details>

### Q3. *왜 convertible 발행* (올바른 이유)?

<details><summary>답</summary>

**Free lunch 환상 (틀림)**:
- ~~낮은 coupon 싸게 차입~~ (전환권 대가)
- ~~높은 가격 주식 발행~~ (불확실)

**올바른 이유**:
1. **Backdoor equity** — 직접 SEO 어려운 성장기업, 주가↑ 시 전환
2. **Agency 완화** — risk-shifting (채권자도 upside), asset substitution 감소
3. **Info asymmetry** — 채권자-주주 valuation 차이 좁힘
4. **Cash 절약** — 낮은 coupon (성장기)

**발행 기업**: 고성장+고위험 (Tesla, Twitter, Netflix), 변동성 ↑ → 전환권 가치 ↑.

</details>

### Q4. 계산 — Convertible 의 3 가치

채권: par $1,000, conversion ratio 20주, 주가 $40, comparable straight yield 8%, coupon 4%, 만기 5년.

(a) Conversion value?
(b) Bond floor (straight value)?
(c) 어느 게 binding?

<details><summary>답</summary>

**(a) Conversion value**:
- = ratio × 주가 = 20 × $40 = **$800**

**(b) Bond floor (straight bond value)**:
- Coupon $40/year (4% of $1,000), 만기 par $1,000, discount at 8%
- $= 40 \times PVIFA(8\%, 5) + 1000 \times PVIF(8\%, 5)$
- $= 40 \times 3.993 + 1000 \times 0.681$
- $= 159.7 + 681 = \$840.7$

**(c) Binding floor**:
- Bond floor $840.7 > Conversion value $800
- → *Bond floor* 가 binding (현재 주가 낮음)
- Convertible 은 *채권처럼* 거래 (+ option premium)
- 시장가 = max($840.7, $800) + premium ≈ $850-900

**해석**:
- 주가 $40 → 전환 안 함 (전환 시 $800 < bond $840)
- 주가 상승 시 → conversion value 가 binding 으로 전환

</details>

### Q5. 계산 — Conversion price + premium

채권: par $1,000, conversion ratio 25주.

(a) Conversion price?
(b) 현재 convertible 시장가 $1,100, 주가 $38 → conversion premium?

<details><summary>답</summary>

**(a) Conversion price**:
$$= \frac{\text{Par}}{\text{Conversion ratio}} = \frac{1000}{25} = \$40$$

→ 주가 $40 도달 시 전환 가치 = par.

**(b) Conversion premium**:
- Conversion value = 25 × $38 = $950
- Convertible price = $1,100
$$\text{Premium} = \frac{1100 - 950}{950} = \frac{150}{950} = 15.8\%$$

**해석**:
- 전환가치($950) 대비 *15.8% 비싸게* 거래
- 이유: bond floor (downside 보호) + option time value
- 주가 $38 < conversion price $40 → 약간 OTM

</details>

### Q6. 계산 — Warrant dilution

회사: 기존 100만주, 주가 $50 (firm value $50M). Warrant 20만개 발행 (strike $50). 모두 행사 시.

(a) Warrant 행사 후 주식 수?
(b) 행사로 유입 cash?
(c) Dilution factor?

<details><summary>답</summary>

**(a) 행사 후 주식 수**:
- 100만 + 20만 = **120만주**

**(b) 유입 cash**:
- 20만 × $50 (strike) = **$10M**

**(c) Dilution factor**:
$$\frac{n}{n + n_w} = \frac{100만}{120만} = 0.833$$

**행사 후 주가 (단순)**:
- 새 firm value = $50M + $10M (cash) = $60M
- 주식 수 120만
- 주가 = $60M / 120만 = **$50** (strike = 현재가, ATM 이므로 불변)

**Warrant 가치 (ITM 예)**:
- 만약 주가 $70 (행사 전):
- 행사 후 firm = $70M + $10M = $80M, 120만주 → $66.67
- Warrant payoff = $66.67 − $50 = $16.67 (call 의 $20 보다 낮음 = dilution)
- = 0.833 × $20 = $16.67 ✓

→ Dilution 으로 call 대비 가치 83.3%.

</details>

### Q7. 디버그 — "Convertible 은 싼 자금 조달"

CFO: *"Convertible 은 coupon 4% 로 일반 채권 8% 보다 훨씬 싸다! 자금 조달 비용 절반!"*

오류?

<details><summary>답</summary>

**오류 — Free lunch 환상**:

**1. 전환권 대가**:
- Coupon 4% (vs 8%) 의 *차이 4%* = *전환권 가치* 의 대가
- 투자자는 *낮은 coupon 을 받는 대신 전환권* 획득

**2. Dilution 비용**:
- 주가 상승 시 *전환* → 기존 주주 *희석*
- 상승 잠재력의 일부를 채권자에 양도

**3. 진짜 비용 (분해)**:
- Convertible = straight bond + call (전환권)
- 옵션 가치 포함하면 실질 비용은 8% 와 유사

**올바른 관점**:
- Implied cost 는 4% 와 8% 사이
- 주가 상승 (전환) → equity 비용 (높음)
- 주가 하락 (미전환) → 4% 채권 (낮음)
- → 상태 의존적

**유명**: Tesla 여러 차례 (성장기 cash + 낮은 coupon), 주가 급등 → 전환 (운 좋은 경우). 사전적으로는 free lunch 아님.

→ Coupon 4% < 8% 차이 = 전환권 대가 + dilution. 진짜 비용 4-8% 사이.

</details>

### Q8. 디버그 — Forced conversion 타이밍

회사 callable convertible (call price $1,050). 주가 상승 → conversion value $1,200. 회사가 즉시 call 안 하고 6개월 기다림.

이론 vs 실무?

<details><summary>답</summary>

**이론 (최적 call)**:
- Conversion value > call price 즉시 → call
- 회사: coupon 부담 제거 + 부채→자본

**실무 (지연)**:

**왜 지연**:
1. Safety margin (주가 변동 위험)
2. Signaling (call = 부정 신호 가능)
3. Notice period (30일, 그 사이 변동)
4. Coupon < dividend 면 지연 유리
5. 경영진 inertia

**Ingersoll (1977)**:
- 실무 call 지연 (conversion value 가 call price 의 *44% 초과* 시 call)
- 이론 (즉시) 과 괴리

**Bondholder**: call 안 하면 coupon 계속 + upside 유지 (bondholder 유리).

**현대**: soft call (주가 조건부), make-whole premium.

→ 이론: 즉시. 실무: 지연. Ingersoll 44% 초과.

</details>

### Q9. 면접 — *왜 성장 기업이 convertible 선호*?

<details><summary>답</summary>

**1. Backdoor equity (핵심)**:
- 직접 SEO → −3% (Myers-Majluf)
- 고평가 우려 신호 회피
- 주가↑ 시 자동 전환 = 지연된 equity ("equity at a premium")

**2. Cash flow 절약**: 성장기 cash 부족, 낮은 coupon.

**3. Agency 완화**: risk-shifting (변동성 높음), 채권자도 upside → asset substitution 감소.

**4. Info asymmetry**: 채권자-주주 valuation 차이 좁힘 (debt+equity 혼합).

**5. 변동성 = 전환권 가치**: 높은 변동성 → call 가치 ↑ → 낮은 coupon 수용.

**전형**: Tesla, Twitter, Netflix, Uber, biotech.

**대조**: 성숙 안정 (utility) → straight bond. Apple → debt/buyback.

**위험**: 전환 안 됨 (주가↓) → 부채 부담. 과도 발행 → dilution overhang.

> 성장기업 convertible = backdoor equity + cash 절약 + agency 완화 + 변동성 전환권. Free lunch 아님.

</details>

### Q10. 면접 — *Convertible arbitrage + 2008 교훈*?

<details><summary>답</summary>

**구조**: Convertible 매수 (long) + 주식 공매도 (short, delta hedge). Option 가치 포착, 주가 방향 중립.

**수익원**: convertible 저평가, coupon carry, 공매도 rebate, gamma trading.

**위험**: credit (부도), liquidity (얇은 시장), volatility (IV↓), leverage.

**2008 교훈**:
- Convertible arb 펀드 대규모 leverage (5-10x)
- 2008 9-10월: prime broker (Lehman) 붕괴 → 자금 회수, 공매도 금지 (financial), deleveraging 강제
- → convertible 투매 → 폭락 (index −35%)

**교훈**:
1. Leverage 위험 (deleveraging spiral)
2. Funding liquidity (prime broker 의존)
3. Short-selling 규제 위험
4. Crowded trade (동시 exit)
5. Correlation breakdown (hedge 작동 안 함)

**회복**: 2009 +40% (저평가 반등).

**현대**: lower leverage, diversified financing.

**철학적**: fat tails (2008 = 정규분포 밖), liquidity 환상, leverage 양날, correlation = 1 in crisis.

> Convertible arb = 매수 + 공매도 (delta hedge). 2008: leverage + funding + 공매도 규제 + crowded → spiral (−35%). 현대: lower leverage.

</details>
