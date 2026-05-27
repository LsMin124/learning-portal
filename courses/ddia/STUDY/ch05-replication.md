# Chapter 5: Replication — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 5** (책 p.151~199, PDF p.173~220).
> 5장: 같은 데이터의 *복제본* 을 여러 node 에 둠. *고가용성, 지연 감소, scale, durability*. 핵심 3 접근: **Single-leader, Multi-leader, Leaderless**.

## 들어가기 전에

- **선수 지식**: 3장 storage engine, 4장 encoding, 기본 분산 시스템 용어 (node, RTT, partition)
- **학습 목표**
  1. **Replication 의 4 목적** — geographic, availability, throughput, durability
  2. **Single-leader** — Postgres, MySQL — *가장 흔한* 모델
  3. **Sync vs async** replication 의 trade-off
  4. **Replication lag** + *5 가지 anomaly* (read-your-writes, monotonic read, ...)
  5. **Multi-leader** — geographic distribution, conflict resolution
  6. **Leaderless** — Cassandra, Riak — *quorum* (W + R > N)
- **예상 학습 시간**: 180~220분 (책의 가장 *기술적* 챕터 중 하나)

---

## 1. Replication 의 4 목적

> "*같은 데이터의 복사본을 여러 머신에 두는 것*"

이유:
1. **Geographic latency** — 사용자 가까운 region 에 replica
2. **Availability** — 한 node 죽어도 서비스 지속
3. **Read throughput** — read 를 여러 replica 로 분산
4. **Durability** — 데이터 손실 보호 (replication 이 *backup* 아님, 별개)

핵심 도전 — *변화를 어떻게 propagate* 하나? 그리고 *propagate 도중 read* 가 어떻게 처리?

---

## 2. Leaders and Followers — Single-leader

### 2.1 동작

![Figure 5-1 — Single-leader replication. 책 p.153](/courses/ddia/figures/ch05/fig-5-1.png)

1. **Leader (primary)** — 모든 write 처리
2. **Follower (replica, secondary, hot standby)** — leader 로부터 *replication log* 받아 적용
3. **Client 의 read** — leader 또는 follower 어디서나 (보통 분산)
4. **Client 의 write** — *오직 leader*

이게 PostgreSQL, MySQL, MongoDB, Oracle 등 *대부분 RDBMS + 일부 NoSQL* 의 default.

### 2.2 Sync vs Async

leader 가 write 받으면:
- **Sync replication**: 적어도 하나의 follower 가 *확인* 한 후 client 에게 OK
  - 보장: follower 에 *반드시* 반영
  - 문제: follower 가 느리면 *leader 도 같이 느려짐*
- **Async replication**: leader 는 *바로* client OK, follower 는 *나중에* 받음
  - 빠름, 그러나 *replication lag* 가능
  - leader 가 *crash 후 failover* 시 *최근 commit 손실* 가능 (durability 위험)

![Figure 5-2 — Sync 와 async replication. 책 p.155](/courses/ddia/figures/ch05/fig-5-2.png)

**산업 패턴 — Semi-synchronous**:
- 1개 follower 만 sync, 나머지 async
- leader 가 *어떤* sync follower 든 확인 받으면 OK
- 균형: 빠름 + 적어도 한 copy 확실

### 2.3 새 Follower 추가

production 에서 *downtime 없이* 새 follower 추가:

1. Leader 의 *consistent snapshot* 생성 (lock 없이, MVCC 활용)
2. 새 follower 에 snapshot copy
3. snapshot 시점부터의 *replication log* 적용
4. follower 가 *caught up* 되면 라이브 트래픽 시작

### 2.4 Node Outage 대응

**Follower 실패** — 단순. follower 가 *어디까지 처리* 했는지 기억하고 (replication log offset), 복구 후 거기부터 catch-up.

**Leader 실패 — Failover**:
1. Leader down 감지 (heartbeat timeout)
2. 새 leader 선출 — 보통 *가장 최신 replication log* 가진 follower
3. Client 가 새 leader 알도록 routing 변경
4. 옛 leader 가 복구되면 *follower* 로 강등

