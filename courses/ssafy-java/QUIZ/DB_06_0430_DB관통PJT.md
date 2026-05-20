# DB 관통 PJT (Web Backend x DB) - 퀴즈

> 14문항. 개념·적용·디버그·면접. users / boards / comments 게시판 스키마.

---

### Q1. (개념) 게시판 앱의 레이어 분리 (Servlet → Service → DAO → DB) 와 각 책임?

<details><summary>정답</summary>

```
[Servlet]  →  [Service]  →  [DAO]  →  [DB]
   HTTP        비즈니스       SQL
```

| 레이어 | 책임 | 절대 하면 안 됨 |
|--|--|--|
| **Servlet** | 요청 파싱, 세션, redirect, 응답 코드 | SQL 직접, 비즈니스 로직 |
| **Service** | 트랜잭션 경계, 여러 DAO 조합, 권한 검증 | HTTP 의존 (HttpServletRequest 받지 X) |
| **DAO** | SQL 실행, ResultSet → 객체 매핑 | 비즈니스 분기 (`if user.isAdmin()`) |
| **Model** | 데이터 운반 (DTO/Entity) | 로직 |

**왜 분리하나**:
- Servlet → Spring MVC 로 갈아끼울 때 Service/DAO 그대로
- Service 는 HTTP 모르므로 배치 작업·테스트 재사용 가능
- DAO 만 알면 SQL 변경 영향 최소

</details>

### Q2. (개념) 게시판 통합 스키마 (users / boards / comments) + FK + INDEX 작성.

<details><summary>정답</summary>

```sql
CREATE TABLE users (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    login_id   VARCHAR(30)  NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,             -- bcrypt 해시 (60자 + 여유)
    nickname   VARCHAR(50)  NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE boards (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    BIGINT       NOT NULL,
    title      VARCHAR(200) NOT NULL,
    content    TEXT         NOT NULL,
    view_count INT          NOT NULL DEFAULT 0,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    board_id   BIGINT   NOT NULL,
    user_id    BIGINT   NOT NULL,
    body       TEXT     NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE
);

CREATE INDEX idx_boards_created ON boards(created_at DESC);
```

**핵심**:
- `password VARCHAR(255)` - bcrypt 출력 60자 + 알고리즘 변경 여유
- `ON DELETE CASCADE` - 회원 탈퇴 시 글·댓글 같이 삭제
- `idx_boards_created` - 목록 정렬 컬럼 인덱스

</details>

### Q3. (디버그) "글 삭제 시 댓글이 안 지워진다" 버그의 의심처 3가지?

<details><summary>정답</summary>

1. **FK `ON DELETE CASCADE` 누락**
   - `comments.board_id` FK 가 RESTRICT (기본) 라면 댓글 있는 글 삭제 시 에러 발생 또는 댓글 안 지워짐
   - 해결: `FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE`

2. **Service 가 트랜잭션으로 안 묶음**
   - 댓글 DELETE → 글 DELETE 순서로 호출하는 코드 일 때, 댓글 DELETE 만 성공·글 DELETE 실패하면 불일치
   - 해결: `setAutoCommit(false)` + 둘 다 성공 시 commit

3. **`comments.board_id` 자체 FK 가 없음**
   - DB 가 참조 무결성을 모름 → CASCADE 도 안 됨
   - 해결: ALTER TABLE 로 FK 추가

```sql
-- 확인
SHOW CREATE TABLE comments;
-- "CONSTRAINT ... FOREIGN KEY (board_id) ... ON DELETE CASCADE" 있는지 확인
```

</details>

### Q4. (적용) 본인 글만 삭제하도록 `WHERE id=? AND user_id=?` 처리. 장점?

<details><summary>정답</summary>

```java
public int delete(Connection con, long boardId, long userId) throws SQLException {
    String sql = "DELETE FROM boards WHERE id = ? AND user_id = ?";
    try (PreparedStatement ps = con.prepareStatement(sql)) {
        ps.setLong(1, boardId);
        ps.setLong(2, userId);
        return ps.executeUpdate();   // 영향 행 수
    }
}

// Service
int affected = boardDao.delete(con, boardId, userId);
if (affected == 0) throw new IllegalStateException("권한 없음 또는 이미 삭제됨");
```

