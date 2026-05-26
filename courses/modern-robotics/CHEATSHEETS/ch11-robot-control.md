# Ch 11 Robot Control — 치트시트

## TL;DR

- **PID**: `τ = K_p e + K_i ∫e + K_d ė`. 단순하지만 nonlinear blind.
- **Computed-torque**: `τ = M(θ)(θ̈_d + K_p e + K_d ė) + c + g`. → linear `ë + K_d ė + K_p e = 0`.
- **Task-space**: `τ = Jᵀ F_d + c + g`. `F_d = Λ(V̇_d + K_p V_e + ...) + η + ρ` (operational space).
- **Force control**: `τ = Jᵀ F_d + g + damping`.
- **Hybrid**: selection matrix `S` 로 force/motion 분리. `S` 와 `(I−S)` orthogonal.
- **Impedance**: `M_d ë + B_d ė + K_d e = F_ext` (spring-damper-mass).
- **Critical damping**: `K_d = 2√K_p`.

---

## Quick Reference

### 표 1. Controller 비교

| Type | 식 | 적용 | 한계 |
|--|--|--|--|
| PID | `K_p e + K_i ∫e + K_d ė` | 단순 task | nonlinear 무시 |
| Computed-torque | `M(θ̈_d + K_p e + K_d ė) + c + g` | high-precision | model 의존 |
| Task-space | `Jᵀ (K_p V_e + K_d V̇_e) + c + g` | EE pose tracking | singularity |
| Force | `Jᵀ F_d + g + damping` | contact task | wall instability |
| Hybrid | `Jᵀ [S F_d + (I−S) Λ V̇_d]` | wipe, polish, assemble | constraint orthogonality |
| Impedance | `M_d ë + B_d ė + K_d e = F_ext` | HRI, compliance | tuning |

### 표 2. Error dynamics (computed-torque, perfect model)

`ë + K_d ė + K_p e = 0`

| 케이스 | 조건 | 거동 |
|--|--|--|
| Overdamped | `K_d² > 4 K_p` | slow, no overshoot |
| Critical | `K_d² = 4 K_p` | fastest no-overshoot |
| Underdamped | `K_d² < 4 K_p` | oscillation, overshoot |

### 표 3. PID 의 boundary 효과

| 항 | 부족 | 과다 |
|--|--|--|
| K_p | slow response | oscillation |
| K_d | overshoot | noise 증폭 |
| K_i | steady-state error | wind-up |

### 표 4. Task-space PID

| 객체 | 값 |
|--|--|
| EE pose | `T = T_sb(θ)` |
| Desired | `T_d` |
| Error transform | `T_e = T⁻¹ T_d` (body) |
| Error twist | `V_e = log(T_e)` (se(3) 6-vector) |
| Control | `F_d = K_p V_e + K_d V̇_e` |
| Joint torque | `τ = J_bᵀ F_d + c + g` |

### 표 5. Impedance / Admittance

| 변수 | Impedance | Admittance |
|--|--|--|
| Input | desired motion | measured force |
| Output | force | motion |
| 식 | `F = Z(s) (X_d - X)` | `X = Y(s) F_ext` |
| Robot 필요 | torque-controlled | position-controlled |
| 적용 | precise force, HRI | low-inertia, light touch |

### 표 6. Hybrid selection 예제

| Task | Force 방향 | Motion 방향 |
|--|--|--|
| Wipe 표면 | `v_z` (수직 압력) | `v_x, v_y, ω_z` |
| Peg-in-hole | `f_z` (insertion force) | `ω_z` (rotation align) |
| Polishing | `v_z` (constant force) | `v_x, v_y` (pattern) |
| Free motion | none | all 6 |

### 표 7. MPC (Model Predictive Control)

```
매 step t_k:
  1. 측정 x(t_k)
  2. 풀기:
       min Σ ℓ(x_k, u_k) + ℓ_f(x_N)
       s.t. x_{k+1} = f(x_k, u_k)
            x_k ∈ X,  u_k ∈ U
            x_0 = x(t_k)
  3. u(t_k) 만 적용 (첫 step)
  4. warm-start 후 다음 step 반복
```

| 변종 | dynamics | solver | 주 응용 |
|--|--|--|--|
| LMPC | linear | QP (OSQP) | drone hover, linearized humanoid |
| NMPC | nonlinear | SQP/IPOPT/ALTRO | manipulator, quadruped |
| MPPI | 임의 | parallel rollout | contact-rich, GPU |

핵심: outer-loop MPC (10~100Hz) + inner-loop computed-torque (1kHz) hierarchical 구조 표준.

### 표 8. RL-based Control (MDP)

| 요소 | 정의 |
|--|--|
| State `s` | `(θ, θ̇)` + sensor (vision, force) |
| Action `a` | `τ` 또는 desired `θ` |
| Reward `r` | task + smooth + safety |
| Policy `π(a|s)` | NN, 학습됨 |
| Objective | `J = E[Σ γ^t r_t]` |

