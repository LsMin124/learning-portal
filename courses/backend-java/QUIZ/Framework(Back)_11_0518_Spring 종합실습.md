# Spring 종합 실습 - 퀴즈

> 14문항. 개념·적용·디버그·면접. Filter / Interceptor / Controller / Service / Mapper 통합.

---

### Q1. (개념) Spring Boot + MyBatis 통합 게시판의 레이어 구조와 각 책임?

<details><summary>정답</summary>

```
[Browser/Postman]
        ↓ HTTP
[Filter: 인코딩/CORS]
[DispatcherServlet]
[Interceptor: 인증 (JWT)]
[Controller (@RestController)]
[Service (@Transactional)]
[Mapper (MyBatis @Mapper)]
[MySQL]
```

| 레이어 | 책임 | 어노테이션 |
|--|--|--|
| **Filter** | 모든 요청 전후 - 인코딩, CORS, 로깅 | `@Component`+`OncePerRequestFilter` |
| **Interceptor** | 컨트롤러 진입 전 - 인증, 권한 | `HandlerInterceptor` |
| **Controller** | HTTP 파라미터 매핑, 응답 형식 | `@RestController`, `@RequestMapping` |
| **Service** | 비즈니스 로직, 트랜잭션 경계 | `@Service`, `@Transactional` |
| **Mapper** | SQL 실행, DB ↔ 객체 매핑 | `@Mapper` |

**원칙**: 각 레이어는 **자기 위의 것을 모름**. Mapper 가 Service 의 존재를 모름, Service 가 Controller 모름 → 테스트·교체 용이.

</details>

### Q2. (디버그) `@Transactional` 메서드 안에서 외부 API 를 호출하면 위험한 이유?

<details><summary>정답</summary>

```java
@Transactional
public void createOrder(OrderReq req) {
    Order order = orderMapper.insert(req);              // 1. DB INSERT
    paymentClient.charge(order.getId(), req.amount());  // 2. 외부 결제 API 호출
    orderMapper.markPaid(order.getId());                // 3. DB UPDATE
}
```

**위험**:

1. **트랜잭션 시간 = 외부 API 응답 시간**
   - 결제 API 가 5초 걸리면 트랜잭션도 5초간 열림
   - DB 행에 락 점유 → 다른 트랜잭션 대기
   - DB 커넥션 풀 고갈 → 전체 서비스 정지

2. **외부 API 실패 시 일관성 어려움**
   - 결제 성공 → DB UPDATE 실패 → 결제는 됐는데 주문 없음
   - 결제 실패 → DB 롤백 → 좋음, 그러나 결제가 timeout 후 성공하면 환불 필요

**해결 패턴**:

```java
// 1. 트랜잭션 밖에서 외부 호출
public void createOrder(OrderReq req) {
    Order order = orderService.createPending(req);          // @Transactional
    PaymentResult r = paymentClient.charge(order.getId(), req.amount());  // 트랜잭션 X
    orderService.markPaid(order.getId(), r.txId());          // @Transactional
}

// 2. Saga 패턴 - 보상 트랜잭션
//    실패 시 이전 단계를 되돌리는 별도 단계
```

**원칙**: **트랜잭션 안에는 DB 작업만**. 외부 API, 메일 발송, 파일 업로드는 트랜잭션 밖.

</details>

### Q3. (개념) `@RestControllerAdvice` 와 `@ControllerAdvice` 의 차이?

<details><summary>정답</summary>

```java
@RestControllerAdvice  =  @ControllerAdvice + @ResponseBody
```

| | `@ControllerAdvice` | `@RestControllerAdvice` |
|--|--|--|
| 반환 | ViewName (JSP/Thymeleaf) | JSON/XML (HttpMessageConverter) |
| 용도 | 전통적 MVC + 뷰 | REST API |

**전통적 MVC**:
```java
@ControllerAdvice
public class GlobalHandler {
    @ExceptionHandler(NotFoundException.class)
    public String notFound() {
        return "error/404";    // resolve to /WEB-INF/views/error/404.jsp
    }
}
```

**REST API**:
```java
@RestControllerAdvice
public class GlobalApiHandler {
    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> notFound(NotFoundException e) {
        return ResponseEntity.status(404)
            .body(ApiResponse.fail(e.getMessage()));    // 자동 JSON 직렬화
    }
}
```

→ REST API 만 만들 거면 `@RestControllerAdvice`.

