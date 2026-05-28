# Chapter 1: Preview — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 1: Preview** (책 p.1~10) 를 단독 학습 가능한 형태로 재구성한 것입니다.
> 1장은 책 전체의 thumbnail — 로봇의 구성요소와 12개 후속 챕터의 큰 그림을 잡는 것이 목적.

## 들어가기 전에

- **선수 지식**
  - 선형대수 (행렬, 벡터, 고유값, 행렬 지수 exponential)
  - 기초 미적분 (편미분, ODE — 특히 second-order ODE)
  - 강체역학 기초 (force/torque, momentum, 가상일 원리)
- **학습 목표**
  1. 본 책의 범위가 *mechanics + planning + control* 이라는 사실 인지
  2. 로봇 메커니즘의 5 가지 구성요소 (link, joint, actuator, transmission, sensor) 의 역할
  3. **open-chain** 과 **closed-chain** 메커니즘의 차이, 그리고 그 차이가 왜 중요한가
  4. **DoF (자유도)** 라는 개념과 책 전체에서 이 개념이 어떻게 확장되는가 (configuration space → Jacobian → dynamics)
  5. 2~13장의 핵심 문제·도구 한 줄 요약 — 어디서 무엇을 배우는지 지도
- **예상 학습 시간**: 60~90분 (코드 없음, 개념 위주)

---

## 1. 로보틱스의 시각 — 본 책이 다루는 것과 다루지 않는 것

> "로보틱스의 가장 근본적 질문은 결국 인간에 대한 질문이다."

학문적 야망은 크다 — 사람처럼 행동하고 사고하는 기계. 그러나 책 한 권이 그 전부를 다룰 수는 없다. 본 책의 **범위**는 다음 셋으로 엄격히 좁혀진다.

```
+----------------+   +----------------+   +----------------+
|   Mechanics    |   |    Planning    |   |    Control     |
| (운동학·동역학) | + | (경로·궤적 생성) | + | (제어 알고리즘) |
+----------------+   +----------------+   +----------------+
                              ↓
                      "로봇 메커니즘이
                       물리 세계에서 움직이게"
```

빠진 것:
- **AI · 인지 (perception)** — 시각/언어/추론. 본 책의 범위 아님 (필요시 가정).
- **모터 회로 설계 · 임베디드** — actuator 의 동특성은 다루지만 회로는 다루지 않음.
- **소프트로보틱스** — 모든 link 가 rigid (강체) 라고 가정.

이 가정 (**rigid links, ideal joints**) 은 강력한 단순화다. 현실에서 link 는 휘고, joint 는 **elasticity, backlash, friction, hysteresis** 의 영향을 받는다. 본 책은 대부분 이를 무시하고, 필요한 경우 (8장 Dynamics, 11장 Control) 에서만 등장.

### 핵심: "로봇" 의 정의

| 비-로봇 | 로봇 |
|--|--|
| 정해진 한 가지 동작만 반복하는 자동화 기계 | **재프로그래밍 (reprogrammable)** 가능. 다양한 작업에 적응. |
| 시계, 자판기 | manipulator, 자율주행, drone |

"reprogrammable" 의 함의 — 컨트롤러가 task 정보로부터 joint 명령을 *자동 생성* 해야 함. 이게 9장 Trajectory Generation, 10장 Motion Planning, 11장 Control 이 존재하는 이유.

---

## 2. 로봇 메커니즘의 5 가지 구성요소

### 2.1 Link & Joint — 메커니즘의 골격

```
  +-[link1]-O-[link2]-O-[link3]-O-[end-effector]
  |          ^         ^         ^
 base       joint1   joint2    joint3
(고정 기준)  (회전·병진) ...
```

- **link**: 강체 (rigid body) — 책 전반의 가정.
- **joint**: 인접 link 간 상대 운동을 허용. 가장 흔한 두 가지:
  - **revolute (R)** — 회전 1자유도
  - **prismatic (P)** — 직선 병진 1자유도

다른 joint type 은 2장에서 (universal, cylindrical, spherical 등) 추가됨. 모두 R/P 의 조합으로 등가 모델링 가능.

### 2.2 Actuator — 움직임의 원천

