# Ch 4 Forward Kinematics — 퀴즈

> 12 문항 (개념 3 / 계산 4 / 디버그 3 / 면접 2).

---

## 개념

### Q1. PoE 의 *전체* 의미

PoE formula `T(θ) = e^{[S₁]θ₁} ⋯ e^{[Sₙ]θₙ} M` 에서 각 기호의 의미를 한 줄씩 적어라.

<details><summary>답</summary>

- `T(θ)`: end-effector frame `{b}` 가 base frame `{s}` 에 대해 가지는 자세, joint 값 `θ` 의 함수
- `M`: zero position (모든 `θ_i = 0`) 에서의 `T_{sb}`
- `S_i ∈ R⁶`: i 번째 joint 의 zero-position screw axis, `{s}` 에서 표현
- `θ_i`: i 번째 joint 변수 (회전 각 또는 병진 거리)
- `e^{[S_i]θ_i} ∈ SE(3)`: i 번째 joint 가 활성화될 때 *그 바깥의* 모든 link 가 받는 강체변환

</details>

---

### Q2. Space form vs Body form

`S_i` (Space) 와 `B_i` (Body) 의 관계식과, *어떤 frame 의 분해* 인가를 설명.

<details><summary>답</summary>

관계: `B_i = [Ad_{M⁻¹}] S_i`.

- `S_i`: zero-position screw axis 를 **{s}** (space frame) 에서 표현
- `B_i`: 같은 joint 의 zero-position screw axis 를 **{b}** (body frame) 에서 표현

`M = T_{sb}(0)` 이므로 `M⁻¹ = T_{bs}(0)` — body frame 에서 본 space frame. `[Ad_{M⁻¹}]` 가 `{s}` → `{b}` 의 twist 변환.

</details>

---

### Q3. PoE vs DH — 본질적 차이

DH 의 *어떤 점* 이 PoE 에서 사라지는가?

<details><summary>답</summary>

DH 의 가장 큰 *부담*: **각 link 에 별도 frame 을 부여** 해야 함 — 또한 그 frame 의 placement 가 임의 (classical vs modified DH convention).

PoE 에서 사라지는 것:
- 중간 link 의 frame placement 의 임의성
- 각 frame 의 `α, a, d, θ` 산출 (특히 비-perpendicular 회전축 케이스의 까다로움)
- prismatic vs revolute 의 서로 다른 표기

남는 것: `{s}`, `{b}` 두 frame 만. 모든 정보는 *zero position* 의 `M` 과 `S_i`.

</details>

---

## 계산

### Q4. 3R planar arm 의 FK (분석적)

3R planar arm: 모든 회전 축이 `ẑ`, link 길이 `L₁ = L₂ = L₃ = 1`. zero position 에서 EE 의 위치는 `(3, 0, 0)`. EE 의 zero-position pose `M` 을 적어라.

<details><summary>답</summary>

zero position 에서:
- 회전 = 단위행렬 (모든 link 가 x 축 방향)
- 병진 = `(L₁ + L₂ + L₃, 0, 0) = (3, 0, 0)`

$$M = \begin{bmatrix} 1 & 0 & 0 & 3 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

</details>

---

### Q5. 3R planar arm 의 screw axes

같은 3R planar arm. 회전축이 모두 `ẑ` 방향이고, zero position 에서 joint 들의 위치가:
- joint 1: `(0, 0, 0)`
- joint 2: `(1, 0, 0)`
- joint 3: `(2, 0, 0)`

각 `S_i = (ω, v)` 를 적어라.

<details><summary>답</summary>

모두 `ẑ` 축 회전 → `ω_i = (0, 0, 1)`.

`v_i = −ω̂ × q_i`:

- `S₁`: `q = (0, 0, 0)`, `v = −(0,0,1)×(0,0,0) = (0, 0, 0)` → `S₁ = (0, 0, 1, 0, 0, 0)`
- `S₂`: `q = (1, 0, 0)`, `v = −(0,0,1)×(1,0,0) = −(0, 1, 0) = (0, −1, 0)` → `S₂ = (0, 0, 1, 0, −1, 0)`
- `S₃`: `q = (2, 0, 0)`, `v = (0, −2, 0)` → `S₃ = (0, 0, 1, 0, −2, 0)`

