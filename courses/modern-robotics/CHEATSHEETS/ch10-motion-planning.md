# Ch 10 Motion Planning — 치트시트

## TL;DR

- **Problem**: `θ_start → θ_goal` collision-free path in `C_free`.
- **Grid-based**: BFS / Dijkstra / **A*** (`f = g + h`). Optimal if `h` admissible. Exponential in dim.
- **Sampling-based**: **RRT** (single query, high-dim), **PRM** (multi-query). Probabilistically complete.
- **RRT***: asymptotically optimal (re-wiring).
- **Trajectory optimization**: CHOMP, TrajOpt — smooth + collision cost, gradient descent. Local min.
- **Potential field**: simple but local min. Demo only.

---

## Quick Reference

### 표 1. 알고리즘 분류

| Type | 알고리즘 | Completeness | Optimal | Dim |
|--|--|--|--|--|
| Grid | BFS, Dijkstra | Complete | ✓ | low |
| Grid | A* | Complete | ✓ (admissible) | low |
| Sampling tree | RRT | Probabilistic | ✗ | high |
| Sampling tree | RRT* | Probabilistic | asymptotic | high |
| Sampling graph | PRM | Probabilistic | sub | high |
| Optimization | CHOMP, TrajOpt | None | local | high |
| Heuristic | Potential field | None | None | low |

### 표 2. A* `f = g + h`

| 변수 | 의미 |
|--|--|
| `g(n)` | start → n 의 *실제* cost |
| `h(n)` | n → goal 의 *추정* cost (admissible: ≤ true) |
| `f(n)` | start → goal *통과 n* 의 estimated total |
| priority | min `f(n)` |

### 표 3. RRT 의 한 step

```
1. θ_rand = sample(C-space)
2. θ_near = nearest(T, θ_rand)
3. θ_new  = step(θ_near, θ_rand, Δ)
4. if collision_free(θ_near → θ_new): add (θ_near, θ_new) to T
5. if dist(θ_new, θ_goal) < ε: return path
```

### 표 4. PRM 두 phase

| Phase | 동작 |
|--|--|
| Construction | sample N + connect k-NN (collision-free) → roadmap |
| Query | start/goal → roadmap + Dijkstra/A* |

### 표 5. Completeness 등급

| 등급 | 의미 |
|--|--|
| Complete | 해 있으면 반드시 찾음 |
| Resolution complete | grid 해상도 ↑ 시 complete |
| Probabilistically complete | sample 무한 → 확률 1 |
| Heuristic | no guarantee |

### 표 6. Trajectory optimization cost

```
J = ∫ [α‖θ̇‖² + β‖θ̈‖² + γ collision_cost(θ)] dt

         smooth          smooth          obstacle
```

CHOMP: + Hamiltonian Monte Carlo.
TrajOpt: SQP + signed distance field.

### 표 7. Pipeline

```
Planner (10장) → path
                    ↓
                Shortcutting + Smoothing
                    ↓
                Time scaling (9장)
                    ↓
                Controller (11장) → robot
```

---

## Mind Map

```
10장 Motion Planning
├─ 1. 정의: collision-free path in C_free
├─ 2. C-space obstacle (Minkowski sum)
├─ 3. Completeness 등급
├─ 4. Grid-based
│   ├─ BFS / Dijkstra
│   └─ A* (admissible h)
├─ 5. Sampling-based
│   ├─ RRT (single query)
│   │   └─ RRT*, RRT-Connect
│   └─ PRM (multi-query)
├─ 6. Trajectory optimization
│   ├─ CHOMP, TrajOpt
│   └─ J = ∫(smooth + collision) dt
├─ 7. Potential field (demo only)
└─ 8. Online (D* Lite, MPC)
```

---

## 자주 쓰는 의사코드

### A*

```python
from heapq import heappush, heappop

def a_star(start, goal, neighbors, cost, h):
    open = [(h(start), 0, start)]
    came_from, g_score = {}, {start: 0}
    while open:
        _, g, n = heappop(open)
        if n == goal: return reconstruct(came_from, n)
        for m in neighbors(n):
            new_g = g + cost(n, m)
            if new_g < g_score.get(m, float('inf')):
                g_score[m] = new_g
                came_from[m] = n
                heappush(open, (new_g + h(m), new_g, m))
    return None
```

### RRT (basic)

```python
def rrt(start, goal, sample, nearest, step, collision_free, N=10000, eps=0.5):
    T = {start: None}
    for _ in range(N):
        q_rand = sample()
        q_near = nearest(T.keys(), q_rand)
        q_new  = step(q_near, q_rand)
        if collision_free(q_near, q_new):
            T[q_new] = q_near
            if dist(q_new, goal) < eps:
                T[goal] = q_new
                return reconstruct(T, goal)
    return None
```

### Shortcutting

```python
def shortcut(path, collision_free, iters=100):
    for _ in range(iters):
        i, j = sorted(random.sample(range(len(path)), 2))
        if j > i + 1 and collision_free(path[i], path[j]):
            path = path[:i+1] + path[j:]
    return path
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | C_free 안에서 path 찾기 |
| 2 | task obstacle → C-space obstacle (Minkowski) |
| 3 | Completeness 4 등급 |
| 4 | A* — admissible h 면 optimal, low-dim |
| 5 | RRT (single-q) / PRM (multi-q) — high-dim |
| 6 | Trajectory opt — smooth + collision gradient |
| 7 | Potential field — local min trap |
| 8 | Online: D* Lite, MPC |
