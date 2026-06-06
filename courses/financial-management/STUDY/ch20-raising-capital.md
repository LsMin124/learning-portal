# Chapter 20: Raising Capital — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 20** (책 p.630~666).
> 20장은 *자본 조달* 의 전 과정 — Venture Capital, IPO, SEO, Rights offering, Shelf registration.

이 장의 *지적 무게중심*:
1. **Early-stage financing** — VC, angel, stages
2. **IPO** — process, underpricing, long-run underperformance
3. **Underwriting** — firm commitment vs best effort
4. **SEO (Seasoned Equity Offering)** — dilution, signaling
5. **Rights offering** — value of a right
6. **Costs of issuing**

---

## §0 도입 — *돈을 어디서 끌어오나*

> **핵심 한 문장**: 가치평가(2부)와 자본구조(4부)가 "얼마짜리냐·어떻게 섞느냐"였다면, 20장은 그 자본을 *실제로 어디서·어떻게 조달하나* — **VC → IPO → SEO** 의 생애주기와, 길목마다 *정보 비대칭* 이 물리는 비용.

기업의 자금 조달은 성장 단계를 따라 사다리를 오른다:

1. **사적 단계 — Venture Capital** (§1): 위험이 커 공개시장이 못 받는 초기 기업을 VC 가 *단계별(staged)* 로 댄다. 대부분 실패하고 소수가 대박이라(figure 20.2 의 exit funnel — IPO 는 14%뿐) *option to abandon* 이 핵심. 소프트웨어·바이오에 집중되고(figure 20.1), 산업 자체가 닷컴버블처럼 출렁인다(figure 20.4).
2. **공개 진입 — IPO** (§2–3): underwriter 가 S-1·로드쇼·book building 으로 가격을 매기고(figure 20.5 의 tombstone 이 그 신디케이트), 첫날 평균 +15~20% *underpricing* 이 발생한다(figure 20.6) — winner's curse 로 설명되는 *균형* 현상. 발행 물량 자체도 *hot issue* 시장처럼 군집한다(figure 20.7).
3. **상장 후 — SEO·Rights** (§4–5): 이미 상장된 회사가 더 발행하면 평균 −3% 하락 — *Myers-Majluf*: "경영진이 고평가라 여길 때 주식을 판다"는 신호. Rights offering 은 그 희석을 기존 주주에게 *우선권* 으로 돌려준다.

관통하는 주제는 **정보 비대칭** 이다: 발행자는 자기 회사를 투자자보다 잘 안다 → underpricing(IPO)과 −3%(SEO)는 그 격차의 *가격표*. §6 은 이 모두를 "발행의 6가지 비용"으로 묶는다.

---

## §1 Early-Stage Financing

### §1.1 자금 조달 단계

| 단계 | 자금원 |
|--|--|
| **Bootstrap** | 창업자, FFF (Friends, Family, Fools) |
| **Seed** | Angel investor, accelerator (Y Combinator) |
| **Series A/B/C** | Venture Capital |
| **Late stage** | Growth equity, crossover funds |
| **Exit** | IPO 또는 M&A |

![Figure 20.3 — 2016 Venture Capital Investment by Company Stage. 교재 p.615](/courses/financial-management/figures/ch20/fig-20-3.png)

> **직관**: VC 투자를 *기업 단계별* 로 쪼갠 파이. Angel/Seed 10% → Early VC 35% → Later VC 56% — 돈의 대부분은 *검증된 후기* 단계로 간다. 초기일수록 위험해 비중이 작은 게 §1.1 사다리의 그림.

### §1.2 Venture Capital 특징

- *High risk, high return* (대부분 실패, 소수 대박)
- *Active involvement* (board seat, mentoring)
- *Staged financing* (milestone 기반)
- *Convertible preferred* (Ch 15) — downside 보호 + upside
- *Exit 목표* (5-7년, IPO/M&A)

![Figure 20.1 — Venture Capital Investments in 2016 by Industry Sector. 교재 p.614](/courses/financial-management/figures/ch20/fig-20-1.png)

> **직관**: VC 가 *어느 산업* 에 가나 — Software 48% + Pharma/Biotech 11% 가 절반 이상. *확장성(scalability)* 높고 IP 로 보호되는 분야에 집중된다. '대부분 실패, 소수 대박' 모델은 이런 고성장 가능 산업에서만 작동한다.

