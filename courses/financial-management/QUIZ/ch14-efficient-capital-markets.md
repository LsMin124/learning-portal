# Ch 14 Efficient Capital Markets — 퀴즈

> 10 문항 (개념 3 / 분석 4 / 디버그 2 / 면접 1).

### Q1. *EMH 3 forms* + evidence?

<details><summary>답</summary>

| Form | Info | Evidence |
|--|--|--|
| Weak | Past prices | Random walk, autocorrelation ≈ 0 |
| Semi-strong | All public | Event studies (quick adjustment) |
| Strong | All (insider) | Generally rejected |

**Evidence for**: Event studies, mutual fund underperformance, random walk daily, HFT immediate.

**Evidence against**: Anomalies (size, value, momentum), calendar, bubbles, behavioral.

</details>

### Q2. *Anomalies* (size, value, momentum)?

<details><summary>답</summary>

| Anomaly | Discoverer | Premium | Note |
|--|--|--|--|
| Size | Banz 1981 | 3-5% | Weakened post-1980s |
| Value | FF 1992 | 4-5% | 2010-2020 weak, 2021- revival |
| Momentum | JT 1993 | 8% | Persists countries/assets |

**Interpretation debates**:
- Risk view: priced risk factors
- Behavioral view: mispricing + limits of arbitrage
- Modern AMH: both contribute

**Practical**: Factor ETFs, multi-factor (AQR), smart beta.

</details>

### Q3. *Behavioral biases* 8 + 영향?

<details><summary>답</summary>

| Bias | 영향 |
|--|--|
| Overconfidence | Over-trading, 6.5% annual cost (Barber-Odean) |
| Anchoring | Initial estimate sticky |
| Loss aversion | Hold losers, sell winners (disposition) |
| Mental accounting | Use-specific money |
| Herding | FOMO |
| Confirmation | Beliefs 확인만 |
| Hindsight | "그럴 줄 알았다" |
| Recency | 최근 events over-weight |

**Limits to Arbitrage** (Shleifer-Vishny 1997):
1. Fundamental risk
2. Noise trader risk
3. Implementation costs
4. Career concerns

**AMH** (Lo 2004):
- EMH dynamic
- Anomalies emerge → exploited → fade
- Markets learn

</details>

### Q4. 분석 — Event Study post-earnings drift

회사 positive earnings:
- Day -10 to -1: normal
- Day 0: +5%
- Day +1 to +5: +0.5% drift
- Day +60 to +90: +3% drift

EMH evidence?

<details><summary>답</summary>

**Semi-strong EMH violation**:
- Day 0: +5% quick adjustment (semi-strong consistent)
- Day +1 to +90: +3.5% drift — *anomaly*

**PEAD (Post-Earnings Announcement Drift)**:
- *Bernard-Thomas (1989)* — robust
- *Behavioral underreaction*
- *Limits of arbitrage*

**Causes**:
1. **Underreaction** — conservative belief revision, slow news diffusion
2. **Limits to arbitrage** — transaction cost, short selling
3. **Information uncertainty** — earnings quality

**Strategy**:
- Buy positive surprise → 60-90 day
- 1-3% per quarter alpha
- Transaction cost erodes some

**Studies**:
- Bernard-Thomas 1989 (initial)
- Ball-Bartov 1996 (replication)
- Sadka 2006 (liquidity-adjusted)
- Hirshleifer-Lim-Teoh 2009 (attention)

</details>

### Q5. 분석 — IPO pattern

- First day: +15% (underpricing)
- 6 month: +5%
- 1 year: -5%
- 3 year: -15%
- 5 year: -20%

해석?

<details><summary>답</summary>

**Two phenomena**:

**1. IPO underpricing** (Day 0):
- +15% first-day pop
- Issuer leaves money on table
- Underwriter aggressive pricing

**Why**: Winner's curse, info asymmetry, underwriter inventory.

**2. Long-run underperformance** (3-5 year):
- *Loughran-Ritter (1995)*: -15% 5yr
- Robust across periods/countries

**Why**:
- IPO market timing (sentiment)
- Hot IPO market over-valued
- Mean reversion
- Lock-up expiration (6-12mo)
- Window dressing pre-IPO

