# Chapter 2: Data Models and Query Languages — 학습 노트

> *Designing Data-Intensive Applications* (Kleppmann, 2017) **Chapter 2** (책 p.27~64, PDF p.49~90).
> 2장의 핵심: 데이터 모델은 *소프트웨어를 어떻게 생각하는가* 의 토대. **Relational / Document / Graph** 세 모델의 *각 특성과 적합한 도메인*.

이 장의 *지적 무게중심*:
1. **데이터 모델 = 사고 도구** — 어떤 모델을 쓰느냐가 *어떤 query 와 evolution 이 자연스러운지* 결정
2. **Relational vs Document** — *impedance mismatch* + schema-on-write/read + locality
3. **Many-to-many 관계** — *데이터 모델 선택의 결정적 기준*
4. **Graph 모델** — *연결 자체가 first-class data*
5. **Declarative > Imperative** — query 의 *언어로서의 진화*
6. **NoSQL 의 4 driver** — 그리고 *역사적 우연*

---

## 들어가기 전에

- **선수 지식**: SQL 기본, JSON·XML 구조, ORM 사용 경험
- **학습 목표**
  1. *데이터 모델 = abstraction layer* — 각 층의 모델이 *아래 층의 복잡도를 숨김*
  2. **Relational vs Document** — schema-on-write vs schema-on-read, *impedance mismatch* 해결
  3. **Many-to-many 관계** 가 모델 선택의 *결정 기준*
  4. **Declarative (SQL)** vs **Imperative (MapReduce)** vs **Graph query (Cypher, SPARQL)**
  5. *NoSQL 의 driver* — scale, OSS, dynamic schema, 그리고 *역사적 우연*
- **예상 학습 시간**: 100~140분

---

## §1 Data Model 의 *층화*

각 layer 가 *아래 layer 의 복잡도를 숨김*:

```
Application code  (객체·자료구조)
       ↓ 표현
Storage data model (JSON, relational, graph)
       ↓ 표현
Storage engine    (bytes on disk / network)
       ↓ 표현
Hardware         (electric signals)
```

각 단계의 *모델 선택* 이 그 위의 코드 작성 방식을 결정. 본 장은 *storage data model* 층.

### §1.1 *왜* layer 가 필요한가

추상화의 가치:
- **분업** — DBA 가 storage engine 을, developer 가 application 을 *독립적으로* 발전
- **재사용** — 같은 storage engine 위에 *수많은 application*
- **evolution** — 한 layer 의 변경이 *다른 layer 에 영향 최소*

각 layer 가 *완전 추상화* 는 아님 — *leaky abstraction* (아래 layer 의 특성이 위로 누출).

### §1.2 이 장의 *질문*

"내 application 에 *어떤 데이터 모델* 이 자연스러운가?"

답하기 위해 본 장은:
1. *세 모델 의 본질* (relational, document, graph)
2. *각 모델의 query 언어*
3. *언제 무엇을 선택*

→ 이게 *모든 backend engineer 의 매일 결정*.

---

## §2 Relational Model

### §2.1 역사

| 시기 | 사건 |
|--|--|
| 1970 | Edgar Codd 의 *관계형 모델* 제안 (CACM 논문) |
| 1974~ | IBM System R, INGRES 의 *연구 implementation* |
| 1979 | Oracle V2 — 첫 상용 RDBMS |
| 1986 | SQL ANSI 표준 |
| 1990s | RDBMS dominance — Oracle, IBM DB2, MS SQL Server |
| 2000s | PostgreSQL, MySQL 의 *open-source 굴기* |
| 2010s | NoSQL 등장 — *상호보완* 으로 자리 |
| 2020s | PostgreSQL 의 *JSON + vector + full-text* — *one DB to rule them all* 트렌드 |

**도전했지만 패배한 경쟁자들**:
- *Network model* (CODASYL, 1969) — 명시적 pointer
- *Hierarchical model* (IBM IMS) — tree 만
- → Relational 이 *generality + declarative* 로 승리

### §2.2 핵심 — *Relations of tuples*

> *데이터를 relations (= tables) 의 모음* 으로. 각 relation 은 *unordered tuples (= rows)* 의 집합.

**핵심 추상화**:
- *Relation* = *집합 (set)* of tuples
- *Order 무관* — query 가 ORDER BY 로 명시
- *Tuple* = (column, value) 쌍의 집합

