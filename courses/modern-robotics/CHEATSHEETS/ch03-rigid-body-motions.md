# Ch 3 Rigid-Body Motions — 치트시트

## TL;DR

- **SO(3)** = `{R | RᵀR = I, det R = +1}`. 3 DoF. 비가환.
- **so(3)** = skew-symmetric 3×3. `[ω] x = ω × x`. tangent space of SO(3).
- **Rodrigues**: `R = e^{[ω̂]θ} = I + sin θ [ω̂] + (1 − cos θ) [ω̂]²`
- **SE(3)** = 4×4 homogeneous transform. 6 DoF. `T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]`.
- **Twist** `V = (ω, v) ∈ R⁶`. Spatial vs Body.
- **Adjoint** `[Ad_T] = [R, 0; [p]R, R]`. twist 변환.
- **Screw axis** `S = (ω, v)` with normalization. `T = e^{[S]θ}`.
- **Wrench** `F = (m, f)`. `F_b = [Ad_T]ᵀ F_a` (dual).

---

## Quick Reference

### 표 1. 군·대수 비교

| | Group | Lie Algebra | 차원 | 지수 |
|--|--|--|--|--|
| 회전 | `SO(3)` | `so(3)` (skew-symm) | 3 | `R = e^{[ω̂]θ}` |
| 강체변환 | `SE(3)` | `se(3)` | 6 | `T = e^{[S]θ}` |
| 평면회전 | `SO(2)` | `so(2)` | 1 | `R = e^{[ω]θ}` |
| 평면강체 | `SE(2)` | `se(2)` | 3 | — |

### 표 2. Skew-symmetric `[·]`

| 객체 | 형태 |
|--|--|
| 3-vector → so(3) | `[ω] = [[0, −ω₃, ω₂], [ω₃, 0, −ω₁], [−ω₂, ω₁, 0]]` |
| 외적 등가 | `[ω] x = ω × x` |
| 전치 | `[ω]ᵀ = −[ω]` |
| 회전 변환 | `R [ω] Rᵀ = [Rω]` |
| 제곱 | `[ω]² = ωωᵀ − \|\|ω\|\|² I` |
| 세제곱 | `[ω̂]³ = −[ω̂]` (unit vector 일 때) |

### 표 3. Rodrigues' formula 핵심

| 식 | 형태 |
|--|--|
| Forward | `R = I + sin θ [ω̂] + (1 − cos θ) [ω̂]²` |
| `tr R` | `tr R = 1 + 2 cos θ` |
| 각도 | `cos θ = (tr R − 1)/2` |
| 축 | `[ω̂] = (R − Rᵀ)/(2 sin θ)` (`θ ≠ 0, π`) |
| `R = I` | `θ = 0`, 축 미정 |
| `tr R = −1` | `θ = π`, 특수 공식 |

### 표 4. SE(3) 연산

| 연산 | 형태 |
|--|--|
| Homogeneous form | `T = [R, p; 0, 1]` (4×4) |
| 점 변환 | `x̃_a = T_{ab} x̃_b`, x̃ = (x, y, z, 1) |
| 합성 | `T_{ac} = T_{ab} T_{bc}` |
| 역원 | `T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]` |
| Subscript cancel | `T_{ab} T_{bc} = T_{ac}` |

### 표 5. Twist `V = (ω, v)`

| 정의 | 형태 |
|--|--|
| Body twist | `[V_b] = T⁻¹ Ṫ ∈ se(3)` |
| Spatial twist | `[V_s] = Ṫ T⁻¹ ∈ se(3)` |
| Frame 변환 | `V_s = [Ad_T] V_b` (T = T_{sb}) |
| `[V]` 형태 | `[V] = [[ω], v; 0, 0]` (4×4) |
| Body ang. vel. | `[ω_b] = Rᵀ Ṙ` |
| Spatial ang. vel. | `[ω_s] = Ṙ Rᵀ` |

### 표 6. Adjoint `[Ad_T]`

| 성분 | 형태 |
|--|--|
| 정의 | `[Ad_T] = [R, 0; [p]R, R]` (6×6) |
| 역 | `[Ad_T]⁻¹ = [Ad_{T⁻¹}] = [Rᵀ, 0; −Rᵀ[p], Rᵀ]` |
| Action on V | `V' = [Ad_T] V` |
| Matrix form | `[V'] = T [V] T⁻¹` |
| 합성 | `[Ad_{T₁T₂}] = [Ad_{T₁}] [Ad_{T₂}]` |

### 표 7. Screw axis `S = (ω, v)`

