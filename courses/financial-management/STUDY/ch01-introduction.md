# Chapter 1: Introduction to Corporate Finance — 학습 노트

> *Corporate Finance* (Ross, Westerfield, Jaffe, Jordan, 12th ed, 2019) **Chapter 1** (책 p.1~19).
> 1장은 기업재무의 *질문 셋팅* — 무엇을 결정하나, 누가 결정하나, 왜 *value* 가 핵심인가.

이 장의 *지적 무게중심*:
1. **재무의 3 가지 질문** — capital budgeting / capital structure / working capital
2. **기업 형태 3 가지** — sole proprietorship / partnership / corporation
3. **Cash flow 의 *3 요소*** — identification / timing / risk
4. **Goal of financial manager** — *주주 부 극대화* 의 정확한 의미
5. **Agency problem** — manager ↔ shareholder 의 *이해 충돌*
6. **Regulation** — Securities Act 1933, SEC 1934, Sarbanes-Oxley 2002

---

## 들어가기 전에

- **선수 지식**: 회계 기초 (B/S, I/S), 기초 미적분 (없어도 OK)
- **학습 목표**
  1. *재무의 본질적 3 질문* 이해
  2. **Corporation** 이 *왜* 지배적 form 인가 — limited liability + 영속성 + 자본 조달
  3. **Cash flow ≠ accounting income** — 가장 중요한 distinction
  4. **Agency cost** — *모니터링 + bonding + residual loss*
- **예상 학습 시간**: 60~90분

---

## §1 What Is Corporate Finance?

### §1.1 Balance Sheet Model of the Firm

![Figure 1.1 — The Balance Sheet Model of the Firm. 교재 p.2](/courses/financial-management/figures/ch01/fig-1-1.png)

> **직관**: 왼쪽(자산)은 *capital budgeting* 질문 — 어떤 자산에 투자하나. 오른쪽(부채+자본)은 *capital structure* 질문 — 어떻게 조달하나. 둘 사이의 *current assets − current liabilities = net working capital* 이 세 번째 질문(단기 관리)이다. 재무의 3 질문이 한 그림에 담겨 있다.

→ Firm = *자산 + 그 자산을 sustain 하는 capital 조달*.

### §1.2 재무의 3 질문

이 책 전체가 *세 가지 질문* 에 답하는 구조:

1. **Capital budgeting** (long-term assets)
   - "어떤 *장기 자산* 에 투자할 것인가?"
   - Part II (Ch 4-9) 의 주제
   - 도구: NPV, IRR, Payback, Real Options

2. **Capital structure** (long-term liabilities + equity)
   - "*자본 조달* 을 어떻게 — debt vs equity?"
   - Part IV (Ch 14-19) 의 주제
   - 도구: MM, trade-off theory, pecking order

3. **Working capital management** (short-term)
   - "*단기 cash flow* 를 어떻게 관리?"
   - Part VII (Ch 26-28) 의 주제
   - 도구: cash cycle, inventory model, credit policy

### §1.3 Financial Manager 의 위치

![Figure 1.2 — Hypothetical Organization Chart. 교재 p.3](/courses/financial-management/figures/ch01/fig-1-2.png)

- **Treasurer**: cash management, capital expenditure, financial plan
- **Controller**: accounting, tax, internal audit

> **직관**: CFO 아래 *Treasurer*(미래 지향 — 현금·자본조달·투자)와 *Controller*(과거 기록 — 회계·세무·감사)로 갈린다. 재무 의사결정(Treasurer)과 재무 보고(Controller)의 분리.

---

## §2 The Corporate Firm — 3 가지 form

| | Sole Proprietorship | Partnership | Corporation |
|--|--|--|--|
| Setup cost | 최소 | 중간 | 큼 (incorporation 비용) |
| Liability | *Unlimited* (개인 자산) | *Unlimited* (general) | **Limited** (주식 가격까지만) |
| Life | 소유자 한정 | 일부 파트너 의존 | **영속 (perpetual)** |
| Tax | 개인소득세 | 개인소득세 (pass-through) | **이중 과세** (법인세 + 배당세) |
| Ownership transfer | 매각 | 어려움 | *주식 양도 자유* |
| Capital raising | 개인 자산 한계 | 파트너 자산 합 | **무제한 (주식 시장)** |

### §2.1 Corporation 의 *지배적* 이유

- **Limited liability** — 주주가 *주식 투자액* 까지만 책임
- **Perpetual life** — 소유자 변경 시에도 *법인 지속*
- **Easy transfer** — 주식 시장에서 *liquidity*
- **Massive capital** — IPO, secondary offering 으로 *수억 달러*

대가:
- **Double taxation** — 법인세 + 배당 소득세
- **Agency cost** — manager ≠ owner

### §2.2 LLC — 새 form

