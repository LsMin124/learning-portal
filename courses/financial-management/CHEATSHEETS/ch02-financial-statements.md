# Ch 2 Financial Statements and Cash Flow — 치트시트

> B/S, I/S, CF / OCF, FCF, FCFF/FCFE / NWC / EBITDA.

## §1 3 재무제표

| | 시간 | 답 |
|--|--|--|
| B/S | 시점 (snapshot) | 무엇 보유? |
| I/S | 기간 | 얼마 벌었나? |
| CF | 기간 | Cash 어떻게? |

## §2 Balance Sheet

```
Assets = Liabilities + Equity
```

```
Current Assets       │  Current Liabilities
  Cash               │    A/P
  Securities         │    Notes payable
  A/R                │    Short-term debt
  Inventory          │
───────────────────  │  ───────────────────
Fixed Assets         │  Long-term Debt
  PP&E (tangible)    │  
  Intangible         │  ───────────────────
                     │  Shareholders' Equity
                     │    Common stock
                     │    Retained earnings
```

## §3 B/S 의 *3 distinction*

| | 의미 |
|--|--|
| Liquidity | Current vs Fixed (1년) |
| Debt vs Equity | 고정 청구 vs residual |
| Value vs Cost | Market vs Book |

## §4 Income Statement

```
Sales
- COGS
= Gross Profit
- SG&A
- D&A
= EBIT
- Interest
= EBT
- Tax
= Net Income
- Dividends
= Retained Earnings
```

## §5 GAAP 의 noncash items

| | I/S | Cash |
|--|--|--|
| Depreciation | 비용 차감 | 없음 (이미 capex) |
| Amortization | 비용 차감 | 없음 |
| Deferred tax | 비용 차감 | 추정 |
| 외상 매출 | 매출 인식 | 없음 |
| 외상 비용 | 비용 인식 | 없음 |

## §6 Tax

| | 의미 |
|--|--|
| Average tax | Total tax / income |
| Marginal tax | 추가 $1 의 세금 |
| US C-Corp (2018+) | 21% flat |
| US Individual | 10~37% progressive |

→ 의사 결정 = marginal.

## §7 Net Working Capital

$$NWC = Current\ Assets - Current\ Liabilities$$

- Positive: standard
- Negative: retailer (Amazon) 의 효율

## §8 Cash Conversion Cycle

$$CCC = DSO + DIO - DPO$$

| 회사 | CCC |
|--|--|
| Amazon | ~-30 days |
| Walmart | ~+5 days |
| Tesla | ~+20 days |

## §9 Operating Cash Flow

$$OCF = EBIT + Depreciation - Taxes$$

또는

$$OCF = NI + Depreciation + Interest$$

## §10 Free Cash Flow

$$FCF = OCF - \Delta NWC - Capex$$

- 모든 capital provider 가용
- DCF valuation 의 input

## §11 FCFF vs FCFE

| | FCFF | FCFE |
|--|--|--|
| 정의 | Firm unlevered | Equity levered |
| 식 | EBIT(1-T) + D&A - ΔNWC - Capex | FCFF - Int(1-T) - Net Debt Repay |
| Discount rate | WACC | $r_E$ |
| 결과 | Enterprise Value | Equity Value |

## §12 Cash Flow Statement (3 activities)

| | 항목 |
|--|--|
| **Operating** | NI + D&A + ΔWC + other |
| **Investing** | -Capex, -M&A, +Divestiture |
| **Financing** | +Debt, -Repay, +Equity, -Buyback, -Dividend |

## §13 EBITDA

$$EBITDA = NI + Interest + Tax + Depreciation + Amortization = EBIT + D\&A$$

**용도**:
- EV/EBITDA multiple
- Capital structure 비교
- Bond covenant

**한계**:
- Capex 무시
- NWC 무시
- Tax, interest 무시

Charlie Munger: *"EBITDA = bullshit earnings"*

## §14 EBITDA 의 *cousin*

| | 의미 |
|--|--|
| Adjusted EBITDA | Management 재량 |
| EBITDAR | + Rent (lease 회피) |
| EBITDA pre-SBC | Stock-based comp 제외 |
| Owner earnings | Buffett 의 진짜 FCF |

## §15 Cash flow red flags

| # | Red flag |
|--|--|
| 1 | NI > OCF (지속) |
| 2 | A/R 매출보다 빠른 증가 |
| 3 | Inventory 매출보다 빠른 증가 |
| 4 | Capex < D&A (asset depletion) |
| 5 | Negative FCF + external financing 의존 |
| 6 | Accrual ratio = (NI - OCF) / Assets ↑ |

## §16 EV vs Equity Value

$$EV = Equity + Debt - Cash$$

- *Enterprise Value* = 모든 capital provider
- *Equity Value* = market cap
- *EV/EBITDA* = capital structure neutral
- *P/E* = equity / NI

## §17 산업의 *capital intensity*

| Industry | Capex/Rev | D&A/Rev |
|--|--|--|
| Software (SaaS) | 1-3% | 1-3% |
| E-commerce | 5-10% | 2-5% |
| Manufacturing | 5-10% | 4-7% |
| Telecom | 15-20% | 15-20% |
| Utility | 15-25% | 8-15% |
| Mining | 10-20% | 10-15% |

→ EBITDA-FCF gap 의 산업 차이.

## §18 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Book = Market | Market > Book 일반 |
| NI = Cash flow | Noncash items |
| EBITDA = FCF | Capex, NWC, tax 무시 |
| Negative NWC = 위험 | Retailer 효율 |
| Depreciation = cash | Noncash |
| Average tax = marginal | 의사 결정 = marginal |
| OCF > 0 = healthy | Capex, NWC 도 |
| Adjusted EBITDA 신뢰 | Management 재량 |

## §19 핵심 mindmap

```
Financial Statements
├── Balance Sheet (snapshot)
│   ├── Assets = L + E
│   ├── Current vs Fixed
│   ├── Debt vs Equity
│   └── Book vs Market
├── Income Statement (period)
│   ├── Sales → EBIT → NI
│   └── GAAP 발생주의 + Noncash items
├── Cash Flow Statement (period)
│   ├── Operating (NI + noncash + ΔWC)
│   ├── Investing (Capex, M&A)
│   └── Financing (Debt, Equity, Dividend)
└── Cash Flow of Firm
    ├── OCF = EBIT + D - T
    ├── FCF = OCF - ΔNWC - Capex
    ├── FCFF (firm, WACC)
    └── FCFE (equity, r_E)
```

## §20 1-line summary

> **B/S (snapshot) + I/S (period) + CF (period). *Cash flow of firm* = OCF − ΔNWC − Capex = FCF. FCFF (WACC, 기업) vs FCFE (cost of equity, 주식). EBITDA 의 한계 (capex, NWC 무시).**
