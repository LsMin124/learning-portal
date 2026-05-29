# Chapter 25: Derivatives and Hedging Risk — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 25** (책 p.781~810).
> 25장은 *파생상품 + 헤징* — forward/futures/swap/option 으로 위험 관리.

이 장의 *지적 무게중심*:
1. **Forward / Futures** — 미래 가격 고정
2. **Hedging** — short/long hedge, basis risk
3. **Duration hedging** — 금리 위험 면역
4. **Swaps** — 금리/통화 교환
5. **왜 헤징하는가** — financial distress, tax, 부채여력

---

## §1 Forward Contracts

### §1.1 정의

> *미래 특정일에 특정 가격으로 매매* 약정 (OTC, 맞춤형).

- *Forward price* — 계약 시 고정 가격
- 만기에만 정산 (no interim cash flow)
- *Counterparty risk* (상대방 부도 위험)
- OTC → 비표준 (수량/만기 자유)

### §1.2 Payoff

$$\text{Long forward payoff} = S_T - F$$

- $S_T$ = 만기 현물가, $F$ = forward price
- Long: 가격 상승 시 이익
- Short: 가격 하락 시 이익 (대칭, linear)

---

## §2 Futures Contracts

### §2.1 정의

> *표준화된 forward* (거래소 상장).

- *표준 수량/만기* (거래소 규격)
- *Clearinghouse* (중앙청산소) — counterparty risk 제거
- *Marking to market* (일일정산)
- *Margin* (증거금) — initial + maintenance

### §2.2 Marking to Market (일일정산)

> 매일 손익을 *현금으로 정산* → margin account 가감.

- 가격 변동분 매일 결제
- Margin < maintenance → *margin call*
- → 부도 위험 ↓ (누적 손실 방지)

### §2.3 Forward vs Futures

| | Forward | Futures |
|--|--|--|
| 거래 | OTC | 거래소 |
| 표준화 | 맞춤형 | 표준 |
| 정산 | 만기 | 일일 (mark-to-market) |
| Counterparty | 있음 | Clearinghouse (없음) |
| 유동성 | 낮음 | 높음 |
| 현금흐름 | 만기만 | 매일 |

→ 가격은 거의 같으나 (이자율 효과 제외), 현금흐름 시점 다름.

---

## §3 Hedging 기본

### §3.1 Hedge 개념

> *기존 노출의 반대 포지션* → 위험 상쇄.

- *Short hedge*: 자산 보유 → futures *매도* (가격 하락 방어)
- *Long hedge*: 미래 매입 예정 → futures *매수* (가격 상승 방어)

### §3.2 예시

| 상황 | Hedge |
|--|--|
| 농부 (밀 재배) | Short hedge (밀 futures 매도) |
| 제빵사 (밀 매입) | Long hedge (밀 futures 매수) |
| 항공사 (연료) | Long hedge (원유 매수) |
| 정유사 (원유 재고) | Short hedge (원유 매도) |

### §3.3 Hedging vs Speculation

| | Hedging | Speculation |
|--|--|--|
| 목적 | 위험 *감소* | 위험 *부담* (수익) |
| 노출 | 기존 노출 상쇄 | 신규 노출 생성 |
| 동기 | 안정 | 방향성 베팅 |

→ 같은 futures 라도 *기존 노출 유무*가 헤징/투기 구분.

---

## §4 Basis Risk

### §4.1 Basis 정의

$$\text{Basis} = \text{Spot price} - \text{Futures price}$$

- 만기에 basis → 0 (수렴, convergence)
- *완전 헤지는 드뭄* (basis 변동)

### §4.2 Basis Risk 원천

1. *Asset mismatch* — 헤지 대상 ≠ futures 기초자산 (cross hedge)
2. *Maturity mismatch* — 만기 불일치
3. *Quantity mismatch* — 수량 불일치

### §4.3 Cross Hedge

- 정확한 futures 없을 때 *유사 자산*으로 헤지
- 예: 제트연료 → 원유 futures
- → basis risk 증가 (상관 < 1)