**LLC** (Limited Liability Company):
- *Partnership 의 tax* (pass-through) + *Corporation 의 limited liability*
- 1977 Wyoming 처음, 2000s 일반화
- *Hybrid* — IRS 가 LLC 의 corporate-like 여부 판정

### §2.3 국제 비교

| 국가 | 명칭 | 의미 |
|--|--|--|
| 미국 | Inc., Corp. | corporation |
| 영국 | PLC, Ltd. | public/private limited |
| 독일 | AG, GmbH | Aktiengesellschaft / mit beschränkter Haftung |
| 일본 | 株式会社 (KK) | joint stock company |
| 한국 | 주식회사 | joint stock company |

---

## §3 Importance of Cash Flows

> *"The key to understanding how value is added is cash flows."*

회계 이익 (accounting income) ≠ cash flow. 가치 평가의 *근본 단위* 는 cash flow.

![Figure 1.3 — Cash Flows between the Firm and the Financial Markets. 교재 p.8](/courses/financial-management/figures/ch01/fig-1-3.png)

> **직관**: 기업과 금융시장 사이 현금흐름 — (A) 증권 발행으로 자금 조달 → (B) 자산에 투자 → (C) 현금 창출 → 일부는 정부에 세금(D), 일부는 유보(E), 나머지는 주주·채권자에 배당·이자(F). **가치 창출 조건: 시장에 돌려주는 F > 시장에서 조달한 A.**

### §3.1 Identification — 무엇이 cash flow 인가

| 항목 | Cash Flow? |
|--|--|
| 매출 ↔ 외상 매출금 | *매출은 즉시 X*. 수금 시 cash flow |
| 감가상각비 | *비용이지만 cash flow 아님* (이미 자본 지출 시 발생) |
| 이자 지급 | Cash outflow |
| 배당 지급 | Cash outflow (financing activity) |
| Capex (자산 매입) | Cash outflow (investing activity) |

→ 회계의 *발생주의* vs 재무의 *현금주의*.

### §3.2 Timing — *언제* 발생

> "$1 today > $1 tomorrow" (time value of money)

같은 금액이라도 *언제 받느냐* 가 가치를 결정. 4장 의 *discounted cash flow* 의 base.

### §3.3 Risk — *얼마나 확실*

- Risk-free (US Treasury) — 명목 가치 보장
- Corporate bond — credit risk
- Equity — 가장 큰 불확실성

→ *Required return* 이 risk 따라 다름 (Ch 11 CAPM).

---

## §4 Goal of Financial Manager

### §4.1 가능한 목표들

- 이익 최대화 — *언제* 이익? *얼마나 risky*?
- 매출 극대화 — 손해 보면서 매출 늘릴 위험
- 시장 점유율 — 단기 vs 장기
- 임직원 만족 — important but 측정 어려움

### §4.2 정답: *주주 부의 극대화*

> *Maximize the current value of the firm's existing stock*.

**왜 이게 정답**:
- *측정 가능* — 주가
- *Time + risk 둘 다 포함* — market 이 평가
- *장기 vs 단기 통합* — 미래 cash flow 의 present value

### §4.3 Stakeholder vs Shareholder

**Stakeholder view**:
- 직원, 고객, 공급업체, 지역사회, 환경
- 모두 firm 의 *이해당사자*

**Shareholder view (Milton Friedman)**:
- *주주 부 극대화* 가 social goal
- 다른 stakeholder 보호 = 법 + 규제

**현대 절충 — ESG**:
- *Long-term shareholder value* 가 *stakeholder 보호* 와 *어차피 일치*
- BlackRock 의 Larry Fink, Business Roundtable 2019 의 *stakeholder capitalism*

---

## §5 Agency Problem — Owner ↔ Manager

### §5.1 Agency Relationship

> Principal (주주) 이 *대리인* (manager) 에게 *경영 위임*. 그러나 이해 일치 안 됨.

**Conflict 의 예**:
- Manager 의 *과도한 perks* (corporate jet, 사무실)
- Manager 의 *empire building* — 본인 회사 확장으로 *power, salary* ↑ (주주 부 하락해도)
- Manager 의 *risk aversion* — 본인 직장 안전 vs 주주의 risk-taking 선호
- Manager 의 *short-term* — bonus 기준 vs 주주의 long-term

### §5.2 Agency Cost 의 3 종

1. **Monitoring** — 주주의 *감시 비용* (board, audit, regulator)
2. **Bonding** — manager 의 *자기 구속* (stock ownership, performance bonus)
3. **Residual loss** — 위 두 가지로도 *완전 해결 안 됨*

### §5.3 통제 메커니즘

- **Board of directors** — *주주 대리*
- **Executive compensation** — *stock option, RSU* 로 *이해 일치*
- **Takeover threat** — *경영 부진 시 hostile takeover*
- **Activist investor** — Carl Icahn, Pershing Square
- **Proxy fight** — 의결권 위임 경쟁

