# Spring DI — 개념·IoC 컨테이너·미니 구현·Spring Container·명시적/묵시적 DI

> **이 강의는 무엇인가**: Spring 의 심장인 **DI(의존성 주입)** 의 사상부터, IoC 컨테이너의 동작 원리, 그리고 컨테이너를 **직접 만들어보고**, 마지막으로 진짜 Spring Container 를 빌드하여 **XML/Java Config/Annotation 3가지 방식**으로 객체를 주입하는 전 과정.
> **왜 배우는가**: 모든 Spring 강의의 토대. 어노테이션이 "마법" 처럼 보이지 않으려면 IoC 컨테이너가 리플렉션 + HashMap 으로 어떻게 객체를 관리하는지 직접 만들어봐야 한다. 본 강의는 그 직관을 깐다.

---

## 들어가기 전에

- **선수**: Java OOP (인터페이스·다형성), Framework 강의(IoC 의 의미·Spring 3대 패턴).
- **마인드셋**: "객체 생성을 누가 하는가" 라는 한 가지 질문을 계속 던질 것. 생성 주체가 바뀌면(나 → 컨테이너) 모든 게 바뀐다.

---

# Part A. DI 개념

## 1. 의존성 (Dependency) 이란

```java
class Programmer {
    private Computer computer;  // Programmer 는 Computer 가 "필요"
}
```

**의존성**: 하나의 객체가 자신의 기능을 수행하기 위해 **다른 객체를 필요로 하는 관계**.

- 프로그래머 → 컴퓨터 (업무 수행에 필수)
- 주문 서비스 → 결제 클라이언트 (주문 처리에 필수)
- 컨트롤러 → 서비스 → DAO (계층 의존)

```
       Programmer  --needs-->  Computer
       (의존하는 쪽)             (의존되는 쪽)
```

## 2. DI 없이 — 강한 결합의 폐해

```java
public class Programmer {
    private Computer computer = new Desktop();   // 직접 생성!

    public void work() { computer.boot(); }
}
```

**문제**:
- ❌ Programmer 가 Desktop 구현에 묶임 — Laptop 으로 바꾸려면 코드 수정
- ❌ 테스트 시 진짜 Desktop 필요 — Mock 주입 불가
- ❌ Computer 가 더 많은 의존성을 가지면 그것까지 다 새로 만들어야 (의존성 폭발)
- ❌ Programmer 의 단일 책임 위반 — "업무 수행" + "Desktop 생성" 2가지 책임

## 3. DI 적용 후 — 외부에서 주입

```java
public class Programmer {
    private final Computer computer;

    public Programmer(Computer computer) {   // 외부에서 받음
        this.computer = computer;
    }

    public void work() { computer.boot(); }
}

// 사용 측
Computer dell = new Desktop();
Programmer alice = new Programmer(dell);
```

**핵심 변화**:
- Programmer 는 **Computer 인터페이스에만 의존**, 어떤 구현인지 모름
- "누가 들어올지" 는 외부가 결정 — 테스트엔 `new FakeComputer()`, 운영엔 `new Desktop()`
- 객체 생성 책임이 분리됨 → 단일 책임 원칙(SRP) 준수

```
   Before DI                       After DI
   --------                        --------
   Programmer                      Programmer
       |                                ▲
       | new Desktop()                  | 주입
       ▼                                |
    Desktop                          Computer (Desktop OR Laptop OR Fake)
   강한 결합                          약한 결합
```

---

# Part B. IoC Container — 객체 관리 자동화

## 4. IoC(Inversion of Control) 의 의미

**제어의 역전**: 객체의 생성·생명주기·의존성 주입의 주도권이 개발자 → 프레임워크(컨테이너) 로 넘어가는 현상.

```
[Before IoC]  개발자가 직접 생성·연결
  내 코드
    new A();
    new B(a);
    new C(a, b);
  → 주도권: 개발자

[After IoC]   컨테이너가 객체 생명주기 자동 관리
  IoC Container
    A, B, C 빈으로 등록
    의존성 자동 조립 (메타데이터 기반)
  → 주도권: 컨테이너 (개발자는 "필요한 빈" 선언만)
```

