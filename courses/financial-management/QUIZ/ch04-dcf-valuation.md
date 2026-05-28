# Ch 4 Discounted Cash Flow Valuation — 퀴즈

> 10 문항 (개념 2 / 계산 5 / 디버그 2 / 면접 1).

### Q1. Time value of money — *왜 $1 today > $1 tomorrow*?

3 가지 이유?

<details><summary>답</summary>

1. **Inflation** — 명목 가치 보존도 *구매력* 하락
2. **Risk** — 미래 cash flow 의 *불확실*
3. **Opportunity cost** — 지금 받으면 *재투자* 가능

→ Discount rate $r$ = 이 3 가지 의 *compensation*:
- *Real rate* (inflation 보전 후 의 실질 return)
- *Inflation premium*
- *Risk premium*

**Fisher equation**:
$$1 + r_{nominal} = (1 + r_{real}) \times (1 + inflation)$$

→ 근사: $r_{nom} \approx r_{real} + inflation$.

</details>

### Q2. APR vs EAR — *credit card 의 trap*

신용카드 APR 18%. *실제* 부담 EAR?

<details><summary>답</summary>

**Monthly compounding** (대부분 credit card):
$$EAR = (1 + 0.18/12)^{12} - 1 = (1.015)^{12} - 1 = 19.56\%$$

**Daily compounding** (일부 card):
$$EAR = (1 + 0.18/365)^{365} - 1 = 19.72\%$$

**Continuous**:
$$EAR = e^{0.18} - 1 = 19.72\%$$

→ APR 18% vs *실제* 19.56-19.72%. *1.5%p 차이*.

**Truth in Lending Act (1968)**:
- 미국 — APR 의 *통일 disclosure* 강제
- 그러나 *EAR* 표기는 아님 → 소비자 *오해*

**EU**:
- *EAR* (또는 APRC) 표기 강제

**핵심**:
- *APR* = nominal 비교용
- *EAR* = 실제 부담

</details>

### Q3. 계산 — 단순 PV/FV

(a) $5000 at 7% for 20 years 의 FV?
(b) 10년 후 $50,000 at 5% 의 PV?
(c) $1000 → $2000 at 8% — 얼마나?

<details><summary>답</summary>

**(a)**:
$$FV = 5000 \times 1.07^{20} = 5000 \times 3.8697 = \$19,348$$

**(b)**:
$$PV = \frac{50000}{1.05^{10}} = \frac{50000}{1.6289} = \$30,696$$

**(c)**:
$$T = \frac{\ln(2)}{\ln(1.08)} = \frac{0.693}{0.0770} = 9.0\ years$$

*Rule of 72 check*: 72 / 8 = 9 ✓

</details>

### Q4. 계산 — Perpetuity, Growing Perpetuity

(a) 영구 매년 $5000, r = 6% 의 PV?
(b) 내년 $5000, 매년 3% 성장, r = 8% 의 PV?
(c) (b) 에서 g = 9% — 결과는?

<details><summary>답</summary>

**(a)**:
$$PV = \frac{5000}{0.06} = \$83,333$$

**(b)**:
$$PV = \frac{5000}{0.08 - 0.03} = \frac{5000}{0.05} = \$100,000$$

**(c)** — g = 9%, r = 8% → g > r:
$$PV = \frac{5000}{0.08 - 0.09} = \frac{5000}{-0.01} = -\$500,000$$

→ *수학적 negative* — *경제적 의미 없음*. *영원히 r 보다 빠르게 성장* = 무한대 가치, *불가능*.

**현실의 해결**:
- *Two-stage model* — 첫 stage high g, terminal lower g_T < r
- *Three-stage model* — high → mid → stable
- *Ch 9 의 multi-stage DDM*

</details>

### Q5. 계산 — Annuity

(a) 5년간 매년 $10,000, r = 8% 의 PV?
(b) Retirement — 60세 부터 25년 매년 $50,000 받으려면, 60세 시점 의 *necessary corpus* (r = 5%)?
(c) (b) 의 corpus 를 *30년 동안* monthly $1000 saving 으로 만들 수 있나 (r = 6% annual)?

<details><summary>답</summary>

**(a)**:
$$PV = 10000 \times \frac{1 - 1.08^{-5}}{0.08} = 10000 \times 3.9927 = \$39,927$$

**(b)**:
$$PV = 50000 \times \frac{1 - 1.05^{-25}}{0.05} = 50000 \times 14.0939 = \$704,697$$

**(c)** — Monthly saving annuity 의 FV:
- Monthly r = 6%/12 = 0.5%
- T = 30 × 12 = 360 months
$$FV = 1000 \times \frac{1.005^{360} - 1}{0.005} = 1000 \times 1004.5 = \$1,004,515$$

→ $1.0M > $705K ✓ — *충분*.

**전략적 의미**:
- *Power of compounding* — 30년 monthly $1000 (총 saving $360K) → $1M
- *Time + consistency* 가 *amount* 보다 중요
- *Start early* — 20대 vs 40대 시작 의 *지수적 차이*

</details>

### Q6. 계산 — Mortgage

$400,000 mortgage, 30년, APR 6%.

(a) Monthly payment?
(b) Year 1 의 *total interest* + *principal*?
(c) 30년 총 *interest expense*?

<details><summary>답</summary>

**(a)** — Monthly r = 0.5%, T = 360:
$$PMT = \frac{400000 \times 0.005}{1 - 1.005^{-360}} = \frac{2000}{0.8338} = \$2398.20$$

