# Chapter 2: Data Models and Query Languages — 학습 노트

> *Designing Data-Intensive Applications* (Kleppmann, 2017) **Chapter 2** (책 p.27~64, PDF p.49~90).
> 2장의 핵심: 데이터 모델은 *소프트웨어를 어떻게 생각하는가* 의 토대. **Relational / Document / Graph** 세 모델의 *각 특성과 적합한 도메인*.

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

## 1. Data Model 의 *층화*

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

---

## 2. Relational Model

### 2.1 역사

- 1970년 Edgar Codd 의 *관계형 모델* 제안
- 1980년대 Oracle, IBM DB2, MS SQL Server 의 *상용화*
- 도전했지만 패배한 경쟁자들: network model (CODASYL), hierarchical model
- 2010년대 NoSQL 등장 — *상호보완* 으로 자리잡음 (relational 대체 X)

### 2.2 핵심

> *데이터를 relations (= tables) 의 모음* 으로. 각 relation 은 *unordered tuples (= rows)* 의 집합.

장점:
- **JOIN** 을 통한 *임의의* 관계 표현
- **SQL** declarative query — *query planner* 가 최적 실행 결정
- 트랜잭션·일관성 보장 (ACID, 7장)

---

## 3. Document Model — NoSQL 의 대표

### 3.1 NoSQL 의 등장 동기

> "NoSQL" 은 2009년 한 mongoDB meetup 의 해시태그에서 시작. *Not Only SQL*.

NoSQL adoption 의 *4가지 driver*:
1. **Scalability** — RDBMS 의 *vertical scaling 한계* 우회 (sharding, replication 내장)
2. **Open source** 선호
3. **Specialized query operations** — graph, full-text 등
4. **Schema flexibility** — *schema-on-read*

### 3.2 Document database 의 예

- **MongoDB**, **CouchDB**, **RethinkDB**, **Espresso** (LinkedIn)
- **자연 형태** — 객체 (예: LinkedIn 프로필) 가 *self-contained JSON document*

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

### 3.3 Object-Relational Impedance Mismatch

> *애플리케이션의 객체* 와 *관계형 테이블* 사이의 *번역 비용*.

JSON document 모델의 장점:
- **Locality** — 한 query 로 전체 user profile 조회 가능 (JOIN 불필요)
- **Tree 구조 자연 표현** — 부서, 카테고리 등 *1:n* 관계
- **Schema flexibility** — column 추가 시 ALTER TABLE 불필요

### 3.4 한계 — *Many-to-many* 관계

만약 *Bill Gates 의 회사 "Microsoft"* 에 다음을 추가하고 싶다면:
- 회사 자체의 *별도 메타데이터* (logo, 산업)
- 회사 이름의 *normalization* (Microsoft vs Microsoft Corp)
- 같은 학교 (Harvard) 졸업생 *추천*

이때 *회사 / 학교 / 지역* 등이 *별도 entity* 가 되고, 여러 user 가 *공유* (many-to-many) → document 모델로는 어색해짐.

![Figure 2-2 — many-to-many 관계가 등장하면 document 모델의 깔끔함이 깨짐. 책 p.34](/courses/ddia/figures/ch02/fig-2-2.png)

> **함정 1**: 처음에 *one-to-many* 만 있어 document 로 시작했다가 *many-to-many* 가 등장하면 application code 가 JOIN 을 *수동 구현*. relational 의 강점을 *역으로* 직접 짜는 셈.

### 3.5 Schema-on-Read vs Schema-on-Write

| 모델 | 시점 | 비유 |
|--|--|--|
| **Schema-on-write** (relational) | write 시 검증 | static type system (compile time) |
| **Schema-on-read** (document) | read 시 application 이 해석 | dynamic type system (runtime) |

