# Chapter 9: Trajectory Generation — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 9: Trajectory Generation** (책 p.325~352) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 9장의 핵심: **path** + **time scaling** = **trajectory**. 부드러운 `θ(t), θ̇(t), θ̈(t)` 를 생성하여 11장 control 의 reference 로 공급.

## 들어가기 전에

- **선수 지식**
  - 4~6장: FK, Jacobian, IK
  - 8장: manipulator equation (inverse dynamics 의 reference 가 trajectory)
  - 미적분: 보간 다항식, 적분
- **학습 목표**
  1. **Path vs Trajectory** 의 명확한 구분
  2. **Point-to-point time scaling** — cubic, quintic, trapezoidal, S-curve
  3. **Via-point interpolation** — 여러 waypoint 사이 부드러운 보간
  4. **Cartesian-space vs Joint-space** trajectory 의 trade-off
  5. **Time-optimal trajectory** — phase plane 의 bang-bang
- **예상 학습 시간**: 60~90분

---

## 1. Path vs Trajectory — 명확한 구분

### 1.1 정의

> **Path**: configuration space 안의 *기하학적 곡선* — `θ(s)`, `s ∈ [0, 1]` (시간 무관).
>
> **Trajectory**: *시간* 에 매개변수화된 path — `θ(t)`, `t ∈ [0, T]`. = path + time scaling `s(t)`.

요컨대:

$$\theta(t) = \theta(s(t))$$

- `θ(s)`: 어디로 갈지 (geometric)
- `s(t)`: 얼마나 빨리 갈지 (dynamic)

### 1.2 왜 분리?

- *기하* (collision-free path) 와 *동역학* (torque limit, smoothness) 가 *독립적 관심사*
- planner 가 path 만 풀고, 이후 time scaling 으로 dynamics 반영
- **2단계 trajectory generation**: ① path 결정 → ② time scaling

![Figure 9.1 — 2R robot 의 joint-space straight-line vs task-space curve. 교재 p.327](/courses/modern-robotics/figures/ch09/fig-9-1.png)

> **함정 1**: joint-space straight-line 이 task-space straight-line 과 *대응하지 않음*. 두 공간이 *비선형* 관계 (FK 가 비선형). path 가 어디서 표현되는지 명시.

---

## 2. Point-to-Point Time Scaling

가장 단순한 trajectory: `θ_start` 에서 `θ_end` 로 한 번에 이동. `s(t)` 결정.

`s(0) = 0`, `s(T) = 1`, `ṡ(0) = ṡ(T) = 0` 의 boundary condition. T = 총 시간.

### 2.1 Cubic polynomial

