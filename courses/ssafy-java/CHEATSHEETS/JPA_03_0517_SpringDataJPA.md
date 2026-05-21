# JPA 3강: Spring Data JPA — 치트시트

> 인터페이스 한 줄로 Repository 완성. JpaRepository · 메서드 이름 규칙 · @Query · 페이징 · @Modifying · Projection.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄

1. **인터페이스만 선언, 구현은 Spring 이 런타임 프록시로 자동**. 컴파일 타임에는 구현체 없음.
2. `JpaRepository<T, ID>` 상속만으로 `save / findById / findAll / count / delete / 페이징` 등 자동 제공.
3. **메서드 이름 규칙**: `findBy / countBy / existsBy / deleteBy` + 조건 (`Containing`, `GreaterThan`, `In`, ...) + `OrderBy{필드}Desc`. 1~3 조건이면 쓰기 좋음.
4. **`@Query`**: 엔티티 기준 JPQL 직접. **DTO 매핑** (`SELECT new pkg.DTO(...)`) 으로 LAZY 함정·네트워크 효율 잡기.
5. **페이징**: `Page<T>` (COUNT 포함) vs `Slice<T>` (가벼움, 무한 스크롤용). `Pageable` + `Sort`.
6. **`@Modifying`** bulk UPDATE/DELETE 는 영속성 컨텍스트 우회 → `clearAutomatically = true` 안 붙이면 옛 캐시 봄.

## 가장 중요한 코드 3개

```java
// (1) 가장 단순한 Repository - 한 줄로 완성
public interface BoardRepository extends JpaRepository<Board, Long> {
    // CRUD + 페이징/정렬 자동
}
```

```java
// (2) 메서드 이름 규칙으로 조건 검색
public interface BoardRepository extends JpaRepository<Board, Long> {
    List<Board> findByWriterAndViewCntGreaterThanOrderByRegDateDesc(String w, int min);
    Page<Board> findByTitleContaining(String keyword, Pageable pageable);
    boolean existsByEmail(String email);
    long countByCategoryId(Long categoryId);
}
```

```java
// (3) @Query + DTO Projection + 페이징
@Query("""
    SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer)
    FROM Board b WHERE b.categoryId = :cid
""")
Page<BoardSummary> findSummaries(@Param("cid") Long cid, Pageable pageable);
```

## 면접 한 줄 답변

- **Q. Spring Data JPA 가 인터페이스만 정의해도 동작하는 원리는?** → 시작 시 classpath 스캔으로 `JpaRepository` 상속 인터페이스 발견 → **런타임 동적 프록시 생성** → `SimpleJpaRepository` 위임 + 메서드 이름·`@Query` 분석으로 JPQL 자동 발행.
- **Q. `Page<T>` vs `Slice<T>` 의 차이는?** → **Page** 는 전체 개수 (`COUNT(*)`) 포함, 페이지네이션 UI 용. **Slice** 는 COUNT 안 함, hasNext 만 — **무한 스크롤용**.
- **Q. `@Modifying` 의 함정은?** → bulk UPDATE/DELETE 가 **영속성 컨텍스트 우회**. 같은 트랜잭션 안의 managed 엔티티는 옛 값 그대로. `clearAutomatically = true` 로 해결.
- **Q. 메서드 이름 / `@Query` / QueryDSL 선택 기준?** → 정적 1~3 조건은 이름, 정적 4+ 조건/JOIN 은 `@Query`, **동적 조건** 은 QueryDSL.

---

# 2. Quick Reference (실무 복붙)

## 2.1 JpaRepository 자동 제공 메서드

| 메서드 | 동작 | 비고 |
|--|--|--|
| `save(e)` | INSERT 또는 UPDATE | persist/merge 분기 |
| `saveAll(iter)` | 다건 저장 | |
| `findById(id)` | PK 단건 | `Optional<T>` |
| `findAll()` | 전체 | |
| `findAll(Sort)` | 정렬 | |
| `findAll(Pageable)` | 페이징 | `Page<T>` 반환, COUNT 포함 |
| `findAllById(iter)` | PK 다건 IN 절 | |
| `count()` / `existsById(id)` | COUNT / EXISTS | |
| `delete(e)` / `deleteById(id)` | 단건 삭제 | `deleteById` 는 SELECT + DELETE 두 쿼리 |
| `deleteAllInBatch()` | bulk DELETE | 영속성 컨텍스트 우회 |
| `flush()` | 즉시 flush | |

