# JPA 5강: JPQL 심화 + 트랜잭션 + 그 다음

> **이 강의는 무엇인가**: JPA 시리즈 마지막. JPQL 의 *심화 문법* (서브쿼리·CASE·집계), `@Transactional` 의 *진짜 옵션* (propagation·isolation·rollbackFor·readOnly), 그리고 그 다음 단계인 *Specifications* 와 *QueryDSL*.
> **왜 배우는가**: 4강까지가 *기본기* 라면 5강은 *실무·면접의 깊이*. 트랜잭션을 이해하지 못한 채 JPA 를 쓰면 동시성·격리 사고가 발생. QueryDSL 은 실무 신규 프로젝트의 표준.

---

## 들어가기 전에

- **선수**: 1~4 강 전체. 특히 2 강 (영속성 컨텍스트) 과 4 강 (연관관계·N+1) 이 5 강의 기반.
- **마인드셋**: "JPA 의 모든 마법은 *트랜잭션 안* 에서 일어난다." 이 강은 그 트랜잭션의 *경계와 옵션* 을 정밀하게 다룸.
- **시리즈 종착점**: 5 강 끝나면 *JPA 의 핵심* 은 손에 잡힘. 그 뒤는 *실무 경험* 과 *팀의 코딩 컨벤션* 으로 다듬는 단계.

---

# Part A. JPQL 심화

3 강에서 본 JPQL 의 기본은 *엔티티 기준 SELECT*. 5 강에서는 그 위의 심화.

## 1. JOIN 의 종류

```java
// 1) 묵시적 JOIN - 비추
@Query("SELECT b FROM Board b WHERE b.category.name = :name")
List<Board> findByCategoryName(@Param("name") String name);
// SQL 은 정상 JOIN 발행되지만, 어떤 JOIN 인지 *코드만 봐서 모름* (가독성 ↓)

// 2) 명시적 JOIN (조회 only)
@Query("SELECT b FROM Board b JOIN b.category c WHERE c.name = :name")
List<Board> findByCategoryNameExplicit(@Param("name") String name);
// JOIN 발행, 그러나 b.category 는 *LAZY 그대로* (조인은 했지만 가져오진 X)

// 3) JOIN FETCH (4강) - 즉시 로딩까지
@Query("SELECT b FROM Board b JOIN FETCH b.category WHERE b.id = :id")
Optional<Board> findByIdWithCategory(@Param("id") Long id);

// 4) LEFT JOIN - null 포함
@Query("SELECT b FROM Board b LEFT JOIN b.replies r")
List<Board> findAllLeft();
```

| 종류 | 결과 | 사용 |
|--|--|--|
| 묵시적 JOIN (`b.category.name`) | inner join 자동 | 짧은 코드, 가독성 떨어짐 — 권장 X |
| 명시적 JOIN (`JOIN b.category c`) | inner join | 조건만 필요 (연관 객체 안 가져옴) |
| `JOIN FETCH` | inner join + 즉시 로딩 | 4 강의 N+1 회피 |
| `LEFT JOIN` / `LEFT JOIN FETCH` | outer join | 자식 없는 부모도 포함 |

## 2. 서브쿼리

JPQL 도 서브쿼리 지원. 단, **SELECT 또는 WHERE 절만** (FROM 절 서브쿼리 — Hibernate 6+ 부터 일부 지원).

```java
// 댓글이 N 개 이상인 게시글
@Query("""
    SELECT b FROM Board b
    WHERE (SELECT COUNT(r) FROM Reply r WHERE r.board = b) >= :n
""")
List<Board> findWithReplyCountAtLeast(@Param("n") int n);

// EXISTS / NOT EXISTS
@Query("""
    SELECT b FROM Board b
    WHERE NOT EXISTS (SELECT r FROM Reply r WHERE r.board = b)
""")
List<Board> findWithNoReplies();

// ANY / ALL / SOME
@Query("""
    SELECT b FROM Board b
    WHERE b.viewCnt > ALL (SELECT b2.viewCnt FROM Board b2 WHERE b2.writer = :w)
""")
List<Board> moreViewsThanAllOf(@Param("w") String writer);
```

