# DDL & DML - 테이블 만들기 · 데이터 바꾸기 · 트랜잭션

> **이 강의는 무엇인가**: 29페이지. Data Type 종류 + DDL(CREATE/ALTER/DROP) + DML(INSERT/UPDATE/DELETE) + Transaction (COMMIT/ROLLBACK).
> **왜 배우는가**: SELECT 만으론 부족. 실제 앱은 **만들고 바꾸고 지우는** 작업이 절반. 제약조건은 데이터 무결성의 첫 방패, 트랜잭션은 "전부 성공 or 전부 실패" 보장.

---

## 들어가기 전에

- **선수**: SELECT 기본·응용 (1·2강).
- **마인드셋**: SELECT = 데이터 보기, DDL = 그릇 만들기, DML = 그릇에 데이터 채우기/바꾸기, TCL = 변경을 안전하게 묶기.
- **실습 스키마**: member (교육생 정보 테이블).

---

## Part A. Data Type (자료형)

### A-1. 숫자형 (Numeric)

| 데이터유형 | 크기(Byte) | 범위 |
|--|--|--|
| `TINYINT` | 1 | signed -128 ~ 127, unsigned 0 ~ 255 |
| `BOOL` / `BOOLEAN` | 1 | TINYINT(1) 의 동의어. 0=false, 그 외=true |
| `SMALLINT` | 2 | signed -32,768 ~ 32,767 |
| `MEDIUMINT` | 3 | signed -8,388,608 ~ 8,388,607 |
| `INT` / `INTEGER` | 4 | signed -2,147,483,648 ~ 2,147,483,647 |
| `BIGINT` | 8 | signed -9,223,372,036,854,775,808 ~ 9,223,372,036,854,775,807 |
| `DOUBLE` | 8 | 부동 소수점 약 -1.79E+308 ~ 1.79E+308 |
| `DECIMAL(M, D)` | M+1 | 고정 소수점. M=전체자릿수(precision), D=소수점 이하 자릿수(scale) |

**DECIMAL 예제**:
- `DECIMAL(5)` → -99999 ~ 99999
- `DECIMAL(5, 1)` → -9999.9 ~ 9999.9
- `DECIMAL(5, 2)` → -999.99 ~ 999.99

⚠️ **금액엔 DECIMAL**. FLOAT/DOUBLE 은 부동소수점이라 `0.1 + 0.2 != 0.3` 같은 오차 발생.

### A-2. 문자형 (String)

| 데이터유형 | 정의 | 최대 길이 |
|--|--|--|
| `CHAR(M)` | 고정 길이 문자열 | M = 0 ~ 255 문자 |
| `VARCHAR(M)` | 가변 길이 문자열 | M = 0 ~ 65,535 문자 |
| `TINYTEXT` | 소량 텍스트 | 최대 255 문자 |
| `TEXT` | 일반 텍스트 | 최대 65,535 문자 |
| `MEDIUMTEXT` | 중간 크기 텍스트 | 최대 16,777,215 문자 |
| `LONGTEXT` | 대용량 텍스트 | 최대 4,294,967,295 문자 |
| `ENUM('v1', 'v2', ...)` | 정해진 값 중 하나 | 최대 65,535 개의 요소 |
| `SET('v1', 'v2', ...)` | 여러 값 선택 가능 | 최대 64 개의 구성원 |

**CHAR vs VARCHAR**:
- `CHAR(10)`: "abc" 저장 시 → "abc       " (공백 패딩), 항상 10 바이트
- `VARCHAR(10)`: "abc" 저장 시 → "abc" + 길이 정보 (3 + 1 바이트)
- CHAR: 길이 일정 (예: 우편번호·전화번호), 인덱스 효율
- VARCHAR: 가변 길이 (이름·이메일), 공간 절약

### A-3. 날짜·시간형 (Date and Time)

