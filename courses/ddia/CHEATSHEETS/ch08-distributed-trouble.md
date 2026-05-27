# Ch 8 Distributed Trouble — 치트시트

## TL;DR

- **Single → Distributed**: partial failure, unreliable network, unreliable clock, non-determinism, no global state
- **Network**: timeout 만이 dead 판정 도구. *bounded delay 없음*. retry + circuit breaker + hedged request
- **Clock**: time-of-day (NTP, ~100ms) vs monotonic (interval). *LWW 위험* — clock skew
- **Process pause**: GC, swap, VM migration 으로 수 초. *split brain 위험* → fencing token
- **Failure models**: crash-stop / crash-recovery / Byzantine. datacenter 는 보통 crash-stop
- **Timing models**: sync / partial sync / async. 실용은 *partial sync*
- **Safety vs Liveness** — 9장 consensus 의 두 가지 보장

---

## Quick Reference

### 표 1. Distributed 의 5 도전

| 도전 | 영향 |
|--|--|
| Unreliable network | request/response 모두 lost 가능 |
| Unreliable clock | LWW 잘못, ordering 부정확 |
| Partial failure | 일부만 실패, 진단 어려움 |
| Non-determinism | 같은 input 다른 결과 |
| No global state | snapshot 불가, 합의 필요 |

### 표 2. Network — 6 packet 운명

```
1. 정상 도달
2. Drop (router queue full)
3. Delayed (congestion)
4. Reorder (다른 path)
5. Duplicate (router 오류)
6. Corrupt (전송 오류)

→ TCP 가 2,5,6 일부 해결
→ Application 까지 도달하는 건: delay, reorder
```

### 표 3. Clock 종류

| | Time-of-day (wall) | Monotonic |
|--|--|--|
| 의미 | UTC | 단조 증가 |
| 사용 | 표시, log timestamp | interval 측정, timeout |
| 동기화 | NTP (~100ms) | local CPU |
| Node 간 비교 | 가능 (조심) | 불가능 |
| API | `time.time()`, `currentTimeMillis()` | `time.monotonic()`, `nanoTime()` |

### 표 4. Process pause — split brain 위험

```
Leader L (10s lease)
  ↓ GC pause 15s
Other nodes: lease expired → elect L'
  ↓
L wakes up → "I am leader" → write 시도
  ↓
Two leaders!
```

**방지**:
- Fencing token (monotonic epoch)
- STONITH (강제 kill)
- Heartbeat with monotonic check

### 표 5. Failure models

| 모델 | 가정 | 적용 |
|--|--|--|
| Crash-stop | 실패=정지 | 단순 datacenter |
| Crash-recovery | 정지 후 복귀 | 실용 표준 |
| Byzantine | 거짓말 가능 | blockchain, multi-org |

### 표 6. Timing models

| 모델 | 가정 | 알고리즘 적용 |
|--|--|--|
| Synchronous | bounded delay 보장 | 거의 없음 (이상화) |
| Partial sync | 대부분 sync | 대부분 실용 algorithm |
| Asynchronous | 가정 없음 | 이론 (FLP impossibility) |

### 표 7. CAP vs PACELC

```
CAP (혼동 주의):
  Partition 시 → Consistency or Availability
  (정상 시엔 둘 다 가능)

PACELC (정확):
  Partition 시 → A or C
  Else (정상 시) → Latency or Consistency

산업 예시:
  CP+EC: Postgres sync replication, etcd, ZooKeeper
  AP+EL: Cassandra, DynamoDB, Riak
```

---

## Mind Map

```
8장 Distributed Trouble
├─ 1. Partial failure (single 과 질적 차이)
├─ 2. Unreliable network
│   ├─ 6 packet 운명
│   ├─ Timeout 의 어려움
│   └─ Async vs sync network
├─ 3. Unreliable clock
│   ├─ Time-of-day vs monotonic
│   ├─ NTP 의 한계
│   ├─ LWW 의 위험
│   └─ Logical / HLC / TrueTime
├─ 4. Process pause
│   ├─ GC, swap, VM migration
│   └─ Fencing token (split brain 방지)
├─ 5. Truth & lies
│   └─ Crash-stop vs Byzantine
└─ 6. System models
    ├─ Timing: sync / partial / async
    └─ Safety vs Liveness
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | partial failure 가 distributed 의 근본 도전 |
| 2 | network 는 timeout 만이 dead 판정. async, unbounded |
| 3 | clock 부정확. wall vs monotonic, LWW 위험 |
| 4 | process pause → split brain. fencing token 필수 |
| 5 | Byzantine 가정은 보통 불필요. crash-stop 으로 충분 |
| 6 | system model 명시 필수. safety + liveness |
