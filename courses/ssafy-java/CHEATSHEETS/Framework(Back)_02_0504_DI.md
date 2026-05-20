# DI (의존성 주입) — 치트시트

> 37p 슬라이드 · Spring 의 IoC 컨테이너 + DI 깊이.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **DI** = 객체가 자기 의존성을 직접 만들지 않고 외부에서 받음
2. **3 주입 방식**: 생성자 (권장) / Setter / 필드
3. **`@Component` 계열 + `@Autowired`** 면 자동 주입
4. **`@RequiredArgsConstructor` + `private final`** 이 가장 안전한 패턴
5. **같은 타입 빈 여러 개**면 `@Qualifier` 또는 `@Primary` 로 선택
6. **Bean Scope**: singleton (기본, 한 개) / prototype (요청마다 새로) / request / session

## 가장 중요한 코드 3개

```java
// (1) 생성자 주입 (권장)
@Service
@RequiredArgsConstructor       // Lombok
public class BoardService {
    private final BoardMapper mapper;
    private final UserMapper userMapper;
    // 자동 생성자가 두 의존성 주입
}
```

```java
// (2) 빈 등록 4 종류
@Component   // 일반
@Service     // 비즈니스 로직
@Repository  // DAO (예외 변환)
@Controller  // 웹 (또는 @RestController)
@Configuration + @Bean   // 외부 라이브러리 객체

// 예
@Configuration
public class AppConfig {
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

```java
// (3) 같은 타입 여러 빈 - Qualifier
public interface MessageSender { void send(String msg); }

@Service("email") public class EmailSender implements MessageSender { ... }
@Service("sms")   public class SmsSender   implements MessageSender { ... }

@Service
@RequiredArgsConstructor
public class NotifyService {
    @Qualifier("email")
    private final MessageSender sender;     // EmailSender 주입
}
```

## 면접 한 줄 답변
- **DI 의 이점?** → 결합도 ↓ + 테스트 쉬움 (Mock 주입) + 객체 생명주기 컨테이너 관리.
- **생성자 주입 권장 이유?** → 불변 (`final`) + 누락 시 컴파일 에러 + 순환 의존성 즉시 탐지.
- **필드 주입의 문제?** → 테스트 시 reflection 필요 + 불변 안 됨 + 순환 의존성 런타임에야 발견.
- **싱글톤 빈인데 멀티스레드?** → 빈은 1개 공유. 인스턴스 필드 사용 금지, stateless 로.

---

# 2. Quick Reference (실무 복붙)

## 빈 등록 어노테이션

```java
@Component                            // 일반 컴포넌트
@Service                              // 비즈니스 로직 (의미만 다름)
@Repository                           // DAO (예외 변환 + 영속성)
@Controller / @RestController         // 웹 핸들러

@Configuration                        // 설정 클래스
public class AppConfig {
    @Bean                             // 외부 라이브러리 빈
    public ObjectMapper objectMapper() {
        return new ObjectMapper().registerModule(new JavaTimeModule());
    }
}
```

## DI 3 주입 방식

```java
// (1) 생성자 주입 - 권장
@Service
public class BoardService {
    private final BoardMapper mapper;

    public BoardService(BoardMapper mapper) {     // @Autowired 생략 가능 (단일 생성자)
        this.mapper = mapper;
    }
}

// Lombok 사용 (더 간결)
@Service
@RequiredArgsConstructor
public class BoardService {
    private final BoardMapper mapper;             // 자동 생성자
}

// (2) Setter 주입
@Service
public class BoardService {
    private BoardMapper mapper;

    @Autowired
    public void setMapper(BoardMapper mapper) {
        this.mapper = mapper;
    }
}

// (3) 필드 주입 - 비권장
@Service
public class BoardService {
    @Autowired
    private BoardMapper mapper;
}
```

## 생성자 주입의 이점

```java
@Service
@RequiredArgsConstructor
public class BoardService {
    private final BoardMapper mapper;     // (1) 불변 (final)
    private final UserMapper userMapper;  // (2) 누락 시 컴파일 에러
                                          // (3) 테스트 시 new BoardService(mockMapper, mockUserMapper)
                                          // (4) 순환 의존 시 즉시 에러
}
```

## 같은 타입 빈 여러 개

```java
public interface MessageSender { void send(String msg); }

@Service("email")
public class EmailSender implements MessageSender { ... }

@Service("sms")
public class SmsSender implements MessageSender { ... }

// 방법 1: @Qualifier
@Service
@RequiredArgsConstructor
public class NotifyService {
    @Qualifier("email")
    private final MessageSender sender;
}

// 방법 2: @Primary (기본 빈 지정)
@Service @Primary
public class EmailSender implements MessageSender { ... }

@Service
@RequiredArgsConstructor
public class NotifyService {
    private final MessageSender sender;   // @Primary 인 Email 주입
}

// 방법 3: 모든 빈 주입 (Map / List)
@Service
@RequiredArgsConstructor
public class NotifyService {
    private final Map<String, MessageSender> senders;   // {"email": ..., "sms": ...}

