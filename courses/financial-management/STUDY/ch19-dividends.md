# Chapter 19: Dividends and Other Payouts — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 19** (책 p.572~610).
> 19장은 *payout policy* — Dividend vs Buyback, MM dividend irrelevance, signaling, clientele, taxes.

이 장의 *지적 무게중심*:
1. **Payout 종류** — cash dividend, stock dividend, split, buyback
2. **MM Dividend Irrelevance** — homemade dividends
3. **Real-world factors** — taxes, transaction costs, signaling, clientele, agency
4. **Stock repurchase vs dividend**
5. **Dividend policy in practice** — Lintner

---

## §0 도입 — 번 돈을 어떻게 돌려줄까

기업이 양(+)의 NPV 프로젝트에 다 쓰고도 현금이 남으면, *주주에게 돌려주는* 길은 둘이다 — **배당(dividend)** 과 **자사주 매입(buyback)**. 19장의 두 질문: ① *얼마나* 돌려줄까(payout 수준), ② *어떤 형태로*(배당 vs buyback). MM 의 출발점은 충격적이다 — *완전시장에서는 둘 다 가치와 무관*(homemade dividends). 그러나 현실에서는 **세금·신호·clientele·agency** 가 정책을 가른다.

![Figure 19.4 — Quarterly Variation in Reported Earnings, Dividends, and Net Repurchases for Large U.S. Firms. 교재 p.580](/courses/financial-management/figures/ch19/fig-19-4.png)

> **직관**: *dividends(주황)* 는 거의 평탄한 반면 *buybacks(올리브)* 는 이익을 따라 출렁인다 — 배당은 *sticky*(한 번 올리면 잘 못 내림), buyback 은 *유연한* 잔여 분배 수단임을 한눈에 보여준다. 2008 이익 급락(파랑) 때도 배당은 거의 줄지 않았다.

---

## §1 Payout 의 종류

### §1.1 Cash dividend

| 용어 | 의미 |
|--|--|
| **Regular cash dividend** | 분기/연 정기 배당 |
| **Special dividend** | 일회성 (excess cash) |
| **Liquidating dividend** | 청산 시 자본 환원 |

### §1.2 Dividend 의 *4 date*

| Date | 의미 |
|--|--|
| **Declaration date** | 이사회 배당 결의 |
| **Ex-dividend date** | 이 날 *이후* 매수자는 배당 못 받음 (보통 record −1일) |
| **Record date** | 주주명부 확정 |
| **Payment date** | 실제 지급 |

![Figure 19.1 — Example of Procedure for Dividend Payment. 교재 p.574](/courses/financial-management/figures/ch19/fig-19-1.png)

→ *Ex-date 에 주가 ≈ 배당금만큼 하락* (이론).

![Figure 19.2 — Price Behavior around the Ex-Dividend Date for a $1 Cash Dividend. 교재 p.575](/courses/financial-management/figures/ch19/fig-19-2.png)

> **직관**: ex-date 직전 주가 $(P+1)$ 에서 ex-date 에 정확히 배당금 $1 만큼 떨어져 $P 가 된다. 떨어지지 않는다면 *배당락 직전 매수→직후 매도* 로 무위험 차익이 생기므로, 차익거래가 그 간격을 메운다(세금 무시 시).

### §1.3 Stock dividend + Stock split

- **Stock dividend**: 주식으로 배당 (예: 10% → 100주 보유 시 10주 추가)
- **Stock split**: 액면 분할 (예: 2-for-1, 주가 절반, 주식 2배)
- **Reverse split**: 병합 (예: 1-for-10, 주가 ↑, delisting 회피)

→ *Cosmetic* — 총 가치 불변, 그러나 *signaling* 효과.

### §1.4 Stock repurchase (buyback)

| 방식 | 의미 |
|--|--|
| **Open market** | 시장에서 매수 (가장 흔함) |
| **Tender offer** | 고정가 일괄 매수 제안 |
| **Dutch auction** | 가격 범위 제시, 최저가 결정 |
| **Targeted (greenmail)** | 특정 주주 매수 (적대적 인수 방어) |

---

## §2 MM Dividend Irrelevance

### §2.1 명제

