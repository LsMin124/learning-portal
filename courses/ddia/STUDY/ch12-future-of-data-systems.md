# Chapter 12: The Future of Data Systems — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 12** (책 p.489~561, PDF p.511~613).
> 12장: 책의 *결론 + 미래 비전*. 모든 챕터의 idea 들을 *unified architecture* 로 통합. **Unbundled DB**, **derived data**, **end-to-end argument**, **윤리** 까지.

이 장의 *지적 무게중심*:
1. **Polyglot persistence** — 도구의 *각 강점 결합*
2. **Unbundled database** — DB component 의 *분리*, Kafka 의 backbone
3. **Derived data** — primary + multiple views
4. **Lambda → Kappa unification** — Apache Beam, Flink
5. **End-to-end argument** — application 의 idempotency 책임
6. **Ethics is engineering** — privacy, bias, surveillance

---

## 들어가기 전에

- **선수 지식**: 1~11장 모두
- **학습 목표**
  1. Derived data — primary + derived
  2. Unbundled database — Kafka 의 backbone
  3. Dataflow 가 새 abstraction
  4. End-to-end argument
  5. Verifiability + integrity
  6. Doing the right thing — ethics
- **예상 학습 시간**: 240~300분

---

## §1 Data Integration — Many Tools, One System

### §1.1 모든 챕터의 idea 통합

12장 = 다른 모든 장의 결합 패턴.

### §1.2 현실의 polyglot persistence

전형적 web app:
```
사용자 request
  ↓
Web server (stateless)
  ↓
  ├─→ PostgreSQL (primary)
  ├─→ Redis (cache)
  ├─→ Elasticsearch (search)
  ├─→ S3 (file)
  ├─→ pgvector / Pinecone (embedding)
  └─→ Kafka (events)
        ↓
        ├─→ Flink (real-time)
        ├─→ Spark (batch)
        └─→ Snowflake (warehouse)
```

### §1.3 Single tool 의 한계

> 한 system 이 *모든 use case* 못 함.

해결 — 각 도구 강점 결합 + CDC.

### §1.4 HTAP — Hybrid Transactional/Analytical

전통 = OLTP + ETL + warehouse.

**HTAP** — 한 system 이 OLTP + OLAP:
- *SingleStore* (구 MemSQL)
- *TiDB* — TiKV (OLTP) + TiFlash (OLAP)
- *Snowflake* (recent OLTP features)
- *YugaByte*

→ ETL 복잡도 회피. 단 각 workload 의 최적화 trade-off.

---

## §2 Unbundling Databases

### §2.1 Database = 여러 component 의 묶음

전통 DB 의 component:
- Storage engine
- Replication
- Indexing
- Query optimizer
- Transaction manager
- Authentication

### §2.2 Unbundled approach

각 component 를 분리된 system 으로:
- Storage: HDFS, S3, RocksDB
- Replication: Kafka (log)
- Indexing: Elasticsearch, Redis
- Query: Trino, Spark
- Transaction: app-level + outbox

### §2.3 Kafka 가 새 distributed log

Kafka = 통합 backbone:
- DB replication log = Kafka topic
- Write 가 Kafka first, downstream derived
- Source of truth = Kafka log

이게 *Event sourcing + CDC* 의 architectural 결과.

### §2.4 Modern data lakehouse

- *Storage*: S3 + Iceberg/Delta/Hudi
- *Catalog*: Glue, Polaris, Unity Catalog
- *Compute*: Spark, Trino, DuckDB, Snowflake
- *Streaming*: Kafka + Flink
- *ML*: MLflow, SageMaker, Databricks
- *Governance*: Atlan, DataHub

→ Open table format + storage/compute 분리.

---

## §3 Derived Data + Asynchrony

### §3.1 Primary vs Derived

| | Primary | Derived |
|--|--|--|
| 정의 | source of truth | 함수로 도출 |
| Update | client write | recompute / incremental |
| 일관성 | strong | eventual |
| 예시 | user table | search index, cache |

### §3.2 Derived data 의 이점

1. 각자 use case 최적화
2. Failure tolerance — primary 에서 rebuild
3. Multiple views
4. Evolution

### §3.3 Async dataflow

```
Primary write → Kafka
                  ↓
                  ├─→ Search index (async)
                  ├─→ Cache (async)
                  └─→ Analytics (async)
```

> **함정 1**: async = eventual consistency.

### §3.4 Outbox Pattern

Dual write 의 대안 — DB + Kafka atomic:

1. App 이 DB transaction 안:
   - 실제 data update
   - outbox table 에 event
2. CDC (Debezium) 가 outbox → Kafka
3. Outbox row 는 publish 후 삭제

→ DB transaction 보장 + Kafka publish. Microservices 표준.

---

## §4 Lambda → Unification

### §4.1 Lambda 의 2-codebase 문제

batch + stream 의 *같은 logic 두 번* → 운영 부담.

### §4.2 Unified — Apache Beam, Flink

> Batch = bounded stream.

```python
events = pipeline | Read.from(source)
windowed = events | Window.into(FixedWindows.of(60))
counts = windowed | Count.perElement()
```

같은 code, 다른 runner.

### §4.3 Kappa 의 진정한 실현

산업:
- Apache Beam + Dataflow/Flink
- Materialize — streaming SQL
- Apache Pinot — real-time OLAP
- RisingWave — distributed streaming SQL DB

---

## §5 End-to-End Argument

### §5.1 Lower-layer guarantee 의 한계

TCP reliable delivery 보장하지만 *application 정확성* 보장 안 됨.

### §5.2 End-to-end 해결

application 이 *직접 idempotency*:
```
client UUID
  ↓
request 에 포함
  ↓
server: 이미 처리? → idempotent
```

### §5.3 Operation ID

