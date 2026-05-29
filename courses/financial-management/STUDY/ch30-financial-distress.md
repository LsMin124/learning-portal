# Chapter 30: Financial Distress — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 30** (책 p.933~952).
> 30장은 *재무적 곤경* — 정의, 청산 vs 회생, 파산 절차, APR.

이 장의 *지적 무게중심*:
1. **재무적 곤경 정의** — 4 가지 의미
2. **재무 vs 경제적 곤경** — 회생 가능성
3. **청산 vs 회생** — Chapter 7 vs 11
4. **APR** — 절대우선순위
5. **Workout vs 파산** — 사적 vs 공식

---

## §1 재무적 곤경이란?

### §1.1 4 가지 정의

| 정의 | 의미 |
|--|--|
| *Business failure* | 사업 실패 (청산, 손실) |
| *Legal bankruptcy* | 법적 파산 신청 |
| *Technical insolvency* | 채무 불이행 (만기 미상환) |
| *Accounting insolvency* | 부채 > 자산 (negative equity) |

### §1.2 재무적 곤경 정의 (Ross)

> *현금흐름이 채무를 감당 못 함* → 약속 불이행.

- 강제 행동 필요 (채권자와)
- 자본구조 변경 유발

---

## §2 재무 곤경 vs 경제적 곤경

### §2.1 구분

| | 재무적 곤경 | 경제적 곤경 |
|--|--|--|
| 원인 | *과도한 부채* | *사업성 상실* |
| 자산 가치 | 양호 (운영 OK) | 훼손 |
| 해법 | *자본 재구성* | *청산* |

### §2.2 함의

- *재무적 곤경* → 회생 가치 (운영은 건전)
- *경제적 곤경* → 청산 (자원 재배치)
- 구분이 *청산 vs 회생* 결정의 핵심

---

## §3 곤경 대응 — 개요

### §3.1 선택지

```
재무적 곤경
├── 사적 해결 (Private workout)
│   ├── 부채 재조정 (만기/금리/원금)
│   ├── Debt-equity swap
│   └── 신규 자금
└── 공식 파산 (Bankruptcy)
    ├── Chapter 7 (청산)
    └── Chapter 11 (회생)
```

### §3.2 자산 매각/재구성

- 자산 매각 (divestiture)
- 부채 재조정
- 경영진 교체

---

## §4 청산 — Chapter 7

### §4.1 청산 (Liquidation)

> 자산 *매각* → 채권자 분배 → 기업 소멸.

- 회생 불가 (경제적 곤경)
- Trustee (관재인) 가 자산 매각

### §4.2 절차

1. 파산 신청 (자발적/비자발적)
2. Trustee 선임
3. 자산 매각
4. *APR* 에 따라 분배

---

## §5 절대우선순위 (APR)

### §5.1 분배 순위

> *Absolute Priority Rule* — 청산 시 변제 순서.

| 순위 | 청구권 |
|--|--|
| 1 | *담보 채권* (secured) |
| 2 | 파산 관리 비용 (admin) |
| 3 | 파산 후 발생 비용 |
| 4 | 임금 (한도) |
| 5 | 연금, 세금 |
| 6 | *무담보 채권* (unsecured) |
| 7 | *우선주* |
| 8 | *보통주* (잔여) |

### §5.2 핵심

- *상위 완전 변제 후* 하위 (절대적)
- 주주는 *최후* (잔여청구권)
- 실무에서 *위반* 빈번 (Ch 11 협상)

---

## §6 회생 — Chapter 11

### §6.1 회생 (Reorganization)

> 기업 *존속* → 부채 재조정 → 재기.

- 재무적 곤경 (운영 건전)
- 기존 경영진 *DIP* (debtor-in-possession) 유지 가능

### §6.2 절차

1. 파산 신청 → automatic stay (채권 추심 중지)
2. *DIP financing* (우선순위 신규 자금)
3. *회생 계획* (reorganization plan) 수립
4. 채권자 그룹별 투표
5. 법원 인가 (confirmation)
6. 부채 재조정 (debt → equity 등)

### §6.3 Cramdown

- 일부 채권자 반대해도 *법원 강제 인가*
- 조건: 공정·형평 (fair and equitable)

---

## §7 Workout vs 공식 파산

### §7.1 사적 정리 (Private Workout)

