# MyBatis 동적 쿼리 — `<if>`, `<choose>`, `<foreach>`, `<where>`

> **이 강의는 무엇인가**: 실행 시점 입력값에 따라 SQL 구조 자체를 다르게 만드는 **동적 SQL**.
> **왜 배우는가**: 검색 조건 5개 중 3개만, 정렬 컬럼 가변, IN 절 가변 길이 — 자바 String 합치기 지옥을 한 페이지 XML 로.

---

## 들어가기 전에

- **선수**: MyBatis 기본 (8강).

---

## 핵심 개념

### 1. `<if>` — 조건부 절

```xml
<select id="search" resultType="Board">
  SELECT * FROM boards
  WHERE 1 = 1
  <if test="title != null and title != ''">
    AND title LIKE CONCAT('%', #{title}, '%')
  </if>
  <if test="writerId != null">AND user_id = #{writerId}</if>
</select>
```

`1 = 1` 트릭 — `<if>` 모두 false 일 때 WHERE 안 비도록.

### 2. `<where>` — 똑똑한 WHERE

```xml
<select id="search">
  SELECT * FROM boards
  <where>
    <if test="title != null">AND title LIKE CONCAT('%', #{title}, '%')</if>
    <if test="writerId != null">AND user_id = #{writerId}</if>
  </where>
</select>
```

`<where>` 가: 모든 `<if>` false 면 WHERE 안 붙임, 첫 조건 선두 AND/OR 자동 제거. `1=1` 불필요.

### 3. `<choose>` / `<when>` / `<otherwise>` — switch

```xml
<choose>
  <when test="category == 'notice'">type = 'NOTICE'</when>
  <when test="category == 'free'">type = 'FREE'</when>
  <otherwise>type IN ('NOTICE','FREE')</otherwise>
</choose>
```

### 4. `<set>` — UPDATE 친구

```xml
<update id="update">
  UPDATE boards
  <set>
    <if test="title != null">title = #{title},</if>
    <if test="content != null">content = #{content},</if>
  </set>
  WHERE id = #{id}
</update>
```

`<set>` 이 적어도 하나 들어가야 SET 키워드 붙음 + 끝 컴마 자동 제거.

### 5. `<foreach>` — IN 절 / 다중 INSERT

```xml
<select id="findByIds">
  SELECT * FROM boards
  WHERE id IN
  <foreach item="i" collection="ids" open="(" separator="," close=")">
    #{i}
  </foreach>
</select>

<insert id="bulkInsert">
  INSERT INTO tags (board_id, name) VALUES
  <foreach item="t" collection="tags" separator=",">
    (#{boardId}, #{t})
  </foreach>
</insert>
```

`collection` = 매퍼 메서드 인자명.

### 6. `<sql>` / `<include>` — 재사용

```xml
<sql id="boardColumns">b.id, b.title, b.content, b.view_count, b.created_at</sql>

<select id="findById">
  SELECT <include refid="boardColumns"/> FROM boards b WHERE b.id = #{id}
</select>
```

### 7. XML escape

```xml
<if test="age &lt; 20">       <!-- < 는 &lt; -->
  AND group = 'TEEN'
</if>
```

CDATA 도 OK: `<![CDATA[ AND created_at < #{end} ]]>`.

---

## 코드 깊게 들여다보기

검색+정렬+페이지네이션 동적 쿼리:

```java
public class BoardSearchCond {
    private String keyword;
    private Long writerId;
    private LocalDate from;
    private String sortBy;       // "id" | "view_count" | "created_at"
    private String sortDir;      // "ASC" | "DESC"
    private int page = 1, size = 10;
}
```

```xml
<select id="search" resultType="BoardListItem">
  SELECT b.id, b.title, b.view_count, b.created_at, u.nickname AS writer
  FROM boards b
  JOIN users u ON u.id = b.user_id
  <where>
    <if test="keyword != null and keyword != ''">
      AND (b.title LIKE CONCAT('%', #{keyword}, '%')
           OR b.content LIKE CONCAT('%', #{keyword}, '%'))
    </if>
    <if test="writerId != null">AND b.user_id = #{writerId}</if>
    <if test="from != null">AND b.created_at &gt;= #{from}</if>
  </where>
  <choose>
    <when test="sortBy == 'view_count'">ORDER BY b.view_count</when>
    <when test="sortBy == 'created_at'">ORDER BY b.created_at</when>
    <otherwise>ORDER BY b.id</otherwise>
  </choose>
  <choose>
    <when test="sortDir == 'ASC'">ASC</when>
    <otherwise>DESC</otherwise>
  </choose>
  LIMIT #{size} OFFSET #{offset}
</select>
```

ORDER BY 컬럼명은 PS 못 묶음 → `<choose>` 화이트리스트로 안전. `${sortBy}` 로 받으면 SQL Injection.

---

## 실전 패턴 / 자주 빠지는 함정

- ❌ `WHERE 1=1` 수동 → 가독성 ↓.
  ✅ `<where>`.
- ❌ `${}` 로 컬럼명·정렬 키워드 → SQL Injection.
  ✅ `<choose>` + 화이트리스트.
- ❌ `<foreach>` 빈 컬렉션 → `IN ()` 문법 에러.
  ✅ 빈 검사 후 호출.
- ❌ OGNL 문법 헷갈림 (`==`, `and`, `or`, `null`).
  ✅ 공식 문법 참고.
- ❌ XML escape 누락 → `<` 깨짐.
  ✅ `&lt;` 또는 CDATA.

---

## 다음 강의로 가기 전 자가점검

1. `<where>` 가 `WHERE 1=1` 보다 좋은 점?
2. ORDER BY 컬럼명을 안전하게 동적으로 받는 법?
3. `<foreach>` 의 `collection` 속성에 들어가는 것?
4. `<set>` 의 마지막 컴마 처리?

<details><summary>풀이</summary>

1. 모든 `<if>` false 면 WHERE 안 붙음. 첫 AND/OR 자동 제거.
2. `<choose>` + 화이트리스트, `otherwise` 안전 기본값. `${}` 금지.
3. 매퍼 메서드 인자명. `@Param("ids")` 또는 객체 프로퍼티명.
4. 자동 제거.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1~5 표지 | 들어가기 전에 |
| p.6~12 if/where | §1, §2 |
| p.13~18 choose/set | §3, §4 |
| p.19~24 foreach/sql | §5, §6 |
| p.25 escape | §7 |

_단독 학습 가능 노트._
