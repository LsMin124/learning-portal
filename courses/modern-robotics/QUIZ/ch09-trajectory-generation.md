# Ch 9 Trajectory Generation — 퀴즈

> 10 문항.

### Q1. Path vs Trajectory

차이 + 왜 분리하는지.

<details><summary>답</summary>

- Path: 기하학적 경로 `θ(s)`, 시간 무관
- Trajectory: `θ(t) = θ(s(t))`, path + time scaling

분리 이유: *기하* (collision-free) 와 *동역학* (torque limit, smoothness) 가 *독립적 관심사*. 단계 분리로 planner 와 controller 의 역할 명확.

</details>

### Q2. Cubic time scaling 식

`s(0)=0, s(T)=1, ṡ(0)=ṡ(T)=0` 의 cubic.

<details><summary>답</summary>

$$s(t) = 3\left(\frac{t}{T}\right)^2 - 2\left(\frac{t}{T}\right)^3$$

검증: `s(0) = 0`, `s(T) = 3 − 2 = 1`. `ṡ(0) = 0`, `ṡ(T) = 6/T − 6/T = 0`. ✓

</details>

### Q3. Cubic 의 s̈ 문제

`s̈(0)` 과 `s̈(T)` 의 값. 왜 문제?

<details><summary>답</summary>

`s̈(t) = 6/T² − 12 t/T³`. `s̈(0) = 6/T² > 0`, `s̈(T) = 6/T² − 12/T² = −6/T²`.

→ 둘 다 0 아님. `t = 0⁻` 에서 `s̈ = 0` 이었다가 `t = 0⁺` 에서 `6/T²` 로 *jump*. joint acceleration 의 step 발생 → 무한 jerk → 부드럽지 않음 + mechanical shock.

해결: quintic (`s̈(0) = s̈(T) = 0` 추가).

</details>

### Q4. Quintic 식

quintic time scaling 닫힌 형태.

<details><summary>답</summary>

$$s(t) = 10\left(\frac{t}{T}\right)^3 - 15\left(\frac{t}{T}\right)^4 + 6\left(\frac{t}{T}\right)^5$$

6 boundary condition: `s(0) = 0, s(T) = 1, ṡ(0) = ṡ(T) = 0, s̈(0) = s̈(T) = 0`. 6 계수, 5차 polynomial.

</details>

### Q5. Trapezoidal 의 t_a 결정

max velocity `v`, max acceleration `a` 가 주어졌을 때 가속 시간 `t_a`.

<details><summary>답</summary>

가속 phase: `ṡ(t) = a t`. `ṡ(t_a) = v` → `t_a = v / a`.

조건: `∫_0^T ṡ dt = 1` (총 path = 1). 등속 phase 길이 `T − 2 t_a` 와 가속·감속 phase 의 면적:

`1 = a t_a²/2 + v (T − 2 t_a) + a t_a²/2 = v (T − t_a)` (가속/감속이 한 삼각형씩, 그 합이 `v t_a`).

→ `T = (1 + v t_a) / v = 1/v + t_a = 1/v + v/a`.

constraint: `v t_a ≤ 1` (가속만으로도 path 다 끝나면 안 됨). 즉 `v²/a ≤ 1` 또는 `v ≤ √a`.

만약 `v > √a` 면 *triangular profile* (가속·감속만, 등속 없음).

</details>

### Q6. SE(3) 보간

`T_start, T_end ∈ SE(3)` 사이의 *constant-screw* 보간.

<details><summary>답</summary>

$$T(s) = T_{start} \cdot \exp\left(\left[\log(T_{start}^{-1} T_{end})\right] s\right), \quad s \in [0, 1]$$

직관:
1. `T_{start}⁻¹ T_{end}` = start 에서 end 로 가는 *local* transform
2. `log(...)` = 그 transform 의 *screw axis 와 거리* (se(3) 벡터)
3. `exp(... · s)` = `s` 비율의 motion
4. `T_start ·` = world frame 으로 변환

`s = 0`: T_start, `s = 1`: T_end, 중간 부드럽게.

</details>

### Q7. Cartesian 보간 함정

`T(s) = (1−s) T_start + s T_end` 가 SE(3) 보간으로 *잘못된* 이유.

<details><summary>답</summary>

SE(3) 은 *vector space 아님*. linear combination 결과가 일반적으로 SE(3) 안에 *있지 않음*:
- 회전 부분: `(1−s) R_start + s R_end` 가 SO(3) 가 아님 (`RᵀR ≠ I`)
- 결과 행렬에 `det = 0` 또는 비-orthogonal R 발생

올바른: exponential interpolation (위 Q6) 또는 quaternion SLERP (회전만).

</details>

### Q8. Via-point 의 ṡ 결정

Catmull-Rom heuristic 으로 via-point `θ_j` 의 `θ̇_j` 정하기.

<details><summary>답</summary>

Catmull-Rom (centripetal 변형 제외):

$$\dot\theta_j = \frac{\theta_{j+1} - \theta_{j-1}}{T_{j+1} - T_{j-1}}$$

즉 양옆 via-point 의 *기울기 평균*. 양 끝 (j=0 or j=k) 은 *one-sided* 또는 `0`.

장점: closed-form, 부드러움 자동.
단점: control 안 됨, dynamics 무시.

</details>

### Q9. Joint-space vs Cartesian 선택

다음 task 각각에 어느 trajectory space 선택?

(a) Welding torch 가 직선을 그으며 용접
(b) Robot 이 pick-and-place 의 *중간 어디든* 통과
(c) UR5 로 sphere 의 표면 점들을 차례로 방문

<details><summary>답</summary>

(a) **Cartesian** — EE 직선이 task. joint-space 직선 → EE 곡선이라 부적합.

(b) **Joint** — 중간 경로는 상관 없음. joint-space 가 빠르고 singularity-free.

(c) **Cartesian** — sphere 표면 = task 정의. 그러나 *singular configuration* 우회 필요할 수 있음.

</details>

### Q10. Time-optimal 의 한계

bang-bang trajectory 가 *real robot* 에서 *그대로* 동작 안 하는 이유 + 실용적 처방.

<details><summary>답</summary>

**이유**:
1. **Model error** — `M(θ), c, g, friction` 모두 nominal. 실제 ↔ 모델 ε% error → tracking error 누적.
2. **Torque saturation 정확도** — 모터 실제 max torque 가 정격값과 다름 (온도, 마모).
3. **Unmodeled dynamics** — joint flexibility, gear backlash, vibration.
4. **Sensor noise** — `θ, θ̇` 측정 오차.

**처방**:
- *safety margin*: `τ_max → 0.8 τ_max` 로 sub-optimal 하지만 robust
- *trajectory replanning*: tracking error 누적 시 re-generate
- *feedback control* (11장) — feed-forward bang-bang + PID correction
- *robust / adaptive control*: bounded uncertainty 안에서 안정성 보장

</details>
