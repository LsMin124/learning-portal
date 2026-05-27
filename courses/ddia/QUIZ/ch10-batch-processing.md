# Ch 10 Batch Processing — 퀴즈

> 8 문항.

### Q1. MapReduce 의 3 phase 의 *역할*

각 phase 가 *왜* 필요한가.

<details><summary>답</summary>

1. **Map** — 입력 record 를 *(key, value) pair* 로 변환. *partition 안에서 병렬 처리*. 데이터 가까이 (data locality).
2. **Shuffle** — 같은 key 의 모든 value 를 *같은 reducer* 로 모음. *sort + network transfer*.
3. **Reduce** — 같은 key 의 모든 value 를 *집계*. 결과를 새 file 로.

**왜 분리**:
- Map 은 *embarassingly parallel* — 어떤 record 든 독립 처리
- Reduce 는 *같은 key 의 모든 record* 필요 → sort + grouping 의 *barrier*
- Shuffle 이 *가장 비싼 step* (network)

→ 모든 distributed processing 의 *기본 패턴*. Spark, Flink 도 본질적으로 같음.

</details>

### Q2. Broadcast vs Reduce-side join 선택

10TB 의 user activity log + 1GB 의 user profile 을 join. 어느 방식?

<details><summary>답</summary>

**조건**:
- 1GB user profile: *메모리에 들어감* (10GB+ heap 가진 modern executor)
- 10TB activity log: 너무 크다

**Broadcast hash join**:
1. user profile 을 *모든 mapper 에 broadcast* (1GB × N mapper 의 network 비용)
2. 각 mapper 가 *자기 partition 의 activity log 를 stream*, profile 과 in-memory hash lookup
3. **shuffle 없음** — 매우 빠름

**대비 Reduce-side**:
1. user_id 로 *두 dataset 모두 shuffle*
2. 10TB + 1GB = 모두 network 통과 → 매우 비쌈
3. 시간 *수 시간*

**Spark 의 결정**:
- `spark.sql.autoBroadcastJoinThreshold = 10MB` (default) — 이보다 작으면 자동 broadcast
- 10MB ~ 1GB 사이는 *명시적 hint* — `broadcast(profileDF)`
- 1GB+ 는 보통 reduce-side. 단 SSD + 큰 메모리 면 *수 GB* 도 broadcast 가능.

원칙: **Small × Large** = broadcast. **Large × Large** = sort-merge or partitioned.

</details>

### Q3. Spark RDD 의 lineage 와 fault tolerance

Spark task 가 실패하면 어떻게 복구?

<details><summary>답</summary>

**Lineage**:
- 각 RDD 가 *부모 RDD + 어떤 transformation* 의 *기록*
- 예: `rdd3 = rdd2.map(f); rdd2 = rdd1.filter(g); rdd1 = textFile(...)`
- lineage = transformation chain

**Failure 복구**:
1. Task 실패 (executor crash 또는 timeout)
2. Driver 가 *잃은 partition* 식별
3. *Lineage 로 거슬러 올라가* — 그 partition 을 만들 *원래 transformation* 찾음
4. 그 transformation 을 *다른 executor 에서 재실행*
5. 부모 RDD 도 잃었으면 *재귀적으로* 재실행

**최적화**:
- `cache()` — 특정 RDD 를 메모리 / 디스크 에 *저장*. fault 시 그 지점부터 재실행
- `checkpoint()` — RDD 를 *durable storage (HDFS)* 에 저장. lineage 끊고 새로 시작

**전제**:
- Input 이 *immutable* (HDFS, S3)
- Transformation 이 *deterministic*
- 이 두 가지 깨지면 fault tolerance 깨짐

이게 MapReduce 보다 *훨씬 효율* — MR 은 *stage 마다 디스크*, Spark 는 *lineage + 메모리*.

</details>

### Q4. Lazy evaluation 의 최적화 예제

```python
df = spark.read.parquet("/data")
df2 = df.filter("country = 'KR'").select("name", "age")
df3 = df2.groupBy("age").count()
df3.show()
```

Spark 가 *어떻게 최적화* 하나?

<details><summary>답</summary>

**Lazy + 최적화 pipeline**:

1. **Logical plan** 생성 — 위 코드의 DAG (Read → Filter → Select → GroupBy → Count → Show)
2. **Optimizer 적용**:
   - **Predicate pushdown**: filter 를 *read 직후* 로 — parquet file 의 metadata 보고 *부분만 read*
   - **Column pruning**: select 의 *name, age 만* read — parquet 의 column 별 저장 활용
   - **Predicate pushdown to data source**: parquet 의 *각 row group 의 min/max* 로 *country = 'KR'* 가능성 없는 group skip
3. **Physical plan** 결정 — JOIN algorithm 선택, partition 수 결정
4. **Execution** — `show()` 호출 시 비로소 실행

**효과**:
- 1TB parquet → 실제 read 가 *< 10GB* (country=KR 만, 2 column 만)
- 10x 빠름

**대조 — eager evaluation**:
- 모든 transformation 이 *즉시 실행*
- df 가 1TB → 메모리 폭발 또는 매우 느림
- Pandas 가 이 방식 (작은 dataset 용)

이게 Spark / Flink / Dask 가 *Pandas 보다 큰 scale* 처리 가능한 이유.

</details>

### Q5. MapReduce 의 *iterative* 비효율

PageRank 의 100 iteration 을 MR 로 처리 시 *무엇이 비싼가*?

<details><summary>답</summary>

**PageRank pseudocode**:
```
PR[v] = (1 - d) / N  + d * Σ PR[u] / out_degree[u] for u → v
```

매 iteration 이 *graph 전체 scan + neighbor message*.

