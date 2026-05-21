# Chapter 2: Configuration Space — 퀴즈

> 14문항. 개념·적용·디버그·면접. *Modern Robotics* (Lynch & Park) 2장 핵심 (DoF·Joint·Grübler·Topology·Holonomic·Task Space) 자가 진단.

---

### Q1. (개념) **DoF (Degrees of Freedom)** 의 *엄밀한 정의* 와, 동전의 앞/뒤가 가능해도 *DoF 가 4 가 아닌* 이유.

<details><summary>정답</summary>

**정의**: 로봇 configuration 을 표현하는 데 필요한 **real-valued (실수, 연속)** 좌표의 *최소* 개수.

**동전 앞/뒤 예시**:
- 평면 위 동전의 configuration: (x, y, θ) + 앞/뒤
- 앞/뒤는 **이산 (discrete) 변수** {앞, 뒤} → real-valued 가 아님
- DoF 정의에 포함 X
- 결과: DoF = **3** (이산 변수는 *별개 connected component* 만 만듦)

핵심: DoF 는 *연속 좌표* 만. 이산 옵션 (state, mode, on/off) 은 별도 분류.

</details>

---

### Q2. (개념) **6 종 표준 joint** (R / P / H / C / U / S) 의 DoF 와 공간에서의 구속 개수를 표로.

<details><summary>정답</summary>

| Joint | 약자 | DoF (f) | 공간 구속 c | 예시 |
|--|--|--|--|--|
| **Revolute** | R | 1 | 5 | 산업 arm joint, 경첩 |
| **Prismatic** | P | 1 | 5 | 슬라이딩 축, gantry |
| **Helical** (Screw) | H | 1 | 5 | 나사 (회전·병진 결합) |
| **Cylindrical** | C | 2 | 4 | 회전+병진 독립 |
| **Universal** | U | 2 | 4 | 차량 steering column |
| **Spherical** | S | 3 | 3 | 볼조인트, 어깨 |

**일반식**: m-DoF joint → 공간 구속 (6 − m), 평면 구속 (3 − m).

</details>

---

### Q3. (개념) **Topology** 와 **Dimension** 의 차이. 2-dim 이지만 *topologically inequivalent* 한 공간 *3 가지* 예시.

<details><summary>정답</summary>

**Topology** = *공간의 모양* (cutting/gluing 없이 같은 공간으로 변형 가능한가). **Dimension** = *좌표 수*.

같은 dim, 다른 topology 의 2-dim 예시:
1. **R² (평면)** — 무한 평면
2. **S² (구면)** — 닫혀 있고 무한 연장 불가
3. **T² (원환면, 도넛)** = S¹ × S¹ — 두 방향 모두 닫혀 있음
4. **R × S¹ (원기둥)** — 한 방향 무한, 한 방향 닫힘

모두 2-dim 이지만 *서로 부드럽게 변형 불가*. dim 만으로 공간 식별 X.

</details>

---

### Q4. (적용) 평면 위 자유 강체의 DoF = 3 을 **세 점 + 강체 제약** 으로 도출하시오.

<details><summary>정답</summary>

평면 강체 위에 세 점 A, B, C 표시.

- 각 점은 평면에서 2 DoF (x, y)
- 세 점 = **2 × 3 = 6 DoF** (제약 전)
- 강체성 → 세 *거리* 가 일정:
  - d(A, B) = const
  - d(B, C) = const
  - d(A, C) = const
- 독립 제약 **3 개**

따라서 DoF = 6 − 3 = **3**.

(공간이라면: 점당 3 DoF, 세 점 9 DoF, 거리 제약 3 → 6 DoF. 추가 *colinear 아님* 제약은 이산 → DoF 영향 X.)

</details>

---

### Q5. (적용) 평면 4-bar linkage 의 DoF 를 Grübler 로 계산하시오. (N, J, ∑f 값 명시)

<details><summary>정답</summary>

```
        joint2
   link1 ━━━━ link2
   ┃              ┃
   joint1        joint3
   ┃              ┃
   ━━━━━━━━━━━━━━━━━━  (지면, link0)
        joint4
```

