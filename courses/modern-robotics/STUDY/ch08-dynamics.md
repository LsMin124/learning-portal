# Chapter 8: Dynamics of Open Chains — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 8: Dynamics of Open Chains** (책 p.271~325) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 8장은 *kinematics → dynamics* 의 도약. *force·torque 가 어떻게 motion 을 만드는가*. 두 formulation 이 등장 — **Lagrangian** (energy-based, 분석적) 과 **Newton-Euler** (force-based, recursive·efficient).

## 들어가기 전에

- **선수 지식**
  - **3장**: SE(3), twist `V`, wrench `F`, `[Ad_T]`, `[ad_V]`
  - **4장**: PoE FK, screw axes
  - **5장**: Jacobian `J(θ)` (Lagrangian 유도의 핵심), `τ = Jᵀ F`
  - 고전역학: Newton 의 법칙, kinetic / potential energy
  - 선형대수: positive-definite matrix, 행렬 미분
- **학습 목표**
  1. **Manipulator equation**: `τ = M(θ) θ̈ + c(θ, θ̇) + g(θ)`
  2. **Lagrangian formulation** — `L = T − V`, Euler-Lagrange equations
  3. **Mass matrix `M(θ)`** — symmetric positive-definite, joint 공간의 inertia
  4. **Coriolis/centrifugal `c(θ, θ̇)`** — `θ̇` 의 이차항
  5. **Gravity `g(θ)`** — potential energy 의 gradient
  6. **Spatial inertia matrix** `G_b ∈ R^{6×6}` — 강체의 모든 inertia 통합
  7. **Newton-Euler recursive algorithm** — `O(n)` 효율, forward + backward pass
  8. **Forward dynamics** (`τ → θ̈`) vs **Inverse dynamics** (`θ̈ → τ`)
  9. **Task-space dynamics** + Jacobian transpose 의 wrench mapping
- **예상 학습 시간**: 180~240분 (8장은 책에서 가장 무거운 장)

---

## 1. Manipulator Equation — 전체 그림

### 1.1 식

$$\boxed{\tau = M(\theta) \ddot\theta + c(\theta, \dot\theta) + g(\theta)}$$

또는 외부 wrench `F_tip` 이 EE 에 작용할 때:

$$\tau = M(\theta) \ddot\theta + c(\theta, \dot\theta) + g(\theta) + J^T(\theta) \mathcal{F}_{tip}$$

### 1.2 각 항의 의미

| 항 | 차원 | 의미 |
|--|--|--|
| `τ` | `R^n` | joint torque (input) |
| `M(θ)` | `R^{n×n}` | mass matrix, SPD |
| `θ̈` | `R^n` | joint acceleration |
| `c(θ, θ̇)` | `R^n` | Coriolis + centrifugal (θ̇ 의 quadratic) |
| `g(θ)` | `R^n` | gravity torque |
| `J(θ)` | `R^{6×n}` | 5장 Jacobian |
| `F_tip` | `R^6` | EE 외부 wrench |

### 1.3 두 방향

- **Inverse dynamics**: `(θ, θ̇, θ̈)` → `τ`. control 의 feed-forward.
- **Forward dynamics**: `(θ, θ̇, τ)` → `θ̈`. simulation·predictive control.

---

## 2. 2R Arm 예제 — Lagrangian 직관

![Figure 8.1 — 2R open chain under gravity. 교재 p.273](/courses/modern-robotics/figures/ch08/fig-8-1.png)

가장 단순한 두-link arm 으로 *manipulator equation 의 모든 항* 이 어떻게 나오는지.

### 2.1 Configuration·Energy

Link 길이 `L₁, L₂`, mass `m₁, m₂` (link 끝에 point mass 가정).

**Kinetic energy** `T` (= ½ vᵀ m v, 두 mass 모두 합):
$$T(\theta, \dot\theta) = \frac{1}{2} \dot\theta^T M(\theta) \dot\theta$$

**Potential energy** `V` (gravity `g`, height z 방향):
$$V(\theta) = m_1 g L_1 \sin\theta_1 + m_2 g (L_1 \sin\theta_1 + L_2 \sin(\theta_1 + \theta_2))$$

### 2.2 Mass matrix 도출

2R 의 mass matrix 직접 계산 결과 (책 §8.1):

$$M(\theta) = \begin{bmatrix} m_1 L_1^2 + m_2 (L_1^2 + 2 L_1 L_2 \cos\theta_2 + L_2^2) & m_2 (L_1 L_2 \cos\theta_2 + L_2^2) \\ m_2 (L_1 L_2 \cos\theta_2 + L_2^2) & m_2 L_2^2 \end{bmatrix}$$

