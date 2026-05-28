# Chapter 3: Financial Statements Analysis and Financial Models — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 3** (책 p.42~84).
> 3장은 *재무제표 → 의사 결정* 의 *bridge*. **Ratio analysis** + **DuPont identity** + **Financial planning model** (sustainable growth).

이 장의 *지적 무게중심*:
1. **Common-size statements** — 비율로 변환해 *cross-company* 비교
2. **5 ratio category** — liquidity / solvency / efficiency / profitability / market
3. **DuPont identity** — ROE 의 *3 component decomposition*
4. **Financial planning model** — sales 예측 → EFN (External Financing Needed)
5. **Sustainable Growth Rate (SGR)** — 외부 financing 없이 가능한 성장

---

## 들어가기 전에

- **선수 지식**: Ch 2 (재무제표 의 모든 항목)
- **학습 목표**
  1. *Common-size B/S, I/S* — 비율로 변환
  2. *5 ratio* 의 의미 + 산업 별 typical 값
  3. **DuPont** — ROE = profit margin × asset turnover × equity multiplier
  4. *Percentage of sales* 방법 — financial planning 의 base
  5. **SGR** + **IGR** — internal vs sustainable growth
- **예상 학습 시간**: 120~150분

---

## §1 Financial Statements Analysis

### §1.1 *왜* 비율 분석

- Apple 의 NI $100B vs 스타트업 의 NI $1M — *직접 비교 불가*
- *Scale-free* metric 필요

### §1.2 Common-Size Statements

**Common-size B/S** = 각 항목 / Total Assets × 100%.
**Common-size I/S** = 각 항목 / Sales × 100%.

→ *서로 다른 size 의 firm* 도 *직접 비교*.

---

## §2 Ratio Analysis — 5 카테고리

### §2.1 Liquidity Ratios — *단기 viability*

**Current Ratio**:
$$Current\ Ratio = \frac{Current\ Assets}{Current\ Liabilities}$$
- > 1: 단기 obligation 충당 가능
- 산업 표준: 1.5 ~ 3.0

**Quick Ratio** (Acid-test):
$$Quick = \frac{Current\ Assets - Inventory}{Current\ Liabilities}$$

**Cash Ratio**:
$$Cash\ Ratio = \frac{Cash + Securities}{Current\ Liabilities}$$

### §2.2 Long-Term Solvency Ratios

**Debt-to-Equity Ratio**:
$$D/E = \frac{Total\ Debt}{Total\ Equity}$$

**Debt-to-Assets**:
$$D/A = \frac{Total\ Debt}{Total\ Assets}$$

**Interest Coverage** (Times Interest Earned):
$$TIE = \frac{EBIT}{Interest\ Expense}$$
- > 3: 안전
- < 1.5: 위험

**Cash Coverage**:
$$Cash\ Coverage = \frac{EBIT + Depreciation}{Interest}$$

### §2.3 Asset Management / Turnover

**Inventory Turnover**:
$$Inv\ Turnover = \frac{COGS}{Inventory}$$

**Days' Sales in Inventory**:
$$DSI = \frac{365}{Inv\ Turnover}$$

**Receivables Turnover**:
$$AR\ Turnover = \frac{Sales}{Accounts\ Receivable}$$

**Days' Sales Outstanding (DSO)**:
$$DSO = \frac{A/R}{Sales} \times 365$$

**Total Asset Turnover**:
$$TAT = \frac{Sales}{Total\ Assets}$$

### §2.4 Profitability Ratios

**Profit Margin**:
$$PM = \frac{Net\ Income}{Sales}$$

**Return on Assets (ROA)**:
$$ROA = \frac{NI}{Total\ Assets}$$

**Return on Equity (ROE)**:
$$ROE = \frac{NI}{Total\ Equity}$$

### §2.5 Market Value Ratios

**Price-Earnings Ratio (P/E)**:
$$P/E = \frac{Price\ per\ share}{EPS}$$

**Market-to-Book (P/B)**:
$$P/B = \frac{Market\ Cap}{Book\ Equity}$$

**Enterprise Value Multiples**:
$$EV/EBITDA, EV/Sales$$

---

## §3 DuPont Identity — *ROE 분해*

### §3.1 식

$$ROE = \frac{NI}{Equity} = \underbrace{\frac{NI}{Sales}}_{PM} \times \underbrace{\frac{Sales}{Assets}}_{TAT} \times \underbrace{\frac{Assets}{Equity}}_{EM}$$

**해석**:
- **Profit Margin** — 판매 1$ 당 이익
- **Total Asset Turnover** — 자산 1$ 당 매출
- **Equity Multiplier** — leverage (= 1 + D/E)

### §3.2 ROE 의 *3 가지 path*

| | PM | TAT | EM | 전형 |
|--|--|--|--|--|
| **High margin** | High | Low | Low | Luxury (Hermès), Pharma |
| **High turnover** | Low | High | Low | Retail (Walmart) |
| **High leverage** | Mid | Mid | High | Banks, REITs |

**예 — ROE 20% 의 3 방법**:
- Hermès: PM 25%, TAT 0.8, EM 1.0
- Walmart: PM 2.5%, TAT 2.5, EM 3.2
- Bank: PM 25%, TAT 0.07, EM 11.4

---

