# Spring AOP — 관점 지향 프로그래밍 · Proxy · Spring AOP

> **이 강의는 무엇인가**: 객체지향(OOP) 만으로는 풀기 힘든 **횡단 관심사(Cross-Cutting Concern, 로깅·트랜잭션·보안)** 를 분리하는 패러다임 **AOP**. 그리고 Spring 이 어떻게 **Proxy** 기반으로 AOP 를 구현하는지의 메커니즘.
> **왜 배우는가**: `@Transactional` 한 줄로 트랜잭션이 도는 것, `@PreAuthorize` 한 줄로 권한 검사가 되는 것 — 모두 AOP 의 마법이다. 동작 원리를 모르면 트러블슈팅이 막힌다 (특히 self-invocation 함정).

---

## 들어가기 전에

- **선수**: Spring DI/IoC, 인터페이스·다형성, 디자인 패턴 기초 (Proxy 패턴 이름은 들어봐야).
- **마인드셋**: "비즈니스 로직 = 핵심 관심사" 와 "공통 부가 기능 = 횡단 관심사" 의 분리 의식.

---

# Part A. 관점 지향 프로그래밍

## 1. OOP 만으로 풀리지 않는 문제

```java
public void insert(Member m) {
    // === 부가 기능: 로깅 ===
    long start = System.currentTimeMillis();
    log.info("insert called args={}", m);

    // === 부가 기능: 보안 ===
    if (!auth.hasRole("ADMIN")) throw new AccessDeniedException();

    // === 핵심 비즈니스 로직 ===
    memberDao.insert(m);

    // === 부가 기능: 트랜잭션 commit ===
    tx.commit();

    // === 부가 기능: 로깅 ===
    log.info("insert done in {} ms", System.currentTimeMillis() - start);
}

public void update(Member m) {
    // 같은 부가 기능 4종이 또 반복...
}

public void delete(int id) {
    // 또 반복...
}
```

**문제 3가지**:

| 문제 | 영향 |
|--|--|
| **코드 중복 (copy & paste)** | 모든 메서드에 같은 부가 로직 반복 — 한 곳 바꾸면 100곳 바꿔야 |
| **핵심 로직 가려짐** | 5줄짜리 비즈니스 로직이 20줄짜리 부가 기능에 묻힘 |
| **수정 비용 폭증** | 로그 포맷 바꾸려면 모든 메서드 손봐야 |

→ **횡단 관심사(여러 메서드를 가로지르는 공통 기능)** 는 OOP 의 상속·인터페이스로는 깔끔히 분리 불가.

## 2. AOP 의 아이디어

```
[Before AOP - OOP 만으로]    부가 기능이 모든 메서드에 중복

  insert()                      ← 25줄
    로그
    보안
    핵심 로직 (5줄)
    트랜잭션
    로그

  update()                      ← 같은 부가 기능 또 반복!
    로그
    보안
    핵심 로직 (5줄)
    트랜잭션
    로그

  delete()  ... 모든 메서드에 같은 패턴 ...
```

```
[After AOP]   비즈니스 로직만 남고, Aspect 가 자동 적용

  insert() / update() / delete()
    핵심 로직만 (5줄)
            ▲
            | 자동 적용 (Proxy 기반)
  ------------------------------------
    LoggingAspect    - 로그
    SecurityAspect   - 보안
    TxAspect         - 트랜잭션
  ------------------------------------
  (한 곳에서 모든 메서드에 적용 - 비즈니스 코드는 깨끗)
```

**AOP 의 본질**: 횡단 관심사를 **별도 모듈(Aspect)** 로 추출 → **언제·어디에 적용할지**를 선언적으로 명시 → 비즈니스 코드는 깨끗.

## 3. AOP 핵심 용어 5종

| 용어 | 의미 |
|--|--|
| **Aspect** | 횡단 관심사를 모듈화한 단위 (`LoggingAspect`, `TxAspect`) |
| **Join Point** | Aspect 가 적용될 수 있는 지점 (메서드 호출, 필드 접근 등) |
| **Pointcut** | 실제 Aspect 가 적용될 Join Point 의 **선언** (예: "모든 Service 의 모든 메서드") |
| **Advice** | Aspect 가 실행하는 **동작** + **시점** (Before/After/Around) |
| **Weaving** | Aspect 와 비즈니스 코드를 엮는 과정 (컴파일·로드·런타임 시) |

