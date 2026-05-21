# JPA 3강: Spring Data JPA — 퀴즈

> 14문항. 개념·적용·디버그·면접. JpaRepository · 메서드 이름 규칙 · @Query · 페이징 · @Modifying · Projection 자가 진단.

---

### Q1. (개념) Spring Data JPA 의 *동작 원리* 를 한 문단으로 설명. 인터페이스만 선언하는데 어떻게 구현체가 생기는가?

<details><summary>정답</summary>

`@SpringBootApplication` (= `@EnableJpaRepositories` 포함) 가 시작 시 classpath 를 스캔하여 **`JpaRepository` 를 상속하는 인터페이스** 를 찾고, 각각에 대해 **동적 프록시 (Proxy 클래스)** 를 런타임에 생성하여 Spring 컨테이너의 빈으로 등록.

프록시는 호출되는 메서드를 분석:
- **메서드 이름** 이 규칙에 맞으면 → 그에 맞는 JPQL/SQL 자동 생성
- **`@Query`** 어노테이션이 있으면 → 그 JPQL/native SQL 실행
- **표준 메서드** (`save`, `findById` 등) 이면 → `SimpleJpaRepository` 의 기본 구현으로 위임

컴파일 시점에는 구현체가 *없고*, 런타임에 만들어진다. 그래서 IDE 가 구현체를 못 찾는 게 정상.

</details>

---

### Q2. (개념) `JpaRepository<T, ID>` 만 상속해도 자동 제공되는 *대표 메서드 6 개* 를 들고 각각의 SQL 을 한 줄로.

<details><summary>정답</summary>

| 메서드 | SQL |
|--|--|
| `save(entity)` | INSERT (transient) 또는 UPDATE (managed) — 내부 persist/merge 분기 |
| `findById(id)` | `SELECT ... FROM t WHERE id = ?` (`Optional<T>`) |
| `findAll()` | `SELECT ... FROM t` |
| `findAll(Pageable)` | `SELECT ...` + `LIMIT/OFFSET` + 별도 `SELECT COUNT(*)` |
| `count()` | `SELECT COUNT(*) FROM t` |
| `existsById(id)` | `SELECT 1 FROM t WHERE id = ?` (boolean) |
| `deleteById(id)` | `SELECT` (find) + `DELETE` (remove) — *두 쿼리* |
| `deleteAllInBatch()` | bulk `DELETE FROM t` — 영속성 컨텍스트 우회 |

</details>

---

### Q3. (개념) 메서드 이름 규칙의 *주요 접두어 4 개* 와 *조건 키워드 6 개* 를 들고 각각의 SQL.

<details><summary>정답</summary>

**접두어 (Subject)**:

| 접두어 | 동작 |
|--|--|
| `findBy` | SELECT |
| `existsBy` | SELECT 1 → boolean |
| `countBy` | COUNT |
| `deleteBy` / `removeBy` | DELETE |

**조건 키워드 (Predicate)**:

| 키워드 | SQL |
|--|--|
| `Containing(s)` | `LIKE '%' + s + '%'` |
| `StartingWith` / `EndingWith` | `LIKE s + '%'` / `LIKE '%' + s` |
| `GreaterThan` / `LessThan` | `>` / `<` |
| `Between(a, b)` | `BETWEEN a AND b` |
| `In(Collection)` | `IN (...)` |
| `IsNull` / `IsNotNull` | `IS NULL` / `IS NOT NULL` |
| `IgnoreCase` | `LOWER(...) = LOWER(...)` |

연결자: `And`, `Or`, `OrderBy{필드}Asc|Desc`.

</details>

---

### Q4. (적용) 다음 요구사항을 메서드 이름 규칙으로 작성하시오.
- `Board` 엔티티
- 조건: `writer == :w` AND `viewCnt >= :v` AND `title` 안에 `:k` 포함 (대소문자 무시)
- 정렬: `regDate` 내림차순
- 페이징

<details><summary>정답</summary>

```java
Page<Board> findByWriterAndViewCntGreaterThanEqualAndTitleContainingIgnoreCaseOrderByRegDateDesc(
    String writer, int viewCnt, String keyword, Pageable pageable);
```

길지만 컴파일 타임 검증 + 자동 생성 SQL. 이름이 너무 길어지면 `@Query` 로 가는 게 나음:

```java
@Query("""
    SELECT b FROM Board b
    WHERE b.writer = :writer
      AND b.viewCnt >= :viewCnt
      AND LOWER(b.title) LIKE LOWER(CONCAT('%', :keyword, '%'))
    ORDER BY b.regDate DESC
""")
Page<Board> search(@Param("writer") String writer,
                   @Param("viewCnt") int viewCnt,
                   @Param("keyword") String keyword,
                   Pageable pageable);
```

</details>

---

### Q5. (적용) `Board` 의 `(id, title, writer)` 만 SELECT 해서 `BoardSummary` 라는 record 로 받는 `@Query` 메서드를 작성하시오. 페이징도 함께.

<details><summary>정답</summary>

```java
public record BoardSummary(Long id, String title, String writer) {}

public interface BoardRepository extends JpaRepository<Board, Long> {

    @Query("""
        SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer)
        FROM Board b
        WHERE b.categoryId = :cid
    """)
    Page<BoardSummary> findSummariesByCategory(
        @Param("cid") Long categoryId,
        Pageable pageable);
}
```

핵심:
- `SELECT new 풀패키지명.DTO(필드들)` 문법
- **DTO 사용 이유**: LAZY 컬렉션 함정 없음, 트랜잭션 밖에서 안전, 필요한 컬럼만 SELECT (네트워크 효율)

</details>

---

### Q6. (적용) `Board` 의 `viewCnt` 를 모든 row 에 대해 0 으로 reset 하는 bulk UPDATE 메서드를 작성하시오. 영속성 컨텍스트의 동기화도 고려.

<details><summary>정답</summary>

```java
@Modifying(clearAutomatically = true, flushAutomatically = true)
@Query("UPDATE Board b SET b.viewCnt = 0")
int resetAllViewCounts();
```

핵심:
- `@Modifying` **필수** — 없으면 `QueryExecutionRequestException`
- `clearAutomatically = true` — 쿼리 후 영속성 컨텍스트 clear (이전에 managed 였던 엔티티들의 옛 값 캐시 제거)
- `flushAutomatically = true` — 쿼리 전 미반영 변경 flush (정합성)
- 반환 `int` — 영향받은 row 수

호출자도 `@Transactional` 안이어야 함:
```java
@Transactional
public void resetAll() { boardRepo.resetAllViewCounts(); }
```

</details>

---

### Q7. (적용) 다음 두 시나리오에 어느 쪽 (`Page<T>` vs `Slice<T>`) 을 쓸지 선택하고 이유.

A) 게시판 목록 — "총 156개, 1~10개 표시, [이전] [1][2][3]...[16] [다음]" UI
B) 모바일 무한 스크롤 — 사용자가 스크롤하면 다음 10개씩 자동 로딩

<details><summary>정답</summary>

**A) `Page<T>` — 전체 페이지 수가 필요**.
전체 개수 (`getTotalElements()`) → 페이지 번호 표시 (`getTotalPages()`) 필요. 별도 `SELECT COUNT(*)` 쿼리 발행.

**B) `Slice<T>` — 다음 페이지 존재 여부만 필요**.
COUNT 쿼리 안 함 → **성능 ↑**. `hasNext()` 는 *내부적으로 size+1 개 조회 후 size 개만 반환* 으로 판단.

**원칙**: COUNT 가 *불필요* 하면 항상 Slice. 게시판이 100만 row 면 COUNT 한 번이 큰 부담.

</details>

---

### Q8. (적용) 다음 Controller 의 URL `?page=1&size=20&sort=regDate,desc&sort=title,asc` 로 들어왔을 때, `pageable` 의 값이 어떻게 채워지나?

```java
@GetMapping("/boards")
public Page<Board> list(@PageableDefault(size = 10, sort = "id") Pageable pageable) {
    return boardRepo.findAll(pageable);
}
```

<details><summary>정답</summary>

- `page = 1` (0-based 라 *두 번째 페이지*)
- `size = 20` (URL 의 size 가 우선)
- `sort` — 두 정렬 기준 적용:
  1. `regDate DESC` (1순위)
  2. `title ASC` (2순위, tie-breaker)

`@PageableDefault` 의 `size = 10`, `sort = "id"` 는 *URL 에 값이 없을 때만* 사용. URL 에 명시되면 URL 우선.

발행 SQL (대략):
```sql
SELECT * FROM board
ORDER BY reg_date DESC, title ASC
LIMIT 20 OFFSET 20  -- page=1 * size=20
```

</details>

---

