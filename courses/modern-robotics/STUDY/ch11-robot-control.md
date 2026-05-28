# Chapter 11: Robot Control — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 11: Robot Control** (책 p.403~460) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 11장의 핵심: 9~10장의 *desired trajectory* `θ_d(t)` 를 *실제로* 따라가는 controller. **Joint-space**, **Task-space**, **Force**, **Hybrid**, **Impedance** 5 종.

## 들어가기 전에

- **선수 지식**
  - **3~5장**: SE(3), Jacobian
  - **8장**: manipulator equation
  - **9장**: trajectory `θ_d(t), θ̇_d(t), θ̈_d(t)`
  - control 이론: PID, root locus, Lyapunov stability
- **학습 목표**
  1. **Error dynamics** — desired ↔ actual 의 미분 방정식
  2. **PID control** + tuning (`K_p, K_d, K_i`)
  3. **Computed-torque control** — model-based feed-forward
  4. **Task-space control** — Jacobian 변환을 통한 EE pose 추적
  5. **Force control** — 외부 force 와 부드러운 contact
  6. **Hybrid motion-force control** — 방향 분리 (selection matrix)
  7. **Impedance control** — robot 의 *가상 spring-damper* 거동
- **예상 학습 시간**: 120~150분

---

## 1. Error Dynamics

### 1.1 Tracking error

$$e(t) = \theta_d(t) - \theta(t), \quad \dot{e}(t) = \dot\theta_d(t) - \dot\theta(t)$$

목표: `e(t) → 0` as `t → ∞` (asymptotic tracking).

### 1.2 Stability 종류

- **Stable**: `‖e(0)‖ < δ` → `‖e(t)‖ < ε` for all `t`
- **Asymptotically stable**: stable + `e(t) → 0`
- **Exponentially stable**: `‖e(t)‖ ≤ M e^{−λt} ‖e(0)‖`

Robot control 의 목표는 보통 *exponential stability*.

![Figure 11.1 — Robot control 의 일반 architecture. 교재 p.405](/courses/modern-robotics/figures/ch11/fig-11-1.png)

---

## 2. PID Control

### 2.1 식 (joint-space, 단일 joint)

$$\tau = K_p e + K_i \int e \, dt + K_d \dot{e}$$

- `K_p`: proportional gain — error 크면 큰 토크
- `K_d`: derivative gain — error 의 변화 억제 (damping)
- `K_i`: integral gain — steady-state error 제거

### 2.2 Tuning rules of thumb

- 우선 `K_d = 0, K_i = 0` 으로 `K_p` 증가 → oscillation 시작 직전까지
- `K_d` 추가 → damping (overshoot 줄이고 빠른 settling)
- `K_i` 마지막 — steady-state error 만 보정

Ziegler-Nichols, pole-placement 등 정량 tuning 도 있음.

### 2.3 PID 의 한계

- 비선형 (gravity, Coriolis) *무시* → tracking error
- gain *configuration-dependent* — `K_p` 가 한 자세에서 적절해도 다른 자세에서 부족
- `M(θ)` 변화에 *blind* — high inertia 자세에서 underpowered

→ **computed-torque control** 이 해결.

---

## 3. Computed-Torque Control (Model-based)

### 3.1 식

$$\tau = \underbrace{M(\theta) \ddot\theta_d}_{\text{feed-forward}} + c(\theta, \dot\theta) + g(\theta) + \underbrace{M(\theta) (K_p e + K_d \dot{e})}_{\text{feedback}}$$

또는 더 정리하면:

$$\tau = M(\theta) (\ddot\theta_d + K_p e + K_d \dot{e}) + c(\theta, \dot\theta) + g(\theta)$$

### 3.2 Error dynamics — Linear

`τ = M(θ) θ̈ + c + g` (8장 manipulator) 와 위 식을 비교:

$$M(\theta) \ddot{e} + M(\theta) (K_d \dot{e} + K_p e) = 0$$

`M(θ)` invertible 이므로:

$$\ddot{e} + K_d \dot{e} + K_p e = 0$$

→ **각 joint 가 독립 linear ODE**. `K_p, K_d` 선택으로 stable, damping ratio, settling time 자유롭게 결정.

