# JPA 3강: Spring Data JPA

> **이 강의는 무엇인가**: JPA 의 EntityManager 를 직접 다루는 코드를 *인터페이스 선언 한 줄* 로 압축하는 Spring 모듈. `JpaRepository`, 메서드 이름 규칙, `@Query` (JPQL), 페이징, `@Modifying`, Projection.
> **왜 배우는가**: JPA 의 *진짜 실무 코드 패턴*. 2 강에서 본 영속성 컨텍스트의 마법을 *실제 Repository 코드* 로 어떻게 활용하는가. SSAFY 백엔드의 거의 모든 신규 코드가 이 패턴.

---

## 들어가기 전에

- **선수**: 1 강 (Entity 매핑), 2 강 (영속성 컨텍스트 · Dirty Checking · 트랜잭션).
- **마인드셋**: "**인터페이스만 선언** 한다. 구현은 Spring 이 자동." 마법처럼 보이지만 내부는 *Proxy 객체* 가 인터페이스 메서드를 분석해 JPQL 을 자동 생성하는 것뿐.
- **2 강 복습**: 영속성 컨텍스트가 1차 캐시·Dirty Checking 을 관리. `@Transactional` 안에서 setter 만 호출해도 UPDATE 됨. `persist` vs `merge` 차이.

---

# Part A. Spring Data JPA 가 뭔가

## 1. JPA 직접 쓰기 vs Spring Data JPA

```java
// JPA EntityManager 직접 사용 - 보일러플레이트
@Repository
@RequiredArgsConstructor
public class BoardRepositoryImpl {

    @PersistenceContext
    private EntityManager em;

    public Optional<Board> findById(Long id) {
        return Optional.ofNullable(em.find(Board.class, id));
    }

    public List<Board> findAll() {
        return em.createQuery("SELECT b FROM Board b", Board.class).getResultList();
    }

    public Board save(Board b) {
        if (b.getId() == null) {
            em.persist(b);
            return b;
        } else {
            return em.merge(b);
        }
    }

    public void delete(Board b) {
        em.remove(em.contains(b) ? b : em.merge(b));
    }
    // ... count, existsById, findByXxx 등 다 직접 작성
}
```

```java
// Spring Data JPA - 위와 동일 기능
public interface BoardRepository extends JpaRepository<Board, Long> {
    // 끝.
}
```

차이: **인터페이스 한 줄**. 구현체는 Spring 이 *동적 프록시* 로 자동 생성.

## 2. 동작 원리 (간단)

```
Application 시작
   |
   v
@SpringBootApplication 이 @EnableJpaRepositories 자동 활성화
   |
   v
classpath 스캔 - JpaRepository 를 상속하는 인터페이스 발견
   |
   v
각 인터페이스마다 Proxy 클래스 동적 생성
   |
   v
Proxy 가 메서드 이름·@Query·표준 메서드를 분석해 SQL/JPQL 발행
   |
   v
@Autowired 시 Proxy 객체 주입
```

**핵심**: 컴파일 타임에는 구현체 클래스가 없다. 런타임에 만들어진다.

## 3. 계층

```
   Service @Transactional
        |
        v
   +----------------------------+
   | BoardRepository (interface) |  <- 내가 선언
   +----------------------------+
        |
        v
   +-------------------------------------+
   | Spring 의 동적 Proxy (런타임 생성)    |
   +-------------------------------------+
        |
        v
   +----------------------------+
   | SimpleJpaRepository<T, ID> |  <- Spring Data JPA 내부 기본 구현
   +----------------------------+
        |
        v
   EntityManager (JPA)
```

`SimpleJpaRepository` 가 *기본 CRUD* 의 실제 구현. 우리가 메서드 이름 규칙으로 추가한 것은 Proxy 가 *런타임에 JPQL 생성* 해서 처리.

---

# Part B. JpaRepository — 무엇이 자동으로 들어오나

## 1. 자동 제공 메서드

`JpaRepository<엔티티, PK 타입>` 만 상속하면:

```java
public interface BoardRepository extends JpaRepository<Board, Long> {
}
```

다음이 자동:

| 메서드 | 동작 |
|--|--|
| `<S extends T> S save(S entity)` | INSERT (transient) 또는 UPDATE (managed) — 내부적으로 persist/merge 분기 |
| `<S extends T> List<S> saveAll(Iterable)` | 다건 저장 |
| `Optional<T> findById(ID id)` | PK 단건 조회 |
| `List<T> findAll()` | 전체 조회 |
| `List<T> findAllById(Iterable<ID>)` | PK 다건 조회 |
| `List<T> findAll(Sort sort)` | 정렬 |
| `Page<T> findAll(Pageable pageable)` | 페이징 |
| `long count()` | 전체 개수 |
| `boolean existsById(ID)` | 존재 여부 |
| `void delete(T entity)` | 단건 삭제 |
| `void deleteById(ID)` | PK 로 삭제 |
| `void deleteAll()` | 전체 삭제 |
| `void deleteAllById(Iterable<ID>)` | PK 다건 삭제 |
| `void deleteAllInBatch()` | bulk DELETE (영속성 컨텍스트 우회) |
| `void flush()` | 즉시 flush |

상속 계층:
```
JpaRepository<T, ID>           <- 가장 흔히 사용
   extends PagingAndSortingRepository<T, ID>
   extends CrudRepository<T, ID>
   extends Repository<T, ID>
```

특수 상황: `PagingAndSortingRepository` (페이징/정렬만), `CrudRepository` (CRUD 만) 도 있지만 거의 안 씀.

## 2. 가장 단순한 사용

```java
@Service
@RequiredArgsConstructor
public class BoardService {

    private final BoardRepository boardRepo;

    @Transactional
    public Board create(BoardForm form) {
        Board b = Board.builder()
            .title(form.getTitle())
            .content(form.getContent())
            .writer(form.getWriter())
            .build();
        return boardRepo.save(b);   // INSERT
    }

    @Transactional(readOnly = true)
    public Board read(Long id) {
        return boardRepo.findById(id)
            .orElseThrow(() -> new NoSuchElementException("게시글 없음: " + id));
    }

    @Transactional
    public void delete(Long id) {
        boardRepo.deleteById(id);   // SELECT (존재 확인) -> DELETE
    }
}
```

> **함정**: `deleteById(id)` 는 *내부적으로 SELECT 먼저 + DELETE*. 진짜 *바로 DELETE* 하려면 `@Modifying` 의 native query 또는 `deleteAllInBatch()` (Part F).

---

# Part C. 메서드 이름 규칙 (Derived Query)

표준 CRUD 외에 *조건 검색* 을 인터페이스 *메서드 이름만* 으로 자동 생성.

## 1. 기본 형식

```java
public interface BoardRepository extends JpaRepository<Board, Long> {

    // SELECT * FROM board WHERE writer = ?
    List<Board> findByWriter(String writer);

    // SELECT * FROM board WHERE title LIKE %?%
    List<Board> findByTitleContaining(String keyword);

    // SELECT * FROM board WHERE writer = ? AND view_cnt > ?
    List<Board> findByWriterAndViewCntGreaterThan(String writer, int min);

    // SELECT * FROM board ORDER BY reg_date DESC LIMIT 1
    Optional<Board> findFirstByOrderByRegDateDesc();

    // SELECT COUNT(*) FROM board WHERE writer = ?
    long countByWriter(String writer);

    // SELECT EXISTS(SELECT 1 FROM board WHERE title = ?)
    boolean existsByTitle(String title);

    // DELETE FROM board WHERE writer = ? (영속성 컨텍스트 통과)
    @Transactional
    long deleteByWriter(String writer);
}
```

## 2. 명명 규칙

**접두어 (Subject)**:

| 접두어 | 동작 |
|--|--|
| `findBy` | SELECT |
| `existsBy` | SELECT 1 → boolean |
| `countBy` | COUNT |
| `deleteBy` / `removeBy` | DELETE |
| `findFirstBy*` / `findTopBy*` | 첫 N 건. `findTop3By*` 도 가능 |

**조건 키워드 (Predicate)**:

| 키워드 | SQL |
|--|--|
| `Containing(s)` | `LIKE '%' + s + '%'` |
| `StartingWith(s)` | `LIKE s + '%'` |
| `EndingWith(s)` | `LIKE '%' + s` |
| `GreaterThan(n)` / `LessThan(n)` | `>` / `<` |
| `GreaterThanEqual` / `LessThanEqual` | `>=` / `<=` |
| `Between(a, b)` | `BETWEEN a AND b` |
| `In(Collection)` | `IN (...)` |
| `NotIn` | `NOT IN (...)` |
| `IsNull` / `IsNotNull` | `IS NULL` / `IS NOT NULL` |
| `True` / `False` | `= true` / `= false` |
| `IgnoreCase` | 대소문자 무시 (`LOWER(...) = LOWER(...)`) |

**연결자**:
- `And`, `Or`
- `OrderBy{필드}Asc|Desc` (필드명 PascalCase)

**예시**:

```java
// 글쓴이가 X, view_cnt > Y, 등록일 내림차순
List<Board> findByWriterAndViewCntGreaterThanOrderByRegDateDesc(String writer, int min);

// 제목에 키워드 포함 (대소문자 무시)
List<Board> findByTitleContainingIgnoreCase(String keyword);

// 카테고리 ID 가 IN 목록
List<Board> findByCategoryIdIn(List<Long> categoryIds);
```

## 3. 메서드 이름의 한계

```java
// 5 개 이상 조건 → 메서드 이름 폭주
List<Board> findByWriterAndCategoryAndTagInAndViewCntGreaterThanAndRegDateBetweenOrderByRegDateDesc(
    String writer, String category, List<String> tags, int minView, LocalDate from, LocalDate to);
// 가독성 폭망
```

**한계**:
- 3 ~ 4 조건 넘어가면 이름이 너무 길어짐
- 동적 조건 (조건이 *런타임에* 결정) 처리 불가
- 복잡한 JOIN 표현 어려움

해결책: `@Query` (Part D) 또는 **QueryDSL** (별도 학습).

---

# Part D. @Query — JPQL 직접 작성

## 1. 기본

```java
public interface BoardRepository extends JpaRepository<Board, Long> {

    @Query("SELECT b FROM Board b WHERE b.viewCnt > :min ORDER BY b.regDate DESC")
    List<Board> findPopularSince(@Param("min") int min);
}
```

- JPQL 은 **엔티티 객체 기준**: `Board b`, `b.viewCnt`, `b.regDate`
- 테이블명 X, 자바 *필드명* 사용
- `@Param("이름")` 으로 named parameter 바인딩

## 2. 단건 / 다건 / Optional

```java
// 단건 (없으면 null - Optional 추천)
@Query("SELECT b FROM Board b WHERE b.id = :id")
Optional<Board> findOne(@Param("id") Long id);

// 다건
@Query("SELECT b FROM Board b WHERE b.writer = :writer")
List<Board> findByWriter(@Param("writer") String writer);

// 집계
@Query("SELECT COUNT(b) FROM Board b WHERE b.writer = :writer")
long countByWriter(@Param("writer") String writer);
```

## 3. DTO 직접 매핑

```java
public record BoardSummary(Long id, String title, String writer) {}

// JPQL 의 'new' 키워드 + 풀 패키지명 + 생성자 인자
@Query("""
    SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer)
    FROM Board b
    WHERE b.viewCnt > :min
""")
List<BoardSummary> findSummaries(@Param("min") int min);
```

엔티티 전체 (`Board`) 가 아니라 *DTO* 로 받으면:
- LAZY 컬렉션 함정 없음
- 트랜잭션 밖에서도 안전
- 필요한 컬럼만 SELECT → 네트워크 효율

## 4. JOIN 과 fetch (4 강 미리보기)

```java
// 게시글 + 댓글을 한 번에 (N+1 회피)
@Query("SELECT b FROM Board b LEFT JOIN FETCH b.replies WHERE b.id = :id")
Optional<Board> findByIdWithReplies(@Param("id") Long id);
```

`JOIN FETCH` 는 4 강에서 본격적으로 다룸.

## 5. native query (escape hatch)

```java
@Query(value = "SELECT * FROM board WHERE MATCH(title, content) AGAINST(:keyword)",
       nativeQuery = true)
List<Board> fullTextSearch(@Param("keyword") String keyword);
```

JPQL 로 표현 불가한 *DB 특화 기능* (MySQL full-text, PostgreSQL JSONB 등) 만 사용. 남용 시 **DB 종속**.