**장점**:
- **JOIN** 을 통한 *임의의* 관계 표현
- **SQL** declarative query — *query planner* 가 최적 실행 결정
- 트랜잭션·일관성 보장 (ACID, 7장)
- *Decades of optimization* — query planner, index, locking 의 성숙

### §2.3 SQL 의 *declarative magic*

```sql
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
WHERE u.country = 'KR'
GROUP BY u.name
ORDER BY post_count DESC
LIMIT 10;
```

이 *7-line query* 의 *어떤 실행 계획* 인지 *DB 가 결정*:
- *Index 사용?* — `users.country` 인덱스, `posts.user_id` 인덱스
- *JOIN order?* — users → posts? 또는 그 반대?
- *JOIN algorithm?* — nested loop, hash join, merge join?
- *Parallelism?* — partition pruning, parallel scan
- *Memory?* — sort vs external sort

→ DBA + developer 가 *명시 안 해도* DB 가 *최적 가까이* 도달.

→ Imperative 코드 (예: Java loop) 로 같은 일을 작성하면 — *최적화 모두 직접*.

### §2.4 Relational 의 *적용 도메인*

**잘 맞는 곳**:
- *Business transactions* — 주문, 결제, inventory (ACID 필수)
- *Reporting + analytics* — 복잡한 ad-hoc query
- *Many-to-many* — 소셜 graph 의 *팔로우*, e-commerce 의 *주문↔상품*
- *Strong typing* — schema 가 *constraint*

**잘 안 맞는 곳**:
- *Document-shaped data* — 한 객체의 *복잡 nested tree*
- *Schema 가 자주 변경* — startup 초기, A/B test
- *Massive scale + simple key-value* — Redis, DynamoDB
- *Graph traversal* — 깊은 친구의 친구의 친구

---

## §3 Document Model — NoSQL 의 대표

### §3.1 NoSQL 의 등장 동기

> "NoSQL" 은 2009년 한 mongoDB meetup 의 해시태그에서 시작. *Not Only SQL*.

NoSQL adoption 의 *4가지 driver*:
1. **Scalability** — RDBMS 의 *vertical scaling 한계* 우회 (sharding, replication 내장)
2. **Open source** 선호
3. **Specialized query operations** — graph, full-text 등
4. **Schema flexibility** — *schema-on-read*

**역사적 우연**:
- 2009 의 *cloud + web scale* 폭증
- RDBMS 가 *수평 scaling 약함* (sharding 직접)
- *Google BigTable* (2006), *Amazon Dynamo* (2007) paper 의 영향
- → *new generation* 의 DB 가 *cloud-native* 로 등장

### §3.2 Document database 의 예

| | 발표 | 특징 |
|--|--|--|
| **MongoDB** | 2009 | JavaScript-friendly, BSON, popular |
| **CouchDB** | 2005 | HTTP API, multi-master |
| **RethinkDB** | 2009 | Real-time push (rip 2016) |
| **Espresso** (LinkedIn) | 2013 | Internal, profile data |
| **DynamoDB** | 2012 | AWS managed, hybrid k-v + document |
| **Cosmos DB** | 2017 | Azure multi-model |
| **Firestore** | 2017 | Google, real-time |

자연 형태 — 객체 (예: LinkedIn 프로필) 가 *self-contained JSON document*.

LinkedIn 이력서 예제:

```json
{
  "user_id": 251,
  "first_name": "Bill",
  "last_name": "Gates",
  "positions": [
    {"job_title": "Co-chair", "organization": "Bill & Melinda Gates Foundation"},
    {"job_title": "Co-founder, Chairman", "organization": "Microsoft"}
  ],
  "education": [
    {"school_name": "Harvard University", "start": 1973, "end": 1975}
  ]
}
```

![Figure 2-1 — LinkedIn 프로필을 relational schema 로 표현. 책 p.30](/courses/ddia/figures/ch02/fig-2-1.png)

같은 데이터의 *relational* 표현은 *users, positions, education, contact_info* 등 *여러 table* 로 분산 → JOIN 필요.

### §3.3 Object-Relational Impedance Mismatch

> *애플리케이션의 객체* 와 *관계형 테이블* 사이의 *번역 비용*.

**구체적 예** — Java `User` 클래스:

```java
class User {
    int id;
    String name;
    List<Position> positions;
    List<Education> education;
}
```