> *Perfect market 에서 dividend policy 는 firm value 와 무관*.

(Miller-Modigliani 1961)

### §2.2 Homemade dividends

> 투자자가 *스스로* 원하는 cash flow 를 만들 수 있다.

- 회사가 배당 안 함 → *주식 일부 매도* (자가 배당)
- 회사가 배당 많이 함 → *배당 재투자* (배당 거부 효과)

→ *Dividend policy 가 투자자에게 무의미*.

![Figure 19.3 — Homemade Dividends: A Trade-off between Dividends per Share at Date 0 and Date 1. 교재 p.578](/courses/financial-management/figures/ch19/fig-19-3.png)

> **직관**: 기업의 배당 시점 선택은 투자자를 직선 위 한 점(A)에 놓을 뿐이다. 투자자는 *주식 매도/재투자* 로 같은 직선 위 어디로든(B·C) 자유롭게 이동할 수 있다 — 기울기 $-1/1.1$ 은 시간선호(할인). 그래서 배당정책 자체는 가치를 바꾸지 못한다.

### §2.3 가정

1. No taxes
2. No transaction costs
3. No issuance costs
4. Fixed investment policy
5. No information asymmetry

### §2.4 직관

- *Firm value* = *investment policy* 가 결정 (NPV of projects)
- *Dividend* = 단지 *cash 의 분배 방식*
- *배당 ↑* → 주가 하락 + cash 받음 = *zero-sum*

### §2.5 Dividend vs Capital structure irrelevance

- 둘 다 MM, perfect market 가정
- *Capital structure*: 자금조달 방식
- *Dividend*: 분배 방식
- *Investment policy 가 진짜 value driver*

---

## §3 실제 세계 요인 — Dividend 선호 (높은 배당)

### §3.1 Desire for current income

- 은퇴자, 연기금 — *정기 cash flow* 필요
- *Homemade dividend* 의 *transaction cost*

### §3.2 Behavioral / Self-control (Shefrin-Statman)

- *"Don't dip into capital"* — 원금 보존 심리
- *Mental accounting* — 배당 = 소득, 원금 = 별도
- *Bird-in-hand* fallacy (Gordon-Lintner) — 그러나 risk 는 investment 가 결정

### §3.3 Agency cost 감소 (Jensen)

- *Free cash flow 분배* → manager 의 empire building 억제
- *Discipline* 효과

### §3.4 Signaling

- *배당 증가* = 미래 cash flow 자신감 신호
- *배당 삭감* = 강한 부정 신호 (주가 급락)
- *Sticky dividends* — 함부로 올리지 않음

---

## §4 실제 세계 요인 — Dividend 억제 (낮은 배당)

### §4.1 Taxes (가장 중요)

- 전통적으로 *배당 = ordinary income*, *capital gain = 우대세율*
- → *Buyback 이 tax-efficient*
- *US 2003+*: qualified dividend 도 capital gain 세율 (15-20%)
- 그래도 *capital gain 은 deferral 가능* (실현 시점 선택)

![Figure 19.5 — Firm Issues Stock to Pay a Dividend. 교재 p.583](/courses/financial-management/figures/ch19/fig-19-5.png)

> **직관**: 세금이 없으면(왼쪽) 주식을 발행해 배당하는 것은 돈이 회사→주주→회사로 돌기만 하는 *무의미한 순환*이다. 그러나 개인 배당세 15%(오른쪽)가 붙으면 매번 IRS 가 $15 를 떼어가 — 불필요한 배당은 *순전한 세금 누수*다. 배당이 capital gain 보다 불리한 핵심 이유.

### §4.2 Flotation costs

- 배당 후 자금 부족 → 신규 발행 (issuance cost)
- *내부 자금 우선* (Pecking order)

### §4.3 Investment opportunities

- *Growth firm* — 재투자가 우선 (Apple 2012 전, Amazon, Tesla)
- *High ROE reinvestment* > dividend

### §4.4 Dividend restrictions

- *Bond covenants* — 배당 제한
- *법적 제약* — 자본잠식 시 배당 금지

---

## §5 Stock Repurchase vs Dividend

### §5.1 동등성 (perfect market)

> Buyback 과 dividend 는 *perfect market 에서 동일*.

