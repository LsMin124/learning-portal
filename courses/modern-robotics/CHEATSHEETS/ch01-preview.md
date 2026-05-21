# Chapter 1: Preview — 치트시트

> *Modern Robotics* (Lynch & Park, 2017) 1장 — 책 전체 thumbnail. 로봇 구성요소 + 12개 후속 챕터 로드맵.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄

1. 본 책의 범위 = **Mechanics + Planning + Control**. AI, 회로, soft robotics 는 범위 밖.
2. 로봇 = **재프로그래밍 가능한** 메커니즘. 자동화 기계와의 결정적 차이.
3. 메커니즘 5요소: **Link + Joint + Actuator + Transmission + Sensor**. 모든 link 는 *rigid* 로 가정.
4. 가장 근본적 분류: **Open chain** (모든 joint actuated, forward 쉬움) vs **Closed chain** (passive joint 존재, forward 어려움).
5. 책 전체 척추 4 가지 도구: **Exponential coordinate** (회전·운동), **Jacobian** (속도·힘), **Twist·Wrench** (6D 통합), **Recursive Newton-Euler** (dynamics).
6. 12 챕터는 *Configuration → Motion → Kinematics → Dynamics → Trajectory → Planning → Control → Manipulation → Mobile* 순서로 쌓아 올라감.

## 가장 중요한 식 3개

```
(1) DoF = (강체들의 자유도 합) − (joint 가 부과하는 구속 합)
        : 평면 강체 m=3, 공간 강체 m=6 기준.
          Grübler's formula 의 핵심.
```

```
(2) R = exp([ω̂] θ)
    : 회전 행렬의 exponential coordinate 표현.
      ω̂ ∈ R³ (단위 회전축), θ ∈ [0, π].
      4장 PoE, 8장 twist exponential 의 출발점.
```

```
(3) V = J(θ) · θ̇        (속도)
    τ = J(θ)ᵀ · F        (힘, 전치)
    : Jacobian 이 속도·힘을 동시에 다룸 (가상일의 원리).
      5장의 핵심, 6장 inverse, 11장 control 전반에 사용.
```

## 면접 한 줄 답변

- **Q. 로봇과 자동화 기계의 차이는?** → **재프로그래밍 가능성**. 한 가지 task 만 반복하면 자동화 기계, 다양한 task 에 컨트롤러로 적응할 수 있으면 로봇.
- **Q. Open chain 과 closed chain 중 어느 쪽 forward kinematics 가 더 어려운가?** → **Closed chain**. open 은 joint 순서대로 PoE 한 번이면 끝, closed 는 모든 leg 가 polynomial 시스템을 만족해야 하고 다중해.
- **Q. Holonomic 과 nonholonomic 의 차이를 한 줄로?** → **구속을 configuration 식으로 적을 수 있으면 holonomic, velocity 식으로만 적을 수 있으면 nonholonomic** (자동차 평행주차가 대표 사례).
- **Q. Modern Robotics 책의 기술적 특징?** → **Exponential coordinate 통합 표현** — D-H 의 link-frame 부착 규칙 없이 base + EE frame 만으로 운동학·동역학을 일관되게 다룸.

---

# 2. Quick Reference (실무 복붙)

## 2.1 Joint 종류 + 구속

| Joint | 약자 | DoF | 평면 구속 | 공간 구속 | 예시 |
|--|--|--|--|--|--|
| Revolute | R | 1 (회전) | 2 | 5 | 거의 모든 산업용 arm joint |
| Prismatic | P | 1 (병진) | 2 | 5 | Cartesian gantry, 슬라이딩 보조축 |
| Universal | U | 2 | n/a | 4 | 차량 steering column |
| Cylindrical | C | 2 (회전+병진) | n/a | 4 | 일부 telescope mount |
| Spherical | S | 3 (회전 3) | n/a | 3 | 볼조인트, 인간 어깨 |

> 일반화: 공간 1-DoF joint 는 인접 강체에 5 구속 부과. m-DoF joint 는 (6−m) 구속.

## 2.2 Actuator 종류

| 종류 | 적합 영역 | 단점 |
|--|--|--|
| DC motor | 가장 흔함, 일반 industrial | 정밀제어 시 회로·driver 필요 |
| AC motor | 산업용 고출력 | 큰 부피, 제어 복잡 |
| Stepper motor | 오픈루프 정밀 | 토크 한계, 고속 손실 |
| SMA (shape memory alloy) | 소형·생체모방 | 느린 응답, 효율 낮음 |
| Pneumatic | 빠른 응답 | 정밀 위치제어 어려움 |
| Hydraulic | 강력 (heavy load) | 무겁고 소음·누유 |

## 2.3 Transmission 종류