![Figure 20.4 — Capital Commitments to U.S. Venture Funds ($ in billions) 1985 to 2016. 교재 p.616](/courses/financial-management/figures/ch20/fig-20-4.png)

> **직관**: VC 산업 자체의 *경기순환*. 1985~2016 미국 벤처펀드 출자액 — 2000년 닷컴버블에 $100B 로 폭발했다 급락. VC 는 *시장 타이밍* 에 극도로 민감(IPO 창구가 열려야 exit)하다. 자금 가용성이 곧 스타트업 생태계의 호흡.

### §1.3 VC 의 *staged financing* 이유

1. **Option to abandon** — milestone 실패 시 중단
2. **Discipline** — 자금 효율 강제
3. **Information** — 각 단계 정보 업데이트
4. **Valuation step-up** — 성공 시 다음 라운드 높은 가치

![Figure 20.2 — The Exit Funnel: Outcomes of the 11,686 Companies First Funded 1991 to 2000. 교재 p.614](/courses/financial-management/figures/ch20/fig-20-2.png)

> **직관**: 왜 *staged financing* 인가 — 1991~2000 첫 펀딩 11,686개사의 운명. IPO('Went/Going Public')는 **14%** 뿐, Acquired 33%, *Known Failed 18% + Still Private 35%*. 절반이 실패하거나 발이 묶인다. 이 냉혹한 깔때기가 VC 의 *option to abandon*(milestone 실패 시 중단)을 정당화한다.

### §1.4 주요 조항 (term sheet)

- *Liquidation preference* (청산 시 우선)
- *Anti-dilution* (down round 보호)
- *Pro-rata rights* (다음 라운드 참여권)
- *Drag-along / Tag-along*
- *Board composition*

---

## §2 IPO (Initial Public Offering)

### §2.1 IPO 의 *이유*

**장점**:
- *대규모 자금* 조달
- *Liquidity* (창업자/VC exit)
- *M&A currency* (주식 인수)
- *Brand / credibility*
- *Stock-based comp* 도구

**단점**:
- *Underpricing* (money left on table)
- *SOX 비용* (Ch 1)
- *Quarterly pressure* (short-termism)
- *Disclosure* 부담
- *Loss of control*

### §2.2 IPO 절차

1. **IB 선정** (underwriter, bookrunner)
2. **Due diligence + S-1 작성** (SEC registration)
3. **Roadshow** (institutional investor 마케팅)
4. **Book building** (수요 파악)
5. **Pricing** (전날 밤 가격 결정)
6. **Trading 시작** (first day)
7. **Stabilization** (greenshoe option)

### §2.3 Greenshoe (over-allotment) option

- Underwriter 가 *15% 추가 배정* 권리
- *수요 강하면* 행사 (추가 주식)
- *약하면* 시장 매수로 stabilize

### §2.4 IPO Underpricing

> *First-day pop* — 평균 +15-20% (US).

**원인**:
1. **Winner's curse** — uninformed investor 보호
2. **Information asymmetry** (issuer vs investor)
3. **Underwriter incentive** — oversubscription, 다음 거래
4. **Signaling** — "leave good taste" (재발행 대비)
5. **Cascade / bandwagon**

→ *Issuer 손해* (money left on table), 그러나 균형 현상.

![Figure 20.6 — Average Initial Returns by Month for SEC-Registered Initial Public Offerings: 1960–2017. 교재 p.627](/courses/financial-management/figures/ch20/fig-20-6.png)

> **직관**: IPO *underpricing* 의 실증. 1960~2017 월별 평균 첫날 수익률 — 평상시 +10~20%지만 2000년 닷컴기엔 +160%까지 치솟았다. 평균이 *양(+)* 이라는 게 핵심: 발행가가 체계적으로 *낮게* 책정돼 'money left on the table'이 된다. winner's curse 로 설명되는 균형.

![Figure 20.7 — Number of Offerings by Month for SEC-Registered Initial Public Offerings: 1960–2017. 교재 p.628](/courses/financial-management/figures/ch20/fig-20-7.png)

