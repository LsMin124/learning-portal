# Chapter 4: Encoding and Evolution — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 4** (책 p.111~150, PDF p.133~166).
> 4장의 핵심: 데이터를 *시스템 사이* (디스크, 네트워크, 다른 process) 로 *어떻게 옮기는가*. 그리고 *시간에 따라 schema 가 변할 때* 옛 코드와 새 코드가 *공존* 하는 방법.

이 장의 *지적 무게중심*:
1. **Encoding = memory ↔ bytes** — 모든 system boundary 의 *공통 문제*
2. **Schema evolution** — *옛 + 새 코드 가 공존* 시 의 호환성
3. **Forward vs Backward compatibility** — 두 방향 모두 필요
4. **Protobuf, Avro, Thrift** — *각자의 trade-off*
5. **Dataflow 3 패턴** — DB / Service / Message passing

---

## 들어가기 전에

- **선수 지식**: JSON·XML, REST API, RPC 의 존재. 2장의 data model.
- **학습 목표**
  1. *Encoding* 의 정의 — in-memory 객체 ↔ byte sequence
  2. **JSON/XML/CSV** vs **binary (Thrift, Protobuf, Avro)** — schema 와 evolution
  3. **Forward / Backward compatibility** — 다른 version 의 코드가 *같은 데이터* 다룰 때
  4. **Database 의 encoding** — schema-on-read, schema migration
  5. **Service communication** — REST, RPC, gRPC, GraphQL
  6. **Message-passing** — Kafka, RabbitMQ — *async + decoupled*
- **예상 학습 시간**: 100~130분

---

## §1 Encoding 의 두 표현

데이터는 두 표현 사이를 움직임:

| 표현 | 어디서 | 형태 |
|--|--|--|
| **In-memory** | 실행 중 process | 객체, struct, list, hash table (pointer-based) |
| **Bytes** | 디스크, 네트워크, IPC | 일관된 byte sequence |

변환:
- **Encoding** (= serialization, marshalling): memory → bytes
- **Decoding** (= deserialization, unmarshalling, parsing): bytes → memory

### §1.1 Schema evolution 의 *왜*

> *같은 시스템이 옛 코드 + 새 코드 가 동시에 동작* 하는 시기.

**시나리오**:
- **Rolling upgrade** (server) — N 대 server 중 *부분 upgrade* 동안 *옛 + 새 version* 동시 동작
- **Mobile app** — 옛 version 사용자가 *서비스 중지 후 까지* 사용
- **Long-lived data** — DB 의 옛 row 가 *수년 후 새 코드로* 읽힘
- **External API** — third-party 가 *옛 schema* 의존

→ Encoding format 의 *evolution 호환성* 이 핵심.

### §1.2 *두 방향* compatibility

**Forward compatibility**:
- *옛 코드 가 새 data 읽음*
- "내가 모르는 field 가 있어도 OK"

**Backward compatibility**:
- *새 코드 가 옛 data 읽음*
- "옛 data 에 없는 field 는 default"

→ Rolling upgrade 시 *두 방향 모두 필요*.

---

## §2 Language-specific encoding

Java 의 `java.io.Serializable`, Python 의 `pickle`, Ruby 의 `Marshal`, .NET 의 `BinaryFormatter` 등.

**장점**: 같은 언어 안에서 *single line* 으로 객체 ↔ bytes.

**단점** (책의 강력한 경고):
1. **언어 lock-in** — Java pickle 을 Python 으로 못 읽음
2. **Security** — pickle 같은 generic deserialization 은 *임의 코드 실행* 공격 표적
3. **Version 호환성 처리가 약함** — 같은 언어 안에서도 class 변경 시 깨짐
4. **효율성** — 보통 binary 표준 (Protobuf, Avro) 대비 *느리고 큼*

**책의 결론**: language-specific encoding 은 *임시·인-프로세스* 외엔 사용 금지.

**실제 사고 사례**:
- Java RMI 의 Serializable — *exploit* 의 표적 (Apache Commons Collections 등)
- Python pickle — *제 3 자 source 의 pickle decode = code execution*
- .NET BinaryFormatter — Microsoft 가 *deprecated* (2020)

---

## §3 JSON, XML, CSV — Textual Formats

### §3.1 장점