- N = **4** (지면 + 3 link)
- J = **4** (revolute 4 개)
- ∑f = **4** (R joint 각 1 DoF × 4)
- m = **3** (평면)

$$\text{DoF} = 3(N - 1 - J) + \sum f_i = 3(4 - 1 - 4) + 4 = -3 + 4 = \boxed{1}$$

DoF = 1 — 한 link 의 각도가 결정되면 나머지 자동 결정. 직관과 일치.

</details>

---

### Q6. (적용) **Stewart-Gough platform** 의 DoF 를 Grübler 로 계산. 각 다리는 (U joint) + (P joint) + (S joint), 다리 6 개.

<details><summary>정답</summary>

```
top platform
   |
   다리 1: U - P - S
   다리 2: U - P - S
   ...
   다리 6: U - P - S
   |
지면 (base)
```

- N = **14** (지면 1 + top platform 1 + 다리당 link 2 × 6 = 12)
- J = **18** (다리당 joint 3 × 6)
- 각 다리: U(2) + P(1) + S(3) = 6 DoF, 6 다리 → ∑f = **36**
- m = **6** (공간)

$$\text{DoF} = 6(14 - 1 - 18) + 36 = 6(-5) + 36 = -30 + 36 = \boxed{6}$$

DoF = 6 — 6 다리의 길이를 조절하면 top platform 의 6 DoF 모두 제어. 비행 시뮬레이터에 가장 흔히 쓰는 구조.

</details>

---

### Q7. (적용) 자동차 chassis 의 **nonholonomic 제약식** 을 적으시오. configuration 변수 정의부터.

<details><summary>정답</summary>

**Configuration**: $(x, y, \theta) \in \mathbb{R}^2 \times S^1$
- $x, y$: chassis 의 평면 위치
- $\theta$: 진행 방향 (yaw)

**제약** (no-slip — 바퀴는 옆으로 미끄러지지 못함):

$$\dot{x} \sin\theta - \dot{y} \cos\theta = 0$$

해석:
- 자동차의 *순간 속도 벡터* $(\dot{x}, \dot{y})$ 가 *차체 진행 방향* $(\cos\theta, \sin\theta)$ 와 평행해야
- 즉 횡방향 속도 = 0

이는 **velocity 식 제약 (Pfaffian)** — *configuration 식* 으로 적분 불가능 → **Nonholonomic**.

함의:
- C-space 차원 = 3 그대로 (어디든 갈 수 있음)
- 단, *경로* 가 제약됨 — 즉시 횡이동 불가. 평행주차는 회전+전진 조합으로 가능.

</details>

---

### Q8. (적용) 7-DoF arm 의 **C-space** 와 **Task space** 의 차원·topology 를 적으시오. *redundancy* 의 의미는?

<details><summary>정답</summary>

**C-space**: $T^7 = (S^1)^7$ — 7 개의 revolute joint 각각이 원 $S^1$. 차원 **7**.

**Task space**: $\mathbb{R}^3 \times SO(3)$ — EE 의 위치 3 + 자세 3. 차원 **6**.

**Kinematic Redundancy**: C-space dim (7) > Task space dim (6). 즉 같은 EE 위치·자세에 *무한히 많은* joint configuration 이 대응. 한 차원 redundant.

**활용**:
- Secondary task (joint limit 회피, 장애물 회피, manipulability 최대화) 와 결합 가능
- Inverse Kinematics 시 *pseudo-inverse* (Moore-Penrose) 사용 — 6 장에서 본격

이게 *6-DoF arm 으로 못 하는* 일을 *7-DoF arm* 으로 할 수 있게 함.

</details>

---

### Q9. (디버그) 다음 주장의 무엇이 틀렸나?
> "Grübler's formula 가 어떤 메커니즘이든 *정확한 DoF* 를 줍니다. 결과가 음수면 movable 하지 않다는 뜻입니다."

<details><summary>정답</summary>

**Grübler 는 일반적으로 정확하지만 *기하학적 특이* 에서는 *lower bound* 일 뿐**.

**예시** (overconstrained mechanism):
- 모든 R joint 의 축이 *평행* 인 특수한 메커니즘
- Grübler 가 0 또는 *음수* 를 줘도 실제로 1 DoF 가능

