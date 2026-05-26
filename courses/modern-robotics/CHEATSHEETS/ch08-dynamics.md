# Ch 8 Dynamics — 치트시트

## TL;DR

- **Manipulator equation**: `τ = M(θ) θ̈ + c(θ, θ̇) + g(θ) + Jᵀ F_tip`
- `M(θ)`: symmetric positive-definite mass matrix
- `c(θ, θ̇)`: Coriolis + centrifugal (`C(θ, θ̇) θ̇`)
- `g(θ) = ∂V/∂θ`: gravity torque
- **Lagrangian**: `L = T − V`, `τ_i = d/dt(∂L/∂θ̇_i) − ∂L/∂θ_i`
- **Newton-Euler recursive**: forward (V, V̇) + backward (F, τ), `O(n)`
- **Spatial inertia**: `G_b = [[I_b, 0], [0, mI]]`, single rigid body `F = G V̇ − [ad_V]ᵀ G V`
- **Forward dynamics**: `θ̈ = M⁻¹ (τ − c − g − Jᵀ F_tip)`

---

## Quick Reference

### 표 1. Manipulator equation 의 4 항

| 항 | 식 | 의미 |
|--|--|--|
| Inertia | `M(θ) θ̈` | 가속에 필요한 토크 |
| Coriolis | `C(θ, θ̇) θ̇` | velocity-quadratic fictitious force |
| Gravity | `g(θ) = ∂V/∂θ` | 중력 보상 |
| External | `Jᵀ F_tip` | EE 외력 반작용 |

### 표 2. Mass matrix 성질

| 성질 | 식 | 의미 |
|--|--|--|
| Symmetric | `M = Mᵀ` | partial 교환 |
| Positive-definite | `xᵀ M x > 0` (x ≠ 0) | KE > 0 |
| Configuration-dependent | `M = M(θ)` | 일정 행렬 아님 |
| Bounded | `λ_min I ≤ M ≤ λ_max I` | bounded inertia |

### 표 3. Lagrangian 핵심

| | 형태 |
|--|--|
| Lagrangian | `L(θ, θ̇) = T − V` |
| Kinetic energy | `T = ½ θ̇ᵀ M(θ) θ̇` |
| Euler-Lagrange | `τ_i = d/dt(∂L/∂θ̇_i) − ∂L/∂θ_i` |
| Christoffel | `Γ_{ijk} = ½(∂m_{ij}/∂θ_k + ∂m_{ik}/∂θ_j − ∂m_{jk}/∂θ_i)` |
| Coriolis matrix | `c_i(θ, θ̇) = Σ_{j,k} Γ_{ijk} θ̇_j θ̇_k` |
| Gravity | `g_i = ∂V/∂θ_i` |

### 표 4. Spatial inertia & single body

| | 형태 |
|--|--|
| Spatial inertia | `G_b = [[I_b, 0], [0, mI]] ∈ R^{6×6}` |
| Kinetic energy | `K = ½ V_bᵀ G_b V_b` |
| Newton-Euler (single body) | `F_b = G_b V̇_b − [ad_{V_b}]ᵀ G_b V_b` |
| `[ad_V]` | `[[ω], 0; [v], [ω]] ∈ R^{6×6}` |
| Frame 변환 | `G_a = [Ad_{T_{ab}}]ᵀ G_b [Ad_{T_{ab}}]` |

### 표 5. Newton-Euler recursive (요약)

**Forward (V, V̇ propagation, base → EE)**:
```
V_i = A_i θ̇_i + [Ad_{T_{i,i-1}}] V_{i-1}
V̇_i = A_i θ̈_i + [Ad_{T_{i,i-1}}] V̇_{i-1} + [ad_{V_i}] A_i θ̇_i
```

**Backward (F, τ propagation, EE → base)**:
```
F_i = [Ad_{T_{i+1,i}}]ᵀ F_{i+1} + G_i V̇_i − [ad_{V_i}]ᵀ G_i V_i
τ_i = F_iᵀ A_i
```

총 `O(n)`.

### 표 6. Forward vs Inverse dynamics

| 방향 | input | output | 알고리즘 |
|--|--|--|--|
| Inverse | `(θ, θ̇, θ̈)` | `τ` | Recursive Newton-Euler, `O(n)` |
| Forward | `(θ, θ̇, τ)` | `θ̈` | (1) NE for `c+g+Jᵀ F`, (2) NE for M cols, (3) `M⁻¹(...)`. Or **ABA** `O(n)` direct. |

### 표 7. Task-space mapping

| | 식 |
|--|--|
| Velocity | `V = J θ̇` |
| Acceleration | `V̇ = J θ̈ + J̇ θ̇` |
| Force / torque | `τ = Jᵀ F` |
| Task-space inertia | `Λ(θ) = (J M⁻¹ Jᵀ)⁻¹` |
| Task-space dynamics | `F_tip = Λ V̇ + η + ρ` |

### 표 8. Articulated-Body Algorithm (ABA, Featherstone)

