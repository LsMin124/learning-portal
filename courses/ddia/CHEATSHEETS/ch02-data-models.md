# Ch 2 Data Models — 치트시트

## TL;DR

- **3 가지 모델**: Relational (JOIN), Document (tree), Graph (vertices+edges)
- **선택 기준**: 데이터의 *내재적 구조* + *query pattern*
- **NoSQL 4 driver**: scalability, OSS, specialized query, schema flexibility
- **Document vs Relational**: many-to-many 가 분기점. 처음 one-to-many 면 document, many-to-many 면 relational
- **Schema-on-read** (document) = dynamic type. **schema-on-write** (relational) = static type
- **Query**: imperative (어떻게) vs declarative (무엇). Cypher/SPARQL/Datalog 는 graph 의 declarative
- **Convergence**: PostgreSQL jsonb + MongoDB `$lookup` — 양쪽이 닮아가는 중

---

## Quick Reference

### 표 1. 세 모델 비교

| 모델 | 강점 | 약점 | 예시 |
|--|--|--|--|
| Relational | JOIN, ACID, 표준 SQL | impedance mismatch, 경직 schema | Postgres, MySQL |
| Document | locality, schema flex | many-to-many, JOIN | MongoDB, CouchDB |
| Graph | 깊은 traversal | 단순 query 오버헤드 | Neo4j, Neptune |

### 표 2. Schema-on-Read vs Write

| | Read (document) | Write (relational) |
|--|--|--|
| 비유 | dynamic type | static type |
| Evolution | application 코드 *지속 cost* | ALTER TABLE *일회성 cost* |
| 적합 | 빠른 prototyping, log/event | strong consistency, reporting |

### 표 3. NoSQL 4 driver

| Driver | 사용 사례 |
|--|--|
| Scalability | IoT, SaaS, big write |
| Open source | startup, 라이센스 회피 |
| Specialized | graph, full-text, 시계열 |
| Schema flex | prototype, 빈번 변경 |

### 표 4. Query language 종류

| 언어 | 패러다임 | 모델 |
|--|--|--|
| SQL | declarative | relational |
| MongoDB find/aggregate | declarative (점차) | document |
| Cypher | declarative graph | property graph (Neo4j) |
| SPARQL | declarative graph | RDF triple-store |
| Datalog | rule-based recursive | abstract (Datomic, Cascalog) |

### 표 5. Graph query 공통 pattern

```
Cypher: (start)-[:REL*0..]->(end)
SPARQL: ?start (:rel)*  ?end
Datalog: rec(X, Y) :- rel(X, Y).
         rec(X, Y) :- rel(X, M), rec(M, Y).
```

= *variable-length path / transitive closure*. SQL 의 recursive CTE 대비 **수배~수십배** 짧음.

### 표 6. Polyglot persistence 패턴

```
Primary RDBMS (Postgres)
     |
     +-- CDC --> Elasticsearch  (search)
     +-- CDC --> Neo4j          (recommend)
     +-- write --> Redis        (cache)
     +-- ETL  --> BigQuery      (analytics)
```

source-of-truth 는 RDBMS, 나머지는 derived. (4장 + 11장)

---

## Mind Map

```
2장 Data Models
├─ 1. 층화: app → storage model → engine → hw
├─ 2. Relational (Codd 1970)
│   └─ JOIN, ACID, SQL declarative
├─ 3. Document (NoSQL)
│   ├─ MongoDB / CouchDB
│   ├─ locality (self-contained)
│   ├─ impedance mismatch 해결
│   └─ many-to-many 에 약함
├─ 4. Relational vs Document 선택
│   ├─ tree 구조 → document
│   ├─ many-to-many → relational
│   └─ convergence (jsonb, $lookup)
├─ 5. Query languages
│   ├─ imperative vs declarative
│   └─ MapReduce → aggregation pipeline
└─ 6. Graph
    ├─ Property graph + Cypher (Neo4j)
    ├─ Triple-store + SPARQL (RDF, Semantic Web)
    └─ Datalog (recursive rule)
```

---

## Decision Tree (데이터 모델 선택)

```
Q1. 데이터가 self-contained tree 인가? (e.g., blog+comments)
    YES → Document
    NO  → Q2

Q2. Many-to-many 가 많은가? (e.g., social graph, 추천)
    NO  → Document or Relational (취향)
    YES → Q3

Q3. Variable-depth traversal 이 자주 있나?
    NO  → Relational
    YES → Graph

Q4. 그래도 잘 모르겠다?
    → PostgreSQL + jsonb 로 시작. 측정 후 specialized DB 추가.
```

---

## 1-line summary per section

| 절 | 한 줄 |
|--|--|
| 1 | 데이터 모델은 abstraction layer |
| 2 | Relational: JOIN, ACID, declarative SQL |
| 3 | Document: tree, locality, schema flex. many-to-many 약함 |
| 4 | 선택은 데이터 shape + query pattern. convergence 진행 중 |
| 5 | Declarative 가 brevity + 최적화 자유. MapReduce → aggregation |
| 6 | Graph: vertices/edges + Cypher/SPARQL/Datalog. variable-depth 정답 |
