# Chapter 13: Wheeled Mobile Robots — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 13: Wheeled Mobile Robots** (책 p.513~568) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 13장의 핵심: *바퀴를 가진 robot* 의 kinematics, dynamics, control. 특히 **nonholonomic constraint** (2장 의 자동차 예시 의 일반화) 와 **mobile manipulation** (모바일 base + arm).

## 들어가기 전에

- **선수 지식**
  - **2장**: Holonomic vs nonholonomic constraint, Pfaffian form
  - **3장**: SE(2) (평면 강체 변환)
  - **9~11장**: Trajectory generation, control
- **학습 목표**
  1. **Wheel 종류** — fixed, steerable, omnidirectional
  2. 3 종 mobile robot — **omnidirectional**, **differential-drive**, **car-like** (Ackermann)
  3. **Forward / inverse kinematics** — wheel velocity ↔ chassis velocity
  4. **Odometry** — wheel encoder → pose estimation (with drift)
  5. **Motion control of mobile robot** — feedback for tracking
  6. **Mobile manipulation** — base + arm 의 redundancy
- **예상 학습 시간**: 100~120분

---

## 1. Wheel 종류

### 1.1 Standard wheel

- **Fixed wheel**: 회전 축이 *chassis 에 고정*. 예 — 자동차 뒷바퀴.
- **Steered wheel**: 회전 축이 *steering 으로 변함*. 예 — 자동차 앞바퀴.

constraint: *바퀴의 평면 안* 의 motion 만 (sideways slip 금지).

### 1.2 Omniwheel / Mecanum wheel

![Figure 13.1 — Mecanum wheel 의 sideways rolling. 교재 p.514](/courses/modern-robotics/figures/ch13/fig-13-1.png)

- **Omniwheel**: roller 가 바퀴 *둘레* 에 부착, 어느 방향이든 *수동* 으로 굴러감
- **Mecanum**: roller 가 45° 비스듬히 배치, *4 wheel 조합* 으로 *holonomic* motion

omniwheel/mecanum 의 *큰 장점*: **holonomic** mobile robot — sideways 도 자유롭게.

### 1.3 Castor wheel

passive, *supporting* 용도. kinematics 에 직접 기여 X.

---

## 2. Omnidirectional Mobile Robot

### 2.1 KUKA YouBot, 3-wheel omni 등

3+ omniwheel 로 구성. 3 DoF (x, y, θ) 모두 *독립 제어*.

### 2.2 Kinematics (3-wheel symmetric)

각 wheel velocity `ω_i` ↔ chassis velocity `(ω_z, v_x, v_y)`:

$$\begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \end{bmatrix} = H(0) \begin{bmatrix} \omega_z \\ v_x \\ v_y \end{bmatrix}, \quad H(0) \in \mathbb{R}^{3 \times 3}$$

`H(0)` 는 wheel 배치에 의해 결정. invertible → forward / inverse 모두 가능.

![Figure 13.4 — Omnidirectional 3-wheel symmetric. 교재 p.518](/courses/modern-robotics/figures/ch13/fig-13-4.png)

### 2.3 Mecanum 4-wheel

$$\begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \\ \omega_4 \end{bmatrix} = H(\phi) \begin{bmatrix} \omega_z \\ v_x \\ v_y \end{bmatrix}, \quad H \in \mathbb{R}^{4 \times 3}$$

4 wheel → 3 chassis DoF. *over-determined*, pseudoinverse 로 풀이.

---

## 3. Differential-Drive Robot

### 3.1 구조

2 개의 *수직 axis* 의 wheel (왼쪽·오른쪽) + castor.

예: TurtleBot, Roomba, Pioneer.

### 3.2 Kinematics

wheel 반지름 `r`, wheel base `2L`. wheel 각속도 `(ω_L, ω_R)`:

$$v = \frac{r(\omega_L + \omega_R)}{2}, \quad \omega_z = \frac{r(\omega_R - \omega_L)}{2L}$$

chassis velocity in body frame:

