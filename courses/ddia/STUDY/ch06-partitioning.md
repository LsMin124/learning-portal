# Chapter 6: Partitioning — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 6** (책 p.199~220, PDF p.221~242).
> 6장: 데이터를 *여러 partition (= shard)* 으로 나눠 분산. *scalability + parallelism*. replication (5장) 과 *직교* — 보통 둘 다 함께.

이 장의 *지적 무게중심*:
1. **Partition + replication 의 직교성** — 두 차원을 함께 설계
2. **Key-range vs Hash** — *range query* vs *uniformity* 의 trade-off
3. **Hot spot** — celebrity, timestamp key 의 *근본 위험*
4. **Secondary index** — local vs global, *write vs read* 의 trade-off
5. **Consistent hashing** + *rebalancing 의 정치*
6. **Request routing** — ZooKeeper 같은 coordination service

---

## 들어가기 전에

- **선수 지식**: 3장 storage, 5장 replication
- **학습 목표**
  1. *Partition* 의 정의
  2. **Key-range vs Hash partitioning** — 각 trade-off
  3. **Hot spot** — 부하 분포 불균형의 원인 + 해결
  4. **Secondary index** — partition 위에서 *어렵*
  5. **Rebalancing** — partition 이동의 *동적 reallocation*
  6. **Request routing** — client → 적절한 partition 찾기
- **예상 학습 시간**: 90~120분

---

## §1 Partitioning + Replication 의 결합

```
Partition 1: replicas on node A, B, C
Partition 2: replicas on node B, C, D
Partition 3: replicas on node C, D, A
```

→ 데이터를 *N partition* + 각 partition 을 *R replica* 로 분산.

![Figure 6-1 — Partition 과 replication 의 결합. 책 p.200](/courses/ddia/figures/ch06/fig-6-1.png)

**용어**:
- *Partition* (DDIA, MongoDB, Elasticsearch terminology)
- *Shard* (MySQL, Elasticsearch)
- *Region* (HBase, BigTable)
- *Tablet* (Spanner, BigTable)
- *vBucket* (Couchbase)

---

## §2 Key-Value 데이터의 partitioning

### §2.1 Key Range Partitioning

알파벳 책의 백과사전처럼 *key 의 범위* 로 분할:

- Partition 1: A~D
- Partition 2: E~H
- ...

장점:
- **Range query 자연스러움**

단점:
- **Hot spot** — 데이터 분포가 불균등
- *시간 기반 key* (timestamp) 면 *모든 write 가 가장 최근 partition 으로*

![Figure 6-2 — Key range partitioning. 책 p.202](/courses/ddia/figures/ch06/fig-6-2.png)

**예**:
- HBase, BigTable — region 단위 자동 split
- Cassandra (order-preserving partitioner) — option
- Spanner — globally distributed key ranges

### §2.2 Hash Partitioning

key 의 *hash* 로 partition 결정:

```python
partition_id = hash(key) % num_partitions
```

장점:
- **Uniform distribution** — hot spot 회피

단점:
- **Range query 불가능**

**예**:
- Cassandra (Murmur3 partitioner — default)
- MongoDB hashed sharding
- DynamoDB
- Riak

> **함정 1**: hash partitioning 의 *MD5 / Murmur3* 같은 strong hash 필요. Java `Object.hashCode()` 는 *JVM version 마다 다름*.

### §2.3 Hot key — Hash 도 만능 아님

특정 *한 key* 가 *극단적으로 인기* (celebrity, 트렌딩). hash 분산이 안 됨.

**해결**:
1. **Application 분산** — `celebrity_42_a`, `celebrity_42_b`, ... N개 split
2. **Cache** — application 캐시
3. **Read replica** — 모든 replica 에서 read

**실제 — Twitter 의 Justin Bieber 문제**:
- celebrity 의 tweet 의 *수십 million followers* fanout
- 해결 — *separate write path* (celebrity 별도 처리)

### §2.4 Consistent Hashing

전통 `hash mod N` 의 문제 — N 변경 시 거의 모든 key 재배치.

