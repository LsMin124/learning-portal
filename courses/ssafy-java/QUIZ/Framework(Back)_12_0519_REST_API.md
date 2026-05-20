# REST API - 퀴즈

> 15문항. 개념·적용·디버그·면접. Spring `@RestController` + Bean Validation + `@RestControllerAdvice`.

---

### Q1. (개념) REST 의 "Stateless" 가 의미하는 것 한 줄?

<details><summary>정답</summary>

서버가 클라이언트 상태를 기억하지 않는다 — **모든 요청은 그 자체로 완결되어 필요한 정보를 다 담아야** 한다. 인증·세션 정보도 매 요청 동반 (토큰/쿠키).

**왜 stateless?**:
- **수평 확장 (Horizontal Scaling)**: 어떤 서버가 요청 받아도 같은 결과 → Load Balancer 로 자유롭게 분산
- **장애 복구**: 서버 한 대 죽어도 다른 서버가 즉시 처리 (세션 안 잃음)
- **캐시 친화**: 응답이 요청에만 의존 → 캐시 가능

**대조 - Stateful**:
- 서버가 세션 보관 → 그 서버 죽으면 사용자 로그아웃
- Sticky Session 필요 → LB 복잡도 ↑

→ JWT 토큰이 stateless 의 대표 구현. 서버는 토큰만 검증하고 세션 보관 X.

</details>

### Q2. (적용) 다음 중 REST 관점에서 가장 적절한 매핑은?

```
A) POST /api/getUser?id=42
B) GET  /api/user-fetch/42
C) GET  /api/users/42
D) POST /api/users/42/get
```

<details><summary>정답</summary>

**C**. 자원 = 명사(복수형), 동작 = HTTP 메서드. `/api/users/{id}` GET.

**RESTful URL 원칙**:
- **명사** 사용 (`users`, `boards`), 동사 X (`getUser`, `fetch`)
- **복수형** (`/users` not `/user`)
- 계층 구조: `/users/{id}/posts/{postId}`
- 동작은 **HTTP 메서드** (GET/POST/PUT/DELETE)

**RESTful CRUD 패턴**:
| 작업 | 메서드 | URL |
|--|--|--|
| 전체 조회 | GET | `/users` |
| 단건 조회 | GET | `/users/42` |
| 생성 | POST | `/users` |
| 전체 수정 | PUT | `/users/42` |
| 부분 수정 | PATCH | `/users/42` |
| 삭제 | DELETE | `/users/42` |

→ A, B, D 는 모두 동사를 URL 에 넣음 → RPC 스타일.

</details>

### Q3. (개념) PUT 과 PATCH 의 차이?

<details><summary>정답</summary>

- **PUT**: 자원 **전체 교체**. 보내지 않은 필드는 null/default 가 된다고 봐야.
- **PATCH**: **부분 수정**. 보낸 필드만 변경.

```http
# PUT - 전체 교체
PUT /api/users/42
{ "name": "kim", "email": "kim@a.com", "age": 30 }
# -> name, email, age 모두 이 값으로 (안 보낸 필드는 null/default)

# PATCH - 일부만
PATCH /api/users/42
{ "email": "new@a.com" }
# -> email 만 변경, name/age 는 그대로
```

**멱등성 (Idempotency)**:
- PUT: 멱등 - 같은 요청 100번 보내도 결과 동일
- PATCH: 보통 멱등이 아님 (구현에 따라)

**실무**:
- 사용자 프로필 수정 → PATCH (대부분 일부 필드만)
- 설정 객체 전체 교체 → PUT

```java
@PatchMapping("/api/users/{id}")
public User update(@PathVariable long id, @RequestBody UserUpdateReq req) { ... }
```

</details>

### Q4. (개념) HTTP 메서드 중 "안전(safe)" 한 것과 "멱등(idempotent)" 한 것을 모두 고르시오.

<details><summary>정답</summary>

| 메서드 | 안전 (safe) | 멱등 (idempotent) | 의미 |
|--|--|--|--|
| **GET** | O | O | 조회 |
| **HEAD** | O | O | 헤더만 |
| **OPTIONS** | O | O | 메서드 확인 (CORS preflight) |
| **PUT** | X | O | 전체 교체 |
| **DELETE** | X | O | 삭제 |
| **POST** | X | X | 생성 (id 자동 발급) |
| **PATCH** | X | 보통 X | 부분 수정 |