**(b)** — Year 1:
- Total payment: $2398.20 × 12 = $28,778
- Year 1 interest ≈ $23,800 (initial balance × 6%)
- Year 1 principal ≈ $4,978

→ *12 month 동안 $400K → ~$395K*. *1.2% 만 줄어듦*.

**(c)** — 30년 총:
- Total: $2398.20 × 360 = $863,353
- Principal: $400,000
- **Total interest: $463,353** — *원금보다 많음*

**Lesson**:
- 30년 mortgage 의 *interest > principal*
- *Early payoff* 의 power — $100 extra/month = ~5 year shorter, ~$70K saving

</details>

### Q7. 디버그 — Lottery 의 *jackpot lie*

Lottery 광고: *"$200M jackpot!"*. 그러나 실제 *immediate cash* 는 $100M. 무슨 일?

<details><summary>답</summary>

**Lottery 의 일반 *2 옵션***:

1. **Annuity** (광고된 "jackpot"):
   - 30 years, increasing payment
   - 총 nominal: $200M
   - PV (4% discount): ~$110M

2. **Lump sum** (cash option):
   - *현재* 일시 $100M
   - *광고된 jackpot 의 50-60%*

**Tax**:
- US — federal 24% + state ~5% → 총 ~30%
- $100M lump → ~$70M net
- $200M annuity → ~$140M net (30년 분할)

**실제 winner 선택**:
- Lump sum 선택 ~90%
- 이유: *control*, *invest opportunity*, *unknown future tax rate*

**Famous case**:
- 2016 Powerball $1.586B → 3 winner, 각 lump sum ~$330M after tax

</details>

### Q8. 디버그 — DCF 의 *Terminal Value bias*

Analyst 의 DCF:
- 10 year explicit forecast PV: $50M
- Terminal Value (g=3%, r=10%) PV: $150M
- **Total enterprise value: $200M**

문제?

<details><summary>답</summary>

**Terminal Value = 75% of total** — *큰 의존*.

**Sensitivity**:
- g 3% → 4%: TV 50% ↑ → total ~37% ↑
- r 10% → 9%: TV 17% ↑ → total ~13% ↑

**모범 사례**:

1. **Sensitivity table** — g (2-4%), r (8-12%) 의 grid
2. **Two methods** — Gordon Growth + Exit Multiple 비교
3. **Reverse DCF** — *시장 가격이 의미하는 implicit g* 계산
4. **Triangulation** — DCF + comparable + transaction multiple
5. **Stage division** — High g → Transition → Stable

**Famous DCF disasters**:
- **AOL Time Warner** (2000) — $164B merger, DCF assumed perpetual high g, $99B write-off (2002)
- **Nortel** (2000) — DCF on telecom growth, bankruptcy (2009)

</details>

### Q9. 디버그 — *Inflation adjustment*

회사 forecast:
- Year 1 nominal CF $100, *5% annual growth*
- Discount rate 10%
- Inflation expected 3%

5년 후 *real* CF, *real* discount rate?

<details><summary>답</summary>

**Real growth rate** (Fisher):
$$g_{real} = \frac{1.05}{1.03} - 1 = 1.94\%$$

**Real discount rate**:
$$r_{real} = \frac{1.10}{1.03} - 1 = 6.80\%$$

**Year 5 nominal CF**:
$$100 \times 1.05^4 = \$121.55$$

**Year 5 real CF (2020 dollars)**:
$$\frac{121.55}{1.03^4} = \$108.00$$

**Year 5 nominal PV**:
$$\frac{121.55}{1.10^5} = \$75.49$$

**Year 5 real PV (real CF + real r)**:
$$\frac{108.00}{1.068^5} = \$77.78$$

→ *Approximate 일치* (rounding 차이만).

**핵심 원리**:
- *Consistency*: nominal CF + nominal r, real CF + real r
- *Cross-mixing 금지* — 가장 흔한 실수

</details>

### Q10. 면접 — *DCF 의 limitation 4 + alternative*?

"DCF 가 *gold standard* 인데 *문제* 가 뭐?"

<details><summary>답</summary>

**DCF 의 4 가지 fundamental limitation**:

**1. Garbage In, Garbage Out** — Forecast 의 *주관성*, error compounding.

**2. Terminal Value Dominance** — 전체 가치 의 *60-80%*. Small change → large delta.

**3. Discount Rate Determination** — WACC 의 *주관*, CAPM limitation, country risk premium 의 *judgment*.

**4. Flexibility Ignored** — 전통 DCF 는 *static*. Real options (expand, abandon, delay) 무시.

**Alternative valuation methods**:

| Method | 장점 | 단점 |
|--|--|--|
| **Comparable** | 시장 기반 | Peer 선택, mispricing |
| **Precedent transaction** | Control premium | Sparse data |
| **Asset-based** | Tangible | Intangible 무시 |
| **Real options** | Flexibility | 복잡 |
| **Liquidation** | Distressed | Going-concern 무시 |

**Modern best practice — *Triangulation***:

1. *DCF* — intrinsic, *what should it be worth*
2. *Trading comparable* (EV/EBITDA, P/E) — *what market pays*
3. *Transaction comparable* — *what acquirers pay*

→ 3-5 methods 의 *range* + *judgment* = *valuation*.

**Famous valuation debates**:
- **Tesla** (2020s) — $1T+ valuation 의 DCF justify 어려움
- **Twitter** (2022) — Elon $44B vs analyst $30-40B
- **WeWork** (2019) — $47B → $9B (IPO 취소)

> DCF = *one tool, not the only*. *Damodaran*: *"Valuation is at its core a craft."*

</details>
