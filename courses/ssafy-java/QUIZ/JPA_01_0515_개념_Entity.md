# JPA 1강: 개념과 Entity 매핑 — 퀴즈

> 14문항. 개념·적용·디버그·면접. JPA 의 정체성과 Entity 매핑 기본 자가 진단.

---

### Q1. (개념) JPA, Hibernate, Spring Data JPA 의 관계를 각각 한 줄씩으로 설명하시오.

<details><summary>정답</summary>

- **JPA**: 자바의 ORM **표준 인터페이스** (JSR 338). `@Entity`, `EntityManager`, JPQL 등을 정의.
- **Hibernate**: 가장 널리 쓰이는 JPA **구현체**. 사실상 표준.
- **Spring Data JPA**: JPA 위에 *repository 패턴 자동화* 를 얹은 Spring 모듈. `JpaRepository` 만 상속하면 CRUD/페이징 자동 제공.

세 층은 각각 *스펙 / 구현체 / 편의 추상화*.

</details>

---

### Q2. (개념) ORM 이 풀어주는 "객체-테이블 패러다임 차이" 두 가지를 들고 예시와 함께 설명.

<details><summary>정답</summary>

대표적인 차이 두 가지:

1. **관계 표현**: 객체는 *참조* (`board.getWriter()`), 테이블은 *FK 컬럼* (`writer_id`). 객체에서는 한 줄 탐색이지만 SQL 로는 JOIN.
2. **컬렉션 표현**: 객체는 `List<Reply>` 한 필드, 테이블은 *별도 자식 테이블* (`reply` with `board_id` FK) + JOIN 또는 N 번 쿼리.

기타: 상속 (객체엔 자연스럽지만 RDB 엔 불가), 데이터 타입 (`enum`, `LocalDateTime` vs 문자열·정수).

ORM 은 매핑 어노테이션으로 이 차이를 *프레임워크가* 흡수.

</details>

---

### Q3. (개념) "JPA 는 SQL 을 쓰지 않는다" 는 흔한 오해다. 올바른 진술로 고치시오.

<details><summary>정답</summary>

**SQL 을 *안 쓴* 게 아니라, 개발자가 *안 짠* 것**. 

JPA 는 내부적으로 *Dialect* (DB 별 SQL 방언) + 매핑 정보를 사용해 `SELECT`, `INSERT`, `UPDATE`, `DELETE` SQL 을 *자동 생성·실행*. 개발자는 `em.find(...)`, `boardRepo.save(...)` 같은 API 만 호출.

함의: SQL 을 *모르면* JPA 의 함정 (N+1, 잘못된 fetch 전략 등) 을 발견·해결 불가. ORM 학습 = SQL 까지 이해.

</details>

---

### Q4. (적용) 다음 요구사항대로 `Member` 엔티티를 작성하시오.
- 테이블: `member`
- PK: `id`, MySQL AUTO_INCREMENT
- `email`: 100자, NOT NULL, UNIQUE
- `name`: 50자, NOT NULL
- `joinedAt`: 가입 시각, 자동 채움, 수정 불가

<details><summary>정답</summary>

```java
import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import java.time.LocalDateTime;

@Entity
@Table(name = "member")
@Getter @Setter
@NoArgsConstructor
@EntityListeners(AuditingEntityListener.class)
public class Member {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 100, nullable = false, unique = true)
    private String email;

    @Column(length = 50, nullable = false)
    private String name;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime joinedAt;
}
```

추가 필요: 메인 클래스에 `@EnableJpaAuditing`.

</details>

---

### Q5. (적용) `@Column` 어노테이션의 *자주 쓰는 옵션 5 가지* 와 각각의 의미를 적으시오.

<details><summary>정답</summary>

| 옵션 | 의미 |
|--|--|
| `name` | 매핑 컬럼 이름. 생략 시 naming strategy 변환 (예: `regDate` → `reg_date`) |
| `nullable` | NULL 허용 여부 (`false` 면 NOT NULL) |
| `length` | 문자열 컬럼 길이 (`VARCHAR(N)`) |
| `unique` | UNIQUE 제약. 다만 *단일 컬럼* 용. 복합 UNIQUE 는 `@Table(uniqueConstraints=...)` |
| `updatable` | `false` 면 UPDATE 의 SET 절에서 제외. 생성 시각 등에 사용 |
| `insertable` | `false` 면 INSERT 의 컬럼 목록에서 제외 (DB 기본값 사용 시) |
| `columnDefinition` | DDL 직접 지정 (`"TEXT"`, `"JSON"` 등) |