---

## §5 Interest Rate Risk + Duration Hedging

### §5.1 금리 위험

- 채권 가격 = 금리 *역방향*
- 금융기관 (은행): 자산-부채 *duration mismatch*
- 금리 변동 → 순자산가치 변동

### §5.2 Duration (복습, Ch 8)

> 채권 가격의 *금리 민감도* (가중평균 만기).

$$\frac{\Delta P}{P} \approx -D \times \frac{\Delta y}{1+y}$$

- *Modified duration* = D/(1+y)
- Duration ↑ → 금리 민감도 ↑

### §5.3 Duration Hedging (면역)

> 자산-부채 *duration matching* → 금리 위험 면역(immunization).

- $D_{\text{asset}} \times \text{Asset} = D_{\text{liability}} \times \text{Liability}$
- *Duration gap* = 0 목표
- 금리 변동에도 순자산 불변

### §5.4 Interest Rate Futures

- T-bond/T-note futures 로 duration 조정
- 헤지 비율:
$$N = \frac{D_P \times P}{D_F \times F}$$
- $D_P$ = 포트폴리오 duration, $D_F$ = futures duration

---

## §6 Swaps

### §6.1 Interest Rate Swap (금리스왑)

> *고정금리 ↔ 변동금리* 교환.

- 한쪽: 고정금리 지급 / 변동금리 수취
- 다른쪽: 반대
- 원금(notional)은 교환 안 함 (이자만)
- *Comparative advantage* — 차입 우위 활용

### §6.2 금리스왑 예시

| | A 기업 | B 기업 |
|--|--|--|
| 고정 차입 | 10% | 12% |
| 변동 차입 | LIBOR | LIBOR+1.5% |
| 선호 | 변동 | 고정 |

→ A 고정 차입 + B 변동 차입 후 *swap* → 양쪽 이득 (comparative advantage).

### §6.3 Currency Swap (통화스왑)

> *서로 다른 통화의 원리금* 교환.

- 원금 교환 (시작 + 만기)
- 각 통화 이자 교환
- *환위험 + 금리위험* 동시 헤지
- 다국적 기업 자금조달

### §6.4 Swap 위험

- *Counterparty risk* (OTC) — 2008 이후 중앙청산(CCP) 의무화
- *Default* → swap 가치 손실

---

## §7 Options for Hedging

### §7.1 옵션 vs 선물 헤지

| | Futures/Forward | Options |
|--|--|--|
| Payoff | 대칭 (linear) | 비대칭 |
| 비용 | 0 (증거금만) | Premium 지급 |
| Downside | 차단 | 차단 |
| Upside | 포기 | *유지* |

→ 옵션은 *보험* (premium 대가로 upside 유지).

### §7.2 Caps / Floors / Collars

| 도구 | 구조 | 목적 |
|--|--|--|
| *Cap* | 금리 call 매수 | 금리 상한 (차입자) |
| *Floor* | 금리 put 매수 | 금리 하한 (대출자) |
| *Collar* | cap 매수 + floor 매도 | premium 절감 (범위) |

### §7.3 Protective Put (자산 보유)

- 자산 + put 매수 → downside 차단, upside 유지
- 비용 = premium

---

## §8 왜 기업이 헤징하는가?

### §8.1 M&M 역설

> 완전시장: 헤징 *무관* (주주가 직접 분산 가능).

- 그런데 기업은 *왜* 헤징? → 시장 불완전성

### §8.2 헤징의 진짜 이유

**1. Financial distress 비용 감소**:
- Cash flow 안정 → 부도 확률 ↓
- 직접/간접 distress 비용 회피 (Ch 17)

**2. Tax (convexity)**:
- 누진세 → 이익 변동성 ↓ → 기대세금 ↓ (Jensen 부등식)
- Tax shield 활용 안정화

**3. 부채여력 (debt capacity) 증가**:
- Cash flow 안정 → 더 많은 부채 가능 → tax shield ↑