$$\begin{bmatrix} \omega_z \\ v_x \\ v_y \end{bmatrix} = \begin{bmatrix} -r/(2L) & r/(2L) \\ r/2 & r/2 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \omega_L \\ \omega_R \end{bmatrix}$$

`v_y = 0`: **nonholonomic constraint** — sideways motion 불가!

### 3.3 World frame

$$\dot{x} = v \cos\theta, \quad \dot{y} = v \sin\theta, \quad \dot\theta = \omega_z$$

`(x, y, θ)` 공간에서 *어디든* 갈 수 있지만 *직접* 직진/회전 조합 필요.

---

## 4. Car-like Robot (Ackermann)

### 4.1 구조

뒷바퀴 fixed + 앞바퀴 steered. 자동차의 단순화.

### 4.2 Kinematics

steering 각 `φ`, wheel base `L`, longitudinal speed `v`:

$$\dot{x} = v \cos\theta, \quad \dot{y} = v \sin\theta, \quad \dot\theta = \frac{v}{L} \tan\phi$$

회전 반지름: `R = L / tan φ`. min R 가 *작을수록* 작은 회전 가능 (Ackermann 한계).

### 4.3 Parking — 평행주차

car-like 의 *직접 sideways 불가* 하나 (`v_y = 0`), *forward+steering* 의 조합으로 평행주차 가능. **controllable** but *path 가 complex*.

---

## 5. Odometry

### 5.1 정의

> Wheel encoder 의 누적 → pose estimate `(x̂, ŷ, θ̂)` 계산.

### 5.2 Differential-drive odometry

Δt 동안 wheel 회전 `Δφ_L, Δφ_R`:

$$\Delta s = \frac{r(\Delta\phi_L + \Delta\phi_R)}{2}, \quad \Delta\theta = \frac{r(\Delta\phi_R - \Delta\phi_L)}{2L}$$

$$\hat{x} += \Delta s \cos(\hat\theta + \Delta\theta/2), \quad \hat{y} += \Delta s \sin(\hat\theta + \Delta\theta/2), \quad \hat\theta += \Delta\theta$$

### 5.3 Drift

odometry 의 *치명적 단점*: error 가 *누적*. 멀리 갈수록 부정확.

해결:
- IMU 융합 (gyro + accelerometer)
- *외부 sensor* — LiDAR, camera, GPS, AprilTag
- **SLAM** (Simultaneous Localization And Mapping)

---

## 6. Motion Control of Mobile Robots

### 6.1 Holonomic (omnidirectional)

PID 직접 가능 — 3 DoF 모두 독립:

$$\dot\theta_z = K_\theta (\theta_d - \theta), \quad \dot{x} = K_x (x_d - x), \quad \dot{y} = K_y (y_d - y)$$

### 6.2 Nonholonomic (differential-drive, car-like)

`v_y = 0` constraint 로 직접 sideways 불가. *time-varying* controller 필요.

**Linearization 기반**:

$$v = K_x (x_d - x) \cos\theta + K_y (y_d - y) \sin\theta + v_d$$
$$\omega = K_\theta (\theta_d - \theta) + \omega_d$$

