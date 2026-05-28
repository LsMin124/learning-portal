# Chapter 7: Transactions — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 7** (책 p.221~272, PDF p.243~294).
> 7장: 데이터의 *여러 변경을 묶어* 처리 — 동시성 + 부분 실패에 대한 *abstraction*. **ACID** 의 정확한 의미, **isolation level** 의 위계, 분산 환경의 도전.

이 장의 *지적 무게중심*:
1. **ACID 의 *진짜 의미*** — 마케팅 vs 정확한 정의
2. **Isolation level 위계** — Read Committed → Snapshot → Serializable
3. **5 가지 anomaly** — dirty read/write, read skew, lost update, write skew, phantom
4. **Serializability 의 3 구현** — actual serial, 2PL, SSI
5. **분산 transaction** — 2PC 의 *근본 한계*, Saga 의 대안

---

## 들어가기 전에

- **선수 지식**: SQL transaction (BEGIN, COMMIT, ROLLBACK), 5장 replication
- **학습 목표**
  1. **ACID** — atomicity / consistency / isolation / durability 의 *정확한 의미*
  2. **Single-object** vs **multi-object** transaction
  3. **Isolation level** 의 위계 — Read Committed / Snapshot Isolation / Serializable
  4. **Race condition** 의 5 종 — dirty read/write, read skew, lost update, write skew + phantom
  5. **Serializable** 의 3 구현 — actual serial, 2PL, SSI
- **예상 학습 시간**: 200~240분 (밀도 높음)

---

## §1 ACID — *정확히* 무엇

> "ACID" 는 마케팅 용어로 *흐려짐*. 실제 의미를 분리.

### §1.1 Atomicity

**all-or-nothing** — transaction 안 모든 write 가 *모두 성공* 또는 *모두 abort*.

- *부분 성공 없음* — 일부만 적용된 상태에서 멈추지 않음
- Abort 시 *모든 변경 rollback*
- ≠ "concurrent" (그건 isolation 의 역할)

**구현**:
- *Undo log* — 변경 전 값을 기록, abort 시 복구
- *Write-ahead log* — commit 시점 의 *변경 모음 commit*

### §1.2 Consistency

**application-defined invariant** 가 유지됨 (예: "계좌 잔액 합 = 0").

- 사실 *application 책임* — DB 는 invariant 검증 안 함
- 다른 ACID 글자와 *질적으로 다름*. 책의 저자는 "C is overloaded"

### §1.3 Isolation

**concurrent transactions 가 서로 영향 없는 듯** — *마치 직렬 실행* 같은 결과.

- 가장 도전적
- 여러 *isolation level* 존재 (§3)

### §1.4 Durability

**Commit 된 데이터는 영구** — crash 후에도 살아남음.

- 디스크 fsync + WAL
- *분산* 환경에선 replication 까지 (한 disk 만으론 부족)

**Modern durability**:
- *Single disk* — 부족 (drive 실패율 ~ 1% annual)
- *RAID* — 약간 도움 (silent corruption, fire 위험)
- *Replication + cross-region* — 권장

---

## §2 Single-object vs Multi-object Transaction

### §2.1 Single-object

- 한 row / document 의 *atomic update*
- 대부분 NoSQL DB 가 *이것만* 보장

**Atomic operations**:
- `UPDATE balance = balance + 100`
- `INSERT ON CONFLICT UPDATE`
- `INCR counter` (Redis)

### §2.2 Multi-object

- 여러 row / table 의 *atomic 변경*
- 예: 송금 — `accounts.balance -= 100`, `accounts2.balance += 100`
- *둘 다 성공* 또는 *둘 다 실패* 필요

> **함정 1**: 일부 NoSQL 가 "ACID" 라고 광고하지만 실제는 *single-object atomicity* 만.

**Modern NoSQL 의 transaction support**:
- *MongoDB 4.0+* — multi-document transaction
- *DynamoDB* — TransactWriteItems (25 item 까지)
- *Cosmos DB* — stored procedure
- *FoundationDB* — full ACID

---

## §3 Weak Isolation Levels — Race Condition

### §3.1 Dirty Read

다른 transaction 의 *uncommitted* write 가 read 에 보임.

```
T1: UPDATE accounts SET balance = balance + 100 WHERE id=1; -- not committed yet
T2: SELECT balance FROM accounts WHERE id=1; -- sees the 100 update (DIRTY)
T1: ROLLBACK; -- T2 read 가 "phantom"
```

**해결** — Read Committed level. 거의 모든 DB 의 default.

### §3.2 Dirty Write

다른 transaction 의 *uncommitted* write 를 덮어쓰기.

→ Read Committed level 이 row-level lock 으로 방지.

### §3.3 Read Skew (= Non-Repeatable Read)

같은 transaction 안에서 *같은 row 를 두 번 read* — *다른 값* 봄.

```
T1: BEGIN
T1: SELECT balance FROM accounts WHERE id=1; -- $500
T2: UPDATE accounts SET balance=600 WHERE id=1; COMMIT;
T1: SELECT balance FROM accounts WHERE id=1; -- $600 (다름!)
```