이를 relational table 로:

```sql
CREATE TABLE users (id INT, name TEXT);
CREATE TABLE positions (id INT, user_id INT, job_title TEXT, organization TEXT);
CREATE TABLE education (id INT, user_id INT, school_name TEXT, ...);
```

읽으려면 *3 query* 또는 *JOIN*. Application 에서 *재조립*.

**ORM 의 역할** — Hibernate (Java), Django ORM (Python), ActiveRecord (Rails), TypeORM (TS):
- *Mismatch 해소* — 객체와 table 의 *자동 매핑*
- *Lazy loading* — `user.positions` access 시 자동 query
- *Dirty tracking* — 변경된 객체만 UPDATE
- 그러나 *완벽 X* — N+1 query 의 함정, eager vs lazy 의 비용, *ORM-induced abstraction leak*

**JSON document 모델의 장점**:
- **Locality** — 한 query 로 전체 user profile 조회 가능 (JOIN 불필요)
- **Tree 구조 자연 표현** — 부서, 카테고리 등 *1:n* 관계
- **Schema flexibility** — column 추가 시 ALTER TABLE 불필요

### §3.4 한계 — *Many-to-many* 관계

만약 *Bill Gates 의 회사 "Microsoft"* 에 다음을 추가하고 싶다면:
- 회사 자체의 *별도 메타데이터* (logo, 산업)
- 회사 이름의 *normalization* (Microsoft vs Microsoft Corp)
- 같은 학교 (Harvard) 졸업생 *추천*

이때 *회사 / 학교 / 지역* 등이 *별도 entity* 가 되고, 여러 user 가 *공유* (many-to-many) → document 모델로는 어색해짐.

![Figure 2-2 — many-to-many 관계가 등장하면 document 모델의 깔끔함이 깨짐. 책 p.34](/courses/ddia/figures/ch02/fig-2-2.png)

**Document 의 *해법 시도*** + 한계:
- *Embedded denormalization* — 회사 정보 를 *각 user 안에* 복사. 변경 시 *모든 copy 동기화 부담*.
- *Reference + manual JOIN* — `organization_id` 만 저장, 별도 query → *application 이 JOIN 수동 구현*
- *MongoDB `$lookup`* — 후일 추가된 JOIN, *성능 + 표현력 한계*

> **함정 1**: 처음에 *one-to-many* 만 있어 document 로 시작했다가 *many-to-many* 가 등장하면 application code 가 JOIN 을 *수동 구현*. relational 의 강점을 *역으로* 직접 짜는 셈.

### §3.5 Schema-on-Read vs Schema-on-Write

| 모델 | 시점 | 비유 | 변경 비용 |
|--|--|--|--|
| **Schema-on-write** (relational) | write 시 검증 | static type system (compile time) | ALTER TABLE + migration |
| **Schema-on-read** (document) | read 시 application 이 해석 | dynamic type system (runtime) | application 가 *두 형태 모두* 지원 |

**schema-on-read 가 유리한 경우**:
- *Heterogeneous data* — 같은 collection 의 *다른 모양* (예: 다른 타입의 로그)
- *Schema evolution 자주* — startup 초기
- *External data 이미 JSON* — API response 그대로 저장

**schema-on-write 가 유리한 경우**:
- *Homogeneous data* — 모든 row 가 같은 구조
- *Strong consistency 요구*
- *Multiple readers* — schema 가 *문서화* 된 셈

**현실 — Hybrid**:
- PostgreSQL 의 `jsonb` column — *relational + document*
- *Some fields* 가 *strong typed*, *others* 가 *flexible JSON*

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,        -- strict
    profile JSONB              -- flexible
);
```

---

## §4 Document vs Relational — 어떤 걸 선택할까

### §4.1 Document 가 유리한 경우

- 데이터가 *self-contained tree* (예: blog post + comments, e-commerce product + spec)
- *Schema 가 자주 변경* (스타트업 초기, 실험적 feature)
- *Locality* 가 중요 (한 번에 전체 객체 조회)
- *Hierarchical*, no shared references
- 단순 *key-value* (single document lookup)

### §4.2 Relational 이 유리한 경우

- *Many-to-many* 가 많음 (소셜 그래프, 추천)
- *Join 이 많음*
- *Strong typing + consistency* 요구
- *Reporting / analytics* (복잡한 ad-hoc 쿼리)
- *Multiple access patterns* — 다양한 query

### §4.3 *Convergence* — 양쪽이 닮아가는 중

| 방향 | 예 |
|--|--|
| RDBMS → Document | PostgreSQL `jsonb`, MySQL `JSON` type |
| Document → Relational | MongoDB `$lookup` (JOIN), schema validation |
| 둘 다 | Spanner (SQL + horizontal scale), CockroachDB |

**예 — PostgreSQL `jsonb`**:

```sql
SELECT *
FROM products
WHERE properties @> '{"color": "red"}'  -- JSON contains
  AND price < 100;

