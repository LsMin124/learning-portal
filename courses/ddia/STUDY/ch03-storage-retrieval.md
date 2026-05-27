# Chapter 3: Storage and Retrieval — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 3** (책 p.69~112, PDF p.91~132).
> 3장은 DB 엔진의 *내부 구조*. **Log-structured (LSM-tree)** vs **B-tree** — 2가지 dominant storage 엔진. 그리고 OLTP vs OLAP — *transactional* 과 *analytical* 의 분기.

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

## 1. 가장 단순한 DB — append-only log

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

### 핵심 개념: **log**

> Log = *append-only sequence of records*.

DB 의 *모든* storage engine 은 어떤 형태로든 log 를 사용. *write-ahead log* (B-tree 의 WAL), *SSTable* (LSM 의 sorted segment), *transaction log* 등.

---

## 2. Hash Index

read 를 빠르게 — *in-memory hash map* 으로 key → file offset 매핑:

```python
{key: offset_in_log}  # in-memory
```

- Write: log 에 append + hash map update
- Read: hash map 조회 → offset 으로 파일 seek

**Bitcask** (Riak 의 default storage engine) 가 이 방식. 100k+ writes/sec, key 가 *메모리에 다 들어가는* 한.

### 한계

1. **모든 key 가 메모리에 들어가야** — key 가 많으면 못 씀
2. **Range query 불가** — hash 라 정렬 안 됨
3. **Log 가 무한 성장** — *compaction* 필요 (옛 update 삭제, 최신만 남김)

![Figure 3-2 — 압축 후의 segment: 같은 key 의 옛 value 제거. 책 p.74](/courses/ddia/figures/ch03/fig-3-2.png)

### Segment + Compaction

log 를 *고정 크기 segment* 로 나누고, segment 가 full 이면 새 segment. 백그라운드에서 *compaction* — 여러 segment 를 합치며 같은 key 의 *최신 값만* 남김.

---

## 3. SSTable + LSM-Tree

### 3.1 SSTable — *Sorted String Table*

log segment 안의 key 들을 *정렬* 해서 저장:

장점:
1. **Merge 가 mergesort 처럼 효율적** — 정렬된 segment 들을 *streaming merge*
2. **In-memory index 가 sparse 해도 됨** — 모든 key 가 아닌 *일부* (e.g., 1000개에 하나) 만 가져도 binary search 비슷하게 찾음
3. **Block 단위 compression** — 정렬된 인접 key 들이 *비슷한 prefix* → 압축률 높음

![Figure 3-4 — Sparse index + block compression 의 SSTable. 책 p.77](/courses/ddia/figures/ch03/fig-3-4.png)

### 3.2 LSM-Tree 의 동작

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

### 3.3 LSM-tree 구현 예

| 시스템 | 비고 |
|--|--|
| **LevelDB / RocksDB** | Google / Facebook 의 OSS engine |
| **Cassandra** | NoSQL DB |
| **HBase** | Hadoop 의 KV store |
| **Lucene** (Elasticsearch) | 검색 인덱스 |
| **MongoDB WiredTiger** | 옵션 |

### 3.4 LSM-tree 의 trade-off

장점:
- **Write throughput 매우 높음** — sequential write only
- **Compression 잘 됨** — 정렬된 segment
- **공간 효율** — fragmentation 적음

단점:
- **Read amplification** — 한 read 가 여러 SSTable 조회 (bloom filter 가 mitigate)
- **Write amplification** — 같은 데이터가 compaction 으로 여러 번 다시 쓰임
- **Compaction stall** — 큰 compaction 이 진행 중일 때 throughput dip

> **함정 1**: write throughput 만 보고 LSM 선택했다가 *tail latency* 가 spike. Compaction tuning 이 운영의 핵심.

---

## 4. B-Tree

### 4.1 구조

RDBMS 의 *de facto* 표준 (1970년대 이후). 정렬된 key 를 *고정 크기 page* (보통 4KB) 의 *tree* 로:

- **Root** → branching pages → leaf pages
- 각 page 가 *child page reference* 또는 *key-value*
- **Branching factor** (한 page 의 children 수) 가 보통 *수백*

depth = log_B(N). 4 level B-tree 가 *256 TB* 까지 수용 (B=500, page=4KB).

![Figure 3-6 — B-tree 구조. 책 p.81](/courses/ddia/figures/ch03/fig-3-6.png)

### 4.2 Update — In-place

LSM 과 다르게 *기존 page 를 수정*. 같은 자리에 새 값 덮어쓰기.

문제:
- Page split (insert) 가 *여러 page 동시 수정* → crash 시 *부분 update*

**해결 — Write-Ahead Log (WAL)**:
- 모든 modification 을 *먼저* append-only log 에 기록
- 그 다음 실제 page 수정
- Crash 시 WAL 로 *재실행*

> WAL 이 *B-tree 의 log-structured 부분*. 결국 모든 storage engine 은 log 를 씀.

### 4.3 Concurrency

여러 thread 가 동시 수정 → *latches* (lightweight lock) 로 보호. crash recovery 도 latch 와 함께.

