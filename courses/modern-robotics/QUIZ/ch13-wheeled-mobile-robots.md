# Ch 13 Wheeled Mobile Robots — 퀴즈

> 10 문항.

### Q1. Holonomic vs Nonholonomic 구분

다음 robot 들을 holonomic / nonholonomic 분류.
(a) Roomba (2-wheel + castor)
(b) KUKA YouBot (4-wheel mecanum)
(c) Tesla Model S
(d) ASIMO (bipedal)

<details><summary>답</summary>

(a) Roomba — **nonholonomic** (differential-drive, `v_y = 0`)
(b) YouBot — **holonomic** (mecanum, sideways 가능)
(c) Tesla Model S — **nonholonomic** (Ackermann)
(d) ASIMO — *bipedal* 은 mobile robot 범주에 정확히 안 들어감. 단, *body 의 motion* 만 보면 nonholonomic-like.

</details>

### Q2. Differential-drive forward kinematics

`r = 0.05 m`, `L = 0.2 m`. `ω_L = 5 rad/s`, `ω_R = 10 rad/s`. chassis `(v, ω_z)`.

<details><summary>답</summary>

`v = r(ω_L + ω_R)/2 = 0.05 · (5 + 10)/2 = 0.375 m/s`.

`ω_z = r(ω_R − ω_L)/(2L) = 0.05 · (10 − 5)/(2 · 0.2) = 0.625 rad/s`.

Body frame velocity: `(v_x, v_y, ω_z) = (0.375, 0, 0.625)`. → 우측 더 빠르므로 robot 이 좌회전하며 전진.

</details>

### Q3. Differential-drive inverse kinematics

원하는 `v = 0.5 m/s`, `ω_z = 1 rad/s`, 같은 `r, L`. `ω_L, ω_R`.

<details><summary>답</summary>

`ω_L = (2v − 2L ω_z) / (2r) = (v − L ω_z)/r = (0.5 − 0.2)/0.05 = 6 rad/s`.

`ω_R = (v + L ω_z)/r = (0.5 + 0.2)/0.05 = 14 rad/s`.

검증: `(ω_L + ω_R) r / 2 = (6+14)·0.05/2 = 0.5 ✓`. `(ω_R − ω_L) r/(2L) = 8·0.05/0.4 = 1 ✓`.

</details>

### Q4. Car-like turning radius

`L = 2.5 m`, `φ = 30°`. turning radius `R`.

<details><summary>답</summary>

`R = L / tan φ = 2.5 / tan(30°) = 2.5 / 0.577 ≈ 4.33 m`.

min R 가 작을수록 좁은 공간 회전 가능. 보통 sedan 의 `R_min ≈ 5~6 m`.

`φ → 0`: 직진 (`R → ∞`). `φ → π/2`: *순간 회전* (`R → 0`, 그러나 mechanical 한계).

</details>

### Q5. Odometry drift

`r = 0.05 m`, 한 wheel 의 calibration error 가 *1% over-estimate* (실제는 더 작음). 100m 직진 후 *예측 위치* 와 실제 차이.

<details><summary>답</summary>

오류 wheel 이 1% over-estimate → odometry 가 실제보다 *1% 더 멀리 갔다고* 계산.

직진 100m 시 odometry estimate ≈ 101m → 1m 오차.

추가: 두 wheel 중 한쪽만 1% over-estimate 라면 *기울기* 도 발생. `Δθ = r · 0.01 · N_revolutions / (2L)` 의 누적 회전 error → 100m 후 *방향 변화* 까지.

해결: IMU 의 gyro 와 융합 (Kalman filter).

</details>

### Q6. Mecanum 4-wheel kinematics

4 mecanum wheel 의 `H ∈ R^{4×3}`. forward / inverse kinematics 의 차이.

<details><summary>답</summary>

`H` 4×3 — over-determined.