## §4 Problems with Financial Statement Analysis

### §4.1 한계

1. **Time period** — 일년 vs 분기 의 noise
2. **Industry differences** — *비교 불가*
3. **Accounting methods** — FIFO vs LIFO, depreciation method 차이
4. **Window dressing** — *연말 직전 조정*
5. **Inflation** — historical cost 의 distortion
6. **Seasonal**
7. **International** — GAAP vs IFRS

---

## §5 Financial Planning Model

### §5.1 *Percentage of Sales* Approach

**Step**:
1. Sales 예측 (다음 해)
2. 각 항목 의 *historical sales 비율* 계산
3. 새 sales × 비율 = 새 항목 값
4. *Plug variable* (외부 financing) 로 balance

### §5.2 EFN (External Financing Needed) / AFN

$$EFN = (Asset\ Growth) - (Spontaneous\ Liability\ Growth) - (Retained\ Earnings)$$

**예**:
- Asset 증가 $200
- Spontaneous (A/P 증가) $30
- Retained earnings $120
- **EFN** = $50

→ $50 의 *external financing* (debt or new equity) 필요.

---

## §6 Sustainable + Internal Growth Rate

### §6.1 Internal Growth Rate (IGR)

> *외부 financing 없이* 가능한 최대 성장률.

$$IGR = \frac{ROA \times b}{1 - ROA \times b}$$

- $b$ = retention ratio = 1 − payout ratio

### §6.2 Sustainable Growth Rate (SGR)

> *Capital structure 유지하면서* 가능한 최대 성장률.

$$SGR = \frac{ROE \times b}{1 - ROE \times b}$$

### §6.3 예제

**회사 A**: ROE 20%, Retention 60%.
- $SGR = (0.20 \times 0.60) / (1 - 0.20 \times 0.60) = 13.6\%$

→ 외부 financing 없이 *13.6% growth* 가능.

### §6.4 *SGR 의 의의*

- **현실성 check** — 사장의 "30% 성장" 약속 시 *financing plan* 있어야
- **Capital allocation** — *dividend vs reinvest* trade-off
- **Strategic dialogue** — board 의 *growth vs return* 논의

---

## §7 산업의 *Financial Modeling*

### §7.1 3-Statement Model

1. *Revenue model* — units × price + growth
2. *Cost model* — variable + fixed
3. *Balance sheet projection*
4. *Cash flow projection*
5. *Capital structure assumptions*
6. *Sensitivity analysis*

### §7.2 Tools

- **Excel** — *de facto* (FP&A, investment banking)
- **Python** (pandas, numpy) — programmatic
- **Tableau, Power BI** — visualization
- **Anaplan, Workday Adaptive** — enterprise
- **Causal, Pigment** — modern startup

### §7.3 *Scenario Planning*

- *Base case* — 가장 가능
- *Bull case* — upside
- *Bear case* — downside
- *Stress test* — extreme adverse

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 절대 값 비교 | Common-size 또는 ratio |
| 2 | 모든 industry 같은 ratio | 산업 별 표준 다름 |
| 3 | Current ratio 1.5 = 안전 | Quick + cash ratio 도 |
| 4 | ROE 25% = 우수 | Leverage 가 inflate 가능 — DuPont 확인 |
| 5 | High inventory turnover = 좋음 | 너무 높으면 stockout |
| 6 | P/E 가 valuation 전부 | Growth rate, capital structure 도 |
| 7 | SGR 가 *목표* | *Constraint* |
| 8 | Forecast 의 *single number* | Scenario + sensitivity 필수 |
| 9 | LIFO vs FIFO 무관 | 인플레이션 시 *큰 NI 차이* |
| 10 | Percentage of sales 가 모든 항목 | Fixed cost, lumpy capex 는 별도 |

---

## §9 자가점검

1. *Common-size* B/S, I/S 의 base?
2. *Liquidity* ratio 3 가지?
3. *DuPont identity* + 3 component?
4. *ROE 20%* 의 *3 가지 path*?
5. *Percentage of sales* approach 핵심?
6. *EFN* 공식?
7. *IGR* vs *SGR* 차이?
8. *Financial analysis* 의 5 한계?

<details><summary>해답</summary>

1. B/S: Total Assets. I/S: Sales.
2. Current ratio (CA/CL), Quick ratio (excluding inventory), Cash ratio.
3. ROE = Profit Margin × Asset Turnover × Equity Multiplier.
4. Luxury (high margin), Retail (high turnover), Bank (high leverage).
5. 모든 항목이 sales 비율 → 새 sales × 비율.
6. EFN = Δ Assets − Δ Spontaneous Liab − Retained Earnings.
7. IGR: 외부 financing 0. SGR: capital structure 유지.
8. Time period, Industry, Accounting methods, Window dressing, Inflation.

</details>

---

## §10 다음 학습으로

- **Ch 4** — DCF valuation 의 mathematical foundation
- **Ch 5-7** — NPV, IRR, capital budgeting decision
- **Ch 8-9** — Bond + Stock valuation

---

## §11 한 줄 요약

> **Common-size + 5 ratio. *DuPont* 의 ROE = PM × TAT × EM. *Percentage of sales* + *EFN* + *SGR* 의 financial planning. *Modern modeling* = 3-statement + scenario + sensitivity.**
