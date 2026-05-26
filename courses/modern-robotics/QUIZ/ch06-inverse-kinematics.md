# Ch 6 Inverse Kinematics — 퀴즈

> 13 문항.

### Q1. IK 의 어려움 3 가지

FK 대비 IK 의 추가적 어려움 3 가지.

<details><summary>답</summary>

비존재 (workspace 밖), 비유일 (다해, 6R PUMA 는 최대 8), 수치 수렴성 (singular / 초기값).

</details>

### Q2. Pieper criterion

Analytic IK 가능 조건.

<details><summary>답</summary>

6R arm 의 마지막 3 회전축이 한 점에서 만남 (spherical wrist). 그러면 position 과 orientation IK 가 분리 → closed-form.

</details>

### Q3. 6R PUMA 의 최대 해 수

<details><summary>답</summary>

8 (= 2³). front/back × elbow up/down × wrist flip.

</details>

### Q4. Newton-Raphson IK update

`θ_d` 가 *현재 자세 + body twist Δ* 일 때 update 식.

<details><summary>답</summary>

$$V_b = \log(T(\theta_k)^{-1} T_d), \quad \theta_{k+1} = \theta_k + J_b^{-1}(\theta_k) V_b$$

`n > 6` 면 `J_b⁺` (pseudoinverse).

</details>

### Q5. log(T) 의 well-defined 문제

`log : SE(3) → se(3)` 가 unique 아닌 경우.

<details><summary>답</summary>

R 의 회전 각도 `θ = π` 케이스. `R = e^{[ω̂]π}` 에서 `−ω̂` 도 같은 R 줌. 코드에서 별도 처리 (책 §3.2.3.3).

</details>

### Q6. Damped LS

singular 회피 update 식.

<details><summary>답</summary>

`Δθ = J_bᵀ (J_b J_bᵀ + λ² I)⁻¹ V_b`. `λ` 작으면 일반 pseudoinverse, 크면 누그러짐.

</details>

### Q7. 7-DoF redundancy

7-DoF arm 의 *task* 차원과 *redundancy* 차원.

<details><summary>답</summary>

task = 6 (EE pose ∈ SE(3)). redundancy = 7 − 6 = 1. 같은 EE pose 에 1-parameter family 의 joint configuration.

</details>

### Q8. Null-space task

7-DoF arm 에서 *팔꿈치를 위로* 들고 싶을 때 IK update.

<details><summary>답</summary>

```
V_d = body twist toward T_d
θ̇_0 = "팔꿈치 위" 방향의 secondary task gradient

θ̇ = J⁺ V_d + (I − J⁺ J) θ̇_0
```

첫 항이 EE pose 보장, 둘째 항이 *null space 안에서* 팔꿈치 motion.

</details>

### Q9. IK 발산 디버그

`while True: θ ← θ + J⁻¹ V_b` 가 무한 반복. 원인 가능성 3 가지.

<details><summary>답</summary>

1. **Singular configuration** 근처 → `J⁻¹` 발산. damped LS 사용.
2. **초기값 너무 멀어 local minimum** → multiple restart 또는 좋은 `θ_0`.
3. **수렴 조건 누락** → `‖V_b‖ < ε` 체크 없으면 영원히 도는 epsilon-cycle. tolerance 확인.

</details>

### Q10. Analytic vs Numerical 의 선택

산업 현장에서 분석 IK 와 수치 IK 의 *언제 어느 것* 을 쓰는지.

<details><summary>답</summary>

- **Real-time 1kHz 제어** (예: force control): analytic — 일정 시간 보장
- **Arbitrary arm geometry** (PoE 기반 정의만 있는 새 robot): numerical — general-purpose
- **MoveIt 같은 motion planner**: analytic 우선, 실패 시 numerical fallback (하이브리드)
- **연구·개발**: numerical (빠른 prototyping)
- **검증·verification**: 두 방법 모두 → cross-check

</details>

### Q11. PUMA Step 3 — Law of cosines

PUMA 의 `(θ_2, θ_3)` 단계에서 *해 없음* 이 발견되는 식별자는?

<details><summary>답</summary>

$$D = \frac{r^2 + s^2 - L_2^2 - L_3^2}{2 L_2 L_3}$$

이 `D` 가 `|D| > 1` 이면 `arccos D` 미정의 — 즉 *wrist center 가 reach 밖* (`L_2 + L_3 < \sqrt{r^2 + s^2}` 또는 `|L_2 - L_3| > \sqrt{r^2 + s^2}`).

