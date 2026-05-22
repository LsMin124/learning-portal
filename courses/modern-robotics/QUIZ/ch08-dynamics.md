# Ch 8 Dynamics — 퀴즈

> 14 문항 (개념 4 / 계산 4 / 디버그 3 / 면접 3).

## 개념

### Q1. Manipulator equation 의 각 항

`τ = M(θ) θ̈ + c(θ, θ̇) + g(θ) + Jᵀ F_tip` 의 각 항이 *물리적으로* 무엇을 표현하나?

<details><summary>답</summary>

- `M(θ) θ̈`: configuration-dependent inertia × angular acceleration. *순수 가속에 필요한 토크*.
- `c(θ, θ̇)`: Coriolis + centrifugal. *velocity 가 만드는 fictitious force* (좌표계 비-관성).
- `g(θ)`: gravity 토크. *중력 보상* (static).
- `Jᵀ F_tip`: 외부 wrench `F_tip` 이 joint 에 만드는 reaction torque.

</details>

### Q2. Mass matrix 의 성질

`M(θ)` 의 두 핵심 수학 성질과 그 *물리적* 의미.

<details><summary>답</summary>

1. **Symmetric** (`M = Mᵀ`) — Lagrangian 의 mixed partial derivatives 가 같음 (`∂²L/∂θ̇_i ∂θ̇_j = ∂²L/∂θ̇_j ∂θ̇_i`).
2. **Positive-definite** (`xᵀ M x > 0` for `x ≠ 0`) — Kinetic energy `T = ½ θ̇ᵀ M θ̇` 가 *항상 양수* (정지 상태 제외).

이 둘이 *invertible* 보장 → forward dynamics 풀이 가능.

</details>

### Q3. Passivity property

`Ṁ − 2C` 가 skew-symmetric 인 이유와 의미.

<details><summary>답</summary>

Christoffel-symbol 기반 `C` 를 쓸 때 성립. 의미:

`d/dt(½ θ̇ᵀ M θ̇) = θ̇ᵀ M θ̈ + ½ θ̇ᵀ Ṁ θ̇`

`τ = M θ̈ + C θ̇ + g` 에서 `M θ̈` 를 대입:

`Ṫ = θ̇ᵀ (τ − C θ̇ − g) + ½ θ̇ᵀ Ṁ θ̇ = θ̇ᵀ τ + θ̇ᵀ (½ Ṁ − C) θ̇ − θ̇ᵀ g`

만약 `Ṁ − 2C` skew → `θ̇ᵀ (½Ṁ − C) θ̇ = 0` → `Ṫ = θ̇ᵀ τ − θ̇ᵀ g`. 즉 *외부 input 없으면 energy 보존*. 이게 **passivity** — 11장 stable adaptive control 의 기반.

</details>

### Q4. Newton-Euler vs Lagrangian

두 formulation 의 *trade-off*.

<details><summary>답</summary>

| | Lagrangian | Newton-Euler |
|--|--|--|
| 분석성 | 명시적 식 | recursive (식 안 보임) |
| 효율 | O(n²)~O(n³) symbolic | O(n) numeric |
| Real-time | 어렵 | 가능 (1kHz+) |
| 학습용 | 통찰적 | 알고리즘적 |
| 응용 | 이론, 작은 robot, derivation | 실용 control / simulation |

산업 코드 (MuJoCo, Drake, pinocchio) 모두 Newton-Euler 기반. 분석은 Lagrangian.

</details>

## 계산

### Q5. 2R arm gravity 토크

2R planar arm, `m₁ = m₂ = m`, `L₁ = L₂ = L`, vertical gravity `g`. `θ_1, θ_2` 에서 `g(θ)` 직접.

<details><summary>답</summary>

`V(θ) = m g L sin θ_1 + m g (L sin θ_1 + L sin(θ_1 + θ_2)) = m g L (2 sin θ_1 + sin(θ_1 + θ_2))`.

`g_1(θ) = ∂V/∂θ_1 = m g L (2 cos θ_1 + cos(θ_1 + θ_2))`.
`g_2(θ) = ∂V/∂θ_2 = m g L cos(θ_1 + θ_2)`.

검증:
- `θ_1 = θ_2 = 0` (팔 수평): `g(0) = (3 m g L, m g L)` — 큰 gravity 토크 (가장 *팔이 펼친* configuration).
- `θ_1 = π/2` (팔 수직 위): `cos(π/2) = 0` → 두 항 모두 0. 직관 일치 (수직이면 gravity 의 모멘트 없음).

