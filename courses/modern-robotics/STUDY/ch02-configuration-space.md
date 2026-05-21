# Chapter 2: Configuration Space — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 2: Configuration Space** (책 p.11~58) 를 단독 학습 가능한 형태로 재구성한 것입니다.
> 2장은 "로봇이 가질 수 있는 모든 상태의 공간" 이라는 가장 근본적 추상화를 다룬다. 이 개념 위에 3~13장이 모두 쌓인다.

## 들어가기 전에

- **선수 지식**
  - 1장 (책 전체 로드맵) — DoF 의 직관적 의미
  - 선형대수 — 좌표·벡터·constraint equation
  - 기초 미적분 — 편미분 (특히 Pfaffian constraint 의 적분 가능성)
- **학습 목표**
  1. **DoF (Degrees of Freedom)** 의 엄밀한 정의 — *real-valued coordinate 의 최소 개수*
  2. 강체의 평면 (3 DoF) / 공간 (6 DoF) DoF 의 *구속 기반 도출*
  3. **Joint type 6 종** (R / P / H / C / U / S) 의 DoF 와 부과하는 구속
  4. **Grübler's Formula** 와 planar / spatial 식
  5. **Configuration Space (C-space)** 의 *topology* 와 *representation* (explicit vs implicit)
  6. **Holonomic vs Nonholonomic constraint** 의 결정적 차이 — 적분 가능성
  7. **Task space** vs **Workspace** vs **C-space** — 셋 다 다른 개념
- **예상 학습 시간**: 90~120분 (개념 + 수식 + 직관)

---

## 1. Configuration 과 DoF — 가장 근본적 정의

### 1.1 Configuration 이란

> **정의 2.1 (Configuration)**: 로봇의 *모든 점의 위치* 에 대한 완전한 명세. 이를 표현하는 데 필요한 real-valued 좌표의 *최소 개수* 가 **자유도 (DoF)**. 모든 가능한 configuration 의 n-차원 공간을 **Configuration Space (C-space)** 라 하며, 한 configuration 은 C-space 상의 한 점.

핵심: *그 로봇이 가질 수 있는 모든 상태* 의 *추상적 공간*. 이 책의 거의 모든 후속 장이 *C-space 위에서* 수학을 한다.

### 1.2 예시 — 직관 잡기

| 시스템 | DoF | 좌표 |
|--|--|--|
| 문 (경첩 회전) | **1** | 회전각 θ |
| 평면 위의 한 점 | **2** | (x, y) |
| 평면 위의 동전 (앞면 가정) | **3** | (x, y, θ) |
| 평면 위의 동전 (앞/뒤 가능) | **여전히 3** | + discrete {앞, 뒤} (real-valued 가 아니므로 DoF 에 안 들어감) |
| 공간 안의 자유 강체 | **6** | 위치 3 + 자세 3 |

> **함정 1**: DoF 는 *real-valued continuous* 좌표만 셈. 동전의 앞/뒤 같은 *이산* 상태는 *별개의 connected component* 를 만들 뿐 DoF 에는 추가 안 됨.

### 1.3 평면 강체의 DoF = 3 의 도출

동전 위에 세 점 A, B, C 를 표시. 평면에서 각 점은 2 DoF → 합 6 DoF.

그러나 *강체* 라는 조건이 점들 사이 거리 일정을 강제 — 3 개의 constraint:
- d(A,B) = const
- d(B,C) = const
- d(A,C) = const

따라서 평면 강체 DoF = **6 − 3 = 3**.

### 1.4 공간 강체의 DoF = 6 — 일반 원칙

공간에서 각 점 3 DoF, 세 점 = 9 DoF. 거리 3 개 constraint = 6.

하지만 *추가로* 세 점이 *colinear* (한 직선 위) 가 아니라는 제약은 *불연속적* 이라 DoF 영향 없음.

**일반 원칙**:

$$\text{DoF} = \underbrace{(\text{모든 점의 자유도 합})}_{\text{독립 변수 수}} - \underbrace{(\text{독립적 강체 제약 수})}_{\text{equality constraint 수}}$$

이 원칙이 다음 절의 Grübler's formula 로 일반화된다.

---

## 2. Joint 의 종류와 부과하는 구속

### 2.1 6 종 표준 joint

