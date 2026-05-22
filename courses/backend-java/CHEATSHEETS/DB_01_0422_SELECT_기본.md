# SELECT 기본 — 치트시트

> 44p 슬라이드 · HR_CORP (EMP / DEPT) 스키마.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **SQL** = 선언형 (무엇을), 옵티마이저가 어떻게 결정
2. **4 분류**: DML(SELECT/INSERT/UPDATE/DELETE) · DDL(CREATE/ALTER/DROP) · DCL(GRANT/REVOKE) · TCL(COMMIT/ROLLBACK)
3. **SELECT 실행 순서**: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`
4. **NULL 비교는 무조건 `IS NULL`**, `=NULL` 은 0행
5. **WHERE 에선 SELECT 별칭 사용 불가**, ORDER BY 에선 가능
6. **`NOT IN (..., NULL)`** = 항상 0행 (3-valued logic 함정)

## 가장 중요한 코드 3개

```sql
-- (1) 표준 SELECT
SELECT empno, ename, sal * 12 AS annual
FROM   emp
WHERE  deptno IN (20, 30) AND comm IS NOT NULL
ORDER BY annual DESC, ename ASC
LIMIT 10;

-- (2) CASE WHEN 으로 등급 분류
SELECT ename, sal,
       CASE WHEN sal >= 5000 THEN '고액'
            WHEN sal >= 2000 THEN '평균'
            ELSE                  '저액'
       END AS 등급
FROM   emp;

-- (3) NULL 위치 제어 (MySQL)
SELECT ename, comm FROM emp
ORDER BY (comm IS NULL), comm DESC;
```

## 면접 한 줄 답변
- **SQL 이 선언형이라는 게?** → "무엇" 만 기술, 옵티마이저가 "어떻게" 결정. 자바와 달리 인덱스·조인 알고리즘 자동 최적화.
- **`SELECT *` 비권장 이유?** → 새 컬럼 노출 위험 + 네트워크 비용 + 인덱스 효율 ↓.
- **WHERE 별칭 안 되는 이유?** → 실행 순서상 WHERE 가 SELECT 전. 별칭이 아직 안 만들어짐.
- **DBMS 가 필요한 이유?** → 동시 접근 제어 + 무결성 + 권한·복구.

---

# 2. Quick Reference (실무 복붙)

## SQL 4 분류

| 분류 | 풀네임 | 명령어 |
|--|--|--|
| **DML** | Data Manipulation | SELECT, INSERT, UPDATE, DELETE |
| **DDL** | Data Definition | CREATE, ALTER, DROP, RENAME, TRUNCATE |
| **DCL** | Data Control | GRANT, REVOKE |
| **TCL** | Transaction Control | COMMIT, ROLLBACK, SAVEPOINT |

## SELECT 실행 순서 vs 작성 순서

```
실행: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
작성: SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT
```

→ WHERE 에서 SELECT 별칭 사용 불가 (별칭은 SELECT 단계에서 만들어짐)

## WHERE 연산자

```sql
-- 비교
= != <> < > <= >=

-- 범위
WHERE sal BETWEEN 1000 AND 3000        -- 양 끝 포함
WHERE deptno IN (10, 20, 30)
WHERE deptno NOT IN (10, 20)           -- 주의: NULL 포함 시 0행

-- NULL (3-valued logic)
WHERE comm IS NULL                     -- O
WHERE comm IS NOT NULL
WHERE comm = NULL                      -- X (0행)

-- 패턴
WHERE ename LIKE 'S%'                  -- S 로 시작
WHERE ename LIKE '%ING'                -- ING 로 끝
WHERE ename LIKE '__A%'                -- 3번째 글자가 A
```

## 별칭 (alias)

```sql
-- 컬럼 별칭
SELECT empno AS 사번, ename AS "이름", sal*12 annual    -- AS 생략 OK

-- 테이블 별칭 (필수: SELF JOIN)
SELECT e.ename FROM emp e WHERE e.deptno = 10;

-- WHERE 에서 별칭 X
SELECT sal*12 AS annual FROM emp WHERE annual > 50000;  -- X
-- 해결
SELECT sal*12 AS annual FROM emp WHERE sal*12 > 50000;  -- O
SELECT sal*12 AS annual FROM emp ORDER BY annual DESC;  -- O (ORDER BY OK)
```

## ORDER BY

```sql
ORDER BY deptno ASC, sal DESC            -- 다중 정렬
ORDER BY 2                                -- 2번째 컬럼 (비권장)

