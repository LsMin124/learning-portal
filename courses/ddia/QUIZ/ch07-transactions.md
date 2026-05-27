# Ch 7 Transactions — 퀴즈

> 10 문항.

### Q1. ACID 의 *C* 가 왜 *질적으로 다른가*

<details><summary>답</summary>

**A, I, D 는 DB 의 책임**:
- Atomicity: WAL + rollback
- Isolation: lock / MVCC
- Durability: fsync + replication

**C (Consistency) 는 *application 책임***:
- DB 는 *constraint* (CHECK, FOREIGN KEY, UNIQUE) 만 강제
- 진짜 *business invariant* ("계좌 잔액 합 = 0") 는 application 코드가 보장
- DB 는 *transaction 안에서* AID 만 제공

→ 책의 저자는 "C 는 ACID 의 다른 글자에 *얹혀가는*" 표현 사용. 마케팅 용어.

</details>

### Q2. Isolation level 위계

ANSI SQL 의 4 level + 실제 DB 가 무엇 사용.

<details><summary>답</summary>

| Level | Dirty read | Dirty write | Lost update | Phantom | Write skew |
|--|--|--|--|--|--|
| Read Uncommitted | ❌ | ❌ | ❌ | ❌ | ❌ |
| Read Committed | ✓ | ✓ | ❌ | ❌ | ❌ |
| Repeatable Read / Snapshot Isolation | ✓ | ✓ | ✓ | ⚠ | ❌ |
| Serializable | ✓ | ✓ | ✓ | ✓ | ✓ |

**실제 DB**:
- PostgreSQL default: **Read Committed** (snapshot isolation 명시 옵션)
- MySQL InnoDB default: **Repeatable Read** (실제는 *snapshot isolation 가까움*)
- Oracle: **Read Committed**

→ "ACID DB" 라도 *default 가 약함*. 명시적으로 `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE` 필요한 경우 多.

</details>

### Q3. Lost update 의 4 가지 해결

같은 row 의 read-then-update concurrent. 각각의 코드 예.

<details><summary>답</summary>

```sql
-- (1) Atomic operation — read+write 가 한 statement
UPDATE accounts SET balance = balance + 100 WHERE id = 1;

-- (2) Explicit lock
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- ... compute new_balance ...
UPDATE accounts SET balance = :new_balance WHERE id = 1;
COMMIT;

-- (3) Optimistic (CAS / version)
SELECT balance, version FROM accounts WHERE id = 1;
-- ... compute new_balance ...
UPDATE accounts SET balance = :new, version = version + 1
WHERE id = 1 AND version = :old_version;
-- affected rows 0 이면 retry

-- (4) Snapshot Isolation 의 auto-detect
BEGIN ISOLATION LEVEL REPEATABLE READ;
-- DB 가 conflict 감지 시 자동 abort, application 이 retry
```

**선택**:
- 단순 산술: atomic op (가장 빠름)
- 복잡한 read-modify-write: optimistic + retry loop
- 정확한 보장 필요: explicit lock

</details>

### Q4. Write skew — 의사 on-call 예제

invariant 가 *cross-row* — snapshot isolation 으로 안 막힘. 해결.

<details><summary>답</summary>

**문제 재현**:
```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;

-- T1 (Alice): "다른 의사가 on-call 인가?" 확인 후 off-duty
SELECT COUNT(*) FROM doctors WHERE on_call = true AND shift = 1234;
-- 결과: 2 (Alice, Bob 둘 다 on-call)
UPDATE doctors SET on_call = false WHERE id = 'Alice';
COMMIT;

-- T2 (Bob): 같은 시점에 동일하게 진행
SELECT COUNT(*) ... -- 여전히 2 (snapshot)
UPDATE doctors SET on_call = false WHERE id = 'Bob';
COMMIT;

-- 결과: 둘 다 off-duty. invariant 깨짐.
```

**해결**:

1. **Serializable level** — SSI 가 conflict 감지 후 한 transaction abort
```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- 동일 코드. T2 가 commit 시 abort, application 이 retry
```

2. **Explicit lock** — `SELECT ... FOR UPDATE` 로 *예측한 conflict* lock
```sql
SELECT * FROM doctors WHERE on_call = true AND shift = 1234 FOR UPDATE;
-- 모든 on-call 의사를 lock. T2 가 wait.
```