**Failover 의 위험**:
- *Split brain* — 두 leader 가 동시에 (옛 leader 가 복구되면서 또 leader 행세)
- *데이터 손실* — async lag 때문에 새 leader 에 없는 commit
- *Timeout 결정* — 너무 짧으면 false failover, 너무 길면 outage 길어짐

> **함정 1**: failover 의 *모든 corner case* 가 어렵다. 실제 production 의 outage 대부분이 *failover 실패* 또는 *split brain* 에서 발생.

### 2.5 Replication Log 구현

| 방식 | 장점 | 단점 |
|--|--|--|
| **Statement-based** | 가장 작음 | non-deterministic (NOW(), RAND()) 문제 |
| **WAL shipping** | DB 가 native 사용 | binary, version 종속 |
| **Logical (row-based)** | DB version 독립 | parser 필요 |
| **Trigger-based** | application 제어 | overhead 큼 |

**Logical replication** (Postgres 의 logical decoding, MySQL row-based binlog) 가 *현대 표준*. 다른 DB 로 데이터 보낼 때도 사용 — *CDC (Change Data Capture, 11장)*.

---

## 3. Replication Lag — Eventual Consistency 의 문제

### 3.1 Eventually consistent — *시간 충분히 흐르면 다 같은 값*

하지만 *현재 순간* 엔 replica 마다 다른 값. 사용자에게 *이상한 경험* 줌.

### 3.2 *5 가지 anomaly*

#### Anomaly 1: Read-Your-Writes (=Read-after-Write)

사용자 A 가 *자기 댓글* 을 단 직후 *follower* 에서 read → *없음* (lag 때문)

![Figure 5-3 — Read-after-write 문제. 책 p.163](/courses/ddia/figures/ch05/fig-5-3.png)

**해결**:
1. *자기 데이터는 leader 에서* (e.g., 자기 프로필 페이지)
2. *최근 1분간 자기 write 시각 추적*, 그 시각 이전 follower 사용
3. Client 가 *마지막 write 의 log offset* 보유, follower 가 *그 이후* 따라잡을 때까지 wait
4. Cross-device 일치는 더 어려움 (centralized 추적 필요)

#### Anomaly 2: Monotonic Reads

사용자가 두 번 새로고침 — 처음엔 *댓글 보임*, 둘째엔 *없어짐* (다른 follower, lag 다름)

**해결**: 같은 사용자가 *같은 replica* 만 사용 (hash by user ID).

#### Anomaly 3: Consistent Prefix Reads

부분 인과 순서가 깨짐:

```
Mr. Poons: "How far into the future can you see, Mrs. Cake?"
Mrs. Cake: "About ten seconds usually."
```

→ replica 가 *Mrs. Cake 의 답을 먼저* 받으면:

```
Mrs. Cake: "About ten seconds usually."     # 답이 먼저
Mr. Poons: "How far into the future..."      # 질문 다음
```

![Figure 5-5 — Consistent prefix 깨짐. 책 p.166](/courses/ddia/figures/ch05/fig-5-5.png)

**해결**: *인과 관련 write 를 같은 partition* (6장).

#### Anomaly 4 & 5

- *Update 손실* — 동시 update 가 *덮어쓰기* (LWW 문제)
- *Phantom* — *복잡한 multi-step* read 의 일관성 부재

→ 7장 transaction 에서 본격 처리.

### 3.3 *Solution* — 강한 consistency 모델

eventual consistency 가 *불충분* 하면:
- **Read-your-writes** 보장
- **Monotonic reads** 보장
- **Causal consistency** (Lamport / vector clock)
- **Strong consistency** (Linearizability — 9장)

대부분 application 엔 *eventual + read-your-writes* 면 충분. *9장* 에서 정밀 정의.

---

## 4. Multi-Leader Replication

### 4.1 동기

Single-leader 의 한계:
- *Geographic* — 모든 write 가 한 region 의 leader 로 가야 → 멀리 사는 사용자 느림
- *Offline support* — mobile / disconnected 사용자가 *자기 local* 변경 후 sync
- *Collaborative editing* — Google Docs 처럼 *동시 편집*

해결 — **각 region 에 leader, leader 끼리 async 동기화**:

![Figure 5-6 — Multi-leader cross-datacenter replication. 책 p.169](/courses/ddia/figures/ch05/fig-5-6.png)

### 4.2 도전 — Conflict Resolution

같은 record 를 두 leader 가 *동시 수정* → conflict.

**처리 방법**:
1. **Conflict avoidance** — 같은 record 는 *한 region 에서만* (sharding by user → user 의 home region)
2. **Last Write Wins (LWW)** — timestamp 비교, 큰 게 이김. *시계 동기화 문제* (8장)
3. **CRDT** (Conflict-free Replicated Data Type) — 자료구조 자체가 commutative — math 적으로 conflict 없음 (counter, set 등)
4. **Custom resolution** — application 이 *두 version 모두* 받아 결정 (e.g., 사용자에게 manual merge UI)

> **함정 2**: Multi-leader 의 *conflict resolution* 이 가장 복잡한 부분. 단순한 경우 외엔 *큰 운영 부담*. CouchDB, BDR (Postgres), AWS DynamoDB Global Tables 등이 옵션.

### 4.3 Multi-leader Topology

leader 들이 *어떤 topology* 로 연결?

- **All-to-all** — N개 leader 가 *모두 서로* (N² connections)
- **Circular** — 1 → 2 → 3 → 1
- **Star** — 중앙 leader + 다른 leader (실은 single-leader 의 변형)

각 trade-off 가 *fault tolerance + lag* 영향.

---

## 5. Leaderless Replication — Cassandra, Dynamo

### 5.1 동작

> *Leader 없음*. 모든 replica 가 *직접* client 의 write 받음.

Dynamo (Amazon 2007 paper) 영향 — Cassandra, Riak, Voldemort 가 *Dynamo-style*.

![Figure 5-10 — Leaderless 의 read repair + anti-entropy. 책 p.179](/courses/ddia/figures/ch05/fig-5-10.png)

Client 가 *N 개 replica 에 동시 write*. *W* 개 OK 받으면 성공:
- W = 1: 빠름, 데이터 손실 위험
- W = N: 모든 replica 에 확실, 느림
- W = quorum (N/2 + 1): 균형

Read 도 *R 개 replica 에서 동시 read* → *가장 최신* version 선택:
- *Version vector* 또는 *timestamp* 로 최신 판정

### 5.2 Quorum — W + R > N

이 조건이면 *적어도 한 replica* 가 *최신 write 와 read 모두 보유* → *최신 read* 보장.

- N=3, W=2, R=2: quorum, *fault tolerance 1*
- N=3, W=3, R=1: read 빠름, 1 node 실패 시 write 멈춤
- N=5, W=3, R=3: fault tolerance 2

### 5.3 Sloppy Quorum + Hinted Handoff

N replica 중 일부가 *unreachable* 일 때:
- *Sloppy quorum*: 정해진 N 외의 *다른 node* 에 임시 write
- *Hinted handoff*: 원래 node 복구되면 *임시 write 이관*

→ availability 우선이지만 *진정한 quorum 아님*. 일관성 약화.

### 5.4 Anti-entropy + Read Repair

replica 사이 *eventual sync*:
- **Read repair**: read 시 stale version 발견하면 *자동으로 새 version 으로 update*
- **Anti-entropy process**: background 가 *Merkle tree* 등으로 replica 비교 + 동기화

### 5.5 Concurrent Writes — *부분 순서*

같은 key 에 *동시* write — *어떤 게 이김?*:

**Last Write Wins (LWW)** — 단순하지만 *시계 부정확* 위험.

**Version vector** (vector clock 의 일종):
- 각 replica 가 *모든 다른 replica 의 version counter* 보유
- write 마다 *자기 counter 증가*
- 두 version 의 vector 가 *비교 가능* (한쪽이 다른 쪽보다 큼 또는 동등) → 더 큰 게 이김
- *서로 incomparable* (동시 write) → application 이 *둘 다 받음*

CRDT, OR-set 등이 정교한 merge 제공.

---

## 6. 세 모델 비교

