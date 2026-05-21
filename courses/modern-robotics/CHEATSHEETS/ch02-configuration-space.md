# Chapter 2: Configuration Space — 치트시트

> *Modern Robotics* (Lynch & Park, 2017) 2장. DoF / Joint 6 종 / Grübler / Topology / Holonomic vs Nonholonomic / Task Space.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄

1. **DoF** = configuration 표현에 필요한 *real-valued continuous* 좌표의 최소 수. 이산 변수 (앞/뒤) 는 안 들어감.
2. **자유 강체 DoF**: 평면 3 (x, y, θ), 공간 6 (위치 3 + 자세 3). 세 점 (점당 m DoF) − 강체 거리 제약 3 = m·3 − 3 으로 도출.
3. **Joint 6 종**: R/P/H (1 DoF, 공간 구속 5) · C/U (2 DoF, 4) · S (3 DoF, 3). 일반식: m-DoF joint → (6-m) 구속.
4. **Grübler**: `DoF = m(N-1-J) + ∑f_i`. m=3 평면 / m=6 공간. *기하학적 특이* 에서는 lower bound.
5. **Topology ≠ Dimension**: 2-dim 이지만 R², S², T² (도넛), R×S¹ 모두 다른 공간. *Implicit (R∈SO(3))* 이 본 책의 선택 — singularity 없음 + 수치 안정.
6. **Holonomic** (configuration 제약, 차원 감소) vs **Nonholonomic** (velocity 제약 Pfaffian, 차원 그대로 but 경로 제약). 자동차는 nonholonomic — 어디든 가지만 평행주차 필요.

## 가장 중요한 식 3개

```
(1) DoF (Grübler's Formula)
    공간:  DoF = 6(N − 1 − J) + ∑ f_i
    평면:  DoF = 3(N − 1 − J) + ∑ f_i
    
    N = link 수 (지면 포함), J = joint 수, f_i = i 번째 joint 의 DoF
```

```
(2) Joint 구속 일반식
    공간: m-DoF joint → 인접 강체에 (6 − m) 구속
    평면: m-DoF joint → 인접 강체에 (3 − m) 구속
    
    R, P, H (1 DoF) → 공간 5 구속 / 평면 2 구속
```

```
(3) 자동차 Nonholonomic 제약 (no-slip wheels)
    ẋ sin θ − ẏ cos θ = 0
    
    velocity 식 (Pfaffian) — configuration 식으로 적분 불가
    → C-space 차원 3 그대로, 경로만 제약
```

## 면접 한 줄 답변

- **Q. DoF 의 정의는?** → configuration 을 표현하는 데 필요한 **real-valued continuous** 좌표의 최소 수. 이산 변수 (앞/뒤·on/off) 는 별개 component, DoF 영향 없음.
- **Q. 4-bar linkage 의 DoF 는?** → Grübler: `3(4-1-4) + 4 = 1`. **DoF = 1**. 한 link 의 각도가 결정되면 나머지 자동 결정.
- **Q. Holonomic vs Nonholonomic 의 차이?** → Holonomic 은 *configuration 식 제약* (C-space 차원 감소). Nonholonomic 은 *velocity 식 제약 (적분 불가)*. 차원은 그대로, *경로* 만 제약. 자동차가 대표 (평행주차 필요).
- **Q. C-space, Task space, Workspace 의 차이?** → **C-space** = 로봇 전체 자유도 공간. **Task space** = EE 의 자유도 공간 (보통 R³×SO(3)). **Workspace** = task space 안에서 *실제 도달 가능* 한 subset.

---

# 2. Quick Reference (실무 복붙)

## 2.1 Joint 종류 + 구속

