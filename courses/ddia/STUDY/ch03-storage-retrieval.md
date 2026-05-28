# Chapter 3: Storage and Retrieval — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 3** (책 p.69~112, PDF p.91~132).
> 3장은 DB 엔진의 *내부 구조*. **Log-structured (LSM-tree)** vs **B-tree** — 2가지 dominant storage 엔진. 그리고 OLTP vs OLAP — *transactional* 과 *analytical* 의 분기.

이 장의 *지적 무게중심*:
1. **Append-only log 의 단순함** — 그 위에 *모든 storage engine* 이 세워짐
2. **LSM-tree** vs **B-tree** — write-heavy vs read-heavy 의 *2 가지 답*
3. **Bloom filter, WAL, compaction** — storage engine 의 *공통 도구*
4. **OLTP vs OLAP** — workload 가 *storage 를 결정*
5. **Column-oriented storage** — analytics 의 *physics-based optimization*

---

## 들어가기 전에

- **선수 지식**: 자료구조 (hash table, B-tree), 디스크 vs 메모리 cost, sequential vs random I/O
- **학습 목표**
  1. *단순한 hash index* 부터 LSM-tree 의 진화
  2. **LSM-tree** (Cassandra, RocksDB, LevelDB) — write 최적화
  3. **B-tree** (Postgres, MySQL InnoDB) — read 최적화, 표준 RDBMS
  4. **Secondary index**, **multi-column index**, **full-text**, **fuzzy** 의 색인 패턴
  5. **In-memory DB** (Redis, Memcached) — 메모리가 *충분히 싸진* 시대
  6. **OLTP** (transactional) vs **OLAP** (analytical) — *완전 다른 workload + storage engine*
  7. **Column-oriented storage** + **compression** — analytics 의 핵심 기술
- **예상 학습 시간**: 150~200분

---

## §1 가장 단순한 DB — append-only log

```bash
db_set() {
  echo "$1,$2" >> database
}
db_get() {
  grep "^$1," database | sed 's/^[^,]*,//' | tail -n 1
}
```

- **Write**: append → *O(1)*, super fast
- **Read**: grep 전체 → *O(n)*, super slow

> 이게 *log-structured* 의 원형. write 는 빠르고 read 는 느림.

### §1.1 핵심 개념: **log**

> Log = *append-only sequence of records*.

DB 의 *모든* storage engine 은 어떤 형태로든 log 를 사용:
- *Write-ahead log* (B-tree 의 WAL)
- *SSTable* (LSM 의 sorted segment)
- *Transaction log*
- *Replication log* (5장)
- *Event log* (11장 Kafka)

### §1.2 *왜* log 가 빠른가 — 디스크의 물리

| | Sequential I/O | Random I/O |
|--|--|--|
| HDD | ~100 MB/s | ~1 MB/s (100x 차이) |
| SSD (SATA) | ~500 MB/s | ~50 MB/s (10x 차이) |
| NVMe SSD | ~3000 MB/s | ~500 MB/s (6x 차이) |

→ Sequential I/O 가 *수~수십배* 빠름. Append-only = sequential. *Storage engine 의 근본 설계 원리*.

---

## §2 Hash Index

read 를 빠르게 — *in-memory hash map* 으로 key → file offset 매핑:

```python
{key: offset_in_log}  # in-memory
```

- Write: log 에 append + hash map update
- Read: hash map 조회 → offset 으로 파일 seek

**Bitcask** (Riak 의 default storage engine) 가 이 방식. 100k+ writes/sec, key 가 *메모리에 다 들어가는* 한.

### §2.1 Bitcask 의 *실제 architecture*

**Files**:
- *Active file* — 현재 append 중인 segment
- *Older files* — 닫힌 segment (compaction 대상)
- *Hint file* — 각 segment 의 key → offset 매핑 (memory 재구성 빠르게)

