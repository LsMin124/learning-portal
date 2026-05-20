# MyBatis — 치트시트

> 29p 슬라이드 · XML/어노테이션 SQL 매퍼. JDBC 의 보일러플레이트 제거.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **MyBatis** = SQL 직접 작성 + ResultSet ↔ 객체 자동 매핑 (JDBC 보일러플레이트 제거)
2. **`@Mapper` 인터페이스** + XML 또는 어노테이션 SQL → Spring 이 구현체 자동 생성
3. **`#{}` (PreparedStatement) vs `${}` (문자열 치환)** - 사용자 입력은 무조건 `#{}`
4. **`resultMap`** 으로 컬럼 ↔ 필드 매핑 (혹은 `map-underscore-to-camel-case`)
5. **XML 매퍼** 가 복잡한 SQL에 유리, 단순한 건 어노테이션 (`@Select` `@Insert`)
6. **Spring Boot Starter** 가 SqlSessionFactory, MapperScan 자동 설정

## 가장 중요한 코드 3개

```java
// (1) Mapper 인터페이스
@Mapper
public interface BoardMapper {

    @Select("SELECT * FROM boards WHERE id = #{id}")
    Board findById(long id);

    @Insert("INSERT INTO boards (title, content) VALUES (#{title}, #{content})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Board board);

    // XML 매퍼와 같이 쓸 때
    List<Board> search(BoardSearchCond cond);
}
```

```xml
<!-- (2) XML 매퍼 (resources/mapper/BoardMapper.xml) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.ssafy.mapper.BoardMapper">

    <select id="search" parameterType="BoardSearchCond" resultType="Board">
        SELECT id, title, content, user_id AS userId, created_at AS createdAt
        FROM   boards
        <where>
            <if test="keyword != null and keyword != ''">
                AND title LIKE CONCAT('%', #{keyword}, '%')
            </if>
        </where>
        ORDER BY id DESC
        LIMIT #{size} OFFSET #{offset}
    </select>

</mapper>
```

```yaml
# (3) application.yml
mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.ssafy.dto
  configuration:
    map-underscore-to-camel-case: true       # user_id -> userId
    default-fetch-size: 100
    default-statement-timeout: 30
```

## 면접 한 줄 답변
- **MyBatis vs JDBC?** → JDBC 의 try-with-resources + RowMapper 보일러플레이트 제거. SQL 은 직접.
- **MyBatis vs JPA?** → MyBatis 는 SQL 직접 (한국 SI 인기), JPA 는 ORM (객체 중심, 자동 SQL).
- **`#{}` vs `${}`?** → `#{}` PreparedStatement (안전), `${}` 문자열 치환 (SQL Injection 위험, 동적 컬럼명에만).
- **resultMap 의 역할?** → 컬럼 ↔ 필드 매핑. 이름 다르거나 중첩 객체일 때.

---

# 2. Quick Reference (실무 복붙)

## 설정 (Spring Boot)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>
```

```yaml
# application.yml
mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.ssafy.dto
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: false
    default-statement-timeout: 30
```

## Mapper 인터페이스 (어노테이션)

```java
@Mapper
public interface BoardMapper {

    @Select("SELECT * FROM boards WHERE id = #{id}")
    Board findById(long id);

    @Select("SELECT * FROM boards ORDER BY id DESC LIMIT #{size}")
    List<Board> findRecent(@Param("size") int size);

    @Insert("INSERT INTO boards (title, content, user_id) VALUES (#{title}, #{content}, #{userId})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Board board);

    @Update("UPDATE boards SET title = #{title}, content = #{content} WHERE id = #{id}")
    int update(Board board);

    @Delete("DELETE FROM boards WHERE id = #{id} AND user_id = #{userId}")
    int delete(@Param("id") long id, @Param("userId") long userId);
}
```

## XML 매퍼 (복잡한 SQL)

```xml
<!-- resources/mapper/BoardMapper.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.ssafy.mapper.BoardMapper">

    <!-- SELECT -->
    <select id="findById" parameterType="long" resultType="Board">
        SELECT * FROM boards WHERE id = #{id}
    </select>