- *Human-readable*
- 거의 모든 언어가 native parser
- *Schema 없음* — flexibility
- *Web 의 lingua franca* — REST API 의 사실상 표준

### §3.2 한계

| 한계 | 영향 |
|--|--|
| **숫자의 모호함** | JSON 의 number 가 int/float 구분 X. JS 는 IEEE 754 double 만 — 2^53 초과 정수 손실 |
| **Binary data 표현** | base64 인코딩 (33% 공간 낭비) |
| **Schema 부재** | application 코드가 schema 를 *암묵* 으로 가짐 → 일관성 어려움 |
| **CSV 의 한계** | quoting, escape, encoding 등 standardization 부재 |
| **Verbosity** | field 이름이 *모든 row 마다 반복* — 공간 낭비 |

### §3.3 JSON Schema

JSON 에 schema 부여: JSON Schema, OpenAPI/Swagger, AsyncAPI.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer", "minimum": 0}
  },
  "required": ["name"]
}
```

*외부 validation* 만 — encoding 자체엔 schema 정보 없음.

**산업 활용**:
- *OpenAPI* — REST API spec, code generation (openapi-generator)
- *AsyncAPI* — event-driven API
- *JSON Schema* — config 검증, form validation

### §3.4 비교 — JSON 의 *지속성*

JSON 의 *수많은 문제* 에도 *지배적* 인 이유:
- *Browser 의 native* (JS object 그대로)
- *Debugging 쉬움* — 사람이 읽음
- *Tooling* — jq, json viewer, IDE support
- *REST API 의 호환성*

→ Backend 간 binary, frontend 와 JSON 의 *hybrid* 가 표준.

---

## §4 Binary Encoding

### §4.1 동기

text encoding 의 *문제 해결*:
- *작음* — 같은 데이터를 더 적은 byte 로
- *빠름* — parsing 빠름
- *schema-driven* — 명시적 type, 호환성 도구 자체 포함

### §4.2 MessagePack, BSON, CBOR — schema-less binary

JSON 을 그대로 binary 화. Schema 여전히 없음.

```
record JSON     {"userName": "Martin", "favoriteNumber": 1337, ...}
MessagePack     83 a8 75 73 65 72 4e 61 6d 65 a6 4d 61 72 74 69 6e ...
```

작지만 *모든 field 이름 반복*. 큰 절약 X.

**Use case**:
- *MessagePack* — Redis 의 reply, Pinterest internal
- *BSON* — MongoDB 내부
- *CBOR* — IoT (CoAP), WebAuthn

### §4.3 Thrift, Protocol Buffers (Protobuf) — schema-driven binary

Facebook (Thrift), Google (Protobuf). schema (`.thrift`, `.proto`) 가 *별도 파일*:

```protobuf
message Person {
  required string user_name        = 1;
  optional int64  favorite_number  = 2;
  repeated string interests        = 3;
}
```

각 field 가 *tag 번호* 보유. 인코딩 시 *field 이름이 아니라 tag 번호* 만 byte 에 들어감 → 매우 컴팩트.

![Figure 4-2 — Protobuf 의 binary 표현. 책 p.118](/courses/ddia/figures/ch04/fig-4-2.png)

**호환성 규칙**:
- *새 field 추가*: 새 tag 번호. 옛 코드는 *모르는 tag 무시*. → **forward compatible**
- *옛 field 삭제*: tag 번호 *재사용 금지*. optional 또는 default 로.
- *Required 절대 금지* — 한 번 required 면 *제거 불가능* (옛 data 가 항상 깨짐)

### §4.4 Avro — schema 가 *writer + reader* 분리

LinkedIn (Doug Cutting, Hadoop 의 일부). 매우 컴팩트:

```avsc
{
  "type": "record",
  "name": "Person",
  "fields": [
    {"name": "userName",        "type": "string"},
    {"name": "favoriteNumber",  "type": ["null", "long"], "default": null},
    {"name": "interests",       "type": {"type": "array", "items": "string"}}
  ]
}
```

field 의 *tag 번호 없음* — 순서가 schema 와 일치. byte 가 *최소화* (Protobuf 대비도 작음).

**핵심 — Writer's vs Reader's schema**:
- *Writer*: 데이터를 쓸 때의 schema
- *Reader*: 데이터를 읽는 코드의 schema
- *Avro library 가 두 schema 의 차이를 자동 처리*:
  - reader 가 *모르는 field* → 무시
  - reader 가 *기대하는 field 가 writer 에 없으면* → schema 의 default 값

![Figure 4-6 — Avro 의 writer/reader schema 가 evolution 을 어떻게 처리. 책 p.135](/courses/ddia/figures/ch04/fig-4-6.png)

**Avro 의 schema 가 byte 와 분리**:
- 파일 (datafile): 시작에 *schema 한 번* + 데이터 stream
- DB: column 정보가 *별도 위치*
- RPC: connection 시 schema negotiation

Avro 가 *dynamically-generated schema* 에 강함 — DB 테이블의 schema 가 자주 변하는 환경 (Hadoop ecosystem) 에 적합.

### §4.5 Modern serialization — FlatBuffers, Cap'n Proto

**Protobuf 의 한계** — *parsing 필요*. 큰 message 의 parsing latency.

**FlatBuffers** (Google, 2014):
- *Zero-copy* — parsing 없이 직접 access
- *Memory-mapped file* 도 가능
- *Game, real-time* 에 적합

**Cap'n Proto** (Kenton Varda, ex-Protobuf):
- *RPC + serialization 통합*
- *Time-traveling RPC* — promise 사이 pipeline

### §4.6 호환성 비교

| Format | Forward | Backward | Schema | Size |
|--|--|--|--|--|
| JSON / XML | application 처리 | application 처리 | 없음 | 큼 |
| MessagePack / BSON | application 처리 | application 처리 | 없음 | 중간 |
| Thrift / Protobuf | 모르는 tag 무시 ✓ | optional or default ✓ | .proto | 작음 |
| Avro | reader schema 처리 ✓ | reader schema default ✓ | .avsc | 가장 작음 |
| FlatBuffers | tag 무시 ✓ | optional ✓ | .fbs | Protobuf 와 비슷, parsing 없음 |

---

## §5 Database 의 Encoding

### §5.1 Data on disk

DB 가 row 를 어떻게 저장? — 보통 *DB 내부 format* (B-tree page, row-format). 이걸 *외부 노출 시 encoding 변환*.

**DB 별 internal format**:
- MySQL InnoDB — *Compact row format*
- PostgreSQL — *TOAST (oversized) + heap tuple*
- Oracle — *Variable-length row format*
- MongoDB — *BSON*
- Cassandra — *SSTable + sparse columns*

### §5.2 Schema migration

- *Schema-on-write* (relational): `ALTER TABLE ADD COLUMN x INT DEFAULT 0;`
  - 큰 테이블에 *분 단위 lock* 발생 가능
  - **online migration** (pt-online-schema-change, Postgres logical) 로 회피
- *Schema-on-read* (document): write 마다 *application 이 새 형태로* 변환. 옛 row 는 그대로.

**Modern tools**:
- **Liquibase, Flyway** — Java, SQL migration tracking
- **Alembic** — Python, SQLAlchemy
- **Prisma Migrate** — TS, schema-first
- **Atlas** — declarative, multi-DB

### §5.3 Archival storage

dump 를 Avro / Parquet 같은 *column-oriented + compressed* format 로 → archival 효율.

**산업 예**:
- *Snowflake* — internal columnar
- *BigQuery* — Capacitor (columnar)
- *S3 + Parquet* — 가장 흔한 data lake format
- *Apache Iceberg / Delta Lake* — table format on top of Parquet

---

## §6 Modes of Dataflow

세 가지 패턴 — *데이터가 시스템 사이를 어떻게 흐르나*:

### §6.1 Via Databases

- writer 가 write 함, reader 가 read 함
- writer 와 reader 가 *다른 process / 다른 시점*
- **forward + backward compatibility 모두 필요**

**시나리오 — 5년 된 row**:
- 5년 전 코드가 옛 schema 로 write
- 오늘 새 코드 가 read
- → *backward compatible* 필요 + *schema evolution history* 추적

### §6.2 Via Service Calls (REST, RPC)

- client → server 의 *동기 request-response*
- network 통과 → *partial failure* 가능

**REST**:
- HTTP 의 native verb (GET, POST, PUT, DELETE)
- URL 이 resource 표현
- JSON 이 표준
- 호환성: API versioning (`/v1/users`, `/v2/users`)

**RPC** (Remote Procedure Call):
- 함수 호출처럼 보이지만 실제는 network call
- gRPC (Google, Protobuf 기반), Apache Thrift, Avro RPC

**GraphQL** (Facebook, 2015):
- Client 가 *원하는 field 만* query
- *Over-fetching / under-fetching 회피*
- Schema-driven (.graphql)
- 단점: N+1 query, caching 어려움

**비교**:

| | REST | gRPC | GraphQL |
|--|--|--|--|
| Protocol | HTTP/1.1 or 2 | HTTP/2 | HTTP/1.1 or 2 |
| Format | JSON | Protobuf binary | JSON |
| Schema | OpenAPI (optional) | .proto (required) | .graphql (required) |
| 호환성 | Versioning | Protobuf 자동 | Schema evolution |
| Streaming | SSE | bidirectional | Subscriptions |
| 적합 | Public API | Internal service | Frontend ↔ backend |

> **함정 1**: RPC 의 *fallacy* — "함수 호출처럼 단순" 으로 보이지만 실제는:
> - network latency, retry, timeout 필요
> - parameter / return 의 *encoding* 필요
> - service 가 *unreachable* 일 수 있음
> - 양쪽 *version 호환* 필요

**Service mesh** (Istio, Linkerd, Consul):
- *Sidecar proxy* (Envoy) 가 모든 service 통신 중계
- *Retry, timeout, circuit breaker, mTLS, observability* 의 *infrastructure level*

### §6.3 Via Async Message Passing (Kafka, RabbitMQ)

- writer 가 *message* 를 *queue / broker* 에 publish
- reader (consumer) 가 *나중에* 가져감
- *writer 와 reader 가 decoupled*
- 장점: 부하 spike 흡수, 여러 consumer, 자동 retry

**Brokers**:
- RabbitMQ, ActiveMQ, NATS — 전통 *message queue*
- Kafka, Pulsar, Kinesis — *log-based* (11장)
- Redis Streams — Redis 의 log-based
- Cloud — AWS SQS, GCP Pub/Sub, Azure Service Bus

호환성 핵심 — *queue 에 옛 + 새 message 가 공존* → encoding evolution 호환성 필수.

**Confluent Schema Registry** + Kafka 의 *표준 stack*:
- Producer 가 schema 등록 → schema ID 받음
- Message 에 schema ID + Avro/Protobuf binary
- Consumer 가 schema ID 로 lookup → decode

---

## §7 Service Architecture 의 진화

### §7.1 Monolith → Microservices

**Monolith**:
- 하나의 process 안 *모든 기능*
- 호환성 문제 적음
- *부분 deploy 불가*, *team 간 충돌*

**Microservices**:
- service 별 *독립 deploy*
- 같은 시점에 *여러 version* 가 production
- → *encoding 호환성* 이 *생존 조건*

**Modular Monolith** (반전 trend, 2020s):
- Monolith 의 *내부 module 분리*
- Microservices 의 *복잡도 회피*
- *적당한 규모* 에 적합

### §7.2 Schema Registry

Confluent Schema Registry:
- 모든 schema 의 *중앙 저장소*
- producer 가 schema 등록
- consumer 가 *schema ID 로 lookup*
- *호환성 규칙* 자동 검증

**Compatibility 모드**:
- *Backward* — 새 schema 가 옛 data 읽음
- *Forward* — 옛 schema 가 새 data 읽음
- *Full* — 둘 다
- *None* — 검증 없음

### §7.3 Event Sourcing

전통 — *current state* 저장.
**Event Sourcing** — *모든 변경 event* 저장.

```
[OrderCreated, ItemAdded, ItemRemoved, ItemAdded, OrderShipped]
                                                  ↓ replay
                                           Current state
