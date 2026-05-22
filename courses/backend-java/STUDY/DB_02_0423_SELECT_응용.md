# SELECT 응용 - 집계 · 그룹 · 내장함수 · View

> **이 강의는 무엇인가**: 31페이지. 집계 함수(COUNT·SUM·AVG·MIN·MAX) + GROUP BY · HAVING · WITH ROLLUP + MySQL 내장함수(숫자·문자·날짜·논리) + View.
> **왜 배우는가**: "부서별 평균 연봉", "월별 매출", "고객 등급별 통계" - 비즈니스 보고서 90% 가 이걸로 만들어짐.

---

## 들어가기 전에

- **선수**: SELECT 기본 (1강 - DB_01).
- **스키마**: HR_CORP (EMP · DEPT · BONUS · SALGRADE).
- **마인드셋**: "여러 행 → 하나의 결과 값" 으로 축소하는 게 집계. 그룹화는 "어떤 기준으로 묶을 것인가".

---

## Part A. 집계 함수 (Aggregate Function)

### A-1. 집계 함수란

> 여러 행을 하나로 묶어서 **요약된 값**을 반환하는 함수.

별칭: **복수 행 함수**, **통계 함수**, **그룹 함수**.

사용 위치:
- 테이블 전체에 대해: `SELECT COUNT(*) FROM emp;`
- 그룹 단위에 대해: `SELECT deptno, COUNT(*) FROM emp GROUP BY deptno;`

### A-2. 5가지 핵심 집계 함수

| 함수 | 설명 |
|--|--|
| `COUNT(*)` | 행의 개수 (**NULL 포함**) |
| `COUNT(col)` | col 이 NULL 이 아닌 행의 개수 |
| `COUNT(DISTINCT col)` | col 의 고유값 개수 |
| `SUM(col)` | 숫자 컬럼의 합계 |
| `AVG(col)` | 숫자 컬럼의 평균 |
| `MIN(col)` / `MAX(col)` | 최솟값 / 최댓값 |

### A-3. 집계 함수의 4가지 특징

1. **NULL 무시** - 대부분의 집계 함수는 NULL 행을 제외 (단, `COUNT(*)` 는 포함)
2. **GROUP BY 와 함께 사용** - 없으면 전체 테이블이 하나의 그룹
3. **여러 행 → 하나의 값** - 결과는 항상 한 행씩 (또는 그룹당 한 행)
4. **WHERE vs HAVING**:
   - **WHERE**: 집계 **전에** 행 필터링
   - **HAVING**: 집계 **결과를** 필터링
5. **혼합 SELECT 규칙**: 집계 함수와 일반 컬럼을 함께 SELECT 하면, 일반 컬럼은 **반드시 GROUP BY 에 포함**

### A-4. 기본 사용 예제

**모든 사원의 사원수·급여총액·평균급여·최고급여·최저급여**:

```sql
SELECT COUNT(*)   사원수,
       SUM(sal)   급여총액,
       AVG(sal)   평균급여,
       MAX(sal)   최고급여,
       MIN(sal)   최저급여
FROM   emp;
```

| 사원수 | 급여총액 | 평균급여 | 최고급여 | 최저급여 |
|--|--|--|--|--|
| 14 | 29025 | 2073.21 | 5000 | 800 |

---

## Part B. GROUP BY

### B-1. GROUP BY 란

> 행들을 특정 기준으로 묶어서(그룹핑) 집계값을 계산하는 절.

⚠️ **그룹핑 한다고 정렬이 되는 것은 아님**. 정렬이 필요하면 `ORDER BY` 추가.

GROUP BY 절이 없으면 → 테이블 전체가 하나의 그룹.

### B-2. 다양한 사용 패턴

**학생별 평균 점수**:
```sql
SELECT student_id, AVG(score) AS avg_score
FROM   exam
GROUP BY student_id;
```

**다중 컬럼 그룹핑 (반/과목별 평균)**:
```sql
SELECT class_id, subject, AVG(score) AS avg_score
FROM   exam
GROUP BY class_id, subject;
```

**표현식으로 그룹핑 (일자별 주문 수)**:
```sql
SELECT DATE(created_at) AS order_date, COUNT(*) AS cnt
FROM   orders
GROUP BY DATE(created_at)
ORDER BY order_date;
```

