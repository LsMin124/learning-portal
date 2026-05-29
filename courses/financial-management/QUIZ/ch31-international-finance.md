# Ch 31 International Corporate Finance — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *4 평가관계*는?

<details><summary>답</summary>

| 관계 | 내용 | 공식 |
|--|--|--|
| **PPP** | 인플레 차이 → 환율 | E(S_t)=S_0[(1+h_FC)/(1+h_US)]^t |
| **IRP** | 금리 차이 → forward | F_0/S_0=(1+R_FC)/(1+R_US) |
| **UFR** | forward = E(spot) | F_0 = E(S_1) |
| **IFE** | 실질금리 동일 | R_FC−R_US ≈ h_FC−h_US |

→ 네 관계가 *no-arbitrage* 로 연결 (금리·인플레·spot·forward 일관성).

</details>

### Q2. 환위험 *세 노출*?

<details><summary>답</summary>

| 노출 | 의미 | 헤지 |
|--|--|--|
| **Transaction** | 확정 외화 거래 결제 | Forward, option, money market |
| **Translation** | 회계 환산 (재무제표) | 일반적으로 미헤지 (현금 아님) |
| **Economic** | 장기 경쟁력 (구조적) | Operational hedge (생산 분산) |

**핵심**:
- Transaction = 단기, 헤지 명확
- Translation = 회계상 (실제 현금흐름 아님)
- Economic = 가장 어려움 (장기 환율 → 경쟁력)

</details>

### Q3. *Covered Interest Arbitrage*?

<details><summary>답</summary>

**IRP 위반 시 무위험 차익**:

IRP: $F_0/S_0 = (1+R_{FC})/(1+R_{US})$

**위반 시 (예: forward 고평가)**:
1. 저금리 통화 차입
2. Spot 으로 고금리 통화 환전
3. 고금리 예치
4. *Forward 로 환헤지* (covered)
5. 만기 환산 → 무위험 차익

→ 차익거래가 IRP 강제 (균형 복원). "Covered" = forward 헤지로 환위험 제거.

</details>

### Q4. 계산 — Relative PPP

현재 spot **$1.25/€** (유로당 달러, 즉 유로가 외국통화). 미국 인플레 2%, 유로존 인플레 5%.

(a) 1년 후 기대 환율? (b) 유로 절상/절하?

<details><summary>답</summary>

**표기 주의**: $/€ = 달러(국내, US) per 유로(외국, FC). 이 표기에서 *유로 절하 = $/€ 하락*.

**Relative PPP** (이 표기 방향에 맞춰):
$$E(S_1) = S_0 \times \frac{1 + h_{US}}{1 + h_{EUR}} = 1.25 \times \frac{1.02}{1.05}$$
$$= 1.25 \times 0.9714 = \$1.2143/€$$

**(b) 유로 변화**:
- $S_0 = $1.25/€ → E(S_1) = $1.2143/€
- 유로당 달러 *감소* → 유로 **절하**

**직관 (핵심 원리)**:
- *고인플레 통화(유로 5%) → 절하*
- 구매력 하락 → 통화 가치 하락
- 인플레 낮은 달러(2%)는 상대적 절상

→ E(S_1) ≈ $1.2143/€, 유로(고인플레) *절하*. 핵심: 고인플레 통화는 절하.

</details>

### Q5. 계산 — Covered IRP

Spot **¥110/$** (달러당 엔, 즉 달러가 기준). 미국 금리 3%, 일본 금리 1% (1년).

(a) 1년 forward 환율 (IRP)? (b) 엔 forward premium/discount?

<details><summary>답</summary>

**표기**: ¥/$ = 엔 per 달러. 엔이 우리가 평가할 통화, 달러가 기준(분모).

**Covered IRP**:
$$F_0 = S_0 \times \frac{1 + R_{JPY}}{1 + R_{USD}} = 110 \times \frac{1.01}{1.03}$$
$$= 110 \times 0.9806 = ¥107.87/\$$$

**(b) 엔 premium/discount**:
- Forward ¥107.87 < Spot ¥110
- → $ 당 엔이 *적게* 필요 → 엔 *절상* (forward **premium**)
- *저금리 통화(엔 1%) → forward premium* ✓

**IRP 직관 (no free lunch)**:
- 저금리 통화 → forward premium
- 고금리 통화($ 3%) → forward discount
- 금리 우위가 환율 손실로 상쇄

