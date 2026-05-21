# JPA 1강: 개념과 Entity 매핑 — 치트시트

> JPA 가 뭐고 왜 필요한가 + `@Entity` 클래스 만들기. JPA 5강 시리즈의 진입.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄

1. **JPA** = 자바 ORM 표준 인터페이스. **Hibernate** = 가장 흔한 구현체. **Spring Data JPA** = 그 위의 repository 자동화.
2. JPA 는 *SQL 을 안 쓴 게 아니라 개발자가 안 짠 것* — 내부적으로 자동 생성·실행.
3. `@Entity` 클래스의 절대 조건: **기본 생성자** + **non-final**.
4. **PK 타입은 `Long`** (래퍼). primitive `long` 은 `0` 과 transient 구분 안 됨.
5. **enum 은 항상 `EnumType.STRING`**. ORDINAL 은 순서 바뀌면 데이터 폭망.
6. 생성 시각은 `@CreatedDate` + `@EnableJpaAuditing` + `@EntityListeners` — 수동 `LocalDateTime.now()` 금지.

## 가장 중요한 코드 3개

```java
// (1) Entity 기본 골격 - 매번 이 형태로 시작
@Entity
@Table(name = "board")
@Getter @Setter
@NoArgsConstructor
@EntityListeners(AuditingEntityListener.class)
public class Board {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // MySQL
    private Long id;

    @Column(nullable = false, length = 200)
    private String title;
}
```

```java
// (2) Auditing - 생성·수정 시각 자동
@CreatedDate
@Column(updatable = false)
private LocalDateTime regDate;

@LastModifiedDate
private LocalDateTime modDate;

// + 메인 클래스에 @EnableJpaAuditing 필수
```

```java
// (3) enum 안전 매핑 - 반드시 STRING
@Enumerated(EnumType.STRING)
@Column(length = 20, nullable = false)
private Status status;
```

## 면접 한 줄 답변

- **Q. JPA 와 Hibernate 의 차이는?** → **JPA 는 스펙 (인터페이스)**, **Hibernate 는 구현체**. JDBC 인터페이스 vs MySQL Connector/J 같은 관계.
- **Q. MyBatis 와 JPA 중 뭐가 더 좋아요?** → **상황 trade-off**. 도메인 중심·연관관계 다용은 JPA, 복잡 SQL·통계는 MyBatis. 둘 다 알고 선택할 줄 아는 게 실무 역량.
- **Q. `@Entity` 클래스에 `final` 붙이면?** → **예외**. JPA 가 LAZY 프록시 만들 때 상속이 필요한데 final 은 상속 불가.
- **Q. enum 을 ORDINAL 로 매핑하면?** → **데이터 사고 위험**. enum 순서가 바뀌거나 앞에 값 추가하면 기존 DB 정수값이 다른 enum 으로 해석됨.

---

# 2. Quick Reference (실무 복붙)

## 2.1 매핑 어노테이션 표

| 어노테이션 | 의미 | 옵션 |
|--|--|--|
| `@Entity` | JPA 가 관리하는 클래스 | `name` (JPQL 별칭) |
| `@Table` | 매핑 테이블 | `name`, `uniqueConstraints`, `indexes` |
| `@Id` | PK 필드 | — |
| `@GeneratedValue` | PK 자동 생성 | `strategy = IDENTITY/SEQUENCE/TABLE/AUTO` |
| `@Column` | 컬럼 매핑 | `name`, `nullable`, `length`, `unique`, `updatable`, `insertable`, `columnDefinition` |
| `@Enumerated` | enum 매핑 | `EnumType.STRING` (반드시) |
| `@Lob` | CLOB/BLOB | — |
| `@Transient` | 매핑 제외 | — |
| `@EntityListeners` | 라이프사이클 이벤트 핸들러 | `AuditingEntityListener.class` |
| `@CreatedDate` / `@LastModifiedDate` | 자동 시각 | — |
| `@Temporal` | `Date` 시절의 유산 (Java 8 이후 불필요) | — |