**장점**:

1. **DB 한 줄로 권한 검증** - 별도 SELECT 안 함
2. **Race condition 회피** - "SELECT 로 작성자 확인 → DELETE" 사이에 다른 트랜잭션이 글을 수정해도 안전
3. **코드 간결** - if-then-else 없음
4. **영향 행 수로 결과 판별** - 0 = 권한 없음 또는 이미 삭제

**안 좋은 예**:
```java
Board b = boardDao.findById(boardId);     // SELECT
if (b.getUserId() != userId) throw new ...;
boardDao.delete(boardId);                 // DELETE - 이 사이에 누가 바꿨다면?
```

→ 가능하면 권한 검증을 **WHERE 절에 포함**.

</details>

### Q5. (적용) Service 에서 트랜잭션으로 "댓글 일괄 삭제 + 글 삭제" 처리.

<details><summary>정답</summary>

```java
public void deleteBoard(long boardId, long userId) throws SQLException {
    Connection con = null;
    try {
        con = ds.getConnection();
        con.setAutoCommit(false);                  // 트랜잭션 시작

        commentDao.deleteByBoard(con, boardId);    // 1. 댓글 일괄 삭제
        int affected = boardDao.delete(con, boardId, userId);  // 2. 글 삭제

        if (affected == 0) {
            throw new IllegalStateException("권한 없음 또는 이미 삭제됨");
        }

        con.commit();                              // 모두 성공
    } catch (Exception e) {
        if (con != null) con.rollback();           // 한쪽 실패 → 둘 다 취소
        throw e;
    } finally {
        if (con != null) {
            con.setAutoCommit(true);
            con.close();
        }
    }
}
```

**왜 트랜잭션?**:
- 댓글 DELETE 성공 → 글 DELETE 가 권한 에러 → 댓글만 사라진 상태
- ROLLBACK 으로 둘 다 원상 복귀

**FK CASCADE 와의 관계**:
- FK CASCADE 가 있으면 글 DELETE 만으로 댓글도 자동 삭제 → 첫 줄 생략 가능
- 그래도 트랜잭션은 여전히 필요 (다른 작업도 같이 묶일 수 있음)

→ Spring 에선 `@Transactional` 한 줄로 끝.

</details>

### Q6. (적용) 게시글 목록 페이지네이션 + 작성자 닉네임 JOIN 쿼리.

<details><summary>정답</summary>

```sql
SELECT b.id, b.title, b.view_count, b.created_at,
       u.nickname AS writer
FROM   boards b
JOIN   users u ON u.id = b.user_id
ORDER BY b.id DESC
LIMIT  ? OFFSET ?;
```

```java
ps.setInt(1, size);                  // 페이지당 행 수 (예: 10)
ps.setInt(2, (page - 1) * size);     // OFFSET = 0, 10, 20, ...
```

**핵심**:
- `LIMIT ? OFFSET ?` 순서 (MySQL/PG)
- `JOIN users` 로 N+1 회피 (글 N개에 대해 작성자 SELECT N번 안 함)
- `b.id DESC` 정렬 - 최신순 + 인덱스 활용
- `JOIN` 은 INNER → 회원 탈퇴된 글은 제외. 살리려면 LEFT JOIN

**전체 페이지 수** (UI 표시용):
```sql
SELECT COUNT(*) FROM boards;
-- 또는 캐시된 카운터 (Redis)
```

</details>

### Q7. (디버그) 100만 행 boards 에서 `LIMIT 10 OFFSET 990` 이 느린 이유와 키셋 페이지네이션.

<details><summary>정답</summary>