```
전기 -+- DC motor                    : 가장 흔함, 제어 단순
      +- AC motor                    : 산업용
      +- Stepper motor               : 오픈루프 정밀제어
      +- Shape Memory Alloy (SMA)    : 소형·생체모방

유체 -+- Pneumatic cylinder           : 빠름, 정밀제어 어려움
      +- Hydraulic cylinder          : 강력, 무거움/소음
```

### 2.3 Transmission — 토크·속도 매칭

이상적인 모터는 *경량 + 저속 (수백 RPM) + 고토크*. 그러나 실제 가용 모터는 *저토크 + 수천 RPM*. 그래서 **감속·증토크 장치**가 필수:

| 종류 | 특징 | 단점 |
|--|--|--|
| Gear | 정밀, 효율 좋음 | **backlash** (관절 떨림 원인) |
| Cable drive | backlash 거의 없음 | 케이블 늘어남, 정비 |
| Belt & pulley | 조용, 충격 흡수 | slip 가능 |
| Chain & sprocket | 큰 힘 전달 | 무겁고 소음 |

#### 핵심 개념: backlash 와 slippage

- **backlash**: 입력은 정지인데 출력측에 *남아있는 회전 여유* (각도). 정밀 제어 시 hysteresis 의 원인.
- **slippage**: 입력 회전이 출력으로 *전부 전달되지 않음*. 케이블·벨트의 약점.

좋은 transmission = **둘 다 0 에 가까울수록 좋음**. 8장과 11장에서 이 비이상성이 어떻게 dynamic equation 과 controller 설계에 영향을 주는지 다시 등장.

### 2.4 Brake — 멈춤·자세 유지

종종 간과되지만 안전·전력 절약의 핵심. 정전 시 fail-safe 로 brake 가 잠겨야 사람이 다치지 않음.

### 2.5 Sensor — 상태 측정

| 무엇을 재나 | 센서 |
|--|--|
| Joint 위치 | encoder, potentiometer, resolver |
| Joint 속도 | tachometer (또는 encoder 차분) |
| Joint/End-effector 힘 | F/T sensor |
| 외부 환경 | vision camera, **RGB-D camera** (color + depth), laser range finder, acoustic |

11장 Control 에서 **closed-loop** 컨트롤이 가능한 이유는 이 측정값을 피드백으로 쓸 수 있기 때문.

---

## 3. Open-Chain vs Closed-Chain — 가장 근본적인 분류

```
   Open chain (직렬)              Closed chain (폐루프)
   ----------------               ---------------------------
        base                          base --+- leg1 -+
         |                                  +- leg2 -+
        joint1                              +- leg3 -+- top platform
         |                                  +- leg4 -+
        link1                               +- leg5 -+
         |                                  +- leg6 -+
        joint2                            (Stewart-Gough)
         |
        link2
         |
        end-effector
```

| | Open chain | Closed chain |
|--|--|--|
| 예시 | 산업용 6-DoF 매니퓰레이터 | Stewart-Gough platform, Delta robot |
| Joint 작동 | **모든** joint 가 actuated | **일부만** actuated, 나머지는 passive |
| DoF 계산 | joint 자유도 단순 합산 | **Grübler's formula** 가 lower bound |
| Forward kinematics | 항상 **유일해** | **다중해** 가능 |
| Inverse kinematics | 다중해 또는 무해 가능 | 더 복잡 |

이 분류가 책 전체를 가른다:
- 2~6장: 거의 모두 open chain 중심
- 7장: closed chain 만 별도 다룸
- 8장 dynamics 도 open chain 중심 (closed 는 8.7 constrained dynamics)

### 핵심 개념: passive joint

closed chain 에서 일부 joint 는 모터가 없다 (이를 *passive* 라 부름). 이런 joint 의 각도는 *기구학적 구속조건* 으로부터 자연 결정되며, 직접 제어 불가. 이는 7장에서 singularity 분석을 까다롭게 만드는 주범.

---

## 4. 12 챕터 로드맵 — 어떤 문제를 어떤 도구로 푸는가

각 챕터의 *질문 한 줄 + 핵심 도구* 정리. 학습 순서대로 읽으면 됨.

### Ch 2. Configuration Space — "로봇이 가질 수 있는 모든 상태의 공간"

