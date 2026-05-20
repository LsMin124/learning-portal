# MyBatis 동적 쿼리 — 치트시트

> 25p 슬라이드 · `<if>` `<where>` `<choose>` `<foreach>` `<set>` `<sql>`.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **`<where>`** 가 첫 AND 자동 제거 + 모든 if 가 false 면 WHERE 생략
2. **`<set>`** UPDATE 끝 컴마 자동 제거
3. **`<choose>/<when>/<otherwise>`** = switch (상호 배타)
4. **`<foreach>`** IN 절·다중 INSERT (collection, item, separator, open/close)
5. **`<sql>`+ `<include>`** 공통 SQL 조각 재사용
6. **ORDER BY 컬럼명은 `<choose>` 화이트리스트** (`${}` 사용자 입력 금지)

## 가장 중요한 코드 3개

```xml
<!-- (1) 검색 (where + if) -->
<select id="search" resultType="Board">
    SELECT * FROM boards
    <where>
        <if test="keyword != null and keyword != ''">
            AND (title LIKE CONCAT('%', #{keyword}, '%')
                 OR content LIKE CONCAT('%', #{keyword}, '%'))
        </if>
        <if test="userId != null">AND user_id = #{userId}</if>
        <if test="from != null">AND created_at &gt;= #{from}</if>
    </where>
    <choose>
        <when test="sortBy == 'view_count'">ORDER BY view_count DESC</when>
        <otherwise>ORDER BY id DESC</otherwise>
    </choose>
    LIMIT #{size} OFFSET #{offset}
</select>
```

```xml
<!-- (2) 부분 UPDATE (set) -->
<update id="updatePartial">
    UPDATE boards
    <set>
        <if test="title   != null">title   = #{title},</if>
        <if test="content != null">content = #{content},</if>
    </set>
    WHERE id = #{id} AND user_id = #{userId}
</update>
```

```xml
<!-- (3) IN 절 (foreach) -->
<select id="findByIds" resultType="Board">
    SELECT * FROM boards
    WHERE id IN
    <foreach item="i" collection="ids" open="(" separator="," close=")">
        #{i}
    </foreach>
</select>
```

## 면접 한 줄 답변
- **`<where>` 가 `WHERE 1=1` 보다 좋은 점?** → 모든 if false 면 WHERE 생략 + 첫 AND/OR 자동 제거.
- **`<choose>` vs 여러 `<if>`?** → 상호 배타 (switch) → choose, 독립 조건 → if.
- **`${sortBy}` 의 위험?** → SQL Injection. ORDER BY 같은 정적 식별자는 `<choose>` 화이트리스트.
- **`<foreach>` 빈 컬렉션?** → `IN ()` 문법 에러. if 로 빈 검사 또는 자바에서 early return.

---

# 2. Quick Reference (실무 복붙)

## `<if>` + `<where>`

```xml
<!-- 안 좋은 예 (WHERE 1=1 트릭) -->
SELECT * FROM boards
WHERE 1=1
<if test="title != null">AND title LIKE CONCAT('%', #{title}, '%')</if>

<!-- 좋은 예 (<where>) -->
SELECT * FROM boards
<where>
    <if test="title != null">AND title LIKE CONCAT('%', #{title}, '%')</if>
    <if test="userId != null">AND user_id = #{userId}</if>
</where>
```

**`<where>` 자동화**:
1. 모든 if 가 false → WHERE 키워드 생략
2. 첫 조건의 앞 AND/OR 자동 제거

## `<set>` (부분 UPDATE)

```xml
<update id="update">
    UPDATE boards
    <set>
        <if test="title   != null">title   = #{title},</if>
        <if test="content != null">content = #{content},</if>
        <if test="viewCount != null">view_count = #{viewCount},</if>
    </set>
    WHERE id = #{id}
</update>
```

→ 끝의 컴마 자동 제거.

## `<choose>` / `<when>` / `<otherwise>` (switch)

```xml
<choose>
    <when test="category == 'notice'">type = 'NOTICE'</when>
    <when test="category == 'free'">type = 'FREE'</when>
    <otherwise>type IN ('NOTICE', 'FREE')</otherwise>
</choose>

<!-- ORDER BY 화이트리스트 -->
<choose>
    <when test="sortBy == 'view_count'">ORDER BY view_count</when>
    <when test="sortBy == 'created_at'">ORDER BY created_at</when>
    <otherwise>ORDER BY id</otherwise>
</choose>
```

## `<foreach>` (IN 절 + 다중 INSERT)

```xml
<!-- IN 절 -->
<select id="findByIds">
    SELECT * FROM boards
    WHERE id IN
    <foreach item="i" collection="ids" open="(" separator="," close=")">
        #{i}
    </foreach>
</select>

<!-- 다중 INSERT -->
<insert id="bulkInsert">
    INSERT INTO tags (board_id, name) VALUES
    <foreach item="t" collection="tags" separator=",">
        (#{boardId}, #{t})
    </foreach>
</insert>
```

**6 속성**: `collection` (인자명) / `item` (반복 변수) / `index` (인덱스) / `open` / `separator` / `close`

## `<sql>` + `<include>` (재사용)

