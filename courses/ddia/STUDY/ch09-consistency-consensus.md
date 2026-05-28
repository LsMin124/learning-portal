# Chapter 9: Consistency and Consensus — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 9** (책 p.321~388, PDF p.343~410).
> 9장: 책의 *클라이맥스*. 8장의 어려움 위에서 *강한 보장* 을 어떻게 만드나. **Linearizability**, **causal consistency**, **consensus** (Paxos, Raft).

이 장의 *지적 무게중심*:
1. **Linearizability** — *recency guarantee* 의 정확한 의미
2. **CAP / PACELC** — partition 시 *consistency or availability* + latency
3. **Total order broadcast = consensus** — 두 problem 의 동등성
4. **Paxos + Raft** — 실용 consensus
5. **ZooKeeper / etcd** — *시스템 의 뇌*

---

## 들어가기 전에

- **선수 지식**: 5~8장 (replication, partition, transactions, distributed trouble)
- **학습 목표**
  1. **Linearizability** — *atomic register* 처럼 보이는 것
  2. **Linearizability 의 cost** — CAP, latency
  3. **Causal consistency** — 더 약하지만 더 실용적
  4. **Ordering** — total order broadcast 의 핵심
  5. **Consensus** — 한 값에 모든 node 가 동의. *FLP impossibility*
  6. **Paxos, Raft, Zab, Viewstamped Replication** — 실용 consensus
  7. **Membership / Coordination service** — ZooKeeper, etcd
- **예상 학습 시간**: 240~300분

---

## §1 Linearizability — 가장 강한 consistency

### §1.1 직관

> 시스템이 *단일 atomic register* 처럼 보임 — 동시 operation 이 *어떤 직렬 순서* 로 실행된 것 같음.

각 operation 이 *시작-끝 사이 어느 한 순간* 에 *원자적으로* 발생 (linearization point).

### §1.2 정확한 정의

3 client 가 동시 read/write:

```
Client A: write x=1 ----|
Client B:       read x ----|  → ?
Client C:                read x ----|  → 1
```

- B 의 read 는 0 또는 1 모두 OK
- 그러나 *B 가 1 을 본 후 C 가 0 을 보면 위반*

이게 *recency guarantee*.

### §1.3 Linearizability vs Sequential Consistency

| | Linearizability | Sequential Consistency |
|--|--|--|
| Real-time order | 보존 | 무시 |
| Program order | 보존 | 보존 |
| 강도 | 가장 강함 | 중간 |

### §1.4 흔한 오해

- ❌ "DB default" — Postgres default 는 Read Committed, *not linearizable*
- ❌ "Snapshot isolation = linearizable" — 다름
- ❌ "Quorum read = linearizable" — concurrent write ordering 보장 안 됨

### §1.5 어디서 필요?

1. **Lock service** — 한 번에 한 client 만 lock
2. **Constraint** — unique constraint, foreign key
3. **Cross-channel timing** — image upload + url ordering
4. **Leader election** — 유일한 leader

---

## §2 Linearizability 구현

### §2.1 Single-leader replication

leader = linearization point. follower 가 sync 되면 linearizable. 단:
- *Follower read* 는 async lag 로 *not linearizable*
- *Sync follower* read 는 linearizable

### §2.2 Consensus algorithm

Paxos, Raft — 합의된 결정이 linearizable.

### §2.3 Multi-leader / Leaderless — *not linearizable*

- Multi-leader: concurrent write resolve 후 — *not linear*
- Leaderless (Cassandra): quorum read 도 edge case 에서 위반

### §2.4 Cost — CAP

> Linearizability 와 *availability under partition* 은 *동시 불가*.

Partition 시 양쪽이 서로 모르고 write → linearizability 깨짐.

**CAP 정리** (Brewer 2000, Gilbert-Lynch 2002):
- **C**onsistency — linearizability
- **A**vailability — 모든 request 응답
- **P**artition tolerance — partition 견딤
- → partition 동안 C 와 A 중 하나만

**PACELC 의 확장** (Abadi 2012):
- During **P**: **A** or **C**
- **E**lse: **L** (latency) or **C** (consistency)

→ Partition 없을 때도 latency vs consistency trade-off.

대부분 산업 = *availability + latency* 우선.

---

## §3 Ordering Guarantees

### §3.1 Total order vs Partial order

| 순서 | 정의 |
|--|--|
| **Total** | 모든 두 event 비교 가능 |
| **Partial** | 일부 event incomparable (concurrent) |

Linearizable = total order.
Causal consistency = partial order.

### §3.2 Causality

> A 가 B 의 원인이면 모든 node 가 *A 를 B 보다 먼저* 봐야.

happens-before:
- *Same process*: program order
- *Inter-process*: message send → receive
- *Transitive*: A → B, B → C ⟹ A → C