**문제 시나리오**:
- Backup 도중 inconsistent snapshot
- Analytics query 가 *transaction 중간 state* 봄

**해결** — Snapshot Isolation.

### §3.4 Lost Update

```
T1: read balance=100, calculate new=110
T2: read balance=100, calculate new=120
T1: write 110
T2: write 120  -- T1 의 update LOST
```

같은 데이터를 *read-then-update* 하는 두 concurrent transaction.

**해결**:
1. **Atomic operation** — `UPDATE balance = balance + 10`
2. **Explicit lock** — `SELECT ... FOR UPDATE`
3. **Optimistic** — CAS
4. **Auto-detect** (Snapshot Isolation) — DB 가 abort

### §3.5 Snapshot Isolation

**가장 흔히 채택되는 level**. PostgreSQL, MySQL InnoDB, Oracle, MS SQL.

> Transaction 이 시작 시점의 *consistent snapshot* 을 봄.

**MVCC (Multi-Version Concurrency Control)**:
- 각 row 가 *여러 version*
- transaction 마다 *자기 version* 만 봄
- write 가 read 를 막지 않음 (vice versa)

![Figure 7-7 — MVCC 의 row version 관리. 책 p.241](/courses/ddia/figures/ch07/fig-7-7.png)

**MVCC garbage collection**:
- 옛 version 도 *어떤 transaction 이 보고 있을 수 있음*
- *XID* 추적 → 모든 transaction 끝나면 GC
- *Long-running transaction* 이 GC 막음 → *bloat*
- PostgreSQL `VACUUM`

### §3.6 Write Skew + Phantom

가장 미묘한 race condition.

**예제 — 의사 on-call**:
- Invariant: "*적어도 한 의사* 가 on-call"
- 현재 Alice, Bob 두 명 on-call
- T1: "Alice on-call? on-call 둘 이상이면 off-duty" → off-duty
- T2: "Bob on-call? on-call 둘 이상이면 off-duty" → off-duty
- *둘 다 off-duty* — invariant 깨짐

![Figure 7-8 — Write skew 예제. 책 p.246](/courses/ddia/figures/ch07/fig-7-8.png)

**Phantom**: T1 의 SELECT WHERE 결과가 *나중 insert* 로 변함.

**Write skew 의 산업 예**:
- Meeting room 동시 예약
- Username 동시 등록
- Game 의 한정 아이템 동시 구매

**해결** — Serializable.

### §3.7 Isolation level 위계 + ANSI SQL

| Level | Dirty Read | Dirty Write | Lost Update | Read Skew | Phantom | Write Skew |
|--|--|--|--|--|--|--|
| Read Uncommitted | 가능 | 막음 | 가능 | 가능 | 가능 | 가능 |
| Read Committed | 막음 | 막음 | 가능 | 가능 | 가능 | 가능 |
| Repeatable Read (SI) | 막음 | 막음 | 막음 (일부) | 막음 | 막음 (일부) | 가능 |
| Serializable | 막음 | 막음 | 막음 | 막음 | 막음 | 막음 |

**ANSI SQL 의 함정**:
- Repeatable Read 의 정의가 *vague*
- DB 마다 다른 구현:
  - Oracle "Repeatable Read" = Serializable 수준
  - PostgreSQL "Repeatable Read" = Snapshot Isolation
  - MySQL InnoDB "Repeatable Read" = SI + phantom 막음 (gap lock)

---

## §4 Serializability — 3 구현

### §4.1 Actual Serial Execution

> *한 thread* 에서 transaction 을 *한 번에 하나씩*.

- *CPU 빠름 + RAM 크면 OK* — VoltDB, Redis
- *모든 데이터가 메모리*
- *stored procedure* 로 작성

**VoltDB 산업 응용**:
- Telecom billing — Verizon
- Real-time finance
- 수만 TPS per thread
- *partition* 별 single thread

### §4.2 Two-Phase Locking (2PL)

> Read = shared lock, write = exclusive lock. Transaction 끝까지 hold.

- 30년간 *기본 serializable 구현*
- **MySQL Serializable**, **DB2**
- 단점: deadlock, lock contention, latency spike

**Predicate lock**:
- Phantom 막기 위해 *조건 자체* lock
- 구현 어려움 → *gap lock* 으로 근사

### §4.3 Serializable Snapshot Isolation (SSI)

**현대 최고**. PostgreSQL 9.1+, FoundationDB.

- Snapshot isolation 기본
- *serializability 깨지는 패턴* runtime 감지 후 abort
- *OCC* (Optimistic Concurrency Control)

**Detection**:
- Read 가 옛 MVCC version 인 경우 추적
- Stale read + 그에 기반한 write = potential write skew
- Commit 시 *abort + retry*

장점: read-heavy 에 좋음. 단점: write contention 시 abort 폭주.

---

## §5 분산 Transaction — Two-Phase Commit (2PC)

### §5.1 2PC 동작

![Figure 7-10 — 2PC. 책 p.286](/courses/ddia/figures/ch07/fig-7-10.png)

