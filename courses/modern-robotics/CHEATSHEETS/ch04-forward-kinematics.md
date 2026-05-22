# Ch 4 Forward Kinematics — 치트시트

## TL;DR

- **FK** = `θ → T_{sb}(θ)`. (IK 는 6장)
- **PoE Space form**: `T(θ) = e^{[S₁]θ₁} ⋯ e^{[Sₙ]θₙ} M`
- **PoE Body form**: `T(θ) = M e^{[B₁]θ₁} ⋯ e^{[Bₙ]θₙ}`
- `M` = zero-position `T_{sb}(0)`. `S_i, B_i` = zero-position screw axes.
- 관계: `B_i = [Ad_{M⁻¹}] S_i`
- DH 대비 PoE 의 장점: frame 임의성 제거, 기하 직관 명확
- URDF = ROS 의 robot XML, joint·link 정의

---

## Quick Reference

### 표 1. PoE Space form 핵심

| 항목 | 형태 |
|--|--|
| 식 | `T(θ) = e^{[S₁]θ₁} ⋯ e^{[Sₙ]θₙ} M` |
| `M` | zero-position end-effector pose `T_{sb}(0)` |
| `S_i` (회전) | `(ω̂, −ω̂ × q)` (q = 축 위 한 점, `{s}` 좌표) |
| `S_i` (병진) | `(0, v̂)` |
| 순서 | `S₁` 이 가장 왼쪽 (반복 시 reversed iter) |

### 표 2. PoE Body form 핵심

| 항목 | 형태 |
|--|--|
| 식 | `T(θ) = M e^{[B₁]θ₁} ⋯ e^{[Bₙ]θₙ}` |
| `B_i` | 같은 joint 의 screw axis, `{b}` 에서 |
| 변환 | `B_i = [Ad_{M⁻¹}] S_i` |
| 순서 | `B₁` 이 *M 바로 다음*, forward iter |

### 표 3. Screw axis identification

| Joint 타입 | ω | v |
|--|--|--|
| Revolute | unit `ω̂` (회전축 방향) | `−ω̂ × q` (q = 축 위 한 점) |
| Prismatic | `0` | unit `v̂` (병진 방향) |
| Helical | unit `ω̂` | `−ω̂ × q + h·ω̂` |

### 표 4. 평면 3R arm 의 PoE

zero position 에서 모든 link 가 `+x̂` 방향, link 길이 `L₁`, `L₂`, `L₃`.

| 객체 | 값 |
|--|--|
| `M` | `[I, (L₁+L₂+L₃, 0, 0); 0, 1]` |
| `S₁` | `(0, 0, 1, 0, 0, 0)` |
| `S₂` | `(0, 0, 1, 0, −L₁, 0)` |
| `S₃` | `(0, 0, 1, 0, −(L₁+L₂), 0)` |

### 표 5. PoE vs DH

| 측면 | DH | PoE |
|--|--|--|
| 좌표계 부여 | 각 link 마다 | `{s}`, `{b}` 둘만 |
| 파라미터 / joint | 4 (α, a, d, θ) | 6 (screw axis 의 ω, v) |
| 총 파라미터 (n-joint) | 4n | 6n + 6 |
| 기하 직관 | 약함 | 강함 (실제 축이 보임) |
| Prismatic vs Revolute | 다른 표기 | 동일 framework |
| Convention 임의성 | classical vs modified | 거의 없음 |
| URDF 호환 | 자연 (axis 직접) | parsing 부담 |

### 표 6. URDF 핵심 elements

| Element | 의미 |
|--|--|
| `<robot>` | top-level container |
| `<link>` | rigid body (mass, inertia, visual, collision) |
| `<joint>` | parent ↔ child link 의 변환 정의 |
| `joint.type` | `revolute` / `prismatic` / `fixed` / `continuous` |
| `joint.axis` | 회전/병진 축, *parent link frame 기준* |
| `joint.origin` | parent → child 의 변환 (xyz + rpy) |
| `joint.limit` | θ 범위, effort, velocity |
| `link.inertial` | 8장 dynamics 에서 사용 |

---

## Mind Map

```
4장 Forward Kinematics
├─ 1. 정의: θ → T_sb(θ)
├─ 2. 직관: 3R planar arm (chain of T_{i,i+1})
├─ 3. PoE Space form
│   ├─ T = e^[S1]θ1 ⋯ e^[Sn]θn · M
│   ├─ S_i = zero-position screw axis (in {s})
│   └─ M = T_sb(0)
├─ 4. PoE Body form
│   ├─ T = M · e^[B1]θ1 ⋯ e^[Bn]θn
│   └─ B_i = [Ad_M⁻¹] S_i
├─ 5. 예제: 3R planar / 3R spatial / UR5 / WAM
├─ 6. DH vs PoE 비교
└─ 7. URDF 형식 (산업 표준)
```

---

## 자주 쓰는 식 모음

### Space form FK (의사코드)

```
T = M
for i = n downto 1:           # 역방향 iter
    T = expm6(S_i, θ_i) @ T
return T
```

또는

```
T = I
for i = 1 to n:                # 정방향 iter, T 오른쪽 곱
    T = T @ expm6(S_i, θ_i)
T = T @ M
return T
```

### Body form FK (의사코드)

```
T = M
for i = 1 to n:                # 정방향, T 오른쪽 곱
    T = T @ expm6(B_i, θ_i)
return T
```

### screw axis `(ω, v)` from URDF

```
# parent link frame 의 cumulative transform = T_s,parent (already known)
joint.axis_in_s = R_s,parent @ joint.axis        # rotate to {s}
joint.origin_in_s = T_s,parent @ joint.origin    # translate to {s}

if joint.type == "revolute":
    ω = joint.axis_in_s / ||joint.axis_in_s||
    q = joint.origin_in_s
    v = -cross(ω, q)
elif joint.type == "prismatic":
    ω = 0
    v = joint.axis_in_s / ||joint.axis_in_s||

S_i = (ω, v)
```

### `[Ad_T]` for Body form conversion

```
[Ad_M⁻¹] = [Rᵀ,       0;
            -Rᵀ[p],   Rᵀ]   where T_sb(0) = M = [R, p; 0, 1]

B_i = [Ad_M⁻¹] @ S_i
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | FK 는 `θ → T_sb` 의 forward 함수 |
| 2 | 3R planar arm 으로 chain-of-T 직관 |
| 3 | PoE Space: `e^[S1]θ1 ⋯ e^[Sn]θn M`. S_i in {s}. |
| 4 | PoE Body: `M e^[B1]θ1 ⋯ e^[Bn]θn`. B_i = [Ad_M⁻¹]S_i. |
| 5 | UR5 6R 예제 — 산업 적용 |
| 6 | PoE > DH: frame 임의성 ↓, 직관 ↑, prismatic 통일 |
| 7 | URDF 는 ROS 의 robot XML, joint.axis 는 parent frame 기준 |
