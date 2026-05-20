# Spring 종합 실습 — Framework Back 트랙 통합

> **이 노트는 무엇인가**: Framework Back 1~9강 (IoC/DI/SpringBoot/AOP/MVC/Interceptor/MyBatis) 모두 합쳐 **DB+MyBatis+Spring Boot 게시판** 완성.
> **왜 41 페이지인가**: 새 개념 약간 + 끝까지 동작하는 풀스택 예제.

---

## 들어가기 전에

- Framework Back 1~9강 + DB 트랙 완료.
- Spring Boot 3.x, MySQL 8, MyBatis Starter.

---

## 목표 아키텍처

```
[Browser/Postman]
        ↓ HTTP
[Filter: 인코딩·CORS]
[DispatcherServlet]
[Interceptor: 인증]
[Controller (REST)]
[Service (@Transactional)]
[Mapper (MyBatis)]
[MySQL]
```

각 레이어 명확한 책임. 1~9강의 모든 것이 한 자리.

---

## 레이어별 한 줄 예

```java
// 1. Controller
@RestController @RequiredArgsConstructor @RequestMapping("/api/boards")
public class BoardApi {
    private final BoardService service;
    @GetMapping public PageResult<BoardListItem> list(@ModelAttribute BoardSearchCond cond) {
        return service.search(cond);
    }
    @PostMapping
    public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req,
                                         @AuthenticationPrincipal User user) {
        Board saved = service.create(req, user.getId());
        return ResponseEntity.created(URI.create("/api/boards/" + saved.getId())).body(saved);
    }
}

// 2. Service
@Service @RequiredArgsConstructor
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
        if (boardMapper.delete(boardId, userId) == 0)
            throw new ForbiddenException("권한 없음");
    }
}

// 3. Mapper
@Mapper
public interface BoardMapper {
    List<BoardListItem> search(BoardSearchCond cond);
    int count(BoardSearchCond cond);
    int delete(@Param("id") long id, @Param("userId") long userId);
}
```

---

## 핵심 통합 토픽

### 1. 표준 응답 + 전역 예외

```java
public record ApiResponse<T>(boolean ok, T data, String error) {
    public static <T> ApiResponse<T> ok(T data) { return new ApiResponse<>(true, data, null); }
    public static ApiResponse<Void> fail(String error) { return new ApiResponse<>(false, null, error); }
}

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> validation(MethodArgumentNotValidException e) {
        Map<String,String> errors = e.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
        return ResponseEntity.badRequest().body(ApiResponse.ok(errors));
    }
    @ExceptionHandler(ForbiddenException.class)
    public ResponseEntity<?> forbidden(ForbiddenException e) {
        return ResponseEntity.status(403).body(ApiResponse.fail(e.getMessage()));
    }
}
```

### 2. 트랜잭션 경계

```java
@Transactional                              // 기본 RuntimeException 만 rollback
public void place(OrderReq req) { ... }

@Transactional(readOnly = true)              // SELECT 전용 최적화
public Order get(long id) { ... }
```

> ⚠️ 체크 예외는 기본 rollback 안 됨. `@Transactional(rollbackFor = Exception.class)` 또는 RuntimeException 으로.

### 3. 인터셉터로 인증

```java
@Component @RequiredArgsConstructor
public class JwtAuthInterceptor implements HandlerInterceptor {
    private final JwtParser jwt;
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse resp, Object handler) {
        if (!(handler instanceof HandlerMethod hm)) return true;
        if (hm.hasMethodAnnotation(Public.class)) return true;
        String token = req.getHeader("Authorization");
        if (token == null || !token.startsWith("Bearer ")) { resp.setStatus(401); return false; }
        try {
            req.setAttribute("loginUser", jwt.parse(token.substring(7)));
            return true;
        } catch (JwtException e) { resp.setStatus(401); return false; }
    }
}
```

### 4. AOP 시간 측정

```java
@Aspect @Component @Slf4j
public class TimingAspect {
    @Around("@within(org.springframework.stereotype.Service)")
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        long s = System.nanoTime();
        try { return pjp.proceed(); }
        finally { log.debug("{} {}ns", pjp.getSignature().toShortString(), System.nanoTime() - s); }
    }
}
```

### 5. 설정 분리

```yaml
spring:
  profiles: { active: dev }
mybatis:
  mapper-locations: classpath:mapper/*.xml
  configuration: { map-underscore-to-camel-case: true }
---
spring.config.activate.on-profile: dev
spring.datasource.url: jdbc:mysql://localhost:3306/dev_db
---
spring.config.activate.on-profile: prod
spring.datasource.url: jdbc:mysql://prod-host:3306/prod_db
spring.datasource.password: ${DB_PASSWORD}
```

---

## 체크리스트

- [ ] `@RequestBody` DTO 에 `@Valid` + Bean Validation
- [ ] Service 메서드 `@Transactional` 의도적 (readOnly 구분)
- [ ] 모든 SQL `#{}` (또는 `${}` + 화이트리스트)
- [ ] 컨트롤러 try-catch 없음 (전역 핸들러)
- [ ] 비밀 정보 환경변수
- [ ] 로깅 AOP 로 통합
- [ ] 메인 클래스 루트 패키지
- [ ] 동적 SQL `<where>`/`<if>`
- [ ] 페이지네이션 total count 같이

---

## 자가점검

1. `@Transactional` 메서드 안 외부 API 호출의 위험?
2. `@RestControllerAdvice` vs `@ControllerAdvice` 차이?
3. `readOnly = true` 의 이점?
4. 체크 예외 던졌을 때 기본 rollback?

<details><summary>풀이</summary>

1. 외부 API 응답 지연·실패 시 트랜잭션이 그 시간만큼 열려있음 → DB 락 점유, 커넥션 풀 고갈. 외부는 트랜잭션 밖, Saga 패턴 등.
2. `@RestControllerAdvice` = `@ControllerAdvice` + `@ResponseBody`. 응답 JSON.
3. JPA flush·dirty checking 생략으로 성능. MyBatis 도 의도 표현 명시화.
4. **롤백 안 됨**. RuntimeException/Error 만 자동. 체크 예외는 `rollbackFor` 명시.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1~5 표지·아키텍처 | 목표 |
| p.6~15 레이어·DTO | 레이어 예 |
| p.16~25 표준 응답·예외 | §1 |
| p.26~35 트랜잭션·AOP | §2, §4 |
| p.36~41 인터셉터·설정 | §3, §5 |

_단독 학습 가능 노트._
