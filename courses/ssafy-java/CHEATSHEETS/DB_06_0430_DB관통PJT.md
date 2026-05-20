# DB 관통 PJT (Web Back x DB) — 치트시트

> Web Backend 1~5강 + DB 1~5강 통합 게시판 프로젝트.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **레이어**: Servlet → Service → DAO → DB (각 레이어 자기 위 모름)
2. **트랜잭션 경계**는 Service 에서 (Servlet 도 DAO 도 X)
3. **본인 글만 삭제**는 `WHERE id=? AND user_id=?` (DB 한 줄 권한 검증)
4. **OFFSET 깊으면 느림** → 키셋 페이지네이션 (`WHERE id < ?`)
5. **패스워드 평문 금지** → bcrypt (`VARCHAR(255)` 컬럼)
6. **UNIQUE 위반**은 Service 에서 사용자 메시지로 변환

## 가장 중요한 코드 3개

```sql
-- (1) 통합 스키마
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    login_id VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,         -- bcrypt
    nickname VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE boards (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    view_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

```java
// (2) 본인 글만 삭제 (권한 + race condition 회피)
public int delete(Connection con, long boardId, long userId) throws SQLException {
    try (PreparedStatement ps = con.prepareStatement(
            "DELETE FROM boards WHERE id = ? AND user_id = ?")) {
        ps.setLong(1, boardId);
        ps.setLong(2, userId);
        return ps.executeUpdate();   // 0 = 권한 없음
    }
}
```

```java
// (3) Service 트랜잭션
public void deleteBoard(long boardId, long userId) throws SQLException {
    try (Connection con = ds.getConnection()) {
        con.setAutoCommit(false);
        try {
            commentDao.deleteByBoard(con, boardId);
            if (boardDao.delete(con, boardId, userId) == 0)
                throw new ForbiddenException("권한 없음");
            con.commit();
        } catch (Exception e) {
            con.rollback();
            throw e;
        } finally {
            con.setAutoCommit(true);
        }
    }
}
```

## 면접 한 줄 답변
- **레이어 분리가 왜?** → 한 레이어 교체 시 다른 곳 영향 X. MyBatis → JPA 갈아끼울 때 컨트롤러 그대로.
- **OFFSET 990 이 느린 이유?** → DB 가 990 행 모두 읽고 버림. 키셋 페이지네이션 (`WHERE id < ?`) 으로 일정 속도.
- **트랜잭션 경계는 어디?** → Service. Servlet 은 HTTP, DAO 는 SQL, 트랜잭션은 비즈니스.
- **패스워드 왜 bcrypt?** → 단방향 + salt 내장 + 느림 (brute-force 방어). MD5/SHA-1 은 너무 빠름.

---

# 2. Quick Reference (실무 복붙)

## 레이어 책임

| 레이어 | 책임 | 절대 금지 |
|--|--|--|
| **Servlet** | HTTP 파싱·세션·redirect | SQL 직접, 비즈니스 로직 |
| **Service** | 트랜잭션, 권한, 여러 DAO 조합 | HTTP 의존 (HttpServletRequest 받지 X) |
| **DAO** | SQL 실행, ResultSet → 객체 | 비즈니스 분기 |
| **Model** | DTO/Entity | 로직 |

## 핵심 쿼리

```sql
-- 페이지네이션 + 작성자 JOIN
SELECT b.id, b.title, b.view_count, b.created_at, u.nickname AS writer
FROM   boards b JOIN users u ON u.id = b.user_id
ORDER BY b.id DESC LIMIT ? OFFSET ?;

-- 검색 (LIKE)
SELECT * FROM boards
WHERE  title LIKE ? OR content LIKE ?
ORDER BY id DESC LIMIT ?;

-- 조회수 (원자적)
UPDATE boards SET view_count = view_count + 1 WHERE id = ?;

-- 본인 글만 삭제
DELETE FROM boards WHERE id = ? AND user_id = ?;
```

## 키셋 페이지네이션 (큰 데이터)

```sql
-- 첫 페이지
SELECT * FROM boards ORDER BY id DESC LIMIT 10;

-- 다음 페이지 (lastId = 12340)
SELECT * FROM boards
WHERE  id < 12340
ORDER BY id DESC LIMIT 10;
```

## 패스워드 bcrypt

```java
// Spring Security
PasswordEncoder encoder = new BCryptPasswordEncoder();

// 가입
String hashed = encoder.encode("user-password");
// $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy

// 로그인
boolean ok = encoder.matches(input, hashed);
```

## UNIQUE 위반 -> 사용자 메시지

```java
public void signup(User user) {
    try {
        userDao.insert(user);
    } catch (SQLIntegrityConstraintViolationException e) {
        if (e.getMessage().contains("login_id")) {
            throw new DuplicateLoginIdException("이미 사용 중인 ID");
        }
        throw e;
    }
}
```

## 조회수 race condition

```java
// 안 좋은 예 - READ-MODIFY-WRITE
Board b = boardDao.findById(id);
b.setViewCount(b.getViewCount() + 1);     // 동시 접속 시 손실
boardDao.update(b);

