# MyBatis — 개념 · 구성 요소 · Spring Boot 연동

> **이 강의는 무엇인가**: SQL 을 자바 코드와 분리해 XML/어노테이션으로 관리하고, 결과를 자동으로 객체에 매핑하는 SQL 매퍼 **MyBatis**. 순수 자바 사용 + Spring Boot 환경에서의 `@Mapper` 활용까지.
> **왜 배우는가**: JDBC 만 쓰면 `Connection/PreparedStatement/ResultSet/try-finally/close` 보일러플레이트가 50줄 넘는다. JPA 는 추상화가 너무 높아 SQL 제어가 어렵다. MyBatis 는 그 중간 — SQL 은 직접 쓰되 자바 코드는 깨끗. 한국 SI/SM 의 표준.

---

## 들어가기 전에

- **선수**: JDBC 강의 (Connection, PreparedStatement, ResultSet), SQL 기본 (SELECT/INSERT/UPDATE/DELETE), Spring DI, Lombok.
- **마인드셋**: "SQL 은 SQL 답게 쓰되 자바 코드는 비즈니스에 집중" 의 균형.

---

# Part A. MyBatis 개념

## 1. JDBC 만 쓸 때의 보일러플레이트

```java
// JDBC 만으로 게시글 단건 조회
public Board findById(int id) {
    Connection conn = null;
    PreparedStatement ps = null;
    ResultSet rs = null;
    Board board = null;
    try {
        conn = DriverManager.getConnection(URL, USER, PWD);
        ps = conn.prepareStatement("SELECT * FROM board WHERE id = ?");
        ps.setInt(1, id);
        rs = ps.executeQuery();
        if (rs.next()) {
            board = new Board();
            board.setId(rs.getInt("id"));
            board.setTitle(rs.getString("title"));
            board.setContent(rs.getString("content"));
            board.setWriter(rs.getString("writer"));
            board.setRegDate(rs.getTimestamp("reg_date").toLocalDateTime());
            board.setViewCnt(rs.getInt("view_cnt"));
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    } finally {
        try { if (rs != null) rs.close(); } catch (Exception e) {}
        try { if (ps != null) ps.close(); } catch (Exception e) {}
        try { if (conn != null) conn.close(); } catch (Exception e) {}
    }
    return board;
}
```

**문제 4가지**:
1. **30+ 줄 중 비즈니스 로직은 5줄** — 나머지는 자원 관리
2. **자원 누수 위험** — close 호출 누락 시 connection pool 고갈
3. **SQL 이 자바 문자열에 묻혀** 가독성·유지보수 ↓
4. **결과 매핑 수동** — `rs.getInt/getString` 일일이

## 2. MyBatis 가 풀어주는 것

```java
// MyBatis 로 같은 일
public interface BoardMapper {
    Board findById(int id);
}
```

```xml
<!-- BoardMapper.xml -->
<select id="findById" parameterType="int" resultType="Board">
    SELECT * FROM board WHERE id = #{id}
</select>
```

```java
Board b = sqlSession.selectOne("BoardMapper.findById", 42);
// 또는 (Spring Boot)
Board b = boardMapper.findById(42);
```

**얻는 것**:
- 자바 코드 1줄로 SQL 호출
- 자원 관리는 MyBatis 가 자동
- SQL 은 XML 에 격리 → DB 전문가·개발자 분업 가능
- 결과 자동 매핑 (`resultType="Board"` 면 컬럼명 ↔ 필드명 매칭)

## 3. MyBatis 의 위치 — JDBC ↔ JPA 사이

```
       JDBC                 MyBatis               JPA
       -----                --------              -----
   자바가 SQL 직접 작성     자바는 SQL ID 호출     자바가 객체만 다룸
   결과 매핑 수동           결과 자동 매핑          쿼리도 자동 생성
   -----------------       -------------         --------------
   추상화 낮음                                     추상화 높음
   SQL 통제 강함                                   SQL 통제 약함
```