또는 **chained form transformation** (Brockett's theorem):

nonholonomic system 은 *smooth time-invariant* feedback 으로 *stabilize 불가*. *time-varying* 또는 *discontinuous* controller 필요. 책 §13.4.

![Figure 13.10 — Nonholonomic robot 의 tracking control 예제. 교재 p.543](/courses/modern-robotics/figures/ch13/fig-13-10.png)

---

## 7. Mobile Manipulation

### 7.1 Configuration

mobile base `(x, y, θ) ∈ SE(2)` + arm `θ_arm ∈ R^n`. 총 `n + 3` configuration variables.

### 7.2 EE Jacobian

end-effector 의 spatial velocity = base contribution + arm contribution:

$$\mathcal{V}_e = J_{base}(\theta_{base}) \dot\theta_{base} + J_{arm}(\theta_{arm}) \dot\theta_{arm}$$

### 7.3 Redundancy

3 DoF base + 6 DoF arm = 9 DoF, EE pose = 6 → **3 차원 redundancy**. base 와 arm 의 *역할 분담* 가능:
- base: *coarse 위치*
- arm: *fine manipulation*

### 7.4 응용

- mobile manipulator (Toyota HSR, Fetch)
- autonomous warehouse robot (Amazon Kiva)
- humanoid (Boston Dynamics Atlas, Tesla Optimus)

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Differential-drive 가 *holonomic* | nonholonomic — `v_y = 0`. sideways 직접 불가. |
| 2 | Mecanum / Omniwheel 도 nonholonomic | holonomic — sideways 자유 (rollers). |
| 3 | Odometry 가 절대 위치 | drift 누적 — 외부 sensor 융합 필수. |
| 4 | Car-like 가 좁은 공간에서 *어디든* 빠르게 갈 수 있음 | controllable 이긴 하나 *parallel parking* 등 *복잡한 maneuvering* 필요. |
| 5 | Nonholonomic 의 *간단한* PID 가 작동 | Brockett's theorem — smooth time-invariant feedback 불가. time-varying 또는 discontinuous. |
| 6 | Mobile base 가 *항상 평면* | 비탈, slip, soft terrain 에서 model 깨짐. |
| 7 | Castor wheel 가 kinematics 에 영향 | passive — kinematics 영향 거의 없음 (지원만). |
| 8 | 4 wheel Mecanum 의 `H` 가 *정사각형* | 4×3 (over-determined). pseudoinverse. |
| 9 | Mobile manipulation 의 base 와 arm 이 *독립* | EE pose 는 *coupled*. Jacobian 분해. |
| 10 | SLAM 이 odometry 대체 | 보완 — SLAM 도 *initial odometry* 기반, 외부 sensor 로 *보정*. |

---

## 자가점검

1. Holonomic 과 nonholonomic mobile robot 의 차이 (예시 포함).
2. Differential-drive 의 wheel velocity → chassis velocity 식.
3. Differential-drive 의 nonholonomic constraint 식.
4. Car-like robot 의 turning radius `R` 식.
5. Mecanum wheel 의 *holonomicity* 이유.
6. Odometry 의 *drift* 원인 + 해결.
7. Brockett's theorem 의 대략 의미.
8. Mobile manipulation 의 redundancy 차원.
9. Omnidirectional 3-wheel 의 H 가 *정사각형* 인지 검토.
10. Castor wheel 의 역할.

### 해답 (간략)

1. Holonomic: 모든 방향 직접 motion 가능 (omniwheel). Nonholonomic: 일부 방향 제약 (differential-drive 의 `v_y = 0`).
2. `v = r(ω_L + ω_R)/2`, `ω_z = r(ω_R − ω_L)/(2L)`.
3. body frame: `v_y = 0`. world frame: `ẋ sin θ − ẏ cos θ = 0`.
4. `R = L / tan φ`. φ = steering 각, L = wheel base.
5. roller 가 sideways direction 에 *수동 회전* — wheel 의 forward 회전 동안 chassis 가 *어느 방향이든* slip 없이 이동 가능.
6. Wheel slip, encoder noise, calibration error 누적. IMU 융합, 외부 sensor (LiDAR, GPS, SLAM) 로 보정.
7. Nonholonomic system 은 *smooth time-invariant state feedback* 으로 stabilize 할 수 없음. time-varying 또는 discontinuous controller 필요.
8. 3 (base 3 + arm 6 − EE 6).
9. 3-wheel symmetric: 3×3 정사각형, invertible. 4-wheel mecanum: 4×3.
10. Passive support — kinematics 영향 거의 없음, 지지 역할만.

---

## 다음 학습으로

- **SLAM** — Simultaneous Localization And Mapping. odometry + camera/LiDAR.
- **Autonomous driving** — Ackermann 의 정밀 control, perception, planning 통합.
- **Humanoid locomotion** — bipedal walking 의 nonholonomic-like constraints.
- **RL for mobile robots** — autonomous navigation 의 end-to-end learning.