```
Pass 1 (forward V):  V_i  = A_i θ̇_i + [Ad] V_{i-1}
                     c_i  = [ad_{V_i}](A_i θ̇_i)

Pass 2 (backward I^A, p^A):
        U_i = I^A_i · A_i              # 6-vector
        D_i = A_i^T · U_i              # scalar
        u_i = τ_i - A_i^T · p^A_i      # scalar
        I^a_par = I^A_i - U_i U_i^T / D_i
        p^a_par = p^A_i + I^a_par·c_i + U_i·u_i/D_i
        부모로 [Ad]^T 변환하여 누적

Pass 3 (forward V̇, θ̈):
        V̇_prior = [Ad] V̇_{i-1} + c_i
        θ̈_i    = (u_i - U_i^T V̇_prior) / D_i
        V̇_i    = V̇_prior + A_i θ̈_i
```

`M⁻¹` 명시적으로 안 나옴 → O(n).

### 표 9. Forward dynamics 알고리즘 비교 (n=7)

| 방법 | 복잡도 | FLOPs (n=7) | 비고 |
|--|--|--|--|
| Naive: RNEA × 2 + M⁻¹ (LU) | O(n³) | ~24,000 | M⁻¹ 직접 |
| CRBA + Cholesky | O(n²) | ~6,000 | M SPD 활용 |
| **ABA** | **O(n)** | **~1,500** | spatial algebra |

n ≤ 6 에선 상수 차이로 naive 와 비슷, n ≥ 7 부터 ABA 우세.

---

## Mind Map

```
8장 Dynamics
├─ 1. Manipulator eq: τ = M θ̈ + c + g + Jᵀ F_tip
├─ 2. 2R arm 예제 (Lagrangian 직관)
├─ 3. Lagrangian formulation
│   ├─ L = T − V
│   ├─ Euler-Lagrange eq.
│   ├─ Christoffel symbols
│   └─ Passivity (Ṁ − 2C skew)
├─ 4. 단일 강체 dynamics
│   ├─ Spatial inertia G_b
│   └─ F_b = G_b V̇_b − [ad_V]ᵀ G_b V_b
├─ 5. Newton-Euler recursive
│   ├─ Forward (V, V̇) base→EE
│   └─ Backward (F, τ) EE→base
├─ 6. Mass matrix via NE (unit accel trick)
├─ 7. Forward dynamics: M⁻¹(τ − c − g) or ABA
├─ 8. Task-space dynamics (Λ, η, ρ)
└─ 9. Constrained dynamics (Lagrange multipliers)
```

---

## 자주 쓰는 식 / 의사코드

### Lagrangian dynamics

```
1. T = ½ θ̇ᵀ M(θ) θ̇
2. V = Σ_i m_i g h_i(θ)
3. L = T − V
4. τ_i = d/dt(∂L/∂θ̇_i) − ∂L/∂θ_i
5. Rearrange: τ = M θ̈ + C θ̇ + g
```

### Inverse dynamics (Newton-Euler, O(n))

```python
def inverse_dynamics(θ, θ̇, θ̈, F_tip, robot):
    # Forward pass
    V[0] = 0
    V̇[0] = -g_vector  # gravity trick
    for i in range(1, n+1):
        T = robot.M[i] @ expm(skew_se3(-A[i] * θ[i]))
        V[i] = A[i] * θ̇[i] + Ad(T) @ V[i-1]
        V̇[i] = A[i] * θ̈[i] + Ad(T) @ V̇[i-1] + ad(V[i]) @ A[i] * θ̇[i]
    # Backward pass
    F[n+1] = F_tip
    for i in range(n, 0, -1):
        F[i] = Ad(T[i+1,i]).T @ F[i+1] + G[i] @ V̇[i] - ad(V[i]).T @ G[i] @ V[i]
        τ[i] = F[i] @ A[i]
    return τ
```

### Mass matrix via inverse dynamics

```python
def mass_matrix(θ, robot):
    n = len(θ)
    M = np.zeros((n, n))
    for i in range(n):
        e_i = np.zeros(n); e_i[i] = 1
        M[:, i] = inverse_dynamics(θ, np.zeros(n), e_i, np.zeros(6), robot_no_gravity)
    return M
```

### Forward dynamics

```python
def forward_dynamics(θ, θ̇, τ, F_tip, robot):
    # 1. Compute c + g + Jᵀ F_tip
    h = inverse_dynamics(θ, θ̇, np.zeros(n), F_tip, robot)
    # 2. Compute M
    M = mass_matrix(θ, robot)
    # 3. Solve M θ̈ = τ − h
    θ̈ = np.linalg.solve(M, τ - h)
    return θ̈
```

### Computed-torque control (preview)

```python
τ = M(θ) @ θ̈_d + c(θ, θ̇) + g(θ) + K_p @ (θ_d - θ) + K_d @ (θ̇_d - θ̇)
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | `τ = M θ̈ + c + g + Jᵀ F_tip` 가 전부 |
| 2 | 2R arm 으로 mass matrix, c, g 직접 도출 |
| 3 | Lagrangian L = T − V, E-L eq, Christoffel symbols |
| 4 | 강체 1개: `G_b`, `F = G V̇ − [ad_V]ᵀ G V` |
| 5 | Newton-Euler recursive O(n) — forward V, backward F |
| 6 | Mass matrix 효율 계산 (unit accel trick) |
| 7 | Forward dynamics: ABA O(n) 권장 |
| 8 | Task-space inertia `Λ = (J M⁻¹ Jᵀ)⁻¹` |
| 9 | Constraint 시 Lagrange multiplier `Aᵀ λ` |
