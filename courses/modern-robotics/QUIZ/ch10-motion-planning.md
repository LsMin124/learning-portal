# Ch 10 Motion Planning — 퀴즈

> 10 문항.

### Q1. C-space obstacle

2D 평면에 robot 이 *원 (반경 r)*, 장애물이 *직사각형*. C-space obstacle 의 모양.

<details><summary>답</summary>

직사각형을 *Minkowski sum* 으로 r 만큼 *팽창* (rounded corners). robot 의 중심이 그 영역 안에 있으면 충돌. C-space = 직사각형의 각 변에 반경 r 의 *round* 가 더해진 모양.

</details>

### Q2. A* 의 admissibility

`h(n)` 이 *admissible* 이 아니면 어떤 문제가 생기나? 예시.

<details><summary>답</summary>

A* 의 *optimality* 잃음. `h(n) > true_cost(n, goal)` 이면 *최적 경로 통과* 노드가 *우선순위 낮음* 으로 평가되어 탐색 안 됨 → suboptimal path 반환.

예: grid 에서 진짜 cost = 10 인데 `h = 15` 이면 그 노드 우선순위 ↑ (잘못된 방향으로 탐색).

실용 heuristic: Euclidean distance (Manhattan 일 때는 Chebyshev). 둘 다 admissible.

</details>

### Q3. RRT 의 nearest 단계 비용

`N` 개 node 의 RRT 에서 nearest neighbor 검색의 complexity.

<details><summary>답</summary>

naïve: `O(N)` per iter → 전체 `O(N²)`.

가속: k-d tree 사용 → `O(log N)` per iter, 전체 `O(N log N)`. 단, k-d tree 가 *high-dim* 에서 효율 ↓ (curse of dim).

추가 가속: locality-sensitive hashing (LSH), ball tree, FLANN library.

</details>

### Q4. RRT 의 step size

`Δ` 가 너무 작으면 / 너무 크면 각각 문제.

<details><summary>답</summary>

**너무 작음**:
- iteration 수 폭증
- tree 가 *seed 근처* 만 dense 해지고 goal 못 reach

**너무 큼**:
- collision check 가 *부정확* (Δ 내부에서 obstacle 통과 가능)
- *narrow passage* 못 통과

권장: C-space scale 의 ~5% 정도. *adaptive* 가 robust.

</details>

### Q5. RRT-Connect

basic RRT vs RRT-Connect 의 차이 + 장점.

<details><summary>답</summary>

basic RRT: start 에서 random 방향 tree 성장.

**RRT-Connect**: 두 tree 동시 성장 — 하나는 `θ_start` 에서, 하나는 `θ_goal` 에서. 매 iter 양쪽이 *서로* 를 향해 step. 두 tree 연결 시 종료.

장점:
- *goal-biased* 효과 (양쪽이 서로 끌어당김)
- 단방향 RRT 보다 *수렴 빠름*

표준 baseline. MoveIt 의 RRTConnect 가 이것.

</details>

### Q6. PRM 의 narrow passage 문제

좁은 통로에 sample 적게 들어감. 해결책.

<details><summary>답</summary>

1. **Bridge sampling** — 두 obstacle 사이의 *bridge* 위에 sample 집중
2. **Gaussian sampling** — obstacle 근처에 추가 sample
3. **Visibility-based PRM** — obstacle boundary 의 *visible* 영역 sample
4. **Adaptive PRM** — 실패 영역에 더 많이 sample

또는 *hybrid* — initial PRM + RRT-Connect 로 narrow passage 보강.

</details>

### Q7. Asymptotic optimality

RRT 와 RRT* 의 차이.

<details><summary>답</summary>

**RRT** (basic): probabilistically complete 이지만 *optimal 아님*. 즉 시간 → ∞ 에도 최적 path 보장 X.

**RRT*** (Karaman & Frazzoli 2011): *re-wiring* 추가 — 새 node 추가 시 *주변 node 들의 부모* 를 재평가하여 cost 감소 시 갱신. *asymptotically optimal* — 시간 ↑ 에 따라 *optimal path 에 수렴*.

trade-off: re-wiring 비용으로 iteration 당 느림. 그러나 결과 path 품질 ↑.

</details>

### Q8. Trajectory optimization 의 local min

CHOMP / TrajOpt 가 *local minimum* 에 빠짐. 해결책 3 개.

<details><summary>답</summary>

1. **Good initialization** — RRT 등으로 거친 path 먼저 → optimization 의 *시작점*. local min 회피.
2. **Multiple random restart** — 여러 초기값으로 optimization → 가장 좋은 결과 선택.
3. **Convex relaxation** — non-convex 문제를 *convex approximation* 으로 풀고 점진적 refine.
4. **Annealing / homotopy** — collision cost weight 를 *낮게 시작 → 점진적 증가*. early phase 에 global structure 잡음.

산업 robot: RRT (initial) → TrajOpt (refine) 의 hybrid 가 표준.

</details>

### Q9. Potential field local min

`U = U_att + U_rep` 의 gradient descent 가 *local min* 에 빠짐. 검출·회피.

<details><summary>답</summary>

**검출**: gradient `‖∇U‖ < ε` 인데 `θ ≠ θ_goal`. 즉 *force balance* 인데 goal 안 도달.

**회피**:
1. *Random walk* — local min 에서 random 방향으로 escape
2. *Bug algorithm* — wall-following 로 obstacle 우회
3. *Harmonic potential field* — Laplace 방정식 해 → no local min (단 계산 비싸)
4. *Navigation function* (Koditschek 1990) — 수학적으로 *no local min* 인 potential 구조

실용: potential field 단독은 demo 만. real planner 의 *후처리* / RL 의 reward shaping 으로 사용.

</details>

### Q10. Motion planner output

RRT 가 path 반환. 이를 *real robot* 에 보내기 전 4 단계 후처리.

<details><summary>답</summary>

1. **Shortcutting** — path 의 *불필요한 굴절* 제거. (random 두 node 사이 straight line 시도 → collision-free 면 대체.)
2. **Smoothing** — spline / B-spline 로 부드럽게 (`s̈` 연속).
3. **Time scaling** — 9장 cubic / quintic / trapezoidal / S-curve.
4. **Controller** (11장) — desired trajectory 의 tracking + disturbance rejection.

추가: collision verification (final), joint limit check.

이 pipeline 이 MoveIt 등 산업 framework 의 기본.

</details>
