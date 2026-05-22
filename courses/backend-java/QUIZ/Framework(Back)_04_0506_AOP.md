# Spring AOP — 퀴즈

> 14문항. 개념·적용·디버그·면접. 3부(관점 지향·Proxy·Spring AOP) 골고루.

---

### Q1. (개념) AOP 가 풀려는 본질적 문제는?

<details><summary>정답</summary>

여러 메서드·클래스에 흩어진 **횡단 관심사(Cross-Cutting Concern, 로깅·트랜잭션·보안·캐시 등)** 의 코드 중복과 핵심 로직 가려짐 문제. OOP 의 상속·인터페이스로는 깔끔히 분리할 수 없는 영역.

</details>

### Q2. (개념) Aspect, Pointcut, Advice 의 관계?

<details><summary>정답</summary>

- **Aspect**: 횡단 관심사를 모듈화한 단위 (`LoggingAspect` 클래스)
- **Pointcut**: 그 Aspect 가 적용될 위치(Join Point) 선언 (`execution(* service.*.*(..))`)
- **Advice**: 그 위치에서 실행되는 동작 + 시점 (`@Before` 메서드)

한 Aspect 안에 여러 Pointcut + 여러 Advice 가 들어감.

</details>

### Q3. (개념) Advice 5가지 시점과 각 의미?

<details><summary>정답</summary>

| Advice | 시점 |
|--|--|
| `@Before` | 메서드 실행 **전** |
| `@After` | 메서드 실행 **후** (성공·실패 모두) |
| `@AfterReturning` | **정상 반환** 후 |
| `@AfterThrowing` | **예외 발생** 시 |
| `@Around` | 전후 모두 + 실행 자체 제어 (`proceed()` 호출) |

`@Around` 만이 메서드 실행을 막거나 반환값을 바꿀 수 있음.

</details>

### Q4. (적용) 모든 Service 패키지의 메서드에 적용되는 Pointcut 표현식?

<details><summary>정답</summary>

```java
@Pointcut("execution(* com.example.service.*.*(..))")
public void serviceLayer() {}
```

또는 어노테이션 기반:
```java
@Pointcut("@within(org.springframework.stereotype.Service)")
public void serviceLayer() {}
```

전자는 패키지 기반, 후자는 어노테이션 기반.

</details>

### Q5. (적용) `@Around` 로 메서드 실행 시간을 측정하는 Aspect?

<details><summary>정답</summary>

```java
@Aspect @Component @Slf4j
public class TimingAspect {

    @Around("execution(* com.example.service.*.*(..))")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            return pjp.proceed();
        } finally {
            log.info("{} took {} ms",
                pjp.getSignature().toShortString(),
                System.currentTimeMillis() - start);
        }
    }
}
```

`pjp.proceed()` 가 실제 메서드 실행. try/finally 로 예외 발생 시에도 측정.

</details>

### Q6. (개념) Spring AOP 의 Proxy 방식 2가지와 각 적용 조건?

<details><summary>정답</summary>

| 방식 | 조건 |
|--|--|
| **JDK Dynamic Proxy** | Target 클래스가 인터페이스 구현 — 인터페이스 기반 Proxy |
| **CGLIB** | 인터페이스 없어도 OK — Target 클래스를 상속해서 Proxy 생성 |

**Spring Boot 2.x+ 부터 CGLIB 가 기본**. 더 빠른 메서드 디스패치 + 인터페이스 강제 안 함.

</details>

### Q7. (디버그) 다음 코드의 `@Transactional` 이 적용되지 않는 이유와 해결?

```java
@Service
public class MemberService {
    @Transactional
    public void insert(Member m) { ... }

    public void insertAll(List<Member> ms) {
        for (Member m : ms) this.insert(m);   // ❌
    }
}
```

<details><summary>정답</summary>

**Self-Invocation**: `this.insert(m)` 는 Proxy 가 아닌 Target 메서드를 직접 호출 → Advice 가 끼어들 틈 없음 → `@Transactional` 무시.

**해결**:
1. **메서드 분리** (가장 안전): `insertAll` 을 다른 빈으로
2. **self 주입**: `@Autowired @Lazy private MemberService self;` → `self.insert(m)` 호출
3. **ApplicationContext 에서 빈 가져오기**: `ctx.getBean(MemberService.class).insert(m)`

</details>

### Q8. (디버그) `@Transactional private void` 이 적용되지 않는 이유?

<details><summary>정답</summary>

