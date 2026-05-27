# Ch 8 Distributed Trouble — 퀴즈

> 8 문항.

### Q1. Single → Distributed 의 *질적 변화*

추가되는 5 가지 문제.

<details><summary>답</summary>

1. **Unreliable network** — packet loss, reorder, delay
2. **Unreliable clock** — node 마다 다름, NTP 동기화 불완전
3. **Partial failure** — 일부 node 만 실패 (전부 또는 무 아닌)
4. **Non-determinism** — 같은 input 이 다른 결과
5. **No global state** — "지금 시스템 상태" 의 *snapshot* 불가

→ 5~7장의 모든 추상화가 이 위에서 동작. 추상화의 *깨짐* 가능성이 8장의 주제.

</details>

### Q2. Timeout 결정 — 산업 best practice

network call 의 timeout 을 어떻게 결정하나?

<details><summary>답</summary>

**단순한 답 — fixed**:
- 단순 web request: 5초, 30초 등 magic number

**Better — adaptive**:
- p99 latency 의 *3-5 배*
- 예: 평소 p99 = 200ms → timeout 1s
- 측정 기반, *부하 변동 적응*

**Production patterns**:
- **Circuit breaker** — 연속 N timeout → service 자체를 *fail fast*
- **Hedged request** — 50ms 안에 답 없으면 *복제 request* 다른 replica
- **Retry budget** — 시간 단위로 retry 횟수 제한 (cascading retry storm 방지)
- **Deadline propagation** — request 의 *전체 deadline* 을 모든 sub-call 에 전달

**라이브러리**: gRPC 의 deadline, Netflix Hystrix, Polly (.NET), Resilience4j (Java).

</details>

### Q3. Monotonic vs Time-of-day clock — 코드 함정

다음 코드의 버그:

```python
start = time.time()
do_long_work()
elapsed = time.time() - start
if elapsed < 0:
    print("시간 여행?")  # 이게 정말 일어남?
```

<details><summary>답</summary>

**Yes!** 일어남.

`time.time()` 은 *wall clock* — NTP 가 *과거로* 보정하면 elapsed 가 음수.

**Fix**:
```python
start = time.monotonic()  # 단조 증가, NTP 영향 없음
do_long_work()
elapsed = time.monotonic() - start
assert elapsed >= 0
```

**Use cases**:
- 사용자 표시: `time.time()` (UTC 시간)
- 측정 / timeout: `time.monotonic()`
- Log timestamp: `time.time()` + UTC 명시
- 절대 동기화 필요: GPS clock 또는 PTP (precision time protocol)

JVM 의 `System.currentTimeMillis()` (wall) vs `System.nanoTime()` (monotonic) 도 같은 구분.

</details>

### Q4. JVM GC pause 의 split brain 시나리오

```
ZooKeeper-based leader election. Lease TTL = 10s.
Leader L 이 *GC pause* 15s.
다른 node 들이 L 의 lease 만료 → 새 leader L' 선출.
L 깨어남 — 자기는 *여전히 leader* 행세 → 두 leader.
```

방지법 (3 가지).

<details><summary>답</summary>

1. **Fencing token**:
   - ZooKeeper 가 새 leader 마다 *monotonic token* 발급 (epoch number)
   - L 의 옛 token 으로 writeresource 거부
   - Resource (storage, DB) 가 token 검증

2. **STONITH** ("Shoot The Other Node In The Head"):
   - 새 leader 선출 시 *옛 leader 강제 kill* (reboot, isolation)
   - 옛 leader 가 깨어나도 자기가 살아남지 못함

3. **Heartbeat with monotonic check**:
   - 깨어난 leader 가 *자기 last_heartbeat + pause_time > lease* 확인
   - 진짜 자기 lease 만료 알아채면 *step down*
   - 예: Java 의 `JvmPauseMonitor` (HBase, Cassandra)

**추가 — Pause 자체 방지**:
- G1GC, ZGC, Shenandoah 같은 *low-pause GC*
- Off-heap 자료구조 (Netflix HollowDB 등)
- Native code (Rust, Go) — *GC 없음*

</details>

### Q5. NTP 가 잘못된 case

NTP 실패 시 어떤 일?

<details><summary>답</summary>

**가능한 NTP 실패**:

1. **NTP server unreachable** — local clock 이 *자체 drift* (수 분~수 시간)
2. **잘못된 NTP server** — 잘못된 시각 전파
3. **Leap second insert** — 23:59:60 처리 버그 (Linux 2012 의 kernel hang)
4. **Slewing 가 너무 느림** — 큰 drift 를 *천천히* 보정 (slewing) 하느라 *시간차* 오래 지속
5. **Step adjustment** — slewing 못 따라잡으면 *jump* — 시간이 *과거로* 갈 수 있음
6. **Virtualization clock drift** — VM 의 clock 이 host 와 별개

**결과**:
- LWW 의 *최신 write 손실*
- Log timestamp 의 *misorder*
- TLS certificate validity 의 *오판*
- Distributed log 의 *causality 부정확*

