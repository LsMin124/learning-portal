# Ch 20 Raising Capital — 퀴즈

> 10 문항 (개념 3 / 계산 4 / 디버그 2 / 면접 1).

### Q1. *자금 조달 단계* (bootstrap → exit)?

<details><summary>답</summary>

| 단계 | 자금원 |
|--|--|
| Bootstrap | 창업자, FFF |
| Seed | Angel, accelerator (YC) |
| Series A/B/C | Venture Capital |
| Late stage | Growth equity, crossover |
| Exit | IPO 또는 M&A |

**VC staged financing 이유**:
1. Option to abandon
2. Discipline
3. Information update
4. Valuation step-up

**Term sheet**: liquidation preference, anti-dilution, pro-rata, drag/tag-along, board.

</details>

### Q2. *IPO Underpricing* 원인 + 의미?

<details><summary>답</summary>

**현상**: First-day pop +15-20% (US 평균).

**원인**:
1. Winner's curse (uninformed 보호)
2. Information asymmetry
3. Underwriter incentive (oversubscription)
4. Signaling ("leave good taste")
5. Cascade/bandwagon

**의미**:
- Issuer *money left on table*
- 그러나 *균형 현상* (비합리 아님)

**Long-run**: 3-5년 −15~−20% (Loughran-Ritter) — market timing, lock-up, window dressing.

</details>

### Q3. *SEO 발표 시 −3%* 이유?

<details><summary>답</summary>

**Myers-Majluf (Pecking order)**:
- 경영진이 *overvalued 라고 판단* → equity 발행
- 시장이 신호 해석 → 주가 하락
- *Adverse selection* (lemons problem)

**함의**:
- Equity 발행 = *나쁜 신호* (debt < equity 선호)
- *Pecking order*: 내부자금 > debt > equity
- → Growth firm 도 equity 발행 꺼림

**대조**:
- *Internal financing*: 신호 없음
- *Debt*: 작은 신호
- *Equity*: 가장 부정적 신호

</details>

### Q4. 계산 — Value of a Right

현재가 $60, subscription price $48, 5주당 1 신주 (N=5).

(a) Ex-rights price?
(b) Value of one right?
(c) 100주 보유 주주가 받는 right 수 + 총 가치?

<details><summary>답</summary>

**(a) Ex-rights price**:
$$P_X = \frac{N P_0 + S}{N+1} = \frac{5 \times 60 + 48}{6} = \frac{348}{6} = \$58$$

**(b) Value of one right**:
$$P_0 - P_X = 60 - 58 = \$2$$

(또는 $(60-48)/6 = \$2$)

**(c) 100주 보유**:
- Right 수: 100 (주당 1 right)
- 신주 매수: 100/5 = 20주 (5주당 1)
- Right 총 가치: 100 × $2 = **$200**

**검증 (주주 부 불변)**:
- *행사 전*: 100주 × $60 = $6,000
- *행사*: 100주(현) + 20주(신, $48) → 120주, 추가 투자 $960
  - 가치: 120 × $58 = $6,960, 순투자 $960 → 순 $6,000 ✓
- *Right 매도*: 100주 × $58 + $200 = $6,000 ✓

→ 어느 쪽이든 주주 부 동일.

</details>

### Q5. 계산 — IPO underpricing cost

회사 IPO: 1,000만주 발행, 공모가 $20, first-day close $26.

(a) 조달 자금?
(b) Money left on table?
(c) Underpricing %?

<details><summary>답</summary>

**(a) 조달 자금**:
- 1,000만 × $20 = **$200M** (gross, spread 전)

**(b) Money left on table**:
- (first-day − 공모가) × 발행 주식
- ($26 − $20) × 1,000만 = **$60M**

**(c) Underpricing %**:
- ($26 − $20) / $20 = **30%**

**해석**:
- $60M 을 *first-day 투자자에게* 넘김
- 만약 $26 에 발행했으면 $260M 조달 가능했음
- 그러나 *underpricing 은 균형* (수요 확보, 다음 거래)

**추가 비용 (gross spread 7%)**:
- Spread = $200M × 7% = $14M
- Net to issuer = $186M

**총 발행 비용**:
- Spread $14M + Underpricing $60M = $74M
- → *Underpricing 이 spread 보다 큼*

</details>

### Q6. 계산 — Dilution