**문제**: OFFSET N 은 DB 가 **앞 N 행을 스킵하며 모두 읽음**.
- 페이지 100 (10건씩) → OFFSET 990 → 1000 행 읽고 990 행 버림
- 페이지 10000 → OFFSET 99990 → 10만 행 읽고 버림 = 점점 느려짐
- 100만 행에서 마지막 페이지 → 수 초 ~ 수십 초

**키셋 페이지네이션 (Keyset / Cursor)**:

```sql
-- 첫 페이지 (마지막 본 id 없음)
SELECT * FROM boards ORDER BY id DESC LIMIT 10;
-- 결과의 마지막 id = 12340 기억

-- 다음 페이지 (마지막 본 id 사용)
SELECT * FROM boards
WHERE id < 12340                  -- 이전 페이지 마지막 id
ORDER BY id DESC LIMIT 10;
```

**장점**:
- 항상 동일한 속도 (인덱스 사용)
- 페이지가 깊어도 느려지지 않음

**단점**:
- "5페이지로 점프" 같은 임의 페이지 이동 불가
- UI 가 "다음 페이지" / "더 보기" 버튼이어야 함

→ 무한 스크롤·SNS 피드는 키셋, 전통적 1-2-3-4 페이지네이션은 OFFSET (단 깊이 제한).

</details>

### Q8. (적용) 검색 `WHERE title LIKE ? OR content LIKE ?` 의 와일드카드와 ESCAPE 처리.

<details><summary>정답</summary>

```java
// 1. 자바에서 % 추가
ps.setString(1, "%" + keyword + "%");
ps.setString(2, "%" + keyword + "%");
```

또는 SQL 에서:
```sql
WHERE title LIKE CONCAT('%', ?, '%') OR content LIKE CONCAT('%', ?, '%')
```

**LIKE 와일드카드**:
- `%` - 0개 이상의 임의 문자
- `_` - 임의의 한 문자

**ESCAPE 처리 (사용자 입력에 `%`/`_` 가 있을 때)**:

```java
String escaped = keyword
    .replace("\\", "\\\\")
    .replace("%", "\\%")
    .replace("_", "\\_");
ps.setString(1, "%" + escaped + "%");
```

```sql
WHERE title LIKE ? ESCAPE '\\'
```

**왜 ESCAPE?**: 사용자가 "100% 만족" 을 검색하면 `%` 가 와일드카드로 해석되어 의도치 않은 매칭.

⚠️ **성능**: `LIKE '%keyword%'` 는 **인덱스 못 씀** → 풀스캔.
- 대량 데이터는 **FULLTEXT INDEX** (MySQL) 또는 **Elasticsearch** 검색 엔진 사용.

</details>

### Q9. (디버그) `con.setAutoCommit(false)` 후 catch 절 없이 try-finally 만 쓰면?

<details><summary>정답</summary>

**문제 코드**:
```java
con = ds.getConnection();
con.setAutoCommit(false);
try {
    boardDao.delete(con, boardId, userId);
    commentDao.deleteByBoard(con, boardId);
    con.commit();
} finally {                                  // catch 없음
    if (con != null) {
        con.setAutoCommit(true);
        con.close();
    }
}
```

**증상**:
- 첫 DELETE 실패 → 예외 발생 → commit 도 안 함 + **rollback 도 안 함**
- finally 의 `con.close()` 는 호출되지만, 풀이 자동으로 rollback 해주는 게 표준은 아님 (HikariCP 는 해주긴 함)
- 일부 풀·드라이버에선 **부분 commit 상태로 풀에 반환** → 다음 사용자가 이상한 상태의 커넥션 받음

**올바른 패턴**:
```java
try {
    // ...
    con.commit();
} catch (Exception e) {
    if (con != null) con.rollback();         // 명시적 rollback
    throw e;                                 // 예외 다시 던지기 (조용히 삼키면 안 됨)
} finally {
    if (con != null) {
        con.setAutoCommit(true);             // 풀 반환 전 기본값
        con.close();
    }
}
```

→ Spring `@Transactional` 은 이 catch+rollback 을 자동으로. 그래서 어노테이션이 강력.

</details>

