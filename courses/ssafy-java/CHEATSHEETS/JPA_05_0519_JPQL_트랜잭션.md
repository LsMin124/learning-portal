# JPA 5강: JPQL 심화 + 트랜잭션 — 치트시트

> JPA 시리즈 마지막. JPQL 의 깊이 + `@Transactional` 의 진짜 옵션 + QueryDSL 로의 길.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄

1. **JPQL JOIN 3 종**: 묵시적 (비추) / 명시적 (조건만) / **JOIN FETCH** (즉시 로딩). N+1 회피는 JOIN FETCH 또는 그 대안.
2. **JPQL 서브쿼리**: SELECT/WHERE 절만. FROM 절 서브쿼리는 안 됨 (대안: 두 쿼리 분리, native).
3. **`@Transactional` propagation 핵심 2 종**: **REQUIRED** (기본·참여) 와 **REQUIRES_NEW** (독립 트랜잭션·로그용).
4. **rollback 함정**: 디폴트는 **`RuntimeException` 만** 롤백. checked exception (`IOException` 등) 은 commit. `rollbackFor = Exception.class` 필수.
5. **`@Transactional(readOnly = true)`** 효과 3 가지: 스냅샷 X / flush mode 변경 / DB read-only 최적화. **클래스 레벨로 기본 + 변경 메서드만 override**.
6. **동적 쿼리 표준 = QueryDSL**. `@Query` 의 정적 한계 + Specifications 의 문자열 함정 모두 해결. 컴파일 타임 타입 안전 + 자동완성 + 동적 조건.

## 가장 중요한 코드 3개

```java
// (1) @Transactional 의 안전한 기본 패턴
@Service
@Transactional(readOnly = true)   // 클래스 레벨 - 조회 메서드 기본
@RequiredArgsConstructor
public class BoardService {

    private final BoardRepository boardRepo;

    public Board read(Long id) {
        return boardRepo.findById(id).orElseThrow();   // readOnly 적용
    }

    @Transactional(rollbackFor = Exception.class)     // 변경 메서드만 override
    public Board create(BoardForm form) {
        return boardRepo.save(Board.from(form));
    }
}
```

```java
// (2) REQUIRES_NEW - 독립 트랜잭션 (로그·감사)
@Service @RequiredArgsConstructor
public class AuditService {
    private final AuditRepository auditRepo;

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void log(String msg) {
        auditRepo.save(new AuditLog(msg, LocalDateTime.now()));
        // 부모 실패해도 이 commit 은 유지됨
    }
}
```

```java
// (3) QueryDSL 동적 검색 - 신규 프로젝트의 표준
QBoard b = QBoard.board;
List<Board> result = queryFactory
    .selectFrom(b)
    .where(writerEq(form.getWriter()),       // null 자동 무시
           titleContains(form.getKeyword()),
           viewCntGte(form.getMinView()))
    .orderBy(b.regDate.desc())
    .offset(pageable.getOffset())
    .limit(pageable.getPageSize())
    .fetch();

private BooleanExpression writerEq(String w) {
    return w == null ? null : QBoard.board.writer.eq(w);
}
```

## 면접 한 줄 답변

- **Q. JPQL 의 묵시적/명시적/JOIN FETCH 차이?** → 묵시적은 `b.cat.name` 한 줄 (가독성 X), 명시적은 `JOIN b.cat c` (조건만), **JOIN FETCH** 는 *즉시 로딩까지* (N+1 회피).
- **Q. `@Transactional` 의 디폴트 rollback 함정?** → **checked exception (`IOException` 등) 은 commit**. `rollbackFor = Exception.class` 명시 또는 RuntimeException 으로 일관 처리.
- **Q. `REQUIRES_NEW` 의 함정?** → **DB 커넥션 2 개 동시 점유** (부모 일시 중단 + 자식 새 트랜잭션) → 남용 시 풀 고갈. 로그·감사처럼 *진짜 독립이 필요한* 곳에만.
- **Q. 동적 쿼리는 어떻게?** → **QueryDSL**. 컴파일 타임 타입 안전 + IDE 자동완성 + null 자동 무시. `@Query` 의 정적 한계와 Specifications 의 문자열 함정을 모두 해결.

