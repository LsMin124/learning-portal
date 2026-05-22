# JPA 5강: JPQL 심화 + 트랜잭션 — 퀴즈

> 14문항. 개념·적용·디버그·면접. JPQL JOIN·서브쿼리 / @Transactional propagation·isolation·rollbackFor / Specifications / QueryDSL 자가 진단.

---

### Q1. (개념) JPQL 의 *묵시적 JOIN* / *명시적 JOIN* / *JOIN FETCH* 의 차이.

<details><summary>정답</summary>

| | 묵시적 JOIN | 명시적 JOIN | JOIN FETCH |
|--|--|--|--|
| 문법 | `b.category.name` | `JOIN b.category c` | `JOIN FETCH b.category` |
| SQL JOIN | O (자동) | O | O |
| 연관 객체 로딩 | LAZY 유지 | **LAZY 유지** | **즉시 로딩** |
| 가독성 | 떨어짐 | 좋음 | 좋음 |

핵심: **명시적 JOIN 은 조건만 위해 사용** — 연관 객체는 안 가져옴. **JOIN FETCH** 는 즉시 로딩까지 (N+1 회피).

</details>

---

### Q2. (개념) `@Transactional` 의 propagation 중 **REQUIRED** 와 **REQUIRES_NEW** 의 차이. 각각 어떤 상황에?

<details><summary>정답</summary>

| | REQUIRED (기본) | REQUIRES_NEW |
|--|--|--|
| 동작 | 트랜잭션 있으면 참여, 없으면 새로 시작 | **항상 새 트랜잭션 시작**, 기존은 일시 중단 |
| 부모 실패 시 | 함께 롤백 | **자식은 commit 유지** |
| DB 커넥션 | 1 개 사용 | **2 개 점유** (부모·자식 동시) |
| 사용 | 대부분의 비즈니스 로직 | 로그·감사·외부 알림 (부모와 독립 운영) |

**예**: 주문 처리 (REQUIRED) 안에서 감사 로그 (REQUIRES_NEW) — 주문 실패해도 로그는 남아야.

**함정**: REQUIRES_NEW 는 *커넥션 풀 2개 점유* → 풀 고갈 위험. 남용 X.

</details>

---

### Q3. (개념) `isolation` 4 단계와 일반 DB 의 기본값.

<details><summary>정답</summary>

| isolation | 의미 | 일반 DB 기본 |
|--|--|--|
| `READ_UNCOMMITTED` | dirty read 가능 | — |
| **`READ_COMMITTED`** | commit 된 것만 읽음 | PostgreSQL, Oracle |
| **`REPEATABLE_READ`** | 같은 트랜잭션 안의 같은 row 는 같은 값 | MySQL InnoDB |
| `SERIALIZABLE` | 가장 엄격, 동시성 ↓ | — |

**실무**: 대부분 DB 기본값 유지. 보고서·통계는 `REPEATABLE_READ` 또는 `SERIALIZABLE` 로 강화 고려.

</details>

---

### Q4. (적용) "댓글이 N 개 이상인 게시글" 을 *서브쿼리* 로 JPQL 작성.

<details><summary>정답</summary>

```java
@Query("""
    SELECT b FROM Board b
    WHERE (SELECT COUNT(r) FROM Reply r WHERE r.board = b) >= :n
""")
List<Board> findWithReplyCountAtLeast(@Param("n") int n);
```

또는 GROUP BY + HAVING 으로:

```java
@Query("""
    SELECT b FROM Board b
    JOIN b.replies r
    GROUP BY b
    HAVING COUNT(r) >= :n
""")
List<Board> findWithReplyCountAtLeastGroup(@Param("n") int n);
```

성능: 두 방법 다 동작. JOIN + GROUP 가 보통 빠르지만 DB·인덱스 따라 다름.

</details>

---

### Q5. (적용) *글쓴이별 게시글 수* 와 *평균 view* 를 한 번에 가져오는 JPQL + DTO 매핑.

<details><summary>정답</summary>