```
       R               P                H
   (Revolute)      (Prismatic)       (Helical/Screw)
   회전 1축         병진 1축          나선 1축 (회전+병진 결합)

       C               U                S
   (Cylindrical)   (Universal)      (Spherical)
   회전+병진 독립    회전 2축          회전 3축
```

| Joint | 약자 | DoF (f) | 평면 구속 c | 공간 구속 c | 예시 |
|--|--|--|--|--|--|
| **Revolute** | R | 1 | 2 | **5** | 모든 산업용 arm joint, 경첩 |
| **Prismatic** | P | 1 | 2 | **5** | 슬라이딩 축, gantry |
| **Helical (Screw)** | H | 1 | n/a | **5** | 나사 (회전 ↔ 병진 결합) |
| **Cylindrical** | C | 2 | n/a | **4** | 회전 + 병진 독립 |
| **Universal** | U | 2 | n/a | **4** | 차량 steering column |
| **Spherical** | S | 3 | n/a | **3** | 볼조인트, 인간 어깨 |

### 2.2 일반 식

> **공간** 에서: m-DoF joint 는 (6 − m) 개의 구속을 인접 강체에 부과.
> **평면** 에서: m-DoF joint 는 (3 − m) 개의 구속.

R, P 모두 1 DoF 이고 공간 구속 5. 직관적으로 — 공간 자유 강체의 6 DoF 중 5 자유도를 *제거* 하고 남은 1 자유도만 허용.

### 2.3 Joint 가 *허용* 하는 motion vs *제거* 하는 motion

```
공간에서 R joint:
  허용: ω̂ 축 주변 회전 (1 DoF)
  제거: 그 축에 수직인 2 translation + 회전축 다른 2 회전 (총 5 자유도)
```

이 관점이 Grübler's formula 의 계산 기반.

---

## 3. Grübler's Formula — 메커니즘의 DoF

### 3.1 공식

> **공간**:
> $$\text{DoF} = m(N - 1 - J) + \sum_{i=1}^{J} f_i, \quad m = 6$$
>
> **평면**:
> $$\text{DoF} = m(N - 1 - J) + \sum_{i=1}^{J} f_i, \quad m = 3$$
>
> - $N$ = link 수 (지면 포함)
> - $J$ = joint 수
> - $f_i$ = i 번째 joint 의 DoF

또는 등가 형태 (구속 기반):

$$\text{DoF} = m(N - 1) - \sum_{i=1}^{J} c_i, \quad c_i = m - f_i$$

### 3.2 도출 직관

```
1) link N 개 (지면 제외 N-1 개의 자유 강체) — 각 m DoF
   → m(N-1) DoF (구속 전)

2) joint J 개 — 각 c_i 구속
   → -∑ c_i

3) c_i = m - f_i 이므로:
   DoF = m(N-1) - ∑(m - f_i) = m(N-1) - m·J + ∑f_i = m(N-1-J) + ∑f_i
```

### 3.3 예시 1 — 평면 4-bar linkage

```
        joint2
   link1 ━━━━ link2
   ┃              ┃
   joint1        joint3
   ┃              ┃
   ━━━━━━━━━━━━━━━━━━  (지면, link0 = ground)
        joint4
```

- $N = 4$ (지면 포함)
- $J = 4$ (revolute, 평면)
- $\sum f_i = 4$
- $m = 3$ (평면)

$$\text{DoF} = 3(4 - 1 - 4) + 4 = 3(-1) + 4 = -3 + 4 = \boxed{1}$$

DoF = 1 — 4-bar linkage 가 *한 자유도* 만 가짐. 직관과 일치 (한 link 의 각도가 결정되면 나머지 다 결정).

### 3.4 예시 2 — Stewart-Gough Platform (공간)

6 개의 다리 (각 다리: U joint + P joint + S joint), top platform.

- $N = 14$ (지면 + top platform + 다리당 2 link × 6 = 12)
- $J = 18$ (다리당 3 joint × 6)
- 각 다리 joint 자유도: U(2) + P(1) + S(3) = 6, 총 36

$$\text{DoF} = 6(14 - 1 - 18) + 36 = 6(-5) + 36 = -30 + 36 = \boxed{6}$$

DoF = 6 — Stewart-Gough 는 *6 DoF*. 다리 6 개의 길이를 조절하면 top platform 의 6 DoF (위치 3 + 자세 3) 모두 제어 가능.

