# Spring Framework — 프레임워크·DI/AOP/PSA·Maven·SLF4j·JUnit·Lombok

> **이 강의는 무엇인가**: "프레임워크" 가 무엇인지부터 시작해, Spring 의 3대 핵심 패턴(**DI/AOP/PSA**), 의존성을 관리하는 **Maven**, 로그를 남기는 **SLF4j**, 코드를 검증하는 **JUnit**, 보일러플레이트를 줄이는 **Lombok** 까지. Spring 학습 여정의 출발점.
> **왜 배우는가**: 이후 Spring 강의 12개의 모든 개념(DI/AOP/MVC/MyBatis/Interceptor/Batch)이 이 강의에서 깐 토대 위에 쌓인다. Maven 없으면 라이브러리 도입 불가, SLF4j 없으면 디버깅 불가, JUnit 없으면 리팩터링 불가, Lombok 없으면 손목 박살. 5가지 모두 일상 도구.

---

## 들어가기 전에

- **선수**: Java OOP, 인터페이스·다형성 감각, 자바 패키지·jar 의 의미.
- **마인드셋**: "내가 호출하는 코드" vs "내가 호출당하는 코드" 의 차이를 의식. 프레임워크의 본질은 이 호출 방향의 역전이다.

---

# Part A. Framework 의 정의

## 1. 일상에서 보는 프레임워크 — PowerPoint 비유

```
[멋진 발표를 만들고 싶다]

      방법 1: 처음부터 다 만들기              방법 2: PowerPoint 사용
      ---------------------              --------------------------
      ▸ 슬라이드 렌더링 엔진 코딩             ▸ PowerPoint 가 다 해줌
      ▸ 애니메이션 라이브러리 구현             ▸ 나는 발표 "내용" 만 채움
      ▸ 폰트 시스템 구현                      ▸ 슬라이드 디자인은 템플릿
      ▸ ... 그리고 마침내 발표 내용
```

**프레임워크의 본질**: "뼈대(Frame)" 는 미리 만들어져 있고, 내용(Content) 만 채워 넣게 해주는 도구. 작업자가 본 문제(발표 내용) 에 집중할 수 있도록 부수 작업(렌더링·애니메이션) 을 흡수.

## 2. 라이브러리 vs 프레임워크 — 호출 방향의 차이

```java
// 라이브러리 (Library) - "내가 부른다"
String json = Gson.toJson(user);            // 내 코드가 Gson 호출

// 프레임워크 (Framework) - "프레임워크가 내 코드를 부른다" (IoC)
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    protected void doGet(...) { ... }       // Tomcat 이 부름
}

@Controller
public class HomeController {
    @GetMapping("/")
    public String home() { return "home"; } // Spring 이 부름
}
```

**핵심 차이**: **제어의 역전 (IoC, Inversion of Control)**. 라이브러리는 내가 도구를 부르고, 프레임워크는 도구가 나를 부른다.

```
라이브러리:
   [내 코드] --호출--> [라이브러리]      주도권: 내가

프레임워크:
   [프레임워크] --호출--> [내 코드]       주도권: 프레임워크가
```

## 3. Spring Framework — 자바 개발의 봄

- **정의**: 자바 엔터프라이즈 개발을 편하게 해주는 **경량급 오픈소스 애플리케이션 프레임워크**.
- **특징**: 경량 컨테이너 — 객체의 생성부터 소멸까지 **라이프사이클을 대신 관리**.
- **이름의 유래**: EJB(Enterprise Java Bean) 의 춥고 혹독한 기술의 겨울이 가고, 개발자에게 봄(Spring) 이 왔다는 의미.

---

# Part B. Spring 의 3대 핵심 — DI · AOP · PSA

POJO(Plain Old Java Object) 를 중심으로 세 패턴이 조화를 이룬다.

```
POJO  (Plain Old Java Object - 기술 종속성 최소)
  |
  +--> DI   - 의존성 주입 (객체 연결의 자동화)
  +--> AOP  - 횡단 관심사 분리 (로깅·트랜잭션·보안)
  +--> PSA  - 기술 추상화 (표준 인터페이스, 구현체 교체)
```

## 4. DI (Dependency Injection) — 누가 재료를 준비하는가

객체가 의존성 있는 객체를 **직접 생성하지 않고**, 외부에서 생성된 것을 **전달받음**.

