# Ch 3 Rigid-Body Motions — 퀴즈

> 14 문항 (개념 4 / 계산 5 / 디버그 3 / 면접 2). 답은 펼치기 — 먼저 풀어볼 것.

---

## 개념

### Q1. SO(3) 정의

`SO(3)` 의 정의를 두 조건으로 적어라. 각 조건이 의미하는 바를 설명하라.

<details><summary>답</summary>

$$SO(3) = \{ R \in \mathbb{R}^{3 \times 3} \mid R^T R = I, \det R = +1 \}$$

- `RᵀR = I` — *직교성* (orthonormal). 행/열이 모두 단위벡터이며 서로 직교. 회전 후에도 *내적·길이가 보존* 됨을 의미.
- `det R = +1` — *방향 보존* (orientation-preserving). `det = −1` 은 *반사* (거울 대칭) 로, 오른손계 ↔ 왼손계 변환. 회전은 반사가 아니므로 +1 만 허용.

</details>

---

### Q2. so(3) vs SO(3)

`[ω]` (소문자 so(3)) 와 `R` (대문자 SO(3)) 의 차이를 설명하라.

<details><summary>답</summary>

- `R ∈ SO(3)`: *3×3 회전 행렬*. 군 (group). 곱셈으로 합성. 한 시점의 *자세*.
- `[ω] ∈ so(3)`: *3×3 skew-symmetric 행렬*. 군의 *Lie algebra* (tangent space at identity). 덧셈으로 합성. *순간 각속도* 또는 *회전의 미소 변화율*.

연결: `R = e^{[ω̂]θ}` — Lie algebra → Lie group (지수 사상).

> 비유: `SO(3)` 는 *위치*, `so(3)` 는 *속도*. 위치는 multiplicative 로 누적되고, 속도는 additive 로 합성됨.

</details>

---

### Q3. Twist 의 두 frame

`V_s` (spatial twist) 와 `V_b` (body twist) 의 정의 식을 적고, 둘 다 *같은 물리량* 인지 *다른 물리량* 인지 설명하라.

<details><summary>답</summary>

$$T^{-1} \dot{T} = [\mathcal{V}_b], \quad \dot{T} T^{-1} = [\mathcal{V}_s]$$

같은 물리적 운동의 *두 frame 표현*. 즉:
- `V_s` = 운동을 *고정 frame {s}* 에서 표현
- `V_b` = 같은 운동을 *body frame {b}* 에서 표현

관계: `V_s = [Ad_T] V_b` (frame 변환). 같은 운동, 다른 좌표계.

</details>

---

### Q4. Wrench 와 twist 의 dual

Wrench `F = (m, f)` 가 *왜* twist 와 dual 관계인가? Power 와 frame 변환 두 측면에서 답하라.

<details><summary>답</summary>

**Power**: `P = Fᵀ V` 는 frame 무관 (둘 다 같은 frame). 이게 dual pairing.

**Frame 변환**: twist 는 `V_s = [Ad_T] V_b` 로 변환 — pullback. wrench 는 `F_b = [Ad_T]ᵀ F_a` 로 변환 — pushforward 의 transpose. 두 transpose 가 *서로 dual* 이라 power 가 보존됨.

수학적으로 R-vector space 와 그 dual space 의 관계. 5장 (statics) 에서 통일적으로 다룸.

</details>

---

## 계산

### Q5. 회전 행렬 직접 계산

축 `ω̂ = (0, 0, 1)`, 각도 `θ = π/2` 의 회전 행렬을 Rodrigues' formula 로 구하라.

<details><summary>답</summary>

`[ω̂] = [[0, −1, 0], [1, 0, 0], [0, 0, 0]]`. `[ω̂]² = [[−1, 0, 0], [0, −1, 0], [0, 0, 0]]`.

$$R = I + \sin(\pi/2) [\hat{\omega}] + (1 - \cos(\pi/2)) [\hat{\omega}]^2$$

`sin(π/2) = 1`, `1 − cos(π/2) = 1`:

$$R = I + [\hat{\omega}] + [\hat{\omega}]^2 = \begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

검증: z 축 90° 회전 → x → y, y → −x, z → z. ✓

</details>

---

### Q6. SE(3) 역원