### 3.5 함정 — Grübler 는 *lower bound* (overconstrained)

Grübler's formula 가 *항상* 정확한 건 아님. 특수한 기하 (overconstrained mechanism) 에서는 *실제 DoF > Grübler 의 결과* 가 될 수 있음.

예: 3개의 평행 revolute joint 만으로 구성된 메커니즘 — Grübler 가 0 (또는 음수) 을 줘도 실제로는 1 DoF 가질 수 있음.

> **원칙**: Grübler 는 *대부분* 옳지만, *기하학적 특이상황* 에서 lower bound 일 뿐. 의심되면 직접 분석.

---

## 4. Configuration Space — Topology 와 Representation

### 4.1 Topology (모양) vs Dimension (차원)

같은 *차원* 의 두 공간이 *다른 topology* 일 수 있다.

```
1 차원 예시:
- 직선 R (양 끝이 무한)
- 원 S¹ (양 끝이 연결)

같은 1 차원이지만 topology 다름.
```

```
2 차원 예시:
- 평면 R²
- 구면 S² (지구 표면)
- 원환면 T² = S¹ × S¹ (도넛 표면)
- 원기둥 R × S¹

모두 2-dim 이지만 *topologically inequivalent*.
```

> **Topological equivalence**: 두 공간이 *부드럽게* (cutting / gluing 없이) 서로 변형될 수 있으면 동치. 평면 ≠ 구면 (구면은 *닫혀있어* 무한 연장 불가).

### 4.2 실제 로봇의 C-space topology

| 시스템 | C-space topology | 차원 |
|--|--|--|
| 1 회전 joint (혹은 진자) | S¹ | 1 |
| 2 회전 joint (planar 2R arm) | T² = S¹ × S¹ | 2 |
| 평면 자유 강체 (book sliding on table) | R² × S¹ | 3 |
| 공간 자유 강체 (rigid body in space) | R³ × SO(3) | 6 |
| 구면 위의 점 | S² | 2 |

SO(3) = 3D rotation group (다음 장에서 본격적으로 다룸).

### 4.3 Representation — explicit vs implicit

같은 공간을 *어떻게 좌표화* 할지의 문제.

#### Explicit parametrization

*최소 좌표 수* 로 직접 매개변수화. 예: 구면 S² → 위도·경도 (lat, lon).

장점: 좌표 수 = DoF (minimal).
단점:
- **Singularity** — 좌표 자체가 깨지는 점 (극지점 lat = ±90°, lon 정의 안 됨)
- 모든 점을 *하나의 chart* 로 못 덮을 수 있음

#### Implicit parametrization

*더 큰 공간* + *제약식*. 예: 구면 S² → (x, y, z) ∈ R³ + 제약 x² + y² + z² = 1.

장점: **Singularity 없음**, 수치적 안정.
단점: 좌표 수 > DoF (redundant).

> **본 책의 선택**: 강체 자세를 표현할 때 **implicit** (회전 행렬 R ∈ SO(3), 9 개 원소 + 6 개 제약). singular 회피 + 알고리즘 수치 안정.

대안 (3장 미리보기): exponential coordinate ω̂θ (3-vector, minimal) — 회전 *0 근처* 에서만 specific singular, 그러나 *합성* 시 implicit (R = exp([ω̂]θ)) 으로 사용.

### 4.4 Task Space vs C-space (전조)

C-space = 로봇 *전체* 의 자유도 공간 (예: 7-joint arm 의 C-space = T⁷).
Task space = end-effector 의 *목적* 공간 (예: 3D 위치+자세 = R³ × SO(3), 6-dim).

이 둘은 일반적으로 *다르다*. 5장에서 본격적으로 다룸. 이번 장에서는 정의만.

---

## 5. Configuration vs Velocity Constraints

### 5.1 Holonomic constraint

> **Holonomic**: 제약식이 *configuration 만의 함수* 로 적힘.
>
> $$g(\theta) = 0, \quad g: \mathbb{R}^n \to \mathbb{R}^k$$
>
> 효과: C-space 의 *차원을 감소* 시킴. n-dim 시작 → (n-k)-dim 으로.

예시: 4-bar linkage 의 closed-loop constraint, 두 강체가 같은 점을 공유하는 joint.