</details>

### Q4. (개념) `@Transactional(readOnly = true)` 의 3가지 이점?

<details><summary>정답</summary>

```java
@Service
public class BoardService {

    @Transactional(readOnly = true)        // 읽기 전용
    public PageResult<Board> search(BoardSearchCond cond) { ... }

    @Transactional                         // 쓰기 (기본)
    public void create(Board b) { ... }
}
```

**이점**:

1. **성능 최적화**
   - JPA: flush 와 dirty checking 생략 (변경 감지 안 함)
   - MyBatis: 큰 차이 없지만 명시적 의도 표현

2. **읽기 전용 Replica 라우팅**
   - Spring Boot + AbstractRoutingDataSource → readOnly 트랜잭션은 슬레이브 DB 로
   - 마스터 DB 부하 ↓

3. **의도 명시 + 안전성**
   - 코드 리뷰 시 "이 메서드는 데이터를 안 바꾸는구나" 한눈에
   - 실수로 INSERT/UPDATE 하면 `TransientDataAccessException` 등 발생 (드라이버에 따라)

**관습**: SELECT 전용 메서드는 무조건 `readOnly = true` 붙이기.

</details>

### Q5. (디버그) 체크 예외 (`IOException`) 를 던졌는데 트랜잭션이 롤백 안 됨. 이유와 해결?

<details><summary>정답</summary>

```java
@Transactional
public void uploadAndSave(MultipartFile file) throws IOException {
    boardMapper.insert(...);            // DB INSERT
    file.transferTo(...);               // IOException 발생 가능 (체크 예외)
    // -> 예외 발생해도 DB INSERT 는 commit 됨!
}
```

**이유**: Spring `@Transactional` 의 기본 롤백 정책은 **RuntimeException 과 Error 만**. 체크 예외 (`Exception`, `IOException`, `SQLException` 등) 는 **롤백 안 함**.

**왜 이 정책?**: EJB 표준의 영향. RuntimeException 은 "예측 불가능한 시스템 에러" 로 간주, 체크 예외는 "비즈니스에서 예측되는 상황" 으로 간주.

**해결**:

```java
// 방법 1: rollbackFor 명시
@Transactional(rollbackFor = Exception.class)   // 모든 예외 롤백
public void uploadAndSave(MultipartFile file) throws IOException { ... }

// 방법 2: 체크 예외를 RuntimeException 으로 변환 (권장)
@Transactional
public void uploadAndSave(MultipartFile file) {
    try {
        boardMapper.insert(...);
        file.transferTo(...);
    } catch (IOException e) {
        throw new UncheckedIOException(e);     // 자동 롤백됨
    }
}

// 방법 3: 모든 클래스 일괄 적용
@Transactional(rollbackFor = Throwable.class)  // 안전 (Error 포함)
```

**최선**: 비즈니스 예외는 RuntimeException 상속 (`BusinessException extends RuntimeException`).

</details>

### Q6. (적용) 표준 응답 포맷 (ApiResponse) + 전역 예외 처리 (GlobalExceptionHandler) 구현.

<details><summary>정답</summary>

```java
// 1. 표준 응답
public record ApiResponse<T>(boolean ok, T data, String error) {
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(true, data, null);
    }
    public static ApiResponse<Void> fail(String error) {
        return new ApiResponse<>(false, null, error);
    }
}

// 2. 비즈니스 예외
public class ForbiddenException extends RuntimeException {
    public ForbiddenException(String msg) { super(msg); }
}

// 3. 전역 핸들러
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Map<String, String>>> validation(
            MethodArgumentNotValidException e) {
        Map<String, String> errors = e.getBindingResult()
            .getFieldErrors().stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                FieldError::getDefaultMessage));
        return ResponseEntity.badRequest().body(ApiResponse.ok(errors));
    }

    @ExceptionHandler(ForbiddenException.class)
    public ResponseEntity<ApiResponse<Void>> forbidden(ForbiddenException e) {
        return ResponseEntity.status(403).body(ApiResponse.fail(e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> unhandled(Exception e) {
        log.error("Unhandled", e);
        return ResponseEntity.status(500).body(ApiResponse.fail("Internal Server Error"));
    }
}
```

**가치**:
- 클라이언트가 모든 응답 동일 구조로 파싱 (`response.ok`, `response.data`, `response.error`)
- 컨트롤러에 try-catch 거의 안 씀 → 비즈니스 로직 집중
- 에러 로깅·모니터링 일관

