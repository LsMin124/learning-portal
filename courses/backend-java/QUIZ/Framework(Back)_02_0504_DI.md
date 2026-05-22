# Spring DI — 퀴즈

> 16문항. 개념·적용·디버그·면접. 5부(DI 개념·IoC 컨테이너·미니 구현·Spring Container·명시적/묵시적 DI) 골고루.

---

### Q1. (개념) DI 가 없으면 발생하는 문제 4가지?

<details><summary>정답</summary>

1. **강한 결합** — 구현 클래스에 코드가 묶여 교체 시 코드 수정
2. **테스트 불가** — Mock 주입 못 함, 진짜 구현 필요
3. **의존성 폭발** — A→B→C 의존 사슬을 모두 직접 생성해야
4. **단일 책임 위반** — 한 클래스가 "본 업무 + 의존성 생성" 2가지 책임

</details>

### Q2. (개념) DI 와 IoC 의 관계는?

<details><summary>정답</summary>

**DI ⊂ IoC**. DI 는 IoC 를 실현하는 구체적 기법. IoC 는 더 넓은 사상(객체 생성·생명주기·연결의 주도권이 프레임워크로 넘어감).

</details>

### Q3. (개념) IoC 컨테이너의 2가지 핵심 역할?

<details><summary>정답</summary>

1. **객체 관리 자동화** — 생성·초기화·사용·소멸까지 라이프사이클 전담
2. **의존성 조립** — 메타데이터·어노테이션 기반으로 필요한 객체를 스스로 찾아 연결

</details>

### Q4. (적용) `@Retention(RetentionPolicy.CLASS)` 로 어노테이션을 만들었더니 컨테이너가 못 읽음. 원인?

<details><summary>정답</summary>

`CLASS` 는 .class 파일까지만 유지. **JVM 실행 중엔 사라짐** → 리플렉션의 `isAnnotationPresent` 가 false. 컨테이너가 런타임에 어노테이션을 읽으려면 반드시 **`RUNTIME`**.

</details>

### Q5. (적용) 다음 미니 컨테이너의 빈 칸을 채우시오.

```java
public class MyContainer {
    private final Map<String, Object> beanMap = new HashMap<>();

    public MyContainer(Class<?> configClazz) throws Exception {
        Object configInstance = ___;        // (a)
        for (Method method : ___) {         // (b)
            if (method.___) {               // (c) @MyBean 부착 확인
                Object bean = method.invoke(configInstance);
                beanMap.put(method.getName(), bean);
            }
        }
    }
}
```

<details><summary>정답</summary>

```java
(a) configClazz.getDeclaredConstructor().newInstance()
(b) configClazz.getDeclaredMethods()
(c) isAnnotationPresent(MyBean.class)
```

리플렉션으로 (a) 설정 클래스 인스턴스 생성, (b) 메서드 순회, (c) 마커 어노테이션 검사.

</details>

### Q6. (개념) `BeanFactory` 와 `ApplicationContext` 의 차이?

<details><summary>정답</summary>

`ApplicationContext` 는 `BeanFactory` 의 **확장판**. Bean 관리 기능에 더해:
- 이벤트 발행/구독 (`ApplicationEvent`)
- 국제화 (`MessageSource`)
- 리소스 로딩 (`ResourceLoader`)
- 환경 설정 (`Environment`)

실무는 항상 `ApplicationContext` 를 사용.

</details>

### Q7. (적용) Spring Container 를 Java Config 로 빌드하는 코드?

<details><summary>정답</summary>

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
Programmer p = ctx.getBean(Programmer.class);
```

XML 기반은 `GenericXmlApplicationContext("applicationContext.xml")`.

</details>

### Q8. (개념) 명시적 DI 와 묵시적 DI 의 차이? 실무 표준은?

<details><summary>정답</summary>

- **명시적 DI**: XML `<bean>` 태그 또는 Java Config 의 `@Bean` 메서드로 **하나씩 등록**
- **묵시적 DI**: `@Component` + `@ComponentScan` 으로 **자동 탐색·등록**

**실무 표준은 묵시적**. 명시적은 외부 라이브러리 객체(어노테이션 못 붙이는) 만 한정.

</details>

### Q9. (개념) `@Component` 의 형제 5가지와 각 의미?

<details><summary>정답</summary>

| 어노테이션 | 의미 |
|--|--|
| `@Component` | 일반 컴포넌트 |
| `@Service` | 비즈니스 로직 계층 |
| `@Repository` | DAO 계층 + 예외 변환 |
| `@Controller` | 웹 컨트롤러 |
| `@RestController` | REST API 컨트롤러 (= Controller + ResponseBody) |
| `@Configuration` | 설정 클래스 |

모두 빈 등록이라는 동작은 같음. 의미적 분류용.

</details>

### Q10. (적용) 다음 클래스를 생성자 주입으로 리팩터링하시오. (Lombok 포함)

```java
@Service
public class OrderService {
    @Autowired private PaymentClient pay;
    @Autowired private EmailSender mail;
}
```

<details><summary>정답</summary>

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final PaymentClient pay;
    private final EmailSender mail;
}
```

