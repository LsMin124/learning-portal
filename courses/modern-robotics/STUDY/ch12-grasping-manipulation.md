# Chapter 12: Grasping and Manipulation — 학습 노트

> 이 노트는 *Modern Robotics: Mechanics, Planning, and Control* (Lynch & Park, 2017) **Chapter 12: Grasping and Manipulation** (책 p.461~512) 의 핵심을 학습 가능한 형태로 재구성한 것입니다.
> 12장의 핵심: *contact* 의 *기하·역학* — *어떻게 손이 물체를 잡고 움직이게 하는가*. **Form closure** (geometric immobilization) vs **Force closure** (friction-based grip), **friction cone**, **manipulation primitives** (pushing, sliding).

## 들어가기 전에

- **선수 지식**
  - **3장**: SE(3), twist `V`, wrench `F`
  - **5장**: `τ = Jᵀ F` (statics)
  - **11장**: hybrid motion-force control
  - 선형대수 + convex geometry
- **학습 목표**
  1. **Contact 의 종류** — point/line/plane, frictionless/frictional
  2. **Friction cone** — Coulomb friction 의 wrench 표현
  3. **Form closure** — geometric immobilization (4+ contact in plane, 7+ in 3D)
  4. **Force closure** — friction 기반 grip 의 stability
  5. **Grasp matrix** `G` — 손가락 접점 wrench → object wrench
  6. **Manipulation primitives** — pushing, sliding, throwing
- **예상 학습 시간**: 90~120분

---

## 1. Contact 의 기하

### 1.1 Contact 종류

| Type | 차원 | DoF 손실 |
|--|--|--|
| Point | 0D | 1 (수직만) |
| Line | 1D | 2 |
| Plane | 2D | 3 |

### 1.2 Frictionless vs Frictional

- **Frictionless**: contact normal 방향의 *밀어내는* (compressive) force 만
- **Frictional**: tangential force 도 가능 (단 `‖f_t‖ ≤ μ f_n`)

![Figure 12.1 — 다양한 contact 종류. 교재 p.462](/courses/modern-robotics/figures/ch12/fig-12-1.png)

---

## 2. Friction Cone

### 2.1 Coulomb friction model

contact normal 방향 `n̂`, friction coefficient `μ`. 가능한 contact force `f`:

$$f \cdot \hat{n} \geq 0 \quad \text{(compressive)}, \quad \|f - (f \cdot \hat{n})\hat{n}\| \leq \mu (f \cdot \hat{n})$$

기하적으로: `n̂` 을 축으로 하는 *반각 `tan⁻¹ μ`* 의 **원뿔** 안의 force.

![Figure 12.4 — Friction cone. 교재 p.488](/courses/modern-robotics/figures/ch12/fig-12-4.png)

### 2.2 Linearized friction cone (polyhedron)

원뿔 → *다면체 근사* (예: 4~8 면 pyramid). LP / QP 해법 가능.

### 2.3 Composite wrench

contact 의 force/torque 통합:

$$\mathcal{F}_{contact} = \begin{bmatrix} (r \times f) \\ f \end{bmatrix}$$

`r` = contact point 위치.

---

## 3. Form Closure (geometric immobilization)

### 3.1 정의

> **Form closure**: 물체가 *어떤 작은 motion 도 할 수 없도록* 기하학적으로 고정. friction 무관.

### 3.2 Reuleaux's principle

평면에서:
- 1 contact: 5 DoF 손실 안 됨 — motion 자유로움
- 2 contact: motion 가능
- 3 contact: 가능 (line of action)
- **4 contact**: 일반적으로 *first-order form closure* 가능 (필요 조건)

공간에서: **7 contact** 필요 (6 DoF 모두 immobilize).

### 3.3 검사 알고리즘

각 contact 의 *constraint wrench* 가 origin 을 *positively span* → form closure.

수학적: convex hull (또는 positive span) 이 `R^d` 의 전체 → first-order form closure.

