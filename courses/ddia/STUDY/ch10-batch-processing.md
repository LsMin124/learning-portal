# Chapter 10: Batch Processing — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 10** (책 p.389~438, PDF p.411~460).
> 10장: *대용량 입력* 의 *일괄 처리* — Unix philosophy 의 *분산 확장*. **MapReduce**, **Spark**, **Dataflow** 의 패러다임.

## 들어가기 전에

- **선수 지식**: Unix shell (pipe, sort, uniq), 5~6장 (replication, partitioning), 3장 (column store)
- **학습 목표**
  1. **Unix philosophy** — small, composable tools. data flow 의 *원형*
  2. **MapReduce** — distributed sort + group by
  3. **Map-side vs reduce-side join**
  4. **Dataflow engines** — Spark, Flink batch, Tez — MR 의 진화
  5. **Graph processing** — Pregel
  6. **Batch 의 *철학*** — *deterministic, idempotent, immutable input*
- **예상 학습 시간**: 150~180분

---

## 1. Unix Philosophy 의 가치

### 1.1 Unix tool 의 단순 예제

웹 server log 에서 *top 5 URL* 추출:

```bash
cat /var/log/nginx/access.log |
  awk '{print $7}' |              # URL column 추출
  sort |
  uniq -c |
  sort -rn |
  head -n 5
```

작동:
- 각 도구가 *입력 → 출력*
- pipe (`|`) 로 *streaming*
- 각 도구는 *작고, 한 가지만 잘함*

### 1.2 Unix 의 *철학*

> *Make each program do one thing well.*
> *Expect the output of every program to become the input to another.*

특징:
- *Uniform interface* — stdin / stdout, byte sequence
- *Composition* — pipe 로 chaining
- *Files 가 일급 객체* — log 도, config 도 다 file
- *Transformation* — input 안 바꾸고 새 output

이게 *MapReduce 의 영감*.

---

## 2. MapReduce — Google 2004

### 2.1 모델

```python
# Map: input record → (key, value) 다수 emit
def map(record):
    for word in record.split():
        emit(word, 1)

# Shuffle (framework): 같은 key 의 value 모음
# {hello: [1, 1, 1], world: [1, 1]}

# Reduce: (key, values) → 최종 결과
def reduce(key, values):
    emit(key, sum(values))
```

전형 — *word count*. 모든 batch problem 의 *hello world*.

### 2.2 데이터 흐름

![Figure 10-1 — MapReduce 의 mapper + shuffle + reducer. 책 p.401](/courses/ddia/figures/ch10/fig-10-1.png)

1. **Input** — HDFS / S3 의 file 들. partition 별
2. **Map task** — 각 input partition 하나당 mapper 하나. 같은 machine 에서 (data locality)
3. **Shuffle** — mapper 의 output 을 *key 별로 sort* + *같은 key 같은 reducer*
4. **Reduce task** — 각 key 의 모든 value 처리
5. **Output** — HDFS 의 새 file

### 2.3 핵심 통찰

- **Sort-merge** based shuffle — 5장의 LSM-tree merge 와 같은 아이디어
- **Data locality** — mapper 가 *데이터 있는 node* 에서. network 절감
- **Fault tolerance** — task 실패 시 *재실행* (input 이 immutable 이라 OK)

### 2.4 MapReduce 의 한계

- *Materialize between stages* — mapper output 을 *디스크에 저장* 후 reducer 로. **slow**
- *Map + Reduce 만 표현* — 복잡한 workflow 는 *여러 MR job chaining*
- *Iterative algorithm 어색* — graph, ML 의 매 iteration 이 새 job

→ 다음 세대 engine 으로 진화.

---

## 3. Joining in MapReduce

### 3.1 Sort-Merge Join (Reduce-side)

두 input dataset 을 *같은 key* 로 join:

1. **Map**: 두 dataset 모두 *같은 key* emit
2. **Shuffle**: 같은 key 의 record 모두 같은 reducer 로
3. **Reduce**: 같은 key 의 *두 dataset record* 결합

장점: 임의 dataset size OK.
단점: 모든 데이터가 *shuffle 거침* → 비쌈.

![Figure 10-2 — Reduce-side join. 책 p.405](/courses/ddia/figures/ch10/fig-10-2.png)

### 3.2 Broadcast Hash Join (Map-side)

작은 dataset 을 *모든 mapper 에 broadcast*. mapper 가 큰 dataset 의 각 record 와 join.

장점: *shuffle 없음* — 매우 빠름.
조건: 작은 dataset 이 *메모리* 에 들어가야.

### 3.3 Partitioned Hash Join

두 dataset 이 *같은 partition 함수* 로 분할되어 있으면 — 같은 partition 끼리만 join.

---

## 4. MapReduce 후속 — Dataflow Engines

### 4.1 동기

MR 의 한계:
- *Stage 간 materialization* 으로 느림
- *Iterative algorithm* 비효율
- *복잡한 workflow* 가 *MR job sequence* 로 표현

해결 — **Dataflow engines**:
- **Spark** (Berkeley AMPLab, 2010) — *in-memory* 처리, RDD/Dataset API
- **Tez** (Hortonworks) — DAG 기반 execution. Hive query engine.
- **Flink batch** — stream + batch unified

### 4.2 Spark 의 RDD

> **Resilient Distributed Dataset** — *immutable partitioned collection*. transformation 으로 새 RDD 생성.

```python
text = sc.textFile("s3://bucket/data")
words = text.flatMap(lambda line: line.split())
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("s3://bucket/output")
```

