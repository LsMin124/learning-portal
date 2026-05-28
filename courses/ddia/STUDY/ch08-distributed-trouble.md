# Chapter 8: The Trouble with Distributed Systems — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 8** (책 p.273~320, PDF p.295~342).
> 8장: 분산 시스템의 *근본적 어려움* — *network 신뢰 불가, clock 부정확, process pause*. 이 모든 *partial failure* 가 5~7장의 모든 abstraction 을 흔든다.

이 장의 *지적 무게중심*:
1. **Partial failure** — *single ↔ distributed* 의 질적 차이
2. **The 8 Fallacies** of distributed computing (Sun, 1994)
3. **Unreliable network** — timeout 의 *근본 어려움*
4. **Unreliable clock** — physical vs monotonic vs logical
5. **Process pause** — GC, swap, VM migration 의 *split brain*
6. **Byzantine** vs *crash-stop* 의 fault model

---

## 들어가기 전에

- **선수 지식**: 5~7장 (replication / partitioning / transactions)
- **학습 목표**
  1. **Partial failure** — single machine ↔ distributed 의 *질적 차이*
  2. **Unreliable network** — timeout, packet loss, GC pause
  3. **Unreliable clock** — physical / monotonic / logical
  4. **Process pause** — GC, swap, VM migration
  5. **Truth & lies in distributed systems** — *Byzantine* faults vs *crash-stop*
  6. **System model** — synchronous / partial sync / asynchronous
- **예상 학습 시간**: 150~180분

---

## §1 Partial Failure — single machine 과의 *질적 차이*

### §1.1 Single machine

- *Fault: deterministic* — RAM bit flip 같은 random hardware 외엔, 같은 input 에 같은 output
- *Crash 시 reboot* — clean state 로 시작
- *내부 통신 신뢰* — function call 의 round-trip 가 ns 단위

### §1.2 Distributed system

- *Network 통신* — packet loss, latency variance, reorder
- *부분적 fault* — 한 node 가 *부분* 실패 (CPU 동작, network 끊김)
- *Non-deterministic* — 같은 input 이 다른 시점에 다른 결과
- *Time 의 비신뢰* — node 마다 clock 다름

> "*The cloud is dark and full of terrors*" — 책의 표현.

### §1.3 8 Fallacies of Distributed Computing

Peter Deutsch (Sun, 1994):
1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

→ *모두 거짓*.

### §1.4 Why distribute?

1. **Scale** — 단일 머신 한계 초과
2. **Reliability** — 일부 node 실패해도 서비스 지속
3. **Latency** — 사용자 가까운 region

---

## §2 Unreliable Networks

### §2.1 Packet 의 6 운명

1. 정상 도달
2. *Drop* (router queue full)
3. *Delayed* (congestion)
4. *Reorder* (다른 path)
5. *Duplicate* (router 오류)
6. *Corrupt* (전송 오류)

→ TCP 가 (2) (5) (6) 일부 해결. *지연·순서·duplicate* 은 application 까지.

### §2.2 Timeout 의 어려움

> "응답 없음" 의 가능 원인:
> 1. Request lost
> 2. Request 처리 중 (느림)
> 3. Response lost
> 4. Server crashed before processing
> 5. Server processed but crashed before response
> 6. Server processed, but partition

원격 host 의 *생존 확인* = *timeout 만*. 결정 어려움:
- 너무 짧음 → false positive
- 너무 김 → outage 길어짐

### §2.3 Asynchronous networks 의 본질

대부분 datacenter network 는 *asynchronous packet network*:
- *bounded delay 없음*
- *Best-effort*

대조: *synchronous network* (전화망의 dedicated circuit). bounded delay, *bandwidth 비효율*.

### §2.4 실제 사고 사례

**Cloudflare 2019 — Regex 의 catastrophic backtracking**:
- WAF rule 의 regex 가 *exponential time*
- CPU 100% — 수 분 outage
- 전 세계 영향
- → *Resilience to malformed input* 의 중요성

**AWS S3 2017 — Typo outage**:
- Internal command typo
- 수 시간 service down
- 많은 SaaS dependent
- → *Blast radius* 교훈

**GitLab 2017 — DB delete**:
- DBA 의 잘못된 server delete
- 6 시간 outage
- Backup 5 종 중 4 종 깨짐
- → Live blogging incident response

---

## §3 Unreliable Clocks

### §3.1 Clock 의 2 종류

**Time-of-day clock** (UTC):
- 사용자 표시
- NTP (잘 되면 ~1ms, 보통 ~100ms)
- Wall clock 시간 — leap second 가능
- 수동 조정 — 과거 점프 가능