홀로노믹 제약은 *configuration 식* 그 자체로 적힘 → C-space 의 *subset* 으로 표현 가능.

### 5.2 Pfaffian constraint

velocity (속도) 단계의 제약:

$$A(\theta) \dot{\theta} = 0, \quad A(\theta) \in \mathbb{R}^{k \times n}$$

이 형태가 **Pfaffian constraint**.

Pfaffian 의 두 가지 종류:

1. **적분 가능 (integrable) 한 Pfaffian** — *holonomic 의 미분형*. 어떤 g(θ) 가 있어 dg/dt = A(θ)θ̇ 로 적분 → 결국 g(θ) = 0 인 holonomic 과 등가.

2. **적분 불가능 (non-integrable) 한 Pfaffian** — *nonholonomic*. configuration 식으로 환원 불가.

### 5.3 Nonholonomic constraint — 자동차 예

**자동차** (no-slip 가정):
- chassis 의 configuration: (x, y, θ) ∈ R² × S¹ (평면 위치 + 진행 방향)
- 제약: 바퀴는 *옆으로 미끄러지지 못함* → 속도가 차체 방향이어야

$$\dot{x} \sin\theta - \dot{y} \cos\theta = 0$$

이 식은 *velocity 식*. *configuration 식* 으로 환원 불가 (적분 불가능). 자동차의 *configuration* 자체는 (x, y, θ) 공간 전체 (3-dim) 어디든 갈 수 있음 — 단지 *순간 속도* 만 제약.

```
시사점:
- C-space 차원 = 3 (감소 X)
- 그러나 *어떤 경로* 로 갈 수 있는가는 제약됨
- 평행주차 가능 (회전+전진 조합으로 어디든 도달) but 직접 횡이동 불가
```

> **결정적 차이**:
> - Holonomic: *어디에 갈 수 있나* 가 제한
> - Nonholonomic: *어떻게 갈 수 있나* (경로) 가 제한

### 5.4 적분 가능성 판별 — 직관

Pfaffian 제약 $A(\theta)\dot{\theta} = 0$ 이 적분 가능한지의 수학적 판별은 **Frobenius theorem** 등으로 가능. 이 책 범위 밖. 직관:

- 한 Pfaffian 제약 (k=1) 도 *일반적으로* 적분 불가
- 자동차의 경우도 한 제약 (`sin·cos` 식) 이지만 nonholonomic
- holonomic 인 경우는 *드물고 특수* (예: 4-bar linkage 의 loop closure 의 미분형)

13 장 (mobile robots) 에서 nonholonomic 의 motion planning · control 을 깊이 다룸.

---

## 6. Task Space 와 Workspace

### 6.1 정의 분리

| 개념 | 정의 |
|--|--|
| **C-space** | 로봇 *전체* 의 모든 가능 configuration 의 공간 (예: 7-joint arm → T⁷) |
| **Task Space** | task 가 자연스럽게 표현되는 공간 (보통 end-effector 의 위치·자세) |
| **Workspace** | end-effector 가 *실제로 도달 가능* 한 task space 의 subset |

### 6.2 예시 — 6-DoF 산업용 arm

- **C-space**: T⁶ (6 개 회전 joint 각도) — 차원 6
- **Task space**: R³ × SO(3) (EE 위치 3 + 자세 3) — 차원 6
- **Workspace**: task space 안에서 *팔이 닿을 수 있는* 영역 (보통 *볼록하지 않은* 모양)

여기서 C-space dim = task space dim = 6. 우연히 같은 차원.

### 6.3 Redundancy — C-space dim > task space dim

7-DoF arm:
- **C-space**: T⁷ — 차원 7
- **Task space**: R³ × SO(3) — 차원 6

C-space 가 한 차원 더 많음 → **kinematic redundancy** (운동학적 잉여). 같은 EE 위치·자세에 *무한히 많은* joint configuration 이 대응.

활용: secondary task (joint limit 회피, 장애물 회피) 와 결합 가능. 6 장 (Inverse Kinematics) 에서 본격.

### 6.4 Under-actuation — C-space dim 작음

차량형 mobile robot:
- **C-space**: R² × S¹ — 3 dim
- **Task space**: R² (chassis 의 평면 위치만 신경 쓰면) — 2 dim

