# Ch 9 Consistency and Consensus — 퀴즈

> 8 문항.

### Q1. Linearizable vs Serializable

흔히 혼동. 정확한 차이.

<details><summary>답</summary>

| | Linearizable | Serializable |
|--|--|--|
| 범위 | *단일 register / object* | *multi-object transaction* |
| 보장 | *recency* — 최신 write 가 즉시 보임 | *직렬 등가* — concurrent transaction 의 결과 = 어떤 직렬 실행 |
| 적합 | counter, lock, leader election | multi-row transaction (송금) |
| 비용 | high (consensus per op) | high (lock 또는 OCC) |

**모두 갖춤 = strict serializable** — Spanner 의 보장. 가장 비싼 consistency.

산업 — *서로 다른 시스템 부분에 다른 level*. core counter 는 linearizable, OLTP 는 serializable, 그 외는 eventual.

</details>

### Q2. CAP 의 *정확한 해석*

5 node 의 *Raft 기반 etcd cluster*. *3-2 partition* 발생 시 각 쪽의 동작.

<details><summary>답</summary>

**Majority side (3 node)**:
- Quorum 보유 (3 ≥ floor(5/2)+1 = 3)
- Leader 가 그쪽에 있거나 *재선출*
- Read/write 정상

**Minority side (2 node)**:
- Quorum 미달
- Leader 가 거기 있어도 *commit 못함* (majority ack 못 받음)
- Write 거부 → unavailable
- Stale read 만 가능 (옛 데이터)

→ *CP 시스템* — linearizability 보장, minority partition 의 *availability 양보*.

대조 — Cassandra 의 *AP*:
- 양쪽 모두 *write 받음* (sloppy quorum)
- partition 회복 시 *hinted handoff + last-write-wins resolve*
- Linearizability 위반 가능

**산업 선택**:
- *State machine* (leader election, config): CP (etcd, ZK)
- *Data storage* (user data, log): AP (Cassandra) 또는 *adjustable* (Cosmos DB 의 5 level)

</details>

### Q3. Lamport timestamp 의 한계 — Vector clock 필요한 경우

Lamport timestamp 가 total order 만들지만 *concurrent 식별 못함*. 왜 중요?

<details><summary>답</summary>

**Lamport timestamp**:
- `(counter, node_id)` 의 total order
- *causally related* 이면 항상 `t(a) < t(b)`
- 그러나 *concurrent* 인 두 event 도 *strict order* — 어느 게 *진짜 먼저* 인지 모름

**Vector clock**:
- 모든 node 의 *counter array*
- 두 vector 가 *비교 가능* 하면 causally related, *incomparable* 이면 concurrent
- *Concurrent 명시적 식별*

**Lamport 가 충분한 경우**:
- 단순 total order broadcast (모든 node 가 같은 순서)
- *concurrent 의 임의 순서* 가 OK
- 예: log sequence number

**Vector 가 필요한 경우**:
- *Concurrent write 의 conflict 감지* (Riak, Cassandra 의 multi-version)
- *Causality 추적* (multi-leader replication 의 sync)
- 예: 5장의 leaderless replication

**산업 패턴**:
- Kafka offset: Lamport 의 단순화 (single partition, monotonic)
- Cassandra: vector clock variant (timeuuid)
- CRDT (Riak): vector clock for concurrent merge

</details>

### Q4. Total order broadcast = Consensus

이 두 문제가 *수학적 동등* 이라는 의미.

<details><summary>답</summary>

**Reduction 1: Consensus from total order broadcast**:
1. 각 node 가 *자기 proposal* 을 broadcast
2. Total order 에서 *첫 번째 message* 가 *결정값*
3. 모든 node 가 *같은 순서* 받으므로 *같은 첫 번째* → agreement
4. 한 번 결정 후 *바꾸지 않음* → integrity
5. Validity, termination 도 broadcast 가 보장하면 따라옴

**Reduction 2: Total order broadcast from consensus**:
1. 각 message 를 *consensus 의 한 round* 로 처리
2. 모든 node 가 *어떤 message 가 i-번째* 에 동의
3. 순서가 결정됨

**Significance**:
- 한 문제 풀면 *다른 문제도* 풀림
- FLP impossibility 가 *둘 다* 적용
- Raft / Paxos 가 두 가지 *모두* 구현

**실용 시사**:
- Kafka 의 *consistent ordering* 이 consensus 와 같은 비용
- 단 Kafka 의 *partition 안* 만 total order — *partition 사이* 는 partial
- 그래서 Kafka 가 *Raft 없이도* 빠름 (scale 우선)

</details>

### Q5. Raft 의 leader election 디테일

`election timeout` 의 typical 값 + 왜 *random*?

<details><summary>답</summary>

**Typical 값**: 150~300ms (random, uniform distribution).

**왜 random?**:
- 모든 follower 가 *동시에* timeout 하면 *모두 candidate* → vote split → 아무도 majority 못 받음
- Random timeout 으로 *한 follower 가 먼저* candidate 됨 → vote 모음 → leader

**왜 그 값?**:
- *Network RTT* 의 ~10x — RTT 가 ~30ms 이면 timeout 150ms+
- 너무 짧음: false timeout (잠시 slow 일 뿐인 leader 를 잘못 dead 판정)
- 너무 김: leader failure 후 *outage 길어짐*

**Leader 의 heartbeat**:
- Leader 가 *election timeout 의 1/3 ~ 1/5* 마다 heartbeat (~50ms)
- Follower 의 timer reset

**Multi-term scenario**:
- 한 term 안에 *vote split* 발생 → 다음 random timeout 후 *다시 election*
- 보통 1~2 term 안에 결정. 최악 케이스에도 *몇 round*

