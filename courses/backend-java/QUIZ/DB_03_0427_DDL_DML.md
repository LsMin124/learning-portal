# DDL / DML / Transaction - 퀴즈

> 14문항. 개념·적용·디버그·면접. member 스키마 기준.

---

### Q1. (개념) 금액 저장에 `FLOAT/DOUBLE` 대신 `DECIMAL` 을 쓰는 이유와 `DECIMAL(10, 2)` 의 의미?

<details><summary>정답</summary>

**이유**: FLOAT/DOUBLE 은 IEEE 754 부동소수점이라 **정확하지 않음**.
- `0.1 + 0.2 = 0.30000000000000004` (자바·MySQL 모두 동일)
- 금액 1억 행 합산 시 수십 ~ 수백 원 오차 누적

**DECIMAL(M, D)**: 고정 소수점.
- `M` = 전체 자릿수 (precision)
- `D` = 소수점 이하 자릿수 (scale)

예시:
- `DECIMAL(10, 2)` → 정수부 8자리 + 소수부 2자리 → 최대 `99999999.99`
- `DECIMAL(5)` → -99999 ~ 99999 (소수 없음)
- `DECIMAL(5, 1)` → -9999.9 ~ 9999.9

```sql
CREATE TABLE payment (
    id      INT PRIMARY KEY,
    amount  DECIMAL(15, 2) NOT NULL    -- 13자리 원 + 2자리 (전·후)
);
```

→ **금액·환율·이자율은 무조건 DECIMAL**. FLOAT 는 과학 계산용.

</details>

### Q2. (개념) `CHAR(10)` 과 `VARCHAR(10)` 의 저장 방식 차이와 각각의 적합한 용도?

<details><summary>정답</summary>

| | CHAR(10) | VARCHAR(10) |
|--|--|--|
| 저장 | "abc" → "abc       " (공백 7개 패딩) | "abc" + 길이 정보 (3 + 1 바이트) |
| 크기 | 항상 10 바이트 고정 | 가변 (실제 길이 + 1~2 바이트) |
| 속도 | 길이 일정 → 인덱스·정렬 빠름 | 약간 느림 |
| 공간 | 짧은 값엔 낭비 | 절약 |

**적합한 용도**:
- **CHAR**: 길이가 거의 일정한 코드 - 우편번호 (5자리), 국가코드 ('KR'), 성별 ('M'/'F'), MD5 해시 (32자리)
- **VARCHAR**: 가변 길이 - 이름, 이메일, URL, 게시글 제목

`member` 의 `user_id VARCHAR(20)` 은 사용자 ID 길이가 4 ~ 20 자로 가변이라 VARCHAR 선택.

</details>

### Q3. (개념) `DATETIME` 과 `TIMESTAMP` 의 차이 + 2038년 문제는 무엇?

<details><summary>정답</summary>

| | DATETIME | TIMESTAMP |
|--|--|--|
| 범위 | '1000-01-01' ~ '9999-12-31' | '1970-01-01' ~ '2038-01-19' UTC |
| 저장 | 입력된 그대로 | UTC 로 변환 저장 |
| 조회 | 그대로 출력 | 세션 시간대로 자동 변환 |
| 시간대 | 무시 | 자동 보정 |
| 크기 | 8 byte | 4 byte |

**TIMESTAMP 장점**: 글로벌 서비스에서 한국 사용자엔 KST, 미국 사용자엔 EST 로 자동 보정.
**TIMESTAMP 단점**: **2038년 1월 19일 03:14:07 UTC** 에 32-bit 정수 오버플로 발생 (Y2K38 문제).

→ 2038 이후의 시간이 필요하면 (예: 50년 만기 적금) **DATETIME 사용**.
→ member 의 `signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP` 는 가입 시점이라 2038 이전 사용 가정.

</details>

### Q4. (개념) MySQL 의 6가지 제약 조건 (Constraint) 을 모두 정리.

<details><summary>정답</summary>

| 제약 | 설명 | NULL 허용 | 개수 |
|--|--|--|--|
| **NOT NULL** | 반드시 값 필요 | 불가 | 컬럼당 |
| **UNIQUE** | 중복 불가 | **가능** (여러 NULL 가능) | 테이블당 여러 개 |
| **PRIMARY KEY** | 기본키 (UNIQUE + NOT NULL) | 불가 | 테이블당 **1개** |
| **FOREIGN KEY** | 다른 테이블의 PK 참조 | 가능 | 여러 개 |
| **DEFAULT** | 기본값 (입력 누락 시) | (값 있음) | - |
| **CHECK** | 값 범위 검증 (MySQL 8.0+) | 가능 | 여러 개 |

