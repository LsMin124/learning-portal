# Chapter 5: Velocity Kinematics and Statics — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 5: Velocity Kinematics and Statics** (책 p.171~218) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 5장의 핵심은 **Jacobian** `J(θ)`. PoE 의 *미분* 이 그대로 Jacobian. `V = J(θ) θ̇` 와 `τ = Jᵀ F` 두 식이 *5장 전체* 의 압축.

## 들어가기 전에

- **선수 지식**
  - **3장**: SE(3), twist `V = (ω, v)`, `[Ad_T]`, wrench `F = (m, f)`
  - **4장**: PoE formula, space/body screw axes `S_i`, `B_i`
  - 선형대수: rank, null space, pseudoinverse, SVD
- **학습 목표**
  1. **Jacobian** `J(θ) ∈ R^{6×n}` 의 정의 — `V = J(θ) θ̇`
  2. **Space Jacobian** `J_s` 의 컬럼이 *현재 configuration 의 spatial screw axis*
  3. **Body Jacobian** `J_b` 의 컬럼이 *현재 configuration 의 body screw axis*
  4. 둘 사이 관계: `J_s(θ) = [Ad_{T_{sb}(θ)}] J_b(θ)`
  5. **Singularity** — `J` 의 rank 손실 → 어떤 방향의 end-effector velocity 불가능
  6. **Manipulability ellipsoid** — Jacobian 의 *지향성* 시각화
  7. **Statics**: `τ = Jᵀ F` — joint torque ↔ end-effector wrench
- **예상 학습 시간**: 120~180분

---

## 1. 평면 2R 예제 — Jacobian 직관

![Figure 5.1 — 평면 2R arm 의 end-effector velocity 분해. 교재 p.172](/courses/modern-robotics/figures/ch05/fig-5-1.png)

2-link planar arm, link 길이 `L₁ = L₂ = 1`. End-effector 위치:
$$x = \cos\theta_1 + \cos(\theta_1 + \theta_2), \quad y = \sin\theta_1 + \sin(\theta_1 + \theta_2)$$

체인 룰로 미분:
$$\begin{bmatrix} \dot{x} \\ \dot{y} \end{bmatrix} = J(\theta) \begin{bmatrix} \dot\theta_1 \\ \dot\theta_2 \end{bmatrix}$$

$$J(\theta) = \begin{bmatrix} -\sin\theta_1 - \sin(\theta_1+\theta_2) & -\sin(\theta_1+\theta_2) \\ \cos\theta_1 + \cos(\theta_1+\theta_2) & \cos(\theta_1+\theta_2) \end{bmatrix}$$

`J` 의 *컬럼* 이 *각 joint 의 단위 속도가 end-effector 에 만드는 velocity*. 이게 일반 framework 의 핵심.

---

## 2. Space Jacobian `J_s`

### 2.1 정의

PoE Space form `T(θ) = e^{[S_1]θ_1} ⋯ e^{[S_n]θ_n} M` 의 미분으로부터:

$$\mathcal{V}_s = J_s(\theta) \dot{\theta}, \quad J_s \in \mathbb{R}^{6 \times n}$$

각 컬럼:

$$J_{si}(\theta) = [Ad_{e^{[\mathcal{S}_1]\theta_1} \cdots e^{[\mathcal{S}_{i-1}]\theta_{i-1}}}] \mathcal{S}_i$$

- `J_{s1}(θ) = S_1` (그냥 zero-position screw axis)
- `J_{si}(θ)` (i ≥ 2): *현재 configuration 에서의* spatial screw axis

### 2.2 직관

각 컬럼이 *현재 configuration 에서 joint i 만 활성화될 때* end-effector 가 받는 spatial twist (단위 joint velocity 당).

> **함정 1**: `J_{si}` 는 *현재* configuration 의 screw axis 이지 zero-position 의 `S_i` 그대로가 아님. zero-position 부터 누적된 변환 `e^{[S_1]θ_1} ⋯ e^{[S_{i-1}]θ_{i-1}}` 의 adjoint 가 적용됨.

---

## 3. Body Jacobian `J_b`

### 3.1 정의

PoE Body form `T(θ) = M e^{[B_1]θ_1} ⋯ e^{[B_n]θ_n}` 의 미분:

$$\mathcal{V}_b = J_b(\theta) \dot{\theta}, \quad J_b \in \mathbb{R}^{6 \times n}$$

각 컬럼:

$$J_{bi}(\theta) = [Ad_{e^{-[\mathcal{B}_{i+1}]\theta_{i+1}} \cdots e^{-[\mathcal{B}_n]\theta_n}}] \mathcal{B}_i$$

- `J_{bn}(θ) = B_n`
- `J_{bi}(θ)` (i < n): *i 이후* 의 joint 들의 *역변환* 의 adjoint