| Joint | 약자 | DoF (f) | 평면 c | 공간 c | 예시 |
|--|--|--|--|--|--|
| **Revolute** | R | 1 | 2 | **5** | arm joint, 경첩 |
| **Prismatic** | P | 1 | 2 | **5** | gantry, 슬라이딩 |
| **Helical (Screw)** | H | 1 | — | **5** | 나사 |
| **Cylindrical** | C | 2 | — | **4** | 회전+병진 독립 |
| **Universal** | U | 2 | — | **4** | steering column |
| **Spherical** | S | 3 | — | **3** | 볼조인트, 어깨 |

**일반식**: m-DoF joint → 공간 (6 − m) 구속.

## 2.2 Grübler's Formula

```
공간 (m=6): DoF = 6(N − 1 − J) + ∑ f_i
평면 (m=3): DoF = 3(N − 1 − J) + ∑ f_i
```

**Worked examples**:

| 메커니즘 | N | J | ∑f | m | DoF |
|--|--|--|--|--|--|
| 평면 4-bar linkage | 4 | 4 | 4 | 3 | **1** |
| Stewart-Gough (U+P+S × 6) | 14 | 18 | 36 | 6 | **6** |
| Delta robot (간단화) | 8 | 12 | 18 | 6 | **3** |
| SCARA (RRPR) | 5 | 4 | 4 | 6 | (open chain → ∑f = **4**) |

> Open chain (직렬) 은 ∑f 가 곧 DoF (Grübler 의 (N-1-J) 항이 -1 로 끝).

## 2.3 자유 강체 DoF

| 공간 | DoF | 분해 |
|--|--|--|
| 평면 | **3** | x, y + 각도 θ |
| 공간 | **6** | x, y, z + 자세 3 (roll, pitch, yaw 또는 회전축 + 각) |

## 2.4 C-space Topology

| 시스템 | C-space | 차원 |
|--|--|--|
| 1 회전 joint | S¹ | 1 |
| 2 회전 joint (planar 2R) | T² = S¹×S¹ | 2 |
| 평면 자유 강체 | R²×S¹ | 3 |
| 공간 자유 강체 | R³×SO(3) | 6 |
| 구면 위의 점 | S² | 2 |
| n 회전 joint 연쇄 | Tⁿ | n |
| 자동차 chassis | R²×S¹ | 3 |

## 2.5 Representation — Implicit vs Explicit

| | Implicit | Explicit |
|--|--|--|
| 정의 | 더 큰 공간 + 제약식 | 최소 좌표 |
| 예 | R∈SO(3) (9 원소 + 6 제약) | RPY (3 좌표) |
| Singularity | **없음** | 있음 (gimbal lock 등) |
| 수치 안정 | 좋음 | 보통 |
| 좌표 수 | 많음 (redundant) | 최소 (DoF 와 같음) |
| **본 책 선택** | **O** (R∈SO(3)) | X |

## 2.6 Constraint 분류

| 종류 | 형태 | C-space 효과 | 적분 가능? |
|--|--|--|--|
| **Holonomic** | g(θ) = 0 | 차원 감소 | 자명히 가능 |
| **Pfaffian (integrable)** | A(θ)θ̇ = 0 의 적분형 | 차원 감소 | 가능 (holonomic 의 미분) |
| **Pfaffian (nonintegrable)** | A(θ)θ̇ = 0 적분 불가 | 차원 유지, **경로 제약** | **불가** |
| = **Nonholonomic** | (위와 동일) | (위와 동일) | (위와 동일) |

**예시**:
- Holonomic: 4-bar linkage 의 loop closure, 두 강체 공유 joint
- Nonholonomic: 자동차 wheels, 공·자전거 굴림

## 2.7 C-space / Task space / Workspace

| | 정의 | 6-DoF arm 예 | 7-DoF arm 예 |
|--|--|--|--|
| **C-space** | 모든 joint configuration | T⁶ (dim 6) | T⁷ (dim 7) |
| **Task space** | EE 의 위치·자세 공간 | R³×SO(3) (dim 6) | R³×SO(3) (dim 6) |
| **Workspace** | task space 중 EE 도달 가능 subset | (제한된 영역) | (제한된 영역) |
| **Redundancy** | C-space dim > Task space dim | — | 1 차원 redundant |