---

# 2. Quick Reference (실무 복붙)

## 2.1 JPQL JOIN 3 종

| 형태 | 문법 | 연관 객체 로딩 | 사용 |
|--|--|--|--|
| 묵시적 | `b.category.name` | LAZY 유지 | 비추 (가독성) |
| 명시적 | `JOIN b.category c` | LAZY 유지 | 조건만 필요 |
| JOIN FETCH | `JOIN FETCH b.category` | **즉시 로딩** | N+1 회피 |
| LEFT JOIN (FETCH) | `LEFT JOIN [FETCH] b.replies` | (옵션) | null 포함 |

## 2.2 JPQL 서브쿼리

```sql
-- 가능 (SELECT, WHERE)
SELECT b FROM Board b WHERE (SELECT COUNT(r) FROM Reply r WHERE r.board = b) >= :n
SELECT b FROM Board b WHERE NOT EXISTS (SELECT r FROM Reply r WHERE r.board = b)
SELECT b FROM Board b WHERE b.viewCnt > ALL (SELECT b2.viewCnt FROM Board b2 WHERE ...)

-- 안 됨 (FROM)
SELECT s.writer FROM (SELECT ...) s   -- JPQL 표준 X
```

대안: 두 쿼리로 분리 또는 native query.

## 2.3 집계 + CASE + COALESCE

```sql
-- 집계 + GROUP BY + HAVING + DTO
SELECT new com.example.dto.WriterStat(b.writer, COUNT(b), AVG(b.viewCnt))
FROM Board b
GROUP BY b.writer
HAVING COUNT(b) >= :min

-- CASE
CASE WHEN b.viewCnt > 1000 THEN 'HOT'
     WHEN b.viewCnt > 100  THEN 'WARM'
     ELSE 'COLD' END

-- COALESCE - 첫 non-null
COALESCE(b.title, '제목 없음')

-- NULLIF - 같으면 null
NULLIF(b.title, '삭제됨')
```

집계 함수: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

## 2.4 @Transactional 옵션

| 옵션 | 기본 | 의미 |
|--|--|--|
| `propagation` | `REQUIRED` | 트랜잭션 전파 정책 |
| `isolation` | DB 기본 | 격리 수준 |
| `rollbackFor` | `RuntimeException` 만 | 어느 예외에 롤백 |
| `noRollbackFor` | 없음 | 롤백 안 할 예외 |
| `readOnly` | `false` | 조회 전용 최적화 |
| `timeout` | -1 (무제한) | 시간 제한 (초) |

## 2.5 propagation 7 종

| 옵션 | 동작 |
|--|--|
| **REQUIRED** (기본) | 트랜잭션 있으면 참여, 없으면 새로 |
| **REQUIRES_NEW** | 항상 새 트랜잭션 (기존 일시 중단) |
| `SUPPORTS` | 있으면 참여, 없으면 트랜잭션 없이 |
| `MANDATORY` | 있어야만 실행, 없으면 예외 |
| `NESTED` | 중첩 (savepoint), 일부 DB |
| `NEVER` | 트랜잭션 있으면 예외 |
| `NOT_SUPPORTED` | 항상 트랜잭션 없이 |

**실무 90%**: REQUIRED. **10%**: REQUIRES_NEW (로그·감사).

## 2.6 isolation 4 단계

| 단계 | dirty | non-repeat | phantom | 일반 DB |
|--|--|--|--|--|
| `READ_UNCOMMITTED` | O | O | O | — |
| **`READ_COMMITTED`** | X | O | O | PostgreSQL, Oracle |
| **`REPEATABLE_READ`** | X | X | O | MySQL InnoDB |
| `SERIALIZABLE` | X | X | X | — |

대부분 DB 기본값 그대로. 보고서·통계만 `REPEATABLE_READ` 고려.