**Restart 시**:
- Hint file 로 *빠른 startup*
- Hint 없으면 *모든 segment scan* — 큰 dataset 에 분 단위

### §2.2 한계

1. **모든 key 가 메모리에 들어가야** — key 가 많으면 못 씀
2. **Range query 불가** — hash 라 정렬 안 됨
3. **Log 가 무한 성장** — *compaction* 필요 (옛 update 삭제, 최신만 남김)

![Figure 3-2 — 압축 후의 segment: 같은 key 의 옛 value 제거. 책 p.74](/courses/ddia/figures/ch03/fig-3-2.png)

### §2.3 Segment + Compaction

log 를 *고정 크기 segment* 로 나누고, segment 가 full 이면 새 segment. 백그라운드에서 *compaction* — 여러 segment 를 합치며 같은 key 의 *최신 값만* 남김.

**Compaction 의 동시성 문제**:
- 옛 segment 의 read 가 진행 중인 동안 *delete 안 됨*
- *Reference counting* 또는 *garbage collection* 패턴
- *Lock-free* 구현이 표준

---

## §3 SSTable + LSM-Tree

### §3.1 SSTable — *Sorted String Table*

log segment 안의 key 들을 *정렬* 해서 저장:

장점:
1. **Merge 가 mergesort 처럼 효율적** — 정렬된 segment 들을 *streaming merge*
2. **In-memory index 가 sparse 해도 됨** — 모든 key 가 아닌 *일부* (e.g., 1000개에 하나) 만 가져도 binary search 비슷하게 찾음
3. **Block 단위 compression** — 정렬된 인접 key 들이 *비슷한 prefix* → 압축률 높음

![Figure 3-4 — Sparse index + block compression 의 SSTable. 책 p.77](/courses/ddia/figures/ch03/fig-3-4.png)

### §3.2 LSM-Tree 의 동작

> **Log-Structured Merge-Tree** (O'Neil 1996, Patrick O'Neil et al.).

쓰기 path:
1. **Memtable** (in-memory sorted, balanced BST 또는 skip list) 에 write
2. memtable 크기 임계값 도달 → *disk 의 새 SSTable segment* 로 flush
3. 백그라운드 *compaction* 으로 segment 병합

읽기 path:
1. Memtable 조회
2. 없으면 *가장 최근 SSTable* 부터 차례로
3. *Bloom filter* 로 "이 segment 에 key 가 있나?" 빠르게 negative test

![Figure 3-3 — LSM-tree 의 memtable + SSTable + compaction. 책 p.78](/courses/ddia/figures/ch03/fig-3-3.png)

### §3.3 Compaction 전략

**Size-tiered** (Cassandra default):
- 비슷한 크기의 SSTable 끼리 병합
- *Write amplification 낮음*, *space amplification 높음*

**Leveled** (LevelDB, RocksDB):
- *Level 0, 1, 2, ...* — level 마다 10x 크기
- 각 level 의 *key range overlap 없음*
- *Read amplification 낮음*, *write amplification 높음*

| | Size-tiered | Leveled |
|--|--|--|
| Write amplification | 낮음 (4~10x) | 높음 (15~30x) |
| Read amplification | 높음 | 낮음 |
| Space amplification | 높음 | 낮음 (~1.1x) |
| 적합 workload | Write-heavy | Read-heavy or balanced |

### §3.4 LSM-tree 구현 예

| 시스템 | 비고 |
|--|--|
| **LevelDB** | Google, 단일 process |
| **RocksDB** | Facebook fork, 모든 modern KV |
| **Cassandra** | NoSQL DB, size-tiered |
| **HBase** | Hadoop 의 KV store |
| **ScyllaDB** | C++ Cassandra, ~10x 빠름 |
| **Lucene** (Elasticsearch) | 검색 인덱스 |
| **MongoDB WiredTiger** | LSM 옵션 |
| **TiKV** | CockroachDB, RocksDB 기반 |

### §3.5 LSM-tree 의 trade-off

