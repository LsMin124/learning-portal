# Chapter 10: Batch Processing — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 10** (책 p.389~438, PDF p.411~460).
> 10장: *대용량 입력* 의 *일괄 처리* — Unix philosophy 의 *분산 확장*. **MapReduce**, **Spark**, **Dataflow** 의 패러다임.

이 장의 *지적 무게중심*:
1. **Unix philosophy** — small, composable, uniform interface
2. **MapReduce** — distributed sort + group by 의 *원형*
3. **Join 전략** — sort-merge vs broadcast vs partitioned
4. **Dataflow engines** — Spark, Flink, Tez 의 *DAG 기반 진화*
5. **Batch 의 *철학*** — immutable input, deterministic, idempotent

---

## 들어가기 전에

- **선수 지식**: Unix shell, 5~6장, 3장
- **학습 목표**
  1. **Unix philosophy**
  2. **MapReduce** — distributed sort + group by
  3. **Map-side vs reduce-side join**
  4. **Dataflow engines** — Spark, Flink, Tez
  5. **Graph processing** — Pregel
  6. **Batch 의 철학** — deterministic, idempotent, immutable input
- **예상 학습 시간**: 150~180분

---

## §1 Unix Philosophy 의 가치

### §1.1 Unix tool 의 단순 예제

웹 server log 에서 *top 5 URL*:

```bash
cat /var/log/nginx/access.log |
  awk '{print $7}' |
  sort |
  uniq -c |
  sort -rn |
  head -n 5
```

- 각 도구가 입력 → 출력
- pipe 로 streaming
- 작고 한 가지만 잘함

### §1.2 Unix 의 *철학*

> *Make each program do one thing well.*
> *Expect the output of every program to become the input to another.*

특징:
- *Uniform interface* — stdin / stdout, byte sequence
- *Composition* — pipe
- *Files 가 일급 객체*
- *Transformation* — input 안 바꾸고 새 output

이게 *MapReduce 의 영감*.

---

## §2 MapReduce — Google 2004

### §2.1 모델

```python
def map(record):
    for word in record.split():
        emit(word, 1)

# Shuffle: {hello: [1, 1, 1], world: [1, 1]}

def reduce(key, values):
    emit(key, sum(values))
```

전형 — *word count*.

### §2.2 데이터 흐름

![Figure 10-1 — MapReduce. 책 p.401](/courses/ddia/figures/ch10/fig-10-1.png)

1. **Input** — HDFS/S3 의 file. partition 별
2. **Map task** — 각 input partition. data locality
3. **Shuffle** — key 별 sort + 같은 key 같은 reducer
4. **Reduce task** — 각 key 의 모든 value
5. **Output** — HDFS 의 새 file

### §2.3 핵심 통찰

- **Sort-merge** based shuffle
- **Data locality** — network 절감
- **Fault tolerance** — task 실패 시 재실행 (immutable input)

### §2.4 Hadoop ecosystem

| Component | 역할 |
|--|--|
| HDFS | Distributed file system (3-replica) |
| YARN | Resource manager |
| MapReduce | Original execution engine |
| Hive | SQL on Hadoop |
| Pig | Dataflow scripting |
| HBase | KV store on HDFS |
| Sqoop | RDBMS ↔ HDFS |
| Oozie | Workflow scheduler |
| ZooKeeper | Coordination |

→ 2010년대 big data 표준. 현재는 *cloud + S3 + Spark/Flink*.

### §2.5 MapReduce 의 한계

- *Materialize between stages* — slow
- *Map + Reduce 만* — 복잡 workflow 어려움
- *Iterative algorithm* 비효율

→ 다음 세대 진화.

---

## §3 Joining in MapReduce

### §3.1 Sort-Merge Join (Reduce-side)

1. **Map**: 두 dataset 모두 같은 key emit
2. **Shuffle**: 같은 key reducer 로
3. **Reduce**: 결합

장점: 임의 size. 단점: 모든 데이터 shuffle — 비쌈.

![Figure 10-2 — Reduce-side join. 책 p.405](/courses/ddia/figures/ch10/fig-10-2.png)

### §3.2 Broadcast Hash Join (Map-side)

작은 dataset 을 모든 mapper 에 broadcast.

