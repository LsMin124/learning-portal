# Chapter 7: Kinematics of Closed Chains — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 7: Kinematics of Closed Chains** (책 p.245~268) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 7장의 핵심: **closed-chain mechanism** (parallel manipulator) — 여러 leg 가 *공통 end-effector* 를 잡고 *loop closure* 를 형성. open chain 의 trivial PoE 가 안 통함. 대표: **Stewart-Gough platform**, **delta robot**.

## 들어가기 전에

- **선수 지식**
  - **2장**: Grübler's formula, Holonomic constraint
  - **3장**: SE(3), `[Ad_T]`
  - **4~5장**: PoE FK, Jacobian (open chain)
- **학습 목표**
  1. **Closed-chain vs Open-chain** — loop closure constraint 의 의미
  2. **Stewart-Gough platform** — 가장 유명한 6-DoF parallel
  3. **Differential kinematics** — closed chain 의 Jacobian (analytic vs constraint)
  4. **Singularity 종류** — actuator / configuration / end-effector
  5. **5-bar linkage** — 평면 closed chain 의 단순 예
- **예상 학습 시간**: 60~90분 (open chain 보다 까다롭지만 핵심 개념 적음)

---

## 1. Closed Chain 의 동기

### 1.1 Open vs Closed chain

| | Open chain (4~6장) | Closed chain (7장) |
|--|--|--|
| 구조 | base → ... → EE (단일 path) | 여러 path → EE (loop) |
| 예 | 산업용 6R arm, UR5 | Stewart-Gough, delta robot |
| FK | PoE, closed-form | implicit constraint |
| IK | 8-해 (PUMA), 복잡 | *상대적으로 쉬움* |
| DoF | n joints = n DoF | n joints − k loops |
| Payload | 작음 (cantilever) | 큼 (parallel support) |

![Figure 7.1 — Stewart-Gough platform (6-UPS). 교재 p.246](/courses/modern-robotics/figures/ch07/fig-7-1.png)

### 1.2 장점

- *Higher payload* — 여러 leg 가 *parallel* 로 부하 분담
- *High stiffness* — 각 leg 가 *strut*
- *Accuracy* — kinematic error 가 *averaged*
- *EE inertia 낮음* — actuator 가 base 에 (작은 link 만 움직임)

### 1.3 단점

- *작은 workspace*
- *Singularity 복잡* (3 종)
- *FK 어려움* (numerical iteration)

---

## 2. 대표 예제

### 2.1 Stewart-Gough Platform (6-UPS)

- **6 leg**, 각 leg 가 U (Universal) + P (Prismatic 변길이) + S (Spherical)
- *base plate* (지면) 와 *top platform* 을 연결
- *6 prismatic actuator* — leg 길이 조절로 platform pose 제어
- **6 DoF**: Grübler `6(14 − 1 − 18) + 36 = 6` (3장 예제)

응용: flight simulator, machine tool, vibration isolation.

### 2.2 Delta Robot

![Figure 7.4 — Delta robot. 교재 p.249](/courses/modern-robotics/figures/ch07/fig-7-4.png)

- 3 leg, 각 leg 가 *parallelogram* 구조
- **3 DoF translation** (회전 없음)
- 매우 빠름 — pick-and-place 산업의 *왕* (ABB IRB 360, FANUC M-1iA)

### 2.3 5-bar linkage (평면, simplest)

5 link, 5 joint, planar. Grübler: `3(5−1−5) + 5 = 2` (2 DoF).

2 joint actuated → 5-bar 의 end point 가 2D 평면 안의 임의 위치.

![Figure 7.5 — Planar 5-bar linkage. 교재 p.257](/courses/modern-robotics/figures/ch07/fig-7-5.png)

---

## 3. Forward / Inverse Kinematics

### 3.1 Closed chain 의 *역설*

- **Forward kinematics** (joint → EE): **어려움**. 각 leg 의 FK 가 *동일 EE pose 를 산출해야* (constraint).
  - 보통 *수치 해법* (Newton-Raphson) 필요
  - 다해 발생 가능 (Stewart-Gough: 최대 40 해)

- **Inverse kinematics** (EE → joint): **쉬움**. 각 leg 의 IK 독립 풀이.
  - 닫힌 형태 가능
  - 산업 응용에서 *대부분 IK 사용*

→ Open chain 과 *반대*. open chain 은 FK 가 쉽고 IK 어렵.

### 3.2 Loop closure constraint

`k` 개 loop 마다 *6 식의 holonomic constraint*:

$$g_i(\theta) = 0, \quad g_i: \mathbb{R}^n \to \mathbb{R}^6$$

Stewart-Gough: 6 leg 모두 *동일 platform pose 산출* — implicit equations.

---

## 4. Differential Kinematics

### 4.1 Constraint Jacobian

Loop closure 의 시간 미분:

$$\dot{g}_i(\theta) = \frac{\partial g_i}{\partial \theta} \dot\theta = A(\theta) \dot\theta = 0$$

이게 *velocity constraint* — Pfaffian form.

### 4.2 Actuated joint 와 passive joint

closed chain 의 joint = *actuated* + *passive*. actuated 만 input.

joint partition `θ = (θ_a, θ_p)`. `θ̇_a` (input) 으로부터 `θ̇_p` 와 EE velocity `V` 결정.

### 4.3 Stewart-Gough Jacobian

각 leg 의 length 변화율 `L̇_i` ↔ EE twist `V`:

$$\dot{L}_i = J_{leg,i}^T \mathcal{V}$$

행렬 form:

$$\dot{L} = J^T \mathcal{V}, \quad J \in \mathbb{R}^{6 \times 6}$$

`J` 의 *컬럼* = 각 leg 의 normalized screw axis.

