# Ch 7 Transactions — 치트시트

## TL;DR

- **ACID**: A all-or-nothing / I concurrent ≈ serial / D commit 영구. **C 는 app 책임**
- **Isolation level**: Read Committed (대부분 default) → Snapshot Isolation → Serializable
- 4 race condition: dirty read/write, lost update, write skew + phantom
- Snapshot Isolation 의 *MVCC* — read/write 비차단. 단 write skew 못 막음
- Serializable 3 구현: actual serial / 2PL / **SSI** (Postgres 9.1+ 표준)
- 분산 transaction: **2PC** 의 blocking 위험 → **Saga + compensation** 이 산업 선호

---

## Quick Reference

### 표 1. ACID 정의

| Letter | 의미 | 누구 책임 |
|--|--|--|
| A Atomicity | all-or-nothing | DB |
| C Consistency | invariant 유지 | **App** |
| I Isolation | concurrent ≈ serial | DB |
| D Durability | commit 영구 | DB |

### 표 2. Isolation level 매트릭스

| Level | dirty read | dirty write | lost update | phantom | write skew |
|--|--|--|--|--|--|
| Read Uncommitted | ❌ | ❌ | ❌ | ❌ | ❌ |
| Read Committed | ✓ | ✓ | ❌ | ❌ | ❌ |
| Snapshot / Repeatable Read | ✓ | ✓ | ✓ | ⚠ | ❌ |
| Serializable | ✓ | ✓ | ✓ | ✓ | ✓ |

### 표 3. 4 race condition

| Anomaly | 해결 |
|--|--|
| Dirty read | Read Committed |
| Dirty write | row-level lock |
| Lost update | atomic op / explicit lock / OCC / SI auto-detect |
| Write skew | Serializable (SSI) / `SELECT FOR UPDATE` / materialize conflict |

### 표 4. Serializable 3 구현

| | Actual serial | 2PL | SSI |
|--|--|--|--|
| 동시성 | 단일 thread | lock | optimistic |
| 적합 | 메모리 fit, stored procedure | write-heavy, conflict 빈번 | read-heavy, OLTP |
| Throughput | 한정 | 낮음 (lock contention) | 높음 |
| Tail latency | 일정 | spike (lock wait) | 일정 (단 abort retry) |
| 예시 | VoltDB, Redis | DB2, MySQL Serializable | Postgres 9.1+, FoundationDB |

### 표 5. MVCC (Postgres)

```
Row 의 hidden column:
  xmin: 생성한 txid
  xmax: 삭제/update 한 txid (0 = alive)
  cmin, cmax: command sequence

Read 가시성:
  visible iff xmin <= my_txid AND (xmax == 0 OR xmax > my_txid)

Update = insert new row + set xmax of old
VACUUM: 모든 active txn 의 시야 밖 옛 row GC
```

### 표 6. 2PC

```
Phase 1 PREPARE:
  Coordinator → all participants: "ready?"
  Participants: persist intent + reply yes/no

Phase 2 COMMIT/ABORT:
  All yes → coordinator decides COMMIT, sends to all
  Any no → coordinator decides ABORT
  Participants execute decision, reply ACK
```

**Blocking**: coordinator crash 후 phase 2 이전 → participant stuck (lock 보유, abort/commit 결정 못함).

### 표 7. Saga vs 2PC

| | 2PC | Saga |
|--|--|--|
| Atomicity | global | per-step (compensation) |
| Isolation | global | 없음 (중간 상태 보임) |
| Blocking | 위험 | 없음 |
| 복잡도 | DB 가 처리 | application 의 compensation 작성 |
| 적합 | tightly-coupled DB | microservice, event-driven |

---

## Mind Map

```
7장 Transactions
├─ 1. ACID 의 정확한 의미
│   └─ C 는 app 책임
├─ 2. Single vs Multi object
├─ 3. Weak isolation
│   ├─ Dirty read/write
│   ├─ Lost update
│   ├─ Snapshot Isolation (MVCC)
│   └─ Write skew + phantom
├─ 4. Serializability 3 구현
│   ├─ Actual serial
│   ├─ 2PL
│   └─ SSI (Postgres 9.1+)
└─ 5. 분산 transaction
    ├─ 2PC + blocking
    ├─ XA standard
    └─ Saga + compensation
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | ACID 의 C 만 app 책임 |
| 2 | Single (single row atomic) vs Multi (BEGIN/COMMIT) |
| 3 | 4 race condition. SI 가 lost update 까지, Serializable 가 write skew 까지 |
| 4 | Serializable 의 3 구현. SSI 가 현대 표준 |
| 5 | 2PC 의 blocking 위험. Saga + compensation 가 산업 선호 |
