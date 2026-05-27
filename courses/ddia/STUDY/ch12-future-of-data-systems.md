# Chapter 12: The Future of Data Systems — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 12** (책 p.489~561, PDF p.511~613).
> 12장: 책의 *결론 + 미래 비전*. 모든 챕터의 idea 들을 *unified architecture* 로 통합. **Unbundled DB**, **derived data**, **end-to-end argument**, **윤리** 까지.

## 들어가기 전에

- **선수 지식**: 1~11장 모두
- **학습 목표**
  1. **Derived data** — primary + derived 의 통합 view
  2. **Unbundled database** — single DB 의 component 들이 *분리* 됨
  3. **Dataflow** 가 새 abstraction — Kafka + Flink + KV store
  4. **End-to-end argument** — *application-level* idempotency
  5. **Verifiability** + **integrity** — Merkle tree, audit log
  6. **Doing the right thing** — privacy, surveillance, ethical engineering
- **예상 학습 시간**: 240~300분 (책의 마지막, 광범위)

---

## 1. Data Integration — Many Tools, One System

### 1.1 모든 챕터의 idea 통합

12장 = 다른 모든 장의 *결합 패턴*:
- 1장 R/S/M
- 2장 data model
- 3장 storage engine
- 4장 encoding
- 5~6장 replication + partition
- 7장 transaction
- 8장 distributed trouble
- 9장 consensus
- 10~11장 batch + stream

### 1.2 *현실의 polyglot persistence*

전형적 web app:
```
사용자 request
  ↓
Web server (stateless)
  ↓
  ├─→ PostgreSQL (primary)
  ├─→ Redis (cache)
  ├─→ Elasticsearch (search)
  ├─→ S3 (file storage)
  └─→ Kafka (events)
        ↓
        ├─→ Flink (real-time analytics)
        ├─→ Spark (batch ETL)
        └─→ Snowflake (warehouse)
```

각 도구가 *다른 강점*. *어떻게 일관* 유지?

### 1.3 *Single tool* 의 한계

> 한 system 이 *모든 use case* 못 함:
> - PostgreSQL 의 search 가 Elasticsearch 보다 약함
> - Elasticsearch 의 transaction 이 PostgreSQL 보다 약함
> - Redis 의 query 능력이 한정

해결 — *각 도구의 강점 결합* + *데이터 일관성 메커니즘* (CDC).

---

## 2. Unbundling Databases

### 2.1 *Database = 여러 component 의 묶음*

전통 DB 가 *내부적으로* 보유:
- *Storage engine* (B-tree, LSM-tree)
- *Replication* (leader, follower)
- *Indexing* (secondary)
- *Query optimizer*
- *Transaction manager*
- *Authentication, ACL*

→ 모두 *한 server process* 안.

### 2.2 *Unbundled* approach

각 component 를 *분리된 system* 으로:
- *Storage*: HDFS, S3, RocksDB
- *Replication*: Kafka (log)
- *Indexing*: Elasticsearch, Redis (derived from Kafka)
- *Query*: Trino, Spark
- *Transaction*: app-level + outbox pattern

이게 *Hadoop ecosystem + Kafka ecosystem* 의 본질. *각 부분 최적화 + 조합*.

### 2.3 *Kafka 가 새 distributed log*

Kafka 가 *통합 backbone* 역할:
- DB 의 *replication log* = Kafka topic
- *write* 가 *Kafka 에 first*, downstream system 이 derived
- *Source of truth = Kafka log*. DB 는 *current state* 의 *materialized view*

이게 **Event sourcing + CDC** 의 architectural 결과.

---

## 3. Derived Data + Asynchrony

### 3.1 *Primary* vs *Derived*

| | Primary | Derived |
|--|--|--|
| 정의 | source of truth | primary 에서 *함수* 로 도출 |
| Update | client write | recompute 또는 incremental |
| 일관성 | strong | eventual |
| 예시 | DB의 user table | search index, cache, summary |

### 3.2 Derived data 의 이점

1. **각 derived 가 *use case 별* 최적화** — search engine, cache, analytics
2. **Failure tolerance** — derived 손상 시 *primary 에서 rebuild*
3. **Multiple views** — 같은 primary 에서 *여러 derived* 생성
4. **Evolution** — schema 변경 시 *새 derived index 만 새로*