| 데이터유형 | 크기 | 형식 / 범위 |
|--|--|--|
| `DATE` | 3 byte | YYYY-MM-DD ('1000-01-01' ~ '9999-12-31') |
| `TIME` | 가변 | HH:MM:SS ('-838:59:59' ~ '838:59:59') |
| `DATETIME` | 가변 | YYYY-MM-DD HH:MM:SS ('1000-01-01 00:00:00' ~ '9999-12-31 23:59:59') |
| `TIMESTAMP` | 가변 | '1970-01-01 00:00:01' UTC ~ '2038-01-19 03:14:07' UTC |
| `YEAR` | 1 byte | 1901 ~ 2155 |

**DATETIME vs TIMESTAMP**:
- DATETIME: 시간대 변환 없이 그대로 저장
- TIMESTAMP: UTC 로 저장, 조회 시 세션 시간대로 변환 → 시차 다른 사용자에게 자동 조정
- 2038 년 문제 (Y2K38) → BIGINT TIMESTAMP 또는 DATETIME 권장

### A-4. BINARY · BLOB

| 데이터유형 | 정의 |
|--|--|
| `BINARY(M)` | CHAR 와 유사, 이진 데이터. M 바이트 단위 |
| `VARBINARY(M)` | VARCHAR 와 유사, 이진 데이터 |
| `TINYBLOB` | 최대 255 byte |
| `BLOB` | 최대 65,535 byte |
| `MEDIUMBLOB` | 최대 16,777,215 byte |
| `LONGBLOB` | 최대 4,294,967,295 byte |

**BLOB (Binary Large Object)**: 이미지·동영상·PDF 등 이진 데이터 저장. 실무에선 보통 **S3 같은 객체 스토리지에 URL 만 DB 에 저장** (성능·비용 효율).

---

## Part B. DDL (Data Definition Language)

### B-1. DDL 개요

> 데이터베이스 객체 (DB · TABLE · VIEW · INDEX) 의 **구조** 를 정의·수정·삭제.

| 명령 | 용도 |
|--|--|
| `CREATE` | 객체 생성 |
| `ALTER` | 객체 수정 |
| `DROP` | 객체 삭제 |
| `RENAME` | 객체 이름 변경 |
| `TRUNCATE` | 테이블의 모든 데이터 삭제 (DDL, 자동 COMMIT) |

### B-2. 데이터베이스 (DB) 관리

```sql
-- 생성
CREATE DATABASE study_db;
CREATE DATABASE study_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 확인
SHOW DATABASES;

-- 수정 (문자집합·정렬·암호화·읽기전용 등)
ALTER DATABASE study_db DEFAULT CHARACTER SET utf8mb4;

-- 삭제
DROP DATABASE study_db;
DROP DATABASE IF EXISTS study_db;   -- 없어도 에러 안 남

-- 사용 선택
USE study_db;
```

**Character Set vs Collation**:
- **Character Set (문자집합)**: 컴퓨터가 문자를 어떤 코드로 저장하는지 규칙 (`utf8mb4` 권장 - 이모지 지원)
- **Collation**: 비교·정렬 규칙 (`utf8mb4_unicode_ci` = 대소문자 구분 안 함)

### B-3. 테이블 (TABLE) 생성

```sql
CREATE TABLE table_name (
    column1 datatype [options],
    column2 datatype,
    column3 datatype,
    ...
);
```

