# SELECT 기본 - 퀴즈

> 14문항. 개념·적용·디버그·면접. SSAFY_CORPORATION (EMP/DEPT) 기준.

---

### Q1. (개념) DBMS 가 File System 대신 필요한 이유 3가지?

<details><summary>정답</summary>

1. **동시 접근 제어** - 여러 사용자가 같은 데이터를 안전하게 읽고 씀 (Lock·MVCC)
2. **무결성 보장** - PK·FK·CHECK 제약으로 일관된 상태 유지
3. **권한·복구** - 사용자별 GRANT/REVOKE, 장애 복구 (Recovery)

추가:
- 데이터 통합 (중복 최소화)
- 데이터 독립성 (응용 프로그램과 분리)
- SQL 이라는 표준 인터페이스

</details>

### Q2. (개념) SQL 의 4가지 분류와 각 명령어를 정리하시오.

<details><summary>정답</summary>

| 분류 | 풀네임 | 명령어 |
|--|--|--|
| **DML** | Data Manipulation | SELECT, INSERT, UPDATE, DELETE |
| **DDL** | Data Definition | CREATE, ALTER, DROP, RENAME |
| **DCL** | Data Control | GRANT, REVOKE |
| **TCL** | Transaction Control | COMMIT, ROLLBACK, SAVEPOINT |

> SELECT 는 엄밀히 DQL (Query) 이지만 MySQL 공식 문서는 DML 로 분류.

</details>

### Q3. (개념) `SELECT *` 가 비권장인 이유 3가지?

<details><summary>정답</summary>

1. 새 컬럼 추가 시 의도치 않은 데이터 노출 (예: password)
2. 네트워크·메모리 비용 ↑
3. **Index-only scan 불가** - 필요한 컬럼만 명시해야 인덱스에서 바로 조회 가능

</details>

### Q4. (개념) SELECT 의 7단계 실행 순서? 작성 순서와 어떻게 다른가?

<details><summary>정답</summary>

**실행 순서**:
```
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

**작성 순서**:
```
SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT
```

→ 차이 때문에 **`WHERE` 에서 SELECT 별칭 사용 불가** (SELECT 가 아직 실행 안 됨). `ORDER BY` 에선 사용 가능.

</details>

### Q5. (적용) EMP 의 사원 14명 중 부서가 30 또는 20 인 사원의 사번·이름·부서번호 조회. (두 가지 방법)

<details><summary>정답</summary>

**방법 1: OR**
```sql
SELECT empno, ename, deptno
FROM   emp
WHERE  deptno = 30 OR deptno = 20;
```

**방법 2: IN (권장)**
```sql
SELECT empno, ename, deptno
FROM   emp
WHERE  deptno IN (20, 30);
```

IN 은 가독성↑, 값이 많을수록 유리. NOT IN 은 NULL 함정 주의.

</details>

### Q6. (적용) 모든 사원의 사번·이름·급여·연봉등급 (5000+ 고액 / 2000+ 평균 / 그 외 저액) 조회.

<details><summary>정답</summary>

```sql
SELECT empno 사번,
       ename 이름,
       sal   급여,
       CASE
           WHEN sal >= 5000 THEN '고액연봉'
           WHEN sal >= 2000 THEN '평균연봉'
           ELSE                  '저액연봉'
       END   AS 연봉등급
FROM   emp;
```

CASE WHEN 은 위에서부터 첫 매치, ELSE 는 모든 조건 실패 시.

</details>

### Q7. (디버그) `WHERE comm = NULL` 의 결과와 이유?

<details><summary>정답</summary>

**0행**. SQL 의 3-valued logic 으로:
- `NULL = NULL` → NULL (true 아님, false 도 아님)
- WHERE 절은 **TRUE 인 행만** 가져옴 → NULL 행은 제외

**정답 쿼리**:
```sql
WHERE comm IS NULL;          -- 행을 가져옴
WHERE comm IS NOT NULL;
```

이게 SQL 입문자가 가장 많이 빠지는 함정. NULL 비교는 무조건 `IS NULL`.

</details>

### Q8. (디버그) 이 쿼리의 의도와 실제 결과는?

```sql
SELECT empno, ename, deptno FROM emp WHERE deptno NOT IN (10, 20, NULL);
```

<details><summary>정답</summary>

**의도**: 부서 10, 20 이 아닌 사원.
**실제**: 항상 0 행.

**이유**: `NOT IN (10, 20, NULL)` 은:
- `deptno != 10 AND deptno != 20 AND deptno != NULL`
- 마지막 비교가 NULL → 전체 AND 가 NULL
- WHERE 는 NULL 행 제외 → 0 행

**해결**: IN/NOT IN 리스트에 NULL 넣지 말기. NULL 처리 별도:
```sql
WHERE deptno NOT IN (10, 20) AND deptno IS NOT NULL;
```

</details>

### Q9. (적용) 1981 년 입사 사원 조회 (BETWEEN vs YEAR 함수 비교).

<details><summary>정답</summary>

```sql
-- 방법 1: BETWEEN (권장)
SELECT empno, ename, hiredate
FROM   emp
WHERE  hiredate BETWEEN '1981-01-01' AND '1981-12-31';