![Figure 12.6 — Form closure 의 contact wrench. 교재 p.491](/courses/modern-robotics/figures/ch12/fig-12-6.png)

---

## 4. Force Closure (friction-based grip)

### 4.1 정의

> **Force closure**: friction 을 활용해서 모든 external wrench `F_ext` 에 대해 finger 가 *반작용 wrench* 를 만들 수 있음.

Form closure 보다 약함 (friction 의존). 그러나 *적은 contact* 로 가능 → 실용적.

### 4.2 평면 force closure

평면에서 **2 점 contact + frictional** 로 force closure 가능 (조건: 두 contact 의 friction cone 이 *겹침*).

### 4.3 3D force closure

3D 에서 **3+ frictional contact** 필요 (보통).

### 4.4 검사 알고리즘

각 contact 의 friction cone 의 edge wrench 들의 *positive span* 이 `R⁶` 전체 → force closure.

---

## 5. Grasp Matrix `G`

### 5.1 정의

손가락이 `k` 개 contact, 각 contact 의 wrench `F_i`. 물체에 작용하는 *총 wrench* `F_object`:

$$\mathcal{F}_{object} = G \mathcal{F}_{contacts}, \quad G \in \mathbb{R}^{6 \times 3k}$$

(각 contact 가 3D force, k 개)

### 5.2 분석

- **rank G = 6** + friction cone 안에 적절 force → force closure
- **rank G < 6**: 어떤 wrench 방향 못 만듦 — *not even basic grasp*

### 5.3 Grasping force optimization

복수의 finger force 분포가 *force closure* 만족하면서 *contact force* 최소화 → QP 문제.

$$\min \sum_i \|f_i\|^2 \quad \text{s.t. } G f = \mathcal{F}_{required}, \quad f_i \in \text{friction cone}_i$$

---

## 6. Manipulation Primitives

### 6.1 Grasping

가장 흔한 — *hold* and *move*. 위의 force closure 분석.

### 6.2 Pushing

손가락 *하나* 로 물체를 *밀기*. force closure 없어도 가능.

수학: contact friction 의 *지지 다각형* 안에서 물체가 어떻게 회전·병진할지 예측.

### 6.3 Pivoting

물체를 *한 점 중심* 으로 회전.

### 6.4 Throwing

dynamic manipulation — robot 이 물체를 *던지고 받기*. 매우 빠른 motion + perfect timing.

![Figure 12.15 — Manipulation primitives 예시. 교재 p.499](/courses/modern-robotics/figures/ch12/fig-12-15.png)

### 6.5 Sliding

물체를 표면 위에서 *부드럽게 끌기*. friction model 이 핵심.

---

## 7. Assembly with Compliance

### 7.1 Peg-in-hole 의 문제

peg 와 hole 의 미세한 정렬 오차 → contact-rich insertion. *jamming* 위험.

### 7.2 Compliant motion

robot 이 *contact force 에 부드럽게 양보* → 정렬 보정.

방법:
- **Passive compliance**: RCC (Remote Center of Compliance) 기계적 부품
- **Active compliance**: 11장 impedance control

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | Form closure = force closure | form 이 *더 강함* (friction 무관). 7 contact 필요. force 는 friction 으로 가능 (3 contact). |
| 2 | 평면 form closure 에 3 contact 충분 | 4 contact 필요 (3 contact 으로 free DoF 존재). |
| 3 | Frictionless model 이 *실용적* | 실제 robotic gripper 는 거의 모두 frictional. friction cone 모델링 필수. |
| 4 | Friction coefficient `μ` 가 *constant* | 표면 상태·온도·속도에 따라 변동. nominal μ 의 50~150%. |
| 5 | Grasp matrix `G` 가 *직사각형* 이면 항상 OK | rank ≥ 6 필요. underdetermined 면 force closure 안 됨. |
| 6 | Pushing 의 contact 가 *static* | 마찰 표면에 따라 *slip / stick* 동적 변화. |
| 7 | Force closure 가 *충분조건* | *robust grasp* 까진 추가 조건 (예: stability margin). |
| 8 | Friction cone 의 *원형* 이 *exact* model | 실제는 *이방성* (방향 따라 다른 μ). 원형은 isotropic 근사. |
| 9 | Grasping force 가 *클수록 안전* | 너무 크면 물체 손상. min force 최적화 필수. |
| 10 | Manipulation = pick-and-place 만 | pushing, throwing, pivoting 모두 manipulation. dexterous manipulation 의 연구 핫토픽. |