### 3.3 장점

- *exact linearization* (model perfect 시)
- 모든 configuration 에서 *동일한* error 거동
- gain tuning 이 *물리적으로 의미* (critical damping 등)

### 3.4 한계

- *model error* (mass, friction, joint flex) → linearization 깨짐
- Newton-Euler `O(n)` 매 step → CPU 부담 (해결됨, MoveIt 등 표준)

![Figure 11.5 — Computed-torque control block diagram. 교재 p.412](/courses/modern-robotics/figures/ch11/fig-11-5.png)

---

## 4. Task-Space Control

### 4.1 동기

EE 의 *task pose* `X` 직접 제어. joint 가 아니라 task space (보통 SE(3)) error.

### 4.2 식

EE error `X_e = X_d⁻¹ X` (body frame), error twist `V_e = log(X_e)`.

PID in task space:

$$\mathcal{F}_d = K_p \mathcal{V}_e + K_d \dot{\mathcal{V}}_e + K_i \int \mathcal{V}_e \, dt$$

이 wrench 를 joint torque 로:

$$\tau = J^T(\theta) \mathcal{F}_d + c + g$$

### 4.3 Operational space control (Khatib)

Task-space inertia 까지 활용:

$$\mathcal{F}_d = \Lambda(\theta) (\ddot{X}_d + K_p \mathcal{V}_e + K_d \dot{\mathcal{V}}_e) + \eta(\theta, \dot\theta) + \rho(\theta)$$

`Λ = (J M⁻¹ Jᵀ)⁻¹` (8장 task-space inertia). 결과 task-space error 가 *exponential stable*.

> **함정 1**: Task-space control 은 *Jacobian* 통과. singular configuration 근처에서 `J` rank-deficient → unstable. damped least-squares 권장.

---

## 5. Force Control

### 5.1 동기

contact-rich task (assembly, polishing, surgery) — *직접 force 제어*.

### 5.2 식

목표 EE wrench `F_d`. 단순:

$$\tau = J^T(\theta) \mathcal{F}_d + g(\theta) + \text{(damping)}$$

gravity 보상 필수. damping 추가로 *passive* 안정.

### 5.3 Force feedback

force sensor (EE 의 6-axis F/T sensor) 측정 `F_meas` 와 오차 제어:

$$\mathcal{F}_{cmd} = \mathcal{F}_d + K_{fp} (\mathcal{F}_d - \mathcal{F}_{meas})$$

steady-state 에서 measurement = desired.

### 5.4 한계

- 환경 stiffness 모름 → instability 위험 (contact 시 큰 force 발생)
- sensor noise 가 직접 torque 로 전달

→ **impedance control** 이 우회.

---

## 6. Hybrid Motion-Force Control

### 6.1 동기

contact task 의 일부 방향은 *motion control* (constrained), 다른 방향은 *force control*.

예: 책상 표면 닦기:
- 책상 면 *수직* 방향: force control (일정 압력)
- 책상 면 *수평* 방향: motion control (직선 추적)

### 6.2 Selection matrix

$$\tau = J^T \left[ S \mathcal{F}_d + (I - S) \Lambda(\theta) \dot{V}_d + \ldots \right]$$

`S = diag(0, 0, 1, 0, 0, 0)` 같은 *diagonal selection matrix*. 1 = force control, 0 = motion control.

> **함정 2**: Motion 과 force 방향이 *orthogonal* (mutually exclusive) 해야 함. 같은 방향에 둘 다 시도하면 *constraint inconsistency*.

---

## 7. Impedance Control

### 7.1 직관

robot 을 *spring-damper-mass 시스템* 처럼 거동. 외력 `F_ext` 가 들어오면 *부드럽게* 응답.

$$M_d \ddot{e} + B_d \dot{e} + K_d e = \mathcal{F}_{ext}$$

- `M_d`: desired inertia (보통 작게)
- `B_d`: desired damping
- `K_d`: desired stiffness

### 7.2 적용

- Human-robot interaction (협동 로봇)
- compliance — 의도치 않은 contact 시 robot 이 *부드럽게* 양보
- surgical, prosthetics

