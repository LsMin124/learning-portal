# Ch 3 Storage and Retrieval — 퀴즈

> 12 문항.

### Q1. Append-only log 의 read 가 *왜* 느리나, 어떻게 개선?

<details><summary>답</summary>

**문제**: 파일 전체 scan (O(n)). N=10M 이면 매 read 가 *몇 초*.

**개선 단계**:
1. **In-memory hash index** (Bitcask) — key → file offset 매핑. read 가 O(1)
2. **SSTable + LSM-tree** — log 를 정렬된 segment 로. sparse index + bloom filter
3. **B-tree** — 정렬된 tree 로 random access O(log N)

각 단계가 *write 비용을 약간 늘리고 read 를 크게 가속*.

</details>

### Q2. SSTable 의 3 가지 이점

정렬에서 오는 *3 가지 구조적 이점* 각각의 *구체적 메커니즘*.

<details><summary>답</summary>

1. **Merge 의 효율** — 정렬된 segment N개의 merge 가 *mergesort* (linear scan). 메모리 안에 다 안 들어가도 *streaming* 가능.

2. **Sparse in-memory index** — 모든 key 가 아닌 *1000개에 하나* 만 메모리에 두면 됨. nearest 보다 작은 sparse entry → 해당 block 읽어 linear scan. ~1MB block 이라도 OS page cache 가 처리.

3. **Block compression** — 정렬된 인접 key 가 *prefix 비슷* → block 단위 zstd/snappy 압축률 5~10x. disk space + I/O bandwidth 모두 이득.

</details>

### Q3. LSM-tree 의 read amplification 측정

dataset 100GB, memtable 64MB, level 0=64MB×4=256MB, level 1=2.5GB, level 2=25GB, level 3=250GB. 한 key 의 worst-case read 시 *몇 SSTable* 조회?

<details><summary>답</summary>

**Worst case** — key 가 어디 있는지 모름 → 모든 level 조회:

- Memtable: 1
- Level 0: 4 (size-tiered, 4 overlapping segments)
- Level 1~3: 각 1 (leveled, non-overlapping)
- → **7 SSTable 조회**

**Bloom filter 효과**:
- 각 SSTable 의 bloom filter (~10bits/key) 가 *negative test* false positive 1%
- 실제 disk read 가 발생하는 SSTable = 1 (실제 있는 곳) + ~0.06 (1% × 6) ≈ **1.06**
- → 7배 amplification 이 *bloom filter 로 1배 가까이* 회복

운영 — bloom filter false positive rate 가 *read amp 의 결정 요인*. 비트 ↑ → 정확도 ↑ 메모리 ↑.

</details>

### Q4. B-tree 의 WAL crash recovery

B-tree page split 중 (즉, 새 page 할당 + 기존 page 의 절반을 새 page 로 이동 + 부모 page 의 child pointer 갱신) crash. WAL 없이는 어떻게 깨지나?

<details><summary>답</summary>

**WAL 없으면**:
- 새 page 할당 OK, 기존 page 절반 복사 OK
- 그러나 *부모 page 의 pointer 갱신 전* crash → 두 자식 page 가 *고아*
- 또는 *기존 page 의 자기 정리* 전 crash → 같은 key 가 *두 page 에 존재* (duplicate)
- 어떤 경우든 *tree invariant 깨짐* — recovery 불가, DB 손상

**WAL 로**:
1. modification 의 *redo log* (어떤 key 가 어디로 이동) 을 먼저 append + fsync
2. 실제 page 수정
3. Crash 후 startup: WAL 의 *마지막 commit 이후* entry 들을 *재실행*
4. WAL 의 entry 가 *idempotent* — 같은 redo 를 여러 번 실행해도 안전

이게 PostgreSQL 의 *wal_level=replica*, MySQL 의 *redo log* 의 동작.

</details>

### Q5. B-tree vs LSM 선택 — 시나리오별

각 시나리오에 적합한 엔진:

1. 페이스북 timeline (write-heavy, billions/day)
2. 은행 계좌 잔액 조회 (read 우선, ACID 필수)
3. IoT sensor 시계열 (write 폭주, range query 많음)
4. 검색 엔진 inverted index (write+read 균형, 큰 dataset)

<details><summary>답</summary>