**Strategy**:
- Avoid IPO investments
- Wait 1-2 years post-IPO
- Track lock-up expiration

**Disasters**: Webvan 1999, Facebook (first year -50%), Snap, WeWork 2019.

**Winners**: Microsoft 1986, Google 2004.

</details>

### Q6. 분석 — Calendar Effects

- January effect (small-cap) +3%
- Weekend effect -0.18% Monday
- Holiday +0.4% day before

EMH 위반? Exploitable?

<details><summary>답</summary>

**EMH violation**: Predictable patterns.

**Persistence**: 약화 recent.

**Causes**:
- January: tax-loss selling, year-end window dressing, small-cap liquidity
- Weekend: bad news Friday, sentiment, settlement
- Holiday: lower volume, pre-holiday optimism

**Practical exploit**:

**Pros**: Documented historical, free alpha.
**Cons**: Small magnitude, transaction cost > effect, tax inefficiency, persistence weakening.

**Modern**:
- Most weakened (info dissemination)
- Small-cap January persists but small
- Algorithmic arbitrages

**Strategy**:
- Diversified — marginal tilts
- Tax-loss harvesting (capture tax effect)
- Avoid recent holiday speculation

</details>

### Q7. 분석 — Bubble indicators 2024

- CAPE 33 (vs avg 17)
- Margin debt $850B
- IPO frenzy (AI)
- BTC $100K+

Bubble probability?

<details><summary>답</summary>

**Indicators**:

| Indicator | Reading | Likelihood |
|--|--|--|
| CAPE | 33 | High (1929: 31, 2000: 44, 2007: 27) |
| Margin debt | $850B | High |
| IPO frenzy | AI | High |
| BTC ATH | $100K | Mixed |

**Bubble 5 stages**:
1. Displacement (AI) ✓
2. Boom (2023-24) ✓
3. Euphoria — current?
4. Profit taking — not yet
5. Crash

**Scenarios**:
- A: Bubble continues (1-2 year)
- B: Correction soon (12mo)
- C: Slow deflation (multi-year, like 1968-82)

**Hindsight warning**:
- Many false bubble calls
- Schiller 1996 (4yr early)
- Greenspan "irrational exuberance" 1996

**Schiller's 2024 view**:
- CAPE high
- Mean reversion: 4-6%/year forward
- Not necessarily imminent

**Practical**:
1. Don't panic sell
2. Rebalance
3. Diversify
4. Cash buffer
5. Long-term horizon
6. Avoid leverage
7. Tax-efficient

**Survivors**: Buffett 1969 (closed partnership), Druckenmiller 2000.

**Victims**: Newton 1720, many 1929/2000 fortunes.

</details>

### Q8. 디버그 — Active fund underperformance

Manager: *"10 yr -2%/year vs index. 실력 부족?"*

원인?

<details><summary>답</summary>

**4 sources of underperformance**:

**1. Fees** — Active 0.5-1.5% vs Index 0.05% → 0.45-1.45% drag.

**2. Transaction costs** — Turnover 100%+ vs 3%, ~0.5-1% annual.

**3. Tax inefficiency** — Short-term gains, ~0.5-1% drag.

**4. Behavioral biases** — Overconfidence, herding, loss aversion, career risk.

**Mathematical inevitability**:
- Average active = market
- After cost = -1 to -2%
- Zero-sum game

**Studies**: SPIVA 80%+ underperform 10yr.

**Survivorship bias** — true underperformance -2 to -3%.

**Counter — Skill exists**:
- Top 5% persistent
- ID ex ante difficult
- Mean reversion

**Strategy**:

**For most**:
- Index funds (Vanguard, Schwab, Fidelity zero)
- Low cost
- Tax-efficient
- Long-term

**Sophisticated**:
- Factor tilts (smart beta)
- Multi-asset diversification
- Tax-loss harvesting
- Selective active (small-cap, EM)

**Famous failures**: Bill Miller 2008, Berkowitz 2010s, Ackman Valeant 2015.

**Famous successes (rare)**: Buffett 60yr, Renaissance Medallion (2-3 Sharpe), Druckenmiller.

→ Index + low cost + diversification + long-term = winning.

</details>

### Q9. 디버그 — Acquirer's curse

회사 A — 5 acquisitions, 10 yr. 각 announcement:
- Target +25%
- Acquirer -3%