</details>

---

### Q6. (적용) `Status { READY, RUNNING, DONE }` enum 을 안전하게 매핑하는 필드 선언을 적으시오.

<details><summary>정답</summary>

```java
@Enumerated(EnumType.STRING)
@Column(length = 20, nullable = false)
private Status status;
```

핵심: **`EnumType.STRING`** — DB 에 `"READY"`, `"RUNNING"`, `"DONE"` 으로 저장. enum 순서나 신규 값 추가에 안전.

부수: `length` 는 *가장 긴 enum 값 이름* 보다 여유 있게. `nullable = false` 는 default 부여 + NOT NULL.

</details>

---

### Q7. (적용) `@CreatedDate` 가 동작하려면 어떤 설정 두 가지가 필요한가? 코드로 적으시오.

<details><summary>정답</summary>

**① 엔티티 클래스에 `@EntityListeners` 부착**:

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Board { ... }
```

**② 메인 클래스 (또는 `@Configuration`) 에 `@EnableJpaAuditing`**:

```java
@SpringBootApplication
@EnableJpaAuditing
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
```

이러면 `save()` 시 `@CreatedDate`, 수정 시 `@LastModifiedDate` 가 자동 채워짐.

</details>

---

### Q8. (적용) `@Transient` 어노테이션의 용도와, 어떤 상황에 쓰는지 예시 코드로.

<details><summary>정답</summary>

**용도**: 해당 필드를 *매핑 대상에서 제외* — DB 컬럼을 만들지도, 읽고 쓰지도 않음. 메모리에만 존재.

**예시**: 캐시 플래그, 계산된 값, 임시 상태.

```java
@Entity
public class Product {
    @Id @GeneratedValue private Long id;
    private int price;
    private int discountRate;

    @Transient
    private int discountedPrice;  // 계산용. DB 에는 안 들어감.

    public void calcDiscounted() {
        this.discountedPrice = price * (100 - discountRate) / 100;
    }
}
```

JPA 가 기본적으로 *모든 필드* 를 매핑 대상으로 보므로, 제외하고 싶을 때만 명시.

</details>

---

### Q9. (디버그) 다음 코드의 문제를 찾으시오.
```java
@Entity
public final class Member {
    @Id @GeneratedValue
    private Long id;
    private String name;

    public Member(String name) {
        this.name = name;
    }
}
```

<details><summary>정답</summary>

**두 가지 문제**:

1. **`final` 클래스**: JPA (Hibernate) 가 LAZY 로딩 등을 위해 *프록시 클래스* 를 동적으로 생성하는데, final 이면 상속 불가 → 프록시 못 만들어 예외 발생.
2. **기본 생성자 누락**: JPA 가 리플렉션으로 빈 인스턴스를 만들고 필드를 채우는 방식. 인자 있는 생성자만 있으면 호출 불가 → 예외.

**수정**:

```java
@Entity
public class Member {           // final 제거
    @Id @GeneratedValue
    private Long id;
    private String name;

    protected Member() {}       // 기본 생성자 추가 (또는 Lombok @NoArgsConstructor)

    public Member(String name) {
        this.name = name;
    }
}
```

`protected` 로 하면 외부에서 직접 `new Member()` 막을 수 있어 안전성 ↑.

</details>

---

### Q10. (디버그) 다음 코드의 문제와 그 원인을 설명하시오.
```java
@Entity
public class Member {
    @Id private long id;       // primitive long
    private String name;
}