$$T = \begin{bmatrix} 0 & -1 & 0 & 2 \\ 1 & 0 & 0 & 3 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

`T⁻¹` 를 직접 적어라.

<details><summary>답</summary>

`R = [[0, −1, 0], [1, 0, 0], [0, 0, 1]]`, `p = (2, 3, 1)`.

`Rᵀ = [[0, 1, 0], [−1, 0, 0], [0, 0, 1]]`.

`−Rᵀ p = −[[0·2 + 1·3 + 0·1], [−1·2 + 0·3 + 0·1], [0·2 + 0·3 + 1·1]] = −[3, −2, 1] = [−3, 2, −1]`.

$$T^{-1} = \begin{bmatrix} 0 & 1 & 0 & -3 \\ -1 & 0 & 0 & 2 \\ 0 & 0 & 1 & -1 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

검증: `T T⁻¹ = I`. (직접 곱해보면 4×4 identity).

</details>

---

### Q7. 로그 ω̂, θ 계산

회전 행렬

$$R = \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$$

에 대해 `θ` 와 `ω̂` 를 구하라.

<details><summary>답</summary>

`tr R = 0 + 0 + 0 = 0`.

`cos θ = (tr R − 1)/2 = −1/2` → `θ = 2π/3`.

`[ω̂] = (R − Rᵀ)/(2 sin θ)`.

`Rᵀ = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]`.

`R − Rᵀ = [[0, −1, 1], [1, 0, −1], [−1, 1, 0]]`.

`sin θ = sin(2π/3) = √3/2`, `2 sin θ = √3`.

`[ω̂] = (1/√3) · [[0, −1, 1], [1, 0, −1], [−1, 1, 0]]`.

이로부터 `ω̂ = (1/√3) (1, 1, 1)`.

검증: `‖ω̂‖ = √(1/3 + 1/3 + 1/3) = 1`. ✓

</details>

---

### Q8. Screw axis 계산

평면에서 점 `q = (2, 0, 0)` 을 지나고 `z` 축 방향, pitch `h = 1` 인 screw 의 6-vector `S` 를 적어라.

<details><summary>답</summary>

`ω̂ = (0, 0, 1)`. `q = (2, 0, 0)`. `h = 1`.

`v = −ω̂ × q + h · ω̂`.

`ω̂ × q = (0, 0, 1) × (2, 0, 0) = (0·0 − 1·0, 1·2 − 0·0, 0·0 − 0·2) = (0, 2, 0)`.

`−ω̂ × q = (0, −2, 0)`.

`h · ω̂ = (0, 0, 1)`.

`v = (0, −2, 1)`.

`S = (ω̂, v) = (0, 0, 1, 0, −2, 1)`.

</details>

---

### Q9. Adjoint 행렬

`T = (R, p)` 에서 `R = I`, `p = (1, 2, 3)` 일 때 `[Ad_T]` 를 적어라.

<details><summary>답</summary>

`[p] = [[0, −3, 2], [3, 0, −1], [−2, 1, 0]]`.

`[p] R = [p]` (R = I).

$$[Ad_T] = \begin{bmatrix} I & 0 \\ [p] & I \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & -3 & 2 & 1 & 0 & 0 \\ 3 & 0 & -1 & 0 & 1 & 0 \\ -2 & 1 & 0 & 0 & 0 & 1 \end{bmatrix}$$

순수 병진 (회전 없음) 의 adjoint — angular 성분은 그대로, linear 성분은 `[p]ω` 만큼 보정.

</details>

---

## 디버그

### Q10. T 의 역원 잘못

다음 코드의 *버그* 를 찾아라.

```python
def inverse_transform(T):
    R = T[:3, :3]
    p = T[:3, 3]
    T_inv = np.zeros((4, 4))
    T_inv[:3, :3] = R.T
    T_inv[:3, 3] = -p          # ← 여기 의심
    T_inv[3, 3] = 1
    return T_inv
```

<details><summary>답</summary>

`T_inv[:3, 3] = -p` 가 *잘못*. 올바른 식은 `-R.T @ p`.

`T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]` 이므로 `p_inv = −Rᵀ p`. 단순 `−p` 가 아님.

수정:
```python
T_inv[:3, 3] = -R.T @ p
```

검증: `T T_inv` 가 identity 가 나오는지. 버그 있으면 안 나옴.