**Monotonic clock**:
- 단조 증가 (절대 줄지 않음)
- *interval 측정* 만
- *서로 다른 node 간 비교 불가*

> **함정 1**: `time.now() - start_time` 으로 elapsed 측정 시 *NTP 조정* 으로 *음수* 가능. monotonic 사용.

### §3.2 Clock 동기화의 한계

- NTP typical 오차 100ms
- 최악 1 분 이상 가능 (NTP server 실패, virtualization, leap second)
- GPS clock (Spanner) — 7ms 보장. 비쌈.

**Leap second 사고** (2012-06-30):
- Linux kernel bug — high CPU on Java/MySQL
- Reddit, LinkedIn, Yelp 등 영향
- → Google 의 *leap smear* — 24h 천천히 적용

### §3.3 Timestamp 기반 ordering 의 위험

**Last Write Wins (LWW)** — timestamp 큰 게 이김:

![Figure 8-3 — Clock skew 로 인한 LWW 실패. 책 p.292](/courses/ddia/figures/ch08/fig-8-3.png)

- Node A clock 늦음 → A 의 *나중 write 가 더 작은 timestamp* → LWW 잘못

**해결**:

#### Logical clock — Lamport timestamp

```
on local event:
    counter++
    return counter
on receive m:
    counter = max(counter, m.counter) + 1
    return counter
```

→ *Happens-before* 보존. Concurrent event 구분 불가.

#### Vector clock

각 node 가 *모든 다른 node 의 counter* 보유:
```
node i:
on local event:
    vc[i]++
on receive m:
    vc[k] = max(vc[k], m.vc[k]) for all k
    vc[i]++
```

→ *Concurrent event* 구분 가능.

#### Hybrid Logical Clock (HLC)

Physical + logical 결합:
- *Mostly tracks physical time* (debugging)
- *Causality 보존*
- CockroachDB, YugaByte 사용

#### TrueTime (Spanner)

Google 의 *uncertainty interval*:
- API: `TT.now()` returns `[earliest, latest]`
- GPS + atomic clock — ~7 ms uncertainty
- *Wait out* uncertainty 후 commit → *external consistency*

### §3.4 Process Pause

GC, OS swap, VM live migration 으로 process *수 초 정지*:

```
1. process 가 "leader" 자처
2. 다른 node 가 timeout 으로 새 leader 선출
3. process 깨어남 — 여전히 leader 처럼 행동
4. 두 leader → split brain
```

**Fencing token**:
- 새 leader 가 *monotonic 증가 token* 받음
- 모든 write 에 token 포함
- 옛 token write 거부

![Figure 8-5 — Fencing token 으로 split brain 방지. 책 p.302](/courses/ddia/figures/ch08/fig-8-5.png)

**JVM GC 의 실제**:
- *Full GC* — 수 초 ~ 수 분 STW
- *G1 / ZGC* — sub-ms 목표
- *Off-heap* — GC 영향 회피

**Kubernetes 의 process pause**:
- Pod scheduling, image pull — 수 분
- Liveness probe timeout 중요

---

## §4 Truth & Lies — Byzantine Faults

### §4.1 Crash-stop vs Byzantine

| 모델 | 가정 |
|--|--|
| **Crash-stop** | node 실패 → 정지. 살아있으면 프로토콜 준수 |
| **Crash-recovery** | 정지 후 복귀 가능 |
| **Byzantine** | node 가 거짓말 가능 |

### §4.2 Byzantine fault tolerance

> *Byzantine Generals Problem* (Lamport 1982).

**결과**: traitor 가 N/3 미만 이어야 합의 가능 (3f + 1 node).

**현실** — 대부분 datacenter 는 crash-stop 으로 충분.

**Byzantine 필요한 경우**:
- Aerospace — radiation bit flip
- Blockchain — anonymous node
- Multi-organization

### §4.3 PBFT

Castro, Liskov (1999):
- 3f+1 node, f Byzantine 허용
- 3 phase (pre-prepare, prepare, commit)

산업:
- Hyperledger Fabric
- Tendermint (Cosmos)
- Aerospace

---

## §5 System Models

### §5.1 Timing 가정

| 모델 | 가정 |
|--|--|
| **Synchronous** | network delay + process pause 의 bounded upper limit |
| **Partially synchronous** | 대부분 sync, 드물게 어긋남 |
| **Asynchronous** | timing 가정 없음 |