회사: 기존 1,000만주, 주가 $50 (market cap $500M), book equity $300M ($30/share).
신주 200만주 발행 @ $50.

(a) Ownership dilution (기존 주주)?
(b) 발행 후 주가 (자금 용도 무관 가정)?
(c) Book value per share 변화?

<details><summary>답</summary>

**(a) Ownership dilution**:
- 기존 주주 지분: 1,000만 / 1,200만 = **83.3%** (100% → 83.3%)
- 신규 주주: 16.7%

**(b) 발행 후 주가**:
- 조달: 200만 × $50 = $100M
- 새 market cap: $500M + $100M = $600M
- 주식 수: 1,200만
- 주가: $600M / 1,200만 = **$50** (불변)
- → *공정가 발행 시 가치 dilution 없음*

**(c) Book value per share**:
- 새 book equity: $300M + $100M = $400M
- BVPS: $400M / 1,200만 = **$33.33** (↑ $30 → $33.33)
- → *발행가 $50 > BVPS $30* → book value *증가* (accretive to book)

**핵심**:
- *Ownership* dilution: 있음 (83.3%)
- *Value* dilution: 없음 (공정가 발행)
- *Book value*: 오히려 증가 (premium 발행)
- → *자금 용도가 positive NPV* 면 주주 이익

</details>

### Q7. 계산 — Firm commitment vs Best effort

회사: 500만주 목표, 공모가 $30.

**Firm commitment** (spread 6%): underwriter 전량 매입.
**Best effort**: 350만주만 판매됨.

각 시나리오 issuer 자금?

<details><summary>답</summary>

**Firm commitment**:
- Underwriter 가 *전량 $30 에 매입* (위험 부담)
- Spread 6% = $1.80/share
- Issuer 수령: 500만 × ($30 − $1.80) = 500만 × $28.20 = **$141M**
- (시장에서 안 팔려도 underwriter 손해)

**Best effort**:
- 350만주만 판매
- Issuer 수령: 350만 × $28.20 = **$98.7M**
- (나머지 150만주 미판매 — issuer 위험)

**비교**:
- *Firm commitment*: 자금 확정 ($141M), underwriter 위험 부담 → 높은 spread
- *Best effort*: 자금 불확실, issuer 위험 → 낮은 spread

**언제 어느 것**:
- *대형 안정 IPO*: firm commitment (대부분)
- *소형/위험 IPO*: best effort
- *현대*: firm commitment 지배적

</details>

### Q8. 디버그 — IPO 첫날 폭등 = 성공?

스타트업 CEO: *"우리 IPO 첫날 +80%! 대성공!"*

진짜 성공인가?

<details><summary>답</summary>

**관점에 따라 다름**:

**투자자(first-day buyer) 관점**: 성공 (+80% 수익).

**Issuer(회사) 관점**: *부분 실패*.

**왜 issuer 손해**:
- *Money left on table* = (첫날가 − 공모가) × 발행 주식
- +80% = *공모가가 80% 저평가*
- 만약 적정가 발행했으면 *80% 더 많은 자금* 조달 가능
- 예: $20 공모 → $36 첫날 → 주당 $16 손실

**Underwriter 관점**: 성공 (쉬운 판매, 다음 거래 확보, 고객 만족).

**과도한 underpricing 의 문제**:
- *과소 조달* (capital 부족)
- *기존 주주 부 희석* (싸게 발행)
- *Underwriter 의 conflict* (issuer vs investor)

**적정 underpricing**:
- *15-20%* 가 일반적 (균형)
- *+80%* 는 *과도* — pricing 실패
- *Direct listing* 이 이 문제 회피 시도

**유명 과도 underpricing**:
- *VA Linux (1999)*: +698% 첫날 (dot-com)
- *Snowflake (2020)*: +112%
- *Airbnb (2020)*: +112%
- *Bumble (2021)*: +63%

**대조 — Facebook (2012)**:
- 첫날 거의 변동 없음 (+0.6%)
- *과대평가 우려* → 적정 pricing (issuer 관점 좋음)
- 단, 단기 주가 하락 (−50% 첫해)

**결론**:
- 첫날 +80% = *투자자 성공*, *issuer 의 pricing 실패*
- 진짜 성공 = *적정 가격 + 자금 목표 달성 + 장기 주가*

</details>

### Q9. 디버그 — Lock-up expiration

회사 IPO 후 6개월: 주가 안정적이었으나, *lock-up 만료일* 직후 주가 −20%.

