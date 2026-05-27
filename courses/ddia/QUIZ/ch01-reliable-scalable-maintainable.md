# Ch 1 Reliable, Scalable, Maintainable — 퀴즈

> 13 문항 (개념 4 / 계산 3 / 디버그 3 / 면접 3). 답은 펼치기 — 먼저 풀어볼 것.

---

## 개념

### Q1. Fault vs Failure

두 용어의 차이를 한 문장씩 적고, 왜 *fault* 를 막는 것보다 *failure* 를 막는 게 현실적인지 설명.

<details><summary>답</summary>

- **Fault**: 시스템의 한 *component* 가 spec 에서 이탈 (e.g., disk 1대 사망).
- **Failure**: 시스템 *전체* 가 서비스 제공을 멈춤 (사용자가 영향 받음).

Fault 는 *통계적으로 반드시* 발생 (1만 디스크면 매일 1대 죽음, EC2 VM 은 월 1회 reboot). 막는 게 불가능. 대신 fault 가 *failure 로 전파되지 않게* 다층 redundancy + monitoring + 격리 설계. 이게 **fault tolerance**.

Netflix Chaos Monkey 는 *의도적 fault injection* — fault 가 실제로 일어나기 *전에* 시스템의 약점을 발견.

</details>

---

### Q2. Reliability 의 3 fault 유형 + 각 대응

Hardware / Software / Human 의 *각각의 대응 전략 1 가지씩*.

<details><summary>답</summary>

| 유형 | 특징 | 대응 |
|--|--|--|
| **Hardware** | 독립·랜덤 (disk MTTF, ECC error, 정전) | Redundancy (RAID, multi-machine) |
| **Software** | systematic — 같은 input 으로 *모든* node 동시 실패 | 모니터링·테스트·격리 (timeout, retry budget, circuit breaker). leap second 같은 환경 이슈 의식. |
| **Human** | 운영자 설정 실수 (outage 의 ~60%) | Sandbox·staging, 좋은 abstraction, automation, quick rollback, observability |

Software 와 Human 은 *redundancy 만으로 안됨* — 다른 machine 의 동일 software 가 *같은 버그* 로 실패하기 때문.

</details>

---

### Q3. Mean vs Median vs p99

response time 의 *분포 통계* 4 가지 (mean, p50, p99, max) 의 *실용적 의미*.

<details><summary>답</summary>

- **Mean**: outlier 가 끌어올림. *전형* 사용자 경험 못 보여줌. 부적절.
- **Median (p50)**: 절반은 이보다 빠름, 절반은 느림. *전형 사용자 경험*. **SLO 기본**.
- **p95, p99, p999**: tail. *가장 안 좋은 경험*. 데이터 많은 큰 고객일 가능성 → 잃으면 안 됨.
- **Max**: 단일 outlier. 노이즈로 무시.

**SLO 패턴**: "p50 < 200ms, p99 < 1s, p999 < 5s, 99.9% 가동률". *median + tail* 둘 다 명시.

</details>

---

### Q4. Operability / Simplicity / Evolvability

Maintainability 의 3 원칙을 *operations team 입장* / *개발자 입장* / *조직 입장* 으로 각각 매핑.

<details><summary>답</summary>

- **Operability** → operations team — 시스템을 *원활히 다루도록*. 모니터링, 자동화, 좋은 default + override, single-machine 의존 회피.
- **Simplicity** → 개발자 — *새 엔지니어가 이해하기 쉬움*. 좋은 abstraction (= 복잡도 숨김) 으로 머드볼 (big ball of mud) 방지.
- **Evolvability** → 조직 — 미래 요구 변화에 *빠르게 대응*. simple + good abstractions 가 evolvability 의 *전제 조건*.

세 가지는 *독립적* 인 게 아니라 simplicity 가 evolvability 의 *기반*, operability 의 *전제* — 연쇄적.

</details>

---

## 계산

### Q5. Twitter fan-out write 부하 계산

Twitter post tweet 평균 4.6k/sec, 평균 follower 75명. Approach 2 (write-time fan-out) 의 *home timeline cache write 부하*를 계산. 추가로 follower 30M 의 셀럽 한 명이 1초에 트윗 1개 올리면 *몇 timeline write* 가 발생하나?

<details><summary>답</summary>

**평균 부하**: 4.6k tweets/sec × 75 follower/tweet = **345k timeline writes/sec**.

**셀럽 (30M follower) 트윗 1개**: **30M timeline writes** — 한 번에. 이걸 *5초 안에* 모든 follower 에게 전달하려면 *peak 6M writes/sec*.

이 *fat-tail distribution* 이 Twitter 가 hybrid (셀럽은 fetch-on-read) 로 전환한 이유. 셀럽 한 명의 트윗이 *평균 부하의 100배* 시스템 영향.

```python
avg_followers = 75
post_rate = 4_600
avg_fanout = post_rate * avg_followers  # 345_000 writes/sec

celebrity_followers = 30_000_000
celeb_one_tweet_writes = celebrity_followers
# 5초 안에 분산 처리: 6M writes/sec peak
```

