# Ch 13 Cost of Capital — 퀴즈

> 10 문항 (개념 2 / 계산 5 / 디버그 2 / 면접 1).

### Q1. *Cost of equity 3 methods*?

<details><summary>답</summary>

| Method | Inputs | Use |
|--|--|--|
| CAPM | R_f, β, ERP | Industry standard |
| DDM rearranged | D_1, P_0, g | Dividend firm |
| Build-up | R_f, ERP, size, industry, firm | Small/private |

**예 — IBM**:
- CAPM: 4 + 0.9(6) = 9.4%
- DDM: 5/130 + 4 = 7.85%
- Build-up: 9%

**Best practice**: Triangulation + sensitivity range.

</details>

### Q2. *WACC formula*?

<details><summary>답</summary>

$$WACC = \frac{E}{V} R_E + \frac{D}{V} R_D (1 - T_c)$$

**With preferred**:
$$+ \frac{P}{V} R_P$$

**Components**:
- R_E (cost of equity)
- R_D (cost of debt, before tax)
- E, D = market values
- T_c = corporate tax rate

**Why weighted**: Capital provider mix → blended cost.

</details>

### Q3. 계산 — Basic WACC

- E = $800M, D = $200M
- R_E = 14%, R_D = 7%, T_c = 25%

<details><summary>답</summary>

V = $1000M

$$WACC = 0.8(14) + 0.2(7)(0.75) = 11.2 + 1.05 = \mathbf{12.25\%}$$

**Sensitivity by leverage**:
- D/E 50/50: 9.625%
- D/E 75/25 (more debt): 7.4375%

→ More debt → lower WACC (until distress).

</details>

### Q4. 계산 — CAPM vs DDM

- R_f = 5%, β = 1.2, ERP = 6%
- D_1 = $3, P_0 = $50, g = 5%

(a) CAPM?
(b) DDM?
(c) 해석?

<details><summary>답</summary>

**(a) CAPM**: 5 + 1.2(6) = **12.2%**

**(b) DDM**: 3/50 + 5 = **11%**

**(c) 차이 1.2%p**:
1. DDM g 추정 오류 (5% vs 8%?)
2. Market mispricing assumption
3. β 추정 오류 (backward, time-varying)

**Triangulation**:
- Range: 11-12.2%
- Middle: 11.6%
- Sensitivity ±1%

**Industry comparison**: 10-13% — both reasonable.

</details>

### Q5. 계산 — Bottom-up β

4 peers (T_c = 21%):

| Peer | β_L | D/E |
|--|--|--|
| A | 1.5 | 0.3 |
| B | 1.4 | 0.4 |
| C | 1.7 | 0.6 |
| D | 1.3 | 0.2 |

X target D/E = 0.5. β_L?

<details><summary>답</summary>

**Step 1 — Unlever**:
$$\beta_U = \beta_L / [1 + (1-T_c) D/E]$$

| Peer | β_U |
|--|--|
| A | 1.5/1.237 = 1.21 |
| B | 1.4/1.316 = 1.06 |
| C | 1.7/1.474 = 1.15 |
| D | 1.3/1.158 = 1.12 |

**Step 2 — Average**: 1.14

**Step 3 — Re-lever** (D/E = 0.5):
$$\beta_L = 1.14 \times [1 + 0.79 \times 0.5] = 1.14 \times 1.395 = \mathbf{1.59}$$

**Use case**:
- Private firm (no market β)
- Volatile firm
- M&A target
- Project-specific

</details>

### Q6. 계산 — Project-specific WACC

GE conglomerate:
- *Industrial*: peer β 1.0, D/E 0.3
- *Financial*: peer β 0.8, D/E 2.0
- R_f = 4%, ERP = 6%, T_c = 21%, R_D = 5%

각 division WACC?

<details><summary>답</summary>

**Industrial**:
- R_E = 4 + 1.0(6) = 10%
- D/V = 0.3/1.3 = 0.23, E/V = 0.77
- WACC = 0.77(10) + 0.23(5)(0.79) = **8.61%**

**Financial**:
- R_E = 4 + 0.8(6) = 8.8%
- D/V = 2/3 = 0.67, E/V = 0.33
- WACC = 0.33(8.8) + 0.67(5)(0.79) = **5.55%**

**Comparison vs Firm WACC 10%**:

| Division | WACC |
|--|--|
| Industrial | 8.61% (-1.4%) |
| Financial | 5.55% (-4.45%) |

**Implications**:
- Firm WACC 적용 시 financial under-discount, bad projects 채택
- Industrial over-discount, good projects reject

**GE real**:
- Pre-2018: mixed WACC
- 2018 GE Capital divestiture
- Project-specific recognition

</details>

### Q7. 디버그 — Single WACC for All

CEO: *"Firm WACC 10%, 모든 project 적용. Standardization."*

Critique?

<details><summary>답</summary>

**Issues**:

1. **Risk mismatch** — average vs new project
2. **Hurdle distortion** — risk-blind allocation
3. **Wrong incentive** — high-risk gravitate
4. **Strategic blind** — new lines, geography, M&A

**Real failures**:
- **GE pre-2018**: mixed industrial + financial → restructuring
- **GM early 2000s**: GMAC financial wrong WACC → 2009 bankruptcy
- **Conglomerate discount** 15-30%