**대응**:
- *Clock skew 모니터링* — chrony, ntpq -p 로 정기 점검
- *Logical clock* 사용 (Lamport, vector, HLC)
- *Spanner TrueTime* 같이 *uncertainty interval* 명시
- *No 시각 의존 ordering* — Kafka offset, log sequence number

</details>

### Q6. CAP theorem — 면접 단골

"분산 시스템은 CAP 중 *두 개만* 선택 가능" 의 *부정확한 부분*.

<details><summary>답</summary>

**전통 CAP**:
- **C** (Consistency): 모든 read 가 최신 write 봄
- **A** (Availability): 모든 request 가 응답 (성공 or 실패)
- **P** (Partition tolerance): network partition 발생해도 동작

"3 중 2" 선택 프레임 → *오해*.

**정확한 의미**:
1. **P 는 선택 아님** — partition 은 *현실*. 일어남. 무시할 수 없음.
2. **실제 선택은 partition 발생 시**:
   - **CP**: consistency 우선 — partition 시 *일부 request 거부* (HBase, Postgres sync replication)
   - **AP**: availability 우선 — partition 시 *모든 request 응답*, 일관성 양보 (Cassandra eventual)
3. **Partition 없을 땐 둘 다 가능** — 양쪽 시스템 모두 *정상 시 CA*

**더 나은 frame — PACELC** (Abadi 2010):
- Partition 시 → A or C
- *Else* (정상 시) → Latency or Consistency

**산업 현실**: 대부분 *AP-then-eventual* (Cassandra, DynamoDB) 또는 *CP* (etcd, ZooKeeper). 진짜 CA 는 *single-node* 만.

**8장 의 시각**: CAP 자체보다 *consistency 의 정확한 정의* (9장 linearizability) + *partition 의 빈도·영향* 가 중요.

</details>

### Q7. Truth in distributed systems — Quorum 결정 시나리오

5 node cluster. 3 node 한 region (A), 2 node 다른 region (B). A-B network 끊김. *어느 쪽이 살아있다고 결정*?

<details><summary>답</summary>

**Quorum-based decision**:
- 정원 = 5
- Quorum = 3 (과반)
- Region A: 자기 region 의 3 node 와 연결, *quorum 보유* → 계속 동작 (leader 선출 가능, write 가능)
- Region B: 자기 region 의 2 node 만 — *quorum 미달* → write 거부, read-only 또는 정지

**왜 quorum**:
- 두 region 이 *동시에* leader 선출 → split brain
- *과반 합의* 만이 *단일 leader* 보장
- 5장의 *single-leader replication* 의 깊은 이유

**Caveat — *Sloppy quorum***:
- A 가 B 의 node 까지 *임시 substitute* 로 사용 가능 (Cassandra)
- *Availability 우선*, *consistency 약화*
- 데이터 *임시 위치* 에 저장 → partition 회복 시 *hinted handoff*

**산업 구조**:
- 3 region 의 *3-3-3* (9 node) 으로 *어떤 1 region 실패도 quorum 유지*
- *Region 간 sync vs async* trade-off (5장)

</details>

### Q8. 면접 — "MongoDB 가 *데이터 손실* 이 보고됐는데?"

Aphyr (Kyle Kingsbury) 의 Jepsen test 가 *여러 NoSQL DB* 의 데이터 손실 발견. MongoDB 의 사례는?

<details><summary>답</summary>

**Aphyr 의 발견 패턴**:
1. *Network partition* injection
2. 일부 *write* 후 partition 해제
3. *손실되거나 잘못된 read* 검출

**MongoDB 의 옛 (< 3.2) 사례**:
- *Default write concern* 가 `w: 1` (한 node 만 확인)
- Primary 가 partition 후 *옛 primary 의 commit* 가 *새 primary 에 안 propagate*
- Partition 해제 시 *옛 primary 의 데이터 rollback*

**대응 (현대 MongoDB)**:
- `w: "majority"` write concern — quorum 까지 wait
- `readConcern: "majority"` — quorum-replicated read
- *replica set election* 이 *epoch-based fencing*

**더 깊은 교훈**:
1. **Default 신뢰 금지** — production 에선 *명시적 strong consistency 옵션*
2. **Test under partition** — Jepsen 같은 fault injection 자동화
3. **Document carefully** — DB 의 *정확한 guarantee* 파악
4. **Verify with formal model** — TLA+ 의 spec
5. **Periodically validate** — 환경 변화 후 재검증

**산업 변화**:
- Aphyr 의 reports 이후 모든 major NoSQL DB 의 *consistency 큰 개선*
- MongoDB, Cassandra, RethinkDB, etcd 등 *Jepsen test 의 기준* 됨
- 새 system 의 *Jepsen 검증* 이 마케팅 자료

답 핵심 — "*조건을 명시* 안 한 NoSQL 은 *어떤 consistency 도 보장 안 함*". 사용 전 *정확한 옵션* 확인. 그리고 *적정 test* 가 필수.

</details>
