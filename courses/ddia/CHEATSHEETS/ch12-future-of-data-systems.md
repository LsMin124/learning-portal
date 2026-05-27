# Ch 12 Future of Data Systems — 치트시트

## TL;DR

- 책 12 chapter 의 *결론* — 모든 아이디어를 unified architecture 로
- **Unbundled DB**: 전통 DB component (storage, replication, indexing, query) 가 *분리된 system*
- **Kafka** 가 새 backbone — distributed log
- **Primary** (1, source of truth) + **Derived** (many, function of primary). CDC 로 sync
- **Unified processing** (Apache Beam, Flink) — batch = bounded stream
- **End-to-end argument** — application 만이 application correctness 보장
- **Verifiability** — Merkle tree, audit log
- **Ethics** — data is power. minimization, transparency, accountability

---

## Quick Reference

### 표 1. Unbundled architecture

```
                ┌─────────────────────┐
                │   Application       │
                └─────────┬───────────┘
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
   PostgreSQL          Kafka                S3
   (primary)         (event log)          (files)
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
   Elasticsearch        Redis             Snowflake
   (search)           (cache)            (analytics)
        │                 │                  │
        └──── CDC <───────┘                  │
              from Kafka                     │
                                             │
                          ┌──────────────────┘
                          ▼
                       Trino (query federation)
```

### 표 2. Primary vs Derived

| | Primary | Derived |
|--|--|--|
| 정의 | source of truth | 함수로 도출 |
| 갯수 | 1 | 다수 |
| Sync | client write | CDC/stream |
| 일관성 | strong | eventual |
| Rebuild | (X) | Kafka log replay 로 |
| 예시 | Postgres | ES, Redis, Snowflake, Neo4j |

### 표 3. Lambda vs Kappa vs Unified

| | Lambda | Kappa | Unified (Beam/Flink) |
|--|--|--|--|
| Layers | batch + speed | stream | single |
| Code | 중복 | 단일 | 단일 |
| Replay | batch | Kafka log | source 별 |
| 산업 | 옛 표준 | 진행 중 | future |

### 표 4. End-to-end correctness

```
사용자 의도
  ↓
Application logic (idempotency key)
  ↓
RPC client (retry, timeout)
  ↓
Network (TCP — reliable transmission)
  ↓
DB (ACID transaction)

각 layer 는 *각자의 guarantee*. 
app correctness 는 *app layer 의 책임*.
```

### 표 5. Verifiability — Merkle Tree

```
        Root Hash (전체 dataset 의 hash)
        /         \
       H_AB       H_CD
       /   \      /   \
      H_A  H_B  H_C  H_D
       |    |    |    |
      R_A  R_B  R_C  R_D  (records)

검증:
  - 일부 record 변경 → leaf hash 변경 → parent hash → root 변경
  - Root hash 만 비교하면 *전체 dataset* integrity
  - O(log n) proof: 한 record 의 integrity 증명에 *log n hash*만 필요
```

응용: Git, blockchain, IPFS, Certificate Transparency.

### 표 6. Ethical responsibilities

| 원칙 | 의미 |
|--|--|
| Data minimization | 필요한 것만 수집 |
| Purpose limitation | 명시된 목적만 |
| Transparency | 사용자에게 알림 |
| Consent | 의미 있는 선택 |
| Data deletion | 진정한 erasure (cryptographic) |
| Audit trail | 사용 기록 |
| No discrimination | bias 검증 |

### 표 7. 책 전체 핵심 메시지

```
1. No silver bullet         — 각 도구 trade-off
2. Composition over monolith — 작은 도구 결합
3. Immutability is power    — event sourcing, CDC, batch
4. End-to-end thinking      — application 책임
5. Ethics is engineering    — 사회적 영향 인식
```

---

## Mind Map

```
12장 Future of Data Systems
├─ 1. Polyglot persistence (각 도구 강점)
├─ 2. Unbundled database
│   ├─ Storage / Replication / Indexing / Query 분리
│   └─ Kafka 가 backbone
├─ 3. Primary + Derived
│   ├─ CDC 로 sync
│   └─ Async dataflow
├─ 4. Unified processing
│   ├─ Apache Beam, Flink
│   └─ Batch = bounded stream
├─ 5. End-to-end argument
│   └─ idempotency key, operation ID
├─ 6. Verifiability + Integrity
│   ├─ Merkle tree
│   └─ Audit log
└─ 7. Ethics
    ├─ Data minimization
    ├─ Transparency
    └─ Engineer 의 사회적 책임
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | 도구 polyglot, 각자 강점 결합 |
| 2 | Unbundled DB — Kafka 가 backbone |
| 3 | Primary 1 + Derived many. CDC sync |
| 4 | Unified batch+stream (Beam, Flink) |
| 5 | End-to-end: application 이 correctness 책임 |
| 6 | Merkle tree 가 cryptographic integrity |
| 7 | Ethics is engineering. 기술 = 사회 |