## 2.8 자주 빠지는 함정

| 함정 | 정정 |
|--|--|
| DoF 에 이산 변수 포함 | real-valued continuous 만 |
| Joint DoF 와 구속 혼동 | m-DoF → (6-m) 구속 |
| Grübler 항상 정확 가정 | 기하학적 특이에서 lower bound |
| Topology = Dimension 가정 | 같은 dim 다른 topology 가능 |
| Implicit/Explicit trade-off 무지 | Implicit: singularity 없음 (책 선택) / Explicit: 최소 좌표 |
| Holonomic/Nonholonomic 의 차이 모름 | configuration 제약 (차원 감소) vs velocity 제약 (경로 제약) |
| 자동차 nonholonomic = DoF 감소 | 차원 유지, 경로만 제약 |
| C-space ≈ Task space 가정 | 차원·topology·의미 모두 다를 수 있음 |
| Workspace = Task space 전체 | Workspace 는 도달 가능 subset |

## 2.9 약어 표

| 약어 | 풀어쓰기 |
|--|--|
| DoF | Degrees of Freedom |
| R / P / H / C / U / S | Revolute / Prismatic / Helical / Cylindrical / Universal / Spherical |
| C-space | Configuration Space |
| SO(3) | Special Orthogonal Group (3D 회전군) |
| SE(3) | Special Euclidean Group (3D 강체운동군) |
| T^n | n-torus (n 개의 S¹ 곱) |
| EE | End-Effector |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 3.1 책 전체 + Ch 2 상세

```
Modern Robotics
│
├── [Ch 1] Preview (책 전체 thumbnail)
│
├── [Ch 2] Configuration Space          <- 현재 위치
│   │
│   ├── DoF 정의
│   │   ├── real-valued continuous 좌표
│   │   ├── 이산 변수 제외
│   │   └── 동전 앞/뒤의 함정
│   │
│   ├── 자유 강체 DoF
│   │   ├── 평면 3 (3점 6 - 거리 3)
│   │   └── 공간 6 (9 점좌표 - 거리 3)
│   │
│   ├── Joint 6 종 + 구속
│   │   ├── R, P, H (1 DoF)
│   │   ├── C, U (2 DoF)
│   │   ├── S (3 DoF)
│   │   └── 일반식: m-DoF → (6-m) 구속
│   │
│   ├── Grübler's Formula
│   │   ├── 공간 6(N-1-J) + ∑f
│   │   ├── 평면 3(N-1-J) + ∑f
│   │   ├── 4-bar linkage = 1
│   │   ├── Stewart-Gough = 6
│   │   └── 기하적 특이 (lower bound)
│   │
│   ├── Topology vs Representation
│   │   ├── Topology: 공간의 모양
│   │   ├── R² ≠ S² ≠ T² (같은 dim)
│   │   ├── Implicit (R∈SO(3)) - 본 책 선택
│   │   └── Explicit (RPY, lat/lon)
│   │
│   ├── Constraints
│   │   ├── Holonomic: g(θ) = 0
│   │   ├── Pfaffian: A(θ)θ̇ = 0
│   │   ├── Nonholonomic: 적분 불가 Pfaffian
│   │   └── 자동차의 sin·cos 제약
│   │
│   └── Task Space vs Workspace
│       ├── C-space ≠ Task space
│       ├── Redundancy (7-DoF arm)
│       └── Workspace ⊂ Task space
│
├── [Ch 3] Rigid-Body Motions   ← 다음
│   ├── Rotation matrix R∈SO(3)
│   ├── Exponential coord
│   ├── Twist, Wrench
│   └── SE(3)
│
├── [Ch 4~13] ...
│
└── 책 전체 4 가지 도구 (1강에서 본 것)
    Exponential / Jacobian / Twist·Wrench / Recursive Newton-Euler
```