schema-on-read 가 더 유연하지만 *암묵적 schema* 가 *코드 전체* 에 흩어져 일관성 보장 어려움. *evolution* 시: schema-on-write 는 ALTER TABLE + migration, schema-on-read 는 application 이 *두 형태 모두* 지원하는 코드 작성.

---

## 4. Document vs Relational — 어떤 걸 선택할까

### 4.1 Document 가 유리한 경우

- 데이터가 *self-contained tree* (예: blog post + comments, e-commerce product + spec)
- *Schema 가 자주 변경* (스타트업 초기, 실험적 feature)
- *Locality* 가 중요 (한 번에 전체 객체 조회)

### 4.2 Relational 이 유리한 경우

- *Many-to-many* 가 많음 (소셜 그래프, 추천)
- *Join 이 많음*
- *Strong typing + consistency* 요구
- *Reporting / analytics* (복잡한 ad-hoc 쿼리)

### 4.3 *Convergence* — 양쪽이 닮아가는 중

- RDBMS: PostgreSQL/MySQL 이 **JSON column** 지원 (PostgreSQL 의 `jsonb`)
- Document DB: MongoDB 가 **`$lookup`** 으로 JOIN 지원
- → 미래의 *hybrid 모델* 등장 가능성

> **함정 2**: "NoSQL vs SQL" 의 *대결* 프레임은 옛것. 실용은 *use case 별 적합한 도구* 선택. PostgreSQL + jsonb 가 대부분의 startup 에 충분.

---

## 5. Query Languages

### 5.1 Imperative vs Declarative

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

장점:
- *Brevity* — 짧음
- *최적화 자유* — DB 의 query planner 가 *index 선택, JOIN 순서* 등 자동 결정
- *Parallelism 친화* — 순서를 명시 안 하니 병렬 분산 쉬움

### 5.2 MapReduce Query (MongoDB 예제)

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

이후 MongoDB 가 *aggregation pipeline* 을 도입 — SQL 의 declarative 와 *비슷*:

```javascript
db.observations.aggregate([
  { $match: { family: "Sharks" } },
  { $group: { _id: "$species", count: { $sum: 1 } } }
]);
```

> 패턴 — *NoSQL 도 결국 SQL 의 declarative 패러다임* 으로 수렴.

---

## 6. Graph-Like Data Models

### 6.1 동기 — *many-to-many* 가 *지배적* 일 때

소셜 그래프, 웹 페이지, 도로망, 단백질 상호작용 — *연결* 자체가 데이터.

**vertices (= nodes)** + **edges (= relationships)** + **각각의 properties** 로 구성.

### 6.2 Property Graph 모델

**Neo4j, Titan, InfiniteGraph** 등의 모델:

```cypher
CREATE
  (lucy:Person {name: 'Lucy'}),
  (idaho:Location {name: 'Idaho', type: 'state'}),
  (us:Location {name: 'United States', type: 'country'}),
  (lucy)-[:BORN_IN]->(idaho),
  (idaho)-[:WITHIN]->(us)
```

![Figure 2-5 — 한 가족의 person + location graph. 책 p.50](/courses/ddia/figures/ch02/fig-2-5.png)

### 6.3 Cypher Query Language

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

### 6.4 Triple-Stores 와 SPARQL

각 사실을 *(subject, predicate, object)* 의 *3-tuple* 로:

```turtle
@prefix : <urn:example:>.
:lucy :born_in :idaho.
:lucy :marriedTo :alain.
:idaho :within :usa.
```

SPARQL query:
```sparql
SELECT ?personName WHERE {
  ?person :name ?personName ;
          :born_in / :within* / :name "United States" ;
          :lives_in / :within* / :name "Europe" .
}
```

W3C 의 *Semantic Web* 비전 — 모든 웹 데이터를 RDF triple 로 → universal knowledge graph. 학계 적극, 산업 미적용.

### 6.5 Datalog — 학술적 베이스

Prolog 의 deductive 서브셋. 위 query 가:

