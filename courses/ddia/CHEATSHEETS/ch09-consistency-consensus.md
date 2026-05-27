# Ch 9 Consistency and Consensus — 치트시트

## TL;DR

- **Linearizability**: 시스템이 *atomic register* 처럼. recency guarantee
- **Causal consistency**: linearizable 보다 약함. happens-before 만
- **Total order broadcast** ≡ **Consensus** (수학적 동등)
- **Consensus** 의 4 property: agreement / integrity / validity / termination
- **FLP impossibility**: async + crash-stop 에선 deterministic consensus 불가. 실용은 *partial sync* 가정
- **Raft / Paxos**: 산업 표준 consensus. election + log replication + safety
- **ZooKeeper / etcd**: consensus-based coordination service — leader election, locks, membership, config

---

## Quick Reference

### 표 1. Consistency 모델 위계

```
strongest:
  Linearizable (atomic register, recency)
    |
  Sequential consistency (program order 유지)
    |
  Causal consistency (happens-before 유지)
    |
  Read-your-writes / Monotonic reads
    |
  Eventual consistency
weakest
```

각 *위 level* 이 *모든 아래 level* 을 함의.

### 표 2. Linearizable vs Serializable

| | Linearizable | Serializable |
|--|--|--|
| 범위 | 단일 object | multi-object transaction |
| 보장 | recency | 직렬 동등 |
| 비용 | high | high |
| 예시 | counter, lock | 송금 transaction |

**둘 다 = strict serializable** (Spanner).

### 표 3. Ordering

| Concept | 특징 |
|--|--|
| Total order | 모든 두 event 비교 가능 |
| Partial order | 일부 incomparable (concurrent) |
| happens-before | causality + program order + send→receive |
| Lamport timestamp | (counter, node_id), total order, causality 보장 |
| Vector clock | counter array per node, partial order, concurrent 식별 |
| Total order broadcast | reliable + same order. = consensus |

### 표 4. Consensus

```
Properties:
  1. Agreement — 모두 같은 값
  2. Integrity — 한 번 결정 후 불변
  3. Validity — proposal 의 값
  4. Termination — 살아있으면 결정

FLP Impossibility (1985):
  async network + crash-stop + deterministic
  → 적어도 1 fault 처리 시 consensus 불가능

우회:
  - Randomization
  - Failure detector (partial sync)
  - Timing 가정
```

### 표 5. Consensus algorithms

| | 비고 |
|--|--|
| Paxos (Lamport 1998) | classic, 이해 어려움 |
| Raft (Ongaro 2014) | 이해 친화. **etcd, Consul, CockroachDB** |
| Zab | ZooKeeper |
| Viewstamped Replication | Raft 영감 |

### 표 6. Raft 핵심 mechanism

```
1. Leader Election
   - random timeout (150-300ms)
   - candidate → request vote → majority → leader

2. Log Replication
   - leader: append entry → AppendEntries to followers
   - majority ack → commit
   - leader 가 commit index follower 에 전달

3. Safety
   - Log Matching Property:
     같은 (index, term) 의 entry 는 *모든 prior entry 도 동일*
   - Election restriction:
     candidate 의 log 가 majority 만큼 *최신* 이어야 leader
```

### 표 7. ZooKeeper 의 사용 패턴

| 패턴 | znode 방식 |
|--|--|
| Lock | ephemeral + sequential, watch on previous |
| Leader election | ephemeral + sequential, lowest # = leader |
| Membership | ephemeral node per node, watcher on parent |
| Config | persistent znode, watcher on data change |
| Service discovery | service name → endpoint znode |
| Barrier | sequential, count children |

### 표 8. CAP vs PACELC

```
Partition 시:
  CP: linearizable, minority unavailable (etcd)
  AP: available, eventual consistency (Cassandra)

PACELC (Abadi):
  P → A or C
  Else → L or C
  
산업:
  CP+EC: Postgres sync, etcd, ZK
  AP+EL: Cassandra, DynamoDB
  CP+EL: 거의 없음
  AP+EC: 거의 없음
```

---

## Mind Map

```
9장 Consistency and Consensus
├─ 1. Linearizability
│   ├─ atomic register, recency
│   ├─ 구현: single-leader, consensus
│   └─ Cost: CAP — partition 시 unavailable
├─ 2. Ordering
│   ├─ Total vs Partial order
│   ├─ Causality (happens-before)
│   ├─ Lamport timestamp
│   ├─ Vector clock
│   └─ Total order broadcast = consensus
├─ 3. Consensus
│   ├─ 4 properties
│   ├─ FLP impossibility
│   ├─ Raft (election + log + safety)
│   └─ 대안: Paxos, Zab
└─ 4. Coordination service
    ├─ ZooKeeper / etcd / Consul
    └─ Leader election / locks / membership / config
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | Linearizable = atomic register, recency. Partition 시 unavailable |
| 2 | Causal consistency 가 partial order. Lamport (total) vs Vector (partial) |
| 3 | Total order broadcast ≡ Consensus 수학적 동등 |
| 4 | Consensus = 4 property. FLP — async + crash-stop 에선 불가 |
| 5 | Raft = election + log replication + log matching property |
| 6 | ZooKeeper = consensus 기반 coordination. 큰 시스템의 뇌 |
