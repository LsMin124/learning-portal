# JOIN · SubQuery — 치트시트

> 43p 슬라이드 · EMP / DEPT / SALGRADE / members / orders 스키마.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **JOIN 5종**: INNER (교집합) / LEFT / RIGHT / FULL (MySQL X) / CROSS (카티시안)
2. **LEFT JOIN + WHERE 에 우측 조건** = INNER 됨 (조건은 ON 에)
3. **서브쿼리 위치**: WHERE / FROM (인라인뷰) / SELECT (스칼라)
4. **상관 서브쿼리** = 바깥 컬럼 참조, 행마다 실행 → 느림 (JOIN 으로)
5. **EXISTS vs IN**: EXISTS 는 짧은 회로 + NULL 안전, IN 은 `NOT IN (..., NULL)` 함정
6. **JOIN 컬럼 인덱스 없으면 풀스캔**, 큰 테이블 90% 성능 = JOIN 컬럼 인덱스

## 가장 중요한 코드 3개

```sql
-- (1) 표준 INNER JOIN + 외래 컬럼
SELECT e.ename, d.dname, d.loc
FROM   emp e
JOIN   dept d ON e.deptno = d.deptno;

-- (2) SELF JOIN + LEFT (매니저 없는 사원 포함)
SELECT e.ename AS 사원, m.ename AS 매니저
FROM   emp e
LEFT JOIN emp m ON e.mgr = m.empno;

-- (3) 상관 서브쿼리 -> 인라인뷰 (성능)
SELECT e.empno, e.ename, e.sal
FROM   emp e
JOIN  (SELECT deptno, AVG(sal) AS avg_sal FROM emp GROUP BY deptno) d
       ON e.deptno = d.deptno
WHERE  e.sal > d.avg_sal;
```

## 면접 한 줄 답변
- **JOIN vs Subquery?** → 컬럼 동시 SELECT → JOIN, 존재 확인 → EXISTS, 행마다 다른 집계 비교 → 윈도우 함수.
- **N+1 query 가 뭐?** → 자바에서 회원 N 명 조회 후 각자의 주문을 N 번 더 쿼리. JOIN 한 번으로 해결.
- **LEFT JOIN 결과가 INNER 같이 나오는 이유?** → WHERE 에 우측 컬럼 조건 → NULL 행 탈락. ON 에 두기.
- **EXISTS 가 IN 보다 빠른 이유?** → 첫 매칭 즉시 중단 (짧은 회로). IN 은 서브쿼리 전체 결과 모음.

---

# 2. Quick Reference (실무 복붙)

## JOIN 5종

| 종류 | 결과 | MySQL |
|--|--|--|
| **INNER JOIN** | 양쪽 매칭만 | O |
| **LEFT JOIN** | 왼쪽 전체 + 매칭 (없으면 NULL) | O |
| **RIGHT JOIN** | 오른쪽 전체 + 매칭 | O |
| **FULL OUTER JOIN** | 양쪽 모두 | **X** (UNION 으로) |
| **CROSS JOIN** | 카티시안 (m x n) | O |

행 수 관계: `INNER ≤ LEFT/RIGHT ≤ FULL ≤ CROSS`

## INNER JOIN

```sql
-- 현대 (권장)
SELECT e.ename, d.dname
FROM   emp e
INNER JOIN dept d ON e.deptno = d.deptno;

-- 구식 (콤마 + WHERE)
SELECT e.ename, d.dname
FROM   emp e, dept d
WHERE  e.deptno = d.deptno;

-- INNER 키워드 생략 가능
JOIN dept d ON ...
```

## LEFT JOIN

```sql
-- 모든 사원 + 부서 (부서 없는 사원도)
SELECT e.ename, d.dname
FROM   emp e
LEFT JOIN dept d ON e.deptno = d.deptno;

-- ON vs WHERE (중요!)
LEFT JOIN dept d ON e.deptno = d.deptno AND d.loc = 'DALLAS';
-- vs
LEFT JOIN dept d ON e.deptno = d.deptno
WHERE  d.loc = 'DALLAS';   -- INNER 됨!
```

## SELF JOIN

```sql
SELECT e.ename AS 사원, m.ename AS 매니저
FROM   emp e
LEFT JOIN emp m ON e.mgr = m.empno;
-- 별칭 필수, 자기 참조 데이터 (조직도, 댓글-대댓글)
```

## Non-Equi JOIN

```sql
-- 급여 등급 매핑
SELECT e.ename, e.sal, s.grade
FROM   emp e
JOIN   salgrade s ON e.sal BETWEEN s.losal AND s.hisal;
```

## FULL OUTER (MySQL 흉내)

```sql
SELECT * FROM A LEFT JOIN B ON A.id = B.id
UNION
SELECT * FROM A RIGHT JOIN B ON A.id = B.id WHERE A.id IS NULL;
```

## 서브쿼리 6 종류

| 종류 | 위치 | 반환 |
|--|--|--|
| 단일행 | WHERE | 1행 1컬럼 (`=`, `>`) |
| 다중행 | WHERE | n행 1컬럼 (`IN`, `ANY`, `ALL`) |
| 다중컬럼 | WHERE | n행 n컬럼 (`(a,b) IN (...)`) |
| 스칼라 | SELECT | 1행 1컬럼 |
| 상관 | WHERE/SELECT | 바깥 컬럼 참조 |
| 인라인뷰 | FROM | 테이블처럼 |

