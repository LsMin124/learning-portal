# Ch 12 Future of Data Systems — 퀴즈

> 6 문항.

### Q1. Unbundled DB — 전통 DB 와의 차이

전통 RDBMS 가 가진 *내부 component* 들이 *unbundled* 에서 *어떻게 분리*?

<details><summary>답</summary>

**전통 RDBMS (한 process)**:
- Storage engine (B-tree, LSM-tree)
- Replication (leader, follower)
- Indexing (primary, secondary)
- Query optimizer + planner
- Transaction manager (lock, MVCC)
- Authentication, ACL

**Unbundled (각각 분리)**:
- *Storage*: S3, HDFS, RocksDB
- *Replication / log*: **Kafka** (distributed log)
- *Indexing*: Elasticsearch, Redis, Postgres (derived from Kafka)
- *Query*: Trino, Spark SQL
- *Transaction*: app-level + outbox pattern
- *Auth*: Vault, IAM

**장점**:
- 각 component *최적화* (Elasticsearch 의 search > RDBMS)
- *부분 교체* 가능 (RDBMS → MongoDB 만)
- *Scale 각 부분 독립*

**단점**:
- 운영 부담 ↑↑ — 여러 system
- *Consistency 어려움* — 각 system 의 sync
- *Latency* — multi-hop

산업 현실 — 대부분 *unbundled* 으로 진화 중. *databases of the future* (FaunaDB, CockroachDB, TiDB) 가 *re-bundled* 시도.

</details>

### Q2. Primary vs Derived — 어떻게 분리?

E-commerce 시스템에서 *primary* 와 *derived* 각각 무엇.

<details><summary>답</summary>

**Primary** (1개, source of truth):
- *Orders table* in PostgreSQL — order_id, user_id, items, status, timestamps
- *Users table* in PostgreSQL — user_id, name, email, password_hash

**Derived** (여러 개, primary 에서 함수):
1. *Search index* (Elasticsearch): order/product 검색용. text fields, partial match
2. *Cache* (Redis): user profile, top products. 빠른 read
3. *Analytics warehouse* (Snowflake): aggregate report. column store
4. *Recommendation graph* (Neo4j): "이 product 와 함께 산"
5. *Email queue* (Kafka topic): 결제 confirmation, shipping update

**동기화 — CDC**:
```
Postgres write → logical replication → Debezium → Kafka
                                                     ↓
                                                     ├─ Elasticsearch sink
                                                     ├─ Redis updater
                                                     ├─ Snowflake loader
                                                     ├─ Neo4j updater
                                                     └─ Email service
```

**Rebuild policy**:
- Derived 손상 → *Kafka log replay* 로 *시점부터 rebuild*
- Schema 변경 → *새 derived* 만들기, 옛것은 *deprecate*
- 새 derived 추가 → 처음부터 Kafka replay

이게 *Kappa architecture* 의 실현. Kafka 가 *infinite log + 다중 reader*.

</details>

### Q3. End-to-end idempotency — 결제 시스템

결제 service 의 *exactly-once* 를 *어떻게* 보장?

<details><summary>답</summary>

**문제** — 결제 시 network 실패:
- Client → server: payment request
- Server processed payment OK
- Response *lost*
- Client retry → *double charge*?

**End-to-end 해결 — Idempotency Key**:

```python
# Client
import uuid
idempotency_key = uuid.uuid4()  # 한 결제 시도 = 한 key
response = post("/charge", headers={"Idempotency-Key": str(idempotency_key)}, ...)
# Retry 시 같은 key 사용

# Server
def charge(req):
    key = req.headers["Idempotency-Key"]
    existing = db.find("idempotency_records", key=key)
    if existing:
        return existing.response  # 이미 처리됨, 같은 response 반환
    
    # 처음 처리
    result = process_payment(...)
    db.insert("idempotency_records", key=key, response=result, expires_in=24h)
    return result
```

**산업 패턴 — Stripe**:
- *Idempotency-Key HTTP header*
- 24 시간 동안 cache
- 같은 key + 같은 request body = 같은 response

**Layer 별 책임**:
- *Network (TCP)*: reliable transmission — packet retry 자동
- *RPC client*: timeout + retry with backoff
- *Application*: idempotency key 의 dedup
- *DB*: ACID transaction 안에서 idempotency check

End-to-end argument — *application 만이 application correctness 보장*. Lower layer 는 *helper*.

</details>

### Q4. Kafka 기반 architecture — 새 feature 추가

기존 e-commerce 에 *추천 시스템* 신규. 어떻게 *기존 system 안 건드리고* 추가?

<details><summary>답</summary>

**Kafka backbone 이 있으면** *non-invasive*:

```
기존:
  Postgres → Kafka (CDC) → ES, Redis, Snowflake

신규 추천 시스템 추가:
  Postgres → Kafka (CDC, 변경 없음!) →
                                       └─ NEW: Recommendation pipeline
                                                ↓
                                                Spark / Flink (collaborative filtering)
                                                ↓
                                                Redis (user → recommended products)

API:
  /recommendations/{user_id} → Redis lookup
```