**Forward** (`u → V`): `V = (HᵀH)⁻¹ Hᵀ u = H⁺ u`. left-pseudoinverse. 4 wheel 의 noisy data 의 *least-squares* estimate.

**Inverse** (`V → u`): `u = H V`. *unique* (3 → 4 mapping). 그러나 *실제 wheel velocity 가 H V 와 정확히 일치* 안 하면 *slip / drift*.

→ 4 wheel coordination 이 *control challenge*.

</details>

### Q7. Brockett's theorem 의 실용 함의

이론: nonholonomic system 은 *smooth time-invariant feedback* 으로 *stabilize 불가*. 실용적 결과.

<details><summary>답</summary>

자동차를 *목표 pose `(x_d, y_d, θ_d)`* 로 *부드럽게* (single equilibrium) 제어 불가. 항상:

1. **Time-varying controller** — `u(t, x)` (시간 명시적 의존)
2. **Discontinuous controller** — sliding mode, hybrid switching
3. **Open-loop maneuvering** — 평행주차의 *step-by-step* 절차 (back, steer right, forward, steer left, ...)
4. **Lyapunov 기반 nonlinear** — chained form, Pomet 알고리즘

자동차 *자율주행* 의 motion control 이 *왜 어려운가* 의 근본 이유. ROS 의 `nav2`, Apollo 의 planner 가 모두 이 문제와 씨름.

</details>

### Q8. Mecanum 의 slip

YouBot 같은 mecanum robot 이 *고속 회전* 시 *예상대로 안 움직임*. 원인.

<details><summary>답</summary>

**Slip**. Mecanum 의 holonomicity 는 *roller 가 perfect 하게 rolling* 한다는 ideal model. 고속 / 무거운 load / rough floor 에서:

1. **Static friction limit 초과** — roller 가 *grip* 못함
2. **Roller dynamics** — high speed 에서 vibration / wear
3. **Asymmetric load** — robot 자체 weight 가 wheel 마다 다름

→ 실제 chassis velocity ≠ commanded velocity.

해결: lower speed limit, *closed-loop* localization (visual odometry, LiDAR SLAM) 으로 *drift correction*, slip detection + compensation.

</details>

### Q9. Mobile manipulation 의 redundancy 활용

7-DoF arm + holonomic base (3 DoF). EE pose 6 DoF. redundancy = 4. 4 차원 null-space 활용 예시.

<details><summary>답</summary>

EE pose 추적하면서 추가로:

1. **base position** 을 *door 가까이* (예: 다음 task)
2. **arm posture** 을 *manipulability max* (singular 회피)
3. **joint limit 회피** (arm 의 어느 joint 도 limit 근처 안 가게)
4. **사람 안전** — base / arm 이 *사람 영역* 침범 안 함

cost function:

```
min  α · (base_to_door_distance)² + β · (1/manipulability)
     + γ · (joint_limit_distance penalty) + δ · (human_proximity penalty)
s.t. EE pose = T_d
```

→ 4-dim null space 안에서 위 cost 최소화. *whole-body control* 의 핵심.

</details>

### Q10. SLAM 의 역할

odometry 는 drift. SLAM 이 어떻게 보완하나?

<details><summary>답</summary>

**SLAM** (Simultaneous Localization And Mapping):
1. **Localization**: 외부 sensor (LiDAR, camera, IMU) 로 *환경 특징* 매칭 → robot 위치 추정
2. **Mapping**: 매 step 새 measurement 로 *환경 지도* 갱신
3. **Loop closure**: 이미 방문한 장소를 *재인식* → drift 누적 *재보정*

```
odometry → SLAM front-end → SLAM back-end (factor graph)
                ↑
        sensor data (LiDAR / camera)
```

대표 algorithms: ORB-SLAM3 (visual), Cartographer (LiDAR), RTAB-Map (RGB-D).

결과: 절대 위치 (1cm~1m 오차) + 환경 지도. 자율주행, AGV, SLAM-based exploration 의 표준.

</details>
