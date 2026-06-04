# Chapter 2: Financial Statements and Cash Flow — 학습 노트

> *Corporate Finance* (Ross 12e) **Chapter 2** (책 p.20~41).
> 2장은 *재무제표 의 본질* + *cash flow 의 정확한 정의*. 1장의 cash flow > accounting income 의 *수치 화*.

이 장의 *지적 무게중심*:
1. **Balance Sheet** — Assets = Liabilities + Equity 의 항등식
2. **Income Statement** — *발생주의* 의 함정 (GAAP)
3. **Cash Flow Statement** — 3 activity (operating, investing, financing)
4. **Cash Flow of the Firm** — *재무에서 실제로 사용* 하는 cash flow 정의
5. **Net Working Capital (NWC)** — 단기 viability

---

## 들어가기 전에

- **선수 지식**: 기초 회계 (B/S, I/S 의 항목들)
- **학습 목표**
  1. *3 재무제표* 의 구조 + 상호 관계
  2. *Liquidity, Debt vs Equity, Value vs Cost* 의 distinction
  3. *GAAP vs Cash* 의 격차
  4. **CFO = OCF − ΔNWC − Capex** 의 의미
  5. *Free Cash Flow* (FCF) 의 *valuation* 의의
- **예상 학습 시간**: 90~120분

---

## §0 도입 — 회계 숫자에서 '진짜 현금'으로

1장은 *cash flow 가 가치의 근본 단위* 라 했다. 그런데 재무제표가 보여주는 **순이익(net income)** 은 *발생주의(accrual)* 의 산물 — 외상 매출도 매출로 잡고, 이미 현금을 쓴 자산도 감가상각으로 *수년에 걸쳐* 비용 처리한다. 즉 *장부 이익 ≠ 손에 쥔 현금*.

2장의 임무는 세 재무제표(B/S·I/S·CF)에서 **재무가 실제로 쓰는 현금흐름**을 정확히 뽑아내는 것이다. 핵심 정체식(§4):

$$\text{CF from assets} = \text{CF to creditors} + \text{CF to stockholders}$$

> **직관**: 기업이 자산에서 만든 현금(OCF − ΔNWC − Capex)은 *반드시* 채권자(이자·원금)와 주주(배당·자사주)에게 흘러간다 — 새는 곳이 없다. 이 항등식이 2장의 뼈대이고, 여기서 나오는 FCF 가 4장 DCF valuation 의 입력이 된다.

---

## §1 The Balance Sheet

> *Snapshot 의 firm at a point in time*. 항등식: **Assets = Liabilities + Equity**.

### §1.1 구조

```
ASSETS                      LIABILITIES + EQUITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Assets:             Current Liabilities:
  Cash                        Accounts payable
  Marketable securities       Notes payable
  Accounts receivable         Accrued expenses
  Inventory                   Short-term debt
─────────────              ─────────────
Fixed Assets:               Long-term Debt:
  Tangible (PP&E)             Bonds
  Intangible (patents,        Loans
   goodwill, brand)
                            ─────────────
                            Shareholders' Equity:
                              Common stock
                              Retained earnings
                              Treasury stock (deduction)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Assets       =        Total Liab + Equity
```

### §1.2 3 가지 *distinction*

**(1) Liquidity** — 빨리 cash 로 전환 가능?
- *Current* (1년 이내): cash, securities, A/R, inventory
- *Fixed* (1년 초과): PP&E, intangible
- 더 *liquid* 일수록 *수익률 낮음* (cash = 0%, inventory > 0%)

**(2) Debt vs Equity**:
- *Debt* — 채권자, *고정 청구권* (interest + principal)
- *Equity* — 주주, *residual claim* (debt 갚은 후 나머지)

**(3) Value vs Cost**:
- **Book value** (accounting) = *historical cost* − *depreciation*
- **Market value** (재무) = *현재 시점 의 fair value*
- 일반적으로 *market > book* (성장하는 회사)

### §1.3 책의 *유명한 경고*

> *"Managers and investors care about market values, not book values."*

회계는 *historical cost* 의 *conservative measure*. 의사 결정의 *base* 는 *market value*.

---

## §2 The Income Statement

> *기간 (year, quarter) 의 performance*.

### §2.1 구조