1. **LSM-tree** (Cassandra, HBase). write throughput. timeline 의 일부 staleness 허용.
2. **B-tree** (PostgreSQL, Oracle). ACID, read latency 우선. 잔액은 *틀리면 안 됨*.
3. **LSM-tree** (Cassandra, InfluxDB). write 폭주 + sequential range (time series 정렬).
4. **LSM-tree** (Elasticsearch 의 Lucene). 둘 다 잘하지만 large dataset 에 LSM 우세 + compression.

핵심: *workload 의 read:write ratio* + *dataset size*. read-heavy + GB → B-tree. write-heavy 또는 TB+ → LSM.

</details>

### Q6. Index 많이 만들면 어떻게 *느려지는가*

테이블에 index 10개. INSERT 가 느림. 분석.

<details><summary>답</summary>

**원인**: 매 INSERT 가 *모든 index 갱신* 필요. 10개 index = *10번의 B-tree write*. + 모두 fsync (durability) → disk I/O 폭주.

**대응**:
1. **꼭 필요한 index 만** — `EXPLAIN ANALYZE` 로 *사용되지 않는 index* 식별 후 제거
2. **Partial index** — `WHERE active = true` 같은 조건으로 *일부 row 만* index
3. **Bulk insert** — 여러 row 를 transaction 으로 묶음. WAL 의 fsync 횟수 감소
4. **Index 비활성 후 일괄 빌드** — 큰 데이터 import 시 `DROP INDEX` → `INSERT` → `CREATE INDEX`. 마지막 build 는 *bulk* 라 빠름

원칙: index 는 *read 가속 vs write 감속* 의 trade-off. 측정 후 결정.

</details>

### Q7. Column-oriented vs Row-oriented 의 *workload 결정 기준*

같은 데이터 (orders 테이블, 1억 row, 50 column) 의 두 query 의 분석:

```sql
-- Q1
SELECT * FROM orders WHERE order_id = 12345;

-- Q2
SELECT product_id, SUM(amount) FROM orders
WHERE date >= '2025-01-01' GROUP BY product_id;
```

<details><summary>답</summary>

**Q1 — point lookup, OLTP**:
- 1 row, 50 column 모두 필요
- **Row-oriented**: 한 page 읽고 끝. ~ms.
- **Column-oriented**: 50개 column file 각각 seek → 50 disk seek. *50x 느림*.
- → row-oriented 우세.

**Q2 — aggregate scan, OLAP**:
- 1억 row, 3 column 만 (date, product_id, amount)
- **Row-oriented**: 50 column × 1억 = 50억 cell *모두* 디스크에서 읽음
- **Column-oriented**: 3 column × 1억 = 3억 cell. *17x 적은 I/O*. 추가로 *압축* 으로 더 줄어듦.
- → column-oriented 압도적.

원칙: **point lookup → row**, **aggregate scan → column**. *OLTP+OLAP 같이 하려면 별도 system + ETL*.

</details>

### Q8. Materialized view 의 staleness

`CREATE MATERIALIZED VIEW daily_revenue ...` 의 staleness 문제.

<details><summary>답</summary>

Materialized view 는 *주기적 refresh* 가 표준:
- `REFRESH MATERIALIZED VIEW daily_revenue;` 가 *full recompute* (큰 view 엔 분 단위)
- 또는 `CONCURRENTLY` 옵션으로 *online refresh* (read 가능)

**Staleness trade-off**:
- 1시간 마다 refresh → 1시간 latency
- 실시간 refresh → 매 write 가 view 도 갱신 (write 비용 ↑)

**해결**:
- **Incremental materialized view** (Materialize, Apache Pinot) — write 마다 view 의 *delta* 만 계산
- **Stream processing 의 stateful agg** (11장) — Flink 의 windowed aggregation
- **Cube + drill-down** — 다차원 pre-aggregate

원칙: *report 의 freshness 요구* 가 refresh 주기 결정. real-time 요구면 stream 으로 가야.

</details>

### Q9. 디버그 — 갑자기 disk space 폭증

LSM-tree DB 의 disk usage 가 갑자기 *2배* 가 됨. 진단.

<details><summary>답</summary>

**가능 원인**:

1. **Compaction backlog** — write 폭주로 새 SSTable 쌓이는 속도가 compaction 보다 빠름. compaction 이 따라잡기 전엔 *중복 데이터* 누적.

2. **Long-running snapshot** — backup 또는 read transaction 이 *옛 segment* 를 hold → compaction 이 *옛것 삭제 못함*.

3. **Bloom filter 메모리 부족** — bloom filter 가 disk 로 spill 하면서 fragment 화.

