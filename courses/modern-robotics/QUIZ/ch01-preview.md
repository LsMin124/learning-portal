# Chapter 1: Preview — 퀴즈

> 14문항. 개념·적용·디버그·면접. *Modern Robotics* (Lynch & Park) 1장 (책 p.1~10) 의 핵심 개념 자가 진단.

---

### Q1. (개념) 본 책이 다루는 세 가지 핵심 주제를 한 단어씩 적으세요. 또한 본 책이 다루지 *않는* 로보틱스 주제 두 가지를 들어 보세요.

<details><summary>정답</summary>

다루는 것: **Mechanics** (운동학·동역학), **Planning** (경로·궤적 생성), **Control** (제어 알고리즘).

다루지 않는 것 (대표 두 가지):
- **AI / Perception** — 영상 인식, 자연어, 추론
- **모터 회로 설계 · 임베디드 소프트웨어** — actuator 의 *동특성* 은 다루지만 회로는 별개

추가로 **soft robotics** (link 가 휘는 로봇) 도 범위 밖 — 본 책은 모든 link 가 *rigid* 라고 가정.

</details>

---

### Q2. (개념) "로봇 (robot)" 과 단순한 "자동화 기계" 를 구분하는 정의적 특성은 무엇인가? 한 단어로 답하고, 한 문장으로 설명하시오.

<details><summary>정답</summary>

**Reprogrammability (재프로그래밍 가능성)**.

자동화 기계는 정해진 한 가지 task 만 반복하지만, 로봇은 다양한 task 에 맞게 다시 프로그램할 수 있다. 이 특성 때문에 *task 정보로부터 joint 명령을 자동 생성* 하는 컨트롤러가 필요하며, 이게 9장 (Trajectory Generation), 10장 (Motion Planning), 11장 (Control) 이 존재하는 이유.

</details>

---

### Q3. (개념) 로봇 메커니즘을 구성하는 **다섯 가지 요소**를 각각 한 줄 설명과 함께 나열하시오.

<details><summary>정답</summary>

1. **Link** — 강체 (rigid body). 메커니즘의 골격.
2. **Joint** — 인접 link 간 상대 운동을 허용 (revolute / prismatic 이 가장 흔함).
3. **Actuator** — 움직임의 원천 (전기모터 DC/AC/stepper, SMA, 또는 유압·공압 실린더).
4. **Transmission** — 모터의 저토크·고속을 로봇의 고토크·저속으로 변환 (gear, cable drive, belt, chain).
5. **Sensor** — 상태 측정 (encoder, F/T sensor, vision, RGB-D, laser range finder 등).

Brake 를 별도로 꼽기도 하지만 본 1장에서는 transmission 의 일부로 묶어 다룸.

</details>

---

### Q4. (개념) **Revolute** joint 와 **Prismatic** joint 의 차이를 운동의 종류로 답하시오. 각각 평면과 공간에서 인접 강체에 부과하는 *구속 개수* 는?

<details><summary>정답</summary>

| | Revolute (R) | Prismatic (P) |
|--|--|--|
| 운동 | 회전 1 DoF | 직선 병진 1 DoF |
| 평면 강체-강체 간 구속 | **2** | **2** |
| 공간 강체-강체 간 구속 | **5** | **5** |

공간에서 자유 강체는 6 DoF — joint 가 1 DoF 만 허용하면 나머지 **5 자유도**를 구속한다. 이 사실이 Grübler's formula 의 핵심 빌딩블록.

</details>

---

### Q5. (개념) **Open-chain** 과 **Closed-chain** 메커니즘을 다음 4 기준으로 비교하시오: 예시, joint actuation, forward kinematics 해, inverse kinematics 해.

<details><summary>정답</summary>

| 기준 | Open chain | Closed chain |
|--|--|--|
| 예시 | 산업용 6-DoF 매니퓰레이터 | Stewart-Gough platform, Delta robot |
| Joint actuation | **모든** joint 가 모터로 구동 | **일부만** actuated, 나머지는 passive |
| Forward kinematics | 항상 **유일해** (closed-form) | **다중해** 또는 어려움 |
| Inverse kinematics | 0개·유한 개·무한 개 가능 | 더 복잡, 특수해 분석 필요 |