관찰:
- `M(θ)` 가 *configuration-dependent* (θ_2 함수). 일정 행렬 아님.
- `M(θ)` 가 *symmetric* — 일반 mass matrix 의 항상 그렇다.
- `M(θ)` 가 *positive-definite* — kinetic energy 가 양수.

---

## 3. Lagrangian Formulation

### 3.1 Lagrangian

$$L(\theta, \dot\theta) = T(\theta, \dot\theta) - V(\theta)$$

### 3.2 Euler-Lagrange equations

$$\boxed{\tau_i = \frac{d}{dt} \frac{\partial L}{\partial \dot\theta_i} - \frac{\partial L}{\partial \theta_i}, \quad i = 1, \ldots, n}$$

`τ_i` 는 *generalized force* on joint i. revolute → torque, prismatic → force.

### 3.3 명시적 form

`T = ½ θ̇ᵀ M(θ) θ̇` 를 대입하여 정리하면:

$$\tau_i = \sum_j m_{ij}(\theta) \ddot\theta_j + \sum_{j,k} \Gamma_{ijk}(\theta) \dot\theta_j \dot\theta_k + \frac{\partial V}{\partial \theta_i}$$

**Christoffel symbols** (1st kind):

$$\Gamma_{ijk}(\theta) = \frac{1}{2} \left( \frac{\partial m_{ij}}{\partial \theta_k} + \frac{\partial m_{ik}}{\partial \theta_j} - \frac{\partial m_{jk}}{\partial \theta_i} \right)$$

### 3.4 Coriolis 와 Gravity 분리

매트릭스 form:

$$\tau = M(\theta) \ddot\theta + \underbrace{C(\theta, \dot\theta) \dot\theta}_{c(\theta, \dot\theta)} + g(\theta)$$

`C(θ, θ̇) θ̇` 가 *velocity 의 이차항* (Coriolis + centrifugal). `g(θ) = ∂V/∂θ`.

> **함정 1**: `C(θ, θ̇)` 의 정의는 *유일하지 않음*. Christoffel-symbol 기반 `C` 는 `Ṁ − 2C` 가 skew-symmetric 인 특수 형태. 이게 passivity property 의 핵심 (11장 control).

---

## 4. 단일 강체의 Dynamics

### 4.1 Spatial inertia matrix

강체 1 개의 *통합 inertia* 표기:

$$\mathcal{G}_b = \begin{bmatrix} \mathcal{I}_b & 0 \\ 0 & m I \end{bmatrix} \in \mathbb{R}^{6 \times 6}$$

- `I_b ∈ R^{3×3}`: rotational inertia tensor about center of mass, body frame
- `m`: 총 질량

### 4.2 Twist-Wrench 형태의 단일 강체 dynamics

![Figure 8.5 — 강체의 spatial dynamics. 교재 p.291](/courses/modern-robotics/figures/ch08/fig-8-5.png)

body frame 에서 표현:

$$\mathcal{F}_b = \mathcal{G}_b \dot{\mathcal{V}}_b - [ad_{\mathcal{V}_b}]^T \mathcal{G}_b \mathcal{V}_b$$

이게 *Newton-Euler equation* 의 6D 형태. `[ad_V] = [[ω], 0; [v], [ω]]` 는 twist 의 *bracket*.

### 4.3 Kinetic energy

$$K = \frac{1}{2} \mathcal{V}_b^T \mathcal{G}_b \mathcal{V}_b$$

---

## 5. Newton-Euler Recursive Algorithm

### 5.1 동기 — Lagrangian 의 한계

Lagrangian 접근:
- 분석적, 명시적 식
- 그러나 `n` joint 에서 `O(n²)` ~ `O(n³)` (symbolic 폭증)
- Real-time control 어려움

Newton-Euler 접근:
- *recursive*, `O(n)` 효율
- *forward pass* (kinematics propagation) + *backward pass* (forces propagation)
- *Featherstone* 의 algorithm 표준화

![Figure 8.6 — link i 의 free-body diagram. 교재 p.293](/courses/modern-robotics/figures/ch08/fig-8-6.png)

### 5.2 Forward Pass — Kinematics propagation

base 부터 EE 방향으로:

```
V_0 = 0 (base 정지)
V̇_0 = (0, 0, 0, 0, 0, g)  # gravity 를 base 가속도로 표현 (수렴 트릭)

for i = 1 to n:
    T_{i,i-1} = M_{i,i-1} · e^{-[A_i]θ_i}    # link 사이 변환
    V_i = A_i · θ̇_i + [Ad_{T_{i,i-1}}] V_{i-1}
    V̇_i = A_i · θ̈_i + [Ad_{T_{i,i-1}}] V̇_{i-1} + [ad_{V_i}](A_i θ̇_i)
```

- `A_i`: joint i 의 screw axis, link i frame `{i}` 에서 표현
- `M_{i,i-1}`: zero-position 의 `T_{i,i-1}`
- gravity 를 base 의 가짜 가속도로 → 별도 gravity 항 불필요

### 5.3 Backward Pass — Force propagation

EE 부터 base 방향으로:

```
F_{n+1} = F_tip  # EE 외부 wrench (없으면 0)

for i = n downto 1:
    F_i = [Ad_{T_{i+1,i}}]^T · F_{i+1} + G_i · V̇_i − [ad_{V_i}]^T (G_i · V_i)
    τ_i = F_i^T · A_i        # screw axis 방향 projection
```

### 5.4 결과

전체 알고리즘: **O(n)** — 1000Hz real-time control 가능.

---

## 6. Mass Matrix 효율 계산

`M(θ)` 를 Lagrangian 으로 풀면 symbolic 폭증. **Newton-Euler 활용**:

각 joint 에 *단위 가속도* `θ̈ = e_i` (i 번째만 1, 나머지 0), `θ̇ = 0`, `g = 0` 으로 inverse dynamics 호출 → 결과 `τ` 가 `M` 의 i 번째 컬럼.

```
for i = 1 to n:
    M[:,i] = inverse_dynamics(θ, θ̇=0, θ̈=e_i, g=0)
```

`n` 번 호출, 각 `O(n)` → `O(n²)` 으로 `M` 전체 얻음. 직접 symbolic 보다 *훨씬* 빠르다.

---

## 7. Forward Dynamics

`(θ, θ̇, τ) → θ̈` 풀기:

$$\ddot\theta = M^{-1}(\theta) (\tau - c(\theta, \dot\theta) - g(\theta) - J^T(\theta) \mathcal{F}_{tip})$$

알고리즘:
1. Newton-Euler 로 `c + g` 계산 (`inverse_dynamics(θ, θ̇, θ̈=0, g=g)`)
2. Newton-Euler 로 `M` 계산 (앞 절)
3. `M⁻¹ (τ − c − g − Jᵀ F_tip)` 로 `θ̈` 얻음
4. RK4 등으로 시간적분 → `θ(t), θ̇(t)`

이것이 robot **simulator** (MuJoCo, PyBullet, Drake) 의 핵심.

> **함정 2**: `M⁻¹` 직접 계산은 `O(n³)`. 효율적 방법: *Articulated-Body Algorithm (ABA)* — Featherstone, `O(n)` 으로 forward dynamics 자체 해결. 7-DoF 이상 arm 에서 큰 차이.

---

## 8. Task-Space Dynamics

End-effector 의 task space 좌표 `x ∈ R⁶` 에 대한 dynamics:

$$\mathcal{F}_{tip} = \Lambda(\theta) \dot{\mathcal{V}} + \eta(\theta, \dot\theta) + \rho(\theta)$$

- `Λ(θ) = (J M⁻¹ Jᵀ)⁻¹` — *task-space inertia matrix*
- `η, ρ`: task space 의 Coriolis 와 gravity

응용: **operational space control** (11장) — 직접 task space 에서 PID·impedance.

---

## 9. Constrained Dynamics (간단)

Closed-chain 또는 contact 가 있는 경우:

$$\tau = M(\theta) \ddot\theta + c + g + A^T(\theta) \lambda$$
$$A(\theta) \dot\theta = 0 \quad \text{(constraint)}$$

`λ` 는 constraint force (Lagrange multiplier). *projection matrix* 로 풀이.

