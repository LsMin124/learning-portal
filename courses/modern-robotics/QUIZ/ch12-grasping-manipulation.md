# Ch 12 Grasping and Manipulation — 퀴즈

> 10 문항.

### Q1. Form vs Force closure

두 closure 의 *결정적* 차이.

<details><summary>답</summary>

- **Form closure**: friction *무관*, geometric immobilization. 평면 4 contact, 3D 7 contact. *strong* guarantee.
- **Force closure**: friction *활용*, 모든 external wrench 반작용. 평면 2 frictional, 3D 3+ frictional. *practical*.

Form closure 가 *더 엄격*. Force closure 가 실제 robotic hand 에서 *훨씬 흔함*.

</details>

### Q2. Friction cone 의 반각

`μ = 0.5` 의 friction cone 의 반각 (radians).

<details><summary>답</summary>

반각 = `tan⁻¹(μ) = tan⁻¹(0.5) ≈ 0.4636 rad ≈ 26.57°`.

즉 contact normal 에서 *26.57° 이내* 의 force 만 가능. 큰 μ → wider cone → 더 안정.

</details>

### Q3. 평면 form closure 의 4-contact 이유

왜 *3 contact* 으로 안 되는가?

<details><summary>답</summary>

평면 강체는 3 DoF (x, y, θ). 3 contact 의 *constraint wrench* 는 평면의 line 또는 점에 *positive span* 불가 — 어느 방향의 motion 이 남음.

Reuleaux: 3 contact 라인이 *모두 한 점에서 교차* 또는 *모두 평행* 하면 그 점 회전 또는 그 방향 병진 가능. 4 contact 으로 모든 방향 봉쇄.

수학: contact wrench 의 positive span 이 *R³ 전체* 가 되려면 4 개 필요 (보통).

</details>

### Q4. Grasp matrix rank

3-finger 평면 grasp, 각 contact 2D force. `G` 의 차원 + rank 조건.

<details><summary>답</summary>

평면 object wrench `R³` (force x, y + moment z). 3 finger × 2 force = 6 components.

`G ∈ R^{3 × 6}`. force closure 위해 **rank G = 3** (object wrench 6D 부분 공간 모두 cover).

rank 3 이지만 friction cone constraint 도 만족해야 → LP / QP 검사.

</details>

### Q5. Grasping force optimization

물체에 `F_required = (0, 0, 0, 0, 0, −9.81)` (중력만) 적용. minimum `f_i` 분포 찾는 QP.

<details><summary>답</summary>

```
min  Σ ‖f_i‖²
s.t. G f = F_required = (0, 0, 0, 0, 0, -9.81)
     f_i ∈ friction_cone_i  for each contact
```

QP — quadratic objective + linear constraints (friction cone 의 polyhedral approximation 시).

해법: cvxpy, OSQP, MATLAB quadprog.

```python
import cvxpy as cp
f = cp.Variable(3*k)
problem = cp.Problem(
    cp.Minimize(cp.sum_squares(f)),
    [G @ f == F_required] + friction_cone_constraints
)
problem.solve()
```

</details>

### Q6. Pushing 의 *contact mode*

손가락이 물체를 밀 때 contact 의 상태 3 가지.

<details><summary>답</summary>

1. **Stick** — friction force 가 cone 안. contact 가 *고정 점* 처럼 작용.
2. **Slip (one direction)** — friction force 가 cone *경계*. contact 점이 표면 위에서 *미끄러짐*.
3. **Separation** — contact 끊어짐. force = 0.

Manipulator 가 *목표 mode 를 유지* 하면서 push 해야 — *mode 변환* 시 contact 동역학이 *불연속* 변화.

비유: 자동차 타이어 grip → slip 의 dynamic transition.

</details>

### Q7. Form closure 검사 알고리즘

`k` 개 contact 의 constraint wrench `w_i ∈ R^d` 가 form closure 인지 검사.

<details><summary>답</summary>

`w_i` 가 *positively span* `R^d` 인지 검사:

$$\exists \lambda_i \geq 0 \quad \text{s.t. } \sum_i \lambda_i w_i = -v \quad \forall v \in \mathbb{R}^d$$

LP 형태:

```
For each direction v in basis of R^d (positive and negative):
    LP: find λ ≥ 0 such that Σ λ_i w_i = -v
    If infeasible for any v → not form closure
```

또는 *convex hull of wrenches* 가 *origin 을 내부 점으로 포함* 하는지 검사.

`d` 작으면 (평면 d=3, 3D d=6) 계산 빠름.

</details>

### Q8. Force closure 의 *robust* margin

force closure 가 있어도 *작은 perturbation* 에 무너질 수 있음. robust margin 측정.

<details><summary>답</summary>

가장 흔한 metric: **Ferrari-Canny grasp quality** Q = grasp wrench space 의 *origin 까지의 최단 거리*. 큰 Q = robust.

```
1. 각 contact 의 friction cone 의 edge wrench enumeration
2. 모든 edge wrench 의 *convex hull* C
3. Q = min { ‖w‖ : w ∈ ∂C }   # origin 에서 hull boundary 까지
```

Q > 0 → force closure. Q ↑ → robust.

다른 metric: minimum singular value of G, sum of contact forces 등.

</details>

### Q9. Peg-in-hole 의 jamming

hole 에 peg 가 *비스듬히* 들어가서 *움직이지도 빠지지도* 못함. 원인 + 해결.

<details><summary>답</summary>

**원인**:
- peg 의 두 모서리가 hole 의 내벽에 *동시에* contact
- friction 으로 *normal force 가 어떻게든 같이 받쳐* — 어느 방향으로 force 가해도 anti-friction force 가 cancel

조건: peg 의 *기울기 각* 이 hole 의 *clearance* 와 friction coefficient 의 *임계값* 초과.

**해결**:
1. **Impedance / compliance** — robot 이 *contact force 따라 부드럽게 양보* (RCC + impedance control)
2. **Spiral / wiggle search** — 작은 circular motion 으로 정렬 보정
3. **Tilt-then-insert** — 먼저 *기울여 한쪽 모서리만 contact* → 정렬 → 수직 insertion

산업 표준: RCC + force-feedback insertion.

</details>

### Q10. Modern grasping 의 *learning-based* 접근

DexNet, GraspNet 등의 핵심 아이디어.

<details><summary>답</summary>

**전통**: 정확한 object model → analytical force closure 계산 → grasp pose 최적화.

**Learning-based**:
1. **DexNet** (Mahler et al.) — depth image 입력 → grasp pose + 성공 확률 predictor (CNN). 무수한 synthetic grasp 으로 training.
2. **GraspNet-1Billion** — large-scale grasp dataset 으로 6-DoF grasp pose 직접 회귀.
3. **CLIP-grasp** — language-conditioned grasp (예: "give me the red cup").
4. **Dexterous policy** — RL 로 5-finger hand 의 in-hand manipulation (Shadow Hand cube rotation).

장점:
- *unknown object* 에 일반화
- depth/RGB image 만으로 작동 (object model 불필요)
- contact-rich tasks 에 robust

단점:
- training data 양 大
- *force closure 보장* 안 됨 (heuristic)
- Sim2Real gap

산업: Amazon Robotics, Covariant.ai 등 picking 의 핵심.

</details>
