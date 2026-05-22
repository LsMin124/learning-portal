# Ch 5 Velocity Kinematics — 퀴즈

> 12 문항 (개념 4 / 계산 3 / 디버그 3 / 면접 2).

## 개념

### Q1. Jacobian 의 정의

`V = J(θ) θ̇` 에서 `V`, `J`, `θ̇` 각각의 차원과 의미.

<details><summary>답</summary>

- `V ∈ R⁶`: end-effector 의 *6D twist* `(ω, v)`
- `J(θ) ∈ R^{6×n}`: configuration-dependent Jacobian 행렬, n = joint 수
- `θ̇ ∈ R^n`: joint velocity 벡터

`J` 의 *컬럼* = 각 joint 의 단위 velocity 가 end-effector 에 만드는 spatial / body twist.

</details>

### Q2. Space vs Body Jacobian 의 frame

`J_s` 와 `J_b` 가 각각 *어느 frame* 에서 표현된 twist 를 만드는지.

<details><summary>답</summary>

- `J_s θ̇ = V_s` (space frame `{s}` 에서 본 EE twist)
- `J_b θ̇ = V_b` (body frame `{b}` 에서 본 EE twist)

변환: `J_s = [Ad_{T_{sb}}] J_b`.

</details>

### Q3. Singularity 정의

Kinematic singularity 의 정확한 정의 + 기하적 의미.

<details><summary>답</summary>

`rank J(θ) < min(6, n)` 인 configuration.

기하적: 어떤 EE velocity 방향이 *어떤 `θ̇` 로도 달성 불가*. velocity ellipsoid 가 *degenerate* (한 축 0).

</details>

### Q4. Force ellipsoid 의 *쌍대*

Velocity ellipsoid 의 *긴 축* 이 force ellipsoid 의 *짧은 축* 인 이유.

<details><summary>답</summary>

Velocity: `V = J θ̇`. 단위 `‖θ̇‖ = 1` 에 대해 V 의 norm 은 `‖J‖` 의 singular value 와 비례.

Force: `τ = Jᵀ F` → `F = (Jᵀ)⁻¹ τ`. 단위 `‖τ‖ = 1` 에 대해 F 의 norm 은 `1/σ` (역수) 와 비례.

따라서 같은 방향에서 σ 큼 ↔ V 큼 (velocity 잘 됨) ↔ F 작음 (큰 토크가 작은 힘 만듦). σ 작음 ↔ V 작음 ↔ F 큼 (작은 토크가 큰 힘 만듦). 

즉 *velocity 좋은 방향* 에선 *force 약함*, *velocity 약한 방향* (singular 근처) 에선 *force 강함*. 이게 쌍대.

</details>

## 계산

### Q5. 2R planar arm Jacobian

`L₁ = L₂ = 1`, `θ_1 = π/2`, `θ_2 = 0` 에서 `J(θ)` 의 값.

<details><summary>답</summary>

`θ_1 + θ_2 = π/2`.

`J = [[-sin(π/2) - sin(π/2), -sin(π/2)], [cos(π/2) + cos(π/2), cos(π/2)]] = [[-2, -1], [0, 0]]`.

→ singularity! `det J = 0`. y 방향 velocity 불가능.

검증: `θ_2 = 0` (팔 완전 펼침) 은 singular configuration. ✓

</details>

### Q6. Space Jacobian column 1

3R planar arm, link 길이 1, screw axes `S_1 = (0,0,1,0,0,0)`, `S_2 = (0,0,1,0,-1,0)`, `S_3 = (0,0,1,0,-2,0)`. `J_{s1}(θ)` 의 형태.

<details><summary>답</summary>

`J_{s1} = S_1 = (0, 0, 1, 0, 0, 0)`. (i=1 의 경우 누적 변환 없음.)

</details>

### Q7. Statics with frame mismatch

End-effector 에 `F_s = (0, 0, 0, 0, -10, 0)` (− y 방향 10N 힘) 이 작용. `J_b` (body Jacobian) 만 알고 있을 때 `τ` 계산.

<details><summary>답</summary>

1. `F_s` 를 `F_b` 로 변환: `F_b = [Ad_{T_{sb}}]ᵀ F_s`.
2. `τ = J_bᵀ F_b`.

또는 (등가):
1. `J_s = [Ad_{T_{sb}}] J_b`.
2. `τ = J_sᵀ F_s`.

둘 다 같은 답. 직접 `τ = J_bᵀ F_s` 는 *잘못* — frame 불일치.

</details>

## 디버그

### Q8. Singularity 미검출

