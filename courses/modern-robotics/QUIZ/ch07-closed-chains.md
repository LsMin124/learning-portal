# Ch 7 Kinematics of Closed Chains — 퀴즈

> 10 문항.

### Q1. Open vs Closed FK/IK

각각의 *어려움 방향* 이 반대인 이유.

<details><summary>답</summary>

**Open chain**:
- FK = `θ → T`, PoE 의 *forward 곱* — closed-form, 1 해.
- IK = `T → θ`, 비선형, 다해 (PUMA 8-해), numerical.

**Closed chain**:
- IK = `T_EE → joint values`, 각 leg 독립으로 IK 풀이 가능 — closed-form, 일반적으로 쉬움.
- FK = `actuated joint → T_EE`, 각 leg 의 *동일 EE pose 산출* loop closure 만족 — *implicit equations* → 수치해법, 다해 (Stewart-Gough 40 해).

이게 *parallel robot 의 산업 응용* 이 잘 작동하는 이유 — *desired EE → joint command* 가 빠르고 closed-form.

</details>

### Q2. Stewart-Gough DoF 계산

6-UPS Stewart-Gough 의 Grübler 계산.

<details><summary>답</summary>

`N = 14` (base + top + 다리당 2 link × 6 = 12). `J = 18` (다리당 3 joint × 6).

각 다리 joint DoF: U(2) + P(1) + S(3) = 6. 6 다리 → Σ f_i = 36.

`DoF = m(N − 1 − J) + Σ f_i = 6(14 − 1 − 18) + 36 = 6 × (−5) + 36 = −30 + 36 = 6`.

→ 6 DoF (위치 3 + 자세 3). prismatic 6 개 actuator 로 모두 제어.

</details>

### Q3. Delta robot 의 3 DoF translation

3 leg 평행구조가 *왜* orientation 변화를 막는가?

<details><summary>답</summary>

Delta 의 각 leg = **parallelogram linkage**. 두 끝의 link 가 *항상 평행* 유지.

→ end-effector plate 가 base plate 와 *항상 평행*. orientation 고정, translation 3 DoF 만.

이게 *높은 속도 + 정확도* 의 비밀 — orientation 신경 안 쓰니 dynamics 단순. pick-and-place 같은 *XYZ 만 필요한* 작업에 최적.

응용: chocolate packaging, electronics assembly, food handling.

</details>

### Q4. 5-bar inverse kinematics

5-bar linkage, link 길이 `L₁ = L₂ = L₃ = L₄ = L₅ = 1`. EE 가 `(x, y)`. 좌측 actuator 각 `θ_1` 의 IK.

<details><summary>답</summary>

5-bar 의 *좌측 leg* (joint 1, link 1, link 2) 만 보면 2-link planar arm.

EE 의 거리 `D = √(x² + y²)`. 단 이건 *base origin* 부터의 거리.

좌측 sub-chain 의 elbow 각도:
`cos(θ_2) = (D² − L₁² − L₂²) / (2 L₁ L₂)` (law of cosines).

좌측 actuator: `θ_1 = atan2(y, x) ± atan2(L₂ sin θ_2, L₁ + L₂ cos θ_2)` (± = elbow up/down).

마찬가지로 우측 sub-chain 으로 `θ_3` (우측 actuator) IK. 우측 base origin offset 고려.

→ 각 leg *독립* IK — closed-chain IK 의 *easiness* 의 좋은 예.

</details>

### Q5. Loop closure constraint 예제

5-bar 에서 *loop closure* 식 1 개.

<details><summary>답</summary>

5-bar: 두 sub-chain 의 *공통 EE* 가 같은 좌표여야.

`x_left(θ_1, θ_2) = x_right(θ_3, θ_4)`
`y_left(θ_1, θ_2) = y_right(θ_3, θ_4)`

수식:
- `L₁ cos θ_1 + L₂ cos(θ_1 + θ_2) = d + L₃ cos θ_3 + L₄ cos(θ_3 + θ_4)`
- `L₁ sin θ_1 + L₂ sin(θ_1 + θ_2) = L₃ sin θ_3 + L₄ sin(θ_3 + θ_4)`

(d = 두 base joint 사이 거리.)

→ 2 식 = loop closure. 4 joint variables 에서 2 자유도 (DoF) 만 independent.

</details>

### Q6. Type 1 vs Type 2 singularity