| 비교 | JDBC | MyBatis | JPA |
|--|--|--|--|
| SQL 작성 | 직접 (자바 문자열) | 직접 (XML/Annotation) | 자동 또는 JPQL |
| 결과 매핑 | 수동 | 자동 | 자동 |
| 학습 곡선 | 낮음 | 중간 | 높음 |
| SQL 튜닝 자유도 | 최고 | 높음 | 낮음 |
| 한국 SI/SM 점유율 | 적음 | **압도적** | 증가 중 |

---

# Part B. MyBatis 구성 요소

## 4. 핵심 5가지

```
[자바 코드]
    | 호출
    ▼
SqlSession                       ← 작업 단위 (트랜잭션 흐름)
    | 만들어주는
    ▼
SqlSessionFactory                ← 팩토리 (싱글톤)
    | 만들어주는
    ▼
SqlSessionFactoryBuilder         ← 빌더 (XML 읽어서 팩토리 생성)
    | 읽음
    ▼
mybatis-config.xml               ← 전역 설정 (typeAliases, env)
    | 참조
    ▼
BoardMapper.xml                  ← SQL Mapper (실제 SQL 정의)
```

| 구성 요소 | 역할 |
|--|--|
| **SqlSessionFactoryBuilder** | XML 설정 읽어서 Factory 빌드 (앱 시작 시 1번) |
| **SqlSessionFactory** | SqlSession 객체 생성 팩토리 (싱글톤) |
| **SqlSession** | 실제 DB 작업 단위 — `selectOne`/`insert`/`update`/`delete` 호출 |
| **mybatis-config.xml** | 전역 설정 (typeAliases, datasource, mappers) |
| **Mapper XML** | SQL 정의 (`<select>`, `<insert>` 등) |

## 5. mybatis-config.xml — 전역 설정

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration
    PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <!-- 1) 타입 별칭 -->
    <typeAliases>
        <typeAlias type="com.example.dto.Board" alias="Board"/>
        <package name="com.example.dto"/>     <!-- 패키지 단위 -->
    </typeAliases>

    <!-- 2) 환경 (DataSource) -->
    <environments default="dev">
        <environment id="dev">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url"    value="jdbc:mysql://localhost:3306/db"/>
                <property name="username" value="user"/>
                <property name="password" value="pwd"/>
            </dataSource>
        </environment>
    </environments>

    <!-- 3) Mapper 등록 -->
    <mappers>
        <mapper resource="mappers/BoardMapper.xml"/>
        <package name="com.example.mapper"/>   <!-- 자동 스캔 -->
    </mappers>
</configuration>
```

**typeAliases** 의 역할: XML 에서 클래스 풀패키지명 대신 짧은 별칭 사용 (`com.example.dto.Board` → `Board`).

## 6. Mapper XML — SQL 정의

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
    PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.example.mapper.BoardMapper">

    <!-- 단건 조회 -->
    <select id="findById" parameterType="int" resultType="Board">
        SELECT id, title, content, writer,
               reg_date AS regDate, view_cnt AS viewCnt
        FROM board WHERE id = #{id}
    </select>

    <!-- 다건 조회 -->
    <select id="findAll" resultType="Board">
        SELECT * FROM board ORDER BY id DESC
    </select>

    <!-- 등록 (자동 생성 키 반환) -->
    <insert id="insert" parameterType="Board"
            useGeneratedKeys="true" keyProperty="id">
        INSERT INTO board(title, content, writer)
        VALUES (#{title}, #{content}, #{writer})
    </insert>

    <!-- 수정 -->
    <update id="update" parameterType="Board">
        UPDATE board SET title = #{title}, content = #{content}
        WHERE id = #{id}
    </update>

    <!-- 삭제 -->
    <delete id="delete" parameterType="int">
        DELETE FROM board WHERE id = #{id}
    </delete>

</mapper>
```