**질문**: 로봇의 상태를 몇 개의 숫자로 표현해야 하는가?

**도구**:
- DoF 정의: 강체는 평면에서 3, 공간에서 6 자유도
- **Grübler's formula**: 일반 메커니즘의 DoF lower bound
- topology vs representation (예: 구면 = `(lat, lon)` *explicit* 또는 `x²+y²+z²=1` *implicit*). 책은 *implicit* 표현을 표준으로 채택.
- **task space** (EE 가 놓일 수 있는 모든 위치·자세의 공간) ↔ **workspace** (그 중 실제로 도달 가능한 부분 집합)

이 챕터의 가장 흔한 함정: *configuration space 차원* 과 *task space 차원* 의 혼동. 7-DoF arm (kinematic redundancy) 이 task space 6 차원을 다 채우면서도 여분 freedom 한 차원이 남는 게 그 예.

### Ch 3. Rigid-Body Motions — "위치·자세를 어떻게 수학적으로 표현"

**질문**: 강체의 위치 + 자세를 어떻게 표현해야 계산이 편한가?

**도구**:
- **Rotation matrix** R ∈ SO(3) — 3×3 행렬
- **Exponential coordinates** — R = exp([ω̂]θ), ω̂ 단위 회전축 + 회전각 θ. 가장 직관적·통합적.
- 다른 표현: Euler angle, Cayley-Rodrigues, **unit quaternion** (Appendix B)
- **Twist** V ∈ R⁶ — 6D 속도 (각속도 + 선속도). *spatial velocity* 라고도.
- **Wrench** F ∈ R⁶ — 6D 힘+모멘트. *spatial force*.
- Homogeneous transformation matrix T ∈ SE(3) — 4×4 행렬로 강체운동 통합 표현

본 책의 **고유한 선택**: rotation·motion 을 **exponential coordinate** 중심으로 풀어감. 이게 4장 PoE 의 기반이 됨.

### Ch 4. Forward Kinematics — "joint 각도 → end-effector 위치"

**질문**: 각 joint 의 위치가 주어지면 손끝은 어디에 있나?

**도구**:
- **PoE (Product of Exponentials)** 공식 — *두 가지 표현*:
  - **Space frame** (base 기준)
  - **End-effector frame** (body 기준)
- D-H (Denavit-Hartenberg) — Appendix C. 더 적은 파라미터지만 link frame 부착 규칙이 번거로움. D-H ↔ PoE 변환식도 Appendix C 에.

PoE 의 장점: link frame 따로 안 박아도 됨. base + EE frame 만으로 충분.

### Ch 5. Velocity Kinematics & Statics — "joint 속도 ↔ EE 속도, joint 토크 ↔ EE 힘"

**질문**: joint 가 빠르게 움직이면 end-effector 는 얼마나 빨라지나? 반대로 end-effector 에 힘을 주려면 joint 토크는?

**도구**:
- **Jacobian** J (configuration 에 의존하는 행렬). twist = J · joint_velocities.
- **Kinematic singularity** — J 가 full rank 잃는 configuration. 특정 방향 운동 불가.
- **Manipulability ellipsoid** — 어느 방향이 움직이기 쉬운지 시각화.
- **Static force**: τ = Jᵀ · wrench (전치).

이 한 챕터의 통찰이 책 후반 (Ch 6 inverse, Ch 11 control) 의 절반을 떠받침.

### Ch 6. Inverse Kinematics — "EE 목표 위치 → joint 각도"

**질문**: 손을 (x, y, z) 에 두려면 각 joint 를 얼마로?

**도구**:
- **Analytic solution** — 6R PUMA-type arm, Stanford-type arm 처럼 닫힌 형태 풀이 가능한 구조
- **Numerical** — Newton-Raphson (Jacobian inverse 반복)
- **Kinematic redundancy** — joint 수 > task dim. 이 경우 **Jacobian pseudoinverse** 사용. 남는 자유도로 *secondary task* (joint limit 회피 등) 도 동시 수행 가능.
- closed loop 가 섞인 경우의 주의사항 (6.4)

해 개수: forward 는 1개 (open chain). inverse 는 **0개·유한 개·무한 개** 모두 가능.

