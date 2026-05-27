# Ch 5 Replication — 치트시트

## TL;DR

- 4 목적: geographic, availability, throughput, durability
- 3 모델: **Single-leader** (대세), **Multi-leader** (geo, offline), **Leaderless** (Cassandra)
- Sync vs async vs **semi-sync** (산업 표준 — 1개 sync + 나머지 async)
- 5 anomaly: read-your-writes / monotonic / consistent prefix / lost update / phantom
- Multi-leader 의 핵심 도전 = conflict resolution (avoid / LWW / CRDT / custom)
- Leaderless 의 **W + R > N** quorum → 최신 read 보장 (concurrent write 별개)
- **Logical replication** (row-based) 이 현대 표준. CDC 의 기반

---

## Quick Reference

### 표 1. 세 모델

| | Single-leader | Multi-leader | Leaderless |
|--|--|--|--|
| Write | leader 만 | 어느 leader | 어느 replica |
| 충돌 | 없음 | 빈번 | quorum 회피 |
| 일관성 | 강 (leader) | 약 (eventual) | tunable (W,R) |
| Geographic | 한 region | native | OK |
| 예시 | Postgres, MySQL | CouchDB, BDR | Cassandra, Riak |

### 표 2. Sync 모드

| | Durability | Latency | Availability |
|--|--|--|--|
| Sync (all) | 강 | 가장 느림 | 모두 up |
| Async | 약 | 빠름 | replica 죽어도 OK |
| Semi-sync (1+) | 중간 | 빠름 | 표준 |

### 표 3. Replication log

| 방식 | 비고 |
|--|--|
| Statement-based | NOW/RAND 문제 |
| WAL (physical) | binary, version 종속 |
| Logical (row) | **현대 표준**, CDC |
| Trigger | overhead |

### 표 4. 5 anomaly

| Anomaly | 해결 |
|--|--|
| Read-your-writes | 자기 데이터는 leader / log offset wait |
| Monotonic reads | sticky session (consistent hashing) |
| Consistent prefix | 인과 데이터 같은 partition |
| Lost update | transaction (7장) |
| Phantom | transaction (7장) |

### 표 5. Multi-leader conflict resolution

| 방법 | 적합 |
|--|--|
| Avoidance (home region) | 단순, 사용자 이동 어색 |
| LWW (timestamp) | 단순, 시계 부정확 위험 |
| CRDT (commutative) | counter, set 등 |
| Custom merge | 복잡 객체 (Google Docs OT) |

### 표 6. Quorum (Leaderless)

```
N: replica 수
W: write quorum
R: read quorum

조건: W + R > N → 최신 read 보장

표준: N=3, W=2, R=2  (1 node failure tolerance)
     N=5, W=3, R=3  (2 node failure tolerance)

W=1: 빠른 write, 데이터 손실 위험
R=1: 빠른 read, stale 위험
```

### 표 7. Failover 위험

| 위험 | 예방 |
|--|--|
| Split brain | Fencing token, STONITH, Quorum election |
| Data loss (async lag) | Semi-sync, log offset 기록 |
| False failover | Heartbeat timeout 조정 (~30s) |
| Cascading failure | Circuit breaker, automated rollback |

---

## Mind Map

```
5장 Replication
├─ 1. 4 목적 (geo, avail, throughput, durability)
├─ 2. Single-leader (대세)
│   ├─ Sync / async / semi-sync
│   ├─ Replication log (4 방식)
│   └─ Failover (split brain 위험)
├─ 3. Replication lag
│   └─ 5 anomaly + 각 해결
├─ 4. Multi-leader
│   ├─ Geographic, offline, collab edit
│   └─ Conflict resolution (4 방법)
└─ 5. Leaderless (Dynamo-style)
    ├─ W + R > N quorum
    ├─ Sloppy quorum + hinted handoff
    └─ Version vector for concurrent write
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | 4 목적: geo / avail / throughput / durability |
| 2 | Single-leader 가 대세. semi-sync 표준 |
| 3 | Lag 의 5 anomaly. 각각 다른 해결 |
| 4 | Multi-leader 의 충돌이 *항상* 운영 부담 |
| 5 | Leaderless 의 W+R>N 으로 quorum 조정 |