### 3.2 Space ↔ Body 관계

같은 운동의 두 frame 표현:

$$J_s(\theta) = [Ad_{T_{sb}(\theta)}] J_b(\theta), \quad J_b(\theta) = [Ad_{T_{bs}(\theta)}] J_s(\theta)$$

`V_s = [Ad_{T_{sb}}] V_b` 의 일반화.

---

## 4. Singularity

### 4.1 정의

> **Singularity (kinematic)**: `J(θ)` 가 *full rank 가 아닌* configuration. 즉 `rank J(θ) < 6` (또는 6 < n 인 경우 `rank J < min(6, n)`).

기하적 의미: 어떤 end-effector velocity 방향 `V_d` 가 *어떤 `θ̇` 로도 달성 불가*.

### 4.2 흔한 singularity 종류

1. **Wrist singularity** — 6R arm 의 마지막 3 회전 축이 한 점에서 만나는 spherical wrist 에서, 두 축이 *동일* 해지는 configuration
2. **Elbow singularity** — 팔이 *완전히 펼친* 또는 *완전히 접힌* configuration
3. **Shoulder singularity** — 첫 번째와 두 번째 회전 축이 *평행* 해지는 configuration

### 4.3 검출

`det(J Jᵀ) = 0` (정사각형 J 가 아닐 때) 또는 `det J = 0` (정사각형). 또는 SVD 의 최소 singular value 가 0 에 근접.

> **함정 2**: singularity 근처에선 *분석적 IK* 가 무한대 해를 가질 수 있음. 6장 numeric IK 에서도 J 의 pseudoinverse 가 *수치적으로 불안정*. damped least-squares 같은 정규화 필요.

---

## 5. Manipulability Ellipsoid

### 5.1 정의

`θ̇` 에 *단위 norm* 제약 (예: `‖θ̇‖ = 1`) 을 줬을 때 end-effector 가 도달 가능한 `V` 의 집합:

$$\mathcal{V} = J \dot\theta, \quad \|\dot\theta\| = 1$$

→ `V` 의 집합이 `R⁶` (또는 R³ 의 linear / angular 부분) 의 **타원체** (ellipsoid).

### 5.2 의미

타원체의 *축* 과 *반경* 이 end-effector 의 *동작 능력의 지향성*:
- 긴 축 방향 = 그 방향으로 *빠르게* 움직일 수 있음
- 짧은 축 방향 = 그 방향으로 *느리게* (작은 EE velocity 당 큰 joint velocity 필요)
- 한 축이 *0 으로 줄어드는* configuration = singularity

### 5.3 정량적 manipulability measures

| 지표 | 정의 | 의미 |
|--|--|--|
| Yoshikawa | `√det(J Jᵀ)` | 타원체 부피 |
| Condition number | `σ_max / σ_min` | 가장 길고 짧은 축의 비율 |
| Min singular value | `σ_min` | singularity 까지의 거리 |

---

## 6. Statics — `τ = Jᵀ F`

### 6.1 *Principle of virtual work*

End-effector 에 wrench `F` 가 작용하면, robot 이 *static equilibrium* 을 유지하기 위해 joint torque `τ ∈ R^n` 이 필요. 가상 운동 `δθ` 와 `δx = J δθ` 에 대해:

$$\delta W = \tau^T \delta\theta - \mathcal{F}^T \delta x = (\tau^T - \mathcal{F}^T J) \delta\theta = 0$$

가상 운동이 임의이므로:

$$\boxed{\tau = J^T \mathcal{F}}$$

### 6.2 의미

- *역방향* statics — end-effector 의 외력 `F` 를 *지탱하기 위한* joint torque
- *force control* 의 기본 식 — 원하는 end-effector force 를 만들기 위한 joint torque 계산

### 6.3 Force ellipsoid

Manipulability ellipsoid 의 *쌍대* 개념. 단위 norm `‖τ‖ = 1` 에 대해 end-effector 가 만들 수 있는 force `F = (Jᵀ)⁻¹ τ` 의 집합.

> **함정 3**: Singularity 에서 *velocity 측면* 에선 *작은* 타원체, *force 측면* 에선 *무한* 으로 길어진 타원체. 즉 singular 에서 *어떤 방향엔 무한 힘 가능* 하지만 *그 방향으로 움직일 수 없음*.

---

## 7. Velocity / Force frame 의 일관성

### 7.1 핵심 일관성 규칙

`τ = Jᵀ F` 의 `J` 와 `F` 는 *같은 frame* 에서.
- `J_s` 와 `F_s` → `τ = J_sᵀ F_s` ✓
- `J_b` 와 `F_b` → `τ = J_bᵀ F_b` ✓
- 섞이면 안 됨 — `J_s` 와 `F_b` 는 `τ` 도출 안 됨 (frame 변환 먼저)