### 4.4 B-tree vs LSM 비교

| 측면 | B-tree | LSM-tree |
|--|--|--|
| Write | random I/O (in-place update) | sequential I/O (append + flush) |
| Read | 빠름 (한 path) | 느림 (여러 SSTable) |
| Write amplification | 1~2x | 2~30x (compaction) |
| Read amplification | ~log(N) | 더 큼 |
| Space | fragmentation 가능 | 압축 우수 |
| Concurrency | latch, complex | append 만 → 단순 |
| 대표 | Postgres, MySQL InnoDB | Cassandra, RocksDB |

> 결정 가이드: **read-heavy** → B-tree. **write-heavy + 거대한 dataset** → LSM-tree.

---

## 5. Index 변형들

### 5.1 Secondary Index

primary key 가 아닌 column 으로 검색:

```sql
CREATE INDEX idx_email ON users(email);
```

- B-tree 가 *그 column → primary key* 매핑
- LSM 도 같은 구조

### 5.2 Heap File vs Clustered Index

| | Heap | Clustered |
|--|--|--|
| Data 위치 | 별도 heap, index 가 row pointer | row 가 *index 안* (Postgres 의 *non-clustered*, MySQL InnoDB 의 *clustered primary key*) |
| Insert | append heap, index 만 갱신 | tree 안 자리 찾아 insert |
| Update (size 변화) | 새 위치, index pointer 갱신 | tree 안 reorganize |

### 5.3 Multi-column Index

`CREATE INDEX ON items(latitude, longitude)` — 2D 좌표 검색에 *어색*. 진짜 2D 는 **R-tree** (PostGIS). 또는 **geohash** 같은 인코딩.

### 5.4 Full-text Search

- **Lucene** (Elasticsearch base): *term → posting list* 의 inverted index
- 각 단어가 *어느 document* 의 *어느 위치* 에 있는지
- *Tokenization, stemming, fuzzy* 등의 preprocessing

### 5.5 In-Memory DB

> "디스크가 비싸서 인-메모리는 못 했다" 는 *과거*. 메모리 가격 ↓ → **in-memory** DB 가 주류:

- **Memcached / Redis** — KV cache (Redis 는 persistence 옵션)
- **VoltDB / MemSQL** — in-memory OLTP
- **SAP HANA** — in-memory analytics

장점 — *디스크 layout 신경 안 써도* 되어 *더 풍부한 data structure* (priority queue, sorted set, geo).

trade-off — RAM 크기 한계, *durability* 위해 disk log 또는 replication 필요.

---

## 6. Transaction Processing vs Analytics

> 같은 SQL DB 라도 *완전 다른 workload* — 다른 storage engine 이 적합.

### 6.1 OLTP — Online Transaction Processing

| 특징 | 값 |
|--|--|
| Read pattern | small number of records, fetched by key |
| Write pattern | random-access, low-latency |
| Bottleneck | disk seek time |
| Data size | GB to TB |
| User | end user, web app |
| 예시 | 주문 입력, 회원 가입, 결제 |

→ B-tree (Postgres, MySQL) 의 영역.

### 6.2 OLAP — Online Analytical Processing

| 특징 | 값 |
|--|--|
| Read pattern | aggregate over millions of records |
| Write pattern | bulk import (ETL) |
| Bottleneck | disk bandwidth |
| Data size | TB to PB |
| User | analyst, dashboard |
| 예시 | "지난달 매출이 가장 많은 상품 top 10" |

→ *column-oriented* + *data warehouse* (BigQuery, Snowflake, Redshift, Vertica).

### 6.3 Data Warehouse — *별도의 분석용 DB*

OLTP DB 에서 *ETL* (Extract-Transform-Load) 로 데이터를 warehouse 로 옮김. 이유:
- OLTP 쿼리에 *영향 없음* (full-table scan 이 OLTP latency 죽임)
- Warehouse 가 *분석 schema* (star schema, snowflake) 로 *최적화*
- 다양한 source 통합 → *unified view*

![Figure 3-9 — Star schema: fact table + dimension tables. 책 p.94](/courses/ddia/figures/ch03/fig-3-9.png)

---

## 7. Column-Oriented Storage

### 7.1 동기

OLAP query 는 보통 *수십 column 중 3~5 만 사용*. row-oriented 는 *모든 column 을 디스크에서 읽음* → 낭비.

**column-oriented**: 각 column 을 *별도 파일* 로 저장.

```
row-oriented:
  Row 1: [id=1, name="A", price=100, ...]
  Row 2: [id=2, name="B", price=200, ...]

column-oriented:
  id:    [1, 2, 3, 4, ...]
  name:  ["A", "B", "C", "D", ...]
  price: [100, 200, 300, 400, ...]
```

→ 필요한 column 만 읽기. *bandwidth 효율 압도*.

### 7.2 Column Compression

같은 column 의 값은 *비슷한 패턴* — 압축률 매우 좋음:

- **Bitmap encoding** — 가능 value 가 적을 때 (성별, 카테고리)
- **Run-length encoding (RLE)** — 같은 값 반복
- **Delta encoding** — 정렬된 숫자의 *차이* 만 저장
- **Dictionary encoding** — 문자열 → 정수 매핑

