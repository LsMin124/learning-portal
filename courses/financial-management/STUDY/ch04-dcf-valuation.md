# Chapter 4: Discounted Cash Flow Valuation — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 4** (책 p.85~132).
> 4장은 *재무의 가장 중심 개념*. **Time value of money** + **Present value** + **Annuity/Perpetuity** + **Compounding**. 이후 모든 chapter 의 *수학적 base*.

이 장의 *지적 무게중심*:
1. **Time Value of Money** — *$1 today > $1 tomorrow*
2. **PV / FV** — discounting + compounding
3. **Annuity + Perpetuity** — *반복 cash flow* 의 *closed form*
4. **Compounding periods** — APR vs EAR
5. **Loan amortization** — *mortgage, car loan* 의 mathematics

---

## §0 도입 — *왜* 돈의 시간가치인가

> **핵심 한 문장**: *오늘의 $1 은 내일의 $1 보다 가치 있다* — 오늘 받으면 *투자해서 이자를 벌 수 있기* 때문.

재무의 거의 모든 질문("이 채권은? 이 주식은? 이 프로젝트는? 이 회사는 얼마인가?")은 결국 하나의 작업으로 환원된다 — **미래 cash flow 를 현재가치로 discount**. 4장은 그 *기계* 를 만든다. 이후 장들은 *어떤 CF 를, 어떤 r 로* 넣느냐의 변주일 뿐, 식 자체는 여기서 끝난다.

**두 방향의 같은 연산**:
- **Compounding** (PV → FV): 현재 금액을 *미래로* 굴린다 — *× (1+r)^T*
- **Discounting** (FV → PV): 미래 금액을 *현재로* 당긴다 — *÷ (1+r)^T*

이 둘은 *같은 화살표의 반대 방향* — 곱하기냐 나누기냐의 차이뿐이다.

**4개 중 1개를 푸는 게임**: $PV,\ FV,\ r,\ T$ — 이 중 *3개를 알면 나머지 1개* 가 나온다.

| 모르는 것 | 푸는 법 | 절 |
|--|--|--|
| FV | compounding | §2.1 |
| PV | discounting | §2.4 |
| r | "요구 수익률" 역산 | §2.5 |
| T | "얼마나 기다려야" | §2.5 |

**왜 이게 전부의 base 인가**: Ch 5(NPV/IRR)·Ch 6(자본예산)·Ch 8(채권)·Ch 9(주식)·Ch 13(WACC) 가 모두 "어떤 cash flow 를 어떤 r 로 discount 하느냐". 4장을 *손가락이 기억할 때까지* 익히면 나머지는 *CF 와 r 을 어디서 구하느냐* 의 문제로 좁혀진다.

---

## §1 The One-Period Case

### §1.1 Future Value (FV)

$$FV = PV \times (1 + r)$$

**예**: $100 at 10% → 1년 후 $110.

### §1.2 Present Value (PV)

$$PV = \frac{FV}{1 + r}$$

**예**: 1년 후 $110 at 10% discount → 현재 $100.