**Consistent hashing** (Karger, 1997):
- Hash space 를 *circular ring* 으로
- Node 가 ring 의 *임의 위치*
- Key 는 *시계방향 다음 node*

**Node 추가/제거**: *인접 node 의 일부 key 만* 이동 → ~ 1/N

**Virtual nodes** (vnode):
- 각 physical node 가 ring 의 *여러 위치* (100~256)
- *균등 분포* 보장
- *Heterogeneous capacity* — 큰 node 가 더 많은 vnode

**산업 사용**:
- Cassandra — 256 vnodes per node (default)
- DynamoDB — internal
- Memcached client — Ketama
- Riak — 1024 vnodes default

---

## §3 Partitioning of Secondary Indexes

### §3.1 Local Index (Document-partitioned)

각 partition 이 *자기 데이터의 secondary index 만* 보유.

장점:
- Write 가 *한 partition* 만 → 단순, 빠름

단점:
- Read 가 *모든 partition* — *scatter-gather*

예: MongoDB sharded, Cassandra, Elasticsearch.

![Figure 6-4 — Local secondary index. 책 p.207](/courses/ddia/figures/ch06/fig-6-4.png)

**Scatter-gather 의 latency**:
- N partition, 각 100 ms ± 10
- Total = max(all) — *tail latency 가 N 에 증가*
- *Slow node* 가 전체 latency 결정

### §3.2 Global Index (Term-partitioned)

각 *term* (color=red) 의 index 가 *partition*.

장점:
- Read 가 *해당 term partition 만* → 빠름

단점:
- Write 가 *여러 partition* 갱신 (해당 doc 의 모든 term)

예: Solr, DynamoDB Global Secondary Index.

![Figure 6-5 — Global secondary index. 책 p.209](/courses/ddia/figures/ch06/fig-6-5.png)

**DynamoDB GSI 의 비동기 update**:
- Main table write 후 *GSI async update*
- *Eventually consistent*
- *Strongly consistent read* 는 main table only

---

## §4 Rebalancing

### §4.1 잘못된 전략 — `hash mod N`

N 변경 시 *거의 모든 key* partition 변경.

### §4.2 Fixed Number of Partitions

처음에 partition 수를 node 수보다 *훨씬 많이* (예: node 10, partition 1000).

새 node 추가 → 기존 partition 일부 이동. partition 수 고정.

예: Riak, Voldemort, Elasticsearch.

![Figure 6-6 — Fixed partition rebalancing. 책 p.213](/courses/ddia/figures/ch06/fig-6-6.png)

**Elasticsearch 의 함정**:
- *Shard 수 한번 결정되면 변경 어려움*
- Over-sharding → metadata + heap 비효율
- Under-sharding → scale 제한
- *Best*: shard 당 ~10-50 GB

### §4.3 Dynamic Partitioning

partition 크기 기반 자동 split/merge:

```
Partition A 크기 > 10GB → A1, A2
```

예: HBase, RethinkDB, MongoDB.

### §4.4 Partition Per Node

node 수 = partition 수. 옛 Cassandra default.

### §4.5 Rebalancing 의 *Operational concern*

**Manual vs Automatic**:
- Auto — 빠름, *unexpected cascading*
- Manual — 안전, operator 부담
- 산업 — *suggest + approve*

**Bandwidth cost**:
- 1 TB partition 이동 = 수십 분 ~ 수 시간
- Rate limiting + off-peak schedule

---

## §5 Request Routing

### §5.1 세 가지 접근

![Figure 6-7 — 3 가지 routing. 책 p.215](/courses/ddia/figures/ch06/fig-6-7.png)

1. **Any node** — client → 아무 node → forward
2. **Routing tier** — proxy / LB 가 결정
3. **Client-side** — client 가 routing 정보 보유

### §5.2 Coordination Service

*분산 메타데이터 service* (ZooKeeper, etcd) 가 partition → node 매핑.

**예**:
- HBase, SolrCloud — ZooKeeper
- Kubernetes — etcd (Raft)
- Espresso (LinkedIn) — Helix
- Couchbase, Cassandra — gossip protocol (no central)