압축 후 *CPU vectorized 처리* (SIMD) 까지 가능 — 10~100x 빠른 scan.

### 7.3 Sort Order in Column

*Primary sort key* 로 정렬 → range query 의 *block skip* 가능. *Secondary sort* 도 가능 (Vertica 의 multiple sort orders projection).

### 7.4 Materialized Views & Cubes

자주 사용하는 *집계 결과* 를 미리 계산:

```sql
CREATE MATERIALIZED VIEW daily_sales AS
SELECT date, product_id, SUM(amount) AS total
FROM orders GROUP BY date, product_id;
```

또는 **OLAP cube** — *다차원 pre-aggregated* (date × product × region 의 모든 cell). drill-down 매우 빠름.

> **함정 2**: warehouse 에 column store 채택했다고 *모든 query 가 빨라지지 않음*. *적합한 schema (star/snowflake)* + *sort order* + *materialized view* 까지 함께 설계.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "LSM 이 write 빠르다" 만 보고 채택 | tail latency, compaction stall, write amplification 트레이드오프 |
| 2 | B-tree 가 무조건 reliable | 같은 WAL crash recovery 가 필요. crash 시 *최근 commit* 복구 |
| 3 | Index 많이 만들면 좋다 | write 마다 모든 index 갱신. write cost ↑↑ |
| 4 | Hash index = HashMap = O(1) | 디스크 hash index 는 *모든 key 가 메모리* 필요. 큰 dataset 엔 부적합 |
| 5 | OLTP 와 OLAP 를 같은 DB 에 | resource contention. ETL → 별도 warehouse 가 표준 |
| 6 | Column store 가 row store 보다 *항상* 빠름 | OLTP 의 *전체 row insert/update* 엔 column store 가 *심각하게 느림* |
| 7 | Materialized view 가 항상 빠름 | 갱신 비용 + staleness. *자주 쓰는 query* 에만 |
| 8 | Bloom filter 가 *false negative* 없음 | false *positive* 가능. negative test 만 활용 |
| 9 | In-memory DB = no durability | replication + WAL 로 충분 durable |
| 10 | full-text search 가 단순 LIKE | tokenization, stemming, ranking 등 *전혀 다른 문제* |

---

## 자가점검

1. *Log* 의 정의 + 모든 storage engine 에서 *어떤 역할*.
2. *Hash index* 의 한계 *3가지*.
3. *SSTable* 의 *3 가지 이점* (정렬에서 오는).
4. *LSM-tree* 의 write path (memtable → SSTable → compaction) 흐름.
5. *Bloom filter* 가 LSM-tree 의 *read* 를 어떻게 가속.
6. *B-tree* 의 *write-ahead log* 가 *왜* 필요.
7. *Write amplification* vs *read amplification* 의 정의 + 두 engine 에서의 값.
8. *OLTP vs OLAP* 의 핵심 차이 (3가지).
9. *Column-oriented storage* 의 OLAP 우월성 이유.
10. *Materialized view* 와 *OLAP cube* 의 trade-off.

### 해답 (간략)

1. *Append-only sequence of records*. LSM 의 SSTable, B-tree 의 WAL, transaction log 등 모든 곳.
2. (1) key 가 메모리 한계 (2) range query 불가 (3) log 무한 성장 (compaction 필요).
3. (1) merge 가 mergesort (2) sparse in-memory index 가능 (3) block compression 우수.
4. write → memtable → 임계값 → SSTable flush → background compaction 으로 병합.
5. read 시 "이 SSTable 에 key 가 *없다*" 를 *false positive 가능, false negative 없음* 으로 빠르게 negative test.
6. page split, tree restructure 가 *여러 page 동시 수정* → crash 시 partial update. WAL 로 *재실행* 가능하게 함.
7. Write amp = 한 write 가 *몇 번 디스크에 쓰여지나*. Read amp = 한 read 가 *몇 번 disk seek*. B-tree: write 1~2x, read log(N). LSM: write 2~30x, read 더 큼.
8. (1) workload: many small key lookup vs few big scan. (2) bottleneck: seek time vs bandwidth. (3) data layout: row vs column.
9. OLAP 가 *몇 column 만* 읽으므로 column 별 저장이 bandwidth 효율. 추가로 같은 column 의 *압축률 매우 좋음*, *SIMD vectorized scan* 가능.
10. Materialized view: 쿼리 결과를 pre-compute. 빠르지만 갱신 비용 + staleness. *자주 쓰는 일부* 에만. Cube: 다차원 pre-aggregate. drill-down 빠름, 공간 ↑↑.

---

## 다음 학습으로

- **4장 (Encoding and Evolution)** — schema migration, 데이터 *직렬화* (JSON, Avro, Protobuf).
- **5~6장** — replication 과 partitioning 의 *physical storage* 위에서 동작.
- **10장 (Batch Processing)** — MapReduce, Spark — column store 의 분산 버전.
- **11장 (Stream Processing)** — log 가 *event stream* 으로 진화. Kafka 가 log 의 distributed 버전.
