# Chapter 10: Motion Planning — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 10: Motion Planning** (책 p.353~404) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 10장의 핵심: *시작 → 목표* 의 **collision-free path** 를 *configuration space* 위에서 찾는 알고리즘들. 9장이 *time scaling* 이었다면 10장은 그 앞단의 *기하* 결정.

## 들어가기 전에

- **선수 지식**
  - **2장**: C-space, obstacle
  - 알고리즘: graph search (BFS, DFS, Dijkstra, A*), 자료구조 (queue, tree)
  - 확률 / 통계 (sampling-based 알고리즘)
- **학습 목표**
  1. **C-space obstacle** — task-space 장애물의 *C-space 안* 표현
  2. Planning 의 *3가지 결과*: complete / probabilistically complete / heuristic
  3. **Grid-based** (Dijkstra, A*) — discrete, optimal, exponential in dim
  4. **Sampling-based** (RRT, PRM) — high-dim 에서 실용
  5. **Trajectory optimization** — gradient descent on smooth cost
- **예상 학습 시간**: 90~120분

---

## 1. 문제 정의

### 1.1 Motion planning problem

> Given start configuration `θ_start`, goal configuration `θ_goal`, 그리고 obstacle 정의 `C_obs ⊂ C-space`. Find continuous path `θ : [0, 1] → C_free` such that `θ(0) = θ_start`, `θ(1) = θ_goal`. (`C_free = C-space \ C_obs`)

### 1.2 C-space obstacle

task-space 의 *physical obstacle* 을 *C-space 안의 obstacle* 로 변환. 예: 2D 평면에서 점 로봇 + 사각형 장애물 → C-space 도 2D, obstacle 도 사각형 (단순).

복잡한 경우: 2R arm + 1 장애물 → C-space (torus T²) 안의 *복잡한 모양*.

![Figure 10.1 — C-space obstacle 의 task-space → C-space 변환. 교재 p.354](/courses/modern-robotics/figures/ch10/fig-10-1.png)

### 1.3 Completeness 분류

| Type | 의미 |
|--|--|
| **Complete** | 해 존재 시 *반드시* 찾음, 없을 시 *증명* |
| **Resolution complete** | grid 해상도 ↑ 시 complete |
| **Probabilistically complete** | sample 무한히 시 확률 1 로 찾음 (RRT, PRM) |
| **Heuristic** | no guarantee, *실용적* (potential field) |

---

## 2. Grid-based Search

### 2.1 C-space 의 discretization

`C-space` 를 *grid* 로 분할. 각 cell 이 graph 의 *node*. 인접 cell 이 *edge* (collision-free 일 때).

### 2.2 알고리즘

| 알고리즘 | 특징 | 복잡도 |
|--|--|--|
| **BFS** | shortest *step* path (unweighted) | O(V + E) |
| **Dijkstra** | shortest *cost* path | O((V + E) log V) |
| **A*** | Dijkstra + heuristic `h(n)` | O((V + E) log V), faster in practice |
| **Greedy best-first** | `h(n)` 만, no `g(n)` | not optimal |

### 2.3 A* 알고리즘

```
priority_queue (min-heap) of (f(n), n) where f(n) = g(n) + h(n)
visited = ∅

add (h(start), start) to queue, g(start) = 0
while queue not empty:
    (f, n) = pop()
    if n == goal: return reconstruct_path(n)
    if n in visited: continue
    add n to visited
    for each neighbor m of n:
        if m in visited: continue
        new_g = g(n) + cost(n, m)
        if new_g < g(m):
            g(m) = new_g
            parent(m) = n
            add (new_g + h(m), m) to queue
return None  # no path
```

`h(n)`: admissible heuristic (예: Euclidean distance to goal). admissible → A* optimal.

![Figure 10.5 — A* search 의 grid 예제. 교재 p.379](/courses/modern-robotics/figures/ch10/fig-10-5.png)

### 2.4 차원의 저주

grid 크기 = `O(n^d)` where d = C-space dim. 7-DoF arm 의 grid 100^7 = 10^14 cell → infeasible. high-dim 에선 sampling-based 필요.

---

## 3. Sampling-based Planning

### 3.1 동기

high-dim C-space 에서 *전체 탐색 불가*. 대신 *random sample* 로 *충분히 dense* tree / graph 구축.

### 3.2 RRT (Rapidly-exploring Random Tree)

LaValle 1998. 가장 인기 sampling-based.

```
T = {root = θ_start}
for iter = 1 to N:
    θ_rand = sample C-space uniformly
    θ_near = nearest node in T to θ_rand
    θ_new  = step from θ_near toward θ_rand by Δ (small step)
    if collision_free(θ_near, θ_new):
        add θ_new to T with parent θ_near
        if dist(θ_new, θ_goal) < ε:
            return path from θ_start to θ_new to θ_goal
return None
```

![Figure 10.9 — RRT 의 tree 성장 예제. 교재 p.387](/courses/modern-robotics/figures/ch10/fig-10-9.png)

**특징**:
- *probabilistically complete*
- high-dim 에 robust
- path 가 *jaggy*, 후처리 *shortcutting* 필요
- 변형: RRT-Connect (양쪽 tree), RRT* (asymptotically optimal)

### 3.3 PRM (Probabilistic Roadmap)

Kavraki 1996. *multi-query* 용도.

```
Construction phase:
    sample N random θ in C_free
    for each θ:
        connect to k nearest neighbors via collision-free local planner
    → roadmap (graph)

Query phase:
    connect θ_start, θ_goal to roadmap
    Dijkstra/A* on roadmap → path
```

**특징**:
- *probabilistically complete*
- *graph reuse* (multi-query 효율적)
- *narrow passage* 문제 — sample 가 *좁은 영역* 안에 잘 안 들어감