(Lamport 1978)

### §3.3 Lamport Timestamps

```python
class LamportClock:
    def __init__(self, node_id):
        self.counter = 0
        self.node_id = node_id

    def event(self):
        self.counter += 1
        return (self.counter, self.node_id)

    def receive(self, other_timestamp):
        self.counter = max(self.counter, other_timestamp[0]) + 1
```

비교: `(c1, n1) < (c2, n2)` iff `c1 < c2` or `(c1 == c2 and n1 < n2)`.

*Total order* 만들지만 *causality* 만 보장.

### §3.4 Total Order Broadcast

- **Reliable delivery** — 모든 non-fail node 받음
- **Totally ordered delivery** — 같은 순서

이게 *consensus 와 동등*.

**Kafka 의 partition 안** = total order. 전체 cluster 는 partial.

**Apache BookKeeper** — 다른 total order broadcast 구현.

---

## §4 Consensus

### §4.1 정의

> N 개의 process 가 *한 값* 에 합의:
> - **Uniform agreement** — 모두 같은 값
> - **Integrity** — 한 번 결정 후 변하지 않음
> - **Validity** — 어떤 proposal 의 값
> - **Termination** — 살아있는 node 는 결국 결정

### §4.2 FLP Impossibility

> *Async + crash-stop* 에서 *deterministic consensus 불가능* (FLP 1985).

**우회**: Randomization / Timing 가정 / Partial sync.

### §4.3 Consensus Algorithms

| Algorithm | 발표 | 특징 |
|--|--|--|
| **Paxos** | Lamport 1998 | classic, 이해 어려움 |
| **Raft** | Ongaro 2014 | 친화적. etcd, Consul, CockroachDB |
| **Zab** | Reed 2008 | ZooKeeper |
| **Viewstamped Replication** | Liskov 1988 | Raft 영감 |
| **EPaxos** | 2013 | Leaderless Paxos |

핵심:
1. *Leader election*
2. *Log replication*
3. *Commit* (majority ack)
4. *Failure* — 새 leader + recovery

### §4.4 Raft 동작 개요

![Figure 9-7 — Raft 의 leader, follower, candidate. 책 p.367](/courses/ddia/figures/ch09/fig-9-7.png)

**3 state**:
- *Follower* — passive
- *Candidate* — election 시도
- *Leader* — active replication

**2 RPC types**:
- *AppendEntries* — leader → follower (replication + heartbeat)
- *RequestVote* — candidate → other (vote 요청)

**Term**: 매 election 마다 ↑. 옛 term leader 는 자동 step down.

**Leader election**:
- Follower 의 random timeout (150~300ms) → candidate
- Term++, self-vote, RequestVote
- Majority → leader

**Log replication**:
- Client → leader
- Leader log append + AppendEntries
- Majority ack → commit
- Leader 가 commit index update

**Safety — Log Matching**:
- 같은 index + 같은 term → 모든 prior entry 동일

### §4.5 Paxos vs Raft

| | Paxos | Raft |
|--|--|--|
| 발표 | 1998 | 2014 |
| 이해도 | 어려움 | 친화적 |
| Leader | 약함 | 강함 (leader 중심) |
| 산업 | Chubby, Megastore | etcd, Consul, CockroachDB |

Modern preference = Raft.

### §4.6 Consensus 의 비용

- **Voting overhead** — majority RTT
- **Leader-only write** — bottleneck
- **Sync replication** — 과반 ack wait
- **Network partition** — minority unavailable

→ 고성능 store = consensus 회피 (eventual consistency).

### §4.7 Quorum 의 정확한 의미

**Strict quorum** = N node 중 majority (N/2 + 1):
- N=3 → 2
- N=5 → 3
- N=7 → 4

**일반화**: W + R > N → 적어도 한 node overlap.

---

## §5 Membership & Coordination Services

### §5.1 ZooKeeper / etcd / Consul

| | ZooKeeper | etcd | Consul |
|--|--|--|--|
| 발표 | 2008 (Yahoo) | 2013 (CoreOS) | 2014 (HashiCorp) |
| Algorithm | Zab | Raft | Raft |
| API | hierarchical tree | flat KV | KV + service mesh |
| 산업 | HBase, Kafka, Storm | Kubernetes, CockroachDB | HashiCorp 생태계 |

**용도**:
1. Leader election
2. Membership
3. Configuration
4. Distributed locks
5. Service discovery
6. Coordinated work (barrier, queue)

### §5.2 Linearizable read 의 cost

ZooKeeper 의 read 도 *linearizable* 하려면 consensus → 느림. 대안:
- *Local read* — eventually consistent, 빠름
- *Sync read* — quorum, linearizable
- *`sync()` + read* — explicit linearizable

### §5.3 Membership 알고리즘

