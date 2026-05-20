# SELECT 기본 - 관계형 DB 와의 첫 대화

> **이 강의는 무엇인가**: 44페이지 짜리 DB 트랙 첫 강의. DataBase 가 무엇인지부터 SELECT/WHERE/ORDER BY 의 기본 문법까지.
> **왜 배우는가**: 모든 백엔드 = 데이터를 가져와 처리·저장. SQL 못 쓰면 자바 코드로 모든 데이터를 끌어와 메모리에서 돌리게 됨 → 100배 느리고 비쌈.

---

## 들어가기 전에

- **선수**: 자바 기초 정도면 충분. DB 학습 첫 강의.
- **환경**: MySQL 8 + Workbench. SSAFY 는 보통 MySQL.
- **실습 스키마**: SSAFY_CORPORATION (EMP · DEPT · BONUS · SALGRADE).
- **마인드셋**: "어떻게(how)" 가 아니라 "무엇(what)" 을 선언. 옵티마이저가 실행 계획 결정.

---

## Part A. DataBase 와 RDBMS 개요

### A-1. 데이터 vs 정보

| 구분 | 정의 | 예시 |
|--|--|--|
| **데이터(Data)** | 가공되지 않은 사실·값. 의미 해석 없는 상태. | 성적: 80, 90, 100 |
| **정보(Information)** | 데이터를 가공·처리·분석하여 의미 부여한 결과. | 성적 평균: 85 |

데이터에 **맥락·의미**가 더해지면 정보. 의사결정 가능한 형태.

### A-2. DataBase 의 4가지 속성

| 속성 | 의미 |
|--|--|
| **통합된 데이터(Integrated Data)** | 중복 최소화, 여러 사람이 함께 쓰는 데이터 모음 |
| **저장된 데이터(Stored Data)** | 컴퓨터 저장장치에 물리적으로 저장 |
| **공유 데이터(Shared Data)** | 여러 사용자·프로그램이 동시 접근 가능 |
| **운영 데이터(Operational Data)** | 실제 업무·서비스 운영에 필요한 최신 데이터 |

### A-3. DB 의 7가지 특징

1. **통합성(Integration)**: 데이터 중복 최소화·일관성 유지
2. **독립성(Independence)**: 데이터 구조와 응용 프로그램 분리
3. **무결성(Integrity)**: 정확하고 일관된 상태 유지
4. **보안성(Security)**: 사용자별 접근 권한 관리
5. **일관성(Consistency)**: 동시 접근에도 데이터 모순 없음
6. **공유성(Sharing)**: 같은 데이터를 여러 응용에서 함께 사용
7. **회복성(Recovery)**: 장애·오류 발생 시 복구 가능

### A-4. DBMS 의 역할

```
[User]  [App]                       [User]  [App]
   |      |                            |      |
   v      v                            v      v
 +----+ +----+                       +----------+
 | F1 | | F2 |  (file system)        |   API    |
 +----+ +----+                       +----------+
   |      |                               |
   v      v                               v
 +--------+                         +----------+
 |  DISK  |                         |   DBMS   |
 +--------+                         +----------+
                                          |
                                          v
                                       +----+
                                       | DB |
                                       +----+
```

**File System 의 문제**: 동시 접근 충돌, 중복, 무결성 보장 X, 권한 관리 어려움.
**DBMS 의 해결**: 사용자·앱 사이에서 **생성·정의·공유·관리** 인터페이스 제공.

DBMS 가 제공하는 기능:
- 데이터베이스 조작 인터페이스 (SQL)
- 효율적 데이터 관리 (인덱싱·쿼리 최적화)
- 데이터베이스 구축 (DDL)
- 복구 (Recovery)
- 사용자 권한 부여 (DCL)
- 유지보수 (백업·복제)

---

## Part B. 관계형 데이터베이스 (Relational DB)

### B-1. RDBMS 의 정의

