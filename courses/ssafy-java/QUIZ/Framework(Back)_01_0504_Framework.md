# Spring Framework — 퀴즈

> 18문항. 개념·적용·디버그·면접. 5부(Framework·DI/AOP/PSA·Maven·SLF4j·JUnit·Lombok) 골고루.

---

## Part A. Framework / Spring 3대 핵심

### Q1. (개념) 라이브러리와 프레임워크의 본질적 차이를 한 문장으로?

<details><summary>정답</summary>

**호출 방향**. 라이브러리는 내가 부르고, 프레임워크는 프레임워크가 내 코드를 부른다(IoC, 제어 역전). 그래서 프레임워크는 흐름의 주도권을 갖는다.

</details>

### Q2. (개념) Spring 의 3대 핵심 패턴은? 각 1줄 설명.

<details><summary>정답</summary>

- **DI** (Dependency Injection): 객체 의존성을 외부에서 주입 → 결합도 ↓ + 테스트 가능
- **AOP** (Aspect-Oriented Programming): 횡단 관심사(로깅·보안·트랜잭션) 분리 → 비즈니스 로직 순수성
- **PSA** (Portable Service Abstraction): 표준 인터페이스로 기술 추상화 → 기술 교체 시 코드 변경 0

이 셋이 POJO(순수 자바 객체) 를 중심으로 조화.

</details>

### Q3. (적용) 다음 코드의 문제점과 DI 적용 후 모습?

```java
public class OrderService {
    private final PaymentClient pay = new TossPayment();
}
```

<details><summary>정답</summary>

**문제**: 강한 결합. 카드사 바꾸려면 코드 수정. 테스트 시 실제 Toss 연동 필요 → 테스트 불가.

**DI 적용**:
```java
public class OrderService {
    private final PaymentClient pay;

    public OrderService(PaymentClient pay) {
        this.pay = pay;
    }
}
```
`PaymentClient` 인터페이스만 의존. 구현체는 외부(컨테이너) 가 주입.

</details>

### Q4. (면접) "AOP 의 횡단 관심사가 뭔가요? 예를 들어 설명해주세요."

<details><summary>정답</summary>

여러 메서드·클래스에 **공통으로 적용되는 부가 기능**. 비즈니스 로직과 별개지만 어디든 따라다님.

**예**:
- **로깅** — 모든 컨트롤러 메서드의 입/출력을 자동 기록
- **트랜잭션** — `@Transactional` 한 줄로 자동 begin/commit/rollback
- **보안** — 메서드 호출 전 권한 검사 (`@PreAuthorize`)
- **성능 측정** — 메서드 실행 시간 자동 측정

AOP 없이는 모든 메서드 앞뒤에 같은 코드 반복.

</details>

### Q5. (개념) Spring 과 Spring Boot 의 관계?

<details><summary>정답</summary>

**Spring Boot 는 Spring 의 새 버전이 아니라 Spring 을 더 쉽게 쓰게 해주는 도구**. 두 핵심 사상:

1. **자동 설정 (Auto-configuration)**: 클래스패스 라이브러리를 보고 기본 설정 자동 적용
2. **설정보다 관습 (Convention over Configuration)**: 80% 의 흔한 기본값 미리 적용

Spring Boot 를 쓰더라도 Spring 의 원리(DI/AOP/PSA) 는 그대로 작동.

</details>

---

## Part B. Maven

### Q6. (개념) Maven 의 G.A.V 3요소가 무엇인가?

<details><summary>정답</summary>

전 세계 유일한 프로젝트 식별자:
- **GroupId** — 소속 그룹/도메인 (역순). 예: `org.springframework`
- **ArtifactId** — 프로젝트 이름. 예: `spring-context`
- **Version** — 현재 버전. 예: `6.1.0`

</details>

### Q7. (적용) `pom.xml` 의 dependency scope 5가지와 각 의미는?

<details><summary>정답</summary>

| scope | 의미 |
|--|--|
| `compile` | 기본값. 컴파일·테스트·런타임 모두 |
| `test` | 테스트 시에만 (배포 jar 에 포함 안 됨) |
| `provided` | 컴파일 시 제공, 런타임은 외부 (WAS 가 제공) — servlet-api 등 |
| `runtime` | 런타임만 (컴파일 시 불필요) — DB 드라이버 등 |
| `system` | 로컬 파일 시스템 (잘 안 씀) |

</details>

### Q8. (디버그) `mvn package` 가 실패. 출력에 `tests failed`. 어떻게 동작했나?

<details><summary>정답</summary>

`mvn package` 는 `clean → compile → test → package` 라이프사이클을 순차 실행. `test` 단계에서 **JUnit 테스트가 하나라도 실패하면 빌드를 중단** → `package` 단계까지 진행 안 됨.

해결: 실패한 테스트 수정. 임시로 건너뛰려면 `mvn package -DskipTests=true` (권장하지 않음).

</details>

---

## Part C. SLF4j / Logging

### Q9. (개념) System.out.println 의 4가지 한계?

<details><summary>정답</summary>

1. **휘발성** — 콘솔 버퍼가 가득차면 과거 데이터 손실
2. **성능 저하** — 운영 환경에서 불필요한 출력이 메서드 호출마다
3. **정보 부족** — 언제·어디서·어느 스레드 메타데이터 없음
4. **구분 불가** — 디버깅 메시지와 에러가 한 스트림에 섞임

</details>

### Q10. (개념) SLF4j 가 Logback 보다 한 단계 위에 있는 이유? 어떤 패턴인가?

<details><summary>정답</summary>

