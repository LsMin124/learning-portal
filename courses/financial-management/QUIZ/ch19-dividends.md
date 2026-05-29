# Ch 19 Dividends and Other Payouts — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *Dividend 의 4 date*?

<details><summary>답</summary>

| Date | 의미 |
|--|--|
| Declaration | 이사회 결의 |
| Ex-dividend | 이 날 이후 매수자 배당 못 받음 (record −1일) |
| Record | 주주명부 확정 |
| Payment | 실제 지급 |

→ *Ex-date 에 주가 ≈ 배당금만큼 하락* (이론).

**예**: $2 배당, ex-date 전날 $52 → ex-date $50 (이론, tax 무시).

</details>

### Q2. *MM Dividend Irrelevance* + homemade dividend?

<details><summary>답</summary>

**명제**: Perfect market 에서 dividend policy 는 firm value 무관 (MM 1961).

**Homemade dividend**:
- 배당 부족 → 주식 일부 매도 (자가 배당)
- 배당 과다 → 배당 재투자

**가정**: No tax, no transaction cost, no issuance cost, fixed investment, no info asymmetry.

**직관**: Firm value = investment policy (NPV of projects). Dividend = 단지 분배 방식, zero-sum.

→ 실제로는 tax/signaling/clientele 때문에 관련 있음.

</details>

### Q3. *Buyback 의 장점 + 비판*?

<details><summary>답</summary>

**장점**:
1. Tax efficiency (capital gain deferral)
2. Flexibility (의무 아님)
3. No signal commitment (삭감 부담 없음)
4. EPS boost (주식 수 ↓)
5. Undervaluation signal
6. Dilution offset (stock-comp 상쇄)

**비판**:
1. Manipulation (EPS, 경영진 option)
2. Bad timing (고점 매수 — 2007, 2021)
3. Underinvestment (R&D/capex 대신)
4. Debt-funded leverage 증가
5. 정치적 (2022 US 1% excise tax)

**트렌드**: Buyback > Dividend (US 2000s+), Apple $90B+/year, S&P 500 $900B+/year.

</details>

### Q4. 계산 — Dividend vs Buyback 동등성

회사: 100만주, 주가 $50, market cap $50M. Excess cash $5M 분배.

(a) $5M 배당 시 주주 부?
(b) $5M buyback 시 주주 부 (안 판 주주)?

<details><summary>답</summary>

**(a) $5M 배당** ($5/share):
- 주가: $50 − $5 = $45
- 주주: 주식 $45 + cash $5 = **$50** (변동 없음)

**(b) $5M buyback**:
- 매수 주식 수: $5M / $50 = 100,000주
- 남은 주식: 900,000주
- 남은 market cap: $50M − $5M = $45M
- 주가: $45M / 900,000 = **$50** (변동 없음)
- 안 판 주주: 주식 $50 보유, 지분율 ↑

**결론** (perfect market):
- 배당: 모두 cash $5 + 주식 $45
- Buyback: 판 사람 cash $50, 안 판 사람 주식 $50
- *주주 부 동일* ✓ (MM)

**차이는 tax**: 배당 = 즉시 과세, buyback = 양도세 (deferral 가능).

</details>

### Q5. 계산 — Stock split + Stock dividend

회사: 100만주, 주가 $80, EPS $4.

(a) 2-for-1 split 후 주가, 주식 수, EPS?
(b) 25% stock dividend 후?

<details><summary>답</summary>

**(a) 2-for-1 split**:
- 주식 수: 100만 × 2 = **200만주**
- 주가: $80 / 2 = **$40**
- EPS: $4 / 2 = **$2**
- Market cap: 불변 ($80M)
- P/E: 불변

**(b) 25% stock dividend**:
- 주식 수: 100만 × 1.25 = **125만주**
- 주가: $80 / 1.25 = **$64**
- EPS: $4 / 1.25 = **$3.2**
- Market cap: 불변 ($80M)

**핵심**: 둘 다 *cosmetic* — 총 가치, P/E 불변.

**왜 하는가 (signaling)**:
- *Split*: "주가가 높아졌다" (자신감), 거래 편의 (소액 투자자 접근성)
- 단, *Berkshire A* ($600K+)는 split 거부 (장기 투자자 유치)
- *Apple* 여러 차례 split (2020 4-for-1)

</details>

### Q6. 계산 — Lintner model

회사: target payout 40%, adjustment speed 0.3, 작년 배당 $1.50/share, 올해 EPS $5.

올해 배당?

<details><summary>답</summary>

**Lintner**:
$$\Delta Div = Speed \times (Target \times EPS - Div_{prev})$$

- Target dividend = 0.4 × $5 = $2.00
- Gap = $2.00 − $1.50 = $0.50
- Δ Div = 0.3 × $0.50 = $0.15
- **올해 배당 = $1.50 + $0.15 = $1.65**

**해석**:
- *Full adjustment* 면 $2.00 이지만
- *Speed 0.3* 로 점진 조정 → $1.65
- *Dividend smoothing* — 급격한 변화 회피

**왜 점진적**:
- EPS 변동성 > 배당 변동성
- *삭감 회피* 심리
- *Signaling* — 안정성 신호
- 지속 가능한 수준만 인상

</details>

### Q7. 계산 — Total payout yield

회사: 주가 $100, 주식 1억주, 연 배당 $2/share, 연 buyback $300M.

(a) Dividend yield?
(b) Buyback yield?
(c) Total payout yield?

<details><summary>답</summary>

**Market cap** = $100 × 1억 = $10B

**(a) Dividend yield**:
- 총 배당 = $2 × 1억 = $200M
- Dividend yield = $200M / $10B = **2.0%**

**(b) Buyback yield**:
- Buyback yield = $300M / $10B = **3.0%**