</details>

### Q6. Mass matrix 행렬식

2R arm 의 `M(θ)` 행렬식.

<details><summary>답</summary>

`M_{11} = m₁L₁² + m₂(L₁² + 2 L₁L₂ cos θ_2 + L₂²)`
`M_{12} = M_{21} = m₂(L₁L₂ cos θ_2 + L₂²)`
`M_{22} = m₂ L₂²`

`det M = M_{11} M_{22} − M_{12}²`

`= [m₁L₁² + m₂(L₁² + 2L₁L₂ cos θ_2 + L₂²)] · m₂L₂² − [m₂(L₁L₂ cos θ_2 + L₂²)]²`

`= m₂L₂² [m₁L₁² + m₂L₁² − m₂ L₁² cos² θ_2 ... 정리하면]`

`= m₁ m₂ L₁² L₂² + m₂² L₁² L₂² sin² θ_2`

`= m₂ L₁² L₂² (m₁ + m₂ sin² θ_2) > 0`. ✓ (`M` SPD 검증)

특히 `θ_2 = 0` (singular kinematics) 에서도 `det M = m₁ m₂ L₁² L₂² > 0` — **dynamics 의 inertia 는 kinematics singular 와 무관**.

</details>

### Q7. Spatial inertia 변환

`{a}` frame 의 spatial inertia `G_a` 가 주어졌을 때 `{b}` frame 에서.

<details><summary>답</summary>

$$\mathcal{G}_b = [Ad_{T_{ab}}]^T \mathcal{G}_a [Ad_{T_{ab}}]$$

bilinear 변환. wrench 변환 `F_b = [Ad_{T_{ab}}]ᵀ F_a` 와 *형태 동일*.

</details>

### Q8. Forward dynamics 한 step

`M(θ) = [[2, 0.5], [0.5, 1]]`, `c + g = (0.1, 0.2)`, `τ = (1, 0)`. `θ̈` 는?

<details><summary>답</summary>

`τ − c − g = (0.9, −0.2)`.

`M⁻¹`: `det M = 2 − 0.25 = 1.75`. `M⁻¹ = (1/1.75) [[1, −0.5], [−0.5, 2]] = [[0.571, −0.286], [−0.286, 1.143]]`.

`θ̈ = M⁻¹ (τ − c − g) = [[0.571·0.9 + (−0.286)·(−0.2)], [(−0.286)·0.9 + 1.143·(−0.2)]] = [0.514 + 0.057, −0.257 − 0.229] = (0.571, −0.486)`.

</details>

## 디버그

### Q9. Coriolis 부호 실수

```python
def coriolis(theta, theta_dot, M_func):
    M = M_func(theta)
    dM = compute_jacobian_M(theta, M_func)   # ∂M/∂θ
    C = 0.5 * (dM + dM.transpose((0, 2, 1)) + dM.transpose((1, 2, 0)))   # ← 의심
    return C @ theta_dot
```

부호 어디 잘못?

<details><summary>답</summary>

Christoffel symbol: `Γ_{ijk} = ½(∂m_{ij}/∂θ_k + ∂m_{ik}/∂θ_j − ∂m_{jk}/∂θ_i)`.

세 번째 항이 **마이너스**. 위 코드에서 세 번째 transpose 가 *플러스* — 잘못.

수정: `C = 0.5 * (dM + dM.transpose((0, 2, 1)) - dM.transpose((1, 2, 0)))`.

(인덱스 매핑은 `dM[i,j,k] = ∂m_{ij}/∂θ_k` 가정.)

</details>

### Q10. Gravity 처리 누락

Newton-Euler 코드에서 `V̇_0 = (0, 0, 0, 0, 0, 0)` (zero base accel) 으로 init 하니 gravity 항이 사라짐. 어떻게 수정?

<details><summary>답</summary>

표준 트릭: base 의 acceleration 을 *gravity 의 반대 방향* 으로 *가짜 init*:

```
g_vec = (0, 0, 0, 0, 0, 9.81)  # +z gravity 일 때
V̇_0 = g_vec
```

이러면 *base 가 위로 가속* 하는 *비-관성계* 가 되고, 그 안에서 보면 모든 link 가 *아래 방향 fictitious force* 를 받음 — 정확히 gravity 와 같은 효과. Newton-Euler 알고리즘 안 바꾸고 gravity 자동 처리.

