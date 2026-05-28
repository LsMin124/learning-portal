# Chapter 11: Stream Processing — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 11** (책 p.439~488, PDF p.461~510).
> 11장: batch 의 *continuous* 버전. *event stream* + *Kafka* + *Flink/Spark Streaming*. **CDC**, **event sourcing**, **windowing**.

이 장의 *지적 무게중심*:
1. **Event stream** — *unbounded log*, batch 와의 unification
2. **Kafka** — log-based broker 의 표준
3. **CDC + Event Sourcing** — DB ↔ stream 의 통합
4. **Windowing** — event time vs processing time, watermark
5. **Exactly-once** — idempotency + transaction

---

## 들어가기 전에

- **선수 지식**: 4장 (encoding), 5장 (CDC), 10장 (batch)
- **학습 목표**
  1. Event stream — unbounded log
  2. Message broker (Kafka) vs traditional queue
  3. CDC — DB write → stream
  4. Event sourcing — append-only state
  5. Stream processing — Flink, Spark, Kafka Streams
  6. Time — event vs processing, watermark
  7. Window — tumbling, hopping, session
  8. Exactly-once semantics
- **예상 학습 시간**: 200~240분

---

## §1 Event Stream 의 정의

### §1.1 Stream 의 본질

> *Unbounded sequence of events*, *appended over time*.

batch (bounded) ↔ stream (unbounded). 같은 데이터 모델:
- Event = immutable record + timestamp
- Producer → broker → consumer
- Storage = append-only log

### §1.2 Message brokers — 두 가지 모델

**Traditional message queue** (AMQP — RabbitMQ, ActiveMQ):
- *Transient*: consumer 받으면 삭제
- *Queue* 단위 fan-out
- 사용: task queue (Celery, Sidekiq)

**Log-based broker** (Kafka, Pulsar, Kinesis):
- *Persistent*: log file 영구
- *Topic-partition*, partition 안 strict order
- Consumer offset 추적
- *Replay 가능*

→ 11장 = log-based. Kafka dominant.

---

## §2 Kafka — 분산 log

### §2.1 구조

```
Topic: "user_events"
  └─ Partition 0: [event 1, 2, 3, ...]
  └─ Partition 1: [event 100, 101, ...]
  └─ Partition 2: [event 200, 201, ...]
```

- 각 partition = log file
- *Replication factor* — partition 마다 N copy
- *Consumer group* — partition 분배

### §2.2 Kafka architecture

```
[Producer] → [Kafka Broker] → [Consumer]
                  |
   [Broker 1] [Broker 2] [Broker 3]
                  |
              [Metadata]
       (ZooKeeper 또는 KRaft)
```

**KRaft** (KIP-500, 2022):
- ZooKeeper 의존 제거
- 내부 Raft consensus
- Self-managed metadata

### §2.3 Kafka 의 핵심 보장

- **Per-partition total order**
- **At-least-once delivery**
- **Replay** — offset reset
- **Retention** — TTL 또는 compact

> **함정 1**: *전체 topic* total order 아님. partition 안만.

### §2.4 Topic 종류

- **Compacted topic** — key 별 최신 value (KV store 처럼)
- **Regular topic** — TTL retention (7일, 30일)

### §2.5 Kafka alternatives

| | 발표 | 특징 |
|--|--|--|
| Apache Pulsar | 2016 (Yahoo) | Multi-tenant, geo-replication |
| AWS Kinesis | 2013 | Managed |
| Google Pub/Sub | 2015 | Managed, auto-scaling |
| Azure Event Hubs | 2014 | Managed |
| NATS JetStream | 2020 | Lightweight |
| Redpanda | 2021 | C++ Kafka-compat |

---

## §3 Change Data Capture (CDC)

### §3.1 동기

primary RDBMS 의 변경을 *downstream* (검색 index, cache, warehouse) 에 sync.

전통 — *dual write*: app 이 *DB 와 search 둘 다*. 위험:
- 한쪽 실패 → 불일치
- ordering 깨짐

**CDC 해결**:
1. App 이 *DB 만* write
2. DB replication log (WAL, binlog) → stream
3. Consumer 가 변경 받음

![Figure 11-5 — CDC stream → derived. 책 p.455](/courses/ddia/figures/ch11/fig-11-5.png)

### §3.2 산업 도구

- **Debezium** — PG, MySQL, MongoDB → Kafka
- **Maxwell** — MySQL binlog
- **AWS DMS** — managed
- **Kafka Connect** — connector framework
- **Striim, Fivetran, Airbyte** — modern ELT