CREATE INDEX idx_props ON products USING GIN (properties);
```

JSON 안의 *임의 path 의 index* + JOIN + ACID.

> **함정 2**: "NoSQL vs SQL" 의 *대결* 프레임은 옛것. 실용은 *use case 별 적합한 도구* 선택. PostgreSQL + jsonb 가 대부분의 startup 에 충분.

### §4.4 산업 사례 — Use case 별 선택

| App | DB 선택 | 이유 |
|--|--|--|
| E-commerce product catalog | PostgreSQL + jsonb | Many product schemas + ACID |
| Social network | PostgreSQL or Graph DB | Many-to-many (follow) |
| Real-time chat | DynamoDB or Cassandra | Massive write + simple key-value |
| Blog / CMS | MongoDB or PostgreSQL | Document-shaped (post + comments) |
| Financial transactions | PostgreSQL / Oracle | ACID + audit |
| Sensor / IoT data | TimescaleDB / InfluxDB | Time-series specialized |
| Logging / observability | Elasticsearch / Loki | Full-text + aggregation |
| Session store | Redis | In-memory + TTL |
| Embedding / RAG | pgvector / Pinecone | Vector similarity |

---

## §5 Query Languages

### §5.1 Imperative vs Declarative

**Imperative** (어떻게 할지 명시):
```python
def get_sharks(animals):
    sharks = []
    for animal in animals:
        if animal.family == "Sharks":
            sharks.append(animal)
    return sharks
```

**Declarative** (무엇을 원하는지만 명시):
```sql
SELECT * FROM animals WHERE family = 'Sharks';
```

**Declarative 의 장점**:
- *Brevity* — 짧음
- *최적화 자유* — DB 의 query planner 가 *index 선택, JOIN 순서* 등 자동 결정
- *Parallelism 친화* — 순서를 명시 안 하니 병렬 분산 쉬움
- *Evolution* — index 추가, partition 변경 시 *query 그대로*

**Imperative 의 가치**:
- *복잡 logic* — declarative 로 표현 어려운 case
- *Performance critical* — fine-grained 제어 필요 시
- *Stateful processing* — streaming, ML

→ 현대 — declarative 가 *default*, imperative 가 *escape hatch*.

### §5.2 Declarative on the Web — CSS 비유

**Imperative DOM 조작**:
```js
const links = document.querySelectorAll('a');
links.forEach(link => {
    if (link.classList.contains('selected')) {
        link.style.backgroundColor = 'blue';
    }
});
```

**Declarative CSS**:
```css
a.selected { background-color: blue; }
```

→ Browser 가 *어떻게 적용할지* 결정 + re-render 자동 + CSS engine 최적.

→ *Declarative 의 패턴* 이 *전 컴퓨팅 분야* 에서 동일.

### §5.3 MapReduce Query (MongoDB 예제)

MongoDB 의 *aggregation* — 함수형 + declarative:

```javascript
db.observations.mapReduce(
  function map() { emit(this.family, this.numAnimals); },
  function reduce(key, values) { return Array.sum(values); },
  { query: { observationTimestamp: { $gte: ISODate("2013-12-01") } },
    out: "monthlyTotals" }
);
```

이 패턴이 10장 (batch processing) 의 MapReduce 와 동일. *데이터 가까이* 가서 계산.

**MapReduce 의 본질**:
- *map* — 각 record 의 *(key, value)* emit
- *shuffle* — same key 의 value 모음
- *reduce* — value list 의 aggregation
- → *parallelism* 의 자연 표현 (Hadoop, Spark)

이후 MongoDB 가 *aggregation pipeline* 을 도입 — SQL 의 declarative 와 *비슷*:

```javascript
db.observations.aggregate([
  { $match: { family: "Sharks" } },
  { $group: { _id: "$species", count: { $sum: 1 } } }
]);
```

> 패턴 — *NoSQL 도 결국 SQL 의 declarative 패러다임* 으로 수렴.

### §5.4 SQL 의 *현대 발전*

**Window functions** (SQL:2003):
```sql
SELECT name, salary,
  AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