**4. 과소투자 회피 (underinvestment)**:
- Cash flow 안정 → 내부자금 확보 → 좋은 NPV 투자 실행 (Froot-Scharfstein-Stein)

**5. 경영진 위험회피**:
- 경영진 인적자본/부 집중 → 위험회피적
- 헤징으로 개인 위험 ↓ (agency 측면)

### §8.3 헤징하지 말아야 할 때

- *주주가 더 잘 분산* (체계적 위험)
- 헤징 비용 > 편익
- *투기로 변질* 위험

---

## §9 Hedging 재앙 (실패 사례)

| 사례 | 교훈 |
|--|--|
| *Metallgesellschaft* (1993) | Rolling hedge + margin call → $1.3B 손실 (maturity mismatch) |
| *Barings* (1995) | Nick Leeson 무단 투기 (헤지 아닌 투기) |
| *P&G* (1994) | 복잡한 leveraged swap → $157M 손실 |
| *Orange County* (1994) | Reverse repo leverage → 파산 |
| *Amaranth* (2006) | 천연가스 투기 → $6B 손실 |
| *AIG* (2008) | CDS 무담보 매도 → 정부 구제 |

→ 공통: *헤지가 투기로 변질* + leverage + 감독 실패.

---

## §10 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Forward = Futures 동일 | Mark-to-market, counterparty 차이 |
| 2 | 완전 헤지 항상 가능 | Basis risk 존재 |
| 3 | Hedging = 항상 이득 | M&M: 완전시장 무관 |
| 4 | Swap 원금 교환 (금리스왑) | 이자만 (currency 는 원금도) |
| 5 | 옵션 헤지 = 무료 | Premium 지급 |
| 6 | Futures 헤지 = upside 유지 | 대칭 (upside 포기) |
| 7 | Duration gap 무시 | 면역 = duration matching |
| 8 | 헤징 = 투기 구분 모호 | 기존 노출 유무 |

---

## §11 자가점검

1. *Forward vs Futures* 차이?
2. *Short/Long hedge* 예시?
3. *Basis risk* 원천?
4. *Duration hedging* (면역)?
5. *Interest rate swap* vs *currency swap*?
6. *왜 기업이 헤징* (4가지 이상)?

<details><summary>해답</summary>

1. Forward: OTC, 맞춤형, 만기 정산, counterparty 위험. Futures: 거래소, 표준, 일일정산(mark-to-market), clearinghouse.
2. Short hedge: 자산 보유 → futures 매도 (농부). Long hedge: 미래 매입 → futures 매수 (항공사 연료).
3. Asset mismatch (cross hedge), maturity mismatch, quantity mismatch. 만기에 basis → 0 수렴.
4. 자산-부채 duration matching → duration gap 0 → 금리 변동에도 순자산 면역.
5. 금리스왑: 고정↔변동, 원금 교환 안 함 (이자만). 통화스왑: 다른 통화 원리금 교환 (원금도).
6. Financial distress 비용 ↓, tax convexity, 부채여력 ↑, 과소투자 회피, 경영진 위험회피.

</details>

---

## §12 다음 학습으로

- **Ch 26** — Short-term finance and planning
- **Ch 8** — Duration (복습)
- **Ch 22-23** — Options (헤징 도구)
- **Ch 31** — 환위험 헤징 (currency swap)

---

## §13 한 줄 요약

> **Derivatives = 위험 관리 도구. *Forward* (OTC, 만기정산) vs *Futures* (거래소, mark-to-market, clearinghouse). *Hedging*: short (자산보유→매도) / long (매입예정→매수), 단 *basis risk* (mismatch). *Duration hedging* = 자산-부채 duration matching (금리 면역). *Swap*: 금리(고정↔변동, 이자만) / 통화(원리금). *옵션 헤지* = 비대칭 (premium, upside 유지). *왜 헤징*: distress 비용↓ + tax convexity + 부채여력 + 과소투자 회피 (M&M: 완전시장 무관). 재앙: Metallgesellschaft, Barings, AIG (투기 변질).**