    public void notify(String type, String msg) {
        senders.get(type).send(msg);
    }
}
```

## Bean Scope

| Scope | 의미 | 사용 예 |
|--|--|--|
| **singleton** (기본) | 컨테이너당 1 개 | Service, Repository, Controller |
| **prototype** | 요청마다 새 인스턴스 | 상태가 있는 객체 |
| **request** | HTTP 요청당 1개 | 요청별 데이터 |
| **session** | 세션당 1개 | 로그인 사용자 별 |
| **application** | ServletContext 당 1개 | 앱 전체 공유 |

```java
@Service
@Scope("prototype")
public class StatefulProcessor { ... }

@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestContext { ... }
```

## @Value + 환경 설정

```java
@Service
public class MyService {
    @Value("${app.name}")              // application.yml
    private String appName;

    @Value("${app.maxConnections:10}") // 기본값 10
    private int maxConnections;

    @Value("#{T(System).currentTimeMillis()}")  // SpEL
    private long startedAt;
}
```

## @ConfigurationProperties (Type-safe)

```yaml
# application.yml
app:
  name: SSAFY
  version: 1.0
  features:
    - login
    - search
```

```java
@ConfigurationProperties(prefix = "app")
@Component
@Data
public class AppProperties {
    private String name;
    private String version;
    private List<String> features;
}
```

## 생명주기 콜백

```java
@Component
public class MyBean {
    @PostConstruct
    public void init() {
        // 의존성 주입 후 실행 (DB 풀 초기화 등)
    }

    @PreDestroy
    public void cleanup() {
        // 컨테이너 종료 시 (자원 해제)
    }
}
```

## 순환 의존성 (Circular Dependency)

```java
// 안 좋은 예 - 컴파일은 되지만 런타임 에러
@Service
@RequiredArgsConstructor
public class A {
    private final B b;
}

@Service
@RequiredArgsConstructor
public class B {
    private final A a;     // 순환!
}
// BeanCurrentlyInCreationException

// 해결 1: 설계 재검토 (보통 잘못된 설계)
// 해결 2: @Lazy (지연 주입)
@Service
public class A {
    public A(@Lazy B b) { ... }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `@Autowired` 필드 주입 | 생성자 주입 + final |
| 같은 타입 여러 빈 → NoUniqueBeanException | @Qualifier 또는 @Primary |
| 순환 의존성 | 설계 재검토 (또는 @Lazy) |
| singleton 빈에 인스턴스 필드 | stateless 로 |
| @Bean 메서드 안에서 다른 @Bean 호출 직접 | `@Configuration` 이 프록시로 처리 (proxyBeanMethods=true) |
| @ComponentScan 범위 밖 | 메인 클래스가 루트 패키지에 |
| `new MyService()` 직접 | DI 받기 (또는 ApplicationContext.getBean) |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
DI (37p)
│
├── [A] IoC 컨테이너
│   ├── BeanFactory (최소)
│   ├── ApplicationContext (실무)
│   ├── 빈 등록 / 조회 / 생성 / 소멸
│   └── @ComponentScan
│
├── [B] 빈 등록
│   ├── @Component / @Service / @Repository / @Controller
│   ├── @Configuration + @Bean
│   └── XML (옛)
│
├── [C] DI 3 방식
│   ├── 생성자 (권장: 불변 + 누락 검출)
│   ├── Setter (선택적 의존성)
│   └── 필드 (비권장)
│
├── [D] 같은 타입 빈
│   ├── @Qualifier (이름 지정)
│   ├── @Primary (기본)
│   ├── Map/List 주입 (모두)
│   └── @Profile (환경별)
│
├── [E] Bean Scope
│   ├── singleton (기본)
│   ├── prototype (매번 새로)
│   ├── request / session / application
│   └── ScopedProxyMode
│
├── [F] 설정 주입
│   ├── @Value (단일 값)
│   ├── @ConfigurationProperties (객체)
│   └── SpEL
│
└── [G] 생명주기
    ├── @PostConstruct
    ├── @PreDestroy
    └── InitializingBean / DisposableBean
```

## 학습 진도 체크리스트

### A. IoC 컨테이너
- [ ] ApplicationContext 생성 방법
- [ ] 빈 등록 vs 조회
- [ ] @ComponentScan 동작

### B. DI
- [ ] 3 주입 방식 비교
- [ ] 생성자 주입 권장 이유 4가지
- [ ] @RequiredArgsConstructor + final

### C. 같은 타입
- [ ] @Qualifier 사용
- [ ] @Primary 사용
- [ ] Map / List 주입 패턴

### D. Scope
- [ ] singleton 의 thread-safety
- [ ] prototype 의 의미
- [ ] request scope + proxyMode

### E. 설정
- [ ] @Value
- [ ] @ConfigurationProperties
- [ ] 외부 환경변수 주입

### F. 생명주기
- [ ] @PostConstruct
- [ ] @PreDestroy
- [ ] 순환 의존성 + @Lazy

## 연관 강의

```
1강 Framework        -> IoC 개념
2강 DI               <- 현재 위치
3강 SpringBoot       -> 자동 빈 등록
4강 AOP              -> 빈에 프록시 적용
5강 MVC1             -> Controller 빈
8강 MyBatis          -> Mapper 빈 자동 등록
```

→ 다음 (Spring Boot) 에서 **Auto Configuration + Starter**.
