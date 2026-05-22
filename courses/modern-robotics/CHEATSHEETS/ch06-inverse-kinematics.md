# Ch 6 Inverse Kinematics — 치트시트

## TL;DR

- **IK** = `T_d → θ`. 비선형, 다해 (또는 무해).
- **Analytic IK**: Pieper criterion 만족 (spherical wrist) → closed-form, 최대 8 해.
- **Numerical IK**: Newton-Raphson with body Jacobian.
  - `V_b = log(T⁻¹ T_d)`
  - `θ ← θ + J_b⁻¹ V_b`
- **Damped LS**: `Δθ = J_bᵀ (J_b J_bᵀ + λ²I)⁻¹ V_b` (singular 회피)
- **Redundancy**: `θ̇ = J⁺ V_d + (I − J⁺J) θ̇_0` (null-space task)

---

## Quick Reference

### 표 1. Analytic vs Numerical IK

| | Analytic | Numerical |
|--|--|--|
| 적용 | Pieper-criterion arm | general arm |
| 속도 | constant time | iterative (수렴 시간 가변) |
| 정확도 | exact | tolerance dependent |
| 코딩 | per-robot | general-purpose |
| Real-time 1kHz | ✓ | borderline (좋은 초기값 필요) |
| 다해 처리 | 모든 해 enumerate | 한 해 (초기값 의존) |

### 표 2. 6R PUMA 의 8 해

| 변수 | 의미 | 케이스 |
|--|--|--|
| `θ_1` | shoulder rotation | front / back |
| elbow | `θ_2, θ_3` | up / down |
| wrist | `θ_4, θ_5, θ_6` | flip / no flip |

총 2³ = 8.

### 표 3. Numerical IK 알고리즘

```
Input:  T_d, θ_0, ε_ω, ε_v, max_iter
Output: θ such that T(θ) ≈ T_d

θ = θ_0
for k = 1 to max_iter:
    T   = FK(θ)
    V_b = log(T⁻¹ T_d)               # body twist
    if ‖ω_b‖ < ε_ω and ‖v_b‖ < ε_v:
        return θ
    Δθ  = pinv(J_b(θ)) · V_b          # or damped LS
    θ   = θ + Δθ
return None  # 수렴 실패
```

### 표 4. Singular 회피 전략

| 전략 | 식 |
|--|--|
| Damped LS | `Δθ = Jᵀ (J Jᵀ + λ²I)⁻¹ V` |
| Adaptive damping | `λ = λ(σ_min)` |
| Singularity-robust | SVD truncation |

### 표 5. Redundancy resolution

| Primary task | EE pose `T_d` |
|--|--|
| Secondary task | joint limit / obstacle / manipulability |
| Update | `θ̇ = J⁺ V_d + (I − J⁺J) θ̇_0` |
| `θ̇_0` 예 | `∇ μ(θ)` (manipulability gradient) |

---

## Mind Map

```
6장 Inverse Kinematics
├─ 1. 정의: T → θ (비선형, 다해)
├─ 2. Analytic IK
│   ├─ Pieper criterion (spherical wrist)
│   ├─ Position decoupling → first 3 joints
│   ├─ Orientation decoupling → last 3 joints
│   └─ 최대 8 해 (front/back × up/down × flip)
├─ 3. Numerical IK (Newton-Raphson, body)
│   ├─ V_b = log(T⁻¹ T_d)
│   ├─ θ ← θ + J_b⁻¹ V_b
│   └─ damped LS for singular
└─ 4. Redundancy resolution (7-DoF)
    ├─ θ̇ = J⁺ V_d + (I − J⁺J) θ̇_0
    └─ 응용: joint limit / obstacle / manipulability
```

---

## 1-line summary

| 절 | 요약 |
|--|--|
| 1 | IK = T → θ, 비유일·비존재·수렴성 문제 |
| 2 | Pieper criterion → analytic, 최대 8 해 |
| 3 | Newton-Raphson with body Jacobian, log(T⁻¹ T_d) |
| 4 | 7-DoF arm 의 null-space 로 secondary task |