> **직관**: 발행 *물량* 도 군집한다 — 같은 기간 월별 IPO 건수. underpricing 이 높은 시기(2000)에 건수도 폭증하는 *hot issue market*. 창구가 열리면 너도나도 상장 → 시장 타이밍이 발행 결정을 지배함을 보여준다(20.6 과 짝).

### §2.5 IPO Long-run Underperformance

- *3-5년* market 대비 *−15~−20%* (Loughran-Ritter)
- *Market timing* (issuer 가 overvalued 시 발행)
- *Lock-up expiration* (6개월 후 insider 매도)
- *Window dressing* (IPO 전 earnings 관리)

---

## §3 Underwriting

### §3.1 방식 (Ch 15 recap)

| 방식 | 위험 부담 |
|--|--|
| **Firm commitment** | Underwriter (전량 매입 후 재판매) |
| **Best effort** | Issuer (최선 노력, 보장 X) |
| **Dutch auction** | 시장 (Google 2004) |

### §3.2 Spread (gross spread)

| 증권 | Spread |
|--|--|
| IPO | 6-7% |
| SEO | 4-5% |
| Bond | 1-2% |
| Private placement | 1-3% |

### §3.3 Syndicate

- *Lead underwriter* (bookrunner) + *co-managers* + *selling group*
- *위험 분산* + *distribution network*
- *League table* (IB 순위)

![Figure 20.5 — An Example of a Tombstone Advertisement. 교재 p.618](/courses/financial-management/figures/ch20/fig-20-5.png)

> **직관**: *Tombstone 광고* — 발행 완료를 알리는 공식 공고(WWF 1999 IPO). 'New Issue 11,500,000 Shares, $17.00'와 함께 아래로 *신디케이트* 가 위계순으로 나열된다: lead(Bear Stearns·Credit Suisse·Merrill) → co-manager → selling group. 누가 어디에 적히느냐가 IB league table 의 자존심.

### §3.4 Direct Listing (대안)

- *Spotify (2018), Slack (2019), Coinbase (2021)*
- *No underwriter spread* (6-7% 절감)
- *기존 주주 직접 매도* (신규 발행 X, 자금 조달 아님)
- *Liquidity 만* 제공

### §3.5 SPAC (대안)

- *Blank check company* — 먼저 상장, 후 합병
- *2020-2021 붐* (600+ SPACs)
- *Backdoor IPO*
- *대부분 실망스러운 성과*, SEC 규제 강화

---

## §4 SEO (Seasoned Equity Offering)

### §4.1 정의

> 이미 상장된 회사의 *추가 주식 발행*.

### §4.2 종류

- **General cash offer** — 일반 공모
- **Rights offer** — 기존 주주 우선
- **Private placement** — 특정 투자자

### §4.3 SEO 의 *주가 하락 효과*

- *발행 발표 시 평균 −3%* 주가 하락
- **이유 (Myers-Majluf, Pecking order)**:
  - *경영진이 overvalued 라고 판단* → equity 발행
  - 시장이 이 신호 해석 → 주가 하락
  - *Adverse selection* (lemons)

### §4.4 Dilution

- **Ownership dilution** — 지분율 감소
- **EPS dilution** — 주식 수 증가
- **Book value dilution** — 발행가 < book value 시
- *Percentage ownership* vs *value* 구분

---

## §5 Rights Offering

### §5.1 정의

> 기존 주주에게 *신주 우선 매수권* (보통 discount).

- *한국, 유럽* 흔함 (pre-emptive right, Ch 15)
- *Subscription price* < 시장가 (참여 유도)

### §5.2 Value of a Right

**Setup**: N개 주식당 1 신주 매수권, subscription price S, 현재가 P_0.

**Ex-rights price**:
$$P_X = \frac{N \times P_0 + S}{N + 1}$$

**Value of one right**:
$$\text{Right value} = \frac{P_0 - S}{N + 1} = P_0 - P_X$$

### §5.3 예제

현재가 $50, subscription $40, 4주당 1 신주 (N=4).

**Ex-rights price**:
$$P_X = \frac{4 \times 50 + 40}{5} = \frac{240}{5} = \$48$$

**Right value**:
$$50 - 48 = \$2$$

(또는 $(50-40)/5 = 2$)

### §5.4 주주 부 불변

- Rights 행사하든, 팔든 → *주주 부 동일* (이론)
- *행사 안 + 안 팔면* → 손해 (right 가치 소멸)
- → *반드시 행사 또는 매도*