![Figure 11.13 — Impedance control 의 spring-damper 모델. 교재 p.443](/courses/modern-robotics/figures/ch11/fig-11-13.png)

### 7.3 Admittance control (variant)

inertia 가 *낮은* robot — force 측정 → motion 결정 (위와 인과 반대):

$$\dot{X} = Y(s) \mathcal{F}_{ext}$$

`Y(s)` = admittance (inverse impedance).

---

## 8. Stability 분석 (간단)

### 8.1 Lyapunov function

`V(e, ė) = ½ eᵀ K_p e + ½ ėᵀ M(θ) ė` (energy-like).

`V̇` 가 negative semi-definite → stable. 적절한 controller 로 negative definite → asymptotic stable.

### 8.2 Robust / Adaptive control

- *Robust*: `‖model error‖ ≤ bound` 가정, controller 가 *최악 case* 에 대비
- *Adaptive*: parameter (mass, friction) 를 online 학습

상세는 11.5~11.7 (책).

---

## 9. Model Predictive Control (MPC)

> **동기** — §1~§7 의 controller 는 *모두 즉시 응답* (one-step feedback). 미래의 *제약·constraint* 를 사전에 고려하지 못함. MPC 는 *finite horizon* 의 trajectory 를 매 step 다시 풀어 *constraint-aware* 제어를 한다.

### 9.1 Receding horizon 의 개념

매 control step `t_k` 에서:

1. 현재 상태 `x(t_k)` 측정
2. 미래 $[t_k, t_k + N \Delta t]$ 의 *최적* control trajectory $u(t_k), \ldots, u(t_k + (N-1)\Delta t)$ 계산 (cost 최소화 + constraint 만족)
3. **첫 step `u(t_k)` 만 실제 robot 에 적용**
4. 다음 step `t_{k+1}` 에서 (1) 부터 반복 (*sliding window*)

이게 *receding horizon* — 매 번 새 horizon 으로 최적화.

### 9.2 수식 형태

매 step 의 최적화 문제:

$$\begin{aligned}
\min_{u_0, \ldots, u_{N-1}} \quad & \sum_{k=0}^{N-1} \ell(x_k, u_k) + \ell_f(x_N) \\
\text{s.t.} \quad & x_{k+1} = f(x_k, u_k) \quad \text{(dynamics)} \\
& x_k \in \mathcal{X}, \ u_k \in \mathcal{U} \quad \text{(state / input constraints)} \\
& x_0 = x(t_k) \quad \text{(initial condition)}
\end{aligned}$$

- $\ell$ — *stage cost* (예: tracking + control effort): $\|x_k - x_d\|^2_Q + \|u_k\|^2_R$
- $\ell_f$ — *terminal cost*: $\|x_N - x_d\|^2_{Q_f}$
- $\mathcal{X}, \mathcal{U}$ — 안전 box, torque limit, joint limit, obstacle avoidance halfspace 등
- $f$ — robot dynamics (8장 manipulator equation)

### 9.3 Linear vs Nonlinear MPC

| 종류 | dynamics | cost | solver | 응용 |
|--|--|--|--|--|
| **Linear MPC (LMPC)** | `x_{k+1} = A x_k + B u_k` | quadratic | **QP** (OSQP, qpOASES) | linearized humanoid, quad-rotor hover |
| **Nonlinear MPC (NMPC)** | `x_{k+1} = f(x_k, u_k)` (`f` 비선형) | quadratic/일반 | SQP, IPOPT, ALTRO | manipulator full dynamics, locomotion |
| **MPPI** (sampling) | `f` 임의 | 임의 (rollout 평가) | parallel rollout + softmax | contact-rich, GPU 친화 |

### 9.4 manipulator MPC — 예제 cost 형태

7-DoF arm 의 *tracking + collision avoidance* MPC:

$$\ell(x_k, u_k) = \underbrace{\|p(x_k) - p_d(t_k)\|^2_{Q_p}}_{\text{EE 위치}} + \underbrace{\|R(x_k) - R_d(t_k)\|^2_{Q_R}}_{\text{EE 자세}} + \underbrace{\|u_k\|^2_R}_{\text{torque 절약}} + \underbrace{\sigma(d_{obs}(x_k))}_{\text{barrier}}$$

