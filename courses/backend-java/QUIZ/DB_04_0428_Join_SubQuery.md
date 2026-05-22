# JOIN / SubQuery - 퀴즈

> 14문항. 개념·적용·디버그·면접. EMP / DEPT / SALGRADE 스키마 기준.

---

### Q1. (개념) JOIN 5종류 (INNER / LEFT / RIGHT / FULL / CROSS) 의 결과 차이를 표로.

<details><summary>정답</summary>

| 종류 | 결과 | MySQL 지원 |
|--|--|--|
| **INNER JOIN** | 양쪽 매칭 행만 (교집합) | O |
| **LEFT (OUTER) JOIN** | 왼쪽 전체 + 매칭되는 오른쪽 (없으면 NULL) | O |
| **RIGHT (OUTER) JOIN** | 오른쪽 전체 + 매칭되는 왼쪽 (없으면 NULL) | O |
| **FULL OUTER JOIN** | 양쪽 모든 행 (매칭 없으면 NULL) | **X** (LEFT UNION RIGHT 로) |
| **CROSS JOIN** | 카티시안 곱 (m x n 행) | O |

**행 수 관계**: `INNER <= LEFT/RIGHT <= FULL <= CROSS`.

**선택 가이드**:
- "양쪽 다 있어야" → INNER
- "이쪽은 무조건 다, 저쪽은 있으면" → LEFT (실무 90%)
- "양쪽 다 살리고 싶음" → FULL (MySQL 은 UNION)

</details>

### Q2. (개념) Cartesian Product (카티시안 곱) 가 발생하는 조건과 위험성?

<details><summary>정답</summary>

**조건**: 두 테이블을 JOIN 하면서 **ON / WHERE 조건이 없으면** 모든 조합이 만들어짐.

수식: `A x B = {(a, 1), (a, 2), (b, 1), (b, 2), ...}` → `|A| x |B|` 행.

```sql
-- 위험 (의도치 않은 카티시안 곱)
SELECT e.ename, d.dname
FROM   emp e, dept d;          -- WHERE 누락 → 14 x 4 = 56 행

-- 정상 (조건 있음)
SELECT e.ename, d.dname
FROM   emp e, dept d
WHERE  e.deptno = d.deptno;    -- 14 행

-- 명시적 (현대 SQL 권장)
SELECT e.ename, d.dname
FROM   emp e INNER JOIN dept d ON e.deptno = d.deptno;
```

**위험**:
- 1만 x 1만 = 1억 행 → 메모리·디스크 폭주
- 결과는 의미 없는 모든 조합 → 비즈니스적으로 잘못된 답
- 조인 조건을 깜빡한 신입의 가장 흔한 실수

→ 의도된 CROSS JOIN 이 아니면 ON / WHERE 절 필수 확인.

</details>

### Q3. (개념) `ON` 절과 `WHERE` 절의 역할 차이는?

<details><summary>정답</summary>

| 절 | 시점 | 역할 |
|--|--|--|
| **ON** | JOIN 단계 - 두 테이블을 결합하는 **조건** | 어떤 행과 어떤 행을 매칭할지 |
| **WHERE** | JOIN 후 - 결합된 결과에 대한 **필터** | 만들어진 행을 거를지 |

**INNER JOIN 에선 둘이 거의 같지만, OUTER JOIN 에선 결정적으로 다름**.

```sql
-- (1) ON 에 조건 - LEFT JOIN 의 의도 유지
SELECT e.ename, d.dname
FROM   emp e
LEFT JOIN dept d ON e.deptno = d.deptno AND d.loc = 'DALLAS';
-- 결과: 모든 사원 + DALLAS 부서면 dname, 아니면 NULL

-- (2) WHERE 에 조건 - LEFT JOIN 이 INNER 됨
SELECT e.ename, d.dname
FROM   emp e
LEFT JOIN dept d ON e.deptno = d.deptno
WHERE  d.loc = 'DALLAS';
-- 결과: dname=DALLAS 인 사원만 (다른 사원은 d.loc 가 NULL → 제외)
```