**과정**:
1. *Kafka log* 의 historical data 를 *replay* — 과거 user behavior 학습
2. 그 후 *real-time stream* 으로 계속 update
3. 결과는 *별도 Redis store* 에. *기존 PostgreSQL/ES 안 건드림*
4. API gateway 가 *추천 endpoint* 추가 노출

**이점**:
- *Primary system 무영향* — 기존 service 의 *throughput 영향 없음*
- *Independent scale* — 추천 system 만 따로 확장
- *Independent deploy* — 추천 코드 만 deploy
- *Failure isolation* — 추천 service 다운 시 *상품·결제는 영향 없음*

**비교 — Without Kafka**:
- *Dual write* 필요 — application 이 *Postgres 와 추천 service 둘 다* write
- 둘 다 sync 면 *latency 추가*
- 한쪽 실패 시 *불일치*

이게 *unbundled architecture* 의 *evolution friendly* 의 진수.

</details>

### Q5. GDPR 의 "Right to be Forgotten" 구현 도전

사용자가 *계정 삭제* 요청. 모든 system 에서 *진짜 삭제* 어떻게?

<details><summary>답</summary>

**도전** — 데이터의 *복제·파생* 이 다층:

1. **Primary DB** (Postgres)
2. **Derived indices** (Elasticsearch, Redis cache)
3. **Backups** (daily, weekly, monthly)
4. **Logs** (application log, audit log, request log)
5. **Stream history** (Kafka topic with TTL)
6. **Analytics warehouse** (Snowflake)
7. **ML training data** (S3 bucket)
8. **3rd party services** (마케팅 도구, payment processor)

**해결 전략 — Multi-pronged**:

1. **Cryptographic erasure**:
   - 모든 user data 를 *user-specific key* 로 암호화
   - 삭제 시 *key 만* 삭제 → encrypted data 가 *읽을 수 없게* 됨
   - 산업 표준 (Apple 의 device 암호화 모델)

2. **Tombstone + cascading delete**:
   - Primary 에 `deleted_at` 마크
   - CDC 를 통해 모든 derived 에 propagate
   - 각 system 의 *physical delete* 후 audit log

3. **Backup policy**:
   - Backup 도 *retention 기간* 명시 (예: 90일)
   - Backup 안의 *해당 user 영역* 의 zero-out (어려움)
   - 실용: 명시된 retention 후 *전체 backup 삭제 + 새로*

4. **Stream truncation**:
   - Kafka 의 *compacted topic* 에 *tombstone marker*
   - TTL retention 이 진행되면서 자연 삭제

5. **3rd party**:
   - Stripe, Mixpanel 등 각자의 *delete API* 호출
   - 일부는 *진짜 삭제* 어렵 — 사용자에게 명시

**현실** — 100% deletion 거의 불가능. *best effort + documented*.

GDPR 의 *enforcement* 는 *demonstrable effort* 중심 — perfect 삭제가 아닌 *합리적 노력*.

</details>

### Q6. 면접 — Engineer 로서의 *ethical* 책임

"내가 만든 system 이 사용자 *프라이버시 침해*. 회사는 알면서도 강행. 어떻게?"

<details><summary>답</summary>

**Engineer 의 선택지**:

1. **Speak up internally**:
   - 직접 manager 에게 의견 전달
   - *Specific 한 위험* 제시 (regulatory, brand damage, user harm)
   - 대안 제안 (privacy-preserving design)

2. **Document concerns**:
   - 정식 review 과정에서 *기록 남김*
   - 결정의 근거가 *후일 audit* 시 명확

3. **Escalate**:
   - 더 위 management, ethics committee, board
   - Internal whistleblower channel

4. **Refuse to implement**:
   - 본인이 *책임 못 지는* 부분은 *작성 거부*
   - Career risk 가 있음

5. **External**:
   - Regulator 에 신고 (illegal 인 경우)
   - Media (public interest)
   - Resign

**책 (Kleppmann) 의 관점**:
- *"We are not just builders, we are also citizens"*
- Technology choices = *value choices*
- *Code 가 society 의 형태를 정함* — *who has power*, *who is monitored*

**산업 movement**:
- *Tech Workers Coalition*
- *Algorithmic Justice League*
- Google 의 *Maven contract* 직원 항의
- *Ethical AI* 분야 (Fei-Fei Li, Timnit Gebru 등)

**Practical limits**:
- *모든 engineer 의 모든 결정* 에 ethics filter — 불가능
- *큰 결정* (data collection, ML model use, surveillance) 에 우선
- 회사의 *culture + leadership* 이 더 큰 영향

**핵심** — *기술적 결정 = 사회적 결정*. 침묵은 *동의*. Engineer 의 *주체적 책임*.

DDIA 가 *이 책의 마지막 chapter 를 윤리에 할애한* 이유 — engineering 의 *비도덕적 도구화* 를 막을 *마지막 방어선* 이 engineer 자신.

</details>