코드 패턴:
```python
D = (r*r + s*s - L2*L2 - L3*L3) / (2 * L2 * L3)
if abs(D) > 1.0 + 1e-9:
    raise IKError("target out of reach")
D = max(-1.0, min(1.0, D))            # 수치 clamp
sin_t3_sq = 1.0 - D*D
theta3_up   = math.atan2(+math.sqrt(sin_t3_sq), D) - phi
theta3_down = math.atan2(-math.sqrt(sin_t3_sq), D) - phi
```

또한 `D = ±1` 정확히 *boundary* (single solution — elbow 완전 펴짐/접힘). 이 케이스가 *workspace boundary singularity*.

</details>

### Q12. Wrist singularity 검출

PUMA Step 6 의 ZYZ 분해에서 *wrist singularity* 가 어떻게 식별되며, 그 *물리적* 의미는?

<details><summary>답</summary>

**식별** — `R_{36}` 에서:

$$\sin\theta_5 = \sqrt{r_{13}^2 + r_{23}^2}$$

이 값이 0 에 가까우면 (즉 `r_{13} ≈ r_{23} ≈ 0`) singularity. → `r_{33} = \pm 1` (joint 4 와 6 의 축이 *평행* 또는 *반대*).

**물리** — joint 4 와 joint 6 의 회전축이 *공선* 이 되어 한 자유도가 *손실*. EE 가 그 축 방향으로 *추가 회전 불가능*. (5-DoF instantaneous mobility.)

**코드 처리**:
```python
sin_t5 = math.sqrt(r13*r13 + r23*r23)
if sin_t5 < 1e-6:                     # wrist singularity
    theta5 = 0.0                       # 또는 π (r33 sign)
    theta4 = current_theta4             # 유지 (분해 불가)
    theta6 = math.atan2(r21, r11) - theta4
else:
    theta5 = math.atan2(sin_t5, r33)
    theta4 = math.atan2(r23, r13)
    theta6 = math.atan2(r32, -r31)
```

`θ_4 + θ_6` 만 결정되고 *개별 분해* 가 불가 — current `θ_4` 를 유지하고 `θ_6` 를 조정.

이 wrist singularity 가 *PUMA arm 의 가장 흔한* singular configuration. operational 측 대처 = path planning 단계에서 회피.

</details>

### Q13. PUMA IK 종합 코드

8 개의 후보 해를 모두 생성한 후 *현재 자세* `θ_curr` 와의 *L1 거리* 가 최소인 해를 선택하는 의사코드.

<details><summary>답</summary>

```python
def puma_ik_select(T_d, theta_curr, robot):
    # 1. Wrist center
    p_w = T_d[:3, 3] - d6 * T_d[:3, 2]

    candidates = []
    # 2. θ_1: front / back
    for theta1 in [atan2(p_w[1], p_w[0]),
                   atan2(p_w[1], p_w[0]) + pi]:
        # 3. θ_2, θ_3: elbow up / down
        for elbow_sign in [+1, -1]:
            try:
                theta2, theta3 = solve_planar_2r(
                    p_w, theta1, L2, L3, phi, elbow_sign)
            except IKError:
                continue
            # 4. R_03 → R_36
            R03 = compute_R03(theta1, theta2, theta3)
            R36 = R03.T @ T_d[:3, :3]
            # 5. θ_4, θ_5, θ_6: wrist flip
            for wrist_sign in [+1, -1]:
                theta4, theta5, theta6 = solve_zyz_euler(R36, wrist_sign)
                cand = (theta1, theta2, theta3, theta4, theta5, theta6)
                if respects_joint_limits(cand, robot.limits):
                    candidates.append(cand)

    if not candidates:
        raise IKError("no feasible solution")

    # 6. 현재 자세와 가장 가까운 해 선택 (L1 norm in joint space)
    def dist(cand):
        return sum(abs(angle_diff(c, q)) for c, q in zip(cand, theta_curr))
    return min(candidates, key=dist)
```

핵심: 8 가지 후보 모두 *시도* → joint limit filter → 현재와의 거리로 *minimum-jerk* 선택.

`angle_diff` 는 `(a - b + π) mod 2π - π` 로 *최단 회전* 차이 계산. 직접 `a - b` 면 ±2π 차이가 큰 거리로 잘못 측정됨.

</details>
