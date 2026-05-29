# Ch 25 Derivatives and Hedging — 치트시트

> Forward/Futures / Hedge / Basis / Duration / Swap / 왜 헤징.

## §1 Forward vs Futures

| | Forward | Futures |
|--|--|--|
| 거래 | OTC | 거래소 |
| 표준 | 맞춤 | 표준 |
| 정산 | 만기 | 일일 (M2M) |
| Counterparty | 있음 | Clearinghouse |
| 유동성 | 낮음 | 높음 |

## §2 Forward payoff

$$\text{Long} = S_T - F, \quad \text{Short} = F - S_T$$

(대칭, linear)

## §3 Marking to Market

- 매일 손익 현금 정산
- Margin < maintenance → margin call
- → 부도 위험 ↓

## §4 Hedge 방향

| 노출 | Hedge |
|--|--|
| 자산 보유/생산 | Short (futures 매도) |
| 미래 매입 예정 | Long (futures 매수) |

## §5 Hedge 예시

| 주체 | Hedge |
|--|--|
| 농부 (밀) | Short |
| 항공사 (연료) | Long |
| 정유사 (재고) | Short |
| 제빵사 (밀 매입) | Long |

## §6 Hedging vs Speculation

| | Hedge | Speculation |
|--|--|--|
| 노출 | 기존 상쇄 | 신규 생성 |
| 목적 | 위험 ↓ | 수익 (위험 부담) |

## §7 Basis Risk

$$\text{Basis} = \text{Spot} - \text{Futures}$$

- 만기 → 0 수렴
- 원천: asset/maturity/quantity mismatch
- Cross hedge → basis risk ↑

## §8 Duration (복습)

$$\frac{\Delta P}{P} \approx -D \times \frac{\Delta y}{1+y}$$

(금리 민감도)

## §9 Duration Gap / 면역

$$DG = D_A - D_L \times \frac{L}{A}$$

- DG = 0 → immunization
- 금리 변동에도 순자산 불변

## §10 Duration hedge 비율

$$N = \frac{D_P \times P}{D_F \times F}$$

(T-bond futures 로 조정)

## §11 Interest Rate Swap

- 고정 ↔ 변동 교환
- *원금 교환 X* (이자만)
- Comparative advantage 활용

## §12 Swap 총이득

$$\text{Gain} = |\Delta_{\text{고정}}| - |\Delta_{\text{변동}}|$$

(두 기업 차입조건 차이)

## §13 Currency Swap

- 다른 통화 *원리금* 교환
- 원금 교환 O (시작+만기)
- 환위험 + 금리위험

## §14 Options 헤지

| | Futures | Options |
|--|--|--|
| Payoff | 대칭 | 비대칭 |
| 비용 | 0 | Premium |
| Upside | 포기 | 유지 |

## §15 Cap / Floor / Collar

| 도구 | 구조 | 목적 |
|--|--|--|
| Cap | 금리 call 매수 | 상한 (차입자) |
| Floor | 금리 put 매수 | 하한 (대출자) |
| Collar | cap 매수 + floor 매도 | premium 절감 |

## §16 왜 헤징 (M&M 불완전성)

1. Financial distress 비용 ↓
2. Tax convexity (Jensen)
3. 부채여력 ↑
4. 과소투자 회피 (FSS)
5. 경영진 위험회피

→ 완전시장: 무관 (주주 분산).

## §17 Hedge 재앙

| 사례 | 교훈 |
|--|--|
| Metallgesellschaft | Maturity mismatch + margin call |
| Barings | 무단 투기 |
| P&G | Leveraged swap |
| Orange County | Repo leverage |
| Amaranth | 천연가스 투기 ($6B) |
| AIG (2008) | CDS 무담보 매도 |

## §18 자주 함정

| 함정 | 정정 |
|--|--|
| Forward = Futures | M2M, counterparty 차이 |
| 완전 헤지 항상 | Basis risk |
| 헤징 = 항상 이득 | M&M (완전시장 무관) |
| 금리스왑 원금 교환 | 이자만 |
| 옵션 헤지 무료 | Premium |
| Futures upside 유지 | 대칭 (포기) |

## §19 핵심 mindmap

```
Derivatives & Hedging
├── Forward (OTC, 만기) / Futures (거래소, M2M)
├── Hedge (short/long, basis risk)
├── Duration hedge (gap=0 면역)
├── Swap (금리: 이자만 / 통화: 원리금)
├── Options (cap/floor/collar, 비대칭)
└── 왜 헤징 (distress/tax/부채여력, M&M)
```

## §20 1-line summary

> **Forward (OTC, 만기정산) vs Futures (거래소, mark-to-market, clearinghouse). Hedge = 반대 포지션 (short: 보유→매도, long: 매입→매수), basis risk (mismatch) 잔존. Duration hedge: gap=0 → 금리 면역. Swap: 금리(고정↔변동, 이자만) / 통화(원리금). Options(cap/floor/collar) = 비대칭(premium, upside 유지). 왜 헤징: distress↓+tax convexity+부채여력+과소투자 회피 (M&M: 완전시장 무관). 재앙: Metallgesellschaft(maturity mismatch), Barings, AIG.**