    <!-- 다중 결과 -->
    <select id="search" resultType="Board">
        SELECT * FROM boards
        <where>
            <if test="keyword != null">AND title LIKE CONCAT('%', #{keyword}, '%')</if>
            <if test="userId != null">AND user_id = #{userId}</if>
        </where>
        ORDER BY id DESC
        LIMIT #{size} OFFSET #{offset}
    </select>

    <!-- INSERT + 자동 ID -->
    <insert id="insert" parameterType="Board" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO boards (title, content, user_id)
        VALUES (#{title}, #{content}, #{userId})
    </insert>

    <!-- UPDATE -->
    <update id="update" parameterType="Board">
        UPDATE boards
        SET title = #{title}, content = #{content}
        WHERE id = #{id}
    </update>

    <!-- DELETE -->
    <delete id="delete">
        DELETE FROM boards WHERE id = #{id} AND user_id = #{userId}
    </delete>

</mapper>
```

## `#{}` vs `${}` (가장 중요!)

```xml
<!-- O - PreparedStatement (안전) -->
SELECT * FROM boards WHERE title = #{title}
<!-- 실행: SELECT * FROM boards WHERE title = ?  (PS 바인딩) -->

<!-- X - 문자열 치환 (SQL Injection) -->
SELECT * FROM boards WHERE title = '${title}'
<!-- 실행: SELECT * FROM boards WHERE title = 'value'  (텍스트 그대로) -->
```

| | `#{}` | `${}` |
|--|--|--|
| 방식 | PreparedStatement (`?`) | 문자열 치환 |
| 안전 | O (자동 escape) | X (Injection 위험) |
| 사용 | 모든 값 | 컬럼명·정렬 키워드 (화이트리스트 후) |

```xml
<!-- ${} 의 유일한 합법적 용도: 동적 컬럼명 -->
<choose>
    <when test="sortBy == 'view_count'">ORDER BY view_count</when>
    <when test="sortBy == 'created_at'">ORDER BY created_at</when>
    <otherwise>ORDER BY id</otherwise>
</choose>
```

## resultMap (복잡한 매핑)

```xml
<resultMap id="BoardResult" type="Board">
    <id     property="id"        column="id"/>
    <result property="title"     column="title"/>
    <result property="userId"    column="user_id"/>
    <result property="createdAt" column="created_at"/>

    <!-- 1:1 -->
    <association property="writer" javaType="User">
        <id     property="id"       column="u_id"/>
        <result property="nickname" column="u_nickname"/>
    </association>

    <!-- 1:N -->
    <collection property="comments" ofType="Comment">
        <id     property="id"   column="c_id"/>
        <result property="body" column="c_body"/>
    </collection>
</resultMap>

<select id="findWithWriter" resultMap="BoardResult">
    SELECT b.id, b.title, b.user_id, b.created_at,
           u.id AS u_id, u.nickname AS u_nickname
    FROM   boards b JOIN users u ON u.id = b.user_id
    WHERE  b.id = #{id}
</select>
```

→ map-underscore-to-camel-case 켜져 있으면 단순 매핑은 자동.

## 동적 SQL (간단한 것만, 자세한 건 9강)

```xml
<select id="search" resultType="Board">
    SELECT * FROM boards
    <where>
        <if test="keyword != null">AND title LIKE CONCAT('%', #{keyword}, '%')</if>
        <if test="userId != null">AND user_id = #{userId}</if>
    </where>
</select>
```

## 트랜잭션

```java
@Service @RequiredArgsConstructor
public class BoardService {
    private final BoardMapper mapper;

    @Transactional(readOnly = true)
    public List<Board> findAll() { return mapper.findAll(); }

    @Transactional
    public Board create(Board b) {
        mapper.insert(b);          // useGeneratedKeys -> b.id 자동 채워짐
        return b;
    }
}
```

## SqlSession 직접 사용 (드물게)

```java
@Component @RequiredArgsConstructor
public class BatchService {
    private final SqlSessionFactory sqlSessionFactory;

    public void batchInsert(List<Board> boards) {
        try (SqlSession session = sqlSessionFactory.openSession(ExecutorType.BATCH)) {
            BoardMapper mapper = session.getMapper(BoardMapper.class);
            for (Board b : boards) mapper.insert(b);
            session.commit();
        }
    }
}
```

## SQL 로깅

```yaml
logging.level:
  com.ssafy.mapper: DEBUG          # Mapper 인터페이스 경로
  org.mybatis: DEBUG
```

또는 P6Spy 라이브러리로 더 예쁜 SQL 로그.

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `${}` 에 사용자 입력 → SQL Injection | `#{}` 사용 |
| 컬럼명 ↔ 필드명 다름 → null | resultMap 또는 map-underscore-to-camel-case |
| @Mapper 누락 → 빈 안 생김 | `@Mapper` 또는 `@MapperScan` |
| XML 의 namespace 와 인터페이스 FQN 불일치 | namespace = 완전한 패키지 + 클래스명 |
| useGeneratedKeys 없이 ID 받으려 시도 | @Options(useGeneratedKeys = true, keyProperty = "id") |
| 여러 인자 `@Param` 누락 | 인자 2 개 이상이면 @Param 필수 |
| XML 의 `<` `>` 깨짐 | `&lt;` `&gt;` 또는 CDATA |
| Service 안 @Transactional 누락 | 변경 메서드엔 @Transactional |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
MyBatis (29p)
│
├── [A] 위치
│   ├── JDBC 위 추상화
│   ├── ORM (JPA) 보다 가벼움
│   ├── SQL 직접 작성
│   └── 한국 SI 표준
│
├── [B] Mapper 인터페이스
│   ├── @Mapper
│   ├── @MapperScan (옵션)
│   ├── @Select / @Insert / @Update / @Delete
│   └── @Options (useGeneratedKeys)
│
├── [C] XML 매퍼
│   ├── namespace = FQN
│   ├── <select> / <insert> / <update> / <delete>
│   ├── parameterType / resultType
│   └── resultMap (복잡한 매핑)
│
├── [D] 파라미터 바인딩
│   ├── #{} - PS (안전)
│   ├── ${} - 문자열 치환 (위험)
│   ├── @Param (다중 인자)
│   └── 객체 프로퍼티 자동
│
├── [E] resultMap
│   ├── id / result
│   ├── association (1:1)
│   ├── collection (1:N)
│   └── map-underscore-to-camel-case 자동
│
├── [F] 동적 SQL (9강에서 깊이)
│   ├── <if> / <where> / <set>
│   ├── <choose> / <when> / <otherwise>
│   ├── <foreach>
│   └── <sql> / <include>
│
└── [G] Spring 통합
    ├── mybatis-spring-boot-starter
    ├── SqlSessionFactory 자동
    ├── @Transactional
    └── 로깅 (logging.level.mapper)
```

## 학습 진도 체크리스트

### A. 위치
- [ ] MyBatis vs JDBC 차이
- [ ] MyBatis vs JPA 선택 기준

### B. Mapper
- [ ] @Mapper 인터페이스
- [ ] 어노테이션 SQL (@Select 등)
- [ ] @Options(useGeneratedKeys)

### C. XML
- [ ] mapper.xml 위치 + namespace
- [ ] parameterType / resultType
- [ ] resultMap 정의

### D. 바인딩
- [ ] `#{}` vs `${}` 의미
- [ ] @Param 다중 인자
- [ ] 객체 프로퍼티 자동 매핑

### E. resultMap
- [ ] association (1:1) JOIN
- [ ] collection (1:N) JOIN
- [ ] map-underscore-to-camel-case

### F. Spring 통합
- [ ] mybatis-spring-boot-starter
- [ ] @Transactional 위치
- [ ] application.yml 설정

## 연관 강의

```
DB 5강 JDBC          -> JDBC 표준 API
8강 MyBatis          <- 현재 위치
9강 MyBatis 동적쿼리 -> <if>/<where>/<choose>/<foreach>
11강 종합 실습       -> Spring + MyBatis 통합
```

→ 다음 (MyBatis 동적쿼리) 에서 **검색 조건이 동적인 쿼리 작성**.
