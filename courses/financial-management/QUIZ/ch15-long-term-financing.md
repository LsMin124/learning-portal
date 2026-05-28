# Ch 15 Long-Term Financing — 퀴즈

> 10 문항 (개념 4 / 분석 3 / 디버그 2 / 면접 1).

### Q1. *Common stock features*?

<details><summary>답</summary>

| Feature | 의미 |
|--|--|
| Voting | Director election |
| Residual claim | Last in liquidation |
| Limited liability | Loss limited |
| Dividend rights | Variable |
| Pre-emptive | Buy new issue first |

**Voting**:
- Cumulative: $\frac{S \times D}{N+1}+1$
- Straight: majority controls all

**Dual-class**: Google, Facebook, Snap. Long-term vs agency.

</details>

### Q2. *Preferred tax advantage*?

<details><summary>답</summary>

- Corporate recipient: **50% exclusion**
- Effective tax: 0.5 × 21% = **10.5%**
- Popular: banks, insurance

**Valuation**: $P = D/R$ (perpetuity)

**Hybrid**: Like debt (fixed) + like equity (perpetual). Priority above common.

**Variants**: Cumulative, Convertible (VC standard), Adjustable rate.

</details>

### Q3. *Bond covenants*?

<details><summary>답</summary>

**Negative**:
- D/E ≤ 2
- No additional debt
- Dividend limit
- No asset sale
- Min interest coverage

**Positive**:
- Submit financials
- Maintain insurance
- Pay taxes
- Normal business

**Purpose**: Protect bondholders, limit agency, reduce default → lower yield.

**Modern trends**:
- Cov-lite loans 80%+ leveraged loans
- Strong credit markets — looser
- Future default risk

</details>

### Q4. *Internal vs External 비율*?

<details><summary>답</summary>

**US 1995-2024**:
- Internal: **70-80%**
- External: 20-30% (Debt 15-20%, Equity 5-10%)

**Pecking Order (Myers-Majluf 1984)**:
1. No flotation cost
2. No info asymmetry signal
3. No dilution
4. Manager autonomy
5. Faster

**Industry**:

| Industry | Internal % |
|--|--|
| Tech growth | 50-70% |
| Utility | 80-90% |
| Pharma | 60-80% |
| Bank | 90%+ |
| Real estate | 30-50% |

</details>

### Q5. 분석 — Underwriting spread

(a) IPO $200M (6.5%)?
(b) SEO $200M (4.5%)?
(c) Bond $500M (1.5%)?

<details><summary>답</summary>

| | Gross | Spread | Net |
|--|--|--|--|
| IPO | $200M | $13M | $187M |
| SEO | $200M | $9M | $191M |
| Bond | $500M | $7.5M | $492.5M |

**Why IPO 비쌈**: Uncertainty, no prior market, distribution, marketing, stabilization.

**Modern**: Direct listing (Spotify 2018, Slack 2019) — no spread.

**Real**:
- Facebook 2012 $16B IPO → $200M fee
- Alibaba 2014 $25B → $300M
- Aramco 2019 $25.6B (sovereign discount)

</details>

### Q6. 분석 — Cumulative vs Straight voting

9 director seats, 1000 shares.

(a) Cumulative — 1 director 선출 shares?
(b) Straight?

<details><summary>답</summary>

**(a) Cumulative**:
$$Shares = \frac{1000 \times 1}{10} + 1 = \mathbf{101}$$

**(b) Straight**: Need > 500 (majority of voted) for *any* director.

**Implications**:

**Cumulative**: Minority protection, proportional, European + some US.

**Straight**: Majority controls all, insider entrenchment, Delaware standard.

**Modern**:
- Staggered board (takeover defense)
- Majority voting (not plurality)
- Proxy access

**Battles**:
- Engine No. 1 vs Exxon (2021) — 3 board seats
- Pershing Square vs CP Rail (2011)

</details>

### Q7. 디버그 — Dual-class agency

회사 X (founder 75% voting):
- Founder pay $50M (median $10M)
- Negative NPV $5B acquisition (-15%)
- Shareholder vote irrelevant

Public protection?

<details><summary>답</summary>

**Failures**:
- WeWork (2019): Neumann dual-class, IPO 취소
- Snap: 0-vote public, absolute control
- Lyft: 20:1 voting, -50% post-IPO

**Successes**:
- Google: Larry/Sergey long-term R&D
- Facebook: Zuckerberg Meta pivot
- Berkshire: Buffett A/B nearly identical voting

**Protections**:

1. **Sunset clauses** — time, ownership, event-based
2. **Independent board** — lead director, committees
3. **Class action** — fiduciary breach, self-dealing
4. **Index restrictions** — S&P 500 (2017) no new dual-class
5. **Stewardship** — BlackRock, Vanguard increasingly vocal
6. **Regulatory** — say-on-pay (Dodd-Frank), proxy advisors