inverse Jacobian 이 *간단* — *forward* Jacobian (`V = J L̇`) 가 필요 시 J 역행렬.

---

## 5. Singularity (3 종)

### 5.1 Actuator singularity

actuated joint 들이 *과잉* 또는 *부족* — input 으로 EE velocity 못 산출.

- *Type 1*: actuator 가 motion 만들어도 EE 정지 (input 손실)
- *Type 2*: EE 가 *uncontrolled DOF* 갖게 됨 (위험! payload 떨어짐)

### 5.2 Configuration singularity

closed chain 의 *configuration* 자체가 *degenerate* — Jacobian rank loss.

5-bar 의 *3 link colinear* configuration 이 예.

### 5.3 End-effector singularity

EE 가 *self-motion* 가능 — 같은 EE pose 에 *다른 internal configuration*.

![Figure 7.10 — Closed chain 의 3 종 singularity. 교재 p.263](/courses/modern-robotics/figures/ch07/fig-7-10.png)

### 5.4 검출

actuator + configuration + end-effector singularity 모두 *Jacobian rank* 로 분석.

> **함정 1**: open chain 의 singular 와 다름. closed chain 의 *Type 2 actuator singular* 는 *control 측면에서 위험* — actuator 가 EE 잡지 못함.

---

## 6. Hybrid Open-Closed Robot

- **Cooperative dual-arm** — 두 arm 이 *같은 물체* 잡으면 *closed chain*
- **Quadruped** — 4 leg 가 *지면* 과 *closed loop* (지면이 *지지 element*)
- **Humanoid** — 양 발 stance 시 closed kinematic chain

8장 dynamics 의 *constrained dynamics* (`τ = M θ̈ + ... + Aᵀ λ`) 가 이런 시스템에 적용.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Closed chain 의 FK 가 open chain 처럼 쉬움 | 어려움. 보통 수치 해법, 다해 (Stewart 최대 40). |
| 2 | Closed chain 의 IK 가 어려움 | *상대적으로 쉬움*. 각 leg IK 독립. |
| 3 | Stewart-Gough 의 leg 가 6 개 = 6 DoF | Grübler 계산: 6(14−1−18) + 36 = 6 OK. 하지만 leg 수 ≠ DoF 일반화 X. |
| 4 | Delta robot 이 6 DoF | 3 DoF translation 만. orientation 변화 없음. |
| 5 | Closed chain 이 *항상 stiff* | configuration 따라 *극도로 stiff* 또는 *singular floppy* — workspace 잘 설계. |
| 6 | Singularity 가 1 종 | 3 종 (actuator / configuration / end-effector) — open chain 보다 복잡. |
| 7 | Type 2 actuator singularity 가 *안전* | *위험* — actuator 가 EE motion 못 막음. fail-safe 필요. |
| 8 | Closed chain 의 Jacobian = open chain Jacobian | 다른 정의. constraint Jacobian + leg Jacobian 의 조합. |
| 9 | Stewart-Gough 의 workspace 가 *큼* | 작음. 6 leg length 의 *동시 만족* 영역만 — typical industrial arm 의 10~30%. |
| 10 | Quadruped 가 open chain | stance phase 에선 *closed chain* (지면 + 4 leg 의 loop). swing phase 에선 open. |

---

## 자가점검

1. Open vs closed chain 의 FK / IK 어려움 비교.
2. Stewart-Gough 의 leg 구성 (UPS) + DoF.
3. Delta robot 의 *6 DoF 가 아닌* 이유.
4. 5-bar linkage 의 Grübler DoF.
5. Loop closure constraint 의 일반 형태.
6. Closed chain singularity 3 종.
7. Type 1 vs Type 2 actuator singularity 의 차이.
8. Closed chain 의 *왜* payload 가 큰가.
9. Quadruped 가 closed chain 인 *상태*.
10. Closed chain FK 의 수치 해법 전략.

### 해답 (간략)

1. Open: FK 쉬움 (PoE), IK 어려움. Closed: FK 어려움 (loop closure), IK 쉬움 (leg 독립).
2. 각 leg = U (universal, 2 DoF) + P (prismatic, 1 DoF actuated) + S (spherical, 3 DoF). 6 leg × actuated P → 6 DoF.
3. 3 leg parallelogram 으로 translation 만 — orientation 변화 없는 *3 DoF translation*.
4. `3(5 − 1 − 5) + 5 = 2`. 2 actuated joint.
5. `g_i(θ) = 0`, `g_i: R^n → R⁶`. closed chain 의 *geometric consistency*.
6. Actuator / Configuration / End-effector.
7. Type 1: actuator 가 motion 만들어도 EE 정지 (input loss). Type 2: EE 가 *uncontrolled motion* (위험).
8. *Parallel* leg 가 부하 분담 — 각 leg 가 일부만 지지. cantilever 대비 stiffness ↑, EE inertia ↓.
9. Stance phase — leg(s) 가 지면 contact, 지면 + leg 의 loop 형성. swing leg 는 open.
10. Newton-Raphson with loop closure equations + *initial guess* (이전 step pose). multiple solutions 의 *closest to previous*.

---

## 다음 학습으로

- **Stewart-Gough simulation** — V-REP, Gazebo 에서 6-UPS model 학습.
- **Delta robot industrial** — ABB IRB 360, FANUC M-1iA 의 picking applications.
- **Parallel robot 연구** — 6-DoF haptics (Force Dimension), VR simulator.
- **Cooperative manipulation** — 다중 robot 의 closed chain control.

7장은 short 하지만 *parallel mechanism* 의 *분석 framework*. 산업·연구 모두에서 closed-chain robot 비중 증가 (특히 picking, flight simulator, haptics).