**Gossip 의 장단**:
- *No SPOF*
- *Eventually consistent metadata*
- 큰 cluster 에 overhead

---

## §6 산업 사례

### §6.1 Slack 의 sharding (Vitess)

- *Per-workspace sharding* — 한 회사 메시지가 같은 shard
- *Vitess* (YouTube MySQL sharding) 사용
- *Shard key* = team_id
- 대부분 query 가 *한 team 안*

### §6.2 Discord 의 message sharding

- *Cassandra → ScyllaDB* 전환 (2022)
- *Shard key* = (channel_id, message_bucket)
- *Bucket* = month-based — time-based ordering
- channel_id 가 첫 key → 채널 별 분산

### §6.3 GitHub 의 sharding

- MySQL + Vitess
- *Shard by repository*
- Cross-shard query 는 application
- *gh-ost* (online schema change)

### §6.4 Pinterest 의 sharding

- 자체 MySQL sharding (2012~)
- *Virtual shards* — 8192 ~ 65536
- Each physical DB = many virtual shards
- Scaling = physical DB 추가 → virtual 재분배

---

## §7 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Partitioning = replication | 직교 |
| 2 | Hash 가 *완전* 균등 | hot key 는 한 partition |
| 3 | Java `hashCode` 로 partition | JVM 별 차이 → MD5/Murmur3 |
| 4 | `hash mod N` rebalancing | 거의 전부 재이동 |
| 5 | Range query 가 hash 위 OK | range scan 모든 partition |
| 6 | Local secondary 가 항상 빠름 | scatter-gather tail latency |
| 7 | Global index 의 write 가벼움 | 여러 partition 갱신 |
| 8 | Rebalancing 자동·즉시 | 큰 partition 이동 = 시간 + bandwidth |
| 9 | Routing 항상 정확 | 메타데이터 stale 가능 → retry |
| 10 | Partition 수 변경 쉬움 | fixed partitions 에선 매우 어려움 |
| 11 | Time-based partition key OK | hot spot 의 classic 함정 |
| 12 | Sharding 한 번 결정 → 영구 | Resharding 의 큰 비용 (수일~수주) |

---

## §8 자가점검

1. *Partitioning + replication* 의 관계?
2. *Key-range vs hash* 의 trade-off?
3. *Hot spot* 의 원인 + 해결?
4. *Local* vs *global* secondary index?
5. `hash mod N` 이 *왜 잘못*?
6. *Fixed* vs *dynamic* partitioning?
7. *Request routing* 의 3 가지?
8. *Coordination service* 가 *왜* 필요?
9. *Consistent hashing* + virtual node?
10. *Shard key* 선택의 고려?

<details><summary>해답 (간략)</summary>

1. 직교 — partition + replication. 보통 결합.
2. Range: range query 자연, hot spot. Hash: uniform, range 불가.
3. 분포 불균등, timestamp key, celebrity. 해결: random suffix, cache, replica.
4. Local: write 빠름, read scatter. Global: read 빠름, write distributed.
5. N 변경 시 모든 key 이동.
6. Fixed: 수 고정, 일부 이동. Dynamic: 크기 기반 split/merge.
7. (1) any node + forward (2) routing tier (3) client-side.
8. partition → node 매핑의 consistent view. 변경 propagation.
9. Hash space ring + 시계방향 다음 node + vnode 균등 분포.
10. Query pattern, hot spot 회피, future resharding 비용.

</details>

---

## §9 다음 학습으로

- **7장 (Transactions)** — 여러 partition 의 transaction = *distributed transaction*
- **8장 (Trouble)** — partitioning + network partition 의 복합
- **9장 (Consistency)** — coordination service 의 consensus
- **10장 (Batch)** — partitioned data 의 parallel processing

---

## §10 한 줄 요약

> **Partitioning = scale 의 *수평 차원*. Replication 과 직교. *Hash* (uniform, no range) vs *Range* (range query, hot spot 위험). *Hot key* 의 application-level 분산. Consistent hashing + virtual nodes. ZooKeeper 같은 coordination service.**
