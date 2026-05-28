# Ch 5 Velocity Kinematics — 치트시트

## TL;DR

- `V = J(θ) θ̇` — Jacobian 의 정의식
- `J_s` (Space Jacobian): `V_s = J_s θ̇`, 컬럼이 *현재* configuration 의 spatial screw axis
- `J_b` (Body Jacobian): `V_b = J_b θ̇`, 컬럼이 *현재* body screw axis
- 관계: `J_s = [Ad_{T_{sb}}] J_b`
- Singularity: `rank J < min(6, n)` → velocity ellipsoid degenerate
- Statics: `τ = Jᵀ F` (`J` 와 `F` 같은 frame!)

---

## Quick Reference

### 표 1. Jacobian 핵심

| | Space `J_s` | Body `J_b` |
|--|--|--|
| 분해 | `V_s = J_s θ̇` | `V_b = J_b θ̇` |
| 차원 | `6 × n` | `6 × n` |
| Col 1 | `J_{s,1} = S_1` (그대로) | `J_{b,1}` (가장 누적) |
| Col n | `J_{s,n}` (가장 누적) | `J_{b,n} = B_n` (그대로) |
| 적용 | 외부 관찰, 시뮬레이션 | EE 시점, IK iteration, force sensor |

### 표 2. 컬럼 공식

| | Space | Body |
|--|--|--|
| Col i | `[Ad_{e^{[S_1]θ_1} ⋯ e^{[S_{i-1}]θ_{i-1}}}] S_i` | `[Ad_{e^{-[B_{i+1}]θ_{i+1}} ⋯ e^{-[B_n]θ_n}}] B_i` |

### 표 3. Singularity 검출

| 방법 | 조건 | 적용 |
|--|--|--|
| $\det J$ | $\lvert \det J \rvert < \epsilon$ | n = 6 only |
| $\det(J J^T)$ | $\lvert \det(J J^T) \rvert < \epsilon$ | n ≥ 6 |
| Rank | `rank J < min(6, n)` | 일반 |
| SVD | `σ_min < ε` | 가장 robust |

### 표 4. 흔한 singularity (6R arm)

| 종류 | 발생 | 손실 방향 |
|--|--|--|
| Wrist | 마지막 3 회전 축 정렬 | 한 회전 자유도 |
| Elbow | 팔 완전 펼침/접힘 | 길이 방향 velocity |
| Shoulder | 첫 두 축 평행 | 한 회전 방향 |

### 표 5. Manipulability 지표

| 지표 | 정의 | 의미 |
|--|--|--|
| Yoshikawa | `μ = √det(J Jᵀ)` | ellipsoid 부피 |
| Condition | `κ = σ_max / σ_min` | aspect ratio |
| Min σ | `σ_min` | singularity 거리 |

### 표 6. Statics 일관성

| `J` | `F` | `τ = Jᵀ F` 가능? |
|--|--|--|
| `J_s` | `F_s` | ✓ |
| `J_b` | `F_b` | ✓ |
| `J_s` | `F_b` | ✗ (frame 변환 먼저) |
| `J_b` | `F_s` | ✗ (frame 변환 먼저) |

변환: `F_a = [Ad_{T_{ba}}]ᵀ F_b`.

---

## Mind Map

```
5장 Velocity Kinematics
├─ Jacobian J(θ) — V = J θ̇
├─ Space Jacobian J_s ─ 컬럼: 현재 spatial screw
├─ Body Jacobian J_b ─ 컬럼: 현재 body screw
├─ J_s = [Ad_T_sb] J_b
├─ Singularity ─ rank J < min(6, n)
│   ├─ Wrist / Elbow / Shoulder
│   └─ damped least-squares 로 회피
├─ Manipulability ellipsoid
│   ├─ Yoshikawa √det(JJᵀ)
│   └─ Velocity ↔ Force ellipsoid 쌍대
└─ Statics τ = Jᵀ F (같은 frame!)
```

---

## 자주 쓰는 식

### Damped least-squares (singular 회피)

```
θ̇ = Jᵀ (J Jᵀ + λ² I)⁻¹ V_d
```

### Pseudoinverse (redundant arm)

```
θ̇ = J⁺ V_d + (I − J⁺ J) θ̇_0   # null-space task
```

`J⁺ = Jᵀ (J Jᵀ)⁻¹` (right pseudoinverse for n > 6).

### Force control basic

```
τ_d = Jᵀ F_d           # desired force → joint torque
```

### Frame 변환 (J)

```
J_s = [Ad_{T_sb(θ)}] J_b
J_b = [Ad_{T_bs(θ)}] J_s
```

### Frame 변환 (F)

```
F_s = [Ad_{T_bs}]ᵀ F_b
F_b = [Ad_{T_sb}]ᵀ F_s
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | 2R planar 예제로 `V = J θ̇` 직관 |
| 2 | `J_s` 컬럼 = 현재 config 의 spatial screw axis |
| 3 | `J_b` 컬럼 = 현재 config 의 body screw axis |
| 4 | `J_s = [Ad_T_sb] J_b` (twist 변환의 일반화) |
| 5 | Singularity = rank loss, ellipsoid degenerate |
| 6 | Manipulability ellipsoid = velocity 지향성 |
| 7 | `τ = Jᵀ F` (가상일 원리, 같은 frame) |