**DI 와 IoC 의 관계**: DI ⊂ IoC. DI 는 IoC 를 실현하는 구체적 기법.

## 5. IoC Container 의 2가지 역할

| 역할 | 내용 |
|--|--|
| **객체 관리 자동화** | 클래스 생성부터 소멸까지 라이프사이클(생성·초기화·사용·소멸) 전담 |
| **의존성 조립** | 메타데이터·어노테이션을 기반으로 필요한 객체를 스스로 찾고 연결 |

## 6. 어노테이션 + 리플렉션 — 컨테이너의 두 무기

컨테이너가 "어떤 객체를 만들고 어떻게 연결할지" 를 알려면 **설계도** 가 필요하다. 그 설계도가 어노테이션이고, 그 설계도를 읽는 도구가 리플렉션.

```
[설계도 - 어노테이션]                [읽는 도구 - 리플렉션]
  @Component                        Reflection API
  @MyBean              ---->          · class.getDeclaredMethods()
  @Configuration                       · method.isAnnotationPresent()
  (코드 위 메모)                        · method.invoke()
```

```java
// 어노테이션 선언
@Retention(RetentionPolicy.RUNTIME)   // ← 런타임까지 살아있어야 리플렉션 가능
@Target(ElementType.METHOD)
public @interface MyBean {}

// 어노테이션 사용
public class AppConfig {
    @MyBean
    public Computer getComputer() { return new Desktop(); }
}

// 컨테이너가 리플렉션으로 읽기
Method[] methods = AppConfig.class.getDeclaredMethods();
for (Method m : methods) {
    if (m.isAnnotationPresent(MyBean.class)) {
        Object bean = m.invoke(configInstance);   // 메서드 호출해 빈 생성
        beanMap.put(m.getName(), bean);
    }
}
```

---

# Part C. 미니 IoC Container 직접 만들기

## 7. STEP 1 — 어노테이션 정의

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyBean { }
```

`RUNTIME` 이 핵심 — 컴파일 후 .class 에 살아남아야 리플렉션으로 읽을 수 있다.

## 8. STEP 2 — 설정 클래스

```java
public class AppConfig {
    @MyBean public Computer getComputer() { return new Desktop(); }
    @MyBean public Programmer getProgrammer() { return new Programmer(); }
}
```

## 9. STEP 3 — 미니 컨테이너 구현

```java
public class MyContainer {
    // 이름(String) → 객체(Object) 매핑 저장소
    private final Map<String, Object> beanMap = new HashMap<>();

    // 생성자에서 설정 클래스를 받아 빈을 모두 등록
    public MyContainer(Class<?> configClazz) throws Exception {
        Object configInstance = configClazz.getDeclaredConstructor().newInstance();

        // 리플렉션으로 메서드 순회
        for (Method method : configClazz.getDeclaredMethods()) {
            // @MyBean 이 붙은 메서드만
            if (method.isAnnotationPresent(MyBean.class)) {
                Object bean = method.invoke(configInstance);
                beanMap.put(method.getName(), bean);
            }
        }
    }

    public Object getBean(String name) {
        return beanMap.get(name);
    }

    @SuppressWarnings("unchecked")
    public <T> T getBean(String name, Class<T> type) {
        return (T) beanMap.get(name);
    }
}
```

## 10. STEP 4 — 사용

```java
MyContainer container = new MyContainer(AppConfig.class);
Computer c = container.getBean("getComputer", Computer.class);
Programmer p = container.getBean("getProgrammer", Programmer.class);
p.setComputer(c);
p.work();   // 동작!
```

**얻은 것**:
- 직접 `new` 하지 않고 컨테이너가 객체 관리
- 빈 추가는 `AppConfig` 에 메서드 + `@MyBean` 만 추가
- 이것이 **Spring 의 작동 원리** — 같은 사상 (HashMap + 리플렉션) 을 더 정교하게 구현한 게 Spring Container

---

# Part D. Spring Container 빌드

## 11. 의존성 추가 — `pom.xml`

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>6.1.0</version>
</dependency>
```