**실습 - member 테이블**:
```sql
CREATE TABLE member (
    user_num      INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id       VARCHAR(20)  NOT NULL,
    user_name     VARCHAR(20)  NOT NULL,
    user_password VARCHAR(20)  NOT NULL,
    user_email    VARCHAR(30),
    signup_date   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### B-4. 제약 조건 (Constraint) 6가지

| 제약사항 | 설명 |
|--|--|
| **NOT NULL** | 해당 컬럼은 반드시 값을 가져야 함. NULL 금지 |
| **UNIQUE** | 컬럼에 중복 값 불가. **NULL 은 허용** (여러 NULL 가능) |
| **PRIMARY KEY** | 기본키. 중복 불가 + NULL 불가. 테이블당 1개 |
| **FOREIGN KEY** | 외래키. 다른 테이블의 PK 참조 (참조 무결성). NULL 허용 |
| **DEFAULT** | 입력 누락 시 기본값 |
| **CHECK** | 값의 범위·종류 검증 (MySQL 8.0+) |

**PRIMARY KEY 작성 방식 3가지**:
```sql
-- 컬럼 옆에 인라인
CREATE TABLE t1 (id INT PRIMARY KEY, name VARCHAR(20));

-- 테이블 레벨
CREATE TABLE t2 (id INT, name VARCHAR(20), PRIMARY KEY(id));

-- 복합 키 (테이블 레벨로만 가능)
CREATE TABLE t3 (a INT, b INT, name VARCHAR(20), PRIMARY KEY(a, b));
```

**FOREIGN KEY 예제**:
```sql
CREATE TABLE board (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    title      VARCHAR(100) NOT NULL,
    writer_id  INT          NOT NULL,
    FOREIGN KEY (writer_id) REFERENCES member(user_num)
        ON DELETE CASCADE       -- 부모 삭제 시 자식도 삭제
        ON UPDATE CASCADE       -- 부모 갱신 시 자식도 갱신
);
```

ON DELETE / ON UPDATE 옵션:
- `CASCADE`: 함께 삭제·수정
- `SET NULL`: NULL 로 설정
- `RESTRICT` / `NO ACTION`: 자식이 있으면 부모 삭제·수정 거부 (기본)

### B-5. 테이블 스키마 확인

```sql
DESCRIBE member;    -- 또는 DESC member;
SHOW CREATE TABLE member;  -- 생성 DDL 전체 확인
SHOW TABLES;            -- DB 안 모든 테이블 목록
```

DESC 결과:

| Field | Type | Null | Key | Default | Extra |
|--|--|--|--|--|--|
| user_num | int | NO | PRI | NULL | auto_increment |
| user_id | varchar(20) | NO |  | NULL |  |
| user_name | varchar(20) | NO |  | NULL |  |
| user_password | varchar(20) | NO |  | NULL |  |
| user_email | varchar(30) | YES |  | NULL |  |
| signup_date | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### B-6. ALTER TABLE - 테이블 수정

```sql
-- 컬럼 추가
ALTER TABLE member ADD COLUMN age INT;

-- 컬럼 타입 변경
ALTER TABLE member MODIFY COLUMN user_email VARCHAR(50);

-- 컬럼 이름 + 타입 변경
ALTER TABLE member CHANGE user_email email VARCHAR(50);

-- 컬럼 삭제
ALTER TABLE member DROP COLUMN age;

-- 제약조건 추가
ALTER TABLE member ADD CONSTRAINT uq_email UNIQUE(user_email);

-- 제약조건 삭제
ALTER TABLE member DROP INDEX uq_email;
```

### B-7. DROP vs TRUNCATE vs DELETE

| 명령 | 종류 | 구조 | 데이터 | 속도 | 트랜잭션 |
|--|--|--|--|--|--|
| `DROP TABLE` | DDL | 삭제 | 삭제 | 빠름 | 자동 커밋 |
| `TRUNCATE TABLE` | DDL | 유지 | 모두 삭제 | 빠름 | 자동 커밋, **AUTO_INCREMENT 리셋** |
| `DELETE FROM` | DML | 유지 | WHERE 조건 행만 | 느림 (행마다 로그) | **ROLLBACK 가능** |

→ "테이블 비우기" 가 의도면 TRUNCATE, "조건 행만 삭제" 면 DELETE.

---

## Part C. DML (Data Manipulation Language)

### C-1. DML 개요

> 테이블의 **데이터** 를 조작 (CRUD).

| 명령 | CRUD | 설명 |
|--|--|--|
| `INSERT` | C | 새 레코드 삽입 |
| `SELECT` | R | 레코드 조회 (1~2강) |
| `UPDATE` | U | 레코드 수정 |
| `DELETE` | D | 레코드 삭제 |

### C-2. INSERT

```sql
-- 방법 1: 모든 컬럼 (컬럼명 생략, 순서대로)
INSERT INTO member
VALUES (1, 'godqhr', '양명균', '1234', 'godqhr@gmail.com', NOW());