**Common Table Expressions** (CTE, SQL:1999):
```sql
WITH recent_orders AS (
  SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '7 days'
)
SELECT user_id, COUNT(*) FROM recent_orders GROUP BY user_id;
```

**Recursive CTE** (graph traversal):
```sql
WITH RECURSIVE ancestors AS (
  SELECT id, parent_id FROM categories WHERE id = 42
  UNION ALL
  SELECT c.id, c.parent_id FROM categories c
  JOIN ancestors a ON c.id = a.parent_id
)
SELECT * FROM ancestors;
```

→ SQL 이 *graph query* 도 가능. 그러나 표기가 *번거로움* → graph DB 의 우위 영역.

---

## §6 Graph-Like Data Models

### §6.1 동기 — *many-to-many* 가 *지배적* 일 때

소셜 그래프, 웹 페이지, 도로망, 단백질 상호작용 — *연결* 자체가 데이터.

**산업 예**:
- *Social network* — Facebook (~3B nodes, ~500B edges)
- *Recommendation* — Amazon, Netflix (collaborative filtering)
- *Knowledge graph* — Google search, Wikipedia
- *Fraud detection* — banking (suspicious transfer paths)
- *Supply chain* — manufacturing, logistics
- *Bioinformatics* — protein interaction, drug discovery

**vertices (= nodes)** + **edges (= relationships)** + **각각의 properties** 로 구성.

### §6.2 Property Graph 모델

**Neo4j, Titan, InfiniteGraph, JanusGraph, Amazon Neptune** 등의 모델:

```cypher
CREATE
  (lucy:Person {name: 'Lucy'}),
  (idaho:Location {name: 'Idaho', type: 'state'}),
  (us:Location {name: 'United States', type: 'country'}),
  (lucy)-[:BORN_IN]->(idaho),
  (idaho)-[:WITHIN]->(us)
```

![Figure 2-5 — 한 가족의 person + location graph. 책 p.50](/courses/ddia/figures/ch02/fig-2-5.png)

**구조**:
- **Vertex** = node, with *label* (`:Person`) + *properties* (key-value)
- **Edge** = directed relationship, with *label* (`:BORN_IN`) + *properties*

**관계 모델과 비교**:
- Relation: *table per type*
- Graph: *flexible* — 새 node type 추가 시 schema 변경 *불필요*
- 모든 edge 가 *first-class* — 새 edge type 추가 자유

### §6.3 Cypher Query Language

Neo4j 의 declarative graph query:

```cypher
MATCH (person)-[:BORN_IN]->()-[:WITHIN*0..]->(us:Location {name: 'United States'}),
      (person)-[:LIVES_IN]->()-[:WITHIN*0..]->(eu:Location {name: 'Europe'})
RETURN person.name
```

> *미국 출생 + 현재 유럽 거주* 인 사람 찾기. `[:WITHIN*0..]` 가 *0회 이상* WITHIN 관계로 transitive closure.

같은 query 를 SQL 로:

```sql
WITH RECURSIVE
  in_usa(vertex_id) AS (
    SELECT vertex_id FROM vertices WHERE properties->>'name' = 'United States'
    UNION
    SELECT edges.tail_vertex FROM edges
      JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
      WHERE edges.label = 'within'
  ),
  in_europe(vertex_id) AS ( ... 유사 ... ),
  born_in_usa AS ( ... ),
  lives_in_europe AS ( ... )
SELECT vertices.properties->>'name'
FROM vertices
  JOIN born_in_usa ON vertices.vertex_id = born_in_usa.vertex_id
  JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;
```

→ **graph query 가 압도적으로 짧고 명료**. *recursive CTE* 가 가능하지만 표기가 번거로움.

**Cypher 의 핵심**:
- *Pattern matching* — `(a)-[:KNOWS]->(b)` 패턴이 *visual*
- *Variable-length path* — `*0..3` (0~3 hop), `*` (무한)
- *ASCII art* 같은 표기 — 학습 용이