**이유**: Grübler 는 모든 constraint 를 *독립적* 으로 셈. 그러나 *기하학적 우연* 으로 어떤 constraint 가 *다른 constraint 에 의해 자동 만족* 되면 *유효 constraint 수* 감소.

**올바른 해석**:
- Grübler 결과 > 0: *최소* 그만큼의 DoF 보장 (실제로는 더 클 수도)
- Grübler 결과 = 0 또는 음수: *대부분* 안 움직이지만, *특수 기하* 면 movable 가능

의심되면 *kinematic 분석* (Jacobian rank 확인 등) 으로 검증.

</details>

---

### Q10. (디버그) 학생이 *공간 위* 의 동전 (앞/뒤 가능) 의 DoF 를 *4* 라고 답함. 어떻게 정정?

<details><summary>정답</summary>

학생의 추론: 공간 강체 = 6 DoF, 앞/뒤 → +1 = 7? 또는 평면 가정에서 3 + 1 = 4?

**핵심 오류**: 앞/뒤는 *real-valued continuous* 좌표가 아니라 **이산** {앞, 뒤}.

**올바른 답**:
- 동전이 *공간* 안 자유 강체 → DoF = **6** (3D 위치 + 3D 자세)
- 동전이 *평면 위* 자유 강체 → DoF = **3** (x, y, θ)
- 앞/뒤는 *별도의 connected component* — DoF 에 추가 안 됨

**비유**: 두 개의 동전을 두 *서로 분리된 방* 에 둘 수 있다고 해서 DoF 가 늘진 않음. 두 방은 각각 같은 DoF 의 *복사본*.

DoF 정의의 *real-valued continuous* 조건을 강조.

</details>

---

### Q11. (디버그) 다음 주장의 어디가 *잘못* 됐나?
> "강체 자세를 표현할 때 *3 변수 explicit parametrization* (예: roll-pitch-yaw) 이 *9 원소 회전 행렬* 보다 항상 우수합니다. 좌표가 적으니까요."

<details><summary>정답</summary>

**잘못**: "*항상* 우수" 라는 단정. 실제로는 *trade-off*.

**Explicit (예: roll-pitch-yaw, Euler angle, 위도·경도)** 의 약점:
- **Singularity** — 특정 자세에서 좌표 정의 깨짐
  - 예: roll-pitch-yaw 의 *gimbal lock* (pitch = ±90° 에서 yaw 와 roll 이 같은 축이 됨)
  - 위도·경도의 극지점 (lat = ±90°)
- 모든 자세를 *하나의 chart* 로 못 덮을 수 있음
- *알고리즘 수치 안정성* 떨어짐

**Implicit (회전 행렬 R ∈ SO(3), 9 원소 + 6 제약)** 의 장점:
- **Singularity 없음** — 모든 자세 매끄럽게 표현
- 수치 안정 (정규화·orthogonalization 용이)
- 합성 (chain rule) 이 단순 행렬 곱

**본 책의 선택**: **Implicit (R ∈ SO(3))**. 좌표 9 개로 redundant 하지만 *singularity 회피* + *수치 안정* 가치가 큼.

**대안**: Quaternion (4 원소 + 1 제약) — 부분적 절충. 게임·로보틱스 둘 다 흔히 사용. 본 책 Appendix B 에서 다룸.

</details>

---

### Q12. (디버그) 학생이 "6-DoF arm 의 *C-space* 와 *task space* 가 같은 공간이다" 라고 주장. 어떻게 반박?

<details><summary>정답</summary>

**차원만 같고 *공간 자체* 는 다름**.

| | C-space | Task space |
|--|--|--|
| **차원** | 6 | 6 (R³ × SO(3)) |
| **Topology** | $T^6 = (S^1)^6$ — 6 개의 원의 곱 | $\mathbb{R}^3 \times SO(3)$ — 평면 위치 × 회전군 |
| **의미** | 모든 joint 각도 조합 | EE 의 위치·자세 |
| **물리** | arm 의 *내부* 상태 | EE 의 *외부* 상태 |