</details>

---

### Q11. ω 정규화 누락

다음 코드의 *버그* 를 찾아라.

```python
def rotation_from_axis_angle(omega, theta):
    # omega: 3-vector (회전축), theta: 회전 각도
    omega_hat = skew(omega)
    R = np.eye(3) + np.sin(theta) * omega_hat + (1 - np.cos(theta)) * omega_hat @ omega_hat
    return R
```

<details><summary>답</summary>

`omega` 가 *unit vector* 가 아닐 수 있음. Rodrigues' formula 는 `[ω̂]` (unit) 기준. 만약 `‖ω‖ = 2` 면 결과 회전이 잘못된 각도로 나옴.

수정:
```python
norm = np.linalg.norm(omega)
if norm > 1e-9:
    omega_hat = skew(omega / norm)
else:
    return np.eye(3)  # 회전 없음
```

또는 호출자에게 *반드시 unit vector* 요구하는 contract 로 처리.

</details>

---

### Q12. 회전 합성 순서

"frame {b} 를 frame {s} 에서 본 자세 `R_sb` 가 있다. 추가로 body frame 기준으로 `R_local` 만큼 회전했을 때 새 자세는?" 라는 질문에 *오답* `R_new = R_local R_sb` 를 적는다. 정답은?

<details><summary>답</summary>

정답: `R_new = R_sb R_local`.

이유: *body-fixed rotation* (body frame 기준) 은 오른쪽 곱셈. *space-fixed rotation* (space frame 기준) 은 왼쪽 곱셈.

규칙:
- "body frame 기준으로 회전" → 오른쪽 (post-multiply): `R_new = R_old R_local`
- "space frame 기준으로 회전" → 왼쪽 (pre-multiply): `R_new = R_global R_old`

이 둘 헷갈리는 게 *5장 Jacobian 의 spatial vs body* 혼동 의 뿌리.

</details>

---

## 면접

### Q13. SO(3) 가 비가환임을 직관으로

회전이 *비가환* 임을 손 동작으로 어떻게 직관적으로 보일 수 있나?

<details><summary>답</summary>

책을 손에 들고:
1. 먼저 *x 축* 으로 90° 회전 → 다음 *z 축* 으로 90° 회전
2. *(처음으로 돌리기)* 다시 책을 잡고, *z 축* 으로 90° → *x 축* 으로 90°

두 결과의 책 방향이 *다름*. SO(3) 가 비가환임의 직관적 증거.

수학적: `Rot(x̂, π/2) Rot(ẑ, π/2) ≠ Rot(ẑ, π/2) Rot(x̂, π/2)`. 직접 행렬 곱으로 확인 가능.

이 비가환성이 *오일러 각* 표현에 ambiguity (회전 순서를 별도 지정해야 함) 와 *gimbal lock* 을 만든다. 또한 angular velocity 가 *Lie algebra* (덧셈 합성) 인 이유.

</details>

---

### Q14. PoE formula 의 동기

다음 장의 *PoE formula* (Product of Exponentials) 는 robot 의 forward kinematics 를 어떻게 표현하나? Ch 3 의 어떤 결과가 직접 적용되나?

<details><summary>답</summary>

**PoE formula** (n-joint robot):

$$T(\theta) = e^{[\mathcal{S}_1] \theta_1} e^{[\mathcal{S}_2] \theta_2} \cdots e^{[\mathcal{S}_n] \theta_n} M$$

- `M`: zero-position end-effector pose (모든 joint 가 0 일 때)
- `S_i`: i-번째 joint 의 *zero-position screw axis*, space frame {s} 에서 표현
- `θ_i`: i-번째 joint 변수

Ch 3 의 직접 적용:
- 각 항 `e^{[S_i]θ_i}` 가 *SE(3) 의 지수 좌표* (§7.3)
- 각 `S_i` 가 *screw axis* (§7.2)
- 항들의 곱이 *SE(3) 의 군 연산* (§5.3)

장점 (DH parameter 대비):
- 좌표계 부여 *덜 임의적* — base frame {s} 하나만 정하면 됨
- 기하적 의미 명확 — 각 항이 *축과 pitch* 라는 물리 객체
- Jacobian 도출이 자연스러움

이 패턴이 4장 전체의 핵심.

</details>
