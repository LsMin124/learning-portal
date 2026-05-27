# Ch 4 Encoding and Evolution — 퀴즈

> 10 문항.

### Q1. Forward vs Backward compatibility

각 정의 + rolling upgrade 시 *왜 둘 다* 필요한가.

<details><summary>답</summary>

- **Forward**: *옛 코드* 가 *새 data* 를 읽음 (옛 reader 가 새 schema 데이터 처리)
- **Backward**: *새 코드* 가 *옛 data* 를 읽음 (새 reader 가 옛 schema 데이터 처리)

**Rolling upgrade**: 일부 server 는 v1, 일부는 v2 로 *공존*. v1→v2 message 는 *forward* (v1 reader 처리), v2→v1 message 는 *backward* 필요. 또한 DB 의 옛 row 를 새 코드가 읽음 = backward.

둘 다 없으면 deploy 가 *all-or-nothing* — 큰 시스템에선 불가능.

</details>

### Q2. Protobuf 의 *required* 가 왜 위험

<details><summary>답</summary>

`required` field 는 *제거 불가능* — 옛 schema 의 required 가 새 schema 에 없으면 옛 reader 가 *parse error*.

**문제 시나리오**:
1. v1: `required string email = 1;`
2. v2 에서 email 을 deprecate 하고 싶음
3. v2 가 email 없이 message 작성
4. v1 reader 가 *required field missing* → exception
5. 호환 깨짐

**Google 공식 가이드**: proto3 에선 *required 자체를 제거*. 모든 field 가 optional 같음. proto2 사용자는 *required 사용 금지*.

대안: `optional` + application 단의 validation, 또는 별도 message type.

</details>

### Q3. Avro 가 dynamic schema 환경에 강한 이유

Hadoop ecosystem 처럼 *수백 table 의 schema 가 자주 변하는* 환경에서 Avro 가 우월한 이유.

<details><summary>답</summary>

1. **Schema 가 데이터와 *분리*** — Protobuf 처럼 *tag 번호 관리* 안 함. schema 자체가 식별자.
2. **Reader 와 writer schema 가 *다를 수 있음*** — library 가 자동 변환. 새 field 는 default, 모르는 field 무시.
3. **Schema 가 *JSON*** — 도구로 동적 생성 가능 (예: DB table → Avro schema).
4. **No 필드 번호 관리** — schema 변경마다 *번호 할당 결정* 안 함. Protobuf 의 *조직적 관리* 부담 없음.
5. **Compact** — tag 번호 없이 *순서 기반* 으로 byte 절약.

산업 패턴: **Kafka + Confluent Schema Registry + Avro** — Hadoop / 스트림 ecosystem 의 표준.

</details>

### Q4. RPC 의 fallacy — 4 가지 *오해*

<details><summary>답</summary>

L. Peter Deutsch 의 *Eight Fallacies of Distributed Computing* 중 RPC 관련:

1. **Network is reliable** — packet loss, partition 있음
2. **Latency is zero** — 같은 datacenter 도 ~ms, 다른 region 은 100ms+
3. **Bandwidth is infinite** — 대용량 transfer 는 *시간 걸림*
4. **Network is secure** — TLS 필수, auth/authz 필요

추가 (5~8): topology changes, single admin, transport cost zero, network is homogeneous.

**시사점**: RPC 코드도 *명시적으로* retry, timeout, circuit breaker, idempotency 처리해야. 함수 호출 같은 단순함을 *흉내* 만 내고 실제는 분산 시스템 복잡도.

</details>

### Q5. Schema 변경 — ALTER TABLE 의 위험

10억 row table 에 `ALTER TABLE orders ADD COLUMN notes TEXT;` 실행 시?

<details><summary>답</summary>

**위험**:
- MySQL InnoDB: default 가 NULL/static 이면 *online*, default 가 *값* 이면 *전체 rewrite* (수십 분 ~ 시간)
- PostgreSQL 11+ 이면 default 값도 *metadata only* — *순간*
- 그러나 옛 버전이면 *table-wide AccessExclusiveLock* → 모든 read/write block

**Online tool**:
- **pt-online-schema-change** (Percona) — 새 table 만들고 trigger 로 동기화 → atomic rename
- **gh-ost** (GitHub) — binary log 기반, trigger-less
- **PostgreSQL Logical Replication** — replica 에 새 schema, switchover

**원칙**: 큰 table 의 ALTER 는 *online migration tool* 필수. *prod 에서 직접 ALTER 금지*.

</details>

### Q6. JSON 숫자 모호함 — 실제 버그

JS frontend 가 `{"id": 9007199254740993}` JSON 을 받으면?

<details><summary>답</summary>

JS Number 는 IEEE 754 double — **2^53 = 9007199254740992 까지만 정확**. 그 초과는 *반올림*.

`9007199254740993` → `9007199254740992` (또는 994). ID *변경*! → 잘못된 record 조회·갱신 가능.

