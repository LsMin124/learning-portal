# Ch 6 Partitioning — 퀴즈

> 8 문항.

### Q1. Range vs Hash partitioning 의 use case

각각 어떤 사용 사례가 적합한지.

<details><summary>답</summary>

**Range** 적합:
- *시계열 데이터* (timestamp key 의 range scan 자주) — 단 *최신만 hot* 문제
- *사전식* 정렬 query (`name LIKE 'A%'`)
- HBase, BigTable, RethinkDB

**Hash** 적합:
- *균등 분산* 필요
- *Random access* 가 주 (point lookup)
- Range query 적음
- Cassandra, MongoDB hashed, DynamoDB

**복합**: Cassandra 의 *composite key* — `(partition_key, clustering_key)`. partition_key 는 hash, clustering_key 는 range 정렬. 한 partition 안에서 range query 가능.

</details>

### Q2. Hot key 의 4 가지 해결

celebrity user 의 timeline 이 hot spot. 단계별 해결.

<details><summary>답</summary>

1. **Application split**: `celebrity_42` → `celebrity_42_a`, `celebrity_42_b`, ... 10개 split. Write 시 *random* 으로 한 split 에. Read 시 모든 10개 fetch + merge.
2. **Cache layer**: Redis 또는 Memcached 가 hot key 의 결과 cache. DB hit 회피.
3. **Read replica**: hot key 의 read 를 *N replica 에 분산*. write 는 한 곳, read 는 N 군데.
4. **Dedicated infrastructure**: 진짜 큰 celebrity 의 경우 *별도 service / DB cluster*. Twitter 의 Approach 1 (5장) 의 partial 적용.

순서: 일단 cache → split → replica → dedicated. 측정 후 점진적.

</details>

### Q3. Local vs Global secondary index 선택

100 partition 의 DB 에서 `WHERE color='red'` 검색. 어떻게 결정?

<details><summary>답</summary>

**Local (document-partitioned)**:
- 100 partition 모두 조회 → 100 RPC + merge
- *Tail latency* = max(100 partition 의 응답)
- Write: 한 partition 만 갱신

**Global (term-partitioned)**:
- `color=red` term 의 *partition* 만 조회 (예: 5개)
- *Tail* 작음
- Write: doc 의 모든 term 이 *각자 partition* 갱신 (distributed)

**선택**:
- *Read 가 빈번 + 적은 term* → Global
- *Write 가 빈번 + 단순 schema* → Local
- 절충: Elasticsearch 가 local 인데 *coordinator node* 가 scatter-gather. tail latency 의 *적극 mitigate* (timeout, hedging)

</details>

### Q4. Consistent hashing — `hash mod N` 의 해결

Cassandra 가 사용하는 *consistent hashing* 원리.

<details><summary>답</summary>

**문제**: `hash mod N`, N 변경 시 모든 key 이동.

**Consistent hashing** (Karger 1997):
1. hash 공간을 *원형 ring* 으로 (0 ~ 2^32)
2. 각 node 가 *ring 위 여러 위치* (virtual node, ~256개) 점유
3. key 는 *hash(key) 의 ring 위치에서 시계 방향 가장 가까운 node*

**Node 추가**:
- 새 node 가 *몇 개 ring 위치* 점유
- 인접 node 의 *일부 key 만 이동* (전체의 ~1/N)

**Node 제거**:
- 그 node 의 key 가 *다음 node* 로 이전

이 방식이 *데이터 이동 최소화* + *균등 분산*. Cassandra, DynamoDB, Discord 등 표준.

DDIA 는 "consistent hashing" 이라는 단어 자체보다 *fixed partitions* 와 *dynamic partitioning* 의 일반 패턴 강조. 실용에선 둘이 결합.

</details>

### Q5. Rebalancing 의 정책 결정

운영자 입장 — automatic rebalancing 의 *위험*.

<details><summary>답</summary>

**Automatic rebalancing 의 위험**:

1. **Cascading failure** — 한 node 의 부하 spike 가 *rebalancing trigger*. 새 node 에 이동하는 동안 *bandwidth saturation* → 더 많은 node 가 slow → 더 많은 rebalancing... 폭주.

2. **False positive** — 일시 network blip 으로 *node 죽음* 오판. 실제는 살아있는 node 의 data 가 *불필요하게 이동*.

3. **Capacity planning 어려움** — 언제 무엇이 이동할지 *예측 불가*. peak 시간에 이동하면 영향 큼.