이 일관성이 5장의 가장 자주 빠지는 버그.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | `J_si = S_i` (zero-position 그대로) | 아님. 현재 configuration 의 누적 변환 adjoint 적용. |
| 2 | Singular configuration 에선 *모든* velocity 가 불가능 | 일부 방향만. velocity ellipsoid 의 한 축이 0 으로. |
| 3 | `det J = 0` 만 보면 singularity 검출 충분 | 정사각형 J 일 때만. n ≠ 6 이면 `det(J Jᵀ)` 또는 SVD. |
| 4 | `τ = J F` (transpose 안 함) | 잘못. `τ = Jᵀ F`. 차원 안 맞음. |
| 5 | `J_s` 와 `F_b` 로 `τ` 계산 | frame 불일치. 변환 먼저. |
| 6 | Manipulability ellipsoid 가 *구* (각 축 반경 같음) 가 항상 좋음 | 그렇긴 하지만 *작업의 방향성* 에 맞춘 *지향적* 타원체가 더 유리할 때도. |
| 7 | Body Jacobian 의 컬럼 순서 = `B_1, B_2, ...` 그대로 | 아님. `B_n` 이 가장 단순 (그대로), `B_1` 이 가장 변환 많이 받음. |
| 8 | 7-DoF redundant arm 에선 singularity 없음 | 있음. 단지 *redundancy resolution* 으로 회피 가능한 경우 많음. |
| 9 | force control 에서 `J⁻¹` 사용 | force 는 `Jᵀ` 사용. velocity 가 `J`. 둘 헷갈리지 말 것. |
| 10 | `J(θ)` 를 *수치 미분* 으로 구함 | 가능하나 비효율. analytical (PoE adjoint 누적) 이 훨씬 빠르고 정확. |

---

## 자가점검

1. Jacobian 의 정의 식 (velocity).
2. Space Jacobian `J_s` 의 i 번째 컬럼 공식.
3. Body Jacobian `J_b` 의 i 번째 컬럼 공식.
4. `J_s` 와 `J_b` 의 관계.
5. Singularity 의 정의 (rank 측면).
6. Manipulability ellipsoid 와 *singular configuration* 의 시각적 관계.
7. Statics 식 `τ = Jᵀ F` 의 *가상일* 원리 도출.
8. `J_s` 와 `F_b` 를 *그대로* 사용해서 `τ` 계산 시 문제점.
9. 평면 2R arm 의 두 가지 singular configuration.
10. 7-DoF redundant arm 의 manipulability ellipsoid 가 *6-DoF arm 대비* 가지는 장점.
11. Yoshikawa manipulability measure 의 정의.
12. Force ellipsoid 와 velocity ellipsoid 의 *쌍대* 관계.

### 해답 (간략)

1. `V = J(θ) θ̇`.
2. `J_{si} = [Ad_{e^{[S_1]θ_1} ⋯ e^{[S_{i-1}]θ_{i-1}}}] S_i`.
3. `J_{bi} = [Ad_{e^{-[B_{i+1}]θ_{i+1}} ⋯ e^{-[B_n]θ_n}}] B_i`.
4. `J_s = [Ad_{T_{sb}}] J_b`.
5. `rank J(θ) < min(6, n)`.
6. Singular = ellipsoid 의 한 축 길이가 0 (degenerate ellipsoid, 차원 손실).
7. `δW = τᵀ δθ − Fᵀ δx = τᵀ δθ − Fᵀ J δθ = 0` → `τ = Jᵀ F`.
8. frame 불일치. `F_s = [Ad_{T_{bs}}]ᵀ F_b` 로 먼저 변환.
9. (a) 팔 완전 펼침 (`θ_2 = 0`), (b) 완전 접힘 (`θ_2 = π`).
10. *Redundancy* 가 singular 회피 + secondary task 동시 처리 가능. ellipsoid 가 6-DoF 보다 *유연*.
11. `μ = √det(J Jᵀ)` — ellipsoid 부피의 proxy.
12. velocity ellipsoid 의 *주축이 길면* force ellipsoid 의 같은 축이 *짧음* (반비례).

---

## 다음 학습으로

- **6장 (Inverse Kinematics)** — Newton-Raphson 의 update: `Δθ = J⁻¹(θ) V_d` 또는 pseudoinverse. 본 장의 `J(θ)` 가 직접 사용.
- **8장 (Dynamics)** — Lagrangian `L = T - V` 의 미분에서 Jacobian 등장. mass matrix `M(θ)`, Coriolis `C(θ, θ̇)`.
- **11장 (Control)** — operational space control. `τ = Jᵀ F_d` 의 force loop + impedance.
- **13장 (Mobile)** — nonholonomic Jacobian.