**규칙**: OUTER JOIN 의 우측 컬럼 필터는 **ON 에**, 좌측은 **WHERE 에**.

</details>

### Q4. (적용) 모든 사원의 이름·부서명·근무지 조회 (INNER JOIN).

<details><summary>정답</summary>

```sql
SELECT e.ename, d.dname, d.loc
FROM   emp e
INNER JOIN dept d ON e.deptno = d.deptno;
```

**구식 (콤마) 문법**:
```sql
SELECT e.ename, d.dname, d.loc
FROM   emp e, dept d
WHERE  e.deptno = d.deptno;
```

→ 같은 결과지만 현대 SQL 은 INNER JOIN ... ON 권장 (조인 조건과 필터 분리 → 가독성·실수 방지).

`INNER` 키워드는 생략 가능 (`JOIN` 만 써도 INNER).

</details>

### Q5. (적용) 모든 사원과 매니저의 이름을 함께 조회 (매니저 없는 KING 도 포함).

<details><summary>정답</summary>

**SELF JOIN + LEFT JOIN**:
```sql
SELECT e.ename AS 사원,
       m.ename AS 매니저
FROM   emp e
LEFT JOIN emp m ON e.mgr = m.empno
ORDER BY e.ename;
```

- 같은 테이블을 두 번 참조 → **별칭 (alias) 필수**
- `e` = 사원, `m` = 매니저 (자기 자신의 부하)
- KING 은 `mgr` 컬럼이 NULL → INNER 면 제외, LEFT 면 매니저=NULL 로 포함

**용례**: 조직도, 카테고리 트리, 친구 관계 등 **자기 참조 데이터**.

</details>

### Q6. (적용) Non-Equi JOIN 으로 각 사원의 급여 등급 조회 (SALGRADE 테이블 활용).

<details><summary>정답</summary>

```sql
-- SALGRADE: GRADE, LOSAL, HISAL
SELECT e.ename, e.sal, s.grade
FROM   emp e
JOIN   salgrade s ON e.sal BETWEEN s.losal AND s.hisal;
```

**Non-Equi JOIN**: `=` 가 아닌 **범위·부등호** 로 매칭.
- Equi JOIN: `ON a.id = b.id` (가장 흔함)
- Non-Equi JOIN: `ON a.col BETWEEN b.lo AND b.hi`, `ON a.x < b.y`

용례: 등급표, 요금 구간, 점수→학점 변환, 가격 할인율 매핑.

</details>

### Q7. (개념) 서브쿼리 종류 (단일행·다중행·다중컬럼·스칼라·상관·인라인뷰) 정리.

<details><summary>정답</summary>

| 종류 | 위치 | 반환 | 예시 |
|--|--|--|--|
| **단일행 서브쿼리** | WHERE | 1행 1컬럼 | `WHERE deptno = (SELECT deptno FROM emp WHERE empno=7788)` |
| **다중행 서브쿼리** | WHERE | n행 1컬럼 | `WHERE deptno IN (SELECT deptno FROM dept WHERE loc='NY')` |
| **다중컬럼 서브쿼리** | WHERE | n행 n컬럼 | `WHERE (deptno, job) IN (SELECT deptno, job FROM ...)` |
| **스칼라 서브쿼리** | SELECT | 1행 1컬럼 | `SELECT ename, (SELECT dname FROM dept d WHERE d.deptno=e.deptno) FROM emp e` |
| **상관 서브쿼리** | WHERE / SELECT | 바깥 컬럼 참조 | `WHERE sal > (SELECT AVG(sal) FROM emp x WHERE x.deptno=e.deptno)` |
| **인라인 뷰** | FROM | 테이블처럼 | `FROM (SELECT deptno, AVG(sal) avg FROM emp GROUP BY deptno) t` |

**연산자**:
- 단일행: `=`, `<`, `>`, `<>`
- 다중행: `IN`, `ANY`, `ALL`, `EXISTS`

</details>

### Q8. (적용) 사번이 7788 인 사원의 부서 이름 조회 (단일행 서브쿼리).

<details><summary>정답</summary>

