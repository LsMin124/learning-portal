# Ch 3 Financial Statements Analysis — 치트시트

> Common-size / 5 Ratios / DuPont / Financial Planning / SGR.

## §1 Common-Size Statements

| | Base |
|--|--|
| B/S | Total Assets |
| I/S | Sales |

→ *Scale-free* comparison.

## §2 5 Ratio Categories

| Category | Measures |
|--|--|
| Liquidity | 단기 viability |
| Solvency | Long-term default |
| Asset Turnover | 효율 |
| Profitability | Margin |
| Market Value | Valuation |

## §3 Liquidity Ratios

| | 공식 | 기준 |
|--|--|--|
| Current | CA / CL | > 1.5 |
| Quick | (CA - Inv) / CL | > 1.0 |
| Cash | Cash / CL | > 0.2 |

## §4 Solvency Ratios

| | 공식 | 의미 |
|--|--|--|
| D/E | Debt / Equity | Leverage |
| D/A | Debt / Assets | Leverage |
| TIE | EBIT / Interest | > 3 안전 |
| Cash Coverage | (EBIT+D&A) / Interest | Cash 기준 |

## §5 Asset Turnover

| | 공식 |
|--|--|
| Inventory T | COGS / Inventory |
| DSI | 365 / Inv T |
| AR T | Sales / A/R |
| DSO | (A/R / Sales) × 365 |
| TAT | Sales / Assets |

## §6 Profitability

| | 공식 |
|--|--|
| Profit Margin | NI / Sales |
| ROA | NI / Assets |
| ROE | NI / Equity |

## §7 Market Value

| | 공식 |
|--|--|
| P/E | Price / EPS |
| P/B | Mkt Cap / Book Equity |
| EV/EBITDA | (MC + Debt - Cash) / EBITDA |
| EV/Sales | EV / Sales |

## §8 DuPont Identity

$$ROE = \underbrace{\frac{NI}{Sales}}_{PM} \times \underbrace{\frac{Sales}{Assets}}_{TAT} \times \underbrace{\frac{Assets}{Equity}}_{EM}$$

## §9 DuPont — 3 Path 의 ROE 20%

| | PM | TAT | EM | Example |
|--|--|--|--|--|
| Luxury | 25% | 0.8 | 1.0 | Hermès |
| Retail | 2.5% | 2.5 | 3.2 | Walmart |
| Bank | 25% | 0.07 | 11.4 | JPM |

## §10 산업 별 Typical Ratios

| Industry | PM | TAT | D/E | EV/EBITDA |
|--|--|--|--|--|
| SaaS | 20-30% | 0.3-0.5 | 0-0.3 | 15-30x |
| E-comm | 2-5% | 1.5-2.5 | 0.5-1 | 8-15x |
| Manufacturer | 5-10% | 1-1.5 | 0.5-1 | 6-10x |
| Retail | 2-5% | 2-3 | 0.5-1 | 6-10x |
| Telecom | 8-15% | 0.4-0.6 | 1-2 | 5-8x |
| Utility | 8-12% | 0.3-0.5 | 1-1.5 | 8-12x |
| Bank | 20-30% | 0.05-0.10 | 10+ | (P/B 0.5-1.5) |

## §11 Financial Planning Model

**Percentage of Sales**:
1. Sales forecast
2. 항목 / Sales 의 historical ratio
3. 새 Sales × 비율
4. Plug variable (external financing)

## §12 EFN

$$EFN = \Delta Assets - \Delta Spontaneous\ Liab - Retained\ Earnings$$

## §13 IGR vs SGR

**IGR** (외부 financing 0):
$$IGR = \frac{ROA \times b}{1 - ROA \times b}$$

**SGR** (capital structure 유지):
$$SGR = \frac{ROE \times b}{1 - ROE \times b}$$

$b$ = retention ratio.

## §14 SGR 의 의미

- *Internal capability* measure
- *Constraint*, not strict 상한
- 더 빠른 = equity issue 또는 operational improvement

## §15 ROE 의 leverage trap

- ROE 가 leverage 로만 ↑ = quality 낮음
- Operating (PM, TAT) 이 sustainable
- DuPont 으로 source 분리

## §16 Cash flow vs accounting

| 항목 | 의도 |
|--|--|
| NI > OCF | Earnings quality 의문 |
| A/R > 매출 증가 | Receivable quality |
| Inventory > 매출 증가 | Unsalable |
| Capex < D&A | Asset depletion |

## §17 Window dressing

- 분기 말 ratio artificial improvement
- Channel stuffing (소매)
- Bill and hold
- Sales discount push

## §18 Famous frauds

| 회사 | 연도 | 수법 |
|--|--|--|
| Enron | 2001 | SPV 부채 숨김 |
| WorldCom | 2002 | Expense capitalization |
| Sunbeam | 1998 | Bill and hold |
| HealthSouth | 2003 | $2.7B fictitious |
| Wirecard | 2020 | Phantom A/R $2B |
| FTX | 2022 | Commingling |

## §19 LIFO vs FIFO

| | LIFO | FIFO |
|--|--|--|
| COGS | 최근 (높음) | 옛것 (낮음) |
| Inventory | 옛것 (낮음) | 최근 (높음) |
| NI (인플레) | 낮음 | 높음 |
| Tax | 적음 | 많음 |
| GAAP | 허용 | 허용 |
| IFRS | **금지** | 허용 |

## §20 핵심 mindmap

```
Financial Statements Analysis
├── Common-Size (B/S / TA, I/S / Sales)
├── 5 Ratios
│   ├── Liquidity (Current, Quick, Cash)
│   ├── Solvency (D/E, TIE)
│   ├── Turnover (Inv, AR, TAT)
│   ├── Profitability (PM, ROA, ROE)
│   └── Market (P/E, P/B, EV/EBITDA)
├── DuPont (ROE = PM × TAT × EM)
│   ├── Luxury (high PM)
│   ├── Retail (high TAT)
│   └── Bank (high EM)
├── Financial Planning
│   ├── Percentage of sales
│   ├── EFN = ΔA - ΔSL - RE
│   ├── IGR (외부 financing 0)
│   └── SGR (capital structure 유지)
└── Limitations
    ├── Industry diff
    ├── Accounting methods
    ├── Window dressing
    └── Inflation
```

## §21 1-line summary

> **Common-size + 5 ratio. *DuPont* 의 ROE = PM × TAT × EM. *Percentage of sales* + *EFN* + *SGR* 의 financial planning. *SGR* = constraint. *Industry-specific* + *cash flow quality* + *window dressing* 검출.**
