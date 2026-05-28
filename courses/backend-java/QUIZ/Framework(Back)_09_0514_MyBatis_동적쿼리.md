# MyBatis 동적 쿼리 - 퀴즈

> 14문항. 개념·적용·디버그·면접. `<if>` `<where>` `<choose>` `<foreach>` `<set>` `<sql>` 위주.

---

### Q1. (개념) `<where>` 가 `WHERE 1=1 <if>` 패턴보다 나은 점 2가지?

<details><summary>정답</summary>

**WHERE 1=1 패턴 (안 좋음)**:
```xml
SELECT * FROM boards
WHERE 1=1
<if test="title != null">AND title LIKE CONCAT('%', #{title}, '%')</if>
<if test="writerId != null">AND user_id = #{writerId}</if>
```

**`<where>` 패턴 (좋음)**:
```xml
SELECT * FROM boards
<where>
    <if test="title != null">AND title LIKE CONCAT('%', #{title}, '%')</if>
    <if test="writerId != null">AND user_id = #{writerId}</if>
</where>
```

**`<where>` 가 자동으로 해주는 것**:

1. **모든 `<if>` 가 false 면 WHERE 키워드 자체를 안 붙임** → `SELECT * FROM boards` 만 남음
2. **첫 번째 조건의 선두 `AND/OR` 를 자동 제거** → `WHERE AND title = ...` 같은 문법 에러 방지

→ MyBatis 가 동적 SQL 을 깔끔하게 해주는 가장 자주 쓰는 태그.

</details>

### Q2. (개념) `<choose>/<when>/<otherwise>` 와 여러 `<if>` 의 차이?

<details><summary>정답</summary>

| | 여러 `<if>` | `<choose>` |
|--|--|--|
| **의미** | 독립 조건 (모두 평가) | 상호 배타 (첫 매치만, switch) |
| **사용 예** | `if (title) ... if (writer) ...` | `switch (category) case 'NOTICE' ... case 'FREE' ...` |
| **default** | 없음 | `<otherwise>` |

```xml
<!-- 독립 조건: 여러 <if> -->
<where>
    <if test="title != null">AND title LIKE ...</if>
    <if test="writerId != null">AND user_id = ...</if>     <!-- 둘 다 적용 가능 -->
</where>

<!-- 상호 배타: <choose> -->
<choose>
    <when test="category == 'notice'">type = 'NOTICE'</when>
    <when test="category == 'free'">type = 'FREE'</when>
    <otherwise>type IN ('NOTICE', 'FREE')</otherwise>      <!-- 위 모두 false 일 때 -->
</choose>
```

→ "AND 로 조합" 이면 여러 `<if>`, "이 중 하나" 면 `<choose>`.

</details>

### Q3. (개념) `<set>` 태그의 동작과 UPDATE 에서의 이점?

<details><summary>정답</summary>

```xml
<update id="update">
    UPDATE boards
    <set>
        <if test="title != null">title = #{title},</if>
        <if test="content != null">content = #{content},</if>
        <if test="viewCount != null">view_count = #{viewCount},</if>
    </set>
    WHERE id = #{id}
</update>
```

**`<set>` 이 자동으로 해주는 것**:

1. **적어도 하나의 `<if>` 가 truthy** 면 `SET` 키워드 붙임
2. **마지막 컴마 자동 제거** → `SET title = ?, content = ?,` → `SET title = ?, content = ?`
3. 모두 false 면 → `UPDATE boards WHERE id = ?` (문법 에러 → 호출 자체를 막아야 함)

**왜 필요한가**: 자바에서 SQL 직접 만들면 마지막 컴마 제거 코드를 매번 작성 → 휴먼 에러.

```java
// 안 좋은 예 - 자바에서 처리
StringBuilder sql = new StringBuilder("UPDATE boards SET ");
if (title != null) sql.append("title = ?, ");
if (content != null) sql.append("content = ?, ");
sql.setLength(sql.length() - 2);   // 마지막 ", " 제거
```