### 3.4 비교

| 측면 | RRT | PRM |
|--|--|--|
| 사용 | single query | multi-query |
| 자료구조 | tree | graph |
| 효율 | high-dim 빠름 | multi-query 빠름 |
| Optimality | basic 비-optimal, RRT* optimal | sub-optimal (roadmap dependent) |

---

## 4. Trajectory Optimization

### 4.1 Gradient descent on smooth cost

trajectory `θ(t)` 를 *parametrize* (예: cubic spline 의 control points) → cost `J` 정의:

$$J = \int_0^T \left[ \alpha \|\dot\theta\|^2 + \beta \|\ddot\theta\|^2 + \gamma \cdot \text{collision\_cost}(\theta(t)) \right] dt$$

`J` 의 gradient (control points 기준) 계산 → gradient descent.

### 4.2 CHOMP / TrajOpt

- **CHOMP** (Ratliff 2009): Hamiltonian Monte Carlo + collision gradient
- **TrajOpt** (Schulman 2014): Sequential Quadratic Programming

장점:
- *smooth* trajectory 직접 출력 (post-processing 불필요)
- collision avoidance + dynamics + custom cost 통합 처리

단점:
- *local minimum* (좋은 초기값 필요)
- non-convex → no completeness

### 4.3 Practice

- *initialization*: RRT 로 거친 path → trajectory optimization 으로 smooth
- *MoveIt* 표준: OMPL (RRT/PRM) + CHOMP/TrajOpt 후처리

---

## 5. Potential Field

### 5.1 직관

goal 은 *attractive* potential, obstacle 은 *repulsive* potential. gradient descent.

$$U(\theta) = U_{att}(\theta) + U_{rep}(\theta)$$

$$\dot\theta = -\nabla U(\theta)$$

### 5.2 한계 — Local minimum

obstacle 의 *오목한 형태* 에서 robot 이 *local minimum* 에 빠짐. goal 못 도달.

**처방**: random restart, bug algorithm, harmonic potential field (no local min).

대형 motion planner 의 *후처리* 용도로만 권장.

---

## 6. Online / Reactive Planning

실시간 환경 변화 (사람 움직임, 동적 장애물) 에 *재계획* 필요.

- **D* / D* Lite** — A* 의 incremental 변형, 환경 변화 시 빠른 re-plan
- **Dynamic window** — 차량형 robot 의 단기 horizon
- **MPC** — model predictive control 의 trajectory replanning

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | C-space obstacle = task-space obstacle | 일반적으로 *다른 모양*. 변환 필요. |
| 2 | A* 가 항상 optimal | heuristic 이 *admissible* (`h ≤ 실제 cost`) 해야 함. |
| 3 | RRT 가 *optimal* path 찾음 | basic RRT 는 *not optimal*. RRT* 가 asymptotically optimal. |
| 4 | High-dim 에서 grid 잘 작동 | dim ↑ 시 exponential blowup. sampling-based 필수. |
| 5 | PRM 의 sample 이 *균등* 분포면 좋음 | 좁은 영역 (narrow passage) 에 sample 안 들어감 — bridge sampling 등 heuristic. |
| 6 | Trajectory optimization 이 *반드시* convex | 일반적으로 비-convex. local min 위험. |
| 7 | Potential field 가 *간단* 하고 잘 됨 | 대표적 *local min* 문제. demo 만. |
| 8 | Sampling-based 가 *항상* 완성 | *Probabilistic* completeness — 시간 무한 시 확률 1. 유한 시간엔 보장 없음. |
| 9 | Motion planner 가 trajectory 까지 출력 | 일반적으로 *path* 만. time scaling (9장) 별도. |
| 10 | Planner 의 결과가 *그대로* robot 에 보내짐 | smoothing, shortcutting, time scaling, controller (11장) 까지 필요. |

---

## 자가점검

1. C-space obstacle 의 정의.
2. Planning 의 4 가지 completeness 등급.
3. A* 의 `f(n), g(n), h(n)` 의 의미와 `h` 의 admissibility.
4. RRT 의 한 step 의 4 단계.
5. PRM 의 두 phase.
6. RRT vs PRM 의 적용 시나리오.
7. Trajectory optimization 의 cost 의 일반 형태.
8. Potential field 의 가장 큰 *실패 mode*.
9. Online planning 에서 D* Lite 의 장점.
10. Motion planner → robot 의 *후처리* 단계.

### 해답 (간략)

1. Task-space obstacle 이 C-space 안에서 차지하는 영역 — 일반적으로 다른 모양.
2. Complete / Resolution complete / Probabilistically complete / Heuristic.
3. `f = g + h`, `g` = start 부터의 실제 비용, `h` = goal 까지 추정. admissible = `h ≤ true cost`. → A* optimal.
4. sample → nearest → step → collision check + add.
5. Construction (roadmap 구축) + Query (start/goal 연결 + search).
6. RRT: single-query, high-dim. PRM: multi-query, static environment.
7. `J = ∫ [α‖θ̇‖² + β‖θ̈‖² + γ collision_cost] dt`.
8. Local minimum — 오목한 obstacle 근처에 갇힘.
9. 환경 변경 시 전체 re-plan 대신 *incremental update* → 실시간.
10. Smoothing (shortcut, spline) + time scaling (9장) + controller (11장).

---

## 다음 학습으로

- **11장 (Control)** — 본 장의 path 를 9장 time scaling 으로 trajectory 화 → 11장 controller 의 reference.
- **MoveIt / OMPL** — 산업 robot 의 motion planning 라이브러리. RRT / PRM / CHOMP 모두 포함.
- **Optimization-based**: TrajOpt, CHOMP, GPMP — collision + dynamics + smoothness 통합.
- **RL-based motion planning** — recent trend. neural network policy → planning.
