# SELECT 응용 - 퀴즈

> 14문항. 개념·적용·디버그·면접. EMP/DEPT 스키마 기준.

---

### Q1. (개념) 5가지 핵심 집계 함수와 NULL 처리?

<details><summary>정답</summary>

| 함수 | NULL 처리 |
|--|--|
| `COUNT(*)` | NULL 포함 (모든 행) |
| `COUNT(col)` | NULL 제외 |
| `SUM(col)` | NULL 제외 |
| `AVG(col)` | NULL 제외 (분자·분모 모두) |
| `MIN/MAX(col)` | NULL 제외 |

⚠️ AVG 는 NULL 을 0 으로 치지 않음. 14명 중 4명만 COMM 있으면 `AVG(comm) = SUM(comm)/4`, 14가 아님.

</details>

### Q2. (개념) WHERE 와 HAVING 의 차이를 실행 순서로 설명.

<details><summary>정답</summary>

**SELECT 실행 순서**: `FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT`

- **WHERE**: GROUP BY **이전** - 개별 행 필터링. 집계함수 사용 불가.
- **HAVING**: GROUP BY **이후** - 그룹 (집계 결과) 필터링. 집계함수 사용 가능.

```sql
SELECT deptno, AVG(sal)
FROM   emp
WHERE  sal > 1000           -- 1000 이상 행만 그룹화 대상
GROUP BY deptno
HAVING AVG(sal) > 2500;     -- 그룹 평균이 2500 이상인 그룹만
```

</details>

### Q3. (디버그) 이 쿼리의 표준 SQL 위반 사항?

```sql
SELECT name, dept, COUNT(*) FROM emp GROUP BY dept;
```

<details><summary>정답</summary>

`name` 이 GROUP BY 에 없음. **표준 SQL 위반**.

- MySQL 5.7+ 의 `ONLY_FULL_GROUP_BY` 모드: 에러
- 옛 MySQL: 임의의 name 반환 (그룹의 첫 행? 마지막 행? 예측 불가)

**해결**:
```sql
-- (1) GROUP BY 에 name 추가 (의도 다름)
GROUP BY dept, name

-- (2) 집계 함수로 감싸기
SELECT MIN(name), dept, COUNT(*) FROM emp GROUP BY dept

-- (3) GROUP_CONCAT 으로 합치기 (MySQL)
SELECT GROUP_CONCAT(name), dept, COUNT(*) FROM emp GROUP BY dept
```

</details>

### Q4. (적용) 부서별 사원수·급여총액·평균급여 (소수 둘째 자리 반올림)·최고급여·최저급여 조회.

<details><summary>정답</summary>

```sql
SELECT deptno                 부서,
       COUNT(*)               사원수,
       SUM(sal)               급여총액,
       ROUND(AVG(sal), 2)     평균급여,
       MAX(sal)               최고급여,
       MIN(sal)               최저급여
FROM   emp
GROUP BY deptno
ORDER BY deptno;
```

`ROUND(x, n)` - n 자릿수로 반올림. 음수면 정수부 반올림 (`ROUND(1526, -2) = 1500`).

</details>

### Q5. (적용) 급여(커미션포함) 평균이 2000 이상인 부서·사원수·평균급여 조회.

<details><summary>정답</summary>

```sql
SELECT deptno                                         부서번호,
       COUNT(*)                                       사원수,
       ROUND(AVG(sal + IFNULL(comm, 0)), 2)           "평균급여(커미션포함)"
FROM   emp
GROUP BY deptno
HAVING AVG(sal + IFNULL(comm, 0)) > 2000;
```

핵심:
- `IFNULL(comm, 0)` - NULL → 0 으로 (안 그러면 평균에 영향)
- HAVING 에 동일 식 (별칭이 아닌 식 직접 - 표준 호환)

</details>

### Q6. (적용) WITH ROLLUP 으로 부서별 + 전체 합계 한 번에 구하기.

<details><summary>정답</summary>

```sql
SELECT IFNULL(d.dname, '총계') AS 부서,
       SUM(e.sal)              AS 급여총액
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname WITH ROLLUP;
```

결과: 부서별 행들 + 마지막에 `(NULL, 전체합)` 한 행.

ROLLUP 의 NULL 과 실제 NULL 구분: `GROUPING(d.deptno) = 1` 이면 ROLLUP NULL.

</details>

### Q7. (디버그) `LENGTH('BOOTCAMP 김')` 결과는? `CHAR_LENGTH` 와 어떻게 다른가?

<details><summary>정답</summary>

- `LENGTH('BOOTCAMP 김')` = **9 바이트**
  - BOOTCAMP 5바이트 + 공백 1바이트 + 김 3바이트 (UTF-8)
- `CHAR_LENGTH('BOOTCAMP 김')` = **7 문자**
  - S, S, A, F, Y, ' ', 김 = 7개 문자

**핵심**: UTF-8 한글 1글자 = 3바이트. 한글·이모지 다루는 검색·길이 제한엔 `CHAR_LENGTH` 사용.

</details>

### Q8. (적용) 모든 사원 이름의 앞 3글자만 추출 + 대문자로 변환.

<details><summary>정답</summary>

