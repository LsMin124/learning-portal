# Chapter 6: Inverse Kinematics — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 6: Inverse Kinematics** (책 p.219~242) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 6장의 핵심은 **IK = `T → θ`** — FK 의 역. *비선형*, *다해*, *무해* 가능. 두 접근: **analytic** (closed-form, 특수 robot) vs **numerical** (Newton-Raphson, 일반).

## 들어가기 전에

- **선수 지식**
  - **3장**: SE(3), matrix log, `[Ad_T]`
  - **4장**: PoE FK, `M`, `B_i`
  - **5장**: Body Jacobian `J_b`
  - 수치해석: Newton-Raphson 방법
- **학습 목표**
  1. **IK 의 정의** — `T → θ` 의 *비선형 역문제*
  2. IK 의 *비유일성·비존재성* — multiple solutions, no solution
  3. **Analytic IK** — 6R PUMA arm 의 closed-form solution
  4. **Numerical IK** (Newton-Raphson with body Jacobian) — 가장 자주 쓰임
  5. *Damped least-squares* 로 singular 회피
  6. *Redundancy resolution* — 7-DoF arm 의 null-space 활용
- **예상 학습 시간**: 90~120분

---

## 1. IK 문제의 정의

### 1.1 문제

> Given 목표 EE pose `T_d ∈ SE(3)`, find joint values `θ ∈ R^n` such that `T(θ) = T_d`.

### 1.2 FK 와의 비교

| 측면 | FK | IK |
|--|--|--|
| 방향 | `θ → T` | `T → θ` |
| 선형성 | 비선형 (closed-form) | 비선형 (분석/수치) |
| 해의 수 | 1 (유일) | 0, 1, ∞ (다양) |
| 계산 | 한 번에 (PoE) | 반복 또는 case-by-case |

### 1.3 IK 의 *어려움*

- **Existence (존재)**: `T_d` 가 workspace 밖이면 *해 없음*
- **Uniqueness (유일성)**: 일반적으로 *다해* (elbow up/down, wrist flip)
- **Singularity 근처**: 수치 해법 발산
- **Joint limits**: 모든 해가 limit 안에 있어야

![Figure 6.1 — 평면 2R arm 의 IK: 두 해 (elbow up/down). 교재 p.220](/courses/modern-robotics/figures/ch06/fig-6-1.png)

---

## 2. Analytic IK — 6R PUMA arm

### 2.1 *Pieper's criterion*

> 6R arm 의 마지막 3 회전축이 *한 점에서 만나면* (= spherical wrist) → **analytic IK 가능**.

이유:
1. **Position decoupling**: wrist center 의 위치 `p_w` 는 처음 3 joint 만의 함수
2. **Orientation decoupling**: 끝 자세는 마지막 3 joint 가 결정
3. 두 sub-problem 으로 분리 → 각각 closed-form

PUMA, KUKA KR, ABB 대부분 산업용 6R arm 이 이 구조.

### 2.2 6R PUMA IK 단계

![Figure 6.4 — PUMA arm 의 IK geometric decomposition. 교재 p.223](/courses/modern-robotics/figures/ch06/fig-6-4.png)

1. **Wrist center 계산**: `p_w = p_d − d_6 · ẑ_b` (마지막 link 의 z 축 따라 d_6 만큼 후퇴)
2. **First 3 joints** (position): `p_w` 의 위치에서 `θ_1, θ_2, θ_3` 분석
   - `θ_1 = atan2(p_{wy}, p_{wx})` (또는 + π 의 두 케이스)
   - `θ_2, θ_3`: law of cosines (elbow up/down 두 케이스)
3. **Last 3 joints** (orientation): `R_{36}` (마지막 3 joint 의 누적 회전) = `R_{03}⁻¹ R_d` 에서 Euler-angle 추출
   - `θ_4, θ_5, θ_6` (3 회전축의 종류에 따라 ZYZ 또는 ZYX 등 Euler convention)

### 2.3 *최대 8 개* 의 IK 해

각 단계에서 binary choice:
- `θ_1`: front / back (2)
- elbow: up / down (2)
- wrist: flip / no flip (2)

→ 총 **2 × 2 × 2 = 8 해**. 모든 해가 joint limit 안에 들 가능성 X.

> **함정 1**: 8 해 중 *현재 joint configuration 에 가까운* 해를 선택해야 robot 의 *jerky* 움직임 방지.

---

## 3. Numerical IK — Newton-Raphson

### 3.1 Body twist 기반 update

목표: `T(θ) = T_d`. error 를 body twist 로:

$$[\mathcal{V}_b] = \log(T(\theta)^{-1} T_d)$$

`V_b` 는 current → desired 의 *body frame 에서 본* twist.

Newton-Raphson update:

$$\theta_{k+1} = \theta_k + J_b^{-1}(\theta_k) \mathcal{V}_b$$

`n > 6` (redundant) 이면 pseudoinverse `J_b⁺`.

### 3.2 알고리즘

```
Algorithm: Numerical IK (body frame)
Input: T_d (desired EE pose), θ_0 (initial guess), ε (tolerance)
Output: θ such that T(θ) ≈ T_d

θ ← θ_0
while True:
    T ← FK(θ)                        # current EE pose
    V_b ← log(T⁻¹ T_d)                # body twist (error)
    if ‖ω_b‖ < ε_ω and ‖v_b‖ < ε_v:
        return θ                      # converged
    Δθ ← pinv(J_b(θ)) · V_b
    θ ← θ + Δθ
```

### 3.3 수렴

- 초기값이 *충분히 가까우면* 빠른 수렴 (quadratic)
- *멀거나* singular 근처: 발산 가능
- **Damped LS**: `Δθ = J_bᵀ (J_b J_bᵀ + λ² I)⁻¹ V_b` — robust