### B-3. EMP 실습 - 부서별 통계

```sql
SELECT deptno                          부서,
       COUNT(*)                        사원수,
       SUM(sal)                        급여총액,
       ROUND(AVG(sal), 2)              평균급여,
       MAX(sal)                        최고급여,
       MIN(sal)                        최저급여
FROM   emp
GROUP BY deptno;
```

| 부서 | 사원수 | 급여총액 | 평균급여 | 최고급여 | 최저급여 |
|--|--|--|--|--|--|
| 10 | 3 | 8750  | 2916.67 | 5000 | 1300 |
| 20 | 5 | 10875 | 2175.00 | 3000 | 800  |
| 30 | 6 | 9400  | 1566.67 | 2850 | 950  |

**다중 그룹 - 부서별 + 직급별**:
```sql
SELECT deptno 부서, job 업무, COUNT(*) 사원수,
       SUM(sal) 급여총액, ROUND(AVG(sal),2) 평균급여,
       MAX(sal) 최고급여, MIN(sal) 최저급여
FROM   emp
GROUP BY deptno, job;
```

---

## Part C. HAVING

### C-1. WHERE vs HAVING

```
[원본 테이블]
     |
     v
1. WHERE       <-- 개별 행 필터링 (집계 전)
     |
     v
2. GROUP BY    <-- 그룹화
     |
     v
3. HAVING      <-- 그룹별 필터링 (집계 후)
     |
     v
4. SELECT      <-- 집계값 계산
     |
     v
5. ORDER BY
```

| 항목 | WHERE | HAVING |
|--|--|--|
| 적용 시점 | GROUP BY **이전** | GROUP BY **이후** |
| 대상 | 개별 행 | 집계 결과 (그룹) |
| 집계함수 사용 | ❌ 불가 | ✅ 가능 |
| 별칭 사용 | ❌ 불가 | ⚠️ MySQL 만 가능 (비표준) |

### C-2. HAVING 실습

**급여(커미션 포함) 평균이 2000 이상인 부서**:
```sql
SELECT deptno                                          부서번호,
       COUNT(*)                                        사원수,
       ROUND(AVG(sal + IFNULL(comm, 0)), 2)            "평균급여(커미션포함)"
FROM   emp
GROUP BY deptno
HAVING AVG(sal + IFNULL(comm, 0)) > 2000;
```

| 부서번호 | 사원수 | 평균급여(커미션포함) |
|--|--|--|
| 10 | 3 | 2916.67 |
| 20 | 5 | 2175.00 |

**반/과목별 평균 80 이상 + 응시자 10명 이상**:
```sql
SELECT class_id, subject,
       AVG(score) AS avg_score,
       COUNT(*)   AS n
FROM   exam
GROUP BY class_id, subject
HAVING AVG(score) >= 80 AND COUNT(*) >= 10;
```

### C-3. HAVING 단독 사용 (주의)

GROUP BY 없이 HAVING 단독 사용 가능 - 이때 **전체 테이블이 하나의 그룹**:
```sql
SELECT AVG(sal) FROM emp HAVING AVG(sal) > 2000;
-- 전체 평균이 2000 이상이면 반환, 아니면 빈 결과
```

용도가 제한적. 보통 WHERE + 집계함수 조합으로 처리.

---

## Part D. WITH ROLLUP

### D-1. WITH ROLLUP 이란

> GROUP BY 결과에 **소계(부분합)** 와 **총계(전체합)** 행을 자동 추가.

DBMS 마다 사용법이 조금씩 다름. MySQL 의 문법:

```sql
SELECT d.deptno, d.dname, SUM(e.sal) AS total_sal
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname WITH ROLLUP;
```

결과:

| DEPTNO | DNAME      | total_sal |
|--|--|--|
| 10 | ACCOUNTING | 8750 |
| 10 | NULL       | 8750  (← 10번 부서 소계) |
| 20 | RESEARCH   | 10875 |
| 20 | NULL       | 10875 (← 20번 부서 소계) |
| 30 | SALES      | 9400 |
| 30 | NULL       | 9400  (← 30번 부서 소계) |
| 40 | OPERATIONS | NULL |
| 40 | NULL       | NULL  (← 40번 부서 소계) |
| NULL | NULL     | 29025 (← 전체 총계) |