- **Phi accrual failure detector** (Cassandra) — 확률적
- **SWIM** (Consul) — gossip
- **Lease** — 시간 제한 + renewal

> **함정 1**: failure detection 은 probabilistic. *false positive* 가능 → fencing token 필수.

### §5.4 Distributed Locks — Redlock controversy

**Redlock** (Redis-based):
- N independent Redis 의 majority lock
- Salvatore Sanfilippo

**Martin Kleppmann 의 비판** (2016):
- Process pause 시 fencing 없음
- Clock drift 시 일관성 깨짐
- 진짜 mutual exclusion 보장 안 됨

**Antirez 의 반박**:
- 단순 시스템에 충분
- Fencing 은 application layer

→ Production = ZooKeeper + fencing token 권장.

---

## §6 산업 사례

### §6.1 Google Spanner

- Multi-region strong consistency
- TrueTime + Paxos
- External consistency (linearizable)
- F1, AdWords 의 base

### §6.2 CockroachDB

- Spanner-inspired
- Raft per range
- Serializable default
- PostgreSQL wire protocol

### §6.3 etcd + Kubernetes

- Kubernetes 의 state store
- Raft consensus
- Pod state, secrets, config
- 최대 ~10k node cluster

### §6.4 Apache Kafka 의 KRaft

- 옛 — ZooKeeper 의존
- 신 — KRaft (내부 Raft) — ZooKeeper 제거
- Self-managed metadata

---

## §7 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "Strong consistency" = "linearizable" | 다양한 의미 |
| 2 | Quorum read = linearizable | concurrent write ordering 보장 안 됨 |
| 3 | Linearizable 항상 가능 | CAP — partition 시 양보 |
| 4 | Lamport = vector clock | 다름. Lamport = total, vector = partial |
| 5 | Total order broadcast > consensus | 같은 문제 |
| 6 | Paxos vs Raft 큰 차이 | 거의 같음. Raft 가 친화 |
| 7 | 모든 system 이 consensus 필요 | eventual + CRDT 회피 가능 |
| 8 | ZooKeeper read fast | local read 는 eventual |
| 9 | Consensus = 2PC | Consensus = value 합의, 2PC = transaction commit |
| 10 | FLP = consensus 불가 | 특정 model. 실용 partial sync |
| 11 | Redlock = safe lock | pause, drift 한계. ZooKeeper + fencing 권장 |
| 12 | Sequential = linearizable | Sequential 은 real-time 무시 |

---

## §8 자가점검

1. *Linearizability* 정의 + atomic register?
2. *Linearizable* vs *serializable*?
3. *Linearizable* vs *sequential consistency*?
4. *CAP* + *PACELC* 의미?
5. *Causality* 와 *happens-before*?
6. *Lamport* vs *vector clock*?
7. *Total order broadcast* 의 두 property + consensus 동등성?
8. *Consensus* 의 4 property?
9. *FLP impossibility*?
10. *Raft* 의 3 state + 2 RPC?
11. *ZooKeeper* 사용 사례?
12. *Redlock* 의 안전성 논쟁?

<details><summary>해답 (간략)</summary>

1. 시스템이 atomic register 처럼 보임. 각 op 가 시작-끝 사이 어느 한 순간 발생.
2. Linearizable: 단일 객체 recency. Serializable: multi-object transaction 의 직렬 동등.
3. Linearizable = real-time order. Sequential = program order 만.
4. CAP: partition 시 C or A. PACELC: partition 없을 때 L or C trade-off.
5. happens-before: same process program order + message send→receive + transitive.
6. Lamport: 한 counter, total order. Vector: 모든 node counter, partial order, concurrent 식별.
7. Reliable delivery + total order. Consensus 와 동등.
8. Agreement, Integrity, Validity, Termination.
9. Async + crash-stop + deterministic 에선 적어도 한 fault 처리 시 consensus 불가.
10. State: Follower, Candidate, Leader. RPC: AppendEntries, RequestVote.
11. Leader election, membership, configuration, locks, service discovery, coordination.
12. Process pause 시 fencing 없음, clock drift 시 일관성 깨짐. ZooKeeper + fencing 권장.

</details>

---

## §9 다음 학습으로

- **10장 (Batch)** — partitioned data 의 parallel processing
- **11장 (Stream)** — total order broadcast 의 응용. Kafka 의 distributed log
- **12장 (Future)** — unbundled DB, deterministic 시스템

---

## §10 한 줄 요약

> **Consistency + consensus = 분산 시스템의 *진짜 답*. Linearizability 의 atomic register. CAP + PACELC trade-off. Total order broadcast = consensus. Raft 의 leader election + log replication + safety. ZooKeeper/etcd 가 *시스템 의 뇌*. Spanner + CockroachDB 의 modern strong-consistency-at-scale.**