```sql
-- 단일행
SELECT dname FROM dept
WHERE  deptno = (SELECT deptno FROM emp WHERE empno = 7788);

-- 다중행
SELECT * FROM emp
WHERE  deptno IN (SELECT deptno FROM dept WHERE loc = 'NY');

-- 스칼라
SELECT ename,
       (SELECT dname FROM dept d WHERE d.deptno = e.deptno) AS 부서
FROM   emp e;

-- 상관 (느림)
SELECT * FROM emp e
WHERE  sal > (SELECT AVG(sal) FROM emp x WHERE x.deptno = e.deptno);

-- 인라인뷰
SELECT e.*, d.avg_sal FROM emp e
JOIN  (SELECT deptno, AVG(sal) avg_sal FROM emp GROUP BY deptno) d
       ON e.deptno = d.deptno;
```

## 다중행 연산자

```sql
WHERE sal > ANY (SELECT sal FROM emp WHERE deptno = 30);  -- 최솟값보다 큼
WHERE sal > ALL (SELECT sal FROM emp WHERE deptno = 30);  -- 최댓값보다 큼
WHERE deptno IN  (SELECT deptno FROM dept WHERE loc = 'NY');
```

## EXISTS / NOT EXISTS

```sql
-- 주문 있는 회원
SELECT * FROM members m
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id);

-- 주문 없는 회원
SELECT * FROM members m
WHERE  NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id);
```

**EXISTS vs IN**:
- EXISTS: 첫 매칭 즉시 중단 (짧은 회로), NULL 안전
- IN: 서브쿼리 전체 결과 후 비교, `NOT IN (..., NULL)` 함정

## 윈도우 함수 (MySQL 8+)

```sql
SELECT *,
       AVG(sal) OVER (PARTITION BY deptno) AS avg_per_dept,
       RANK()   OVER (PARTITION BY deptno ORDER BY sal DESC) AS rnk
FROM   emp;
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `SELECT *` JOIN → 같은 컬럼 중복 | 명시적 컬럼 + 별칭 |
| LEFT JOIN + WHERE 우측 조건 → INNER | ON 에 두기 |
| ON 없는 JOIN → 카티시안 | ON 또는 WHERE 필수 |
| 상관 서브쿼리 N+1 | JOIN, 윈도우 함수 |
| `COUNT(*)` + LEFT JOIN → NULL 도 1 | `COUNT(o.id)` |
| `NULL = NULL` → false | MySQL `<=>`, PG `IS NOT DISTINCT FROM` |
| 단일행 서브쿼리가 2행 반환 | `IN` 또는 `LIMIT 1` |
| `NOT IN (..., NULL)` → 0행 | `NOT IN (...) AND col IS NOT NULL` 또는 NOT EXISTS |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
JOIN · SubQuery (43p)
│
├── [A] JOIN 종류
│   ├── INNER (교집합)
│   ├── LEFT / RIGHT (한쪽 보존)
│   ├── FULL OUTER (MySQL 미지원)
│   ├── CROSS (카티시안)
│   └── SELF (자기 참조)
│
├── [B] JOIN 조건
│   ├── Equi JOIN (=)
│   ├── Non-Equi (BETWEEN, <, >)
│   ├── ON vs WHERE (OUTER JOIN 핵심)
│   └── 다중 JOIN (3 테이블 이상)
│
├── [C] SubQuery 종류
│   ├── 단일행 (=, <, >)
│   ├── 다중행 (IN, ANY, ALL)
│   ├── 다중컬럼 ((a,b) IN ...)
│   ├── 스칼라 (SELECT 안)
│   ├── 상관 (바깥 컬럼 참조)
│   └── 인라인뷰 (FROM 안)
│
├── [D] EXISTS
│   ├── EXISTS / NOT EXISTS
│   ├── vs IN (짧은 회로, NULL 안전)
│   └── 존재 확인 전용
│
└── [E] 성능
    ├── JOIN 컬럼 인덱스
    ├── 카티시안 곱 방지
    ├── 상관 서브쿼리 → JOIN 변환
    └── N+1 query (자바·JPA)
```

## 학습 진도 체크리스트

### A. JOIN
- [ ] INNER vs LEFT 결과 행 수 관계
- [ ] ON 절과 WHERE 절의 의미 차이
- [ ] SELF JOIN 작성 (조직도)
- [ ] Non-Equi JOIN (SALGRADE)
- [ ] FULL OUTER MySQL 흉내 (UNION)

### B. SubQuery
- [ ] 6 종류 구분
- [ ] 단일행 vs 다중행 연산자
- [ ] 스칼라 서브쿼리 작성
- [ ] 상관 서브쿼리 → 인라인뷰 변환

### C. EXISTS
- [ ] EXISTS / NOT EXISTS 작성
- [ ] EXISTS vs IN 차이
- [ ] NULL 안전성

### D. 성능
- [ ] N+1 query 이해 (JOIN 으로 해결)
- [ ] LEFT JOIN + COUNT(*) 함정
- [ ] 카티시안 곱 방지
- [ ] 윈도우 함수 (MySQL 8+)

## 연관 강의

```
2강 SELECT 응용    -> GROUP BY, 집계
3강 DDL/DML/TX     -> 테이블 만들기
4강 JOIN/SubQuery  <- 현재 위치
5강 JDBC           -> 자바에서 JOIN 결과 받기
6강 관통 PJT       -> 게시판 페이지네이션 + JOIN
```

→ 다음 (JDBC) 에서 **자바 코드로 JOIN 결과 받기** 학습.