**(c) Total payout yield**:
- = 2.0% + 3.0% = **5.0%**

**해석**:
- *Dividend yield 만 보면 2%* — 과소평가
- *Total payout 5%* — 실제 주주 환원
- *Apple* 같은 buyback-heavy 기업 평가 시 critical

**현대 valuation**:
- DDM 대신 *total payout model* (Ch 9)
- $P = (Div + Buyback) / (R - g)$

</details>

### Q8. 디버그 — 배당 삭감 후 주가 급락

회사 X: 20년 연속 배당 인상 (dividend aristocrat) → 갑자기 50% 삭감 발표 → 주가 −30%.

왜 삭감폭(50%)보다 주가 하락이 의미가 큰가?

<details><summary>답</summary>

**Signaling 효과**:

**1. 정보 비대칭**:
- 배당은 *미래 cash flow 신호*
- 20년 인상 → 강한 commitment
- *삭감* = 경영진이 *미래 비관* 신호

**2. 시장 해석**:
- "삭감할 정도로 나쁜가?"
- *Earnings 전망 하향* 추론
- *미래 배당 흐름 전체* 재평가 → DDM value 하락

**3. Clientele 이탈**:
- Dividend aristocrat 추종 펀드 (NOBL)
- 삭감 → index 탈락 → 강제 매도
- Income 투자자 이탈

**4. Sticky dividend 위반**:
- Lintner — 삭감 극도로 회피
- 삭감 = 최후의 수단 신호
- → 충격 증폭

**실제 사례**:
- GE (2017, 2018): 50% → 추가 삭감, 폭락
- Kraft Heinz (2019): 36% 삭감 + write-down, −27% 하루
- Wells Fargo (2020): COVID 80% 삭감
- Boeing (2020): 배당 중단

**대조 — 합리적 삭감**:
- 재투자 기회 명확 + communication 좋으면 수용 가능
- 성장 전환 스토리

**교훈**: 지속 가능 수준만 배당, buyback 으로 유연성, 불가피 시 명확 communication.

</details>

### Q9. 디버그 — Buyback EPS 착시

회사: NI $100M, 주식 1억주, EPS $1.00, 주가 $20. $200M debt 차입 buyback (R_D 5%, T_c 21%).

(a) Buyback 후 EPS?
(b) EPS 증가 = 가치 창출?

<details><summary>답</summary>

**(a) Buyback 후 EPS**:
- 매수 주식: $200M / $20 = 1,000만주
- 남은 주식: 9,000만주
- 추가 interest: $200M × 5% = $10M
- After-tax: $10M × 0.79 = $7.9M
- 새 NI: $100M − $7.9M = $92.1M
- **새 EPS: $92.1M / 9,000만 = $1.023** (+2.3%)

**(b) 가치 창출인가? — 아니다 (착시 가능)**:

1. **EPS ↑ ≠ 가치 ↑**: 분모(주식) 감소, 분자(NI) interest 만큼 감소, mechanical.
2. **Leverage ↑**: 재무 위험 ↑, equity β 상승 (MM Prop II), R_E 상승 → P/E 하락 압력.
3. **진짜 가치 창출 조건**: undervalued 매수 + tax shield + excess cash 대안 부재.
4. **가치 파괴**: overvalued 고점 매수, 재투자 포기, 과도 leverage.

**Manipulation 우려**:
- 경영진 보상 EPS 연동 → buyback 유인
- Option vesting 직전 buyback

**실제**:
- IBM (2010s): $100B+ buyback, revenue 정체, 주가 부진
- Boeing (2013-2019): $43B buyback → 그 후 현금 부족 위기

→ EPS boost 는 mechanical, 가치 창출은 undervaluation + tax shield + 대안 부재 일 때만.

</details>

### Q10. 면접 — *배당 vs buyback 결정*?

<details><summary>답</summary>

**의사결정 framework**:

**1. 먼저 Payout vs Reinvest**:
- 재투자 ROE > 자본비용 → 재투자 (Buffett)
- Excess cash → payout
- Growth firm → 재투자 우선

**2. Dividend vs Buyback**:

**Dividend 선호**: 안정 income clientele, 지속 가능 수준, signaling commitment, agency discipline.

**Buyback 선호**: flexibility, tax efficiency, undervaluation, dilution offset, 변동성 대응.

**3. 실무 mix**:
- 대기업: dividend(안정) + buyback(유연)
- Apple: 소액 dividend + 대규모 buyback
- Berkshire: no dividend + occasional buyback
- Utility/REIT: high dividend

**4. 결정 요인**:

| 요인 | Dividend | Buyback |
|--|--|--|
| Cash flow 안정 | 높을 때 | 변동 시 |
| Tax | 배당 우대 | capital gain 우대 |
| Valuation | 무관 | undervalued 시 |
| Clientele | income | tax-sensitive |
| Stock-comp | — | offset |

**5. 현대 트렌드 (US)**: Buyback dominance (2000s+), total payout 관점, 2022 1% excise tax.

**6. 한국**: 전통 낮은 배당 (재벌 재투자) → Korea discount → 2024 밸류업 프로그램, 행동주의 압력.

**유명 사례**:
- Microsoft (2003): 첫 배당 + buyback
- Apple (2012): 첫 배당 (Jobs 사후) + 대규모 buyback
- Costco: 정기 + special dividend

**best practice**:
1. 재투자 우선 (ROE > WACC)
2. 지속 가능 dividend (삭감 회피)
3. Buyback 유연성 + undervaluation 활용
4. Total payout 일관성
5. Clear communication
6. Tax-aware

> 배당 vs buyback = cash flow 안정성 + tax + valuation + clientele + signaling. 재투자 우선, 그 다음 dividend(안정) + buyback(유연) mix.

</details>