### 3.3 *Async* dataflow

```
Primary write → Kafka
                  ↓
                  ├─→ Search index (async)
                  ├─→ Cache (async)
                  └─→ Analytics (async)
```

*Async* → *primary 의 write* 가 다른 system 에 *직접 의존 안 함*. failure independence.

> **함정 1**: async = *eventual consistency*. 짧은 시간에 *불일치* 발생. user-facing UI 라면 *읽은 직후 자기 write* 처리 필요 (5장 read-your-writes).

---

## 4. Lambda Architecture 의 한계 + Unification

### 4.1 Lambda 의 *2-codebase* 문제 (10~11장)

batch + stream 의 *같은 logic 두 번 작성* → 운영 부담.

### 4.2 *Unified processing model* — Apache Beam, Flink

> Batch = bounded stream. 같은 API, 같은 runtime.

```python
# Apache Beam — same code for batch + stream
events = pipeline | Read.from(source)        # batch: file, stream: Kafka
windowed = events | Window.into(FixedWindows.of(60))
counts = windowed | Count.perElement()
```

*같은 코드* 가 *batch 모드* 면 file 기준, *stream 모드* 면 Kafka 기준 실행.

### 4.3 *Kappa 의 진정한 실현*

> *Single dataflow definition*. *Replay* 가 *batch 효과*.

산업:
- **Apache Beam** + Dataflow / Flink
- **Materialize** — streaming SQL with consistency
- **Apache Pinot** — real-time OLAP

---

## 5. End-to-End Argument

### 5.1 *Lower-layer* guarantee 의 한계

TCP 의 *reliable delivery* 보장하지만 *application 의 정확성* 보장 안 됨. 예:
- packet 이 reliably 도착했어도 *application 이 처리* 못했을 수 있음
- DB 의 *atomic write* 보장해도 *application logic 의 dup* 가능

### 5.2 *End-to-end* 해결

application 이 *직접 idempotency 보장*:

```
client generates UUID
  ↓
include UUID in request
  ↓
server: check "이 UUID 이미 처리?" → idempotent
```

*Lower layer 의 retry, dup* 모두 OK — *application 이 idempotent* 면.

### 5.3 *Operation ID*

각 important operation 에 *unique ID*:
- Payment: transaction_id
- Order: order_id (client 가 UUID 생성)
- API request: idempotency key (Stripe, AWS)

이게 *분산 시스템의 end-to-end correctness*.

---

## 6. Verifiability + Integrity

### 6.1 *Trust* 의 한계

데이터가 *외부 system* 또는 *오래된 storage* 에 있으면:
- *Silent corruption* — disk bit flip, software bug
- *Tampering* — 외부자 또는 내부자
- *Lost message* — Kafka topic 의 *부분 손실*

### 6.2 *Cryptographic* integrity

**Merkle tree**:
- 각 record 의 *hash* 가 *parent hash* 에 포함
- 한 record 변경 시 *모든 parent hash* 변경
- *Root hash* 만 비교하면 *전체 dataset 일관* 확인

→ Blockchain, Git, BitTorrent, IPFS 의 핵심.

### 6.3 *Audit trail*

- *Append-only log* (event sourcing) + cryptographic chain
- 누가 언제 무엇을 했는지 *불변 기록*
- 외부 audit 가능 (회계, 규제)

---

## 7. Doing the Right Thing — Ethics

### 7.1 *Data is power*

데이터의 *비대칭* — 회사가 사용자보다 *훨씬 많이* 알고 있음:
- 사용자 행동 추적
- 친구·관심사 *profile*
- 의도하지 않은 *민감 정보* 누설

### 7.2 *Bias + discrimination*

ML model 의 *학습 data 의 bias*:
- 채용 model 이 *과거 채용 패턴* 학습 → *역사적 불평등* 영속
- 신용 평가가 *특정 zip code* → discrimination
- Facial recognition 이 *minority 에 error rate ↑*

### 7.3 *Privacy + surveillance*