```python
def is_singular(J):
    return np.abs(np.linalg.det(J)) < 1e-6
```

7-DoF arm 에서 이 코드가 *항상 True* 반환. 왜?

<details><summary>답</summary>

`J ∈ R^{6×7}` — 정사각형 아님. `np.linalg.det(J)` 는 *정사각형* 만. numpy 가 LinAlgError 던지거나 wrong result.

수정:
```python
def is_singular(J, tol=1e-6):
    return np.linalg.matrix_rank(J, tol) < min(J.shape)
```

또는 SVD:
```python
sing_vals = np.linalg.svd(J, compute_uv=False)
return sing_vals[-1] < tol
```

</details>

### Q9. J_b 컬럼 순서

Body Jacobian 계산에서 `J_{b,n}` 을 가장 *복잡한* 식으로, `J_{b,1}` 을 `B_1` 그대로 둔다. 잘못 어디?

<details><summary>답</summary>

반대. **`J_{b,n} = B_n` (그대로), `J_{b,1}` 이 가장 복잡** (i+1 부터 n 까지의 모든 joint 의 역변환 adjoint).

수식: `J_{bi} = [Ad_{e^{-[B_{i+1}]θ_{i+1}} ⋯ e^{-[B_n]θ_n}}] B_i`.

- `i = n`: 누적 없음 → `J_{bn} = B_n`
- `i = 1`: `[Ad_{e^{-[B_2]θ_2} ⋯ e^{-[B_n]θ_n}}] B_1` — 가장 누적.

Space form 은 반대 — `J_{s1} = S_1`, `J_{sn}` 이 가장 복잡.

</details>

### Q10. Damped least-squares 미적용

Near-singular configuration 에서 `θ̇ = J⁻¹ V_d` 의 `θ̇` 가 *무한대* 로 발산. 해결책?

<details><summary>답</summary>

**Damped least-squares (DLS)**:
$$\dot\theta = J^T (J J^T + \lambda^2 I)^{-1} \mathcal{V}_d$$

`λ` 가 작으면 일반 pseudoinverse, 크면 누그러짐. singular 근처에서도 `θ̇` 가 *유한* 으로 유지 — 다만 EE velocity 정확도 약간 손해.

또는 *adaptive damping* — singular 측정 (예: σ_min) 에 따라 λ 동적 조정.

</details>

## 면접

### Q11. Why two Jacobians?

면접관 — "왜 Space Jacobian 과 Body Jacobian 두 개를 따로 다루나?"

<details><summary>답</summary>

같은 robot 의 *같은 velocity* 이지만 *표현 frame* 이 다릅니다. 

- **Space Jacobian** (`J_s`): fixed frame `{s}` 기준. 외부 관찰자 시점. 시뮬레이션·visualization 자연스럽고, 작업 공간 좌표가 명확할 때 (예: 픽업 위치 = world coord) 직접 사용.

- **Body Jacobian** (`J_b`): body frame `{b}` 기준. End-effector 시점. *그 EE 가 들고 있는 도구* 가 *자기 기준 어디로 갈지* 자연스러움. 6장 IK 의 Newton-Raphson iteration 에서 body frame error 가 자연스러운 error metric. 또한 force/torque sensor 가 *EE 자체에 부착* 된 경우 측정도 body frame.

선택 기준: *작업이 어느 frame 에서 더 자연스럽게 표현되는가*. 변환은 `[Ad_T]` 한 번이라 큰 코드 부담 아님.

</details>

### Q12. Manipulability ellipsoid 의 활용

산업 robot 설계에서 manipulability ellipsoid 가 *실제로* 어떻게 쓰이나?

<details><summary>답</summary>

1. **Workspace design** — 작업 영역에서 ellipsoid 가 *균등하고 큰* 영역이 되도록 link 길이·축 배치 최적화.
2. **Task-aware posture selection** — 7-DoF redundant arm 의 *추가 자유도* 를 사용해 manipulability 최대화하는 configuration 선택. (예: pick-and-place 의 *어떤 자세로 pick 하나*).
3. **Singularity avoidance** — manipulability measure 가 임계값 이하 → 작업 일시정지 또는 회피 경로.
4. **Optimal task placement** — 동일 작업을 *workspace 의 어느 위치* 에서 수행할지 선택. ellipsoid 좋은 영역에 작업 배치.
5. **Force control** — *force ellipsoid* (쌍대) 가 큰 방향이 *큰 힘 필요한 작업* (예: drilling) 에 유리.

산업 케이스: 자동차 도장 robot 이 *spray 방향* manipulability 최적화한 base 위치 선택.

</details>