→ Forward ¥107.87/$, 엔 forward premium (저금리 통화).

</details>

### Q6. 계산 — 국제 자본예산 (Home Currency)

미국 기업이 유럽 프로젝트: 초기 €10M 투자. 1년 후 €12M 회수 (1회성). Spot $1.20/€. 1년 forward $1.18/€. 미국 할인율 10%.

NPV (home currency approach)?

<details><summary>답</summary>

**Home Currency Approach**:

**초기 투자 (spot 환산)**:
- €10M × $1.20/€ = $12.0M (유출)

**1년 후 회수 (forward 환산)**:
- €12M × $1.18/€ = $14.16M

**NPV (미국 할인율 10%)**:
$$NPV = -12.0 + \frac{14.16}{1.10} = -12.0 + 12.87 = +\$0.87M$$

**해석**:
- 초기는 spot, 미래 CF 는 forward (또는 expected) 환율로 환산
- 자국통화로 변환 후 자국 할인율 적용
- NPV ≈ +$0.87M → *프로젝트 채택*

**Foreign currency approach 와 일관성**:
- 외화 NPV 계산 후 spot 환산 → 같은 결과 (parity)

→ NPV ≈ +$0.87M. 채택.

</details>

### Q7. 디버그 — 고금리 통화 투자

투자자: *"호주 금리가 6%, 일본 금리가 0.5% 네. 일본에서 빌려서 호주에 예치하면 무위험으로 5.5% 먹는다! Carry trade!"*

위험은?

<details><summary>답</summary>

**Carry trade 의 위험 (무위험 아님)**:

**1. IRP — 이론상 상쇄**:
- 고금리 통화(호주)는 *forward discount*
- Forward 로 헤지하면 (covered) → 차익 0
- 금리 우위 = 예상 환율 손실

**2. Uncovered carry trade (헤지 안 함)**:
- Forward 없이 spot 환위험 노출
- IFE: 고금리 통화 *절하* 예상 (이론)
- → 금리 차익이 환손실로 상쇄 (평균)

**3. 실제 위험**:
- *환율 급변* (호주달러 폭락 → 큰 손실)
- *Crash risk* — carry trade 는 비대칭 ("picking up nickels in front of a steamroller")
- 2008: 엔 carry trade 청산 → 엔 급등, 큰 손실

**4. 실증 (forward premium puzzle)**:
- 사실 고금리 통화가 단기 *덜 절하* (UIP 위반)
- → carry trade 가 *평균 수익* (위험 프리미엄/crash risk 보상)
- 단 tail risk 큼

**올바른 관점**:
- Covered (헤지) → 무위험 차익 0 (IRP)
- Uncovered → 환위험 부담 (carry premium = 위험 보상)
- "무위험 5.5%" 는 착각

→ Covered 면 IRP 로 차익 0. Uncovered carry trade 는 환위험 (crash risk, 2008 엔 급등). "무위험" 아님.

</details>

### Q8. 디버그 — Translation 노출 과민반응

CFO: *"유로 약세로 우리 유럽 자회사 자산이 환산 시 $50M 줄었다! 당장 forward 로 헤지해서 이 손실 막아야 한다!"*

문제점?

<details><summary>답</summary>

**Translation 노출 과민반응**:

**1. Translation = 회계상 (현금 아님)**:
- 재무제표 환산 손익 (OCI, 자본 항목)
- *실제 현금흐름 영향 없음* (자회사 계속 운영)
- 매각/청산 전엔 미실현

**2. Forward 헤지의 역설**:
- 회계 손실 막으려 forward → *실제 현금* 위험 생성
- 회계(가짜) 헤지하려 경제적(진짜) 위험 부담
- → 본말전도

**3. 우선순위**:
- *Transaction 노출* (실제 거래) → 헤지 우선
- *Economic 노출* (장기 경쟁력) → operational hedge
- *Translation* → 일반적으로 미헤지 (또는 제한적)

**4. 예외 (translation 헤지가 타당한 경우)**:
- Covenant (부채비율) 위배 우려
- 곧 매각 예정 (실현 임박)
- 신용등급 영향

**올바른 관점**:
- 회계 숫자 vs 경제적 실질 구분
- 진짜 현금흐름 (transaction, economic) 에 집중
- Translation 은 disclosure 로 설명

→ Translation = 회계상(현금 아님, 미실현). Forward 헤지는 진짜 현금위험 생성 (본말전도). Transaction/economic 노출에 집중.

