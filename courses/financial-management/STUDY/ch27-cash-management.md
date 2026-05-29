# Chapter 27: Cash Management — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 27** (책 p.839~862).
> 27장은 *현금 관리* — 보유 동기, float, 수금/지급, 목표잔액 모형.

이 장의 *지적 무게중심*:
1. **현금 보유 동기** — transaction, precautionary, speculative
2. **Float** — collection / disbursement / net
3. **수금·지급 관리** — lockbox, concentration, ZBA
4. **목표 현금잔액** — Baumol, Miller-Orr
5. **유휴 현금 투자** — money market

---

## §1 현금 보유 동기

### §1.1 세 가지 동기 (Keynes)

| 동기 | 의미 |
|--|--|
| *Transaction* | 일상 결제 (급여, 매입) |
| *Precautionary* | 예비 (불확실 대비) |
| *Speculative* | 기회 (인수, 투자) |

### §1.2 추가 이유

- *Compensating balance* — 은행 보상예금
- *Tax* — 해외 현금 (송금 시 과세, 과거 미국)

### §1.3 현금 보유 비용

- *기회비용* — 현금은 낮은 수익 (유휴)
- → 너무 많이 보유 ↔ 너무 적게 보유 trade-off

---

## §2 Float (플로트)

### §2.1 정의

> *장부 잔액*과 *은행 가용 잔액*의 차이 (수표 처리 시차).

$$\text{Float} = \text{은행 잔액} - \text{장부 잔액}$$

### §2.2 종류

**Disbursement float (지급 플로트, +)**:
- 우리가 수표 발행 → 아직 인출 안 됨
- 장부 < 은행 (우리에게 *유리*)

**Collection float (수금 플로트, −)**:
- 우리가 수표 수취 → 아직 입금 안 됨
- 장부 > 은행 (우리에게 *불리*)

**Net float**:
$$\text{Net float} = \text{Disbursement float} - \text{Collection float}$$

### §2.3 Float 관리 목표

- *Collection float ↓* — 수금 가속 (빨리 쓸 수 있게)
- *Disbursement float ↑* — 지급 지연 (가능한 오래 보유)
- → Net float 극대화

---

## §3 수금 (Collection) 가속

### §3.1 Float 구성

| 단계 | Float |
|--|--|
| *Mailing* | 우편 시간 |
| *Processing* | 사내 처리 |
| *Availability* | 은행 결제 |

### §3.2 수금 도구

**Lockbox (사서함)**:
- 고객이 *지역 사서함*에 직접 송금
- 은행이 직접 수거·처리 → mailing + processing float ↓

**Concentration banking (집중)**:
- 지역 은행 → *집중 계좌*로 자금 이동
- 잉여자금 통합 관리

### §3.3 전자 수금

- *Wire transfer*, *ACH*, *EDI*
- Float ≈ 0 (즉시)

---

## §4 지급 (Disbursement) 관리

### §4.1 지급 지연 (float 활용)

**Controlled disbursement**:
- *원거리 은행* 사용 → 결제 지연
- (윤리·규제 논란)

**Zero-balance account (ZBA)**:
- 잔액 0 유지 → 수표 결제 시점에만 자금 이동
- 유휴 현금 ↓

### §4.2 윤리/현실

- 과도한 disbursement float = *"playing the float"* (논란)
- 전자결제 확산 → float 축소
- *Check 21 Act* (2004) — 수표 전자처리, float ↓

---

## §5 목표 현금잔액 — Baumol Model

### §5.1 개념

> *EOQ (경제적 주문량)* 를 현금에 적용.

- 현금 소진 → 증권 매도로 보충
- *Trade-off*: 거래비용 vs 기회비용

### §5.2 공식

$$C^* = \sqrt{\frac{2 \times T \times F}{K}}$$

- $T$ = 기간 총 현금 수요
- $F$ = 거래당 고정비용 (증권 매매)
- $K$ = 기회비용 (이자율)
- $C^*$ = 최적 거래(인출) 규모

### §5.3 평균 현금잔액

$$\text{평균 현금} = \frac{C^*}{2}$$

### §5.4 가정 (한계)

- *일정한* 현금 유출 (현실 비현실적)
- 유입 무시
- → Miller-Orr 가 보완

---

## §6 목표 현금잔액 — Miller-Orr Model

### §6.1 개념

> 현금흐름이 *불확실(랜덤)* 할 때.

