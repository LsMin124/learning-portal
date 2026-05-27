# Ch 2 Data Models — 퀴즈

> 12 문항 (개념 4 / 비교 3 / 디버그 3 / 면접 2).

### Q1. Object-Relational Impedance Mismatch

용어 정의 + document 모델이 *어떻게* 해결.

<details><summary>답</summary>

**정의**: application 의 *객체* (nested, polymorphic) 와 relational *table* (flat, normalized) 사이의 *번역 비용*. ORM (Hibernate, Django ORM) 으로 일부 해소되지만 SQL 의 type system 과 OOP 사이 *gap* 은 남음.

**Document 모델의 해결**: 객체와 *같은 형태* (tree-shaped JSON) 로 저장 → ORM 불필요, locality 우수. 단 *many-to-many* 가 등장하면 다시 어색해짐.

</details>

### Q2. Schema-on-Read vs Write

각 모델을 *type system* 에 비유 + evolution 시의 *비용 비교*.

<details><summary>답</summary>

| 모델 | type system 비유 | evolution 비용 |
|--|--|--|
| Schema-on-write (relational) | static (compile-time) | ALTER TABLE + 마이그레이션 (큰 테이블엔 비싸지만 *일회성*) |
| Schema-on-read (document) | dynamic (runtime) | application 코드가 *옛 형태 + 새 형태 모두* 지원 (*지속적* cost) |

trade-off: write 시 비용 vs read 시 (계속) 비용. 큰 데이터는 *현재 row 만 새 schema 로* 쓰는 게 가능해 schema-on-read 가 *마이그레이션 회피* 에 유리. 그러나 코드 복잡도 ↑.

</details>

### Q3. Many-to-Many 의 모델 선택 영향

LinkedIn 의 직장 정보가 *그냥 string* 일 때 document 가 OK 인데, *별도 회사 entity* 가 되면 어떻게 바뀌나?

<details><summary>답</summary>

**string 일 때**: document 안에 `"organization": "Microsoft"` 만 저장. self-contained, locality 좋음.

**entity 일 때**:
- 회사 ID 를 별도 collection `companies` 에 저장
- user document 가 `"organization_id": 42` 로 참조
- *application 이 두 collection JOIN* (또는 MongoDB `$lookup`)
- 회사 이름 변경 시 *한 곳만* 수정 (normalization)

→ relational 의 강점을 *문서 DB 안에서 직접 구현*. 이쯤이면 relational 로 가는 게 자연스러움. *evolution 가능성* 을 미리 고려.

</details>

### Q4. NoSQL 채택의 4 driver

각 driver 가 *어떤 사용 사례* 와 가장 잘 맞는지.

<details><summary>답</summary>

1. **Scalability** — 트래픽 폭주 SaaS, IoT (millions writes/sec)
2. **Open source** — startup, 라이센스 부담 회피
3. **Specialized query** — 추천 graph DB, 시계열 (InfluxDB), 검색 (Elasticsearch)
4. **Schema flexibility** — 빠른 prototyping, log/event 저장

→ 채택 결정 시 *어떤 driver* 가 가장 중요한지 명시. "그냥 NoSQL" 은 잘못된 선택. relational + JSON column 이 *대부분 사용 사례에 충분*.

</details>

### Q5. Cypher vs SQL recursive CTE

같은 query 를 두 언어로 짠 코드의 *길이 비율*. 왜 graph DB 가 이런 query 에 우세한가?

<details><summary>답</summary>

전형적인 *transitive closure* (예: 미국 출생 + 유럽 거주) query:
- Cypher: ~5 줄
- SQL (recursive CTE): ~30 줄 (UNION ALL 안에서 join 재귀)

**길이 차이 ~6배**. 이유:
- Cypher 가 *graph pattern* (`(node)-[:REL]->(node2)`) 을 *first-class syntax* 로 표현
- SQL 은 graph 가 *2-table relation* 으로 normalize 되어 모든 traversal 이 *recursive JOIN*
- *Variable-length path* (`*0..`) 를 Cypher 가 한 기호로, SQL 은 CTE 재귀로