![Figure 4.1 — Cash Flow for Jim Ellis's Sale. 교재 p.86](/courses/financial-management/figures/ch04/fig-4-1.png)

> **직관**: 같은 차를 *지금 $10,000* 에 팔까, *1년 후 $11,424* 에 팔까? 두 금액은 *다른 시점* 에 있어 직접 비교할 수 없다 — *같은 시점으로* 옮겨야 한다. 12% 로 discount 하면 $11,424 의 PV = $10,200 > $10,000 → *기다리는 게 낫다*. Timeline 은 *모든 PV 문제의 출발점* — 흩어진 화살표를 한 시점에 모으는 것.

### §1.3 Net Present Value (NPV)

$$NPV = -Cost + PV(future\ cash\ flow)$$

NPV > 0 → 가치 창출, 투자.
NPV < 0 → 가치 파괴, 거부.

![Figure 4.2 — Cash Flows for Land Investment. 교재 p.87](/courses/financial-management/figures/ch04/fig-4-2.png)

> **직관**: 땅을 *$85,000 에 사서* 1년 후 *$91,000* 에 판다. 좋아 보이지만 — 그 $85,000 을 10% 에 그냥 굴리면 $93,500. 시장 수익률로 따지면 $91,000 의 PV = $82,727, NPV = −85,000 + 82,727 = *−$2,273* < 0 → *거부*. **NPV 의 본질** = "이 투자가 *돈을 시장에 그냥 맡기는 것보다* 나은가?"

![Figure 4.3 — Cash Flows for Investment in Painting. 교재 p.88](/courses/financial-management/figures/ch04/fig-4-3.png)

> **직관**: 그림을 *$400,000* 에 사서 1년 후 *$480,000*(기대값) 에 판다. 10% 로 discount → PV $436,364 > $400,000 → *매수*. 단 $480,000 은 *expected* — 불확실하다. 여기서 r 은 단순 이자가 아니라 *위험에 대한 보상* 까지 담아야 한다 (Ch 10~13 의 risk-adjusted discount rate 의 씨앗).

---

## §2 The Multi-Period Case

### §2.1 Future Value Compounding

$$FV = PV \times (1 + r)^T$$

T 기간 후 의 future value.

**예** — $100 at 10% for 5 years:
$$FV = 100 \times 1.1^5 = \$161.05$$

![Figure 4.5 — Suh-Pyng Ku's Savings Account. 교재 p.90](/courses/financial-management/figures/ch04/fig-4-5.png)

> **직관**: $500 을 7% 에 3년 — 계단처럼 *매년 이자가 원금에 합쳐져* 다음 해 이자의 base 가 커진다. $500 → $535 → $572.45 → $612.52. *이자가 이자를 낳는* 것, 그게 compounding 의 전부다. (계단의 *높이가 점점 커지는* 데 주목 — 정액 증가가 아니다.)

### §2.2 Compounding 의 위력

**Albert Einstein**: *"Compound interest is the eighth wonder of the world."*

- $100 at 6% for 30 years → $574
- $100 at 12% for 30 years → $2996

→ Rate doubling = *5x more* (linear 가 아닌 *exponential*).

![Figure 4.4 — Simple and Compound Interest. 교재 p.90](/courses/financial-management/figures/ch04/fig-4-4.png)

> **직관**: 막대의 *파란 부분* = compound 와 simple interest 의 차이 — "*이자에 붙은 이자*". 1~3년은 작아 보이지만 (그림의 note: *수십 년이면 차이가 막대해진다*), 이게 위 6%/12% 가 30년 후 *5배* 벌어지는 메커니즘이다.

![Figure 4.6 — The Growth of the SDH Dividends. 교재 p.91](/courses/financial-management/figures/ch04/fig-4-6.png)

> **직관**: 같은 compounding 을 *성장하는 cash flow* 에 적용 — 배당 $2.00 → $2.40 → $2.88 (매년 20% 성장). FV 공식 $C\times(1+g)^T$ 가 *원금* 뿐 아니라 *흐름* 에도 적용됨을 보여준다. §4.2 growing perpetuity 의 직관적 토대.

### §2.3 Rule of 72

> 원금이 *2배* 되는 데 걸리는 시간 ≈ 72 / rate.

- 6% → 12년
- 12% → 6년
- 24% → 3년

### §2.4 Present Value Discounting

$$PV = \frac{FV}{(1 + r)^T}$$

**예** — 10년 후 $1000, r = 8%:
$$PV = \frac{1000}{1.08^{10}} = \$463$$

![Figure 4.8 — Compounding and Discounting. 교재 p.94](/courses/financial-management/figures/ch04/fig-4-8.png)

> **직관**: *한 장에 담긴 4장 전체*. $1,000 을 위로 굴리면(compound) 10년 후 $2,367(위 곡선); 미래의 $1,000 을 아래로 당기면(discount) 현재 $422(아래 곡선). **Discounting = compounding 의 거울상** — 같은 9% 곡선을 반대 방향으로 읽을 뿐이다. 가운데 직선은 *simple interest* (이자에 이자가 안 붙어 직선).

![Figure 4.9 — Discounting Bernard Dumas's Opportunity. 교재 p.95](/courses/financial-management/figures/ch04/fig-4-9.png)

> **직관**: *왼쪽* = $7,938 을 8% 에 굴리면 3년 후 $10,000 (compounding). *오른쪽* = 3년 후 $10,000 을 받는 기회 (그 자체). 둘은 *무차별* — 지금 $7,938 받아 굴리든, 3년 뒤 $10,000 받든 같다. PV 가 말하는 *경제적 동등성* 의 그림.

### §2.5 Finding T or r

**T 찾기** (얼마나 기다려야):
$$T = \frac{\ln(FV/PV)}{\ln(1+r)}$$

**r 찾기** (요구 수익률):
$$r = (FV/PV)^{1/T} - 1$$

![Figure 4.7 — Cash Flows for Purchase of Fernando Zapetero's Car. 교재 p.92](/courses/financial-management/figures/ch04/fig-4-7.png)

> **직관**: *r 찾기* 문제. 지금 가치 $10,000 이 5년 후 $16,105 가 되려면 *몇 %*? $(16{,}105/10{,}000)^{1/5} − 1 = 10\%$. 가격(PV)·미래값(FV)·기간(T) 을 알 때 *내재 수익률* 을 역산한다.

![Figure 4.10 — Cash Flows for Tugboat. 교재 p.96](/courses/financial-management/figures/ch04/fig-4-10.png)

> **직관**: 같은 *r 찾기*. 지금 $38,610(건조비) 을 들여 3년 후 $50,000 을 받으려면 *손익분기 이자율*? $(50{,}000/38{,}610)^{1/3} − 1 = 9\%$. 이 9% 가 *break-even rate* — 시장 r 이 9% 보다 *낮으면* 이 거래가 유리하다.

---

## §3 Compounding Periods

### §3.1 APR vs EAR

**APR** (Annual Percentage Rate) — *명목* 연이율.
- 신용카드, mortgage 에 표기

**EAR** (Effective Annual Rate) — *실효* 연이율 (compounding 효과 반영):
$$EAR = (1 + \frac{APR}{m})^m - 1$$

m = compounding 횟수/year.

**예** — APR 12%, monthly compounding (m=12):
$$EAR = (1 + 0.12/12)^{12} - 1 = 12.68\%$$

### §3.2 Continuous Compounding

$$FV = PV \times e^{rT}$$

이자 가 *연속* 으로 계산. 수학적 *극한*.

**예** — $100 at 10% continuous for 1 year:
$$FV = 100 \times e^{0.10} = \$110.52$$

### §3.3 *얼마나 자주 compounding*

| Compounding | EAR (APR 12%) |
|--|--|
| Annual | 12.00% |
| Semi-annual | 12.36% |
| Quarterly | 12.55% |
| Monthly | 12.68% |
| Daily | 12.747% |
| Continuous | 12.750% |

→ Daily ≈ continuous. *Compounding 빈도* 의 효과 한계.

![Figure 4.11 — Annual, Semiannual, and Continuous Compounding. 교재 p.104](/courses/financial-management/figures/ch04/fig-4-11.png)

> **직관**: 왼쪽→오른쪽으로 compounding *빈도* 가 늘어난다 — 연 1회(큰 계단), 반기(잔 계단), 연속(매끈한 곡선). 빈도가 오를수록 곡선은 매끈해지지만 *최종 높이의 증가분은 점점 작아진다* — 위 표의 daily ≈ continuous 가 그 한계의 수치 증거다.

---

## §4 Simplifications — Annuity + Perpetuity

### §4.1 Perpetuity

> *매 기간 같은 cash flow*, *영원히*.

$$PV = \frac{C}{r}$$

**예** — 매년 $100, r = 5%:
$$PV = \frac{100}{0.05} = \$2000$$

**현실 예**:
- *Preferred stock* 의 *고정 배당*
- *Consol bonds* (영국 정부 영구채, 2015 상환)
- 영구 *real estate ground lease*

### §4.2 Growing Perpetuity

> 매 기간 cash flow 가 *g% 성장*.

$$PV = \frac{C_1}{r - g}$$

조건: $r > g$ (그렇지 않으면 무한대).

**예** — 내년 $100, 매년 3% 성장, r = 8%:
$$PV = \frac{100}{0.08 - 0.03} = \$2000$$

**Gordon Growth Model** (Ch 9) 의 base — *주식 가치 평가*.

### §4.3 Annuity

> *매 기간 같은 cash flow*, *T 기간 동안만*.

$$PV = C \times \frac{1 - (1+r)^{-T}}{r}$$

**Annuity factor** (책의 PVIFA table):
$$PVIFA(r, T) = \frac{1 - (1+r)^{-T}}{r}$$

**예** — 5년간 매년 $100, r = 10%:
$$PV = 100 \times \frac{1 - 1.1^{-5}}{0.10} = 100 \times 3.7908 = \$379$$

![Figure 4.12 — Discounting Danielle Caravello's Annuity. 교재 p.111](/courses/financial-management/figures/ch04/fig-4-12.png)

> **직관**: *지연된(delayed) annuity* 의 처리법 — 그림의 2단계. **Step 1**: 4번의 $500(year 6~9) 을 annuity 공식으로 *year 5* 로 당긴다 → $1,584.93. **Step 2**: 그 $1,584.93 을 다시 *year 0* 로 discount → $984.12. annuity 공식은 *첫 지급 1기간 전* 시점의 PV 를 주므로, 늘 *"공식이 떨어뜨려 주는 시점이 어디인지"* 확인하는 게 함정 회피의 핵심.

### §4.4 Growing Annuity

$$PV = \frac{C_1}{r - g} \times \left[1 - \left(\frac{1+g}{1+r}\right)^T\right]$$

**예** — Salary $50K, 3% raise, 30년 일하기, r = 8%:
$$PV = \frac{50000}{0.05} \times \left[1 - (1.03/1.08)^{30}\right] = \$748,316$$

### §4.5 Annuity Due

> Cash flow 가 *기말* 이 아닌 *기초*.

$$PV_{due} = PV_{ordinary} \times (1+r)$$

**예** — 임대료 (보통 기초 지불) — ordinary annuity 의 *(1+r)x*.

---

## §5 Loan Amortization

### §5.1 표준 amortizing loan

매월 *같은 금액* 지불, 시간에 따라 *원금 + 이자 비율 변화*.

**Example — 30년 mortgage**:
- Loan $300,000
- APR 6%, monthly (r = 0.5%)
- 360 months

**Monthly payment**:
$$PMT = \frac{PV \times r}{1 - (1+r)^{-T}} = \frac{300000 \times 0.005}{1 - 1.005^{-360}} = \$1,799$$

**Year 1 — Month 1**:
- Interest: $300,000 × 0.5% = $1,500
- Principal: $1,799 − $1,500 = $299
- → 대부분 이자

**Year 30 — Month 360**:
- Interest: ~$9
- Principal: ~$1,790
- → 대부분 원금

→ *Front-loaded interest*. 초기에 *원금 거의 안 줄어듦*.

### §5.2 Other Loan Types

**Pure discount loan** — 만기에 일시 상환 (Treasury bill).
**Interest-only loan** — 매 기간 이자만, 만기에 원금 (corporate bond).
**Amortizing loan** — 위 표준 (mortgage, car loan).
**Balloon loan** — 일부 amortize + 만기 large payment.

---

## §6 What Is a Firm Worth?

> 4장의 *결정적 질문* — *firm value* 의 계산.

### §6.1 DCF — *모든 future cash flow* 의 PV

$$V_0 = \sum_{t=1}^{T} \frac{CF_t}{(1+r)^t} + \frac{Terminal\ Value}{(1+r)^T}$$

- $CF_t$ = year t 의 *free cash flow* (Ch 2 의 FCF)
- $r$ = *discount rate* (보통 WACC, Ch 13)
- *Terminal Value* — explicit forecast 후 *residual*

### §6.2 Terminal Value 방법

**Gordon Growth (perpetuity)**:
$$TV = \frac{CF_{T+1}}{r - g}$$

**Exit Multiple**:
$$TV = EBITDA_T \times Multiple$$

전형적 multiple — 산업 별 EV/EBITDA.

### §6.3 *DCF 의 sensitivity*

DCF 의 *큰 약점* — Terminal Value 가 *전체 가치 의 60-80%*.

- $g$ 의 *작은 변화* 가 *큰 차이*
- $r$ 의 *작은 변화* 도 동일

**Reverse DCF**:
- "이 주가가 *의미하는* growth rate?"
- 시장의 *implied* assumption 검토

---

## §7 산업의 *DCF 응용*

### §7.1 Investment Banking

- M&A — *target valuation*
- IPO — *pricing*
- Fairness opinion

### §7.2 Equity Research

- *Buy/Hold/Sell* recommendation
- Multi-stage DCF (high growth → stable)
- *Margin of safety* — Buffett 의 30% discount

### §7.3 Private Equity

- *LBO valuation* — *5 year IRR* target
- *Exit assumption* — multiple expansion + EBITDA growth
- *Debt paydown* 의 leverage effect

### §7.4 Real Estate

- *NOI* (Net Operating Income) discount
- *Cap rate* = NOI / Property Value
- *Cap rate* 이 *DCF 의 perpetuity 의 r*

### §7.5 Modern *real options* (Ch 7, 22)

- 전통 DCF 의 *flexibility 무시*
- *Option to expand, abandon, delay*
- *Binomial model, Black-Scholes*

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Nominal vs real rate 혼동 | 일관되게 — nominal CF + nominal rate |
| 2 | Annuity vs annuity due | Due 는 *기초* 지불, ordinary × (1+r) |
| 3 | g ≥ r 의 perpetuity | 무한대 — 식 적용 불가, 다른 stage 분리 |
| 4 | EAR vs APR | Compounding 빈도 확인 |
| 5 | Loan 의 *front-loaded interest* | 초기 원금 거의 안 줄어듦 |
| 6 | Terminal Value 가 전체 의 80%+ | Sensitivity 검토 필수 |
| 7 | Single estimate g | Stage 별 분리 (Ch 9 의 multi-stage DDM) |
| 8 | 같은 nominal CF + 다른 inflation | Real 로 변환 후 비교 |

---

## §9 자가점검

1. *FV* + *PV* 공식?
2. *Rule of 72*?
3. *APR* vs *EAR* + *Continuous compounding*?
4. *Perpetuity* 공식?
5. *Growing perpetuity* 의 조건?
6. *Annuity* 공식?
7. *Mortgage* 의 *front-loaded interest* 의미?
8. *DCF* 의 *Terminal Value* 2 방법?

<details><summary>해답</summary>

1. FV = PV(1+r)^T. PV = FV / (1+r)^T.
2. 원금 2배 시간 ≈ 72/rate.
3. APR = 명목, EAR = 실효 (compounding 반영). Continuous = e^rT.
4. PV = C/r.
5. r > g (그렇지 않으면 무한대).
6. PV = C × [1 - (1+r)^-T] / r.
7. 초기에 *대부분 이자*, 후기에 *대부분 원금*. 초기 원금 거의 안 줄어듦.
8. (1) Gordon Growth: TV = CF / (r-g). (2) Exit Multiple: TV = EBITDA × Multiple.

</details>

---

## §10 다음 학습으로

- **Ch 5** — NPV, IRR, payback — investment rules
- **Ch 6** — Capital investment decisions — incremental CF
- **Ch 9** — Stock valuation — Gordon Growth, multi-stage DDM
- **Ch 13** — WACC — *어떤 r* 을 discount rate

---

## §11 한 줄 요약

> **Time value of money. *FV = PV(1+r)^T*, *PV = FV/(1+r)^T*. *Annuity* (limited) + *Perpetuity* (infinite) 의 closed form. *APR* (명목) vs *EAR* (실효). *DCF* 의 firm valuation = 모든 future FCF 의 PV. *Terminal Value* (Gordon Growth 또는 Exit Multiple) 가 *전체 의 60-80%*.**