// 사용
Member m = new Member();
m.setName("kim");
memberRepo.save(m);            // 예상: INSERT, 실제: ???
```

<details><summary>정답</summary>

**문제**: PK 타입이 primitive `long` 이면 *기본값 `0`*. JPA 가 영속 상태 판단 시 *PK 가 null 또는 default 인가* 를 보는데, `0` 을 *이미 부여된 PK* 로 오인할 수 있음.

`save(entity)` 의 내부 동작:
- PK 가 `null` (Long) 또는 미설정 → `persist()` (INSERT)
- PK 가 설정됨 → `merge()` (이미 존재한다 가정, SELECT 후 UPDATE 또는 새 INSERT)

primitive `long` 의 `0` 은 *설정된 PK 0* 으로 해석되어, *merge* 경로로 들어가 의도와 다른 동작 (예: SELECT WHERE id=0 → 없으면 새 INSERT, 있으면 UPDATE).

**수정**:

```java
@Id private Long id;   // 래퍼 Long
```

`null` 로 시작 → JPA 가 transient 로 정확히 인식 → `persist()` 호출.

</details>

---

### Q11. (디버그) 다음 진술을 반박하시오.
> "`@Enumerated(EnumType.ORDINAL)` 는 정수로 저장되어 공간 효율적이니까 항상 쓰는 게 좋다."

<details><summary>정답</summary>

**반박**: 공간 효율 (몇 바이트) 보다 **데이터 무결성 (사고 비용)** 이 압도적으로 큼.

`ORDINAL` 은 enum 값을 *선언 순서대로 0, 1, 2, ...* 저장:

```java
// 처음
enum Status { READY, RUNNING, DONE }     // 0=READY, 1=RUNNING, 2=DONE
```

6개월 뒤 요구사항: "PAUSED 도 추가". 누군가 *앞에* 추가:

```java
enum Status { PAUSED, READY, RUNNING, DONE }
// 새 매핑: 0=PAUSED, 1=READY, 2=RUNNING, 3=DONE
// 기존 DB 의 0=READY 가 → 이제 0=PAUSED 로 잘못 해석!
```

복구는 데이터 마이그레이션 + 모든 row 의 status 컬럼을 `+1` 로 변환. 운영 중 사고면 큰 비용.

**원칙**: *처음부터* `EnumType.STRING`. 공간 차이는 무시 가능 (`"READY"` = 5 byte, `0` = 4 byte int → 차이 ~1B/row, 100만 row 면 1MB. 데이터 무결성과 비교 불가).

</details>

---

### Q12. (디버그) Lombok `@Data` 를 `@Entity` 클래스에 붙였을 때 발생할 수 있는 두 가지 문제를 들고 권장 대안 적으시오.

<details><summary>정답</summary>

`@Data` = `@Getter` + `@Setter` + `@ToString` + `@EqualsAndHashCode` + `@RequiredArgsConstructor`.

**문제 1: `@ToString` 의 무한 순회**
양방향 연관관계 (`Board` ↔ `Reply`) 가 있으면 `Board.toString()` → `Reply.toString()` → `Board.toString()` → ... StackOverflowError 또는 무한 SQL.

**문제 2: `@EqualsAndHashCode` 의 transient/managed 충돌**
모든 필드로 hashCode 를 만들면, *id 가 null 인 transient 상태* 와 *id 가 부여된 managed 상태* 가 다른 hashCode → HashSet 등에서 객체를 못 찾음. 또한 dirty checking 의 비교에도 영향.

**권장 대안**:

```java
@Entity
@Getter @Setter      // 필요한 것만
@NoArgsConstructor
public class Board {
    // ...

    // equals/hashCode 는 PK 기준으로 직접 작성
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Board b)) return false;
        return id != null && id.equals(b.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();   // PK 가 변해도 일관성 유지
    }
}
```

또는 *equals/hashCode 자체를 안 쓰는* 코드 스타일 (대부분의 경우 안전).

</details>

---

### Q13. (면접) "MyBatis 와 JPA 중 어느 게 더 좋아요?" 한 줄로 답하시오.

<details><summary>정답</summary>

**상황에 따라 다름. 둘은 trade-off** — JPA 는 *도메인 중심·연관관계 다용·DB 종속 최소화* 에 강하고, MyBatis 는 *복잡한 SQL·동적 쿼리·통계·튜닝 자유도* 에 강함.

신규 도메인 모델은 JPA, 복잡한 보고서·legacy DB 는 MyBatis — *한 프로젝트에 같이 쓰는 것* 도 흔함. *둘 다 알고 선택할 줄 아는 게* 실무 역량.

</details>

---

### Q14. (면접) "Hibernate 와 JPA 는 같은 건가요?" — 면접관의 함정 질문. 어떻게 답할지.

<details><summary>정답</summary>

**같지 않다**.

- **JPA**: 자바 표준 *스펙* (JSR 338). 인터페이스·어노테이션의 정의 — `EntityManager`, `@Entity`, `@Id`, JPQL 등.
- **Hibernate**: 그 스펙의 *구현체*. 다른 구현체로 EclipseLink, OpenJPA 등이 있지만 사실상 Hibernate 가 표준.

비유:
- JPA = JDBC 인터페이스 (스펙)
- Hibernate = MySQL Connector/J 같은 *구체 드라이버*

또 하나: Hibernate 는 JPA 스펙 *밖* 의 자체 기능 (예: `@DynamicUpdate`, native API) 을 추가로 제공. 그래서 *JPA 만 쓰면* 구현체 교체 자유, *Hibernate 자체 기능 쓰면* 종속.

</details>
