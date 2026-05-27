# Chapter 8: The Trouble with Distributed Systems — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 8** (책 p.273~320, PDF p.295~342).
> 8장: 분산 시스템의 *근본적 어려움* — *network 신뢰 불가, clock 부정확, process pause*. 이 모든 *partial failure* 가 5~7장의 모든 abstraction 을 흔든다.

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

## 1. Partial Failure — single machine 과의 *질적 차이*

### 1.1 Single machine

- *Fault: deterministic* — RAM bit flip 같은 random hardware 외엔, 같은 input 에 같은 output
- *Crash 시 reboot* — clean state 로 시작
- *내부 통신 신뢰* — function call 의 round-trip 가 ns 단위

### 1.2 Distributed system

- *Network 통신* — packet loss, latency variance, reorder
- *부분적 fault* — 한 node 가 *부분* 실패 (CPU 동작, network 끊김)
- *Non-deterministic* — 같은 input 이 다른 시점에 다른 결과
- *Time 의 비신뢰* — node 마다 clock 다름

> "*The cloud is dark and full of terrors*" — 책의 표현. 분산은 *fundamental 어려움*, *technology 만으로 해결 안 됨*.

### 1.3 Why distribute?

이 어려움에도 *왜* 분산:
1. **Scale** — 단일 머신 한계 초과
2. **Reliability** — 일부 node 실패해도 서비스 지속
3. **Latency** — 사용자 가까운 region

---

## 2. Unreliable Networks

### 2.1 Packet 의 6 운명

데이터 packet 의 가능 결과:
1. 정상 도달
2. *Drop* (router 의 queue full)
3. *Delayed* (네트워크 congestion)
4. *Reorder* (다른 path)
5. *Duplicate* (router 오류)
6. *Corrupt* (전송 오류)

→ TCP 가 (2) (5) (6) 일부 해결. *지연·순서·duplicate* 은 application 까지 전파 가능.

### 2.2 Timeout 의 어려움

> "응답이 없음" 의 가능 원인:
> 1. Request lost
> 2. Request 처리 중 (느림)
> 3. Response lost
> 4. Server crashed before processing
> 5. Server processed but crashed before response
> 6. Server processed, but partition (response 갈 곳 없음)

원격 host 가 *살아있는지* 알 방법은 *timeout 만*. 하지만 timeout 값 결정 어려움:
- 너무 짧음 → false positive (살아있는데 dead 판정)
- 너무 김 → outage 길어짐

### 2.3 Asynchronous networks 의 본질

대부분 datacenter network 는 *asynchronous packet network*:
- *bounded delay 없음*
- *Best-effort* 만
- TCP timeout 은 *adaptive* (Karn-Partridge, Jacobson algorithm)

대조: *synchronous network* (전화망의 dedicated circuit). bounded delay 보장, 그러나 *bandwidth 비효율*.

---

## 3. Unreliable Clocks

### 3.1 Clock 의 2 종류

**Time-of-day clock** (UTC):
- 사용자 표시용 (현재 시각)
- NTP 로 동기화 (잘 되면 ~1ms, 보통 ~100ms)
- *Wall clock 시간* — leap second, daylight saving 으로 *뛰기* 가능
- *수동 조정* 으로 *과거로 점프* 가능

**Monotonic clock**:
- 단조 증가 (절대 줄지 않음)
- *interval 측정* 에만 사용 (예: `now() - start_time`)
- *서로 다른 node 의 monotonic 은 비교 불가*

> **함정 1**: `time.now() - start_time` 으로 elapsed 측정 시 *NTP 조정* 으로 *음수* 가능. monotonic clock 사용.

### 3.2 Clock 동기화의 한계

- NTP 의 typical 오차 100ms
- 그러나 *최악* 1 분 이상 가능 (NTP server 실패, virtualization, leap second)
- *GPS clock* (Google Spanner) — 7ms 보장. 비쌈.

### 3.3 Timestamp 기반 ordering 의 위험

**Last Write Wins (LWW)** — timestamp 큰 게 이김:

![Figure 8-3 — Clock skew 로 인한 LWW 실패. 책 p.292](/courses/ddia/figures/ch08/fig-8-3.png)

- Node A 의 timestamp 가 *과거* (clock 늦음)
- Node B 의 *나중 write 가 더 작은 timestamp* → *LWW 가 잘못된 결과*

**해결**:
- **Logical clock** (Lamport timestamp, vector clock) — 시계 무관
- **Hybrid logical clock** (HLC) — physical + logical 결합
- **TrueTime** (Spanner) — *uncertainty interval* `[earliest, latest]` 명시

### 3.4 Process Pause

GC, OS swap, VM live migration 등으로 process 가 *수 초 정지*. 이때:

```
1. process 가 "나는 leader" 라고 생각
2. 그러나 다른 node 들은 timeout 으로 "leader 죽음", 새 leader 선출
3. process 가 깨어남 — 자기는 *여전히 leader* 처럼 행동
4. 두 leader → split brain
```

**대응** — **Fencing token**:
- 새 leader 가 *monotonic 증가 token* 받음
- 모든 write 에 token 포함
- 옛 leader 의 옛 token write 는 *거부*

![Figure 8-5 — Fencing token 으로 split brain 방지. 책 p.302](/courses/ddia/figures/ch08/fig-8-5.png)

---

## 4. Truth & Lies — Byzantine Faults

### 4.1 Crash-stop vs Byzantine