```xml
<sql id="boardColumns">
    b.id, b.title, b.content, b.view_count, b.created_at, b.user_id
</sql>

<select id="findById" resultType="Board">
    SELECT <include refid="boardColumns"/>, u.nickname AS writer
    FROM   boards b JOIN users u ON u.id = b.user_id
    WHERE  b.id = #{id}
</select>

<select id="findAll" resultType="Board">
    SELECT <include refid="boardColumns"/>
    FROM   boards b
    ORDER BY b.id DESC
</select>
```

## OGNL 표현식 (`test` 안)

| 자바 | OGNL |
|--|--|
| `&&` | `and` |
| `||` | `or` |
| `==` | `==` 또는 `eq` |
| `!=` | `!=` 또는 `neq` |
| `null` | `null` |
| 빈 문자열 | `''` (작은따옴표) |

```xml
<!-- 가장 자주 -->
<if test="keyword != null and keyword != ''">

<!-- 객체 프로퍼티 -->
<if test="user.role == 'ADMIN'">

<!-- 컬렉션 크기 -->
<if test="ids != null and ids.size() > 0">
```

## XML escape

```xml
<!-- 안 좋은 예 - XML 파서 에러 -->
<if test="age < 20">

<!-- 좋은 예 1: HTML escape -->
<if test="age &lt; 20">

<!-- 좋은 예 2: CDATA (긴 SQL) -->
<![CDATA[
    SELECT * FROM boards WHERE created_at < #{end}
]]>
```

| 문자 | escape |
|--|--|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |

## 빈 컬렉션 함정

```xml
<!-- ids 가 빈 리스트면 SELECT ... WHERE id IN () -> SQL 에러 -->
<select id="findByIds">
    SELECT * FROM boards
    WHERE id IN
    <foreach item="i" collection="ids" open="(" separator="," close=")">
        #{i}
    </foreach>
</select>
```

**해결 1**: 자바에서 early return
```java
public List<Board> findByIds(List<Long> ids) {
    if (ids == null || ids.isEmpty()) return List.of();
    return mapper.findByIds(ids);
}
```

**해결 2**: `<if>` 로 감싸기
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

## 검색+정렬+페이지네이션 완성형

```xml
<select id="search" resultType="BoardListItem">
    SELECT b.id, b.title, b.view_count, b.created_at, u.nickname AS writer
    FROM   boards b JOIN users u ON u.id = b.user_id
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

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `WHERE 1=1` 수동 | `<where>` 사용 |
| `${sortBy}` 사용자 입력 → Injection | `<choose>` 화이트리스트 |
| `<foreach>` 빈 컬렉션 → SQL 에러 | `<if>` 빈 검사 또는 자바 early return |
| OGNL `&&` → XML escape 에러 | `and` 사용 |
| `<` 깨짐 | `&lt;` 또는 CDATA |
| keyword 빈 문자열도 통과 | `keyword != null and keyword != ''` |
| `<set>` 컴마 직접 제거 시도 | `<set>` 자동 처리 신뢰 |
| `<sql>` property 사용자 입력 | property 도 화이트리스트 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
MyBatis 동적쿼리 (25p)
│
├── [A] <if>
│   ├── test 표현식 (OGNL)
│   ├── 독립 조건 (여러 if)
│   └── null + empty 체크
│
├── [B] <where>
│   ├── 첫 AND/OR 자동 제거
│   └── 모든 if false 면 WHERE 생략
│
├── [C] <set>
│   ├── UPDATE 끝 컴마 자동 제거
│   └── 모든 if false 면 SET 생략
│
├── [D] <choose> / <when> / <otherwise>
│   ├── switch 의미 (상호 배타)
│   ├── 첫 매치만
│   └── otherwise (default)
│
├── [E] <foreach>
│   ├── collection (인자명)
│   ├── item / index
│   ├── open / separator / close
│   ├── IN 절
│   └── 다중 INSERT
│
├── [F] <sql> + <include>
│   ├── 공통 컬럼 조각 재사용
│   └── property 전달
│
├── [G] OGNL 표현식
│   ├── ==, !=, and, or
│   ├── null / '' 비교
│   ├── 객체 프로퍼티
│   └── 컬렉션 size()
│
└── [H] 보안
    ├── #{} vs ${}
    ├── ORDER BY 화이트리스트
    └── XML escape
```

## 학습 진도 체크리스트

### A. 기본
- [ ] `<if>` test 표현식
- [ ] `<where>` 의 자동화 2가지
- [ ] OGNL null + empty 체크

### B. SET / CHOOSE
- [ ] `<set>` UPDATE 끝 컴마 제거
- [ ] `<choose>` 의 switch 의미
- [ ] ORDER BY 화이트리스트

### C. FOREACH
- [ ] 6 속성
- [ ] IN 절 작성
- [ ] 다중 INSERT
- [ ] 빈 컬렉션 함정

### D. 재사용
- [ ] `<sql>` + `<include>`
- [ ] property 전달
- [ ] 공통 컬럼 모듈화

### E. 보안
- [ ] `${}` 사용 금지 원칙
- [ ] 정렬 컬럼 화이트리스트
- [ ] XML escape

## 연관 강의

```
DB 4강 JOIN/SubQuery -> SQL 기본
8강 MyBatis          -> Mapper / XML
9강 MyBatis 동적쿼리  <- 현재 위치
11강 종합 실습       -> 통합 검색 화면
12강 REST API        -> 검색 API
```

→ 다음 (Spring 종합실습) 에서 **모든 모듈 통합 게시판**.