### Ch 7. Kinematics of Closed Chains — "Stewart-Gough 같은 폐루프 다리"

**질문**: closed chain 의 forward/inverse 와 singularity 는 어떻게 다른가?

**도구**:
- 3×RPR 평면 parallel mechanism, Stewart-Gough platform 사례 분석
- 일반 closed chain 으로 확장
- **Differential kinematics** — 속도 매핑이 open chain 과 구조적으로 다름
- actuated vs passive joint 의 singularity 결합 효과

### Ch 8. Dynamics of Open Chains — "힘·토크 ↔ 가속도"

**질문**: 어떤 joint 토크가 어떤 joint 가속도를 만드나? (또는 반대)

**두 가지 문제 분리**:
- **Forward dynamics**: joint 힘·토크 → joint 가속도 (시뮬레이션·예측)
- **Inverse dynamics**: 원하는 joint 가속도 → 필요한 joint 힘·토크 (제어·planning)

둘 다 **second-order ordinary differential equation** 형태.

**두 가지 도출 방식**:
- **Lagrangian** 방식 — *generalized coordinates* 선택 → 운동 에너지 + 위치 에너지를 그 좌표·시간미분으로 표현 → **Euler-Lagrange 방정식** 에 대입. 해석적·심볼릭 형태에 강함.
- **Newton-Euler** 방식 — F=ma 의 강체 일반화. *재귀적 (recursive)* 알고리즘:

```
1. Outward pass  (proximal → distal):
   base 부터 EE 방향으로 link velocity·acceleration 전파
   ─ 각 link 의 운동 상태 계산

2. Backward pass (distal → proximal):
   EE 부터 base 방향으로 각 link 의 wrench·joint torque 계산
   ─ "이 link 를 그렇게 움직이려면 어떤 힘이 필요?"
```

이 두 패스 구조가 **recursive Newton-Euler** 의 본질. 빠르고 실시간 구현 적합.

| | Lagrangian | Newton-Euler |
|--|--|--|
| 직관 | 에너지 보존 | F=ma 직접 |
| 식 도출 | 해석적, 닫힌 형태 | 재귀, 알고리즘적 |
| 어디 적합 | 이론·심볼릭 | 실시간 계산, 컨트롤 |

**추가 주제**:
- task-space dynamics (EE 기준 동역학)
- constrained dynamics (closed chain 의 loop closure 처리)
- 실제 actuator + gearing + friction 효과 (8.9) — apparent inertia, motor inertia, joint/link flexibility

### Ch 9. Trajectory Generation — "시간에 따른 joint 목표값"

**질문**: 목표만 주어졌을 때 매 순간 joint 가 어디 있어야 하나?

**핵심 분리**:
```
 trajectory = path + time scaling
           = "어떤 모양"   +  "언제 어디"
            (기하)            (속도 프로필)
```

**도구**:
- **Point-to-point** 직선 경로 (joint space / task space 양쪽 다)
- **Via point** 부드러운 통과 (polynomial trajectory, 5차·3차)
- **Time-optimal** time scaling — 동역학·액추에이터 한계 고려한 최단시간 (8장 dynamics 와 결합)

핵심: 사용자는 "control point + control time" 정도만 주고, 나머지는 자동 생성.

### Ch 10. Motion Planning — "장애물을 피하면서 경로 찾기"

**질문**: 어수선한 환경에서 충돌 없이 어떻게 갈까?

> **용어 분리**: **Path planning** 은 motion planning 의 *하위 문제*. 동역학·시간·제어 입력 무시하고 *시작 → 목표* 의 *충돌 없는 기하 경로* 만 찾는다. **Motion planning** 은 여기에 액추에이터 한계·동역학·시간 등 추가 제약을 얹은 더 넓은 문제.

**도구**:
- **Grid methods** — discrete 그래프 탐색 (A*, Dijkstra). multi-resolution grid 도 사용.
- **Sampling methods** — 무작위 샘플 + 연결:
  - **RRT (Rapidly-exploring Random Tree)** — 단일 트리 확장
  - **PRM (Probabilistic Roadmap)** — 사전 grid + 쿼리
- **Virtual potential fields** — 목표 인력 + 장애물 척력. 단순하지만 *local minima* 함정.
- 그 외: nonlinear optimization, path smoothing (geometric 경로 후처리)

