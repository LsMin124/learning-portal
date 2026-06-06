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

## §0 도입 — *유휴 현금과의 싸움*

> **핵심 한 문장**: 현금은 수익을 못 내는 자산이라 "*필요한 만큼만, 그러나 부족하지 않게*" 들고 있어야 한다 — 26장이 운전자본 전체를 봤다면 27장은 그중 **현금 자체** 의 보유·회수·지급·투자를 정밀하게 다룬다.

현금 관리는 다섯 갈래다:

1. **왜 들고 있나** (§1): 일상 결제(transaction)·예비(precautionary)·기회(speculative) — 세 동기. 다만 현금은 *기회비용* 이 크므로 과다 보유는 손해.
2. **float — 장부와 은행의 시차** (§2): 수표가 처리되는 동안 *장부 잔액 ≠ 은행 가용 잔액*. 발행한 수표가 아직 안 빠진 *disbursement float*(우리에게 유리, figure 27.1 의 누적)와, 받은 수표가 아직 안 들어온 *collection float*(불리). float 를 없애면 잔액이 곧장 0 으로 떨어진다(figure 27.2).
3. **수금은 빠르게, 지급은 늦게** (§3–4): *lockbox*(고객이 지역 사서함에 직접 송금 → 은행이 수거, figure 27.3)와 *concentration bank*(figure 27.4)로 수금을 가속하고, *ZBA*(잔액 0 유지, figure 27.5)로 유휴 현금을 줄인다.
4. **목표 잔액** (§5–6): 현금흐름이 *일정* 하면 EOQ 형 *Baumol*($C^*=\sqrt{2TF/K}$), *랜덤* 이면 *Miller-Orr*(상·하한·목표). 변동성이 클수록 범위가 넓어진다.
5. **남는 현금은 굴린다** (§7): 임시 잉여(계절, figure 27.6)는 T-bill·CD·MMF 같은 *money market* 에 — 유동·안전·낮은 수익. 영구 잉여는 배당/buyback(19장).

한 문장으로: **현금 관리는 float 를 내 편으로 만들고, 목표 잔액을 지키며, 남는 건 안전하게 굴리는 일이다.**

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

![Figure 27.1 — Buildup of the Float. 교재 p.831](/courses/financial-management/figures/ch27/fig-27-1.png)

> **직관**: *disbursement float* 가 쌓이는 모습. 매일 $1,000 짜리 수표를 받지만(checks received) 인출(cash available)은 며칠 늦으므로 ending float 가 $1,000→$2,000→$3,000 으로 쌓이다 안정된다. 이 시차만큼 *은행 잔액이 장부보다 많아* 우리에게 유리하다.

![Figure 27.2 — Effect of Eliminating the Float. 교재 p.831](/courses/financial-management/figures/ch27/fig-27-2.png)

> **직관**: 그 float 를 *없애면*. 첫날 누적 float($3,000)이 한꺼번에 인출되며(−$4,000) ending float 가 0 으로 떨어지고, 이후 매일 받는 만큼 매일 빠져 *항상 0*. float 가 사라지면 장부=은행 — '현금이 더 있는 것처럼' 쓰던 여유가 없어진다.

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

![Figure 27.3 — Overview of Lockbox Processing. 교재 p.835](/courses/financial-management/figures/ch27/fig-27-3.png)

> **직관**: *lockbox* 의 흐름. 고객이 대금을 본사가 아닌 *지역 사서함* 으로 보내면(여러 Customer payments → Post office box), 은행이 하루에도 여러 번 직접 수거해 곧장 계좌에 넣는다. 우편·사내처리 시간이 빠져 *collection float ↓* — 수금 가속의 핵심 도구.

![Figure 27.4 — Lockboxes and Concentration Banks in a Cash Management System. 교재 p.836](/courses/financial-management/figures/ch27/fig-27-4.png)

> **직관**: lockbox 위에 *concentration bank* 를 얹은 전체 그림. 여러 지역의 lockbox·local bank 자금을 *집중 계좌* 하나로 모으고, firm cash manager 가 거기서 현금 준비·지급·단기투자·보상예금을 한꺼번에 관리한다. 분산된 잔액을 통합해 유휴 현금을 줄인다.

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

![Figure 27.5 — Zero-Balance Accounts. 교재 p.839](/courses/financial-management/figures/ch27/fig-27-5.png)

> **직관**: *ZBA(잔액 0 계좌)* 의 효과. 왼쪽(ZBA 없음): 급여·지급 계좌마다 *각각 안전재고* 현금을 깔아둬 돈이 묶인다. 오른쪽(ZBA): *master account* 하나에만 안전재고를 두고, 수표가 결제될 때만 자금을 흘려보낸다 — 유휴 현금을 한 곳으로 모아 최소화.

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

![Figure 27.6 — Seasonal Cash Demands. 교재 p.840](/courses/financial-management/figures/ch27/fig-27-6.png)

> **직관**: *계절적* 현금 수요와 투자. 총자금 수요(물결)가 장기 자금(직선) 위로 솟는 구간은 *bank loans*(단기차입)로, 아래로 내려가 *남는* 구간은 *marketable securities* 매수로 굴린다. 임시 잉여를 money market 에 넣었다 필요할 때 빼는 전형.

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