</details>

### Q4. (개념) `<foreach>` 의 6개 속성 (collection, item, index, open, separator, close) 의 의미?

<details><summary>정답</summary>

```xml
<foreach
    collection="ids"     <!-- 매퍼 인자명 (List/Array) -->
    item="i"             <!-- 반복 변수명 (사용 시 #{i}) -->
    index="idx"          <!-- 인덱스 변수 (선택) -->
    open="("             <!-- 시작 문자 -->
    separator=","        <!-- 항목 구분자 -->
    close=")">           <!-- 끝 문자 -->
    #{i}
</foreach>
```

**collection 값 결정**:
- `List<Long> ids` (단일 인자) → `collection="list"` 또는 `@Param("ids")` 후 `"ids"`
- 객체 프로퍼티 → `collection="cond.ids"`

**예시 - IN 절**:
```xml
<select id="findByIds">
    SELECT * FROM boards
    WHERE id IN
    <foreach item="i" collection="ids" open="(" separator="," close=")">
        #{i}
    </foreach>
</select>
```
결과 SQL: `WHERE id IN (?, ?, ?)`

**예시 - 다중 INSERT**:
```xml
<insert id="bulkInsert">
    INSERT INTO tags (board_id, name) VALUES
    <foreach item="t" collection="tags" separator=",">
        (#{boardId}, #{t})
    </foreach>
</insert>
```
결과 SQL: `INSERT INTO tags (...) VALUES (?, ?), (?, ?), (?, ?)`

</details>

### Q5. (적용) 검색 조건 (keyword·writerId·from) 이 선택적으로 들어오는 동적 SELECT 작성.

<details><summary>정답</summary>

```xml
<select id="search" resultType="BoardListItem">
    SELECT b.id, b.title, b.view_count, b.created_at,
           u.nickname AS writer
    FROM   boards b
    JOIN   users u ON u.id = b.user_id
    <where>
        <if test="keyword != null and keyword != ''">
            AND (b.title LIKE CONCAT('%', #{keyword}, '%')
                 OR b.content LIKE CONCAT('%', #{keyword}, '%'))
        </if>
        <if test="writerId != null">
            AND b.user_id = #{writerId}
        </if>
        <if test="from != null">
            AND b.created_at &gt;= #{from}
        </if>
    </where>
    ORDER BY b.id DESC
    LIMIT #{size} OFFSET #{offset}
</select>
```

**핵심**:
- `<where>` 가 첫 `AND` 자동 제거
- `keyword != null and keyword != ''` - null 과 빈 문자열 둘 다 체크 (OGNL)
- `&gt;=` - XML 에선 `>` 가 escape (또는 CDATA)
- 검색 키워드는 `#{...}` (자동 escape) - 절대 `${...}` 금지

**호출**:
```java
BoardSearchCond cond = new BoardSearchCond();
cond.setKeyword("MyBatis");
cond.setSize(10);
cond.setOffset(0);
List<BoardListItem> list = boardMapper.search(cond);
```

</details>

### Q6. (적용) `<set>` 으로 title/content 중 변경된 컬럼만 UPDATE.

<details><summary>정답</summary>

```xml
<update id="updatePartial">
    UPDATE boards
    <set>
        <if test="title   != null">title   = #{title},</if>
        <if test="content != null">content = #{content},</if>
    </set>
    WHERE id = #{id} AND user_id = #{userId}
</update>
```

```java
// title 만 변경
Board b = new Board();
b.setId(123L);
b.setUserId(7L);
b.setTitle("새 제목");
// content 는 null -> SET 에서 제외
boardMapper.updatePartial(b);

// 실제 SQL: UPDATE boards SET title = ? WHERE id = ? AND user_id = ?
```

