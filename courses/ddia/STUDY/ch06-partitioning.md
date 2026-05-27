# Chapter 6: Partitioning — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 6** (책 p.199~220, PDF p.221~242).
> 6장: 데이터를 *여러 partition (= shard)* 으로 나눠 분산. *scalability + parallelism*. replication (5장) 과 *직교* — 보통 둘 다 함께.

## 들어가기 전에

- **선수 지식**: 3장 storage, 5장 replication
- **학습 목표**
  1. *Partition* 의 정의 — 데이터를 *큰 dataset 의 부분 집합* 으로 나눔
  2. **Key-range vs Hash partitioning** — 각 trade-off
  3. **Hot spot** — 부하 분포 불균형의 원인 + 해결
  4. **Secondary index** — partition 위에서 *어렵* (local vs global)
  5. **Rebalancing** — partition 이동의 *동적 reallocation*
  6. **Request routing** — client → 적절한 partition 찾기
- **예상 학습 시간**: 90~120분

---

## 1. Partitioning + Replication 의 결합

```
Partition 1: replicas on node A, B, C
Partition 2: replicas on node B, C, D
Partition 3: replicas on node C, D, A
```

→ 데이터를 *N partition* + 각 partition 을 *R replica* 로 *N×R / R = N* 머신에 분산.

![Figure 6-1 — Partition 과 replication 의 결합. 책 p.200](/courses/ddia/figures/ch06/fig-6-1.png)

---

## 2. Key-Value 데이터의 partitioning

### 2.1 Key Range Partitioning

알파벳 책의 백과사전처럼 *key 의 범위* 로 분할:

- Partition 1: A~D
- Partition 2: E~H
- ...

장점:
- **Range query 자연스러움** — 한 partition 또는 인접 partition 들만 보면 됨

단점:
- **Hot spot** — 데이터 분포가 *불균등* (예: 알파벳 분포 — Z 적음, S 많음) → partition 마다 *부하 차이*
- *시간 기반 key* (timestamp) 면 *모든 write 가 가장 최근 partition 으로* → 한 partition hot spot

![Figure 6-2 — Key range partitioning. 책 p.202](/courses/ddia/figures/ch06/fig-6-2.png)

예: HBase, BigTable, RethinkDB.

### 2.2 Hash Partitioning

key 의 *hash* 로 partition 결정:

```python
partition_id = hash(key) % num_partitions
```

장점:
- **Uniform distribution** — hash 가 *무작위 분포* → hot spot 회피

단점:
- **Range query 불가능** — 같은 prefix 의 key 들이 *다른 partition*

예: Cassandra, MongoDB hashed sharding, DynamoDB.

> **함정 1**: hash partitioning 의 *MD5 / SHA* 같은 strong hash 필요. Java 의 `Object.hashCode()` 는 *JVM version 마다* 다를 수 있어 *partition 위치 바뀜*.

### 2.3 Hot key — Hash 도 만능 아님

특정 *한 key* 가 *극단적으로 인기* (예: celebrity, 트렌딩 뉴스). hash 분산이 안 됨 — 모든 read/write 가 *한 partition* 으로.

**해결**:
1. **Application 분산** — `celebrity_id` 끝에 random suffix 추가 (`celebrity_42_a`, `celebrity_42_b`, ...). N개 split, write 시 분산, read 시 모두 합침
2. **Cache** — 자주 read 되는 key 를 *application 캐시*
3. **Read replica** — 인기 key 의 read 를 *모든 replica* 에서

---

## 3. Partitioning of Secondary Indexes

primary key 가 아닌 column 으로 검색 — secondary index. 분산 환경에선 *2 가지 접근*.

### 3.1 Local Index (Document-partitioned)

각 partition 이 *자기 데이터의 secondary index 만* 보유:

```
Partition 1: docs + index of {color, brand} within Partition 1
Partition 2: docs + index of {color, brand} within Partition 2
```

장점:
- Write 가 *한 partition* 만 → 단순, 빠름

단점:
- Read 가 *모든 partition* 조회 → *scatter-gather* — slow tail

예: MongoDB sharded cluster, Cassandra.

![Figure 6-4 — Local secondary index (document-partitioned). 책 p.207](/courses/ddia/figures/ch06/fig-6-4.png)

### 3.2 Global Index (Term-partitioned)

각 *term* (예: color=red) 에 대한 index 자체가 *partition* 됨:

```
Index 1 (a-m): color=blue,brown,gold,...
Index 2 (n-z): color=red,white,yellow,...
```

장점:
- Read 가 *해당 term partition 만* → 빠름

단점:
- Write 가 *여러 partition* 갱신 (해당 doc 의 모든 term) → distributed transaction 필요 (7장) 또는 async

예: Solr, DynamoDB Global Secondary Index.

![Figure 6-5 — Global secondary index (term-partitioned). 책 p.209](/courses/ddia/figures/ch06/fig-6-5.png)

---

## 4. Rebalancing — Partition 의 동적 이동

cluster 에 node 추가/제거 시 *partition 재분배*.

### 4.1 잘못된 전략 — `hash mod N`

```python
partition = hash(key) % N
```

N 변경 시 *거의 모든 key* 의 partition 이 바뀜. 대량 이동.