### §3.3 Event Sourcing

> *상태 변경 자체* 를 *Kafka topic 의 first-class event* 로.

전통:
```
User updates email → DB.update(user, {email: "new"})
```

Event sourcing:
```
User updates email → emit event {type: "EmailChanged", user_id: 42, new: "new"}
→ event log append (immutable)
→ Read model 갱신
```

**장점**:
- 완전한 audit trail
- Time travel
- Multiple read models

**단점**:
- 복잡
- Event schema evolution
- Snapshot 관리

### §3.4 CQRS

**Command Query Responsibility Segregation**:
- *Command side* (write) — event 발행
- *Query side* (read) — event 로 projection

**예 — e-commerce**:
- Command: `PlaceOrder` event
- Query 1: 주문 목록 (PostgreSQL)
- Query 2: 매출 dashboard (ClickHouse)
- Query 3: 추천 (vector DB)

Event log = source of truth.

---

## §4 Stream Processing

### §4.1 Stream processor 의 task

- Transformation (map, filter)
- Aggregation (count, sum, avg)
- Join (stream × stream, stream × table)
- Pattern detection (CEP)

### §4.2 Stream processor 비교

| | 발표 | 특징 |
|--|--|--|
| Apache Storm | 2011 | First-gen, low-level |
| Spark Streaming | 2013 | Micro-batch, RDD |
| Spark Structured Streaming | 2016 | DataFrame, exactly-once |
| Apache Flink | 2014 | True streaming, low-latency |
| Kafka Streams | 2016 | Library (no cluster) |
| Apache Beam | 2016 | Unified API |
| ksqlDB | 2017 (Confluent) | SQL on Kafka |
| Materialize | 2019 | Streaming SQL DB |

### §4.3 Window

```
Tumbling (5 min): [0-5][5-10][10-15]   # 겹침 없음
Hopping (5 min, 1 min hop): [0-5][1-6][2-7]   # 겹침
Sliding: 시간/count 기준
Session: idle 기반 동적
```

### §4.4 Event time vs Processing time

| | Event time | Processing time |
|--|--|--|
| 의미 | 실제 발생 시각 | 받은 시각 |
| 결정 | producer | broker / processor |
| 신뢰 | producer clock | local clock |
| 사용 | 정확 aggregate | 빠른 처리 |

**Event time 의 도전**:
- *Late event* — network delay, mobile offline
- *Out-of-order*
- *얼마나 기다려야* late event 안 옴?

### §4.5 Watermark

> "Event time t 이전 event 는 *더 이상 안 옴* 추정."

Watermark t → event time ≤ t 의 window close + emit. t 이후 late event:
- *Drop* (default)
- *Side output*
- *Update*

### §4.6 Stream-Table Duality

> **Stream = Table 의 *change log***. **Table = Stream 의 *현재 state*** (aggregate).

Kafka 의 *compacted topic* = 이 idea — key 별 최신 = table.

**ksqlDB 예**:
```sql
CREATE STREAM orders (id INT, amount DOUBLE, user_id INT)
  WITH (kafka_topic='orders', value_format='JSON');

CREATE TABLE user_totals AS
  SELECT user_id, SUM(amount) AS total
  FROM orders
  GROUP BY user_id;
```

→ Stream 위 SQL, table = continuous aggregate.

---

## §5 Exactly-Once Semantics

### §5.1 도전

- *At-most-once* — drop 가능
- *At-least-once* — 중복 처리 가능
- *Exactly-once* — 정확히 한 번

### §5.2 Achieving exactly-once

1. **Idempotency** — 같은 event 반복 = 같은 결과
   - `SET counter = 100` (idempotent)
   - `INCREMENT counter` (NOT)

2. **Distributed transaction** — write + offset commit atomic (2PC). Kafka 0.11+.

3. **Output topic + input offset** atomic.

Flink, Kafka Streams = production-ready exactly-once.

> **함정 2**: *Side effect 가 외부 system* (DB, API) 이면 진정한 exactly-once 불가. *idempotent operation* 으로 효과 동등.

### §5.3 Idempotent 패턴

**Unique key + upsert**:
```sql
INSERT INTO orders (id, ...) VALUES (123, ...)
ON CONFLICT (id) DO UPDATE SET ...
```

**Idempotent ID**:
- Event 마다 unique ID
- 처리한 ID set 유지
- 재처리 시 skip

**Compare-and-swap**:
- Version 검사 후 update

---

## §6 Fault tolerance — Checkpoint

Flink, Spark Streaming 의 *state recovery*:

1. *주기적 checkpoint* — operator state + offset 저장
2. *Failure* → 마지막 checkpoint rollback
3. *Replay* — 그 offset 부터 재처리

이게 batch 의 *immutable input* 과 같은 효과.

**Flink 의 Chandy-Lamport-style**:
- *Barrier* (special marker) 가 stream 따라 흐름
- 각 operator 가 barrier 받으면 state snapshot
- *Consistent global snapshot*

---

## §7 Lambda vs Kappa

### §7.1 Lambda Architecture (Marz, 2014)

```
Source → Batch (Hadoop) → Serving DB
       → Stream (Storm) → Serving cache
```

- Batch: 정확, 분~시간 latency
- Stream: 빠름, 부정확 가능

**문제**: *두 codebase 유지*.

### §7.2 Kappa Architecture (Kreps, 2014)

```
Source → Kafka → Stream processor → Serving
```

- *재처리* = 옛 offset replay
- Single codebase
- Beam, Flink unified API

**현대 trend** = Kappa. 단 *역사적 batch* 는 여전히.

---

## §8 산업 사례

### §8.1 Uber

- Kafka — 핵심 event bus
- Flink — real-time analytics
- Pinot — real-time OLAP
- Hudi — incremental data lake

### §8.2 LinkedIn 의 origin

- Kafka 의 origin (2010)
- Activity stream — 100B+ events/day
- Samza — 자체 stream processor

### §8.3 Netflix

- Mantis — 자체 stream processor
- Keystone — Kafka pipeline
- Real-time content recommendation

### §8.4 Kafka Connect ecosystem

| Source | Sink |
|--|--|
| Debezium (PG, MySQL, MongoDB) | Elasticsearch |
| JDBC | S3, HDFS |
| File | BigQuery, Snowflake |
| MQTT (IoT) | Redis |

→ Kafka = data integration hub.

---

## §9 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Kafka topic = global total order | partition 안만 |
| 2 | Stream = "fast batch" | event time, watermark 고유 도전 |
| 3 | Event time = processing time | 다름 |
| 4 | Exactly-once = no failure | idempotent + 2PC. 외부 system 어려움 |
| 5 | Stream processor 가 DB | 한정된 query. complex = batch + warehouse |
| 6 | CDC = dual write | dual write 의 대체 |
| 7 | Event sourcing = 모든 system | 복잡도. audit-critical 만 |
| 8 | RabbitMQ = Kafka | 다른 모델 |
| 9 | Watermark = 정확 | 추정 |
| 10 | Stream 이 모든 batch 대체 | 둘 다 필요 |
| 11 | Lambda = 표준 | Kappa 가 modern |
| 12 | Kafka 무한 retention | TTL 또는 compact. 무한은 비용 큼 |

---

## §10 자가점검

1. Queue vs log-based broker 의 3 차이?
2. Kafka per-partition order 의 의미?
3. CDC 정의 + dual-write 대비 장점?
4. Event sourcing 의 3 장단점?
5. Tumbling/hopping/sliding/session window?
6. Event time vs processing time + watermark?
7. Stream-table duality?
8. Exactly-once 의 3 방법?
9. Checkpoint 가 fault tolerance 어떻게?
10. Lambda vs Kappa?

<details><summary>해답 (간략)</summary>

1. Queue: transient, 단위. Log: persistent, partition order, replay.
2. 한 partition 안 strict total. 다른 사이 X.
3. DB 변경 → stream. Dual write 의 불일치 + 순서 깨짐 회피.
4. + audit, time travel, multi read. − 복잡, schema evolution, snapshot.
5. Tumbling: 겹침 X. Hopping: 겹침. Sliding: 시간/count. Session: idle 동적.
6. Event time: 실제. Processing: 받은 시각. Watermark: t 이전 event 안 옴 추정.
7. Stream = table change log. Table = stream aggregate.
8. Idempotency, distributed transaction, output + offset atomic.
9. 주기적 operator state + offset 저장. Failure 시 rollback + replay.
10. Lambda: batch + stream 2 layer. Kappa: stream 만. Kappa 가 modern.

</details>

---

## §11 다음 학습으로

- **12장 (Future)** — unbundled DB
- Apache Beam — unified
- Streaming SQL (ksqlDB, Materialize)

---

## §12 한 줄 요약

> **Stream = batch 의 *continuous* 버전. Kafka log-based broker. CDC + Event Sourcing + CQRS 의 DB-stream 통합. Window + Event time + Watermark. Exactly-once = idempotency + 2PC. Lambda 의 dual stack → Kappa 의 unified streaming.**