**왜 부분 UPDATE 가 좋은가**:
- 모든 컬럼 UPDATE → 클라이언트가 일부만 알아도 전체 보내야 함 (PUT vs PATCH 의 차이)
- 트리거·감사 로그 (Audit) 가 모든 컬럼을 변경으로 기록 → 노이즈

⚠️ **권한 검증**: WHERE 절에 `user_id = #{userId}` 포함 → 본인 글만 수정.

</details>

### Q7. (적용) `<foreach>` 로 IN 절 동적 처리 (회원 ID 리스트로 글 조회).

<details><summary>정답</summary>

```xml
<select id="findByUserIds" resultType="Board">
    SELECT * FROM boards
    WHERE user_id IN
    <foreach item="uid" collection="userIds" open="(" separator="," close=")">
        #{uid}
    </foreach>
    ORDER BY id DESC
</select>
```

```java
// Mapper interface
List<Board> findByUserIds(@Param("userIds") List<Long> userIds);

// 호출
List<Long> ids = List.of(1L, 5L, 7L);
List<Board> boards = boardMapper.findByUserIds(ids);
```

결과 SQL: `WHERE user_id IN (?, ?, ?)` + 자동 바인딩.

**`@Param` 필요한 이유**: 매퍼 인자가 1개여도 `collection="userIds"` 로 명시적 지정해야 안 헷갈림. 없으면 기본 이름 `"list"` 또는 `"collection"`.

**주의**: Q10 의 빈 컬렉션 함정 확인.

</details>

### Q8. (적용) `<foreach>` 로 태그 다중 INSERT (한 게시글에 여러 태그 동시).

<details><summary>정답</summary>

```xml
<insert id="bulkInsertTags">
    INSERT INTO tags (board_id, name) VALUES
    <foreach item="t" collection="tags" separator=",">
        (#{boardId}, #{t})
    </foreach>
</insert>
```

```java
void bulkInsertTags(@Param("boardId") long boardId,
                    @Param("tags") List<String> tags);

// 호출
tagMapper.bulkInsertTags(123L, List.of("MyBatis", "Spring", "동적쿼리"));
```

결과 SQL:
```sql
INSERT INTO tags (board_id, name) VALUES
    (?, ?),
    (?, ?),
    (?, ?)
```

**장점 (단일 INSERT vs 다중 INSERT)**:
- 네트워크 왕복 1회 (vs N회)
- 트랜잭션 1개로 일관성
- DB 인덱스 갱신 최적화

**한계**:
- MySQL `max_allowed_packet` 초과 시 에러 → 1000건씩 chunking
- ORM 의 batch insert 보다 느릴 수 있음 (JDBC `addBatch()`)

</details>

### Q9. (디버그) ORDER BY 컬럼명을 사용자 입력으로 받을 때 SQL Injection 방어?

<details><summary>정답</summary>

**문제**: ORDER BY 컬럼명은 **PreparedStatement 로 바인딩 불가능**. `#{}` 로 받으면 따옴표 붙어서 `ORDER BY 'view_count'` → 정렬 안 됨.

**위험 (절대 금지)**:
```xml
<!-- 안 좋은 예 -->
ORDER BY ${sortBy}      <!-- sortBy = "view_count; DROP TABLE boards--" 가능 -->
```

**해결 1: `<choose>` 화이트리스트 (XML 안)**:
```xml
<choose>
    <when test="sortBy == 'view_count'">ORDER BY view_count</when>
    <when test="sortBy == 'created_at'">ORDER BY created_at</when>
    <otherwise>ORDER BY id</otherwise>          <!-- 안전 기본값 -->
</choose>
```

**해결 2: 자바에서 검증 후 `${}`**:
```java
private static final Set<String> ALLOWED_SORT =
    Set.of("id", "created_at", "view_count");

public List<Board> search(BoardSearchCond cond) {
    if (cond.getSortBy() != null && !ALLOWED_SORT.contains(cond.getSortBy())) {
        throw new IllegalArgumentException("Invalid sortBy");
    }
    return boardMapper.search(cond);
}
```