## 2.7 Specifications vs QueryDSL

| | Specifications | QueryDSL |
|--|--|--|
| 동적 조건 | O (null 자동 무시) | O (null 자동 무시) |
| 타입 안전 | 문자열 (`"writer"`) — 부분 | **완벽** (`b.writer`) |
| IDE 자동완성 | 한계 | **완벽** |
| 학습 곡선 | 중상 | 중상 |
| 빌드 설정 | 없음 | Q-class 생성 (Gradle/Maven 설정) |
| 컴파일 검증 | 약함 | **강함** |
| 실무 표준 | 점차 X | **O** |

신규 프로젝트는 처음부터 QueryDSL.

## 2.8 자주 빠지는 함정 모음 (5강)

| 함정 | 정정 |
|--|--|
| JPQL 묵시적 JOIN 만 사용 | 명시적 JOIN 또는 JOIN FETCH |
| FROM 절 서브쿼리 시도 | 두 쿼리 분리 또는 native |
| `@Transactional` 의 디폴트 rollback 정책 모름 | **`rollbackFor = Exception.class`** 명시 또는 RuntimeException 일관 |
| `@Transactional` 같은 클래스 내부 호출 | 메서드 분리 / self-injection / outer 에 부착 |
| REQUIRES_NEW 남용 | 커넥션 풀 2 개 점유 → 풀 고갈. 로그·감사에만 |
| isolation 기본만 사용 | 보통은 OK. 보고서·통계는 REPEATABLE_READ 고려 |
| 조회 메서드에 readOnly 안 붙임 | 클래스 레벨로 기본 + 변경 메서드만 override |
| Specifications 의 문자열 오타 | 메타모델 또는 QueryDSL 전환 |
| QueryDSL 의 Q-class 안 생성 | `annotationProcessor` 등록·`build/generated` 인식 |
| `@Modifying` UPDATE 후 옛 값 | `clearAutomatically = true` 또는 dirty checking 으로 통일 |
| 영속성 컨텍스트 *수명 = 트랜잭션* 잊고 LAZY 접근 | OSIV / DTO 변환 |

## 2.9 약어 표

| 약어 | 풀어쓰기 |
|--|--|
| JPQL | Java Persistence Query Language |
| AOP | Aspect-Oriented Programming |
| MVCC | Multi-Version Concurrency Control |
| DDD | Domain-Driven Design |
| TDD | Test-Driven Development |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 3.1 JPA 5강 시리즈 — 완결

```
JPA Series (완결!)
│
├── [1강] 개념 + Entity 매핑
│   └── @Entity / @Id / @Column / enum.STRING / Auditing
│
├── [2강] 영속성 컨텍스트
│   └── 1차 캐시 / 4 상태 / Dirty Checking / flush / OSIV
│
├── [3강] Spring Data JPA
│   └── JpaRepository / 메서드 이름 / @Query / 페이징 / @Modifying / Projection
│
├── [4강] 연관관계 매핑
│   └── @ManyToOne / 주인 / LAZY / N+1 / cascade / @ManyToMany 풀기
│
└── [5강] JPQL 심화 + 트랜잭션      <- 현재 위치 (마지막!)
    │
    ├── JPQL 심화
    │   ├── JOIN 3종 (묵시/명시/FETCH)
    │   ├── 서브쿼리 (SELECT/WHERE 만)
    │   ├── CASE / COALESCE / NULLIF
    │   ├── 집계 + GROUP BY + HAVING + DTO
    │   └── 정적 조건의 한계
    │
    ├── @Transactional 심화
    │   ├── propagation 7종 (REQUIRED, REQUIRES_NEW)
    │   ├── isolation 4단계
    │   ├── rollbackFor 함정 (checked 예외)
    │   ├── readOnly 효과
    │   ├── timeout
    │   └── AOP 프록시 함정 (2강 복습)
    │
    ├── Specifications
    │   ├── JpaSpecificationExecutor
    │   ├── null = 조건 없음
    │   └── 문자열 함정
    │
    ├── QueryDSL
    │   ├── 왜 (컴파일 타임 안전 + 자동완성 + 동적)
    │   ├── 빌드 설정 (Q-class)
    │   ├── BooleanExpression vs BooleanBuilder
    │   └── Projections.constructor
    │
    └── 시리즈 정리
        ├── 5강 한 줄씩
        ├── 실무 5 원칙
        └── 다음 학습 (QueryDSL·DDD·Batch·JOOQ·Reactive)
```