> **함정**: FROM 절 서브쿼리는 *대부분 안 됨*. 복잡한 *집계 → 다시 조회* 는 두 쿼리로 나누거나 native query.

## 3. CASE · COALESCE · NULLIF

```java
@Query("""
    SELECT b.id,
           CASE
               WHEN b.viewCnt > 1000 THEN 'POPULAR'
               WHEN b.viewCnt > 100  THEN 'NORMAL'
               ELSE 'NEW'
           END
    FROM Board b
""")
List<Object[]> findWithLevel();

// COALESCE - 첫 non-null 반환 (SQL 의 동일 함수)
@Query("SELECT COALESCE(b.title, '제목 없음') FROM Board b WHERE b.id = :id")
String getTitleOrDefault(@Param("id") Long id);

// NULLIF - 같으면 null, 다르면 첫 값
@Query("SELECT NULLIF(b.title, '삭제됨') FROM Board b")
List<String> getTitlesOrNull();
```

## 4. 집계와 GROUP BY · HAVING

```java
// 글쓴이별 게시글 수
@Query("""
    SELECT b.writer, COUNT(b)
    FROM Board b
    GROUP BY b.writer
    HAVING COUNT(b) >= :min
""")
List<Object[]> countByWriter(@Param("min") long min);
```

`Object[]` 대신 DTO 로:

```java
public record WriterStat(String writer, long boardCount) {}

@Query("""
    SELECT new com.example.dto.WriterStat(b.writer, COUNT(b))
    FROM Board b
    GROUP BY b.writer
    HAVING COUNT(b) >= :min
""")
List<WriterStat> writerStats(@Param("min") long min);
```

**집계 함수**: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

## 5. 페이징과 정적 조건의 한계

JPQL 의 강점: *컴파일 시점에 검증* (시작 시점, 정확히는). 단점:

- **동적 조건**: 검색 폼처럼 *조건 ON/OFF* 가 런타임에 결정되면 JPQL 문자열 조합이 *지저분*
- **컴파일 타임 보장 X**: 문자열이라 IDE 자동완성 한계, 오타는 시작 시점에 발견

**대안 두 가지**:
- **Specifications** (Criteria API 래퍼) — Part C
- **QueryDSL** — Part D (실무 표준)

---

# Part B. `@Transactional` 심화

2 강에서 본 `@Transactional` 의 기본 (`readOnly` 외) 을 깊이 다룸.

## 1. propagation — 트랜잭션 전파 (7 종)

```java
@Transactional(propagation = Propagation.REQUIRED)   // 기본
public void outer() {
    inner();
}

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void inner() { ... }
```

| propagation | 의미 |
|--|--|
| **REQUIRED** (기본) | 트랜잭션 있으면 참여, 없으면 새로 시작 |
| **REQUIRES_NEW** | *항상 새 트랜잭션*. 기존 트랜잭션은 일시 중단 |
| **SUPPORTS** | 있으면 참여, 없으면 트랜잭션 없이 실행 |
| **MANDATORY** | 있어야만 실행, 없으면 예외 |
| **NESTED** | 중첩 트랜잭션 (savepoint). 일부 DB 만 지원 |
| **NEVER** | 트랜잭션 있으면 예외. 트랜잭션 없이만 실행 |
| **NOT_SUPPORTED** | 항상 트랜잭션 없이. 기존이 있으면 중단 |

**실무에서 가장 자주 쓰는 것**: **REQUIRED** (기본) 와 **REQUIRES_NEW** (로그·감사 기록 등 *부모 실패해도 자식은 commit*).

### REQUIRES_NEW 의 예

```java
@Service @RequiredArgsConstructor
public class OrderService {

    private final AuditService auditService;

    @Transactional
    public void placeOrder(Order o) {
        orderRepo.save(o);
        auditService.log("주문: " + o.getId());   // 별도 트랜잭션
        // 여기서 예외 발생 → order 는 롤백, 그러나 audit log 는 *남아있음*
    }
}

@Service
public class AuditService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void log(String msg) {
        auditRepo.save(new AuditLog(msg, LocalDateTime.now()));
    }
}
```

