# JPA 1강: 개념과 Entity 매핑

> **이 강의는 무엇인가**: 자바 객체와 RDB 테이블을 자동 매핑·동기화하는 ORM 표준 **JPA (Java Persistence API)** 의 정체, 그리고 가장 먼저 익혀야 할 **Entity 클래스 매핑 어노테이션**.
> **왜 배우는가**: MyBatis 가 "SQL 은 직접, 자바는 깨끗" 이었다면 JPA 는 "객체 그래프 그대로 다루면 SQL 은 알아서". 도메인 중심 설계가 필요할 때 표준. 한국에서도 신규 프로젝트는 점차 JPA 로 이동.

---

## 들어가기 전에

- **선수**: JDBC, MyBatis, Spring DI, Lombok, 트랜잭션 기본 (commit/rollback).
- **마인드셋**: "테이블이 아니라 객체를 다룬다." 그리고 *내가 SQL 안 짠다 ≠ SQL 을 몰라도 된다*. **SQL 을 알아야 ORM 의 함정을 피한다**.
- **표기 약속**: 모든 코드는 Spring Boot 3.x + JPA 3.x (Jakarta) 기준. `jakarta.persistence.*` 패키지.
- **본 5강 시리즈 구성**:
  - **1강 (현재)**: 개념 + Entity 매핑
  - 2강: 영속성 컨텍스트
  - 3강: Spring Data JPA
  - 4강: 연관관계 매핑
  - 5강: JPQL + 트랜잭션

---

# Part A. JPA 가 뭐고 왜 필요한가

## 1. SQL 중심의 한계 (MyBatis 까지 모든 방식 공통)

MyBatis 강의에서 JDBC 의 30 줄 보일러플레이트는 줄였다. 그러나 **자바 객체와 테이블 사이의 패러다임 차이**는 그대로:

| | 객체 (자바) | 테이블 (RDB) |
|--|--|--|
| 식별성 | 메모리 주소 / `equals` | PK |
| 관계 | 참조 (`board.getWriter()`) | FK 컬럼 |
| 상속 | 자연스러움 | 불가 (구현 우회 필요) |
| 컬렉션 | `List<Reply>` | 별도 테이블 + JOIN |
| 데이터 타입 | enum, LocalDateTime, ... | 문자열·숫자·날짜 |

MyBatis 도 매핑은 해주지만, **연관관계를 따라가는 코드**가 결국 SQL JOIN 또는 N 번 쿼리로 직접 짜야 함:

```java
// MyBatis 로 게시글 + 댓글 리스트 같이 가져오기 - 직접 SQL JOIN + 매퍼 작성
Board board = boardMapper.findByIdWithReplies(boardId);
// SQL 의 JOIN 결과를 nested resultMap 으로 매핑해야...
```

객체지향 자연스러움: `board.getReplies()` 한 줄로 끝나야.

## 2. ORM 의 발상

**ORM (Object-Relational Mapping)**: 객체-테이블 매핑을 *프레임워크가* 한다. 개발자는 객체만 다룸.

```java
// JPA 로 게시글 + 댓글 가져오기 - SQL X
Board board = em.find(Board.class, boardId);
List<Reply> replies = board.getReplies();  // 자연스러운 객체 탐색
```

JPA 가 내부적으로 `SELECT ... FROM board WHERE id = ?` + (필요 시) `SELECT ... FROM reply WHERE board_id = ?` 를 자동 발행. **SQL 을 안 쓴 게 아니라 안 짠 것**.

### MyBatis vs JPA 한 줄 비교

| | MyBatis | JPA |
|--|--|--|
| SQL | 개발자가 XML/어노테이션에 직접 작성 | JPA 가 자동 생성 (JPQL/메서드 이름 기반) |
| 결과 매핑 | resultMap 또는 자동 매핑 | 자동 (객체 그래프) |
| 연관관계 | JOIN SQL + nested resultMap | `@OneToMany`, `@ManyToOne` 등 매핑만 |
| 변경 추적 | 직접 UPDATE SQL | **Dirty Checking** 자동 (2강) |
| DB 종속 | 높음 (특정 SQL 문법) | 낮음 (Dialect 가 분기) |
| 학습 곡선 | 낮음 | 가파름 (영속성 컨텍스트 개념) |

JPA 가 무조건 우수한 것이 아니라 **trade-off**. SSAFY 같은 학습 후 실무에서는 *둘 다 알고* 상황 따라 선택하는 게 정답.

