# Ch 11 Robot Control — 퀴즈

> 10 문항.

### Q1. PID 3 항

P / I / D 의 역할 + 부족할 때 증상.

<details><summary>답</summary>

| 항 | 역할 | 부족 시 증상 |
|--|--|--|
| P | error 크기 비례 토크 | tracking 늦음, slow response |
| I | steady-state error 적분 | constant offset 안 사라짐 |
| D | error 변화율 억제 | oscillation, overshoot |

D 너무 크면 noise 증폭. I 너무 크면 wind-up.

</details>

### Q2. Computed-torque 의 error dynamics

`τ = M(θ)(θ̈_d + K_p e + K_d ė) + c + g` 대입 시 error ODE.

<details><summary>답</summary>

Manipulator: `M(θ) θ̈ + c + g = τ`.

대입: `M(θ) θ̈ = M(θ)(θ̈_d + K_p e + K_d ė)`.

`M(θ) (θ̈_d − θ̈) = M(θ) (K_p e + K_d ė)`. 즉 `M(θ) ë = M(θ)(K_p e + K_d ė)`. 부호 정리:

`M(θ) (ë + K_d ė + K_p e) = 0` → `M` invertible → **`ë + K_d ė + K_p e = 0`**.

각 joint *독립 linear* 2nd-order ODE. `K_p, K_d` 자유 선택.

</details>

### Q3. Critical damping

joint ODE `ë + K_d ė + K_p e = 0` 가 *critical damping* 인 조건.

<details><summary>답</summary>

특성방정식 `s² + K_d s + K_p = 0`. discriminant `K_d² − 4 K_p = 0` 일 때 *critical damping*. 즉:

$$K_d = 2\sqrt{K_p}$$

→ overshoot 없으면서 가장 빠른 settling. 또는 damping ratio `ζ = K_d / (2√K_p) = 1`.

`ζ > 1`: overdamped (느림). `ζ < 1`: underdamped (overshoot).

</details>

### Q4. Task-space PID

EE 의 desired pose `T_d`, current `T`. body twist error `V_e = log(T⁻¹ T_d)` 계산.

<details><summary>답</summary>

`T_e = T⁻¹ T_d` (current 에서 desired 로의 transform, body frame).

`V_e = log(T_e)` → se(3) 6-vector. *body frame* 의 *desired motion*.

```python
T_err = inv(T) @ T_d
V_err = matrix_log_se3(T_err)   # (ω_b, v_b)
F_d = K_p @ V_err + K_d @ V_err_dot
tau = J_b.T @ F_d
```

`J_b` = body Jacobian. frame 일치 (body twist ↔ body Jacobian).

</details>

### Q5. Force control 의 stability

robot 이 *rigid wall* 에 force control 적용 시 instability 원인.

<details><summary>답</summary>

rigid wall stiffness `k → ∞`. robot 이 wall 에 살짝 닿으면 force `F = k · δ` 가 *폭증*. controller 가 measured force 줄이려고 retract 하면 contact lost → F=0 → 다시 push... **limit cycle (oscillation)**.

해결:
- *Force filtering* (low-pass)
- *Velocity damping* — push 속도 제한
- *Impedance control* 로 전환 (직접 force 대신 *spring 거동*)
- 환경 estimation + adaptive control

</details>

### Q6. Hybrid control selection

EE 가 표면 *닦기* — task frame 의 `ẑ` 가 surface normal. selection matrix.

<details><summary>답</summary>

(twist 순서 `(ω_x, ω_y, ω_z, v_x, v_y, v_z)` 가정)

- *force control* in `v_z` (surface 수직 force)
- *motion control* in `v_x, v_y` (surface 면 내 이동)
- *motion control* in `ω_z` (orientation 유지)
- `ω_x, ω_y` 는 보통 surface 접촉 유지로 *motion control* (0)

`S = diag(0, 0, 0, 0, 0, 1)`. (force 항만 `v_z` 활성.)

motion control 부분: `(I − S) = diag(1, 1, 1, 1, 1, 0)`.

</details>

### Q7. Impedance control 의 stiffness 결정

medical 협동 robot — 사람과 협업. `K_d`, `B_d`, `M_d` 의 상대값.

<details><summary>답</summary>

**부드러운 응답** 우선:
- `K_d`: 작게 (수십 N/m 정도) — 사람이 *쉽게 밀 수 있음*
- `B_d`: 중간 (critical-damped 정도) — oscillation 방지
- `M_d`: 작게 (수 kg 정도) — *가볍게 느껴짐*

critical damping: `B_d ≈ 2√(K_d · M_d)`.

대조 — *Industrial precise*: `K_d` 매우 크게 (수천 N/m), 단단함.

</details>

### Q8. Lyapunov stability

`V = ½ eᵀ K_p e + ½ ėᵀ M(θ) ė`. computed-torque control 의 `V̇` 계산.

<details><summary>답</summary>

`V̇ = eᵀ K_p ė + ėᵀ M ë + ½ ėᵀ Ṁ ė`.

`M ë = −M K_p e − M K_d ė` (error dynamics, K_d 곱):

`ėᵀ M ë = −ėᵀ M K_p e − ėᵀ M K_d ė`.

대입 + passivity `Ṁ − 2C` skew 같이 정리하면:

`V̇ = −ėᵀ M K_d ė ≤ 0`.

negative semi-definite — *stability*. LaSalle invariance principle 로 *asymptotic*.

(상세 유도는 책 §11.4.2.)

</details>

### Q9. Adaptive control 필요성

robot 이 *unknown payload* 를 잡고 작업. controller 가?

<details><summary>답</summary>

payload 가 *EE inertia* 와 *gravity 토크* 에 영향. nominal model 에서 차이 → tracking error.

**Adaptive control**:
- payload mass `m̂`, inertia `Î` 를 *online estimate*
- error 가 클수록 estimate 갱신
- gradient-based update law: `m̂̇ = −γ ėᵀ (...) g`

장점: payload 정확 측정 안 해도 *수렴*.
단점: persistent excitation 필요, 초기 수렴 시간.

Slotine-Li adaptive controller (1987) 가 표준.

</details>

### Q10. Sim2Real

simulation 에서 *완벽한* controller 가 real robot 에서 *작동 안 함*. 4 원인 + 처방.

<details><summary>답</summary>

**원인**:
1. **Model mismatch** — sim 의 mass, friction, joint flex 가 real 과 다름
2. **Sensor noise** — sim 은 perfect, real 은 noise / delay
3. **Actuator dynamics** — sim 은 ideal torque source, real 은 motor + gearbox
4. **Communication delay** — control loop 의 latency

**처방**:
1. **Domain randomization** — sim training 시 *parameter 무작위화* (mass, friction 분포)
2. **System identification** — real robot 의 parameter *측정* → sim model 갱신
3. **Robust / adaptive control** — bounded uncertainty 에 robust
4. **Fine-tuning on real** — sim policy → real 에서 추가 학습

산업 표준: Isaac Gym (sim) + domain randomization + small real-robot fine-tune.

</details>