4. **Tombstone 누적** — delete 가 *tombstone marker* 로 표시. tombstone 도 disk 차지. 충분한 compaction 후 *실제 삭제*.

5. **WAL 누적** — checkpoint 가 안 진행되어 WAL 파일이 무한 성장.

**진단 순서**:
- compaction stats 확인 (Cassandra `nodetool compactionstats`, RocksDB `compaction_stats`)
- long-running transaction 종료
- WAL checkpoint 강제
- 안 되면 *manual compaction* trigger

</details>

### Q10. Bloom filter — 정확한 사용법

bloom filter 를 LSM-tree 의 read 에 *어떻게* 사용? false positive / negative 의 의미.

<details><summary>답</summary>

**Bloom filter** — *확률적 set membership 자료구조*. m 비트 + k hash 함수.

- **insert(x)**: k 개 hash 위치를 1 로 set
- **contains(x)**: k 개 위치가 *모두 1* 이면 "있을 수도 있음" (false positive 가능), *하나라도 0* 이면 "확실히 없음"

**LSM-tree 의 활용**:
```
for sstable in sstables_by_recency:
    if not sstable.bloom.contains(key):
        continue        # 100% 없음, skip
    value = sstable.lookup(key)  # disk seek
    if value is found:
        return value
return NOT_FOUND
```

→ key 가 *실제로 없는* sstable 의 disk seek 회피. read amp 의 핵심 mitigate.

**파라미터 trade-off**:
- 1% false positive: ~10 bits/key
- 0.1% false positive: ~15 bits/key

100M key + 1% FP = 125MB 메모리. 합리적.

</details>

### Q11. Heap file vs Clustered index — 운영 시사점

PostgreSQL (heap + B-tree index) 와 MySQL InnoDB (clustered primary key) 의 *insert 동작 차이*.

<details><summary>답</summary>

**PostgreSQL (heap)**:
- INSERT: heap 끝에 append (sequential, 빠름)
- index 가 *heap row pointer* 보유
- VACUUM 필요 (옛 row 정리)

**MySQL InnoDB (clustered)**:
- 모든 row 가 *primary key B-tree 안*
- INSERT: B-tree 의 해당 자리 찾아 삽입 → primary key 의 random insert 면 *page split 빈번*
- 추가 secondary index 도 *primary key value* 를 가짐 (heap pointer 가 아니라)
- secondary lookup: secondary B-tree → primary key → clustered B-tree 두번 traversal

**시사점**:
- InnoDB 에서 *random primary key (UUID)* → page split 폭주. → *sequential PK (auto-increment, ULID)* 권장.
- PostgreSQL 은 random PK 도 *heap append* 라 OK.
- Secondary lookup: PostgreSQL 이 *한 번* (index → heap), InnoDB 가 *두 번* (secondary → primary → row).

각 trade-off 가 *PK 디자인* 과 *secondary lookup 패턴* 에 영향.

</details>

### Q12. 면접 — "PostgreSQL 이 LSM-tree 가 아닌 이유?"

<details><summary>답</summary>

답:
1. **역사적 — 1980년대 University of California Berkeley 의 POSTGRES 가 B-tree 베이스로 출발**. 30년 codebase 가 B-tree 에 깊이 결합.

2. **OLTP 위주 워크로드** — PostgreSQL 의 *주 사용처* 는 web app 의 mixed read/write. B-tree 의 *read latency 일정* + *낮은 read amp* 가 더 적합.

3. **MVCC + ACID** — PostgreSQL 의 *Multi-Version Concurrency Control* (7장) 이 B-tree 의 page-level versioning 에 자연스럽게 통합. LSM 에선 더 복잡.

4. **Cost-based query planner** — B-tree 의 *예측 가능한 cost* (index seek = log N) 가 planner 의 결정 정확도 ↑. LSM 의 read 가 *불확정* (bloom filter 통과 여부).

5. **Mature ecosystem** — pg_stat_*, EXPLAIN ANALYZE, partial index, BRIN index 등 *B-tree 변종* 이 풍부.

**예외**:
- *write-heavy* 워크로드: PostgreSQL 의 *unlogged tables* + asynchronous replica
- *time-series*: TimescaleDB extension 이 *hypertable* 로 LSM-like 동작
- *foreign data wrappers* 로 RocksDB engine 직접 연결 가능

답 핵심: "PostgreSQL = mature B-tree + transaction 의 합". 새 시스템 선택할 땐 *workload 측정* 후 LSM 도 고려.

</details>