```sql
CREATE TABLE member (
    user_num      INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id       VARCHAR(20)  NOT NULL UNIQUE,
    user_name     VARCHAR(20)  NOT NULL,
    user_password VARCHAR(20)  NOT NULL,
    user_email    VARCHAR(30)  CHECK (user_email LIKE '%@%'),
    age           INT          DEFAULT 0,
    signup_date   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

</details>

### Q5. (개념) PRIMARY KEY 와 UNIQUE 의 차이 3가지?

<details><summary>정답</summary>

| 구분 | PRIMARY KEY | UNIQUE |
|--|--|--|
| **개수** | 테이블당 1개 | 여러 개 가능 |
| **NULL** | 불가 | 허용 (여러 NULL 가능) |
| **인덱스** | 클러스터형 (데이터 자체 정렬) | 보조 인덱스 |

추가:
- PK 는 행을 **유일하게 식별** 하는 메인 키. FK 가 참조하는 대상.
- UNIQUE 는 "이메일은 중복되면 안 됨" 처럼 비즈니스 규칙.
- MS SQL Server 만 UNIQUE 에 NULL 1개만 허용 (표준에선 여러 개).

```sql
CREATE TABLE member (
    user_num   INT PRIMARY KEY,         -- 유일 식별자
    user_id    VARCHAR(20) UNIQUE,      -- 로그인 ID (중복 X, NULL 가능)
    user_email VARCHAR(30) UNIQUE       -- 이메일 (중복 X, NULL 가능)
);
```

</details>

### Q6. (적용) member 테이블을 PK·NOT NULL·DEFAULT CURRENT_TIMESTAMP 포함하여 CREATE.

<details><summary>정답</summary>

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

PRIMARY KEY 작성 3가지 방식:
```sql
-- (1) 인라인
user_num INT PRIMARY KEY,

-- (2) 테이블 레벨 (복합키 가능)
PRIMARY KEY (user_num)

-- (3) ALTER 로 나중에 추가
ALTER TABLE member ADD PRIMARY KEY (user_num);
```

`AUTO_INCREMENT` 는 PK 컬럼에만 사용 (보통 1개 INT/BIGINT).

</details>

### Q7. (적용) INSERT 3가지 방법으로 member 에 데이터 입력.

<details><summary>정답</summary>

```sql
-- 방법 1: 모든 컬럼 (순서대로, 컬럼명 생략)
INSERT INTO member
VALUES (1, 'godqhr', '양명균', '1234', 'godqhr@gmail.com', NOW());

-- 방법 2: 원하는 컬럼만 (AUTO_INCREMENT·DEFAULT 컬럼 생략 가능)
INSERT INTO member (user_id, user_name, user_password)
VALUES ('kimstudent', '김학생', '1q2w3e4r!@');

-- 방법 3: 여러 행 한 번에 (성능↑, 트랜잭션 1개)
INSERT INTO member (user_id, user_name, user_password) VALUES
    ('leestudent',  '이학생', '0000'),
    ('parkstudent', '박학생', '1111'),
    ('5student',    '오학생', '2222');
```

**자동 처리**:
- `user_num` (AUTO_INCREMENT) - 생략 시 다음 시퀀스
- `signup_date` (DEFAULT CURRENT_TIMESTAMP) - 생략 시 NOW()
- `user_email` (NULL 허용) - 생략 시 NULL

⚠️ AUTO_INCREMENT 컬럼에 값 명시 → 시퀀스 꼬임. 생략 또는 `DEFAULT` 사용.

</details>

### Q8. (적용) ALTER TABLE 로 컬럼 추가·타입 변경·이름 변경·삭제·제약 추가를 각각 작성.

<details><summary>정답</summary>

```sql
-- 컬럼 추가 (NOT NULL DEFAULT 로 안전하게)
ALTER TABLE member ADD COLUMN age INT NOT NULL DEFAULT 0;

-- 컬럼 타입 변경 (이름 유지)
ALTER TABLE member MODIFY COLUMN user_email VARCHAR(50);

-- 컬럼 이름 + 타입 변경
ALTER TABLE member CHANGE user_email email VARCHAR(50);

-- 컬럼 삭제
ALTER TABLE member DROP COLUMN age;