성능도 graph DB 가 *수십~수백배* 빠른 경우 다수 (index 가 *edge 자체* 에 최적화).

</details>

### Q6. Document → Relational 마이그레이션 디버그

MongoDB 의 user 컬렉션을 PostgreSQL 로 옮기는 중. user 의 `addresses` field 가 *array* 인데 어떻게 모델링?

<details><summary>답</summary>

**옵션 1: Normalized** — 별도 `addresses` 테이블
```sql
CREATE TABLE addresses (
  user_id INT REFERENCES users(id),
  type VARCHAR(20),
  street TEXT,
  city TEXT,
  -- ...
);
```
장점: 정규화, 검색 친화. 단점: JOIN 비용.

**옵션 2: JSONB column** — PostgreSQL 의 jsonb
```sql
ALTER TABLE users ADD COLUMN addresses JSONB;
```
장점: 객체 그대로. 단점: 인덱스가 *GIN* 필요, 표현이 어색.

**옵션 3: Array of composite type** — Postgres 의 array
```sql
CREATE TYPE address AS (type TEXT, street TEXT, city TEXT);
ALTER TABLE users ADD COLUMN addresses address[];
```
장점: 정형 + array. 단점: 잘 안 쓰여서 도구 지원 약함.

**선택 가이드**:
- 주소 검색·정렬 → 옵션 1
- 그냥 객체 조회 → 옵션 2
- 주소 *연산* 이 많음 → 옵션 3

</details>

### Q7. Imperative 가 Declarative 보다 *나은* 경우

declarative SQL 의 장점이 명백한데도 imperative 가 더 *나은* 경우.

<details><summary>답</summary>

1. **Complex business logic** — multi-step 계산이 SQL window function + CTE 의 chain 으로 *읽기 어려움*. application 코드의 imperative 가 더 명료.
2. **External API call 포함** — query 도중 외부 service 호출 (지오코딩, 결제). SQL 안에서 불가능.
3. **Conditional branching** — "조건 A 면 path X, 아니면 Y" 의 *깊은 분기*. CASE 로 표현 가능하지만 가독성 ↓.
4. **Streaming aggregate** — 무한 stream 에서 *online* 집계. 11장 stream processing 의 imperative pipeline.
5. **Debug / profile** — imperative 는 *line-by-line* 검사 가능. SQL planner 의 결정은 EXPLAIN 으로 봐도 *왜 그렇게* 가 어려움.

원칙: *간단한 query 는 declarative*, *복잡한 business logic + side effect 는 imperative*. 양쪽 적절히.

</details>

### Q8. Polyglot Persistence — 도구 조합 설계

e-commerce 사이트 (상품·주문·검색·추천·캐시) 에 *어떤 DB 들* 을 *어떻게* 조합?

<details><summary>답</summary>

| 컴포넌트 | DB | 이유 |
|--|--|--|
| 상품·주문 (primary) | PostgreSQL | ACID, JOIN, jsonb 로 spec 도 |
| 검색 | Elasticsearch | full-text + facet |
| 추천 | Neo4j | "이걸 산 사람이 같이 산" graph traversal |
| 캐시 | Redis | 고빈도 read (상품 detail) |
| 분석 | BigQuery / Snowflake | column store + ad-hoc query (10장) |
| 이벤트 (장바구니, 결제) | Kafka | 11장 stream |

**일관성** — PostgreSQL 이 source-of-truth. 나머지는 CDC (change data capture, 11장) 로 *derived*. 추가 DB 마다 운영 비용 ↑ 이므로 *진짜 필요할 때만* 추가.

</details>

### Q9. SPARQL 의 Semantic Web 비전이 *왜 산업에 안 정착*?

<details><summary>답</summary>