이 챕터의 핵심 한 문장: **"모든 motion planning 에 만능 알고리즘은 없다"** — 상황별 trade-off.

### Ch 11. Robot Control — "feedback 으로 명령 따라가게 만들기"

**질문**: 모델 불확실성·외란이 있어도 desired trajectory 를 어떻게 추종?

**5 가지 제어 패러다임 + 실제 task 예시**:

| 패러다임 | 무엇을 제어 | 실제 task 예시 |
|--|--|--|
| **Motion control** (position/velocity) | EE 위치·속도 | pick-and-place, manufacturing trajectory tracing |
| **Force control** | 접촉력 | grinding, polishing (일정한 누름력) |
| **Hybrid motion-force** | 방향별 분리 | *writing on chalkboard*: 보드면 *수직* = 힘제어, 보드면 *내* = 위치제어 |
| **Impedance / Admittance control** | 동적 응답 (스프링·댐퍼·질량) | haptic display, 협동로봇의 사람 접촉 안전 |
| **Computed torque control** | 모델 + feedback | 정밀 추종이 필요한 산업·연구 |

**근본 제약**: 같은 방향에서 위치와 힘을 *동시에 독립* 제어할 수 없다. 위치를 강제하면 힘은 환경이 결정, 그 반대도 마찬가지. *hybrid motion-force* 가 존재하는 이유.

또한 정밀 dynamics 모델이 없으면 *feedback* 이 부족분을 보완. 모델 정확도와 feedback gain 의 trade-off 가 controller 설계의 핵심.

### Ch 12. Grasping & Manipulation — "물건과의 접촉"

**질문**: 물건을 잡고, 밀고, 옮기려면 접촉을 어떻게 모델링?

**도구**:
- 접촉 운동학 (contact kinematics) — 접촉이 부과하는 *움직임 구속*
- 마찰 모델 (friction cone)
- **Form closure** — 기하만으로 물체 고정 (마찰 0 가정에서도 움직임 불가)
- **Force closure** — 마찰을 이용한 고정. form closure 보다 약하지만 일반적.
- 비-grasping 조작: **pushing** (밀기), **dynamic carry** (동적 운반), **stability test** (구조의 안정성 판정)

### Ch 13. Wheeled Mobile Robots — "바퀴로 굴러가는 로봇"

**질문**: arm 만이 아닌 차량형 로봇은 어떻게 모델·제어?

**도구**:
- **omniwheel / mecanum wheel** (omnidirectional, **holonomic** — 즉시 횡이동 가능)
- 자동차·차동구동 (**nonholonomic** — 속도구속이 위치구속으로 적분 불가)
- **Odometry** — wheel encoder 데이터로 chassis configuration 추정. **흥미롭게도, 두 종류 mobile robot 에 같은 방법으로 풀린다.**
- **Mobile manipulation** — arm + 차체 동시 제어. 핵심 도구는 *joint rate + wheel velocity → EE twist* 의 통합 Jacobian. **이것도 두 종류 robot 에 동일 형식**.

**holonomic vs nonholonomic** 의 차이가 motion planning·control 알고리즘을 크게 가른다. nonholonomic 은 평행주차처럼 즉시 횡방향 이동 불가능 → 경로 자체를 회전+전진 조합으로 만들어야.

---

## 5. 본 책의 4 가지 "프레임워크 선택"

전체 흐름을 한 줄로:

1. **Exponential coordinates** 가 회전·운동·forward kinematics 의 중심
2. **Jacobian** 이 velocity kinematics, statics, inverse, redundancy, control 을 관통
3. **Twist & Wrench** 라는 6D 표현이 속도·힘을 통합
4. **Recursive Newton-Euler** 가 dynamics 의 알고리즘적 표준

이 4 가지를 일관되게 사용하는 것이 본 책 (vs. 다른 로보틱스 교과서) 의 정체성.