**정의**:
- **안전 (Safe)**: 서버 상태를 변경하지 않음 (조회 전용)
- **멱등 (Idempotent)**: 같은 요청을 N번 보내도 결과 동일

**예시**:
```
DELETE /api/users/42
- 1번째: 사용자 삭제됨, 200 OK
- 2번째: 이미 없음, 404 또는 204 - "최종 상태" 는 같음 -> 멱등
```

```
POST /api/users
- 1번째: 사용자 1 생성
- 2번째: 사용자 2 생성 (id 다름) -> 비멱등
```

**왜 중요?**:
- **재시도 안전성**: 멱등하면 네트워크 실패 시 안심하고 재시도
- **캐시**: 안전한 메서드만 캐시 가능
- **HTTP 표준 준수**: 프록시·캐시·로깅이 의미를 알고 동작

</details>

### Q5. (개념) Spring 의 4가지 파라미터 어노테이션 - `@RequestBody`, `@RequestParam`, `@PathVariable`, `@ModelAttribute`?

<details><summary>정답</summary>

| 어노테이션 | 위치 | 예 |
|--|--|--|
| `@RequestBody` | HTTP body (JSON) | `POST /api/users` with `{"name":"kim"}` |
| `@RequestParam` | URL 쿼리 파라미터 | `GET /api/users?page=1&size=10` |
| `@PathVariable` | URL 경로 변수 | `GET /api/users/42` |
| `@ModelAttribute` | form-data 또는 query (객체 매핑) | `POST` form 데이터 |

**예제 - 한 컨트롤러에 모두**:
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    // GET /api/users/42
    @GetMapping("/{id}")
    public User get(@PathVariable long id) { ... }

    // GET /api/users?page=1&size=10
    @GetMapping
    public PageResult<User> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        return userService.list(page, size);
    }

    // POST /api/users    Body: {"email":"...", "password":"..."}
    @PostMapping
    public ResponseEntity<User> create(@RequestBody @Valid SignupReq req) { ... }

    // GET /api/users/search?keyword=kim&minAge=20  (객체 자동 매핑)
    @GetMapping("/search")
    public List<User> search(@ModelAttribute UserSearchCond cond) { ... }
}
```

**선택 가이드**:
- **REST API JSON 요청** → `@RequestBody`
- **검색·필터·페이지네이션** → `@RequestParam` (여러 개) 또는 `@ModelAttribute` (객체)
- **단일 자원 식별** → `@PathVariable`
- **전통적 HTML form** (Content-Type: application/x-www-form-urlencoded) → `@ModelAttribute`

⚠️ **흔한 함정**: GET 요청 + `@RequestBody` 는 안 됨 (GET 은 body 가 없음). 검색은 `@RequestParam` 또는 `@ModelAttribute`.

</details>

### Q6. (적용) `POST /api/boards` 로 게시글을 만들었다. 응답으로 가장 적절한 것은?

```
A) 200 OK
   { "id": 42, "title": "..." }
B) 201 Created
   Location: /api/boards/42
   { "id": 42, "title": "..." }
C) 204 No Content
D) 200 OK
   { "success": true, "data": { "id": 42 } }