**PSA (Portable Service Abstraction)** 의 모범 사례. 코드는 SLF4j 인터페이스에만 의존, 실제 로깅 구현체(Logback/Log4j/JUL) 는 교체 가능.

log4j2 보안 이슈(Log4Shell) 가 터졌을 때 SLF4j 쓰던 프로젝트는 의존성만 Logback 으로 바꾸고 끝. 코드 변경 0.

</details>

### Q11. (적용) 다음 두 코드의 성능 차이는 언제 발생하나?

```java
log.debug("user " + userId + " ordered " + count);   // A
log.debug("user {} ordered {}", userId, count);      // B
```

<details><summary>정답</summary>

**DEBUG 가 비활성화된 상태**에서 차이 발생.

- A: log level 무시돼도 `"user " + userId + " ordered " + count` 문자열 결합이 **항상** 실행됨
- B: DEBUG 가 비활성이면 `{}` 자리 치환 자체가 **실행되지 않음**

운영 환경에서 DEBUG off + 메서드 호출 빈번하면 누적 비용 큼. B 패턴이 압도적.

</details>

### Q12. (적용) 다음 클래스에 SLF4j Logger 를 적용하시오. (Lombok 활용)

```java
public class OrderService {
    public void order(Order order) {
        // 여기에 로깅
    }
}
```

<details><summary>정답</summary>

```java
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class OrderService {
    public void order(Order order) {
        log.info("order placed id={}", order.getId());
    }
}
```

`@Slf4j` 가 컴파일 시 `private static final Logger log = LoggerFactory.getLogger(OrderService.class);` 를 자동 생성.

</details>

---

## Part D. JUnit

### Q13. (적용) 다음 메서드의 0으로 나누기 케이스를 검증하는 JUnit 테스트?

```java
public int divide(int a, int b) {
    if (b == 0) throw new ArithmeticException("Cannot divide by zero");
    return a / b;
}
```

<details><summary>정답</summary>

```java
@Test
@DisplayName("0으로 나누면 ArithmeticException 발생")
void divide_byZero_throws() {
    ArithmeticException e = assertThrows(
        ArithmeticException.class,
        () -> calc.divide(10, 0)
    );
    assertEquals("Cannot divide by zero", e.getMessage());
}
```

`assertThrows` 가 람다 실행 → 예외 발생 시 객체 반환 → 메시지 검증까지 한 번에.

</details>

### Q14. (개념) `@BeforeEach` 와 `@BeforeAll` 의 차이? 언제 각각 쓰나?

<details><summary>정답</summary>

- `@BeforeEach`: **각 테스트 메서드마다** 매번 실행 → 테스트 간 독립성 보장. 가벼운 초기화 (DTO 생성 등).
- `@BeforeAll`: **클래스에서 1번만** 실행 (`static` 필수) → 비싼 초기화 (DB 컨테이너 기동, 외부 서버 연결).

`@BeforeAll` 로 만든 상태를 테스트가 공유하면 순서 의존이 생길 수 있으니 주의 — 보통 읽기 전용 자원에만.

</details>

### Q15. (적용) 입력값 여러 개로 같은 테스트를 반복하려면 어떤 어노테이션?

<details><summary>정답</summary>

`@ParameterizedTest` + 데이터 소스.

```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3, 5, 8, 13})
void isPositive(int n) {
    assertTrue(n > 0);
}

// 또는 CSV
@ParameterizedTest
@CsvSource({
    "1, 2, 3",
    "4, 5, 9",
    "0, 0, 0"
})
void add(int a, int b, int expected) {
    assertEquals(expected, calc.add(a, b));
}
```

같은 로직을 여러 입력으로 검증 — 코드 중복 0.

</details>

---

## Part E. Lombok

### Q16. (개념) `@Data` 어노테이션이 자동 생성하는 것 5가지?

<details><summary>정답</summary>

1. `@Getter` — 모든 필드 getter
2. `@Setter` — 모든 non-final 필드 setter
3. `@ToString` — `toString()`
4. `@EqualsAndHashCode` — `equals()`, `hashCode()` (모든 필드 기반)
5. `@RequiredArgsConstructor` — `final` 필드만 받는 생성자

</details>

### Q17. (디버그) JPA 엔티티에 `@Data` 를 붙였더니 `StackOverflowError`. 원인과 해결?

<details><summary>정답</summary>

`@Data` 의 `equals/hashCode/toString` 이 **모든 필드**를 비교/출력. 양방향 연관관계 (`@OneToMany` ↔ `@ManyToOne`) 에서 부모 → 자식 → 부모 → 자식 ... **무한 재귀** → `StackOverflowError`.

해결:
- 엔티티엔 `@Data` 금지 → `@Getter` + `@Setter` 만
- `equals/hashCode` 는 ID 기반으로 직접 정의
- `toString` 도 직접 정의하거나 `@ToString(exclude = "children")`

</details>

### Q18. (면접) "Lombok 의존성에 왜 `<scope>provided</scope>` 또는 compileOnly 를 추천하나요?"

<details><summary>정답</summary>

Lombok 은 **컴파일 시점에 AST(추상 구문 트리) 를 조작해 메서드를 생성**. 컴파일 후 `.class` 파일엔 메서드가 이미 실체로 들어가 있어서 **런타임엔 Lombok jar 가 필요 없다**.

`compile` scope 로 두면 운영 jar 에 Lombok 이 포함되어:
- 배포 jar 크기 증가
- 런타임 클래스로더에 불필요한 라이브러리 추가
- 보안 관점에서 공격 표면 확대

따라서 `provided` (Maven) 또는 `compileOnly` + `annotationProcessor` (Gradle) 가 권장.

</details>
