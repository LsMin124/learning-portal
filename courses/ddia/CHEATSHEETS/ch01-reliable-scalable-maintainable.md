# Ch 1 Reliable, Scalable, Maintainable — 치트시트

## TL;DR

- **세 가지 차원** — Reliability / Scalability / Maintainability. 책 전체의 *평가 기준*.
- **Reliability**: fault (component) vs failure (system). 3 종 fault: hardware / software / human. 막는 게 아니라 *견디는* 것.
- **Scalability**: *load → performance* 의 함수. 1차원 라벨 X. *어떤 axis* 에서 *얼마만큼* scale 하느냐.
- **Twitter fan-out**: read-time SQL join vs write-time fan-out cache. R:W ratio 에 따라 정답 다름.
- **Performance**: response time = service + queueing + network. *분포* 로 봐야. mean ❌ → p50/p99/p999.
- **Tail latency amplification**: fan-out backend 의 일부 tail 이 사용자 tail 로 증폭.
- **Maintainability**: operability + simplicity + evolvability. simplicity 가 evolvability 의 전제.

---

## Quick Reference

### 표 1. Reliability 의 3 fault 유형

| 유형 | 특징 | 대응 |
|--|--|--|
| **Hardware** | 독립·랜덤 | RAID, multi-machine redundancy |
| **Software** | systematic — 모든 node 동시 실패 가능 | 모니터링·격리·테스트 |
| **Human** | outage 의 ~60% 원인 | sandbox, abstraction, rollback, observability |

핵심: Software / Human 은 redundancy 만으로 부족.

### 표 2. Performance metrics

| 통계 | 의미 | 사용 |
|--|--|--|
| **Mean** | outlier 끌어올림 | ❌ |
| **p50 (median)** | 전형 사용자 경험 | SLO 기본 |
| **p95, p99, p999** | tail — 최악 경험 | SLA, 큰 고객 보호 |
| **Max** | 단일 outlier | 노이즈 |

### 표 3. SLA 가동률 → 다운타임

| SLA | 다운타임/년 | 다운타임/월 |
|--|--|--|
| 99% (two nines) | 87.6h | 7.3h |
| 99.9% (three nines) | 8.77h | 43.8min |
| 99.99% (four nines) | 52.6min | 4.4min |
| 99.999% (five nines) | 5.3min | 26.3s |

각 *9 추가* 가 *engineering cost 기하급수* 증가.

### 표 4. Twitter fan-out 두 접근

| | Approach 1 (read-time JOIN) | Approach 2 (write-time fan-out) |
|--|--|--|
| Read | 비쌈 (JOIN) | 저렴 (cache 조회) |
| Write | 저렴 (1 row insert) | 비쌈 (75 follower 평균, 셀럽 30M) |
| 적합 | low read:write | **high read:write** |
| Twitter 채택 | ✗ (struggled) | ✓ (셀럽은 hybrid) |

핵심 load parameter: *follower 수 분포* (fat-tail).

### 표 5. Scaling 전략

| 전략 | 의미 | 적합 |
|--|--|--|
| **Scale up (vertical)** | 더 강한 머신 | small load, 단순 |
| **Scale out (horizontal)** | 머신 수 증가 | large load, 분산 OK |
| **Elasticity** | 자동 조정 | unpredictable load |
| **Manual** | 수동 | predictable load |

### 표 6. Maintainability 의 3 원칙

| 원칙 | 의미 | 주체 |
|--|--|--|
| **Operability** | 운영 원활 | ops/SRE |
| **Simplicity** | 이해 쉬움 | 개발자 |
| **Evolvability** | 변경 쉬움 | 조직 |

연쇄: simplicity → evolvability + operability.

### 표 7. Tail latency 대응

| 기법 | 의미 |
|--|--|
| **Hedged request** | 같은 요청 2 backend, 빠른 응답 사용 |
| **Timeout + fallback** | 비핵심 sub-call 은 잘라냄 |
| **Parallel sub-calls** | sequential X, max 만 보임 |
| **HdrHistogram / t-digest** | percentile 정확 측정 |

### 표 8. Golden Signals (모니터링)

| Signal | 의미 |
|--|--|
| **Latency** | request 처리 시간 (p50, p99) |
| **Traffic** | request rate, QPS |
| **Errors** | 실패율 |
| **Saturation** | resource 포화도 (CPU%, queue depth) |

USE: Utilization, Saturation, Errors (resource 관점).
RED: Rate, Errors, Duration (service 관점).

---

## Mind Map

```
1장 Reliable, Scalable, Maintainable
├─ 1. Data systems building blocks
│   └─ DB / Cache / Search / Stream / Batch
├─ 2. Reliability
│   ├─ fault vs failure
│   ├─ hardware: redundancy
│   ├─ software: monitoring + isolation
│   └─ human: abstraction + sandbox + rollback
├─ 3. Scalability
│   ├─ load: load parameters (Twitter fan-out 예제)
│   ├─ performance: response time 분포
│   │   ├─ p50 (median) — 전형
│   │   ├─ p99, p999 — tail
│   │   └─ tail amplification
│   └─ coping: vertical / horizontal / elastic
└─ 4. Maintainability
    ├─ operability — ops 친화
    ├─ simplicity — abstraction
    └─ evolvability — change easy
```

---

## Anti-pattern 체크리스트

| ❌ Anti-pattern | ✓ 대응 |
|--|--|
| Mean response time 으로 SLO | p50 + p99 + p999 |
| "Scalable system" 라벨링 | "어떤 axis 에서 X배 scale" |
| Hardware redundancy 만 | + software/human 대응 |
| 모든 시스템이 100k QPS 처음부터 | 측정 후 단계적 |
| 60+ 그래프 dashboard | Golden Signals 4~6개 |
| fault 0 목표 | fault tolerance 목표 |

---

## 1-line summary per section

| 절 | 한 줄 요약 |
|--|--|
| 1 | data system 의 building blocks 와 3 차원 (R/S/M) |
| 2 | fault ≠ failure. 3 종 fault, 각각 다른 대응 |
| 3 | scale 은 axis. Twitter fan-out 예제로 load parameter, percentile, scaling 전략 |
| 4 | maintainability = operability + simplicity + evolvability |
