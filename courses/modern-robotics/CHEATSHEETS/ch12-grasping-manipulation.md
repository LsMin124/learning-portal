# Ch 12 Grasping and Manipulation — 치트시트

## TL;DR

- **Form closure**: friction-free immobilization. 평면 ≥4 contact, 3D ≥7 contact.
- **Force closure**: friction 활용. 평면 ≥2 frictional, 3D ≥3 frictional. friction cone 겹침.
- **Coulomb friction**: `‖f_t‖ ≤ μ f_n`, cone 반각 `tan⁻¹ μ`.
- **Grasp matrix**: `F_obj = G F_contacts`, `G ∈ R^{6×3k}`. force closure 위해 rank G = 6.
- **Manipulation primitives**: grasping / pushing / pivoting / sliding / throwing.
- **Compliance**: peg-in-hole 의 jamming 회피 (RCC + impedance).

---

## Quick Reference

### 표 1. Closure 종류

| | Form closure | Force closure |
|--|--|--|
| Friction | 무관 | 활용 |
| 평면 최소 contact | 4 | 2 (frictional) |
| 3D 최소 contact | 7 | 3 (frictional) |
| Guarantee | strong | weaker (friction 의존) |
| 실용 | rare | common |

### 표 2. Friction cone

| 변수 | 의미 |
|--|--|
| `n̂` | contact normal (점에서 안쪽) |
| `μ` | friction coefficient (보통 0.1~1.0) |
| 반각 | `tan⁻¹ μ` |
| Wrench | `(r × f, f)`, `f ∈ cone` |
| Linearized | k-side pyramid (k = 4, 8) |

### 표 3. Coulomb friction cases

| μ | 반각 | 예시 |
|--|--|--|
| 0.1 | ~5.7° | smooth metal |
| 0.3 | ~16.7° | wood |
| 0.5 | ~26.6° | rubber on glass |
| 1.0 | 45° | rubber on rubber |

### 표 4. Grasp matrix `G`

| 변수 | 차원 / 의미 |
|--|--|
| Object wrench | `F_obj ∈ R⁶` (3D) or `R³` (planar) |
| Contact force | `f_i ∈ R³` (3D point contact) |
| Stacked | `F_c = (f_1, ..., f_k) ∈ R^{3k}` |
| Grasp matrix | `G ∈ R^{6×3k}` (3D) |
| Relation | `F_obj = G F_c` |
| Force closure | rank G = 6 + ∃ `F_c` ∈ friction cones with `G F_c = F_obj` ∀ `F_obj` |

### 표 5. Force optimization (QP)

```
min   ½ f^T H f                # quadratic objective (energy)
s.t.  G f = F_required           # equality (grasp wrench)
      A_i f_i ≤ b_i              # friction cone polyhedron
      f_i,n ≥ 0                  # compressive
```

H = positive definite (e.g., I). 해법: OSQP, cvxpy.

### 표 6. Manipulation primitives

| Primitive | 차원 | 특징 |
|--|--|--|
| Grasping | 6-DoF | force closure 보장 |
| Pushing | 2-3 DoF | non-prehensile |
| Pivoting | 1 DoF | single point rotation |
| Sliding | 2 DoF | surface friction |
| Throwing | dynamic | timing critical |
| Pulling | 3 DoF | usually with hook |

### 표 7. Contact mode in pushing

| Mode | Condition | 효과 |
|--|--|--|
| Stick | `‖f_t‖ < μ f_n` | contact = 점 |
| Slip (1 dir) | `‖f_t‖ = μ f_n` | tangential motion |
| Separation | `f_n = 0` | contact 끊김 |

---

## Mind Map

```
12장 Grasping and Manipulation
├─ 1. Contact 기하 (point/line/plane, friction)
├─ 2. Friction cone (Coulomb)
│   ├─ μ → 반각 tan⁻¹ μ
│   └─ Linearized (pyramid)
├─ 3. Form closure
│   ├─ 평면 4 contact / 3D 7 contact
│   └─ Reuleaux's principle
├─ 4. Force closure
│   ├─ 평면 2 / 3D 3 (frictional)
│   └─ friction cone 겹침
├─ 5. Grasp matrix G (6×3k)
│   ├─ rank 6
│   └─ Force optimization (QP)
├─ 6. Manipulation primitives
│   ├─ Grasping / Pushing / Pivoting
│   └─ Sliding / Throwing
└─ 7. Compliance (RCC + impedance)
```

---

## 자주 쓰는 식

### Friction cone constraint

```
f_n ≥ 0
‖f_t‖² ≤ μ² f_n²
```

또는 polyhedral approx (k-side):

```
For i in range(k):
    a_i^T f ≤ μ f_n   # i-th friction cone edge constraint
```

### Force closure QP

```python
import cvxpy as cp
import numpy as np

f = cp.Variable(3*k)
F_obj = ...   # desired object wrench (R^6)

# Friction cone constraints (linearized 8-side)
cone_constraints = []
for i in range(k):
    f_i = f[3*i:3*i+3]
    cone_constraints += [
        f_i[2] >= 0,                       # compressive (z = normal)
        cp.norm(f_i[:2], 2) <= mu * f_i[2] # friction
    ]

problem = cp.Problem(
    cp.Minimize(cp.sum_squares(f)),
    [G @ f == F_obj] + cone_constraints
)
problem.solve()
```

### Form closure check (LP)

```python
def is_form_closure(W):  # W: contact wrench matrix R^{d×k}
    d, k = W.shape
    for sign in [+1, -1]:
        for i in range(d):
            v = sign * np.eye(d)[:, i]
            # LP: minimize 0 s.t. W λ = v, λ ≥ 0
            res = linprog(c=np.zeros(k), A_eq=W, b_eq=v, bounds=(0, None))
            if not res.success: return False
    return True
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | Contact 기하 — point/line/plane, frictionless/frictional |
| 2 | Friction cone — Coulomb, μ → 반각 |
| 3 | Form closure — friction-free, 평면 4 / 3D 7 |
| 4 | Force closure — friction 활용, 평면 2 / 3D 3 |
| 5 | Grasp matrix G, force optimization QP |
| 6 | Manipulation primitives — grasp/push/pivot/slide |
| 7 | Compliance — RCC + impedance for assembly |
