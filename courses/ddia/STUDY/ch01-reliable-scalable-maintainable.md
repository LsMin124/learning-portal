# Chapter 1: Reliable, Scalable, and Maintainable Applications — 학습 노트

> 이 노트는 *Designing Data-Intensive Applications* (Martin Kleppmann, O'Reilly 2017) **Chapter 1** (책 p.1~24, PDF p.25~48) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 1장은 책 전체의 **세 가지 키워드** — *Reliability, Scalability, Maintainability* — 를 정의하고 이후 12 장이 어떤 문제를 다루는지 *지도* 를 그린다.

## 들어가기 전에

- **선수 지식**
  - 기본 분산 시스템 개념 (HTTP, TCP, latency)
  - 관계형 DB / NoSQL 사용 경험
  - 캐시 / 큐 / 로드 밸런서 등 *데이터 시스템 컴포넌트* 의 존재
- **학습 목표**
  1. **Data-intensive application** 의 정의 — *데이터양·복잡도·변화 속도* 가 주요 도전
  2. **Reliability** — *fault* vs *failure* 의 구분, fault-tolerant 시스템 설계
  3. **Scalability** — *load* / *performance* 의 정량적 기술, p99·p999 tail latency
  4. **Maintainability** — *operability, simplicity, evolvability* 3가지 차원
  5. *Twitter fan-out* 예제로 architectural trade-off 사고하기
  6. *Percentile* 기반 SLO 정의
- **예상 학습 시간**: 60~90분 (개념 위주, 수식 없음)

---

## 1. Thinking About Data Systems

### 1.1 Data-intensive vs compute-intensive

| 측면 | Data-intensive | Compute-intensive |
|--|--|--|
| 병목 | data 의 *양·복잡도·변화 속도* | raw CPU power |
| 예시 | 웹 서비스, 분석 플랫폼 | HPC, 머신러닝 학습 |
| 도전 | scale, consistency, evolution | parallelism, FLOPS |

> 책의 범위 — *data-intensive* 에 집중. 분산 데이터 시스템의 *공통 building block* 을 다룬다.

### 1.2 Data system 의 building blocks

전형적 application 의 컴포넌트:

- **Database** — 데이터 영구 저장 + 조회 (RDBMS, NoSQL)
- **Cache** — 자주 읽는 결과를 빠르게 (Redis, Memcached)
- **Search index** — 키워드·필터 검색 (Elasticsearch)
- **Stream processing** — 비동기 메시지·이벤트 처리 (Kafka, Flink)
- **Batch processing** — 주기적 대량 데이터 가공 (Spark, Hadoop)

이 모든 것을 하나의 *data system* 으로 묶어 application 이 동작. *경계가 흐려진* 것이 현대.

![Figure 1-1 — 여러 컴포넌트를 결합한 data system 의 가능한 아키텍처. 책 p.5](/courses/ddia/figures/ch01/fig-1-1.png)

### 1.3 세 가지 관심사

> 모든 data system 설계는 **세 가지 차원** 의 trade-off:
> 1. **Reliability** — *문제가 생겨도* 올바르게 동작
> 2. **Scalability** — *부하가 커져도* 합리적으로 대응 가능
> 3. **Maintainability** — *시간이 지나도* 사람들이 다룰 수 있음

이후 §2~§4 가 각각을 상세히 다룬다.

---

## 2. Reliability

### 2.1 정의

> *시스템이 fault 가 있어도 (faults expected) 올바르게 (correct) 동작해야 한다*.

핵심 구분:

| 용어 | 정의 |
|--|--|
| **Fault** | 시스템의 한 *component* 가 spec 에서 벗어남 |
| **Failure** | 시스템 *전체* 가 서비스 제공을 멈춤 |

목표: **fault-tolerant** / **resilient** — fault 가 발생해도 failure 를 막음. fault 자체를 *없앨 수 없으므로* 견디는 것.

> **함정 1**: "fault 가 안 나게 한다" 가 아니라 "fault 가 나도 buggy software 가 되지 않게 한다". 의도적 fault injection (Netflix Chaos Monkey) 이 안티프래질 (antifragile) 접근.

### 2.2 Hardware Faults

- **Disk**: MTTF ~10~50 년 (1만 디스크 cluster 면 *하루 1개* 사망)
- **AWS EC2**: 가상 머신 평균 *1 reboot/month*
- **메모리·전원**: 무작위 ECC 에러, 정전

**대응**:
1. *Redundancy* — RAID, dual power, hot-swap
2. 소프트웨어 *fault tolerance* — multi-machine redundancy 가 점점 일반화 (cloud 의 표준)

### 2.3 Software Errors

- **Systematic bugs** — 한 가지 input pattern 으로 *모든* node 가 동시 실패 (vs hardware 의 *독립* 실패)
- **Cascading failures** — 한 서비스 장애가 의존 서비스로 전파
- **Leap second 버그** (2012 Linux kernel) — 시스템 전체가 hang

**대응** — 단순한 redundancy 로 불충분. 모니터링·테스트·격리 (process boundary, retry budget) 등.

### 2.4 Human Errors

- 운영자 설정 오류가 outage 의 *가장 큰 원인* (한 연구에서 ~60%)
- 대응:
  1. *Well-designed abstractions, APIs* — 실수 어렵게
  2. *Sandbox*, staging env — 실수해도 production 영향 없음
  3. 충분한 *testing* — manual 부터 fuzz 까지
  4. *Quick recovery* — rollback, canary deploy
  5. *Detailed monitoring* — 빨리 발견

### 2.5 Reliability 가 *얼마나* 중요한가

| 도메인 | 비용 |
|--|--|
| Business app | 매출 손실, 평판 |
| Consumer service | 사용자 이탈 |
| **Critical**: 의료·항공·재난 | 인명 |

작은 사이드 프로젝트에선 *cost of reliability* (engineering effort) 가 *benefit* 을 초과할 수 있음. 의도적 trade-off.

---

## 3. Scalability

### 3.1 정의

> *increasing load* 에 대응할 능력.

"이 시스템은 scalable 한가?" 는 잘못된 질문 — 1차원 라벨이 아님. 정확한 질문:
- "load 가 X 배로 늘면 어떤 옵션이 있나?"
- "computing resource 를 얼마나 추가해야 하나?"

### 3.2 Describing Load — *Load parameters*

시스템 architecture 에 따라 다른 *load parameter*:

| 시스템 | Load parameter |
|--|--|
| Web server | requests/sec |
| Database | reads:writes ratio |
| Chat | simultaneously active users |
| Cache | hit rate |
| **Twitter 예제** | fan-out distribution |

#### Twitter fan-out 예제 (2012, 책의 대표 사례)

두 메인 연산:
- **Post tweet**: avg 4.6k/sec, peak 12k/sec
- **Home timeline read**: avg 300k/sec

**Approach 1 — Read-time SQL join**

```sql
SELECT tweets.* FROM tweets
JOIN follows ON follows.followee_id = tweets.user_id
WHERE follows.follower_id = :current_user
```

![Figure 1-2 — Twitter home timeline 의 관계형 스키마. 책 p.11](/courses/ddia/figures/ch01/fig-1-2.png)

**Approach 2 — Write-time fan-out to per-user cache**

User 의 follow 관계를 미리 펼쳐, post 시 follower 의 timeline cache 에 직접 insert. Read 는 그 cache 만 보면 됨.

![Figure 1-3 — Twitter 의 write-time fan-out pipeline. 책 p.12](/courses/ddia/figures/ch01/fig-1-3.png)

**Trade-off**

| | Approach 1 | Approach 2 |
|--|--|--|
| Read cost | 비쌈 (JOIN) | 저렴 (cache 조회) |
| Write cost | 저렴 (1 row insert) | 비쌈 (avg 75 follower 에 insert, 셀럽은 30M) |
| 적합한 read:write | low ratio | **high ratio** (Twitter 같이) |

Twitter 의 *결정* — *Approach 2* 채택. 평균 timeline read 가 post 대비 75배 많아서 *write 에 더 일하고 read 를 가볍게* 가 유리.

**현재의 hybrid** — 셀럽 (follower > 수백만) 은 *Approach 1* 으로 fetch-on-read, 일반 유저는 *Approach 2* fan-out. 두 stream 을 read 시 merge.

> 핵심 load parameter — *follower 수의 분포* (특히 fat-tail).

### 3.3 Describing Performance

부하 정의 후 두 가지 질문:

1. **Load 증가, 자원 고정** → performance 어떻게 변하나?
2. **Load 증가, performance 유지** → 자원 얼마나 늘려야 하나?

#### Batch system: Throughput

records/sec. 1 batch job 의 완료 시간.

#### Online system: Response time

response time = *client 가 보는* 전체 시간 = service time + network + queueing.

latency ≠ response time:
- **latency**: 처리 대기 중인 시간만 (waiting in queue)
- **response time**: 클라이언트 관점 전체

**Distribution, not single number**

같은 request 반복해도 response time 이 *다름*. 측정해서 분포로 봐야 함.

원인: context switch, network packet loss + retransmission, GC pause, page fault, mechanical vibration (HDD), ...

![Figure 1-4 — 100 requests 의 response time 분포: mean vs percentiles. 책 p.14](/courses/ddia/figures/ch01/fig-1-4.png)

### 3.4 Percentiles in Practice — *Tail latency*

| 통계 | 의미 |
|--|--|
| **Mean (avg)** | 부적절. outlier 가 평균을 끌어올림. 사용자 *전체* 의 *전형* 경험 못 보여줌 |
| **Median = p50** | 절반의 요청이 이보다 빠름/느림. *전형적 사용자 경험* |
| **p95, p99, p999** | tail latency. *최악 경험* 측정 |
| **Max** | 단일 outlier, 노이즈 |

**왜 tail 이 중요한가**:
- *가장 비싼 (=오래 걸리는) 요청 = 가장 큰 고객 (= 데이터 많은 사용자)*. 잃으면 안 됨.
- p999 의 1초 지연이 *0.1%* 사용자에게 발생 — Amazon 의 경우 매출 0.1% 손실은 *연간 수백만 달러*.

**Service Level Objective (SLO) / Agreement (SLA)**

> 예: "p50 < 200ms, p99 < 1s, 99.9% 가동률 (downtime ≤ 53min/year)"

이런 식으로 *분포 기반* SLO 정의가 표준.

**Tail latency amplification**

backend call 이 *여러 service* 에 fan-out 되는 경우, 사용자 입장 response time 은 *모든 sub-call 의 max*. 각 backend 의 p99 이 1초 라도 100 sub-call 합치면 사용자 p99 가 *훨씬 더 큼*.

![Figure 1-5 — Tail latency amplification: 일부 backend 만 느려도 사용자 전체에 영향. 책 p.17](/courses/ddia/figures/ch01/fig-1-5.png)

**Percentile 계산 코드 패턴**

```python
# Online algorithm — 메모리 효율
from heapq import heappush, heappop

def p99_approx(samples):
    samples.sort()
    idx = int(0.99 * len(samples))
    return samples[idx]

# 실시간: t-digest 또는 HdrHistogram 사용
# (반올림된 bucket 으로 정확도·메모리 trade-off)
```

산업 도구: **HdrHistogram** (Java), **t-digest** (Apache Druid), Prometheus `histogram_quantile()`.

### 3.5 Approaches for Coping with Load

| 전략 | 의미 | 비고 |
|--|--|--|
| **Scaling up (vertical)** | 더 강한 머신 | 단순, 상한 있음, 고가 |
| **Scaling out (horizontal)** | 머신 수 증가 | "shared-nothing", 분산 복잡도 |
| **Elasticity** | 자동 추가/제거 | unpredictable load 에 |
| **Manual scaling** | 수동 조정 | predictable load 에 단순 |

> 책의 입장: *one-size-fits-all* scalable architecture 는 없다. 시스템마다 *어떤 연산이 흔하고 어떤 게 드문지* (load parameter) 가 architecture 를 결정.

scaling 결정은 *추측이 아닌 측정·실험* 기반.

---

## 4. Maintainability

### 4.1 정의 — Software 의 *대부분 비용은 유지보수*

> 신규 개발 < bug fix + 운영 + adaptation + 신기능 추가.

세 가지 design principle:

| 원칙 | 의미 |
|--|--|
| **Operability** | 운영팀이 시스템을 *원활히 다루도록* |
| **Simplicity** | 새 엔지니어가 *시스템을 쉽게 이해* |
| **Evolvability** | 미래에 *변경이 쉬움* (= extensibility, modifiability) |

### 4.2 Operability

운영팀 (DevOps / SRE) 의 *책임*:
- 시스템 상태 모니터링·복구
- 장애 원인 파악
- 보안 패치·소프트웨어 업데이트
- 다른 시스템과의 interaction
- 향후 변경 예측
- 좋은 *runbook* + *deployment* + config management
- *복잡한 manual 작업* 자동화·검증

**좋은 운영성을 만드는 구체 요소**:
- 좋은 모니터링·observability
- 자동화·표준 도구 통합
- *machine 1대 의존* 피함 (서비스 무중단 유지보수)
- 좋은 문서·이해 가능한 운영 모델
- *기본 동작이 좋고*, override 도 가능

### 4.3 Simplicity — *복잡도 관리*

작은 프로젝트가 처음엔 단순했다가 *큰 머드볼* (big ball of mud) 이 됨:
- 상태 공간 폭증, tight coupling, 일관 없는 naming
- 성능 hack, 특수 케이스 처리

**대응** — **abstraction**:

좋은 abstraction 의 예:
- *고급 프로그래밍 언어* — 기계어 / CPU 사이클 추상화
- *관계형 DB* — 디스크 구조 추상화
- *SQL* — 데이터 조회의 선언적 추상화

> 좋은 abstraction 은 *세부 복잡도를 깔끔한 인터페이스* 뒤로 숨김. 더 적은 노력으로 더 많은 기능 제공.

### 4.4 Evolvability — *변경의 용이성*

> Agility 의 데이터 시스템 버전.

핵심 요소:
- **Simple, easy-to-understand** 시스템이 *더 쉽게 수정* 가능
- *TDD, refactoring* 의 작은 단위 적용
- *Schema migration* 의 용이성 (4장 의 주제)

연결: **simplicity** + **good abstractions** → evolvability.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "scalable system" 이라는 한 단어 라벨 | scalable 은 *load 의 어떤 dimension* 에 대해서인지 명시 필요. read scale 과 write scale 이 다름. |
| 2 | Mean response time 으로 SLO 정의 | tail (p99, p999) 가 더 중요. 사용자 *최악 경험* 이 평판 결정. |
| 3 | Fault tolerance = fault 가 없음 | fault 는 *반드시 발생*. 대응이 잘 되는 게 fault tolerance. |
| 4 | Hardware redundancy 만으로 충분 | software bug 는 *모든 redundancy* 에 동시 영향. 다층 대응 필요. |
| 5 | Twitter Approach 1 (SQL JOIN) 이 항상 단순 | read:write ratio 가 무엇인지에 따라 *완전 반대* 가 정답. |
| 6 | Vertical scaling 이 항상 단순 | 가격이 *기하급수적* 으로 비싸짐. 어느 시점부터 horizontal 외 선택지 없음. |
| 7 | p99 가 평균의 ~2배 정도 | *수십 배* 일 수 있음. tail 은 분포가 다른 세계. |
| 8 | Maintainability = good code style | *시스템 전체* 의 abstraction·operability 까지 포함. style 만으론 부족. |
| 9 | 운영팀이 잘 알아서 함 | 시스템 *자체* 의 operability 가 부족하면 어떤 운영팀도 못 구함. |
| 10 | Tail latency 는 분산 시스템만의 문제 | 단일 서버도 GC, context switch, disk seek 으로 long tail 발생. |

---

## 자가점검

1. *Data-intensive* application 과 *compute-intensive* 의 차이.
2. **fault** vs **failure** 의 정의.
3. *Reliability* 의 3 가지 fault 유형.
4. Twitter 의 fan-out 두 접근의 각각의 trade-off.
5. *Mean* response time 대신 *median* / *percentile* 을 보는 이유.
6. *Tail latency amplification* 의 정의.
7. *Vertical* vs *horizontal* scaling.
8. *Maintainability* 의 세 가지 design principle.
9. Operability 를 좋게 만드는 구체적 4 가지 요소.
10. Software *대부분 비용* 이 어디 들어가는가.

### 해답 (간략)

1. Data-intensive: 데이터의 *양·복잡도·변화* 가 병목. Compute-intensive: raw CPU 가 병목.
2. fault = component 가 spec 이탈. failure = 시스템 *전체* 가 사용 불가.
3. Hardware, software, human errors.
4. Approach 1 (SQL join read-time): write 저렴 / read 비쌈. Approach 2 (fan-out write-time): write 비쌈 / read 저렴. high read:write 일 때 Approach 2 우세.
5. mean 은 outlier 에 끌려가고 사용자 *전형* 경험 못 보여줌. median/p95/p99 가 *분포* 를 표현.
6. backend 가 여러 service 에 fan-out 될 때, 사용자 response 는 *모든 sub-call 의 max* — 일부의 tail 이 전체 user 의 tail 로 *증폭*.
7. Vertical: 더 강한 머신 1대. Horizontal: 머신 여러 대 (shared-nothing).
8. Operability, Simplicity, Evolvability.
9. Monitoring, 자동화, single-machine dependency 회피, 좋은 문서, 좋은 기본 동작 + override 가능, 운영 단순성.
10. *유지보수* (bug fix, 운영, 변경, 신기능). 신규 개발은 작은 비중.

---

## 다음 학습으로

- **2장 (Data Models)** — relational vs document vs graph. application 에 *맞는 모델* 선택.
- **3장 (Storage and Retrieval)** — DB 내부 구조. B-tree vs LSM-tree.
- **5~6장** — replication / partitioning 으로 *horizontal scaling* 실현.
- **7장** — transaction 이 reliability 의 핵심 도구.
- **9장** — distributed consistency / consensus 가 *fault tolerance* 의 정점.

1장의 *Reliability / Scalability / Maintainability* 가 이후 모든 장의 *평가 기준*. 새 기술이 등장할 때마다 "이 셋 중 어느 것을 *어떻게* 개선하나?" 로 정리하면 책의 전체 흐름이 *지도처럼* 잡힌다.