- $1M 배당 vs $1M buyback → *주주 부 동일*
- 배당: 모두 cash 받음
- Buyback: 판 사람 cash, 안 판 사람 주가 유지 (지분율 ↑)

### §5.2 Buyback 의 장점

1. **Tax efficiency** — capital gain deferral
2. **Flexibility** — 의무 아님 (dividend 는 sticky)
3. **No signal commitment** — 삭감 부담 없음
4. **EPS boost** — 주식 수 감소
5. **Undervaluation signal** — "우리 주식 싸다"
6. **Offset dilution** — stock-based comp 상쇄

### §5.3 Buyback 의 단점 / 비판

1. **Manipulation** — EPS 조작, 경영진 보상 (option) 연계
2. **Bad timing** — 고점 매수 흔함 (2007, 2021)
3. **Underinvestment** — R&D/capex 대신 buyback
4. **Leverage 증가** — 차입 buyback (debt-funded)
5. *정치적 비판* — 2022 US 1% excise tax

### §5.4 현대 트렌드

- *Buyback > Dividend* (US, 2000s+)
- *Apple*: $90B+/year buyback (역대 최대)
- *S&P 500 buyback*: $900B+/year (2022 peak)
- *Total payout yield* = dividend yield + buyback yield (~4%)

---

## §6 Dividend Policy in Practice — Lintner

### §6.1 Lintner (1956) 의 발견

> 기업은 *목표 payout ratio* 를 향해 *점진적으로 조정*.

$$\Delta Div_t = \text{Speed} \times (\text{Target} - Div_{t-1})$$

- *Target payout ratio* (예: 40%)
- *Adjustment speed* (보통 0.3-0.5)
- *Sticky* — 급격한 변화 회피

### §6.2 4 stylized facts (Lintner)

1. 기업은 *장기 target payout ratio* 보유
2. *배당 변화* 가 *수준* 보다 중요
3. *지속 가능한 earnings 증가* 에만 배당 인상
4. *배당 삭감* 을 극도로 꺼림

### §6.3 Dividend smoothing

- *Earnings 변동* 보다 *배당 변동 훨씬 작음*
- *Signaling* — 안정성 신호
- *Clientele* — 예측 가능성 선호

![Figure 19.7 — Ratio of Aggregate Dividends to Aggregate Earnings for All U.S. Firms: 1980 to 2016. 교재 p.594](/courses/financial-management/figures/ch19/fig-19-7.png)

> **직관**: 총 배당/이익 비율(payout ratio)이 해마다 0.4~0.8 사이를 오가는데, *분모(이익)* 가 경기 따라 출렁이는 게 주원인이다. 기업이 배당을 매끄럽게 유지(smoothing)하므로, 이익이 급락한 해엔 payout ratio 가 *치솟는다*(2008·2001).

### §6.4 Catering theory (Baker-Wurgler)

- 투자자가 *배당주 선호* 시기 → 기업 배당 시작
- *Dividend premium* 변동
- *Behavioral*

![Figure 19.8 — Proportion of Dividend Payers among All Publicly Held U.S. Industrial Firms: 1980–2015. 교재 p.595](/courses/financial-management/figures/ch19/fig-19-8.png)

> **직관**: 배당하는 기업 비율이 1980 ~60% 에서 2000 ~15% 로 급락했다(Fama-French "disappearing dividends") — 신규 상장한 성장·기술 기업이 배당 대신 *재투자·buyback* 을 택했기 때문. 2002 이후 반등은 catering(투자자의 배당 선호 회귀)과도 맞물린다.

---

## §7 Clientele Effect

### §7.1 명제

> 서로 다른 투자자 그룹이 서로 다른 payout policy 선호.

| Clientele | 선호 |
|--|--|
| 은퇴자, 연기금 | 높은 배당 (current income) |
| 고소득 개인 | 낮은 배당 (tax) |
| 기관 (tax-exempt) | 무차별 |
| Growth 투자자 | 낮은 배당 (재투자) |

![Figure 19.6 — Preferences of Investors for Dividend Yield. 교재 p.593](/courses/financial-management/figures/ch19/fig-19-6.png)