### Q9. (디버그) 다음 코드가 *기대와 다르게* 동작하는 이유와 수정 방법.
```java
@Transactional
public void incrementAndCheck(Long id) {
    Board b = boardRepo.findById(id).orElseThrow();   // viewCnt = 0
    boardRepo.incrementViewCount(id);                  // bulk UPDATE
    System.out.println(b.getViewCnt());                // 0 출력
}

// Repository
@Modifying
@Query("UPDATE Board b SET b.viewCnt = b.viewCnt + 1 WHERE b.id = :id")
int incrementViewCount(@Param("id") Long id);
```

<details><summary>정답</summary>

**원인**: `@Modifying` JPQL 은 **영속성 컨텍스트를 우회하고 DB 를 직접 변경**.

- `findById(id)` 로 가져온 `b` 는 영속성 컨텍스트의 1차 캐시에 `viewCnt = 0` 으로 저장
- `incrementViewCount(id)` 가 DB 의 `viewCnt` 를 1 로 만듦 (영속성 컨텍스트는 모름)
- `b.getViewCnt()` 는 영속성 컨텍스트의 *옛 값* 0 을 반환

**수정 1**: `clearAutomatically = true`
```java
@Modifying(clearAutomatically = true)
@Query("UPDATE Board b SET b.viewCnt = b.viewCnt + 1 WHERE b.id = :id")
int incrementViewCount(@Param("id") Long id);
```
쿼리 후 영속성 컨텍스트 clear → 다음 `findById` 가 DB 에서 새로 가져옴.

**수정 2** (더 자연스러운 방법): **Dirty Checking 사용**
```java
@Transactional
public void incrementAndCheck(Long id) {
    Board b = boardRepo.findById(id).orElseThrow();
    b.setViewCnt(b.getViewCnt() + 1);   // dirty checking 으로 UPDATE
    System.out.println(b.getViewCnt()); // 1 출력
}
```

`@Modifying` 은 *bulk* 변경에만. 단건은 dirty checking 이 안전.

</details>

---

### Q10. (디버그) `deleteById(id)` 호출 시 발행되는 *SQL 쿼리 개수* 와 그 이유. 단일 DELETE 만 원하면?

<details><summary>정답</summary>

**쿼리 개수: 2 개**
1. `SELECT ... FROM t WHERE id = ?` — 엔티티 존재 확인 (없으면 `EmptyResultDataAccessException`)
2. `DELETE FROM t WHERE id = ?` — 실제 삭제

이유: `deleteById` 내부 구현이 *`findById` 후 `remove`*. 영속성 컨텍스트에 등록된 후 삭제 처리 (cascade·orphanRemoval 적용 위해).

**단일 DELETE 만 원하면**:

```java
@Modifying
@Query("DELETE FROM Board b WHERE b.id = :id")
int deleteByIdDirect(@Param("id") Long id);
```

또는 `deleteAllByIdInBatch(Iterable)` — bulk 처리. **다만** cascade·orphanRemoval 안 동작하므로 연관관계 있는 엔티티에는 주의.

</details>

---

### Q11. (디버그) 다음 Repository 가 *컴파일은 성공* 하는데 애플리케이션 시작 시 예외가 발생. 원인과 해결책.
```java
public interface BoardRepository extends JpaRepository<Board, Long> {
    List<Board> findByViewCount(int min);   // (?)
}

// Board 엔티티의 실제 필드명
private int viewCnt;
```

<details><summary>정답</summary>

**원인**: 메서드 이름의 `ViewCount` 가 엔티티 필드명 `viewCnt` 와 불일치.

Spring Data JPA 가 시작 시 *Repository 를 분석* 하면서 메서드 이름의 필드명을 엔티티의 실제 필드와 매칭. 매칭 실패 시 `PropertyReferenceException` 던지며 애플리케이션 시작 실패.

**다행스러운 점**: 컴파일 타임에 잡히진 않지만 *시작 시점* 에 잡힘 (런타임 호출 시점이 아님).

**해결책**:
```java
List<Board> findByViewCnt(int min);   // 엔티티 필드명에 맞춤
// 또는 정확한 의미라면
List<Board> findByViewCntGreaterThan(int min);
```

**예방**: `@DataJpaTest` 같은 통합 테스트로 Repository 메서드를 *시작 시점* 에 검증. CI 가 항상 돌리도록.

</details>

---