</details>

### Q9. 면접 — *다국적기업의 환위험 관리 전략 전반*?

<details><summary>답</summary>

**MNC 환위험 관리 — 통합 프레임워크**:

**1. 노출 식별 (3종)**:
- Transaction (확정 거래) → 헤지 우선순위 1
- Economic (장기 경쟁력) → operational
- Translation (회계) → 제한적

**2. Operational hedge (구조적, 우선)**:
- *Natural hedge* — 수익-비용 통화 매칭
- 현지 생산 (해외 매출 = 해외 비용)
- 글로벌 공급망 분산
- 현지 자금조달 (현지 부채)

**3. Financial hedge (잔여 위험)**:
- *Forward/futures* — 확정 거래
- *Currency option* — 비대칭 (불확실 노출)
- *Currency swap* — 장기 (Ch 25)
- *Money market hedge* — 차입+예치

**4. 정책 결정**:
- Hedge ratio (full vs selective)
- 중앙집중 (treasury) vs 분산
- Netting (사내 상계), in-house bank
- Hedge horizon (얼마나 멀리)

**5. 거버넌스**:
- Hedge accounting (ASC 815, IFRS 9)
- 정책·한도 (투기 방지)
- 모니터링·보고

**6. 헤지 vs 비헤지 논쟁 (M&M, Ch 25)**:
- 완전시장: 무관
- 헤지 정당화: distress 비용, 세금, 과소투자
- Selective hedging = 투기 위험

**사례**:
- Coca-Cola, P&G — 대규모 FX 노출 (글로벌 매출)
- 일본 자동차 — natural hedge (미국 생산)
- 항공사 — 연료(달러) + 환위험 동시

**정치 위험 통합**:
- 현지 조달, JV, 정치보험, 국가 프리미엄

> MNC 환위험: 3 노출 식별 (transaction 우선). Operational hedge (natural hedge, 현지생산/조달) 먼저, 잔여는 financial (forward/option/swap). 정책 (hedge ratio, netting, 중앙집중) + 거버넌스 (hedge accounting, 투기 방지). M&M: distress/세금/과소투자 있을 때 정당. + 정치위험.

</details>

### Q10. 면접 — *왜 PPP 가 단기엔 잘 안 맞고 장기엔 성립하는가*? 🎉 (마지막 문항)

<details><summary>답</summary>

**PPP 의 단기 실패 / 장기 성립**:

**단기 실패 이유**:

**1. 거래/이동 비용**:
- 운송비, 관세, 비관세 장벽
- 차익거래 즉시 안 됨

**2. 비교역재 (non-tradables)**:
- 서비스, 부동산, 인건비 (이발, 임대)
- 국가 간 차익거래 불가 (Balassa-Samuelson)

**3. 가격 경직성 (sticky prices)**:
- 명목 가격 천천히 조정 (메뉴 비용)
- 환율은 즉시 변동 (자산 가격)
- → 단기 괴리

**4. 자본 흐름 지배**:
- 단기 환율 = *자본 이동* (금리, 투자) 지배
- 무역(PPP)보다 자본계정이 큼

**5. 실증 (PPP puzzle)**:
- 실질환율 평균회귀 *반감기 3-5년* (Rogoff)
- 단기 변동성 큼

**장기 성립 이유**:
- 누적 인플레 차이 → 결국 환율 반영
- 차익거래 (교역재) 압력 축적
- 평균회귀 (mean reversion)

**Big Mac Index (실증 도구)**:
- 단순 PPP 측정 (The Economist)
- 통화 과대/과소평가 가늠
- 한계: 비교역 요소 (임대료, 인건비)

**함의**:
- 단기 환율 예측 = 어려움 (random walk 에 가까움, Meese-Rogoff)
- 장기 fair value = PPP 기준
- 자본예산: 장기 PPP/IFE 가정 합리적

**철학적**:
- 환율 = 자산가격 (단기 변동) + 재화가격 (장기 PPP)
- 두 force 의 시계(time horizon) 차이

> PPP 단기 실패: 거래비용·관세, 비교역재(서비스), 가격 경직성, 자본흐름 지배. 장기 성립: 누적 인플레 차이 반영, 차익거래 압력, 평균회귀(반감기 3-5년, Rogoff). Big Mac Index. 단기 예측 불가(Meese-Rogoff), 장기 fair value=PPP. 🎉 전 과정 완료!

</details>