> **직관**: 실제 데이터에서 *고소득(주황)* 투자자일수록 *고배당(High)* 분위 비중이 낮고, *저소득(올리브)* 일수록 고배당주를 더 담는다 — 세금 유인에 따라 clientele 이 갈린다는 증거. 다만 차이가 극적이진 않아 MM 을 부분적으로만 뒤집는다.

### §7.2 함의

- 기업은 *특정 clientele* 를 끌어들임
- *Policy 변경* → clientele 이동 (transaction cost)
- *Supply-demand* 균형 → 추가 가치 창출 어려움 (MM 부분 지지)

---

## §8 Taxes 의 상세

### §8.1 US 세율 역사

| 시기 | 배당 세율 | Capital gain |
|--|--|--|
| ~2003 | Ordinary (최대 39.6%) | 우대 (20%) |
| 2003-2012 | 15% (qualified) | 15% |
| 2013+ | 20% (고소득) + 3.8% NIIT | 20% + 3.8% |

### §8.2 Capital gain 의 추가 이점

- *Deferral* — 실현 시점 선택
- *Step-up basis* — 상속 시 과세 회피
- *Tax-loss harvesting* 결합

### §8.3 한국 (참고)

- *배당소득세* 15.4% (원천징수)
- *금융소득종합과세* (2천만원 초과 시)
- *양도소득세* — 대주주 과세 (소액주주 비과세, 변동 중)

→ 국가별 *배당 vs 양도* 세제가 payout policy 영향.

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 높은 배당 = 좋은 회사 | MM — investment policy 가 value driver |
| 2 | Bird-in-hand (배당이 덜 risky) | Risk 는 investment 가 결정, fallacy |
| 3 | Stock split 이 가치 창출 | Cosmetic, signaling 만 |
| 4 | Buyback = 항상 좋음 | Bad timing, manipulation 위험 |
| 5 | 배당 삭감 = 항상 나쁨 | 재투자 기회 있으면 합리적 (단 signal 주의) |
| 6 | Dividend irrelevance = 실무 무의미 | Tax, signaling, clientele 가 실제론 중요 |
| 7 | EPS boost = 가치 창출 | 분모 감소일 뿐, 가치는 별개 |
| 8 | Ex-date 주가 무변 | 배당금만큼 하락 (이론) |

---

## §10 자가점검

1. *Dividend 의 4 date*?
2. *MM dividend irrelevance* + homemade dividend?
3. *높은 배당 선호* 요인?
4. *낮은 배당 선호* 요인?
5. *Buyback 의 장점* 6 가지?
6. *Lintner* 의 stylized facts?
7. *Clientele effect*?

<details><summary>해답</summary>

1. Declaration → Ex-dividend → Record → Payment.
2. Perfect market 에서 dividend policy 무관. Homemade: 투자자가 주식 매도/재투자로 원하는 cash flow 생성.
3. Current income (은퇴자), behavioral (self-control), agency 감소 (Jensen), signaling.
4. Taxes (배당 > capital gain 세율, 전통), flotation cost, investment opportunities, covenants.
5. Tax efficiency, flexibility, no commitment, EPS boost, undervaluation signal, dilution offset.
6. Target payout ratio, 점진 조정, 변화>수준, 지속가능 earnings 에만 인상, 삭감 극도로 회피.
7. 투자자 그룹별 payout 선호 다름 (은퇴자 high, 고소득 low). 기업이 특정 clientele 유치.

</details>

---

## §11 다음 학습으로

- **Ch 20** — Raising capital (IPO)
- **Ch 16-17** — Capital structure (payout 과 연결)
- **Ch 14** — Behavioral (catering)

---

## §12 한 줄 요약

> **Payout policy — cash dividend / stock dividend / split / buyback. *MM*: perfect market 에서 dividend irrelevant (homemade dividends). 실제: *taxes* (배당<capital gain 전통, buyback tax-efficient), *signaling* (sticky, 삭감 회피), *clientele*, *agency*. *Buyback*: tax efficiency + flexibility + EPS boost, 그러나 *bad timing / manipulation* 위험. *Lintner*: target payout 향해 점진 조정, dividend smoothing. *Total payout yield* = dividend + buyback (~4%).**