**핵심 속성**:
| 속성 | 의미 |
|--|--|
| `namespace` | Mapper 인터페이스의 풀패키지명 (Spring Boot 연동 시) |
| `id` | SQL 식별자 (Java 메서드명과 매칭) |
| `parameterType` | 입력 파라미터 타입 |
| `resultType` | 결과 타입 (단건/다건 모두 같은 속성) |
| `useGeneratedKeys` | AUTO_INCREMENT 키를 객체에 자동 set |

## 7. `#{}` vs `${}`

```xml
<!-- ✅ #{} - PreparedStatement 의 ? 바인딩 -->
<select id="findByEmail" parameterType="string" resultType="User">
    SELECT * FROM user WHERE email = #{email}
</select>
<!-- 실제 SQL: SELECT * FROM user WHERE email = ? -->

<!-- ❌ ${} - 문자열 그대로 치환 (SQL Injection 위험!) -->
<select id="findByColumn" resultType="User">
    SELECT * FROM user WHERE ${column} = #{value}
</select>
<!-- 실제 SQL: SELECT * FROM user WHERE email = ? -->
<!-- ${column} 에 "1 OR 1=1" 들어가면 모든 데이터 조회 가능 -->
```

**원칙**:
- **값**(이메일·이름·ID 등): **`#{}`**
- **칼럼명·테이블명 등 SQL 구조 자체**: `${}` (단, **반드시 화이트리스트 검증** 후)

---

# Part C. 순수 자바 + MyBatis

## 8. SqlSessionFactory 빌드 + 사용

```java
public class MyBatisTest {

    private static SqlSessionFactory factory;

    static {
        try (InputStream is = Resources.getResourceAsStream("mybatis-config.xml")) {
            factory = new SqlSessionFactoryBuilder().build(is);
        } catch (IOException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    public static void main(String[] args) {
        try (SqlSession session = factory.openSession()) {

            // 단건 조회
            Board b = session.selectOne("com.example.mapper.BoardMapper.findById", 1);
            System.out.println(b);

            // 다건 조회
            List<Board> list = session.selectList("com.example.mapper.BoardMapper.findAll");
            list.forEach(System.out::println);

            // 등록
            Board newBoard = new Board("제목", "내용", "writer1");
            session.insert("com.example.mapper.BoardMapper.insert", newBoard);
            session.commit();    // ⚠ 명시적 commit
            System.out.println("새 ID: " + newBoard.getId());
        }
    }
}
```

**주의 사항**:
- `SqlSessionFactory` 는 **싱글톤** (앱 시작 시 1번 빌드)
- `SqlSession` 은 **요청마다 새로** (try-with-resources 로 자동 close)
- `insert`/`update`/`delete` 는 **명시적 `commit()`** 필요 (또는 `openSession(true)` 로 autocommit)

## 9. Mapper 인터페이스 패턴 (권장)

순수 자바에서도 인터페이스로 호출하면 타입 안전:

```java
// 인터페이스 (메서드명이 XML 의 id 와 매칭)
public interface BoardMapper {
    Board findById(int id);
    List<Board> findAll();
    int insert(Board board);
}

// 사용
try (SqlSession session = factory.openSession()) {
    BoardMapper mapper = session.getMapper(BoardMapper.class);

    Board b = mapper.findById(1);                  // 타입 안전!
    List<Board> all = mapper.findAll();
}
```

`session.selectOne("..문자열..")` 대신 **컴파일 시점에 검증**되는 인터페이스 호출. 오타·타입 미스매치 컴파일 단계 잡힘.

---

# Part D. Spring Boot + MyBatis

## 10. 의존성 추가

```xml
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>

<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
</dependency>
```

`mybatis-spring-boot-starter` 가 자동으로:
- `SqlSessionFactory` 빈 등록
- `SqlSessionTemplate` 빈 등록 (스레드 안전한 SqlSession)
- `@Mapper` 자동 스캔

## 11. `application.properties` 설정