요점: open chain 은 forward 가 쉽고 inverse 가 어려운 경우가 많고, **closed chain 은 그 반대인 경우가 흔함** (Stewart-Gough 가 대표).

</details>

---

### Q6. (적용) 평면 위의 자유 강체 한 개의 DoF, 그리고 공간 안 자유 강체 한 개의 DoF 를 각각 위치·자세로 분해해 적으시오.

<details><summary>정답</summary>

- **평면**: 위치 2 (x, y) + 자세 1 (각도 θ) = **3 DoF**
- **공간**: 위치 3 (x, y, z) + 자세 3 (rotation의 3 자유도, 예: roll-pitch-yaw) = **6 DoF**

이 사실이 본 책 전반의 *task space 차원* 의 기본값. EE 를 자유롭게 위치·자세시키려면 6-DoF arm 이 최소 요구.

</details>

---

### Q7. (적용) 두 개의 강체가 **revolute joint** 하나로 평면에서 연결되어 있다. 두 강체 시스템의 총 DoF 는?

<details><summary>정답</summary>

각 평면 강체는 3 DoF, 합쳐서 **6 DoF**.
Revolute joint 는 평면에서 **2 개의 구속**을 부과.
시스템 DoF = 6 − 2 = **4 DoF**.

(좀 더 직관적: 두 강체가 같은 joint 위치를 공유 → 위치 2 공유 → 한 강체 3 DoF + 다른 강체의 회전 1 DoF = 4.)

이게 평면 Grübler's formula 적용의 가장 단순한 사례.

</details>

---

### Q8. (적용) Modern Robotics 책에서는 회전 표현으로 **exponential coordinate** 를 핵심으로 삼는다. 회전 행렬 R 을 단위 회전축 ω̂ 과 각도 θ 로 어떻게 표현하는지 한 줄 식으로 적으시오. (구체 공식 X, 개념 식만.)

<details><summary>정답</summary>

```
R = exp([ω̂] θ)
```

또는 동일하게:
```
R = exp([ω])    where   ω = ω̂ · θ  in R³
```

여기서 `[·]` 는 3-벡터를 3×3 skew-symmetric 행렬로 만드는 연산자. exponential 은 행렬 exponential.

직관: 단위 회전축 ω̂ 주변으로 θ 만큼 회전.

이 선택이 4장 PoE, 8장 동역학의 6D twist exponential 까지 일관되게 확장됨.

</details>

---

### Q9. (디버그) 다음 진술의 무엇이 틀렸는가?
> "Forward kinematics 는 항상 유일해를 가지므로 inverse kinematics 만 어렵다."

<details><summary>정답</summary>

이 진술은 **open chain 에 한해서만** 옳음. **Closed chain 에서는 forward 도 다중해**를 갖는 경우가 흔함 (Stewart-Gough 가 대표 사례 — 6 다리 길이가 주어져도 platform 자세가 여러 개 가능).

올바른 진술:
- Open chain: forward 1 해 / inverse 0~∞
- Closed chain: forward 다중해 / inverse 도 다중해

</details>

---

### Q10. (디버그) "Backlash 와 slippage 는 같은 현상이다" 는 주장의 오류를 지적하고 둘의 차이를 명확히 하시오.

<details><summary>정답</summary>

둘은 **별개 현상**.

| | Backlash | Slippage |
|--|--|--|
| 정의 | 입력이 정지인데 출력측에 *남아있는 회전 여유* | 입력 회전의 *일부가 전달되지 않음* |
| 주된 원인 | gear 의 톱니 간격 | belt/cable/chain 의 미끄러짐 |
| 컨트롤러 영향 | 위치 hysteresis, 미세 떨림 | 전달 비율의 부정확성 |
| 정밀제어 대응 | dual-motor preload, harmonic drive | tensioner, sensor 직접 측정 |

좋은 transmission = 둘 다 0 에 가까울수록 좋음. 다만 약점이 다르므로 *어느 transmission 을 쓰는가* 에 따라 어느 보정이 필요한지 다름.