```java
// ❌ 강한 결합
public class OrderService {
    private final PaymentClient pay = new TossPayment();
    private final EmailSender   m   = new SmtpEmailSender();
}

// ✅ DI
public class OrderService {
    private final PaymentClient pay;
    private final EmailSender   mail;

    public OrderService(PaymentClient pay, EmailSender mail) {
        this.pay = pay;          // 누가 들어올지는 Spring 컨테이너가 결정
        this.mail = mail;
    }
}
```

**비유**: 직접 시장 가서 재료 사오는 비효율 → 외부에서 배달된 재료로 요리에만 집중.

**얻는 것**:
- **결합도 감소**: 카드사 바꿀 때 `OrderService` 코드 0줄 수정
- **테스트 가능**: 가짜(Mock) 객체 주입 가능
- **유연성**: 환경별로 다른 구현체 (테스트=Mock, 운영=실제)

## 5. AOP (Aspect-Oriented Programming) — 누가 공통 기능을 처리하는가

비즈니스 로직(핵심) 과 공통 부가 기능(로깅·보안·트랜잭션) 을 **분리해서 모듈화**.

```
[Before AOP]  매 메서드에 부가 기능 반복
  insert()
      로그 기록
      보안 검사
      핵심 로직            ← 5줄
      로그 기록
  update()
      로그 기록            ← 또 같은 부가 기능 반복!
      보안 검사
      핵심 로직
      로그 기록

[After AOP]   Aspect 가 모든 메서드에 자동 적용
  insert() / update() / delete()
      핵심 로직만 (5줄)    ← 순수
                ▲
                | 자동 적용
  LoggingAspect · SecurityAspect · TxAspect (별도 모듈로 분리)
```

**비유**: 요리사는 요리에만 집중. 계산·청소·보안은 다른 전문가가 전담. **횡단 관심사(Cross-cutting Concern)** 를 한 곳에 모음.

## 6. PSA (Portable Service Abstraction) — 기술을 분리하라

서로 다른 기술을 **동일한 방식(표준 인터페이스)** 으로 사용할 수 있게 하는 추상화 계층.

```
내 코드
  | depends on
  ▼
표준 인터페이스 (Spring 이 제공 - PSA)
  • JpaRepository
  • JdbcTemplate
  • CacheManager
  | runtime impl
  ▼
  +- JPA / Hibernate
  +- MyBatis
  +- Redis
  +- Memcached
```

**예**: `@Transactional` 한 줄로 JDBC/JPA/JTA 어떤 기술이 뒤에 있든 동일 동작. `CacheManager` 인터페이스로 Redis/Memcached/Caffeine 을 같은 코드로.

## 7. Spring Boot — 준비된 템플릿

|  | Spring | Spring Boot |
|--|--|--|
| 설정 방식 | XML 수동 작성 | 자동 설정 + 어노테이션 |
| 서버 | 톰캣 별도 설치 | 내장 (jar 실행만) |
| 의존성 | 버전 직접 명시 | starter 가 자동 조합 |
| 운영 도구 | 직접 구축 | actuator 내장 |

**핵심 사상 2가지**:
- **자동 설정 (Auto-configuration)**: 클래스패스에 있는 라이브러리를 보고 기본 설정 자동 적용
- **설정보다 관습 (Convention over Configuration, CoC)**: 80% 의 개발자가 쓰는 기본값을 미리 적용 — Opinionated Defaults

**오해 금지**: Spring Boot 는 **새로운 프레임워크가 아니다**. Spring 을 더 쉽게 쓰게 해주는 **개발 도구**.

---

# Part C. Maven — 의존성 지옥 탈출

## 8. Maven 등장 이전의 한계 — 의존성 지옥

수동 다운로드 시:
- ❌ 어떤 jar 가 어디 있는지 찾기
- ❌ 라이브러리 간 버전 호환성 직접 검증
- ❌ transitive 의존성 (라이브러리가 의존하는 또 다른 라이브러리) 누락
- ❌ `NoClassDefFoundError`, `MethodNotFoundException` 폭격

## 9. Maven 의 핵심 역할

| 역할 | 내용 |
|--|--|
| **의존성 관리** | `pom.xml` 에 목록만 적으면 중앙 저장소에서 자동 다운로드 + transitive 함께 |
| **구조 표준화** | 모든 프로젝트에 동일한 디렉토리 구조 강제 |
| **빌드 체계화** | compile → test → package → install → deploy 의 라이프사이클 |

