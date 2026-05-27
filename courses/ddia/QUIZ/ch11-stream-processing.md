# Ch 11 Stream Processing — 퀴즈

> 8 문항.

### Q1. Queue vs Log-based broker

RabbitMQ vs Kafka 의 *모델 차이* + 각 사용 사례.

<details><summary>답</summary>

| | RabbitMQ (queue) | Kafka (log) |
|--|--|--|
| Storage | transient (받으면 삭제) | persistent (TTL or 영구) |
| Order | weak | partition 안 strict |
| Replay | 불가 | offset reset 으로 가능 |
| Fan-out | exchange + binding | consumer group |
| Backpressure | flow control | consumer lag |

**RabbitMQ 적합**:
- Task queue (Celery, Sidekiq, jobs)
- 메시지가 *처리되면 삭제* 가 자연스러움
- 복잡한 routing (header, fanout, topic)

**Kafka 적합**:
- Event stream (CDC, analytics, audit log)
- *여러 consumer* 가 같은 stream 의 *다른 view*
- Replay 가 valuable (debug, new feature)
- High throughput (수십만 msg/sec)

산업 트렌드 — *데이터 backbone* 은 Kafka. *control plane / RPC reply* 는 RabbitMQ.

</details>

### Q2. CDC pipeline 설계

Postgres → Elasticsearch + Redis 의 sync. 어떻게?

<details><summary>답</summary>

**Pipeline**:

```
PostgreSQL (primary)
   │ logical replication slot
   ▼
Debezium connector → Kafka topic "users_cdc"
   │
   ├─ Kafka Connect Elasticsearch sink → ES index
   └─ Custom consumer (Java/Python) → Redis cache
```

**상세**:

1. **Postgres 설정**:
   ```sql
   ALTER SYSTEM SET wal_level = logical;
   CREATE PUBLICATION my_pub FOR TABLE users;
   ```

2. **Debezium 등록**:
   ```json
   {"name": "users-connector", "config": {
     "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
     "database.hostname": "postgres",
     "publication.name": "my_pub",
     "topic.prefix": "users"
   }}
   ```

3. **Kafka topic 구조**:
   - 각 message: `{op: "u", before: {...}, after: {...}, ts_ms: ...}`
   - INSERT / UPDATE / DELETE 모두 캡처
   - *Key = primary key* → compacted topic 가능

4. **Downstream**:
   - Elasticsearch sink connector: `users` index 자동 sync
   - Redis: custom consumer 가 `op=u` 시 cache invalidate

**Gotcha**:
- Initial snapshot 처리 (Debezium 의 snapshot mode)
- Schema evolution (4장)
- Backpressure — Kafka lag 모니터링
- ES/Redis 의 *eventual consistency* 인지

**대안**:
- AWS DMS (managed)
- Fivetran, Airbyte (saas)
- Striim, HVR (enterprise)

</details>

### Q3. Event sourcing 의 *snapshot* 필요성

10년 user account 의 모든 event (1M 개) 가 stream 에. 매번 *전체 replay* 면 느림. 해결.

<details><summary>답</summary>

**Snapshot 패턴**:

1. *Periodic snapshot* — 매 N event 마다 또는 *일정 시간* 마다 *현재 state* 를 저장
2. *Read 시* — *최신 snapshot* + 그 이후 event 만 replay
3. *Compaction* — 옛 event 는 *archive* (S3 cold storage)

**예시**:
```
Event log (1M events):
  e_1, e_2, ..., e_1000000

Snapshot at every 10000 events:
  snapshot_10k: state after e_10000
  snapshot_20k: state after e_20000
  ...
  snapshot_1M: state after e_1000000

Reconstruct user_42:
  1. Load latest snapshot (snapshot_1M)
  2. Apply event 1_000_001 to current (if any new)
```

**구현 옵션**:
- *Kafka Streams* 의 *state store* (RocksDB) — 자동 snapshot + replay
- *EventStoreDB* — built-in snapshot
- *Custom*: 각 aggregate ID 의 snapshot 을 KV store 에 저장

