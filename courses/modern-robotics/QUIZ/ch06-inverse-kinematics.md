# Ch 6 Inverse Kinematics — 퀴즈

> 10 문항.

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