이렇게 *부모와 독립적 트랜잭션* 으로 운영. 로그·감사·외부 알림에 흔히 사용.

## 2. isolation — 격리 수준 (4 단계)

```java
@Transactional(isolation = Isolation.READ_COMMITTED)
public Order getOrder(Long id) { ... }
```

| isolation | 의미 | 일반적 DB 디폴트 |
|--|--|--|
| `READ_UNCOMMITTED` | dirty read 가능 (안 정해진 데이터 읽음) | — |
| **`READ_COMMITTED`** | commit 된 것만 읽음 | PostgreSQL, Oracle |
| **`REPEATABLE_READ`** | 같은 트랜잭션 안에서 같은 row 는 같은 값 | MySQL InnoDB |
| `SERIALIZABLE` | 가장 엄격, 동시성 ↓ | — |

**대부분 DB 기본값 그대로 둠**. 명시적 isolation 은:
- 보고서·집계 트랜잭션을 `REPEATABLE_READ` 또는 `SERIALIZABLE` 로 강화
- 짧은 단순 조회를 `READ_COMMITTED` 로 완화

## 3. rollbackFor / noRollbackFor

**기본 동작**: `RuntimeException` (unchecked) 발생 시 롤백. `Exception` (checked) 은 **롤백 X** ❗

```java
@Transactional   // checked exception 시 commit (위험!)
public void process() throws IOException {
    orderRepo.save(...);
    Files.readAllBytes(somePath);   // IOException 발생 → 그래도 commit!
}
```

**해결**:

```java
@Transactional(rollbackFor = Exception.class)   // 모든 예외 시 롤백
public void process() throws IOException { ... }
```

또는 *RuntimeException 으로 래핑*:

```java
try {
    Files.readAllBytes(somePath);
} catch (IOException e) {
    throw new RuntimeException(e);   // unchecked 로 변환
}
```

실무 가이드: **모든 `@Transactional` 에 `rollbackFor = Exception.class` 또는 코딩 컨벤션** 으로 통일. 또는 *모든 예외를 RuntimeException 으로* 일관 처리.

## 4. readOnly — 조회 전용 최적화

2 강에서 본 `@Transactional(readOnly = true)`:

```java
@Transactional(readOnly = true)
public Board getBoard(Long id) {
    return boardRepo.findById(id).orElseThrow();
}
```

효과 (*정정 — JPA_02 의 함정 참고*):
- **JDBC connection `setReadOnly(true)`** — driver 가 무시 가능
- **Hibernate FlushMode → `MANUAL`/`COMMIT`** — *commit 시 자동 flush 안 함* → Dirty Checking 효과 *결과적으로* 없어짐 (snapshot 자체는 여전히 생성)
- 일부 DB 는 `read-only` 트랜잭션을 *별도 최적화* (예: PostgreSQL)

> **주의**: "snapshot 자체를 안 만든다" 는 *흔한 오해*. 실제는 *flush 안 일어남* 으로 변경이 DB 반영 안 됨.

**원칙**: SELECT 만 하는 모든 메서드에 `readOnly = true`. 클래스 레벨로:

```java
@Service
@Transactional(readOnly = true)   // 클래스 전체 기본
public class BoardService {

    @Transactional   // 메서드별 override - 변경 메서드만
    public Board create(...) { ... }
}
```

## 5. timeout — 트랜잭션 시간 제한

```java
@Transactional(timeout = 30)   // 30 초
public Report heavyReport() { ... }
```

긴 보고서·배치성 트랜잭션에 안전장치. 초과 시 `TransactionTimedOutException`.

## 5a. 동시성 제어 — @Version + @Lock

**Optimistic Locking** (`@Version`) — version 컬럼 기반:
```java
@Entity
public class Account {
    @Id Long id;
    int balance;

    @Version
    Long version;   // commit 시 자동 증가 + 비교
}
```

- Read 시점의 version → update 시점에 *다르면* `OptimisticLockException`
- *retry 책임 application* — `@Retryable` 또는 manual catch

**Pessimistic Locking** (`@Lock`) — DB 단위 잠금:
```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("select a from Account a where a.id = :id")
Account findForUpdate(@Param("id") Long id);
```