// 좋은 예 - 원자적
UPDATE boards SET view_count = view_count + 1 WHERE id = ?;
```

## 쿠키 중복 조회 방지

```java
String cookieName = "viewed_" + boardId;
if (Arrays.stream(req.getCookies()).noneMatch(c -> c.getName().equals(cookieName))) {
    boardDao.incrementView(boardId);
    Cookie c = new Cookie(cookieName, "1");
    c.setMaxAge(24 * 60 * 60);
    resp.addCookie(c);
}
```

## 트랜잭션 격리 수준

| 수준 | Dirty | Non-Repeat | Phantom |
|--|--|--|--|
| READ UNCOMMITTED | O | O | O |
| READ COMMITTED (PG/Oracle 기본) | X | O | O |
| **REPEATABLE READ (MySQL 기본)** | X | X | O |
| SERIALIZABLE | X | X | X |

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| 글 삭제 시 댓글 안 지움 | FK `ON DELETE CASCADE` + 트랜잭션 |
| OFFSET 깊을수록 느림 | 키셋 페이지네이션 |
| SELECT 후 user_id 자바 비교 | `WHERE id=? AND user_id=?` |
| setAutoCommit(false) + catch 없음 | rollback 안 됨, 명시적 catch |
| UNIQUE 위반 raw 메시지 노출 | Service 에서 사용자 메시지 |
| 패스워드 평문 | bcrypt + VARCHAR(255) |
| 조회수 READ-MODIFY-WRITE | 원자적 UPDATE |
| LIKE '%k%' 인덱스 미사용 | FULLTEXT INDEX 또는 Elasticsearch |

## DB 느려졌을 때 진단 순서

```
1. Slow Query Log + EXPLAIN
2. 인덱스 추가 (WHERE/JOIN/ORDER BY)
3. N+1 query 제거 (JOIN FETCH)
4. SELECT * 제거 + keyset 페이지네이션
5. Redis 캐시 (자주 읽고 안 바뀌는 데이터)
6. 읽기 Replica
7. 샤딩 (최후)
```

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
DB 관통 PJT (43p)
│
├── [A] 통합 스키마
│   ├── users (login_id UNIQUE, password bcrypt)
│   ├── boards (FK user_id ON DELETE CASCADE)
│   └── comments (FK board_id, user_id)
│
├── [B] 레이어 분리
│   ├── Servlet (HTTP)
│   ├── Service (트랜잭션, 권한)
│   ├── DAO (SQL)
│   └── Model (DTO/Entity)
│
├── [C] 핵심 쿼리
│   ├── 목록 + JOIN (작성자 닉네임)
│   ├── 검색 (LIKE)
│   ├── 조회수 원자 UPDATE
│   └── 본인 글 삭제 (WHERE id + user_id)
│
├── [D] 페이지네이션
│   ├── OFFSET (간단, 깊으면 느림)
│   └── 키셋 (WHERE id < ?, 일정)
│
├── [E] 보안
│   ├── bcrypt (PasswordEncoder)
│   ├── UNIQUE 위반 사용자 메시지
│   ├── XSS (c:out, 자동 escape)
│   └── SQL Injection (PreparedStatement)
│
├── [F] 동시성
│   ├── 조회수 원자 UPDATE
│   ├── 쿠키 중복 방지
│   └── 트랜잭션 격리 수준
│
└── [G] 성능
    ├── 인덱스 (created_at DESC)
    ├── N+1 query 제거 (JOIN)
    ├── 캐시 (Redis)
    └── 슬레이브 Replica
```

## 학습 진도 체크리스트

### A. 스키마·레이어
- [ ] users / boards / comments 통합 스키마
- [ ] FK CASCADE 효과
- [ ] Servlet / Service / DAO 책임

### B. 쿼리
- [ ] JOIN 목록 + 작성자 닉네임
- [ ] LIKE 검색 + 와일드카드
- [ ] 조회수 원자 UPDATE

### C. 페이지네이션
- [ ] LIMIT + OFFSET
- [ ] 키셋 페이지네이션 (큰 데이터)
- [ ] COUNT(*) 전체 + 페이지 데이터

### D. 보안
- [ ] bcrypt 적용
- [ ] UNIQUE 위반 → 사용자 메시지
- [ ] 본인 글 권한 (WHERE id + user_id)

### E. 트랜잭션
- [ ] Service 의 try-catch-rollback
- [ ] 격리 수준 4가지
- [ ] FK CASCADE + 트랜잭션 조합

### F. 운영
- [ ] Slow Query Log
- [ ] EXPLAIN 으로 인덱스 검증
- [ ] N+1 제거

## 연관 강의

```
Web Back 1~5강    -> Servlet, JSP, Cookie/Session, EL/JSTL, Filter
DB 1~5강           -> SELECT, DDL, JOIN, JDBC
6강 관통 PJT       <- 현재 위치
Framework 1~11강   -> Spring MVC + MyBatis 로 재구현
```

→ 다음 (Framework Back) 에서 **Spring 으로 같은 게시판 재구현**.