$$s(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3$$

4 boundary condition 으로 4 계수 결정:
- `a_0 = 0`
- `a_1 = 0`
- `a_2 = 3/T²`
- `a_3 = −2/T³`

따라서:

$$s(t) = \frac{3 t^2}{T^2} - \frac{2 t^3}{T^3}, \quad \dot{s}(t) = \frac{6t}{T^2} - \frac{6t^2}{T^3}$$

**Pros**: 단순.
**Cons**: `s̈(0), s̈(T)` 가 *불연속* — joint acceleration 의 *jump* → 부드럽지 않음.

### 2.2 Quintic (5th-order) polynomial

`s̈(0) = s̈(T) = 0` 추가 → 6 condition → 5차 다항식.

$$s(t) = 10 \left(\frac{t}{T}\right)^3 - 15 \left(\frac{t}{T}\right)^4 + 6 \left(\frac{t}{T}\right)^5$$

![Figure 9.4 — Quintic time scaling 의 s(t), ṡ(t), s̈(t). 교재 p.331](/courses/modern-robotics/figures/ch09/fig-9-4.png)

**Pros**: `s̈` 도 연속 — 더 smooth, 8장 dynamics 와 호환성 ↑.
**Cons**: 약간 더 복잡.

### 2.3 Trapezoidal motion profile

세 구간:
- `[0, t_a]`: 가속 (constant `s̈ = a`)
- `[t_a, T − t_a]`: 등속 (`ṡ = v`)
- `[T − t_a, T]`: 감속 (constant `s̈ = −a`)

![Figure 9.5 — Trapezoidal motion profile. 교재 p.331](/courses/modern-robotics/figures/ch09/fig-9-5.png)

조건: `v · t_a = a · t_a²/2` 처럼 면적이 1 이 되어야 (`∫ ṡ dt = 1`).

**Pros**: max velocity / max acceleration 명시적으로 제어 가능. 산업 robot 의 표준.
**Cons**: `s̈` 가 *jump* — jerk 무한대. mechanical wear ↑.

### 2.4 S-curve time scaling

Trapezoidal 에 *jerk* 까지 제한. 7 구간 (constant-jerk 의 시작·끝):

`[acc-jerk, acc-const, acc-dejerk, vel-const, dec-jerk, dec-const, dec-dejerk]`

**Pros**: jerk bounded → 가장 smooth. 고급 robot controller (KUKA, ABB) 기본.
**Cons**: 7 구간의 파라미터 결정 복잡.

### 2.5 비교

| Method | smooth | jerk bounded | computation |
|--|--|--|--|
| Cubic | s, ṡ | No (s̈ jumps) | trivial |
| Quintic | s, ṡ, s̈ | No (still s̈⃛ jumps) | trivial |
| Trapezoidal | s, ṡ | No | simple |
| S-curve | s, ṡ, s̈ | **Yes** | medium |

---

## 3. Via-Point Interpolation

여러 waypoint `θ_0, θ_1, ..., θ_k` 를 *부드럽게* 잇기.

### 3.1 Cubic 보간 (연속 ṡ)

각 구간 `[T_j, T_{j+1}]` 에 cubic polynomial. 인접 구간이 `β(T_j), β̇(T_j)` 일치.

$$\beta_j(t) = a_{j0} + a_{j1}(t - T_j) + a_{j2}(t - T_j)^2 + a_{j3}(t - T_j)^3$$

각 구간 4 계수, `β̇_j` 가 *주어졌으면* 닫힌 형태로 풀이 가능.

![Figure 9.8 — Cubic via-point interpolation 의 시간 사상. 교재 p.335](/courses/modern-robotics/figures/ch09/fig-9-8.png)

### 3.2 ṡ_j 결정 (heuristic)

각 via-point 에서의 `ṡ_j` 가 주어지지 않으면 보통:
- *Catmull-Rom*: 양쪽 via-point 의 평균 기울기
- *Hermite*: 사용자 명시
- *최적화 기반*: 적분 jerk² 최소화

### 3.3 B-spline (간단)

다항식 한 조각 대신 *base function* 의 합으로 부드러운 곡선. CAD 의 표준. 모든 control point 가 *near* 일 뿐 *통과 안 함* (단 *interpolating B-spline* 변형 가능).

---

## 4. Joint-Space vs Cartesian-Space Trajectory

### 4.1 Joint-Space trajectory

`θ_d(t)` 직접 — joint 변수의 시간 함수.

**Pros**: joint limit 보장 자연, FK 만 호출 (IK 안 필요), singularity 무관.
**Cons**: EE path 가 *기하학적으로 직관적이지 않음* (curved in task space).

### 4.2 Cartesian-Space trajectory

`T_d(t)` 또는 `(x_d(t), R_d(t))` — EE pose 의 시간 함수.

**Pros**: task 표현 자연 (예: "EE 가 직선으로 이동").
**Cons**: 매 step *IK* 호출 필요, singular 근처 trajectory 발산.

### 4.3 비교 표

| 측면 | Joint-Space | Cartesian-Space |
|--|--|--|
| 좌표 | `θ ∈ R^n` | `T ∈ SE(3)` |
| 시간 분해 | `θ(s(t))` | `T(s(t))` |
| 매 step IK | 불필요 | 필요 |
| Singularity | 무관 | 영향 받음 |
| EE path | 곡선 | 직선 가능 |
| Joint limit | 자연 | 검사 필요 |

> **함정 2**: SE(3) 의 *직선* 은 *exponential interpolation* `T_d(s) = T_{start} e^{[log(T_{start}⁻¹ T_{end})]s}` — 단순 `(1-s)T_start + s T_end` 가 *아님* (SE(3) 비-vector).

---

## 5. Time-Optimal Time Scaling

### 5.1 문제

Path `θ(s)` 가 주어졌을 때 *최소 시간* `T` 로 통과하면서 joint torque limit `τ_min ≤ τ ≤ τ_max` 만족.

### 5.2 Phase plane (s, ṡ)

trajectory 를 `(s, ṡ)` 평면의 곡선으로 표현. 각 점에서:
- **U(s, ṡ)**: maximum 가능 가속도 `s̈`
- **L(s, ṡ)**: minimum 가능 가속도 `s̈`

`s̈ ∈ [L(s, ṡ), U(s, ṡ)]`. *bang-bang* (extreme) 이 time-optimal.

![Figure 9.12 — Time-optimal bang-bang time scaling 의 phase plane. 교재 p.341](/courses/modern-robotics/figures/ch09/fig-9-12.png)

### 5.3 알고리즘 (Bobrow-Dubowsky-Gibson)

1. `s = 0` 부터 `U` (max accel) 로 forward integrate
2. `s = 1` 부터 `L` (min accel) 로 backward integrate (역시간)
3. 두 곡선의 *교점* `s*` 에서 switch — bang-bang
4. velocity limit curve `V(s)` 가 가로막으면 multi-switch

### 5.4 적용

- pick-and-place cycle time 최소화
- production robot 최적화
- 결과: 보통 30~50% 시간 단축 vs trapezoidal

> **함정 3**: bang-bang trajectory 는 *torque saturation* 에서 작동. 실제 robot 에서 *모델 오차* 가 누적되어 tracking error 큼. 안전 margin 가지고 사용 권장.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Joint-space 직선 = task-space 직선 | 다름. FK 비선형. |
| 2 | Cubic 이 enough | `s̈` 가 step → joint 가속 jump. quintic 권장. |
| 3 | Trapezoidal 의 jerk 가 bounded | 무한 (s̈ jumps). S-curve 가 jerk-bounded. |
| 4 | SE(3) 보간 = linear interp | SE(3) 은 vector space 아님. exponential interpolation 필요. |
| 5 | Bang-bang trajectory 가 real robot 에 그대로 작동 | model error 누적 — safety margin 필수. |
| 6 | Via-point 에서 `ṡ` 자동 결정 | heuristic 선택 필요 (Catmull-Rom 등). |
| 7 | Trajectory generator 가 IK 도 풀음 | 일반적으로 separate. trajectory 는 path × time scaling. |
| 8 | T 가 클수록 부드럽지만 cycle time 손해 | trade-off — task 마다 결정. |
| 9 | `s(t)` 가 단조증가 | normally 그렇지만 *부분 후진* (예: humanoid 보행) 도 가능. |
| 10 | trajectory 가 *closed-loop* control 까지 의미 | 아님. open-loop reference 만. 11장 control 이 실제 tracking. |

---

## 자가점검

1. Path 와 trajectory 의 차이.
2. 왜 trajectory 를 path + time scaling 으로 분리?
3. Cubic 의 *boundary condition* 4 개와 결과 계수.
4. Quintic 의 cubic 대비 장점.
5. Trapezoidal motion profile 의 3 구간.
6. S-curve 의 7 구간 + *jerk-bounded* 의 의미.
7. Joint-space vs Cartesian-space trajectory 의 trade-off.
8. SE(3) 의 *exponential interpolation* 식.
9. Time-optimal trajectory 의 phase plane bang-bang.
10. Cubic via-point 의 각 구간 4 계수 결정 조건.

### 해답 (간략)

1. Path = 기하 (시간 무관), Trajectory = path + time scaling (시간 함수).
2. 기하 (collision-free) 와 동역학 (torque limit) 가 *독립* 관심사라 단계 분리.
3. `s(0)=0, s(T)=1, ṡ(0)=0, ṡ(T)=0` → `s(t) = 3t²/T² − 2t³/T³`.
4. `s̈(0) = s̈(T) = 0` 까지 연속 — joint acceleration 가 step 아님.
5. 가속 (constant a) → 등속 (constant v) → 감속 (constant −a).
6. acc-jerk → acc-const → acc-dejerk → vel-const → dec-jerk → dec-const → dec-dejerk. jerk `s⃛` 가 piecewise constant, bounded.
7. Joint: IK 불필요·joint-limit 자연 / Cartesian: EE path 직관·매 step IK 필요.
8. `T_d(s) = T_start · exp([log(T_start⁻¹ T_end)] s)`.
9. `(s, ṡ)` 평면에서 `U(s, ṡ)` (max accel) 로 forward → switching point → `L(s, ṡ)` (min accel) 로 stop. bang-bang.
10. `β_j(T_j) = β_j`, `β_j(T_{j+1}) = β_{j+1}`, `β̇_j(T_j) = β̇_j`, `β̇_j(T_{j+1}) = β̇_{j+1}`.

---

## 다음 학습으로

- **10장 (Motion Planning)** — path 의 *기하* 결정. 본 장은 path 가 *주어진* 상태 가정.
- **11장 (Robot Control)** — 본 장의 `θ_d(t), θ̇_d(t), θ̈_d(t)` 가 control 의 *reference signal*.
- **MPC / optimal control**: 본 장은 *offline* trajectory. real-time MPC 가 같은 trajectory 를 *closed-loop* 으로 풀이.