-- 방법 2: 원하는 컬럼만
INSERT INTO member (user_id, user_name, user_password)
VALUES ('kimstudent', '김학생', '1q2w3e4r!@');

-- 방법 3: 여러 행 한 번에
INSERT INTO member (user_id, user_name, user_password) VALUES
    ('leestudent', '이학생', '0000'),
    ('parkstudent', '박학생', '1111'),
    ('5student', '오학생', '2222');
```

**자동 처리 컬럼**:
- `NULL` 허용 컬럼: 명시 안 하면 NULL
- `DEFAULT` 있는 컬럼: 기본값 적용 (signup_date = NOW())
- `AUTO_INCREMENT`: 다음 시퀀스 번호 자동 부여

⚠️ **INSERT 시 주의**:
- 컬럼 이름과 VALUES 순서가 일치해야
- NOT NULL 컬럼은 값 또는 DEFAULT 필요
- FK 위반 시 에러

### C-3. UPDATE

```sql
UPDATE table_name
SET    col1 = value1, col2 = value2, ...
[WHERE where_condition];
```

**예제**:
```sql
-- 모든 레코드의 이름을 'anonymous' 로 수정 (전체!)
UPDATE member SET user_name = 'anonymous';

-- user_num = 3 인 학생 비밀번호만 변경
UPDATE member
SET    user_password = '1234'
WHERE  user_num = 3;

-- 여러 컬럼 동시 변경 + 표현식
UPDATE emp
SET    sal  = sal * 1.1,
       comm = IFNULL(comm, 0) + 100
WHERE  deptno = 30;
```

⚠️ **WHERE 생략 = 전체 행 수정**. **MySQL Workbench 의 Safe Mode** 가 켜져 있으면 PK 없는 WHERE 의 UPDATE/DELETE 를 막아줌.

설정 해제:
```sql
SET SQL_SAFE_UPDATES = 0;
```

또는 Edit → Preferences → SQL Editor → "Safe Updates" 체크 해제 (재접속 필요).

### C-4. DELETE

```sql
DELETE FROM tbl_name
[WHERE where_condition];
```

**예제**:
```sql
-- user_num = 4 인 사용자 삭제
DELETE FROM member WHERE user_num = 4;

-- 1년 이상 미접속자 삭제
DELETE FROM member
WHERE  last_login < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- 전체 삭제 (TRUNCATE 가 더 빠름)
DELETE FROM member;
```

⚠️ **WHERE 생략 = 모든 행 삭제**. UPDATE 와 동일하게 Safe Mode 가 막아줌.

**복구 가능?**
- DELETE: 트랜잭션 안에서 실행했으면 ROLLBACK 가능
- TRUNCATE: ROLLBACK 불가 (DDL, 자동 커밋)
- DROP: ROLLBACK 불가
- → 운영에선 항상 백업 → 작업 → 검증 → 커밋.

---

## Part D. Transaction (TCL)

### D-1. 트랜잭션이란

> 커밋(Commit) 하거나 롤백(Rollback) 할 수 있는 **가장 작은 작업 단위**.

여러 SQL 을 묶어 **"전부 성공 or 전부 실패"** 를 보장.

### D-2. ACID 속성

| 속성 | 설명 |
|--|--|
| **Atomicity (원자성)** | 트랜잭션 안의 모든 작업은 **전부 실행 or 전부 취소** |
| **Consistency (일관성)** | 트랜잭션 전후 DB 가 **일관된 상태** 유지 (제약조건 위반 X) |
| **Isolation (격리성)** | 동시 실행 트랜잭션이 **서로 영향 X** (또는 격리 수준에 따라 제어) |
| **Durability (지속성)** | COMMIT 된 변경은 **장애 발생해도 유지** |

### D-3. 기본 명령

| 명령 | 설명 |
|--|--|
| `START TRANSACTION` | 트랜잭션 시작 (COMMIT 또는 ROLLBACK 전까지의 SQL 묶음) |
| `COMMIT` | 변경사항을 **영구 반영** |
| `ROLLBACK` | START TRANSACTION 직후 상태로 **되돌림** |

⚠️ **MySQL 기본은 Auto Commit** (모든 SQL 이 즉시 커밋). 트랜잭션 묶음을 쓰려면 명시적 `START TRANSACTION`.

### D-4. COMMIT 예제

```sql
USE study;
CREATE TABLE test_table (val VARCHAR(20));