- Payment: transaction_id
- Order: client UUID
- API: idempotency key (Stripe, AWS)

### §5.4 Stripe 의 idempotency key

```http
POST /v1/charges
Idempotency-Key: 8a4f0e0f-...
```

- 24 시간 안 같은 key = same response
- Network 실패 시 안전한 retry

---

## §6 Verifiability + Integrity

### §6.1 Trust 의 한계

- Silent corruption
- Tampering
- Lost message

### §6.2 Merkle tree

- 각 record hash → parent hash
- Root hash 비교 → 전체 dataset 일관

→ Blockchain, Git, BitTorrent, IPFS, Certificate Transparency.

### §6.3 Audit trail

- Append-only log + cryptographic chain
- 불변 기록
- 외부 audit 가능

### §6.4 Verifiable computation

- Zero-knowledge proof
- Trusted execution environment (Intel SGX)
- Confidential computing

---

## §7 Modern Trends

### §7.1 AI / ML 통합

**Vector database**:
- Pinecone, Weaviate, Qdrant, Milvus
- pgvector (Postgres)
- HNSW, IVF (ANN)
- RAG (LLM + vector search)

**Feature store**:
- Feast, Tecton
- Online + offline

### §7.2 Data Mesh (Zhamak Dehghani 2019)

- Decentralized data ownership
- Domain-driven data
- Data as product
- Self-serve platform

예: Netflix, Spotify, Zalando.

### §7.3 Real-time analytics

- Snowflake Snowpipe — 분 단위
- BigQuery Streaming — 즉시
- ClickHouse — sub-second
- Pinot, Druid — second-level

### §7.4 Sustainability

- Carbon footprint
- Google carbon-free 24/7 (2030)
- Spot instance 효율
- Cold tier storage (Glacier)

---

## §8 Doing the Right Thing — Ethics

### §8.1 Data is power

데이터 비대칭 — 회사가 사용자보다 훨씬 많이.

### §8.2 Bias + discrimination

ML model 의 training bias:
- 채용 model → 역사적 불평등 영속
- 신용 평가 → discrimination
- Facial recognition → minority error rate ↑

**실제 사례**:
- Amazon 채용 AI (2018) — 여성 차별
- COMPAS — 인종 bias
- Apple Card (2019) — 성별 신용 차별 의혹

### §8.3 Privacy + surveillance

- Data 유출 = 영원
- Inference attack
- Right to be forgotten (GDPR) — backup, derived 의 어려움

**규제**:
- GDPR (EU 2018)
- CCPA (California 2020)
- LGPD (Brazil 2020)
- 한국 PIPA

### §8.4 Responsibilities

1. Data minimization
2. Purpose limitation
3. Data deletion
4. Transparency
5. Consent
6. Audit

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Single DB 가 모든 use case | polyglot persistence |
| 2 | Dual-write 로 derived sync | CDC + stream |
| 3 | Primary 변경 시 derived 수동 | Kafka backbone propagation |
| 4 | Lambda 의 두 codebase | Beam, Flink unified |
| 5 | Lower-layer = app correctness | end-to-end argument |
| 6 | Backup = derived | backup PITR, derived current |
| 7 | "데이터 많을수록 좋다" | bias + privacy. minimization |
| 8 | ML model 이 객관적 | training bias |
| 9 | Compliance 충족 = OK | 법은 최소. 윤리 더 큼 |
| 10 | "내 일 아니야" | engineer 책임 |
| 11 | Dual-write outbox 없이 | Outbox pattern |
| 12 | Vector DB 만능 | context window, embedding quality 한계 |

---

## §10 자가점검

1. Polyglot persistence + 각 도구 role?
2. Unbundled database + Kafka?
3. Primary vs Derived + 이점?
4. Outbox pattern?
5. Lambda vs unified?
6. End-to-end argument + idempotency key?
7. Merkle tree?
8. Data Mesh?
9. Data minimization + purpose limitation?
10. ML bias 의 발생?

<details><summary>해답 (간략)</summary>

1. PG (primary), Redis (cache), ES (search), S3 (file), Kafka (event), Flink (stream), Spark (batch), Snowflake (warehouse), pgvector (embedding).
2. DB component 분리. Kafka = 통합 log backbone.
3. Primary: SOT, 1개. Derived: 함수 도출, 여러 개. 이점: 최적화, fault tolerance, multiple views, evolution.
4. DB transaction 안 outbox table 도 write. CDC 가 outbox → Kafka. DB + Kafka atomic.
5. Lambda: batch + stream 둘 다. Unified: 같은 code, batch = bounded stream.
6. Lower layer 가 app correctness 보장 못함. App UUID + dedup.
7. Record hash → parent hash. Root hash 비교 = 전체 무결성.
8. Decentralized domain ownership. Data as product. Self-serve.
9. Minimization: 필요 데이터만. Purpose: 명시 목적만.
10. Training data bias → 학습 → 역사적 불평등 영속.

</details>

---

## §11 끝맺음

12 chapter 의 여정 — *간단한 ACID DB* 에서 *분산 unbundled architecture + 윤리* 까지.

핵심 메시지:
1. **No silver bullet** — 각 도구 trade-off
2. **Composition over monolith** — 작은 도구 결합
3. **Immutability is power** — event sourcing, CDC, batch
4. **End-to-end thinking** — application 책임
5. **Ethics is engineering**

DDIA 마지막 — *"우리는 시스템을 어떻게 만드는가뿐 아니라, 왜 만드는가도 물어야"*.

---

## §12 한 줄 요약

> **Unbundled DB = Kafka backbone + 도구의 결합. Primary + derived data + async. Lambda → Kappa unified. End-to-end idempotency. Modern AI/ML stack (vector, RAG) + Data Mesh. *Ethics is engineering* — privacy, bias, minimization.**