-- 제약조건 추가
ALTER TABLE member ADD CONSTRAINT uq_email UNIQUE (user_email);

-- 제약조건 삭제 (UNIQUE 는 INDEX 로)
ALTER TABLE member DROP INDEX uq_email;
```

⚠️ **운영 1억 행 테이블의 ALTER TABLE** 은 전체 테이블 락 → 서비스 정지 위험.
- MySQL 8.0 `INSTANT` 알고리즘 일부 지원
- pt-online-schema-change, gh-ost 같은 도구로 무중단 변경

</details>

### Q9. (디버그) `UPDATE member SET user_password = '1234';` 실행 시 무슨 일이 일어나는가?

<details><summary>정답</summary>

**모든 사용자의 비밀번호가 '1234' 로 변경됨**. WHERE 가 없으므로 **전체 행 대상**.

이를 막는 **Safe Update Mode** (MySQL Workbench 기본 ON):
- PK·UNIQUE 컬럼이 WHERE 에 없는 UPDATE/DELETE 는 **에러로 거부**
- 에러: `Error Code: 1175. You are using safe update mode...`

해제 방법:
```sql
-- 세션 단위 해제
SET SQL_SAFE_UPDATES = 0;

-- 또는 Workbench Preferences > SQL Editor > "Safe Updates" 체크 해제 (재접속 필요)
```

운영 사고 방지 체크리스트:
1. UPDATE 전에 같은 WHERE 로 **SELECT** 해 영향 행 수 확인
2. `START TRANSACTION` 안에서 실행
3. 결과 확인 후 `COMMIT` 또는 `ROLLBACK`
4. 운영 DB 는 read-only 권한 분리

</details>

### Q10. (디버그) FK 의 `ON DELETE` 옵션 4가지와 동작?

<details><summary>정답</summary>

```sql
CREATE TABLE board (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    title     VARCHAR(100),
    writer_id INT NOT NULL,
    FOREIGN KEY (writer_id) REFERENCES member(user_num)
        ON DELETE CASCADE
);
```

| 옵션 | 부모 (member) 삭제 시 자식 (board) 동작 |
|--|--|
| **CASCADE** | 같이 삭제 |
| **SET NULL** | writer_id 를 NULL 로 (단 컬럼 NULL 허용해야) |
| **RESTRICT** / **NO ACTION** | 자식이 있으면 부모 삭제 거부 (**기본**) |
| **SET DEFAULT** | DEFAULT 값으로 (MySQL 미지원, 표준만) |

**선택 가이드**:
- 게시글 → 댓글 → CASCADE (게시글 삭제 시 댓글도 무의미)
- 사원 → 작성한 글 → SET NULL (글은 살리고 작성자만 익명)
- 부서 → 사원 → RESTRICT (사원이 있는 부서는 삭제 금지)

위험: CASCADE 잘못 걸면 의도치 않은 대량 삭제. 운영 적용 전 SELECT 로 영향 범위 확인.

</details>

### Q11. (디버그) DROP / TRUNCATE / DELETE 의 차이를 종류·구조·트랜잭션·AUTO_INCREMENT·속도로 비교.

<details><summary>정답</summary>

| 항목 | DROP TABLE | TRUNCATE TABLE | DELETE FROM |
|--|--|--|--|
| **종류** | DDL | DDL | DML |
| **테이블 구조** | 삭제 | 유지 | 유지 |
| **데이터** | 삭제 (테이블째) | 모두 삭제 | WHERE 조건 행만 |
| **WHERE** | 불가 | 불가 | 가능 |
| **AUTO_INCREMENT** | (테이블 사라짐) | **리셋 (1로)** | 유지 (계속 증가) |
| **ROLLBACK** | 불가 (자동 커밋) | 불가 (자동 커밋) | **가능** (트랜잭션 안) |
| **트리거** | (실행 안 됨) | 실행 안 됨 | 행마다 실행 |
| **속도** | 즉시 | 매우 빠름 | 느림 (행마다 로그) |

**선택 가이드**:
- 테이블 자체가 필요 없음 → `DROP`
- "비우기" + AUTO_INC 1부터 다시 → `TRUNCATE`
- 조건 행만 삭제 / 롤백 가능성 필요 → `DELETE`

```sql
DELETE FROM member;          -- 행은 다 지웠지만 다음 가입 user_num = 100
TRUNCATE TABLE member;       -- 행 다 지우고 다음 가입 user_num = 1
```

</details>

### Q12. (적용) 계좌 이체 트랜잭션 (A → B 1000원). 부분 실패 시 부정합을 ROLLBACK 으로 방지.

<details><summary>정답</summary>

```sql
START TRANSACTION;

