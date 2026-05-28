# Chapter 3: Rigid-Body Motions — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 3: Rigid-Body Motions** (책 p.59~135) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 3장은 책의 **수학적 토대**. 이 장의 SO(3), SE(3), twist, screw axis 표기법 위에 4장 (FK), 5장 (Jacobian), 6장 (IK), 8장 (dynamics), 11장 (control) 의 거의 모든 식이 적힌다.

## 들어가기 전에

- **선수 지식**
  - 2장 — Configuration space, implicit vs explicit representation
  - 선형대수 — 행렬·행렬식·고유값, 직교행렬, skew-symmetric 행렬
  - 미적분 — 행렬의 미분, ODE `ẋ = Ax` 와 matrix exponential
  - 벡터 미적분 — 외적 (cross product) 의 기본 성질
- **학습 목표**
  1. **SO(3)** (3D 회전군) 의 정의와 성질 — `RᵀR = I`, `det R = +1`
  2. Angular velocity `ω` ↔ **skew-symmetric** `[ω] ∈ so(3)` 의 1:1 대응
  3. **Rodrigues' formula** — 회전축 `ω̂` 와 각도 `θ` 로부터 `R = e^{[ω̂]θ}`
  4. **SE(3)** (homogeneous transform) 와 frame 변환 규칙 (subscript cancellation)
  5. **Twist** `V = (ω, v) ∈ R⁶` 와 spatial/body 표현의 차이
  6. **Screw axis** `S = (ω, v)` 와 SE(3) 의 지수 좌표
  7. **Adjoint** `[Ad_T]` — twist 좌표계 변환
  8. **Wrench** (force + moment) 와 twist 의 dual 관계
- **예상 학습 시간**: 150~210분 (수식 밀도 높음, 직관·계산 모두 필요)

---

## 1. 평면에서 시작 — SO(2) 와 SE(2)

3D 의 어려움을 피하기 위해 평면부터.

### 1.1 SO(2) — 평면 회전군

평면에서 한 frame `{b}` 가 `{s}` 에 대해 각도 `θ` 만큼 회전했을 때:

$$P = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \in SO(2)$$

성질:
- `PᵀP = I` (직교)
- `det P = +1` (방향 보존)
- `P⁻¹ = Pᵀ`

### 1.2 SE(2) — 평면 강체변환군

회전 `P` + 병진 `p ∈ R²` 를 결합:

$$T = \begin{bmatrix} P & p \\ 0 & 1 \end{bmatrix} \in SE(2), \quad T \in \mathbb{R}^{3 \times 3}$$

평면 강체의 configuration = `(x, y, θ)` 3 DoF, 또는 등가적으로 `T ∈ SE(2)`.

이 *평면 패턴* 이 3D 의 SO(3) / SE(3) 로 자연스럽게 일반화된다.

---

## 2. SO(3) — 3D 회전 행렬

### 2.1 정의

$$SO(3) = \{ R \in \mathbb{R}^{3 \times 3} \mid R^T R = I, \det R = +1 \}$$

- `RᵀR = I` (9 식 중 독립 6 식) → **6 개의 implicit constraint**
- 9 원소 − 6 constraint = **3 DoF** (회전의 자유도)
- 1 개의 connected component (det = +1 만 허용; det = −1 은 *반사*)

### 2.2 핵심 성질 5종

| # | 성질 | 의미 |
|--|--|--|
| 1 | `Rᵀ = R⁻¹` | 역행렬 = 전치 (직교성) |
| 2 | `Rᵀ ∈ SO(3)` | 회전의 역도 회전 |
| 3 | `R₁R₂ ∈ SO(3)` | 회전의 합성도 회전 (군 연산) |
| 4 | `(R₁R₂)R₃ = R₁(R₂R₃)` | 결합법칙 |
| 5 | `R₁R₂ ≠ R₂R₁` (일반적으로) | 비가환! 회전 순서 중요 |

> **함정 1**: SO(3) 는 *비가환군*. 두 회전을 곱하는 순서가 바뀌면 결과 다름. 이게 *오일러 각* 표현이 까다로운 이유.

### 2.3 Subscript cancellation rule

세 frame `{a}`, `{b}`, `{c}` 가 있을 때:

$$R_{ab} R_{bc} = R_{ac}$$
$$R_{ab} p_b = p_a$$