## 2.2 PK 생성 전략

| 전략 | 동작 | 적합 DB | 함정 |
|--|--|--|--|
| `IDENTITY` | DB AUTO_INCREMENT 위임 | MySQL, MariaDB | INSERT 즉시 실행 (쓰기 지연 X) |
| `SEQUENCE` | DB 시퀀스 사용 | Oracle, PostgreSQL | `@SequenceGenerator` 옵션 |
| `TABLE` | 별도 테이블 시퀀스 흉내 | 모든 DB | 느림 — 호환성용 |
| `AUTO` | JPA 가 자동 선택 | 시작 단계 | 명시 안 한 위험 — 비추 |

> **PK 타입**: `Long` (래퍼) 으로. `long` (primitive) 은 transient 와 PK=0 구분 안 됨.

## 2.3 Auditing 한 줄 설정

```java
// 1. 메인 클래스
@SpringBootApplication
@EnableJpaAuditing
public class App { ... }

// 2. 엔티티 클래스
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Board {
    @CreatedDate @Column(updatable = false) private LocalDateTime regDate;
    @LastModifiedDate private LocalDateTime modDate;
}
```

> 누가 만들었는지까지 (`@CreatedBy`) 는 Spring Security + `AuditorAware` 추가 필요 (별도 강의).

## 2.4 자주 빠지는 함정 모음 (1강)

| 함정 | 정정 |
|--|--|
| `@Entity` 가 `final` 클래스 | LAZY 프록시 불가 → 예외. final 제거. |
| 기본 생성자 없음 | `@NoArgsConstructor` 또는 `protected MyEntity()` |
| PK 가 primitive `long` | 0 과 transient 구분 X → `Long` 으로 |
| `@Enumerated(EnumType.ORDINAL)` 또는 미명시 | **항상 `EnumType.STRING`** |
| 모든 필드에 Lombok `@Data` | `@ToString` 무한순회, `@EqualsAndHashCode` 의 transient 충돌 → `@Getter @Setter` 만 |
| `regDate` 수동으로 `LocalDateTime.now()` | `@CreatedDate` + `@EnableJpaAuditing` |
| `@Column(name="...")` 매번 명시 | naming strategy 가 `camelCase → snake_case` 자동 — 예외만 명시 |

## 2.5 약어 표

| 약어 | 풀어쓰기 |
|--|--|
| JPA | Java Persistence API (JSR 338) |
| ORM | Object-Relational Mapping |
| JPQL | Java Persistence Query Language |
| DDL | Data Definition Language (CREATE/ALTER) |
| DML | Data Manipulation Language (INSERT/UPDATE/DELETE) |
| FK | Foreign Key |
| Dialect | JPA 의 DB 별 SQL 방언 처리 모듈 |
| Auditing | 자동 메타데이터 (생성·수정 시각·주체) 추적 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 3.1 JPA 5강 시리즈 토픽 트리

```
JPA Series
│
├── [1강] 개념 + Entity 매핑      <- 현재 위치
│   ├── 왜 JPA? (객체-테이블 패러다임 차이)
│   ├── JPA / Hibernate / Spring Data JPA 계층
│   ├── @Entity / @Table / @Id / @Column
│   ├── PK 생성 전략 (IDENTITY/SEQUENCE/...)
│   ├── enum 매핑 (STRING 만!)
│   └── Auditing (@CreatedDate, @LastModifiedDate)
│
├── [2강] 영속성 컨텍스트
│   ├── 1차 캐시
│   ├── 엔티티 4 상태 (transient/managed/detached/removed)
│   ├── Dirty Checking
│   └── flush 시점
│
├── [3강] Spring Data JPA
│   ├── JpaRepository
│   ├── 메서드 이름 규칙
│   ├── @Query / JPQL
│   └── 페이징 (Page, Slice, Pageable)
│
├── [4강] 연관관계 매핑
│   ├── @ManyToOne / @OneToMany
│   ├── 단방향 vs 양방향, mappedBy
│   ├── fetch (LAZY vs EAGER)
│   ├── N+1 문제와 해결 (fetch join, EntityGraph, BatchSize)
│   └── cascade, orphanRemoval
│
└── [5강] JPQL + 트랜잭션
    ├── JPQL 기본 문법
    ├── DTO 매핑
    ├── @Modifying bulk 연산
    └── @Transactional (readOnly, propagation, rollbackFor)
```