- **행(Row)과 열(Column)** 로 구성된 **테이블(Table)** 형태로 관리.
- 1970 년 E.F. Codd 가 제안한 **관계형 모델** 에 기반.
- 2차원 표 구조 → 직관적 표현.
- **관계(Relationship)**: 기본키·외래키로 테이블 간 연결.
- **SQL** 표준 언어로 조작.
- 데이터 **무결성·일관성** 보장.

### B-2. NoSQL 과의 차이

| 구분 | RDBMS | NoSQL |
|--|--|--|
| 구조 | 스키마 고정, 2차원 테이블 | 스키마 자유, 다양한 모델 (Key-Value, Document, Graph) |
| 데이터 | 정형 | 비정형·반정형 |
| 강점 | 무결성·트랜잭션·복잡 쿼리 | 수평 확장·대용량·유연성 |
| 예시 | MySQL · Oracle · PostgreSQL · MariaDB · SQLite | MongoDB · Redis · Cassandra · DynamoDB |

NoSQL = "Not Only SQL". RDBMS 의 대안일 뿐 우열은 없음.

### B-3. 스키마 (Schema)

DB 안 자료 **구조·표현방법·관계 등 전반적인 명세**.

| 속성명 (Column) | 자료형 | 설명 |
|--|--|--|
| id | VARCHAR(20) | 아이디 |
| name | VARCHAR(50) | 이름 |
| password | VARCHAR(255) | 비밀번호 |
| join_date | DATE | 가입날짜 |

### B-4. 테이블 (Table) 구조

- **테이블**: 행과 열의 모델로 조직된 데이터 요소들의 집합
- **열(Column / Attribute)**: 고유한 자료형 지정 (예: VARCHAR(10), INT)
- **행(Row / Record)**: 실제 데이터가 저장되는 단위
- **기본 키(Primary Key)**: 각 행의 고유 값 (NULL 불가, 중복 불가)
- **외래 키(Foreign Key)**: 다른 테이블의 PK 를 참조

```
+----+----------+--------+------------+
| id | name     | passwd | join_date  |
+----+----------+--------+------------+
| 1  | ssafy    | 1234   | 2019-01-01 |
| 2  | edu      | abcd   | 2020-06-07 |
| 3  | ssafy.pro| 1q2w   | 2021-02-26 |
| 4  | admin    | admin  | 2022-11-28 |
+----+----------+--------+------------+
```

### B-5. SSAFY_CORPORATION 실습 스키마

```
EMP                          DEPT
+----------+----------+      +----------+----------+
| EMPNO    | INT (PK) |      | DEPTNO   | INT (PK) |
| ENAME    | VARCHAR  |      | DNAME    | VARCHAR  |
| JOB      | VARCHAR  |      | LOC      | VARCHAR  |
| MGR      | INT      |      +----------+----------+
| HIREDATE | DATETIME |
| SAL      | DOUBLE   |      SALGRADE
| COMM     | DOUBLE   |      +----------+----------+
| DEPTNO   | INT (FK) |      | GRADE    | INT      |
+----------+----------+      | LOSAL    | DOUBLE   |
                             | HISAL    | DOUBLE   |
                             +----------+----------+
```

- **EMP**: 사원 14명 (Scott·Tiger 의 클래식 예제)
- **DEPT**: 부서 4개 (ACCOUNTING / RESEARCH / SALES / OPERATIONS)
- **SALGRADE**: 급여 등급 5단계 (LOSAL ~ HISAL 범위로 등급 결정)
- **BONUS**: 거의 빈 테이블 (실습용)

이 노트의 모든 예제는 이 스키마 기준.

---

## Part C. SQL (Structured Query Language)

### C-1. SQL 의 정의

> RDBMS 에서 데이터 조작·정의를 위해 사용하는 **표준 언어**.

```
[User] --SQL--> [API] --> [DBMS] --> [DB]
              <-data-
```

### C-2. SQL 의 4가지 특징

1. **배우고 사용하기 쉽다** - 영어 문장 같은 문법
2. **대소문자 구별 안 함** (단, **데이터의 대소문자는 구별**: `'KING' != 'king'`)
3. **선언적 언어** - "어떻게" 가 아니라 "무엇" 을 기술
4. **DBMS 종속적이지 않다** - 표준 SQL 은 모든 DBMS 에서 (방언 일부 제외)