```
Sales (revenue)
- Cost of Goods Sold (COGS)
━━━━━━━━━━━━━━━━━━━
Gross Profit
- Operating Expenses (SG&A, R&D)
- Depreciation & Amortization
━━━━━━━━━━━━━━━━━━━
EBIT (Operating Income)
- Interest Expense
━━━━━━━━━━━━━━━━━━━
EBT (Earnings Before Tax)
- Taxes
━━━━━━━━━━━━━━━━━━━
Net Income (= EAT)
- Dividends
━━━━━━━━━━━━━━━━━━━
Retained Earnings (→ Balance Sheet)
```

### §2.2 GAAP — *발생주의* 의 함정

**Revenue recognition**: 매출은 *판매 시점* (수금 아님). 외상 매출 → A/R 증가.

**Matching principle**: 비용은 *수익 대응 시점* (현금 지출 아님).

**Noncash items**:
- *Depreciation* — 자산 매입 시 *현금 지출 완료*, I/S 엔 *수년 분할*
- *Amortization* — intangible 의 분할
- *Deferred tax* — *세금 추정* 과 *실제 납부* 의 차이

### §2.3 Tax — *marginal* vs *average*

**Average tax rate** = total tax / total income.

**Marginal tax rate** = *추가 $1* 당 세금.

→ *경제적 의사 결정* 의 base 는 *marginal* (예: capex 의 tax shield).

**미국 (2018 TCJA 후)**:
- *C-Corp*: 21% flat
- *Individual*: 10%, 12%, 22%, 24%, 32%, 35%, 37% (progressive)

---

## §3 Net Working Capital (NWC)

> NWC = Current Assets − Current Liabilities.

### §3.1 의미

**Positive NWC**:
- Cash + A/R + inventory > A/P + short-term debt
- *단기 viability* — 1년 안 obligations 충당 가능

**Negative NWC**:
- 위험 (default risk)
- 단 일부 *retailer* 의 *negative NWC* — supplier credit > customer credit (예: Amazon, Walmart) — 자본 효율

### §3.2 ΔNWC — *Investment in working capital*

매출 증가 → A/R + Inventory 증가 → *cash tied up*.

**예** — 회사가 매년 매출 10% 성장:
- 매출 $100 → $110: $10 더 produce 해야 (inventory + A/R)
- *ΔNWC*: ~$2 (가정 NWC = 20% of sales)
- *Free cash flow* 에서 *차감*

→ **성장 의 cost** — capex + NWC 증가.

---

## §4 Cash Flow of the Firm

> 1장에서 본 *cash is fact* 의 *수치화*. 책의 핵심 식.

### §4.1 The Identity

$$\text{CF from assets} = \text{CF to creditors} + \text{CF to stockholders}$$

**CF from assets**:
- Operating cash flow (OCF) − ΔNWC − Capex

**CF to creditors**:
- Interest paid − net new borrowing

**CF to stockholders**:
- Dividends paid − net new equity raised

### §4.2 OCF — Operating Cash Flow

$$OCF = EBIT + Depreciation - Taxes$$

**왜 이 식**:
- EBIT — 영업 이익 (이자 전, 세금 전)
- + Depreciation — *noncash expense* 환원
- − Taxes — *실제* 납부 세금

**대안 표현**:
$$OCF = Net\ Income + Depreciation + Interest$$

### §4.3 Free Cash Flow (FCF)

$$FCF = OCF - \Delta NWC - Capex$$

**해석**:
- OCF — 영업 활동의 cash 생성
- − ΔNWC — 운전자본 투자
- − Capex — 자본 지출
- = *주주 + 채권자 에게 분배 가능* 한 cash

**Valuation 의 base**:
- *DCF valuation* (Ch 4) 의 *input*
- 각 년도의 expected FCF 를 *discount*

### §4.4 *FCFF* vs *FCFE*

**FCFF** (Free Cash Flow to Firm):
$$FCFF = EBIT(1-T) + D\&A - \Delta NWC - Capex$$

- *Unlevered* — debt holder + equity holder 모두에게 가용
- WACC 로 discount (Ch 13)

**FCFE** (Free Cash Flow to Equity):
$$FCFE = FCFF - Interest(1-T) - Net\ Debt\ Repayment$$

- *Levered* — equity holder 만
- Cost of equity ($r_E$) 로 discount

→ FCFF 가 *기업 가치*, FCFE 가 *주식 가치*.

---

## §5 The Cash Flow Statement (GAAP)

> *Indirect method* — Net Income 부터 시작.

### §5.1 3 Activities

**(1) Operating Activities**:
- Net Income
- + Depreciation (noncash)
- + ΔWorking capital items (A/R, inventory, A/P)
- + Other adjustments (stock-based compensation)

**(2) Investing Activities**:
- − Capex
- − Acquisitions
- + Divestitures