---

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| Configuration space dimension 과 task space dimension 혼동 | DoF = joint 자유도 합 − 구속. Task space = end-effector 가 놓일 수 있는 공간. 일치 안 할 수 있음 (redundancy, under-actuation). |
| forward = 쉬움, inverse = 어려움 — *항상* 그렇다고 착각 | open chain 은 그렇지만 **closed chain 에서는 inverse 가 쉽고 forward 가 어려운 경우**가 흔함 (예: Stewart-Gough). |
| Forward dynamics ↔ Inverse dynamics 를 혼동 | forward = "토크 주어졌을 때 가속도" (시뮬레이션). inverse = "원하는 가속도 만들 토크" (제어용). 둘은 다른 *방향*. |
| Path planning 과 Motion planning 을 같은 것으로 묶음 | Path planning ⊂ Motion planning. Path 는 기하만, Motion 은 동역학·시간·제약 모두 포함. |
| Jacobian 의 정의가 한 가지뿐이라고 생각 | end-effector velocity 의 표현 (twist, EE-frame, hybrid) 에 따라 **Jacobian 도 다름**. 책은 spatial twist 기준을 표준으로. |
| Backlash 와 slippage 를 같은 것으로 묶음 | backlash = 빈 회전 여유 (gear 의 약점), slippage = 전달 손실 (cable/belt 의 약점). 컨트롤러 영향도 다름. |
| Holonomic vs nonholonomic 을 단순히 "구속 있냐 없냐" 로 분류 | holonomic = 구속을 *configuration 식* 으로 적을 수 있음. nonholonomic = *velocity 식* 으로만. 차로 평행주차가 어려운 이유. |
| Closed chain 의 모든 joint 를 모터로 구동한다고 가정 | 보통 일부만 actuated. passive joint 의 각도는 기구학적 구속에서 결정. |
| 모든 robot 이 reprogrammable 한 "로봇" 인 줄 앎 | 산업용 자동화 기계는 단일 task. **재프로그래밍 가능성**이 로봇의 정의적 특성. |
| 위치 제어와 힘 제어를 같은 방향에서 동시에 할 수 있다고 생각 | 같은 방향에서는 *상호 배타*. 위치 강제 → 힘은 환경 결정. 그래서 *hybrid motion-force control* 이 별도 패러다임. |

---

## 자가점검

1. 본 책이 다루지 *않는* 로보틱스 주제 두 가지를 들고, 왜 본 책의 범위에서 빠졌는지 한 줄로 설명.
2. 6-DoF 공간 강체의 자유도가 6 인 이유를 위치 3 + 자세 3 으로 분해해 설명.
3. Open-chain 6-axis 로봇과 6-leg Stewart-Gough platform 중 **forward kinematics 가 더 어려운** 쪽은? 이유와 함께.
4. Backlash 와 slippage 의 정의를 각각 한 문장으로. 어떤 transmission 종류가 어느 약점을 가지나?
5. Jacobian 이 *동시에* 다루는 두 가지 물리 — 속도 매핑과 힘 매핑 — 의 관계를 한 식으로 적어보기.
6. Forward dynamics 와 Inverse dynamics 의 차이를 한 문장씩으로. 시뮬레이션·제어 중 각각 어느 쪽에 쓰이나?
7. Path planning 과 Motion planning 의 관계를 부등호로 표현하시오 (⊂ 또는 ⊃).
8. holonomic 과 nonholonomic 구속의 차이를, 자동차 평행주차를 예로 설명.
9. 12 챕터를 *문제 → 도구* 짝으로 한 줄씩 적기 (외워서).

<details><summary>풀이</summary>

1. **AI/perception** 과 **모터 회로 설계**. 둘 다 mechanics/planning/control 의 알고리즘 층과 다른 추상화 단계라 별도 분야로 분리됨.
2. 강체는 임의의 한 점 (3 자유도) + 그 점 주변 자세 (rotation, 3 자유도) = 6. 평면이면 점 (2) + 자세 (1) = 3.
3. **Stewart-Gough**. open chain 은 joint 가 순차적이라 PoE 한 번이면 끝. closed chain 은 모든 leg 가 polynomial system 을 만족해야 하고 다중해가 흔함.
4. backlash = 입력 정지에서 출력측이 가질 수 있는 빈 회전 (gear 의 약점). slippage = 입력 회전 일부가 손실 (belt/cable/chain 의 약점).
5. velocity: V = J(θ) · θ̇. force: τ = J(θ)ᵀ · F. **전치 관계**. 가상일 원리의 결과.
6. *Forward*: joint 토크 → joint 가속도 (시뮬레이션·예측). *Inverse*: 원하는 가속도 → 필요한 토크 (제어·trajectory tracking). 같은 second-order ODE 의 *방향* 만 다름.
7. **Path planning ⊂ Motion planning**. Path 는 기하만, Motion 은 동역학·시간·액추에이터 한계까지 포함.
8. 자동차는 즉시 횡으로 못 이동 (velocity 구속). 그래도 위치는 어디든 갈 수 있음 (회전 + 전진 조합). 따라서 *configuration 식* 으로는 적을 수 없는 *velocity 식 구속* — nonholonomic.
9. (앞 4 절의 표를 보고 답하세요.)

