# MyBatis — 퀴즈

> 15문항. 개념·적용·디버그·면접. 4부(MyBatis 개념·구성 요소·순수 자바·Spring Boot 연동) 골고루.

---

### Q1. (개념) JDBC 만 쓸 때의 4가지 보일러플레이트 문제는?

<details><summary>정답</summary>

1. **30+ 줄 보일러플레이트** — 비즈니스 로직은 5줄, 나머지는 자원 관리
2. **자원 누수 위험** — close 호출 누락 시 connection pool 고갈
3. **SQL 이 자바 문자열에 묻힘** — 가독성·유지보수 ↓
4. **결과 매핑 수동** — `rs.getInt`/`rs.getString` 일일이

MyBatis 가 모두 해결.

</details>

### Q2. (개념) MyBatis 의 핵심 5가지 구성 요소는?

<details><summary>정답</summary>

1. **SqlSessionFactoryBuilder** — XML 설정 읽어서 Factory 빌드 (앱 시작 시 1번)
2. **SqlSessionFactory** — SqlSession 생성 팩토리 (싱글톤)
3. **SqlSession** — 실제 DB 작업 단위 (selectOne/insert/update/delete)
4. **mybatis-config.xml** — 전역 설정 (typeAliases, env, mappers)
5. **Mapper XML** — SQL 정의

</details>

### Q3. (개념) `#{}` 와 `${}` 의 차이를 한 문장으로?

<details><summary>정답</summary>

- **`#{}`**: PreparedStatement 의 `?` 바인딩 (값 전달, SQL Injection 안전)
- **`${}`**: 문자열 그대로 치환 (SQL 구조 — 칼럼명·정렬 방향, **SQL Injection 위험**)

값은 항상 `#{}`, `${}` 는 화이트리스트 검증한 SQL 구조에만.

</details>

### Q4. (적용) 다음 Mapper XML 을 작성하시오.

```
인터페이스: List<Board> findByCategory(String category);
조건: category 컬럼이 #{category} 와 같은 행, 최신순
```

<details><summary>정답</summary>

```xml
<select id="findByCategory" parameterType="string" resultType="Board">
    SELECT * FROM board
    WHERE category = #{category}
    ORDER BY id DESC
</select>
```

XML 의 `id` 와 인터페이스 메서드명 일치. `parameterType` 은 단일 파라미터일 때만 필요.

</details>

### Q5. (디버그) INSERT 후 `board.getId()` 가 항상 0. 원인과 해결?

<details><summary>정답</summary>

**원인**: `useGeneratedKeys` 설정 누락. AUTO_INCREMENT 키가 객체에 set 안 됨.

**해결**:
```xml
<insert id="insert" parameterType="Board"
        useGeneratedKeys="true" keyProperty="id">
    INSERT INTO board(title, content, writer)
    VALUES (#{title}, #{content}, #{writer})
</insert>
```

`useGeneratedKeys="true"` 가 키를 받아오고, `keyProperty="id"` 가 객체 필드에 set.

</details>

### Q6. (적용) `reg_date` (DB) ↔ `regDate` (Java) 자동 매핑 설정?

<details><summary>정답</summary>

`application.properties`:
```properties
mybatis.configuration.map-underscore-to-camel-case=true
```

이 설정 없으면 XML 에서 `AS regDate` 별칭 일일이 작성해야.

</details>

### Q7. (적용) 여러 파라미터를 받는 Mapper 인터페이스?

<details><summary>정답</summary>

```java
@Mapper
public interface BoardMapper {
    List<Board> findByWriterAndCategory(@Param("writer") String writer,
                                          @Param("category") String category);
}
```

XML:
```xml
<select id="findByWriterAndCategory" resultType="Board">
    SELECT * FROM board
    WHERE writer   = #{writer}
      AND category = #{category}
</select>
```

`@Param("이름")` 없이는 `#{param1}`, `#{param2}` 또는 `#{0}`, `#{1}` 로 접근 — 가독성 나쁨.

</details>

### Q8. (디버그) `BindingException: Invalid bound statement (not found): com.example.mapper.BoardMapper.findById`. 원인 후보?

<details><summary>정답</summary>

1. **Mapper XML 의 `namespace` 가 인터페이스 풀패키지명과 불일치**
   ```xml
   <mapper namespace="com.example.mapper.BoardMapper">   <!-- 정확히 매칭 -->
   ```

2. **XML 의 `id` 가 인터페이스 메서드명과 불일치**
   ```xml
   <select id="findById">     <!-- 메서드명과 동일 -->
   ```

3. **Mapper XML 위치 설정 오류**
   ```properties
   mybatis.mapper-locations=classpath:mappers/**/*.xml
   ```

4. **인터페이스에 `@Mapper` 누락** → 빈 등록 안 됨

</details>

### Q9. (개념) `@Mapper` 가 붙은 인터페이스는 어떻게 실제 구현체가 되나?

<details><summary>정답</summary>