장점:
- **Write throughput 매우 높음** — sequential write only
- **Compression 잘 됨** — 정렬된 segment
- **공간 효율** — fragmentation 적음

단점:
- **Read amplification** — 한 read 가 여러 SSTable 조회
- **Write amplification** — 같은 데이터가 compaction 으로 여러 번 다시 쓰임
- **Compaction stall** — 큰 compaction 진행 중 throughput dip

> **함정 1**: write throughput 만 보고 LSM 선택했다가 *tail latency* 가 spike. Compaction tuning 이 운영의 핵심.

### §3.6 Bloom filter 의 원리

**문제**: LSM-tree 의 read 가 *모든 SSTable 조회* 필요. Key 가 *없는* SSTable 도 disk seek.

**Bloom filter**:
- *Bit array* (예: 10x key 수)
- 각 key 가 *k 개 hash function* 으로 *k 개 bit* 설정
- Query: k bit 모두 1? Yes → *probably present*. No → *definitely absent*

**특성**:
- *False positive 가능*
- *False negative 없음*
- 1% false positive rate → 약 10 bit/key

---

## §4 B-Tree

### §4.1 구조

RDBMS 의 *de facto* 표준 (1970년대 이후). 정렬된 key 를 *고정 크기 page* (보통 4KB) 의 *tree* 로:

- **Root** → branching pages → leaf pages
- 각 page 가 *child page reference* 또는 *key-value*
- **Branching factor** (한 page 의 children 수) 가 보통 *수백*

depth = log_B(N). 4 level B-tree 가 *256 TB* 까지 수용 (B=500, page=4KB).

![Figure 3-6 — B-tree 구조. 책 p.81](/courses/ddia/figures/ch03/fig-3-6.png)

### §4.2 Update — In-place

LSM 과 다르게 *기존 page 를 수정*. 같은 자리에 새 값 덮어쓰기.

**Page split** (key 가 page 에 안 들어갈 때):
- Page 를 *2 개로 나눔*
- *부모 page 도 update*
- *최악* — root 까지 split propagate

**문제**:
- Page split 가 *여러 page 동시 수정* → crash 시 *부분 update*

**해결 — Write-Ahead Log (WAL)**:
- 모든 modification 을 *먼저* append-only log 에 기록
- 그 다음 실제 page 수정
- Crash 시 WAL 로 *재실행*

> WAL 이 *B-tree 의 log-structured 부분*. 결국 모든 storage engine 은 log 를 씀.

### §4.3 Concurrency

여러 thread 가 동시 수정 → *latches* (lightweight lock) 로 보호.

**Latch 종류**:
- *Read latch* — shared
- *Write latch* — exclusive

**Lock coupling**:
- Tree 따라 내려갈 때 *부모 latch 의 child latch 획득 후 부모 release*
- *Deadlock 회피*

### §4.4 B-tree 변종

| | 특징 | 예 |
|--|--|--|
| B+-tree | leaf 만 data, internal = key only. Range scan 빠름 | Postgres, MySQL InnoDB |
| B*-tree | Page utilization ↑ (2/3 minimum) | 일부 commercial DB |
| Fractal tree | Buffered B-tree, write 빠름 | TokuDB |
| Copy-on-Write B-tree | Page 수정 시 새 copy. Snapshot 자연 | LMDB, BoltDB |

### §4.5 B-tree vs LSM 비교

| 측면 | B-tree | LSM-tree |
|--|--|--|
| Write | random I/O | sequential I/O |
| Read | 빠름 (한 path) | 느림 (여러 SSTable) |
| Write amp | 1~2x | 2~30x |
| Read amp | ~log(N) | 더 큼 |
| Space | fragmentation 가능 | 압축 우수 |
| Concurrency | latch, complex | append, 단순 |
| Predictable latency | 보통 | Compaction spike |
| 대표 | Postgres, MySQL InnoDB | Cassandra, RocksDB |

