# Chapter 11: Stream Processing — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 11** (책 p.439~488, PDF p.461~510).
> 11장: batch 의 *continuous* 버전. *event stream* + *Kafka* + *Flink/Spark Streaming*. **CDC (Change Data Capture)**, **event sourcing**, **windowing**.

## 들어가기 전에

- **선수 지식**: 4장 (encoding), 5장 (replication, CDC), 10장 (batch)
- **학습 목표**
  1. **Event stream** — unbounded, append-only log
  2. **Message broker** (Kafka) vs **traditional queue** (RabbitMQ)
  3. **CDC** — DB write 를 stream 으로 변환
  4. **Event sourcing** — append-only state evolution
  5. **Stream processing** — Flink, Spark Streaming, Kafka Streams
  6. **Time** — event vs processing time, watermark
  7. **Window** — tumbling, hopping, session
  8. **Exactly-once** semantics — *어떻게* 달성하나
- **예상 학습 시간**: 200~240분

---

## 1. Event Stream 의 정의

### 1.1 Stream 의 본질

> *Unbounded sequence of events*, *appended over time*.

batch (bounded) ↔ stream (unbounded). 그러나 *같은 데이터 모델*:
- Event = immutable record with timestamp
- Producer → broker → consumer
- Storage 가 *append-only log*

### 1.2 Message brokers — 두 가지 모델

**Traditional message queue** (AMQP — RabbitMQ, ActiveMQ):
- *Transient*: consumer 가 받으면 message 삭제
- *Queue* 단위 fan-out
- *Order* 강하지 않음
- 사용: task queue (Celery, Sidekiq)

**Log-based broker** (Kafka, Pulsar, Kinesis):
- *Persistent*: log file 에 영구 저장 (TTL or 무한)
- *Topic-partition* 단위. partition 안 *strict order*
- Consumer 가 *offset 추적*
- *Replay 가능* — 옛 메시지 다시 읽기

→ 11장 의 주제는 *log-based*. Kafka 가 dominant.

---

## 2. Kafka — 분산 log

### 2.1 구조

```
Topic: "user_events"
  └─ Partition 0: [event 1, event 2, event 3, ...]
  └─ Partition 1: [event 100, event 101, ...]
  └─ Partition 2: [event 200, event 201, ...]
```

- 각 partition 이 *log file* (3장의 LSM-like)
- *Replication factor* — partition 마다 N copy
- *Consumer group* — group 안 partition 분배 (parallelism)

### 2.2 Kafka 의 핵심 보장

- **Per-partition total order** — 한 partition 안에선 *완전 순서*
- **At-least-once delivery** — message 못 잃음 (consumer 가 ack 후 commit)
- **Replay** — consumer offset reset 으로 *옛 message 다시*
- **Retention** — TTL 또는 *compact* (key 별 latest 만 유지)

> **함정 1**: *전체 topic* total order 아님. *partition 안* 만. *causality 가 partition 경계* 면 ordering 보장 안 됨.

### 2.3 Topic 종류

- **Compacted topic** — key 별 최신 value 만 유지 (key-value store 처럼). Kafka Streams 의 state.
- **Regular topic** — TTL 기반 retention (7일, 30일 등). event log.

---

## 3. Change Data Capture (CDC)

### 3.1 동기

primary RDBMS 의 변경을 *downstream system* (검색 index, cache, warehouse) 에 *실시간 sync*.

전통 — *dual write*: app 이 *DB 와 search index 둘 다* write. 위험:
- 한쪽 실패 시 *불일치*
- ordering 깨질 수 있음

**CDC 의 해결**:
1. App 이 *DB 만* write
2. DB 의 *replication log* (write-ahead log, binlog) 를 *stream 으로*
3. Downstream consumer 가 stream 에서 변경 받음

![Figure 11-5 — Database 의 변경이 CDC stream 으로 → derived system. 책 p.455](/courses/ddia/figures/ch11/fig-11-5.png)

### 3.2 산업 도구

- **Debezium** — PostgreSQL, MySQL, MongoDB 의 CDC → Kafka
- **Maxwell** — MySQL binlog → Kafka
- **AWS DMS** — managed CDC service
- **Kafka Connect** — connector framework

### 3.3 Event Sourcing — 더 깊은 패턴

> *상태 변경* 자체를 *Kafka topic 에 first-class event* 로.

전통:
```
User updates email → DB.update(user, {email: "new"})
```

Event sourcing:
```
User updates email → emit event {type: "EmailChanged", user_id: 42, new: "new"}
→ event log 에 append (immutable)
→ Read model (cached projection) 갱신
```

**장점**:
- *완전한 audit trail*
- *Time travel* — 과거 시점 state 재구성
- *Multiple read models* — 같은 event 에서 *여러 view* 도출

**단점**:
- 복잡함
- Event schema evolution (4장)
- Snapshot 관리 (state 재구성 비용)

---

## 4. Stream Processing — Flink, Spark Streaming, Kafka Streams

### 4.1 Stream processor 의 task

각 event 에 대해:
- *Transformation* (map, filter)
- *Aggregation* (count, sum, avg over time)
- *Join* (stream × stream, stream × table)
- *Pattern detection* (CEP — complex event processing)

### 4.2 Window — *stream 위에서 aggregate*

stream 은 무한. *aggregate 결과* 를 *언제* 출력?

**Window 종류**:

```
Tumbling window (5 분):
  [0-5][5-10][10-15]...   # 겹침 없음
  
Hopping window (5 분, 1 분 hop):
  [0-5][1-6][2-7][3-8]...  # 1분마다 새 window

Sliding window (사용자 정의):
  마지막 N 개 event 또는 *event 시간 기준*

Session window:
  사용자가 *X 시간 동안 idle* 이면 새 session
  → 동적 길이
```