3. **Materialize the conflict** — phantom 을 막기 위해 *실제 row* 생성
```sql
CREATE TABLE doctor_locks (shift INT PRIMARY KEY);
-- 각 shift 마다 row 추가
UPDATE doctor_locks SET shift = shift WHERE shift = 1234;  -- exclusive lock
-- 이후 logic
```

산업: PostgreSQL SSI 또는 explicit `FOR UPDATE` 가 표준.

</details>

### Q5. MVCC 의 핵심 — Postgres 의 구현

`SELECT * FROM users WHERE id = 1` 의 row version 처리.

<details><summary>답</summary>

**Postgres 의 row** 가 *4 가지 hidden column* 보유:
- `xmin`: 이 row 를 *생성* 한 transaction ID
- `xmax`: 이 row 를 *삭제 또는 update* 한 transaction ID (없으면 0)
- `cmin`, `cmax`: 같은 transaction 안의 *명령 순서*

**Update 동작**:
- Row 의 *update* 가 아니라 *새 row insert + 옛 row 의 xmax 설정*
- 같은 user 의 *여러 version* 이 디스크에 공존

**Snapshot read**:
- Transaction 시작 시 *현재 active transaction set* 기록
- Row 가 *내 transaction 시점에 보였어야 함*:
  - `xmin <= my_txid` (이미 commit)
  - `xmax == 0` 또는 `xmax > my_txid` (아직 삭제 안 됨)

**VACUUM**:
- *모든 active transaction* 이 더 이상 안 보는 *옛 version* 을 GC
- Postgres 의 *autovacuum* 이 자동 진행

→ 이게 PostgreSQL 의 *읽기-write 비차단* 의 근간. 단 *vacuum 부담* (bloat) 이 운영 이슈.

</details>

### Q6. SSI vs 2PL — 워크로드별

각 isolation 구현이 *어떤 워크로드* 에 우월한가.

<details><summary>답</summary>

**2PL (Two-Phase Locking)**:
- *Write 가 많고 conflict 가 빈번*
- Reader 가 적은 *transactional* OLTP
- Tail latency 가 *중요하지 않음*
- 예: 옛 mainframe banking, MySQL Serializable

**SSI (Serializable Snapshot Isolation)**:
- *Read-heavy* (analytics-mix)
- Write *작은* OLTP
- *Concurrency 높음* (수천 simultaneous transaction)
- 예: PostgreSQL 9.1+, FoundationDB

**Actual Serial**:
- *모든 데이터 메모리* 가능
- Stored procedure 작성 가능
- 매우 단순 워크로드
- 예: VoltDB, Redis

**산업 트렌드** — SSI 가 압도적. 단 *write contention 높으면* abort 폭주로 throughput 떨어짐 — 그땐 2PL 또는 *application split*.

</details>

### Q7. 2PC 의 *blocking* 위험 시나리오

coordinator crash 시 *어떻게 stuck* 인가?

<details><summary>답</summary>

**Stuck 시나리오**:
1. Coordinator C 가 모든 participant 에 *prepare* 명령
2. P1, P2, P3 모두 *yes* response
3. P1, P2 가 *yes* 응답 후 — *commit 까지 wait*
4. **Coordinator C crash** — *commit/abort 결정 못 함*
5. P1, P2 가 *prepare 상태로 영원히 wait*:
   - Local lock 보유 중 → 다른 transaction block
   - Rollback 불가 (혹시 다른 participant 가 commit 했을 수도)
   - 자기 마음대로 commit 도 불가 (다른 게 abort 했을 수도)
6. C 복구 전까지 *모든 관련 transaction* freeze

**대응**:
- **Heuristic decision** — DBA 가 *수동* commit/abort. 잘못하면 *atomicity 깨짐* (P1 commit, P2 abort)
- **Coordinator HA** — coordinator 자체를 *replicated* (Raft, 9장) → SPOF 제거
- **Timeout-based abort** — 일정 시간 후 자동 abort. 그러나 *false abort* 위험

**근본 해결** — *Distributed transaction 회피*. Saga pattern, event sourcing.

</details>

### Q8. Saga 패턴 — 2PC 의 대안

2PC 대신 *각 step 의 compensation*. 송금 예제로 설명.

<details><summary>답</summary>

**전통 2PC**:
```
BEGIN GLOBAL TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = A;  -- bank A
  UPDATE accounts SET balance = balance + 100 WHERE id = B;  -- bank B
COMMIT;  -- 2PC
```