```properties
# DB
spring.datasource.url=jdbc:mysql://localhost:3306/db
spring.datasource.username=user
spring.datasource.password=pwd
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# MyBatis
mybatis.mapper-locations=classpath:mappers/**/*.xml
mybatis.type-aliases-package=com.example.dto
mybatis.configuration.map-underscore-to-camel-case=true   # 자동 카멜케이스 매핑
```

`map-underscore-to-camel-case=true` 의 효과:
- DB `reg_date` 컬럼 ↔ 자바 `regDate` 필드 자동 매칭
- XML 에서 `AS regDate` 별칭 불필요

## 12. `@Mapper` — 인터페이스만 작성하면 끝

```java
@Mapper
public interface BoardMapper {

    // XML 의 같은 id 와 매칭
    Board findById(int id);
    List<Board> findAll();
    int insert(Board board);
    int update(Board board);
    int delete(int id);

    // 또는 어노테이션으로 SQL 직접 (간단한 쿼리)
    @Select("SELECT count(*) FROM board")
    int count();
}
```

**자동 구현 동작**:
1. Spring Boot 가 `@Mapper` 스캔
2. MyBatis 가 인터페이스를 구현한 Proxy 객체 생성 (런타임)
3. 컨테이너에 빈으로 등록
4. Service 에서 `@Autowired` 또는 생성자 주입으로 사용

## 13. Service 에서 사용

```java
@Service
@RequiredArgsConstructor
@Transactional
public class BoardService {

    private final BoardMapper boardMapper;

    public List<Board> findAll() {
        return boardMapper.findAll();
    }

    public Board findById(int id) {
        Board b = boardMapper.findById(id);
        if (b == null) throw new NotFoundException("게시글 없음");
        return b;
    }

    public int create(Board board) {
        boardMapper.insert(board);
        return board.getId();    // useGeneratedKeys 로 자동 set 됨
    }

    public void update(Board board) {
        if (boardMapper.update(board) == 0) {
            throw new NotFoundException("수정 대상 없음");
        }
    }

    public void delete(int id) {
        boardMapper.delete(id);
    }
}
```

`@Transactional` 로 트랜잭션 자동 — `commit/rollback` 신경 안 써도 됨.

## 14. 한 개 이상의 파라미터 — `@Param`

```java
public interface BoardMapper {
    // 단일 파라미터 - 그대로 사용
    Board findById(int id);

    // 여러 파라미터 - @Param 필요
    List<Board> findByWriterAndCategory(@Param("writer") String writer,
                                          @Param("category") String category);
}
```

```xml
<select id="findByWriterAndCategory" resultType="Board">
    SELECT * FROM board
    WHERE writer   = #{writer}
      AND category = #{category}
</select>
```

`@Param("이름")` 없이 여러 파라미터 받으면 XML 에서 `#{0}`, `#{1}` 또는 `#{param1}`, `#{param2}` 로 접근 — 가독성 나빠서 **`@Param` 권장**.

---

## 15. 코드 깊게 — 게시판 풀스택

```java
// === DTO ===
@Data
public class Board {
    private int id;
    private String title;
    private String content;
    private String writer;
    private LocalDateTime regDate;
    private int viewCnt;
}

// === Mapper Interface ===
@Mapper
public interface BoardMapper {
    Board findById(int id);
    List<Board> findAll();
    int insert(Board board);
    int update(Board board);
    int delete(int id);
    int updateViewCnt(int id);
}
```