> 결정 가이드: **read-heavy** → B-tree. **write-heavy + 거대한 dataset** → LSM-tree.

### §4.6 InnoDB 의 *clustered primary key*

MySQL InnoDB 의 *기본 구조*:
- *Primary key 의 B+-tree 자체 가 row data*
- *Secondary index* 는 *(secondary key) → primary key* 매핑
- → Secondary lookup 은 *2 tree* traversal

PostgreSQL 의 *non-clustered* — heap file 별도.

**시사**:
- Primary key 가 *짧을수록* → secondary index 가 *작아짐*
- *PK 선택* 이 *공간 효율 + 성능* 에 큰 영향

---

## §5 Index 변형들

### §5.1 Secondary Index

primary key 가 아닌 column 으로 검색:

```sql
CREATE INDEX idx_email ON users(email);
```

### §5.2 Heap File vs Clustered Index

| | Heap | Clustered |
|--|--|--|
| Data 위치 | 별도 heap | row 가 *index 안* |
| Insert | append heap, index 만 갱신 | tree 안 자리 찾아 insert |
| Update | 새 위치 OK | tree 안 reorganize |
| 대표 | PostgreSQL | MySQL InnoDB |

### §5.3 Multi-column Index

```sql
CREATE INDEX ON items(latitude, longitude);
```

**B-tree 의 multi-column** — *concatenated key* `(lat, lon)`:
- `WHERE lat = 37.5` — 효율적
- `WHERE lon = 127` — 비효율적 (full scan)
- `WHERE lat = 37.5 AND lon = 127` — 효율적

**2D 검색** — R-tree (PostGIS), geohash.

### §5.4 Full-text Search

- **Lucene** (Elasticsearch base): *term → posting list* 의 inverted index
- *Tokenization, stemming, fuzzy* 등의 preprocessing

**Inverted index 예**:
```
"hello" → [doc1:pos5, doc3:pos12, doc7:pos1]
"world" → [doc1:pos6, doc2:pos8]
"hello world" 검색 = posting list intersect
```

**Modern — vector search**:
- *Embedding* (sentence → 768-dim vector)
- *Approximate nearest neighbor* (HNSW, IVF)
- pgvector, Pinecone, Weaviate
- LLM era 의 *semantic search*

### §5.5 In-Memory DB

| | 특징 | 사용처 |
|--|--|--|
| Memcached | KV cache, no persistence | Hot cache |
| Redis | KV + data structure, persistence option | Session, queue, leaderboard |
| VoltDB | In-memory OLTP, ACID | High-throughput |
| SAP HANA | In-memory analytics + OLTP | Enterprise |
| MemSQL / SingleStore | HTAP, in-memory + disk | Real-time analytics |

장점 — *디스크 layout 신경 안 써도* 되어 *더 풍부한 data structure*.

trade-off — RAM 크기 한계, *durability* 위해 disk log 또는 replication 필요.

---

## §6 Transaction Processing vs Analytics

### §6.1 OLTP — Online Transaction Processing

| 특징 | 값 |
|--|--|
| Read pattern | small number of records by key |
| Write pattern | random-access, low-latency |
| Bottleneck | disk seek time |
| Data size | GB to TB |
| User | end user, web app |
| 예시 | 주문, 회원 가입, 결제 |
| Query latency | < 100 ms |

→ B-tree (Postgres, MySQL) 의 영역.

### §6.2 OLAP — Online Analytical Processing

| 특징 | 값 |
|--|--|
| Read pattern | aggregate over millions |
| Write pattern | bulk import (ETL) |
| Bottleneck | disk bandwidth |
| Data size | TB to PB |
| User | analyst, dashboard |
| 예시 | "지난달 매출 top 10" |
| Query latency | 수 초 ~ 수 분 |

→ *column-oriented* + *data warehouse*.

### §6.3 Data Warehouse — *별도의 분석용 DB*