1. Spring Boot 가 `@Mapper` 어노테이션을 스캔
2. MyBatis 가 **런타임에 인터페이스를 구현한 Proxy 객체** 자동 생성 (JDK Dynamic Proxy 또는 CGLIB)
3. 컨테이너에 빈으로 등록
4. Service 에서 `@Autowired` 또는 생성자 주입으로 사용
5. 메서드 호출 시 Proxy 가 `namespace + id` 로 XML 의 SQL 을 찾아 실행

개발자는 인터페이스만 작성, 구현은 런타임 자동 생성.

</details>

### Q10. (적용) 어노테이션으로 SQL 직접 작성 (간단한 쿼리)?

<details><summary>정답</summary>

```java
@Mapper
public interface BoardMapper {

    @Select("SELECT count(*) FROM board")
    int count();

    @Select("SELECT * FROM board WHERE id = #{id}")
    Board findById(int id);

    @Insert("INSERT INTO board(title, content, writer) " +
            "VALUES (#{title}, #{content}, #{writer})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Board board);
}
```

**언제 어노테이션**: 단순한 단일 쿼리. **언제 XML**: 복잡한 동적 쿼리, 긴 SQL, DBA 와 협업.

대부분 프로젝트는 XML 표준 채택 (한국 SI/SM).

</details>

### Q11. (디버그) `SqlSessionFactory` 빈이 등록 안 됨. 원인?

<details><summary>정답</summary>

1. **`mybatis-spring-boot-starter` 의존성 누락**
2. **DataSource 빈 등록 안 됨** — `spring.datasource.url` 등 설정 누락
3. **`@SpringBootApplication` 의 패키지 위치가 깊어 자동 설정 안 됨**

Spring Boot 의 자동 설정은 의존성 + DataSource 설정 둘 다 있어야 트리거.

</details>

### Q12. (개념) `SqlSession` 의 생명주기는?

<details><summary>정답</summary>

**요청마다 새로 생성, 작업 끝나면 close**. 스레드 간 공유 X.

- 순수 자바: try-with-resources 로 자동 close
- Spring Boot: MyBatis Spring 이 자동 관리 — `SqlSessionTemplate` 이 트랜잭션 단위로 `SqlSession` 을 lazy 생성/관리

vs `SqlSessionFactory` 는 **싱글톤** (앱 시작 시 1번 빌드, 평생 사용).

</details>

### Q13. (디버그) MyBatis Mapper 호출 시 항상 같은 객체가 반환됨 (캐시 의심). 원인?

<details><summary>정답</summary>

**MyBatis 의 1차 캐시** — 같은 SqlSession 안에서 같은 SQL + 같은 파라미터로 호출하면 캐시된 객체 반환. Spring 환경에선 트랜잭션 단위로 캐시 유지.

**해결 (필요 시)**:
- `sqlSession.clearCache()` 호출
- Mapper XML 에 `flushCache="true"` 설정
- `@CacheNamespace` 비활성화

대부분 캐시가 도움이 되니 의도적으로 끄는 경우는 드물다.

</details>

### Q14. (면접) "MyBatis 와 JPA 중 어느 것을 추천하시나요? 그 이유는?"

<details><summary>정답</summary>

**상황별 선택**:

**MyBatis 추천**:
- 레거시 SI 프로젝트 / SM 유지보수
- DBA 가 SQL 튜닝하는 환경
- 복잡한 동적 쿼리·집계·리포팅 위주
- 학습 곡선 낮음 + 한국 시장 점유율 높음

**JPA 추천**:
- 신규 도메인 중심 설계
- DDD 적용 — 객체 그래프 위주
- 간단한 CRUD 가 대부분
- MSA 의 작은 서비스

**솔직한 결론**: 한국 SI/SM 환경에선 MyBatis 가 사실상 표준. 외국계·신규 도메인엔 JPA. 둘 다 가능하면 좋지만 한국 첫 직장 면접은 MyBatis 가 더 자주 나옴.

</details>

### Q15. (면접) "`#{}` 와 `${}` 의 차이를 코드 예시로 설명하시오."

<details><summary>정답</summary>

```xml
<!-- 사용자가 입력한 이메일로 검색 -->

<!-- ✅ #{}  — 안전한 PreparedStatement 바인딩 -->
<select id="findByEmail" parameterType="string" resultType="User">
    SELECT * FROM user WHERE email = #{email}
</select>
<!-- 실행 SQL: SELECT * FROM user WHERE email = ?
     파라미터:                              = "alice@example.com" -->

<!-- ❌ ${} — 문자열 치환 (SQL Injection 위험) -->
<select id="findByEmailBad" parameterType="string" resultType="User">
    SELECT * FROM user WHERE email = '${email}'
</select>
<!-- 사용자가 "' OR '1'='1" 입력하면? -->
<!-- 실행 SQL: SELECT * FROM user WHERE email = '' OR '1'='1'
     → 모든 사용자 조회 가능! -->
```

`${}` 는 **칼럼명·테이블명·정렬 방향(ASC/DESC) 같은 SQL 구조** 에만 + **반드시 화이트리스트 검증** 후. 값은 항상 `#{}`.

</details>
