# Ch 5 Replication — 퀴즈

> 10 문항.

### Q1. Replication 의 4 목적

각 목적이 *어떤 architecture 결정* 으로 이어지나.

<details><summary>답</summary>

1. **Geographic** → multi-region replica, 사용자 가까운 region 으로 read 라우팅
2. **Availability** → standby replica + automatic failover
3. **Read throughput** → read replica, load balancer
4. **Durability** → replication + backup + cross-region 의 *결합*

각 목적은 *독립* — 한 가지를 위해 한 setup, 모두 위해 더 복잡한 setup. *replication 자체* 가 backup 대체는 아님 (소프트웨어 버그·실수가 모든 replica 에 전파).

</details>

### Q2. Sync vs Async vs Semi-sync

각 trade-off 와 *production 표준*.

<details><summary>답</summary>

| | Durability | Latency | Availability |
|--|--|--|--|
| Sync (모든 replica 확인) | 강 | 가장 느림 | 모든 replica up 필요 |
| Async | 약 (lag-loss) | 빠름 | replica 죽어도 OK |
| Semi-sync (1개 sync) | 중간 | 빠름 | sync replica 죽어도 다음 fallback |

**산업 표준 — Semi-sync**:
- PostgreSQL: `synchronous_standby_names = 'ANY 1 (replica_a, replica_b)'`
- MySQL: `rpl_semi_sync_master_wait_for_slave_count = 1`
- "최소 한 replica 확인" + 나머지 async → 빠르면서도 *적어도 하나의 copy* 보장

</details>

### Q3. Failover 의 corner case — Split brain

GitHub 2012 outage (MySQL failover 후 두 leader). 무슨 일?

<details><summary>답</summary>

**시나리오**:
1. Leader A 의 *network partition* — heartbeat 못 보냄
2. 시스템이 leader A 죽었다고 판단, leader B 승격
3. Client 가 B 로 라우팅, write 진행
4. A 의 network 회복 — 자기는 *여전히 leader* 라고 생각, 일부 client 가 A 로 write
5. **두 leader 의 다른 데이터** → reconcile 불가

**예방**:
- **Fencing token** — 새 leader 가 *monotonic 증가 token*, A 의 옛 token 무효
- **STONITH** ("Shoot The Other Node In The Head") — 새 leader 승격 전 옛 leader 강제 kill
- **Quorum-based election** (Raft, 9장) — 과반 합의로 leader

GitHub 사고 후엔 *Orchestrator + Vitess* 도입.

</details>

### Q4. Logical replication 의 이점

physical (WAL) vs logical (row-based) replication.

<details><summary>답</summary>

**Physical (WAL shipping)**:
- DB 의 내부 *page-level* binary diff
- 같은 DB version + same OS 필요
- Replica 가 *완전 1:1 copy*

**Logical (row-based)**:
- *Row-level event* (INSERT/UPDATE/DELETE) 형태
- DB version 독립 (upgrade 시 mixed-version 동작)
- 다른 시스템으로 보낼 수 있음 (Kafka, Elasticsearch — *CDC*)
- 더 큰 overhead

**산업 트렌드**: logical 이 dominant.
- PostgreSQL 10+ 의 logical replication
- MySQL row-based binlog
- AWS DMS, Debezium 등의 CDC tool

이게 11장 *event-driven architecture* 의 기반.

</details>

### Q5. Read-your-writes 의 4 가지 해결

사용자 A 가 *자기 댓글* 쓴 직후 *자기 댓글이 안 보임* 문제.

<details><summary>답</summary>

1. **자기 데이터는 leader** — user A 의 프로필 페이지는 항상 leader read. 다른 사람 댓글 read 는 follower OK.

2. **Write timestamp 추적** — client 가 "최근 1분 안에 write 함" 기억. 그 동안엔 leader 사용.

3. **Log offset wait** — client 가 *마지막 write 의 log offset* 보유. follower 가 그 offset 따라잡을 때까지 wait.

4. **Sticky session** — same user → same replica (consistent hashing). lag 가 있어도 *자기 자신* 에겐 일관.

**선택**: app 의 *복잡도 vs latency*. 보통 (1) + (4) 조합이 표준.

</details>

### Q6. Multi-leader 의 conflict resolution

같은 record 의 동시 update 가 *두 region* 에서 발생. 4 가지 처리.

<details><summary>답</summary>

1. **Conflict avoidance** — record 마다 *home region* 정함. 그 region 에서만 write. 단순하지만 사용자 이동 시 어색.

2. **LWW (Last Write Wins)** — timestamp 비교, 큰 게 이김. *시계 동기화 부정확* → 데이터 손실 (8장).

3. **CRDT** — counter, OR-set 같은 자료구조가 *math 적으로 commutative*. 자동 merge.
   - 예: Redis CRDB, Riak, Phoenix LiveView

4. **Custom merge** — application 이 *두 version 모두* 받음. e.g., Google Docs 의 operational transform, 사용자에게 manual merge UI.