## 3.2 1강 학습 진도 체크리스트

### 개념 이해
- [ ] JPA, Hibernate, Spring Data JPA 의 관계를 한 줄씩 설명 가능
- [ ] ORM 이 풀어주는 "객체-테이블 패러다임 차이" 두 가지 이상 설명 가능
- [ ] JPA 가 *SQL 을 자동 생성* 한다는 의미를 *SQL 을 안 쓰는 게 아님* 으로 정정 가능
- [ ] MyBatis 와 JPA 의 trade-off 한 줄로 답변 가능

### Entity 매핑 (실습 가능)
- [ ] `@Entity` 의 두 필수 조건 (기본 생성자, non-final) 을 외움
- [ ] `@Id`, `@GeneratedValue`, `@Column` 의 옵션을 외워서 작성 가능
- [ ] PK 생성 전략 4 가지를 적합 DB 와 함께 외움
- [ ] PK 타입은 `Long` (래퍼) 으로 — 이유 설명 가능
- [ ] enum 은 *반드시* `EnumType.STRING` — ORDINAL 의 사고 시나리오 설명 가능
- [ ] `@CreatedDate` 가 동작하려면 두 가지 설정 (`@EntityListeners`, `@EnableJpaAuditing`) 필요한 것을 안다
- [ ] `@Column(updatable = false)` 의 의미와 어디 쓰는지 안다

### 함정 인지
- [ ] Lombok `@Data` 의 위험 (`@ToString` 무한순회, `@EqualsAndHashCode` 의 transient 충돌) 을 안다
- [ ] `@Entity` 에 `final` 못 붙이는 이유 (LAZY 프록시) 를 안다
- [ ] naming strategy 가 `camelCase → snake_case` 자동 처리 하는 것을 안다

## 3.3 연관 학습 흐름

```
이전 (선수):
  JDBC ─────────┐
  MyBatis ──────┼── JPA 1강 (현재)
  Spring DI ────┤
  Lombok ───────┘

현재: 1강 개념 + Entity 매핑

다음:
  2강 영속성 컨텍스트  ← *반드시* 다음. JPA 의 정체성 이해
       │
       v
  3강 Spring Data JPA  ← 실무 코드 패턴
       │
       v
  4강 연관관계 매핑    ← 가장 함정 많음 (N+1 등)
       │
       v
  5강 JPQL + 트랜잭션  ← 깊이 있는 활용

병행 학습 추천:
  - Spring Data JPA 공식 문서
  - Spring Boot 의 application.yml 의 JPA 설정 옵션
    (`hibernate.dialect`, `hibernate.show_sql`, `hibernate.format_sql` 등)
  - JPA 실습 시 H2 in-memory DB → MySQL 전환 경험
```

## 3.4 1강 이후 자기점검 신호

- "왜 `@Entity` 에 `final` 안 되지?" 가 *자연스럽게* 답이 나옴 → 1강 통과
- "save() 후 굳이 update() 안 호출해도 되는데 어떻게?" 가 궁금하면 → **2강 즉시 진입**
- "이 엔티티에 댓글 리스트 추가하고 싶다" 가 막히면 → **4강 (연관관계)**
- "조건 5 개로 검색하고 싶다" 가 막히면 → **3강 (Spring Data JPA + @Query)**