C-space 가 더 크지만 nonholonomic 제약으로 *경로* 가 제약됨. 13 장.

### 6.5 함정 — 차원 ≠ 등가

| 함정 | 정정 |
|--|--|
| C-space dim 과 task space dim 이 같으면 *비슷한 공간* | 차원은 같아도 *topology* 와 *물리적 의미* 다름. 7-DoF arm 의 redundancy 가 그 예. |
| Workspace 가 task space 와 동일 | 거의 다름. Workspace 는 *도달 가능* 부분만. arm 외 *팔이 안 닿는* 영역이 task space 에 있을 수 있음. |
| EE = arm 의 마지막 link | end-effector 는 *task 기준* 으로 정의. arm 의 마지막 link 위에 grip·tool 부착되어 EE 로 동작 가능. |

---

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| DoF 에 *이산 변수* 포함 | DoF 는 *real-valued continuous* 만. 동전 앞/뒤는 별개 component. |
| Joint type 의 DoF 와 *공간 구속* 혼동 | 1-DoF joint → 공간 구속 5 (= 6-1). m-DoF → (6-m). |
| Grübler 가 *항상 정확* 하다고 가정 | 일반적으로 정확하지만 *기하학적 특이* (overconstrained) 에서는 *lower bound* |
| Topology 와 dimension 혼동 | 같은 차원의 다른 topology 가능 (R² vs S² vs T²). dim 만으로 공간 식별 X. |
| Implicit vs explicit 의 trade-off 모름 | Implicit: singularity 없음 + 수치 안정 (좌표 redundant). Explicit: 최소 좌표 (singularity). 본 책은 강체 자세에 implicit (회전 행렬) |
| Holonomic 과 Nonholonomic 을 *제약 있냐 없냐* 로 분류 | 둘 다 제약 있음. 차이는 *configuration 식 으로 적힘* 여부. Holonomic = configuration 수준, Nonholonomic = velocity 수준 (적분 불가). |
| 자동차의 nonholonomic 이 *DoF 감소* 인 줄 앎 | C-space dim 은 3 그대로. 변하는 건 *경로* (어떤 trajectory 로 갈 수 있나). |
| C-space dim = task space dim 가정 | redundancy (7-DoF arm), under-actuation (mobile robot) 시 다름. |
| Workspace = task space 전체 | Workspace 는 *도달 가능* subset. 보통 비볼록·복잡한 모양. |
| 4-bar linkage 의 DoF 계산을 *joint 자유도 합* 으로만 | Grübler 의 (N-1-J) 항을 잊지 말 것. 자유도 합만으로는 closed loop 처리 안 됨. |

---

## 자가점검

1. **DoF** 의 정의를 한 줄로. 동전이 앞뒤 가능한 경우 *4 DoF 가 아닌* 이유.
2. 평면·공간 자유 강체의 DoF (3 / 6) 를 *3 점 + 강체 제약* 으로 도출하시오.
3. **6 종 joint** (R / P / H / C / U / S) 의 DoF 와 *공간에서의 구속 개수* 를 표로 적으시오.
4. Grübler's Formula 의 *공간 식* 과 평면 식. 각 기호의 의미.
5. 평면 4-bar linkage 의 DoF 를 Grübler 로 계산 (N, J, ∑f, 결과).
6. Grübler 가 *lower bound* 인 경우의 예시 시나리오.
7. **Topology** 와 **dimension** 의 차이. 2-dim 인데 *topologically inequivalent* 한 공간 3 가지.
8. **Implicit** vs **Explicit** parametrization 의 trade-off. 본 책의 선택은?
9. **Holonomic** vs **Nonholonomic** 제약의 핵심 차이를 *자동차 평행주차* 로 설명.
10. **C-space** / **Task space** / **Workspace** 셋의 정의와 차이.
11. **Kinematic redundancy** 의 의미. 7-DoF arm 의 C-space, task space 의 차원은?
12. Task space 와 C-space 의 차원이 *같다면* 두 공간이 *같은 공간* 인가?

<details><summary>풀이</summary>

1. **로봇 configuration 을 표현하는 데 필요한 *real-valued continuous* 좌표의 최소 수**. 동전의 앞/뒤는 *이산* 변수 → DoF 에 안 들어감 (별개 connected component 만 생성). DoF = 3 그대로.