## 10. pom.xml — 프로젝트의 명찰

`pom.xml` (Project Object Model) — **유일한 식별자 (G.A.V)** + 모든 설정.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>            <!-- 도메인 역순 -->
    <artifactId>my-app</artifactId>           <!-- 프로젝트 이름 -->
    <version>0.0.1-SNAPSHOT</version>         <!-- 현재 버전 -->

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>6.1.0</version>
            <scope>compile</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

**의존성 scope 5가지**:

| scope | 의미 |
|--|--|
| `compile` | 기본값. 컴파일·테스트·런타임 모두 |
| `test` | 테스트 시에만 (배포 jar 에 포함 안 됨) |
| `provided` | 컴파일만, 런타임은 외부 (WAS) — servlet-api 등 |
| `runtime` | 런타임만 (컴파일 시엔 불필요) — DB 드라이버 등 |
| `system` | 로컬 파일 시스템 (잘 안 씀) |

## 11. 표준 디렉토리 구조

```
project-root/
+-- pom.xml                          ← 프로젝트 명세
+-- src/
|   +-- main/
|   |   +-- java/                    ← 비즈니스 로직
|   |   +-- resources/               ← XML, properties, yml
|   +-- test/
|       +-- java/                    ← 테스트 코드
|       +-- resources/
+-- target/                          ← 빌드 결과물 (.class, .jar)
```

## 12. 빌드 라이프사이클

```
clean -> compile -> test -> package -> install -> deploy

  ↓        ↓         ↓        ↓          ↓         ↓
target  .class    JUnit    .jar 생성  ~/.m2/    원격 저장소
삭제     생성      실행      또는 .war  로컬     (Nexus 등)
```

| 단계 | 동작 |
|--|--|
| `clean` | `target/` 삭제 |
| `compile` | `.java` → `.class` |
| `test` | JUnit 실행. 실패 시 빌드 중단 |
| `package` | `.jar` 또는 `.war` 로 압축 |
| `install` | `~/.m2/repository` 로컬 등록 |
| `deploy` | 원격 저장소(Nexus, Artifactory) 등록 |

**도미노 효과**: `mvn package` 실행 → 자동으로 `clean → compile → test → package` 까지 차례대로.

---

# Part D. SLF4j 와 Logging

## 13. System.out.println 의 4가지 한계

| 문제 | 영향 |
|--|--|
| **휘발성** | 콘솔 버퍼 가득차면 과거 데이터 손실 → 운영 사고 시 증거 0 |
| **성능 저하** | 운영 환경에서 불필요한 출력이 메서드 호출마다 |
| **정보 부족** | 언제·어디서·어느 스레드 메타데이터 부재 |
| **구분 불가** | 단순 디버깅과 심각한 에러가 한 스트림에 섞임 |

## 14. SLF4j + Logback — PSA 패턴의 모범

```
            애플리케이션 코드
                  |
                  ▼
           SLF4j 인터페이스   ← 표준 (개발자는 이것만)
                  |
              +---+---+
              ▼   ▼   ▼
          Logback Log4j java.util.logging
                            (구현체 Worker)
```

**SLF4j (Simple Logging Facade for Java)**: PSA 의 교과서. 인터페이스만 노출, 구현체는 교체 가능. 가장 흔한 구현체: **Logback** (SLF4j 와 같은 저자, 사실상 표준).

## 15. Logger 사용 + Log Level

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderService {
    private static final Logger log = LoggerFactory.getLogger(OrderService.class);

    public void order(Order order) {
        log.trace("entering order() args={}", order);
        log.debug("order.userId={}", order.getUserId());
        log.info("order placed id={}", order.getId());
        log.warn("retry count={}", retries);
        log.error("payment failed", e);
    }
}
```

**Log Level 우선순위** (낮을수록 상세):
```
TRACE  <  DEBUG  <  INFO  <  WARN  <  ERROR
```

설정에서 `INFO` 로 잡으면 TRACE/DEBUG 는 무시.

**Lombok 의 `@Slf4j`** 어노테이션 쓰면 자동:
```java
@Slf4j
public class OrderService {
    public void order() { log.info("..."); }
}
```

## 16. 파라미터화 메시지 — `{}` 플레이스홀더

```java
// ❌ 문자열 결합 - log level 무시돼도 비용 발생
log.debug("user " + userId + " ordered " + count);