---

# Part E. 페이징

## 1. Pageable / Page / PageRequest

```java
// Repository - JpaRepository 기본 메서드
Page<Board> findAll(Pageable pageable);

// 또는 derived query 와 결합
List<Board> findByWriter(String writer, Pageable pageable);

// 또는 @Query 와 결합
@Query("SELECT b FROM Board b WHERE b.writer = :writer")
Page<Board> searchByWriter(@Param("writer") String writer, Pageable pageable);
```

```java
// Service / Controller
Page<Board> page = boardRepo.findAll(
    PageRequest.of(0, 10, Sort.by("regDate").descending())
);

page.getContent();        // 현재 페이지의 List<Board>
page.getTotalElements();  // 전체 row 수
page.getTotalPages();     // 전체 페이지 수
page.getNumber();         // 현재 페이지 (0-based)
page.getSize();           // 페이지당 size
page.hasNext();
page.hasPrevious();
```

`Page<T>` 는 *별도 COUNT 쿼리* 까지 자동 (전체 개수 알기 위해).

## 2. Slice — COUNT 없는 가벼운 페이징

```java
Slice<Board> slice = boardRepo.findByWriter(writer, PageRequest.of(0, 10));
slice.hasNext();   // 다음 페이지 존재? (size + 1 미리 조회로 판단)
slice.getContent();
```

전체 개수가 필요 없는 *무한 스크롤* / *다음 버튼만* 인 UI 에 적합. COUNT 쿼리 안 함 → 성능 ↑.

## 3. Sort

```java
Sort.by("regDate").descending();
Sort.by(Sort.Order.desc("regDate"), Sort.Order.asc("title"));
PageRequest.of(0, 10, Sort.by("viewCnt").descending());
```

또는 Controller 에서 `?sort=regDate,desc&size=10&page=0` 같은 query string 으로 받으면 Spring 이 자동 바인딩.

## 4. Pageable parameter binding (Controller)

```java
@GetMapping("/boards")
public Page<Board> list(
    @PageableDefault(size = 10, sort = "regDate", direction = Sort.Direction.DESC)
    Pageable pageable
) {
    return boardRepo.findAll(pageable);
}
```

URL: `/boards?page=0&size=20&sort=regDate,desc`

---

# Part F. @Modifying — bulk UPDATE / DELETE

## 1. JPQL UPDATE / DELETE

```java
@Modifying
@Query("UPDATE Board b SET b.viewCnt = b.viewCnt + 1 WHERE b.id = :id")
int incrementViewCount(@Param("id") Long id);

@Modifying
@Query("DELETE FROM Board b WHERE b.writer = :writer")
int deleteByWriter(@Param("writer") String writer);
```

**`@Modifying` 이 없으면** `QueryExecutionRequestException` — JPQL UPDATE/DELETE 는 변경 쿼리라 명시적 표식 필수.

반환 타입: `int` 또는 `void`. `int` 면 영향받은 row 수.

## 2. 함정 — 영속성 컨텍스트 우회

`@Modifying` JPQL 은 **영속성 컨텍스트를 거치지 않고 DB 직접** 변경:

```java
@Transactional
public void problem(Long id) {
    Board b = boardRepo.findById(id).orElseThrow();   // managed, viewCnt=0
    boardRepo.incrementViewCount(id);                  // DB 의 viewCnt 가 1 됨

    System.out.println(b.getViewCnt());                // 0 ← 영속성 컨텍스트는 옛 값
}
```

해결책 1: `clearAutomatically = true`

```java
@Modifying(clearAutomatically = true)
@Query("UPDATE Board b SET b.viewCnt = b.viewCnt + 1 WHERE b.id = :id")
int incrementViewCount(@Param("id") Long id);
```

쿼리 실행 후 *영속성 컨텍스트 전체 clear* → 다음 접근 시 DB 에서 다시 가져옴.

해결책 2: `flushAutomatically = true`

```java
@Modifying(flushAutomatically = true, clearAutomatically = true)
```

쿼리 *실행 전* flush 도 자동. 더 안전 (영속성 컨텍스트의 다른 미반영 변경이 *쿼리 결과에 반영*).

## 3. Dirty Checking 으로 대체 가능