### D-2. GROUPING 함수

ROLLUP 으로 생긴 NULL 인지, 진짜 NULL 인지 구분:

```sql
SELECT IFNULL(d.dname, '총계') AS dept,
       GROUPING(d.deptno)      AS is_subtotal,
       SUM(e.sal)              AS total_sal
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname WITH ROLLUP;
```

`GROUPING()` 은 ROLLUP 이 만든 NULL 에 대해 1, 일반 행에선 0 반환.

---

## Part E. MySQL 내장 함수

### E-1. 숫자 관련 함수 (Numeric Functions)

| 함수 | 설명 |
|--|--|
| `ABS(숫자)` | 절댓값 |
| `CEIL(숫자)` / `CEILING(숫자)` | 올림 (값 이상 정수 중 최소) |
| `FLOOR(숫자)` | 내림 (값 이하 정수 중 최대) |
| `ROUND(숫자, 자릿수)` | 반올림 |
| `TRUNCATE(숫자, 자릿수)` | 버림 |
| `POW(X, Y)` | X 의 Y 제곱 |
| `MOD(X, Y)` | X 를 Y 로 나눈 나머지 |
| `GREATEST(n1, n2, ...)` | 최댓값 |
| `LEAST(n1, n2, ...)` | 최솟값 |

**FROM 절 없이도 사용 가능** (MySQL):
```sql
SELECT POW(2, 3);                              -- 8
SELECT MOD(8, 3);                              -- 2
SELECT GREATEST(4, 3, 7, 5, 9);                -- 9
SELECT ROUND(1526.159, 2);                     -- 1526.16
SELECT ROUND(1526.159, -2);                    -- 1500 (10의 자리 반올림)
```

### E-2. 문자 관련 함수 (String Functions)

| 함수 | 설명 |
|--|--|
| `CONCAT(s1, s2, ...)` | 문자열 결합 |
| `LENGTH(s)` | 문자열 길이 (**바이트**) |
| `CHAR_LENGTH(s)` | 문자열 길이 (**문자**) |
| `UPPER(s)` / `LOWER(s)` | 대/소문자 변환 |
| `TRIM(s)` | 양쪽 공백 제거 |
| `REPLACE(s, from, to)` | 치환 |
| `SUBSTR(s, pos, len)` | 부분 문자열 추출 |
| `INSTR(s, substr)` | 위치 반환 (1-based, 없으면 0) |
| `LPAD(s, len, pad)` / `RPAD(s, len, pad)` | 왼쪽/오른쪽 채우기 |
| `REPEAT(s, n)` | 반복 |
| `REVERSE(s)` | 뒤집기 |
| `ASCII(c)` | 아스키 코드 |

**예제**:
```sql
-- PRESIDENT 의 이름은 KING 입니다.
SELECT CONCAT('PRESIDENT 의 이름은 ', ename, ' 입니다.')
FROM   emp WHERE job = 'PRESIDENT';

-- 이름의 길이가 5인 직원
SELECT ename FROM emp WHERE LENGTH(ename) = 5;

-- '김학생' 의 길이
SELECT LENGTH('김학생'), CHAR_LENGTH('김학생');
--      9 (UTF-8 1글자=3바이트)         3

-- 이름 앞 3글자
SELECT SUBSTR(ename, 1, 3) FROM emp;

-- '*****BOOTCAMP', 'BOOTCAMP*****'
SELECT LPAD('BOOTCAMP', 10, '*'), RPAD('BOOTCAMP', 10, '*');

-- '!YFASS OLLEH'
SELECT REVERSE('HELLO BOOTCAMP!');
```

⚠️ **LENGTH vs CHAR_LENGTH**: 한글·이모지 등 multi-byte 문자는 둘이 다름. UTF-8 한글 1글자 = 3바이트.

### E-3. 날짜 관련 함수 (Date Functions)