-- 1. A 잔액 차감
UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';

-- 2. B 잔액 추가
UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';

-- 검증 후 COMMIT
COMMIT;

-- 실패 시
-- ROLLBACK;
```

**트랜잭션 없으면 위험한 시나리오**:
1. UPDATE A 성공 (A 의 1000 차감 COMMIT)
2. 네트워크 끊김 / 서버 다운
3. UPDATE B 실행 안 됨
4. → A 는 1000 잃었는데 B 에 안 들어옴. **데이터 부정합**.

**ACID 의 A (Atomicity, 원자성)**: "전부 성공 or 전부 실패". 둘 다 성공해야 COMMIT, 하나라도 실패하면 ROLLBACK 으로 둘 다 취소.

⚠️ MySQL **기본 Auto Commit ON** - 모든 SQL 즉시 COMMIT. 트랜잭션 묶음 쓰려면 명시적 `START TRANSACTION`.

</details>

### Q13. (적용) SAVEPOINT 로 트랜잭션 안에서 일부만 ROLLBACK.

<details><summary>정답</summary>

```sql
START TRANSACTION;

INSERT INTO test_table VALUES ('A');
SAVEPOINT sp1;                        -- 여기에 저장점 찍기

INSERT INTO test_table VALUES ('B');
INSERT INTO test_table VALUES ('C');

ROLLBACK TO sp1;                      -- B, C 만 취소 (A 는 남음)

INSERT INTO test_table VALUES ('D');
COMMIT;

-- 최종 결과: A, D
```

**용도**:
- 긴 트랜잭션에서 일부 단계만 재시도
- 배치 처리: 100건 중 일부 실패 시 그 부분만 되돌리고 계속

**주의**:
- `ROLLBACK TO sp1` 후에도 트랜잭션은 **계속 진행** (COMMIT/ROLLBACK 안 한 상태)
- 최종 COMMIT 안 하면 모든 변경 사라짐
- DDL 은 SAVEPOINT 와 별개로 자동 커밋

</details>

### Q14. (면접) "트랜잭션은 왜 필요한가? ACID 4 속성으로 설명하시오."

<details><summary>정답</summary>

**한 줄**: 여러 SQL 을 묶어 **부분 실패로 인한 데이터 부정합을 막기 위해**.

**ACID 4 속성**:

| 속성 | 설명 | 예시 |
|--|--|--|
| **A (Atomicity, 원자성)** | 전부 성공 or 전부 실패. 중간 상태 노출 X | 계좌 이체에서 차감만 성공·입금 실패 → 둘 다 ROLLBACK |
| **C (Consistency, 일관성)** | 트랜잭션 전후 DB 가 무결성 제약 만족 | FK 위반 시 자동 ROLLBACK → 고아 자식 행 발생 X |
| **I (Isolation, 격리성)** | 동시 실행 트랜잭션이 서로 영향 X | A 가 잔액 읽는 동안 B 의 이체가 끼어들지 못함 |
| **D (Durability, 지속성)** | COMMIT 된 변경은 장애·재부팅에도 유지 | COMMIT 직후 서버 다운 → 재기동 시 변경 복구 |

**실제 사례**:

```sql
-- 쇼핑몰 주문
START TRANSACTION;
    INSERT INTO orders VALUES (...);              -- 주문 생성
    UPDATE products SET stock = stock - 1         -- 재고 차감
        WHERE id = 100;
    UPDATE accounts SET balance = balance - 50000 -- 결제
        WHERE user_id = 'kim';
COMMIT;
```

이 3개 중 하나라도 실패하면 **3개 모두 취소**. 그렇지 않으면:
- 주문은 생성됐는데 재고 차감 안 됨 → 재고 부정확
- 결제는 됐는데 주문 없음 → 사용자 환불 분쟁

**자바와 비교**: 자바의 `try-catch-finally` 는 단일 머신 안에서만. DB 트랜잭션은 디스크·로그까지 보장 (D=Durability). Spring `@Transactional` 은 이 ACID 를 메서드 단위로 묶어주는 추상화.

**MySQL 기본**: Auto Commit ON → 모든 SQL 이 단독 트랜잭션. 묶음이 필요하면 `START TRANSACTION` 명시.

</details>
