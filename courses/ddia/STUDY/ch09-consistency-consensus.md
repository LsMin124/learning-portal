# Chapter 9: Consistency and Consensus — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 9** (책 p.321~388, PDF p.343~410).
> 9장: 책의 *클라이맥스*. 8장의 어려움 위에서 *강한 보장* 을 어떻게 만드나. **Linearizability**, **causal consistency**, **consensus** (Paxos, Raft).

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
- **예상 학습 시간**: 240~300분 (책의 가장 어려운 챕터)

---

## 1. Linearizability — 가장 강한 consistency

### 1.1 직관

> 시스템이 *단일 atomic register* 처럼 보임 — 동시 operation 이 *어떤 직렬 순서* 로 실행된 것 같음.

각 operation 이 *시작-끝 사이 어느 한 순간* 에 *원자적으로* 발생 (linearization point).

### 1.2 정확한 정의

3 client 가 동시 read/write:

```
Client A: write x=1 ----|
Client B:       read x ----|  → ?
Client C:                read x ----|  → 1
```

- B 의 read 는 0 또는 1 모두 OK (write 와 시간 겹침)
- 그러나 *B 가 1 을 본 후 C 가 0 을 보면 위반*. 한 번 1 이 보이면 *그 이후 read 는 모두 1*

이게 *recency guarantee* — "최근 commit 한 값 봄".

### 1.3 *Linearizable 시스템 의 흔한 오해*

- ❌ "DB 의 default" — Postgres default 는 *Read Committed*, *not linearizable*
- ❌ "Snapshot isolation = linearizable" — 다름. snapshot 은 *과거 시점* 일관성, linearizable 은 *최신 보장*
- ❌ "Quorum read = linearizable" — concurrent write 의 ordering 보장 안 됨

### 1.4 어디서 필요?

1. **Lock service** — 한 번에 한 client 만 lock 보유
2. **Constraint** — unique constraint, foreign key
3. **Cross-channel timing** — image upload + url 의 ordering
4. **Leader election** — *유일한* leader

---

## 2. Linearizability 구현

### 2.1 Single-leader replication

leader 가 *linearization point*. follower 가 sync 되면 *linearizable*. 단:
- *Follower read* 는 *async lag* 로 *not linearizable*
- *Sync follower* read 는 linearizable

### 2.2 Consensus algorithm

Paxos, Raft — *합의된 결정* 이 linearizable. 9장 §3.

### 2.3 Multi-leader / Leaderless — *not linearizable*

- Multi-leader: concurrent write 의 *resolve 후* 일관성 — *not linear*
- Leaderless (Cassandra): quorum read 가 *대부분* linearizable 같지만 *edge case* 에서 위반

### 2.4 Cost — CAP

> Linearizability 와 *availability under partition* 은 *동시 불가*.

Partition 시 양쪽 부분이 *서로 모르고* write 하면 linearizability 깨짐. 어느 쪽이 *멈춰야* 함 (= unavailable).

대부분 산업 시스템은 *availability 우선* (eventual consistency). 진짜 linearizable 이 필요한 곳만 cost 감수.

---

## 3. Ordering Guarantees

### 3.1 Total order vs Partial order

| 순서 | 정의 |
|--|--|
| **Total** | 모든 두 event 가 *비교 가능* (A < B 또는 B < A) |
| **Partial** | 일부 event 가 *incomparable* (concurrent) |

Linearizable = total order.
Causal consistency = partial order (causality 기반).

### 3.2 Causality

> A 가 B 의 원인이면 (A 가 B 보다 *먼저 일어났음*), 모든 node 가 *A 를 B 보다 먼저* 봐야.

predecessors:
- *Same process*: program order
- *Inter-process*: message 의 send → receive
- *Transitive*: A → B, B → C ⟹ A → C

이 partial order 가 **happens-before relation** (Lamport 1978).

### 3.3 Lamport Timestamps

각 node 가 *counter* + *node ID*:

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

*Total order* 만들지만 *causality* 만 보장 (concurrent events 의 *임의 순서*).

### 3.4 Total Order Broadcast

모든 node 가 *같은 순서로* message 받음:
- **Reliable delivery** — 모든 non-fail node 가 받음
- **Totally ordered delivery** — 모든 node 가 *같은 순서*

이게 *consensus 와 동등* — 한쪽이 풀리면 다른 쪽도 풀림. 9장의 핵심 정리.

Kafka 의 *partition 안* 이 total order. *전체 cluster* 는 partial. 11장 의 핵심.

---

## 4. Consensus

### 4.1 정의

> N 개의 process 가 *한 값* 에 합의:
> - **Uniform agreement** — 모든 node 가 *같은 값* 결정
> - **Integrity** — 한 번 결정 후 *바뀌지 않음*
> - **Validity** — 결정된 값이 *어떤 proposal* 의 것
> - **Termination** — fault-tolerant — 살아있는 node 는 *결국* 결정

### 4.2 FLP Impossibility

> *Asynchronous network + crash-stop* 에서 *deterministic consensus 불가능* — *적어도 한 fault 처리 시* (Fischer, Lynch, Paterson 1985)

**우회**:
- Randomization (Ben-Or)
- Timing 가정 (failure detector — Chandra-Toueg)
- Partial sync 가정

산업 algorithm 들이 *partial sync* + *timing-based failure detector* 사용.

### 4.3 Consensus Algorithms

| Algorithm | 특징 |
|--|--|
| **Paxos** (Lamport 1998) | classic, 이해 어려움 |
| **Raft** (Ongaro 2014) | 이해 친화적. etcd, Consul, CockroachDB |
| **Zab** | ZooKeeper 의 algorithm |
| **Viewstamped Replication** (Liskov) | Raft 의 영감 |