ETL 로 OLTP → warehouse:
- OLTP 쿼리에 *영향 없음*
- *Star/snowflake schema* 로 최적화
- 다양한 source 통합

![Figure 3-9 — Star schema. 책 p.94](/courses/ddia/figures/ch03/fig-3-9.png)

**Star schema**:
- *Fact table* (큰, narrow)
- *Dimension tables* (작은, wide)
- *JOIN* — fact ↔ dimension

### §6.4 Modern data stack

**ETL → ELT**:
- 전통 ETL: source → transform → warehouse
- 현대 ELT: source → warehouse → *SQL transform* (dbt)

**Data Lakehouse** (2020s):
- Data lake (object storage, raw, schema-on-read)
- + Warehouse (column, SQL)
- = Lakehouse
- **Apache Iceberg, Delta Lake, Hudi** — table format
- Databricks, Snowflake 의 표준

---

## §7 Column-Oriented Storage

### §7.1 동기

OLAP query 는 *수십 column 중 3~5 만 사용*. row-oriented 는 *모든 column 을 읽음* → 낭비.

```
row-oriented:
  Row 1: [id=1, name="A", price=100, ...]

column-oriented:
  id:    [1, 2, 3, 4, ...]
  name:  ["A", "B", "C", "D", ...]
  price: [100, 200, 300, 400, ...]
```

→ 필요한 column 만 읽기. *bandwidth 효율 압도*.

### §7.2 Column Compression

같은 column 의 값은 *비슷한 패턴* — 압축률 매우 좋음:

- **Bitmap encoding** — 가능 value 가 적을 때
- **Run-length encoding (RLE)** — 같은 값 반복
- **Delta encoding** — 정렬된 숫자의 차이
- **Dictionary encoding** — 문자열 → 정수

압축 후 *CPU vectorized 처리* (SIMD) 까지 가능 — 10~100x 빠른 scan.

### §7.3 Vectorized Execution

전통 — *row by row*:
```c
for (row in rows) if (row.price > 100) count++;
```

**Vectorized** — *batch by batch*:
```c
__m256i prices = _mm256_load_si256(prices_array);
__m256i mask = _mm256_cmpgt_epi32(prices, threshold);
count += _mm256_popcnt(mask);
```

- AVX2: 한 instruction 으로 *8 값* 처리
- *Cache miss 줄임*
- *10~50x speedup*

**산업** — ClickHouse, DuckDB, Apache Arrow.

### §7.4 Sort Order in Column

*Primary sort key* 로 정렬 → range query 의 *block skip*.

### §7.5 Materialized Views & Cubes

```sql
CREATE MATERIALIZED VIEW daily_sales AS
SELECT date, product_id, SUM(amount) AS total
FROM orders GROUP BY date, product_id;
```

**OLAP cube** — *다차원 pre-aggregated*. drill-down 매우 빠름.

> **함정 2**: warehouse 에 column store 채택했다고 *모든 query 가 빨라지지 않음*. 적합한 schema + sort order + materialized view 까지.

### §7.6 산업의 column store

| 시스템 | 특징 |
|--|--|
| C-Store / Vertica | 학술 → 상용 |
| Apache Parquet | 파일 포맷, Hadoop 생태계 |
| Apache ORC | 또 다른 column file |
| ClickHouse | OSS, 빠른 OLAP |
| DuckDB | Embedded analytics |
| BigQuery | Google, serverless |
| Snowflake | Cloud-native |
| Redshift | AWS |
| Druid / Pinot | Real-time OLAP |

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "LSM 이 write 빠르다" 만 보고 | tail latency, compaction stall, write amp |
| 2 | B-tree 가 무조건 reliable | WAL crash recovery 필요 |
| 3 | Index 많이 = 좋다 | write 마다 모든 index 갱신 |
| 4 | Hash index = HashMap = O(1) | 모든 key 가 메모리 필요 |
| 5 | OLTP + OLAP 같은 DB | resource contention. 별도 warehouse 표준 |
| 6 | Column store 항상 빠름 | OLTP 의 row insert/update 는 *심각하게 느림* |
| 7 | Materialized view 항상 빠름 | 갱신 비용 + staleness |
| 8 | Bloom filter false negative 없음 | false positive 가능 — *negative test* 만 |
| 9 | In-memory = no durability | replication + WAL 로 durable |
| 10 | Full-text = LIKE | tokenization, stemming, ranking 등 전혀 다른 문제 |
| 11 | Compaction default OK | 큰 dataset 에 size-tiered vs leveled 큰 차이 |
| 12 | Clustered index 항상 좋음 | Wide row 시 secondary index 도 큼 |