표기 trick: 인접한 subscript 가 *상쇄*. 자유롭게 frame 사이 변환 가능. 이게 3장 전체에서 *계속* 쓰이는 핵심 표기법.

![Figure 3.7 — 같은 점 p 를 서로 다른 자세의 세 frame {a}, {b}, {c} 에서 본 모습. 교재 p.72](/courses/modern-robotics/figures/ch03/fig-3-7.png)

### 2.4 회전이 *세 가지* 로 작용

같은 회전 행렬 `R` 이 다음 셋 모두에 사용된다 — 헷갈리지 말 것:

| 작용 | 의미 |
|--|--|
| **frame 의 자세 표현** | `R_{sb}` = {s} 에서 본 {b} 의 자세 |
| **벡터의 frame 변환** | `p_a = R_{ab} p_b` (같은 점, 다른 frame) |
| **벡터/frame 의 회전** | `p' = R p` (같은 frame, 회전된 결과) |

문맥으로 구분. 표기는 같아도 의미 다름.

---

## 3. Angular Velocity 와 so(3)

### 3.1 회전 행렬의 미분

`R(t) ∈ SO(3)` 가 시간에 따라 변할 때:

`RᵀR = I` 양변을 미분 → `ṘᵀR + RᵀṘ = 0` → `RᵀṘ = −(RᵀṘ)ᵀ`.

즉 **`RᵀṘ` 는 skew-symmetric**. 이 객체를 `[ω_b]` 라 표기.

$$[\omega_b] = R^T \dot{R} \in so(3)$$

### 3.2 Skew-symmetric `[·]` 연산

3-vector `ω = (ω₁, ω₂, ω₃)` 에 대해:

$$[\omega] = \begin{bmatrix} 0 & -\omega_3 & \omega_2 \\ \omega_3 & 0 & -\omega_1 \\ -\omega_2 & \omega_1 & 0 \end{bmatrix}$$

핵심 항등식:
- `[ω] x = ω × x` (외적의 행렬 형태)
- `[ω]ᵀ = −[ω]`
- `R [ω] Rᵀ = [Rω]` (회전된 angular velocity)

### 3.3 Spatial vs Body angular velocity

회전 운동의 angular velocity 를 **두 가지** frame 으로 표현:

$$\dot{R} R^{-1} = [\omega_s], \quad R^{-1} \dot{R} = [\omega_b]$$

| 표현 | 의미 |
|--|--|
| `ω_s` | **Spatial** — 회전을 *고정 frame {s}* 에서 본 angular velocity |
| `ω_b` | **Body** — 회전을 *body frame {b}* 에서 본 angular velocity |

관계: `ω_s = R ω_b` (즉 같은 물리량의 frame 변환).

> **함정 2**: `ω_b` 는 *moving frame 의 관성계 기준 angular velocity* 가 아님. *현재 순간 body frame 에 일치한 stationary frame* 에서 본 angular velocity. (책 p.79 강조)

---

## 4. SO(3) 의 지수 좌표 — Rodrigues' Formula

### 4.1 동기 — 회전의 *최소* 좌표

R 은 9 원소 + 6 constraint. *minimal* 표현은 3 개의 실수. *Exponential coordinates* `ω̂θ ∈ R³`:
- 단위벡터 `ω̂` ∈ S² (2 개의 좌표) — *회전축*
- 스칼라 `θ ∈ R` — *회전 각도*
- 결합: 3-vector `ω̂θ`

### 4.2 핵심 공식 — Rodrigues' formula

$$R = e^{[\hat{\omega}] \theta} = I + \sin\theta \, [\hat{\omega}] + (1 - \cos\theta) \, [\hat{\omega}]^2$$

![Figure 3.11 — 벡터 p(0) 가 축 ω̂ 주변으로 각도 θ 만큼 회전. 교재 p.83](/courses/modern-robotics/figures/ch03/fig-3-11.png)

**도출 직관**: ODE `ṗ = ω̂ × p = [ω̂] p` 의 해 `p(θ) = e^{[ω̂]θ} p(0)`. matrix exponential 의 power series 를 `[ω̂]³ = −[ω̂]` 항등식으로 정리하면 위 식.

### 4.3 Matrix exponential 정의

$$e^A = I + A + \frac{A^2}{2!} + \frac{A^3}{3!} + \cdots$$