**Best practice — Project-specific**:

1. *Pure-play* — same business peer
2. *Divisional WACC* — segment own
3. *Subjective adjustment* — ±2-5%
4. *Bottom-up β* (Damodaran)
5. *Real options* — flexibility value

**Capital allocation discipline**:
- Each division own WACC
- Each project risk-adjusted hurdle
- Post-audit
- Reallocation

**Buffett**:
> *"Each project must clear its own hurdle."*

</details>

### Q8. 디버그 — Book vs Market weights

- E book $400M / market $1200M
- D book $300M / market $320M

WACC 차이?

<details><summary>답</summary>

**Book weights**:
- E/V = 57%, D/V = 43%

**Market weights**:
- E/V = 79%, D/V = 21%

**WACC** (R_E = 12%, R_D = 6%, T_c = 21%):

- **Book**: 0.57(12) + 0.43(6)(0.79) = 8.88%
- **Market**: 0.79(12) + 0.21(6)(0.79) = 10.48%

→ Difference 1.6%p — significant.

**Why Market 우선**:
1. Forward-looking
2. Investor expectation
3. Refinancing reality
4. DCF consistency
5. Target structure (Ch 16)

**Book의 valid use**:
- Bank regulator (capital ratios)
- Debt covenant
- Internal accounting
- Tax purposes

**Special**:
- Distressed: target recovery
- Private: industry comparable
- Recent IPO: stabilize 6-12 months

**Real example — Apple**:
- Book equity ~$60B
- Market equity ~$3T (50x)
- Book WACC severely wrong

**Damodaran**:
> *"Always market value. Book defensible use 거의 없음."*

</details>

### Q9. 디버그 — Emerging market WACC

Brazil mining:
- R_f (US) = 4%, β = 1.2, ERP (US) = 6%
- CAPM: R_E = 11.2%

US-based CAPM 충분?

<details><summary>답</summary>

**Issue — Country Risk Premium**:

**Damodaran's CRP**:
$$CRP = Sovereign\ Spread \times \frac{\sigma_{stocks}}{\sigma_{bonds}}$$

**Brazil**:
- Sovereign spread (Brazil-US 10yr): 3%
- Relative volatility: 1.5
- *CRP = 4.5%*

**Adjusted**:
$$R_E = 4 + 1.2(6) + 4.5 = \mathbf{15.7\%}$$

→ Original 11.2% severely under-estimates.

**Country risks**:
1. Sovereign default (historical)
2. Political (election, tax, nationalization)
3. Currency (BRL volatility, inflation)
4. Liquidity (smaller capital market)

**CRP by rating (S&P)**:

| Rating | CRP |
|--|--|
| AAA | 0% |
| AA | 0.5% |
| A | 1.0% |
| BBB | 2.0% |
| BB | 3.5% |
| B | 5% |
| CCC | 8% |
| D | 15%+ |

**Famous examples**:
- Petrobras pre/post-Lula
- Gazprom 2022 sanctions
- Alibaba 2020-21 crackdown
- Argentina hyperinflation

**Modern integrated CAPM**:
- World market portfolio
- Country β
- Currency forward
- Country-specific WACC

</details>

### Q10. 면접 — Modern WACC trends + challenges?

<details><summary>답</summary>

**Traditional challenges**:

1. **β estimation** — time-varying, crisis correlations
2. **ERP debate** — historical 8% vs forward 4-5%
3. **Cost of debt** — rate cycles, refinancing risk
4. **Capital structure** — stock-comp, hybrid, pension, leases
5. **Tax uncertainty** — TCJA, BEPS, Pillar 2

**Modern trends**:

1. **Project-specific WACC** — each hurdle separate
2. **Sustainability-linked WACC** — ESG factors
3. **Real options augmented** — flexibility value
4. **Multi-factor R_E** — beyond CAPM
5. **AI / ML estimation** — forward-looking β
6. **QT era** — higher real rates
7. **Crypto + digital** — no traditional framework

**Industry WACC (2024)**:

| Industry | WACC |
|--|--|
| Utility | 5-7% |
| Mature tech | 8-10% |
| Mature industrial | 9-12% |
| Growth tech | 11-14% |
| Pharma | 9-12% |
| Bank | 8-11% |
| EM | 12-20% |

**Damodaran's view**:
- CAPM baseline (still standard)
- Implied ERP forward
- Bottom-up β
- Country risk explicit
- Sensitivity range

**Sensitivity reporting standard**:
- Base 10%, Low 9%, High 11%
- NPV at each — range

**Quotes**:
- *Damodaran*: *"WACC at best an estimate, at worst a guess. Sensitivity mandatory."*
- *Buffett*: *"I don't use WACC. I use opportunity cost."*
- *Munger*: *"Hurdle rate = best alternative."*

**Behavioral insights**:
- Over-confidence in calculation
- Status quo bias
- Anchoring on prior
- Confirmation bias in input

**Best practice (10 points)**:

1. Multiple methods R_E
2. Bottom-up β
3. Implied ERP forward
4. Market weights
5. Project-specific WACC
6. Country risk for EM
7. Sensitivity range
8. Annual reassessment
9. Post-audit feedback
10. Real options + multi-factor augment

> WACC = useful but imperfect. *Range + sensitivity + judgment*. *Single number false precision avoid*.

</details>
