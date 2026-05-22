# Chapter 4: Forward Kinematics — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 4: Forward Kinematics** (책 p.137~169) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 4장의 핵심은 **PoE (Product of Exponentials) Formula** — open-chain 로봇의 forward kinematics 를 *각 joint 의 screw axis 의 지수의 곱* 으로 표현하는 우아한 framework. 3장 SE(3) 지수 좌표가 *그대로 응용* 된다.

## 들어가기 전에

- **선수 지식**
  - **3장 (필수)** — SE(3), screw axis, exponential coordinates
  - 선형대수 — 행렬 곱
- **학습 목표**
  1. **Forward kinematics** 의 정의 — joint 각 `θ` → end-effector pose `T(θ)`
  2. **PoE formula (Space form)**: `T(θ) = e^{[S₁]θ₁} ⋯ e^{[Sₙ]θₙ} M`
  3. **PoE formula (Body form)**: `T(θ) = M e^{[B₁]θ₁} ⋯ e^{[Bₙ]θₙ}`
  4. Zero-position frame `M` 과 screw axis `S_i` / `B_i` 식별 방법
  5. DH parameters 와 PoE 의 비교 — *왜 PoE 가 더 자연스러운가*
  6. 산업 표준 **URDF** 형식 — joint·link 의 XML 표현
- **예상 학습 시간**: 90~120분 (구조는 단순하나 표기 익숙해지기)

---

## 1. Forward Kinematics 의 정의

> **Forward Kinematics (FK)**: 로봇의 joint 변수 `θ = (θ₁, ..., θₙ)` 에서 end-effector frame `{b}` 가 fixed frame `{s}` 에 대해 가지는 자세 `T_{sb}(θ) ∈ SE(3)` 를 계산하는 문제.

함수 형태:
$$T_{sb}: \mathbb{R}^n \to SE(3), \quad \theta \mapsto T_{sb}(\theta)$$

- 입력: n 개의 joint 각 (회전형 R) 또는 변위 (병진형 P)
- 출력: end-effector 의 4×4 transform

대조: **Inverse Kinematics (IK)** = `T → θ` (6장). FK 보다 어려움 — 비선형, 다해, 무해 가능.

---

## 2. 평면 예제 — 3R planar arm 으로 직관

![Figure 4.1 — 3R planar open chain. 교재 p.138](/courses/modern-robotics/figures/ch04/fig-4-1.png)

3 개의 회전 joint, 평면. Link 길이 `L₁, L₂, L₃`.

**고전적 방법** (homogeneous transform 의 chain):

$$T_{04}(\theta) = T_{01}(\theta_1) T_{12}(\theta_2) T_{23}(\theta_3) T_{34}$$

각 `T_{i,i+1}` 은 link 사이의 *상대* 변환. 이 방식은 익숙하지만 *각 joint 마다 frame 부여* 가 필요 — 임의성 ↑.

**PoE 방법** (다음 절): frame 은 `{s}` 와 `{b}` 둘만. screw axis 로 직접 표현.

---

## 3. PoE Formula — Space Form

### 3.1 핵심 식

$$T_{sb}(\theta) = e^{[\mathcal{S}_1] \theta_1} e^{[\mathcal{S}_2] \theta_2} \cdots e^{[\mathcal{S}_n] \theta_n} M$$

- `M ∈ SE(3)`: **zero-position** 의 `T_{sb}` — 모든 `θ_i = 0` 일 때 end-effector pose
- `S_i ∈ R⁶`: i 번째 joint 의 **screw axis at zero position**, frame `{s}` 에서 표현
- `θ_i`: i 번째 joint 변수

![Figure 4.2 — PoE formula 의 n-link spatial 일러스트. 교재 p.141](/courses/modern-robotics/figures/ch04/fig-4-2.png)

### 3.2 *왜* 이 식이 성립?

직관:
1. 처음엔 모두 zero position → end-effector at `M`
2. joint n 부터 *역방향* 으로 하나씩 활성화
3. joint i 가 `θ_i` 만큼 회전/병진 → 그 *바깥쪽* 모든 link 가 함께 움직임
4. `e^{[S_i]θ_i}` 가 *space frame {s} 기준* 의 그 운동

**관찰**: joint i 가 작동하면, link i 부터 link n 까지 *모두* `e^{[S_i]θ_i}` 만큼 같이 변환. 이게 `S_i` 가 *zero-position* 의 axis 인 이유 — 미리 변형된 형태가 아니라 *home position 의 정적 axis*.

### 3.3 `S_i` 식별 방법

각 joint 의 zero-position 에서:
- 회전 joint: `ω_i = ω̂` (축 방향, unit), `v_i = −ω̂ × q` (q = 축 위의 한 점)
- 병진 joint: `ω_i = 0`, `v_i = v̂` (병진 방향, unit)

**팁**: 모든 좌표는 `{s}` 에서. 회전 축의 방향과 axis 위의 *임의의 한 점* `q` 만 정하면 됨.

### 3.4 예제 — 3R spatial open chain