### C-3. SQL 의 분류 (4가지)

| 분류 | 풀네임 | 용도 | 명령어 |
|--|--|--|--|
| **DML** | Data Manipulation Language | 데이터 조작 (조회·추가·수정·삭제) | SELECT, INSERT, UPDATE, DELETE |
| **DDL** | Data Definition Language | 객체 구조 정의/수정/삭제 | CREATE, ALTER, DROP, RENAME |
| **DCL** | Data Control Language | 권한·보안 제어 | GRANT, REVOKE |
| **TCL** | Transaction Control Language | 트랜잭션 단위 제어 | COMMIT, ROLLBACK, SAVEPOINT |

> 💡 SELECT 는 엄밀히는 DQL(Query) 이지만 MySQL 공식 문서는 DML 로 분류.

### C-4. MySQL 주석

```sql
-- 한 줄 주석 (대시 두 개 + 공백)
# 한 줄 주석 (MySQL 만의 확장)
/*
  여러 줄 주석
*/
```

---

## Part D. SELECT 문 - 기본

### D-1. SELECT 문 전체 문법

```sql
SELECT [DISTINCT] {* | column_name | expression [alias]}
  FROM table_references
[WHERE  where_condition]
[GROUP BY {col_name | expr | position}]
[HAVING where_condition]
[ORDER BY {col_name | expr | position} [ASC | DESC]]
[LIMIT  {[offset,] row_count | row_count OFFSET offset}]
```

### D-2. SELECT 문 실행 순서 (논리적 처리 순서)

```
1. FROM     : 데이터를 가져올 대상 테이블 지정
2. WHERE    : 조건을 만족하는 행 필터링
3. GROUP BY : 데이터를 그룹화
4. HAVING   : 그룹 조건 필터링
5. SELECT   : 지정된 열 선택
6. ORDER BY : 결과 정렬
7. LIMIT    : 결과 개수 제한
```

⚠️ **헷갈리는 부분**: 작성 순서 (`SELECT ... FROM ... WHERE`) ≠ 실행 순서 (`FROM → WHERE → ... → SELECT → ORDER BY → LIMIT`).

→ `WHERE` 에서 `SELECT` 의 별칭 사용 불가 (`SELECT sal*12 AS annual FROM emp WHERE annual > 50000` → 에러)

### D-3. 기본 SELECT

```sql
-- 모든 사원 정보 검색
SELECT * FROM emp;

-- 사원이 근무하는 부서번호 검색 (중복 포함)
SELECT deptno FROM emp;

-- 사원이 근무하는 부서번호 검색 (중복 제거)
SELECT DISTINCT deptno FROM emp;

-- 사원의 이름·부서번호·업무 조회
SELECT ename, deptno, job FROM emp;
```

> 💡 `SELECT *` 회피 이유: ① 새 컬럼 추가 시 의도치 않은 노출, ② 네트워크 트래픽 증가, ③ Index-only Scan 못 씀.

### D-4. 별칭 (Alias)

```sql
-- AS 키워드 (생략 가능, 가독성 위해 권장)
SELECT ename AS 이름,
       empno AS 사번,
       sal * 12 AS 연봉,
       job   AS "업 무"          -- 띄어쓰기 포함 시 따옴표
FROM emp;
```

별칭 용도:
- 결과 헤더 명확화
- 자바 ResultSet 매핑 키
- 계산 컬럼(`sal*12`)에 의미 부여

### D-5. 사칙연산 · NULL 처리

```sql
SELECT ename       이름,
       empno    AS "사번",
       sal               급여,
       comm              커미션,
       sal + comm     AS "커미션 포함 급여",
       sal + IFNULL(comm, 0) AS "커미션 포함 급여2"
FROM   emp;
```

| EMPNO | ENAME | SAL  | COMM | SAL+COMM | SAL+IFNULL |
|--|--|--|--|--|--|
| 7369 | SMITH | 800  | NULL | NULL     | 800 |
| 7499 | ALLEN | 1600 | 300  | 1900     | 1900 |
| 7521 | WARD  | 1250 | 500  | 1750     | 1750 |