성질:
- `e^A` 의 역 = `e^{−A}`
- `AB = BA` 이면 `e^A e^B = e^{A+B}` — 일반적으로 비가환!
- `d(e^{At})/dt = A e^{At}`

### 4.4 로그 — 역방향 (R → ω̂θ)

`log : SO(3) → so(3)` 는 *부분적으로 일대일* (멀티값):

| R 의 케이스 | ω̂θ |
|--|--|
| `R = I` | `θ = 0`, `ω̂` undefined (회전 0) |
| `tr R = −1` (`θ = π`) | 특수 케이스 — 별도 공식 |
| 일반 | `cos θ = (tr R − 1)/2`, `[ω̂] = (R − Rᵀ)/(2 sin θ)` |

> **함정 3**: `θ = π` 부근에서 분모 `sin θ → 0` 으로 수치 불안정. 알고리즘에서 별도 처리 필요.

### 4.5 Quaternion — 회전의 *4번째* 표현

**동기 — 왜 또 하나의 표현?**

지금까지 SO(3) 의 표현:

| 표현 | 원소 수 | 단점 |
|--|--|--|
| 회전 행렬 `R` | 9 (+ 6 constraint) | 메모리·연산 redundant, 행렬 곱 누적 시 *직교성 drift* |
| Euler angles (`α, β, γ`) | 3 | *gimbal lock* (특정 자세에서 1 DoF 손실) |
| Axis-angle `ω̂θ` | 3 | `θ = π` 부근 `log` *singular* (위 함정 3) |

문제 — IK 의 Newton 반복, SLAM 의 sensor fusion, animation interpolation 에서 *singular 없이 연속·미분 가능* 한 회전 표현이 필요.

**Unit quaternion** $q = (q_w, \mathbf{q}_v) = (q_w, q_x, q_y, q_z) \in S^3 \subset \mathbb{R}^4$:

- 4 원소 + 1 norm constraint $\|q\| = 1$ → effective *3 DoF*
- *non-singular* (S³ 위 매끄러움, `log` 안정)
- composition 16 mul (R 의 27 mul 대비 적음) + 누적 직교성 유지가 *재정규화 1 단계*

**Axis-angle ↔ Quaternion (핵심 공식)**

회전축 `ω̂` 와 각도 `θ` 에서:

$$q = \left( \cos\frac{\theta}{2}, \ \sin\frac{\theta}{2} \, \hat{\omega} \right)$$

`θ/2` 가 핵심 — `θ = 2π` 회전 (원 위치 복귀) 시 `q → (-1, 0, 0, 0) = -q`. 즉 **`q` 와 `-q` 는 같은 회전**. $S^3 \to SO(3)$ 가 *double cover*.

**Quaternion ↔ Rotation matrix**

$$R(q) = I + 2 q_w [\mathbf{q}_v] + 2 [\mathbf{q}_v]^2$$

`q_v = (q_x, q_y, q_z)` 는 vector part, $[\mathbf{q}_v]$ 는 skew-symmetric.

역방향 ($R \to q$):

$$q_w = \tfrac{1}{2}\sqrt{1 + \mathrm{tr}(R)}, \quad \mathbf{q}_v = \frac{1}{4 q_w} \begin{bmatrix} R_{32} - R_{23} \\ R_{13} - R_{31} \\ R_{21} - R_{12} \end{bmatrix}$$

`q_w ≈ 0` (`θ ≈ π`) 케이스에선 *대각합 trace* 중 가장 큰 항목을 기준으로 분기 (Shepperd 1978 알고리즘).

**Quaternion 곱 (회전의 합성)**

$$q_1 \otimes q_2 = \big(\, q_{1w} q_{2w} - \mathbf{q}_{1v} \cdot \mathbf{q}_{2v}, \ q_{1w} \mathbf{q}_{2v} + q_{2w} \mathbf{q}_{1v} + \mathbf{q}_{1v} \times \mathbf{q}_{2v} \,\big)$$

비가환 — SO(3) 비가환성 그대로 반영. $R(q_1) R(q_2) = R(q_1 \otimes q_2)$ 가 성립.

**점의 회전**

3-vector `p` 를 *pure quaternion* `(0, p)` 로 augment:

