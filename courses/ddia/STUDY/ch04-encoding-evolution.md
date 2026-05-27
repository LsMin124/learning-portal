# Chapter 4: Encoding and Evolution — 학습 노트

> *DDIA* (Kleppmann, 2017) **Chapter 4** (책 p.111~150, PDF p.133~166).
> 4장의 핵심: 데이터를 *시스템 사이* (디스크, 네트워크, 다른 process) 로 *어떻게 옮기는가*. 그리고 *시간에 따라 schema 가 변할 때* 옛 코드와 새 코드가 *공존* 하는 방법.

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

## 1. Encoding 의 두 표현

데이터는 두 표현 사이를 움직임:

| 표현 | 어디서 | 형태 |
|--|--|--|
| **In-memory** | 실행 중 process | 객체, struct, list, hash table (pointer-based) |
| **Bytes** | 디스크, 네트워크, IPC | 일관된 byte sequence |

변환:
- **Encoding** (= serialization, marshalling): memory → bytes
- **Decoding** (= deserialization, unmarshalling, parsing): bytes → memory

> **Schema evolution** — 같은 시스템이 *옛 코드 + 새 코드* 가 *동시에 동작* 하는 시기 (rolling upgrade, mobile app 의 옛 버전 사용자). 이때 *encoding format* 의 evolution 호환성이 핵심.

---

## 2. Language-specific encoding

Java 의 `java.io.Serializable`, Python 의 `pickle`, Ruby 의 `Marshal` 등.

**장점**: 같은 언어 안에서 *single line* 으로 객체 ↔ bytes.

**단점** (책의 강력한 경고):
1. **언어 lock-in** — Java pickle 을 Python 으로 못 읽음
2. **Security** — pickle 같은 generic deserialization 은 *임의 코드 실행* 공격 표적
3. **Version 호환성 처리가 약함** — 같은 언어 안에서도 class 변경 시 깨짐
4. **효율성** — 보통 binary 표준 (Protobuf, Avro) 대비 *느리고 큼*

**책의 결론**: language-specific encoding 은 *임시·인-프로세스* 외엔 사용 금지.

---

## 3. JSON, XML, CSV — Textual Formats

### 3.1 장점

- *Human-readable*
- 거의 모든 언어가 native parser
- *Schema 없음* — flexibility

### 3.2 한계

| 한계 | 영향 |
|--|--|
| **숫자의 모호함** | JSON 의 number 가 int/float 구분 X. JS 는 IEEE 754 double 만 — 2^53 초과 정수 손실 |
| **Binary data 표현** | base64 인코딩 (33% 공간 낭비) |
| **Schema 부재** | application 코드가 schema 를 *암묵* 으로 가짐 → 일관성 어려움 |
| **CSV 의 한계** | quoting, escape, encoding 등 standardization 부재 |

### 3.3 JSON Schema

JSON 에 schema 부여: JSON Schema, OpenAPI/Swagger. *외부 validation* 만 — encoding 자체엔 schema 정보 없음.

---

## 4. Binary Encoding

### 4.1 동기

text encoding 의 *문제 해결*:
- *작음* — 같은 데이터를 더 적은 byte 로
- *빠름* — parsing 빠름
- *schema-driven* — 명시적 type, 호환성 도구 자체 포함

### 4.2 MessagePack, BSON — schema-less binary

JSON 을 그대로 binary 화. Schema 여전히 없음. 약간 작아짐 (~1/3).

```
record JSON     {"userName": "Martin", "favoriteNumber": 1337, ...}
MessagePack     83 a8 75 73 65 72 4e 61 6d 65 a6 4d 61 72 74 69 6e ...
```

작지만 *모든 field 이름 반복*. 큰 절약 X.

### 4.3 Thrift, Protocol Buffers (Protobuf) — schema-driven binary

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

### 4.4 Avro — schema 가 *writer + reader* 분리

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

### 4.5 호환성 비교

| Format | Forward (옛 코드 + 새 data) | Backward (새 코드 + 옛 data) |
|--|--|--|
| JSON / XML | application 처리 | application 처리 |
| Thrift / Protobuf | 모르는 tag 무시 ✓ | optional 이거나 default ✓ |
| Avro | reader schema 가 처리 ✓ | reader schema 가 default ✓ |

---

## 5. Database 의 Encoding

### 5.1 Data on disk

DB 가 row 를 어떻게 저장? — 보통 *DB 내부 format* (B-tree page, row-format). 이걸 *외부 노출 시 encoding 변환*.

### 5.2 Schema migration

- *Schema-on-write* (relational): `ALTER TABLE ADD COLUMN x INT DEFAULT 0;`
  - 큰 테이블에 *분 단위 lock* 발생 가능
  - **online migration** (pt-online-schema-change, Postgres logical) 로 회피
- *Schema-on-read* (document): write 마다 *application 이 새 형태로* 변환. 옛 row 는 그대로.

### 5.3 Archival storage

dump 를 Avro / Parquet 같은 *column-oriented + compressed* format 로 → archival 효율.

---

## 6. Modes of Dataflow

세 가지 패턴 — *데이터가 시스템 사이를 어떻게 흐르나*:

### 6.1 Via Databases

- writer 가 write 함, reader 가 read 함
- writer 와 reader 가 *다른 process / 다른 시점*
- **forward + backward compatibility 모두 필요** (옛 reader 가 새 data, 새 reader 가 옛 data)

### 6.2 Via Service Calls (REST, RPC)

- client → server 의 *동기 request-response*
- network 통과 → *partial failure* 가능
- 두 가지 스타일:

**REST**:
- HTTP 의 native verb (GET, POST, PUT, DELETE)
- URL 이 resource 표현
- JSON 이 표준
- 호환성: API versioning (`/v1/users`, `/v2/users`)

**RPC** (Remote Procedure Call):
- 함수 호출처럼 보이지만 실제는 network call
- gRPC (Google, Protobuf 기반), Apache Thrift, Avro RPC
- 같은 회사 내부 service 간 통신에 흔히

> **함정 1**: RPC 의 *fallacy* — "함수 호출처럼 단순" 으로 보이지만 실제는:
> - network latency, retry, timeout 필요
> - parameter / return 의 *encoding* 필요
> - service 가 *unreachable* 일 수 있음
> - 양쪽 *version 호환* 필요

### 6.3 Via Async Message Passing (Kafka, RabbitMQ)

- writer 가 *message* 를 *queue / broker* 에 publish
- reader (consumer) 가 *나중에* 가져감
- *writer 와 reader 가 decoupled*
- 장점: 부하 spike 흡수 (queue 의 buffer), 여러 consumer 가 같은 stream 처리, 자동 retry

**Brokers**:
- RabbitMQ, ActiveMQ — 전통 *message queue*
- Kafka, Pulsar, Kinesis — *log-based* (11장)

호환성 핵심 — *queue 에 옛 message + 새 message* 가 *공존* → encoding 의 evolution 호환성 필수.

---

## 7. Service Architecture 의 진화

### 7.1 Monolith → Microservices

Monolith:
- 하나의 process 안 *모든 기능*
- 호환성 문제 적음 (deploy 시 모두 같이)
- 하지만 *부분 deploy 불가*, *team 간 충돌*

Microservices:
- service 별 *독립 deploy*
- 같은 시점에 *여러 version* 가 production
- → *encoding 호환성* 이 *생존 조건*

### 7.2 Schema Registry — 산업 패턴

Confluent Schema Registry 같은 service:
- 모든 schema 의 *중앙 저장소*
- producer 가 schema 등록
- consumer 가 *schema ID 로 lookup*
- *호환성 규칙* 자동 검증 (Avro, Protobuf, JSON Schema)

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | language-specific serialization 으로 ok | security, version, language lock-in. *binary standard 사용* |
| 2 | JSON 이 *universal* | 숫자 모호, binary 못 다룸, schema 없음 |
| 3 | Protobuf 의 *required* 사용 | 한번 required 면 *제거 불가능*. 항상 optional |
| 4 | Avro 의 schema 가 *byte 와 같이* 가야 | 별도 transport (schema registry). data 는 schema-less binary |
| 5 | RPC 가 *local call 처럼* | network failure 가능, retry/timeout/idempotency 필요 |
| 6 | 새 column 추가 = ALTER TABLE | 큰 테이블엔 *분 단위 lock*. online migration tool 필수 |
| 7 | message queue 가 *항상 in-order* | 여러 partition / consumer 에서 order 보장 어려움 (11장) |
| 8 | API version 으로 *큰 변경* | semver 의 *breaking change* 는 *완전 새 endpoint*. /v1/, /v2/ 병행 |
| 9 | GraphQL 이 *모든 문제 해결* | over-fetch 는 해결되나 N+1, caching, rate limiting 어려움 |
| 10 | Forward compat 만 있으면 충분 | 두 방향 모두 필요. rolling upgrade 시 옛↔새 양방향 통신 |

---

## 자가점검

1. *Encoding* 의 정의 + *language-specific* 의 4 가지 문제.
2. JSON / XML 의 4 가지 한계.
3. Protobuf 의 *tag 번호* 가 *왜* compact 한가.
4. Protobuf 의 *forward / backward compatibility* 규칙.
5. Avro 의 *writer's vs reader's schema* 의 핵심 아이디어.
6. *Forward* vs *backward* compatibility 의 차이.
7. *Schema migration* — schema-on-write 와 schema-on-read 의 각 비용.
8. *Database / Service / Message-passing* 의 dataflow 차이.
9. RPC 의 *fallacy* 4 가지.
10. *Schema registry* 의 역할.

### 해답 (간략)

1. memory 객체 ↔ bytes 변환. 문제: 언어 lock-in, security, version 호환 약함, 비효율.
2. 숫자 모호, binary 못, schema 부재, CSV 의 quoting standardization 부재.
3. field 이름 대신 *정수 tag* 만 byte 에 들어감 → schema 가 *외부* 에.
4. forward: 모르는 tag 무시. backward: optional + default. *required 절대 금지*.
5. writer 와 reader 가 *다른 schema* 가능. library 가 *자동 호환 처리* — 새 field 없으면 default, 모르는 field 무시.
6. forward = 옛 코드가 새 data 읽음. backward = 새 코드가 옛 data 읽음.
7. write: ALTER TABLE (큰 테이블 lock). read: application 이 *두 형태 모두* 지원.
8. DB: writer ↔ reader 시간 차이. Service: 동기 request-response. Message: async + decoupled.
9. (1) network failure (2) latency 비용 (3) encoding 필요 (4) version 호환 필요.
10. 중앙 schema 저장 + 자동 호환성 검증. Kafka 같은 broker 와 함께 표준.

---

## 다음 학습으로

- **5장 (Replication)** — replica 사이 데이터 sync 의 encoding.
- **10장 (Batch Processing)** — Avro / Parquet 의 archival storage 응용.
- **11장 (Stream Processing)** — Kafka + schema registry.
- **12장 (Future)** — Event sourcing — 모든 변경을 *immutable event stream* 으로.