// ✅ 파라미터화 - 실제 출력 시에만 결합
log.debug("user {} ordered {}", userId, count);
```

DEBUG 비활성 시 결합 자체가 실행 안 됨.

## 17. logback.xml 설정

```xml
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/app.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>logs/app.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder><pattern>%d %-5level %logger - %msg%n</pattern></encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="STDOUT" />
        <appender-ref ref="FILE" />
    </root>

    <logger name="com.example.payment" level="DEBUG" />
</configuration>
```

**Appender** 가 출력 위치, **pattern** 으로 포맷 제어. `RollingFileAppender` 로 일자·크기 자동 분할.

---

# Part E. JUnit — 단위 테스트의 표준

## 18. JUnit 의 역할

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private Calculator calc;

    @BeforeEach
    void setUp() { calc = new Calculator(); }

    @Test
    @DisplayName("두 양수 더하기")
    void add_positiveNumbers() {
        assertEquals(5, calc.add(2, 3));
    }

    @Test
    @DisplayName("0으로 나누면 예외 발생")
    void divide_byZero_throws() {
        assertThrows(ArithmeticException.class,
            () -> calc.divide(10, 0));
    }
}
```

## 19. Assertions — 단정문

| 단정문 | 의미 |
|--|--|
| `assertEquals(expected, actual)` | 값 같음 (`equals()`) |
| `assertNotEquals(expected, actual)` | 값 다름 |
| `assertSame(expected, actual)` | 같은 객체 (`==`) |
| `assertNotSame(expected, actual)` | 다른 객체 |
| `assertNull` / `assertNotNull` | null 여부 |
| `assertTrue` / `assertFalse` | 불리언 |
| `assertThrows(Type.class, lambda)` | 예외 발생 검증 |
| `assertDoesNotThrow(lambda)` | 예외 없음 검증 |
| `assertAll(...)` | 여러 단정문 일괄 |

`assertEquals` 는 `equals()` 비교, `assertSame` 은 메모리 주소(`==`) 비교.

## 20. 라이프사이클 어노테이션

```
@BeforeAll   ← 클래스 전체에서 1번 (static)
  +------------------------+
  | @BeforeEach            | ← 각 테스트 전에
  |   @Test method1        |
  | @AfterEach             | ← 각 테스트 후에
  +------------------------+
  | @BeforeEach            |
  |   @Test method2        |
  | @AfterEach             |
  +------------------------+
@AfterAll    ← 클래스 전체에서 1번 (static)
```

- `@BeforeAll`/`@AfterAll`: 비싼 자원(DB 컨테이너) 한 번만 초기화·정리
- `@BeforeEach`/`@AfterEach`: 각 테스트 사이에 상태 초기화 → 테스트 간 독립성

## 21. 추가 핵심 어노테이션

```java
@DisplayName("사용자 친화적 테스트 이름")
@Test
void test() { ... }

@Disabled("이슈 #123 수정 후 활성화")
@Test
void brokenTest() { ... }

@ParameterizedTest                          // 여러 인자로 반복
@ValueSource(ints = {1, 2, 3, 5, 8})
void isPositive(int n) {
    assertTrue(n > 0);
}

@RepeatedTest(5)                            // 5번 반복 (플레이키 탐지)
void unstableTest() { ... }
```

---

# Part F. Lombok (Appendix) — 보일러플레이트 박멸

## 22. Lombok 이 풀어주는 보일러플레이트

```java
// ❌ 일반 자바 - 60줄
public class User {
    private Long id;
    private String name;
    private String email;

    public User() {}
    public User(Long id, String name, String email) {
        this.id = id; this.name = name; this.email = email;
    }
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    // ... getter/setter 6개 더
    @Override public boolean equals(Object o) { ... }
    @Override public int hashCode() { ... }
    @Override public String toString() { ... }
}

// ✅ Lombok - 5줄
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private String email;
}
```

## 23. 주요 어노테이션

| 어노테이션 | 생성되는 것 |
|--|--|
| `@Getter` / `@Setter` | getter / setter |
| `@ToString` | `toString()` |
| `@EqualsAndHashCode` | `equals()`, `hashCode()` |
| `@NoArgsConstructor` | 빈 생성자 |
| `@AllArgsConstructor` | 모든 필드 생성자 |
| `@RequiredArgsConstructor` | `final` 필드만 (DI 친화!) |
| `@Data` | 위 모든 것 한 번에 |
| `@Slf4j` | `Logger log = ...` |
| `@Builder` | Builder 패턴 자동 |

