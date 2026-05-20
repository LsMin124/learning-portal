# Framework 입문 — 치트시트

> 44p 슬라이드 · Framework 의 의미, IoC, Spring 의 위치.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Framework** = 흐름이 정해진 반제품 (Library 는 내가 호출, Framework 는 나를 호출 = IoC)
2. **IoC (Inversion of Control)**: 제어의 역전. 객체 생성·생명주기를 컨테이너가
3. **Spring** = 자바 엔터프라이즈의 사실상 표준. IoC + DI + AOP + 데이터 접근 + MVC
4. **Spring 모듈**: Core (IoC/DI) / AOP / Data / Web (MVC) / Security / Test
5. **POJO 중심** = 평범한 자바 객체로 비즈니스 로직. 어노테이션만 추가
6. **Spring Boot** = Spring 설정 자동화 + 내장 톰캣 + Starter 의존성

## 가장 중요한 코드 3개

```java
// (1) POJO + @Service - Framework 의 핵심 (간결함)
@Service
@RequiredArgsConstructor
public class BoardService {
    private final BoardMapper mapper;       // DI 자동 주입

    public Board findById(long id) {
        return mapper.findById(id);
    }
}
```

```java
// (2) Spring Boot 메인 클래스 - 마법
@SpringBootApplication                       // 자동 설정 + 컴포넌트 스캔
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}
```

```yaml
# (3) application.yml - 외부 설정
server.port: 8080
spring.datasource:
  url: jdbc:mysql://localhost:3306/mydb
  username: root
  password: ${DB_PASSWORD}
mybatis.mapper-locations: classpath:mapper/*.xml
```

## 면접 한 줄 답변
- **Library vs Framework?** → 라이브러리는 내가 호출 (jQuery), 프레임워크는 나를 호출 (Spring). IoC.
- **IoC 의 의미?** → 객체 생성·생명주기 제어를 개발자가 아니라 컨테이너가. 결합도 ↓.
- **Spring vs Spring Boot?** → Spring 은 프레임워크, Boot 는 Spring 설정 자동화 + Starter + 내장 톰캣.
- **왜 Spring 이 표준?** → POJO 기반 + 무수한 모듈 + DI/AOP 깊이 + 압도적 생태계.

---

# 2. Quick Reference (실무 복붙)

## Library vs Framework

| | Library | Framework |
|--|--|--|
| 호출 방향 | 내가 호출 | 나를 호출 (IoC) |
| 흐름 | 내가 결정 | Framework 가 결정 |
| 자유도 | 높음 | 낮음 (제약 있음) |
| 예 | Lombok, Apache Commons, jQuery | Spring, Django, React |

## IoC 의 의미

```java
// 안 좋은 예 - 직접 new
public class BoardController {
    private final BoardService service = new BoardService(new BoardMapper());
    // 강한 결합, 테스트 어려움
}

// 좋은 예 - DI (IoC 컨테이너가 주입)
@RestController
@RequiredArgsConstructor
public class BoardController {
    private final BoardService service;     // Spring 이 자동 주입
}
```

## Spring 의 7 모듈

| 모듈 | 책임 |
|--|--|
| **Core** | IoC 컨테이너, DI |
| **AOP** | 횡단 관심사 (로깅·트랜잭션) |
| **Data Access** | JDBC, ORM (Hibernate), Tx |
| **Web** | MVC, REST, WebSocket |
| **Web Reactive** | WebFlux (논블로킹) |
| **Security** | 인증·인가, OAuth, CSRF |
| **Test** | MockMvc, TestContainers |

## Spring Boot 핵심

```java
@SpringBootApplication
//= @Configuration + @EnableAutoConfiguration + @ComponentScan
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}
```

**자동화 3가지**:
1. **Auto Configuration**: classpath 보고 자동 설정 (`@EnableAutoConfiguration`)
2. **Starter 의존성**: `spring-boot-starter-web` 한 줄로 web 전체
3. **내장 톰캣**: WAR 배포 불필요, `java -jar app.jar`

## POJO 기반의 의미

```java
// 옛 EJB - Framework 특정 클래스 상속
public class BoardBean extends StatelessSessionBean {
    public void create() throws RemoteException { ... }
}

// Spring POJO - 평범한 자바 객체 + 어노테이션
@Service
public class BoardService {
    public Board create(Board b) { ... }
}
```

