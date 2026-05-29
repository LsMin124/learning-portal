# Ch 18 Valuation for the Levered Firm — 퀴즈

> 10 문항 (개념 3 / 계산 5 / 디버그 1 / 면접 1).

### Q1. *APV / FTE / WACC* — cash flow + discount rate?

<details><summary>답</summary>

| 방법 | Cash flow | Discount rate |
|--|--|--|
| APV | Unlevered FCF (UCF) + tax shield 별도 | R_0 + R_D (shield) |
| FTE | Levered (equity) CF | R_E |
| WACC | Unlevered FCF (UCF) | After-tax WACC |

**APV**: $V_U + \sum$ financing effects.
**FTE**: 초기투자 = equity분만, LCF at R_E.
**WACC**: UCF at WACC, tax shield 이미 반영.

→ *Target D/V constant* 하 *셋 다 동일*.

</details>

### Q2. *Financing side effects* 4 가지 (APV)?

<details><summary>답</summary>

1. **Tax shield of debt** (+) — 가장 흔함
2. **Flotation cost** (−) — issuance cost
3. **Cost of financial distress** (−)
4. **Subsidized financing** (+) — 정부 저리 대출

$$APV = V_U + PV(TS) - Flotation - PV(Distress) + Subsidy$$

→ APV 의 강점: 각 효과 *명시적 분리*.

</details>

### Q3. *언제 APV vs WACC*?

<details><summary>답</summary>

| 상황 | 방법 |
|--|--|
| Target D/V *ratio* constant | WACC (간단) |
| Debt *level* 고정/변동 (LBO) | APV |
| 시간에 따라 debt schedule | APV |
| Going-concern 단순 | WACC |

**Rule of thumb**:
- *Ratio 일정* → WACC/FTE
- *Level 변동* → APV

**실무**:
- 기업 valuation: WACC
- LBO/PE: APV (debt paydown)

</details>

### Q4. 계산 — APV (tax shield)

Project: 초기 $-20M, UCF $3M/year 영구, R_0 = 13%, 영구 debt $8M, R_D = 7%, T_c = 25%.

APV?

<details><summary>답</summary>

**NPV (all-equity)**:
$$-20 + \frac{3}{0.13} = -20 + 23.08 = \$3.08M$$

**PV(Tax Shield)**:
$$T_c \times D = 0.25 \times 8 = \$2.0M$$

**APV**:
$$3.08 + 2.0 = \$5.08M$$

→ Tax shield 가 *$2.0M 추가*. Project 채택 (APV > 0).

**해석**: 동일 project 라도 debt financing 으로 *$2M 가치 증가* (tax 절감).

</details>

### Q5. 계산 — LCF + FTE

위 project (Q4):
- 초기 $-20M 중 debt $8M → equity $12M
- E = V_L − D, V_L = V_U + TS = 23.08 + 2.0 = $25.08M → E = $17.08M

(a) Annual LCF?
(b) R_E?
(c) FTE NPV?

<details><summary>답</summary>

**(a) LCF**:
- Interest = $8M × 7% = $0.56M
- LCF = UCF − interest(1−T_c) = $3M − $0.56M(0.75) = $3M − $0.42M = **$2.58M**

**(b) R_E** (MM Prop II with tax):
$$R_E = R_0 + (R_0-R_D)(1-T_c)\frac{D}{E} = 0.13 + (0.06)(0.75)\frac{8}{17.08}$$
$$= 0.13 + 0.0211 = 15.11\%$$

**(c) FTE NPV**:
$$-12 + \frac{2.58}{0.1511} = -12 + 17.08 = \$5.08M$$

→ APV 와 *동일* ✓

</details>

### Q6. 계산 — WACC method 검증

위 project (Q4, Q5):
- E = $17.08M, D = $8M, V = $25.08M
- R_E = 15.11%, R_D = 7%, T_c = 25%

(a) WACC?
(b) WACC NPV?

<details><summary>답</summary>

**(a) WACC**:
$$WACC = \frac{17.08}{25.08}(15.11\%) + \frac{8}{25.08}(7\%)(0.75)$$
$$= 0.681 \times 15.11\% + 0.319 \times 5.25\%$$
$$= 10.29\% + 1.675\% = 11.96\%$$

**(b) WACC NPV**:
$$-20 + \frac{3}{0.1196} = -20 + 25.08 = \$5.08M$$

→ APV, FTE 와 *동일* ✓ — 세 방법 일치 확인.

**핵심**: WACC 는 *UCF $3M* 사용 (LCF 아님), tax shield 는 *WACC 에 이미 반영*.

</details>

### Q7. 계산 — Beta unlever / re-lever

Peers:

| Peer | β_L | D/E |
|--|--|--|
| A | 1.6 | 0.4 |
| B | 1.4 | 0.2 |
| C | 1.8 | 0.7 |

T_c = 21%. 우리 회사 target D/E = 0.5.

(a) 각 β_U?
(b) 평균 β_U?
(c) re-levered β_L?

<details><summary>답</summary>

**(a) Unlever** $\beta_U = \beta_L / [1+(1−T_c)D/E]$:

| Peer | 계산 | β_U |
|--|--|--|
| A | 1.6/(1+0.79×0.4) | 1.6/1.316 = 1.216 |
| B | 1.4/(1+0.79×0.2) | 1.4/1.158 = 1.209 |
| C | 1.8/(1+0.79×0.7) | 1.8/1.553 = 1.159 |

**(b) 평균 β_U** = (1.216 + 1.209 + 1.159)/3 = **1.195**

**(c) Re-lever** (D/E = 0.5):
$$\beta_L = 1.195 \times [1 + 0.79 \times 0.5] = 1.195 \times 1.395 = \mathbf{1.667}$$

**R_E** (R_f = 4%, ERP = 6%):
$$R_E = 4\% + 1.667 \times 6\% = 14.0\%$$

→ Peer 들의 leverage 가 달라도 *β_U 평균* 으로 business risk 추출, 우리 target 으로 re-lever.

</details>

### Q8. 계산 — APV for LBO

LBO: V_U = $100M, R_0 = 14%, R_D = 9%, T_c = 21%. Debt schedule:

| Year | Debt balance |
|--|--|
| 1 | $60M |
| 2 | $45M |
| 3 | $30M |
| 4 | $15M |
| 5 | $0 |

(a) 각 연도 tax shield?
(b) PV of tax shields?

<details><summary>답</summary>

**(a) Annual tax shield** = $T_c \times R_D \times D_t$:

| Year | Debt | TS = 0.21×0.09×D |
|--|--|--|
| 1 | $60M | $1.134M |
| 2 | $45M | $0.851M |
| 3 | $30M | $0.567M |
| 4 | $15M | $0.284M |
| 5 | $0 | $0 |

**(b) PV of tax shields** (discount at R_D = 9%):
$$\frac{1.134}{1.09} + \frac{0.851}{1.09^2} + \frac{0.567}{1.09^3} + \frac{0.284}{1.09^4}$$
$$= 1.040 + 0.716 + 0.438 + 0.201 = \$2.40M$$

**핵심**: *Debt 가 매년 감소* → tax shield 가 *매년 다름* → **APV 가 각 연도 명시** → WACC 의 constant ratio 가정으로는 부정확.

**LBO value creation 3 source**:
1. Tax shield ($2.40M)
2. Operational improvement (margin, efficiency)
3. Multiple expansion (entry vs exit EV/EBITDA)

</details>

### Q9. 디버그 — 세 방법 답이 다름

분석가: *"같은 project 인데 APV $6M, FTE $5M, WACC $7M — 왜?"*

진단?

<details><summary>답</summary>

**이론상 동일** → 불일치 = *계산 오류* 또는 *가정 불일치*.

**WACC 과대 ($7M)**:
- β re-lever 안 함 (peer β 직접)
- Book weight 사용 (market 아님)
- Tax shield 이중 계산

**FTE 과소 ($5M)**:
- 초기 투자에서 debt 미차감 (equity분만 써야)
- R_E 과대 (잘못된 D/E)
- LCF 대신 UCF discount

**APV**:
- Tax shield discount rate (R_D vs R_0) 불일치
- Debt level 가정 불일치

**일관성 체크리스트**:
1. D/E ratio 세 방법 동일?
2. R_E consistent (MM Prop II ↔ WACC)?
3. Market value weight?
4. UCF (APV/WACC) vs LCF (FTE) 구분?
5. 초기투자 — FTE 만 equity분?
6. Tax shield 이중 계산 없음?

**진단 절차**:
- WACC 부터 재계산 → V_L 확정 → E = V_L − D → R_E 재계산 → iterate 수렴.

→ 불일치는 *항상 가정/계산 오류*, 이론 결함 아님.

</details>

### Q10. 면접 — *PE firm 은 왜 APV (WACC 아님)*?

<details><summary>답</summary>

**핵심 — Debt *level* 변동 (ratio 아님)**:

**1. LBO debt paydown**:
- 초기 high leverage (D/V 60-90%)
- FCF 로 debt 매년 상환
- D/V ratio 매년 급감 (constant 아님)
- → WACC 의 *constant ratio 가정 위배*

**2. APV 가 자연스러움**:
- 각 연도 debt balance 명시
- Tax shield 매년 정확
- Debt schedule 모델링 직관적

**3. Value creation 분해**:
- Tax shield / Operational / Multiple expansion 분리
- PE 의 *value bridge* 분석

**4. 실무 LBO model**:
- Sources & Uses
- Debt waterfall (senior → mezz → equity)
- Cash sweep (excess FCF → 상환)
- IRR / MOIC (exit)

**WACC 의 LBO 문제**:
- Constant D/V 가정 → 초기 high leverage 무시
- 순환 문제 심화
- Tax shield 과소평가

**유명 LBO**:
- RJR Nabisco (1989) $25B — "Barbarians at the Gate"
- Dell (2013) $24B
- Hilton (2007) Blackstone — 위기 생존 → $14B 수익
- TXU (2007) $45B — 역대 최대, *2014 파산*

**현대 PE 트렌드**:
- Higher entry multiples (expansion 어려움)
- Operational value-add 강조
- Add-on (buy-and-build)
- Private credit 다양화

> PE 는 *debt level 변동* → **APV** 가 tax shield 정확히 포착. WACC 의 constant ratio 부적합. APV 의 value source 분해도 유리.

</details>
