# Chapter 7: Transactions — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 7** (책 p.221~272, PDF p.243~294).
> 7장: 데이터의 *여러 변경을 묶어* 처리 — 동시성 + 부분 실패에 대한 *abstraction*. **ACID** 의 정확한 의미, **isolation level** 의 위계, 분산 환경의 도전.

## 들어가기 전에

- **선수 지식**: SQL transaction (BEGIN, COMMIT, ROLLBACK), 5장 replication
- **학습 목표**
  1. **ACID** — atomicity / consistency / isolation / durability 의 *정확한 의미*
  2. **Single-object** vs **multi-object** transaction
  3. **Isolation level** 의 위계 — Read Committed / Snapshot Isolation / Serializable
  4. **Race condition** 의 4 종 — dirty read, dirty write, lost update, write skew + phantom
  5. **Serializable** 의 3 구현 — actual serial, 2PL, SSI
- **예상 학습 시간**: 200~240분 (밀도 높음)

---

## 1. ACID — *정확히* 무엇

> "ACID" 는 마케팅 용어로 *흐려짐*. 실제 의미를 분리.

### 1.1 Atomicity

**all-or-nothing** — transaction 안 모든 write 가 *모두 성공* 또는 *모두 abort*.

- *부분 성공 없음* — 일부만 적용된 상태에서 멈추지 않음
- Abort 시 *모든 변경 rollback*
- ≠ "concurrent" (그건 isolation 의 역할)

### 1.2 Consistency

**application-defined invariant** 가 유지됨 (예: "계좌 잔액 합 = 0").

- 사실 *application 책임* — DB 는 invariant 검증 안 함
- 다른 ACID 글자와 *질적으로 다름*. 책의 저자는 "C is overloaded"

### 1.3 Isolation

**concurrent transactions 가 서로 영향 없는 듯** — *마치 직렬 실행* 같은 결과.

- 가장 도전적
- 여러 *isolation level* 존재 (§3)

### 1.4 Durability

**Commit 된 데이터는 영구** — crash 후에도 살아남음.

- 디스크 fsync + WAL
- *분산* 환경에선 replication 까지 (한 disk 만으론 부족)

---

## 2. Single-object vs Multi-object Transaction

### 2.1 Single-object

- 한 row / document 의 *atomic update*
- 대부분 NoSQL DB 가 *이것만* 보장
- 그래도 *부분 update* 어색 (예: JSON document 의 일부 field)

### 2.2 Multi-object

- 여러 row / table 의 *atomic 변경*
- 예: 송금 — `accounts.balance -= 100`, `accounts2.balance += 100`
- *둘 다 성공* 또는 *둘 다 실패* 필요
- BEGIN/COMMIT 의 영역

> **함정 1**: 일부 NoSQL 가 "ACID" 라고 광고하지만 실제는 *single-object atomicity* 만. multi-key transaction 은 7.4 절의 별도 메커니즘.

---

## 3. Weak Isolation Levels — Race Condition

### 3.1 Dirty Read

다른 transaction 의 *uncommitted* write 가 read 에 보임.

```
T1: UPDATE accounts SET balance = balance + 100 WHERE id=1; -- not committed yet
T2: SELECT balance FROM accounts WHERE id=1; -- sees the 100 update (DIRTY)
T1: ROLLBACK; -- T2 read 가 "phantom"
```

**해결** — Read Committed level 이 dirty read 방지. 거의 모든 DB 의 default.

### 3.2 Dirty Write

다른 transaction 의 *uncommitted* write 를 덮어쓰기.

→ Read Committed level 이 row-level lock 으로 방지.

### 3.3 Lost Update

```
T1: read balance=100, calculate new=110
T2: read balance=100, calculate new=120
T1: write 110
T2: write 120  -- T1 의 update LOST
```

같은 데이터를 *read-then-update* 하는 두 concurrent transaction.

**해결**:
1. **Atomic operation** — `UPDATE balance = balance + 10` (read 와 write 가 하나)
2. **Explicit lock** — `SELECT ... FOR UPDATE`
3. **Optimistic** — CAS (Compare-And-Swap): "version 이 X 이면 update"
4. **Auto-detect** (Snapshot Isolation) — DB 가 자동 감지 후 abort