특징:
- **Lazy evaluation** — `saveAsTextFile` 호출 시에만 실행
- **DAG of transformation** — 실제 실행 전 *최적화*
- **In-memory caching** — `cache()`, `persist()`
- **Lineage** — fault tolerance. 잃은 partition 을 *transformation 다시 실행* 으로 복구

### 4.3 *Higher-level abstraction*

- **Hive**: SQL on Hadoop. MR 또는 Tez 백엔드
- **Pig**: dataflow scripting
- **Spark SQL / DataFrame**: structured data + SQL
- **Cascading, Crunch**: Java DSL

이게 *현대 batch 의 표준*. 대부분 직접 MR/Spark API 보다 *Hive/Spark SQL* 사용.

---

## 5. Graph Processing — Pregel

### 5.1 동기

PageRank, shortest path 같은 *graph algorithm* 은 MapReduce 로 *비효율* — 매 iteration 이 새 MR job.

### 5.2 Pregel 모델 — Bulk Synchronous Parallel (BSP)

> "**Think like a vertex**". 각 vertex 가 *작은 process*. *Super-step* 마다 메시지 교환.

```
each super-step:
  for each vertex (in parallel):
    process incoming messages
    update local state
    send messages to neighbors
  barrier — wait for all vertices
```

장점:
- *Iterative algorithm 자연*
- *Message-passing* 직관적
- Apache **Giraph**, **GraphX** (Spark) 가 구현

---

## 6. Batch 의 *철학*

### 6.1 Input 의 *immutability*

> Input file 은 *절대 수정 안 함*. 출력은 *새 file* 로.

이점:
1. **Fault tolerance** — task 재실행이 *항상 같은 결과*
2. **Debug 가능** — 옛 input 으로 다시 실행, 비교 가능
3. **Idempotency** — *부분 실패 후 재실행* 안전

### 6.2 Deterministic transformation

- *non-determinism 회피* — NOW(), RAND() 등 사용 시 *재실행 결과 다름*
- *순서 의존* 회피 — set 처럼 *순서 무관* 한 op 위주
- *외부 state 호출 회피* — RPC, DB 조회는 batch 에 부적합

### 6.3 Failure 처리

batch job 의 일부 task 실패 → *그 task 만 재실행*. immutable input + deterministic transformation 이라 *전체 다시* 안 해도 OK.

> **함정 1**: deterministic 가정이 깨지면 *재실행이 다른 결과* — fault tolerance 깨짐. 코드 작성 시 *purity* 의식.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | MapReduce 가 *모든 problem* 해결 | iterative, complex workflow 엔 비효율. Spark/Flink 가 진화 |
| 2 | Shuffle 이 *공짜* | 모든 데이터의 *network 이동 + sort*. 가장 비쌈 |
| 3 | broadcast join 이 *항상 빠름* | broadcast dataset 이 *메모리* 에 들어가야. 큰 dataset 엔 OOM |
| 4 | Spark 의 *모든 게 메모리* | shuffle, spill 시 디스크. memory 부족하면 disk overflow |
| 5 | non-deterministic 의 batch 사용 | NOW(), RAND() 가 fault tolerance 깨뜨림 |
| 6 | Batch job 안 RPC 호출 | external dependency 의 *비결정성*. cache 또는 *별도 stage* |
| 7 | Output 도 *append* 로 update | batch 는 *새 output file*. 옛 것 옆에. mutability 회피 |
| 8 | Hive 가 *real-time query* | 분 단위 latency. real-time 은 Presto/Trino/ClickHouse |
| 9 | Graph 도 그냥 MapReduce | iterative 비효율. Pregel / GraphX 사용 |
| 10 | Batch 의 *exactly-once* 어려움 | input immutable + deterministic 으로 *자동 보장* — 같은 결과 |

---

## 자가점검

1. Unix philosophy 의 3 가지 원칙.
2. MapReduce 의 *3 phase* + 각 역할.
3. *Reduce-side* vs *map-side* join 의 trade-off.
4. *Broadcast hash join* 의 조건.
5. *Spark RDD* 의 *3 가지 핵심 특성*.
6. *Lazy evaluation* 이 *왜 중요*.
7. *Pregel* 의 BSP 모델.
8. *Immutability of input* 의 3 가지 이점.

### 해답 (간략)

1. (1) do one thing well (2) output 이 다른 입력 (3) uniform interface (stdin/stdout, files).
2. Map (record → key-value), Shuffle (same key 모음), Reduce (key 의 values 처리).
3. Reduce-side: 모든 데이터 shuffle, 임의 size OK. Map-side: shuffle 없음, broadcast 가능한 작은 size 만.
4. Broadcast dataset 이 *모든 mapper 의 메모리* 에 들어가야.
5. (1) immutable (2) partitioned (3) lineage (fault tolerance).
6. *DAG 최적화* 가능 (predicate pushdown, projection pruning, plan rewrite). 또한 *unused transformation* 안 실행.
7. 각 vertex 가 superstep 마다 message 받음 + state 갱신 + neighbor 에 message. barrier 후 다음 superstep.
8. (1) fault tolerance (재실행 안전) (2) debug 가능 (3) idempotency (부분 실패 OK).

---

## 다음 학습으로

- **11장 (Stream)** — batch 의 *continuous* 버전. Kafka + Flink/Spark Streaming
- **12장 (Future)** — *unbundled DB* — batch + stream + storage 의 통합
