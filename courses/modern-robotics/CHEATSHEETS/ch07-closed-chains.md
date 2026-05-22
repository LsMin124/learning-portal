# Ch 7 Kinematics of Closed Chains — 치트시트

## TL;DR

- **Open vs Closed**: open 은 FK 쉬움/IK 어려움, **closed 는 정반대** (FK 어려움/IK 쉬움).
- **Stewart-Gough** (6-UPS): 6 leg, 6 DoF, flight simulator.
- **Delta robot**: 3 leg parallelogram, *3 DoF translation only*, pick-and-place 챔피언.
- **5-bar linkage**: planar, Grübler `3(5−1−5)+5 = 2`, 2 actuated.
- **Loop closure constraint**: `g(θ) = 0`, R^n → R^k.
- **Singularity 3 종**: actuator (Type 1/2) / configuration / end-effector.
- **Type 2 actuator singular**: 위험 — payload 떨어짐.

---

## Quick Reference

### 표 1. Open vs Closed chain

| | Open | Closed |
|--|--|--|
| 예 | UR5, PUMA | Stewart-Gough, Delta |
| 구조 | base → ... → EE | 여러 path → EE (loop) |
| FK | PoE (easy, closed-form) | implicit (hard, numerical) |
| IK | hard (8-해) | easy (leg 독립) |
| Payload | 작음 | 큼 |
| Workspace | 큼 | 작음 |
| Stiffness | 낮음 | 높음 |
| Singularity | 1 종 | 3 종 |

### 표 2. 대표 closed-chain robots

| Robot | 구조 | DoF | 응용 |
|--|--|--|--|
| Stewart-Gough | 6-UPS | 6 | flight simulator, machine tool |
| Delta | 3 leg parallelogram | 3 (T only) | pick-and-place |
| 5-bar (planar) | 5 link | 2 | educational, manipulanda |
| 6-RUS | 6 leg RUS | 6 | research |
| Diamond, Tricept | varied | 3~6 | machining |

### 표 3. Stewart-Gough Grübler

```
N = 14 (base + top + 12 link)
J = 18 (6 leg × 3 joint)
Σ f_i = 36 (each leg: U=2 + P=1 + S=3 = 6)
DoF = 6(14 − 1 − 18) + 36 = 6
```

### 표 4. 5-bar Grübler

```
N = 5, J = 5, Σ f_i = 5 (all revolute)
DoF = 3(5 − 1 − 5) + 5 = 2
→ 2 actuated joint
```

### 표 5. Stewart-Gough IK (closed-form!)

```
For i = 1..6:
    L_i = ‖p + R · t_i − b_i‖

p, R: platform pose (input)
b_i: base attachment point (constant)
t_i: top attachment point (in platform frame)
L_i: i-번째 leg length (output)
```

→ 6 closed-form 계산. Real-time 1kHz.

### 표 6. Singularity 3 종

| Type | 정의 | 결과 | 위험 |
|--|--|--|--|
| Actuator Type 1 | actuator motion 만들어도 EE 정지 | input loss | medium |
| Actuator Type 2 | actuator fixed 인데 EE motion | uncontrolled DoF | **high** |
| Configuration | Jacobian rank loss | 일부 motion 불가 | medium |
| End-effector | self-motion | redundant joint motion | medium |

### 표 7. FK 의 numerical 해법

```python
# Stewart-Gough FK via Newton-Raphson
def closed_chain_fk(L_target, T_init):
    T = T_init
    for _ in range(20):
        L_curr = stewart_ik(T)              # 6 leg lengths
        e = L_target - L_curr
        if ‖e‖ < tol: return T
        J = stewart_jacobian(T)              # 6×6
        dV = solve(J, e)                     # body twist update
        T = T @ matrix_exp_se3(dV)
    return None
```

---

## Mind Map

```
7장 Kinematics of Closed Chains
├─ 1. Open vs Closed (FK/IK reversal)
├─ 2. 대표 robot
│   ├─ Stewart-Gough (6-UPS, 6 DoF)
│   ├─ Delta (3 leg, 3 T DoF)
│   └─ 5-bar (planar, 2 DoF)
├─ 3. FK / IK
│   ├─ IK: leg 독립, closed-form
│   └─ FK: loop closure → numerical
├─ 4. Differential kinematics
│   ├─ Constraint Jacobian A(θ)
│   └─ Actuated vs passive joint
├─ 5. Singularity 3 종
│   ├─ Actuator Type 1 / Type 2
│   ├─ Configuration
│   └─ End-effector
└─ 6. Hybrid open-closed
    ├─ Cooperative manipulation
    ├─ Quadruped stance
    └─ Humanoid double-support
```

---

## 자주 쓰는 식

### Stewart-Gough IK (full code)

```python
def stewart_ik(R, p, b, t):
    """
    R: 3x3 platform rotation (in base frame)
    p: 3 platform position (in base frame)
    b: 6x3 base attachment points (in base frame)
    t: 6x3 top attachment points (in platform frame)
    Returns: 6 leg lengths
    """
    L = np.zeros(6)
    for i in range(6):
        leg_vector = p + R @ t[i] - b[i]
        L[i] = np.linalg.norm(leg_vector)
    return L
```

### Stewart-Gough Jacobian

```python
def stewart_jacobian(R, p, b, t):
    """
    Returns: 6x6 J such that L_dot = J @ V_body
    Each row = i-번째 leg 의 unit screw axis projection
    """
    J = np.zeros((6, 6))
    for i in range(6):
        leg = p + R @ t[i] - b[i]
        leg_unit = leg / np.linalg.norm(leg)
        # body-frame contributions
        moment = np.cross(R @ t[i], leg_unit)
        force  = leg_unit
        J[i] = np.concatenate([moment, force])
    return J
```

### 5-bar IK (closed-form)

```python
def five_bar_ik(x, y, L1, L2, L3, L4, d):
    """좌측·우측 actuator (θ_1, θ_3) 각도"""
    # 좌측 leg
    D1 = math.hypot(x, y)
    cos_alpha1 = (D1**2 - L1**2 - L2**2) / (2*L1*L2)
    alpha1 = math.acos(cos_alpha1)  # elbow angle
    theta1 = math.atan2(y, x) - math.atan2(L2*math.sin(alpha1), L1 + L2*math.cos(alpha1))

    # 우측 leg
    D2 = math.hypot(x - d, y)
    cos_alpha2 = (D2**2 - L3**2 - L4**2) / (2*L3*L4)
    alpha2 = math.acos(cos_alpha2)
    theta3 = math.atan2(y, x - d) + math.atan2(L4*math.sin(alpha2), L3 + L4*math.cos(alpha2))

    return theta1, theta3
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | Open: FK 쉬움, Closed: IK 쉬움 (reversal) |
| 2 | Stewart 6-DoF, Delta 3-DoF T, 5-bar 2-DoF |
| 3 | Loop closure g(θ)=0, IK leg-independent, FK numerical |
| 4 | Constraint Jacobian A(θ) θ̇ = 0 |
| 5 | Singularity 3 종, Type 2 actuator 위험 |
| 6 | Hybrid: quadruped stance, dual-arm grasp |