대부분의 경우 *managed 엔티티의 setter* 가 더 자연스럽고 안전:

```java
@Transactional
public void increment(Long id) {
    Board b = boardRepo.findById(id).orElseThrow();
    b.setViewCnt(b.getViewCnt() + 1);
    // Dirty Checking 으로 자동 UPDATE
}
```

**`@Modifying` 은 *bulk* (한 번에 수백/수천 row) 변경에 한해 사용.** 단건 변경에는 dirty checking 이 더 안전·간결.

---

# Part G. Projection — 필요한 필드만

## 1. Interface-based Projection

```java
public interface BoardSummary {
    Long getId();
    String getTitle();
    String getWriter();
}

public interface BoardRepository extends JpaRepository<Board, Long> {
    List<BoardSummary> findByCategoryId(Long categoryId);
}
```

Spring 이 *프록시 구현체* 자동 생성. SELECT 도 *필요한 컬럼만*:

```sql
SELECT id, title, writer FROM board WHERE category_id = ?
```

## 2. Class-based Projection (DTO)

```java
public record BoardSummary(Long id, String title, String writer) {}

@Query("SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer) FROM Board b WHERE b.categoryId = :cid")
List<BoardSummary> findSummaries(@Param("cid") Long cid);
```

또는 *생성자 자동 매칭* (Spring Data 3.x+):

```java
// @Query 없이도 가능 - 생성자 인자 이름이 엔티티 필드와 일치하면
List<BoardSummary> findByCategoryId(Long categoryId);
```

## 3. Dynamic Projection

```java
public interface BoardRepository extends JpaRepository<Board, Long> {
    <T> List<T> findByCategoryId(Long categoryId, Class<T> type);
}

// 사용처에서 결정
List<BoardSummary> summaries = repo.findByCategoryId(1L, BoardSummary.class);
List<Board> fullBoards = repo.findByCategoryId(1L, Board.class);
```

---

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| 메서드 이름이 너무 길어짐 (5+ 조건) | `@Query` 또는 QueryDSL 사용 |
| `@Modifying` 없이 JPQL UPDATE/DELETE → `QueryExecutionRequestException` | `@Modifying` 부착 필수 |
| `@Modifying` 후 영속성 컨텍스트의 옛 값이 보임 | `clearAutomatically = true` |
| `deleteById(id)` 가 *SELECT + DELETE* 두 쿼리 | 진짜 단일 DELETE 원하면 `@Modifying DELETE` 또는 `deleteAllInBatch()` |
| 동적 조건 (어떤 조건이 활성화될지 런타임 결정) 을 메서드 이름으로 처리 | 불가. **Specifications** 또는 **QueryDSL** 사용 |
| 페이징 + LAZY 컬렉션 JOIN FETCH → 메모리 폭증 | JOIN FETCH 는 `OneToMany` 와 페이징 *동시* 사용 금지 (Hibernate 가 메모리 페이징으로 fallback). DTO Projection 권장 |
| `Page<T>` 대신 `Slice<T>` 도 모르고 항상 `Page<T>` 사용 | 전체 개수 안 쓰면 `Slice<T>` 가 빠름 (COUNT 쿼리 X) |
| native query 남용으로 DB 종속 | DB 특화 기능 (MySQL full-text, PostgreSQL JSONB) 에만 사용. 일반 검색은 JPQL |
| `@Param` 누락 + parameter 이름이 컴파일 후 사라짐 | `@Param("name")` 명시 (`-parameters` 컴파일 옵션 없으면 필수) |
| 메서드 이름의 필드명 오타 (`viewCount` 대신 `viewCnt`) → *애플리케이션 시작 시점 예외* | 다행히 *컴파일이 아닌 시작 시* 잡힘. test profile 으로 빨리 잡기 |
| Repository 메서드에 `@Transactional` 안 붙임 → `@Modifying` 동작 안 함 | Service 층의 `@Transactional` 안에서 호출 또는 메서드에 직접 부착 |
| `findByWriterIgnoreCase` 가 큰 테이블에서 풀스캔 | 검색 컬럼에 인덱스 + `LOWER()` 함수 인덱스 (DB 별 지원) 또는 별도 검색 엔진 (Elasticsearch) 고려 |

---

## 자가점검

