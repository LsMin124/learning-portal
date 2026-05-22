# Ch 13 Wheeled Mobile Robots — 치트시트

## TL;DR

- **3 종 mobile robot**: omnidirectional / differential-drive / car-like (Ackermann)
- **Wheel**: fixed / steerable / omniwheel / mecanum / castor
- **Differential-drive**: `v = r(ω_L+ω_R)/2`, `ω_z = r(ω_R−ω_L)/(2L)`. nonholonomic (`v_y = 0`).
- **Car-like**: `R = L/tan φ`. min R 작을수록 좁은 회전.
- **Mecanum**: holonomic — sideways 가능. `H ∈ R^{4×3}` over-determined.
- **Odometry**: encoder → pose, *drift 누적*. SLAM 으로 보정.
- **Brockett**: nonholonomic → smooth time-invariant feedback 불가.

---

## Quick Reference

### 표 1. 3 종 mobile robot

| Type | Wheel | DoF | Holonomic | 예 |
|--|--|--|--|--|
| Omnidirectional | 3+ omni / mecanum | 3 | ✓ | YouBot |
| Differential-drive | 2 fixed + castor | 2 (3 reachable) | ✗ | Roomba, TurtleBot |
| Car-like (Ackermann) | 2 fixed + 2 steered | 2 (3 reachable) | ✗ | car |

### 표 2. Wheel 종류

| Wheel | Constraint | Use |
|--|--|--|
| Fixed | 평면 안 motion 만 | 자동차 뒤 |
| Steered | 평면 + steering | 자동차 앞 |
| Omniwheel | 모든 방향 passive roll | YouBot, omni base |
| Mecanum | 45° roller, holonomic 조합 | YouBot, AGV |
| Castor | passive support | Roomba 뒤 |

### 표 3. Differential-drive kinematics

| | 식 |
|--|--|
| Forward (wheel → chassis) | `v = r(ω_L+ω_R)/2`, `ω_z = r(ω_R−ω_L)/(2L)` |
| Inverse | `ω_L = (v − L ω_z)/r`, `ω_R = (v + L ω_z)/r` |
| Body twist | `(0, v, 0, ω_z)` (ω_y, v_x, v_y, ω_z 순) — `v_y = 0` |
| World | `ẋ = v cos θ`, `ẏ = v sin θ`, `θ̇ = ω_z` |
| Constraint | `ẋ sin θ − ẏ cos θ = 0` (Pfaffian) |

### 표 4. Car-like kinematics

| | 식 |
|--|--|
| Forward | `ẋ = v cos θ`, `ẏ = v sin θ`, `θ̇ = v tan φ / L` |
| Turning radius | `R = L / tan φ` |
| φ → 0 | 직진 (R → ∞) |
| φ → π/2 | 순간 회전 (R → 0, mechanical limit) |
| Constraint | `v_y = 0` (body), `ẋ sin θ − ẏ cos θ = 0` (world) |

### 표 5. Omnidirectional 3-wheel symmetric

| 변수 | 값 |
|--|--|
| Wheel 배치 | 120° 간격, radius `d` |
| H | 3×3, invertible |
| Body twist | `(ω_z, v_x, v_y)` ∈ R³ — all controllable |
| Wheel ω | `H · V` |

### 표 6. Mecanum 4-wheel

| 변수 | 값 |
|--|--|
| H | 4×3 (over-determined) |
| Forward | `V = H⁺ u` (least-squares) |
| Inverse | `u = H V` (unique) |
| Slip risk | high speed, asymmetric load |

### 표 7. Odometry algorithm

```
init: x̂ = 0, ŷ = 0, θ̂ = 0

while operating:
    Δφ_L, Δφ_R = encoder difference
    Δs = r(Δφ_L + Δφ_R) / 2
    Δθ = r(Δφ_R − Δφ_L) / (2L)
    x̂ += Δs · cos(θ̂ + Δθ/2)
    ŷ += Δs · sin(θ̂ + Δθ/2)
    θ̂ += Δθ
```

drift 누적 — 외부 sensor (LiDAR/camera/IMU) + SLAM 필요.

---

## Mind Map

```
13장 Wheeled Mobile Robots
├─ 1. Wheel 종류 (fixed/steered/omni/mecanum/castor)
├─ 2. Omnidirectional (3-wheel/Mecanum)
│   └─ holonomic, H invertible/pinv
├─ 3. Differential-drive
│   ├─ Kinematics: v, ω_z
│   ├─ Nonholonomic: v_y = 0
│   └─ World: ẋ=vcosθ, ẏ=vsinθ
├─ 4. Car-like (Ackermann)
│   ├─ Steering φ
│   └─ R = L/tan φ
├─ 5. Odometry (drift)
│   └─ → SLAM 보정
├─ 6. Motion control
│   ├─ Holonomic: direct PID
│   ├─ Nonholonomic: time-varying / discontinuous
│   └─ Brockett's theorem
└─ 7. Mobile manipulation (base + arm, redundancy)
```

---

## 자주 쓰는 식

### Differential-drive control (linearized)

```python
def diff_drive_control(x, y, theta, x_d, y_d, v_d, omega_d, Kx, Ky, Kth):
    e_x = (x_d - x) * cos(theta) + (y_d - y) * sin(theta)
    e_y = -(x_d - x) * sin(theta) + (y_d - y) * cos(theta)
    v   = Kx * e_x + v_d
    omega = Ky * v_d * e_y + Kth * sin(theta_d - theta) + omega_d
    return v, omega
```

### Car-like motion model

```python
def car_dynamics(x, y, theta, v, phi, L, dt):
    x_new     = x + v * cos(theta) * dt
    y_new     = y + v * sin(theta) * dt
    theta_new = theta + (v / L) * tan(phi) * dt
    return x_new, y_new, theta_new
```

### Mecanum inverse kinematics (YouBot-like)

```python
def mecanum_inverse(vx, vy, omega_z, r, l, w):
    # l = half wheel base, w = half wheel track
    H = (1/r) * np.array([
        [-l - w, 1, -1],
        [ l + w, 1,  1],
        [ l + w, 1, -1],
        [-l - w, 1,  1],
    ])
    return H @ np.array([omega_z, vx, vy])
```

### Mobile manipulator EE Jacobian

```
V_e = J_base(θ_base) · (v_x, v_y, ω_z) + J_arm(θ_arm) · θ̇_arm
        ↑                ↑
        6×3              6×n
```

---

## 1-line summary per section

| 절 | 요약 |
|--|--|
| 1 | Wheel: fixed/steered/omni/mecanum/castor |
| 2 | Omni 3-wheel: H 3×3 invertible, holonomic |
| 3 | Differential-drive: v = r(ω_L+ω_R)/2, nonholonomic v_y=0 |
| 4 | Car-like: R = L/tan φ, Ackermann |
| 5 | Odometry drift → SLAM 보정 |
| 6 | Nonholonomic control: time-varying (Brockett) |
| 7 | Mobile manipulation: base 3 + arm 6, redundancy 3 |