**핵심**: NULL 은 어떤 연산을 해도 NULL.
- `NULL + 100 = NULL`
- `NULL = NULL` → false (등호 비교도 NULL)
- → `IFNULL(comm, 0)` 으로 NULL 을 0 으로 치환해야 의미 있는 합산

다른 DBMS 의 동등 함수:
- Oracle / SQLite: `NVL(comm, 0)`
- ANSI 표준: `COALESCE(comm, 0)` (가장 호환성 높음)

### D-6. CASE WHEN - SQL 의 if/else

```sql
-- 문법
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE              result_else
END
```

- 위에서부터 평가, **첫 매치** 의 result 반환
- 모든 조건이 false 면 ELSE
- ELSE 생략 시 NULL

```sql
-- 예시: 사원의 연봉 등급 분류
SELECT empno 사번,
       ename 이름,
       sal   급여,
       CASE
           WHEN sal >= 5000 THEN '고액연봉'
           WHEN sal >= 2000 THEN '평균연봉'
           ELSE                  '저액연봉'
       END AS 연봉등급
FROM   emp;
```

| EMPNO | ENAME | SAL  | 연봉등급 |
|--|--|--|--|
| 7369 | SMITH | 800  | 저액연봉 |
| 7499 | ALLEN | 1600 | 저액연봉 |
| 7566 | JONES | 2975 | 평균연봉 |
| 7839 | KING  | 5000 | 고액연봉 |

**활용 시나리오**:
- 데이터 분류 표시
- 피벗 (가로 → 세로 변환)
- 행별 다른 계산식 적용

---

## Part E. WHERE 절 - 조건 필터링

### E-1. WHERE 의 역할

```sql
SELECT column1, column2, ...
FROM   table_name
WHERE  condition;
```

조건에 맞는 레코드만 조회. UPDATE/DELETE 에서도 동일하게 사용.

### E-2. 비교 연산자

| 연산자 | 의미 |
|--|--|
| `=` | 같다 |
| `<` `>` `<=` `>=` | 대소 비교 |
| `!=` 또는 `<>` | 같지 않다 |

### E-3. 논리 연산자 (NOT · AND · OR) 와 3-valued logic

**NOT 진리표**:

| A | NOT A |
|--|--|
| TRUE | FALSE |
| FALSE | TRUE |
| **NULL** | **NULL** |

**AND 진리표** (Short Circuit):

| AND | TRUE | FALSE | NULL |
|--|--|--|--|
| **TRUE**  | TRUE  | FALSE | NULL |
| **FALSE** | FALSE | FALSE | FALSE |
| **NULL**  | NULL  | FALSE | NULL |

**OR 진리표** (Short Circuit):

| OR | TRUE | FALSE | NULL |
|--|--|--|--|
| **TRUE**  | TRUE | TRUE  | TRUE |
| **FALSE** | TRUE | FALSE | NULL |
| **NULL**  | TRUE | NULL  | NULL |

**3-valued logic** 의 핵심:
- SQL 의 boolean 은 TRUE/FALSE 만이 아니라 **NULL 도 가능**
- WHERE 절은 **TRUE 인 행만** 가져옴 (FALSE 와 NULL 은 제외)
- 즉, `WHERE col = NULL` 이 NULL 을 반환하므로 → 한 행도 안 옴

### E-4. AND / OR 예시

```sql
-- 부서 30, 급여 1500 이상
SELECT ename, sal, deptno
FROM   emp
WHERE  deptno = 30
  AND  sal   >= 1500;

-- 부서 20 또는 30
SELECT empno, ename, deptno
FROM   emp
WHERE  deptno = 30
   OR  deptno = 20;
```

### E-5. NOT · != · <>

```sql
-- 부서가 20, 30 이 아닌 사원
SELECT empno, ename, deptno
FROM   emp
WHERE  deptno != 30
  AND  deptno <> 20;

-- 동일한 의미: NOT 으로 묶기
SELECT empno, ename, deptno
FROM   emp
WHERE  NOT (deptno = 30 OR deptno = 20);
```