```

<details><summary>정답</summary>

**B**. 자원 생성 = 201, 새 자원의 URL = `Location` 헤더. 클라이언트가 후속 GET 요청에 그대로 사용.

**Spring 구현**:
```java
@PostMapping
public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req) {
    Board saved = boardService.create(req);
    return ResponseEntity
        .created(URI.create("/api/boards/" + saved.getId()))   // 201 + Location
        .body(saved);
}
```

**왜 201 Created?**:
- HTTP 표준의 의미를 정확히 (자원 생성)
- 클라이언트가 매번 응답 본문 파싱 없이 status 만으로 판단 가능
- 모니터링 도구가 상태 코드로 자동 분류

**왜 Location 헤더?**:
- 새 자원의 URL 을 제공 → 클라이언트가 후속 작업 가능
- `GET ${Location}` 으로 상세 조회

**다른 옵션은 왜 안 좋은가**:
- **A (200 OK)**: 의미가 모호함. 200 은 일반 성공. 생성은 201 이 더 명확.
- **C (204 No Content)**: 본문 없음 → 클라이언트가 생성된 id 모름. PUT/DELETE 에 적합.
- **D**: 모든 응답을 200 으로 통일 + body 의 success 필드로 분기 → HTTP 의미 시스템 무력화 (Q14 참조).

</details>

### Q7. (적용) DELETE 의 적절한 응답 코드와 본문은?

<details><summary>정답</summary>

**가장 일반적 - 204 No Content (본문 없음)**:
```java
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable long id) {
    boardService.delete(id);
    return ResponseEntity.noContent().build();   // 204
}
```

응답:
```http
HTTP/1.1 204 No Content
```

**왜 204?**: "삭제됐고, 더 말할 것 없음". 본문이 비어있음을 명시.

**대안 - 200 OK + 메시지**:
```java
return ResponseEntity.ok(Map.of("deleted", true, "id", id));
```
- 클라이언트가 추가 정보 필요할 때
- "삭제된 항목의 백업" 같은 데이터 반환

**삭제 실패 케이스**:
- **404 Not Found**: 자원이 없음
- **403 Forbidden**: 권한 없음
- **409 Conflict**: 삭제할 수 없는 상태 (예: 자식이 있음)

```java
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(
        @PathVariable long id,
        @AuthenticationPrincipal User user) {
    int affected = boardService.delete(id, user.getId());
    if (affected == 0) {
        // 본인 글이 아니거나 이미 삭제됨
        throw new ForbiddenException("권한 없음 또는 이미 삭제됨");
    }
    return ResponseEntity.noContent().build();
}
```

**멱등성**: DELETE 는 멱등이지만 응답이 다를 수 있음:
- 1번째: 200/204 (실제 삭제)
- 2번째: 404 (이미 없음) - 표준에선 둘 다 OK

**실무 권장**: 멱등성을 유지하려면 두 번째도 204 반환 (이미 없으면 → 원하는 최종 상태).

</details>

### Q8. (적용) Bean Validation 으로 다음을 만족하는 record DTO 를 작성하시오.
- `email`: 이메일 형식, 빈 값 불가
- `password`: 길이 8~64
- `nickname`: 빈 값 불가, 최대 20자

<details><summary>정답</summary>

```java
public record SignupReq(
    @NotBlank @Email String email,
    @Size(min = 8, max = 64) String password,
    @NotBlank @Size(max = 20) String nickname
) {}
```

**컨트롤러 사용**:
```java
@PostMapping("/api/signup")
public ResponseEntity<User> signup(@RequestBody @Valid SignupReq req) {
    User saved = userService.signup(req);
    return ResponseEntity.status(201).body(saved);
}
```

**검증 실패 시 자동 동작**:
- Spring 이 `MethodArgumentNotValidException` 던짐
- 전역 핸들러가 400 응답 + 필드별 에러 메시지

**자주 쓰는 Validation 어노테이션**:

| 어노테이션 | 대상 | 의미 |
|--|--|--|
| `@NotNull` | 모든 타입 | null 불가 (빈 문자열 OK) |
| `@NotEmpty` | String/Collection | null + size 0 불가 |
| `@NotBlank` | String | null + trim 후 empty 불가 |
| `@Size(min, max)` | String/Collection | 길이 |
| `@Min` / `@Max` | 숫자 | 값 범위 |
| `@Positive` / `@Negative` | 숫자 | 부호 |
| `@Email` | String | 이메일 형식 |
| `@Pattern(regexp)` | String | 정규식 |
| `@Valid` | 객체 | 중첩 객체 검증 |

**커스텀 검증**:
```java
@Target({ ElementType.FIELD })
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = StrongPasswordValidator.class)
public @interface StrongPassword {
    String message() default "강한 비밀번호가 아닙니다";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

</details>

### Q9. (개념) `@RestController` 와 `@Controller` 의 차이?

<details><summary>정답</summary>

```
@RestController  =  @Controller + @ResponseBody
```

| | `@Controller` | `@RestController` |
|--|--|--|
| 반환값 처리 | ViewName (JSP/Thymeleaf 로 매핑) | HttpMessageConverter (JSON/XML 직렬화) |
| `@ResponseBody` | 메서드별로 명시 필요 | 자동 적용 |
| 용도 | 전통 MVC (서버 사이드 렌더) | REST API |

**`@Controller`**:
```java
@Controller
public class BoardController {

    @GetMapping("/board/{id}")
    public String detail(@PathVariable long id, Model model) {
        model.addAttribute("board", service.findById(id));
        return "board/detail";     // -> /WEB-INF/views/board/detail.jsp 렌더
    }

    @GetMapping("/api/board/{id}")
    @ResponseBody              // 명시적 추가
    public Board detailJson(@PathVariable long id) {
        return service.findById(id);   // JSON 반환
    }
}
```

**`@RestController`**:
```java
@RestController              // 모든 메서드가 자동 @ResponseBody
@RequestMapping("/api/boards")
public class BoardApi {

    @GetMapping("/{id}")
    public Board detail(@PathVariable long id) {
        return service.findById(id);   // JSON 자동
    }

    @GetMapping
    public List<Board> list() {
        return service.findAll();      // JSON 자동
    }
}
```

**언제 무엇?**:
- 서버에서 HTML 렌더 (JSP, Thymeleaf) → `@Controller`
- JSON 응답 (Vue/React 가 호출) → `@RestController`
- 같은 컨트롤러에서 둘 다 → `@Controller` + 메서드별 `@ResponseBody`

**현대 추세**: SPA + REST API → `@RestController` 가 압도적.

</details>

### Q10. (디버그) 클라이언트가 잘못된 JSON 본문을 보냈을 때 다음 핸들러가 동작하지 않는 이유?

```java
@ExceptionHandler(IllegalArgumentException.class)
public ResponseEntity<?> handle(IllegalArgumentException e) {
    return ResponseEntity.badRequest().body(e.getMessage());
}
```

<details><summary>정답</summary>

JSON 파싱 실패는 `HttpMessageNotReadableException`. `IllegalArgumentException` 이 아니다.

**Spring 의 검증 단계별 예외**:

| 시점 | 예외 | 처리 |
|--|--|--|
| **JSON 파싱 실패** | `HttpMessageNotReadableException` | 400 - 잘못된 형식 |
| **타입 변환 실패** (`@PathVariable long id` 에 "abc") | `MethodArgumentTypeMismatchException` | 400 |
| **`@Valid` 검증 실패** | `MethodArgumentNotValidException` | 400 - 필드별 메시지 |
| **`@RequestParam` 누락** | `MissingServletRequestParameterException` | 400 |
| **HTTP 메서드 불일치** | `HttpRequestMethodNotSupportedException` | 405 |
| **Content-Type 불일치** | `HttpMediaTypeNotSupportedException` | 415 |

**해결 - 각각 명시적으로 처리**:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> badJson(HttpMessageNotReadableException e) {
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("INVALID_JSON", "JSON 형식 오류"));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> validation(MethodArgumentNotValidException e) {
        Map<String, String> errors = e.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
        return ResponseEntity.badRequest().body(errors);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> fallback(Exception e) {
        log.error("Unhandled", e);
        return ResponseEntity.status(500).body(new ErrorResponse("INTERNAL", "서버 오류"));
    }
}
```

**일괄 처리 방법**: `@ExceptionHandler({A.class, B.class, C.class})` 또는 `Throwable` 까지 캐치.

</details>

### Q11. (적용) `@RestControllerAdvice` 로 다음 예외들을 처리하시오:
- `EntityNotFoundException` → 404
- `AccessDeniedException` → 403
- 그 외 → 500

<details><summary>정답</summary>

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(EntityNotFoundException e) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", e.getMessage()));
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> forbidden(AccessDeniedException e) {
        log.warn("Access denied: {}", e.getMessage());
        return ResponseEntity.status(403)
            .body(new ErrorResponse("FORBIDDEN", "권한이 없습니다"));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> unknown(Exception e) {
        log.error("Unhandled exception", e);     // 스택트레이스는 로그에만
        return ResponseEntity.status(500)
            .body(new ErrorResponse("INTERNAL_ERROR", "서버 오류"));   // 사용자엔 일반 메시지
    }
}

public record ErrorResponse(String code, String message) {}
```

**우선순위**: Spring 이 가장 **구체적인 예외 타입** 부터 매칭. 따라서:
- `EntityNotFoundException` → 첫 핸들러
- `AccessDeniedException` → 두 번째
- 그 외 (NPE, RuntimeException, IOException 등) → 세 번째 fallback

**보안 원칙**:
- 사용자에겐 **일반 메시지** ("서버 오류")
- 스택트레이스는 **로그에만** (`log.error("...", e)`)
- 에러 코드 (`"NOT_FOUND"`) 로 클라이언트 분기 가능하게

**테스트**:
```java
@Test
void notFound_returns404() throws Exception {
    when(service.findById(99L)).thenThrow(new EntityNotFoundException("없음"));

    mockMvc.perform(get("/api/boards/99"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.code").value("NOT_FOUND"));
}
```

</details>

### Q12. (디버그) 클라이언트가 받은 응답에 무엇이 잘못됐나? 두 가지.
```
500 Internal Server Error
{ "timestamp": "...", "path": "/api/boards", "trace": "java.lang.NullPointerException at ..." }
```

<details><summary>정답</summary>

**1. NPE 가 표면화**:
- 비즈니스 예외로 변환 안 됨
- Service 에서 null 검사 후 의미 있는 예외 던져야:
```java
Board board = boardMapper.findById(id);
if (board == null) throw new EntityNotFoundException("게시글 " + id + " 없음");
```
- 또는 `Optional` 사용:
```java
return Optional.ofNullable(boardMapper.findById(id))
    .orElseThrow(() -> new EntityNotFoundException("..."));
```

**2. 스택트레이스 노출 (보안 사고)**:
- **위험**: 공격자에게 시스템 정보 제공
  - 패키지 구조 (`com.ssafy.board.service.BoardService`)
  - 라이브러리 버전
  - 코드 결함 위치
- **해결**: 운영 환경에서는 일반 메시지만, 스택트레이스는 로그에만.

```yaml
# application-prod.yml
server.error:
  include-stacktrace: never            # 응답에 스택트레이스 X
  include-message: never               # 예외 메시지도 X (옵션)
  include-binding-errors: never
```

**올바른 응답 예**:
```json
500 Internal Server Error
{
    "code": "INTERNAL_ERROR",
    "message": "서버 오류가 발생했습니다",
    "requestId": "req-abc-123"
}
```

**서버 로그에는**:
```
2026-05-20 14:30:22 ERROR [req-abc-123] Unhandled exception
java.lang.NullPointerException
    at com.ssafy.board.service.BoardService.findById(BoardService.java:42)
    ...
```

→ 운영자가 `requestId` 로 로그에서 상세 확인 가능.

**OWASP 권장**: 에러 응답에 시스템 정보 절대 노출 X.

</details>

### Q13. (디버그) CORS 가 막혀서 Vue 앱이 Spring API 를 호출 못 할 때 해결법?

<details><summary>정답</summary>

**증상**:
```
Access to fetch at 'http://localhost:8080/api/boards' from origin
'http://localhost:5173' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present
```

**해결 1: 글로벌 CORS 설정** (`WebMvcConfigurer`):
```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:5173", "https://myapp.com")
            .allowedMethods("GET", "POST", "PUT", "PATCH", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)             // 쿠키·인증 헤더 허용
            .maxAge(3600);                       // preflight 캐시
    }
}
```

**해결 2: 컨트롤러별 어노테이션**:
```java
@CrossOrigin(origins = "http://localhost:5173", allowCredentials = "true")
@RestController
public class BoardApi { ... }
```

**해결 3: Spring Security 환경**:
```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration cfg = new CorsConfiguration();
    cfg.setAllowedOrigins(List.of("http://localhost:5173"));
    cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    cfg.setAllowedHeaders(List.of("*"));
    cfg.setAllowCredentials(true);

    UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/**", cfg);
    return src;
}

@Bean
public SecurityFilterChain security(HttpSecurity http) throws Exception {
    http.cors(Customizer.withDefaults())     // CORS 활성화
        .csrf(c -> c.disable());              // REST API 면 CSRF off
    return http.build();
}
```

**CORS Preflight (OPTIONS)**:
- 브라우저가 실제 요청 전에 OPTIONS 요청으로 "이 origin/method 허용되나?" 확인
- 비표준 헤더 (Authorization 등) 사용 시 자동 트리거
- `maxAge` 설정으로 캐시 가능

**개발 시 대안**: Vite proxy 로 CORS 우회.

⚠️ **`allowedOrigins("*")` + `allowCredentials(true)` 는 호환 X** - 보안 위험. 명시적 origin 만.

</details>

### Q14. (면접) "왜 모든 응답을 200 OK 로 통일하고 body 에 `success` 필드로 구분하면 안 되나요?"

<details><summary>정답</summary>

**안 좋은 패턴 (안티 패턴)**:
```http
200 OK
{ "success": false, "error": "NOT_FOUND", "data": null }
```

**문제점**:

1. **HTTP 의 의미 시스템(상태 코드) 을 무력화**
   - 클라이언트가 매번 본문을 파싱해서 분기해야
   - `if (response.success)` 같은 추가 코드 매번

2. **캐시·프록시·모니터링이 상태 코드를 못 읽음**
   - CDN/Reverse Proxy 가 4xx 에러를 캐시하지 말아야 하는데, 200 이면 잘못 캐시
   - CloudWatch / DataDog 의 "5xx 비율 > 1%" 알람 동작 안 함
   - APM 도구가 에러 추적 불가

3. **표준 HTTP 클라이언트의 이점 상실**
   - `axios` 의 `error` 콜백, `fetch` 의 `response.ok`, Retrofit 의 자동 예외화 모두 4xx/5xx 가정
   - 200 으로 통일하면 → 모든 응답을 200 으로 받고 body 파싱 후 다시 throw 해야

4. **OpenAPI/Swagger 문서화 약화**
   - "이 API 는 항상 200 반환" → 의미 없는 문서
   - 클라이언트 코드 생성 도구도 무력

5. **테스트·디버깅 어려움**
   - "왜 안 되지?" → 200 인데 success=false → 한 단계 더 파야 함

**옳은 패턴**:
```http
404 Not Found
{ "code": "NOT_FOUND", "message": "게시글이 없습니다" }
```

```js
// 클라이언트 - 표준 패턴
try {
    const res = await fetch('/api/boards/999');
    if (!res.ok) throw new ApiError(await res.json());
    const data = await res.json();
} catch (e) {
    // 자동으로 에러 처리
}
```

**반론**: "프론트가 매번 try-catch 해야 해서 200 으로 통일이 편하다"
**답변**: 표준 HTTP 클라이언트 (axios, fetch wrapper) 가 4xx/5xx 를 자동으로 throw 함. 한 곳에서 처리 가능.

→ **표준이 곧 비용 절감**. HTTP 상태 코드 정확히 사용은 RESTful 의 기본.

</details>

### Q15. (면접) REST API 의 버저닝 방식 3가지와 각각의 trade-off?

<details><summary>정답</summary>

| 방식 | 예시 | 장점 | 단점 |
|--|--|--|--|
| **URI 버저닝** | `/api/v1/users` | 명확, 캐시·로깅 친화, 디버깅 쉬움 | URL 이 영구적이지 못함 (RESTful 원칙 위배 주장) |
| **쿼리 파라미터** | `/api/users?v=1` | URL 그대로 유지 | 캐시 키 헷갈림, 헤매기 쉬움, 잘 안 씀 |
| **헤더 (Accept)** | `Accept: application/vnd.myapi.v1+json` | RESTful 가장 부합, URL 깔끔 | 디버깅 어려움, 브라우저로 직접 호출 불편, 캐시 복잡 |

**실무는 URI 방식이 압도적**:
```
GET /api/v1/users/42
GET /api/v2/users/42      (breaking change 발생 시 신설)
```

**v2 출시 시**:
1. `/api/v1` 유지 + `/api/v2` 신설
2. 6 개월~1 년 deprecation 기간 알림
3. v1 응답 헤더에 `Deprecation: true`, `Sunset: 2026-12-31`
4. 모든 클라이언트 v2 이동 후 v1 제거

**언제 버저닝이 필요한가?**:

- **Breaking change** = 버저닝
  - 응답 필드 제거 또는 이름 변경
  - 필수 파라미터 추가
  - 인증 방식 변경
  - 의미 변경 (`status: 1` 이 `ACTIVE` 였는데 `INACTIVE` 로)

- **Non-breaking change** = 같은 버전 유지
  - 새 필드 추가 (옵셔널)
  - 새 엔드포인트 추가
  - 성능 개선

**버전 없이 시작하는 방법**:
- 모바일 앱: 자동 업데이트 → 버전 강제 가능
- 내부 API: 클라이언트가 한정적 → 버전 불필요

**큰 회사 사례**:
- Stripe: `Stripe-Version: 2023-08-16` 헤더 (날짜 기반)
- GitHub: `/v3/`, `/v4/` URI
- Twitter: `/2/` URI + 옛 `/1.1/` 유지

**조언**: 처음부터 `/api/v1` 로 시작. 나중에 추가하기보단 처음부터 있는 게 자연스러움.

</details>