```prolog
within_recursive(Location, Name) :- name(Location, Name).
within_recursive(Location, Name) :- within(Location, Via), within_recursive(Via, Name).

migrated(Name, BornIn, LivingIn) :-
  name(Person, Name),
  born_in(Person, BornLoc), within_recursive(BornLoc, BornIn),
  lives_in(Person, LivingLoc), within_recursive(LivingLoc, LivingIn).

migrated(Who, 'United States', 'Europe')?  % 질의
```

Cascalog, Datomic 등이 실용 구현. *Cypher / SPARQL 보다 더 추상적* 이지만 큰 query 의 *분해* 에 유용.

---

## 7. 세 모델 비교

| 모델 | 강점 | 약점 | 예시 |
|--|--|--|--|
| **Relational** | JOIN, ACID, 표준 SQL | impedance mismatch, schema 경직 | PostgreSQL, MySQL |
| **Document** | locality, schema flex | many-to-many, JOIN | MongoDB, CouchDB |
| **Graph** | 깊은 관계 traversal | 단순 query 도 오버헤드 | Neo4j, AWS Neptune |

선택 가이드:
- 데이터의 *내재적 구조* 가 무엇인가? Tree → document. Graph → graph. Relational → relational.
- *Query pattern* 이 어떻게 되나? Aggregation → relational. Traversal → graph.

> **함정 3**: 한 시스템에 *모두 다 시도*. 보통 *하나의 primary store + secondary specialized index* 가 표준. 예: PostgreSQL primary + Elasticsearch full-text + Redis cache.

---

## 자주 빠지는 함정

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
| 10 | impedance mismatch 가 *항상 큼* | ORM (Hibernate, Django ORM, Active Record) 가 대부분 해결 |

---

## 자가점검

1. *Relational, document, graph* 세 모델의 *근본적 차이*.
2. *Schema-on-read* vs *schema-on-write* — 각각 *type system* 에 비유.
3. *Impedance mismatch* 의 정의 + document 모델이 어떻게 해결.
4. *Many-to-many* 관계가 발생하면 document 모델에 어떤 문제.
5. *Locality* 의 의미 + document 모델의 *장단점*.
6. *Declarative* 와 *imperative* query 의 차이 + declarative 의 *3 가지 이점*.
7. *Property graph* 와 *triple-store* 의 차이.
8. *Cypher* / *SPARQL* / *Datalog* 의 *공통 query pattern* (transitive closure).
9. *NoSQL 채택 4 driver*.
10. 실제 production 의 *polyglot persistence* 의미.

### 해답 (간략)

1. Relational: tuples + JOIN. Document: tree-shaped self-contained. Graph: vertices + edges.
2. Write: static type. Read: dynamic type.
3. 객체와 table 의 번역 비용. document 는 객체와 같은 tree 로 *번역 없음*.
4. document 가 *반복·중복* 됨, application 이 JOIN 수동 구현, 일관성 깨짐.
5. 한 query 로 객체 전체 조회. 잦은 수정에 fragmentation 위험.
6. *무엇* 만 명시. Brevity + 최적화 자유 + 병렬 친화.
7. Property graph: vertex/edge 에 *property* (key-value). Triple-store: (s, p, o) 의 3-tuple.
8. *Variable-length path* (Cypher `*`, SPARQL `*`, Datalog 의 recursive rule).
9. scalability, OSS, specialized query, schema flexibility.
10. 하나의 primary store + 여러 specialized index/cache (Postgres + Elasticsearch + Redis 등).

---

## 다음 학습으로

- **3장 (Storage and Retrieval)** — 위 모델들의 *내부 구조*. B-tree vs LSM-tree, hash index, column store.
- **4장 (Encoding and Evolution)** — schema migration 의 *forward/backward compatibility*.
- **7장 (Transactions)** — relational 의 ACID 가 distributed 환경에서 *얼마나 변하는지*.
- **12장 (Future)** — graph + document + relational 의 *unified data system*.