```
                    Spring 의 weaving 은 런타임에 일어남 (Proxy 기반)
                    ---------------------------------------------

   클라이언트
       |
       ▼
   [ Proxy 객체 ]
       |  (Advice 적용 시점에 따라 호출 직전/직후/주변)
       |     • Before - 메서드 실행 전
       |     • After  - 메서드 실행 후 (성공·실패 모두)
       |     • AfterReturning - 정상 반환 후
       |     • AfterThrowing  - 예외 발생 시
       |     • Around - 직전·직후·반환값 조작 가능 (가장 강력)
       ▼
   [ 실제 빈 (Target) ]
```

## 4. Advice 5가지 시점

```java
@Aspect
@Component
public class LoggingAspect {

    // 1) Before - 메서드 실행 전
    @Before("execution(* com.example.service.*.*(..))")
    public void before(JoinPoint jp) {
        log.info("Before: {}", jp.getSignature());
    }

    // 2) After - 정상·예외 모두 실행 후
    @After("execution(* com.example.service.*.*(..))")
    public void after(JoinPoint jp) { ... }

    // 3) AfterReturning - 정상 반환 후
    @AfterReturning(value = "execution(* com.example.service.*.*(..))",
                    returning = "result")
    public void afterReturning(JoinPoint jp, Object result) { ... }

    // 4) AfterThrowing - 예외 발생 시
    @AfterThrowing(value = "execution(* com.example.service.*.*(..))",
                   throwing = "ex")
    public void afterThrowing(JoinPoint jp, Exception ex) { ... }

    // 5) Around - 전·후·반환값 모두 제어 (가장 강력, 가장 위험)
    @Around("execution(* com.example.service.*.*(..))")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = pjp.proceed();           // ← 실제 메서드 실행
        log.info("took {} ms", System.currentTimeMillis() - start);
        return result;
    }
}
```

`Around` 만이 `proceed()` 를 직접 호출하므로 **실행 자체를 막거나, 반환값을 바꾸거나, 재시도** 가 가능.

---

# Part B. Proxy — Spring AOP 의 동작 원리

## 5. Proxy 패턴 — 대리인을 두는 패턴

```
       클라이언트
           |
           ▼
       [ Proxy ]   ←- 본인 행세하며 부가 작업 수행
           |
           ▼
       [ Target ]  ←- 진짜 작업자
```

일상 비유:
- **공인중개사** — 집주인(Target) 을 대리해서 매수자(Client) 와 응대. 도장 찍기·계약서 검토 등 부가 작업
- **연예인 매니저** — 연예인(Target) 의 스케줄·미디어 응대를 대리

## 6. Spring 의 Proxy — CGLIB 와 JDK Dynamic Proxy

```
                       Target 클래스에 인터페이스 있나?
                                |
                  +-------------+-------------+
                 Yes                          No
                  |                            |
                  ▼                            ▼
         JDK Dynamic Proxy              CGLIB Proxy
         인터페이스 기반                 클래스 상속 기반
         (Spring 5 까지 기본)            (Spring Boot 2.x+ 기본)
```

**Spring Boot 2.x 이후 기본은 CGLIB**:
- 인터페이스 없어도 Proxy 생성 가능 (Target 을 상속)
- 더 빠른 호출 (인터페이스 vs 클래스의 메서드 디스패치 차이)

**CGLIB 의 동작**: 컨테이너 기동 시 Target 클래스를 상속한 새 클래스를 동적 생성 → 각 메서드를 오버라이드해서 Advice 호출을 끼워넣음.

```java
// 우리가 작성한 코드
@Service
public class MemberService {
    public void insert(Member m) { ... }
}

// Spring 이 런타임에 생성하는 Proxy (대략 이런 모습)
public class MemberService$$EnhancerByCGLIB extends MemberService {
    @Override
    public void insert(Member m) {
        // Advice 호출
        logBefore();
        try {
            super.insert(m);     // ← 원래 메서드
            logAfterReturning();
        } catch (Exception e) {
            logAfterThrowing();
            throw e;
        }
        logAfter();
    }
}
```

컨테이너는 우리가 `@Autowired MemberService` 로 받으면 **Proxy 객체를 주입**한다 → 모든 호출이 Proxy 를 거침.

## 7. Self-Invocation 함정

```java
@Service
public class MemberService {

    @Transactional
    public void insert(Member m) { ... }

    public void insertAll(List<Member> ms) {
        for (Member m : ms) {
            this.insert(m);    // ❌ self 호출 - @Transactional 무시됨!
        }
    }
}
```

**왜?** `this.insert(m)` 는 Proxy 가 아니라 Target 의 메서드를 직접 호출. Advice 가 끼어들 틈이 없음.

**해결**:
```java
// 1) 분리 - 다른 빈으로 추출
@Service
public class MemberServiceImpl {
    @Autowired
    private MemberService self;        // 자기 자신을 Proxy 로 주입

    public void insertAll(List<Member> ms) {
        for (Member m : ms) self.insert(m);   // Proxy 거침
    }
}

// 2) 또는 ApplicationContext 에서 직접 가져오기
ctx.getBean(MemberService.class).insert(m);
```