```java
public record WriterStat(String writer, long count, double avgView) {}

@Query("""
    SELECT new com.example.dto.WriterStat(b.writer, COUNT(b), AVG(b.viewCnt))
    FROM Board b
    GROUP BY b.writer
    HAVING COUNT(b) >= :min
""")
List<WriterStat> writerStats(@Param("min") long min);
```

핵심:
- `GROUP BY b.writer` + 집계 함수
- `HAVING` 으로 그룹 필터링 (WHERE 는 그룹 *전*, HAVING 은 그룹 *후*)
- DTO 매핑 `new pkg.WriterStat(...)` — record 의 생성자 인자 순서 맞춤

</details>

---

### Q6. (적용) 주문이 실패해도 *감사 로그는 commit* 되도록 작성. `REQUIRES_NEW` 활용.

<details><summary>정답</summary>

```java
@Service @RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepo;
    private final AuditService auditService;

    @Transactional
    public void placeOrder(Order o) {
        orderRepo.save(o);
        auditService.log("주문 시도: " + o.getId());   // 별도 트랜잭션
        validatePayment(o);                            // 여기서 예외 발생 가능
        // 예외 → orderRepo.save() 는 롤백, 그러나 auditService.log() 는 commit 유지
    }
}

@Service @RequiredArgsConstructor
public class AuditService {

    private final AuditRepository auditRepo;

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void log(String msg) {
        auditRepo.save(new AuditLog(msg, LocalDateTime.now()));
    }
}
```

핵심:
- `AuditService` 가 *별 클래스* (같은 클래스 내부 호출은 AOP 우회로 안 됨)
- `REQUIRES_NEW` → 부모 트랜잭션 일시 중단, 새 트랜잭션 시작·종료

</details>

---

### Q7. (적용) `Specifications` 로 "writer / keyword / 최소 viewCnt" 의 *동적 검색* 구현.

<details><summary>정답</summary>

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

// Repository
public interface BoardRepository
    extends JpaRepository<Board, Long>, JpaSpecificationExecutor<Board> {}

// Service
Specification<Board> spec = Specification
    .where(BoardSpecs.writerEquals(form.getWriter()))
    .and(BoardSpecs.titleContains(form.getKeyword()))
    .and(BoardSpecs.viewCntGte(form.getMinView()));

Page<Board> result = boardRepo.findAll(spec, pageable);
```

핵심:
- `JpaSpecificationExecutor` 도 상속
- 각 Spec 메서드는 *null 반환* 시 *조건 없음* 으로 자동 해석
- `.where().and().and()` 로 조합

</details>

---

### Q8. (적용) QueryDSL 로 Q7 과 동일한 동적 검색을 구현하시오.

<details><summary>정답</summary>

```java
@Repository @RequiredArgsConstructor
public class BoardQueryRepository {

    private final JPAQueryFactory queryFactory;

    public Page<Board> search(BoardSearchForm form, Pageable pageable) {
        QBoard b = QBoard.board;

        List<Board> content = queryFactory
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

        long total = queryFactory.selectFrom(b)
            .where(writerEq(form.getWriter()), titleContains(form.getKeyword()), viewCntGte(form.getMinView()))
            .fetchCount();   // 또는 별도 count query

        return new PageImpl<>(content, pageable, total);
    }