### Q10. (디버그) `UNIQUE` 제약 위반 (이미 사용 중인 login_id) 을 사용자 친화 메시지로 변환?

<details><summary>정답</summary>

**안 좋은 예**:
```java
userDao.insert(user);
// SQLIntegrityConstraintViolationException: Duplicate entry 'kim' for key 'users.login_id'
// -> 사용자에게 그대로 노출 (보안·UX 문제)
```

**좋은 예 - Service 에서 변환**:
```java
public void signup(User user) {
    try {
        userDao.insert(user);
    } catch (SQLIntegrityConstraintViolationException e) {
        if (e.getMessage().contains("login_id")) {
            throw new DuplicateLoginIdException("이미 사용 중인 ID 입니다");
        }
        throw e;
    }
}
```

**Spring 에서**:
```java
try {
    userMapper.insert(user);
} catch (DuplicateKeyException e) {       // Spring 이 변환해줌
    throw new BusinessException("이미 사용 중인 ID");
}
```

**더 나은 방법 - 먼저 체크**:
```java
if (userDao.existsByLoginId(loginId)) {
    throw new DuplicateLoginIdException(...);
}
userDao.insert(user);
```

⚠️ **Race condition**: 체크와 INSERT 사이에 다른 가입이 끼면 여전히 UNIQUE 위반. → **UNIQUE 제약 + try-catch 가 최종 방어선**.

**보안**: DB 의 raw 메시지를 노출하면 테이블·컬럼명 유출 → 공격자에 정보 제공.

</details>

### Q11. (개념) 패스워드를 평문으로 저장하면 안 되는 이유와 bcrypt 적용?

<details><summary>정답</summary>

**평문 저장 위험**:
- DB 덤프 유출 시 → 모든 사용자 비밀번호 노출
- 사용자가 같은 비밀번호를 다른 사이트에서도 사용 → 다른 서비스도 뚫림 (Credential Stuffing 공격)
- 운영자도 비밀번호를 봄 → 윤리·법적 문제

**bcrypt 해시 + salt**:
```java
// Spring Security
PasswordEncoder encoder = new BCryptPasswordEncoder();

// 가입
String hashed = encoder.encode("user-password");
// 결과: $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy

// 로그인
boolean ok = encoder.matches("user-password", hashed);
```

**bcrypt 특징**:
- **단방향 해시** - 복호화 불가능
- **salt 내장** - 같은 비밀번호도 매번 다른 결과
- **느림 (의도적)** - brute-force 공격을 어렵게 (cost 파라미터로 조절)
- **출력 길이 60자** - 그래서 `VARCHAR(255)` 컬럼 사용 (알고리즘 변경 여유)

**대안**: PBKDF2, Argon2 (현대 권장), scrypt. **MD5/SHA1 은 금지** (너무 빠름 = brute-force 쉬움).

**평문도 안 되고, 단순 SHA-256 도 안 됨**: bcrypt/Argon2 같은 **느린 해시** 필수.

</details>

### Q12. (개념) 트랜잭션 격리 수준 4가지와 각각 허용하는 이상 현상?

<details><summary>정답</summary>

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|--|--|--|--|
| **READ UNCOMMITTED** | O | O | O |
| **READ COMMITTED** (PG/Oracle 기본) | X | O | O |
| **REPEATABLE READ** (MySQL InnoDB 기본) | X | X | O (MySQL 은 X) |
| **SERIALIZABLE** | X | X | X |

**이상 현상**:
- **Dirty Read** - 다른 트랜잭션의 commit 안 된 변경을 읽음
- **Non-Repeatable Read** - 같은 행을 두 번 SELECT 했을 때 값이 다름 (중간에 다른 트랜잭션 commit)
- **Phantom Read** - 같은 조건의 SELECT 가 두 번째 실행 시 행 수가 다름 (다른 트랜잭션 INSERT)

**설정**:
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

```java
con.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);
```