→ 테스트 쉬움 (그냥 new 해서 단위 테스트), Framework 종속성 낮음.

## 어노테이션 핵심

```java
// 빈 등록
@Component / @Service / @Repository / @Controller / @RestController

// DI
@Autowired           // 필드/세터 주입 (비권장)
@RequiredArgsConstructor + private final  // 생성자 주입 (권장)

// 설정
@Configuration
@Bean
@Value("${app.name}")
@ConfigurationProperties(prefix = "app")

// 웹
@GetMapping / @PostMapping / @PutMapping / @DeleteMapping
@PathVariable / @RequestParam / @RequestBody / @ModelAttribute

// 트랜잭션
@Transactional

// AOP
@Aspect / @Pointcut / @Around / @Before / @After
```

## 의존성 (pom.xml)

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
</dependency>
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency>
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `new` 로 객체 생성 → 결합도 ↑ | DI 받기 |
| `@Autowired` 필드 주입 | 생성자 주입 (final + RequiredArgsConstructor) |
| @ComponentScan 범위 누락 | 메인 클래스가 루트 패키지에 |
| @SpringBootApplication 없음 | 메인 클래스 필수 어노테이션 |
| 비밀번호 application.yml hardcoding | 환경변수 (`${DB_PASSWORD}`) |
| Framework 클래스 상속 강요 | POJO 만 사용 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Framework 입문 (44p)
│
├── [A] Framework 의 의미
│   ├── Library vs Framework
│   ├── IoC (Inversion of Control)
│   ├── Hollywood Principle ("Don't call us, we'll call you")
│   └── 흐름 제어
│
├── [B] Spring 의 위치
│   ├── 자바 엔터프라이즈 표준
│   ├── POJO 기반
│   ├── 7 모듈 (Core/AOP/Data/Web/Reactive/Security/Test)
│   └── 생태계 (Spring Data, Spring Security, ...)
│
├── [C] IoC 컨테이너
│   ├── BeanFactory / ApplicationContext
│   ├── 빈 등록 어노테이션 (@Component 등)
│   ├── 빈 생명주기 (init / destroy)
│   └── 범위 (singleton / prototype / request / session)
│
├── [D] DI
│   ├── 생성자 주입 (권장)
│   ├── Setter 주입
│   ├── 필드 주입 (비권장)
│   └── @Qualifier / @Primary
│
├── [E] Spring Boot
│   ├── @SpringBootApplication
│   ├── Auto Configuration
│   ├── Starter 의존성
│   ├── 내장 톰캣
│   └── application.yml (profile)
│
└── [F] 다음 강의 예고
    ├── 2강 DI 심화
    ├── 3강 Spring Boot 깊이
    ├── 4강 AOP
    └── 5~6강 MVC
```

## 학습 진도 체크리스트

### A. 개념
- [ ] Library vs Framework 차이 설명
- [ ] IoC 의 의미와 이점
- [ ] Hollywood Principle

### B. Spring
- [ ] 7 모듈 구분
- [ ] POJO 기반의 의미
- [ ] Spring vs Spring Boot 차이

### C. IoC 컨테이너
- [ ] ApplicationContext 생성
- [ ] 빈 등록 (@Component, @Bean)
- [ ] 빈 조회 (getBean)

### D. DI
- [ ] 생성자/세터/필드 주입 비교
- [ ] `@RequiredArgsConstructor` + `final`
- [ ] @Qualifier / @Primary

### E. Spring Boot
- [ ] @SpringBootApplication 의 구성
- [ ] Auto Configuration 의미
- [ ] application.yml profile 분리

## 연관 강의

```
1강 Framework        <- 현재 위치
2강 DI                -> IoC 컨테이너 깊이
3강 SpringBoot        -> 자동 설정 + Starter
4강 AOP               -> 횡단 관심사
5~6강 MVC             -> Web 모듈
7강 Interceptor       -> Web 깊이
8~9강 MyBatis         -> Data Access
11강 종합 실습        -> 모든 모듈 통합
```

→ 다음 (DI) 에서 **IoC 컨테이너의 작동 원리**.