- `LockModeType`:
  - `PESSIMISTIC_READ` — 공유 lock (SELECT ... FOR SHARE)
  - `PESSIMISTIC_WRITE` — 배타 lock (SELECT ... FOR UPDATE)
  - `OPTIMISTIC` — version check (@Version 필수)
  - `OPTIMISTIC_FORCE_INCREMENT` — version 강제 증가
  - `PESSIMISTIC_FORCE_INCREMENT` — 배타 + version 증가

**선택**:
- 충돌 *드묾* → optimistic (성능 우수)
- 충돌 *빈번* → pessimistic (deadlock 위험 ↑)
- *재고 차감, 송금* 등 critical → pessimistic 또는 optimistic + retry

## 6. AOP 프록시 함정 (2강 복습)

```java
@Service
public class BoardService {

    public void outer(Long id) {
        this.inner(id);     // ❌ 프록시 우회 → @Transactional 안 먹힘
    }

    @Transactional
    public void inner(Long id) { ... }
}
```

해결:
- 메서드를 *다른 클래스* 로 분리
- `@Lazy` self-injection
- outer 자체에 `@Transactional` 부착

이건 2 강에서 한 번 봤지만, 모든 트랜잭션 관련 사고의 30% 는 이 함정. 항상 의식.

## 7. @Transactional 옵션 정리

```java
@Transactional(
    propagation = Propagation.REQUIRED,      // 트랜잭션 전파
    isolation = Isolation.READ_COMMITTED,    // 격리 수준
    rollbackFor = Exception.class,           // 어느 예외에 롤백
    noRollbackFor = NotFoundException.class, // 예외 중 롤백 안 할 것
    timeout = 30,                            // 시간 제한 (초)
    readOnly = false                         // 조회 전용 여부
)
```

대부분 메서드는 `@Transactional` 단독 또는 `@Transactional(readOnly = true)` 만 사용. 나머지 옵션은 *필요한 곳에만* 명시.

---

# Part C. Specifications — 동적 조건의 표준 (1)

3 강에서 메서드 이름 규칙의 한계로 *동적 조건* 을 언급. Specifications 는 그 한 가지 답.

## 1. 사용

```java
public interface BoardRepository
    extends JpaRepository<Board, Long>, JpaSpecificationExecutor<Board> {
}
```

`JpaSpecificationExecutor` 가 자동 제공하는 메서드:
- `findOne(Specification)`
- `findAll(Specification)`
- `findAll(Specification, Pageable)`
- `findAll(Specification, Sort)`
- `count(Specification)`

```java
public class BoardSpecs {

    public static Specification<Board> writerEquals(String writer) {
        return (root, query, cb) -> writer == null
            ? null
            : cb.equal(root.get("writer"), writer);
    }

    public static Specification<Board> titleContains(String keyword) {
        return (root, query, cb) -> keyword == null
            ? null
            : cb.like(root.get("title"), "%" + keyword + "%");
    }

    public static Specification<Board> viewCntGte(Integer min) {
        return (root, query, cb) -> min == null
            ? null
            : cb.greaterThanOrEqualTo(root.get("viewCnt"), min);
    }
}

// 사용
Specification<Board> spec = Specification
    .where(BoardSpecs.writerEquals(form.getWriter()))
    .and(BoardSpecs.titleContains(form.getKeyword()))
    .and(BoardSpecs.viewCntGte(form.getMinView()));

Page<Board> result = boardRepo.findAll(spec, pageable);
```

null 조건은 자동 무시 (Spring Data 가 `null` 반환을 *조건 없음* 으로 해석).

## 2. 장점·단점

| | Specifications |
|--|--|
| 동적 조건 | **O** |
| 타입 안전 | 문자열 (`"writer"`) 사용 — 부분적 |
| 가독성 | Criteria API 의 함수형 패턴 — *익숙해지면 OK* |
| 학습 곡선 | 중상 |
| 컴파일 타임 검증 | 약함 (문자열) |

**결론**: 동적 조건이 필요한데 *QueryDSL 도입은 부담* 일 때. 대부분의 신규 프로젝트는 **QueryDSL** 로 직행.