5-bar 의 두 가지 singularity 예시.

<details><summary>답</summary>

**Type 1 (actuator)**: 두 actuator (`θ_1, θ_3`) 가 motion 만들어도 EE 가 *정지*.

예: 양쪽 link 2, link 4 가 *세로로 늘어선* configuration. actuator 가 motion 만들어도 EE 의 *수직 motion* 못 만듦 (link 의 모멘트 zero).

**Type 2 (configuration)**: actuator *fixed* 인데 EE 가 *self-motion*.

예: 두 EE link 가 *모두 수직 line 위*. actuator 가 고정해도 *EE 가 좌우 작은 motion* 가능 — *uncontrolled DoF*. *payload 떨어질 위험*.

산업 design: 두 singular configuration 모두 workspace 안에서 회피.

</details>

### Q7. Constraint Jacobian rank

5-bar 의 *normal* configuration 에서 constraint Jacobian `A(θ)` 의 차원과 rank.

<details><summary>답</summary>

4 joint variables, 2 loop closure constraints → `A(θ) ∈ R^{2×4}`.

Normal (non-singular) configuration: `rank A = 2` (full row rank).

`A θ̇ = 0` 의 null space = 4 − 2 = **2-dim** → 2 actuated joint 로 모든 motion 결정 가능 (DoF = 2).

singular configuration 에서 `rank A < 2` → null space ↑ → uncontrolled DoF 발생.

</details>

### Q8. Stewart-Gough IK

Stewart-Gough 의 EE pose `T = (R, p) ∈ SE(3)`. i-번째 leg 의 length `L_i` 계산.

<details><summary>답</summary>

각 leg 의 *base attachment point* `b_i` (base frame), *top attachment point* `t_i` (platform frame, body).

`L_i = ‖p + R t_i − b_i‖` (Euclidean distance).

즉 platform pose 가 정해지면 모든 leg length 즉시 계산 — **6 leg, 6 closed-form 계산**. real-time 1kHz 가능.

→ Stewart-Gough 의 산업 적용 가능 이유.

</details>

### Q9. Quadruped 의 closed chain

4-leg robot (Spot, Anymal) 이 *trotting* 시 닮은 *closed chain* 상태.

<details><summary>답</summary>

**Stance phase** (3-leg ground contact, 1-leg swing):
- 3 stance leg + body + 지면 → *closed loop*
- 각 stance foot 가 *spherical joint with ground* 같이 작용 (no-slip 가정)
- *Loop closure*: 3 stance foot 의 *지면 위치 고정* — implicit constraint
- DoF: body 6 DoF (`SE(3)`) — *어떻게 움직일 수 있나* 가 stance constraint 로 제한

**Swing phase**: swing leg 는 open chain.

Mixed control:
- stance leg: *closed-chain inverse kinematics* (body motion → joint torque)
- swing leg: *open-chain trajectory* (foot reposition)

이게 *whole-body MPC* (Boston Dynamics, ETH Anymal) 의 핵심 framework.

</details>

### Q10. Closed-chain FK numeric 알고리즘

Stewart-Gough 의 actuated leg lengths `L = (L_1, ..., L_6)` 에서 EE pose `T` 를 구하는 Newton-Raphson.

<details><summary>답</summary>

```python
def closed_chain_fk(L_target, T_init, robot, max_iter=20, tol=1e-6):
    """
    Stewart-Gough FK via Newton-Raphson.
    Input: target leg lengths L_target (6,), initial guess T_init ∈ SE(3).
    Output: T ∈ SE(3) such that IK(T) ≈ L_target.
    """
    T = T_init
    for _ in range(max_iter):
        L_current = stewart_ik(T, robot)         # 6 leg lengths from current T
        e         = L_target - L_current
        if np.linalg.norm(e) < tol: return T
        J         = stewart_jacobian(T, robot)   # 6×6, dL/dV (twist)
        dV        = np.linalg.solve(J, e)        # body twist update
        T         = T @ matrix_exp_se3(dV)       # SE(3) update
    return None  # convergence failed
```

전략:
- *initial guess* = 이전 time step 의 T (continuous motion 가정)
- 다해 위험 → 가장 *가까운* solution 으로 수렴
- singular configuration 회피 (damped LS)

real-time control: 1kHz 가능 (Newton-Raphson 5~10 iter).

</details>