    private BooleanExpression writerEq(String w) {
        return w == null ? null : QBoard.board.writer.eq(w);
    }
    private BooleanExpression titleContains(String k) {
        return k == null ? null : QBoard.board.title.contains(k);
    }
    private BooleanExpression viewCntGte(Integer min) {
        return min == null ? null : QBoard.board.viewCnt.goe(min);
    }
}
```

핵심:
- Q-class (`QBoard.board`) — 빌드 시 자동 생성
- `BooleanExpression` 메서드는 null 반환 시 자동 무시 (QueryDSL 의 핵심 매력)
- IDE 자동완성·컴파일 타임 타입 안전

vs Specifications: 문자열 `"writer"` 대신 `b.writer` (타입 안전).

</details>

---

### Q9. (디버그) 다음 코드의 함정.
```java
@Transactional
public void process() throws IOException {
    orderRepo.save(order);
    Files.readAllBytes(Path.of("config.json"));   // IOException 발생 가능
}
```

<details><summary>정답</summary>

**함정**: `IOException` 은 **checked exception**. `@Transactional` 의 디폴트 rollback 정책은 **`RuntimeException` (unchecked) 만 롤백**.

결과: `Files.readAllBytes` 에서 `IOException` 발생 시:
- `orderRepo.save(order)` 의 변경은 **commit** 됨 (롤백 X)
- 호출자에게 IOException 전파
- DB 에는 *불완전한 상태* (order 만 저장됨)

**해결**:

```java
@Transactional(rollbackFor = Exception.class)   // 모든 예외에 롤백
public void process() throws IOException { ... }
```

또는 RuntimeException 으로 래핑:

```java
try {
    Files.readAllBytes(...);
} catch (IOException e) {
    throw new RuntimeException(e);
}
```

**실무 가이드**: 모든 `@Transactional` 에 `rollbackFor = Exception.class` 코딩 컨벤션. 또는 *모든 예외를 RuntimeException* 으로 일관 처리.

</details>

---

### Q10. (디버그) 다음 코드의 트랜잭션이 적용되지 않는다. 원인과 해결.
```java
@Service
public class OrderService {

    public void placeOrder(Order o) {
        validate(o);
        save(o);
    }

    @Transactional
    public void save(Order o) {
        orderRepo.save(o);
        auditRepo.save(new AuditLog("..."));
    }
}
```

<details><summary>정답</summary>

**원인**: 같은 클래스 내부의 `this.save(o)` 호출 → Spring AOP 프록시 우회 → `@Transactional` 안 먹힘.

`@Transactional` 은 *프록시 클래스* 가 메서드 호출을 가로채 트랜잭션을 시작하는 방식. `this.method()` 는 *프록시를 통하지 않은 직접 호출* — 트랜잭션 적용 안 됨.

결과: `save` 안의 두 `repo.save()` 가 *각각 짧은 트랜잭션* 으로 처리되거나, 트랜잭션 없이 실행 (auto-commit). 부분 실패 시 데이터 불일치.

**해결 1**: 메서드 분리 — 다른 클래스로
```java
@Service @RequiredArgsConstructor
public class OrderService {
    private final OrderSaveService saveService;
    public void placeOrder(Order o) {
        validate(o);
        saveService.save(o);   // 프록시 경유 OK
    }
}