## 3.2 Ch 2 학습 진도 체크리스트

### DoF 기본
- [ ] DoF 정의 (real-valued continuous 좌표) 외움
- [ ] 동전 앞/뒤가 DoF 에 안 들어가는 이유 안다
- [ ] 자유 강체 DoF (평면 3 / 공간 6) 의 도출 (3 점 + 강체 제약) 가능

### Joint
- [ ] 6 종 joint (R/P/H/C/U/S) 의 DoF·공간 구속·예시 외움
- [ ] m-DoF joint → (6-m) 공간 구속 일반식 안다

### Grübler's Formula
- [ ] 공간·평면 식 외움
- [ ] 평면 4-bar linkage DoF (= 1) 계산 가능
- [ ] Stewart-Gough DoF (= 6) 계산 가능
- [ ] *기하적 특이* 에서 lower bound 라는 점 안다

### Topology / Representation
- [ ] Topology 와 dimension 의 차이 안다
- [ ] 2-dim 이지만 topology 다른 공간 3 가지 예시 (R²/S²/T²/R×S¹)
- [ ] Implicit vs Explicit 의 trade-off 안다
- [ ] 본 책이 R∈SO(3) 의 *implicit* 을 채택한 이유 (singularity 없음 + 수치 안정)
- [ ] 흔한 시스템의 C-space topology 안다 (자동차 = R²×S¹, etc.)

### Constraints
- [ ] Holonomic 의 정의 (configuration 식 제약) 안다
- [ ] Pfaffian constraint 의 형태 A(θ)θ̇ = 0 안다
- [ ] Nonholonomic = 적분 불가 Pfaffian
- [ ] 자동차의 `ẋ sin θ − ẏ cos θ = 0` 제약 안다
- [ ] *차원 감소* vs *경로 제약* 의 차이 안다

### Task Space
- [ ] C-space, Task space, Workspace 각각의 정의 안다
- [ ] 6-DoF arm 의 C-space (T⁶) 와 Task space (R³×SO(3)) 가 *차원만 같고 다른 공간* 임을 안다
- [ ] 7-DoF arm 의 *kinematic redundancy* (C-space dim 7 > Task space dim 6) 안다
- [ ] Workspace 가 *비볼록 subset* 일 수 있음을 안다

## 3.3 다음 학습 흐름

```
Ch 2 Configuration Space (현재)
    │
    │  ─ 추상적 C-space 개념이 잡혔다면 ─
    v
Ch 3 Rigid-Body Motions ← 다음
    ─ Rotation matrix R∈SO(3)
    ─ Exponential coord R = exp([ω̂]θ)
    ─ Twist (6D 속도), Wrench (6D 힘)
    ─ Homogeneous transform T∈SE(3)

    그 다음:
    │
    v
Ch 4 Forward Kinematics (PoE) ──→ Ch 5 Velocity (Jacobian) ──→ Ch 6 Inverse ...
```

## 3.4 Ch 2 이후 자기 점검 신호

- "이 메커니즘의 DoF 는?" 가 Grübler 로 *자동 계산* 가능 → Ch 2 통과
- "이건 holonomic 인가 nonholonomic 인가?" 가 *velocity 식 vs configuration 식* 으로 자연 답 → 통과
- "C-space 와 task space 의 차이가 뭐지?" 가 *물리적·수학적 의미* 둘 다 답 → 통과
- "이 자세를 어떻게 표현?" 에서 *implicit vs explicit trade-off* 떠오름 → Ch 3 준비 완료

## 3.5 Ch 2 의 직관 한 줄

> **Configuration Space = "그 로봇이 가질 수 있는 모든 상태의 공간."**
>
> Ch 3~13 의 모든 수학·알고리즘이 *이 공간 위에서* 진행된다.