## 24. 동작 원리 + 함정

**동작 원리**: 컴파일 시 **AST(추상 구문 트리)** 를 조작해 메서드 생성. `.class` 엔 메서드가 실제로 존재. IDE 인식엔 Lombok 플러그인 필요.

**함정 5가지**:

1. **`@Data` + JPA 엔티티** → 양방향 연관관계에서 `equals/hashCode` 무한 재귀 → `StackOverflowError`
2. **`@AllArgsConstructor` 순서 변경 위험** — 필드 추가 시 생성자 시그니처가 조용히 바뀜
3. **상속 + `@EqualsAndHashCode`** — 부모 필드 안 비교됨. `@EqualsAndHashCode(callSuper = true)` 명시
4. **`final` 필드 누락** — `@RequiredArgsConstructor` 는 `final` 필드만 인자
5. **롬복 scope** — `compileOnly` + `annotationProcessor` (또는 `provided`). 런타임 jar 에 포함 불필요

---

## 25. 코드 깊게 — 풀스택 통합

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>6.1.0</version>
    </dependency>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>2.0.9</version>
    </dependency>
    <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-classic</artifactId>
        <version>1.4.14</version>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.30</version>
        <scope>provided</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

```java
// Calculator.java
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Calculator {

    public int add(int a, int b) {
        log.debug("add called a={}, b={}", a, b);
        int result = a + b;
        log.info("add result={}", result);
        return result;
    }

    public int divide(int a, int b) {
        if (b == 0) {
            log.error("divide by zero attempted a={}", a);
            throw new ArithmeticException("Cannot divide by zero");
        }
        return a / b;
    }
}
```

```java
// CalculatorTest.java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private Calculator calc;

    @BeforeEach
    void setUp() { calc = new Calculator(); }

    @Test
    @DisplayName("양수 더하기")
    void add_positives() {
        assertEquals(5, calc.add(2, 3));
    }

    @Test
    @DisplayName("0으로 나누면 ArithmeticException")
    void divide_byZero_throws() {
        ArithmeticException e = assertThrows(
            ArithmeticException.class,
            () -> calc.divide(10, 0)
        );
        assertEquals("Cannot divide by zero", e.getMessage());
    }
}
```

`mvn test` → JUnit 자동 실행 → 모두 통과해야 빌드 성공.

---

## 26. 실전 패턴 / 자주 빠지는 함정

### Framework / DI
- ❌ "Spring 은 마법" → 어노테이션을 외우기만 ✅ "프레임워크가 내 코드를 부른다(IoC)" 의 본질
- ❌ DI 를 "그냥 의존성 받는 거" 로만 이해 ✅ "테스트 가능성·환경별 교체 가능성" 이 목적

### Maven
- ❌ 라이브러리 검색해 jar 직접 다운로드 ✅ `mvnrepository.com` 에서 스니펫 복사
- ❌ scope 안 지정 → JUnit 이 운영 jar 에 포함되어 보안 위협 ✅ `<scope>test</scope>`
- ❌ 버전 충돌로 빌드 실패 → 직접 강제 ✅ `mvn dependency:tree` + `<dependencyManagement>`

### Logging
- ❌ `System.out.println` 으로 디버깅 ✅ `Logger` + 적절한 level
- ❌ `log.debug("msg " + obj)` ✅ `log.debug("msg {}", obj)`
- ❌ 운영에서 DEBUG/TRACE 활성 ✅ 운영은 INFO+, 개발은 DEBUG
- ❌ 비밀번호·토큰을 로그에 ✅ `@ToString(exclude = "password")`

### JUnit
- ❌ 테스트끼리 static 상태 공유 ✅ `@BeforeEach` 로 매번 초기화
- ❌ `assertEquals(expected, actual)` 순서 헷갈림 ✅ JUnit 5 는 `(expected, actual)`
- ❌ 한 테스트에 단정문 10개 ✅ 한 테스트 = 한 행동. 일괄 검증은 `assertAll`

