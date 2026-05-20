# DB 관통 PJT — Web Backend × DB 통합

> **이 노트는 무엇인가**: Web Backend(1~5강) + DB(1~5강) 모두 합쳐 **DB 기반 게시판** 완성하는 통합 프로젝트.
> **왜 짧은가**: 새 개념 없음. "각 강의 조각이 한 앱에서 어떻게 맞물리는가" 확인.

---

## 들어가기 전에

- Web Backend 1~5강 + DB 1~5강 완료.
- MySQL 설치, 스키마 생성 권한.

---

## 목표

이전 Back 종합 실습의 인메모리 `BoardStore` 를 **실제 DB** 로 대체.

**기능**: 회원가입/로그인/로그아웃(세션), 게시판 목록(페이지네이션+검색), 글 CRUD(본인만), 댓글, 조회수.

---

## 스키마

```sql
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    login_id VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
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
CREATE TABLE comments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    board_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_boards_created ON boards(created_at DESC);
```

---

## 레이어 분리

```
[Servlet] → [Service] → [DAO] → [DB]
  HTTP       비즈니스    SQL
```

- Servlet: 요청 파싱·세션·redirect
- Service: 트랜잭션·여러 DAO 조합
- DAO: SQL + ResultSet → 객체
- Model: 데이터 운반

댓글까지 들어가면 트랜잭션이 필요 → Service 가 빛난다.

---

## 핵심 쿼리

```sql
-- 페이지네이션 + 작성자 닉네임 JOIN
SELECT b.id, b.title, b.view_count, b.created_at, u.nickname AS writer
FROM boards b
JOIN users u ON u.id = b.user_id
ORDER BY b.id DESC LIMIT ? OFFSET ?;

-- 검색
SELECT * FROM boards
WHERE title LIKE ? OR content LIKE ?
ORDER BY id DESC LIMIT ?;

-- 조회수 증가
UPDATE boards SET view_count = view_count + 1 WHERE id = ?;

-- 본인 글만 삭제
DELETE FROM boards WHERE id = ? AND user_id = ?;
```

---

## DAO 예 — `BoardDao.findPage`

```java
public List<BoardListItem> findPage(int page, int size) throws SQLException {
    String sql = """
        SELECT b.id, b.title, b.view_count, b.created_at, u.nickname AS writer
        FROM boards b
        JOIN users u ON u.id = b.user_id
        ORDER BY b.id DESC
        LIMIT ? OFFSET ?""";
    try (Connection con = ds.getConnection();
         PreparedStatement ps = con.prepareStatement(sql)) {
        ps.setInt(1, size);
        ps.setInt(2, (page - 1) * size);
        try (ResultSet rs = ps.executeQuery()) {
            List<BoardListItem> out = new ArrayList<>();
            while (rs.next()) {
                out.add(new BoardListItem(
                    rs.getLong("id"), rs.getString("title"),
                    rs.getInt("view_count"),
                    rs.getTimestamp("created_at").toLocalDateTime(),
                    rs.getString("writer")));
            }
            return out;
        }
    }
}
```

---

## Service — 트랜잭션 예

```java
public void deleteBoard(long boardId, long userId) throws SQLException {
    Connection con = ds.getConnection();
    con.setAutoCommit(false);
    try {
        commentDao.deleteByBoard(con, boardId);
        int affected = boardDao.delete(con, boardId, userId);
        if (affected == 0) throw new IllegalStateException("권한 없음");
        con.commit();
    } catch (Exception e) {
        con.rollback();
        throw e;
    } finally {
        con.setAutoCommit(true);
        con.close();
    }
}
```

FK CASCADE 쓰면 첫 줄 생략 가능. 트랜잭션 익히기 위해 명시.

---

## 체크리스트

- [ ] 회원가입 `UNIQUE` 위반 → 사용자 친화 메시지
- [ ] 패스워드 bcrypt 해시 (평문 금지)
- [ ] 로그인 후 `req.changeSessionId()`
- [ ] 페이지네이션 동작
- [ ] 수정·삭제는 작성자 본인만 (Service 에서 userId 검증)
- [ ] 조회수 쿠키로 중복 방지
- [ ] `serverTimezone=Asia/Seoul`
- [ ] 모든 DAO try-with-resources
- [ ] 모든 SQL PreparedStatement

---

## 자가점검

1. 글 삭제 시 댓글 안 지워지는 버그 의심처?
2. 페이지 100 (페이지당 10건) OFFSET 은? 100만 행에서 느린 이유와 대안?
3. 본인 글만 삭제 로직을 `WHERE id=? AND user_id=?` 로 처리 시 장점?
4. `setAutoCommit(false)` 후 catch 없으면?

<details><summary>풀이</summary>

1. FK `ON DELETE CASCADE` 누락 OR 트랜잭션 안 묶음 OR `comments.board_id` FK 자체 누락.
2. OFFSET 990. DB 가 990 행 스킵하느라 전부 스캔. 대안: **키셋 페이지네이션** (`WHERE id < ? ORDER BY id DESC LIMIT 10`).
3. DB 한 줄로 권한 검증 → "select 후 자바에서 user_id 비교" 의 race condition 회피 + 코드 간결.
4. 예외 시 rollback 안 함. finally 의 close 만 호출, 부분 commit 위험. 명시적 catch+rollback 필수.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1~5 표지·요구 | 목표 |
| p.6~15 스키마·레이어 | 스키마, 레이어 |
| p.16~30 핵심 쿼리·DAO | 쿼리, DAO |
| p.31~43 트랜잭션·체크 | Service, 체크리스트 |

_단독 학습 가능 노트._