근본 해결은 **메서드를 다른 클래스로 분리** 하는 게 가장 안전.

---

# Part C. Spring AOP 사용

## 8. 의존성 추가

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

`spring-boot-starter-aop` 가 `spring-aop` + `aspectjweaver` 를 가져옴. AspectJ 의 어노테이션 문법을 Spring AOP 가 사용.

## 9. Pointcut 표현식 (`execution` 패턴)

```
execution([modifier]  return-type  package.Class.method(params))

예시:
execution(public * com.example.service.*.*(..))
   - public                - 접근 제한자
   - *                     - 모든 반환 타입
   - com.example.service.* - service 패키지의 모든 클래스
   - *(..)                 - 모든 메서드, 모든 인자
```

**자주 쓰는 패턴**:

| 표현식 | 의미 |
|--|--|
| `execution(* *(..))` | 모든 메서드 |
| `execution(* *.service.*.*(..))` | 모든 패키지의 service 안 모든 메서드 |
| `execution(* com.example..*(..))` | com.example 하위 모든 메서드 (`..` 다중 패키지) |
| `execution(* save*(..))` | save 로 시작하는 메서드 |
| `@annotation(com.example.MyAnno)` | `@MyAnno` 가 붙은 메서드 |
| `@within(org.springframework.stereotype.Service)` | `@Service` 클래스의 모든 메서드 |
| `bean(memberService)` | 특정 빈 이름 |

## 10. 어노테이션 방식 AOP 완성 예제

```java
@Aspect
@Component
public class LoggingAspect {

    private static final Logger log = LoggerFactory.getLogger(LoggingAspect.class);

    // 재사용 가능한 Pointcut 정의
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceLayer() {}

    @Pointcut("@annotation(com.example.LogExecution)")
    public void logExecutionAnno() {}

    // Around - 가장 자주 쓰는 advice
    @Around("serviceLayer() || logExecutionAnno()")
    public Object logExecutionTime(ProceedingJoinPoint pjp) throws Throwable {
        String name = pjp.getSignature().toShortString();
        long start = System.currentTimeMillis();
        try {
            Object result = pjp.proceed();
            log.info("[{}] took {} ms", name, System.currentTimeMillis() - start);
            return result;
        } catch (Throwable t) {
            log.error("[{}] failed: {}", name, t.getMessage());
            throw t;
        }
    }
}
```

`@Aspect` + `@Component` 둘 다 필요 — `@Aspect` 는 AOP 식별, `@Component` 는 빈 등록.

## 11. Spring 이 제공하는 AOP 활용 예 — 어노테이션만으로 끝

```java
// 트랜잭션
@Transactional
public void transfer(Account from, Account to, int amount) { ... }

// 보안 (Spring Security)
@PreAuthorize("hasRole('ADMIN')")
public void deleteAll() { ... }

// 캐시
@Cacheable("users")
public User findById(long id) { ... }

// 비동기 실행
@Async
public void sendEmail(String to, String msg) { ... }

// 재시도
@Retryable(maxAttempts = 3)
public Payment charge(Order order) { ... }
```

이 어노테이션들이 다 AOP. 같은 패턴이라 우리도 직접 만들 수 있다.

---

## 12. 코드 깊게 — 실시간 메서드 실행 시간 측정 Aspect

```java
// === 어노테이션 ===
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LogExecutionTime { }

// === Aspect ===
@Aspect
@Component
@Slf4j
public class ExecutionTimeAspect {

    @Around("@annotation(com.example.LogExecutionTime)")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        String method = pjp.getSignature().toShortString();
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            log.info("[PERF] {} → {} ms", method, elapsed);
        }
    }
}

// === 사용 ===
@Service
public class ReportService {

    @LogExecutionTime
    public Report generate(int year) {
        // ... 무거운 작업
        return new Report();
    }
}

// === 로그 출력 ===
// [PERF] ReportService.generate(..) → 1234 ms
```

`@LogExecutionTime` 한 줄로 어떤 메서드든 실행 시간 측정. 비즈니스 코드는 1 줄도 안 늘어남.

---

## 13. 실전 패턴 / 자주 빠지는 함정

### 개념
- ❌ AOP = 로깅만 하는 도구로 이해 ✅ 트랜잭션·보안·캐시·재시도·모니터링 등 모든 횡단 관심사
- ❌ AOP 가 OOP 를 대체 ✅ AOP 는 OOP 의 **보완** — OOP 가 풀기 어려운 영역만