### 4.2 Fixed Number of Partitions

처음에 *partition 수* 를 *node 수보다 훨씬 많이* 만듦 (예: node 10개, partition 1000개). 각 node 가 *여러 partition*.

새 node 추가:
- *기존 node 의 일부 partition* 을 새 node 로 이동
- partition 수 *고정* → key 의 partition 결정은 *불변*

예: Riak, Voldemort, Elasticsearch.

![Figure 6-6 — Fixed partition rebalancing. 책 p.213](/courses/ddia/figures/ch06/fig-6-6.png)

**단점**: 처음 partition 수 결정이 어렵 — 너무 적으면 scale 한계, 너무 많으면 *각 partition 의 overhead* (1000+ partition 의 metadata).

### 4.3 Dynamic Partitioning

partition 이 너무 커지면 *자동 split*, 너무 작아지면 *자동 merge*:

```
Partition A 크기 > 10GB → split 으로 A1, A2
```

예: HBase, RethinkDB, MongoDB.

장점: partition 수가 *데이터 크기에 적응*.
단점: 구현 복잡.

### 4.4 Partition Per Node

node 수 = partition 수. node 추가 시 partition 도 늘어남:

예: Cassandra, Ketama.

---

## 5. Request Routing

client 가 *어느 partition 어느 node* 에 query 보낼지?

### 5.1 세 가지 접근

![Figure 6-7 — 3 가지 request routing 방식. 책 p.215](/courses/ddia/figures/ch06/fig-6-7.png)

1. **Any node** — client 가 *아무 node* 에 보내면 *그 node 가 forward*
2. **Routing tier** — proxy / load balancer 가 *routing 결정*
3. **Client-side** — client 가 *routing 정보 보유*, 직접 connect

### 5.2 Coordination Service

대부분 *분산 메타데이터 service* (ZooKeeper, etcd) 가 *partition → node 매핑* 보유:
- 변경 시 client 또는 routing tier 에 알림
- 9장 (consensus) 의 기반

예:
- **Espresso (LinkedIn)**: Helix (ZooKeeper 기반) 가 routing
- **HBase, SolrCloud**: ZooKeeper
- **Couchbase, Cassandra**: gossip protocol 로 *client 자체* 가 routing 학습

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Partitioning = replication | 직교. 보통 둘 다 함께 (partition + replica per partition) |
| 2 | Hash partitioning 이 *완전* 균등 | hot key (celebrity) 는 그래도 한 partition. application 분산 필요 |
| 3 | Java `hashCode` 로 partition | JVM 별 차이 → MD5 / Murmur3 같은 stable hash |
| 4 | `hash mod N` rebalancing | N 변경 시 *거의 전부* 재이동. consistent hashing or fixed partitions |
| 5 | Range query 가 hash 위에서 OK | hash 는 *order 부수기* → range scan 모든 partition |
| 6 | Local secondary index 가 항상 빠름 | read 가 scatter-gather (모든 partition). tail latency 발생 |
| 7 | Global index 의 write 가 가벼움 | term 들이 *여러 partition* 갱신 → distributed transaction 또는 async |
| 8 | Rebalancing 이 자동·즉시 | 큰 partition 이동은 *시간 + bandwidth* 소요. 운영 영향 |
| 9 | Routing 결정이 *항상 정확* | 메타데이터 stale 가능 → "wrong partition" response → client retry |
| 10 | Partition 수 변경 쉬움 | fixed partitions 에선 매우 어려움. dynamic partitioning 만 자유 |

---

## 자가점검

1. *Partitioning + replication* 의 관계.
2. *Key-range vs hash* partitioning 의 trade-off.
3. *Hot spot* 의 원인 + 해결.
4. *Local* vs *global* secondary index 의 read/write trade-off.
5. `hash mod N` 이 *왜 잘못된* rebalancing 전략.
6. *Fixed partitions* vs *dynamic partitioning* 의 차이.
7. *Request routing* 의 3 가지 방식.
8. *Coordination service* (ZooKeeper) 가 *왜* 필요한가.

### 해답 (간략)

1. 직교 — partition (수평 분할) + replication (각 partition 의 복제). 보통 결합.
2. Range: range query 자연스러움, hot spot 위험. Hash: uniform, range 불가.
3. 원인 — 데이터 분포 불균등, timestamp key, celebrity. 해결 — random suffix, cache, replica 분산.
4. Local: write 빠름, read scatter-gather. Global: read 빠름, write distributed.
5. N 변경 시 *모든 key* 의 partition 이동.
6. Fixed: partition 수 고정, node 추가 시 partition 일부 이동. Dynamic: 크기 기반 자동 split/merge.
7. (1) any node + forward (2) routing tier (3) client-side routing.
8. partition → node 매핑의 *consistent view* 유지. 변경 propagation. 9장 consensus 의 응용.

---

## 다음 학습으로

- **7장 (Transactions)** — 여러 partition 에 걸친 transaction = *distributed transaction*
- **8장 (Trouble)** — partitioning + network partition 의 *복합 문제*
- **9장 (Consistency)** — coordination service 가 어떻게 *consensus* 달성
- **10장 (Batch)** — partitioned data 의 *parallel processing* (MapReduce)
