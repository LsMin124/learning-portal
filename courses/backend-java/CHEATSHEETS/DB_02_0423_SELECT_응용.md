# SELECT 응용 — 치트시트

> 31p 슬라이드 · 집계·GROUP BY·HAVING·내장 함수·View. EMP/DEPT 스키마.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **집계 함수 5종**: COUNT / SUM / AVG / MIN / MAX (모두 NULL 제외, COUNT(*) 만 포함)
2. **WHERE = 행 필터, HAVING = 그룹 필터** (실행 순서 다름)
3. **GROUP BY 안 한 컬럼은 SELECT 에 못 둠** (집계 함수로 감싸거나 GROUP BY 에 추가)
4. **WITH ROLLUP** 으로 부분합·총계 한 번에
5. **`LENGTH` 는 바이트**, `CHAR_LENGTH` 는 문자 수 (UTF-8 한글 1자 = 3 bytes)
6. **View** = 자주 쓰는 SELECT 의 이름. 재사용 + 권한 분리, 단 성능·수정 한계

## 가장 중요한 코드 3개

```sql
-- (1) 부서별 통계
SELECT deptno, COUNT(*) AS 인원, ROUND(AVG(sal), 2) AS 평균
FROM   emp
GROUP BY deptno
HAVING AVG(sal) > 2000
ORDER BY deptno;

-- (2) WITH ROLLUP (부분합 + 총계)
SELECT IFNULL(d.dname, '총계') AS 부서, SUM(e.sal) AS 합계
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname WITH ROLLUP;

-- (3) View 정의
CREATE OR REPLACE VIEW dept_summary AS
SELECT d.deptno, d.dname, COUNT(e.empno) cnt, AVG(e.sal) avg_sal
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname;
```

## 면접 한 줄 답변
- **WHERE vs HAVING?** → WHERE 는 GROUP BY 이전 행 필터, HAVING 은 이후 그룹 필터. 집계 함수는 HAVING 만.
- **COUNT(*) vs COUNT(col) 차이?** → `*` 는 NULL 포함 모든 행, `col` 은 NULL 제외 행.
- **View 의 한계?** → 매번 원본 쿼리 실행 (캐싱 X) + 복잡 View 는 INSERT/UPDATE 불가.
- **SQL = 엑셀 피벗?** → GROUP BY = 피벗 행/열, 집계 = 값, WITH ROLLUP = 소계·총계.

---

# 2. Quick Reference (실무 복붙)

## 집계 함수 5종

| 함수 | NULL 처리 | 메모 |
|--|--|--|
| `COUNT(*)` | **포함** | 전체 행 수 |
| `COUNT(col)` | 제외 | col 이 NULL 아닌 행만 |
| `COUNT(DISTINCT col)` | 제외 + 중복 제거 | - |
| `SUM(col)` | 제외 | 숫자만 |
| `AVG(col)` | 제외 (분모도) | NULL 을 0 으로 안 침 |
| `MIN(col)` / `MAX(col)` | 제외 | 문자열·날짜 OK |

## GROUP BY

```sql
-- 단일 그룹
SELECT deptno, COUNT(*) FROM emp GROUP BY deptno;

-- 다중 그룹
SELECT deptno, job, AVG(sal) FROM emp GROUP BY deptno, job;

-- 표현식 그룹
SELECT YEAR(hiredate), COUNT(*) FROM emp GROUP BY YEAR(hiredate);

-- 함정: GROUP BY 없는 컬럼은 집계로 감싸야
SELECT ename, deptno FROM emp GROUP BY deptno;     -- X (ename 미정의)
SELECT MIN(ename), deptno FROM emp GROUP BY deptno; -- O
```

## HAVING

```sql
-- WHERE vs HAVING
SELECT deptno, AVG(sal)
FROM   emp
WHERE  sal > 1000          -- 1000 이상 행만 그룹화
GROUP BY deptno
HAVING AVG(sal) > 2500;    -- 그룹 평균이 2500 이상

-- A: 2000 초과 사원이 한 명이라도 있는 부서
SELECT deptno FROM emp WHERE sal > 2000 GROUP BY deptno;
-- B: 모든 사원이 2000 초과인 부서
SELECT deptno FROM emp GROUP BY deptno HAVING MIN(sal) > 2000;
```

## WITH ROLLUP

```sql
SELECT deptno, job, SUM(sal)
FROM   emp
GROUP BY deptno, job WITH ROLLUP;

-- 결과:
-- (10, CLERK, 1300)
-- (10, MANAGER, 2450)
-- (10, NULL, 8750)      <- 부서 10 소계
-- (20, ...)
-- (NULL, NULL, 29025)   <- 전체 총계

-- ROLLUP NULL vs 실제 NULL
SELECT GROUPING(deptno), deptno, SUM(sal) FROM emp
GROUP BY deptno WITH ROLLUP;
-- GROUPING() = 1 이면 ROLLUP NULL
```

## 내장 함수