## 3.2 5강 학습 진도 체크리스트

### JPQL 심화
- [ ] 묵시적 / 명시적 / JOIN FETCH 의 차이 안다
- [ ] JPQL 서브쿼리의 가능 절·불가 절 안다
- [ ] CASE / COALESCE / NULLIF 사용 가능
- [ ] GROUP BY + HAVING + DTO 매핑 작성 가능

### @Transactional 심화
- [ ] propagation 7종 외움 (특히 REQUIRED / REQUIRES_NEW)
- [ ] isolation 4단계와 일반 DB 기본 안다
- [ ] **rollbackFor 의 디폴트 함정** 안다 (checked 예외 commit)
- [ ] `readOnly = true` 의 3가지 효과 안다
- [ ] timeout 옵션 사용 가능
- [ ] AOP 프록시 함정 항상 의식

### Specifications
- [ ] 사용 패턴 (JpaSppecificationExecutor + Specification 람다) 안다
- [ ] null 반환 = 조건 없음 의 자동 해석 안다
- [ ] 문자열 필드 참조의 한계 안다

### QueryDSL
- [ ] 왜 QueryDSL 인지 (3 가지 장점) 안다
- [ ] Q-class 자동 생성 메커니즘 안다
- [ ] BooleanExpression null 자동 무시 패턴 안다
- [ ] Projections.constructor 로 DTO 매핑 안다

### 시리즈 완결
- [ ] 5 강 각각의 핵심을 한 줄씩 외움
- [ ] 실무에서 매일 의식해야 할 5 가지 원칙 안다
- [ ] 다음 학습 단계 (QueryDSL·DDD·Batch 등) 선택 가능

## 3.3 JPA 마스터 후 학습 흐름

```
JPA 5강 완결 (현재)
    │
    │
    ┌────────────┴────────────┐
    │                         │
    v                         v
즉시 (1~2주)             1~2 개월 후
    │                         │
    ├── QueryDSL 본격         ├── DDD Aggregate
    ├── @DataJpaTest          ├── Spring Batch
    └── p6spy (SQL 모니터)    └── 2차 캐시 + Caffeine

         │                         │
         └────────────┬────────────┘
                      v
              인접 분야 탐색
                      │
                      ├── JOOQ (SQL + 타입 안전)
                      ├── Hibernate Reactive (WebFlux)
                      ├── MyBatis 와 공존 패턴
                      └── DB 특화 (MySQL/PostgreSQL)
```

## 3.4 시리즈 마스터 후 자기 점검 신호

- 새 프로젝트 시작 시 *Entity 매핑부터 막힘없이* 작성 가능 → 1강 통과
- 코드 리뷰에서 "이거 N+1 인데" 가 자연스럽게 떠오름 → 4강 통과
- "이 메서드 readOnly 인가?" 가 자동 체크 → 5강 통과
- 동적 검색 폼을 보면 자동으로 *QueryDSL 설계* 가 떠오름 → 5강 + QueryDSL 합격 시그널
- 면접에서 "Hibernate vs JPA 차이는?" 에 *스펙 vs 구현체* 로 1초 답변 → 시리즈 마스터

## 3.5 JPA 시리즈 완결 — 한 마디

> **JPA 의 마법은 모두 *영속성 컨텍스트* + *트랜잭션* 안에서 일어난다.**
> 이 두 개념을 *코드 리뷰 30초 안에 머리에 떠올릴 수 있으면* 시리즈 마스터.

**축하합니다 — JPA 시리즈 완결!**