**대응 (kinematics)**:
- Forward kinematics: $T^6 \to \mathbb{R}^3 \times SO(3)$ (joint 각 → EE 위치)
- Inverse kinematics: $\mathbb{R}^3 \times SO(3) \to T^6$ — 다중해 가능

같은 차원이라도:
- 6-DoF arm 의 workspace 는 task space 의 *제한된 부분*
- 같은 EE 위치·자세에 *여러 joint 조합* 가능 (inverse kinematics 다중해)
- C-space 의 joint limit, task space 의 obstacle 등 *다른 종류 제약*

**한 줄 반박**: "차원이 같다고 공간이 같은 건 아닙니다. R² 와 S² 도 다르듯이."

</details>

---

### Q13. (면접) "Holonomic 과 nonholonomic 의 차이를 *자동차 평행주차* 예시로 1분 안에 설명하시오."

<details><summary>정답</summary>

**자동차의 configuration**: $(x, y, \theta) \in \mathbb{R}^2 \times S^1$, **3 차원** 공간.

**제약**: 바퀴는 옆으로 안 미끄러짐 → 속도가 차체 방향이어야 함:
$$\dot{x} \sin\theta - \dot{y} \cos\theta = 0$$

이 식은 **velocity 식** — *configuration 식 으로 적을 수 없음 (적분 불가)*. → **Nonholonomic**.

**핵심 결과**:
- C-space 차원은 **3 그대로** (감소 X)
- 자동차는 *어디든 갈 수 있음* (평행주차로 옆 자리 진입 가능)
- 단 *경로* 가 제약 — 즉시 횡이동 불가, 회전+전진 조합 필요

**비교 — Holonomic**:
- 만약 자동차가 *옆으로 미끄러질 수 있는 omniwheel* 이면 → holonomic
- C-space 차원도 3 이고 *모든 방향 직접 이동 가능*

**결정적 차이**:
- **Holonomic**: *어디에 갈 수 있나* 가 제한 (configuration 차원 감소)
- **Nonholonomic**: *어떻게 갈 수 있나* (경로) 가 제한 (차원 그대로, 경로 제약)

자동차는 **nonholonomic** — 위치는 어디든 가지만 경로는 제약. 이게 motion planning 을 *복잡하게* 만드는 주범 (13 장).

</details>

---

### Q14. (면접) "Modern Robotics 책은 강체 자세를 *implicit* (회전 행렬) 로 표현합니다. 왜 그런 선택을 했을까요?" 면접 단골.

<details><summary>정답</summary>

**핵심 답변**:

> 강체 자세 표현의 trade-off 에서 본 책은 **수치 안정성과 singularity 회피** 를 우선시했기 때문입니다.

**선택지 비교**:

| 표현 | 좌표 수 | Singularity | 수치 안정 |
|--|--|--|--|
| **회전 행렬 R ∈ SO(3)** (책의 선택) | 9 (+6 제약) | **없음** | 좋음 |
| Roll-Pitch-Yaw / Euler angle | 3 | 있음 (gimbal lock) | 보통 |
| Quaternion | 4 (+1 제약) | 없음 | 좋음 |
| Exponential coordinate $\hat{\omega}\theta$ | 3 | 있음 (작은 회전 근처) | 양호 |

**Implicit 선택의 이유**:
1. **Singularity 없음**: 모든 회전을 *매끄럽게* 표현
2. **합성 (chain rule)**: 행렬 곱 한 번으로 끝남 — 알고리즘적 단순
3. **PoE (Product of Exponentials)** 와 결합: R = exp([ω̂]θ) 로 *합성 시 implicit* (4장)
4. **Twist 와 Wrench**: 6D 표현이 자연스럽게 확장 (3장)
5. **수치 안정**: 회전 행렬을 그대로 누적해도 *정규화* 로 자세 유지

**비용**:
- 좌표 9 개 (3 개 minimal 보다 redundant)
- 메모리·계산 약간 더

**책의 일관성**: 강체 자세 implicit + exponential coordinate (회전축 × 각도) 의 결합 — 이게 본 책의 *기술적 정체성* 이고 PoE / Newton-Euler 알고리즘의 깔끔함의 원천.

</details>
