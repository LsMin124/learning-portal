# AOP (Aspect-Oriented Programming) — 치트시트

> 27p 슬라이드 · 횡단 관심사 (로깅·트랜잭션·보안) 를 비즈니스 코드에서 분리.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **AOP** = "여러 클래스에 공통 코드 (로깅·트랜잭션) 가 흩어진 문제" 를 한 곳에서
2. **횡단 관심사 (Cross-cutting concerns)**: 로깅·트랜잭션·보안·캐싱·성능 측정
3. **5 Advice**: `@Before` / `@After` / `@AfterReturning` / `@AfterThrowing` / `@Around` (가장 강력)
4. **Pointcut** = "어디에 적용할지" 표현식 (`execution(...)`, `@annotation(...)`)
5. **`@Transactional`, `@Async`, `@Scheduled` 모두 AOP** 의 한 예
6. **Spring AOP 는 프록시 기반** - 같은 클래스 내 메서드 호출은 AOP 안 걸림

## 가장 중요한 코드 3개

```java
// (1) 로깅 Aspect
@Aspect
@Component
@Slf4j
public class LoggingAspect {

    @Around("@within(org.springframework.stereotype.Service)")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            long ms = (System.nanoTime() - start) / 1_000_000;
            log.info("{} took {}ms", pjp.getSignature().toShortString(), ms);
        }
    }
}
```

```java
// (2) 트랜잭션 (Spring 이 자동 AOP)
@Service
public class TransferService {
    @Transactional(rollbackFor = Exception.class)
    public void transfer(long fromId, long toId, BigDecimal amount) {
        // 메서드 시작 = 트랜잭션 시작
        // 정상 종료 = commit
        // 예외 = rollback
    }
}
```

```java
// (3) 커스텀 어노테이션 + AOP
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface AdminOnly {}

@Aspect
@Component
public class SecurityAspect {
    @Before("@annotation(adminOnly)")
    public void checkAdmin(AdminOnly adminOnly) {
        User user = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        if (!user.isAdmin()) throw new AccessDeniedException("관리자 권한 필요");
    }
}

// 사용
@Service
public class AdminService {
    @AdminOnly
    public void deleteUser(long id) { ... }
}
```

## 면접 한 줄 답변
- **AOP 가 뭐?** → 횡단 관심사 (모든 메서드에 공통) 를 한 곳에 모아 비즈니스 코드에서 분리.
- **Spring AOP 의 원리?** → 프록시 객체. 빈을 직접 안 주입하고 프록시를 주입 → 메서드 호출 시 추가 동작.
- **`@Transactional` 동작?** → AOP 가 메서드 앞에 `con.setAutoCommit(false)`, 뒤에 `commit/rollback` 추가.
- **AOP 의 한계?** → 같은 클래스 내 메서드 호출 (this 호출) 은 프록시를 거치지 않아 AOP 안 걸림.

---

# 2. Quick Reference (실무 복붙)

## AOP 5 Advice

| Advice | 시점 | 용례 |
|--|--|--|
| `@Before` | 메서드 실행 전 | 권한 체크, 입력 로깅 |
| `@After` | 메서드 종료 후 (성공/실패 무관) | 정리 |
| `@AfterReturning` | 정상 반환 후 | 결과 로깅 |
| `@AfterThrowing` | 예외 발생 시 | 에러 알림 |
| `@Around` | 전체 둘러쌈 (가장 강력) | 시간 측정, 캐싱, 트랜잭션 |

## Pointcut 표현식

```java
// execution - 메서드 시그니처
@Pointcut("execution(public * com.study.service..*.*(..))")
// public · 모든 반환 타입 · com.study.service 하위 모든 패키지 · 모든 클래스 · 모든 메서드 · 모든 파라미터

@Pointcut("execution(* com.study.service.BoardService.*(..))")
@Pointcut("execution(* find*(..))")               // find 로 시작
@Pointcut("execution(* *(*, ..))")                // 1개 이상 파라미터

// within - 클래스/패키지
@Pointcut("within(com.study.service..*)")
@Pointcut("within(@org.springframework.stereotype.Service *)")

// @within - 클래스 어노테이션
@Pointcut("@within(org.springframework.stereotype.Service)")

// @annotation - 메서드 어노테이션
@Pointcut("@annotation(com.study.AdminOnly)")

// args - 파라미터
@Pointcut("execution(* *.find*(Long))")
@Pointcut("args(java.lang.Long)")

// 조합
@Pointcut("execution(* com.study.service..*(..)) && !execution(* *.toString())")
```

## @Around 패턴 (가장 강력)

```java
@Aspect @Component @Slf4j
public class TimingAspect {

    @Around("@within(org.springframework.stereotype.Service)")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        // === 메서드 실행 전 ===
        long start = System.nanoTime();
        log.debug("진입: {}", pjp.getSignature());

        try {
            // === 실제 메서드 호출 ===
            Object result = pjp.proceed();
            return result;
        } catch (Throwable t) {
            log.error("에러: {}", pjp.getSignature(), t);
            throw t;
        } finally {
            // === 메서드 실행 후 ===
            long ms = (System.nanoTime() - start) / 1_000_000;
            if (ms > 1000) log.warn("SLOW: {} took {}ms", pjp.getSignature().toShortString(), ms);
        }
    }
}
```

## JoinPoint API