**Proxy 가 외부에서 호출하는 메서드만 가로챌 수 있기 때문**. private 메서드는 클래스 외부에서 호출 불가 → Proxy 가 가로챌 기회 자체가 없음. CGLIB 는 상속 기반인데 private 메서드는 상속·오버라이드 불가.

해결: **public 으로 변경** 또는 다른 클래스로 메서드 추출.

</details>

### Q9. (개념) JoinPoint 와 ProceedingJoinPoint 의 차이?

<details><summary>정답</summary>

- **JoinPoint**: 일반 advice (`@Before`, `@After` 등) 의 인자. 현재 메서드 시그니처·인자·Target 정보 조회만 가능.
- **ProceedingJoinPoint**: **`@Around` 전용**. `JoinPoint` 의 모든 기능 + **`proceed()` 메서드**로 실제 메서드 실행을 제어 가능.

`@Around` 만이 메서드 실행 자체를 막거나 결과를 조작할 수 있는 이유는 `ProceedingJoinPoint.proceed()` 때문.

</details>

### Q10. (적용) `@MyAuditLog` 어노테이션이 붙은 메서드에만 적용되는 Pointcut 과 Advice?

<details><summary>정답</summary>

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface MyAuditLog { }

@Aspect @Component
public class AuditAspect {

    @Around("@annotation(com.example.MyAuditLog)")
    public Object audit(ProceedingJoinPoint pjp) throws Throwable {
        String user = SecurityContextHolder.getContext()
                       .getAuthentication().getName();
        log.info("AUDIT: {} called {}", user, pjp.getSignature());
        return pjp.proceed();
    }
}
```

`@annotation(...)` Pointcut 으로 특정 어노테이션이 붙은 메서드만 매칭.

</details>

### Q11. (적용) `final` 클래스에 `@Transactional` 을 붙였더니 동작 안 함. 원인?

<details><summary>정답</summary>

**CGLIB 가 `final` 클래스를 상속할 수 없음**. Spring Boot 2.x+ 는 기본이 CGLIB 인데, `final` 클래스는 상속 불가 → Proxy 생성 실패.

**해결**:
- `final` 키워드 제거
- 또는 인터페이스 도입 + JDK Dynamic Proxy 사용 (`spring.aop.proxy-target-class=false`)

</details>

### Q12. (면접) "AOP 를 안 쓰고 직접 같은 기능을 만들면 어떤 단점이 있나요?"

<details><summary>정답</summary>

1. **코드 중복** — 모든 메서드에 같은 부가 로직 반복
2. **수정 비용 폭증** — 정책 변경 시 100곳 손봐야
3. **핵심 로직 가려짐** — 5줄 비즈니스 + 20줄 부가 기능
4. **잊혀짐** — 새로 추가한 메서드에 부가 로직 누락 → 버그
5. **테스트 어려움** — 모든 메서드가 부가 로직과 결합

AOP 는 이걸 **선언적 모듈화** 로 해결. `@Transactional` 한 줄로 모든 메서드에 자동 적용.

</details>

### Q13. (면접) "`@Around` advice 가 다른 advice 보다 강력한 이유는?"

<details><summary>정답</summary>

`@Around` 만이 `ProceedingJoinPoint.proceed()` 를 호출하므로 **실행 자체를 제어** 할 수 있다.

가능한 동작:
- 실행 자체를 막기 (`return null;` 만 하면 메서드 호출 안 됨)
- 인자 변경 후 실행 (`pjp.proceed(newArgs)`)
- 반환값 변경 (`Object result = pjp.proceed(); return result.modify();`)
- 재시도 (`for (int i=0; i<3; i++) try { return pjp.proceed(); } catch(...)`)
- 예외 변환 (`try { return pjp.proceed(); } catch(SQLException e) { throw new MyException(e); }`)

다른 advice 는 **시점만** 잡을 뿐 실행 제어 못함.

</details>

### Q14. (면접) "`@Transactional` 어노테이션이 안 먹히는 경우 5가지를 나열하시오."

<details><summary>정답</summary>

1. **Self-Invocation** — 같은 클래스 안에서 다른 메서드 호출
2. **private 메서드** — Proxy 가 가로챌 수 없음
3. **`final` 클래스/메서드** — CGLIB 상속 불가
4. **컨테이너 밖에서 `new` 로 생성한 객체** — Proxy 가 안 만들어짐
5. **`@Transactional` 이 트랜잭션 매니저를 못 찾음** — DataSource·TransactionManager 빈 누락

추가: 클래스가 `@Component`/`@Service` 등으로 빈 등록 안 되어 있으면 당연히 Proxy 안 생김.

</details>