**Trade-off**:
- Snapshot 주기 짧음 → fast read, 많은 storage
- 길음 → slow read, 적은 storage
- 보통 *10k-100k event 마다* 또는 *일 단위*

**Compaction**:
- 옛 event 는 *archive* 만, 일상 query 안 함
- 진짜 *audit / time-travel* 시에만 archive read

</details>

### Q4. Window 선택 — 시간 vs 카운트 vs session

다음 use case 의 적절한 window:

1. 매 분 *order 수*
2. 사용자 *login session 길이*
3. *최근 100 transaction* 의 평균
4. *지난 10 분* (매분 update) 의 active user

<details><summary>답</summary>

1. **Tumbling 1 minute (event-time)** — 1분 단위 *겹침 없는* count. dashboard 의 표준.

2. **Session window (30 min idle)** — 사용자 idle 30분 = 새 session. 가변 길이.
   ```
   user_clicks → keyBy(user_id) → sessionWindow(gap = 30 min) → count
   ```

3. **Sliding count window (size = 100)** — count-based, 매 새 event 마다 *최근 100개* aggregate.
   ```
   transactions → slidingCountWindow(100, 1) → avg(amount)
   ```

4. **Hopping window (size=10 min, hop=1 min)** — 매분 update + 10분 윈도우.
   ```
   user_events → hoppingWindow(size=10m, hop=1m) → distinct(user_id)
   ```

**선택 가이드**:
- 정해진 시간 단위 → tumbling
- 겹치는 trailing → hopping
- count 단위 → count window
- 사용자 행동 (variable) → session

</details>

### Q5. Watermark 이해 — Late event 처리

다음 시나리오에서 *late event* 가 어떻게 처리되나?

```
Window: tumbling 5 min event-time
Allowed lateness: 1 min

Events:
  10:01 (event-time 10:00) ✓
  10:04 (event-time 10:03) ✓
  10:06 (event-time 10:04) ← window 10:00-10:05 일찍 close 됐을까?
  10:07 (event-time 10:02) ← late event!
```

<details><summary>답</summary>

**Window 10:00-10:05 의 close**:
- Watermark 가 *10:05 + allowed_lateness (1 min)* = *10:06* 도달 시 close
- 즉 *event-time 10:06* 의 event 가 오면 *window close + emit*

**Event 처리**:
- `10:01 (10:00)`: window 10:00-10:05 에 추가. 아직 안 emit.
- `10:04 (10:03)`: 같은 window 에 추가.
- `10:06 (10:04)`: 같은 window 에 추가 + watermark 10:06 도달 → *window close + emit aggregate*.
- `10:07 (10:02)`: **late event**. allowed_lateness 1 min 안 (10:02 vs watermark 10:06 = 4 min late > 1 min)
  - Policy 따라:
    - **Drop**: 무시
    - **Side output**: 별도 stream 으로
    - **Update emitted**: 옛 window 다시 emit (downstream 이 처리)

**Flink 의 trigger**:
- `allowedLateness(Time.minutes(1))` — 1분 안 late event 는 *window 재 trigger*
- 1분 초과 late event 는 *late side output* 으로 분리
- Production 패턴: 분당 emit + 시간당 *correction* (lambda architecture)

</details>

### Q6. Stream-Table duality — Kafka Streams 의 KTable

`KStream` 과 `KTable` 의 차이 + 변환.

<details><summary>답</summary>

**KStream**:
- *변경 stream* — 각 record 가 *event* (immutable)
- `events.filter(...)` — 각 event 처리

**KTable**:
- *현재 state* — key 별 *최신 value*
- *Compacted topic* 으로 backing
- `users.join(...)` — 현재 user state 조회

**변환**:

```java
// KStream → KTable (aggregate)
KTable<String, Long> counts = events
    .groupByKey()
    .count();   // 각 key 별 누적 count

// KTable → KStream (every change as event)
KStream<String, Long> changes = counts.toStream();

// KStream → KTable (latest value per key)
KTable<String, String> latestPrice = priceStream
    .toTable();   // 최신 가격만 보유
```