- 채권자와 *협상* (법원 밖)
- 빠르고 저렴
- *Holdout 문제* (무임승차, 소수 반대)

### §7.2 Prepackaged Bankruptcy

> 사전 합의 + Chapter 11 (하이브리드).

- 파산 신청 *전* 계획 합의
- 법원 인가로 holdout 해결
- 빠른 절차 (속도 + 강제력)

### §7.3 선택 기준

| | Workout | Chapter 11 |
|--|--|--|
| 비용 | 낮음 | 높음 |
| 속도 | 빠름 | 느림 |
| Holdout | 문제 | 해결 (강제) |
| 공개 | 비공개 | 공개 |

---

## §8 곤경 비용 + 예측

### §8.1 재무 곤경 비용 (Ch 17 복습)

**직접 비용**:
- 법률·회계·자문 수수료
- 시간·경영 주의 소모

**간접 비용** (더 큼):
- 매출 상실 (고객 이탈)
- 공급업체 신용 축소
- 핵심 인재 이탈
- Fire sale (헐값 매각)
- 과소투자/위험전가

### §8.2 파산 예측 — Altman Z-score

$$Z = 1.2X_1 + 1.4X_2 + 3.3X_3 + 0.6X_4 + 1.0X_5$$

| 변수 | 정의 |
|--|--|
| $X_1$ | 운전자본 / 총자산 |
| $X_2$ | 이익잉여금 / 총자산 |
| $X_3$ | EBIT / 총자산 |
| $X_4$ | 자기자본 시가 / 부채 장부가 |
| $X_5$ | 매출 / 총자산 |

- *Z < 1.81* → 위험 (부도 가능)
- *Z > 2.99* → 안전
- 1.81~2.99 → 회색지대

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 재무 곤경 = 경제적 곤경 | 부채 문제 vs 사업성 |
| 2 | 파산 = 청산 | Chapter 11 회생 가능 |
| 3 | APR 항상 준수 | 실무 위반 (Ch 11 협상) |
| 4 | 주주가 일부 먼저 | 최후 (잔여) |
| 5 | Workout 항상 우월 | Holdout 문제 |
| 6 | 곤경 비용 = 직접만 | 간접 (매출/인재) 더 큼 |
| 7 | Chapter 11 = 경영진 퇴출 | DIP 유지 가능 |

---

## §10 자가점검

1. 재무적 곤경 *4 정의*?
2. 재무 vs *경제적* 곤경?
3. Chapter 7 vs *Chapter 11*?
4. *APR* 순서?
5. *Workout* vs prepackaged?
6. Altman Z-score 의미?

<details><summary>해답</summary>

1. Business failure, legal bankruptcy, technical insolvency (불이행), accounting insolvency (부채>자산).
2. 재무: 과도한 부채 (운영 건전→회생). 경제적: 사업성 상실 (→청산).
3. Ch 7: 청산 (자산 매각, 소멸). Ch 11: 회생 (존속, 부채 재조정, DIP, cramdown).
4. 담보 → 관리비용 → 임금 → 세금 → 무담보 → 우선주 → 보통주 (최후).
5. Workout: 사적 협상 (저렴·빠름, holdout 문제). Prepackaged: 사전 합의 + Ch 11 (holdout 강제 해결).
6. Z = 1.2X₁+1.4X₂+3.3X₃+0.6X₄+1.0X₅. Z<1.81 위험, >2.99 안전.

</details>

---

## §11 다음 학습으로

- **Ch 17** — Financial distress 비용 (자본구조)
- **Ch 29** — LBO 후 곤경 위험
- **Ch 31** — 국제 파산 (다음, 마지막)

---

## §12 한 줄 요약

> **재무적 곤경. *정의*: business failure / legal bankruptcy / technical insolvency(불이행) / accounting insolvency(부채>자산). *재무 곤경*(과도한 부채, 운영 건전→회생) vs *경제적 곤경*(사업성 상실→청산). *Chapter 7* (청산, trustee, APR 분배) vs *Chapter 11* (회생, DIP, automatic stay, cramdown). *APR*: 담보→관리비용→임금→세금→무담보→우선주→보통주(최후). *Workout*(사적, holdout 문제) vs *prepackaged*(사전합의+Ch11). 곤경 비용: 직접<간접(매출/인재). 예측: Altman Z (Z<1.81 위험).**