---

# Part D. QueryDSL — 실무의 표준 (2)

## 1. 왜 QueryDSL

```java
// QueryDSL
QBoard b = QBoard.board;
List<Board> result = queryFactory
    .selectFrom(b)
    .where(
        writerEq(form.getWriter()),
        titleContains(form.getKeyword()),
        viewCntGte(form.getMinView())
    )
    .orderBy(b.regDate.desc())
    .offset(pageable.getOffset())
    .limit(pageable.getPageSize())
    .fetch();

private BooleanExpression writerEq(String w) {
    return w == null ? null : QBoard.board.writer.eq(w);
}
```

**장점**:
- **컴파일 타임 타입 안전** (`b.writer` 가 진짜 필드인지 IDE 가 검증)
- IDE 자동완성 완벽
- 동적 조건 자연스러움 (null 반환 시 자동 무시)
- 가독성 좋음

**단점**:
- Q-class 생성 설정 (Gradle/Maven)
- 학습 곡선 (Criteria API 보다 낫지만 여전히 학습 필요)
- 도구 의존 (의존성·코드 생성)

## 2. 설정 한 줄 요약

Gradle 의 `build.gradle.kts` 예 (*modern 방식 — Gradle 7+ 호환*):

```kotlin
dependencies {
    implementation("com.querydsl:querydsl-jpa:5.0.0:jakarta")
    annotationProcessor("com.querydsl:querydsl-apt:5.0.0:jakarta")
    annotationProcessor("jakarta.persistence:jakarta.persistence-api")
    annotationProcessor("jakarta.annotation:jakarta.annotation-api")
}
```

> **주의 — `com.ewerk.gradle.plugins.querydsl` plugin 은 deprecated** (Gradle 7+ 비호환). 위 처럼 *annotationProcessor 만으로* QClass 자동 생성. 생성 위치는 `build/generated/sources/annotationProcessor/java/main` (Gradle 5+ 기본).

빌드 시 `@Entity` 마다 `QXxx` 클래스 자동 생성 (`build/generated/...`).

## 3. JPAQueryFactory 빈 등록

```java
@Configuration
public class QueryDslConfig {
    @Bean
    public JPAQueryFactory jpaQueryFactory(EntityManager em) {
        return new JPAQueryFactory(em);
    }
}
```

## 4. 동적 where — BooleanBuilder vs BooleanExpression

```java
// 1) BooleanBuilder
BooleanBuilder builder = new BooleanBuilder();
if (writer != null) builder.and(b.writer.eq(writer));
if (keyword != null) builder.and(b.title.contains(keyword));
queryFactory.selectFrom(b).where(builder).fetch();

// 2) BooleanExpression - 더 깔끔 (권장)
queryFactory.selectFrom(b)
    .where(writerEq(writer), titleContains(keyword))
    .fetch();
// null 반환 자동 무시
```

`BooleanExpression` 메서드는 *재사용·조합* 도 자연스러움.

## 5. 페치 조인 + 페이징

QueryDSL 도 JOIN FETCH 의 *페이징 함정* 은 동일. **DTO Projection 권장**.

```java
queryFactory
    .select(Projections.constructor(BoardSummary.class, b.id, b.title))
    .from(b)
    .where(...)
    .offset(...)
    .limit(...)
    .fetch();
```

`Projections.constructor` 가 DTO 의 생성자에 자동 매핑.

## 6. 면접 포인트

면접관의 단골 질문 — "QueryDSL 을 왜 쓰시나요?"

> "메서드 이름 규칙은 정적 조건에, `@Query` 는 정적 복잡 쿼리에 좋지만, *동적 조건* (검색 폼 등 런타임 결정) 에는 한계가 있습니다. QueryDSL 은 *컴파일 타임 타입 안전* + *동적 조건* + *IDE 자동완성* 의 세 가지를 모두 만족해서, 검색·보고서·복잡한 조회를 *깔끔하게 정리* 할 수 있습니다. 신규 프로젝트의 사실상 표준입니다."

---

# Part E. JPA 시리즈 정리