**대응**:
1. **string 으로 전송** — `{"id": "9007199254740993"}` — 안전
2. **BigInt** — `9007199254740993n` (JSON.parse 의 reviver 로 변환)
3. **UUID** — 처음부터 string ID 사용

Twitter API 가 *snowflake ID (64-bit int)* 사용 → JS client 에서 깨져서 *JSON 의 `id_str`* 추가. 책 출판 후에도 여전한 함정.

</details>

### Q7. REST vs RPC 의 선택

같은 회사의 내부 service 4개. REST vs gRPC?

<details><summary>답</summary>

**gRPC 가 유리**:
- Service 간 통신 (frontend → backend X, backend ↔ backend)
- Type safety 중요
- High throughput (binary, HTTP/2 multiplexing)
- Bidirectional streaming
- Polyglot (Go, Java, Python, Node 등 자동 client 생성)

**REST 가 유리**:
- Public API (외부 개발자 사용)
- Browser 직접 호출
- Simple CRUD, low frequency
- Caching (HTTP cache)
- Debug (curl, 브라우저)

**산업 패턴 (Google, Netflix 등)**:
- *내부* service 간: gRPC + Protobuf
- *외부* API: REST + JSON 또는 GraphQL
- *Gateway* 가 둘을 변환

답 — 내부 service 4개의 통신이면 **gRPC**, schema registry 와 함께. 다만 *모두 같은 deploy lifecycle* 이면 monolith 가 더 단순할 수도.

</details>

### Q8. Message queue 의 호환성

Kafka 의 topic 에 producer A (v1) 와 producer B (v2) 가 동시에 write. Consumer C 는?

<details><summary>답</summary>

**상황**:
- Topic 에 v1 message + v2 message 가 *섞임*
- Consumer C 는 v1, v2 모두 처리해야

**호환성 요구**:
- C 가 v1 으로 짜였으면 → v2 message 가 *forward compat* 필요 (C 의 v1 reader 가 v2 처리)
- C 가 v2 로 짜였으면 → v1 message 가 *backward compat* 필요 (C 의 v2 reader 가 v1 처리)

**산업 패턴 — Schema Registry**:
1. Producer 가 schema 를 registry 에 등록 → schema ID 받음
2. Message 에 *schema ID + payload* 만 write
3. Consumer 가 schema ID 로 *writer schema* lookup
4. Consumer 의 *reader schema* 와 자동 *resolution* (Avro)
5. Registry 가 *compatibility 규칙 강제* — incompatible schema 등록 거부

→ producer/consumer 가 *완전 decoupled deploy* 가능.

</details>

### Q9. 디버그 — 옛 client 가 새 server 호출 시 깨짐

새 server 에 *required field* 를 추가했더니 옛 mobile app (v1) 에서 *parse 실패*.

<details><summary>답</summary>

**원인**: server 의 *response schema 변경* 이 *backward compat 깨짐*.

옛 client (v1) 가 *모르는 required field* 를 받으면 — 일부 library 는 silently ignore, 일부는 *exception throw*. Protobuf 의 `required` 가 특히 위험.

**해결**:
1. **롤백** — server v2 deploy 취소
2. **새 field 를 optional 로** — required 제거
3. **API versioning** — `/v1/api` 와 `/v2/api` 병행. 옛 client 는 /v1, 새 client 는 /v2
4. **두 schema 모두 지원** — server 가 *둘 다* return (예: 두 field 병행)

**예방 — Schema compatibility 자동 검증**:
- CI 에서 새 schema 와 옛 schema 의 *compat 자동 비교*
- Confluent Schema Registry 같은 도구가 이걸 강제
- *backward-compatible only* 또는 *forward-compatible only* 모드 선택

</details>

### Q10. 면접 — Event sourcing 의 encoding 함의

"event sourcing 채택했는데 *몇 년 후* event format 을 바꾸고 싶음". 어떻게?

<details><summary>답</summary>

Event sourcing 은 *모든 과거 event 가 영원히 immutable* — replay 시 *옛 event 도 처리* 가능해야.

**전략**:

1. **Upcasting** — *옛 event format 을 새 format 으로* 변환하는 transformer. event 를 읽을 때 자동으로 upcast.
2. **Versioned events** — `OrderCreatedV1`, `OrderCreatedV2` 별개 type. consumer 가 *모든 version 처리*.
3. **Event payload 가 schema evolvable format** (Avro 권장):
   - 새 event 가 옛 reader 와 호환 → 옛 query 도 작동
4. **Snapshot + checkpoint**:
   - 일정 주기 *aggregate state snapshot* 저장
   - 옛 event 를 *지우는* 대신 *접근 안 함*
   - migration 후엔 snapshot 부터 replay

**원칙**:
- *Event 자체는 영원* — 형태 바꾸지 말고 새 event type 추가
- *Application 의 read model* 은 자유롭게 rebuild
- Avro + schema registry 로 long-term 호환성 확보

이게 12장의 *unbundled database* + event sourcing 의 핵심.

</details>