### §6.4 Triple-Stores 와 SPARQL

각 사실을 *(subject, predicate, object)* 의 *3-tuple* 로:

```turtle
@prefix : <urn:example:>.
:lucy :born_in :idaho.
:lucy :marriedTo :alain.
:idaho :within :usa.
```

**RDF (Resource Description Framework)** — W3C 표준.

SPARQL query:
```sparql
SELECT ?personName WHERE {
  ?person :name ?personName ;
          :born_in / :within* / :name "United States" ;
          :lives_in / :within* / :name "Europe" .
}
```

**W3C 의 *Semantic Web* 비전** — 모든 웹 데이터를 RDF triple 로 → universal knowledge graph. 학계 적극, 산업 미적용.

**실제 적용**:
- *Wikidata* — Wikipedia 의 structured data, RDF
- *DBpedia* — Wikipedia → RDF 추출
- *Google Knowledge Graph* — 부분적 RDF
- *생명과학 ontology* — Gene Ontology, MeSH

### §6.5 Property Graph vs Triple-Store

| | Property Graph | Triple-Store |
|--|--|--|
| Unit | Vertex / Edge | Triple (S, P, O) |
| Properties | Vertex/Edge 의 K-V | 또 다른 triple |
| 표현력 | 같음 | 같음 |
| 표기 | 직관적, ASCII art | 형식적, 학술적 |
| Schema | Flexible labels | RDF Schema, OWL |
| Query | Cypher (Neo4j), Gremlin | SPARQL |
| Reasoning | 약함 | 강함 (ontology inference) |
| 산업 채택 | 강함 | 약함 (학계 위주) |

### §6.6 Datalog — 학술적 베이스

Prolog 의 deductive 서브셋. 위 query 가:

```prolog
within_recursive(Location, Name) :- name(Location, Name).
within_recursive(Location, Name) :- within(Location, Via), within_recursive(Via, Name).

migrated(Name, BornIn, LivingIn) :-
  name(Person, Name),
  born_in(Person, BornLoc), within_recursive(BornLoc, BornIn),
  lives_in(Person, LivingLoc), within_recursive(LivingLoc, LivingIn).
```

Cascalog, Datomic 등이 실용 구현. *Cypher / SPARQL 보다 더 추상적* 이지만 큰 query 의 *분해* 에 유용.

---

## §7 세 모델 비교

| 모델 | 강점 | 약점 | 예시 |
|--|--|--|--|
| **Relational** | JOIN, ACID, 표준 SQL | impedance mismatch, schema 경직 | PostgreSQL, MySQL |
| **Document** | locality, schema flex | many-to-many, JOIN | MongoDB, CouchDB |
| **Graph** | 깊은 관계 traversal | 단순 query 도 오버헤드 | Neo4j, AWS Neptune |

**선택 가이드**:
- 데이터의 *내재적 구조* 가 무엇인가? Tree → document. Graph → graph. Relational → relational.
- *Query pattern* 이 어떻게 되나? Aggregation → relational. Traversal → graph.

### §7.1 *Polyglot persistence* — 실제 production

> **함정 3**: 한 시스템에 *모두 다 시도*. 보통 *하나의 primary store + secondary specialized index* 가 표준.

**예 — 중급 SaaS startup 의 데이터 스택**:
- *PostgreSQL* — primary OLTP (user, order, billing)
- *Elasticsearch* — full-text + search aggregation
- *Redis* — session, rate limit, hot cache
- *S3* — file (image, log archive)
- *ClickHouse* — analytics (event tracking)
- *Pinecone / pgvector* — embedding search (LLM era)

→ 각 store 가 *자기 강점의 work*. *데이터 sync* 가 핵심 challenge (CDC, event-driven).

### §7.2 Future — *Unified data system*

12장 의 vision — *one DB that does all*:
- *PostgreSQL 의 확장* — JSON + vector + full-text + time-series + graph
- *SurrealDB* — multi-model (document + graph + relational)
- *Foundation DB* — layered architecture
- *EdgeDB* — relational + object-oriented