| 모델 | 가정 |
|--|--|
| **Crash-stop** | node 가 *실패하면 정지*. 살아있으면 *프로토콜 준수* |
| **Crash-recovery** | 정지 후 *복귀* 가능. recovery 의 정확성 |
| **Byzantine** | node 가 *거짓말* 가능 (악의적 또는 버그) — 다른 node 에 다른 답 |

### 4.2 Byzantine fault tolerance

> *Byzantine Generals Problem* (Lamport 1982) — N 개의 일반 중 일부 traitor 가 있을 때 *합의* 어떻게.

**결과**: traitor 가 *N/3 미만* 이어야 합의 가능 (3f + 1 node 필요).

**현실** — 대부분 datacenter 는 *crash-stop* 가정으로 충분:
- 같은 회사의 node 가 *거짓말 안 함* (소프트웨어 버그는 별개)
- 인증·암호화로 *외부 공격* 방지

Byzantine 가정이 필요한 경우:
- **Aerospace** — radiation 으로 bit flip
- **Blockchain** — 모르는 anonymous node 간 합의
- **Multi-organization** — 신뢰 없는 parties

---

## 5. System Models

분산 algorithm 의 *가정* 을 명시.

### 5.1 Timing 가정

| 모델 | 가정 |
|--|--|
| **Synchronous** | network delay 와 process pause 의 *bounded upper limit* 알려져 있음 |
| **Partially synchronous** | 대부분 시간엔 synchronous, *드물게* 어긋남 |
| **Asynchronous** | timing 가정 *전혀 없음* |

대부분 실용 algorithm 은 *partially sync* 가정. *fully async* 는 너무 약함 (FLP impossibility 같은 이론).

### 5.2 Node 실패 모델

위 §4.1 — crash-stop / crash-recovery / Byzantine.

### 5.3 Algorithm 의 *정확성*

- **Safety** ("나쁜 일이 안 일어남") — 예: 두 leader 가 동시 존재하지 않음
- **Liveness** ("결국 좋은 일이 일어남") — 예: 결국 leader 선출됨

→ 9장의 *consensus* 는 safety + liveness 모두 보장하려 함.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Network 가 신뢰 가능 | Fallacies. timeout 이 *기본 가정* |
| 2 | Clock 이 정확 | NTP 도 ~100ms 오차. 최악 1분 이상 |
| 3 | `time.now() - start_time` 으로 interval 측정 | NTP 조정으로 음수 가능. monotonic 사용 |
| 4 | GC pause 무시 | JVM 의 STW 가 *수 초* — split brain 위험 |
| 5 | "Leader 다" 라고 *스스로* 판단 | Fencing token + external election 필요 |
| 6 | LWW 가 anomaly 해결 | Clock skew 로 *최신 write 손실* 가능 |
| 7 | Crash-stop 가정 무시 | Crash-recovery 가 더 현실적. partial fault handling |
| 8 | Byzantine 가정 필요 | 대부분 단일 organization 에선 불필요. 비싸짐 |
| 9 | Async network 에서 *bounded timeout* | 절대 보장 안 됨. retry + circuit breaker |
| 10 | "분산 systme 이 *알아서* 처리" | application 이 *retry, idempotency, compensation* 명시 처리 |

---

## 자가점검

1. *Partial failure* — single 과 distributed 의 *질적 차이*.
2. *Asynchronous network* 의 특성 + 그로 인한 timeout 의 어려움.
3. *Time-of-day vs monotonic* clock 의 사용 차이.
4. *LWW* 가 clock skew 로 *어떻게* 잘못된 결과.
5. *Process pause* 가 *어떻게* split brain 유발.
6. *Fencing token* 의 동작.
7. *Crash-stop / crash-recovery / Byzantine* 모델 정의.
8. *Synchronous / partially sync / asynchronous* timing 모델.
9. *Safety* vs *Liveness* 의 차이.
10. 분산 algorithm 의 *system model* 이 왜 명시 필요.

### 해답 (간략)

1. Single: deterministic, crash 시 clean. Distributed: partial failure, network unreliable, clock 다름.
2. Bounded delay 없음. 어떤 packet 이 *언제 도착할지* 모름. timeout 결정 어려움.
3. Time-of-day: 사용자 표시 (NTP, leap second 가능). Monotonic: interval 측정 (단조 증가, node 간 비교 불가).
4. Node A 의 clock 늦음 → A 의 *나중 write* 의 timestamp 가 *작아* → LWW 가 잘못된 write 채택.
5. Long pause 동안 timeout 으로 새 leader 선출 → pause node 가 깨어나면 *자기도 leader* 행세 → split brain.
6. 새 leader 가 *증가 token* 받음. 모든 write 에 포함. 옛 token 의 write 거부.
7. Crash-stop: 실패=정지. Crash-recovery: 복귀 가능. Byzantine: 거짓말 가능.
8. Sync: bounded delay 보장. Partial sync: 대부분 sync, 드물게 어긋남. Async: 가정 없음.
9. Safety: *나쁜 일 안 일어남*. Liveness: *결국 좋은 일 일어남*.
10. 같은 algorithm 이 다른 model 에서 *동작 다름*. 명시 안 하면 *false expectation*.

---

## 다음 학습으로

- **9장 (Consistency & Consensus)** — 위 어려움들을 *어떻게 극복* 하는 algorithm
- **11장 (Stream)** — *event ordering* 의 정확한 처리. logical clock 의 응용