- *상한 (H)*, *하한 (L)*, *목표 (Z)* 설정
- 상한 도달 → 증권 매입 (현금 ↓)
- 하한 도달 → 증권 매도 (현금 ↑)
- 범위 내 → 방치

### §6.2 공식

**목표 잔액 (return point)**:
$$Z^* = \sqrt[3]{\frac{3 F \sigma^2}{4K}} + L$$

**상한**:
$$H^* = 3Z^* - 2L$$

**평균 현금잔액**:
$$\text{평균} = \frac{4Z^* - L}{3}$$

- $\sigma^2$ = 일일 현금흐름 분산
- $F$ = 거래비용, $K$ = 일일 기회비용

### §6.3 직관

- 변동성 $\sigma^2$ ↑ → 범위 넓음 (Z, H ↑)
- 거래비용 $F$ ↑ → 범위 넓음 (덜 자주 거래)
- 이자율 $K$ ↑ → 범위 좁음 (현금 보유 비용 ↑)

---

## §7 유휴 현금 투자 (Money Market)

### §7.1 단기 투자 수단

| 수단 | 특징 |
|--|--|
| *T-bill* | 국채 (무위험, 유동) |
| *CD* | 양도성예금증서 |
| *Commercial paper* | 기업 단기 어음 |
| *Repo* | 환매조건부채권 |
| *MMF* | 머니마켓펀드 |
| *Banker's acceptance* | 무역금융 |

### §7.2 선택 기준

1. *유동성* (즉시 현금화)
2. *안전성* (원금 보전)
3. *수익성* (낮지만 양수)
4. *만기 매칭* (필요 시점)

### §7.3 임시 vs 영구 잉여

- *임시 잉여* (계절) → money market 투자
- *영구 잉여* → 배당/buyback, 투자, 부채상환 (Ch 19)

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Float = 장부 오류 | 처리 시차 (정상) |
| 2 | Disbursement float 나쁨 | 우리에게 유리 (지급 지연) |
| 3 | Collection float 좋음 | 불리 (수금 지연) |
| 4 | Baumol = 불확실 현금흐름 | 일정 유출 가정 (Miller-Orr 가 랜덤) |
| 5 | 현금 많을수록 안전 | 기회비용 (유휴) |
| 6 | 유휴현금 = 장기 투자 | Money market (유동·안전) |
| 7 | Float 무한 활용 | 전자결제·규제로 축소 |

---

## §9 자가점검

1. 현금 보유 *3 동기*?
2. *Float* 정의 + collection/disbursement?
3. *Lockbox* / *ZBA* 목적?
4. *Baumol model* 공식 + 가정?
5. *Miller-Orr* 와 Baumol 차이?
6. 유휴 현금 투자 수단?

<details><summary>해답</summary>

1. Transaction (결제), precautionary (예비), speculative (기회). + compensating balance.
2. Float = 은행잔액 − 장부잔액 (처리 시차). Disbursement(+, 유리, 지급지연), collection(−, 불리, 수금지연).
3. Lockbox: 고객 직접 송금 → mailing/processing float ↓ (수금 가속). ZBA: 잔액 0 → 결제 시점 자금이동 (유휴↓).
4. C* = √(2TF/K). 가정: 일정한 현금 유출, 유입 무시.
5. Baumol: 일정 유출 (EOQ). Miller-Orr: 랜덤 현금흐름, 상한/하한/목표 (Z*=∛(3Fσ²/4K)+L).
6. T-bill, CD, CP, repo, MMF, banker's acceptance (유동·안전·낮은 수익).

</details>

---

## §10 다음 학습으로

- **Ch 28** — Credit and inventory (AR/재고 정책)
- **Ch 26** — 단기 재무 (운전자본, cash budget)
- **Ch 19** — 영구 잉여 (배당/buyback)

---

## §11 한 줄 요약

> **현금 관리. *보유 동기*: transaction/precautionary/speculative (+compensating balance). *Float* = 은행−장부 (처리시차): disbursement(+유리, 지급지연), collection(−불리, 수금가속). *수금*: lockbox(float↓), concentration. *지급*: ZBA, controlled disbursement. *목표잔액*: Baumol C*=√(2TF/K) (일정유출, EOQ) vs Miller-Orr Z*=∛(3Fσ²/4K)+L (랜덤, 상/하한). *유휴현금*: money market (T-bill/CD/CP/MMF, 유동·안전).**