## 2.2 메서드 이름 규칙

**접두어**: `findBy` / `existsBy` / `countBy` / `deleteBy` / `findFirstBy` / `findTop{N}By`

**조건 키워드**:

| 키워드 | SQL |
|--|--|
| `Equals` (기본) | `=` |
| `Containing` / `StartingWith` / `EndingWith` | `LIKE` |
| `GreaterThan` / `LessThan` / `GreaterThanEqual` / `LessThanEqual` | `>` / `<` / `>=` / `<=` |
| `Between(a, b)` | `BETWEEN a AND b` |
| `In(coll)` / `NotIn(coll)` | `IN` / `NOT IN` |
| `IsNull` / `IsNotNull` | `IS NULL` / `IS NOT NULL` |
| `True` / `False` | `= true` / `= false` |
| `IgnoreCase` | `LOWER(...) = LOWER(...)` |

**연결자**: `And` / `Or` / `OrderBy{필드명}Asc|Desc`

## 2.3 @Query (JPQL)

```java
// 기본
@Query("SELECT b FROM Board b WHERE b.viewCnt > :min")
List<Board> popular(@Param("min") int min);

// DTO 매핑
@Query("SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer) FROM Board b")
List<BoardSummary> summaries();

// JOIN FETCH (4 강 미리)
@Query("SELECT b FROM Board b LEFT JOIN FETCH b.replies WHERE b.id = :id")
Optional<Board> findWithReplies(@Param("id") Long id);

// native
@Query(value = "SELECT * FROM board WHERE MATCH(title) AGAINST(:kw)", nativeQuery = true)
List<Board> fullText(@Param("kw") String kw);
```

## 2.4 페이징

```java
// 메서드
Page<Board> findAll(Pageable p);
Slice<Board> findByWriter(String w, Pageable p);

// 호출
PageRequest.of(0, 10, Sort.by("regDate").descending());

// Controller 자동 바인딩
@GetMapping("/boards")
public Page<Board> list(@PageableDefault(size=10, sort="regDate") Pageable p) {
    return repo.findAll(p);
}
// URL: ?page=0&size=20&sort=regDate,desc&sort=title,asc
```

`Page<T>` 메서드: `getContent()`, `getTotalElements()`, `getTotalPages()`, `getNumber()`, `hasNext()`, `hasPrevious()`.
`Slice<T>` 는 `getTotalElements/Pages` 없음 (COUNT 안 함).

## 2.5 @Modifying

```java
@Modifying(clearAutomatically = true, flushAutomatically = true)
@Query("UPDATE Board b SET b.viewCnt = 0 WHERE b.categoryId = :cid")
int resetByCategory(@Param("cid") Long cid);
```

- `@Modifying` **필수** (없으면 예외)
- `clearAutomatically = true`: 쿼리 후 영속성 컨텍스트 clear
- `flushAutomatically = true`: 쿼리 전 flush
- 반환: `int` (영향 row 수) 또는 `void`

## 2.6 Projection

```java
// Interface-based - Spring 이 자동 프록시
public interface BoardSummary {
    Long getId();
    String getTitle();
    String getWriter();
}
List<BoardSummary> findByCategoryId(Long cid);

// Class-based (DTO record)
public record BoardSummary(Long id, String title, String writer) {}
@Query("SELECT new com.example.dto.BoardSummary(b.id, b.title, b.writer) FROM Board b WHERE ...")
List<BoardSummary> summaries(...);

// Dynamic - 사용처에서 결정
<T> List<T> findByCategoryId(Long cid, Class<T> type);
```

## 2.7 자주 빠지는 함정 모음

