# Ch 10 Batch Processing — 치트시트

## TL;DR

- **Unix philosophy** 의 distributed 확장: small composable tools, immutable input, deterministic transformation
- **MapReduce** = Map (parallel) + Shuffle (sort+group) + Reduce. Sort-merge 가 핵심
- **Joins**: reduce-side (sort-merge), map-side (broadcast hash), partitioned hash
- **Dataflow engines** (Spark, Tez, Flink batch) = MR 진화. in-memory, DAG 최적화
- **Spark RDD**: immutable, partitioned, lineage. lazy + cache
- **Pregel** (think like a vertex): iterative graph algorithm
- **철학**: input immutable + deterministic transformation = fault tolerance

---

## Quick Reference

### 표 1. MapReduce 흐름

```
Input (HDFS/S3, partitioned, immutable)
  │
  ▼
Map task per partition
  │   record → emit(key, value)
  ▼
Shuffle
  │   - sort by key
  │   - send same key to same reducer
  │   - network transfer
  ▼
Reduce task per key partition
  │   key, values → emit(output)
  ▼
Output (new HDFS files)
```

### 표 2. Join 종류

| 방식 | 조건 | Shuffle | 적합 |
|--|--|--|--|
| Reduce-side (sort-merge) | 무관 | 양쪽 모두 | Large × Large |
| Broadcast hash | 한쪽이 메모리 fit | 큰쪽만 (없음) | Small × Large |
| Partitioned hash | 둘 다 같은 partition | 없음 | 미리 partitioned 된 경우 |

### 표 3. Engine 진화

| | MapReduce | Spark | Flink | Trino |
|--|--|--|--|--|
| 표현력 | Map + Reduce | DAG | DAG + stream | SQL |
| Materialization | stage 마다 disk | in-memory + cache | streaming | in-memory |
| Iteration | 비효율 | 효율 (cache) | 효율 | N/A |
| Latency | 시간 | 분 | 분/초 | 초 |
| Fault tolerance | task retry | lineage replay | checkpoint | query retry |

### 표 4. Spark RDD 특성

| | 의미 |
|--|--|
| Resilient | lineage 로 fault tolerance |
| Distributed | partition 으로 cluster 전체에 |
| Dataset | immutable collection |
| Lazy | `action()` (collect, count, save) 시 실행 |
| Cached | memory/disk 에 저장 가능 |

### 표 5. Pregel (BSP) 모델

```
each super-step (parallel for each vertex):
  receive messages from prev step
  update local state
  send messages to neighbors
barrier (모든 vertex 끝나야 다음 step)

terminate when:
  - all vertices "voted to halt", AND
  - no messages in flight
```

### 표 6. 산업 도구

| 용도 | 도구 |
|--|--|
| Schedule batch jobs | Airflow, Prefect, Dagster |
| Storage | S3, HDFS, GCS |
| Format | Parquet, ORC, Avro (4장) |
| Engine | Spark, Trino, Hive, Flink |
| Catalog | Hive Metastore, Iceberg, Delta |
| Streaming/Batch unified | Flink, Spark Structured Streaming |

### 표 7. Batch 철학

```
Input:
  - immutable (HDFS, S3, never modify)
  - schema 명시 (Avro, Parquet)

Transformation:
  - deterministic (NOW/RAND 금지)
  - pure (no external state, no RPC)
  - composable (DAG)

Output:
  - new file (옛 것 옆에)
  - atomic (commit 시점 분명)

Fault tolerance:
  - failed task → 재실행
  - 같은 input + deterministic → 같은 output
  - automatic
```

---

## Mind Map

```
10장 Batch Processing
├─ 1. Unix philosophy (data flow 의 원형)
├─ 2. MapReduce
│   ├─ Map + Shuffle + Reduce
│   └─ Sort-merge 가 핵심
├─ 3. Joins
│   ├─ Reduce-side (sort-merge)
│   ├─ Broadcast hash (map-side)
│   └─ Partitioned hash
├─ 4. Dataflow engines
│   ├─ Spark (RDD, DAG, lineage)
│   ├─ Tez, Flink batch
│   └─ Higher: Hive, Pig, SparkSQL
├─ 5. Graph (Pregel BSP)
│   └─ GraphX, Giraph
└─ 6. Philosophy
    ├─ Input immutable
    ├─ Deterministic transformation
    └─ Fault tolerance 자동
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | Unix philosophy = small + composable + immutable input |
| 2 | MapReduce = Map + Sort-Shuffle + Reduce, sort-merge 핵심 |
| 3 | Joins: small × big → broadcast, big × big → sort-merge |
| 4 | Spark/Flink = MR 진화, in-memory + DAG 최적화 |
| 5 | Pregel = think like a vertex, iterative graph 친화 |
| 6 | Batch 의 fault tolerance = immutable + deterministic |