</details>

### Q7. (적용) Service 메서드의 트랜잭션 분리 (조회는 readOnly, 변경은 기본).

<details><summary>정답</summary>

```java
@Service
@RequiredArgsConstructor
public class BoardService {
    private final BoardMapper boardMapper;
    private final CommentMapper commentMapper;

    // 조회 - readOnly
    @Transactional(readOnly = true)
    public PageResult<BoardListItem> search(BoardSearchCond cond) {
        List<BoardListItem> items = boardMapper.search(cond);
        int total = boardMapper.count(cond);
        return new PageResult<>(items, total, cond.getPage(), cond.getSize());
    }

    @Transactional(readOnly = true)
    public Board findById(long id) {
        return boardMapper.findById(id);
    }

    // 변경 - 기본 (rollbackFor 명시 권장)
    @Transactional
    public Board create(BoardCreateReq req, long userId) {
        Board b = Board.of(req, userId);
        boardMapper.insert(b);
        return b;
    }

    @Transactional
    public void delete(long boardId, long userId) {
        commentMapper.deleteByBoard(boardId);
        int affected = boardMapper.delete(boardId, userId);
        if (affected == 0) throw new ForbiddenException("권한 없음");
    }
}
```

**원칙**:
- SELECT 전용 → `readOnly = true`
- 변경 (INSERT/UPDATE/DELETE) → 기본
- 여러 DB 작업 → 같은 메서드 안에 묶기 (자동 트랜잭션)
- 권한 검증은 affected = 0 으로 (Race condition 회피)

</details>

### Q8. (적용) JWT 인증 Interceptor 골격 + `@Public` 어노테이션으로 일부 제외.

<details><summary>정답</summary>

```java
// 인증 제외 어노테이션
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Public {}

// Interceptor
@Component
@RequiredArgsConstructor
public class JwtAuthInterceptor implements HandlerInterceptor {
    private final JwtParser jwt;

    @Override
    public boolean preHandle(HttpServletRequest req,
                             HttpServletResponse resp,
                             Object handler) throws Exception {
        if (!(handler instanceof HandlerMethod hm)) return true;

        // @Public 메서드는 통과
        if (hm.hasMethodAnnotation(Public.class)) return true;

        String header = req.getHeader("Authorization");
        if (header == null || !header.startsWith("Bearer ")) {
            resp.setStatus(401);
            return false;
        }

        try {
            String token = header.substring(7);
            User user = jwt.parse(token);
            req.setAttribute("loginUser", user);
            return true;
        } catch (JwtException e) {
            resp.setStatus(401);
            return false;
        }
    }
}

// 등록
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(jwtAuthInterceptor)
            .addPathPatterns("/api/**")
            .excludePathPatterns("/api/auth/**");      // 로그인·가입 제외
    }
}

// 사용
@RestController
public class AuthApi {
    @Public                                              // 인증 없이 OK
    @PostMapping("/api/auth/login")
    public TokenResponse login(...) { ... }
}
```

</details>

### Q9. (개념) `@AuthenticationPrincipal` 의 효과와 동작 원리?

<details><summary>정답</summary>

```java
@GetMapping("/mypage")
public ResponseEntity<User> mypage(@AuthenticationPrincipal User loginUser) {
    return ResponseEntity.ok(loginUser);
}
```

**효과**: Spring Security 의 `SecurityContextHolder.getContext().getAuthentication().getPrincipal()` 을 메서드 인자로 **자동 주입**.

**동작 원리**:
1. Security Filter 가 토큰/세션 → 사용자 인증
2. `SecurityContextHolder` (ThreadLocal) 에 사용자 저장
3. 컨트롤러 진입 시 `AuthenticationPrincipalArgumentResolver` 가 인자에 주입

**없으면 매번 반복**:
```java
@GetMapping("/mypage")
public ResponseEntity<User> mypage() {
    User loginUser = (User) SecurityContextHolder.getContext()
        .getAuthentication().getPrincipal();
    return ResponseEntity.ok(loginUser);
}
```

**커스텀 어노테이션** (더 깔끔):
```java
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
@AuthenticationPrincipal
public @interface LoginUser {}

// 사용
public ResponseEntity<User> mypage(@LoginUser User user) { ... }
```

→ Spring Security 안 쓰는 Interceptor 자체 인증이면 `request.getAttribute("loginUser")` 패턴.