</details>

---

## 다음 학습으로

- **Chapter 2: Configuration Space** — DoF, Grübler's formula, topology, task space, workspace
- 이 책을 따라가지 않더라도 **선형대수의 rotation matrix** 와 **rigid body kinematics** 는 어디서든 다시 만남

### 학습 자원

- **공식 사이트**: http://modernrobotics.org — 영상, 추가 자료, feedback form
- **동반 라이브러리** (`modernrobotics` 패키지, Python · MATLAB · Mathematica 버전 제공)
  - 책의 핵심 함수들을 그대로 구현. PoE, Jacobian, Newton-Euler, trajectory 생성 등
  - 저자가 **"읽기 쉽게 의도적으로 작성했으므로 *쓰는 것보다 읽으며 학습* 하라"** 고 권장
  - 각 함수의 docstring 에 sample usage 포함 — 인터랙티브 학습 가능
  - 설치: `pip install modern_robotics` (Python)
- **각 챕터 끝의 *Summary***: 그 챕터의 핵심 식·정의 한 페이지 정리
- **Appendix A**: 가장 많이 쓰는 식들의 *equation reference* — 복습·치팅용 한 페이지
- **Appendix B**: Euler angle, quaternion, Cayley-Rodrigues 등 *대안 회전 표현*
- **Appendix C**: D-H 표기와 PoE 와의 변환

---

## 6. Modern Robotics 산업 landscape (2025)

본 책의 이론이 *어디에서 실제로 적용*?

### 6.1 산업용 로봇

| 회사 | 제품 | 특징 |
|--|--|--|
| ABB | 6-axis arm | 산업용 표준, IRB 시리즈 |
| KUKA | LBR iiwa | 7-DoF collaborative |
| Fanuc | M-2000iA | 초중량 (2.3톤 페이로드) |
| Universal Robots | UR5, UR10 | 협동로봇 (cobot) 표준 |
| Yaskawa | Motoman | 산업 자동화 |

### 6.2 Humanoid + Mobile

| | 제조사 | 특징 |
|--|--|--|
| Atlas | Boston Dynamics | parkour, hydraulic → electric (2024) |
| Spot | Boston Dynamics | 4-leg, industrial inspection |
| Digit | Agility Robotics | bipedal warehouse |
| Optimus | Tesla | bipedal, mass production 목표 |
| Figure 01 | Figure AI | OpenAI 협력, AI integration |
| 1X NEO | 1X Technologies | home robot |

### 6.3 Robot OS + simulation

**ROS (Robot Operating System)**:
- *De facto* 산업 표준
- ROS 1 (deprecated 2025) → **ROS 2** (real-time, secure)
- Publisher-subscriber, RPC, parameter server

**Simulation tools**:
- **Gazebo** — ROS 의 표준
- **MuJoCo** (DeepMind, 2021 free) — 빠른 contact-rich
- **NVIDIA Isaac Sim** — GPU-accelerated, photorealistic
- **PyBullet** — Python, 학습용
- **Drake** (MIT) — model-based + optimization

### 6.4 Modern challenges

- **Sim-to-real gap** — simulation 의 모델 ↔ 실제 robot 차이
- **Reinforcement learning** — Atlas, Optimus 의 학습 기반 control
- **Foundation models** — RT-2 (Google), VLA (vision-language-action) — natural language → robot action
- **Human-robot collaboration** — 안전 + 효율
- **Generalist robots** — 단일 task → 다양한 task 의 transition