@Service
public class OrderSaveService {
    @Transactional
    public void save(Order o) { ... }
}
```

**해결 2**: `placeOrder` 자체에 `@Transactional`
```java
@Transactional
public void placeOrder(Order o) { validate(o); ... }
```

**해결 3** (덜 권장): self-injection
```java
@Autowired @Lazy
private OrderService self;
public void placeOrder(Order o) { validate(o); self.save(o); }
```

</details>

---

### Q11. (디버그) `REQUIRES_NEW` 를 *남용* 했을 때 발생하는 시스템 차원의 문제.

<details><summary>정답</summary>

**커넥션 풀 고갈**.

`REQUIRES_NEW` 는 *기존 트랜잭션을 일시 중단* 하고 *새 트랜잭션* 을 시작. 이때:
- 새 트랜잭션도 **별도 DB 커넥션** 점유
- 부모 트랜잭션은 *대기* 하면서 그 커넥션도 *그대로 점유*
- 즉 호출 한 번에 **2 개 커넥션 동시 점유**

만약 `REQUIRES_NEW` 메서드가 *내부에서 또 REQUIRES_NEW* 를 호출하면 3 개, 4 개로 누적. HikariCP 의 max-pool-size 가 10 인데 동시 호출이 5 회면 풀 고갈.

**증상**: `HikariPool-1 - Connection is not available, request timed out`. 응답 지연 → 전체 시스템 장애.

**가이드**:
- `REQUIRES_NEW` 는 *정말 필요한 곳에만* (로그·감사·외부 알림)
- 너무 자주 발생할 가능성 있으면 *별 스레드·메시지 큐* 로 분리
- HikariCP pool 모니터링 (`hikari.active`, `hikari.pending`)

</details>

---

### Q12. (디버그) 다음 Specifications 코드가 *시작 시점에는 정상* 인데 *런타임에 예외* 발생. 원인 추정.

```java
public static Specification<Board> categoryEquals(String name) {
    return (root, query, cb) -> name == null
        ? null
        : cb.equal(root.get("catgory").get("name"), name);   // (?)
}
```

<details><summary>정답</summary>

**원인**: 문자열 `"catgory"` 의 *오타* (`category` 가 맞음).

Specifications 의 `root.get("...")` 는 *문자열로* 필드명 지정 — **컴파일 타임에 안 잡힘**. 시작 시점에도 검증 안 됨 (lazy 평가). *런타임에 spec 실행* 시점에야:
```
PathElementException: Could not resolve attribute 'catgory' on Board
```

**한계**: Specifications 의 가장 큰 단점. 모든 필드 참조가 *문자열* → 오타·리팩토링 시 깨짐.

**해결책 두 가지**:

1. **메타모델 사용** — Spring/JPA 의 정적 메타모델 생성 (`@StaticMetamodel`):
   ```java
   cb.equal(root.get(Board_.category).get(Category_.name), name)
   ```
   타입 안전. 다만 빌드 설정 + 보일러.

2. **QueryDSL 로 전환**:
   ```java
   QBoard.board.category.name.eq(name)
   ```
   컴파일 타임 검증 완벽. 신규 프로젝트는 이쪽이 표준.

</details>

---

### Q13. (면접) "메서드 이름 규칙 / `@Query` / Specifications / QueryDSL 을 어떻게 선택하나요?" 1분 답변.

<details><summary>정답</summary>

**복잡도와 동적 정도** 에 따른 선택:

| 도구 | 적합 상황 | 한계 |
|--|--|--|
| **메서드 이름 규칙** | 1~3 조건 정적 검색 | 5+ 조건이면 이름 폭주, 동적 X |
| **`@Query` JPQL** | 4+ 조건 정적, JOIN, 집계, DTO | 동적 조건 처리 어려움, 문자열 |
| **Specifications** | 동적 조건 | 문자열 필드 참조 — 부분 타입 안전, 학습 곡선 |
| **QueryDSL** | 동적 + 복잡 + 타입 안전 | Q-class 생성 설정 |

**실무 가이드**:
- 단순 CRUD·정적 검색은 **메서드 이름** + **@Query** 로 80% 처리
- 검색 폼·동적 보고서 → **QueryDSL**
- Specifications 는 *QueryDSL 도입 부담* 일 때만 (대부분 신규 프로젝트는 처음부터 QueryDSL)

**한 줄 요약**: *정적은 @Query, 동적은 QueryDSL.*

</details>

---

### Q14. (면접) "JPA 시리즈를 마쳤다면, 다음으로 무엇을 공부하실 건가요?" — 학습 의지 + 깊이 평가.

<details><summary>정답</summary>

**모범 답변 — 우선순위 + 이유**:

**즉시 학습 (1~2 주)**:
1. **QueryDSL 본격** — 동적 검색이 필요한 모든 곳의 표준
2. **`@DataJpaTest` + H2** — Repository TDD. 발행 SQL 을 *눈으로 보면서* JPA 동작 검증
3. **p6spy** — 운영 환경에서 *실제 발행 SQL* 모니터링 + N+1 자동 감지

**1~2 개월 후**:
4. **DDD (Domain-Driven Design)** — Aggregate Root 패턴. JPA cascade·orphanRemoval 의 *철학적 기반*
5. **Spring Batch** — 대량 데이터 처리. 영속성 컨텍스트 분리 패턴
6. **2 차 캐시 + Caffeine** — 적절한 곳에 캐싱 추가

**인접 분야**:
- **JOOQ** — JPA 의 *SQL 중심 대안*. QueryDSL 의 SQL 사촌
- **Hibernate Reactive** — WebFlux 비동기 스택
- **MyBatis 와의 공존 패턴** — 한 프로젝트에서 복잡 보고서는 MyBatis, CRUD 는 JPA

면접관이 듣고 싶은 것: *체계적 학습 계획* + *실무 도구* + *지속 학습 의지*.

</details>
