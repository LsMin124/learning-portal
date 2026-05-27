# Ch 4 Encoding and Evolution — 치트시트

## TL;DR

- **Encoding** = in-memory ↔ bytes. Language-specific 은 *금지* (security, lock-in)
- **Text** (JSON/XML): readable, schema 없음, 숫자 모호
- **Binary** (Protobuf/Thrift): schema + tag 번호, compact. *required 금지*
- **Avro**: writer/reader schema 분리, dynamic schema 친화. Hadoop/Kafka 표준
- **Forward** (옛 reader, 새 data) + **Backward** (새 reader, 옛 data) 둘 다 필요
- **Dataflow**: DB (시간차), Service RPC (sync), Message queue (async decoupled)
- **Schema Registry** + Avro/Protobuf = 산업 표준

---

## Quick Reference

### 표 1. Encoding 종류

| Format | Schema | Binary | Evolution | 사용 |
|--|--|--|--|--|
| JSON / XML | 외부 (JSON Schema) | text | 수동 | API, config |
| MessagePack | 없음 | binary | 수동 | JSON 의 binary 버전 |
| Thrift / Protobuf | 함께 (.thrift, .proto) | binary | tag 기반 | gRPC, 내부 service |
| Avro | 별도 (data 와 분리) | binary | reader/writer | Kafka, Hadoop |
| Parquet | 함께 | columnar binary | 비슷 | 분석, archive |

### 표 2. Compatibility

| | Forward (옛 reader, 새 data) | Backward (새 reader, 옛 data) |
|--|--|--|
| 의미 | 새 field 무시 가능 | 누락 field default |
| Protobuf | 모르는 tag skip ✓ | optional ✓ |
| Avro | reader schema 가 처리 ✓ | reader schema default ✓ |
| JSON | 코드가 직접 | 코드가 직접 |

### 표 3. Dataflow 3 종

| Mode | 특징 | 호환성 요구 |
|--|--|--|
| DB | writer ↔ reader 시간차 | forward + backward |
| Service (REST/RPC) | sync req-resp | request + response 양방향 |
| Message queue | async, decoupled | producer↔consumer 양방향 |

### 표 4. REST vs gRPC

| | REST | gRPC |
|--|--|--|
| Protocol | HTTP/1.1 | HTTP/2 |
| Payload | JSON (text) | Protobuf (binary) |
| Schema | OpenAPI (optional) | .proto (required) |
| Streaming | SSE / WS | bidirectional native |
| Type safety | runtime | compile-time |
| Browser 직접 | ✓ | ✗ (grpc-web 필요) |
| 사용 | public API | internal service |

### 표 5. Schema 변경 best practices

```
ADD new field:
  - 항상 optional + default
  - tag 번호 새로 할당
  → forward + backward compat

REMOVE field:
  - tag 번호 *재사용 금지*
  - optional 이면 silent 제거 OK
  - required 면 단계: required → optional → 제거 (long process)

RENAME field:
  - 같은 tag, 다른 name → name 만 변경 (Protobuf OK)
  - Avro: alias 사용

CHANGE type:
  - int32 → int64: backward 가능 (Avro/Proto)
  - string → int: 불가능. 새 field 추가 후 migrate
```

### 표 6. Schema Registry (Confluent)

```
Producer:
  1. POST /subjects/{topic}/versions {schema}
  2. registry → schema ID (예: 42)
  3. message = [magic_byte, schema_id=42, avro_payload]

Consumer:
  1. message 에서 schema_id 추출
  2. GET /schemas/ids/{id} → writer schema
  3. local reader schema 와 resolve → 객체

Compatibility 모드:
  - BACKWARD: 새 schema 가 옛 data 읽을 수 있어야
  - FORWARD: 옛 schema 가 새 data 읽을 수 있어야
  - FULL: 둘 다
  - NONE: 비활성
```

### 표 7. JSON 의 함정

| 함정 | 대응 |
|--|--|
| 큰 정수 (≥2^53) | string 으로 |
| binary data | base64 (33% 낭비) |
| datetime | ISO 8601 string + UTC |
| 정밀 소수 | string + Decimal type |
| schema 부재 | OpenAPI / JSON Schema |
| boolean / null 누락 | strict mode 활용 |

---

## Mind Map

```
4장 Encoding and Evolution
├─ 1. Encoding = memory ↔ bytes
├─ 2. Language-specific 금지
├─ 3. Text (JSON/XML/CSV)
│   └─ readable, 모호함, schema 없음
├─ 4. Binary (Protobuf, Avro, Thrift)
│   ├─ Protobuf: tag-based, required 금지
│   └─ Avro: reader/writer schema, dynamic
├─ 5. Database
│   ├─ schema migration (ALTER, online tool)
│   └─ archival (Parquet)
├─ 6. Dataflow 3 종
│   ├─ DB
│   ├─ Service (REST, gRPC)
│   └─ Message queue (Kafka, RabbitMQ)
└─ 7. Architecture
    ├─ Microservice → encoding 호환성 필수
    └─ Schema Registry
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | encoding 은 memory ↔ bytes 변환 |
| 2 | language-specific 금지. binary standard 권장 |
| 3 | text format 은 readable 하지만 schema 없음 |
| 4 | Protobuf 는 tag, Avro 는 writer/reader schema |
| 5 | DB migration 은 online tool 필수 |
| 6 | DB / Service / Message 의 dataflow 각각 호환성 다름 |
| 7 | Microservice 시대의 schema registry 가 표준 |