여기서 `x_k = (θ_k, θ̇_k)`, `u_k = τ_k`. `d_{obs}` 는 가장 가까운 obstacle 의 signed distance, `σ` 는 *log barrier* (`-log d` 형태).

constraint:
- joint limit: $\theta_{\min} \leq \theta_k \leq \theta_{\max}$
- torque limit: $|\tau_k| \leq \tau_{\max}$
- velocity limit: $|\dot\theta_k| \leq \dot\theta_{\max}$

### 9.5 MPC vs computed-torque

| 측면 | Computed-torque (§3) | MPC |
|--|--|--|
| Horizon | 1 step | N step (수십~수백) |
| Constraint | 직접 처리 X (saturation 후 hand-tuned) | optimization 안에서 명시적 |
| Real-time | ✓ (단순 식) | borderline (NMPC ~ ms, LMPC ~ μs) |
| Trajectory | 외부에서 주어짐 | 내부에서 동시 생성 가능 |
| Model error | tracking error 직접 | predictive cost 통해 부드럽게 흡수 |

### 9.6 실용 — 산업 채용

- **ANYmal, Spirit, Spot quadruped locomotion**: convex MPC for body trajectory + Whole-Body QP (WB-QP) for joint torque. 100~400 Hz.
- **Boston Dynamics Atlas humanoid**: model-predictive control for ZMP trajectory.
- **MuJoCo MPC (Howell et al. 2022)**: differentiable simulator + iLQR / Cross-Entropy / PI² — 노트북 1 대로 manipulation·locomotion.
- **OCS2** (ETH): C++ NMPC framework. quadruped, mobile manipulator 표준.

### 9.7 한계

1. **연산 비용** — n=7 arm, N=20 horizon, 1kHz 가 borderline. GPU 또는 model simplification.
2. **Terminal cost design** — finite horizon 의 *과거 효과* 무시 → terminal cost 가 *infinite horizon value function* 근사 필요. 이론적·실용적으로 어려움.
3. **Local minima** — nonconvex problem 에서 초기값 의존성.
4. **Robustness** — model mismatch 가 누적되면 horizon 끝에서 prediction 발산.

> **함정 MPC**: NMPC 가 *수렴 안 함* 또는 *previous solution 부근에 갇힘* — 이를 *warm-starting* 으로 거의 해결. 첫 firing 부터 *steady-state solution + 작은 perturbation* 으로 init 필수.

---

## 10. Reinforcement Learning-based Control

> **동기** — §3 (computed-torque) 가 좋은 모델을 요구, §9 (MPC) 가 매 step 비싼 optimization. **RL 은 *데이터* 로 policy $\pi(u|x)$ 를 학습** → online 비용은 forward pass 만. model-free + complex dynamics 친화.

### 10.1 MDP formulation

Robot control 을 *Markov Decision Process* 로:

| 요소 | 정의 |
|--|--|
| State `s_t` | `(θ_t, θ̇_t)` + sensor (vision, force) |
| Action `a_t` | `τ_t` 또는 desired `θ_t` (low-level controller 가 wrap) |
| Reward `r_t` | task 보상 + control penalty + safety |
| Transition `P` | robot dynamics (8장) |
| Policy `π(a\|s)` | learned (neural network, $\sim 10^6$ parameters) |

목표 — *expected discounted return* 최대화:

$$J(\pi) = \mathbb{E}_{\tau \sim \pi}\left[ \sum_{t=0}^{T} \gamma^t r_t \right]$$

### 10.2 주요 알고리즘

| 알고리즘 | 종류 | 특징 |
|--|--|--|
| **PPO** (Schulman 2017) | on-policy | 안정·tuning 쉬움, 대부분의 quadruped/humanoid 표준 |
| **SAC** (Haarnoja 2018) | off-policy + entropy | sample efficient, manipulation 흔히 |
| **TD3** (Fujimoto 2018) | off-policy + twin critic | DDPG 의 안정화 |
| **DreamerV3** (Hafner 2023) | world model | latent dynamics 학습 + planning |
| **PPO + Asymmetric actor-critic** | privileged info | sim 학습 시 ground truth, deploy 시 sensor only |