```xml
<!-- BoardMapper.xml -->
<mapper namespace="com.example.mapper.BoardMapper">

    <select id="findById" parameterType="int" resultType="Board">
        SELECT * FROM board WHERE id = #{id}
    </select>

    <select id="findAll" resultType="Board">
        SELECT * FROM board ORDER BY id DESC
    </select>

    <insert id="insert" parameterType="Board"
            useGeneratedKeys="true" keyProperty="id">
        INSERT INTO board(title, content, writer)
        VALUES (#{title}, #{content}, #{writer})
    </insert>

    <update id="update" parameterType="Board">
        UPDATE board SET title = #{title}, content = #{content}
        WHERE id = #{id}
    </update>

    <update id="updateViewCnt" parameterType="int">
        UPDATE board SET view_cnt = view_cnt + 1 WHERE id = #{id}
    </update>

    <delete id="delete" parameterType="int">
        DELETE FROM board WHERE id = #{id}
    </delete>

</mapper>
```

```java
// === Service ===
@Service
@RequiredArgsConstructor
@Transactional
public class BoardService {
    private final BoardMapper mapper;

    public List<Board> list() { return mapper.findAll(); }

    public Board view(int id) {
        Board b = mapper.findById(id);
        if (b == null) throw new NotFoundException();
        mapper.updateViewCnt(id);
        return b;
    }

    public int create(Board b) {
        mapper.insert(b);
        return b.getId();
    }
}

// === Controller ===
@Controller
@RequiredArgsConstructor
@RequestMapping("/board")
public class BoardController {
    private final BoardService service;

    @GetMapping
    public String list(Model m) {
        m.addAttribute("boards", service.list());
        return "board/list";
    }

    @GetMapping("/{id}")
    public String detail(@PathVariable int id, Model m) {
        m.addAttribute("board", service.view(id));
        return "board/detail";
    }

    @PostMapping
    public String create(@ModelAttribute Board b) {
        int id = service.create(b);
        return "redirect:/board/" + id;
    }
}
```

---

## 16. 실전 패턴 / 자주 빠지는 함정

### MyBatis 설정
- ❌ `mybatis-config.xml` 과 `application.properties` 양쪽에 설정 ✅ Spring Boot 는 properties 가 우선
- ❌ Mapper XML 위치를 잘못 지정 → 404 ✅ `mybatis.mapper-locations=classpath:mappers/**/*.xml`
- ❌ `map-underscore-to-camel-case` 안 켜면 `reg_date` ↔ `regDate` 매핑 실패 ✅ properties 에 명시

### SQL 작성
- ❌ `#{}` 와 `${}` 혼동 ✅ 값은 `#{}`, SQL 구조(칼럼명·정렬 방향) 만 `${}` + 화이트리스트
- ❌ `${}` 에 사용자 입력 직접 → SQL Injection ✅ 절대 금지, 화이트리스트 필수
- ❌ `SELECT *` 만 사용 ✅ 컬럼 명시 (성능 + 명세 명확)
- ❌ `useGeneratedKeys` 없이 INSERT 후 ID 가 0 ✅ `useGeneratedKeys="true" keyProperty="id"`

### Mapper 인터페이스
- ❌ XML 의 `namespace` 와 인터페이스 풀패키지명 불일치 ✅ 정확히 매칭
- ❌ XML 의 `id` 와 인터페이스 메서드명 불일치 ✅ 메서드명과 정확히 같아야
- ❌ 여러 파라미터에 `@Param` 누락 ✅ 명시
- ❌ `@Mapper` 누락 → 빈 등록 안 됨 ✅ 인터페이스에 부착

### 성능
- ❌ N+1 쿼리 (게시글 + 각각의 작성자 조회) ✅ JOIN 또는 `resultMap` 으로 한 번에
- ❌ 페이지네이션 없이 전체 조회 ✅ LIMIT 사용 + 인덱스
- ❌ 로깅 OFF — 실제 SQL 안 보임 ✅ `logging.level.com.example.mapper=DEBUG`

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| `BindingException: Invalid bound statement` | Mapper XML 의 namespace·id 가 인터페이스와 불일치 | 정확히 매칭 |
| `reg_date` 가 null | snake_case ↔ camelCase 자동 매핑 OFF | `map-underscore-to-camel-case=true` |
| INSERT 후 `board.getId()` 가 0 | `useGeneratedKeys` 누락 | `useGeneratedKeys="true" keyProperty="id"` |
| 여러 파라미터 받을 때 `#{0}` 만 동작 | `@Param` 누락 | `@Param("name")` 명시 |
| Mapper XML 못 찾음 | `mapper-locations` 경로 오류 | `classpath:mappers/**/*.xml` 확인 |
| SQL Injection 의심 | `${}` 에 사용자 입력 직접 사용 | `#{}` 로 변경 + 화이트리스트 |
| Transaction rollback 안 됨 | checked exception 또는 `@Transactional` 누락 | `@Transactional` + RuntimeException |