**방법 1: 서브쿼리**
```sql
SELECT dname
FROM   dept
WHERE  deptno = (SELECT deptno FROM emp WHERE empno = 7788);
```

**방법 2: JOIN**
```sql
SELECT d.dname
FROM   emp e JOIN dept d ON e.deptno = d.deptno
WHERE  e.empno = 7788;
```

⚠️ **단일행 서브쿼리 함정**: 서브쿼리가 2행 이상 반환하면 `Subquery returns more than 1 row` 에러.
→ 결과가 1행임을 보장 못 하면 `IN` (다중행 연산자) 사용.

</details>

### Q9. (적용) 'RESEARCH' 또는 'SALES' 부서에 속한 사원 전체 조회 (다중행 서브쿼리 - IN / ANY / ALL).

<details><summary>정답</summary>

```sql
SELECT empno, ename, deptno
FROM   emp
WHERE  deptno IN (SELECT deptno FROM dept WHERE dname IN ('RESEARCH', 'SALES'));
```

**다중행 연산자**:
- `IN (list)` - 리스트 중 하나와 일치
- `ANY` - 하나라도 만족 (`> ANY (...)` = 최솟값보다 큼)
- `ALL` - 모두 만족 (`> ALL (...)` = 최댓값보다 큼)

```sql
-- ANY: SALES 부서 최소 급여보다 큰 사원
WHERE sal > ANY (SELECT sal FROM emp WHERE deptno = 30);

-- ALL: SALES 부서 최대 급여보다 큰 사원
WHERE sal > ALL (SELECT sal FROM emp WHERE deptno = 30);
```

</details>

### Q10. (적용) 주문 이력이 있는 회원만 조회 (EXISTS) + EXISTS vs IN 차이.

<details><summary>정답</summary>

```sql
-- members(id, name), orders(id, member_id, amount)

SELECT m.*
FROM   members m
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id);

-- 주문 없는 회원
SELECT m.*
FROM   members m
WHERE  NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id);
```

**EXISTS vs IN 차이**:

| | EXISTS | IN |
|--|--|--|
| 동작 | 행마다 서브쿼리 실행, 존재하면 즉시 TRUE (짧은 회로) | 서브쿼리 전체 결과 모은 후 비교 |
| NULL | 영향 없음 | `NOT IN (..., NULL)` 함정 (전체 0행) |
| 속도 | 큰 데이터 + 인덱스에 유리 | 작은 결과 집합엔 충분 |

`SELECT 1` 은 관습 - EXISTS 는 컬럼값을 안 쓰니 무엇이든 OK.

</details>

### Q11. (적용) 각 부서의 평균 급여보다 많이 받는 사원 (상관 서브쿼리 → JOIN → 윈도우 함수 3 방식).

<details><summary>정답</summary>

**상관 서브쿼리 (가장 직관적, 느림)**:
```sql
SELECT e.empno, e.ename, e.deptno, e.sal
FROM   emp e
WHERE  e.sal > (
    SELECT AVG(x.sal)
    FROM   emp x
    WHERE  x.deptno = e.deptno      -- 바깥 e.deptno 참조 = 상관
);
```

**JOIN + 인라인뷰 (빠름)**:
```sql
SELECT e.empno, e.ename, e.deptno, e.sal
FROM   emp e
JOIN  (SELECT deptno, AVG(sal) AS avg_sal FROM emp GROUP BY deptno) d
       ON e.deptno = d.deptno
WHERE  e.sal > d.avg_sal;
```

**윈도우 함수 (MySQL 8.0+, 가장 빠름)**:
```sql
SELECT * FROM (
    SELECT e.*, AVG(sal) OVER (PARTITION BY deptno) AS avg_sal FROM emp e
) t
WHERE sal > avg_sal;
```

→ 결과는 같지만 옵티마이저가 처리하는 방식이 다름. `EXPLAIN` 으로 실행 계획 비교.

</details>

### Q12. (디버그) 다음 두 쿼리의 결과가 다른 이유?