### Lombok
- ❌ `@Data` 를 JPA 엔티티에 ✅ `@Getter` + `@Setter` + `equals/hashCode` 직접 정의
- ❌ Lombok 플러그인 미설치 → IDE 빨간줄 ✅ IntelliJ/VS Code 플러그인 설치

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| `NoClassDefFoundError` 런타임 | scope 가 test 인 의존성을 운영 코드가 참조 | scope 를 compile 로 |
| `mvn compile` 시 `package does not exist` | IDE 인덱싱 안 됨 | `mvn dependency:resolve` |
| `log.debug` 가 안 찍힘 | logback root level 이 INFO | logger 설정 추가 |
| `@Slf4j` 후 `log` 빨간 줄 | Lombok 플러그인 미설치 | IDE 플러그인 설치 |
| JUnit 테스트가 IDE 에서 안 보임 | jupiter 의존성 missing | `junit-jupiter` 추가 |
| `assertEquals` 통과인데 결과 이상 | `equals()` 가 reference 비교 (Object 기본) | `equals/hashCode` 오버라이드 |
| jar 패키징 후 Logback 충돌 | 다른 SLF4j 구현체 동시 포함 | `mvn dependency:tree` 로 충돌 제거 |

---

## 27. 자가점검

1. 라이브러리와 프레임워크의 본질적 차이를 한 문장으로?
2. Spring 의 3대 핵심 패턴 (DI·AOP·PSA) 의 역할을 각각 1줄로?
3. POJO 가 왜 중요한가?
4. Maven 의 `scope` 5가지와 각 의미는?
5. SLF4j 가 Logback 보다 위에 있는 이유는?
6. `log.debug("msg " + x)` 와 `log.debug("msg {}", x)` 의 성능 차이가 발생하는 시점은?
7. JUnit 의 `@BeforeEach` 와 `@BeforeAll` 의 차이는?
8. `@Data` 를 엔티티에 쓰면 안 되는 이유는?

<details><summary>풀이</summary>

1. **호출 방향**. 라이브러리는 내가 부르고(IoC ❌), 프레임워크는 프레임워크가 내 코드를 부른다(IoC ✓).
2. **DI**: 객체 의존성을 외부에서 주입 → 결합도 ↓ 테스트 가능. **AOP**: 횡단 관심사 분리 → 비즈니스 로직 순수. **PSA**: 기술 표준 인터페이스 → 기술 교체 시 코드 변경 0.
3. 기술 종속성 최소화. 특정 프레임워크에 묶이지 않아 테스트 가능 + 이식성 ↑.
4. `compile`(기본 전 단계), `test`(테스트만), `provided`(컴파일만 + 런타임은 외부), `runtime`(런타임만, DB 드라이버), `system`(로컬 파일).
5. **PSA 패턴**. SLF4j 인터페이스에만 의존, 구현체 교체 가능. log4j2 보안 이슈 때 Logback 으로 갈아탈 수 있었던 이유.
6. **DEBUG 비활성**에도 문자열 결합 실행 (전자) vs **DEBUG 활성 시에만** 결합 (후자). 운영 DEBUG off 면 후자가 압도적 빠름.
7. `@BeforeEach` 는 **각 테스트마다** 매번, `@BeforeAll` 은 **클래스에서 1번**. `@BeforeAll` 은 `static`.
8. `@Data` 가 `equals/hashCode/toString` 을 모든 필드로 생성 → JPA 양방향 연관관계 무한 재귀 → `StackOverflowError`. 엔티티엔 `@Getter` + `equals/hashCode` 직접 정의 (ID 기반).

</details>

---

## 28. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.9 Framework 정의·라이브러리 vs FW | §1, §2 |
| p.10 ~ p.12 Spring·Boot 비교 | §3, §7 |
| p.13 ~ p.16 POJO·DI·AOP·PSA | §4 ~ §6 (Part B) |
| p.17 ~ p.23 Maven (pom.xml·구조·라이프사이클) | §8 ~ §12 (Part C) |
| p.24 ~ p.29 SLF4j·Logback·Logger·설정 | §13 ~ §17 (Part D) |
| p.30 ~ p.39 JUnit (Assertions·Lifecycle·Parameterized) | §18 ~ §21 (Part E) |
| p.40 ~ p.43 Lombok (어노테이션·동작 원리) | §22 ~ §24 (Part F) |
| p.44 마무리 | (생략) |

_44p 슬라이드 모두 커버._