## 1. 5 강 한 줄 요약

| 강 | 핵심 |
|--|--|
| 1강 | `@Entity` 매핑. PK 는 Long, enum 은 STRING, Auditing 으로 시각 자동 |
| 2강 | 영속성 컨텍스트가 JPA 의 정체. Dirty Checking 의 3 조건. flush vs commit. OSIV |
| 3강 | Spring Data JPA — 인터페이스만 선언, 런타임 프록시. 메서드 이름·@Query·페이징·@Modifying·Projection |
| 4강 | 연관관계 — 주인은 FK 가진 쪽. 모든 fetch LAZY. N+1 의 4 해결책. @ManyToMany 안 씀 |
| 5강 | JPQL 심화 + @Transactional 옵션 + QueryDSL 로의 길 |

## 2. 실무에서 매일 의식해야 할 5 가지

1. **모든 연관관계 LAZY**
2. **N+1 의심**: 루프 안에서 LAZY 접근 = 빨간불
3. **`@Transactional(readOnly = true)`**: 조회 메서드의 기본
4. **JOIN FETCH + OneToMany + 페이징 = OOM 위험**
5. **bulk UPDATE 후 `clearAutomatically = true`** 또는 dirty checking 으로 단건 처리

## 3. 다음 단계 추천

- **QueryDSL 본격 학습** — 동적 검색, Projections, fetch join 활용
- **`@DataJpaTest`** — H2 in-memory 로 Repository 단위 테스트
- **p6spy 또는 hibernate.generate_statistics** — 실제 발행 SQL 모니터링
- **DDD Aggregate 패턴** — JPA cascade·orphanRemoval 과 자연스럽게 부합
- **Spring Batch** — 대량 데이터 처리. JPA 와의 통합 시 영속성 컨텍스트 관리 패턴 별도 학습 필요
- **DB 별 특화** — MySQL InnoDB 의 격리·잠금, PostgreSQL 의 JSONB·MVCC 등

---

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| JPQL 묵시적 JOIN (`b.category.name`) 만 사용 | 명시적 `JOIN` 또는 `JOIN FETCH` 권장 |
| FROM 절 서브쿼리 시도 | JPQL 표준 안 됨. 두 쿼리로 분리 또는 native |
| `@Transactional` 의 디폴트 `RuntimeException` 만 롤백 | `rollbackFor = Exception.class` 명시 또는 RuntimeException 으로 래핑 |
| `@Transactional` 같은 클래스 내부 호출 → AOP 우회 | 메서드 분리 또는 self-injection |
| `REQUIRES_NEW` 의 *부모 트랜잭션 일시 중단* 인지 모름 | 별도 트랜잭션이 *DB 커넥션 새로 점유* — 풀 고갈 주의 |
| isolation 을 기본값만 사용 | 보통은 DB 기본값 OK. 보고서·통계는 `REPEATABLE_READ` 고려 |
| `@Transactional(readOnly = true)` 안 붙임 | 조회 메서드는 무조건 readOnly. 클래스 레벨 + 변경 메서드만 override |
| Specifications 의 문자열 `"writer"` 오타 | 컴파일 시 안 잡힘. 통합 테스트로. QueryDSL 로 가면 해결 |
| QueryDSL 의 Q-class 가 안 생성 | `annotationProcessor` 등록·`build/generated` IDE 인식 확인 |
| `@Modifying` UPDATE 후 Service 안에서 같은 엔티티 setter 호출 | `clearAutomatically = true` 안 붙이면 옛 값. 또는 dirty checking 으로 통일 |
| 영속성 컨텍스트 *수명 = 트랜잭션* 잊고 별 메서드에서 LAZY 접근 | 2 강 OSIV / DTO 변환 |

---

## 자가점검

