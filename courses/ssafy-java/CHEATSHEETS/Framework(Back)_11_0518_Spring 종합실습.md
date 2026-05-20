# Spring 종합 실습 — 치트시트

> 41p 슬라이드 · Framework Back 1~9강 통합 (Spring Boot + MyBatis + MVC + AOP + Interceptor + 트랜잭션).
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **레이어**: Filter → Interceptor → Controller → Service (@Transactional) → Mapper → DB
2. **표준 응답**: `ApiResponse<T>(ok, data, error)` 또는 ResponseEntity + 상태 코드
3. **전역 예외**: `@RestControllerAdvice` 로 비즈니스 예외 → 사용자 메시지
4. **트랜잭션**: SELECT 는 `readOnly = true`, 변경은 기본, 외부 API 호출은 트랜잭션 밖
5. **인증**: Interceptor + `@LoginUser` ArgumentResolver
6. **페이지네이션**: `PageResult<T>(items, total, page, size)` 반환

## 가장 중요한 코드 3개

```java
// (1) Controller (REST API)
@RestController
@RequestMapping("/api/boards")
@RequiredArgsConstructor
public class BoardApi {

    private final BoardService service;

    @GetMapping
    public PageResult<BoardListItem> list(@ModelAttribute BoardSearchCond cond) {
        return service.search(cond);
    }

    @PostMapping
    public ResponseEntity<Board> create(
            @RequestBody @Valid BoardCreateReq req,
            @LoginUser User user) {
        Board saved = service.create(req, user.getId());
        return ResponseEntity.created(URI.create("/api/boards/" + saved.getId())).body(saved);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id, @LoginUser User user) {
        service.delete(id, user.getId());
        return ResponseEntity.noContent().build();
    }
}
```

```java
// (2) Service (트랜잭션)
@Service
@RequiredArgsConstructor
public class BoardService {

    private final BoardMapper boardMapper;
    private final CommentMapper commentMapper;

    @Transactional(readOnly = true)
    public PageResult<BoardListItem> search(BoardSearchCond cond) {
        List<BoardListItem> items = boardMapper.search(cond);
        int total = boardMapper.count(cond);
        return new PageResult<>(items, total, cond.getPage(), cond.getSize());
    }

    @Transactional
    public void delete(long boardId, long userId) {
        commentMapper.deleteByBoard(boardId);
        if (boardMapper.delete(boardId, userId) == 0) {
            throw new ForbiddenException("권한 없음");
        }
    }
}
```

```java
// (3) 전역 예외 처리
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> validation(MethodArgumentNotValidException e) {
        Map<String, String> errors = e.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
        return ResponseEntity.badRequest().body(ApiResponse.ok(errors));
    }

    @ExceptionHandler(ForbiddenException.class)
    public ResponseEntity<?> forbidden(ForbiddenException e) {
        return ResponseEntity.status(403).body(ApiResponse.fail(e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> fallback(Exception e) {
        log.error("Unhandled", e);
        return ResponseEntity.status(500).body(ApiResponse.fail("서버 오류"));
    }
}
```

## 면접 한 줄 답변
- **레이어 분리가 왜?** → MyBatis → JPA 갈아끼울 때 Service/Controller 영향 X. 테스트·재사용 ↑.
- **`@Transactional` 안에서 외부 API 호출 위험?** → 트랜잭션 시간 = API 응답 시간. 락 점유 + 풀 고갈.
- **체크 예외 롤백?** → 기본은 RuntimeException 만. `rollbackFor = Exception.class` 명시.
- **표준 API 응답 포맷의 가치?** → 클라이언트 일관 파싱 + 에러 로깅 자동화 + Swagger 문서화.

---

# 2. Quick Reference (실무 복붙)

## 레이어 책임

```
[Browser/Postman]
        ↓
[Filter] - 인코딩, CORS
[DispatcherServlet]
[Interceptor] - 인증 (JWT)
[Controller] - @RestController, HTTP 매핑, Validation
        ↓
[Service] - @Transactional, 비즈니스, 권한
        ↓
[Mapper] - @Mapper, SQL
        ↓
[MySQL]
```

## ApiResponse 표준

```java
public record ApiResponse<T>(boolean ok, T data, String error) {
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(true, data, null);
    }
    public static ApiResponse<Void> fail(String error) {
        return new ApiResponse<>(false, null, error);
    }
}
```

## PageResult

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
```

## Service 트랜잭션

```java
@Service @RequiredArgsConstructor
public class BoardService {

    private final BoardMapper boardMapper;

    @Transactional(readOnly = true)            // SELECT 전용
    public PageResult<Board> search(BoardSearchCond cond) {
        List<Board> items = boardMapper.search(cond);
        int total = boardMapper.count(cond);
        return new PageResult<>(items, total, cond.getPage(), cond.getSize());
    }

    @Transactional                             // 변경
    public Board create(BoardCreateReq req, long userId) {
        Board b = Board.of(req, userId);
        boardMapper.insert(b);
        return b;
    }

    @Transactional(rollbackFor = Exception.class)   // 체크 예외 롤백
    public void uploadAndSave(MultipartFile file) throws IOException { ... }
}
```

## JWT 인증 Interceptor (`@Public` 으로 제외)

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Public {}

@Component @RequiredArgsConstructor
public class JwtAuthInterceptor implements HandlerInterceptor {
    private final JwtParser jwt;

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        if (!(handler instanceof HandlerMethod hm)) return true;
        if (hm.hasMethodAnnotation(Public.class)) return true;

        String h = req.getHeader("Authorization");
        if (h == null || !h.startsWith("Bearer ")) { res.setStatus(401); return false; }

        try {
            User user = jwt.parse(h.substring(7));
            req.setAttribute("loginUser", user);
            return true;
        } catch (JwtException e) { res.setStatus(401); return false; }
    }
}
```