```sql
-- 숫자
ROUND(1234.5678, 2)      -- 1234.57
ROUND(1234, -2)          -- 1200 (정수부 반올림)
CEIL(1.1)                -- 2
FLOOR(1.9)               -- 1
ABS(-5)                  -- 5
MOD(10, 3)               -- 1

-- 문자
CONCAT('A', 'B', 'C')                    -- ABC (MySQL 은 || X)
SUBSTR(ename, 1, 3)                      -- 1-base
LEFT(ename, 3) / RIGHT(ename, 3)
LENGTH('BOOTCAMP 김')                       -- 9 byte (UTF-8 한글 3B)
CHAR_LENGTH('BOOTCAMP 김')                  -- 7 자
UPPER(ename) / LOWER(ename)
TRIM(' x ')                               -- 'x'
REPLACE(ename, 'A', 'X')

-- 날짜
NOW() / CURDATE() / CURTIME()
DATEDIFF('2026-05-20', '2024-01-01')     -- 일 수 차이
DATE_ADD(hiredate, INTERVAL 1 YEAR)
YEAR(hiredate) / MONTH(hiredate) / DAY(hiredate)
DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')

-- NULL 처리
IFNULL(comm, 0)
COALESCE(a, b, c)
NULLIF(a, b)
IF(sal > 3000, '고액', '저액')           -- MySQL only
```

## View

```sql
-- 생성
CREATE OR REPLACE VIEW dept_summary AS
SELECT d.deptno, d.dname, COUNT(e.empno) AS cnt
FROM   dept d LEFT JOIN emp e ON d.deptno = e.deptno
GROUP BY d.deptno, d.dname;

-- 사용
SELECT * FROM dept_summary WHERE cnt > 3;

-- 삭제
DROP VIEW dept_summary;

-- 4 가지 이점
-- 1. 재사용 (복잡 쿼리 이름 짓기)
-- 2. 보안 (민감 컬럼 숨김)
-- 3. 추상화 (스키마 변경 흡수)
-- 4. 가독성

-- 2 가지 한계
-- 1. 성능 (매번 원본 쿼리, Materialized View 미지원)
-- 2. 복잡 View 는 INSERT/UPDATE/DELETE 불가
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `AVG(comm)` NULL 무시 14명 중 4명만 | `AVG(IFNULL(comm, 0))` 으로 14 분모 |
| GROUP BY 없는 컬럼 SELECT | 집계로 감싸거나 GROUP BY 추가 |
| `LENGTH` 한글 길이 제한 | `CHAR_LENGTH` 사용 |
| LEFT JOIN + COUNT(*) | `COUNT(o.id)` 로 NULL 제외 |
| ROLLUP NULL vs 실제 NULL | `GROUPING()` 함수 |
| View 가 느림 | Materialized View 불가 → 캐시 테이블 + 배치 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
SELECT 응용 (31p)
│
├── [A] 집계 함수 5종
│   ├── COUNT(*) / COUNT(col) / COUNT(DISTINCT)
│   ├── SUM / AVG (NULL 제외)
│   └── MIN / MAX
│
├── [B] GROUP BY
│   ├── 단일·다중·표현식 그룹
│   ├── 표준 SQL 위반 (ONLY_FULL_GROUP_BY)
│   └── ORDER BY 와의 조합
│
├── [C] HAVING
│   ├── WHERE vs HAVING (실행 순서)
│   ├── 집계 함수 조건
│   └── A (한 명이라도) vs B (모두) 패턴
│
├── [D] WITH ROLLUP
│   ├── 부분합·총계 자동
│   ├── ROLLUP NULL vs 실제 NULL
│   └── GROUPING() 함수
│
├── [E] 내장 함수
│   ├── 숫자 (ROUND·CEIL·FLOOR·ABS·MOD)
│   ├── 문자 (CONCAT·SUBSTR·LENGTH·CHAR_LENGTH·UPPER)
│   ├── 날짜 (NOW·DATEDIFF·DATE_ADD·DATE_FORMAT)
│   └── NULL (IFNULL·COALESCE·NULLIF·IF)
│
└── [F] View
    ├── 정의 (CREATE OR REPLACE)
    ├── 4 이점 (재사용·보안·추상화·가독성)
    └── 2 한계 (성능·수정 제약)
```

## 학습 진도 체크리스트

### A. 집계
- [ ] 5 함수의 NULL 처리 (COUNT(*) 만 포함)
- [ ] `AVG(comm)` 의 분모 함정 (IFNULL 로 해결)
- [ ] COUNT(*) vs COUNT(col) vs COUNT(DISTINCT)

### B. GROUP BY / HAVING
- [ ] 실행 순서상 WHERE → GROUP BY → HAVING
- [ ] GROUP BY 없는 컬럼 SELECT 금지
- [ ] WHERE 와 HAVING 선택 기준

### C. WITH ROLLUP
- [ ] 부분합·총계 자동 생성
- [ ] GROUPING() 으로 ROLLUP NULL 구분
- [ ] IFNULL 로 '총계' 라벨

### D. 내장 함수
- [ ] LENGTH vs CHAR_LENGTH (한글)
- [ ] SUBSTR 1-base
- [ ] DATEDIFF 일 단위 차이
- [ ] IFNULL / COALESCE / NULLIF

### E. View
- [ ] CREATE OR REPLACE VIEW
- [ ] 4 이점 + 2 한계
- [ ] Materialized View (MySQL 미지원)

## 연관 강의

```
1강 SELECT 기본    -> SELECT 7단계
2강 SELECT 응용    <- 현재 위치
3강 DDL/DML/TX     -> 테이블·트랜잭션
4강 JOIN/SubQuery  -> 여러 테이블 합치기
```

→ 다음 (DDL/DML) 에서 **테이블 만들고 데이터 바꾸기** 학습.