---

## 17. 자가점검

1. JDBC 의 4가지 보일러플레이트 문제는?
2. MyBatis 의 핵심 5가지 구성 요소는?
3. `#{}` 와 `${}` 의 차이와 각 사용 시점?
4. `useGeneratedKeys` 와 `keyProperty` 는 왜 필요한가?
5. `@Mapper` 가 붙은 인터페이스는 어떻게 실제 구현체가 되나?
6. snake_case ↔ camelCase 자동 매핑 설정은?
7. MyBatis 와 JPA 중 어느 게 한국 SI/SM 에서 압도적인가? 이유는?

<details><summary>풀이</summary>

1. ① 30+ 줄 보일러플레이트 ② 자원 누수 위험 ③ SQL 이 자바 문자열에 묻힘 ④ 결과 매핑 수동.
2. **SqlSessionFactoryBuilder** (XML 읽어 Factory 빌드) / **SqlSessionFactory** (싱글톤 팩토리) / **SqlSession** (실제 DB 작업 단위) / **mybatis-config.xml** (전역 설정) / **Mapper XML** (SQL 정의).
3. **`#{}`**: PreparedStatement 의 `?` 바인딩 (값 — 안전). **`${}`**: 문자열 그대로 치환 (SQL 구조 — 칼럼명·정렬 방향. SQL Injection 위험으로 반드시 화이트리스트).
4. `useGeneratedKeys="true"` 가 INSERT 후 DB 의 AUTO_INCREMENT 값을 받아서, `keyProperty="id"` 가 그 값을 객체의 `id` 필드에 자동 set. 없으면 INSERT 후 객체의 id 는 0.
5. Spring Boot 가 `@Mapper` 인터페이스를 스캔 → MyBatis 가 **런타임에 Proxy 객체** 를 자동 생성 (JDK Dynamic Proxy 또는 CGLIB) → 컨테이너에 빈으로 등록. 메서드 호출 시 namespace + id 로 XML 의 SQL 을 찾아 실행.
6. `mybatis.configuration.map-underscore-to-camel-case=true` (application.properties). 또는 XML 설정의 `<settings><setting name="mapUnderscoreToCamelCase" value="true"/></settings>`.
7. **MyBatis 가 압도적**. 이유: ① 한국 기업은 SI 프로젝트에서 DBA 가 별도로 SQL 튜닝 → MyBatis 가 SQL 통제권을 유지. ② 레거시 SP 호출이나 복잡한 동적 쿼리에 강함. ③ 학습 곡선이 JPA 보다 낮음. JPA 는 새 프로젝트·도메인 중심 설계에 유리하지만 SI 환경엔 부적합.

</details>

---

## 18. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.6 사전설정 (Mybatipse 플러그인) | (생략) |
| p.7 ~ p.19 MyBatis (구성요소·SqlSession·typeAliases) | §1 ~ §7 (Part A, B) |
| p.20 ~ p.22 SqlSessionFactory·순수 자바 사용 | §8, §9 (Part C) |
| p.23 ~ p.28 MyBatis Spring Boot 실습 (@Mapper) | §10 ~ §14 (Part D) |
| p.29 마무리 | (생략) |

_29p 슬라이드 모두 커버. 다음 강의는 동적 쿼리 (`<where>`/`<if>`/`<foreach>`)._
