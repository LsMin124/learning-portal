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

## §1 The One-Period Case

### §1.1 Future Value (FV)

$$FV = PV \times (1 + r)$$

**예**: $100 at 10% → 1년 후 $110.

### §1.2 Present Value (PV)

$$PV = \frac{FV}{1 + r}$$

**예**: 1년 후 $110 at 10% discount → 현재 $100.

### §1.3 Net Present Value (NPV)

$$NPV = -Cost + PV(future\ cash\ flow)$$

NPV > 0 → 가치 창출, 투자.
NPV < 0 → 가치 파괴, 거부.

---

## §2 The Multi-Period Case

### §2.1 Future Value Compounding

$$FV = PV \times (1 + r)^T$$

T 기간 후 의 future value.

**예** — $100 at 10% for 5 years:
$$FV = 100 \times 1.1^5 = \$161.05$$

### §2.2 Compounding 의 위력

**Albert Einstein**: *"Compound interest is the eighth wonder of the world."*

- $100 at 6% for 30 years → $574
- $100 at 12% for 30 years → $2996

→ Rate doubling = *5x more* (linear 가 아닌 *exponential*).

### §2.3 Rule of 72

> 원금이 *2배* 되는 데 걸리는 시간 ≈ 72 / rate.

- 6% → 12년
- 12% → 6년
- 24% → 3년

### §2.4 Present Value Discounting

$$PV = \frac{FV}{(1 + r)^T}$$

**예** — 10년 후 $1000, r = 8%:
$$PV = \frac{1000}{1.08^{10}} = \$463$$

### §2.5 Finding T or r

**T 찾기** (얼마나 기다려야):
$$T = \frac{\ln(FV/PV)}{\ln(1+r)}$$

**r 찾기** (요구 수익률):
$$r = (FV/PV)^{1/T} - 1$$

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