1. `JpaRepository<T, ID>` 가 자동 제공하는 *대표 메서드 5 개* 를 들고 각각 무슨 SQL 인지.
2. Spring Data JPA 의 동작 *원리* 를 한 문단으로 (인터페이스 → 무엇이 어떻게 채워지나).
3. 다음 쿼리를 *메서드 이름 규칙* 으로 표현하시오:
   - "writer 가 X 이면서 viewCnt 가 Y 이상, 제목에 keyword 포함, regDate 내림차순"
4. `@Modifying` 의 *두 가지 옵션* (`flushAutomatically`, `clearAutomatically`) 의 의미.
5. `Page<T>` 와 `Slice<T>` 의 차이. 어느 쪽이 더 가볍나? 왜?
6. `deleteById(id)` 가 *발행하는 쿼리 개수* 와 그 이유.
7. JPQL 의 `new 패키지.DTO(...)` 문법이 *어떤 함정* 을 해결해주나?
8. native query 를 *언제만* 써야 하나?
9. Interface-based Projection 의 *장점 2 가지*.
10. 메서드 이름 규칙이 *동적 조건* 을 처리 못 하는 이유와 대안 두 가지.

<details><summary>풀이</summary>

1. `save`/`findById`/`findAll`/`count`/`deleteById` — INSERT or UPDATE / SELECT WHERE id=? / SELECT * / SELECT COUNT(*) / SELECT + DELETE.
2. 시작 시 `@EnableJpaRepositories` 가 classpath 스캔으로 `JpaRepository` 상속 인터페이스를 찾고, 각각에 *동적 프록시* 를 만들어 빈으로 등록. 프록시는 메서드 이름·`@Query`·기본 메서드 (SimpleJpaRepository) 를 분석해 JPQL/SQL 을 발행.
3. `findByWriterAndViewCntGreaterThanEqualAndTitleContainingOrderByRegDateDesc(String writer, int viewCnt, String keyword)`
4. `flushAutomatically = true` — bulk 쿼리 *실행 전* 영속성 컨텍스트의 미반영 변경을 flush. `clearAutomatically = true` — 쿼리 *실행 후* 영속성 컨텍스트 전체 clear (옛 값 캐시 제거).
5. `Page<T>` — content + 전체 개수 (별도 COUNT 쿼리). `Slice<T>` — content + hasNext (size+1 조회로 판단). `Slice` 가 **가볍다** (COUNT 쿼리 안 함).
6. **2 개**: SELECT (존재 확인) + DELETE. 이유: `deleteById` 내부 구현이 *find 후 remove*. 진짜 단일 DELETE 원하면 `@Modifying DELETE`.
7. **N+1 / LAZY 함정**. 엔티티 전체 대신 *필요한 필드만* SELECT → 연관 컬렉션 LAZY 프록시가 안 생김 → 트랜잭션 밖에서 안전 + 네트워크 효율.
8. **DB 특화 기능** (MySQL full-text, PostgreSQL JSONB/배열, DB 함수) 만. 일반 검색은 JPQL.
9. ① **SELECT 컬럼 최적화** (필요한 것만), ② **자동 프록시** (DTO 직접 작성 안 함).
10. **이유**: 메서드 이름은 *컴파일 타임 고정*. 런타임에 조건 ON/OFF 가 안 됨. **대안**: ① `Specifications` (Criteria API 래퍼), ② **QueryDSL** (타입 안전 + 동적).

</details>

---

## 다음 학습으로

- **JPA 4강: 연관관계 매핑** — `@ManyToOne`, `@OneToMany`, fetch 전략 (LAZY/EAGER), **N+1 문제**와 해결책 (JOIN FETCH, EntityGraph, BatchSize), cascade, orphanRemoval. 가장 함정이 많은 단원.
- 보강:
  - **QueryDSL** 시작 — `@Query` 의 한계를 절감하는 시점에 필수. Maven/Gradle 설정 + Q-class 생성 + dynamic where.
  - `application.yml` 의 `spring.jpa.hibernate.ddl-auto`, `show-sql`, `format-sql` 옵션 익히기 — 발행 SQL 을 *눈으로 보면서* 학습.
  - Spring Boot 의 `@DataJpaTest` 로 Repository 테스트 패턴.