## 3. JPA 표준 vs Hibernate

```
+-------------------------------------+
|   JPA (스펙, 자바 표준 인터페이스)        |
|   EntityManager, @Entity, JPQL...   |
+-----+--------------+----------------+
      |              |
      v              v
+-----------+   +-------------+
| Hibernate |   | EclipseLink |     <- 구현체 (옵션)
+-----------+   +-------------+
```

- **JPA**: 인터페이스/어노테이션 *스펙*. 자바 표준 (JSR 338).
- **Hibernate**: 가장 널리 쓰는 *구현체*. 사실상 표준.
- 우리는 JPA 의 인터페이스만 쓰면 구현체 교체 가능 (이론상).

Spring Boot 의 `spring-boot-starter-data-jpa` 가 기본으로 Hibernate 를 가져옴.

## 4. Spring Data JPA 까지의 계층

```
   비즈니스 로직 (Service)
            |
   +--------v-------------------+
   |  Spring Data JPA           |  <- JpaRepository, 메서드 이름 규칙
   |  (반복 코드 줄이는 한 겹 더)     |
   +--------+-------------------+
            |
   +--------v-------------------+
   |  JPA (EntityManager API)   |  <- 표준 인터페이스
   +--------+-------------------+
            |
   +--------v-------------------+
   |  Hibernate                 |  <- 구현체
   +--------+-------------------+
            |
   +--------v-------------------+
   |  JDBC                      |
   +--------+-------------------+
            v
          RDBMS
```

실무에서 직접 만지는 건 대부분 **Spring Data JPA** (3 강) 와 **`@Entity` 클래스** (이번 강의 주제).

---

# Part B. Entity 와 매핑 어노테이션

여기서부터 *손에 잡히는* 코드. 자바 POJO 를 JPA 에게 "이건 테이블이야" 라고 알리는 어노테이션들.

## 1. 가장 단순한 Entity

```java
import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "board")
@Getter @Setter
@NoArgsConstructor                       // JPA 가 리플렉션으로 인스턴스화하려면 기본 생성자 필수
@AllArgsConstructor
public class Board {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String content;

    @Column(nullable = false, length = 50)
    private String writer;

    @Column(name = "reg_date", nullable = false)
    private LocalDateTime regDate;

    @Column(name = "view_cnt", nullable = false)
    private int viewCnt;
}
```

대응되는 DDL 은 JPA 가 자동 생성 (개발 환경에서). 운영은 별도 마이그레이션 도구 (Flyway, Liquibase) 사용 권장.

### 핵심 어노테이션 표

| 어노테이션 | 의미 |
|--|--|
| `@Entity` | JPA 가 관리하는 클래스. **반드시** 기본 생성자 + non-final 클래스. |
| `@Table(name=…)` | 매핑 테이블 이름. 생략 시 클래스명 (대소문자 정책은 구현체 설정에 따름) |
| `@Id` | PK 필드 |
| `@GeneratedValue(strategy=…)` | PK 자동 생성 전략 |
| `@Column(name=, nullable=, length=, unique=)` | 컬럼 세부 매핑 |
| `@Enumerated(EnumType.STRING)` | enum 매핑. **반드시 STRING** (이유는 함정 절에) |
| `@Temporal` | `java.util.Date` 시절의 유산. `LocalDate / LocalDateTime` 쓰면 불필요. |
| `@Transient` | 매핑 *제외*. 메모리에만 존재하는 계산 필드. |
| `@Lob` | CLOB / BLOB 매핑. 큰 텍스트·바이너리. |

### 매핑 어노테이션이 *없는* 자바 필드는?

JPA 는 기본적으로 *모든 필드를 매핑 대상으로* 봄. 매핑하기 싫으면 `@Transient` 명시.

```java
@Entity
public class Board {
    @Id @GeneratedValue private Long id;
    private String title;          // 자동으로 title 컬럼에 매핑
    @Transient
    private boolean cached;        // DB 에 컬럼 안 만듦
}
```