</details>

---

### Q6. Tail latency amplification

backend service 의 p99 = 100ms. 사용자 한 페이지 렌더에 *100개* backend 호출이 *직렬* 로 발생. 사용자 체감 p99 의 *근사 lower bound*?

<details><summary>답</summary>

각 backend 호출이 *독립* 이라면 (idealized), 사용자 response 가 *어떤 sub-call 도 tail* 에 안 걸릴 확률:

```
P(all fast) = (0.99)^100 ≈ 0.366
```

즉 *36.6% 의 user request* 만 모든 sub-call 이 99 percentile 안에 들어옴. 나머지 *63.4% user request* 는 *최소 한 개* 의 sub-call 이 tail (≥ 100ms).

사용자 *p99* 는 *backend 100ms 보다 훨씬 큼*. 정확한 값은 분포에 의존하지만 *수 초* 단위로 늘어남.

**구원책**:
- backend call 을 *병렬* 화 (max 가 아닌 동일 max)
- fan-out 후 *hedged request* — 같은 요청 두 backend 에 보내고 *빠른 응답* 사용
- 중요하지 않은 sub-call 은 *timeout + fallback*

</details>

---

### Q7. SLA 의 가동률 → 다운타임 계산

"99.9% 가동률" (= three nines) 의 *연간 허용 downtime* 은? "99.99%" (four nines) 는?

<details><summary>답</summary>

연간 = 365 × 24 × 60 = 525,600 분.

| SLA | 다운타임/년 | 다운타임/월 | 다운타임/일 |
|--|--|--|--|
| 99% (two nines) | 87.6 시간 | 7.3 시간 | 14.4 분 |
| 99.9% (three nines) | 8.77 시간 | 43.8 분 | 1.44 분 |
| 99.99% (four nines) | 52.6 분 | 4.4 분 | 8.6 초 |
| 99.999% (five nines) | 5.3 분 | 26.3 초 | 0.86 초 |

산업 일반:
- Consumer web: three nines 충분
- Financial / e-commerce checkout: four nines
- Telecom / aviation: five nines

각 *9 추가* 가 *engineering cost 기하급수* 로 증가. four nines → five nines 가 *가장 비싼* 한 9.

</details>

---

## 디버그

### Q8. p99 가 갑자기 튀어오름

서비스 평균 latency 는 그대로인데 p99 가 50ms → 500ms 로 갑자기 *10배 증가*. 진단 순서.

<details><summary>답</summary>

평균은 그대로지만 p99 만 튐 = *일부 요청만* 매우 느려짐. 가능 원인:

1. **GC pause** — heap 압박, full GC 발생 → 1~2초 stop the world. → GC log 확인.
2. **새 deploy 의 slow path bug** — 특정 input pattern 만 느려짐. → A/B 비교, slow query log.
3. **Disk I/O 지연** — page fault, journal flush 누적. → iostat, await time.
4. **Backend dependency 의 tail latency 증가** — 우리는 빠른데 호출하는 외부 service 가 느림. → distributed tracing (Jaeger, Zipkin).
5. **Thundering herd / cache stampede** — 캐시 expire 동시 발생으로 backend 폭발. → cache hit rate.
6. **Network packet loss + TCP retransmission** — 평소엔 거의 0%, 가끔 0.5% 가 1초씩 늘림. → network metrics.
7. **Noisy neighbor** (cloud) — 같은 hypervisor 의 다른 VM 이 CPU/disk 점유. → cloud provider 의 host metrics.

순서 — 비용 낮은 것부터: deploy diff → GC log → tracing → infra metrics.

</details>

---

### Q9. Approach 2 (fan-out) 의 함정

Twitter Approach 2 (write-time fan-out) 로 구현했더니 *home timeline 에 옛날 follow 끊은 사용자의 트윗* 이 계속 보임. 원인과 해결.

<details><summary>답</summary>

**원인**: Approach 2 의 timeline cache 는 *과거 fan-out 시점의 follow 관계* snapshot. unfollow 후에도 *이미 cache 에 insert 된 트윗* 은 그대로 남아 있음.

**해결 옵션**:

1. **Cache invalidation on unfollow** — unfollow 시 해당 user 의 모든 트윗을 follower 의 timeline cache 에서 *제거*. 비싸지만 정확.
2. **Read-time filter** — timeline read 시 *현재 follow 관계* 와 join 으로 unfollow 한 user 의 트윗 제외. cache 는 안 건드림.
3. **TTL** — timeline cache entry 에 TTL, 자연 소멸.
4. **Hybrid** — unfollow 가 드물면 background batch job 이 주기적으로 정리.

산업: 보통 *Read-time filter (option 2)* 가 표준. cache invalidation 의 race 와 비용 회피.

이게 *consistency model* 문제의 단순화 버전 — 9장 (Consistency and Consensus) 에서 다층적으로 다룸.

</details>

---

### Q10. Operations 동료가 만든 *복잡한* monitoring dashboard

DevOps 동료가 한 화면에 *60+ 그래프* 의 dashboard 를 만들었음. 보면 *모든 게 다 정상* 처럼 보이는데 outage 가 발생. 진단.