**산업 패턴**: 단순 KV 면 LWW, counter / shopping cart 면 CRDT, 복잡한 객체면 custom.

</details>

### Q7. Quorum 계산

N=5, W=3, R=3 인 Cassandra cluster. 동시에 *몇 node 까지 실패해도* 서비스 유지?

<details><summary>답</summary>

**Write quorum** = W = 3. 5 - 3 = **2 node 까지 실패 시 write 가능**.

**Read quorum** = R = 3. 5 - 3 = **2 node 까지 실패 시 read 가능**.

→ 동시에 *2 node 실패까지* 양쪽 가능.

**W + R = 6 > N = 5** → quorum 보장. 적어도 한 node 가 *최신 write 와 read 모두* 가짐 → 최신 read 보장 (concurrent write 제외).

**다른 옵션 trade-off** (N=5):
- W=5, R=1: read 빠르지만 *0 node 실패 만* 허용 (모든 replica up 필요)
- W=1, R=5: write 빠르지만 read 모든 replica 검사
- W=3, R=3: 표준 quorum, 가장 균형

</details>

### Q8. Version vector — concurrent write 식별

3 replica (A, B, C) 의 version vector:
- Write X by A: [A:1, B:0, C:0]
- Write Y by B: [A:0, B:1, C:0]
- Write Z by A (after X): [A:2, B:0, C:0]

X, Y, Z 의 happens-before 관계?

<details><summary>답</summary>

**비교 규칙**: V₁ ≤ V₂ ⟺ 모든 i 에 대해 V₁[i] ≤ V₂[i]. *strict <* 이면 happens-before, *incomparable* 이면 concurrent.

- **X = [1,0,0]** vs **Y = [0,1,0]**: 
  - X[A]=1 > Y[A]=0, X[B]=0 < Y[B]=1 → **incomparable** → **concurrent**
- **X = [1,0,0]** vs **Z = [2,0,0]**: 
  - 모든 X ≤ Z, strict (Z[A]=2 > X[A]=1) → **X happens-before Z**
- **Y = [0,1,0]** vs **Z = [2,0,0]**:
  - Y[A]=0 < Z[A]=2, Y[B]=1 > Z[B]=0 → **incomparable** → **concurrent**

결론: X happens-before Z, Y 는 둘 모두와 concurrent. application 이 Y vs Z 의 merge 결정.

</details>

### Q9. 디버그 — Async replication lag spike

평소 100ms lag 인데 갑자기 *60초* 로 spike. 원인?

<details><summary>답</summary>

**가능 원인**:

1. **Long transaction** on leader — leader 가 *큰 SELECT* 또는 *큰 batch update* 처리 중. follower 는 transaction 완료 후에야 받음.
2. **Network bandwidth saturation** — backup 또는 다른 traffic 이 network 점유.
3. **Follower 의 slow disk** — follower 가 *디스크 fsync* 느려져서 apply 못 따라잡음.
4. **Follower 의 long query** — analytics query 가 follower 점유. WAL apply 가 *lock* 으로 막힘.
5. **DDL on large table** — `ALTER TABLE` 이 follower 에서 *full table rewrite* — 분 단위 lag.

**진단 순서**:
- `pg_stat_replication` (Postgres) / `SHOW SLAVE STATUS` (MySQL) 로 *current lag*
- Follower 의 *current query* — long-running 있나?
- Leader 의 *active transaction* — 큰 거 진행 중?
- Disk / network 메트릭

**예방**:
- Analytics 는 *별도 follower* 또는 *warehouse* 로
- Online DDL tool 사용
- Bandwidth 모니터링

</details>

### Q10. 면접 — Postgres 의 replica 가 갑자기 *느려짐*

특정 replica 의 read 가 *평소 1ms, 지금 1000ms*. 원인 진단 + 대응.

<details><summary>답</summary>

**진단 단계**:

1. **현재 query 확인** — `pg_stat_activity` 의 long-running. analytics 또는 *report* query?
2. **Lock 확인** — `pg_locks` + `pg_stat_activity` JOIN. *idle in transaction* 이 있나?
3. **Cache hit rate** — `pg_stat_statements`. cache miss 폭증?
4. **Disk I/O** — `iostat` 의 `%util` 와 `await`. burst 발생?
5. **Replication lag** — 같이 spike 면 *apply backpressure*

**대응**:
- *Long query kill* — `pg_cancel_backend(pid)` 또는 `pg_terminate_backend(pid)`
- *Connection pool 조정* — too many connection 으로 starvation?
- *Replica 분리* — 분석용 / 사용자용 따로
- *Tier the workload* — *primary* (user-facing) vs *secondary* (analytics)
- *autovacuum* 점검 — table bloat 으로 cache miss 증가?

**근본 대응**:
- *Multiple replica* — 워크로드 격리
- *PgBouncer + read-only replica pool*
- *Materialized view* 로 expensive query 분리

이게 6장 partitioning 과 11장 CDC + warehouse 의 *분리* 로 자연스럽게 이어짐.

</details>