### E-6. IN - 여러 값 중 하나

```sql
-- 업무가 MANAGER, ANALYST, PRESIDENT
SELECT empno, ename, job
FROM   emp
WHERE  job IN ('MANAGER', 'ANALYST', 'PRESIDENT');

-- NOT IN
SELECT empno, ename, deptno
FROM   emp
WHERE  deptno NOT IN (10, 20);
```

⚠️ **NOT IN + NULL 함정**: `WHERE col NOT IN (1, 2, NULL)` → 항상 0 행 (NULL 비교가 NULL 이라 NOT 도 NULL).

### E-7. BETWEEN - 범위

```sql
-- 급여 2000 이상 3000 이하
SELECT empno, ename, sal
FROM   emp
WHERE  sal BETWEEN 2000 AND 3000;
-- 동등: sal >= 2000 AND sal <= 3000

-- 1981 년 입사
SELECT empno, ename, hiredate
FROM   emp
WHERE  hiredate BETWEEN '1981-01-01' AND '1981-12-31';
```

- BETWEEN 은 **양 끝 포함**
- 숫자·문자·날짜 모두 지원

### E-8. NULL 비교 - IS NULL / IS NOT NULL

```sql
-- 커미션 NULL 인 사원
SELECT empno, ename, comm
FROM   emp
WHERE  comm IS NULL;       -- ✅ 행 가져옴

SELECT empno, ename, comm
FROM   emp
WHERE  comm = NULL;        -- ❌ 항상 0 행 (3-valued logic)

-- 커미션이 있는 사원 (SALESMAN 들)
SELECT empno, ename, job, comm
FROM   emp
WHERE  comm IS NOT NULL;
```

**SQL 의 가장 흔한 버그 1순위**. NULL 비교는 무조건 `IS NULL` / `IS NOT NULL`.

### E-9. LIKE - 패턴 매칭

| 와일드 카드 | 의미 |
|--|--|
| `%` | 0개 이상의 임의 문자 |
| `_` | 정확히 1개의 임의 문자 |

```sql
-- M 으로 시작
SELECT empno, ename FROM emp WHERE ename LIKE 'M%';

-- E 가 포함됨
SELECT empno, ename FROM emp WHERE ename LIKE '%E%';

-- 세 번째 글자가 A
SELECT empno, ename FROM emp WHERE ename LIKE '__A%';
```

**인덱스 함정**:
- ✅ `LIKE 'M%'` - prefix scan 인덱스 사용 가능
- ❌ `LIKE '%M'`, `LIKE '%M%'` - prefix 가 와일드카드라 **풀스캔**
- → 부분 매칭이 자주 필요하면 Full-text Index 또는 검색 엔진 (Elasticsearch).

---

## Part F. ORDER BY - 정렬

### F-1. 기본 문법

```sql
SELECT column1, column2, ...
FROM   table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...;
```

- 기본은 **ASC** (오름차순). DESC 만 명시.
- 여러 컬럼 가능 (1차 정렬 → 2차 정렬).

### F-2. 예시

```sql
-- 이름 내림차순
SELECT * FROM emp ORDER BY ename DESC;

-- 급여 내림차순
SELECT empno, ename, sal
FROM   emp
ORDER BY sal DESC;

-- 부서 오름차순 + 부서 내에서 급여 내림차순
SELECT empno, ename, deptno, sal
FROM   emp
WHERE  deptno IN (20, 30)
ORDER BY deptno ASC, sal DESC;
```

### F-3. NULL 위치 제어

```sql
-- MySQL: NULL 은 ASC 시 맨 앞, DESC 시 맨 뒤
ORDER BY comm DESC;            -- NULL 들이 맨 뒤

-- 명시적 제어 (MySQL 트릭)
ORDER BY (comm IS NULL), comm DESC;   -- NOT NULL 먼저, NULL 맨 뒤

-- Oracle / PostgreSQL 표준
ORDER BY comm DESC NULLS LAST;
```

---

## 자주 빠지는 함정