**Damodaran**: *"Dual-class legitimate but abuse mechanism destroys long-term value."*

**Best practice**:
- Sunset mandatory
- Independent majority
- Annual continuation vote
- Transparent disclosure

</details>

### Q8. 디버그 — Convertible debt complexity

회사 - $500M convertible:
- 5% coupon
- $100/share conversion
- Current $80, 5yr

Valuation?

<details><summary>답</summary>

**Decomposition** = Bond + Call option on stock:

1. **Straight bond value** (YTM 7%): $459M
2. **Conversion value**: 5M shares × $80 = $400M (out-of-money)
3. **Option premium**: ~$30-50M (Black-Scholes)
- **Convertible**: ~$490-510M (near par)

**Issuer benefits**:
- Lower coupon (5% vs 7% straight)
- Equity conversion (no cash repay)
- Broader investor base

**Issuer costs**:
- Future dilution
- Complex pricing
- Convertible arbitrage pressure

**Investor benefits**:
- Downside protection (bond floor)
- Upside participation
- Lower volatility than stock

**Investor costs**:
- Lower coupon
- Conversion premium paid
- Issuer call option

**Use cases**:
- Tech: Tesla, Twitter, Netflix
- Distressed: cheap financing
- Mezzanine: PE deals

**Famous**:
- Berkshire-Goldman 2008: $5B + warrant
- Tesla 2014-24: multiple issues
- Twitter 2014: $1.8B

**Arbitrage**:
- Long convertible + short stock
- Citadel, Millennium

</details>

### Q9. 디버그 — Public vs Private debt

회사 X (mid-cap $5B revenue):
- Public bond $500M (5% YTM)
- Bank loan $500M (6% rate)

Trade-off?

<details><summary>답</summary>

**Public bond pros**:
- Lower rate (5% < 6%)
- Wide investor base
- Brand visibility
- Mature profile

**Public bond cons**:
- SEC registration slow
- Disclosure burden
- Rigid indenture
- Public scrutiny

**Bank loan pros**:
- Fast execution
- Negotiable covenants
- Flexible repayment
- Bank monitoring (info value)
- Confidential

**Bank loan cons**:
- Higher rate
- Tighter covenants
- Concentrated risk
- Banking relationship dependence

**Choose public when**:
- Cost-sensitive (1%p large on $500M)
- Large frequent issuer
- Public image
- Investment-grade
- Long maturity

**Choose bank when**:
- Flexibility need
- Small/private
- Distressed (renegotiable)
- Speed
- Confidentiality
- Short-term

**Hybrid**: Both for diversification.

**Modern**:
- Leveraged loans $1.5T market
- Cov-lite 80%+
- Private debt funds $1.5T AUM
- Direct lending non-bank

**Real**:
- Apple: $100B+ bond (low rate access)
- Tesla: convertible + revolver
- Distressed: private debt + restructuring

</details>

### Q10. 면접 — Modern financing trends?

<details><summary>답</summary>

**12 Major trends**:

**1. PE dominance**: $7T+ AUM, IPO age 4 → 10yr, secondary markets, continuation funds

**2. Stock-based comp**: 10-20% tech equity, dilution, buyback offset

**3. ESG / Green**: Green bonds $1T+, sustainability-linked loans, transition bonds

**4. Crowdfunding**: Reg CF, Reg A+, retail access

**5. Crypto / DeFi**: Security tokens, DeFi lending, stablecoin treasury

**6. Direct listing**: Spotify 2018, Slack 2019, Coinbase 2021. No underwriter spread.

**7. SPACs**: 2020-21 boom, mostly disappointing, SEC tightening 2024

**8. Decentralized**: ICO, STO, DAO, smart contracts

**9. Buyback dominance**: Tax-efficient, flexible, Apple $90B/year

**10. Negative yield bonds**: 2010s-2020s European/Japanese pre-2022

**11. CAT bonds**: $50B+ outstanding, natural disaster transfer

**12. Sukuk**: $700B Islamic finance, asset-backed

**Industry implications**:

**Corporate**:
- Multiple options
- Cost + flexibility + signal
- Long-term alignment

**Investor**:
- Wider opportunity set
- Alternative growth
- Private access
- ESG integration

**Future**:

**Growth**:
- PE expansion
- ESG mandatory
- Tokenization (eventually)
- AI analysis

**Decline**:
- Traditional IPO
- Bank loans (private credit replacing)
- Dual-class (sunset standard)

**Quotes**:
- Bogle: *"Index + low cost = winning"*
- Buffett: *"Allocate to best opportunities regardless of structure"*
- Marks: *"Distressed cycles create opportunities"*

> Diverse + complex + evolving. Discipline + adaptability + long-term enduring.

</details>