---

## §9 자가점검

1. *Log* 의 정의 + 모든 storage engine 에서 어떤 역할?
2. *Hash index* 의 한계 3가지?
3. *SSTable* 의 3 가지 이점?
4. *LSM-tree* 의 write path 흐름?
5. *Bloom filter* 가 LSM-tree read 를 어떻게 가속?
6. *B-tree* 의 *WAL* 이 왜 필요?
7. *Write amp* vs *read amp* 정의 + 두 engine 의 값?
8. *OLTP vs OLAP* 의 핵심 차이 3가지?
9. *Column-oriented* 의 OLAP 우월성 이유?
10. *Materialized view* 와 *OLAP cube* 의 trade-off?
11. *Size-tiered* vs *leveled* compaction?
12. *Vectorized execution* 의 SIMD 활용?

<details><summary>해답 (간략)</summary>

1. Append-only sequence. LSM SSTable, B-tree WAL, transaction log 등.
2. (1) key 가 메모리 한계 (2) range query 불가 (3) log 무한 성장.
3. (1) merge mergesort (2) sparse index (3) block compression.
4. write → memtable → 임계값 → SSTable flush → background compaction.
5. "이 SSTable 에 key 없다" 를 *false positive 가능, false negative 없음* 으로 빠르게 negative test.
6. page split 가 여러 page 동시 수정 → crash 시 partial update. WAL 로 재실행.
7. Write amp = 한 write 가 몇 번 디스크. Read amp = 한 read 가 몇 번 seek. B-tree: w 1~2x, r log(N). LSM: w 2~30x, r 더 큼.
8. workload (key vs scan), bottleneck (seek vs bandwidth), layout (row vs column).
9. 몇 column 만 읽음 → bandwidth 효율. 압축률 좋음. SIMD scan 가능.
10. MV: pre-compute, 빠르지만 갱신 비용 + staleness. Cube: 다차원, drill-down 빠름, 공간 ↑↑.
11. Size-tiered (Cassandra): 비슷한 크기 병합, write amp 낮음, space amp 높음. Leveled (RocksDB): level 마다 10x, read amp 낮음, write amp 높음.
12. SIMD = Single Instruction Multiple Data. AVX2 256-bit = 8 int. 한 instruction 으로 8 값 처리. 10~50x speedup.

</details>

---

## §10 다음 학습으로

- **4장 (Encoding and Evolution)** — schema migration, 데이터 *직렬화* (JSON, Avro, Protobuf).
- **5~6장** — replication 과 partitioning 의 *physical storage* 위에서 동작.
- **10장 (Batch Processing)** — MapReduce, Spark — column store 의 분산 버전.
- **11장 (Stream Processing)** — log 가 *event stream* 으로 진화. Kafka.

---

## §11 한 줄 요약

> **Storage engine 의 *근본 = append-only log*. LSM-tree (write-heavy) vs B-tree (read-heavy) 의 두 답. Bloom filter + compaction + WAL 의 공통 도구. OLTP (row, B-tree) vs OLAP (column, vectorized) 의 *완전 다른 workload*. Modern = column store + vectorized + cloud (BigQuery, Snowflake, ClickHouse).**