**Saga**:
```
Step 1: Debit A (forward)
  Compensation: Credit A (rollback)

Step 2: Credit B (forward)
  Compensation: Debit B (rollback)

Orchestrator:
  Execute Step 1 → success → Execute Step 2 → success → DONE
  Execute Step 1 → success → Execute Step 2 → FAIL → Execute Compensation 1
```

**구현 방식**:
- **Orchestration**: 중앙 coordinator 가 sequence 제어 (e.g., AWS Step Functions, Temporal)
- **Choreography**: 각 service 가 *event* 로 통신, *다음 step* 을 listener 가 trigger

**Saga 의 trade-off**:
- ✓ 비차단, scale 우수
- ✓ 각 service 의 *local transaction* 만
- ❌ *isolation 없음* — 진행 중에 다른 user 가 *중간 상태* 봄
- ❌ Compensation 의 *복잡도* — 정확한 inverse 작성 어려움

**산업 적용**: 금융 (송금), e-commerce (주문→배송), 여행 예약. 11장의 *event-driven* + saga 가 대세.

</details>

### Q9. 디버그 — Deadlock

PostgreSQL 의 ERROR: deadlock detected. 어떻게 진단?

<details><summary>답</summary>

**진단 단계**:

1. **PG_STAT_ACTIVITY 로 lock 분석**:
```sql
SELECT pid, query, state, wait_event_type, wait_event
FROM pg_stat_activity
WHERE state != 'idle';
```

2. **pg_locks 로 어느 transaction 이 무엇을 hold**:
```sql
SELECT locktype, relation::regclass, mode, pid, granted
FROM pg_locks
WHERE NOT granted;
```

3. **Deadlock log 확인** — PostgreSQL 이 deadlock_timeout (default 1s) 후 detection → log 에 *순환* 출력

**근본 원인 가능성**:
1. **Lock order 불일치** — T1 이 (A, B) 순, T2 가 (B, A) 순으로 lock. → application 에서 *항상 같은 순서* 로 lock.
2. **Long transaction** — 한 transaction 이 너무 오래 hold. → 짧게 분해.
3. **Missing index** — full table scan 이 *table-level lock* 잡음. → index 추가.
4. **Foreign key cascade** — 부모 row update 가 자식 row 까지 lock. → cascade 옵션 점검.

**대응**:
- **Retry loop** — application 이 *deadlock error* 받으면 *exponential backoff* 후 retry
- **Lock ordering 통일**
- **Application-level coordination** — Redis 의 *advisory lock*

</details>

### Q10. 면접 — "ACID 가 *왜* 필요 없을까?"

"우리 시스템은 ACID 없이 eventual consistency 로 됩니다" 라고 주장. 어떻게 평가?

<details><summary>답</summary>

**상황 분석 — ACID 가 *진짜 필요 없는*** 경우:

1. **Idempotent + commutative 연산** — counter, like 누르기. 순서 무관, 중복 OK.
2. **Single-user** 데이터 — 한 사용자가 자기 데이터만 수정. concurrency 충돌 없음.
3. **Append-only** — log, event stream. update 없음.
4. **Compensating action** 가능 — 잘못된 결과를 *나중에 보정* (예: 금융 시스템의 reconciliation).

**ACID 가 *반드시* 필요한** 경우:

1. **금융 거래** — 잔액 정확성. 1 cent 라도 틀리면 안 됨.
2. **재고 관리** — overselling 방지.
3. **예약 시스템** — 좌석 중복 예약 방지 (write skew 가능).
4. **개인정보** — 변경 추적, audit.

**프레임 — "ACID 가 필요 없다" 는 답변에 되묻기**:
- "어떤 *invariant* 가 깨질 수 있어요? 그게 *얼마나 자주*?"
- "Compensation 의 *cost* 가 얼마나? user-facing 이면 신뢰 손상."
- "*Concurrent users* 수가 어떤가요? Single-user 면 OK."

**실용 패턴 — Mixed approach**:
- 핵심 데이터 (금융, 재고): ACID transaction (PostgreSQL)
- 부수적 (analytics, log): eventual + KV store
- 메시지: Kafka 의 *exactly-once*

면접관이 보는 건 — *trade-off 이해 + 측정 데이터 기반 결정*. 절대주의는 양쪽 다 위험.

</details>
