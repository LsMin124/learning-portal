# Chapter 31: International Corporate Finance — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 31** (책 p.953~982).
> 31장은 *국제재무* — 환율, 평가관계(parity), 국제 자본예산, 환위험.

이 장의 *지적 무게중심*:
1. **환율 시장** — spot, forward, 표기
2. **4 평가관계** — PPP, IRP, UFR, IFE
3. **국제 자본예산** — 두 접근법
4. **환위험** — transaction/translation/economic
5. **정치적 위험** — 국가 위험

---

## §0 도입 — *환율이 더해진 재무*

> **핵심 한 문장**: 국제재무는 기업재무에 **환율** 이라는 변수를 더한다 — 환율·금리·물가는 *4개의 평가관계(parity)* 로 *무차익* 하에 서로 묶이고, 그 골격 위에서 국제 자본예산과 환위험·정치위험 관리가 펼쳐진다.

31장(전 과정의 마지막)은 다섯 층이다:

1. **환율 시장** (§1–2): spot/forward, direct/indirect 표기(figure 31.1 의 실제 시세표), cross-rate 와 삼각차익.
2. **4 평가관계** (§3–5) — 무차익이 묶는 네 끈: *PPP*(인플레 차이 → 환율 변화)·*IRP*(금리 차이 = forward premium)·*UFR*(forward = 기대 spot)·*IFE*(실질금리 국가 간 동일). 넷이 연결돼 금리·인플레·spot·forward 가 일관된다.
3. **국제 자본예산** (§6): *home currency*(외화 CF 를 환산 후 자국 할인율)와 *foreign currency*(외화 할인율 후 환산) — parity 가정 하 *같은 NPV*.
4. **환위험** (§7): *transaction*(확정 외화 결제)·*translation*(회계 환산)·*economic*(장기 경쟁력). 앞 둘은 forward/swap 으로, economic 은 *operational hedge*(생산 분산)로.
5. **정치적 위험** (§8): 국유화·송금 제한 → 현지 조달·합작·보험·할인율 가산.

한 문장으로: **국경을 넘으면 모든 현금흐름에 환율이 곱해지고, 그 환율은 금리·물가와 무차익으로 한 몸이다.**

---

## §1 국제재무 용어

### §1.1 핵심 용어

| 용어 | 의미 |
|--|--|
| *Foreign exchange (FX)* | 외환 |
| *Spot rate* | 현물 환율 |
| *Forward rate* | 선물 환율 |
| *Cross-rate* | 제3통화 교차환율 |
| *Eurocurrency* | 자국 밖 예치 통화 (eurodollar) |
| *ADR* | 미국 예탁증서 (외국주식) |
| *LIBOR* | 런던 은행간 금리 |

### §1.2 환율 표기

- *Direct* (직접): 자국통화/외국통화 ($1.20/€)
- *Indirect* (간접): 외국통화/자국통화 (€0.83/$)
- *Appreciation/Depreciation* (절상/절하)

---

![Figure 31.1 — Exchange Rate Quotations. 교재 p.938](/courses/financial-management/figures/ch31/fig-31-1.png)

> **직관**: *환율 시세표* 읽는 법. 각 통화에 대해 *USD equiv*(1단위가 몇 달러)와 *currency per USD*(1달러가 몇 단위)가 나란히 — 둘은 서로 역수다. 지역별(Americas·Europe·Asia-Pacific…)로 나열돼, 여기서 cross-rate 와 삼각차익(§2)이 계산된다. spot 시장의 출발점.

## §2 환율 + Triangle Arbitrage

### §2.1 Cross-rate

> 두 환율로 제3 환율 도출.

- 불일치 시 *triangular arbitrage* (삼각 차익)
- 시장이 cross-rate 일관성 강제

### §2.2 Spot vs Forward

- *Spot* — 즉시 (2영업일)
- *Forward* — 미래 약정
- *Forward premium/discount* — forward ≷ spot

---

## §3 평가관계 ① — Purchasing Power Parity (PPP)

### §3.1 절대적 PPP

> 일물일가 법칙 (law of one price).

$$S_0 = \frac{P_{\text{국내}}}{P_{\text{해외}}}$$

- 동일 재화 = 동일 가격 (환율 조정)
- 현실: 운송비, 관세, 비교역재 → 위반

### §3.2 상대적 PPP

> *물가상승률 차이* → 환율 변화.

$$E(S_t) = S_0 \times \left[\frac{1 + h_{\text{FC}}}{1 + h_{\text{US}}}\right]^t$$

- h = 인플레이션
- *고인플레 통화 → 절하*
- 근사: $\frac{E(S_1) - S_0}{S_0} \approx h_{FC} - h_{US}$

---

## §4 평가관계 ② — Interest Rate Parity (IRP)

### §4.1 Covered IRP

> *금리 차이* = *forward premium*.

$$\frac{F_0}{S_0} = \frac{1 + R_{\text{FC}}}{1 + R_{\text{US}}}$$

- *고금리 통화 → forward discount*
- Covered = forward 로 헤지 (무위험)
- 위반 시 *covered interest arbitrage*

### §4.2 근사

$$\frac{F_0 - S_0}{S_0} \approx R_{FC} - R_{US}$$

---

## §5 평가관계 ③④ — UFR + IFE

### §5.1 Unbiased Forward Rates (UFR)

> Forward = 미래 spot 의 *불편 추정치*.