`spring-context` 는 IoC 컨테이너의 핵심 — `ApplicationContext`, `BeanFactory`, `@Component` 등 포함.

## 12. ApplicationContext — Spring 의 컨테이너

```java
// XML 기반 컨테이너
ApplicationContext context = new GenericXmlApplicationContext("applicationContext.xml");

// Java Config 기반 컨테이너
ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);

// Bean 가져오기
Programmer p = context.getBean("programmer", Programmer.class);
Desktop desktop = context.getBean(Desktop.class);

p.setComputer(desktop);
p.work();
```

`ApplicationContext` 는 **확장된 BeanFactory** — Bean 관리 + 이벤트·국제화·리소스 로딩 등 부가 기능.

---

# Part E. Spring DI 3가지 방식

```
   Spring DI 방식
        |
   +----+------------+
   ▼                 ▼
 명시적 DI         묵시적 DI
   |                 |
   +- XML            +- Java Config + @ComponentScan
   +- Java Config (@Bean 메서드 일일이)
```

## 13. 명시적 DI — XML 방식

**`applicationContext.xml`**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="...">

    <!-- 객체 등록 -->
    <bean id="desktop" class="com.example.Desktop"/>
    <bean id="laptop"  class="com.example.Laptop"/>

    <!-- 의존성 주입 (생성자) -->
    <bean id="programmer" class="com.example.Programmer">
        <constructor-arg ref="desktop"/>
    </bean>

    <!-- 의존성 주입 (setter) -->
    <bean id="programmer2" class="com.example.Programmer">
        <property name="computer" ref="laptop"/>
    </bean>
</beans>
```

**언제**: 레거시 프로젝트 유지보수. 새 프로젝트엔 거의 안 씀.

## 14. 명시적 DI — Java Config 방식

```java
@Configuration
public class AppConfig {

    @Bean
    public Computer desktop() { return new Desktop(); }

    @Bean
    public Computer laptop() { return new Laptop(); }

    @Bean
    public Programmer programmer() {
        return new Programmer(desktop());   // 직접 호출 - Spring 이 알아서 동일 빈 반환
    }
}
```

**`@Configuration` 의 마법**: Spring 이 이 클래스를 CGLIB 프록시로 감싸서, `desktop()` 을 여러 번 호출해도 **항상 같은 빈 반환**.

**언제**: 외부 라이브러리 객체(우리가 어노테이션 못 붙이는) 를 빈으로 등록할 때.

## 15. 묵시적 DI — Annotation + ComponentScan (실무 표준)

```java
@Component
public class Desktop implements Computer { ... }

@Component
public class Programmer {
    private final Computer computer;

    public Programmer(Computer computer) {   // 생성자 주입
        this.computer = computer;
    }
}

@Configuration
@ComponentScan(basePackages = "com.example")
public class AppConfig { }
```

**동작**:
1. `@ComponentScan` 이 지정 패키지를 스캔
2. `@Component`(또는 `@Service`/`@Repository`/`@Controller`) 가 붙은 클래스를 모두 빈으로 등록
3. 생성자 인자에 필요한 빈을 컨테이너가 자동 주입

**`@Component` 의 형제들** (모두 의미적 표시. 동작은 같음):

| 어노테이션 | 의미 |
|--|--|
| `@Component` | 일반 컴포넌트 |
| `@Service` | 비즈니스 로직 |
| `@Repository` | DAO. + 예외 변환 기능 |
| `@Controller` | 웹 컨트롤러 |
| `@RestController` | REST API 컨트롤러 |
| `@Configuration` | 설정 클래스 |

## 16. 주입 방식 3가지 — 생성자/세터/필드

```java
@Component
public class Programmer {

    // 1) 생성자 주입 (권장!)
    private final Computer computer;

    public Programmer(Computer computer) {
        this.computer = computer;
    }
}
```

```java
@Component
public class Programmer {
    private Computer computer;

    // 2) 세터 주입
    @Autowired
    public void setComputer(Computer computer) {
        this.computer = computer;
    }
}
```

```java
@Component
public class Programmer {

