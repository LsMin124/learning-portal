# Ch 11 Stream Processing — 치트시트

## TL;DR

- **Event stream** = unbounded append-only log. Producer → Broker → Consumer
- **Kafka** (log-based): persistent, replay, per-partition order. *RabbitMQ* (queue): transient, weak order
- **CDC** = DB replication log → stream. Dual-write 의 대체
- **Event sourcing** = state change 자체를 immutable event 로
- **Window**: tumbling / hopping / sliding / session
- **Event-time vs processing-time**. **Watermark** = late event 한계 추정
- **Stream-Table duality**: stream = table 의 change log, table = stream 의 aggregate
- **Exactly-once** = idempotent + 2PC. Flink/Kafka Streams 가 production-ready
- **Checkpoint** = stream 의 fault tolerance

---

## Quick Reference

### 표 1. Broker 비교

| | Queue (RabbitMQ) | Log (Kafka) |
|--|--|--|
| Storage | transient | persistent |
| Order | weak | per-partition strict |
| Replay | ✗ | ✓ |
| Fan-out | exchange + binding | consumer group |
| 사용 | task queue, RPC | event stream, CDC |

### 표 2. Kafka 구조

```
Topic (logical name)
  ├─ Partition 0: [event 1, event 2, ...]    ← total order within
  ├─ Partition 1: [event 100, event 101, ...]
  └─ Partition 2: ...

Replication factor = N (각 partition 의 N copy)
Consumer group = parallel consumption
Compacted topic = key 별 latest only
```

### 표 3. Window 종류

| 종류 | 의미 | 사용 |
|--|--|--|
| Tumbling | 겹침 없는 fixed | 매 분 count |
| Hopping | 겹침 있는 fixed | rolling average |
| Sliding | count/time 기준 동적 | 최근 N event |
| Session | idle 기반 | user session |

### 표 4. Time 종류

| | Event time | Processing time |
|--|--|--|
| 의미 | 발생 시각 | 받은 시각 |
| 결정 | producer | broker / processor |
| 정확도 | 정확 (clock 신뢰 시) | 항상 known |
| 사용 | aggregate | rough metric |

**Watermark**: "event-time ≤ t 의 event 더 안 옴" 추정. window close trigger.

### 표 5. CDC pipeline

```
PostgreSQL (logical replication slot)
  ↓
Debezium connector
  ↓
Kafka topic "users_cdc"
  ↓
  ├─ ES sink connector → Elasticsearch
  ├─ Redis consumer → cache
  └─ Spark Streaming → warehouse
```

### 표 6. Stream-Table duality

```
KStream (events):
  {user_1: login}, {user_1: click}, {user_1: logout}

KTable (state, compacted):
  {user_1: logout}  (key 별 latest)

변환:
  stream → table: aggregate (groupByKey + reduce)
  table → stream: toStream() — every change as event
```

### 표 7. Exactly-once 3 기법

```
1. Idempotency:
   - SET counter = 100  ✓
   - INCREMENT counter  ✗ (반복 시 잘못)
   - 자연스러운 idempotent: PUT, write-with-unique-id

2. Distributed transaction (2PC):
   - output write + offset commit atomic
   - Kafka 0.11+, Flink built-in

3. Output dedup:
   - downstream 이 id 로 dedup
   - external system 에 효과적
```

### 표 8. Architectures

| | Lambda | Kappa |
|--|--|--|
| Layers | batch + speed (둘 다) | stream only |
| Code | 중복 (2 buckets) | 단일 |
| Replay | batch 가 자연 | stream replay (Kafka log) |
| Latency | batch hours + stream secs | secs |
| 적합 | 큰 historical re-compute | modern unified |

---

## Mind Map

```
11장 Stream Processing
├─ 1. Event stream (unbounded log)
├─ 2. Brokers
│   ├─ Queue (RabbitMQ) — task queue
│   └─ Log (Kafka) — event stream
├─ 3. CDC
│   ├─ DB log → Kafka
│   └─ Debezium, AWS DMS
├─ 4. Event sourcing
│   ├─ state change = immutable event
│   └─ snapshot for performance
├─ 5. Stream processing
│   ├─ Flink, Spark Streaming, Kafka Streams
│   ├─ Window (tumbling/hopping/sliding/session)
│   ├─ Event time + watermark
│   └─ Stream-table duality
├─ 6. Exactly-once
│   ├─ Idempotency
│   ├─ 2PC (Kafka 0.11+)
│   └─ Output dedup
└─ 7. Fault tolerance
    └─ Checkpoint (state + offset rollback)
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | Stream = unbounded immutable event sequence |
| 2 | Kafka 가 dominant log-based broker, RabbitMQ 는 queue |
| 3 | CDC 가 dual-write 의 대체. Debezium 표준 |
| 4 | Event sourcing 은 state change 자체를 event 로 |
| 5 | Window + event time + watermark 이 stream 의 고유 영역 |
| 6 | Exactly-once = idempotent + 2PC. 외부 system 엔 한계 |
| 7 | Checkpoint = stream 의 batch-like fault tolerance |