</details>

### Q10. (적용) 페이지네이션 결과를 `PageResult<T>` 로 total count 함께 반환.

<details><summary>정답</summary>

```java
public record PageResult<T>(
    List<T> items,
    int total,
    int page,
    int size
) {
    public int totalPages() {
        return (int) Math.ceil((double) total / size);
    }
    public boolean hasNext() {
        return page < totalPages();
    }
}

// Service
@Transactional(readOnly = true)
public PageResult<BoardListItem> search(BoardSearchCond cond) {
    List<BoardListItem> items = boardMapper.search(cond);    // 페이지 데이터
    int total = boardMapper.count(cond);                      // 전체 개수
    return new PageResult<>(items, total, cond.getPage(), cond.getSize());
}

// API 응답
{
    "ok": true,
    "data": {
        "items": [...],
        "total": 1234,
        "page": 3,
        "size": 10,
        "totalPages": 124,
        "hasNext": true
    }
}
```

**왜 total 같이?**:
- 클라이언트가 페이지 버튼 (1, 2, 3, ..., 124) 계산 가능
- "전체 1234건 중 21-30 번째 표시" 같은 UI
- 무한 스크롤도 hasNext 사용

**성능 주의**:
- `COUNT(*)` 는 풀스캔 가능성 → 인덱스 있는 컬럼으로 또는 캐시
- 키셋 페이지네이션이면 total 생략 (다음 버튼만)

</details>

### Q11. (적용) `@RequestBody @Valid` + Bean Validation + 검증 에러 응답.

<details><summary>정답</summary>

```java
// DTO with Validation
public class BoardCreateReq {
    @NotBlank(message = "제목은 필수")
    @Size(max = 200, message = "제목은 200자 이내")
    private String title;

    @NotBlank(message = "본문은 필수")
    private String content;

    // getter/setter
}

// Controller
@PostMapping("/api/boards")
public ResponseEntity<Board> create(
        @RequestBody @Valid BoardCreateReq req,
        @AuthenticationPrincipal User user) {
    Board saved = service.create(req, user.getId());
    return ResponseEntity.created(URI.create("/api/boards/" + saved.getId())).body(saved);
}

// 전역 핸들러 (Q6 와 동일)
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<?> validation(MethodArgumentNotValidException e) {
    Map<String, String> errors = e.getBindingResult().getFieldErrors().stream()
        .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
    return ResponseEntity.badRequest().body(ApiResponse.ok(errors));
}
```

**Validation 어노테이션**:
- `@NotNull` / `@NotEmpty` / `@NotBlank` (String 만 strip 후 비어있지 않음)
- `@Size(min, max)` - 컬렉션·문자열 길이
- `@Min` / `@Max` / `@Positive`
- `@Email`, `@Pattern(regexp=...)`
- 커스텀 - `ConstraintValidator` 인터페이스

**Validation 메시지 i18n** (`messages_ko.properties`):
```properties
NotBlank.boardCreateReq.title=제목은 필수입니다
Size.boardCreateReq.title=제목은 {2}자 이내여야 합니다
```

→ 컨트롤러는 `@Valid` 한 줄, 검증 에러는 전역 처리.

</details>

### Q12. (적용) AOP 로 Service 메서드 실행 시간 측정 + 로깅.

<details><summary>정답</summary>

```java
@Aspect
@Component
@Slf4j
public class TimingAspect {

    @Around("@within(org.springframework.stereotype.Service)")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            long elapsedMs = (System.nanoTime() - start) / 1_000_000;
            String method = pjp.getSignature().toShortString();

            if (elapsedMs > 1000) {
                log.warn("SLOW: {} took {}ms", method, elapsedMs);
            } else {
                log.debug("{} {}ms", method, elapsedMs);
            }
        }
    }
}
```

**효과**:
- 모든 Service 메서드 자동 측정 (코드 수정 X)
- 1초 이상 걸리는 메서드 WARN 로그 → 모니터링 알람 연동
- 비즈니스 로직과 측정 코드 분리 (관심사 분리)

**Pointcut 다양화**:
- `@within(스테레오타입)` - 클래스 레벨
- `@annotation(어노테이션)` - 메서드 레벨
- `execution(..)` - 정확한 메서드 시그니처
- `Pointcut` 합성: `@Around("serviceLayer() && !exclude()")`