| 케이스 | 정규화 | v |
|--|--|--|
| 회전 있음 (h finite) | `\|\|ω\|\| = 1` | `v = −ω̂ × q + h ω̂` |
| 순수 회전 (h=0) | `\|\|ω\|\| = 1` | `v = −ω̂ × q` |
| 순수 병진 | `\|\|v\|\| = 1`, `ω = 0` | (단위 병진 방향) |

`q` = 축 위의 한 점. `h` = pitch.

### 표 8. Wrench `F = (m, f)`

| 항목 | 형태 |
|--|--|
| 6-vector | `F = (m, f)` (moment 먼저) |
| Power | `P = Fᵀ V` (frame 무관) |
| Frame 변환 | `F_b = [Ad_T]ᵀ F_a` (T = T_{ab}) |
| Equilibrium | 적용된 모든 F 의 합 = 0 |

---

## Mind Map

```
3장 Rigid-Body Motions
├─ 1. 평면 (SO(2), SE(2)) — 워밍업
├─ 2. SO(3) ─┬─ 정의 (RᵀR=I, det=+1)
│            ├─ 합성·역·subscript cancel
│            └─ 비가환! 회전 순서 중요
├─ 3. so(3) ─┬─ [ω] skew-symmetric
│            ├─ [ω]x = ω×x
│            └─ Spatial ω_s vs Body ω_b
├─ 4. SO(3) 지수 좌표 ─┬─ Rodrigues' formula
│                     ├─ matrix exp 일반론
│                     └─ log (θ=π 특수)
├─ 5. SE(3) ─┬─ [R, p; 0, 1]
│            ├─ T⁻¹ = [Rᵀ, −Rᵀp; 0, 1]
│            └─ subscript cancel (T_ab T_bc = T_ac)
├─ 6. Twist V = (ω, v) ─┬─ V_b = T⁻¹Ṫ
│                      ├─ V_s = ṪT⁻¹
│                      └─ [Ad_T] = [R, 0; [p]R, R]
├─ 7. Screw axis S ─┬─ Chasles' theorem
│                  ├─ S = (ω̂, −ω̂×q + hω̂)
│                  ├─ T = e^{[S]θ}
│                  └─ → 4장 PoE formula
└─ 8. Wrench F ─┬─ (m, f), power F·V
                ├─ F_b = [Ad_T]ᵀ F_a (dual)
                └─ → 5장 statics
```

---

## 자주 쓰는 식 모음

### 회전축 → R 변환 (Rodrigues)

```
ω̂θ ∈ R³  (3-vector exponential coord)
↓
R = I + sin θ [ω̂] + (1 − cos θ) [ω̂]²
```

### R → 회전축 변환 (log)

```
일반: cos θ = (tr R − 1)/2,  [ω̂] = (R − Rᵀ)/(2 sin θ)
R = I: θ = 0
tr R = −1: θ = π,  ω̂ 는 R 의 +1 eigenvector
```

### Screw 6-vector

```
S = (ω, v)
회전 있음: ω = ω̂, v = −ω̂ × q + h·ω̂
순수 병진: ω = 0, v = v̂ (unit)
```

### SE(3) 지수 (closed form)

```
e^{[S]θ} = [e^{[ω]θ},  G(θ) v;  0, 1]
G(θ) = Iθ + (1 − cos θ) [ω] + (θ − sin θ) [ω]²
```

### Adjoint

```
[Ad_T] = [R,       0;
          [p]R,    R]   ∈ R^{6×6}

[Ad_T]⁻¹ = [Ad_{T⁻¹}] = [Rᵀ,        0;
                         −Rᵀ[p],    Rᵀ]
```

---

## 1-line summary per section

| 절 | 한 줄 요약 |
|--|--|
| 1 | 평면 SO(2)/SE(2) 가 3D 의 작은 prototype |
| 2 | SO(3): 3×3 직교+det+1. 비가환. subscript cancel. |
| 3 | [ω] skew. [ω]x = ω×x. ω_b ≠ moving frame angular vel. |
| 4 | Rodrigues: R = I + sin θ [ω̂] + (1−cos θ)[ω̂]² |
| 5 | SE(3): [R, p; 0, 1]. T⁻¹ = [Rᵀ, −Rᵀp; 0, 1] |
| 6 | Twist V = (ω, v). V_s = [Ad_T] V_b. |
| 7 | Screw S = (ω, v) normalized. T = e^{[S]θ}. Chasles. |
| 8 | Wrench F = (m, f). F_b = [Ad_T]ᵀ F_a. Power = FᵀV. |