## 2. 식별자 (PK) 생성 전략

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;
```

`@GeneratedValue` 의 `strategy` 가 핵심:

| 전략 | 동작 | 적합 DB | 비고 |
|--|--|--|--|
| `IDENTITY` | DB AUTO_INCREMENT 위임. INSERT 직후 PK 확정. | MySQL, MariaDB | INSERT 가 *즉시* 실행됨 |
| `SEQUENCE` | DB 시퀀스 객체 사용. INSERT *전* PK 미리 받음. | Oracle, PostgreSQL | 트랜잭션 끝까지 INSERT 지연 가능 (성능 ↑) |
| `TABLE` | 별도 테이블에 시퀀스 흉내 | 거의 모든 DB | 느림, 호환성용 |
| `AUTO` | JPA 가 DB 보고 선택 | 작은 프로젝트 | 명시 안 함 — 비추 |

> **함정**: `IDENTITY` 는 *INSERT 가 즉시* 실행되어야 PK 를 알 수 있다. 그래서 JPA 의 일부 최적화 (쓰기 지연 — 2강에서 다룸) 가 동작하지 않는다. MySQL 쓰는 한 어쩔 수 없지만, 성능 민감한 곳에선 의식해 둘 것.

### PK 타입은 Long 으로

```java
@Id private Long id;   // 권장
@Id private long id;   // 비추 — null 표현 불가, transient 상태 구분 어려움
```

- `Long` (래퍼) 이면 *아직 PK 가 부여되지 않은* `null` 상태를 표현 가능 → JPA 가 transient 여부 판단에 사용.
- primitive `long` 은 항상 0 — 그래서 `0` 인 새 엔티티가 *이미 영속화된 것* 으로 오인될 수 있음.

## 3. 자동 생성·수정 시각 — Auditing

매번 `regDate = LocalDateTime.now()` 박지 말고:

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Board {
    // ...

    @CreatedDate
    @Column(updatable = false)     // 한 번 박힌 후 수정 불가
    private LocalDateTime regDate;

    @LastModifiedDate
    private LocalDateTime modDate;
}
```

설정 1 줄 추가 필요:

```java
@SpringBootApplication
@EnableJpaAuditing
public class App { ... }
```

이러면 `save()` 시 자동으로 `regDate`, 수정 시 자동으로 `modDate` 채워짐.

Auditing 으로 *누가* 만들었는지·수정했는지 (`@CreatedBy`, `@LastModifiedBy`) 까지 가려면 Spring Security + `AuditorAware` 빈 필요. 별도 강의 주제.

### `@Column(updatable = false)` 의 의미

`regDate` 는 한 번 박히면 변하면 안 됨. `updatable = false` 면 UPDATE 시 이 컬럼은 SET 절에서 빠짐. dirty checking 으로 인한 잘못된 변경 방지.

## 4. enum 매핑 — `EnumType.STRING` 만 사용

```java
public enum Status {
    READY, RUNNING, DONE
}

@Enumerated(EnumType.STRING)   // 추천
private Status status;

@Enumerated(EnumType.ORDINAL)  // 위험! 절대 X
private Status status;
```

- `STRING`: DB 에 `"READY"`, `"RUNNING"`, `"DONE"` 으로 저장. 안전.
- `ORDINAL`: DB 에 `0`, `1`, `2` 로 저장. enum 순서 바뀌면 **데이터가 폭망**.

시나리오:

```java
// 처음
enum Status { READY, RUNNING, DONE }
// DB: 0=READY, 1=RUNNING, 2=DONE

// 6개월 후 PM "PAUSED 도 추가하자"
enum Status { PAUSED, READY, RUNNING, DONE }  // 앞에 추가
// 새 매핑: 0=PAUSED, 1=READY, 2=RUNNING, 3=DONE
// 기존 DB 의 0 (원래 READY) → 이제 PAUSED 로 읽힘!!
```

복구는 데이터 마이그레이션 + 모든 0 → 1 로 변환. 사고 큰 만큼 *처음부터 STRING* 으로.

## 5. 자바 필드명 vs 컬럼명 — naming strategy

```java
@Column(name = "reg_date")
private LocalDateTime regDate;
```

Spring Boot 의 기본 naming strategy 는 `SpringPhysicalNamingStrategy` — `regDate` → `reg_date` 로 자동 변환. 그래서 굳이 `@Column(name=...)` 안 적어도 동작:

```java
private LocalDateTime regDate;  // 자동으로 reg_date 컬럼
```

다만 **테이블이 이미 있고 컬럼명이 예외적** 인 경우 (예: `RegDate`, `REG_DT`) 만 `@Column(name=...)` 명시.

---

## 자주 빠지는 함정 (1 강 한정)