`@RequiredArgsConstructor` 가 `final` 필드만 받는 생성자를 자동 생성. Spring 4.3+ 는 단일 생성자면 `@Autowired` 자동.

</details>

### Q11. (개념) 생성자 주입이 필드 주입보다 권장되는 이유 3가지?

<details><summary>정답</summary>

1. **`final` 가능** — 불변 보장 → 멀티스레드 안전
2. **순환 참조 조기 감지** — 컨테이너 기동 시 실패, 런타임 NPE 아님
3. **테스트 용이** — Spring 없이 `new OrderService(mock1, mock2)` 가능

추가: 필수 의존성이 시그니처에 명확, `@Autowired` 생략 가능.

</details>

### Q12. (디버그) 다음 코드가 `NoUniqueBeanDefinitionException` 을 던지는 이유와 3가지 해결?

```java
@Component public class Desktop implements Computer { }
@Component public class Laptop implements Computer { }

@Component
public class Programmer {
    public Programmer(Computer computer) { }
}
```

<details><summary>정답</summary>

`Computer` 타입 빈이 2개 → 어떤 걸 주입할지 모호.

**해결 3가지**:

1. **`@Qualifier`**: `Programmer(@Qualifier("desktop") Computer c)`
2. **`@Primary`**: `@Component @Primary class Desktop` (한쪽에 우선순위 부여)
3. **변수명을 빈 이름과 일치**: `Programmer(Computer desktop)` — Spring 이 이름 기준 매칭

</details>

### Q13. (디버그) `@Configuration` 없이 `@Bean` 만 붙인 클래스의 메서드를 직접 호출하면?

```java
public class Config {
    @Bean public Foo foo() { return new Foo(); }
    @Bean public Bar bar() { return new Bar(foo()); }   // foo() 직접 호출
}
```

<details><summary>정답</summary>

`foo()` 가 매번 **새 인스턴스** 를 반환. Bean 으로 등록된 foo 와 bar 안의 foo 가 **다른 객체**.

`@Configuration` 이 있으면 Spring 이 CGLIB 프록시로 감싸서 `foo()` 호출 시 이미 등록된 빈을 반환 → 싱글톤 보장.

해결: `Config` 클래스에 `@Configuration` 추가.

</details>

### Q14. (디버그) `@Autowired` 가 `null`. 원인 후보 4가지?

<details><summary>정답</summary>

1. **컨테이너 밖에서 `new` 로 객체 생성** — `@Autowired` 작동 안 함
2. **컴포넌트 스캔 범위 밖** — `@ComponentScan` 의 `basePackages` 확인
3. **`@Component` 류 어노테이션 누락** — 빈 등록 안 됨
4. **생성자 주입을 안 하고 `@PostConstruct` 이전에 필드 접근** — 주입 타이밍 문제

</details>

### Q15. (면접) "`BeanCurrentlyInCreationException` 이 뭐고, 어떻게 해결하나요?"

<details><summary>정답</summary>

**순환 참조** — A 빈이 B 를 필요로 하고, B 가 다시 A 를 필요로 할 때. 생성자 주입이면 컨테이너 기동 시점에 감지 → 빌드 실패.

**해결 (우선순위 순)**:
1. **설계 재검토** — 정말 양방향이 필요한가? 한쪽으로 단방향화 가능?
2. **공통 의존성 추출** — 두 빈이 공통으로 의존하는 제3 클래스로 책임 이동
3. **`@Lazy`** — 한쪽을 지연 주입 (응급조치, 근본 원인 아님)
4. **세터 주입으로 회피** — 권장 안 함

순환 참조는 거의 항상 설계 잘못의 신호.

</details>

### Q16. (면접) "DI 의 본질이 뭔가요? Spring 없이도 DI 라고 부를 수 있는 코드 예시는?"

<details><summary>정답</summary>

**DI 의 본질은 "객체 생성 책임의 분리"**. 클래스가 자기 의존성을 직접 만들지 않고 외부에서 받는 것. Spring 은 그걸 자동화한 도구일 뿐, **DI 자체는 자바 OOP 만으로도 가능**.

```java
// Spring 없는 순수 DI
public class Programmer {
    private final Computer computer;
    public Programmer(Computer computer) { this.computer = computer; }
}

public class Main {
    public static void main(String[] args) {
        Computer c = new Desktop();          // 외부에서 결정
        Programmer p = new Programmer(c);    // 주입
        p.work();
    }
}
```

이게 DI. Spring 컨테이너는 이걸 어노테이션 + 리플렉션으로 자동화한 도구.

</details>