**선택 가이드**:
- 일반 OLTP → READ COMMITTED (대부분)
- MySQL 기본 → REPEATABLE READ (InnoDB MVCC 로 phantom 도 일부 방지)
- 정확한 일관성 필요 (금융, 재고) → SERIALIZABLE (성능 ↓)

→ 격리 수준 ↑ = 일관성 ↑ + 성능 ↓.

</details>

### Q13. (디버그) 조회수 증가에서 동시성 문제와 해결?

<details><summary>정답</summary>

**안 좋은 코드**:
```java
// 1. 현재 조회수 읽기
Board b = boardDao.findById(id);

// 2. +1
int newCount = b.getViewCount() + 1;

// 3. UPDATE
boardDao.updateViewCount(id, newCount);
```

**문제**:
- 사용자 A 가 1 읽음 → 사용자 B 도 1 읽음 → A 가 2 로 UPDATE → B 도 2 로 UPDATE → **하나만 카운트됨**
- 동시 접속 100명이면 50명만 카운트 → 조회수 절반 손실

**해결 1: 원자적 UPDATE**:
```sql
UPDATE boards SET view_count = view_count + 1 WHERE id = ?;
```
- DB 가 락 잡고 한 번에 처리 → 동시성 안전

**해결 2: 쿠키로 중복 방지 (DB 부하 감소)**:
```java
String cookieName = "viewed_" + boardId;
if (req.getCookies() == null || Arrays.stream(req.getCookies())
        .noneMatch(c -> c.getName().equals(cookieName))) {
    boardDao.incrementView(boardId);
    Cookie c = new Cookie(cookieName, "1");
    c.setMaxAge(24 * 60 * 60);
    resp.addCookie(c);
}
```

**해결 3: Redis 카운터 + 배치 동기화** (대규모):
- 실시간 INCR 는 Redis 에 (메모리 = 빠름)
- 1분마다 DB 에 동기화

**원칙**: "READ-MODIFY-WRITE" 패턴은 항상 race condition 의심.

</details>

### Q14. (면접) "DB 가 느려지기 시작했다. 어떤 순서로 진단·처방?"

<details><summary>정답</summary>

**1단계: 측정 (Profiling)**:
```sql
-- Slow Query Log 활성화
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;          -- 1초 이상

-- 가장 느린 쿼리 찾기
SELECT * FROM mysql.slow_log ORDER BY query_time DESC LIMIT 10;

-- 개별 쿼리 실행 계획
EXPLAIN SELECT ...;
```

**2단계: 인덱스** (90% 의 처방):
- WHERE / JOIN / ORDER BY 컬럼에 인덱스
- 단 INSERT/UPDATE 도 인덱스 갱신하므로 무한정 추가 X
- `EXPLAIN` 의 `type` 컬럼이 `ALL` 이면 풀스캔 → 인덱스 없음

**3단계: N+1 query 제거**:
- JOIN, JPA `JOIN FETCH`, MyBatis `<collection>`

**4단계: SELECT 최적화**:
- `SELECT *` 제거 → 필요한 컬럼만
- 페이지네이션 → OFFSET 대신 keyset
- 불필요한 JOIN 제거

**5단계: 캐시** (Redis):
- 자주 읽고 자주 안 바뀌는 데이터 (인기 게시글, 메뉴, 설정값)
- TTL 설정

**6단계: 읽기 Replica**:
- 읽기 부하를 슬레이브 DB 로 분산
- 쓰기는 마스터, 읽기는 슬레이브

**7단계: 샤딩 (마지막 카드)**:
- 데이터를 여러 DB 로 수평 분할 (user_id 해시)
- JOIN, 트랜잭션 어려워짐
- 운영 복잡도 폭증 → 다른 방법 다 시도한 후

**우선순위 요약**:
```
인덱스 -> 쿼리 최적화 -> 캐시 -> Replica -> 샤딩
(쉬움, 효과 큼)              (어려움, 효과 더 큼)
```

→ "DB 가 느리면 인덱스" 는 신화. 먼저 측정하고, EXPLAIN 보고, 가장 비싼 쿼리부터.

</details>