1. JPQL 의 *명시적 JOIN* 과 *JOIN FETCH* 의 차이.
2. JPQL 의 *서브쿼리* 가 가능한 절과 안 되는 절.
3. `@Transactional` 의 *propagation 7 종* 중 `REQUIRED` 와 `REQUIRES_NEW` 의 차이.
4. `@Transactional` 의 *디폴트 rollback 정책* 의 함정과 권장 해결.
5. `@Transactional(readOnly = true)` 의 *세 가지 효과*.
6. Specifications 의 *동적 조건 처리* 메커니즘 (null 반환 시?).
7. QueryDSL 이 `@Query` 보다 *우수한 점* 3 가지.
8. JPA 시리즈 5 강 한 줄씩 요약.
9. 실무에서 매일 의식해야 할 5 가지 원칙.
10. JPA 마스터 후 *다음 단계* 학습 주제 3 가지.

<details><summary>풀이</summary>

1. **명시적 JOIN**: 인 SQL JOIN 발행 but 연관 객체는 *LAZY 프록시* 그대로. **JOIN FETCH**: JOIN + *즉시 로딩* (실제 객체 로딩, 1차 캐시에 등록).
2. **가능**: SELECT, WHERE 절. **안 되는**: FROM 절 서브쿼리 (Hibernate 6+ 일부 지원). 복잡 시 두 쿼리로 분리.
3. **REQUIRED**: 트랜잭션 있으면 참여, 없으면 새로 시작 (가장 흔함). **REQUIRES_NEW**: 항상 *새 트랜잭션* 시작, 기존은 일시 중단. 부모 실패해도 자식 commit 가능 (로그·감사).
4. **함정**: 디폴트가 `RuntimeException` 만 롤백. `IOException` 같은 checked 예외는 발생해도 **commit**. **해결**: `rollbackFor = Exception.class` 명시 또는 RuntimeException 으로 래핑.
5. ① **스냅샷 미생성** → Dirty Checking 비활성, ② **flush mode 변경** → 불필요 flush 생략, ③ 일부 DB 의 **read-only 트랜잭션 최적화**.
6. `Specification` 의 람다가 **null 을 반환하면** Spring Data 가 *조건 없음* 으로 해석 → 동적 조건 자연스럽게.
7. ① **컴파일 타임 타입 안전** (`b.writer` 가 진짜 필드인지 검증), ② **IDE 자동완성 완벽**, ③ **동적 조건 자연스러움** + 메서드 재사용·조합.
8. 1강: `@Entity` 매핑 / 2강: 영속성 컨텍스트 (1차 캐시·Dirty Checking·flush·OSIV) / 3강: Spring Data JPA (Repository·메서드 이름·@Query·페이징·@Modifying) / 4강: 연관관계 (주인·LAZY·N+1·cascade) / 5강: JPQL 심화 + @Transactional + QueryDSL.
9. ① 모든 연관관계 LAZY, ② N+1 의심, ③ 조회는 readOnly=true, ④ JOIN FETCH + OneToMany + 페이징 금지, ⑤ bulk UPDATE 후 clearAutomatically 또는 dirty checking 으로 통일.
10. **QueryDSL** (동적 쿼리 표준) / **`@DataJpaTest`** (Repository 단위 테스트) / **DDD Aggregate** (cascade 와 자연 부합) / **Spring Batch** (대량 처리) / **DB 별 특화** (MySQL InnoDB 잠금, PostgreSQL JSONB).

</details>

---

## 다음 학습으로

JPA 시리즈는 5 강으로 *완결*. 다음은 *옆으로 넓히는* 단계.

### 즉시 학습 권장
- **QueryDSL 본격 학습** — 신규 프로젝트의 표준
- **`@DataJpaTest`** + H2 — Repository TDD
- **p6spy** — 발행 SQL 모니터링 + N+1 자동 감지

### 1~2 개월 후
- **DDD (Domain-Driven Design)** — Aggregate Root + cascade
- **Spring Batch** — 대량 데이터 처리 (영속성 컨텍스트 분리 패턴)
- **Caffeine + JPA 2차 캐시** — 적절한 곳에 캐싱

### 인접 분야
- **JOOQ** — JPA 의 대안. SQL 중심 + 타입 안전 (QueryDSL 의 SQL 사촌)
- **Hibernate Reactive** — 비동기 reactive 스택 (WebFlux 와 결합)
- **MyBatis 와의 공존** — 한 프로젝트에서 복잡한 보고서는 MyBatis, CRUD 는 JPA