    // 3) 필드 주입 (지양)
    @Autowired
    private Computer computer;
}
```

**왜 생성자 주입이 권장인가**:
| 이유 | 설명 |
|--|--|
| **`final` 가능** | 불변 보장 → 멀티스레드 안전 |
| **순환 참조 조기 감지** | 컨테이너 기동 시 실패 (런타임 NPE 아님) |
| **필수 의존성 명확** | 생성자 시그니처가 의존성 목록 |
| **테스트 용이** | Spring 없이 `new Programmer(mock)` 가능 |
| **`@Autowired` 생략 가능** | 단일 생성자면 Spring 이 자동 |

## 17. 의존성 모호성 해결 — `@Qualifier`, `@Primary`

```java
@Component
public class Desktop implements Computer { }

@Component
public class Laptop implements Computer { }

@Component
public class Programmer {
    private final Computer computer;

    public Programmer(Computer computer) { ... }   // ❌ Desktop? Laptop? 모호!
}
```

해결 1: `@Qualifier` 로 명시
```java
public Programmer(@Qualifier("desktop") Computer computer) {
    this.computer = computer;
}
```

해결 2: `@Primary` 로 우선순위
```java
@Component
@Primary                            // 모호할 땐 이걸 우선
public class Desktop implements Computer { }
```

해결 3: 변수명을 빈 이름과 일치
```java
public Programmer(Computer desktop) {   // desktop 이름의 빈 자동 매칭
    this.computer = desktop;
}
```

---

## 18. 코드 깊게 — 풀스택 예제

```java
// === 인터페이스 ===
public interface Computer { void boot(); }

// === 구현체 ===
@Component
@Primary                                            // 모호할 땐 우선
public class Desktop implements Computer {
    public void boot() { System.out.println("Desktop boot"); }
}

@Component
public class Laptop implements Computer {
    public void boot() { System.out.println("Laptop boot"); }
}

// === 의존하는 쪽 ===
@Component
@RequiredArgsConstructor                            // Lombok - final 생성자 자동
public class Programmer {
    private final Computer computer;

    public void work() {
        computer.boot();
        System.out.println("Working...");
    }
}

// === 설정 ===
@Configuration
@ComponentScan(basePackages = "com.example")
public class AppConfig { }

