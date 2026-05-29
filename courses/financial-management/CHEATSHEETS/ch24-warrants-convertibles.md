# Ch 24 Warrants and Convertibles — 치트시트

> Warrant / Convertible / 3 floor / 발행 이유 / Arbitrage.

## §1 Warrant vs Call

| | Call | Warrant |
|--|--|--|
| 발행자 | 거래소 | 회사 |
| 행사 | 기존 주식 | 신주 (dilution) |
| Cash | 무관 | 행사가 수취 |
| 만기 | 단기 | 장기 |

## §2 Warrant dilution

$$W = \frac{n}{n + n_w} \times \text{Call value}$$

→ Dilution factor = n/(n+n_w).

## §3 Convertible 3 가치

| 가치 | 의미 |
|--|--|
| Bond floor | Straight bond (하한) |
| Conversion value | ratio × 주가 |
| Convertible | max(floor, conversion) + premium |

## §4 Conversion 공식

| | 공식 |
|--|--|
| Conversion price | Par / ratio |
| Conversion value | ratio × 주가 |
| Conversion premium | (Conv price − Conv value)/Conv value |

## §5 Convertible 분해

$$\text{Convertible} = \text{Straight bond} + \text{Call option}$$

## §6 왜 발행 (올바른 이유)

1. Backdoor equity (지연 주식 발행)
2. Agency 완화 (risk-shifting)
3. Info asymmetry
4. Cash 절약 (낮은 coupon)

→ Free lunch 아님 (전환권 대가).

## §7 발행 기업 특성

- 고성장 + 고위험, 변동성 ↑ → 전환권 가치 ↑
- Tesla, Twitter, Netflix, biotech

## §8 Forced Conversion

- Callable + 주가↑ → 강제 전환 (부채→자본)
- 이론: 즉시. 실무: 지연 (Ingersoll 44%)

## §9 Convertible 종류

| 종류 | 특징 |
|--|--|
| Standard | 선택권 |
| Mandatory | 강제 전환 (equity-like) |
| CoCo | 자본비율 조건 (Basel III) |
| Convertible preferred | VC 표준 |

## §10 Convertible Arbitrage

- Convertible 매수 + 주식 공매도 (delta hedge)
- 위험: credit, liquidity, leverage
- 2008: leverage spiral → index −35% (2009 +40% 반등)

## §11 자주 함정

| 함정 | 정정 |
|--|--|
| Warrant = call | Dilution (신주) |
| Convertible = 싼 차입 | 전환권 대가 |
| Value = bond floor | + premium |
| Forced conversion 즉시 | 실무 지연 |
| 낮은 coupon = 이득 | 전환권 반영 |

## §12 핵심 mindmap

```
Warrants & Convertibles
├── Warrant (회사 발행 call, dilution)
├── Convertible (3 floor, = bond + call)
├── 발행 이유 (backdoor equity, agency)
├── Forced conversion (Ingersoll 44%)
└── Arbitrage (delta hedge, 2008 교훈)
```

## §13 1-line summary

> **Warrant = 회사 발행 long-term call (신주 dilution, n/(n+n_w)). *Convertible* = straight bond + conversion option, 3 가치 (bond floor/conversion/max+premium). *왜 발행*: backdoor equity + agency 완화 + cash 절약 (free lunch 아님). *Forced conversion* (callable, Ingersoll 44%). *Arbitrage* (매수+공매도, 2008 −35%).**