![Figure 4.3 — 3R spatial open chain. 교재 p.143](/courses/modern-robotics/figures/ch04/fig-4-3.png)

Zero position 에서 base frame `{s}` 의 축이 `(x̂, ŷ, ẑ)` 라 하면 (책 §4.1.2 예제):
- `S₁ = (0, 0, 1, 0, 0, 0)` (ẑ 축 회전, origin 통과)
- `S₂ = (0, −1, 0, ...)` (앞쪽 link 의 ŷ 축 회전)
- `S₃ = ...`

`M = T_{sb}(0)` 은 zero-position 의 end-effector pose 직접 측정.

---

## 4. PoE Formula — Body Form

### 4.1 핵심 식

$$T_{sb}(\theta) = M \cdot e^{[\mathcal{B}_1] \theta_1} e^{[\mathcal{B}_2] \theta_2} \cdots e^{[\mathcal{B}_n] \theta_n}$$

- `B_i`: 같은 joint i 의 screw axis, *body frame `{b}`* 에서 표현 (zero-position 기준)

### 4.2 Space form 과의 관계

`B_i` 와 `S_i` 는 같은 joint 의 *다른 frame 표현*:

$$\mathcal{B}_i = [Ad_{M^{-1}}] \mathcal{S}_i$$

즉 `M⁻¹` 의 adjoint 로 변환. (3장 §6.4)

### 4.3 언제 어느 form 을 쓰나

| 상황 | 권장 form |
|--|--|
| 기하적 이해, 시각화 | Space form (`S_i`) |
| 5장 body Jacobian | Body form (`B_i`) |
| 6장 IK 의 body-frame iteration | Body form |
| URDF parsing | Space form (보통) |

둘 다 같은 답을 줌. 표현의 차이일 뿐.

---

## 5. 산업 로봇 예제 — UR5

![Figure 4.6 — Universal Robots UR5 6R arm + zero position 의 6 screw axes. 교재 p.148](/courses/modern-robotics/figures/ch04/fig-4-6.png)

UR5 (6R 산업용 arm) 의 zero-position screw axes `S₁` ~ `S₆`. 길이 파라미터:
- `W₁ = 109 mm`, `W₂ = 82 mm`
- `L₁ = 425 mm`, `L₂ = 392 mm`
- `H₁ = 89 mm`, `H₂ = 95 mm`

책 §4.1.2 의 표에서 각 `S_i` 의 `(ω, v)` 6 성분이 명시. 그 표를 `M = T_{sb}(0)` 과 결합하여 PoE formula 로 `T(θ)` 계산.

> **실용 팁**: 산업용 robot driver (Universal Robots, KUKA, etc.) 가 받는 joint 각 → 본인 코드에서 PoE 로 EE pose 계산 → 시뮬레이션·rendering 가능.

---

## 6. PoE vs DH (Denavit-Hartenberg)

### 6.1 DH parameters

전통적인 방법 — 4 개의 파라미터 `(α_i, a_i, d_i, θ_i)` 로 인접 joint frame 간 변환 표현.

장점:
- 표준화 (1955 년부터)
- 파라미터 수 minimal (joint 당 4 개)

단점:
- **각 link 에 frame 부여 필요** — 임의성·convention 차이 (modified vs classical DH)
- **기하적 직관 약함** — α, a, d 의 의미가 즉시 안 보임
- prismatic joint 에서 어색

### 6.2 PoE

장점:
- frame 은 `{s}`, `{b}` 둘만 — *임의성 최소*
- **기하적 직관 명확** — 각 `S_i` 가 *공간상의 실제 축*
- prismatic / revolute 동일 framework
- Jacobian 도출이 자연스러움 (5장)

단점:
- 파라미터 수 약간 많음 (joint 당 6 + `M` 의 6)
- 표준화 늦음 (Park 1994)

> **본 책의 선택**: PoE 일관 사용. DH 는 단지 비교 목적으로 §4.1.4 에 언급.

---

## 7. URDF — 산업 표준 robot description

### 7.1 무엇인가

**URDF (Unified Robot Description Format)**: ROS (Robot Operating System) 에서 사용하는 XML 기반 robot 정의 형식.

### 7.2 핵심 구조

```xml
<robot name="ur5">
  <link name="base_link">
    <inertial>
      <origin xyz="0 0 0"/>
      <mass value="4.0"/>
      <inertia ixx="..." .../>
    </inertial>
    <visual> ... </visual>
    <collision> ... </collision>
  </link>

  <joint name="shoulder_pan_joint" type="revolute">
    <parent link="base_link"/>
    <child link="shoulder_link"/>
    <origin xyz="0 0 0.089" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="150" velocity="3.15"/>
  </joint>

  <!-- 반복: link + joint -->
</robot>
```

### 7.3 정보 매핑