| 알고리즘 | 종류 | 주 응용 |
|--|--|--|
| PPO | on-policy | quadruped/humanoid locomotion |
| SAC | off-policy entropy | manipulation |
| TD3 | off-policy twin critic | continuous control |
| DreamerV3 | world model | sample-efficient |

### 표 9. MPC vs RL vs Computed-Torque

| 측면 | Computed-torque | MPC | RL |
|--|--|--|--|
| Horizon | 1 step | N step | trained over many |
| Model | 필요 | 필요 | sim 만 (또는 model-free) |
| Online cost | μs | ms (NMPC) ~ μs (LMPC) | μs (NN inference) |
| Constraint | hand-tuned | explicit | implicit (reward) |
| Sample | 0 | 0 | 1e8~1e9 sim steps |
| Interpretability | high | high | low (black box) |

### 표 10. Sim-to-Real 핵심 4 기법

```
1. Domain randomization — friction, mass, delay, noise 의 random 변동
2. System identification   — real sysid → simulator 보정
3. Adaptive policy         — 초기 N step 으로 latent 추정
4. Real fine-tuning        — sim policy → real 에서 PPO 보강
```

---

## Mind Map

```
11장 Robot Control
├─ 1. Error dynamics + stability
├─ 2. PID (joint-space)
│   └─ tuning (Ziegler-Nichols)
├─ 3. Computed-torque (model-based)
│   ├─ feed-forward M θ̈_d + c + g
│   ├─ feedback M (K_p e + K_d ė)
│   └─ → ë + K_d ė + K_p e = 0 (linear!)
├─ 4. Task-space control
│   ├─ V_e = log(T⁻¹ T_d)
│   ├─ F_d = K_p V_e + K_d V̇_e
│   ├─ τ = Jᵀ F_d
│   └─ Operational space (Λ, η, ρ)
├─ 5. Force control
│   ├─ τ = Jᵀ F_d + g
│   └─ instability (rigid wall)
├─ 6. Hybrid motion-force
│   ├─ Selection matrix S
│   └─ orthogonal subspaces
├─ 7. Impedance control
│   ├─ M_d ë + B_d ė + K_d e = F_ext
│   └─ Admittance variant
└─ 8. Stability (Lyapunov, adaptive)
```

---

## 자주 쓰는 식 / 의사코드

### Computed-torque control

```python
def computed_torque(theta, theta_d, theta_dot, theta_dot_d, theta_ddot_d,
                    Kp, Kd, robot):
    e   = theta_d - theta
    de  = theta_dot_d - theta_dot
    M   = mass_matrix(theta, robot)
    cg  = coriolis_gravity(theta, theta_dot, robot)
    tau = M @ (theta_ddot_d + Kp @ e + Kd @ de) + cg
    return tau
```

### Task-space PID

```python
def task_pid(theta, theta_dot, T_d, V_d_dot, robot, Kp, Kd):
    T   = forward_kinematics(theta, robot)
    Jb  = body_jacobian(theta, robot)
    V_e = matrix_log_se3(inv(T) @ T_d)   # body twist error
    V   = Jb @ theta_dot                  # current body twist
    V_e_dot = V_d - V                     # body twist derivative
    F_d = Kp @ V_e + Kd @ V_e_dot
    tau = Jb.T @ F_d + coriolis_gravity(theta, theta_dot, robot)
    return tau
```

### Force control + gravity comp

```python
def force_control(theta, F_d, robot):
    J = jacobian(theta, robot)
    g = gravity(theta, robot)
    tau = J.T @ F_d + g
    return tau
```

### Impedance control

```python
def impedance_control(theta, theta_dot, T_d, V_d, F_ext, robot,
                      Md, Bd, Kd):
    T   = forward_kinematics(theta, robot)
    V   = body_jacobian(theta, robot) @ theta_dot
    e   = matrix_log_se3(inv(T) @ T_d)    # pose error in body frame
    de  = V_d - V
    # Desired EE acceleration to achieve impedance behavior
    a_d = inv(Md) @ (F_ext - Bd @ de - Kd @ e)
    # Map to joint torque via task-space inertia (operational space)
    Lambda = task_inertia(theta, robot)
    F_d = Lambda @ a_d + task_coriolis_gravity(theta, theta_dot, robot)
    tau = jacobian(theta, robot).T @ F_d
    return tau
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | error dynamics `e = θ_d − θ`, asymptotic vs exponential |
| 2 | PID 3 항 + tuning 직관 |
| 3 | Computed-torque → linear error ODE `ë + K_d ė + K_p e = 0` |
| 4 | Task-space PID with body Jacobian + body twist error |
| 5 | Force control = `Jᵀ F_d + g`, rigid wall instability |
| 6 | Hybrid = motion ⊕ force, orthogonal selection S |
| 7 | Impedance = `M_d ë + B_d ė + K_d e = F_ext` |
| 8 | Lyapunov V = ½eᵀK_p e + ½ ėᵀ M ė, V̇ ≤ 0 |