---

## §6 Costs of Issuing Securities

### §6.1 6 가지 비용

1. **Gross spread** (underwriter)
2. **Other direct expenses** (legal, audit, filing)
3. **Indirect expenses** (management time)
4. **Abnormal returns** (SEO 의 −3%)
5. **Underpricing** (IPO 의 first-day pop)
6. **Greenshoe option** (over-allotment 비용)

### §6.2 규모의 경제

- *큰 발행* → spread % 낮음
- *작은 발행* → 고정비 부담 큼
- *IPO* 가 가장 비쌈 (uncertainty)

### §6.3 Shelf Registration (Rule 415)

- *한 번 등록, 2년간 수시 발행*
- *Market timing* 유연성
- *비용 절감* (반복 등록 불필요)
- *대기업* 선호

---

## §7 실무 / 현대 트렌드

### §7.1 IPO 시장 진화

- *Staying private longer* (IPO age 4 → 10년)
- *Mega private rounds* (SoftBank Vision Fund)
- *Stripe, OpenAI, SpaceX* — 수백억 달러 private

### §7.2 Direct listing + SPAC

- *Spotify, Coinbase* (direct)
- *2020-21 SPAC 붐* → *2022 붕괴*

### §7.3 Crowdfunding

- *Reg CF* ($5M), *Reg A+* ($75M)
- *Retail investor 접근*

### §7.4 한국 IPO

- *KRX (KOSPI/KOSDAQ)*
- *공모가 산정* (수요예측)
- *균등배정 + 비례배정* (2021 개편)
- *따상* (시초가 2배 + 상한가) 현상

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | IPO underpricing = 비합리 | 균형 현상 (winner's curse 등) |
| 2 | IPO = 항상 좋은 투자 | Long-run underperformance |
| 3 | SEO 발표 = 호재 | 평균 −3% (Myers-Majluf signal) |
| 4 | Rights 무시해도 됨 | 행사 안+안 팔면 손해 |
| 5 | Dilution = 항상 나쁨 | 자금 용도 (positive NPV) 가 관건 |
| 6 | Direct listing = 자금 조달 | Liquidity 만 (신주 발행 X) |
| 7 | SPAC = 안전한 IPO | 대부분 실망 성과 |
| 8 | Spread 만이 발행 비용 | Underpricing + indirect 등 6가지 |

---

## §9 자가점검

1. *VC staged financing* 이유?
2. *IPO underpricing* 원인?
3. *Greenshoe option*?
4. *SEO 의 −3%* 이유?
5. *Value of a right* 공식?
6. *발행 비용 6가지*?
7. *Direct listing vs IPO*?

<details><summary>해답</summary>

1. Option to abandon, discipline, information update, valuation step-up.
2. Winner's curse, info asymmetry, underwriter incentive, signaling, cascade.
3. Over-allotment — 15% 추가 배정권, 수요 강하면 행사, 약하면 시장 매수 stabilize.
4. Myers-Majluf — 경영진이 overvalued 판단 시 equity 발행 → adverse selection signal.
5. $\text{Right} = (P_0 - S)/(N+1) = P_0 - P_X$, $P_X = (N P_0 + S)/(N+1)$.
6. Gross spread, direct expense, indirect, abnormal return, underpricing, greenshoe.
7. Direct listing: no underwriter spread, 기존 주주 매도 (liquidity), 신주 발행 X (자금 조달 아님). IPO: 신주 발행, 자금 조달, underwriter.

</details>

---

## §10 다음 학습으로

- **Ch 21** — Leasing
- **Ch 15** — Long-term financing (recap)
- **Ch 29** — M&A (exit 대안)

---

## §11 한 줄 요약

> **자본 조달 — *VC* (staged, convertible preferred, exit 목표) → *IPO* (underwriter, S-1, roadshow, book building). *Underpricing* (first-day +15-20%, winner's curse) + *long-run underperformance* (−15-20%). *SEO* 발표 −3% (Myers-Majluf). *Rights offering*: right value = $(P_0-S)/(N+1)$. *발행 비용 6가지* (spread + underpricing + indirect 등). *Direct listing / SPAC* 대안. *Staying private longer* 트렌드.**
