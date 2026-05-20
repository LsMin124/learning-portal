# JOIN & 서브쿼리 — 여러 테이블 함께 다루기

> **이 강의는 무엇인가**: `INNER/LEFT/RIGHT JOIN`, 셀프 조인, 상관 서브쿼리·`EXISTS`. 한 테이블만으론 답 못 내는 모든 쿼리의 무기.
> **왜 배우는가**: 정규화된 DB 에선 데이터가 여러 테이블에 흩어짐. JOIN 못 쓰면 자바에서 N+1 query 로 끌어와 메모리에서 합치게 됨.

---

## 들어가기 전에

- **선수**: SELECT 응용 (2강).
- **테이블**: `employees(id, name, dept_id, salary, manager_id)`, `depts(id, name, location)`, `orders(id, member_id, amount)`, `members(id, name)`.

---

## 핵심 개념

### 1. JOIN 의 정신

두 테이블의 행을 **연관 조건**으로 묶어 한 행으로.

```
INNER JOIN ON e.dept_id = d.id  →  양쪽 다 있는 것만
LEFT JOIN                       →  왼쪽 다 + 오른쪽은 있으면, 없으면 NULL
RIGHT JOIN                      →  오른쪽 다 + 왼쪽은 있으면
```

### 2. INNER JOIN

```sql
SELECT e.name, d.name AS dept_name
FROM employees e
INNER JOIN depts d ON e.dept_id = d.id;
```

`INNER` 생략 가능. `ON` 절이 조인 조건 — WHERE 와 분리해 의도 명확화.

### 3. OUTER JOIN

```sql
-- 부서 없는 직원도 (그쪽 컬럼 NULL)
SELECT e.name, d.name
FROM employees e
LEFT JOIN depts d ON e.dept_id = d.id;

-- 사람 없는 부서도
RIGHT JOIN depts d ...

-- FULL OUTER (MySQL 미지원, UNION 으로)
SELECT ... LEFT JOIN ... UNION SELECT ... RIGHT JOIN ... WHERE e.id IS NULL;
```

**왼/오 결정**: "이 쪽 행은 무조건 다 나와야"가 LEFT. 90%는 LEFT JOIN.

### 4. JOIN + WHERE — 함정

```sql
-- ❌ LEFT JOIN 후 우측 조건을 WHERE 에 → INNER 가 됨
SELECT e.name, d.name FROM employees e
LEFT JOIN depts d ON e.dept_id = d.id
WHERE d.location = 'Seoul';        -- 부서 NULL 인 직원의 d.location 도 NULL → 탈락

-- ✅ ON 절에 포함
LEFT JOIN depts d ON e.dept_id = d.id AND d.location = 'Seoul';
```

### 5. SELF JOIN

```sql
-- 직원과 매니저 이름
SELECT e.name AS emp, m.name AS mgr
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

별칭 필수. 조직도·카테고리 트리 같은 자기 참조 데이터.

### 6. 다중 JOIN

```sql
SELECT e.name, d.name AS dept, p.name AS project
FROM employees e
JOIN depts d         ON e.dept_id = d.id
JOIN dept_projects dp ON dp.dept_id = d.id
JOIN projects p       ON p.id = dp.project_id;
```

### 7. 상관 서브쿼리

서브쿼리가 **바깥 쿼리 컬럼을 참조** → 행마다 실행 → 느림.

```sql
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary) FROM employees x
    WHERE x.dept_id = e.dept_id          -- ← 바깥 e 참조
);
```

가능하면 JOIN+윈도우 함수로.

### 8. EXISTS / NOT EXISTS

```sql
SELECT m.* FROM members m
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id);

SELECT m.* FROM members m
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id);
```

**EXISTS vs IN**: EXISTS 는 존재 확인 즉시 중단(짧은 회로). 큰 데이터에서 빠름.

---

## 코드 깊게 들여다보기

"부서별 최고 연봉자 + 매니저 이름":

```sql
SELECT
    d.name      AS 부서,
    e.name      AS 최고연봉자,
    e.salary    AS 연봉,
    m.name      AS 매니저
FROM depts d
JOIN employees e ON e.dept_id = d.id
                AND e.salary = (
                    SELECT MAX(salary) FROM employees x
                    WHERE x.dept_id = d.id            -- ① 상관 서브
                )
LEFT JOIN employees m ON e.manager_id = m.id          -- ② 매니저 없을 수도
ORDER BY d.name;
```

**대안 (윈도우 함수)**:
```sql
SELECT * FROM (
    SELECT e.*, d.name AS dept_name,
           RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
    FROM employees e JOIN depts d ON e.dept_id = d.id
) t WHERE rnk = 1;
```

윈도우 함수가 같은 결과를 더 빠르게.

---

## 실전 패턴 / 자주 빠지는 함정

- ❌ `SELECT *` 로 JOIN → 같은 이름 컬럼 중복.
  ✅ 필요한 컬럼만, 별칭.
- ❌ `LEFT JOIN` 후 WHERE 에 우측 조건 → INNER 됨.
  ✅ ON 절에.
- ❌ ON 없는 JOIN → 카티시안 곱.
- ❌ 상관 서브 남발 → N+1.
  ✅ JOIN, 윈도우 함수.
- ❌ `COUNT(*)` + LEFT JOIN → 우측이 NULL 인 행도 카운트.
  ✅ `COUNT(o.id)`.
- ❌ `NULL = NULL` → false.
  ✅ NULL-safe `<=>` (MySQL), `IS NOT DISTINCT FROM` (PostgreSQL).

---

## 다음 강의로 가기 전 자가점검

1. INNER 와 LEFT JOIN 의 결과 행 수 관계?
2. `LEFT JOIN ... COUNT(*) ... GROUP BY` 가 주문 없는 회원에게 0 이 아니라 1 주는 이유?
3. EXISTS 가 IN 보다 빠른 이유?
4. 상관 서브쿼리 → JOIN 변환 일반 패턴?

<details><summary>풀이</summary>

1. LEFT ≥ INNER (우측 매칭 없는 좌측 행만큼 더).
2. `COUNT(*)` 는 행 자체를 셈. LEFT JOIN 으로 회원 행 자체는 1개 유지 → 1. `COUNT(o.id)` 로 바꿔야 0.
3. EXISTS 는 존재 즉시 중단(짧은 회로). IN 은 서브쿼리 전체 결과 모은 후 비교.
4. `WHERE col > (SELECT AVG(col) FROM t WHERE t.g = outer.g)` → `outer JOIN (SELECT g, AVG(col) avg FROM t GROUP BY g) x ON x.g = outer.g WHERE outer.col > x.avg`.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1~5 표지·왜 JOIN | §1 |
| p.6~15 INNER/OUTER | §2, §3, §4 |
| p.16~22 SELF/다중 | §5, §6 |
| p.23~30 서브쿼리/EXISTS | §7, §8 |
| p.31~43 실습/최적화 | 코드, 함정 |

_단독 학습 가능 노트._