| URDF 요소 | PoE 의 무엇 |
|--|--|
| `joint.axis` | screw axis 의 `ω̂` (회전형) 또는 `v̂` (병진형) |
| `joint.origin` (parent link 기준) | zero-position 에서 joint 위치 = `q` |
| 마지막 link 의 누적 transform | `M` (end-effector pose at zero position) |
| `joint.limit` | `θ_i` 의 범위 |
| `link.inertial` | 8장 (dynamics) 에서 사용 |

ROS / Gazebo / RViz / MoveIt 모두 URDF 파싱 후 작업.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | `S_i` 는 *현재 configuration* 의 screw axis | 아님. *zero position* 의 screw axis. 항상 정적. |
| 2 | Space form 과 Body form 이 다른 robot 을 표현 | 같은 robot. `B_i = [Ad_{M⁻¹}] S_i` 로 변환. |
| 3 | `e^{[S_i]θ_i}` 들을 곱하는 *순서* 가 자유로움 | 비가환. `S₁ → S_n` 또는 그 역, 책의 convention 따를 것. |
| 4 | `M` 은 단위행렬 (origin) | 아님. zero-position 의 end-effector pose. 보통 origin 이 아님. |
| 5 | PoE 의 `S_i` 가 DH 파라미터로 자동 변환 가능 | 가능은 하나 일관성 위해 PoE 를 *처음부터* 따로 정립 권장. |
| 6 | URDF 의 `joint.origin` = `S_i` 의 `q` 그대로 | URDF 는 *parent link frame 기준* 좌표. `{s}` 까지 누적 변환 필요. |
| 7 | n-DoF arm 의 zero position 이 *물리적으로 가능한* configuration 인가 | 임의의 base configuration 선택 가능. 보통 모든 joint = 0 의 *기준* configuration. |
| 8 | screw axis 의 `q` 가 유일 | 아님. 축 위의 *어느 점* 이든 OK. `v` 가 그에 따라 달라질 뿐 `S` 는 같은 *축* 을 표현. |
| 9 | PoE 결과가 *반드시* SE(3) | 수치 계산 시 누적 오차로 SO(3) constraint (`RᵀR = I`) 위반 가능. Re-orthogonalization 필요. |
| 10 | URDF 만 있으면 *직접* FK 계산 가능 | URDF parser + PoE 또는 DH chain 빌딩 필요. 자동 안 됨. |

---

## 자가점검

1. PoE Space form 식을 직접 적어라.
2. PoE Body form 식과 Space form 의 관계 (`B_i` 와 `S_i`).
3. `M` 의 의미.
4. revolute joint 의 zero-position screw axis `S_i` 의 `(ω, v)` 결정 방법.
5. prismatic joint 의 zero-position screw axis 형태.
6. PoE 의 *space frame* 은 어디인가 — `{s}` 와 `{0}` 의 차이.
7. DH 와 PoE 의 가장 큰 *구조적* 차이.
8. URDF 의 `<joint axis="...">` 는 어느 frame 기준?
9. 두 joint 의 순서 `e^{[S₁]θ₁} e^{[S₂]θ₂}` 와 `e^{[S₂]θ₂} e^{[S₁]θ₁}` 가 일반적으로 같은 결과인가?
10. 6-DoF industrial arm 의 PoE 표현에서 *총 파라미터 수* 는?

### 해답 (간략)

1. `T(θ) = e^{[S₁]θ₁} ⋯ e^{[Sₙ]θₙ} M`.
2. `T(θ) = M e^{[B₁]θ₁} ⋯ e^{[Bₙ]θₙ}`, `B_i = [Ad_{M⁻¹}] S_i`.
3. zero-position (모든 `θ_i = 0`) 의 end-effector pose `T_{sb}(0)`.
4. `ω = ω̂` (축 방향, unit), `v = −ω̂ × q` (q = 축 위 한 점).
5. `ω = 0`, `v = v̂` (병진 방향, unit).
6. `{s}` = space frame (base). 표준 표기. PoE 책에서 `{s}` 사용. 다른 책의 `{0}` 와 같은 의미.
7. DH 는 *각 link 에 frame 부여* → 임의성. PoE 는 `{s}`, `{b}` 둘만 + screw axis.
8. *parent link frame*. `{s}` 좌표로 변환하려면 누적 변환 필요.
9. 일반적으로 다름. SO(3) / SE(3) 가 비가환.
10. screw axis 6 × n + `M` 의 6 자유도 = 6n + 6. 예: 6-DoF → 42.

---

## 다음 학습으로

- **5장 (Velocity Kinematics)** — Jacobian `J(θ)` 의 *Space form* 과 *Body form* 모두 PoE 에서 자연스럽게 도출. `V_s = J_s(θ) θ̇`, `V_b = J_b(θ) θ̇`.
- **6장 (Inverse Kinematics)** — Newton-Raphson with PoE FK + matrix log. 본 장의 PoE 가 핵심 입력.
- **8장 (Dynamics)** — link 의 inertia frame 표현에 4장의 frame 매개변수 사용.

PoE 의 *우아함* — `T(θ)` 를 *해석적 함수* 로 본 결과, 후속 장의 미분 / 최적화 / 제어가 *기계적* 으로 풀린다.