```sql
A: SELECT e.ename, d.dname FROM emp e
   LEFT JOIN dept d ON e.deptno = d.deptno AND d.loc = 'DALLAS';

B: SELECT e.ename, d.dname FROM emp e
   LEFT JOIN dept d ON e.deptno = d.deptno
   WHERE d.loc = 'DALLAS';
```

<details><summary>정답</summary>

**A (ON 에 조건)**:
- 모든 사원 행 유지
- DALLAS 부서면 dname 채움
- 아니면 dname = NULL

**B (WHERE 에 조건)**:
- LEFT JOIN 후 WHERE 가 d.loc 가 NULL 인 행을 제외
- → LEFT JOIN 이 **INNER JOIN 처럼 동작**
- DALLAS 부서 사원만

**규칙**:
- OUTER JOIN 의 **우측 (NULL 채워질 쪽) 조건은 ON 에**
- 좌측 (유지할 쪽) 조건은 WHERE 또는 ON 둘 다 가능

→ "LEFT JOIN 했는데 결과가 INNER 같다" 면 90% WHERE 의 우측 컬럼 조건 때문.

</details>

### Q13. (디버그) `SELECT m.name, COUNT(*) FROM members m LEFT JOIN orders o ON o.member_id = m.id GROUP BY m.id` 가 주문 없는 회원에게 0 이 아니라 1 을 주는 이유?

<details><summary>정답</summary>

`COUNT(*)` 는 **행 자체** 를 셈. LEFT JOIN 이라 매칭 안 되는 회원도 1행 유지 (orders 컬럼이 NULL) → 카운트 1.

**해결**: 특정 컬럼 (NULL 무시) 으로 카운트.
```sql
SELECT m.name, COUNT(o.id) AS order_count
FROM   members m
LEFT JOIN orders o ON o.member_id = m.id
GROUP BY m.id;
```

| 함수 | 동작 |
|--|--|
| `COUNT(*)` | 모든 행 (NULL 포함) |
| `COUNT(col)` | col 이 NULL 이 아닌 행만 |
| `COUNT(DISTINCT col)` | 중복 제거 |

→ "LEFT JOIN + COUNT" 면 항상 `COUNT(o.컬럼)` 으로.

</details>

### Q14. (면접) "JOIN 과 Subquery 중 무엇을 선택하나? N+1 query 와 어떤 관련?"

<details><summary>정답</summary>

**원칙**: 같은 결과면 **JOIN 우선** (옵티마이저가 잘 처리).

| 상황 | 선택 |
|--|--|
| 여러 테이블의 컬럼을 동시에 SELECT | **JOIN** |
| `EXISTS / IN` 으로 존재 확인만 | **Subquery (EXISTS)** |
| 행마다 다른 집계 결과가 필요 (그룹별 평균과 비교) | **상관 서브쿼리 OR 윈도우 함수** |
| 결과를 임시 테이블처럼 쓰고 싶음 | **인라인 뷰 (FROM 서브쿼리)** |

**N+1 query 문제** (자바·Spring 에서 가장 흔한 성능 함정):

```java
// 안 좋은 예 - 회원 N 명에 대해 N 번의 추가 쿼리
List<Member> members = memberDao.findAll();          // 1번 쿼리
for (Member m : members) {
    m.orders = orderDao.findByMemberId(m.id);        // N 번 쿼리
}
// 총 1 + N 쿼리. 회원 1000 명이면 1001 번.
```

**해결**: JOIN 으로 한 번에 가져오기 (Spring JPA `JOIN FETCH`).
```sql
SELECT m.*, o.*
FROM   members m
LEFT JOIN orders o ON o.member_id = m.id;        -- 1 번 쿼리
```

→ DB JOIN 을 못 쓰면 자바 메모리에서 N+1 발생. **JOIN 은 단순한 SQL 문법이 아니라 성능 문제**.

**언제 서브쿼리가 더 명확?**: "존재 확인" 만 필요할 때 EXISTS, "그룹별 집계를 다시 비교" 할 때 인라인 뷰. 즉 SELECT 컬럼에 양쪽이 다 필요한 게 아니면 서브쿼리.

</details>