START TRANSACTION;
    INSERT INTO test_table VALUES ('S');
    INSERT INTO test_table VALUES ('A');
    INSERT INTO test_table VALUES ('F');
    INSERT INTO test_table VALUES ('Y');
COMMIT;

SELECT * FROM test_table;
-- S, A, F, Y 모두 보임 (영구 저장)
```

### D-5. ROLLBACK 예제

```sql
START TRANSACTION;
    INSERT INTO test_table VALUES ('A');
    INSERT INTO test_table VALUES ('B');
    INSERT INTO test_table VALUES ('C');
    INSERT INTO test_table VALUES ('D');
ROLLBACK;

SELECT * FROM test_table;
-- 위 4개 INSERT 가 모두 취소되어 보이지 않음
```

### D-6. 실전 시나리오 - 계좌 이체

```sql
START TRANSACTION;

-- 1. A 의 잔액에서 1000 차감
UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';

-- 2. B 의 잔액에 1000 추가
UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';

-- 두 작업 모두 성공해야 함
COMMIT;
-- 한쪽이 실패하면 ROLLBACK
```

**왜 트랜잭션 없이는 위험한가**:
- 1번 성공 → 2번 실패 (네트워크 끊김·서버 다운) → A 만 잃음, B 안 들어옴 = 데이터 부정합

### D-7. SAVEPOINT (부분 롤백)

```sql
START TRANSACTION;

INSERT INTO test VALUES ('A');
SAVEPOINT sp1;

INSERT INTO test VALUES ('B');
INSERT INTO test VALUES ('C');
ROLLBACK TO sp1;        -- B, C 만 취소 (A 는 남음)