| 함정 | 해결 |
|--|--|
| `@Entity` 클래스에 기본 생성자 누락 | Lombok 의 `@NoArgsConstructor` 또는 직접 추가 |
| `@Entity` 클래스를 `final` 로 선언 | JPA 가 *프록시* 를 만들 수 없음. final 빼기 |
| PK 타입을 `long` (primitive) 으로 | `Long` 으로. transient 여부 판단·`null` 안전성 |
| enum 을 `EnumType.ORDINAL` 또는 디폴트로 매핑 | **항상 `EnumType.STRING`**. ORDINAL 은 순서 바뀌면 데이터 폭망 |
| `@Column(name=...)` 을 매번 명시 | naming strategy 가 `regDate → reg_date` 자동 처리. *예외적 컬럼명만* 명시 |
| 모든 필드에 Lombok `@Data` (= `@ToString`, `@EqualsAndHashCode`, ...) | `@ToString` 은 연관 엔티티 따라 *무한 순회*, `@EqualsAndHashCode` 는 *PK null 인 transient 상태* 에서 충돌. **`@Getter` + 필요한 것만** |
| `regDate` 를 수동으로 `LocalDateTime.now()` 박기 | `@EnableJpaAuditing` + `@CreatedDate` + `@LastModifiedDate` |

---

## 자가점검

1. JPA, Hibernate, Spring Data JPA 의 관계를 한 줄씩으로.
2. `@Entity` 클래스의 *필수 조건* 두 가지는?
3. PK 타입을 `Long` (래퍼) 으로 권장하는 이유 한 줄.
4. `EnumType.ORDINAL` 이 위험한 이유를 구체 시나리오로 설명.
5. `IDENTITY` 와 `SEQUENCE` 전략의 차이 (PK 가 *언제* 결정되는가).
6. `@CreatedDate` 가 동작하려면 어떤 설정 두 가지가 필요한가?
7. `regDate` 필드를 `@Column(updatable = false)` 로 두는 이유.

<details><summary>풀이</summary>

1. **JPA** = 자바 ORM 표준 인터페이스 (스펙). **Hibernate** = 가장 널리 쓰는 JPA 구현체. **Spring Data JPA** = JPA 위에 repository 패턴 자동화를 얹은 Spring 모듈.
2. **기본 생성자** (public 또는 protected) + **non-final 클래스**. JPA 가 리플렉션과 프록시로 동작하므로.
3. `null` 표현 가능 → JPA 가 *영속화 전 transient 상태* 인지 판단 가능. primitive `long` 은 항상 0 이라 transient 와 PK=0 구분 불가.
4. enum 의 순서가 바뀌거나 *중간 또는 앞에 새 값이 추가* 되면 기존 DB 의 정수값이 다른 enum 으로 매핑되어 데이터 의미가 어긋남. 예: `READY/RUNNING/DONE` (0/1/2) 에 앞에 `PAUSED` 추가 → 기존 0=READY 가 0=PAUSED 로 잘못 해석.
5. `IDENTITY`: DB AUTO_INCREMENT 에 위임 → INSERT 가 *즉시* 실행되어 PK 확정. `SEQUENCE`: DB 시퀀스에서 PK 를 *INSERT 전* 미리 받아옴 → INSERT 자체는 트랜잭션 끝까지 지연 가능.
6. ① 엔티티 클래스에 `@EntityListeners(AuditingEntityListener.class)`, ② 메인 클래스 (또는 `@Configuration`) 에 `@EnableJpaAuditing`.
7. 한 번 INSERT 시 박힌 생성 시각은 절대 변하면 안 됨. dirty checking 이 잘못 변경하지 않도록 *UPDATE 의 SET 절에서 제외*.

</details>

---

## 다음 학습으로

- **JPA 2강: 영속성 컨텍스트** — JPA 의 정체성. 1차 캐시, 엔티티 4 상태 (transient/managed/detached/removed), Dirty Checking, flush 시점. 이 개념을 모르면 JPA 의 동작은 마법처럼만 보임.
- 참고: [Spring Data JPA 공식 문서](https://docs.spring.io/spring-data/jpa/reference/) — 본 강의는 핵심만, 깊이는 공식 문서로.
- 같은 도메인의 다른 접근: MyBatis 강의 (Framework_08/09) 와 비교 — *언제 어느 쪽이 더 적절한가* 의 감을 잡는 게 본 시리즈의 또 다른 목표.
