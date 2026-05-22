# DDL · DML · Transaction — 치트시트

> 29p 슬라이드 · member / accounts 스키마.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **DDL** = 그릇 만들기 (CREATE / ALTER / DROP / TRUNCATE)
2. **DML** = 그릇에 데이터 채우고 바꾸기 (INSERT / UPDATE / DELETE)
3. **TCL** = 변경을 묶어서 안전하게 (COMMIT / ROLLBACK / SAVEPOINT)
4. **금액은 무조건 DECIMAL**, FLOAT 는 오차 누적
5. **WHERE 없는 UPDATE/DELETE** = 전체 행. Safe Mode 로 막기
6. **트랜잭션** = ACID 4 속성. MySQL 기본 AutoCommit ON, 묶음은 `START TRANSACTION` 명시

## 가장 중요한 코드 3개

```sql
-- (1) 표준 테이블 생성
CREATE TABLE member (
    user_num      INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id       VARCHAR(20)  NOT NULL UNIQUE,
    user_name     VARCHAR(20)  NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    user_email    VARCHAR(30),
    signup_date   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- (2) 트랜잭션 (계좌 이체)
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';
    UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';
COMMIT;     -- 실패 시 ROLLBACK

-- (3) 안전한 UPDATE
SET SQL_SAFE_UPDATES = 1;
UPDATE member SET user_password = 'new' WHERE user_num = 3;
```

## 면접 한 줄 답변
- **ACID 가 뭐죠?** → A=원자성, C=일관성, I=격리성, D=지속성.
- **PK 와 UNIQUE 차이는?** → PK: 1개·NULL 불가·클러스터 인덱스 / UNIQUE: 여러 개·NULL OK·보조 인덱스.
- **DROP/TRUNCATE/DELETE 중 뭐?** → 테이블째 DROP / 비우기+리셋 TRUNCATE / 조건+롤백 DELETE.
- **트랜잭션은 왜?** → 부분 실패로 인한 데이터 부정합 방지. 계좌 이체에서 차감만 성공·입금 실패 시 둘 다 롤백.

---

# 2. Quick Reference (실무 복붙)

## Data Type 선택 가이드

| 용도 | 타입 | 메모 |
|--|--|--|
| PK (자동 증가) | `INT AUTO_INCREMENT` 또는 `BIGINT` | 1억 이상이면 BIGINT |
| boolean | `TINYINT(1)` 또는 `BOOLEAN` | 0=false, 그 외=true |
| **금액** | `DECIMAL(M, D)` | **절대 FLOAT/DOUBLE X** |
| 짧은 코드 (우편번호) | `CHAR(N)` | 길이 일정, 빠름 |
| 이름·이메일 | `VARCHAR(N)` | 가변 길이 |
| 본문 (긴 텍스트) | `TEXT` | 65,535 자 |
| 날짜만 | `DATE` | `'YYYY-MM-DD'` |
| 날짜+시간 | `DATETIME` | 시간대 무시, 2038 이후 OK |
| 타임존 자동 | `TIMESTAMP` | UTC 저장, 2038 한계 |
| 이미지·파일 | URL 만 (`VARCHAR`), 실체는 S3 | DB 에 BLOB 비권장 |

## 제약 조건 6가지

```sql
NOT NULL    -- 값 필수
UNIQUE      -- 중복 X (NULL 여러 개 OK)
PRIMARY KEY -- UNIQUE + NOT NULL, 테이블당 1개
FOREIGN KEY -- 다른 테이블 PK 참조
DEFAULT     -- 기본값
CHECK       -- 값 범위 검증 (MySQL 8+)
```

## ALTER TABLE 명령

```sql
ALTER TABLE t ADD COLUMN age INT NOT NULL DEFAULT 0;
ALTER TABLE t MODIFY COLUMN email VARCHAR(50);         -- 타입만 변경
ALTER TABLE t CHANGE old_name new_name VARCHAR(50);    -- 이름 + 타입
ALTER TABLE t DROP COLUMN age;
ALTER TABLE t ADD CONSTRAINT uq_email UNIQUE (email);
ALTER TABLE t DROP INDEX uq_email;
```

## INSERT 3가지 방법

```sql
-- (1) 모든 컬럼 (순서대로)
INSERT INTO member VALUES (1, 'kim', '김학생', '1234', 'a@b.c', NOW());

-- (2) 원하는 컬럼만
INSERT INTO member (user_id, user_name, user_password)
VALUES ('kim', '김학생', '1234');

-- (3) 여러 행 한 번에 (성능 ↑)
INSERT INTO member (user_id, user_name, user_password) VALUES
    ('a', 'A', '111'),
    ('b', 'B', '222');
```

## DROP vs TRUNCATE vs DELETE

|  | DROP | TRUNCATE | DELETE |
|--|--|--|--|
| 종류 | DDL | DDL | DML |
| 구조 | **삭제** | 유지 | 유지 |
| WHERE | X | X | **O** |
| AUTO_INC | - | **리셋** | 유지 |
| ROLLBACK | X | X | **O** |
| 속도 | 즉시 | 매우 빠름 | 느림 |

## FK ON DELETE 옵션