**튜닝 — 실제 production**:
- AWS region 간 (~50ms RTT): election timeout 500-1000ms
- 같은 rack (~1ms RTT): 50-100ms
- *측정 후 결정*. tail latency 가 timeout 초과하면 false election.

</details>

### Q6. ZooKeeper 의 *현실적 사용*

Hadoop 의 HBase 가 ZooKeeper 를 *어떻게* 사용하는지 5 가지.

<details><summary>답</summary>

**HBase + ZooKeeper**:

1. **Master election** — HMaster 가 *유일한 active master*. ZK 의 *ephemeral node* 로 lock. Master 죽으면 ephemeral node 사라짐 → 다른 master 후보가 take over.

2. **Region server membership** — 각 RegionServer 가 *ephemeral znode* 생성. Master 가 그 watcher 로 *살아있는 server 목록* 알아냄.

3. **Metadata** — 어느 RegionServer 가 어느 Region 담당. *root region* 의 위치.

4. **Coordination** — log split, region assignment 등의 *동기적 작업*.

5. **Failure detection** — heartbeat 끊긴 RegionServer 의 *region 재할당* trigger.

**ZooKeeper 의 ZK 자체 patterns**:
- **Ephemeral nodes** — session 끝나면 자동 삭제 → membership, lock
- **Watches** — node 변경 시 push notification → reactive
- **Sequential nodes** — `lock-000001`, `lock-000002` 의 *fair lock*
- **ACL** — 권한 제어

**다른 사용처**:
- Kafka < 2.8: broker membership, topic config
- Kafka 2.8+: KRaft (자체 Raft) 로 ZK 분리
- Solr Cloud: shard 정보
- Spark Standalone: master election

**제약**:
- *작은 데이터* (수 KB znode) 만
- 큰 throughput X — Raft consensus 의 본질적 제약
- *외부 의존성* — 운영 부담 큼

</details>

### Q7. 디버그 — Raft cluster 가 *leader 없는 상태로 정체*

5 node Raft cluster 가 *수 분간* leader 없음. 모든 node 가 candidate. 진단.

<details><summary>답</summary>

**가능 원인**:

1. **Network partition** — node 들 사이 *지속적* connectivity 문제. 어느 쪽도 *majority* 형성 못 함.
   - 진단: `etcdctl endpoint health` 로 node 간 연결 확인
   - 해결: network 복구. 일시적이면 자체 회복

2. **Clock skew** — election timeout 이 *node 마다 다른 시각 인식*. *심한 경우* election cycle 안 끝남.
   - 진단: 각 node 의 `ntpq -p`. NTP sync 확인.
   - 해결: NTP 강제 sync

3. **Slow disk** — fsync 가 느려 *AppendEntries 처리* 못 따라잡음. follower 가 *leader 다운* 오판.
   - 진단: `iostat -x 1`. await time 점검.
   - 해결: SSD 로 교체, fsync interval 조정

4. **CPU starvation** — load 가 높아 *heartbeat 처리* 못함.
   - 진단: top, vmstat. context switch 폭주.
   - 해결: load 분산, CPU 추가

5. **Term inflation** — 한 follower 의 *비정상 high term* 으로 다른 모두 *step down*. 끝없는 election.
   - 진단: `etcdctl member list` 의 each node 의 term
   - 해결: 비정상 node *isolate + reset*

**예방**:
- *Election timeout > 5x typical RTT*
- 모든 node 의 *clock sync* (NTP 또는 PTP)
- *Disk latency 모니터링* (p99 < 10ms)
- *Cluster size 5 (또는 3)* 권장. 7+ 면 quorum 비용 ↑.

</details>

### Q8. 면접 — *왜 Spanner 는 진짜 strong consistency 인가*?

Google Spanner 가 *globally distributed* 인데 *strict serializable* 보장. 어떻게?

<details><summary>답</summary>

**핵심 기술 — TrueTime API**:

1. **GPS + atomic clock** — Google datacenter 마다 *GPS receiver + atomic clock*
2. **Uncertainty interval** — `TT.now()` 가 `[earliest, latest]` 반환 (7ms 이내)
3. **Commit wait** — transaction commit 후 *uncertainty 만큼 wait* 후 announce

**왜 strict serializable**:
- *Linearizable* (atomic register per row)
- *Serializable* (multi-row transaction)
- 둘 다 동시 보장 → strict serializable

**알고리즘**:
1. *Transaction T1 commit at TT.now() = [s_1_earliest, s_1_latest]*
2. T1 *latest 가 지난 후* 까지 wait — 다른 transaction 이 *T1 의 latest 시각 이후* 시작
3. → T1 < T2 의 *real-time order* 가 *모든 client 에 일관*

**대안 (TrueTime 없을 때)**:
- **Hybrid Logical Clock (HLC)** — physical + logical. CockroachDB
- **Sequencer service** — 중앙 시각 발급 service. Spanner 의 *작은 cluster* 버전
- **Raft consensus per shard** — multi-shard 면 *2PC over Raft*

**Cost**:
- *Commit wait* = uncertainty (~7ms) → throughput 영향
- *GPS 가 비쌈* — 일반 cloud 에선 못 함
- AWS, Azure 의 *Spanner-like* 시도 — CockroachDB (HLC), AWS Aurora Limitless (sequencer)

**시사**:
- *Hardware-level guarantee* 가 *software consensus* 보다 우월
- 그러나 *대부분 startup* 엔 *과한 정밀도*. eventual 또는 single-region linearizable 면 충분
- "*Strict serializable* 이 *진짜 필요한가?*" 가 first question. 대부분 답 — No.

</details>