→ *각 store 의 sync 복잡도* 회피 + *polyglot 의 장점 유지*.

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | one-to-many → many-to-many 진화 무시 | document 로 시작했어도 evolution 가능성 미리 평가 |
| 2 | "NoSQL = no SQL" | 결국 declarative aggregation 으로 수렴 |
| 3 | schema-on-read = no schema | *암묵적* schema 는 코드 전체에 존재. 일관성 어려움 |
| 4 | RDBMS 가 always slow | indexing + read replica 로 충분히 빠른 경우 대부분 |
| 5 | Document 가 항상 *locality 좋음* | document 가 자주 *수정* 되면 location 깨짐 (storage engine 의 fragment 화) |
| 6 | Graph DB = social network 만 | 추천, fraud 탐지, supply chain, 의료 ontology 등 광범위 |
| 7 | SPARQL > Cypher (또는 반대) | 같은 표현력. 선호도 + ecosystem 차이 |
| 8 | "Relational vs NoSQL" dichotomy | 실제 production 은 polyglot persistence |
| 9 | MapReduce 가 효율적 | 표현이 어색. aggregation pipeline 이 표준 |
| 10 | impedance mismatch 가 *항상 큼* | ORM (Hibernate, Django ORM, ActiveRecord) 가 대부분 해결 |
| 11 | jsonb 사용 = NoSQL 효과 | jsonb 는 strict typing 없음. *indexing 전략* 필요 |
| 12 | Graph DB = 항상 빠름 | 작은 query 의 *fixed overhead* 큼. 단순 lookup 은 K-V 가 빠름 |

---

## §9 자가점검

1. *Relational, document, graph* 세 모델의 *근본적 차이*?
2. *Schema-on-read* vs *schema-on-write* — 각각 *type system* 에 비유?
3. *Impedance mismatch* 의 정의 + document 모델이 어떻게 해결?
4. *Many-to-many* 관계가 발생하면 document 모델에 어떤 문제?
5. *Locality* 의 의미 + document 모델의 *장단점*?
6. *Declarative* 와 *imperative* query 의 차이 + declarative 의 *3 가지 이점*?
7. *Property graph* 와 *triple-store* 의 차이?
8. *Cypher* / *SPARQL* / *Datalog* 의 *공통 query pattern*?
9. *NoSQL 채택 4 driver*?
10. 실제 production 의 *polyglot persistence* 의미?
11. *PostgreSQL `jsonb`* 가 *왜 hybrid* 의 해답?
12. *Recursive CTE* 의 *graph DB 대비 한계*?

<details><summary>해답 (간략)</summary>

1. Relational: tuples + JOIN. Document: tree-shaped self-contained. Graph: vertices + edges, traversal first-class.
2. Write: static type (compile-time). Read: dynamic type (runtime).
3. 객체와 table 의 번역 비용. Document 는 객체와 같은 tree 로 *번역 없음*.
4. Document 가 *반복·중복* 됨, application 이 JOIN 수동 구현, 일관성 깨짐.
5. 한 query 로 객체 전체 조회. 잦은 수정에 fragmentation 위험.
6. *무엇* 만 명시. Brevity + 최적화 자유 + 병렬 친화 + evolution 친화.
7. Property graph: vertex/edge 에 *property* (key-value). Triple-store: (S, P, O) 의 3-tuple.
8. *Variable-length path* (Cypher `*`, SPARQL `*`, Datalog 의 recursive rule).
9. Scalability, OSS, specialized query, schema flexibility.
10. 하나의 primary store + 여러 specialized index/cache (PostgreSQL + Elasticsearch + Redis 등).
11. Relational ACID + JOIN + document flexibility 동시. *Strict fields + flexible JSON column*.
12. 표기 *번거로움* (CTE 의 boilerplate), *최적화 약함* (graph DB 의 traversal 가 더 빠름).

</details>

---

## §10 다음 학습으로

- **3장 (Storage and Retrieval)** — 위 모델들의 *내부 구조*. B-tree vs LSM-tree, hash index, column store.
- **4장 (Encoding and Evolution)** — schema migration 의 *forward/backward compatibility*.
- **7장 (Transactions)** — relational 의 ACID 가 distributed 환경에서 *얼마나 변하는지*.
- **12장 (Future)** — graph + document + relational 의 *unified data system*.

---

## §11 한 줄 요약

> **데이터 모델 = 사고 도구. Relational (JOIN + ACID) / Document (locality + flex) / Graph (relationship first-class). *Many-to-many* 가 *결정 기준*. Declarative > Imperative — DB 가 optimization. NoSQL 의 4 driver + *역사적 우연*. 실제 production = polyglot persistence.**