| 함정 | 정정 |
|--|--|
| 메서드 이름 5+ 조건 | `@Query` 로 전환 |
| `@Modifying` 빠짐 → 예외 | 반드시 부착 |
| `@Modifying` 후 옛 캐시 | `clearAutomatically = true` |
| `deleteById` 가 SELECT + DELETE | 직접 DELETE 원하면 `@Modifying DELETE` |
| `Page<T>` + `JOIN FETCH OneToMany` | OOM 위험. **DTO Projection** 또는 두 쿼리 분리 |
| `Slice` 알면서도 항상 `Page` 사용 | 무한 스크롤·다음 버튼만 필요면 `Slice` |
| 메서드 이름 필드명 오타 | 시작 시 `PropertyReferenceException` — 테스트로 빨리 잡기 |
| native query 남용 | DB 종속. 특수 기능에만 |
| 동적 조건을 메서드 이름으로 | 불가. Specifications 또는 QueryDSL |

## 2.8 약어 표

| 약어 | 풀어쓰기 |
|--|--|
| JPQL | Java Persistence Query Language |
| DTO | Data Transfer Object |
| OOM | OutOfMemoryError |
| PK / FK | Primary Key / Foreign Key |
| CRUD | Create / Read / Update / Delete |
| AOP | Aspect-Oriented Programming |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 3.1 JPA 5강 시리즈 토픽 트리

```
JPA Series
│
├── [1강] 개념 + Entity 매핑
│   └── @Entity / @Id / @Column / enum.STRING / Auditing
│
├── [2강] 영속성 컨텍스트
│   ├── 1차 캐시 / 4 상태 / Dirty Checking / flush / OSIV
│   └── EntityManager API
│
├── [3강] Spring Data JPA          <- 현재 위치
│   ├── 동작 원리
│   │   ├── @EnableJpaRepositories
│   │   ├── 동적 프록시 (런타임 생성)
│   │   └── SimpleJpaRepository (기본 구현)
│   │
│   ├── JpaRepository 자동 제공 메서드
│   │   ├── save / findById / findAll
│   │   ├── count / existsById
│   │   ├── delete / deleteById / deleteAllInBatch
│   │   └── findAll(Pageable) / findAll(Sort)
│   │
│   ├── 메서드 이름 규칙 (Derived Query)
│   │   ├── 접두어 (findBy / countBy / existsBy / deleteBy)
│   │   ├── 조건 (Containing / GreaterThan / Between / In / IgnoreCase)
│   │   ├── 연결자 (And / Or / OrderBy)
│   │   └── 한계 (5+ 조건 폭주, 동적 조건 불가)
│   │
│   ├── @Query (JPQL)
│   │   ├── 엔티티 기준 (필드명 사용)
│   │   ├── @Param 바인딩
│   │   ├── DTO 매핑 (SELECT new pkg.DTO(...))
│   │   ├── JOIN FETCH (4 강 미리보기)
│   │   └── nativeQuery (escape hatch)
│   │
│   ├── 페이징
│   │   ├── Pageable / PageRequest / Sort
│   │   ├── Page<T>  (COUNT 포함)
│   │   ├── Slice<T> (가벼움, hasNext)
│   │   └── @PageableDefault, URL 바인딩
│   │
│   ├── @Modifying
│   │   ├── bulk UPDATE / DELETE
│   │   ├── 영속성 컨텍스트 우회 함정
│   │   ├── clearAutomatically / flushAutomatically
│   │   └── vs Dirty Checking (단건은 dirty, bulk 는 @Modifying)
│   │
│   └── Projection
│       ├── Interface-based (Spring 자동 프록시)
│       ├── Class-based (DTO / record)
│       └── Dynamic (Class<T> 인자)
│
├── [4강] 연관관계 매핑
│   ├── @ManyToOne / @OneToMany / @OneToOne / @ManyToMany
│   ├── mappedBy / 주인 / 양방향
│   ├── fetch (LAZY / EAGER)
│   ├── N+1 문제와 해결 (JOIN FETCH / EntityGraph / BatchSize)
│   └── cascade / orphanRemoval
│
└── [5강] JPQL + 트랜잭션
    └── JPQL 심화 / @Transactional 옵션 / Specifications / QueryDSL 맛보기
```