| 함수 | 설명 |
|--|--|
| `NOW()` / `SYSDATE()` / `CURRENT_TIMESTAMP` | 현재 날짜+시간 |
| `CURDATE()` | 현재 날짜 |
| `CURTIME()` | 현재 시간 |
| `DATE(dt)` | datetime 에서 날짜만 |
| `YEAR(dt)` / `MONTH(dt)` / `DAY(dt)` | 연/월/일 추출 |
| `YEARWEEK(dt)` | 연도 + 주차 (예: 202207) |
| `DAYNAME(dt)` | 요일 이름 (예: Monday) |
| `ADDTIME(dt, time)` | 시간 더하기 |
| `DATEDIFF(d1, d2)` | 두 날짜 간 일 수 차이 |

**예제**:
```sql
-- 2초 더하기
SELECT ADDTIME('2022-02-13 17:29:21', '2');

-- 두 날짜 차이 (727일)
SELECT DATEDIFF('2008-02-18', '2006-02-21');

-- 오늘 정보
SELECT NOW(), DAY(NOW()), MONTH(NOW()), YEAR(NOW()), YEARWEEK(NOW());
```

### E-4. 기타 중요 함수 (Advanced)

| 함수 | 설명 |
|--|--|
| `BIN(n)` | 숫자의 이진 표현 |
| `CAST(value AS type)` | 형 변환 |
| `CONVERT(value, type)` | 형 변환 |
| `IF(cond, val_if_true, val_if_false)` | 삼항 연산자 |
| `IFNULL(expr, alt)` | expr 이 NULL 이면 alt |
| `NULLIF(e1, e2)` | e1==e2 이면 NULL, 아니면 e1 |
| `LAST_INSERT_ID()` | 직전 INSERT 의 AUTO_INCREMENT ID |

**예제**:
```sql
-- IFNULL: NULL 을 기본값으로
SELECT ename, IFNULL(comm, 0) FROM emp;

-- IF: 삼항
SELECT ename, IF(sal >= 3000, '고연봉', '저연봉') AS grade FROM emp;

-- CAST: 타입 변환
SELECT CAST('123' AS UNSIGNED);    -- 문자열 -> 정수

-- NULLIF: 0으로 나누기 방지
SELECT total / NULLIF(quantity, 0) AS unit_price FROM orders;
```

---

## Part F. View (Appendix)

### F-1. View 란

> **저장된 SELECT 문**. 실행 시점에 원본 테이블에서 데이터를 읽어와 **가상 테이블** 처럼 보여줌.

물리적으로 데이터를 저장하는 게 아니라 **SELECT 정의만 저장**. 매번 조회 시 실행.

### F-2. View 사용 이유

1. **재사용·캡슐화**: 복잡한 SELECT 를 한 번 정의해 이름으로 재사용
2. **보안·권한**: 민감 컬럼 (예: 주민번호·연봉) 제외하고 필요한 컬럼만 노출
3. **추상화**: 스키마 변경을 View 안에서 흡수 → 쿼리 안정성 ↑
4. **가독성**: `SELECT * FROM 영업사원_뷰` 이 `SELECT ... FROM emp WHERE job='SALESMAN'` 보다 명확

### F-3. View 기본 문법

```sql
-- 생성
CREATE VIEW salesman_v AS
SELECT empno, ename, job, sal, deptno
FROM   emp
WHERE  job = 'SALESMAN';

-- 교체 생성 (있으면 덮어쓰기)
CREATE OR REPLACE VIEW salesman_v AS
SELECT ...;

-- 사용 (일반 테이블처럼)
SELECT * FROM salesman_v WHERE sal >= 1500 ORDER BY sal DESC;

-- 삭제
DROP VIEW salesman_v;
```

### F-4. View 와 Index

- **View 는 데이터 저장 안 함** → 인덱스 효과는 원본 테이블 인덱스에 의존.
- **Materialized View** (다른 DBMS) - View 결과를 실제로 저장. 갱신 비용↑, 조회 속도↑. MySQL 은 미지원 (스케줄러로 직접 구현).

### F-5. View 의 한계

- 일반 View 는 **INSERT/UPDATE/DELETE 가능** 하지만 조건이 많음 (단일 테이블 기반, 집계 없음 등).
- 복잡한 View 는 **read-only**.
- View 위에 View 를 쌓으면 성능 저하 위험.

---

## 자주 빠지는 함정

- ❌ `SELECT dept, name, COUNT(*) FROM emp GROUP BY dept` → name 이 GROUP BY 에 없음 (표준 위반)
  ✅ `GROUP BY dept, name` 또는 name 제거