| 옵션 | 부모 삭제 시 자식 |
|--|--|
| `CASCADE` | 같이 삭제 |
| `SET NULL` | NULL 로 (컬럼 NULL 허용 시) |
| `RESTRICT` / `NO ACTION` | 거부 (**기본**) |
| `SET DEFAULT` | MySQL 미지원 |

## Transaction 패턴

```sql
-- 기본 묶음
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';
    UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';
COMMIT;     -- 또는 ROLLBACK

-- SAVEPOINT (부분 롤백)
START TRANSACTION;
INSERT INTO t VALUES ('A');
SAVEPOINT sp1;
INSERT INTO t VALUES ('B');
ROLLBACK TO sp1;     -- B 만 취소, A 는 남음
COMMIT;
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| 금액에 `FLOAT` → 오차 누적 | `DECIMAL(10, 2)` |
| `VARCHAR(N)` N 부족 | bcrypt 는 60자, 여유 두기 |
| `WHERE` 없는 UPDATE → 전체 변경 | Safe Mode + 트랜잭션 |
| `UNIQUE` 위반 → 스택트레이스 노출 | Service 에서 잡아 사용자 메시지 |
| FK 자식 있는데 부모 DROP | 자식 먼저 또는 `FOREIGN_KEY_CHECKS = 0` |
| TRUNCATE 후 ROLLBACK 시도 | 불가능 (DDL) - DELETE 사용 |
| AUTO_INC 컬럼에 값 명시 | 생략 또는 `DEFAULT` |
| TIMESTAMP 2038 한계 | DATETIME 사용 |
| Auto Commit ON 인데 묶음 작업 | `START TRANSACTION` 명시 |
| `=NULL` 비교 | `IS NULL` |

## 디버깅 명령

```sql
DESC member;                  -- 스키마 확인
SHOW CREATE TABLE member;     -- 전체 DDL
SHOW TABLES;                       -- DB 의 테이블 목록
SHOW DATABASES;                    -- 모든 DB
SELECT @@autocommit;               -- AutoCommit 상태
SET SQL_SAFE_UPDATES = 0;          -- Safe Mode 해제
```

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
DB 변경 (29p 슬라이드)
│
├── [A] Data Type
│   ├── 숫자형: TINYINT / INT / BIGINT / DECIMAL(M,D)
│   ├── 문자형: CHAR / VARCHAR / TEXT
│   ├── 날짜·시간: DATE / DATETIME / TIMESTAMP
│   └── 바이너리 (BLOB) → 실무: URL 만 DB, 실체 S3
│
├── [B] DDL
│   ├── DATABASE: CREATE / ALTER / DROP / USE
│   ├── TABLE
│   │   ├── CREATE TABLE + 제약 6가지
│   │   │   └── NOT NULL / UNIQUE / PK / FK / DEFAULT / CHECK
│   │   ├── ALTER TABLE
│   │   │   └── ADD / MODIFY / CHANGE / DROP COLUMN
│   │   ├── DESC / SHOW CREATE TABLE
│   │   ├── DROP TABLE
│   │   └── TRUNCATE TABLE
│   └── FK 옵션: CASCADE / SET NULL / RESTRICT
│
├── [C] DML
│   ├── INSERT (3 방법)
│   ├── UPDATE + Safe Mode
│   └── DELETE (트랜잭션 안 ROLLBACK)
│
└── [D] Transaction (TCL)
    ├── ACID 4 속성
    ├── START TRANSACTION / COMMIT / ROLLBACK
    ├── SAVEPOINT (부분 롤백)
    └── MySQL 기본: AutoCommit ON
```

## 학습 진도 체크리스트

### A. Data Type
- [ ] 숫자형 8종 + DECIMAL 의 금액 적합성
- [ ] CHAR(N) vs VARCHAR(N) 의 저장 차이
- [ ] DATETIME vs TIMESTAMP 의 2038 문제

### B. DDL
- [ ] CREATE TABLE + 6 제약조건 모두 사용
- [ ] PK 작성 3 방식 (인라인 / 테이블 레벨 / ALTER)
- [ ] FK 작성 + ON DELETE 4 옵션
- [ ] ALTER TABLE 5 작업
- [ ] DROP vs TRUNCATE 차이

### C. DML
- [ ] INSERT 3 방법
- [ ] UPDATE + Safe Mode (`SQL_SAFE_UPDATES`)
- [ ] DELETE vs TRUNCATE
- [ ] AUTO_INC + DEFAULT 자동 처리

### D. Transaction
- [ ] ACID 4 속성 설명 가능
- [ ] START TRANSACTION / COMMIT / ROLLBACK
- [ ] SAVEPOINT 부분 ROLLBACK
- [ ] 계좌 이체 시나리오 작성 가능
- [ ] AutoCommit 의미 + 해제

## 연관 강의

```
1강 SELECT 기본    -> SELECT 의 7단계 실행 순서
2강 SELECT 응용    -> GROUP BY, HAVING, View
3강 DDL/DML/TX     <- 현재 위치
4강 JOIN/SubQuery  -> 여러 테이블 합치기
5강 JDBC           -> 자바 -> DB 연결
6강 관통 PJT       -> 통합 게시판
```

→ 다음은 4강 JOIN/SubQuery 로 **여러 테이블 합치기** 학습.