- ❌ `SELECT *` 운영 코드에 사용 → 컬럼 추가 시 깜짝 노출 + 성능
  ✅ 필요한 컬럼만 명시
- ❌ `WHERE col = NULL` → 항상 0 행
  ✅ `WHERE col IS NULL`
- ❌ `sal + comm` (comm 이 NULL) → 결과 NULL
  ✅ `sal + IFNULL(comm, 0)` 또는 `COALESCE(comm, 0)`
- ❌ `ORDER BY` 없이 `LIMIT 10` → "어떤 10개" 가 올지 비결정
  ✅ 항상 `ORDER BY` 와 함께
- ❌ `LIKE '%kim%'` 운영에 빈번하게 → 풀스캔
  ✅ `'kim%'` (prefix), 또는 Full-text Index
- ❌ `WHERE annual > 50000` (annual 은 SELECT 별칭) → 에러
  ✅ WHERE 에선 `WHERE sal * 12 > 50000` 직접 표현, ORDER BY 에서만 별칭 허용
- ❌ `WHERE col NOT IN (1, 2, NULL)` → 항상 0 행
  ✅ NULL 제외하고 `NOT IN (1, 2)`
- ❌ 대소문자 가정: `WHERE ename = 'king'` (실제 KING) → 0 행
  ✅ 데이터 대소문자 확인 또는 `UPPER(ename) = 'KING'`

---

## 자가점검

1. `SELECT * FROM emp WHERE comm = NULL` 결과 행 수는?
2. `LIKE '김%'` 와 `LIKE '%김'` 의 인덱스 활용 차이?
3. `SELECT DISTINCT dept, name FROM emp` 가 dept 만 distinct 하지 않는 이유?
4. SQL 의 실행 순서를 7단계로 나열하시오. 작성 순서와 어떻게 다른가?
5. `comm + 100` 이 NULL 인 사원이 절반인 이유와 해결 방법?

<details><summary>풀이</summary>

1. **0행**. SQL 의 3-valued logic 으로 `= NULL` 은 NULL (false 아님). WHERE 절은 TRUE 인 행만 반환하므로 0 행. `IS NULL` 만 사용.

2. `'김%'` - prefix 가 고정 → **B-Tree 인덱스 prefix scan** 가능. 빠름.
   `'%김'` - prefix 가 와일드카드 → 인덱스 못 씀, **풀스캔**. 대규모 데이터에서 치명적.

3. `DISTINCT` 는 **SELECT 에 명시된 모든 컬럼 조합** 기준. `DISTINCT dept, name` 은 `(dept, name)` 쌍이 같은 행 제거. dept 만 중복 제거하려면 `SELECT DISTINCT dept` (name 빼고).

4. **실행 순서**: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`
   **작성 순서**: `SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT`
   → 차이 때문에 `WHERE` 에서 `SELECT` 별칭 못 씀 (SELECT 가 아직 실행 전이라 별칭이 없음). `ORDER BY` 에선 SELECT 가 먼저 실행되어 별칭 사용 가능.

5. NULL 처리 안 됨. EMP 에서 SALESMAN 4명만 COMM 있고 나머지는 NULL. NULL + 100 = NULL.
   해결: `IFNULL(comm, 0) + 100` 또는 `COALESCE(comm, 0) + 100` 으로 NULL 을 0 으로 치환.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.3 표지·TOC·학습목표 | 들어가기 전에 |
| p.4 ~ p.8 DataBase 개요·특징·DBMS | §Part A |
| p.9 ~ p.13 관계형 DB·스키마·테이블 구조 | §Part B |
| p.14 ~ p.18 SQL 정의·특징·분류 | §Part C |
| p.19 ~ p.28 SELECT 문·alias·CASE | §Part D |
| p.29 ~ p.41 WHERE·논리·IN·BETWEEN·NULL·LIKE | §Part E |
| p.42 ~ p.43 ORDER BY | §Part F |
| p.44 마무리 | (생략) |

_44p 슬라이드 전 범위 + SSAFY_CORPORATION 실습 스키마 정확 반영._