→ AOP 의 대표 용례. 로깅·트랜잭션·보안 모두 비슷한 패턴.

</details>

### Q13. (적용) `application.yml` 의 profile (dev/prod) 분리 + 환경변수로 비밀 관리.

<details><summary>정답</summary>

```yaml
# application.yml (공통)
spring:
  profiles:
    active: ${SPRING_PROFILE:dev}        # 기본 dev

mybatis:
  mapper-locations: classpath:mapper/*.xml
  configuration:
    map-underscore-to-camel-case: true   # user_name -> userName 자동

---
spring.config.activate.on-profile: dev
spring.datasource.url: jdbc:mysql://localhost:3306/dev_db
spring.datasource.username: root
spring.datasource.password: 1234

logging.level.root: DEBUG

---
spring.config.activate.on-profile: prod
spring.datasource.url: jdbc:mysql://prod-host:3306/prod_db
spring.datasource.username: ${DB_USER}
spring.datasource.password: ${DB_PASSWORD}    # 환경변수

logging.level.root: INFO
```

**실행**:
```bash
# 개발 (기본)
java -jar app.jar

# 운영
SPRING_PROFILE=prod DB_USER=app DB_PASSWORD=$(get-secret) java -jar app.jar

# Docker
docker run -e SPRING_PROFILE=prod -e DB_PASSWORD=... myapp
```

**비밀 관리 원칙**:
- DB 비밀번호, API 키, JWT 시크릿 → **환경변수 또는 Secret Manager** (AWS Secrets Manager, Vault)
- Git 에 절대 commit X → `.gitignore` + `application-prod.yml` 제외
- IDE 실행 시 → `Run Configurations > Environment Variables`

**Spring Cloud Config**: 마이크로서비스에서 중앙 설정 서버.

</details>

### Q14. (면접) "Spring 종합 프로젝트의 각 레이어 책임 분리가 왜 중요한가?"

<details><summary>정답</summary>

**한 줄**: 한 레이어를 바꿔도 다른 레이어가 영향 안 받게 하기 위해.

**예시 - 안 좋은 코드**:
```java
@RestController
public class BoardController {
    @GetMapping("/api/boards/{id}")
    public Board get(@PathVariable long id) {
        // 컨트롤러가 SQL 직접
        try (Connection con = DriverManager.getConnection(URL, USER, PW);
             PreparedStatement ps = con.prepareStatement("SELECT * FROM boards WHERE id = ?")) {
            ps.setLong(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                Board b = new Board(...);
                // 비즈니스 로직도 여기
                if (b.getViewCount() > 1000) b.setHot(true);
                return b;
            }
        } catch (SQLException e) { ... }
        return null;
    }
}
```

**문제**:
- MyBatis → JPA 로 갈아끼우려면 컨트롤러 전체 수정
- 비즈니스 로직 테스트하려면 DB 띄워야
- HTTP 없이 배치 작업으로 같은 로직 재사용 불가
- 1000 라인 컨트롤러 → 유지보수 지옥

**레이어 분리 후**:
```java
@RestController
public class BoardController {
    private final BoardService service;

    @GetMapping("/api/boards/{id}")
    public Board get(@PathVariable long id) {
        return service.findById(id);    // 1줄
    }
}

@Service
public class BoardService {
    private final BoardMapper mapper;

    @Transactional(readOnly = true)
    public Board findById(long id) {
        Board b = mapper.findById(id);
        if (b.getViewCount() > 1000) b.setHot(true);   // 비즈니스 로직
        return b;
    }
}

@Mapper
public interface BoardMapper {
    Board findById(long id);    // SQL 만
}
```

**이점**:
1. **교체 용이** - MyBatis → JPA, Spring MVC → WebFlux 갈아끼울 때 한 레이어만
2. **테스트 가능** - Service 테스트는 Mapper Mock, HTTP 안 띄움
3. **재사용** - Service 를 배치 / 스케줄러 / 콘솔 앱에서도 사용
4. **명확한 책임** - 디버깅 시 어디 봐야 할지 명확
5. **팀 분업** - 백엔드/프론트 동시 작업 (API 스펙만 합의)

**Clean Architecture / Hexagonal Architecture**: 이 원칙의 진화형. 도메인 레이어가 외부 (DB, HTTP) 를 모르도록.

→ Spring 의 강점이 어노테이션 한 줄로 이 분리를 만들기 쉬움.

</details>