1. **URI 의 복잡성** — 모든 entity 가 globally unique URI 필요. web-scale 에서 *URI 통일* 이 안 됨 (회사마다 따로).
2. **표현력 over-engineered** — 대부분 사용 사례엔 단순 graph DB 면 충분. RDF 의 *reification, ontology* 가 과함.
3. **Tooling 빈약** — Neo4j 가 *Cypher + 좋은 UI* 로 채택. SPARQL 은 학계 중심.
4. **Schema agreement 어려움** — DBpedia 같은 *공유 ontology* 합의 비용 ↑.
5. **Performance** — SPARQL endpoint 가 generic 이라 *특정 query 최적화* 어려움.

성공한 부분: **Knowledge graph** (Google, Wikidata). 대규모 organization 이 *내부 control* 하면서 일부 SPARQL 컨셉 차용.

</details>

### Q10. Document 의 *Locality 깨짐*

MongoDB user document 가 자주 수정되면 (예: timestamp 매분 update) *어떤 문제*?

<details><summary>답</summary>

**Fragmentation**:
- MongoDB 는 document 를 *연속된 디스크 공간* 에 저장
- 수정으로 document 가 *커지면* 기존 자리에 안 들어감 → 새 위치로 이동
- 기존 자리는 *holes*, 새 위치는 *흩어짐*
- → *locality 깨짐* — 한 document 읽는데 *여러 page* 읽음

**대응**:
- **Pre-allocate** — 처음에 padding 으로 큰 공간 확보 (MongoDB 의 옛 power-of-2 allocation)
- **Append-only** — 수정 대신 *새 version 추가*, 옛것은 GC
- **Update-in-place** — 같은 크기로 유지되는 field 만 자주 수정
- **분리** — 자주 변하는 field (timestamp) 를 *별도 collection*

MongoDB 4.x 의 *WiredTiger* engine 은 이 문제 일부 해결 (LSM-tree 기반, 3장).

</details>

### Q11. 면접: "왜 MongoDB 가 아니라 Postgres 인가?"

면접관의 *전통 vs 모던* 프레임에 어떻게 답?

<details><summary>답</summary>

핵심 — *대결 프레임 자체가 옛것*. 답 흐름:

1. **요구사항 먼저** — "현재 data shape 가 어떤가요? Many-to-many 관계가 많나요? Schema 가 자주 바뀌나요?"
2. **PostgreSQL 의 모던화** — jsonb column 으로 schema-flex, GIN index 로 JSON 쿼리, partial index, table partitioning, logical replication. *MongoDB 의 90% 기능* 을 가짐.
3. **추가 기능** — ACID transaction, JOIN, mature ecosystem, observability (pg_stat_*).
4. **단점도 인정** — *write scale* 이 진짜 큰 경우 (Twitter 급): MongoDB shard cluster 또는 Cassandra 가 운영 더 쉬울 수 있음.
5. **결론** — "MongoDB *대신* 이 아니라 *왜* 인지 명확히. 데이터 shape 와 scale 의 실제 측정 후 결정."

→ 면접관이 보는 건 *technology preference* 가 아니라 *trade-off 분석 능력*.

</details>

### Q12. 면접: Graph DB 가 *언제* 정답?

<details><summary>답</summary>

Graph DB 가 *압도적* 우월한 경우:

1. **Variable-depth traversal 이 query 의 일상** — "X 의 *친구의 친구의 친구*", "X 부품을 사용하는 *모든 제품*"
2. **관계 자체에 metadata** — friendship 의 *시작 시점*, edge 의 *weight*
3. **Pattern matching** — fraud 탐지 ("A → B → C → A 의 cycle")
4. **추천 시스템** — collaborative filtering 의 graph 표현
5. **Knowledge graph** — 의료 ontology, 제품 카탈로그 분류

**Graph DB 가 *과한*** 경우:
- 단순 1-hop relation → relational join 으로 충분
- *aggregation 위주* (count, sum) → relational + index
- *transactional load* — graph DB 의 ACID 가 약함

production 패턴: **primary RDBMS + graph DB 를 *secondary*** 로. 추천·fraud query 만 graph 로 라우팅.

</details>
