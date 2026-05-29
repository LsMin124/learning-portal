# Ch 31 International Corporate Finance — 치트시트

> 환율 / 4 평가관계 / 자본예산 / 환위험 / 정치위험.

## §1 용어

| 용어 | 의미 |
|--|--|
| Spot | 현물 환율 |
| Forward | 선물 환율 |
| Cross-rate | 교차 환율 |
| Eurocurrency | 자국 밖 통화 |
| ADR | 미국 예탁증서 |

## §2 환율 표기

- Direct: $/FC ($1.20/€)
- Indirect: FC/$ (€0.83/$)
- 절상(appreciate)/절하(depreciate)

## §3 평가관계 ① PPP

**절대**:
$$S_0 = \frac{P_{국내}}{P_{해외}}$$

**상대**:
$$E(S_t) = S_0\left[\frac{1+h_{FC}}{1+h_{US}}\right]^t$$

→ 고인플레 통화 절하.

## §4 평가관계 ② IRP (Covered)

$$\frac{F_0}{S_0} = \frac{1+R_{FC}}{1+R_{US}}$$

→ 고금리 통화 forward discount.

## §5 평가관계 ③ UFR

$$F_0 = E(S_1)$$

(forward = 미래 spot 추정)

## §6 평가관계 ④ IFE

$$R_{US} - h_{US} = R_{FC} - h_{FC}$$

→ 실질금리 동일, 명목차 = 인플레차.

## §7 4 관계 통합

```
       PPP (h→S)
        │
IFE ────┼──── IRP
(R=h)         (R차=fwd)
        │
       UFR (F=E(S))
```

no-arbitrage 로 연결.

## §8 근사식

| 관계 | 근사 |
|--|--|
| PPP | (E(S₁)−S₀)/S₀ ≈ h_FC−h_US |
| IRP | (F₀−S₀)/S₀ ≈ R_FC−R_US |
| IFE | R_FC−R_US ≈ h_FC−h_US |

## §9 국제 자본예산

| 접근 | 방법 |
|--|--|
| Home currency | 외화CF→환산→자국 할인 |
| Foreign currency | 외화 할인→spot 환산 |

→ 같은 NPV (parity).

## §10 환위험 3 노출

| 노출 | 의미 |
|--|--|
| Transaction | 거래 (확정 외화) |
| Translation | 회계 환산 |
| Economic | 장기 경쟁력 |

## §11 Transaction 헤지

- Forward/futures
- Money market hedge
- Currency option
- Currency swap

## §12 Economic 노출

- 장기·구조적 (어려움)
- Operational hedge (생산 분산)
- Natural hedge (수익=비용 통화)

## §13 정치 위험

- Expropriation (국유화)
- 송금 제한
- 대응: 현지조달/JV/보험/할인율↑

## §14 Carry Trade

- 저금리 차입 → 고금리 예치
- Covered: 차익 0 (IRP)
- Uncovered: 환위험 (crash risk)

## §15 자주 함정

| 함정 | 정정 |
|--|--|
| 절대 PPP 항상 | 상대적이 현실 |
| 고금리 = 좋은 투자 | forward discount |
| IRP=PPP | 금리vs인플레 |
| 두 자본예산 다름 | 같음 (parity) |
| Translation = 현금손실 | 회계상 |
| Economic = forward | operational |

## §16 핵심 mindmap

```
International Finance
├── 환율 (spot/forward, cross-rate)
├── 4 평가관계
│   ├── PPP (인플레→환율)
│   ├── IRP (금리→forward)
│   ├── UFR (forward=E spot)
│   └── IFE (실질금리 동일)
├── 자본예산 (home/foreign, 같은 NPV)
├── 환위험 (transaction/translation/economic)
└── 정치위험 (국유화, 보험)
```

## §17 시험 요령

- 환율 표기 방향 *항상 확인* (분자/분모)
- 고인플레→절하, 고금리→forward discount
- Parity 는 모두 연결 (하나 알면 도출)
- Translation ≠ 현금흐름

## §18 1-line summary

> **국제재무. 환율: spot/forward, cross-rate. *4 평가관계*: ①PPP(고인플레 통화 절하) ②covered IRP F/S=(1+R_FC)/(1+R_US)(고금리 forward discount) ③UFR F=E(S₁) ④IFE 실질금리 동일(R차=h차) — no-arbitrage 연결. *자본예산*: home/foreign currency (같은 NPV). *환위험*: transaction(forward 헤지)·translation(회계, 미헤지)·economic(operational). *정치위험*: 국유화→현지조달·보험·할인율. Carry trade: covered 차익 0, uncovered 환위험(crash risk).**