| 종류 | 장점 | 단점 |
|--|--|--|
| **Gear** | 정밀, 효율 좋음 | **backlash** |
| **Cable drive** | backlash 거의 0 | 케이블 늘어남·정비 |
| **Belt & pulley** | 조용, 충격 흡수 | slip 가능 |
| **Chain & sprocket** | 큰 힘 전달 | 무겁고 소음 |

## 2.4 Sensor 종류

| 측정 대상 | 센서 |
|--|--|
| Joint 위치 | encoder, potentiometer, resolver |
| Joint 속도 | tachometer, encoder 차분 |
| Joint/EE 힘·토크 | F/T sensor |
| 환경 | vision, RGB-D camera, laser range finder, acoustic |

## 2.5 12 챕터 요약 인덱스

| Ch | 제목 | 핵심 문제 | 핵심 도구 |
|--|--|--|--|
| 2 | Configuration Space | 로봇 상태를 몇 개 숫자로? | Grübler, topology, task/workspace |
| 3 | Rigid-Body Motions | 위치·자세 수학적 표현 | Rotation matrix, exp coord, twist, wrench, SE(3) |
| 4 | Forward Kinematics | joint → EE 위치 | **PoE** 공식, D-H (Appendix) |
| 5 | Velocity Kinematics & Statics | joint 속도 ↔ EE 속도/힘 | **Jacobian**, singularity, manipulability ellipsoid |
| 6 | Inverse Kinematics | EE 목표 → joint | Analytic (PUMA), Newton-Raphson, pseudoinverse |
| 7 | Closed Chains | passive joint 있는 폐루프 | 5-bar, Stewart-Gough, 다중해 분석 |
| 8 | Dynamics | 힘·토크 ↔ 가속도 | Lagrangian, **Newton-Euler (recursive)** |
| 9 | Trajectory Generation | 시간에 따른 joint 목표 | Point-to-point, via point, time-optimal scaling |
| 10 | Motion Planning | 장애물 회피 경로 | Grid, **RRT/PRM**, potential fields |
| 11 | Robot Control | feedback 으로 추종 | Motion/force/hybrid/**impedance**, computed torque |
| 12 | Grasping & Manipulation | 접촉 모델링 | Form closure, force closure, pushing |
| 13 | Wheeled Mobile Robots | 차량형 로봇 | **Holonomic vs nonholonomic**, odometry, mobile manipulation |

## 2.6 자주 빠지는 함정

| 함정 | 정정 |
|--|--|
| Config space dim = task space dim 항상 같음 | redundancy (7-DoF arm) 시 다름 |
| Forward 는 항상 쉽고 inverse 는 항상 어려움 | closed chain 에선 자주 반대 |
| Jacobian 정의가 한 가지 | EE velocity 표현 (spatial/body/hybrid twist) 마다 다름 |
| Backlash = slippage | backlash=gear 약점, slippage=belt/cable 약점 (별개) |
| 구속 있으면 holonomic | configuration 식으로 적을 수 있어야 holonomic |
| Closed chain 모든 joint 가 actuated | 보통 일부만, 나머지는 passive |

## 2.7 약어 표

| 약어 | 풀어쓰기 |
|--|--|
| DoF | Degrees of Freedom |
| R / P | Revolute / Prismatic (joint) |
| EE | End-Effector |
| PoE | Product of Exponentials |
| D-H | Denavit-Hartenberg |
| F/T | Force/Torque |
| RGB-D | RGB + Depth |
| SMA | Shape Memory Alloy |
| RRT | Rapidly-exploring Random Tree |
| PRM | Probabilistic Roadmap |
| SO(3) / SE(3) | 3D 회전군 / 3D 강체운동군 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 3.1 책 전체 토픽 트리

```
Modern Robotics
│
├── [Foundation]
│   ├── Ch 1: Preview  ← 현재 위치
│   │   ├── 범위 (Mechanics + Planning + Control)
│   │   ├── 메커니즘 5요소
│   │   ├── Open vs Closed chain
│   │   └── 12 챕터 로드맵
│   │
│   ├── Ch 2: Configuration Space
│   │   ├── DoF
│   │   ├── Grübler's formula
│   │   ├── Topology / Representation
│   │   └── Task space / Workspace
│   │
│   └── Ch 3: Rigid-Body Motions
│       ├── Rotation matrix R ∈ SO(3)
│       ├── Exponential coordinates
│       ├── Twist (6D 속도)
│       ├── Wrench (6D 힘+모멘트)
│       └── Homogeneous transform T ∈ SE(3)
│
├── [Kinematics]
│   ├── Ch 4: Forward Kinematics (Open Chain)
│   │   ├── PoE (Space frame)
│   │   ├── PoE (Body frame)
│   │   └── D-H (Appendix C)
│   │
│   ├── Ch 5: Velocity Kinematics & Statics
│   │   ├── Jacobian (Space / Body)
│   │   ├── Singularity
│   │   ├── Manipulability ellipsoid
│   │   └── Static force: τ = Jᵀ F
│   │
│   ├── Ch 6: Inverse Kinematics (Open Chain)
│   │   ├── Analytic (6R PUMA, Stanford)
│   │   ├── Numerical (Newton-Raphson)
│   │   └── Redundancy + pseudoinverse
│   │
│   └── Ch 7: Closed Chain Kinematics
│       ├── 5-bar, Stewart-Gough
│       ├── 일반 closed chain
│       └── Singularity (actuated + passive 결합)
│
├── [Dynamics]
│   └── Ch 8: Dynamics of Open Chains
│       ├── Lagrangian
│       ├── Newton-Euler (recursive)
│       ├── Forward / Inverse / Task-space
│       └── Actuator + gearing + friction
│
├── [Motion]
│   ├── Ch 9: Trajectory Generation
│   │   ├── Point-to-point
│   │   ├── Via point (polynomial)
│   │   └── Time-optimal scaling
│   │
│   └── Ch 10: Motion Planning
│       ├── Grid methods
│       ├── Sampling (RRT, PRM)
│       └── Potential fields
│
├── [Control]
│   └── Ch 11: Robot Control
│       ├── Motion control
│       ├── Force control
│       ├── Hybrid motion-force
│       ├── Impedance / Admittance
│       └── Computed torque
│
├── [Interaction]
│   └── Ch 12: Grasping & Manipulation
│       ├── Contact modeling
│       ├── Form closure / Force closure
│       └── Pushing, dynamic carry
│
└── [Mobility]
    └── Ch 13: Wheeled Mobile Robots
        ├── Omnidirectional (holonomic)
        ├── Car-like (nonholonomic)
        ├── Odometry
        └── Mobile manipulation
```

## 3.2 학습 진도 체크리스트

### Ch 1 의 자가 검증
- [ ] 본 책의 3 가지 범위와 *범위 밖* 2 가지를 외우고 있다
- [ ] 메커니즘 5 요소를 한 줄씩 설명할 수 있다
- [ ] Revolute vs Prismatic joint 의 공간 구속 개수 (5 / 5) 를 안다
- [ ] Open chain 과 closed chain 을 4 기준 (예시, actuation, FK, IK) 으로 비교 가능
- [ ] 평면·공간 자유 강체의 DoF (3 / 6) 와 분해 (위치+자세) 가 자연스럽다
- [ ] Exponential coordinate 의 직관 (단위 축 ω̂ 주변 θ 회전) 을 안다
- [ ] τ = Jᵀ F 의 의미와 가상일의 원리 연결을 안다
- [ ] Backlash 와 slippage 의 정의·약점 transmission 종류를 구분한다
- [ ] Holonomic vs nonholonomic 의 차이를 자동차 평행주차로 설명할 수 있다
- [ ] 12 챕터의 문제·도구를 한 줄씩 외울 수 있다

### 다음 학습 (Ch 2 시작 전 워밍업)
- [ ] 평면 4-bar linkage 의 DoF 를 Grübler 로 계산해 본다
- [ ] Spherical (3 DoF) joint 가 부과하는 공간 구속 개수 (3) 의 도출 확인
- [ ] task space 의 정의를 자기 말로 정리

## 3.3 연관 학습 흐름

```
이전 (선수):
  선형대수 (행렬·고유값) ──┐
  미적분 (ODE, 편미분) ───┼── Modern Robotics
  강체역학 (F=ma, 모멘트) ─┘

현재: Ch 1 Preview  ← 책 전체 thumbnail

다음:
  Ch 2 Configuration Space → Ch 3 Rigid-Body Motions
                          ↓
                  Ch 4 Forward Kinematics (PoE)
                          ↓
                  Ch 5 Velocity Kinematics (Jacobian)
                          ↓
              ┌───────────┴───────────┐
              Ch 6 Inverse           Ch 7 Closed Chains
                       │
              ┌────────┴────────┐
              Ch 8 Dynamics
                       │
              Ch 9 Trajectory  → Ch 10 Motion Planning
                       │
                       └──────→ Ch 11 Robot Control
                                        │
                       Ch 12 Manipulation ↓
                       Ch 13 Mobile Robots

병행 학습 추천:
  - Linear algebra refresher (Strang 의 책 또는 3Blue1Brown)
  - 공식 사이트 http://modernrobotics.org 의 영상·MATLAB·Python 라이브러리
```
