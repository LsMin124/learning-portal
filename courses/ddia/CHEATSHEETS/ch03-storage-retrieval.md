# Ch 3 Storage and Retrieval — 치트시트

## TL;DR

- 모든 storage engine 은 *log* (append-only) 을 어떤 형태로든 사용
- **LSM-tree** (Cassandra, RocksDB): memtable → SSTable → compaction. write 빠름, read amp 큼 (bloom filter 로 mitigate)
- **B-tree** (Postgres, MySQL): in-place tree, WAL 로 crash recovery. read 빠름, write amp 작음
- 선택: **write-heavy + 큰 dataset → LSM**, **read-heavy + ACID → B-tree**
- **OLTP** (B-tree, row-oriented) vs **OLAP** (column-oriented, warehouse + ETL)
- **Column compression** (bitmap, RLE, delta, dictionary) + SIMD = 10~100x scan 속도
- **Materialized view** / cube: pre-aggregate for analytics. staleness trade-off

---

## Quick Reference

### 표 1. B-tree vs LSM-tree

| | B-tree | LSM-tree |
|--|--|--|
| Write | random in-place + WAL | sequential append + flush |
| Read | O(log N) one path | multiple SSTables + bloom |
| Write amp | 1~2x | 2~30x (compaction) |
| Read amp | log N | larger (bloom mitigates) |
| Space | fragmentation | compression-friendly |
| 대표 | Postgres, MySQL InnoDB | Cassandra, RocksDB, HBase |

### 표 2. Index 종류

| 종류 | 사용 |
|--|--|
| Hash index | in-memory KV (Bitcask, Redis) |
| B-tree | OLTP RDBMS 표준 |
| LSM-tree | NoSQL, time-series |
| R-tree | 2D 공간 (PostGIS) |
| Inverted index | full-text (Lucene/Elasticsearch) |
| BRIN | 큰 sequential data (Postgres) |
| Bitmap | low-cardinality column |

### 표 3. OLTP vs OLAP

| | OLTP | OLAP |
|--|--|--|
| Read | 소수 row, by key | aggregate over millions |
| Write | random, low-latency | bulk ETL |
| Bottleneck | seek time | bandwidth |
| Size | GB~TB | TB~PB |
| Engine | B-tree row-oriented | column-oriented warehouse |
| 사용자 | end user / web | analyst / dashboard |
| 예시 | 주문, 결제 | "지난달 top 10 상품" |

### 표 4. Column compression

| 기법 | 적합 |
|--|--|
| Bitmap | low-cardinality (성별, 카테고리) |
| RLE | run 많음 (정렬된 상태 변수) |
| Delta | 정렬된 숫자 |
| Dictionary | 문자열 → int 매핑 |

압축 + SIMD vectorized → row-oriented 대비 10~100x scan.

### 표 5. LSM-tree 동작

```
WRITE:
  1. memtable 에 insert (sorted, in-memory)
  2. memtable full → SSTable 로 flush (sorted, immutable)
  3. background compaction: SSTable 들 merge, 옛 update 제거

READ:
  1. memtable 조회
  2. bloom filter 로 SSTable negative test
  3. 통과한 SSTable 의 sparse index → block 읽기
  4. 가장 최근 SSTable 부터 차례로
```

### 표 6. B-tree 동작

```
WRITE:
  1. WAL 에 modification 기록 (append + fsync)
  2. tree page 수정 (in-place)
  3. page split 시 부모도 갱신
  4. crash recovery: WAL 의 unflushed entry redo

READ:
  1. root page 부터 branch traversal
  2. leaf page 도달
  3. binary search within page
```

### 표 7. Polyglot stack 예시

```
OLTP:     Postgres / MySQL  (row, B-tree)
Cache:    Redis             (in-memory, KV)
Search:   Elasticsearch     (LSM + inverted)
Logs:     Cassandra         (LSM)
Stream:   Kafka             (log)
Analytics: BigQuery / Snowflake  (column, MPP)
ML store: ParquetS3 + Trino  (column)
```

---

## Mind Map

```
3장 Storage and Retrieval
├─ 1. 최단순 DB: append-only log
├─ 2. Hash index (Bitcask)
│   └─ 한계: 메모리, range, 압축
├─ 3. SSTable + LSM-tree
│   ├─ memtable → SSTable → compaction
│   ├─ Bloom filter
│   └─ Cassandra, RocksDB, Lucene
├─ 4. B-tree
│   ├─ in-place + WAL
│   └─ Postgres, MySQL
├─ 5. Index 변형
│   ├─ Secondary, multi-column
│   ├─ R-tree, full-text, BRIN
│   └─ In-memory (Redis)
├─ 6. OLTP vs OLAP
│   ├─ workload, bottleneck 차이
│   └─ Data warehouse + ETL
└─ 7. Column-oriented
    ├─ column file 분리
    ├─ compression + SIMD
    └─ Materialized view, cube
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | log = 모든 storage engine 의 building block |
| 2 | hash index: O(1) read, key가 메모리 한계 |
| 3 | LSM: sequential write + bloom-filtered multi-SSTable read |
| 4 | B-tree: in-place + WAL, OLTP RDBMS 표준 |
| 5 | Index 종류는 use case 별. write cost vs read 가속 trade-off |
| 6 | OLTP vs OLAP 는 완전 다른 engine. ETL 로 분리 |
| 7 | column store + compression = analytics 의 핵심 |