// === 실행 ===
public class Main {
    public static void main(String[] args) {
        ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
        Programmer p = ctx.getBean(Programmer.class);
        p.work();
    }
}
```

**출력**:
```
Desktop boot      ← @Primary 덕분에 Desktop 선택
Working...
```

`Laptop` 으로 바꾸려면? `@Primary` 위치만 옮기면 끝. `Programmer` 코드 수정 0.

---

## 19. 실전 패턴 / 자주 빠지는 함정

### DI 개념
- ❌ 필드를 `private Computer c = new Desktop();` 으로 초기화 ✅ 외부 주입 (DI)
- ❌ "DI = 그냥 의존성 받기" ✅ "객체 생성 책임의 분리 + 테스트 가능성"

### 컨테이너
- ❌ `@Retention(CLASS)` 로 어노테이션 선언 → 리플렉션에서 안 보임 ✅ `RUNTIME`
- ❌ `@ComponentScan` 패키지를 안 지정 → 같은 패키지 + 하위만 스캔 ✅ 명시적 `basePackages`
- ❌ XML 과 어노테이션을 마구 섞음 ✅ 새 프로젝트는 어노테이션 중심

### 주입 방식
- ❌ 필드 주입 (`@Autowired private Computer computer;`) ✅ 생성자 주입
- ❌ `final` 안 붙인 생성자 주입 ✅ `final` + `@RequiredArgsConstructor` (Lombok)
- ❌ 순환 참조 (`A → B → A`) → 기동 실패 ✅ 설계 재검토 (정말 둘 다 필요한가?)

### 모호성
- ❌ 같은 인터페이스 구현체 2개 + `@Qualifier`/`@Primary` 없음 → `NoUniqueBeanDefinitionException`
  ✅ 둘 중 하나 명시
- ❌ 빈 이름과 타입 모두 안 맞을 때 `@Autowired(required = false)` 로 회피 ✅ 진짜 필요 없으면 의존성 제거

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| `NoSuchBeanDefinitionException` | 빈으로 등록 안 됨 | `@Component` 부착 + `@ComponentScan` 범위 확인 |
| `NoUniqueBeanDefinitionException` | 같은 타입 빈 2개 이상 | `@Qualifier` 또는 `@Primary` |
| `BeanCurrentlyInCreationException` | 순환 참조 | 설계 재검토 또는 `@Lazy` (응급) |
| `@Autowired` 가 `null` | 컨테이너 밖에서 `new` 로 객체 생성 | 컨테이너 통해 `getBean` |
| Java Config 의 `@Bean` 메서드를 직접 호출했더니 새 인스턴스 | `@Configuration` 안 붙임 → 프록시 없음 | `@Configuration` 추가 |
| `private` 생성자에 `@Autowired` 안 먹힘 | 접근 제한자 | `public` 으로 |

---

## 20. 자가점검

1. DI 와 IoC 의 관계를 한 줄로?
2. IoC 컨테이너가 객체를 만드는 데 필요한 두 가지 무기는?
3. `@Retention(RUNTIME)` 이 컨테이너 입장에서 왜 필수인가?
4. 명시적 DI 와 묵시적 DI 의 차이? 실무는 어느 쪽?
5. 생성자 주입이 필드 주입보다 권장되는 5가지 이유 중 3가지만?
6. `@Qualifier` 와 `@Primary` 의 차이? 둘 다 있으면 어느 게 이김?
7. `@Configuration` 없이 그냥 클래스에 `@Bean` 만 붙이면 어떻게 동작하나?

<details><summary>풀이</summary>

1. **DI ⊂ IoC**. DI 는 IoC 를 실현하는 구체적 기법. IoC 는 더 넓은 사상(제어 역전).
2. **어노테이션 (메타데이터)** + **리플렉션 (런타임에 정보 읽기)**. 둘이 있어야 컨테이너가 "어떤 객체를 만들지" 알 수 있음.
3. 어노테이션은 기본적으로 `RetentionPolicy.CLASS` — .class 까지만 유지. 컨테이너가 런타임에 리플렉션으로 읽으려면 `RUNTIME` 으로 유지해야 함.
4. **명시적**: XML 또는 Java Config 의 `@Bean` 메서드로 일일이 등록. **묵시적**: `@Component` + `@ComponentScan` 으로 자동 탐색. **실무는 묵시적**. 외부 라이브러리 객체만 명시적.
5. (1) `final` 가능 → 불변 (2) 순환 참조 기동 시 감지 (3) 필수 의존성 시그니처로 명확 (4) Spring 없이 테스트 가능 (5) `@Autowired` 생략 가능. (앞 3개로 충분.)
6. **`@Qualifier`**: 주입받는 쪽에서 구체적 빈 이름 지정. **`@Primary`**: 빈 정의 쪽에서 우선순위 부여. 둘 다 있으면 **`@Qualifier` 가 이김** (더 명시적).
7. 빈으로 등록은 되지만 `@Bean` 메서드끼리 호출 시 **매번 새 객체 생성** (CGLIB 프록시 미적용). `@Configuration` 있으면 동일 빈 반환 보장.

</details>

---

## 21. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.3 표지·TOC·학습목표 | 들어가기 전에 |
| p.4 ~ p.9 DI 개념·등장 배경 | §1 ~ §3 (Part A) |
| p.10 ~ p.12 IoC Container 역할 | §4, §5 (Part B) |
| p.13 ~ p.18 어노테이션·리플렉션·미니 컨테이너 | §6 ~ §10 (Part C) |
| p.19 ~ p.27 Spring Container 빌드·ApplicationContext | §11, §12 (Part D) |
| p.28 ~ p.30 Spring DI 개요 | §13 (Part E) |
| p.31 ~ p.33 명시적 DI (XML·Java Config) | §13, §14 |
| p.34 ~ p.36 묵시적 DI (Annotation·ComponentScan) | §15 ~ §17 |
| p.37 마무리 | (생략) |

_37p 슬라이드 모두 커버._