2. **평면**: 세 점 (xA, yA), (xB, yB), (xC, yC) → 각 2 DoF, 합 6. 강체 제약 3 (각 점 쌍 거리 일정) → 6 − 3 = **3**.
   **공간**: 세 점 × 3 좌표 = 9. 강체 제약 3 (거리). 추가 제약 (점 colinear 아님 등) 은 이산적이라 DoF 무관. → 9 − 3 = **6**.

3. | Joint | DoF | 공간 구속 |
   |--|--|--|
   | R | 1 | 5 |
   | P | 1 | 5 |
   | H | 1 | 5 |
   | C | 2 | 4 |
   | U | 2 | 4 |
   | S | 3 | 3 |
   일반: m-DoF joint → (6 − m) 구속.

4. **공간**: `DoF = 6(N − 1 − J) + ∑f_i`
   **평면**: `DoF = 3(N − 1 − J) + ∑f_i`
   - N = link 수 (지면 포함)
   - J = joint 수
   - f_i = i 번째 joint 의 DoF

5. 평면 4-bar: N = 4 (지면+3), J = 4 (R joint), ∑f = 4. → `3(4-1-4) + 4 = -3 + 4 = 1`. **DoF = 1**.

6. *Overconstrained mechanism*. 예: 3개의 평행 revolute joint 만으로 구성된 메커니즘 — Grübler 는 0 또는 음수를 주지만 실제로는 1 DoF 가능. 또는 모든 joint 가 한 평면·축에 놓인 특수 기하.

7. **Topology** = *모양 (cutting/gluing 없이 같은가)*, **dimension** = *좌표 수*. 2-dim 이지만 topology 다른 예: R² (평면), S² (구면), T² (도넛), R × S¹ (원기둥).

8. **Implicit**: 더 큰 공간 + 제약식. *singularity 없음* + 수치 안정, 좌표 redundant. **Explicit**: 최소 좌표. *singularity 발생 가능* (예: lat/lon 의 극지점). **본 책**: 강체 자세는 **implicit** (회전행렬 R ∈ SO(3), 9 원소 + 6 제약).

9. **자동차**: 횡 미끄러짐 안 됨 → velocity 식 `ẋ sin θ − ẏ cos θ = 0` 만으로 제약. *configuration 식 으로 적을 수 없음 (적분 불가)* → **Nonholonomic**. 그래도 평행주차로 어디든 도달 가능 (C-space 차원 감소 X) — 다만 *경로* 가 제약됨.

10. **C-space**: 로봇 *전체* 의 모든 configuration. **Task space**: task 가 자연스럽게 표현되는 공간 (보통 EE 의 위치·자세). **Workspace**: task space 안에서 *실제 도달 가능* 한 subset.

11. **Kinematic redundancy**: C-space dim > task space dim. 같은 EE 위치·자세에 *무한히 많은* joint 조합. 7-DoF arm: C-space = T⁷ (dim 7), task space = R³ × SO(3) (dim 6). 7 > 6 → 한 차원 redundant.

12. **아니오**. 같은 차원이라도 *topology* 와 *물리적 의미* 가 다를 수 있다. 6-DoF arm 의 C-space (T⁶) 와 task space (R³ × SO(3)) 는 둘 다 6-dim 이지만 다른 공간. 또한 dim 이 같아도 *workspace* 는 task space 의 *제한된 부분만* 차지.

</details>

---

## 다음 학습으로

- **Chapter 3: Rigid-Body Motions** — 본격적으로 *회전 행렬* (R ∈ SO(3)), *exponential coordinate* (`R = exp([ω̂]θ)`), *homogeneous transformation matrix* (T ∈ SE(3)), **twist** (6D 속도), **wrench** (6D 힘+모멘트). 2장의 *추상적 C-space* 가 *구체적 수학 표현* 으로 변환됨.
- 보강:
  - **Frobenius theorem** — Pfaffian constraint 의 적분 가능성 판별. 본 책 외 별도 학습 (미분기하·제어이론 교재).
  - **Topology 기초** — *manifold*, *homeomorphism*, *atlas* 등의 개념. 깊이 가려면 differential topology.
  - 실습: 평면 5-bar linkage, Delta robot, SCARA arm 의 DoF 를 Grübler 로 계산해보기.