$$p' = q \otimes (0, p) \otimes q^{-1}, \quad q^{-1} = (q_w, -\mathbf{q}_v) \ \ (\text{unit } q)$$

**SLERP — Spherical Linear Interpolation**

두 quaternion 사이 *최단 측지선* 보간:

$$\mathrm{slerp}(q_0, q_1; t) = \frac{\sin((1-t)\Omega)}{\sin\Omega} q_0 + \frac{\sin(t\Omega)}{\sin\Omega} q_1$$

$\cos\Omega = q_0 \cdot q_1$ (4D 내적). 보간 전 `q_0 · q_1 < 0` 이면 `q_1 ← -q_1` 로 *짧은 경로* 보장.

`Ω → 0` 에선 `sin Ω` 분모 위험 → fallback `lerp(q_0, q_1; t) = (1-t) q_0 + t q_1`, then normalize.

animation, motion blending, IK 의 *desired pose interpolation* 표준.

**IK 안정성 관점 — 핵심 응용**

6 장 (IK) Newton 반복의 일반 형태:

```
error = log(T_desired · T_current^{-1})     # SE(3) → twist
θ_{k+1} = θ_k + J† · error
```

`log` 가 `θ ≈ π` (회전 반전) 부근에서 *불연속·발산* — Rodrigues log 의 `sin θ → 0`. quaternion 으로 회전 부분을 별도 추적하면 이 singular 우회 가능.

**Quaternion-based IK error twist**:

1. 회전 부분: `q_d` (desired), `q_c` (current) 으로 추적
2. error quaternion $q_e = q_d \otimes q_c^{-1}$
3. *짧은 경로*: `q_{e,w} < 0` 이면 `q_e ← -q_e`
4. small-angle approx: $\omega_e \approx 2 \mathbf{q}_{e,v}$ (`θ_e ≈ 0` 에서 $\mathbf{q}_v \approx (\theta/2) \hat{\omega}$)
5. Newton 갱신에 `ω_e` 직접 투입

이 *quaternion-based IK* 가 ROS MoveIt, KDL, Bullet, OpenRAVE 등 모든 산업 IK 의 기본 — 책의 PoE 기반 SE(3) log 가 가르치는 우아함과는 별개로, *실전 코드*는 quaternion path 가 표준.

**Quaternion 전용 함정**

| # | 함정 | 정정 |
|--|--|--|
| q1 | `q` 와 `-q` 가 다른 회전 | 같은 회전 (double cover). 보간 전 부호 통일 (`q_0 · q_1 ≥ 0`). |
| q2 | quaternion 곱 = 원소별 곱 | 아님. Hamilton 곱 (scalar−dot + cross). 행렬 곱과 같이 비가환. |
| q3 | 단위 norm 이 자동 유지 | 누적 곱 시 *수치 drift*. 매 iter `q ← q/‖q‖` 정규화. |
| q4 | SLERP 가 항상 안정 | `Ω → 0` 위험. LERP+normalize 로 fallback. |
| q5 | quaternion 원소 순서 표준 | 라이브러리마다 다름 — Eigen `(x,y,z,w)` vs ROS/책 `(w,x,y,z)`. 데이터 교환 시 확인. |

---

## 5. SE(3) — 강체변환의 homogeneous form

### 5.1 정의

$$SE(3) = \left\{ T = \begin{bmatrix} R & p \\ 0 & 1 \end{bmatrix} \,\middle|\, R \in SO(3),\ p \in \mathbb{R}^3 \right\}$$

4×4 행렬, **6 DoF** (회전 3 + 병진 3).

### 5.2 점·벡터의 변환

3D 점 `x = (x, y, z)` 를 4D homogeneous coord `x̃ = (x, y, z, 1)` 로 augment:

$$\tilde{x}_a = T_{ab} \tilde{x}_b$$

→ `x_a = R_{ab} x_b + p_{ab}` (회전 + 병진).

### 5.3 군 연산

| 연산 | 결과 |
|--|--|
| 합성 | `T_{ac} = T_{ab} T_{bc}` (subscript cancellation) |
| 역원 | `T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]` (그냥 `Tᵀ` 가 아님!) |

> **함정 4**: SE(3) 의 역원은 *전치* 아님. `T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]`. 자주 실수.

![Figure 3.14 — 공간 안의 세 frame {a}, {b}, {c} 와 점 v. 교재 p.92](/courses/modern-robotics/figures/ch03/fig-3-14.png)