</details>

---

### Q11. (디버그) 다음 코드 흐름의 잘못된 가정을 찾으시오.
```
1. 6-DoF arm 의 inverse kinematics 를 구함 (Jacobian inverse).
2. 7-DoF arm 에 같은 알고리즘을 그대로 적용.
3. 결과가 numerically unstable.
```

<details><summary>정답</summary>

문제: 6-DoF 는 task dim 과 같으므로 Jacobian 이 정방 (6×6) 행렬 — 일반적으로 **inverse** 가능. 그러나 **7-DoF arm 은 redundant** (joint 수 > task dim) 이므로 Jacobian 이 직사각형 (6×7) → 일반 inverse 가 존재하지 않음.

올바른 접근:
- **Jacobian pseudoinverse** (Moore-Penrose) 사용: `θ̇ = J⁺ V`
- 추가로 null-space projection 으로 *secondary task* (예: joint limit 회피) 가능

이 사실은 6장 (Inverse Kinematics) 에서 redundancy 다룰 때 등장.

</details>

---

### Q12. (디버그) 어떤 학습자가 "joint torque τ 와 end-effector force F 는 관계 없는 별개 변수다" 라고 주장한다. 어떻게 반박하나?

<details><summary>정답</summary>

5장 (Velocity Kinematics & Statics) 의 핵심 결과:

```
τ = J(θ)ᵀ · F
```

- **J(θ)** 는 forward kinematics 의 Jacobian
- 같은 J 가 *속도 매핑* (V = J θ̇) 과 *힘 매핑* (전치형 τ = Jᵀ F) 을 동시에 함
- 유도: **가상일의 원리** — joint 가 가상 변위 δθ 만큼 움직였을 때 한 일이 EE 에서 한 일과 같아야 함

즉, joint torque 와 EE force 는 **Jacobian 전치 관계**로 직접 연결되어 있음. singularity 에 가까우면 J 가 rank 잃어서 작은 EE force 가 무한대 joint torque 를 요구하기도 함 (제어 측면 문제).

</details>

---

### Q13. (면접) "Holonomic 과 nonholonomic 의 차이를 자동차 평행주차로 설명하시오."

<details><summary>정답</summary>

자동차는 즉시 횡방향으로 못 움직임 — 바퀴는 옆으로 미끄러지지 못함. 이게 *velocity 식 구속* (`ẋ sin θ − ẏ cos θ = 0`). 그런데도 평행주차로 어디든 결국 갈 수 있음. 즉 **configuration 식 구속은 없음**.

**Holonomic**: 구속을 configuration 식으로 적을 수 있음 (`f(q) = 0`). closed chain 의 loop closure 가 대표.
**Nonholonomic**: 구속을 velocity 식으로만 적을 수 있음 (`g(q, q̇) = 0`, 적분 불가). 차량·공·자전거가 대표.

함의: nonholonomic 시스템은 motion planning·control 이 훨씬 복잡. "어느 configuration 에 도달 가능한가" 와 "어떤 *경로* 로 도달 가능한가" 가 분리됨. 13장에서 본격 다룸.

</details>

---

### Q14. (면접) Modern Robotics 책이 다른 로보틱스 교과서와 차별화되는 "기술적 선택" 하나를 꼽고, 그 이유를 한 줄로 답하시오.

<details><summary>정답</summary>

**Exponential coordinate 기반의 통합 표현**.

- 회전 (rotation) 은 `R = exp([ω])`
- 강체 운동 (rigid-body motion) 은 `T = exp([V])` (twist exponential)
- Forward kinematics 는 **PoE (Product of Exponentials)** 공식
- Dynamics 의 6D wrench·twist 도 같은 표현

이 일관성 덕분에 별도 link-frame 부착 규칙 (D-H 의 약점) 없이 base + EE frame 만으로 운동학을 풀 수 있고, 알고리즘 (PoE, Newton-Euler) 도 깔끔하게 재귀형으로 구현된다.

대조: 전통 교과서는 D-H 표기 + 회전행렬 직접 곱셈을 표준으로 삼아 식이 복잡해지는 경향.

</details>
