# Ch 9 Trajectory Generation — 치트시트

## TL;DR

- **Path** (geometric) + **time scaling** `s(t)` = **Trajectory** `θ(t) = θ(s(t))`
- **Cubic**: `s = 3(t/T)² − 2(t/T)³`. `s̈` jumps.
- **Quintic**: `s = 10(t/T)³ − 15(t/T)⁴ + 6(t/T)⁵`. `s̈` continuous.
- **Trapezoidal**: a → const v → −a. industrial standard.
- **S-curve**: 7 phases, *jerk-bounded*. premium.
- **SE(3) 보간**: `T(s) = T_start · exp([log(T_start⁻¹ T_end)] s)` (not linear!)
- **Time-optimal**: phase plane bang-bang U(s, ṡ) ↔ L(s, ṡ).

---

## Quick Reference

### 표 1. Time scaling 비교

| 방법 | 식 | continuous | jerk-bounded |
|--|--|--|--|
| Cubic | `3(t/T)² − 2(t/T)³` | s, ṡ | No |
| Quintic | `10(t/T)³ − 15(t/T)⁴ + 6(t/T)⁵` | s, ṡ, s̈ | No |
| Trapezoidal | piecewise (a, v, −a) | s, ṡ | No |
| S-curve | 7 phases | s, ṡ, s̈ | **Yes** |

### 표 2. Path vs Trajectory

| | Path | Trajectory |
|--|--|--|
| 변수 | `θ(s)`, `s ∈ [0,1]` | `θ(t)`, `t ∈ [0,T]` |
| 의미 | 어디로 | 얼마나 빨리 |
| 결정 | planner (10장) | time scaling |
| input | start, end, obstacles | path + dynamics |

### 표 3. Cubic time scaling 의 모든 값

| 변수 | 식 |
|--|--|
| `s(t)` | `3(t/T)² − 2(t/T)³` |
| `ṡ(t)` | `(6t/T² − 6t²/T³)` |
| `s̈(t)` | `(6/T² − 12t/T³)` |
| `s̈(0)` | `6/T²` ← jumps from 0 |
| `s̈(T)` | `−6/T²` |
| `ṡ_max` | `1.5/T` (at t = T/2) |

### 표 4. Quintic time scaling 의 모든 값

| 변수 | 식 |
|--|--|
| `s(t)` | `10(t/T)³ − 15(t/T)⁴ + 6(t/T)⁵` |
| `ṡ(t)` | `30(t/T)² − 60(t/T)³ + 30(t/T)⁴` (× 1/T) |
| `s̈(0), s̈(T)` | `0` ✓ |
| `ṡ_max` | `1.875/T` (at t = T/2) |
| `s̈_max` | `5.77/T²` |

### 표 5. Trapezoidal 의 식

| 구간 | s(t) | ṡ(t) |
|--|--|--|
| [0, t_a] | `½ a t²` | `a t` |
| [t_a, T−t_a] | `a t_a²/2 + v(t − t_a)` | `v` |
| [T−t_a, T] | symmetric (감속) | `a(T − t)` |

조건: `T = 1/v + v/a` (등속 phase 존재 시).

### 표 6. Joint vs Cartesian trajectory

| | Joint-Space | Cartesian-Space |
|--|--|--|
| 좌표 | `θ ∈ R^n` | `T ∈ SE(3)` |
| IK 호출 | 한 번 (시작·끝) | 매 step |
| EE path | curved | straight (configurable) |
| Singularity | 무관 | 영향 |
| Joint limit | 자연 | 검사 |
| 적용 | 일반 PTP | weld, paint, contour |

### 표 7. SE(3) vs SO(3) 보간

| 객체 | 보간 |
|--|--|
| SO(3) | quaternion SLERP 또는 `R_start · exp([log(R_start⁻¹ R_end)] s)` |
| SE(3) | `T_start · exp([log(T_start⁻¹ T_end)] s)` |
| Trans. only | linear `(1−s)p_start + s p_end` |
| Rotation only | SLERP (quaternion) |

---

## Mind Map

```
9장 Trajectory Generation
├─ 1. Path vs Trajectory (s 분리)
├─ 2. Point-to-point time scaling
│   ├─ Cubic (s, ṡ 연속)
│   ├─ Quintic (s, ṡ, s̈ 연속)
│   ├─ Trapezoidal (industrial)
│   └─ S-curve (jerk-bounded)
├─ 3. Via-point interpolation
│   ├─ Cubic per segment
│   ├─ Catmull-Rom heuristic
│   └─ B-spline
├─ 4. Joint vs Cartesian space
│   └─ SE(3) exp interpolation
└─ 5. Time-optimal (bang-bang on phase plane)
```

---

## 자주 쓰는 식

### Trajectory 정의

```
θ(t) = θ_start + (θ_end − θ_start) · s(t),   t ∈ [0, T]
θ̇(t) = (θ_end − θ_start) · ṡ(t)
θ̈(t) = (θ_end − θ_start) · s̈(t)
```

### Quintic (가장 추천)

```python
def quintic_s(t, T):
    x = t / T
    s   = 10*x**3 - 15*x**4 + 6*x**5
    ds  = (30*x**2 - 60*x**3 + 30*x**4) / T
    dds = (60*x   - 180*x**2 + 120*x**3) / T**2
    return s, ds, dds
```

### SE(3) screw interpolation

```python
def se3_interp(T_start, T_end, s):
    T_rel = inv(T_start) @ T_end
    log_T = matrix_log_se3(T_rel)   # se(3) vector
    return T_start @ matrix_exp_se3(log_T * s)
```

### Trapezoidal 의 파라미터 결정

```python
def trapezoidal_params(v_max, a_max):
    t_a = v_max / a_max                 # 가속 시간
    if v_max**2 / a_max <= 1:
        T = 1/v_max + v_max/a_max       # 정상 trapezoidal
        triangular = False
    else:
        T = 2 * sqrt(1/a_max)           # 가속·감속만
        v_actual = a_max * T / 2
        t_a = T / 2
        triangular = True
    return T, t_a, triangular
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | path(기하) × time scaling = trajectory |
| 2 | cubic 단순 / quintic smooth / trapezoidal industrial / S-curve premium |
| 3 | via-point cubic, Catmull-Rom ṡ_j heuristic |
| 4 | joint(IK-free) vs Cartesian(EE 직선) trade-off |
| 5 | time-optimal = bang-bang on (s, ṡ) phase plane |