장점: shuffle 없음. 조건: 작은 dataset 이 메모리에.

### §3.3 Partitioned Hash Join

두 dataset 이 *같은 partition* 함수 → 같은 partition 끼리.

**Spark 의 자동 선택**:
- `autoBroadcastJoinThreshold` (default 10 MB)
- 큰 table = sort-merge
- *Bucket join* — pre-partitioned, shuffle 회피

---

## §4 MapReduce 후속 — Dataflow Engines

### §4.1 동기

MR 의 한계 → **Dataflow engines**:
- **Spark** (Berkeley AMPLab, 2010) — in-memory
- **Tez** (Hortonworks) — DAG
- **Flink batch** — stream + batch unified

### §4.2 Spark architecture

```
[Driver]
   |
   | DAG scheduler
   ↓
[Cluster Manager] (YARN, Mesos, k8s)
   |
   ↓
[Executor 1] [Executor 2] [Executor 3]
```

**Driver**: application main, DAG 생성+최적화, task scheduling.
**Executor**: task 실행, cache + shuffle storage.
**Cluster Manager**: 자원 할당.

### §4.3 Spark 의 RDD

> **Resilient Distributed Dataset** — immutable partitioned collection.

```python
text = sc.textFile("s3://bucket/data")
words = text.flatMap(lambda line: line.split())
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("s3://bucket/output")
```

특징:
- **Lazy evaluation**
- **DAG optimization**
- **In-memory caching**
- **Lineage** — fault tolerance

### §4.4 Spark 의 *현대 API*

**DataFrame / Dataset**:
- Typed, columnar
- Catalyst optimizer
- Tungsten — off-heap, code gen

**Spark SQL**: ANSI SQL 호환.

**Structured Streaming** (11장).

### §4.5 Modern alternatives

| | 특징 |
|--|--|
| Apache Flink | True streaming, batch = stream special case |
| Apache Beam | Unified API (Spark, Flink, Dataflow runners) |
| Google Cloud Dataflow | Beam managed |
| Trino / Presto | Interactive SQL |
| DuckDB | Embedded analytics |
| ClickHouse | Real-time OLAP |

### §4.6 Higher-level abstraction

- **Hive**: SQL on Hadoop
- **Spark SQL / DataFrame**
- **dbt**: SQL-based transformation — *현대 표준*

---

## §5 Modern Data Stack

### §5.1 ELT vs ETL

**전통 ETL**: source → Transform → load to warehouse.
**Modern ELT**: source → Load to warehouse → SQL transform.

**ELT 의 이점**:
- Warehouse 의 compute 활용
- Raw data 보존
- Analyst-friendly (SQL)

### §5.2 Orchestration tools

| | 발표 | 특징 |
|--|--|--|
| Apache Airflow | 2014 (Airbnb) | DAG, Python, *de facto* |
| Prefect | 2018 | Modern Python |
| Dagster | 2019 | Asset-centric |
| Oozie | 2010 (Yahoo) | XML, legacy |
| Temporal | 2020 | Long-running workflow |

### §5.3 dbt — SQL transformation

```sql
{{ config(materialized='table') }}

select
  customer_id,
  count(distinct order_id) as total_orders,
  sum(order_amount) as total_spent
from {{ ref('stg_orders') }}
group by customer_id
```

특징:
- Modular SQL + Jinja
- Testing (schema + custom)
- Documentation auto-gen
- Lineage graph
- Incremental models

→ *Analytics engineering* 의 표준.

### §5.4 Data Lakehouse

Data lake (raw) + Warehouse (column, SQL) 결합.

**Table formats** (2020s):
- Apache Iceberg (Netflix, 2017)
- Delta Lake (Databricks, 2019)
- Apache Hudi (Uber, 2017)

**기능**:
- ACID on S3/HDFS
- Time travel (snapshot)
- Schema evolution
- Partition evolution
- Hidden partitioning

---

## §6 Graph Processing — Pregel

PageRank, shortest path 같은 graph algorithm 은 MR 비효율.

### §6.1 Pregel — Bulk Synchronous Parallel (BSP)

> "Think like a vertex". 각 vertex = 작은 process. Super-step 마다 message 교환.