### 3.4 Snapshot Isolation

**가장 흔히 채택되는 level**. PostgreSQL, MySQL InnoDB, Oracle, MS SQL, 대부분 NoSQL.

> Transaction 이 시작 시점의 *consistent snapshot* 을 봄. 같은 transaction 안에서 *snapshot 이 변하지 않음*.

**MVCC (Multi-Version Concurrency Control)** 로 구현:
- 각 row 가 *여러 version* 보유
- transaction 마다 *자기 version* 만 봄
- write 가 read 를 막지 않음 (vice versa)

![Figure 7-7 — MVCC 의 row version 관리. 책 p.241](/courses/ddia/figures/ch07/fig-7-7.png)

### 3.5 Write Skew + Phantom

가장 미묘한 race condition. 두 transaction 이 *서로 다른 row* 를 read+write — *각각은 valid* 지만 *결합 결과가 invariant 깨짐*.

**예제 — 의사 on-call**:
- Invariant: "*적어도 한 의사* 가 on-call"
- 현재 Alice, Bob 두 명 on-call
- T1: "Alice on-call 인지 확인 → on-call 이 둘 이상이면 off-duty" → off-duty
- T2: "Bob on-call 인지 확인 → on-call 이 둘 이상이면 off-duty" → off-duty
- *둘 다 off-duty 됨* — invariant 깨짐

![Figure 7-8 — Write skew 예제. 책 p.246](/courses/ddia/figures/ch07/fig-7-8.png)

**Phantom**: T1 의 SELECT WHERE 절 결과가 *나중에 추가된 row* (T2 의 insert) 로 *변함* — *materializing conflict* 가 안 됨.

**해결** — Serializable level.

---

## 4. Serializability — 3 구현

Concurrent transactions 의 결과가 *어떤 직렬 실행과 동등* 함을 보장.

### 4.1 Actual Serial Execution

> *한 thread* 에서 transaction 을 *한 번에 하나씩* 실행.

- 사실 가장 단순
- *CPU 빠름 + RAM 크면 OK* — VoltDB, Redis 가 이 방식
- 단, *모든 데이터가 메모리* 에 있어야
- *stored procedure* 로 작성 (network round-trip 회피)

장점: 단순, 정확. 단점: throughput 제한 (단일 thread).

### 4.2 Two-Phase Locking (2PL)

> Read 도 shared lock, write 는 exclusive lock. Transaction 끝까지 *hold*.

- 30년간 *기본 serializable 구현*
- **MySQL Serializable**, **DB2** 가 이 방식
- 단점:
  - *Deadlock* 발생 → DB 가 detection 후 abort
  - Throughput 매우 낮음 — lock contention
  - Latency 불안정 — tail spike 큼

### 4.3 Serializable Snapshot Isolation (SSI)

**현대 최고**. PostgreSQL 9.1+, FoundationDB.

> Snapshot isolation 기본. 그러나 *serializability 깨지는 패턴* (예: write skew) 을 *runtime 감지 후 abort*.

- *Optimistic concurrency control* (OCC)
- Lock 대신 *concurrent transactions 의 read/write 추적*
- Commit 시점에 *conflict 있으면 abort*

장점: read-heavy 에 좋음 (lock 없음), throughput 높음.
단점: write contention 높으면 *retry 비율 ↑* (abort 빈번).

---

## 5. 분산 Transaction — Two-Phase Commit (2PC)

여러 partition / DB 에 걸친 transaction.

### 5.1 2PC 동작

![Figure 7-10 — 2PC 의 phases. 책 p.286](/courses/ddia/figures/ch07/fig-7-10.png)

1. **Phase 1 — Prepare**: coordinator 가 모든 participant 에 "준비됐냐?" 물음. 각자 *commit 가능* 인지 확인 후 *yes* / *no* 응답.
2. **Phase 2 — Commit**: 모든 *yes* 면 coordinator 가 *commit* 명령. 하나라도 *no* 면 *abort*.

### 5.2 2PC 의 도전