```sql
SELECT ename, UPPER(SUBSTR(ename, 1, 3)) AS prefix
FROM   emp;
```

또는:
```sql
SELECT ename, UPPER(LEFT(ename, 3)) AS prefix FROM emp;
```

`SUBSTR(s, pos, len)` - pos 는 1-based. `LEFT(s, n)` - 앞 n 글자.

</details>

### Q9. (적용) 모든 사원 중 'PRESIDENT' 인 사원에게 "PRESIDENT 의 이름은 XXX 입니다." 문장 생성.

<details><summary>정답</summary>

```sql
SELECT CONCAT('PRESIDENT 의 이름은 ', ename, ' 입니다.') AS msg
FROM   emp
WHERE  job = 'PRESIDENT';
```

`CONCAT(s1, s2, ...)` - 문자열 결합. MySQL 은 `||` 가 OR 라 SQL 표준 연결연산자 미지원. CONCAT 사용.

</details>

### Q10. (적용) 2008-02-18 과 2006-02-21 사이의 일 수 차이? 오늘로부터 EMP 의 HIREDATE 까지 얼마나 됐는지?

<details><summary>정답</summary>

```sql
-- 두 날짜 차이
SELECT DATEDIFF('2008-02-18', '2006-02-21');     -- 727

-- 오늘로부터 입사일까지 일 수
SELECT empno, ename, hiredate,
       DATEDIFF(CURDATE(), hiredate) AS days_employed
FROM   emp;
```

`DATEDIFF(d1, d2)` = d1 - d2 (일 단위 차이).

</details>

### Q11. (디버그) `COUNT(*)` 와 `COUNT(comm)` 이 14 vs 4 로 차이. 의미는?

<details><summary>정답</summary>

- `COUNT(*)` = 14 (전체 사원, NULL 포함)
- `COUNT(comm)` = 4 (comm 이 NULL 이 아닌 행만)

EMP 14명 중 SALESMAN 4명만 COMM 있고 나머지 10명은 NULL → `COUNT(comm) = 4`.

**유의**: 전체 행수 의도면 항상 `COUNT(*)`. 특정 컬럼 NULL 제외 카운트는 `COUNT(col)`.

</details>

### Q12. (디버그) 다음 두 쿼리 결과가 다른 이유는?

```sql
A: SELECT deptno FROM emp WHERE sal > 2000 GROUP BY deptno;
B: SELECT deptno FROM emp GROUP BY deptno HAVING MIN(sal) > 2000;
```

<details><summary>정답</summary>

**A**: 2000 초과 사원이 **한 명이라도 있는** 부서 (적어도 한 명).
**B**: **모든 사원** 이 2000 초과인 부서 (그룹 최솟값이 2000 초과).

예시:
- 부서 10: [800, 5000] → A: 포함 (5000 한 명), B: 미포함 (MIN=800)
- 부서 20: [2500, 3000] → A: 포함, B: 포함 (MIN=2500)

**WHERE 는 행 필터, HAVING 은 그룹 조건** 의 차이를 보여주는 클래식 예제.

</details>

### Q13. (개념) View 의 4가지 사용 이유와 한계 2가지?

<details><summary>정답</summary>

**사용 이유**:
1. **재사용·캡슐화** - 복잡한 SELECT 를 이름으로 부름
2. **보안·권한** - 민감 컬럼 (주민번호·연봉) 숨기고 노출 컬럼만
3. **추상화** - 스키마 변경을 View 안에서 흡수
4. **가독성** - 의미 있는 이름

**한계**:
1. **성능** - 매번 원본 쿼리 실행. Materialized View (MySQL 미지원) 아니면 캐싱 안 됨
2. **읽기 전용** - 복잡한 View (JOIN, 집계 포함) 는 INSERT/UPDATE/DELETE 불가

```sql
CREATE OR REPLACE VIEW dept_summary AS
SELECT d.deptno, d.dname, COUNT(e.empno) AS cnt, AVG(e.sal) AS avg_sal
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname;

SELECT * FROM dept_summary;
```

</details>

### Q14. (면접) "엑셀의 SUMIF·COUNTIF·피벗테이블이 SQL 의 무엇에 해당하는가?"

<details><summary>정답</summary>

| Excel | SQL |
|--|--|
| `SUMIF(range, criteria, sum_range)` | `SUM(col) ... WHERE ...` |
| `COUNTIF(range, criteria)` | `COUNT(*) ... WHERE ...` |
| `AVERAGEIFS` | `AVG(col) ... WHERE ...` |
| **피벗테이블 (행/열/값)** | `GROUP BY 행, 열 + 집계 함수` |
| 피벗 소계·총계 | **WITH ROLLUP** |
| VLOOKUP | **JOIN** |
| 셀 함수 (IF·UPPER·LEN) | **CASE·UPPER·CHAR_LENGTH** |

→ 엑셀로 100 만 행 처리하면 멈춤. SQL 은 1 억 행도 그대로. **선언적 SQL** 의 위력.

```sql
-- 엑셀 피벗 "행=부서, 열=직무, 값=평균급여"
SELECT deptno 부서, job 직무, ROUND(AVG(sal), 2) 평균
FROM   emp
GROUP BY deptno, job
ORDER BY deptno, job;
```

</details>