<details><summary>답</summary>

**진단** — *Operability 실패*:

1. **너무 많은 시그널** — 60 개를 *동시에* 의미있게 모니터링하는 사람은 없음. 핵심 4~6개 (RED: Request rate, Error rate, Duration; USE: Utilization, Saturation, Errors) 로 압축.
2. **Alert 가 그래프와 분리** — 그래프는 *상황 인지* 용, alert 는 *행동 trigger* 용. 별개 시스템.
3. ***Symptom* vs *cause*** — 사용자가 영향 받는 *symptom* (error rate, p99 latency) 을 *cause* (CPU%, disk%) 보다 우선시.
4. **Anomaly detection / 이상치 강조** — 사람이 60 개를 훑는 게 아니라, *비정상 변화* 만 자동 highlight.
5. **Runbook 링크** — 각 alert 에 *어떻게 대응할지* 의 runbook 페이지 직링크.

**원칙**: dashboard 의 목표는 *상황 파악 후 30 초 안에 다음 행동 결정*. 시그널이 많으면 *못 결정*.

Google SRE 책의 *"Golden Signals"* 4가지 (latency, traffic, errors, saturation) 가 표준 출발점.

</details>

---

## 면접

### Q11. "이 시스템은 scalable 한가?"

면접관의 이 질문에 어떻게 *되묻나*?

<details><summary>답</summary>

"Scalable" 은 *1차원 라벨* 이 아니라 *어떤 dimension* 에서 어떻게 scale 하느냐의 *복합 질문*. 되물어야 할 항목:

1. **무엇이 scale 하나** — request rate? data volume? user count? geographic reach?
2. **현재 부하** — peak QPS, data size, user count
3. **타겟 부하** — 10×? 100×? predictable growth? bursty?
4. **R:W ratio** — read-heavy or write-heavy?
5. **Consistency 요구** — strong? eventual? per-feature?
6. **Latency SLO** — p50, p99 target?
7. **운영 제약** — budget, team size, multi-region?

이 답들에 따라 *완전 다른* architecture 선택. *one-size-fits-all scalable* 은 없음.

면접에서 좋은 답: "특정 axis 를 정해주시면 분석할 수 있어요. 예를 들어 *read scale* 이라면 cache + replica 인데, *write scale* 이면 partition + async pipeline 입니다."

</details>

---

### Q12. Simple data system 의 *over-engineering* 함정

"우리는 Netflix 만큼 scale 안 해. 그냥 단일 Postgres 면 됐는데 Kubernetes + 5 micro-services + Kafka + Redis cluster 깔았다가 운영 못 함."

이 상황에서의 *3 가지 교훈*.

<details><summary>답</summary>

1. **Premature distribution** — Knuth 의 premature optimization 의 분산 버전. *측정한 부하* 가 없으면 분산 도구 도입은 *복잡도 증가 = operability 손실*. *수직 확장 한계까지* 단일 서버 + read replica 가 의외로 멀리 감.

2. **Operability vs scalability** — 분산 시스템은 *scale up* 능력을 사고 *operability* 를 잃음. team size 가 작거나 SRE 경험 없으면 *큰 단일 서버 + 좋은 backup* 이 더 reliable.

3. **Evolvability 우선** — 처음부터 distributed 로 가는 게 아니라, *simple* 로 시작해서 *측정 데이터* 기반으로 component 별 분산 도입. simplicity 가 evolvability 의 전제.

**실용 가이드**:
- < 1k QPS, < 100GB data: 단일 RDBMS + 캐시
- 1k~10k QPS: read replica + cache layer
- 10k~100k QPS: partitioning 도입
- 100k+: 본격 distributed (책의 나머지)

대부분 startup 은 *영원히* 1번 범주에 머무름.

</details>

---

### Q13. "Reliability 와 Scalability 의 trade-off"

이 둘이 *충돌* 하는 경우와 *서로 강화* 하는 경우 각각 1 예씩.

<details><summary>답</summary>

**충돌**:
- Scale 을 위한 *async replication* (Ch 5) → *replication lag* 발생 → *eventual consistency* 로 약화 → reliability 의 한 측면 (예: read-after-write 보장) 손실.
- *Write fan-out* (Twitter Approach 2) → write 부하 증가 → write 시스템의 *failure 확률* 증가.

**강화**:
- *Horizontal scaling* (shared-nothing cluster) → 머신 1대 사망해도 다른 머신이 traffic 흡수 → *fault tolerance* 자동으로 ↑.
- *Multi-region deployment* → 한 region 정전에도 다른 region 이 service → reliability + scalability 동시 향상.

**핵심 통찰**: 두 차원은 *독립이 아님*. 같은 architectural 결정이 두 차원에 *다른 방향* 으로 영향. 면접에서 "이걸 어떻게 결정하나?" 의 답은 "*비용 vs 가치*. SLO 정의 후 *측정* 으로 결정. 직감 안 됨."

3번째 차원 (maintainability) 까지 합치면 *3차원 pareto front* — 모든 결정이 trade-off.

</details>