### 10.3 학습 파이프라인

```
1. Simulator 구축 (MuJoCo / Isaac Sim / Brax)
2. Domain randomization — friction, mass, sensor noise 등 변동
3. Curriculum — 쉬운 task → 점진적 어려움
4. Reward shaping — task + smooth + safety penalty
5. Policy training (수억 시뮬 step, GPU 1~16 시간~수일)
6. Sim-to-real deployment — fine-tuning or direct
7. Safety monitor — torque limit, joint limit, fallback controller
```

### 10.4 Sim-to-Real Gap

학습은 *sim* 에서, deploy 는 *real* 에서. 두 환경의 차이가 *Sim-to-Real Gap*. 대처:

- **Domain randomization**: 시뮬 parameter (friction, motor delay, sensor noise) 을 random 변동 → policy 가 *불변* 학습.
- **System identification**: 실제 robot 의 friction·delay·gear backlash 를 측정 → simulator 보정.
- **Adaptive policy**: 처음 N step 에서 환경 *latent* 추정 → policy 가 그것 입력.
- **Real-world fine-tuning**: PPO continues with safer hyperparameters in real.

### 10.5 산업 채용 사례

- **ANYmal / Spot / Solo quadruped** (ETH Hutter, Boston Dynamics): blind locomotion + perceptive locomotion 모두 PPO + privileged learning. *전 지형 robust*.
- **OpenAI Dactyl** (2018): single-handed Rubik's cube. PPO + domain randomization. *완전 model-free*.
- **DeepMind RoboCat / Gato**: foundation model — 수백 manipulation task 학습 후 few-shot adaptation.
- **Tesla Optimus / Figure 02 humanoid**: end-to-end RL + IL (imitation learning) hybrid.

### 10.6 RL vs Classical control

| 측면 | Classical (PID, computed-torque, MPC) | RL |
|--|--|--|
| Model | 필요 (정확할수록 ↑) | 불필요 (또는 simulator 만) |
| Sample | 수십~수백 trajectory | 수억 step |
| Interpretability | 높음 | *블랙박스* |
| Generalization | 새 task → 재설계 | fine-tuning |
| Real-time | μs~ms | μs (inference) |
| Safety | 분석 가능 | 학습 시 보장 어려움 |

### 10.7 한계

1. **Sample efficiency** — 수억 sim step 필요. real robot 학습은 거의 불가능 (시간·마모).
2. **Reward design** — reward sparse 면 학습 안 됨. shaping 이 *art*.
3. **Safety during exploration** — random action 이 robot 망가뜨림. sim 우선.
4. **Distribution shift** — 학습 분포 벗어나면 unpredictable.
5. **Interpretability** — 왜 그렇게 행동하는지 *증명 안 됨*. 의료·항공 등 certification 어려움.

### 10.8 Hybrid — Classical + RL

실용 트렌드:

- **RL high-level + classical low-level**: PPO 가 footstep / waypoint 선택, MPC 가 추적.
- **Residual RL**: classical controller `u_c` + 학습된 residual `u_r` → `u = u_c + u_r`. 안정성 + 적응성 모두.
- **Diffusion Policy** (Chi 2023): RL 대신 diffusion model 로 demonstration 학습.
- **Learning-to-control** (Lyapunov NN, Control Barrier Functions w/ NN): stability *증명* 가능한 NN controller.