```
each super-step:
  for each vertex (in parallel):
    process incoming messages
    update local state
    send messages to neighbors
  barrier — wait for all
```

장점: iterative 자연, message-passing 직관.

구현: Apache Giraph, GraphX (Spark).

---

## §7 Batch 의 *철학*

### §7.1 Input 의 immutability

> Input file 은 *절대 수정 안 함*. 출력은 *새 file*.

이점:
1. **Fault tolerance** — 재실행 항상 같은 결과
2. **Debug 가능** — 옛 input 으로 재실행
3. **Idempotency** — 부분 실패 OK

### §7.2 Deterministic transformation

- non-determinism 회피 (NOW(), RAND())
- 순서 의존 회피
- 외부 state 호출 회피 (RPC, DB)

### §7.3 Failure 처리

일부 task 실패 → 그 task 만 재실행. immutable + deterministic 으로 OK.

> **함정 1**: deterministic 깨지면 재실행 결과 다름 → fault tolerance 깨짐.

### §7.4 산업 사례

**Netflix**: S3 + Iceberg + Spark + Airflow, 수 PB 처리.
**Uber**: Hudi (자체 개발 2017), incremental processing + CDC.
**Airbnb**: Airflow (자체 개발, 2014 오픈소스), Hive + Presto + Spark.

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | MR 가 모든 problem | iterative 비효율. Spark/Flink |
| 2 | Shuffle 이 공짜 | 네트워크 + sort 가장 비쌈 |
| 3 | Broadcast join 항상 빠름 | 메모리 OOM |
| 4 | Spark 의 모든 게 메모리 | shuffle, spill 시 disk |
| 5 | non-deterministic batch | fault tolerance 깨뜨림 |
| 6 | Batch 안 RPC 호출 | external dependency 비결정성 |
| 7 | Output append update | 새 output file, mutability 회피 |
| 8 | Hive 가 real-time | 분 단위, real-time = Presto/Trino |
| 9 | Graph 도 MR | iterative 비효율. Pregel/GraphX |
| 10 | Batch exactly-once 어려움 | immutable + deterministic 자동 보장 |
| 11 | Spark 가 Hadoop 의존 | S3 + Kubernetes 만으로 충분 |
| 12 | dbt 가 ETL 대체 | T (transform) 만 |

---

## §9 자가점검

1. Unix philosophy 의 3 가지 원칙?
2. MapReduce 의 3 phase + 각 역할?
3. Reduce-side vs map-side join?
4. Broadcast hash join 의 조건?
5. Spark RDD 의 3 핵심 특성?
6. Lazy evaluation 이 왜 중요?
7. Pregel 의 BSP 모델?
8. Immutability of input 의 3 이점?
9. ELT vs ETL 차이 + 왜 ELT?
10. Data lakehouse 의 table format?

<details><summary>해답 (간략)</summary>

1. Do one thing well, output 이 다른 입력, uniform interface.
2. Map (record→key-value), Shuffle (same key 모음), Reduce (key 의 values 처리).
3. Reduce-side: shuffle, 임의 size. Map-side: shuffle 없음, broadcast 가능 size.
4. Broadcast dataset 이 모든 mapper 의 메모리.
5. Immutable, partitioned, lineage.
6. DAG 최적화 (predicate pushdown, projection pruning). Unused 안 실행.
7. 각 vertex 가 superstep 마다 message + state 갱신 + neighbor 에. Barrier.
8. Fault tolerance, debug 가능, idempotency.
9. ETL: transform 전 load. ELT: load 후 SQL transform. Warehouse compute 활용 + raw 보존.
10. Iceberg, Delta Lake, Hudi. ACID on object storage, time travel, schema/partition evolution.

</details>

---

## §10 다음 학습으로

- **11장 (Stream)** — batch 의 continuous. Kafka + Flink/Spark Streaming
- **12장 (Future)** — unbundled DB

---

## §11 한 줄 요약

> **Batch = Unix philosophy 의 분산 확장. MapReduce (Google 2004) → Spark/Flink dataflow → Modern (S3 + Iceberg + dbt + Airflow). Immutable input + deterministic = automatic exactly-once. Modern data stack = ELT + warehouse + lakehouse.**