- *Data 가 *유출* — 한 번 leaked 면 *영원*
- *Inference attack* — 익명 데이터에서 *개인 식별*
- *Right to be forgotten* (GDPR) — 그러나 *backup, derived, log* 의 삭제 어려움

### 7.4 *Responsibilities*

engineer 의 책임:
1. **Data minimization** — 필요한 것만 수집
2. **Purpose limitation** — 명시된 목적만 사용
3. **Data deletion** — *진정한 삭제* (모든 derived 포함)
4. **Transparency** — 사용자에게 *명시*
5. **Consent** — 의미 있는 선택권
6. **Audit** — 사용 *기록*

이게 *기술 + 윤리* 의 결합. 책의 마지막 메시지.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | *Single DB* 가 모든 use case 해결 | polyglot persistence 가 산업 표준. 각 도구 강점 활용 |
| 2 | Dual-write 로 derived sync | CDC + stream 으로 (4장, 11장) |
| 3 | Primary 변경 시 derived 도 *수동 업데이트* | Kafka backbone 으로 자동 propagation |
| 4 | Lambda 의 두 codebase 유지 | Apache Beam, Flink 의 unified |
| 5 | *Lower-layer* (TCP, DB) 가 *application correctness* 보장 | end-to-end argument. application 의 idempotency |
| 6 | Backup = derived | backup 은 *point-in-time recovery*. derived 는 *current state* |
| 7 | "데이터 많을수록 좋다" | bias + privacy 위험. minimization 원칙 |
| 8 | ML model 이 *객관적* | training data 의 bias 그대로 학습. inherent unfairness |
| 9 | Compliance 만 충족하면 OK | 법보다 *윤리적 책임* 더 큼. 법은 *최소* |
| 10 | "내 일 아니야" — engineering 만 | technology 의 사회적 영향 *engineer 의 책임* 도 일부 |

---

## 자가점검

1. *Polyglot persistence* + 각 도구의 *role*.
2. *Unbundled database* 의 핵심 idea + Kafka 의 역할.
3. *Primary* vs *Derived data* 의 차이 + derived 의 이점.
4. *Lambda* vs *unified (Beam, Flink)* 의 차이.
5. *End-to-end argument* + *idempotency key* 의 활용.
6. *Merkle tree* 가 *integrity* 어떻게 제공.
7. *Data minimization* + *purpose limitation* 의 의미.
8. *ML bias* 가 *어떻게* 발생.

### 해답 (간략)

1. PostgreSQL (primary), Redis (cache), Elasticsearch (search), S3 (file), Kafka (event), Flink (stream), Spark (batch), Snowflake (warehouse). 각자 use case.
2. DB 의 component (storage, replication, indexing, query) 가 *분리된 system* 으로. Kafka 가 *통합 log backbone*.
3. Primary: source of truth, 1개. Derived: 함수로 도출, 여러 개. Derived 의 이점 — 각자 최적화, failure tolerance, multiple views, evolution.
4. Lambda: batch + speed 둘 다 (코드 중복). Unified: 같은 코드, batch=bounded stream.
5. Lower layer guarantee 가 *app correctness* 보장 못함. app 이 *unique ID + dedup* 직접.
6. 각 record hash 가 parent hash 에 포함. root hash 비교로 *전체 dataset* 무결성 검증.
7. Minimization: *필요한 데이터만 수집*. Purpose limitation: *명시된 목적만 사용*.
8. Training data 의 *bias* 그대로 학습. 채용 model 이 *과거 채용 패턴* (불평등) 영속.

---

## 끝맺음

> 12 chapter 의 여정 — *간단한 ACID DB* 에서 *분산 unbundled architecture + 윤리* 까지.

핵심 메시지:
1. **No silver bullet** — 각 도구가 trade-off. 측정 후 결정.
2. **Composition over monolith** — 작은 도구 결합이 *큰 단일* 보다 유연.
3. **Immutability is power** — event sourcing, CDC, batch 모두 *immutable input* 기반.
4. **End-to-end thinking** — application 책임 명확.
5. **Ethics is engineering** — 기술 결정의 사회적 영향 인식.

DDIA 의 마지막 — *"우리는 시스템을 *어떻게* 만드는가뿐 아니라, *왜* 만드는가도 물어야"*.