1. **Phase 1 — Prepare**: coordinator 가 모든 participant 에 "준비?" 물음. yes/no.
2. **Phase 2 — Commit**: 모든 yes 면 commit, 하나라도 no 면 abort.

### §5.2 2PC 의 도전

- **Blocking** — coordinator crash 시 participant *영원히 wait*
- **Heuristic decision** — DBA 의 수동 결정 (위험)
- **Performance** — 2x RTT, 10배 느림 흔함
- **Coordinator SPOF**

### §5.3 XA

- Java JTA, application server default
- Cross-system transaction
- *Operations 부담* — 산업 지양

### §5.4 Saga Pattern

> *큰 transaction* 을 *작은 local transaction sequence* 로 분해. 실패 시 *compensating transaction*.

**예 — 여행 예약**:
1. Reserve flight
2. Reserve hotel
3. Reserve car (실패 시)
   - Cancel hotel
   - Cancel flight

**두 스타일**:

**Orchestration**:
- 중앙 orchestrator (state machine)
- AWS Step Functions, Temporal, Camunda

**Choreography**:
- Event-driven, 분산
- Kafka + microservices

### §5.5 TCC (Try-Confirm-Cancel)

- *Try* — 자원 예약
- *Confirm* — 실제 commit
- *Cancel* — release

### §5.6 Modern distributed transaction

**Spanner**:
- TrueTime + 2PC + Paxos
- Globally distributed + serializable

**CockroachDB**:
- Spanner-inspired
- Raft per range
- Serializable default

**FoundationDB**:
- Layered architecture
- Deterministic simulation testing

> **함정 2**: "distributed transaction 으로 풀자" 는 *유혹*. 실제는 *eventual consistency + Saga* 가 더 robust.

---

## §6 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "ACID DB" 면 모든 race 안전 | isolation level 따라. default = Read Committed |
| 2 | Lost update 자동 방지 | weak isolation 에선 안 됨 |
| 3 | SI = serializable | Write skew 존재 |
| 4 | Serializable 이 *느림* | SSI 가 read-heavy 에 빠름 |
| 5 | 2PC 가 해결책 | blocking, perf, SPOF. Saga 가 종종 더 |
| 6 | NoSQL = no transaction | MongoDB 4.0+, FoundationDB |
| 7 | Optimistic 이 항상 빠름 | write contention 시 abort 폭주 |
| 8 | Atomicity = concurrency | 별개 |
| 9 | Consistency 가 DB 책임 | application |
| 10 | Single-leader = distributed transaction 불필요 | partition multi-leader 시 필요 |
| 11 | ANSI SQL isolation 이 표준 | DB 마다 같은 이름 다른 구현 |
| 12 | Saga = 모든 답 | Compensating 가능한 경우만 |

---

## §7 자가점검

1. ACID 각 정확한 의미?
2. *Single-object* 와 *multi-object* 차이?
3. *5 가지 anomaly* 각 정의?
4. *SI* 가 막는 것 + 못 막는 것?
5. *Write skew* 의 산업 예 + 해결?
6. *MVCC* 의 핵심 + GC 문제?
7. *Serializability* 의 3 구현?
8. *2PC* 의 두 phase + blocking?
9. *Saga* 의 orchestration vs choreography?
10. *ANSI SQL isolation level* 의 함정?

<details><summary>해답 (간략)</summary>

1. A all-or-nothing. C invariant (app). I concurrent = 직렬 동등. D commit 영구.
2. Single: 한 row atomic. Multi: 여러 row atomic.
3. Dirty read: uncommitted 보임. Dirty write: uncommitted 덮음. Read skew: 같은 row 두 번 다른 값. Lost update: concurrent read-update. Write skew: cross-row invariant. Phantom: SELECT WHERE 의 *새 row* 영향.
4. 막음: dirty read/write, read skew, lost update. 못 막음: write skew, phantom.
5. Meeting room, on-call doctor, username 동시. → Serializable.
6. 여러 version 동시. snapshot version 만 봄. GC: 옛 version 도 누군가 볼 수 있음. Long-running 이 막음.
7. (1) Actual serial: 단일 thread. (2) 2PL: lock-based. (3) SSI: OCC + abort.
8. Phase 1 prepare, Phase 2 commit. Coordinator crash 시 prepare stuck.
9. Orchestration: 중앙 state machine. Choreography: event-driven 분산.
10. Repeatable Read 의 정의가 DB 마다 다름 (Oracle = Serializable 급, MySQL = SI + gap lock).

</details>

---

## §8 다음 학습으로

- **8장** — 2PC 의 *근본 어려움* — clock, GC, partition
- **9장** — serializable + linearizable, consensus
- **11장** — Saga 패턴, event sourcing

---

## §9 한 줄 요약

> **Transaction = abstraction for *atomicity + isolation + concurrent safety*. ACID 의 정확한 의미. 5 가지 anomaly. Serializability 의 3 구현 (actual serial, 2PL, SSI). 분산 transaction = 2PC 의 어려움 → Saga 의 실용적 대안.**