**원칙**: `${}` 는 SQL 텍스트 그대로 삽입 → **사용자 입력에 절대 X**, 시스템 식별자 (테이블명·정렬 컬럼) 도 화이트리스트 검증 후만.

</details>

### Q10. (디버그) `<foreach>` 의 collection 이 빈 리스트일 때 발생하는 문제와 해결?

<details><summary>정답</summary>

```xml
<select id="findByIds">
    SELECT * FROM boards
    WHERE id IN
    <foreach item="i" collection="ids" open="(" separator="," close=")">
        #{i}
    </foreach>
</select>
```

**ids = [] 일 때 실행 SQL**:
```sql
SELECT * FROM boards WHERE id IN ()
-- MySQL: Syntax error or access violation
-- 빈 IN 절은 SQL 표준 위반
```

**해결 1: 빈 검사를 `<if>` 로 감싸기**:
```xml
<where>
    <if test="ids != null and ids.size() > 0">
        AND id IN
        <foreach item="i" collection="ids" open="(" separator="," close=")">
            #{i}
        </foreach>
    </if>
</where>
```

**해결 2: 자바에서 사전 체크 + early return**:
```java
public List<Board> findByIds(List<Long> ids) {
    if (ids == null || ids.isEmpty()) return Collections.emptyList();
    return boardMapper.findByIds(ids);
}
```

**해결 3: 더미 값 사용 (덜 권장)**:
```sql
WHERE id IN (-1, ...)   -- 매칭 안 됨
```

→ 안전: **빈 컬렉션은 SQL 호출 자체를 안 함**.

</details>

### Q11. (디버그) OGNL 표현식 - null/empty 체크와 `and/or` 키워드.

<details><summary>정답</summary>

MyBatis 의 `test` 속성은 **OGNL (Object Graph Navigation Language)** 사용.

| 자바 | OGNL |
|--|--|
| `&&` | `and` (또는 `&amp;&amp;` XML escape) |
| `&#124;&#124;` | `or` |
| `==` | `==` 또는 `eq` |
| `!=` | `!=` 또는 `neq` |
| `null` | `null` |
| `""` | `''` |

**null + empty 체크 (가장 흔함)**:
```xml
<if test="keyword != null and keyword != ''">
    AND title LIKE ...
</if>
```

**객체 프로퍼티 접근**:
```xml
<if test="user.role == 'ADMIN'">
    ...
</if>
```

**컬렉션 크기**:
```xml
<if test="ids != null and ids.size() > 0">     <!-- Java List.size() -->
```

**자주 하는 실수**:
- `keyword != null && keyword != ''` → XML 에서 `&` 가 escape 필요 → `and` 사용 권장
- `keyword.equals('foo')` → `keyword == 'foo'` 로 OK
- 문자열에 큰따옴표 → 작은따옴표 사용 (`'foo'`)

</details>

### Q12. (디버그) XML 에서 `<` (less than) 이 깨지는 이유와 해결?

<details><summary>정답</summary>

**문제**:
```xml
<if test="age < 20">       <!-- XML 파서가 < 를 태그 시작으로 오해 -->
    AND group = 'TEEN'
</if>
<!-- 또는 SQL 안에서 -->
WHERE created_at < #{end}
```

**XML 파싱 에러**: `The content of elements must consist of well-formed character data...`

**해결 1: HTML escape 엔티티**:
```xml
<if test="age &lt; 20">
    AND group = 'TEEN'
</if>

WHERE created_at &lt; #{end}
```

| 문자 | escape |
|--|--|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| `'` | `&apos;` |

**해결 2: CDATA 블록 (긴 SQL 에 유리)**:
```xml
<![CDATA[
    SELECT * FROM boards
    WHERE created_at < #{end} AND view_count > 100
]]>
```

CDATA 안은 XML 파서가 무시 → escape 불필요.

**선택**:
- 한두 글자만 깨질 때 → `&lt;` `&gt;`
- 긴 SQL 블록 → CDATA