대부분 실용 algorithm = *partially sync*.

### §5.2 FLP Impossibility

Fischer, Lynch, Paterson (1985):
> *Asynchronous network* 에서 *consensus 는 impossible*. 한 node fail 가능해도.

**의미**:
- Pure async 는 너무 약함
- 실용은 *partial sync* 또는 *randomized*
- Timeout 으로 consensus 가능 (Paxos, Raft)

### §5.3 Node 실패 모델

위 §4.1 — crash-stop / crash-recovery / Byzantine.

### §5.4 Algorithm 의 *정확성*

- **Safety** ("나쁜 일이 안 일어남") — 예: 두 leader 동시 없음
- **Liveness** ("결국 좋은 일이 일어남") — 예: 결국 leader 선출

---

## §6 Observability — Modern 도구

**Logs**:
- Structured (JSON)
- Centralized — ELK, Loki, Splunk
- *Correlation ID*

**Metrics**:
- Prometheus, Datadog, New Relic
- *RED method* — Rate, Errors, Duration
- *USE method* — Utilization, Saturation, Errors

**Distributed Tracing**:
- Jaeger, Zipkin, Tempo
- *OpenTelemetry* 표준
- *Trace ID + span*

**Service Mesh observability**:
- Istio, Linkerd 의 automatic instrumentation
- *Application 코드 변경 없이* full observability

---

## §7 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Network 신뢰 가능 | Fallacies. timeout 기본 |
| 2 | Clock 정확 | NTP 100ms, 최악 1분+ |
| 3 | `time.now() - start_time` | NTP 조정으로 음수 가능 |
| 4 | GC pause 무시 | JVM STW 수 초 — split brain |
| 5 | "Leader" 스스로 판단 | Fencing token 필요 |
| 6 | LWW 가 anomaly 해결 | Clock skew 손실 |
| 7 | Crash-stop 가정 무시 | Crash-recovery 현실적 |
| 8 | Byzantine 가정 필요 | 단일 organization 엔 불필요 |
| 9 | Async network bounded timeout | 절대 보장 안 됨 |
| 10 | "분산 system 알아서" | application 의 retry, idempotency |
| 11 | Logical clock = physical | Lamport 는 happens-before 만 |
| 12 | Observability = log + metric | Distributed tracing 도 |

---

## §8 자가점검

1. *Partial failure* — single 과 distributed 의 질적 차이?
2. *8 Fallacies* 중 4개?
3. *Asynchronous network* + timeout 어려움?
4. *Time-of-day vs monotonic* 사용 차이?
5. *LWW* 가 clock skew 로 어떻게 실패?
6. *Lamport vs Vector clock* 차이?
7. *Process pause* 가 어떻게 split brain?
8. *Fencing token* 동작?
9. *Crash-stop / crash-recovery / Byzantine* 모델?
10. *Safety vs Liveness*?
11. *FLP impossibility* 의미?
12. *Distributed tracing* 역할?

<details><summary>해답 (간략)</summary>

1. Single: deterministic. Distributed: partial failure, unreliable network, clock 다름.
2. (1) Network reliable (2) Latency 0 (3) Bandwidth ∞ (4) Network secure 등.
3. Bounded delay 없음. timeout = 짧으면 false positive, 길면 outage.
4. Time-of-day: 표시 (NTP). Monotonic: interval (단조 증가).
5. Node A clock 늦음 → A 의 나중 write 가 작은 timestamp → LWW 잘못.
6. Lamport: happens-before. Vector: concurrent event 구분.
7. Pause 중 새 leader 선출 → pause node 깨어나 leader 행세 → split brain.
8. 새 leader 가 증가 token. 옛 token write 거부.
9. Crash-stop: 실패=정지. Crash-recovery: 복귀. Byzantine: 거짓말.
10. Safety: 나쁜 일 없음. Liveness: 결국 좋은 일.
11. Async 에서 consensus impossible. 실용 = partial sync.
12. Request 전체 경로 추적. Jaeger, OpenTelemetry.

</details>

---

## §9 다음 학습으로

- **9장 (Consistency & Consensus)** — 어려움 극복 algorithm
- **11장 (Stream)** — event ordering, logical clock 응용

---

## §10 한 줄 요약

> **분산 시스템의 근본 어려움 = network + clock + process pause 의 *non-determinism*. *8 Fallacies* 의 거짓. Lamport/Vector/HLC/TrueTime 의 logical clock. *Fencing token* + crash-recovery. *Partial sync* 가정 (FLP 회피). Modern observability — log + metric + tracing.**