모두 *유사한 핵심*:
1. *Leader election* — 한 node 가 *master*
2. *Log replication* — leader 가 proposal 을 *follower 에 복제*
3. *Commit* — majority 가 ack 하면 commit
4. *Failure* — leader 실패 시 *새 leader 선출* + recovery

### 4.4 Raft 동작 개요

![Figure 9-7 — Raft 의 leader, follower, candidate 상태 전이. 책 p.367](/courses/ddia/figures/ch09/fig-9-7.png)

- **Term** — *epoch*. 새 leader 선출마다 ↑
- **Leader election** — follower 가 *random timeout* 후 candidate 가 됨, 과반 vote 받으면 leader
- **Log replication** — leader 가 entry append + follower 에 *AppendEntries* RPC. majority ack → commit
- **Safety** — *log matching property* — 같은 index 의 entry 가 *같은 term* 이면 *모든 prior entry 도 동일*

### 4.5 Consensus 의 *비용*

- **Voting overhead** — 매 결정마다 *majority RTT*
- **Leader-only write** — leader 가 *throughput 병목*
- **Sync replication** — leader 가 *과반 ack* 까지 wait
- **Network partition handling** — minority 측은 *unavailable*

이 비용 때문에 *고성능 store* 는 *consensus 회피* — eventual consistency.

---

## 5. Membership & Coordination Services

### 5.1 ZooKeeper / etcd / Consul

작은 *consensus-based store* 가 *큰 시스템의 뇌* 역할:

용도:
1. **Leader election** — 누가 master?
2. **Membership** — 어떤 node 가 살아있나?
3. **Configuration** — service 의 endpoint, secrets
4. **Locks** — distributed lock
5. **Service discovery** — name → endpoint
6. **Coordinated work** — barrier, queue

### 5.2 Linearizable read 의 cost

ZooKeeper 의 read 도 *linearizable* 하려면 *consensus* 통과해야 → 느림. 대안:
- **Local read** — *eventually consistent*, 빠름
- **Sync read** — quorum 검증, linearizable

### 5.3 Membership 알고리즘

- **Phi accrual failure detector** (Cassandra) — heartbeat 의 *확률적* dead 판정
- **SWIM** (Consul) — gossip 기반 membership
- **Lease** — *시간 제한 lease* 가 *renewal* 안 되면 dead

> **함정 1**: failure detection 은 *probabilistic*. 절대 truth 아님. *false positive* 항상 가능 → fencing token 필수.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "Strong consistency" = "linearizable" | 다양한 의미. 정확히 명시 (linearizable, serializable, causal) |
| 2 | Quorum read = linearizable | 일반적으로 X. concurrent write 의 ordering 보장 안 됨 |
| 3 | Linearizable 이 *항상* 가능 | CAP — partition 시 availability 또는 linearizability 양보 |
| 4 | Lamport timestamp = vector clock | 다름. Lamport = total order, vector = partial order |
| 5 | Total order broadcast > consensus | 같은 문제. 한쪽 풀면 다른쪽 풀림 |
| 6 | Paxos vs Raft 의 *큰 차이* | 거의 같음. Raft 가 *교육·구현* 친화 |
| 7 | 모든 distributed system 이 consensus 필요 | eventual + CRDT 로 회피 가능. 정말 필요한 부분만 |
| 8 | ZooKeeper 의 read 가 *fast* | local read 는 eventual. linearizable read 는 quorum |
| 9 | Consensus 가 *2PC* 와 같음 | 다름. Consensus 는 *value 합의*. 2PC 는 *transaction commit* |
| 10 | FLP impossibility = consensus 불가 | 특정 model (async + crash). 실용 algorithm 은 partial sync |

---

## 자가점검

1. *Linearizability* 의 정의 + atomic register 비유.
2. *Linearizable* vs *serializable* 의 차이.
3. *Causality* 와 *happens-before* relation.
4. *Lamport timestamp* 와 *vector clock* 의 차이.
5. *Total order broadcast* 의 두 property.
6. *Consensus* 의 4 가지 property (agreement, integrity, validity, termination).
7. *FLP impossibility* — 어떤 model 에서 무엇이 불가능.
8. *Raft* 의 3 핵심 mechanism (election, log replication, safety).
9. *ZooKeeper* 가 *큰 시스템의 뇌* 로 쓰이는 5 가지 사용 사례.
10. *Linearizable read* 가 ZooKeeper 에서 왜 *비싼가*.

### 해답 (간략)

1. 시스템이 *atomic register* 처럼 보임. 각 op 가 시작-끝 사이 어느 한 순간 발생.
2. Linearizable: 단일 객체 *recency*. Serializable: multi-object transaction 의 *직렬 동등*. 다름.
3. happens-before: same process program order + message send→receive + transitive.
4. Lamport: 한 counter, total order, causality 보장. Vector: 모든 node 의 counter array, partial order, concurrent 식별.
5. Reliable delivery (모든 node 받음) + total order (같은 순서).
6. agreement (모두 같은 값), integrity (변하지 않음), validity (proposal 의 값), termination (살아있는 node 결정).
7. Async network + crash-stop + deterministic algorithm 에선 *적어도 한 fault* 처리 시 consensus 불가.
8. Election (random timeout → candidate → majority vote), Log replication (leader → AppendEntries → majority ack → commit), Safety (log matching property).
9. (1) leader election (2) membership (3) configuration (4) locks (5) service discovery.
10. Read 마다 *quorum 의 ack* 필요 — RTT 추가. local read 가 *eventually consistent* 이면 빠름.

---

## 다음 학습으로

- **10장 (Batch)** — partitioned data 의 *parallel processing*
- **11장 (Stream)** — total order broadcast 의 응용. Kafka 가 *distributed log*
- **12장 (Future)** — unbundled DB, *deterministic 시스템* 의 미래