| 측면 | Single-leader | Multi-leader | Leaderless |
|--|--|--|--|
| Write 라우팅 | leader 만 | 어느 leader든 | 어느 replica든 |
| 충돌 | 없음 (leader 결정) | 빈번 | quorum 으로 회피 |
| 일관성 | 강 (leader 에서) | 약 (eventual) | quorum 으로 조정 |
| Geographic | 한 region | multi-region native | multi-region OK |
| Failover | 복잡 | 단순 (다른 leader) | 자동 |
| 예시 | Postgres, MySQL, MongoDB | CouchDB, Postgres BDR, DynamoDB Global | Cassandra, Riak |

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Replication = backup | 두 가지 다른 목적. backup 은 *과거 시점 복구* (replication 은 *현재* 만) |
| 2 | Async lag 무시 | read-your-writes anomaly 가 사용자 confusion |
| 3 | Failover 가 단순 | split brain, lag-induced data loss, timeout tuning 모두 복잡 |
| 4 | Multi-leader 가 *항상* 좋음 | conflict resolution 의 *지속적 운영 비용* |
| 5 | LWW 가 안전한 conflict 해결 | 시계 동기화 문제 (8장). 데이터 잃을 수 있음 |
| 6 | Quorum 이면 *strong consistency* | quorum 도 *concurrent write* 의 *동시 ordering* 안 보장. linearizability 별개 (9장) |
| 7 | Sloppy quorum = quorum | 정해진 N 외 node 사용 — availability 우선, *진정한 quorum 아님* |
| 8 | CRDT 가 *모든 충돌* 해결 | 일부 type 만 (counter, set). 일반 application state 는 X |
| 9 | Statement-based replication 이 단순 | non-deterministic (NOW, RAND) 문제. logical replication 권장 |
| 10 | replication 이 *durability 보장* | RAID + backup + cross-region 의 *별도 정책* 필요 |

---

## 자가점검

1. Replication 의 *4 가지 목적*.
2. *Single-leader* 의 write/read flow.
3. *Sync vs async* replication 의 trade-off.
4. *Failover* 의 *3 가지 risk*.
5. *Replication log* 의 4 가지 구현 방식.
6. Replication lag 의 *5 가지 anomaly* + 각 *해결 전략*.
7. *Multi-leader* 의 *3 가지 사용 사례*.
8. *Conflict resolution* 의 *4 가지 방법*.
9. *Quorum* 조건 `W + R > N` 이 *왜* strong read 보장?
10. *Version vector* 가 *concurrent write* 어떻게 식별.

### 해답 (간략)

1. Geographic latency, availability, read throughput, durability.
2. Write → leader, leader → log → followers. Read → leader 또는 follower.
3. Sync: durability 보장, leader 가 느려질 수 있음. Async: 빠름, lag + failover 시 data loss.
4. (1) split brain (2) lag-induced data loss (3) timeout 결정 (false failover or 긴 outage).
5. Statement / WAL / Logical (row) / Trigger.
6. (1) Read-your-writes (자기 데이터는 leader). (2) Monotonic reads (같은 user → 같은 replica). (3) Consistent prefix (인과 데이터 같은 partition). (4) Lost update (transaction). (5) Phantom (transaction).
7. (1) Multi-region (geographic) (2) Offline-capable (mobile) (3) Collaborative editing.
8. (1) Avoid (sharding) (2) LWW (3) CRDT (4) Custom (manual merge).
9. W + R > N → write quorum과 read quorum 이 *적어도 한 node 에서 overlap*. 그 node 가 최신 write 와 read 모두 보유.
10. 각 replica 의 counter vector 보유. 한쪽이 *모두 ≤ 다른 쪽* 이면 happens-before. *그렇지 않으면 concurrent*. concurrent 면 application 이 둘 다 받아 merge.

---

## 다음 학습으로

- **6장 (Partitioning)** — replication + partitioning 의 결합
- **7장 (Transactions)** — replication lag 의 anomaly 를 *transaction isolation* 으로 해결
- **8장 (Distributed Trouble)** — failover 의 어려움. *clock, partition, GC pause*
- **9장 (Consistency and Consensus)** — quorum 의 정확한 의미, linearizability