</details>

### Q11. M⁻¹ 의 비용

7-DoF arm 의 simulator 가 1kHz 에서 작동 안 함. `M⁻¹` 계산이 bottleneck. 해결.

<details><summary>답</summary>

`M⁻¹` 직접 = `O(n³)` = 343 floating-point ops for n=7. 1kHz × 7-DoF arm 에 borderline. 

**Articulated-Body Algorithm (ABA)** 사용 — Featherstone 의 spatial vector 기반 `O(n)` forward dynamics. naïve `(τ − c − g) → M⁻¹` 안 거치고 직접 `θ̈` 계산.

또는 `M` 의 *Cholesky factorization* 캐시 + 한 step 안에서 재사용 (`M` 이 SPD). `θ̈ = M⁻¹ (τ − c − g)` 를 `solve(L, ...)` 두 번 (앞·뒤 substitution) 으로 처리.

pinocchio, RBDL 등 라이브러리 사용 권장.

</details>

## 면접

### Q12. Computed-torque control

`τ = M(θ) θ̈_d + c(θ, θ̇) + g(θ)` 의 *물리적 의미* 와 *실용적 한계*.

<details><summary>답</summary>

**의미**: 원하는 가속도 `θ̈_d` 를 *완벽한 모델* 로 정확히 만드는 *feed-forward* 토크. 모델이 perfect 면 `θ̈ = θ̈_d` 가 성립.

**한계**:
1. **Model error** — 실제 `M, c, g` 는 nominal 값과 다름 (mass 부정확, friction 무시 등). → tracking error 발생. → **feedback term 필수** (PD: `+ K_p(θ_d − θ) + K_d(θ̇_d − θ̇)`).
2. **계산 비용** — full inverse dynamics 매 step 1kHz 가능해야. (Newton-Euler O(n) 필요.)
3. **Joint flexibility / harmonic drive** — 실제 robot 의 *모터 ↔ link* 사이 *탄성·gear backlash* 가 manipulator equation 안 들어감.
4. **Saturation** — `τ_max` 초과 시 desired `θ̈_d` 추적 불가.

실용: feed-forward (model-based `τ_ff`) + feedback (PID, robust) 조합이 표준 (11장).

</details>

### Q13. Why robotics 의 Newton-Euler 가 *classical mechanics 의 Newton-Euler 와 다른가*?

<details><summary>답</summary>

**Classical** (Goldstein 등): 각 강체별 `F = ma`, `τ = I α` 별도. 다체계 (multi-body) 시 constraint force 직접 (분리).

**Robotics Recursive Newton-Euler** (Luh-Walker-Paul 1980):
1. **6D 형태**: `F_b = G_b V̇_b − [ad_V]ᵀ G_b V_b` (force + torque + linear + angular 통합)
2. **Recursive**: parent → child → end (forward), end → parent → base (backward)
3. **Constraint 자동**: joint 가 *constraint force 를 transmit* 하므로 별도 풀이 불필요
4. **O(n)** efficient — *symbolic 폭증 회피*

이게 *현대 robotics simulation* 의 표준. Drake / MuJoCo / pinocchio / RBDL 모두 이 형태.

</details>

### Q14. Robot dynamics 의 *최신* 동향

Modern Robotics (2017) 이후 발전.

<details><summary>답</summary>

1. **Differentiable simulators** — PyTorch / JAX 으로 `θ̈ = f(θ, θ̇, τ)` 의 *gradient* 계산. RL·MPC·trajectory optimization 에 활용. (Brax, MJX, Tiny Differentiable Simulator)
2. **GPU-parallel simulation** — Isaac Gym, MuJoCo MJX — 수천 robot 동시 simulation 으로 RL 학습 속도 ↑.
3. **Soft robots / continuum** — 무한 차원 dynamics. PDE-based. PoE 의 *함수 valued* 확장.
4. **Contact-rich dynamics** — *implicit time integration*, *complementarity* 기반 grasping / locomotion.
5. **Learning-based dynamics** — neural network 으로 residual model 학습 (실제 robot 의 friction·flex 등 모델링 어려운 부분).
6. **Body schema for humanoids** — 50+ DoF, articulated body algorithm 의 generalized 확장.

8장의 *고전적 framework* 위에 이 모두가 쌓임.

</details>