```java
@Before("execution(* com.study.service..*(..))")
public void log(JoinPoint jp) {
    jp.getSignature();                  // 메서드 시그니처
    jp.getSignature().getName();        // 메서드 이름
    jp.getSignature().toShortString();  // "BoardService.findById(..)"
    jp.getArgs();                       // 파라미터 배열
    jp.getTarget();                     // 원본 객체
    jp.getThis();                       // 프록시 객체
}
```

## 트랜잭션 AOP (`@Transactional`)

```java
@Service
public class BoardService {

    @Transactional                              // 기본 (RuntimeException 만 롤백)
    public Board create(Board b) { ... }

    @Transactional(readOnly = true)             // SELECT 전용 최적화
    public Board findById(long id) { ... }

    @Transactional(rollbackFor = Exception.class)  // 체크 예외도 롤백
    public void upload(MultipartFile f) throws IOException { ... }

    @Transactional(isolation = Isolation.READ_COMMITTED)
    public void specialQuery() { ... }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void newTransaction() { ... }        // 항상 새 트랜잭션
}
```

## AOP 의 한계 (프록시 기반)

```java
@Service
public class BoardService {

    @Transactional
    public void outer() {
        inner();                                // X - this.inner() 직접 호출 → AOP 안 걸림
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void inner() { ... }
}
```

**해결 1**: 별도 빈으로 분리
```java
@Service @RequiredArgsConstructor
public class A {
    private final B b;
    public void outer() { b.inner(); }          // 다른 빈 호출 → AOP 적용
}
```

**해결 2**: AopContext (덜 권장)
```java
((BoardService) AopContext.currentProxy()).inner();
```

## 로깅 + 시간 측정 + 슬로 알람 풀세트

```java
@Aspect @Component @Slf4j
public class ServiceAspect {

    @Pointcut("@within(org.springframework.stereotype.Service)")
    public void serviceLayer() {}

    @Around("serviceLayer()")
    public Object log(ProceedingJoinPoint pjp) throws Throwable {
        String name = pjp.getSignature().toShortString();
        long start = System.nanoTime();

        try {
            Object result = pjp.proceed();
            long ms = (System.nanoTime() - start) / 1_000_000;
            if (ms > 1000) log.warn("SLOW: {} {}ms", name, ms);
            else           log.debug("{} {}ms", name, ms);
            return result;
        } catch (Throwable t) {
            log.error("{} 실패: {}", name, t.getMessage());
            throw t;
        }
    }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| 같은 클래스 메서드 호출 → AOP 안 걸림 | 별도 빈으로 분리 |
| `@Transactional` 의 private 메서드 | public 만 적용됨 |
| 체크 예외 → 롤백 X | `rollbackFor = Exception.class` |
| Pointcut 오타 → 런타임 후 발견 | 작은 단위로 테스트 |
| Pointcut 이 너무 넓음 → 모든 메서드 영향 | 좁게 + `&&` 조합 |
| `@EnableAspectJAutoProxy` 누락 (옛 Spring) | Spring Boot 는 자동 |
| Aspect 자체가 빈 아님 → 동작 X | `@Component` 필수 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
AOP (27p)
│
├── [A] 횡단 관심사
│   ├── 로깅
│   ├── 트랜잭션
│   ├── 보안 (권한 체크)
│   ├── 캐싱
│   ├── 성능 측정
│   └── 입력 검증
│
├── [B] 5 Advice
│   ├── @Before
│   ├── @After
│   ├── @AfterReturning
│   ├── @AfterThrowing
│   └── @Around (가장 강력)
│
├── [C] Pointcut
│   ├── execution (메서드 시그니처)
│   ├── within (클래스/패키지)
│   ├── @within / @annotation
│   ├── args / target / this
│   └── 조합 (&&, ||, !)
│
├── [D] JoinPoint API
│   ├── getSignature
│   ├── getArgs
│   ├── getTarget / getThis
│   └── proceed (Around 전용)
│
├── [E] Spring 의 AOP 활용
│   ├── @Transactional
│   ├── @Async
│   ├── @Scheduled
│   ├── @Cacheable
│   └── Spring Security
│
├── [F] 프록시 메커니즘
│   ├── JDK Dynamic Proxy (인터페이스)
│   ├── CGLIB Proxy (클래스)
│   └── 같은 클래스 호출 함정
│
└── [G] AspectJ (vs Spring AOP)
    ├── 컴파일 타임 위빙
    ├── 모든 메서드 적용 가능
    └── Spring AOP 보다 강력
```

## 학습 진도 체크리스트

### A. 개념
- [ ] 횡단 관심사의 의미
- [ ] AOP vs OOP 차이

### B. Advice
- [ ] 5 Advice 의 시점·반환값
- [ ] @Around 의 ProceedingJoinPoint
- [ ] @AfterThrowing 의 예외 전파

### C. Pointcut
- [ ] execution 패턴
- [ ] @annotation 으로 커스텀 어노테이션
- [ ] @within 으로 스테레오타입

### D. 실무
- [ ] 로깅 Aspect 작성
- [ ] 시간 측정 + Slow 알람
- [ ] 커스텀 어노테이션 + AOP

### E. Spring 의 AOP
- [ ] @Transactional 의 동작 원리
- [ ] @Async / @Scheduled
- [ ] 프록시 한계 (this 호출)

## 연관 강의

```
1강 Framework      -> 개념
2강 DI             -> 빈 관리
3강 SpringBoot     -> 자동 설정
4강 AOP            <- 현재 위치
5강 MVC1           -> @RestController 도 빈
11강 종합 실습     -> 로깅 AOP 활용
```

→ 다음 (MVC1) 에서 **Web 모듈의 핵심**.