- **Blocking** — coordinator crash 시 participant 가 *영원히 wait* (prepare 후 결정 못함)
- **Heuristic decision** — DBA 가 *수동으로 abort/commit* 결정해야 (위험)
- **Performance** — 모든 participant 의 *2x RTT*. 일반 transaction 대비 *10배 느림* 흔함
- **Coordinator 자체가 SPOF**

### 5.3 XA — 표준 2PC interface

- Java 의 JTA, application server (WebLogic) 의 default
- 다른 vendor DB + message queue 의 *cross-system transaction*
- 실용에선 *operations 부담 큼*. 산업에서 *지양*

> **함정 2**: "distributed transaction 으로 풀자" 는 *유혹*. 실제는 *eventual consistency + 명시적 compensation* (Saga 패턴) 이 더 robust. 7.4 절 + 9장 의 깊은 논의.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "ACID DB" 면 모든 race condition 안전 | isolation level 따라 다름. default 가 Read Committed (가장 약함) |
| 2 | Lost update 가 *자동 방지* | weak isolation 에선 안 됨. atomic op 또는 lock 필요 |
| 3 | Snapshot isolation = serializable | Write skew 같은 anomaly 존재 |
| 4 | Serializable 이 *느림* | 옛 (2PL) 만. SSI 가 read-heavy 에 빠름 |
| 5 | 2PC 가 *해결책* | blocking, perf, SPOF 의 운영 부담. Saga 가 종종 더 나음 |
| 6 | NoSQL = no transaction | MongoDB 4.0+ 의 multi-doc transaction. Cosmos DB, FoundationDB 등 |
| 7 | Optimistic 이 *항상 빠름* | write contention 높으면 abort 폭주 → 실은 더 느림 |
| 8 | Atomicity = concurrency | 별개. atomicity 는 *한 transaction 안*. concurrency 는 *isolation*. |
| 9 | Consistency 가 DB 책임 | 사실 *application*. DB 는 constraint 만 |
| 10 | Single-leader 면 distributed transaction 불필요 | partition 들이 여러 leader 면 여전히 필요 |

---

## 자가점검

1. ACID 의 4 글자 각각 정확한 의미.
2. *Single-object* 와 *multi-object* transaction 의 차이.
3. *Dirty read*, *dirty write*, *lost update*, *write skew* 각 정의 + 해결.
4. *Snapshot isolation* 가 *어떤 anomaly* 를 막고 *어떤 건* 못 막나.
5. *Phantom* 의 정의 + 해결.
6. *MVCC* 의 핵심 아이디어.
7. *Serializability* 의 3 구현 + 각 trade-off.
8. *2PC* 의 두 phase + *blocking* 위험.

### 해답 (간략)

1. **A** all-or-nothing. **C** invariant (app 책임). **I** concurrent 가 직렬 동등. **D** commit 영구.
2. Single: 한 row 의 atomic. Multi: 여러 row / table 의 atomic. BEGIN/COMMIT 필요.
3. Dirty read: uncommitted 보임 → Read Committed. Dirty write: uncommitted 덮음 → row lock. Lost update: read-update concurrent → atomic op 또는 lock. Write skew: invariant cross-row → Serializable.
4. 막음: dirty read, dirty write, lost update (DB 가 detect). 못 막음: write skew, phantom.
5. SELECT WHERE 의 결과가 *나중 insert* 로 바뀜. Serializable 또는 *예측 lock* (예: range lock) 으로.
6. Row 의 *여러 version* 동시 보유. transaction 마다 *snapshot 시점 version* 만 봄. read 가 write 막지 않음.
7. (1) Actual serial: 단일 thread, 단순, 메모리 제한. (2) 2PL: lock-based, deadlock, 느림. (3) SSI: OCC + abort on conflict, read-heavy 에 빠름.
8. Phase 1 prepare (모든 participant yes/no), Phase 2 commit (all yes 면 commit, else abort). Coordinator crash 시 participant 가 prepare 상태로 stuck.

---

## 다음 학습으로

- **8장 (Distributed Trouble)** — 2PC 의 *근본 어려움* — clock, GC, partition
- **9장 (Consistency)** — serializable + linearizable 의 결합. consensus 가 분산 transaction 의 *진짜 답*
- **11장 (Stream)** — Saga 패턴, event sourcing 으로 transaction 회피