$$F_0 = E(S_1)$$

- Forward 가 기대 환율 예측
- 위험 프리미엄 무시 가정

### §5.2 International Fisher Effect (IFE)

> *실질금리* 국가 간 동일.

$$R_{US} - h_{US} = R_{FC} - h_{FC}$$

- 명목금리 차이 = 인플레이션 차이
- $R_{FC} - R_{US} \approx h_{FC} - h_{US}$

### §5.3 4 관계 통합

```
        PPP
   (h차이→환율변화)
        │
IFE ────┼──── IRP
(금리=인플레)  (금리차=forward)
        │
       UFR
   (forward=E(spot))
```

- 네 관계가 *서로 연결* (no-arbitrage)
- 금리·인플레·spot·forward 가 일관

---

## §6 국제 자본예산

### §6.1 두 접근법

**1. Home Currency Approach (자국통화)**:
- 외화 CF → (forward/expected rate) 환산 → 자국통화
- 자국 할인율로 NPV

**2. Foreign Currency Approach (외국통화)**:
- 외화 CF → 외화 할인율 (IFE 조정) → NPV
- → spot 으로 자국통화 환산

### §6.2 일관성

- 두 접근법 *같은 NPV* (parity 가정 시)
- 외화 할인율 = 자국 할인율 + 금리차 (IFE)

### §6.3 송금 (remittance)

- 배당 송금, 세금, 환위험
- *Blocked funds* (송금 제한)

---

## §7 환위험 (Exchange Rate Risk)

### §7.1 세 가지 노출

| 노출 | 의미 |
|--|--|
| *Transaction* | 거래 (확정 외화 결제) |
| *Translation* | 환산 (회계, 재무제표) |
| *Economic* | 경제적 (장기 경쟁력) |

### §7.2 Transaction 노출 헤지

- *Forward/futures* 계약
- *Money market hedge* (차입+예치)
- *Currency option*
- *Currency swap* (Ch 25)

### §7.3 Economic 노출

- 장기·구조적 (가장 어려움)
- *Operational hedge* — 생산 분산, natural hedge
- 예: 해외 생산 (수익-비용 같은 통화)

---

## §8 정치적 위험 (Political Risk)

### §8.1 위험 유형

- *Expropriation* (국유화/몰수)
- 송금 제한, 세금 변경
- 규제, 계약 파기
- 전쟁, 불안정

### §8.2 대응

1. 현지 자금조달 (현지 부채)
2. 합작 (JV, 현지 파트너)
3. 정치 위험 보험 (OPIC/DFC)
4. 구조적 (핵심 기술 본국 보유)
5. 국가 위험 프리미엄 (할인율 ↑)

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 절대 PPP 항상 성립 | 운송비/관세 → 위반 (상대적이 현실) |
| 2 | 고금리 통화 = 좋은 투자 | Forward discount (IRP) |
| 3 | IRP vs PPP 혼동 | IRP=금리/forward, PPP=인플레/spot |
| 4 | 두 자본예산 접근 다른 NPV | 같음 (parity) |
| 5 | 환산(translation) = 현금 손실 | 회계상 (현금 아님) |
| 6 | Economic 노출 = forward 헤지 | Operational hedge 필요 |
| 7 | 정치 위험 무시 | 할인율/보험 반영 |

---

## §10 자가점검

1. *PPP* (절대/상대)?
2. *Covered IRP* 공식?
3. *IFE* 의미?
4. 4 평가관계 통합?
5. 국제 자본예산 두 접근법?
6. 환위험 *세 노출*?

<details><summary>해답</summary>

1. 절대 PPP: S = P국내/P해외 (일물일가). 상대 PPP: E(S_t) = S_0×[(1+h_FC)/(1+h_US)]^t (인플레 차이→환율).
2. F_0/S_0 = (1+R_FC)/(1+R_US). 금리차 = forward premium. 고금리→forward discount.
3. 실질금리 국가 간 동일 → 명목금리 차이 = 인플레 차이 (R_FC−R_US ≈ h_FC−h_US).
4. PPP(인플레-환율), IRP(금리-forward), UFR(forward=E(spot)), IFE(금리-인플레) → no-arbitrage 로 연결.
5. Home currency (외화CF→환산→자국 할인율) vs foreign currency (외화 할인율→환산). 같은 NPV.
6. Transaction (거래, 확정 외화), translation (회계 환산), economic (장기 경쟁력).

</details>

---

## §11 다음 학습으로

- **Ch 25** — Currency swap (환위험 헤지)
- **Ch 8** — 금리 (parity 연결)
- 🎉 **전 과정 완료** — Part I~VIII 31장

---

## §12 한 줄 요약

> **국제재무. *환율*: spot/forward, direct/indirect, cross-rate (triangular arb). *4 평가관계*: ①PPP (절대 S=P국내/P해외, 상대 E(S_t)=S_0[(1+h_FC)/(1+h_US)]^t) ②covered IRP (F/S=(1+R_FC)/(1+R_US), 금리차=forward) ③UFR (F=E(spot)) ④IFE (실질금리 동일, R차=h차) — no-arbitrage 로 연결. *국제 자본예산*: home vs foreign currency 접근 (같은 NPV). *환위험*: transaction(거래)·translation(회계)·economic(장기, operational hedge). *정치 위험*: 국유화/송금제한 → 현지조달·보험·할인율.**