</details>

---

### Q6. `e^{[S]θ}` 의 결과 형태

위 `S₂ = (0, 0, 1, 0, −1, 0)` 에 대해 `e^{[S₂]θ}` 의 형태 (SE(3) 행렬) 을 적어라.

<details><summary>답</summary>

`ω = (0, 0, 1)`, `v = (0, −1, 0)`. 회전 부분: `e^{[ω]θ} = Rot(ẑ, θ)`.

병진 부분 `G(θ) v` 에서 `[ω] = [[0,−1,0],[1,0,0],[0,0,0]]`, `[ω]² = [[−1,0,0],[0,−1,0],[0,0,0]]`.

`G(θ) = Iθ + (1−cos θ)[ω] + (θ−sin θ)[ω]²`.

`G(θ) v = θ(0,−1,0) + (1−cos θ)(1, 0, 0) + (θ−sin θ)(0, 1, 0)`
      = `(1−cos θ, −θ + θ − sin θ, 0)`
      = `(1−cos θ, −sin θ, 0)`.

$$e^{[\mathcal{S}_2]\theta} = \begin{bmatrix} \cos\theta & -\sin\theta & 0 & 1-\cos\theta \\ \sin\theta & \cos\theta & 0 & -\sin\theta \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

검증: `θ = 0` → identity. ✓

</details>

---

### Q7. Body form 의 `B_i`

위 3R planar arm 에서 `B₁` 을 구해라 (Space form `S₁ = (0, 0, 1, 0, 0, 0)` 에서).

<details><summary>답</summary>

`M = [I, (3,0,0); 0, 1]`. `M⁻¹ = [I, (−3, 0, 0); 0, 1]`.

`[Ad_{M⁻¹}] = [I, 0; [(−3,0,0)]I, I]`. `[(−3,0,0)] = [[0,0,0],[0,0,3],[0,−3,0]]`.

`B₁ = [Ad_{M⁻¹}] S₁ = [Ad_{M⁻¹}] (0, 0, 1, 0, 0, 0)`.

ω 부분: `R · ω = I · (0,0,1) = (0,0,1)`.

v 부분: `[(−3,0,0)] I · (0,0,1) + I · (0,0,0) = [(−3,0,0)](0,0,1) = (0·0 + 0·1, 0·0 + 3·1, 0·0 + (−3)·0) = (0, 3, 0)`.

따라서 `B₁ = (0, 0, 1, 0, 3, 0)`.

해석: body frame {b} (zero position 에서 (3,0,0) 에 위치) 기준으로, joint 1 의 축은 +ẑ, axis 위 점 `q_b = −(3, 0, 0)` 에 해당. `v = −ω̂ × q_b = −(0,0,1)×(−3,0,0) = −(0,−3,0) = (0,3,0)`. ✓

</details>

---

## 디버그

### Q8. screw axis 순서 잘못

다음 코드의 *버그* 를 찾아라.

```python
def fk_space(S_list, M, theta_list):
    T = M.copy()
    for S, theta in zip(S_list, theta_list):
        T = expm(skew_se3(S * theta)) @ T
    return T
```

<details><summary>답</summary>

순서가 *역방향*. PoE space form 은 `e^{[S₁]θ₁} ⋯ e^{[Sₙ]θₙ} M` 이라 `S₁` 이 *가장 왼쪽*. 위 코드는 `S_n` 부터 안에서 곱하므로 결과가 `e^{[Sₙ]θₙ} ⋯ e^{[S₁]θ₁} M` 이 됨 — 잘못된 누적.

수정 (역방향 iteration):
```python
def fk_space(S_list, M, theta_list):
    T = M.copy()
    for S, theta in zip(reversed(S_list), reversed(theta_list)):
        T = expm(skew_se3(S * theta)) @ T
    return T
```

또는 forward iteration 에서 *오른쪽* 곱:
```python
T = np.eye(4)
for S, theta in zip(S_list, theta_list):
    T = T @ expm(skew_se3(S * theta))
return T @ M
```