10 yr 후 acquirer -30% vs sector.

해석?

<details><summary>답</summary>

**Acquirer's curse**:

**Announcement returns**:
- Target +25% (control premium)
- Acquirer -1 to -5%
- Combined ~0 to +2% (small synergy)

**Long-run**: 1-3 yr -5 to -10%, 5+ yr -10 to -30%.

**Causes**:

**1. Hubris (Roll 1986)** — overconfidence, winner's curse, empire building
**2. Agency** — manager benefits vs shareholder cost
**3. Method of payment** — stock = signal over-valued
**4. Synergy disappointment** — optimistic projections, integration
**5. Diversification penalty** — conglomerate discount 15-30%

**Famous failures**:

| Deal | Year | 결과 |
|--|--|--|
| AOL-Time Warner | 2000 | $99B write-off |
| Daimler-Chrysler | 1998 | $36B → $7B |
| HP-Compaq | 2002 | Synergy disappointment |
| HP-Autonomy | 2011 | $8.8B write-off |
| Microsoft-Nokia | 2014 | $7.6B write-off |
| GE-Alstom | 2015 | Mistake admitted |

**Famous successes**:
- Berkshire-BNSF 2009 (patient, well-priced)
- Disney-Pixar 2006 (strategic fit)
- Google-YouTube 2006 (visionary)
- Berkshire-Geico 1996 (long-term moat)

**Lessons (CEO)**:
1. Discipline on price
2. Strategic fit > size
3. Cash > stock (confident managers)
4. Cultural integration
5. Realistic synergy
6. Post-audit required

**Lessons (investor)**:
1. Skepticism big M&A
2. Sell on announcement (acquirer)
3. Long-only acquirer underperformance trade
4. Conglomerate spinoffs (value unlock)

**Buffett**:
> *"Most acquisitions don't create value. Acquirers transfer wealth to target shareholders."*

</details>

### Q10. 면접 — Modern market info efficiency?

"AI + HFT + Social media — EMH stronger or weaker?"

<details><summary>답</summary>

**EMH stronger**:

1. **HFT** — microsecond adjustment, arbitrage gone in ms
2. **AI/ML** — pattern recognition, alt data, NLP
3. **Info access** — Bloomberg democratized, SEC EDGAR free
4. **Passive** — index > 50% AUM
5. **Regulatory** — Reg FD, decimalization, SOX

**EMH weaker**:

1. **Coordinated retail** — Reddit WSB, GameStop 2021
2. **Sentiment volatility** — VIX, crypto, FOMO/FUD
3. **AI risk amplification** — flash crashes, crowding
4. **Long-tail mispricing** — small-cap, distressed, EM
5. **HFT limits** — toxic flow, inverted markets

**Net assessment**:

**Where EMH stronger**:
- Large-cap US (FAANG)
- Index components
- Treasury market

**Where EMH weaker**:
- Small-cap (less coverage)
- EM (info asymmetry)
- Distressed (complexity)
- Crypto (sentiment)
- Meme stocks (coordinated)
- Private markets (opaque)

**Investor implications**:

**Large-cap**:
- Index funds (EMH)
- Beating market difficult
- Cost minimization

**Niches**:
- Small-cap active
- EM active
- Distressed specialist
- Quant ML alpha

**AMH (Lo)**:
- EMH 동적
- Anomalies emerge → exploit → fade
- AI accelerates discovery + exploit
- Behavioral biases evolve

**Future trends**:
1. AI-driven price discovery accelerates
2. Retail influence persists
3. Crypto integration
4. Private market growth
5. ESG factors — new frontier
6. Geopolitical risk premium

**Quotes**:
- Buffett: *"Market efficient enough for most."*
- Schiller: *"Market efficiency partial truth."*
- Lo (AMH): *"Markets are adaptive."*

**Practical wisdom**:
1. Most: passive index foundation
2. Sophisticated: factor tilts
3. Specialist: niche active
4. Low cost + long-term + diversification
5. Humility about evolution
6. Adaptability

> Modern market = AI + HFT + Social media + retail democratization. EMH stronger in mega-cap, weaker in niches. AMH adaptive framework. Multi-strategy + low cost + long-term = enduring.

</details>