**MR 로 한 iteration**:
1. Map: 각 page 의 *현재 PR* 를 outgoing link 의 destination 에 send
2. Reduce: incoming PR contribution 합산
3. *전체 graph + 모든 PR* 을 HDFS 에 *materialize*

**100 iteration**:
- HDFS 에 100번 read/write
- 매번 mapper 의 *jar copy*, JVM startup 등 overhead
- 결과: 100 GB graph 의 PageRank 가 *수 시간*

**대안 — Pregel / GraphX**:
- Graph 가 *메모리에 cached*
- 매 iteration 이 *message passing only*
- HDFS materialize 없음
- 같은 PageRank 가 *수 분*

산업 — *Spark GraphX*, *Apache Giraph*, *Neo4j Graph Data Science* (in-DB).

</details>

### Q6. 디버그 — MapReduce job 의 *skew*

20 node cluster 의 MR job 이 *19 node 끝나고 1 node 만 1 시간* 더 걸림. 원인?

<details><summary>답</summary>

**Hot reducer (data skew)**:

특정 key 가 *압도적으로 많은 value* → 그 key 의 reducer 가 *전체 데이터의 상당부분* 처리. 한 node 가 *bottleneck*.

**전형 케이스**:
- *Celebrity user* 의 friend list (Twitter, Facebook)
- *Top-selling product* 의 review (Amazon)
- *NULL key* 의 모든 record (join 의 흔한 함정)

**진단**:
- Hadoop UI 또는 Spark UI 의 *task duration histogram*
- 한 task 가 *p99 의 10x+* 면 skew
- Reducer input 의 *record 수* 비교

**해결**:

1. **Skewed key 분리** — celebrity user 만 별도 처리:
```python
celebrity_keys = {1, 42, 999}
normal_data = data.filter(k not in celebrity_keys)
celebrity_data = data.filter(k in celebrity_keys)
# 각자 다르게 처리, 마지막 union
```

2. **Salting** — key 에 random suffix:
```python
# original: key=42 의 모든 record 가 한 reducer
# salted: key=(42, 0), (42, 1), ..., (42, 9) — 10개 reducer 로 분산
salted = data.map((k, v): ((k, hash(v) % 10), v))
# reduce 후 다시 (k, ...) 로 합침
```

3. **Combiner 사용** — mapper 안에서 *부분 aggregate*. shuffle 데이터 줄임. associative + commutative op 필요 (count, sum, min, max).

4. **Map-side aggregation** — 같은 효과를 mapper 가 batch 로 처리.

Spark 의 `repartition()`, MR 의 `Partitioner` 커스텀이 도구.

</details>

### Q7. Hive vs Presto/Trino 의 *선택*

같은 SQL on Hadoop 인데 *어떻게 다른가*?

<details><summary>답</summary>

| | Hive | Presto / Trino |
|--|--|--|
| Architecture | MR / Tez / Spark backend | *자체 distributed query engine* |
| Latency | 분 단위 | 초 단위 |
| 적합 | 큰 ETL job, batch | interactive query, dashboard |
| Materialization | stage 마다 디스크 | *all in-memory* (failure 시 다시 시작) |
| Fault tolerance | task 재시도 | 전체 query 재시도 |
| Data size | TB~PB | GB~TB |
| SQL | HiveQL (SQL 변종) | ANSI SQL 가까움 |

**선택 가이드**:
- *Daily ETL* (수십 GB → TB 처리): Hive 또는 Spark SQL
- *BI dashboard, ad-hoc analysis*: Presto/Trino
- *Real-time streaming aggregate*: ClickHouse, Druid, Pinot

**산업 패턴**:
- ETL: Spark (Hive 대체 트렌드)
- Interactive: Trino (Presto fork) — Airbnb, Pinterest, Netflix 표준
- 둘 다 *같은 storage* (S3 / HDFS / Hive Metastore) 위에서 동작
- *Lakehouse architecture* (Databricks Delta, Apache Iceberg) 가 이 둘 + transaction 까지 통합

</details>

### Q8. 면접 — Batch 가 *왜 사라지지 않나*?

"실시간 스트리밍이 답이다. Batch 는 옛 기술" 이라는 주장에 어떻게 답?

<details><summary>답</summary>

**Batch 가 *여전히 강한 이유***:

1. **Throughput** — 분 단위 처리에 *bandwidth + CPU* 의 *최대 활용*. Stream 은 record 단위 처리 overhead.

2. **Deterministic + idempotent** — input immutable, transformation deterministic → *재실행 안전*. Stream 의 exactly-once 는 *훨씬 어려움* (11장).

3. **복잡한 transformation** — multi-step JOIN, window, ML feature engineering 등이 *SQL/DataFrame* 으로 자연스럽게 표현. Stream 의 *windowing* 은 까다로움.

4. **Debug + reproducibility** — 잘못된 결과 발견 시 *옛 input 으로 다시 실행*. Stream 은 *입력 stream 재생산* 필요 (Kafka log retention 의존).

5. **Cost** — Spot/Preemptible instance 활용. 실시간 SLA 없으니 *cheap compute*.

6. **Bounded scope** — *어제까지* 의 데이터 처리. cutoff 명확. Stream 의 *late event* 같은 corner case 없음.

**산업 현실 — Lambda Architecture / Kappa Architecture**:
- *Lambda*: batch (정확) + stream (빠르지만 근사) 를 *결합*
- *Kappa*: stream only, batch 는 *처음부터 replay*

대부분 회사는 *둘 다* 운영:
- *Hourly batch*: 정확한 집계, ML 학습
- *Real-time stream*: 대시보드, alert, recommendation

답 핵심 — "*Batch vs Stream* 의 dichotomy 자체가 옛 것. 두 가지가 *서로 다른 도구*. 적절한 곳에 적절히 사용. *unified engine* (Flink, Spark) 이 trend.

</details>