**대응 — 동일 데이터의 두 view**:
- 같은 Kafka topic 이 *stream* 으로 보면 event log, *table* 로 보면 latest snapshot
- *Compacted topic* + read 가 KTable, *regular topic* + read 가 KStream

**예시 — Order processing**:
```
order_events (KStream): {order_1: NEW}, {order_1: PAID}, {order_1: SHIPPED}
order_status (KTable): {order_1: SHIPPED}  (compacted, 최신만)
```

이 duality 가 *Kafka Streams, Flink Table API, Materialize* 의 핵심.

</details>

### Q7. 디버그 — Kafka consumer 가 *느려짐*

producer 10k msg/sec, consumer 5k msg/sec 처리. lag 가 계속 증가. 진단.

<details><summary>답</summary>

**가능 원인**:

1. **Consumer logic 의 slow path**:
   - 외부 API call (synchronous)
   - DB write (fsync)
   - 복잡한 transformation
   - → Profiling 으로 식별

2. **Single-threaded consumer**:
   - Kafka consumer 는 *partition 단위로* parallel
   - Topic 의 partition 수 < consumer 수 면 throttle
   - 해결: partition 수 ↑ + consumer 수 ↑

3. **GC pause**:
   - JVM consumer 의 large heap → GC pause → consumer lag
   - 해결: G1GC, off-heap 자료구조, smaller heap

4. **Network**:
   - Consumer ↔ Broker network latency
   - 다른 region, congested switch
   - 해결: co-located deployment

5. **Fetch size**:
   - `fetch.min.bytes`, `fetch.max.bytes` 설정 부적합
   - 너무 작으면 *round-trip 빈번*
   - 해결: batch fetch 활용

**진단 단계**:
- *Consumer lag* 측정 (`kafka-consumer-groups.sh`)
- *Consumer CPU/disk* — bottleneck identify
- *Single message processing time* profile
- *Partition assignment* — 균등한가?

**대응**:
- **Parallelism**: partition 수 늘림 + consumer instance 추가
- **Batch processing**: 한 message 가 아닌 *batch* 단위 처리 (DB bulk insert)
- **Async pipeline**: 외부 API 호출은 *async + future*
- **Compression**: producer 의 `compression.type=zstd` — bandwidth 감소

</details>

### Q8. 면접 — Lambda vs Kappa architecture

빅데이터 처리의 두 패턴. 각 trade-off.

<details><summary>답</summary>

**Lambda Architecture** (Nathan Marz, ~2012):

```
                  ┌─→ Batch layer (Hadoop/Spark)
                  │   - Full re-compute
                  │   - High accuracy
                  │   - 시간 latency (hours)
Data → Distributor
                  │
                  └─→ Speed layer (Storm/Flink)
                      - Real-time, approximate
                      - Low latency (seconds)
                      - Lost on failure

→ Serving layer (joined view)
```

장점:
- *각 layer 가 최적화*
- batch 의 정확성 + stream 의 latency

단점:
- *코드 중복* — 같은 logic 을 batch + stream 으로
- *결과 합성* 복잡
- *운영 부담 2x*

**Kappa Architecture** (Jay Kreps, 2014):

```
Data → Kafka (single source)
      ↓
      Stream processor (Flink/Kafka Streams)
      ↓
      Serving layer
```

장점:
- *단일 codebase*
- *replay* 로 "re-batch" 효과 — 옛 데이터 새 query 가능

단점:
- Stream processor 가 *큰 state* 다뤄야
- *historic re-processing* 이 stream 같은 throughput 으로 가능해야

**산업 트렌드**:
- 대형 (Netflix, Uber): hybrid — Lambda 비슷 + Kafka 가 *source-of-truth*
- 중소: **Kappa** — Flink 가 stream + batch 통합
- 새 architecture: **Lakehouse** (Databricks Delta, Iceberg) — *batch + stream + transaction* 통합

답 핵심 — 옛 lambda 의 *두 codebase 부담* 이 너무 큼. *modern engine (Flink, Beam, Spark)* 가 *unified batch+stream* 으로 *Kappa 가 dominant*. 단 *대규모 historical re-processing* 에서 batch 의 정확성 + cost 이점이 살아남음.

</details>