INSERT INTO test VALUES ('D');
COMMIT;                  -- 결과: A, D
```

---

## 자주 빠지는 함정

- ❌ `FLOAT` / `DOUBLE` 로 금액 저장 → 부동소수점 오차
  ✅ `DECIMAL(10, 2)` 사용
- ❌ `VARCHAR(10)` 에 한글 10자 저장 시도 → 옛 MySQL 에선 바이트 단위라 실패
  ✅ MySQL 5.0+ 부턴 문자 단위. `utf8mb4` 설정
- ❌ `UPDATE/DELETE` 에 WHERE 생략 → 전체 행 변경/삭제
  ✅ Safe Mode 켜기 + WHERE 항상 확인 + 트랜잭션 안에서
- ❌ FK 있는 테이블의 DROP → 에러
  ✅ 자식 테이블 먼저 DROP 또는 `SET FOREIGN_KEY_CHECKS = 0;`
- ❌ 운영 DB 에서 `TRUNCATE` 후 ROLLBACK 시도 → 불가능
  ✅ DELETE 로 트랜잭션 안에서 실행
- ❌ AUTO_INCREMENT 컬럼에 INSERT 시 값 명시 → 시퀀스 꼬임
  ✅ DEFAULT 또는 컬럼 생략
- ❌ TIMESTAMP 의 2038 년 문제 무시 → 미래 데이터 처리 시 실패
  ✅ DATETIME 또는 BIGINT timestamp 사용
- ❌ 트랜잭션 없이 여러 UPDATE → 중간 실패 시 데이터 부정합
  ✅ `START TRANSACTION` ~ `COMMIT` 으로 묶기

---

## 자가점검

1. CHAR(10) 과 VARCHAR(10) 의 저장 방식 차이는?
2. `UPDATE member SET user_password = '1234'` 의 결과는?
3. PRIMARY KEY 와 UNIQUE 의 차이를 3가지 들으시오.
4. TRUNCATE 와 DELETE 의 차이를 트랜잭션·속도·AUTO_INCREMENT 관점에서.
5. ROLLBACK 이 안 되는 명령 3가지?
6. ACID 의 A 와 C 의 차이는?

<details><summary>풀이</summary>

1. - CHAR(10) "abc" → "abc       " (공백 7개 패딩). 항상 10 바이트 고정.
   - VARCHAR(10) "abc" → "abc" + 길이 정보 (3 + 1 바이트). 가변.
   - CHAR: 길이 일정 시 빠름. VARCHAR: 공간 절약.

2. **모든 member 의 user_password 가 '1234' 로 변경** (WHERE 생략 = 전체).
   Safe Mode 가 켜져 있으면 에러. 운영에선 절대 안 됨.

3. (1) **개수**: PK 는 테이블당 1개, UNIQUE 는 여러 개 가능
   (2) **NULL**: PK 는 NULL 불가, UNIQUE 는 NULL 허용 (여러 NULL 가능)
   (3) **인덱스**: PK 는 클러스터형 인덱스 자동, UNIQUE 는 보조 인덱스

4. | 항목 | TRUNCATE | DELETE |
   |--|--|--|
   | 종류 | DDL | DML |
   | 트랜잭션 | ROLLBACK 불가 (자동 커밋) | ROLLBACK 가능 |
   | 속도 | 빠름 (메타데이터만) | 느림 (행마다 로그) |
   | AUTO_INCREMENT | **리셋** | 유지 |
   | WHERE | 불가 | 가능 |

5. **DDL 모두**:
   - `DROP TABLE` (테이블 삭제)
   - `TRUNCATE TABLE` (모든 행 삭제)
   - `ALTER TABLE` (구조 변경)
   - `CREATE TABLE` (생성)
   → DDL 은 실행 즉시 자동 커밋되어 ROLLBACK 안 됨.

6. - **A (Atomicity, 원자성)**: 트랜잭션 안의 모든 작업이 **전부 성공 or 전부 실패**. 부분 성공 없음.
   - **C (Consistency, 일관성)**: 트랜잭션 전후 DB 가 **일관된 상태** 유지. 제약조건 (PK/FK/CHECK) 위반 시 자동 ROLLBACK.
   - A 는 "작업의 완전성", C 는 "상태의 유효성" 에 초점.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.3 표지·TOC·학습목표 | 들어가기 전에 |
| p.4 ~ p.8 Data Type (숫자·문자·날짜·BLOB) | §Part A |
| p.9 ~ p.13 DDL - DB 생성/수정/삭제 | §Part B-1, B-2 |
| p.14 ~ p.17 DDL - TABLE 생성·제약조건·DESC | §Part B-3, B-4, B-5 |
| p.18 ~ p.21 DML - INSERT | §Part C-1, C-2 |
| p.22 ~ p.24 DML - UPDATE | §Part C-3 |
| p.25 DML - DELETE | §Part C-4 |
| p.26 ~ p.28 Transaction (COMMIT/ROLLBACK) | §Part D |
| p.29 마무리 | (생략) |

_29p 전체 + ALTER TABLE·SAVEPOINT·ACID 등 슬라이드 외 실무 보강._