- ❌ `WHERE AVG(sal) > 2000` → WHERE 에서 집계 함수 불가
  ✅ `HAVING AVG(sal) > 2000`
- ❌ `COUNT(comm)` 으로 전체 행 수 의도 → comm NULL 인 행 제외
  ✅ `COUNT(*)`
- ❌ `LENGTH('김')` 가 1 이라 가정 → UTF-8 에선 3바이트
  ✅ 문자 수는 `CHAR_LENGTH`
- ❌ `SUM(sal + comm)` (comm NULL) → SUM 결과도 영향 받음
  ✅ `SUM(sal + IFNULL(comm, 0))`
- ❌ ROLLUP 의 NULL 을 일반 NULL 로 착각
  ✅ `GROUPING()` 함수로 구분
- ❌ View 가 항상 빠르다고 가정 → 매번 원본 쿼리 실행
  ✅ 자주 쓰이고 무겁다면 Materialized 패턴 (스케줄러+테이블) 검토
- ❌ `ORDER BY` 없이 GROUP BY 결과 사용 → 그룹핑은 정렬 보장 안 함
  ✅ 정렬 필요 시 `ORDER BY` 명시

---

## 자가점검

1. `COUNT(*)` 와 `COUNT(col)` 의 결과가 다른 경우는?
2. WHERE 와 HAVING 의 적용 순서·차이는?
3. `SELECT dept, AVG(salary) FROM emp` 만 쓰면 어떻게 되나?
4. WITH ROLLUP 결과에서 진짜 NULL 과 ROLLUP NULL 을 어떻게 구분?
5. `LENGTH('BOOTCAMP 김')` 의 결과는? (UTF-8 가정)
6. View 와 일반 테이블의 차이를 3가지 들으시오.

<details><summary>풀이</summary>

1. **col 에 NULL 이 있을 때**.
   `COUNT(*)` 는 NULL 행도 포함. `COUNT(col)` 은 NULL 행 제외.
   예: EMP 14명 중 SALESMAN 4명만 COMM 있고 나머지 10명은 NULL → `COUNT(*)` = 14, `COUNT(comm)` = 4.

2. **WHERE → GROUP BY → HAVING** 순.
   WHERE: 개별 행 필터 (집계 전). HAVING: 그룹 필터 (집계 후).
   집계 함수는 WHERE 에 못 쓰고 HAVING 에만 가능.

3. **표준 SQL 에선 에러**. SELECT 에 집계함수(`AVG`) 와 일반 컬럼(`dept`) 이 함께 있으면 일반 컬럼은 GROUP BY 에 있어야.
   MySQL 의 `ONLY_FULL_GROUP_BY` 모드가 켜져 있으면 에러, 아니면 임의의 dept 값 반환 (예측 불가).

4. **`GROUPING(col)` 함수**.
   ROLLUP 이 만든 NULL → `GROUPING(col) = 1`
   일반 데이터의 NULL → `GROUPING(col) = 0`

5. `LENGTH('BOOTCAMP 김')` = **9** (S·S·A·F·Y·공백 = 6바이트, 김 = 3바이트).
   `CHAR_LENGTH('BOOTCAMP 김')` = **7** (글자 수).

6. (1) **데이터 저장 X** - View 는 SELECT 정의만 저장.
   (2) **권한 제어** - View 로 노출 컬럼·행 제한 가능.
   (3) **읽기 전용에 가까움** - 복잡한 View 는 INSERT/UPDATE/DELETE 불가.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.3 표지·TOC·학습목표 | 들어가기 전에 |
| p.4 ~ p.7 집계 함수 정의·종류·특징 | §Part A |
| p.8 ~ p.10 SELECT 문법·실행순서·GROUP BY | §Part B |
| p.11 HAVING | §Part C |
| p.12 WITH ROLLUP | §Part D |
| p.13 ~ p.15 집계 실습 (부서별·HAVING) | §Part A·B·C |
| p.16 ~ p.26 MySQL 내장함수 (숫자·문자·날짜·기타) | §Part E |
| p.27 ~ p.30 Appendix - View | §Part F |
| p.31 마무리 | (생략) |

_31p 전체 + EMP/DEPT 스키마 일관 적용._
