# Ch 6 Partitioning — 치트시트

## TL;DR

- Partition = 데이터를 *수평 분할*. Replication 과 *직교*, 보통 함께
- **Range** (HBase, BigTable): range query 자연. hot spot 위험
- **Hash** (Cassandra, DynamoDB): uniform. range 못
- Hot key 4 해결: app split / cache / replica / dedicated
- Secondary index: **Local** (doc-partitioned, scatter-gather read) vs **Global** (term-partitioned, distributed write)
- Rebalancing: `hash mod N` 금지. **Fixed partitions** + **dynamic split/merge**
- Routing: ZooKeeper/etcd 기반 metadata + gossip

---

## Quick Reference

### 표 1. Range vs Hash

| | Range | Hash |
|--|--|--|
| Range query | ✓ | ✗ |
| Uniform 분산 | ✗ (분포 불균등) | ✓ |
| Hot spot | timestamp key 위험 | celebrity key 위험 |
| 예시 | HBase, BigTable | Cassandra, DynamoDB |

복합: Cassandra `(hash_key, range_key)` — partition_key 는 hash, clustering_key 는 range.

### 표 2. Hot key 해결

| 방법 | 비고 |
|--|--|
| Application split | random suffix 로 N 등분 |
| Cache | Redis, application cache |
| Read replica | hot key 의 read 분산 |
| Dedicated infra | 진짜 큰 case 만 |

### 표 3. Secondary index

| | Local (doc-partitioned) | Global (term-partitioned) |
|--|--|--|
| Read | scatter-gather (모든 partition) | term 의 partition 만 |
| Write | local only | distributed |
| 예시 | MongoDB, Cassandra | Solr, DynamoDB GSI |

### 표 4. Rebalancing

| 전략 | 비고 |
|--|--|
| `hash mod N` | ❌ N 변경 시 모두 이동 |
| Consistent hashing | ✓ 인접 node 의 일부만 |
| Fixed partitions | partition 수 ≫ node, partition 단위 이동 |
| Dynamic partitioning | size-based auto split/merge (HBase) |
| Partition per node | node 추가 시 partition 도 (Cassandra) |

### 표 5. Request routing

| 방식 | 비고 |
|--|--|
| Any node + forward | client 가 어디든 OK |
| Routing tier (proxy) | 중앙 routing |
| Client-side | client 가 metadata 보유 |

Metadata 저장: **ZooKeeper, etcd** (consensus 기반, 9장)

### 표 6. Production partition 결정 체크리스트

```
1. Workload analysis:
   - Range query 빈번? → range
   - Random access only? → hash
   - Hot key 있나? → app split 미리 설계

2. Cardinality:
   - shard key 의 distinct value 수가 partition × 100+ 이어야

3. Monotonic increasing key 회피:
   - timestamp / auto-increment 단독 사용 X
   - composite: (hash, timestamp) 형태

4. Secondary index:
   - read 빈도 vs write 빈도 측정
   - Local: write 빈번 + read 가끔
   - Global: read 빈번 + write 가끔

5. Operations:
   - Rebalancing automation 의 위험 인식
   - Operator-in-the-loop 권장
```

---

## Mind Map

```
6장 Partitioning
├─ 1. + Replication 결합 (직교, 함께)
├─ 2. Range partitioning
│   └─ HBase, BigTable, RethinkDB
├─ 3. Hash partitioning
│   ├─ Cassandra, MongoDB, DynamoDB
│   └─ Hot key 처리 (app split 등)
├─ 4. Secondary index
│   ├─ Local (doc-partitioned)
│   └─ Global (term-partitioned)
├─ 5. Rebalancing
│   ├─ hash mod N 금지
│   ├─ Fixed partitions
│   └─ Dynamic split/merge
└─ 6. Routing
    ├─ Any / Tier / Client-side
    └─ ZooKeeper, etcd, gossip
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | partition + replication 함께 |
| 2 | range = 정렬 자연, hot spot 위험 |
| 3 | hash = uniform, range 못 |
| 4 | hot key = celebrity 의 single-partition 폭주 |
| 5 | secondary index 는 local vs global, read/write trade-off |
| 6 | rebalancing 은 fixed/dynamic, hash mod N 금지 |
| 7 | routing 은 ZooKeeper 메타데이터 + redirect |