---

## 자가점검

1. Form closure 의 정의.
2. Force closure 의 정의 + Form 과의 차이.
3. Friction cone 의 수학 정의 (Coulomb).
4. 평면에서 form closure 의 *contact 수* 필요조건.
5. 3D 에서 form closure 의 *contact 수* 필요조건.
6. 평면 force closure 의 최소 contact 수.
7. Grasp matrix `G` 의 정의와 rank 조건.
8. Grasping force optimization 의 LP / QP 형태.
9. Pushing 과 grasping 의 *제어 측면* 차이.
10. Peg-in-hole 의 compliance 두 가지 (passive / active).

### 해답 (간략)

1. 물체가 기하학적으로 *완전히 immobilized* (friction 무관).
2. Friction 활용한 *모든 external wrench 반작용 가능*. Form 보다 약함 (friction 의존).
3. `f · n̂ ≥ 0` AND `‖f − (f·n̂)n̂‖ ≤ μ (f·n̂)`. → 반각 `tan⁻¹ μ` 의 cone.
4. 평면: **4** contact (frictionless, first-order).
5. 3D: **7** contact (frictionless).
6. 평면 force closure: **2** frictional contact (friction cone 겹침).
7. `F_object = G F_contacts`, `G ∈ R^{6×3k}`. rank G = 6 + friction cone 조건 → force closure.
8. `min Σ ‖f_i‖² s.t. G f = F_req, f_i ∈ friction cone_i`. QP.
9. Grasping = force closure (모든 방향 controllable). Pushing = 부분 contact, *non-prehensile*.
10. Passive: RCC 기계 부품. Active: 11장 impedance control.

---

## 다음 학습으로

- **13장 (Mobile Robots)** — nonholonomic + contact.
- **Robotic Hands** — Allegro, Shadow Hand.
- **Learning-based grasping** — GraspNet, DexNet.
- **Dexterous manipulation** — Shadow Hand Cube rotation.

---

## §X 산업의 Manipulation (2025)

### Robotic grippers

| | 회사 | 특징 |
|--|--|--|
| Parallel jaw | 표준 산업 | 단순, 강력 |
| Suction cup | Schmalz, Piab | 평평한 표면, e-commerce |
| Soft gripper | Soft Robotics | 부드러운 물체 (food) |
| Allegro Hand | Wonik | 4-finger, 16-DoF |
| Shadow Hand | Shadow Robot | 5-finger, 24-DoF |

### Learning-based grasping

**GraspNet** (2020): RGB-D → grasp pose, ~95% success.
**Dex-Net** (Berkeley, 2017~): synthetic + sim2real.
**ACRONYM** (NVIDIA): million-scale grasp dataset.

### Recent advances

**Foundation models**:
- RT-1, RT-2 (Google) — vision-language-action
- Octo — open foundation policy
- RDT-1B — diffusion-based

**Dexterous manipulation**:
- OpenAI Dactyl (2018) — Rubik's cube
- DeepMind RGB-Stacking (2022)
- TRI cooking robot (2024)

### Non-prehensile

- Pushing, throwing (TossingBot), pivoting

### Industry applications

- Amazon Picking Challenge — warehouse
- Tesla FSD — autonomous
- Da Vinci — surgical
- Fruit picking — Soft Robotics + AI