### Q12. (디버그) 다음 코드의 *치명적 함정* 을 지적하시오.
```java
@Query("SELECT b FROM Board b LEFT JOIN FETCH b.replies WHERE b.categoryId = :cid")
Page<Board> findByCategoryWithReplies(@Param("cid") Long cid, Pageable pageable);
```

<details><summary>정답</summary>

**함정**: **`OneToMany` 컬렉션에 대한 `JOIN FETCH` + 페이징 (`Pageable`) 동시 사용**.

이유:
- `LEFT JOIN FETCH b.replies` 는 게시글 한 개당 댓글 N 개를 *플랫한 row* 로 가져옴. 즉 결과 set 의 size 가 *부풀려짐*
- 페이징은 DB 의 `LIMIT/OFFSET` 으로 *row 단위* 자름 — 댓글까지 합친 row 가 잘려서 게시글이 *완전 로딩 안 됨*
- Hibernate 는 이를 감지하고 **경고 로그 + 메모리 페이징** 으로 fallback: *전체 결과를 메모리로 가져와* 페이징 → **데이터 폭증 시 OOM**

해결책:

**방법 1: DTO Projection** (권장)
```java
@Query("""
    SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer)
    FROM Board b WHERE b.categoryId = :cid
""")
Page<BoardSummary> findSummariesByCategory(@Param("cid") Long cid, Pageable pageable);
```
댓글이 필요하면 *별도 쿼리* 로.

**방법 2: 두 쿼리로 분리**
- 1차: 페이징해서 게시글 PK 목록 가져옴
- 2차: 그 PK 들로 댓글 IN 절 조회 (또는 `@BatchSize`)

**방법 3: `OneToOne` 이나 `ManyToOne` 의 JOIN FETCH 는 페이징과 함께 사용 OK** (row 가 안 부풀어).

</details>

---

### Q13. (면접) "Spring Data JPA 는 어떻게 인터페이스만 정의해도 동작하나요?" 면접관 단골. 1분 답변.

<details><summary>정답</summary>

핵심 답변:

> Spring 이 시작 시 `@EnableJpaRepositories` 가 classpath 를 스캔하여 `JpaRepository` 를 상속하는 인터페이스를 찾고, 각각에 대해 **동적 프록시 클래스를 런타임에 생성** 합니다. 프록시는 호출되는 메서드를 분석해서:
> - 표준 메서드 (`save`, `findById` 등) 는 내부 구현 `SimpleJpaRepository` 에 위임
> - 메서드 이름 규칙에 맞으면 JPQL 을 자동 생성
> - `@Query` 가 있으면 그 JPQL/SQL 을 실행
> 
> 이 프록시 객체가 Spring 빈으로 등록되어 `@Autowired` 또는 생성자 주입으로 들어옵니다. 컴파일 타임에는 구현체가 존재하지 않고 런타임에 만들어지는 게 특징입니다.

추가로 알면 좋음:
- `SimpleJpaRepository` 가 기본 구현체 (Spring Data JPA 의 핵심 클래스)
- 메서드 이름 분석은 `PartTree` 라는 내부 컴포넌트가 담당

</details>

---

### Q14. (면접) "메서드 이름 규칙 / `@Query` / QueryDSL 을 어떻게 구분해서 쓰시나요?"

<details><summary>정답</summary>

**선택 기준 — 복잡도 순**:

| 기준 | 메서드 이름 규칙 | `@Query` (JPQL) | QueryDSL |
|--|--|--|--|
| 가독성 | 짧으면 좋음 (1~3 조건) | 어떤 길이도 OK | 타입 안전, 자바 코드처럼 |
| 컴파일 타임 검증 | 시작 시 (필드명 매칭) | 시작 시 (JPQL 파싱) | **컴파일 타임** |
| 동적 조건 | 불가 | 어렵 (문자열 조작) | **자연스러움** |
| IDE 자동완성 | 한계 | JPQL 문법 한계 | **완벽** |
| 학습 곡선 | 낮음 | 중 | 중상 (Q-class 생성, gradle 설정) |

**실무 가이드**:
- **1~3 개 조건**, 정적 → **메서드 이름**
- **4+ 조건** 또는 **JOIN**, 정적 → **`@Query`**
- **동적 조건** (검색 폼 등 런타임 결정), 복잡 → **QueryDSL**
- **DB 특화 기능** (full-text 등) → `@Query(nativeQuery = true)`

대부분의 프로젝트는 *세 가지를 섞어* 사용. 단순 CRUD 는 메서드 이름, 복잡 보고서는 QueryDSL.

</details>