</details>

### Q13. (적용) `<sql>` + `<include>` 로 공통 컬럼 정의 재사용.

<details><summary>정답</summary>

```xml
<!-- 공통 SQL 조각 정의 -->
<sql id="boardColumns">
    b.id, b.title, b.content, b.view_count, b.created_at, b.user_id
</sql>

<sql id="boardJoin">
    FROM boards b
    JOIN users u ON u.id = b.user_id
</sql>

<!-- 재사용 -->
<select id="findById" resultType="Board">
    SELECT <include refid="boardColumns"/>, u.nickname AS writer
    <include refid="boardJoin"/>
    WHERE b.id = #{id}
</select>

<select id="findAll" resultType="Board">
    SELECT <include refid="boardColumns"/>, u.nickname AS writer
    <include refid="boardJoin"/>
    ORDER BY b.id DESC
</select>
```

**효과**:
- 컬럼 추가 시 한 곳만 수정 (DRY)
- 모든 메서드가 같은 컬럼 보장 → DTO 매핑 일관성
- 가독성 ↑

**Property 전달**:
```xml
<sql id="orderBy">
    ORDER BY ${col} ${dir}
</sql>

<select id="search">
    SELECT * FROM boards
    <include refid="orderBy">
        <property name="col" value="id"/>
        <property name="dir" value="DESC"/>
    </include>
</select>
```

⚠️ `${}` 는 SQL Injection 위험 → property 도 화이트리스트 검증 후 사용.

</details>

### Q14. (면접) "MyBatis 동적 SQL vs JPA Criteria / QueryDSL 의 차이?"

<details><summary>정답</summary>

| | MyBatis 동적 SQL | JPA Criteria | QueryDSL |
|--|--|--|--|
| **방식** | XML 안의 `<if>/<choose>` | 자바 API (CriteriaBuilder) | 자바 DSL (Q클래스) |
| **타입 안전** | X (런타임 오타) | O | O |
| **가독성** | 중간 (XML 친숙) | 매우 낮음 (장황) | 매우 높음 |
| **러닝 커브** | 낮음 | 높음 | 중간 |
| **SQL 제어** | 직접 작성 | 추상화 (생성된 SQL 예측 어려움) | 추상화 + 옵션 풍부 |

**예시 - 같은 검색 쿼리**:

**MyBatis**:
```xml
<select id="search">
    SELECT * FROM boards
    <where>
        <if test="keyword != null">AND title LIKE CONCAT('%', #{keyword}, '%')</if>
        <if test="writerId != null">AND user_id = #{writerId}</if>
    </where>
</select>
```

**JPA Criteria** (장황):
```java
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<Board> q = cb.createQuery(Board.class);
Root<Board> b = q.from(Board.class);
List<Predicate> preds = new ArrayList<>();
if (keyword != null) preds.add(cb.like(b.get("title"), "%" + keyword + "%"));
if (writerId != null) preds.add(cb.equal(b.get("userId"), writerId));
q.where(preds.toArray(new Predicate[0]));
return em.createQuery(q).getResultList();
```

**QueryDSL** (깔끔):
```java
QBoard b = QBoard.board;
return queryFactory.selectFrom(b)
    .where(
        keywordContains(keyword),
        writerEq(writerId)
    )
    .fetch();

private BooleanExpression keywordContains(String k) {
    return k != null ? QBoard.board.title.contains(k) : null;
}
```

**선택 가이드**:
- **DBA 와 협업, 복잡한 SQL, 한국 SI** → **MyBatis** (정밀 SQL 제어 + 한국 시장 압도적)
- **객체 중심 도메인 + 빠른 개발** → **JPA + QueryDSL**
- **JPA 만 쓰지 마라** → Criteria 는 너무 장황. QueryDSL 필수 동반.

**BOOTCAMP 커리큘럼**: MyBatis 우선 (한국 SI 시장 현실).

</details>