-- 방법 2: YEAR 함수
SELECT empno, ename, hiredate
FROM   emp
WHERE  YEAR(hiredate) = 1981;
```

BETWEEN 양 끝 포함. `YEAR(hiredate)` 는 함수라 **컬럼 인덱스 미사용** → 큰 테이블엔 BETWEEN 권장.

</details>

### Q10. (적용) 이름의 세 번째 글자가 'A' 인 사원 조회.

<details><summary>정답</summary>

```sql
SELECT empno, ename
FROM   emp
WHERE  ename LIKE '__A%';
```

`_` (언더스코어) = 임의의 한 글자. 따라서 `__A%` = "임의 한 글자 + 임의 한 글자 + A + 나머지".

`%` = 0개 이상의 임의 문자.

</details>

### Q11. (적용) 부서별 오름차순 + 부서 내 급여 내림차순으로 정렬.

<details><summary>정답</summary>

```sql
SELECT empno, ename, deptno, sal
FROM   emp
WHERE  deptno IN (20, 30)
ORDER BY deptno ASC, sal DESC;
```

다중 정렬 - 앞 컬럼이 1차, 뒤 컬럼이 2차. ASC 는 생략 가능 (기본).

</details>

### Q12. (디버그) `SELECT sal*12 AS annual FROM emp WHERE annual > 50000` 이 에러. 왜?

<details><summary>정답</summary>

**실행 순서 때문**. SQL 은 `FROM -> WHERE -> ... -> SELECT -> ORDER BY` 순.
WHERE 가 실행될 때 SELECT 가 아직 처리 안 되어 `annual` 별칭이 없음.

**해결**:
```sql
-- 방법 1: WHERE 에서 직접 표현
WHERE sal * 12 > 50000

-- 방법 2: 서브쿼리
SELECT * FROM (
    SELECT empno, ename, sal * 12 AS annual FROM emp
) t
WHERE annual > 50000;

-- 방법 3: ORDER BY 에선 별칭 OK
SELECT empno, ename, sal * 12 AS annual FROM emp ORDER BY annual DESC;
```

</details>

### Q13. (디버그) MySQL 에서 NULL 위치를 맨 뒤로 보내려면?

<details><summary>정답</summary>

```sql
-- MySQL (NULLS LAST 지원 안 함)
SELECT empno, ename, comm FROM emp
ORDER BY (comm IS NULL), comm DESC;

-- Oracle / PostgreSQL (표준)
SELECT empno, ename, comm FROM emp
ORDER BY comm DESC NULLS LAST;
```

MySQL 트릭: `comm IS NULL` 이 boolean(0/1) 으로 변환되어 정렬 키로 사용됨 (NOT NULL=0 먼저, NULL=1 뒤로).

</details>

### Q14. (면접) "SQL 이 선언적 언어라는 게 무슨 뜻인가? 자바와 비교해서 설명하시오."

<details><summary>정답</summary>

**"어떻게(how)" 가 아니라 "무엇(what)" 을 기술**.

| 구분 | 절차적 (Java) | 선언적 (SQL) |
|--|--|--|
| 코드 | for·if 로 데이터 순회·필터·정렬 | `SELECT ... WHERE ... ORDER BY` |
| 책임 | 개발자가 알고리즘·자료구조 결정 | 옵티마이저가 실행 계획 결정 |
| 변화 | 데이터·인덱스 바뀌면 코드 수정 | 옵티마이저가 자동 재최적화 |

```sql
-- 선언: "DEV 부서의 5000+ 사원을 입사 최신순으로 5명"
SELECT * FROM emp WHERE deptno = 10 AND sal >= 5000
ORDER BY hiredate DESC LIMIT 5;
```

DB 가 알아서:
- 인덱스 사용 여부 결정
- 병렬 처리 가능 여부 평가
- 조인 알고리즘 선택 (nested loop / hash / merge)
- 임시 테이블 사용 여부

**장점**: 데이터가 1만 행이든 10억 행이든 같은 SQL. 자바는 메모리 한계로 알고리즘 자체를 바꿔야 함.

**단점**: 옵티마이저가 잘못 판단하면 느림 → `EXPLAIN` 으로 실행 계획 분석 필수.

</details>