> **함정 RL**: 학습 잘 된 policy 가 *현장 deploy* 후 *느린 drift* → robot 의 friction·wear 가 누적되며 simulator 와 격차 ↑. 정기 re-train 또는 online adaptation 필수.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | PID 만으로 충분 | 비선형·configuration-dependent dynamics 무시. computed-torque + PID 권장. |
| 2 | Computed-torque 가 *모델 perfect* 가정 | 실제는 model error → robust / adaptive 필요. |
| 3 | Task-space control 이 singular 에서 정상 | Jacobian singular → instability. damped LS. |
| 4 | Force control 의 force = sensor 측정 그대로 | noise 큼. filter 필요 (Kalman 등). |
| 5 | Hybrid control 의 selection matrix 가 *configuration-independent* | constraint 의 *방향* 이 task frame 에서 정의 — task frame 이 configuration 따라 변하면 selection 도 변환 필요. |
| 6 | Impedance control 의 `M_d` 가 *robot mass* 와 무관 | 무관 — *원하는* virtual mass 직접 명시 가능 (단 작을수록 robust 어려움). |
| 7 | Gravity compensation 만으로 stable | 마찰·external force 없을 때만. 일반적으로 PD 필요. |
| 8 | `K_p` 가 클수록 좋음 | 너무 크면 instability (high-frequency oscillation). bandwidth 와 actuator 한계 고려. |
| 9 | Force / motion 같은 방향 동시 제어 | constraint inconsistency. orthogonal subspaces 분리 필요. |
| 10 | 11장 controller 가 *반드시* trajectory 가 필요 | regulation (단순 setpoint) 만 해도 됨. trajectory 는 일반 case. |

---

## 자가점검

1. Tracking error 의 정의.
2. PID 의 3 항 + 각각의 역할.
3. Computed-torque control 의 식.
4. Computed-torque 의 *error dynamics* (perfect model 가정).
5. Task-space control 의 task wrench → joint torque 변환.
6. Operational space control 의 `Λ` 의 정의.
7. Force control 의 단순 식.
8. Hybrid control 의 selection matrix.
9. Impedance control 의 spring-damper-mass equation.
10. Asymptotic vs Exponential stability.

### 해답 (간략)

1. `e(t) = θ_d(t) - θ(t)`.
2. P (proportional, error), I (integral, steady-state), D (derivative, damping).
3. `τ = M(θ)(θ̈_d + K_p e + K_d ė) + c + g`.
4. `ë + K_d ė + K_p e = 0` (각 joint 독립 linear ODE).
5. `τ = Jᵀ(θ) F_d + ...` (frame 일치 필수).
6. `Λ(θ) = (J M⁻¹ Jᵀ)⁻¹` — task-space inertia.
7. `τ = Jᵀ F_d + g + damping`.
8. `S = diag(s_i)`, `s_i = 1` (force) or `0` (motion). 6×6.
9. `M_d ë + B_d ė + K_d e = F_ext`.
10. Asymptotic: `e → 0`. Exponential: `‖e(t)‖ ≤ M e^{−λt} ‖e(0)‖` (exponential rate).

---

## 다음 학습으로

- **12장 (Grasping)** — contact 분석과 *force closure*. 본 장의 hybrid / impedance control 응용.
- **13장 (Mobile Robots)** — nonholonomic constraint 의 controller.
- **MPC** — finite horizon trajectory optimization + control.
- **RL-based control** — neural network policy. Sim2Real 핵심.

---

## §X Modern Control Frameworks

### ROS Control

**ros_control** stack:
- Hardware abstraction
- Controllers (joint position, velocity, effort)
- Real-time loop (rt_preempt or Xenomai)
- ros2_control (ROS 2 latest)

### MPC frameworks

| | 언어 | 특징 |
|--|--|--|
| acados | C/Python | Real-time NMPC, autonomous driving |
| CasADi | C++/Python | Optimization + auto-diff |
| OCS2 | C++ | optimal control |
| MPC.pytorch | Python | differentiable MPC |
| Crocoddyl | C++/Python | rigid body MPC |

### RL frameworks

**Sim**:
- Isaac Gym (NVIDIA) — massive parallel
- Brax (Google) — JAX-based, differentiable
- MuJoCo MJX — JAX bindings

**Algorithm**: PPO, SAC, TD3, DDPG, Diffusion Policy (2023~).

**Sim-to-real**: domain randomization, privileged learning (teacher-student), real-world fine-tuning.

### Industry deployment

**Whole-body control**:
- Boston Dynamics Atlas — task-prioritized QP
- ANYmal — model-based whole-body
- Optimus — RL-based

**Cooperative**:
- Dual-arm manipulation
- Swarm robotics
- Human-robot collaboration (cobot)

### Safety-critical

- Force limit (cobot, ISO 10218)
- Speed monitoring
- Emergency stop (E-stop)
- Safety-rated PLC