---

## 6. Twist — SE(3) 의 속도

### 6.1 정의

`T(t) ∈ SE(3)` 의 미분을 *6-vector* 로 표현:

$$\mathcal{V} = \begin{bmatrix} \omega \\ v \end{bmatrix} \in \mathbb{R}^6$$

- 첫 3 원소 `ω` = angular velocity
- 다음 3 원소 `v` = linear velocity (단, 의미 주의 — 6.3 참조)

### 6.2 Spatial twist vs Body twist

$$T^{-1} \dot{T} = [\mathcal{V}_b] = \begin{bmatrix} [\omega_b] & v_b \\ 0 & 0 \end{bmatrix} \in se(3)$$

$$\dot{T} T^{-1} = [\mathcal{V}_s] = \begin{bmatrix} [\omega_s] & v_s \\ 0 & 0 \end{bmatrix} \in se(3)$$

### 6.3 `v_s` 의 *비직관적* 해석

`v_s = ṗ − ω_s × p`. 단순한 origin 의 속도가 *아니다*.

> **물리적 의미**: 강체가 *무한대로 확장* 되었다고 상상할 때, *현재 순간 fixed frame 의 원점* 에 일치하는 그 강체의 점이 가진 속도, fixed frame 에서 본 것. (책 p.99)

![Figure 3.17 — v_s 의 물리 해석. 강체의 가상 확장 + 고정 frame 원점에서의 instantaneous velocity. 교재 p.98](/courses/modern-robotics/figures/ch03/fig-3-17.png)

`v_b` 는 비교적 직관적 — body frame 에 일치한 stationary frame 에서 본 *body origin 의 linear velocity*.

### 6.4 Adjoint — twist frame 변환

$$\mathcal{V}_s = [Ad_T] \mathcal{V}_b, \quad [Ad_T] = \begin{bmatrix} R & 0 \\ [p] R & R \end{bmatrix} \in \mathbb{R}^{6 \times 6}$$

`[Ad_T]` 는 6×6 행렬. spatial ↔ body twist 변환. *모든 frame change* 에서 등장.

---

## 7. Screw Axis 와 SE(3) 지수 좌표

### 7.1 Screw motion 의 의미