![Figure 6.7 — Numerical IK 의 iteration 수렴 시각화. 교재 p.228](/courses/modern-robotics/figures/ch06/fig-6-7.png)

### 3.4 Multiple initialization

해가 여러 개면 *초기값* 에 따라 다른 해로 수렴. 실용 전략:
- 여러 `θ_0` 시도 (random restart 또는 grid)
- 가장 좋은 해 (가장 가까운 / joint limit 안에 드는) 선택

---

## 4. Redundancy Resolution

### 4.1 7-DoF arm 의 자유도

`n = 7, dim(task) = 6` → 1 차원 *redundancy*. 같은 EE pose 에 *무한히 많은* joint configuration 대응.

### 4.2 Null-space task

Primary task (EE pose) 외 *추가 목적*:
- joint limit 회피
- 장애물 회피
- 작업 manipulability 최대화

수식:

$$\dot\theta = J^+ \mathcal{V}_d + (I - J^+ J) \dot\theta_0$$

- 첫 항: primary task 만족
- 둘째 항: null space 안의 자유로운 motion (`J (I - J⁺ J) = 0`)

### 4.3 응용

- humanoid manipulation — 두 팔이 *동시에* 작업하며 *서로 충돌 회피*
- surgical robot — EE 의 자세 유지하며 *팔꿈치가 환자 안건드림*
- redundancy resolution 의 모든 응용이 7-DoF arm 의 *실제* 가치

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | IK 해가 항상 *유일* | 일반적으로 다해 (6R: 8개). 초기값·heuristic 으로 선택. |
| 2 | Analytic IK 가 *모든 6R arm* 에 가능 | Pieper criterion (spherical wrist) 필요. arbitrary 6R 은 polynomial 해 |
| 3 | Newton-Raphson 의 `Δθ = J⁻¹ V` 의 `J` 가 *spatial Jacobian* | body Jacobian 권장. error 가 body frame 에서 자연스러움. |
| 4 | 수치 IK 가 *반드시* 수렴 | 초기값 멀면 발산. singular 근처 발산. multiple restart 필요. |
| 5 | Singularity = "어떤 pose 도 도달 불가" | 해당 *방향* 만 불가능. 다른 방향은 OK. |
| 6 | Redundant arm 은 IK 가 *더 쉬워짐* | 해의 수가 *무한대* — null-space 결정의 *추가 cost function* 필요. |
| 7 | `log(T⁻¹ T_d)` 가 *항상 well-defined* | `R` 의 `θ = π` 케이스 unique 아님. 코드에서 별도 처리. |
| 8 | Damped LS 가 *항상 정확한 답* | 정규화로 *bias* 발생. λ 크면 수렴 느림 / 부정확. trade-off. |
| 9 | Joint limits 가 IK 알고리즘에 *자동 반영* | 안 됨. 별도 *clipping* 또는 *constrained optimization*. |
| 10 | 분석 IK 가 항상 *수치 IK 보다 빠름* | 일반적이긴 하나 case-by-case 코딩 부담 ↑. 수치는 general-purpose. |

---

## 자가점검

1. IK 의 정의를 한 문장으로.
2. FK 대비 IK 의 *세 가지 추가 어려움*.
3. Pieper criterion — 무엇이 만족되어야 analytic IK 가능?
4. 일반 6R PUMA 의 *최대* IK 해의 수.
5. Newton-Raphson update 식.
6. Body twist `V_b = log(T⁻¹ T_d)` 의 의미.
7. Damped least-squares 의 update 식.
8. 7-DoF arm 의 null-space update 식.
9. IK 가 *발산* 하는 두 가지 흔한 원인.
10. *그냥* 수치 IK 가 *충분* 한데 왜 analytic IK 를 따로 다루나?
11. 초기값 `θ_0` 의 *영향*.
12. Joint limits 를 어떻게 IK 에 반영?

### 해답 (간략)

1. 주어진 EE pose `T_d` 에 대해 `T(θ) = T_d` 인 joint values `θ` 를 찾는 문제.
2. 비유일성, 비존재성, 수렴성 (수치 IK).
3. 마지막 3 회전축이 한 점에서 만남 (spherical wrist).
4. 8 (2×2×2: front/back × elbow up/down × wrist flip).
5. `θ_{k+1} = θ_k + J_b⁻¹(θ_k) V_b`, `V_b = log(T(θ_k)⁻¹ T_d)`.
6. current pose → desired pose 의 body-frame twist (error).
7. `Δθ = J_bᵀ (J_b J_bᵀ + λ² I)⁻¹ V_b`.
8. `θ̇ = J⁺ V_d + (I − J⁺ J) θ̇_0`.
9. (a) singular configuration 근처, (b) 초기값 너무 멀어 local minimum 빠짐.
10. 속도. closed-form 은 *상수 시간*, 수치는 *수렴 시간 가변*. real-time 제어 (1kHz) 엔 analytic 필요.
11. local minimum 에 빠지는지 / 어느 해로 수렴할지 결정. 다해 robot 에서 critical.
12. clipping (`θ = clamp(θ, θ_min, θ_max)`) 또는 constrained optimization (예: barrier method).

---

## 다음 학습으로

- **8장 (Dynamics)** — `M(θ) θ̈ + C(θ, θ̇) θ̇ + g(θ) = τ`. IK 의 *동적* 확장.
- **9장 (Trajectory Generation)** — IK 의 *시간 sequence*. via points + smooth trajectory.
- **11장 (Control)** — feedback control 의 *inner loop* 에 IK 가 들어감.
- **MoveIt / pinocchio**: 실제 software 에서 분석 IK + 수치 IK 의 *하이브리드* 가 표준.