### Pointcut
- ❌ `execution(*)` 같이 너무 광범위한 표현 → 모든 호출에 적용되어 성능 저하
  ✅ 패키지·어노테이션으로 구체화
- ❌ Pointcut 표현식 오타 → 조용히 안 적용
  ✅ `@Pointcut` 으로 추출 + 재사용 + 컴파일 단계 검증

### Proxy
- ❌ **self-invocation** (`this.method()`) → Proxy 우회 → Advice 무시
  ✅ 메서드를 다른 빈으로 분리
- ❌ private 메서드에 `@Transactional` → 동작 안 함
  ✅ public 메서드만 Proxy 가 가로챌 수 있음
- ❌ final 클래스/메서드 → CGLIB 상속 불가
  ✅ final 제거 또는 인터페이스 기반 JDK Proxy 활용
- ❌ Proxy 가 너무 많아 메모리·기동 시간 증가
  ✅ Pointcut 범위 좁히기

### Around 사용
- ❌ `pjp.proceed()` 호출 누락 → 원본 메서드 실행 안 됨
  ✅ try 안에서 항상 호출
- ❌ Around 에서 예외 swallow → 비즈니스 예외 묻힘
  ✅ `throw t;` 명시적 재throw

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| `@Transactional` 적용 안 됨 | self-invocation | 다른 빈으로 분리 또는 `@Lazy` self 주입 |
| `@Transactional` 적용 안 됨 (private) | Proxy 가 private 메서드 못 잡음 | public 으로 변경 |
| `@Async` 가 동기 실행됨 | self-invocation 또는 `@EnableAsync` 누락 | 빈 분리 + 설정 추가 |
| Around 에서 반환값이 null | `pjp.proceed()` 반환값 반환 안 함 | `return pjp.proceed()` 명시 |
| `final` 클래스에 AOP 안 먹힘 | CGLIB 상속 불가 | final 제거 또는 인터페이스 도입 |
| Pointcut 표현식 0 매칭 | 패키지·메서드명 오타 | `execution()` 패턴 다시 확인 |
| Spring Boot 에서 빈 시작 시간 폭증 | 광범위 Pointcut + 많은 빈 | Pointcut 범위 좁힘 |

---

## 14. 자가점검

1. 횡단 관심사(Cross-Cutting Concern) 의 예 4가지?
2. Aspect, Pointcut, Advice 의 관계를 한 문장으로?
3. Advice 5가지 시점은? 각 차이는?
4. Spring AOP 의 Proxy 방식 2가지와 각 적용 조건?
5. Self-Invocation 문제의 원인과 해결?
6. `@Transactional` 이 private 메서드에 안 먹는 이유?
7. Around advice 가 다른 advice 보다 강력한 이유?

<details><summary>풀이</summary>

1. 로깅, 트랜잭션, 보안, 캐시, 모니터링, 재시도, 비동기 실행 (택 4).
2. **Aspect** 는 횡단 관심사 모듈. **Pointcut** 은 그 Aspect 가 적용될 위치 선언. **Advice** 는 그 위치에서 실행되는 동작 + 시점.
3. **Before** (실행 전) / **After** (성공·실패 모두 후) / **AfterReturning** (정상 반환 후) / **AfterThrowing** (예외 시) / **Around** (전후 모두 + 실행 자체 제어).
4. **JDK Dynamic Proxy** — 인터페이스 기반. **CGLIB** — 클래스 상속 기반. Spring Boot 2.x+ 는 CGLIB 가 기본 (인터페이스 없어도 OK).
5. **원인**: `this.method()` 호출은 Proxy 가 아닌 Target 의 메서드 직접 호출 → Advice 안 끼어듦. **해결**: 메서드를 다른 빈으로 분리, 또는 self 를 Proxy 로 다시 주입.
6. **Proxy 가 외부에서 호출하는 메서드만 가로챌 수 있기 때문**. private 메서드는 클래스 외부에서 호출 불가 → Proxy 가 가로챌 기회 없음. CGLIB 는 상속 기반인데 private 은 상속 불가.
7. `proceed()` 를 직접 호출하므로 **실행 자체를 막거나, 반환값을 바꾸거나, 재시도하거나, 둘러싼 try/catch 로 예외를 변환**할 수 있음. 다른 advice 는 시점만 잡을 뿐 실행 제어 못 함.

</details>

---

## 15. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.13 관점 지향 프로그래밍 (배경·예시) | §1 ~ §4 (Part A) |
| p.14 ~ p.19 Proxy (개념·CGLIB·동작 원리) | §5 ~ §7 (Part B) |
| p.20 ~ p.26 Spring AOP (Annotation·Pointcut) | §8 ~ §11 (Part C) |
| p.27 마무리 | (생략) |

_27p 슬라이드 모두 커버._