> 모든 강체 운동은 **하나의 축** 을 중심으로 *회전 + 그 축을 따라 병진* 의 결합 (= screw 운동) 으로 표현 가능. (**Chasles' theorem**)

이를 정량화하면 SE(3) 의 *minimal 6-parameter* 표현이 나옴.

### 7.2 Screw axis 와 normalized twist

Screw 의 표현:
- **축의 방향** `ω̂ ∈ S²` (단위벡터)
- **축 위의 한 점** `q ∈ R³`
- **pitch** `h` — 한 바퀴 회전 당 축 방향 병진 거리

이 셋을 *6-vector* `S = (ω, v)` 로 인코딩:

$$\mathcal{S} = (\omega, v), \quad \omega = \hat{\omega}, \quad v = -\hat{\omega} \times q + h \hat{\omega}$$

- 순수 회전 (h = 0): `v = −ω̂ × q`
- 순수 병진 (회전 없음, ω = 0): `S = (0, v̂)` with `‖v̂‖ = 1`

> **함정 5**: 일반 twist `V` 는 *normalized* 가 아님. **screw axis** `S` 는 `‖ω‖ = 1` 또는 (회전 없을 시) `‖v‖ = 1` 로 *정규화* 된 twist. 헷갈리지 말 것.

### 7.3 SE(3) 의 지수 좌표

스칼라 `θ` 와 함께:

$$T = e^{[\mathcal{S}] \theta}, \quad [\mathcal{S}] = \begin{bmatrix} [\omega] & v \\ 0 & 0 \end{bmatrix}$$

이 *6-vector `Sθ`* 가 SE(3) 의 *exponential coordinates*. SO(3) 의 `ω̂θ` 일반화.

**닫힌 형태** (Rodrigues 의 SE(3) 버전):

$$e^{[\mathcal{S}]\theta} = \begin{bmatrix} e^{[\omega]\theta} & G(\theta) v \\ 0 & 1 \end{bmatrix}$$

$$G(\theta) = I \theta + (1 - \cos\theta) [\omega] + (\theta - \sin\theta) [\omega]^2$$

### 7.4 SE(3) 의 로그

역방향 `T → Sθ` 도 정의됨. 자세한 공식은 책 §3.3.3.2.

> **응용 전조**: 다음 장 (FK) 의 *PoE (Product of Exponentials) formula* 가 바로 이 SE(3) 지수 좌표의 직접 적용. 각 joint 마다 screw axis 의 지수를 곱한다.

![Figure 3.20 — 평면 위 두 frame {b} 와 {c} 를 잇는 screw motion. 교재 p.107](/courses/modern-robotics/figures/ch03/fig-3-20.png)

---

## 8. Wrench — Twist 의 dual

### 8.1 정의

강체에 작용하는 **force + moment** 를 6-vector 로:

$$\mathcal{F} = \begin{bmatrix} m \\ f \end{bmatrix} \in \mathbb{R}^6$$

- `m` ∈ R³ — moment (토크)
- `f` ∈ R³ — force

(twist 와 *순서가 다름* — twist 는 (ω, v), wrench 는 (m, f). 일관성 위해 책의 표기 따를 것.)

### 8.2 Twist 와의 dual 관계 — Power

물리적으로 **power** = 일 / 시간:

$$P = \mathcal{F}^T \mathcal{V}$$

이 inner product 는 frame 무관 (둘 다 같은 frame 에서 표현하면).

### 8.3 Wrench 의 frame 변환

$$\mathcal{F}_b = [Ad_T]^T \mathcal{F}_a, \quad T = T_{ab}$$

twist 는 `[Ad_T]` 로 변환, wrench 는 `[Ad_T]ᵀ` 로 변환 — *dual* 관계.

> **함정 6**: twist 변환 ↔ wrench 변환 의 방향과 transpose 위치. 외워두지 않으면 부호·축 헷갈림 발생. 자주 빠지는 5장 (statics) 함정.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | 두 회전 `R₁R₂` 가 `R₂R₁` 와 같다 | SO(3) 는 *비가환*. 회전 순서 중요. |
| 2 | `ω_b` = *moving frame 에서 본* angular velocity | 아님. *순간 일치한 stationary frame* 에서 본 것. |
| 3 | `θ = π` 근처에서 `log R` 일반 공식 사용 | `sin θ → 0` 으로 수치 불안정. 별도 공식 필요. |
| 4 | `T⁻¹ = Tᵀ` | 아님. `T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]`. R 만 직교. |
| 5 | 모든 twist 가 screw axis | screw axis 는 *정규화된* twist. 일반 twist 와 다름. |
| 6 | wrench 가 `[Ad_T]` 로 frame 변환 | `[Ad_T]ᵀ` 로 (transpose). dual 관계. |
| 7 | `[ω]` 의 `[·]` 와 SE(3) 의 `[V]` 표기 혼동 | 같은 brace 지만 다른 객체. so(3) vs se(3). |
| 8 | `e^{A+B} = e^A e^B` 항상 성립 | `AB = BA` 인 경우만. SO(3) / SE(3) 에선 *일반적으로 안 성립*. |
| 9 | screw motion 의 pitch `h` 가 항상 finite | 순수 회전이면 `h = 0`, 순수 병진이면 `h = ∞` (별도 표기). |
| 10 | spatial twist `v_s` = body origin 의 속도 | 아님. *가상 확장된 body 의 fixed frame 원점에서의 속도*. |

---

## 자가점검

1. `SO(3)` 의 정의를 2 개의 조건으로 적어라.
2. `[ω] x = ?` — 외적과의 관계.
3. Rodrigues' formula 를 직접 적어라.
4. `T = (R, p) ∈ SE(3)` 의 *역원* `T⁻¹` 를 닫힌 형태로.
5. Spatial vs body angular velocity 의 정의 (`Ṙ R⁻¹` 와 `R⁻¹ Ṙ`).
6. `[Ad_T]` 의 6×6 형태와 그 역할.
7. Screw axis `S = (ω, v)` 의 정규화 조건 (회전 / 병진 케이스).
8. 평면 회전 30° 의 `R ∈ SO(2)` 행렬을 직접 적어라.
9. 두 회전 `R₁ = Rot(x̂, π/2)`, `R₂ = Rot(ẑ, π)` 의 합성 `R₁R₂` 와 `R₂R₁` 가 다름을 확인하라.
10. `tr R = −1` 인 회전 행렬의 회전 각도는?
11. Twist `V_s` 와 `V_b` 의 변환식.
12. Wrench frame 변환식 — `F_b = ? · F_a`.
13. Unit quaternion `q` 의 *axis-angle* 형태 (`ω̂`, `θ` 주어졌을 때).
14. 같은 회전을 표현하는 두 quaternion 사이의 관계 (`q` 와 누구가 같음?).
15. SLERP 가 LERP 와 다른 점, 그리고 LERP 로 *fallback* 되는 조건.

### 해답 (간략)

1. `RᵀR = I`, `det R = +1`.
2. `[ω] x = ω × x`.
3. `R = I + sin θ [ω̂] + (1 − cos θ) [ω̂]²`.
4. `T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]`.
5. `[ω_s] = Ṙ R⁻¹` (spatial), `[ω_b] = R⁻¹ Ṙ` (body).
6. `[Ad_T] = [R, 0; [p]R, R]`, twist 의 frame 변환 `V_s = [Ad_T] V_b`.
7. 회전 있을 때 `‖ω‖ = 1`, 순수 병진일 때 `‖v‖ = 1`.
8. `[cos 30°, −sin 30°; sin 30°, cos 30°]`.
9. 두 회전 모두 직접 곱해보면 결과 행렬이 다름 (SO(3) 비가환 확인).
10. `cos θ = (tr R − 1)/2 = −1` → `θ = π`.
11. `V_s = [Ad_T] V_b` (`T = T_{sb}`), `V_b = [Ad_{T⁻¹}] V_s`.
12. `F_b = [Ad_T]ᵀ F_a` (dual; transpose 위치 주의).
13. $q = (\cos(\theta/2), \sin(\theta/2)\hat{\omega})$.
14. `q` 와 `-q` 가 같은 회전 (S³ → SO(3) double cover).
15. SLERP 는 4D 단위 구의 *측지선* (각속도 일정). LERP 는 4D *직선*. `Ω → 0` (두 quaternion 이 거의 같음) 일 때 SLERP 의 `sin Ω` 분모 위험 → LERP + normalize 로 fallback.

---

## 다음 학습으로

- **4장 (Forward Kinematics)** — *PoE (Product of Exponentials) formula*. 본 장의 SE(3) 지수 좌표가 robot arm 의 각 joint screw axis 에 직접 적용.
- **5장 (Velocity Kinematics)** — *Jacobian*. 본 장의 spatial / body twist 가 그대로 등장. `V = J(θ) θ̇`.
- **6장 (Inverse Kinematics)** — *Newton-Raphson* with body twist + matrix log. 본 장의 `log : SE(3) → se(3)` 가 핵심.
- **8장 (Dynamics)** — *Lagrangian formulation* 에서 Adjoint 가 inertia frame 변환에 사용.
- **11장 (Control)** — body wrench 와 desired twist trajectory tracking.

본 장의 표기 (`[ω̂]θ`, `S`, `[Ad_T]`, `V_b`, `F_s`) 가 책 나머지 모든 장의 *언어* 다. 외울 게 많아도 표기에 익숙해지면 이후 장이 *기계적으로* 풀린다.

---

## §X Modern Lie Group Library

### 라이브러리

| | 언어 | 특징 |
|--|--|--|
| Sophus | C++ | SLAM 표준, header-only |
| manif | C++/Python | modern Lie group + auto-diff |
| modern_robotics | Python | 책의 ref |
| Pinocchio | C++/Python | rigid body + Lie group |
| Eigen + Geometry | C++ | basic SO(3), SE(3) |

### Quaternion 산업 응용

- Game engine — Unity, Unreal
- Aerospace — IMU, attitude estimation
- VR/AR — head tracking (Oculus, Apple Vision Pro)
- Robotics — SLAM, sensor fusion

### Dual quaternion

$q_{dual} = q_r + \epsilon q_d, \epsilon^2 = 0$. Rotation + translation 통합, SE(3) 의 8-parameter, screw motion 직접 표현.

### Numerical stability

- Quaternion: renormalization 필요 (drift 방지)
- Rotation matrix: re-orthogonalization (SVD)
- SE(3) log: identity 근처 Taylor expansion