```

장점:
- *Audit log 자동*
- *Time-travel* — 옛 상태 재현
- *Multiple projections* — 같은 event 의 다른 view
- *CDC + analytics 자연스러움*

산업:
- **Event Store** (eventstore.com)
- **Axon Framework** (Java)
- *Kafka + state store* — Confluent 의 ksqlDB

CQRS 와 자주 함께 — Command (write) + Query (read) 분리. 11장 + 12장 에 상세.

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | language-specific serialization 으로 ok | security, version, language lock-in. *binary standard 사용* |
| 2 | JSON 이 *universal* | 숫자 모호, binary 못 다룸, schema 없음 |
| 3 | Protobuf 의 *required* 사용 | 한번 required 면 *제거 불가능*. 항상 optional |
| 4 | Avro 의 schema 가 *byte 와 같이* 가야 | 별도 transport (schema registry) |
| 5 | RPC 가 *local call 처럼* | network failure, retry/timeout/idempotency 필요 |
| 6 | 새 column 추가 = ALTER TABLE | 큰 테이블엔 *분 단위 lock*. online migration tool 필수 |
| 7 | message queue 가 *항상 in-order* | 여러 partition / consumer 에서 order 보장 어려움 |
| 8 | API version 으로 *큰 변경* | semver 의 breaking change = 완전 새 endpoint |
| 9 | GraphQL 이 *모든 문제 해결* | over-fetch 해결되나 N+1, caching, rate limiting 어려움 |
| 10 | Forward compat 만 있으면 충분 | 두 방향 모두 필요 |
| 11 | Microservices = 항상 좋음 | 호환성 + operational complexity. Modular monolith 가 더 적합한 경우 多 |
| 12 | Schema registry 가 *optional* | Production Kafka 의 *사실상 필수* |

---

## §9 자가점검

1. *Encoding* 의 정의 + *language-specific* 의 4 가지 문제?
2. JSON / XML 의 4 가지 한계?
3. Protobuf 의 *tag 번호* 가 *왜* compact?
4. Protobuf 의 *forward / backward compatibility* 규칙?
5. Avro 의 *writer's vs reader's schema* 의 핵심 아이디어?
6. *Forward* vs *backward* compatibility 의 차이?
7. *Schema migration* — schema-on-write 와 schema-on-read 의 각 비용?
8. *Database / Service / Message-passing* 의 dataflow 차이?
9. RPC 의 *fallacy* 4 가지?
10. *Schema registry* 의 역할?
11. *REST vs gRPC vs GraphQL* 의 적합 use case?
12. *Event Sourcing* 의 장점?

<details><summary>해답 (간략)</summary>

1. memory 객체 ↔ bytes 변환. 문제: 언어 lock-in, security, version 호환 약함, 비효율.
2. 숫자 모호, binary 못, schema 부재, CSV 의 quoting standardization 부재.
3. field 이름 대신 *정수 tag* 만 byte 에 들어감 → schema 가 *외부* 에.
4. forward: 모르는 tag 무시. backward: optional + default. *required 절대 금지*.
5. writer 와 reader 가 *다른 schema* 가능. library 가 *자동 호환 처리*.
6. forward = 옛 코드가 새 data 읽음. backward = 새 코드가 옛 data 읽음.
7. write: ALTER TABLE (큰 테이블 lock). read: application 이 *두 형태 모두* 지원.
8. DB: writer ↔ reader 시간 차이. Service: 동기 request-response. Message: async + decoupled.
9. (1) network failure (2) latency 비용 (3) encoding 필요 (4) version 호환 필요.
10. 중앙 schema 저장 + 자동 호환성 검증. Kafka 의 사실상 필수.
11. REST: public API. gRPC: internal service. GraphQL: frontend ↔ backend.
12. Audit log 자동, time-travel, multiple projections, CDC + analytics 자연스러움.

</details>

---

## §10 다음 학습으로

- **5장 (Replication)** — replica 사이 데이터 sync 의 encoding.
- **10장 (Batch Processing)** — Avro / Parquet 의 archival storage 응용.
- **11장 (Stream Processing)** — Kafka + schema registry.
- **12장 (Future)** — Event sourcing — 모든 변경을 *immutable event stream* 으로.

---

## §11 한 줄 요약

> **Encoding = memory ↔ bytes 의 boundary. *Schema evolution* 의 forward + backward 호환성이 *모든 distributed system 의 생존 조건*. Protobuf/Avro 의 schema-driven binary. REST + gRPC + GraphQL 의 use case 별 선택. Schema registry + service mesh 의 modern stack.**