원인?

<details><summary>답</summary>

**Lock-up expiration 효과**:

**Lock-up 이란**:
- IPO 후 *90-180일* 동안 insider (창업자, VC, 임직원) *매도 금지*
- 목적: *공급 안정*, 시장 신뢰

**만료 직후**:
- *Insider 매도 가능* → 공급 급증
- *VC exit* (펀드 청산 압력)
- *임직원 cash out*
- → 주가 하락 압력

**관찰된 패턴**:
- 만료 *전후 며칠* 주가 약세
- 평균 *−1~−3% abnormal return*
- *변동성 증가*
- 큰 holder 매도 시 더 큼

**예측 가능성 (EMH 위배?)**:
- *Lock-up 만료일은 공개 정보* → 효율시장이면 미리 반영
- 그러나 *실증적으로 만료 후 하락* → anomaly
- *Limits to arbitrage* (공매도 비용, 차입 어려움)

**완화 요인**:
- *강한 펀더멘털* → insider 보유 지속
- *Staggered lock-up* (단계적 해제)
- *대형주* → 흡수 가능

**유명 사례**:
- *Facebook (2012)*: lock-up 만료마다 매도 압력
- *Snap (2017)*: 만료 후 약세
- *많은 SPAC* (2021): 만료 후 폭락

**투자자 전략**:
- *Lock-up 만료일 추적*
- 만료 전 *차익 실현* 고려
- 만료 후 *진입 기회* (가격 하락 시)

**경영진 대응**:
- *명확한 communication*
- *Insider 매도 계획 공시* (10b5-1 plan)
- *Staggered release*

→ Lock-up 만료 = *공급 충격*, 예측 가능하나 실증적 하락 (anomaly).

</details>

### Q10. 면접 — *왜 staying private longer*?

"예전엔 빨리 IPO 했는데, 요즘 유니콘은 10년+ private. 왜?"

<details><summary>답</summary>

**Staying private longer 의 원인**:

**1. Private capital 풍부**:
- *VC/PE 자금 폭증* ($7T+ AUM)
- *SoftBank Vision Fund* ($100B)
- *Crossover funds* (Tiger, Coatue)
- *Mega rounds* — IPO 없이도 수십억 조달

**2. IPO 의 비용/부담**:
- *SOX compliance* (Ch 1)
- *Quarterly earnings pressure* (short-termism)
- *Disclosure* (경쟁자에 노출)
- *Underpricing* (money left on table)

**3. Founder control**:
- *Private* = founder 통제 유지
- *Dual-class* 도 control 수단이나 private 가 더 확실
- *Activist 압력* 회피

**4. Secondary market 발달**:
- *임직원/초기투자자 liquidity* (private 에서도 가능)
- *Forge, EquityZen* 등 플랫폼
- IPO 없이도 cash out

**5. Regulatory**:
- *JOBS Act (2012)*: 500 → 2,000 shareholder 한도 (IPO 강제 완화)
- *Reg D* private placement 확대

**결과 / 함의**:

**기업**:
- *더 성숙한 상태* 로 IPO
- *Higher IPO valuation*
- *Less room for public investor* (가치 상승 분 private 가 가져감)

**Public investor**:
- *유니콘 성장 분 놓침* (IPO 시 이미 고평가)
- *Retail 의 access 감소*
- *부의 불평등* 논란

**Private investor**:
- *더 긴 hold period*
- *Continuation funds* (exit 연장)
- *Secondary 의존*

**대표 사례**:
- *Stripe*: 14년+ private, $50B+ valuation
- *SpaceX*: 20년+ private, $180B+
- *OpenAI*: private, $80B+
- *Airbnb*: 12년 후 IPO (2020)
- *Uber*: 10년 후 IPO (2019)

**대조 (과거)**:
- *Amazon (1997)*: 3년 후 IPO ($438M valuation)
- *Google (2004)*: 6년 후

**트렌드 전망**:
- *Direct listing* 증가 (Spotify, Coinbase)
- *Private secondary* 시장 성장
- *Regulatory* 변화 가능 (retail access 확대 논의)

> Staying private longer = *private capital 풍부* + *IPO 비용/부담* + *founder control* + *secondary liquidity* + *regulatory 완화*. 결과: 더 성숙한 IPO, public investor 의 성장 분 감소.

</details>