</details>

---

### Q9. Body form 의 `M` 곱셈 위치

다음의 *버그* 를 찾아라.

```python
def fk_body(B_list, M, theta_list):
    T = np.eye(4)
    for B, theta in zip(B_list, theta_list):
        T = T @ expm(skew_se3(B * theta))
    return M @ T   # ← 의심
```

<details><summary>답</summary>

Body form: `T(θ) = M e^{[B₁]θ₁} ⋯ e^{[Bₙ]θₙ}` — `M` 이 *왼쪽*, 위 코드도 그렇게 함. 사실 정답!

다만 *주의*: B 의 순서. body form 은 `B₁` 부터 *왼쪽에서 오른쪽* 으로 곱. forward iteration 에서 `T = T @ exp(B_i θ_i)` 면 OK.

→ 사실 버그 없음. 만약 *Space form 처럼 reversed 로 iter* 했다면 그게 버그.

검증 팁: zero `θ = 0` 일 때 `T = M` 인지 확인.

</details>

---

### Q10. URDF axis frame 혼동

URDF 의 `<joint axis="0 0 1"/>` 를 *그대로* `S_i = (0, 0, 1, ...)` 로 사용하는 코드가 작동 안 한다. 이유?

<details><summary>답</summary>

URDF 의 `axis` 는 *parent link frame 기준*. PoE 의 `S_i` 는 *space frame {s} 기준*. 두 frame 이 *같지 않음*.

올바른 처리:
1. URDF 파싱 시 각 joint 의 *parent link frame* 을 누적해서 *base ({s}) frame* 까지 가져감
2. `joint.axis` 와 `joint.origin` 을 그 누적 변환으로 `{s}` 로 변환
3. 그 결과를 `S_i = (ω, v)` 의 ω 와 q 로 사용

대안: 각 joint 의 *현재 frame* 에서 axis 를 *Body form* 의 `B_i` 로 직접 매핑하는 방법도 있음 (책 §4.1.3).

자동화 라이브러리: `pinocchio`, `RBDL`, MR Python 라이브러리.

</details>

---

## 면접

### Q11. Why PoE?

면접관 — "왜 DH 대신 PoE 를 쓰나?" 한 분 이내로 답하라.

<details><summary>답</summary>

PoE 는 *frame 부여의 임의성을 제거* 합니다. DH 는 각 link 에 frame 을 부여해야 하고, classical / modified convention 차이가 생깁니다. PoE 는 `{s}`, `{b}` 두 frame 만 잡고, 각 joint 의 *공간상 실제 screw axis* 로 표현해서 기하적 직관이 명확합니다. 또한 prismatic / revolute joint 가 동일 framework 로 다뤄지고, 5장 Jacobian 도출이 자연스럽고, 6장 IK 의 body-frame iteration 도 잘 맞습니다. URDF parsing 시 부담이 늘긴 하나, 한 번 `S_i` 와 `M` 만 잡으면 나머지 장 전체가 *기계적* 으로 풀립니다.

</details>

---

### Q12. PoE 의 *한계*

PoE 가 *못하는 것* 또는 *불편한 점* 은?

<details><summary>답</summary>

1. **Closed-chain robot** (parallel manipulator, 7장 주제) — PoE 는 open-chain 가정. closed-chain 에선 loop closure constraint 가 별도 필요.
2. **Soft / continuum robot** — 이산 joint 가 아니라 연속 변형이면 PoE 직접 적용 안 됨.
3. **수치 안정성** — long chain 에서 `e^{[S_i]θ_i}` 의 누적 시 SE(3) 의 SO(3) constraint (`RᵀR = I`) 위반 가능. Re-orthogonalize 필요.
4. **파라미터 수** — DH 의 4n 보다 약간 많음 (6n + 6). 메모리 보다는 표현의 명료성 trade-off.
5. **standardization** — URDF 가 *DH 친화적이지 않은* 형태. PoE 와 URDF 의 매핑이 명시적 코드 필요.

</details>
