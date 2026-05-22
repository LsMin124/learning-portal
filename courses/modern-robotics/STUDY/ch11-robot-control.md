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
- **MPC** — finite horizon 의 *trajectory optimization* + control 통합. 본 장의 computed-torque 를 매 step 재계획.
- **RL-based control** — neural network policy 가 PID / model-based 대체. Sim2Real 의 핵심.