**(3) Financing Activities**:
- + New debt issuance
- − Debt repayment
- + Equity issuance (IPO, secondary)
- − Equity buyback
- − Dividends paid

### §5.2 Reconciliation 예제

**Year 시작 cash**: $100
**+ Operating CF**: $50
**− Investing CF**: $30 (capex)
**+ Financing CF**: $20 (new debt $30 − dividend $10)
**Year 끝 cash**: $140

→ 1년 후 cash + $40.

---

## §6 산업의 *Cash Flow Quality*

### §6.1 Earnings vs Cash

**Net Income 이 좋아도 cash flow 가 나쁠 때**:
- A/R 의 *aggressive recognition*
- Inventory *buildup* (수요 misjudgment)
- Capex 의 *understatement*

**Cash flow 가 더 *honest*** — *cash 는 조작 어려움*.

### §6.2 Red flags

1. *Net Income > Operating Cash Flow* — 매년
2. *Receivables* 가 매출보다 *빨리 증가*
3. *Inventory* 가 매출보다 *빨리 증가*
4. *Capex < Depreciation* 지속 — *asset depletion*
5. *Negative FCF* — *external financing* 의존

### §6.3 Modern *non-GAAP* metrics

산업의 *EBITDA*, *Adjusted EBITDA*, *Free Cash Flow* — *non-GAAP*.

**EBITDA**:
- *Earnings Before Interest, Tax, Depreciation, Amortization*
- *Capital structure neutral*
- *Acquisition valuation* 의 표준 (EV/EBITDA multiple)
- 단점: *capex 무시*, *working capital 무시*

**Adjusted EBITDA**:
- Management 의 *재량적* 조정
- *Stock-based comp 제거* (Silicon Valley 의 흔함)
- *Restructuring charge 제외*
- 비판 — *"earnings before bad stuff"*

---

## §7 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Book value = market value | 일반적으로 market > book |
| 2 | Net Income = cash flow | 발생주의의 noncash items |
| 3 | EBITDA = FCF | EBITDA 가 capex, NWC, tax 무시 |
| 4 | Negative NWC = 위험 | Retailer (Amazon, Walmart) 의 *효율* 가능 |
| 5 | Depreciation 이 cash outflow | Noncash. Capex 가 cash |
| 6 | Average tax rate = marginal | 의사 결정엔 marginal |
| 7 | Operating CF > 0 = healthy | Capex, working capital 도 확인 |
| 8 | Adjusted EBITDA 신뢰 | Management 재량 — 보수적 보기 |

---

## §8 자가점검

1. *Balance Sheet* 의 항등식?
2. *Book value* vs *market value* 차이?
3. *Net Income* vs *Cash Flow* 의 *3 가지 noncash item*?
4. *NWC* 의 정의 + *ΔNWC* 의미?
5. *OCF* 의 식?
6. *FCF* 의 식?
7. *FCFF* vs *FCFE* 차이?
8. *EBITDA* 의 한계?
9. *3 activities* 의 cash flow statement?
10. *Cash flow red flags* 5 가지?

<details><summary>해답</summary>

1. Assets = Liabilities + Equity.
2. Book = historical cost − depreciation. Market = 현재 fair value. 일반 market > book.
3. Depreciation, amortization, deferred tax.
4. NWC = Current Assets − Current Liabilities. ΔNWC = 매출 성장 시 A/R + inventory 증가의 cash 묶임.
5. OCF = EBIT + Depreciation − Taxes.
6. FCF = OCF − ΔNWC − Capex.
7. FCFF: 모든 holder 가용, WACC discount. FCFE: equity 만, cost of equity discount.
8. Capex, NWC, tax 무시.
9. Operating (NI + noncash + ΔWC), Investing (capex, M&A), Financing (debt, equity, dividend).
10. (1) NI > OCF (2) A/R 빠른 증가 (3) Inventory 빠른 증가 (4) Capex < D&A (5) Negative FCF.

</details>

---

## §9 다음 학습으로

- **Ch 3** — Ratio analysis, DuPont, financial planning model
- **Ch 4** — DCF — FCF 를 *어떻게 discount*
- **Ch 13** — WACC 계산 — *어떤 rate* 로 discount

---

## §10 한 줄 요약

> **B/S = snapshot (A = L + E). I/S = period performance (발생주의). Cash Flow Statement = 3 activities. *Cash flow of the firm* = OCF − ΔNWC − Capex = FCF. FCFF (WACC discount) vs FCFE (cost of equity). *EBITDA* 의 한계 (capex, NWC 무시).**