-- NULL 위치 (MySQL 트릭)
ORDER BY (comm IS NULL), comm DESC       -- NULL 뒤로
ORDER BY comm DESC NULLS LAST            -- Oracle/PostgreSQL
```

## NULL 처리 함수

```sql
IFNULL(comm, 0)                          -- NULL 이면 0
COALESCE(a, b, c)                        -- 첫 non-NULL
NULLIF(a, b)                             -- a=b 면 NULL, 아니면 a
```

## CASE WHEN

```sql
CASE WHEN sal >= 5000 THEN '고액'
     WHEN sal >= 2000 THEN '평균'
     ELSE                  '저액'
END

-- 단순 CASE
CASE deptno
    WHEN 10 THEN 'ACCOUNTING'
    WHEN 20 THEN 'RESEARCH'
    ELSE        'OTHER'
END
```

## LIMIT (페이지네이션)

```sql
LIMIT 10                                 -- 처음 10행
LIMIT 10 OFFSET 20                       -- 21번째부터 10행 (3페이지)
LIMIT 20, 10                             -- 위와 동일 (옛 문법)
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `WHERE comm = NULL` → 0행 | `IS NULL` |
| `NOT IN (10, 20, NULL)` → 0행 | `NOT IN (10, 20) AND col IS NOT NULL` |
| WHERE 에 SELECT 별칭 | 식 직접 또는 서브쿼리 |
| `SELECT *` 운영 코드 | 명시적 컬럼만 |
| `YEAR(hiredate) = 1981` 큰 테이블 | `BETWEEN '1981-01-01' AND '1981-12-31'` (인덱스) |
| 한글 정렬 깨짐 | `COLLATE utf8mb4_unicode_ci` |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
SELECT 기본 (44p)
│
├── [A] DataBase 기초
│   ├── DB 4 속성 (영속성·통합·공유·변화)
│   ├── DBMS 7 특징
│   ├── RDBMS vs NoSQL
│   └── 스키마 (Schema)
│
├── [B] SQL 4 분류
│   ├── DML (SELECT, INSERT, UPDATE, DELETE)
│   ├── DDL (CREATE, ALTER, DROP)
│   ├── DCL (GRANT, REVOKE)
│   └── TCL (COMMIT, ROLLBACK)
│
├── [C] SELECT 문법
│   ├── 7단계 실행 순서
│   ├── 별칭 (AS)
│   ├── IFNULL / NULLIF / COALESCE
│   └── CASE WHEN
│
├── [D] WHERE 절
│   ├── 비교 연산자
│   ├── IN / BETWEEN / LIKE
│   ├── 3-valued logic (TRUE/FALSE/NULL)
│   └── IS NULL / IS NOT NULL
│
└── [E] ORDER BY / LIMIT
    ├── ASC / DESC
    ├── 다중 정렬
    ├── NULL 위치 제어
    └── LIMIT + OFFSET
```

## 학습 진도 체크리스트

### A. DB 기초
- [ ] DB 4 속성과 DBMS 7 특징
- [ ] RDBMS 와 NoSQL 의 차이

### B. SQL 분류
- [ ] DML / DDL / DCL / TCL 명령어 구분
- [ ] SELECT 가 엄밀히 DQL 인 이유

### C. SELECT
- [ ] 7단계 실행 순서 (FROM → WHERE → ... → LIMIT)
- [ ] WHERE 에 별칭 안 되는 이유
- [ ] IFNULL / COALESCE / NULLIF 차이
- [ ] CASE WHEN 작성

### D. WHERE
- [ ] 3-valued logic 이해
- [ ] `= NULL` 함정 / `IS NULL` 사용
- [ ] `NOT IN (..., NULL)` 함정
- [ ] IN / BETWEEN / LIKE 활용

### E. ORDER BY
- [ ] 다중 정렬
- [ ] MySQL NULL 위치 트릭
- [ ] LIMIT + OFFSET 페이지네이션

## 연관 강의

```
1강 SELECT 기본    <- 현재 위치
2강 SELECT 응용    -> GROUP BY, HAVING, View, 내장 함수
3강 DDL/DML/TX     -> 테이블 만들기, 트랜잭션
4강 JOIN/SubQuery  -> 여러 테이블 합치기
5강 JDBC           -> 자바 -> DB 연결
```

→ 다음 강의 (SELECT 응용) 에서 **집계·그룹화·뷰** 학습.