### 4.3 Event time vs Processing time

| | Event time | Processing time |
|--|--|--|
| 의미 | event 가 *실제 발생* 한 시각 | processor 가 *받은* 시각 |
| 결정 시점 | producer 가 결정 | broker / processor |
| 신뢰성 | producer clock 의존 | local clock |
| 사용 | 정확한 aggregate | 빠른 처리 |

**Event time 의 도전**:
- *Late event* — network delay, mobile offline
- *Out-of-order* arrival
- *얼마나 기다려야* late event 가 안 옴?

### 4.4 Watermark — *late event 의 한계 신호*

> "Event time t 이전의 event 는 *더 이상 안 옴* 이라고 *추정*."

Watermark t 가 오면 *event time ≤ t* 의 window 를 *close + emit*. t 이후의 event 는 *late* (handle policy 결정 — drop, side-output, update).

Apache Beam, Flink 의 *first-class concept*.

### 4.5 Stream-Table Duality

> **Stream = Table 의 *change log***. **Table = Stream 의 *현재 state* (aggregate)**.

Kafka 의 *compacted topic* 이 이 idea — *key 별 최신 value* 가 table.

이게 *unified batch+stream* 의 이론적 기반 (Flink, Beam).

---

## 5. Exactly-Once Semantics

### 5.1 도전

stream processing 의 *각 event 가 정확히 한 번 처리*. 실패 시:
- *At-most-once* — event drop 가능 (under-count)
- *At-least-once* — event 중복 처리 가능 (over-count)
- *Exactly-once* — 정확히 한 번

### 5.2 Achieving exactly-once

1. **Idempotency** — 같은 event 의 *반복 처리* 가 같은 결과 (예: `SET counter = 100` 은 idempotent, `INCREMENT counter` 은 아님)
2. **Distributed transaction** — write + offset commit 을 *atomic* (2PC). Kafka 0.11+ 의 *exactly-once* 가 이 방식.
3. **Effectful operation 의 transaction 결합** — *output topic write* 가 *input offset commit* 과 *atomic*.

Flink, Kafka Streams 가 *production-ready exactly-once*.

> **함정 2**: *Side effect 가 외부 system* (DB, API) 이면 *진정한 exactly-once 불가능*. *idempotent operation* 으로 *효과 동등* 만 보장.

---

## 6. Fault tolerance — Checkpoint

Flink, Spark Streaming 의 *state recovery*:

1. *주기적 checkpoint* — 모든 operator 의 state + input offset 을 storage 에
2. *Failure 시* — 마지막 checkpoint 로 *모든 operator + offset rollback*
3. *Replay* — 그 offset 부터 input stream 재처리

이게 batch 의 *immutable input* 와 같은 효과. *stream 에서 fault tolerance* 의 표준.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Kafka topic = global total order | partition 안만. 전체 topic 은 partial |
| 2 | Stream = "fast batch" | event time, watermark, late event 등 *고유* 도전 |
| 3 | Event time = processing time | 다름. 신뢰할 만한 *event time* 가 어려움 |
| 4 | Exactly-once = no failure | 실제로는 *idempotent + 2PC*. 외부 system 엔 어려움 |
| 5 | Stream processor 가 DB 대체 | 한정된 query. complex query 는 batch + warehouse |
| 6 | CDC = dual write | dual write 의 *대체*. dual write 자체가 안티패턴 |
| 7 | Event sourcing = *모든 system 적용* | 복잡도 큼. *audit-critical* 부분에만 |
| 8 | RabbitMQ = Kafka | 다른 모델. queue vs log |
| 9 | Watermark = 정확 | 추정. late event handling 정책 결정 |
| 10 | Stream processing 이 *모든 batch 대체* | 둘 다 필요. Lambda / Kappa architecture |

---

## 자가점검

1. *Traditional queue* vs *log-based broker* 의 *3 가지 차이*.
2. *Kafka 의 per-partition order* 의 의미.
3. *CDC* 의 정의 + dual-write 대비 *장점*.
4. *Event sourcing* 의 *3 가지 장단점*.
5. *Tumbling, hopping, sliding, session* window 의 차이.
6. *Event time* vs *processing time* + *watermark* 의 역할.
7. *Stream-table duality* 의 의미.
8. *Exactly-once* 의 *3 가지 달성 방법*.
9. *Checkpoint* 가 *fault tolerance* 어떻게 제공.

### 해답 (간략)

1. Queue: transient, queue 단위. Log: persistent, partition 안 order, replay 가능.
2. 한 partition 안에선 *strict total order*. 다른 partition 사이 순서 보장 X.
3. DB 의 변경 (replication log) 을 *stream* 으로. Dual write 의 *불일치 + 순서 깨짐* 회피.
4. + complete audit, time travel, multiple read models. − 복잡도, schema evolution, snapshot.
5. Tumbling: 겹침 없는 고정 길이. Hopping: 겹침 있는 고정 길이. Sliding: 시간/count 기준 이동. Session: idle 기반 동적.
6. Event time: 실제 발생. Processing time: 받은 시각. Watermark: event time t 이전의 event 가 더 안 옴 추정.
7. Stream = table 의 change log. Table = stream 의 aggregate. 둘은 같은 데이터의 두 view.
8. Idempotency, distributed transaction (2PC), output write + offset commit atomic.
9. 주기적으로 모든 operator state + input offset 저장. failure 시 그 시점으로 rollback + replay.

---

## 다음 학습으로

- **12장 (Future)** — unbundled DB. stream 이 *모든 derived data* 의 backbone
- *Apache Beam* — batch + stream unified programming model
- *Streaming SQL* (ksqlDB, Materialize) — SQL on stream