상세는 7장 (closed chain) 과 12장 (grasping).

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | `C(θ, θ̇)` 가 *유일하게 정의됨* | 정의 다수. Christoffel 기반이 표준 — passivity (`Ṁ − 2C` skew). |
| 2 | `M(θ)` 가 일정 행렬 | configuration-dependent. `θ_2` 변하면 변함. |
| 3 | Coriolis 와 centrifugal 이 다른 항 | 같은 `c(θ, θ̇)` 항 안. centrifugal = `c_{iii} θ̇_i²` (단일 joint), Coriolis = 다른 joint 곱. 합쳐서 `C(θ, θ̇)θ̇`. |
| 4 | Gravity 를 *별도* 처리 | Newton-Euler 에선 `V̇_0` 에 gravity 가속도 넣으면 자동. |
| 5 | Newton-Euler 가 *Lagrangian 보다 항상 빠름* | symbolic 단계 다르지만 실용 코드에선 Newton-Euler 이 빠름. *분석* 은 Lagrangian. |
| 6 | `M⁻¹` 가 forward dynamics 의 *bottleneck* | `O(n³)` 이지만 `O(n)` Articulated-Body Algorithm 으로 대체 가능. |
| 7 | Task-space inertia `Λ` 가 항상 well-defined | singular 에서 `J M⁻¹ Jᵀ` 가 rank-deficient → `Λ` 정의 안 됨. |
| 8 | Damping / friction 이 manipulator equation 에 *없음* | 이상화. 실제 robot 에선 viscous friction `B θ̇`, Coulomb friction 추가. |
| 9 | spatial inertia `G_b` 가 *body frame* 만 가능 | 다른 frame 도 OK, 단 `G_a = [Ad_{T_{ab}}]ᵀ G_b [Ad_{T_{ab}}]`. |
| 10 | `τ = Jᵀ F_tip` 가 *5장 statics 와 동일* | 8장은 *동적 외력*. statics 는 *static equilibrium*. 식 형태 같지만 의미는 dynamics 의 한 항. |

---

## 자가점검

1. Manipulator equation 의 *완전한* 형태.
2. Mass matrix `M(θ)` 의 두 가지 핵심 수학적 성질.
3. Euler-Lagrange equation.
4. Christoffel symbols `Γ_{ijk}` 의 정의.
5. Coriolis matrix `C(θ, θ̇)` 의 *passivity* 성질 (`Ṁ − 2C`).
6. Spatial inertia matrix `G_b` 의 6×6 형태.
7. 단일 강체의 Newton-Euler equation (body frame).
8. Newton-Euler recursive 의 *forward pass* 가 propagate 하는 것.
9. Newton-Euler recursive 의 *backward pass* 가 propagate 하는 것.
10. Mass matrix 를 Newton-Euler 로 구하는 방법.
11. Forward dynamics 식 (θ̈ 풀기).
12. Articulated-Body Algorithm 의 복잡도 vs naïve forward dynamics.

### 해답 (간략)

1. `τ = M(θ) θ̈ + c(θ, θ̇) + g(θ) + Jᵀ(θ) F_tip`.
2. Symmetric, positive-definite (모든 θ 에서).
3. `τ_i = d/dt(∂L/∂θ̇_i) − ∂L/∂θ_i`, `L = T − V`.
4. `Γ_{ijk} = ½(∂m_{ij}/∂θ_k + ∂m_{ik}/∂θ_j − ∂m_{jk}/∂θ_i)`.
5. `Ṁ − 2C` 가 skew-symmetric → `xᵀ(Ṁ − 2C) x = 0`, energy 보존 (input 없을 때).
6. `G_b = [[I_b, 0], [0, mI]]` (rotational + translational 통합).
7. `F_b = G_b V̇_b − [ad_{V_b}]ᵀ G_b V_b`.
8. twist `V_i` 와 그 미분 `V̇_i` — kinematics 정보.
9. wrench `F_i` 와 그로부터 `τ_i` — force 정보.
10. 각 joint 에 unit accel `θ̈ = e_i`, θ̇=0, g=0 로 inverse dynamics → 결과가 M 의 컬럼.
11. `θ̈ = M⁻¹ (τ − c − g − Jᵀ F_tip)`.
12. ABA: `O(n)`, naïve `O(n³)` (M⁻¹).

---

## 다음 학습으로

- **9장 (Trajectory Generation)** — `θ(t), θ̇(t), θ̈(t)` 의 *smooth* trajectory 생성. inverse dynamics 의 입력.
- **11장 (Robot Control)** — manipulator equation 을 *exploit* 한 *computed-torque control*: `τ = M(θ) θ̈_d + c + g` (model-based, perfect tracking 이상화).
- **12장 (Grasping)** — contact 가 더해진 constrained dynamics.
- **13장 (Mobile Robots)** — nonholonomic constraint 가 더해진 dynamics.

8장은 *어렵지만* 그 위의 9~12장 control / planning 의 *언어*. 한 번 정리해두면 후속 장이 *공식의 조합* 으로 풀린다.
