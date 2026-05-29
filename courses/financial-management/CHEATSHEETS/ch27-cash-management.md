# Ch 27 Cash Management — 치트시트

> 보유동기 / Float / 수금·지급 / Baumol / Miller-Orr / Money market.

## §1 현금 보유 동기 (Keynes)

| 동기 | 의미 |
|--|--|
| Transaction | 일상 결제 |
| Precautionary | 예비 (불확실) |
| Speculative | 기회 (M&A) |

+ compensating balance, 세금(해외).

## §2 Float 정의

$$\text{Float} = \text{은행잔액} - \text{장부잔액}$$

## §3 Float 종류

| | 부호 | 우리에게 |
|--|--|--|
| Disbursement (발행) | + | 유리 (지급지연) |
| Collection (수취) | − | 불리 (수금가속) |

$$\text{Net float} = \text{Disb} - \text{Coll}$$

## §4 Float 구성 (수금)

| 단계 | 내용 |
|--|--|
| Mailing | 우편 |
| Processing | 사내 |
| Availability | 은행 결제 |

## §5 수금 가속

| 도구 | 효과 |
|--|--|
| Lockbox | 고객 직접 송금 (mailing/processing↓) |
| Concentration | 집중 계좌 |
| Wire/ACH | float ≈ 0 |

## §6 지급 관리

| 도구 | 목적 |
|--|--|
| ZBA | 잔액 0 → 유휴↓ |
| Controlled disb | 결제 지연 (논란) |

## §7 Baumol Model

$$C^* = \sqrt{\frac{2TF}{K}}$$

- T=총수요, F=거래비용, K=이자율
- 평균 = C*/2
- 가정: *일정 유출* (EOQ)

## §8 Baumol trade-off

- 거래비용 (자주 인출) vs 기회비용 (현금 보유)
- 최적: 두 비용 같음

## §9 Miller-Orr Model

$$Z^* = \sqrt[3]{\frac{3F\sigma^2}{4K}} + L$$

$$H^* = 3Z^* - 2L$$

$$\text{평균} = \frac{4Z^* - L}{3}$$

- 랜덤 현금흐름, σ² = 일일 분산

## §10 Miller-Orr 직관

| 변수 ↑ | 범위 |
|--|--|
| σ² (변동성) | 넓음 |
| F (거래비용) | 넓음 |
| K (이자율) | 좁음 |

## §11 Baumol vs Miller-Orr

| | Baumol | Miller-Orr |
|--|--|--|
| 현금흐름 | 일정 | 랜덤 |
| 결과 | C* | Z*, H*, L |

## §12 Money Market 수단

| 수단 | 특징 |
|--|--|
| T-bill | 무위험 |
| CD | 양도성예금 |
| CP | 기업 어음 |
| Repo | 환매조건부 |
| MMF | 펀드 |

## §13 투자 기준

1. 유동성
2. 안전성
3. 수익성 (낮음)
4. 만기 매칭

## §14 임시 vs 영구 잉여

| | 처리 |
|--|--|
| 임시 (계절) | Money market |
| 영구 | 배당/buyback (Ch 19) |

## §15 Float 축소 (현대)

- Check 21 Act (2004)
- ACH / wire / RTP / FedNow
- → float ≈ 0, "playing float" 무의미

## §16 자주 함정

| 함정 | 정정 |
|--|--|
| Disbursement float 나쁨 | 유리 (지급지연) |
| Collection float 좋음 | 불리 (수금가속) |
| Baumol = 불확실 | 일정유출 (MO가 랜덤) |
| 현금 많을수록 안전 | 기회비용 |
| Float 무한 활용 | 전자결제로 소멸 |

## §17 핵심 mindmap

```
Cash Management
├── 보유동기 (transaction/precautionary/speculative)
├── Float (disb +유리 / coll −불리)
├── 수금 (lockbox) / 지급 (ZBA)
├── Baumol C*=√(2TF/K) (일정)
├── Miller-Orr Z*=∛(3Fσ²/4K)+L (랜덤)
└── Money market (T-bill/CP/MMF)
```

## §18 1-line summary

> **현금관리. 보유동기: transaction/precautionary/speculative. *Float* = 은행−장부: disbursement(+유리, 지급지연), collection(−불리, 수금가속), net=disb−coll. 수금: lockbox(float↓). 지급: ZBA. *목표잔액*: Baumol C*=√(2TF/K) (일정유출, 평균 C*/2) vs Miller-Orr Z*=∛(3Fσ²/4K)+L, H=3Z−2L (랜덤). 유휴현금: money market (T-bill/CD/CP/MMF). Float은 Check 21·RTP로 소멸.**