**Best practice — Manual or operator-in-the-loop rebalancing**:
- DB 가 *권장 사항* 만 emit, 운영자가 *승인* 후 진행
- *peak 시간 회피*
- *bandwidth limit*
- 진행 *모니터링 + 중단 가능*

Couchbase, Riak 의 default — automatic 이지만 운영자가 *조정 가능*. Cassandra 의 `nodetool removenode` — explicit 명령.

</details>

### Q6. Routing 의 stale metadata 문제

partition → node 매핑이 *바뀐 직후* client 가 옛 정보로 요청. 어떻게 처리?

<details><summary>답</summary>

**문제**: client 가 *옛 node* 에 query. 그 node 는 *내 partition 이 아님* response.

**해결 — Routing redirect**:
1. node 가 query 받음
2. 자기 partition 이 아님 확인
3. 두 가지 옵션:
   - **Forward**: 그 node 가 *올바른 node* 로 forward + response 그대로 전달
   - **Redirect**: client 에게 "이 node 로 가" response → client 가 retry

**Metadata 갱신**:
- ZooKeeper / etcd 의 *watcher* — 변경 시 client 에 push
- Gossip protocol (Cassandra) — node 들이 *서로 정보 전파*
- Periodic refresh — client 가 *1분마다* metadata fetch

**산업 트렌드**: client 가 *smart* — routing 정보 cache + retry on miss. service mesh (Envoy, Istio) 가 이걸 *application 외부* 에서 자동 처리.

</details>

### Q7. 디버그 — 한 shard 만 hot

10 shard 의 MongoDB cluster. shard 7 만 CPU 99%, 나머지는 30%. 원인?

<details><summary>답</summary>

**가능 원인**:

1. **Hot key on that shard** — 인기 user / product 가 shard 7 에 있음. `db.users.find().sort({last_active: -1})` 같은 query 가 *최신 user* 만 자주 hit.

2. **Shard key 의 distribution** — shard key 가 *monotonic increasing* (timestamp) → 모든 새 write 가 *마지막 shard* 로.

3. **Bad shard key choice** — 카디널리티 낮은 key (예: country) → 큰 국가가 한 shard 에.

4. **Unbalanced data** — 초기 shard split 의 boundary 가 잘못 잡힘. *chunk migration* 이 따라잡지 못함.

**진단**:
- `db.users.aggregate([{$collStats: {storageStats: {}}}])` — shard 별 size
- `db.printShardingStatus()` — chunk 분포
- `db.currentOp()` — 진행 중 query

**대응**:
- **Shard key 변경** — MongoDB 5.0+ 의 `reshardCollection`. 큰 비용.
- **Hot key 분산** — application split (Q2 참고)
- **Manual chunk migration** — `moveChunk` 명령
- **Compound shard key** — `{country, user_id}` 같이 *카디널리티 ↑*

</details>

### Q8. 면접 — Twitter 의 trending 같이 *전 세계 글로벌* read 

Trending hashtag 가 *전 세계 모두 똑같이* 보여야. 어떻게 partition + replication?

<details><summary>답</summary>

**도전**:
- *읽기 폭주* (수억 user 가 매 분 새로고침)
- *Real-time* — 트렌딩이 분 단위 변화
- *글로벌 일관성* — 모두 같은 트렌딩 list

**Architecture**:

1. **Compute layer (write-side)**:
   - 모든 tweet 의 hashtag 추출 → Kafka stream (11장)
   - Flink/Spark Streaming 이 *Top-K hashtag* 매 1분 계산
   - 결과: *작은 dataset* (~100 hashtag) — partition 불필요

2. **Storage layer**:
   - Result 를 *모든 region 의 KV store* (Redis cluster) 에 *fan-out*
   - *Multi-leader replication* — 각 region 이 자기 copy 보유, 1분마다 갱신
   - Read 가 *local region* 에서 (low latency)

3. **Hot key 처리**:
   - 한 hashtag detail page 가 hot → *cache hierarchy* (CDN → Redis → DB)
   - 인기 hashtag 의 *application-level split* (Q2)

4. **Personalization**:
   - 사용자별 trending 은 *region + interest* 로 partitioned
   - 5장의 sharding-by-user

**핵심 통찰** — *작은 글로벌 dataset 은 partition 보단 모든 region 에 fan-out*. *큰 user-specific dataset* 만 partition. 이게 *11장 stream + 6장 partition* 의 결합.

</details>