## @LoginUser 자동 주입

```java
@Component @RequiredArgsConstructor
public class LoginUserResolver implements HandlerMethodArgumentResolver {
    @Override public boolean supportsParameter(MethodParameter p) {
        return p.hasParameterAnnotation(LoginUser.class)
            && p.getParameterType().equals(User.class);
    }
    @Override public Object resolveArgument(MethodParameter p, ModelAndViewContainer mavc,
            NativeWebRequest req, WebDataBinderFactory df) {
        return req.getNativeRequest(HttpServletRequest.class).getAttribute("loginUser");
    }
}

// 컨트롤러에서
@PostMapping
public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req,
                                     @LoginUser User user) { ... }
```

## AOP 시간 측정

```java
@Aspect @Component @Slf4j
public class TimingAspect {
    @Around("@within(org.springframework.stereotype.Service)")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try { return pjp.proceed(); }
        finally {
            long ms = (System.nanoTime() - start) / 1_000_000;
            if (ms > 1000) log.warn("SLOW: {} {}ms", pjp.getSignature().toShortString(), ms);
        }
    }
}
```

## application.yml profile

```yaml
spring.profiles.active: ${SPRING_PROFILE:dev}

mybatis:
  mapper-locations: classpath:mapper/*.xml
  configuration:
    map-underscore-to-camel-case: true

---
spring.config.activate.on-profile: dev
spring.datasource.url: jdbc:mysql://localhost:3306/dev_db
logging.level.com.ssafy.mapper: DEBUG

---
spring.config.activate.on-profile: prod
spring.datasource.url: jdbc:mysql://prod-host:3306/prod_db
spring.datasource.password: ${DB_PASSWORD}
```

## 체크리스트

- [ ] @RequestBody DTO 에 @Valid + Bean Validation
- [ ] Service 메서드 @Transactional (readOnly 구분)
- [ ] 모든 SQL `#{}` (또는 `${}` + 화이트리스트)
- [ ] 컨트롤러 try-catch 없음 (전역 핸들러)
- [ ] 비밀 정보 환경변수
- [ ] 로깅 AOP 로 통합
- [ ] 메인 클래스 루트 패키지
- [ ] 동적 SQL `<where>`/`<if>`
- [ ] 페이지네이션 total count 같이

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| @Transactional 안 외부 API 호출 | 트랜잭션 밖에서 호출 |
| 체크 예외 → 롤백 X | rollbackFor 명시 |
| `@RestController` view name 반환 | ResponseEntity |
| writerId 클라이언트 신뢰 | `@LoginUser` 서버 검증 |
| stacktrace 응답 노출 | 사용자엔 일반 메시지, 로그에 stack |
| 200 으로 통일 + success 필드 | HTTP 상태 코드 정확히 |
| 비밀번호 평문 | bcrypt VARCHAR(255) |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Spring 종합 실습 (41p)
│
├── [A] 통합 아키텍처
│   ├── Filter (CORS, 인코딩)
│   ├── Interceptor (인증)
│   ├── Controller (HTTP)
│   ├── Service (트랜잭션)
│   ├── Mapper (SQL)
│   └── DB
│
├── [B] REST API
│   ├── @RestController
│   ├── @RequestBody @Valid
│   ├── @LoginUser ArgumentResolver
│   ├── ResponseEntity
│   └── HTTP 상태 코드
│
├── [C] Service
│   ├── @Transactional(readOnly)
│   ├── rollbackFor
│   ├── 권한 검증 (affected = 0)
│   └── 외부 API 분리
│
├── [D] Mapper
│   ├── @Mapper + XML
│   ├── 동적 SQL
│   ├── resultMap
│   └── #{} 안전
│
├── [E] 응답 표준
│   ├── ApiResponse<T>
│   ├── PageResult<T>
│   └── ErrorResponse
│
├── [F] 예외 처리
│   ├── @RestControllerAdvice
│   ├── Validation / Business / Fallback
│   └── 보안 (stack 숨김)
│
└── [G] 운영
    ├── application.yml profile
    ├── 환경변수 (DB_PASSWORD)
    ├── AOP 시간 측정
    └── DevTools 자동 재시작
```

## 학습 진도 체크리스트

- [ ] 레이어 분리의 의미 (5 레이어)
- [ ] @Transactional 외부 API 위험
- [ ] @LoginUser + ArgumentResolver
- [ ] ApiResponse / PageResult 표준
- [ ] @RestControllerAdvice 전역 예외
- [ ] JWT Interceptor + @Public
- [ ] AOP 시간 측정 + 슬로 알람
- [ ] Profile (dev/prod) 분리
- [ ] 환경변수로 비밀 관리

## 연관 강의

```
1~9강 Framework Back -> 개별 학습
11강 종합 실습       <- 현재 위치 (통합)
12강 REST API        -> 심화
13강 Spring Batch    -> 배치
14강 CORS PJT        -> 전체 PJT
```

→ 다음 (REST API) 에서 **API 심화 + CORS + 버저닝**.