---

## §6 Regulation

### §6.1 Securities Act 1933

대공황 후 *securities fraud* 방지:
- IPO 시 *registration statement* + *prospectus* 제출
- *Material information* 의 *full disclosure*

### §6.2 Securities Exchange Act 1934

- **SEC** 설립
- 상장 후 *주기적 disclosure*: 10-K (연), 10-Q (분기), 8-K (event)
- Insider trading 규제 (Section 16)
- *Proxy* 규정

### §6.3 Sarbanes-Oxley Act 2002 (SOX)

Enron, WorldCom 회계 사기 후:
- *CEO/CFO 의 personal certification* — 회계 정확성 서명
- *Internal control* 의 documentation + audit
- *Independent audit committee*
- *PCAOB* (Public Company Accounting Oversight Board) 신설
- *Whistleblower* 보호

### §6.4 Dodd-Frank Act 2010

2008 금융위기 후:
- *Volcker Rule* — 은행의 proprietary trading 제한
- *CFPB* (Consumer Financial Protection Bureau)
- *Say-on-pay* — 주주의 executive comp 의결권

### §6.5 JOBS Act 2012

- IPO 규제 완화 (emerging growth company)
- *Crowdfunding* 의 합법화

---

## §7 산업의 현대 trend

### §7.1 Private equity 의 부상

- 1980s LBO 의 시대 (KKR, Blackstone)
- 현대 — *수조 달러 AUM*
- *Private 의 매력* — public market 의 *short-termism* + *disclosure burden* 회피

### §7.2 Tech 회사의 *founder control*

- *Dual-class stock* — Google, Facebook, Snap
- Founder 의 *지속적 control*
- *Agency problem* 의 *역설* — agent 가 *principal 위*

### §7.3 ESG + Sustainable finance

- *Climate-related disclosure* (SEC 2024)
- *Sustainability-linked debt*
- *Impact investing*

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "Profit maximization = firm value max" | Profit 의 *timing + risk* 무시. *Value* 가 정답 |
| 2 | Accounting income = cash flow | 발생주의 vs 현금주의. 감가상각, 외상 매출 등 |
| 3 | Corporation 만 큰 회사 | LLC 가 *small-medium* 의 dominant form |
| 4 | Limited liability = no personal risk | Founder 의 *personal guarantee* (작은 회사) 흔함 |
| 5 | Agency problem = manager 의 사기 | Subtle — perks, empire, short-termism |
| 6 | SOX 가 모든 fraud 막음 | Theranos, FTX 등 — *enforcement gap* |
| 7 | Stakeholder = shareholder 와 충돌 | 현대 — *long-term shareholder = stakeholder* |
| 8 | Goal 이 단기 주가 | *Current value of existing stock* = 장기 expected value |

---

## §9 자가점검

1. 재무의 *3 가지 질문*?
2. *Corporation* 의 *3 가지 장점*?
3. *Cash flow* vs *accounting income* 의 차이?
4. *3 요소* (identification, timing, risk) 의 의미?
5. *주주 부 극대화* 가 *정답* 인 이유?
6. *Agency problem* 의 *3 가지 cost*?
7. *SOX* 의 핵심 4 가지?
8. *Dual-class stock* 의 의미?

<details><summary>해답</summary>

1. Capital budgeting (어떤 자산?), Capital structure (어떻게 조달?), Working capital (단기 cash 관리).
2. Limited liability, perpetual life, easy transfer / massive capital raising.
3. Accounting income = 발생주의 (감가상각 차감, 외상 매출 포함). Cash flow = 실제 현금.
4. Identification (무엇이 cash flow), Timing (언제), Risk (얼마나 확실).
5. 측정 가능 (주가), time + risk 모두 반영, 장기 + 단기 통합.
6. Monitoring (감시), Bonding (자기 구속), Residual loss (남은 손실).
7. CEO/CFO certification, internal control + audit, independent audit committee, PCAOB.
8. Class A (founder, 10 vote/share) + Class B (public, 1 vote/share). Founder 의 control 유지.

</details>

---

## §10 다음 학습으로

- **Ch 2** — Financial statements + cash flow 의 *정확한 정의*
- **Ch 3** — Ratio analysis + financial planning model
- **Ch 4** — DCF valuation 의 *수학적 기초*

---

## §11 한 줄 요약

> **Corporate finance = 3 질문 (capital budgeting + structure + working capital) 의 답. *Corporation* 의 limited liability + perpetual life 가 dominant. *Cash flow* (≠ income) 의 *identification + timing + risk* 가 valuation 의 base. Goal = *주주 부 극대화*. Agency cost (monitoring + bonding + residual) 의 통제. SOX + Dodd-Frank 의 regulation.**