## 3.2 3강 학습 진도 체크리스트

### 동작 원리
- [ ] `@EnableJpaRepositories` 가 시작 시 무엇을 하는지 안다
- [ ] 동적 프록시가 런타임에 생성된다는 점 안다
- [ ] `SimpleJpaRepository` 가 기본 구현체인 것 안다
- [ ] 컴파일 타임에 구현체가 없는 게 정상임을 안다

### JpaRepository
- [ ] `save`, `findById`, `findAll`, `count`, `existsById`, `deleteById` 의 SQL 외움
- [ ] `deleteById` 가 *SELECT + DELETE* 두 쿼리임을 안다
- [ ] `deleteAllInBatch` 가 *영속성 컨텍스트 우회* 임을 안다

### 메서드 이름 규칙
- [ ] 접두어 4 종 + 조건 키워드 6 종 외움
- [ ] `And`, `Or`, `OrderBy` 사용법 안다
- [ ] `IgnoreCase` 의 SQL (`LOWER`) 안다
- [ ] 5+ 조건 시 `@Query` 로 전환할 줄 안다

### @Query
- [ ] JPQL 이 *엔티티 기준* 임을 안다 (테이블 X, 필드명)
- [ ] `@Param` 바인딩 안다
- [ ] DTO 매핑 `SELECT new pkg.DTO(...)` 작성 가능
- [ ] native query 의 사용 시기 안다

### 페이징
- [ ] `Page<T>` 와 `Slice<T>` 의 차이 (COUNT 유무) 안다
- [ ] `PageRequest.of(page, size, Sort)` 사용 가능
- [ ] Controller 의 `@PageableDefault` + URL 바인딩 패턴 안다
- [ ] `Page<T>` 의 주요 메서드 (`getTotalElements`, `getTotalPages`, `hasNext` ...) 알고 있다

### @Modifying
- [ ] bulk UPDATE/DELETE 시 `@Modifying` 필수임을 안다
- [ ] *영속성 컨텍스트 우회* 함정 안다
- [ ] `clearAutomatically` 옵션의 의미 안다
- [ ] 단건은 dirty checking 이 더 안전함을 안다

### Projection
- [ ] Interface-based / Class-based / Dynamic 의 차이 안다
- [ ] DTO Projection 이 LAZY 함정·페이징·JOIN FETCH 문제를 해결함을 안다

## 3.3 다음 학습 흐름

```
3강 Spring Data JPA (현재)
    │
    │  ─ Repository 패턴이 손에 잡혔다면 ─
    v
4강 연관관계 매핑   ← *가장 함정 많음*
    ─ @ManyToOne, @OneToMany, mappedBy
    ─ fetch (LAZY/EAGER) + N+1 문제 + JOIN FETCH
    ─ cascade, orphanRemoval
    │
    v
5강 JPQL + 트랜잭션 (마지막)
    ─ JPQL 심화 + @Transactional 옵션
    ─ Specifications / QueryDSL 맛보기

병행 학습:
  - application.yml: spring.jpa.show-sql / format-sql 켜기 (발행 SQL 눈으로)
  - @DataJpaTest 로 Repository 단위 테스트
  - QueryDSL 시작 (4강 끝나면)
```

## 3.4 3강 자기 점검 신호

- "메서드 이름 규칙은 너무 길어. `@Query` 로 가자." 가 자연스러우면 → 통과
- "이 동적 조건은 메서드 이름으로 안 되네" 가 떠오르면 → QueryDSL 학습 시작 시점
- "`@Modifying` 했더니 영속성 컨텍스트 옛 값이 나와" → 2 강 + Part F 복습
- "페이징 + JOIN FETCH 가 메모리 폭증" → 4 강 (연관관계) 미리 학습 권장
- "Repository 시작 시 PropertyReferenceException" → 메서드 이름 규칙의 *필드명* 매칭 실패. 엔티티 필드명 재확인
