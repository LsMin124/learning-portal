# REST API — 치트시트

> Spring REST API 심화. HTTP 메서드·상태 코드·CORS·버저닝.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **REST 원칙**: 자원 = 명사 (복수형), 동작 = HTTP 메서드 (GET/POST/PUT/PATCH/DELETE)
2. **Stateless**: 서버가 클라이언트 상태 기억 X. 매 요청에 인증 정보 동봉 (JWT)
3. **HTTP 상태 코드 정확히**: 201 (Created+Location), 204 (No Content), 401/403/404 구분
4. **PUT vs PATCH**: 전체 교체 vs 부분 수정
5. **CORS**: 다른 origin 의 fetch 차단 → 백엔드 Access-Control-Allow-Origin 또는 Vite proxy
6. **버저닝**: URI 방식 (`/api/v1/users`) 이 가장 흔함

## 가장 중요한 코드 3개

```java
// (1) 표준 REST 컨트롤러
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserApi {

    @GetMapping
    public List<User> list() { ... }

    @GetMapping("/{id}")
    public ResponseEntity<User> detail(@PathVariable long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<User> create(@RequestBody @Valid SignupReq req) {
        User saved = userService.signup(req);
        return ResponseEntity
            .created(URI.create("/api/v1/users/" + saved.getId()))
            .body(saved);
    }

    @PatchMapping("/{id}")
    public User update(@PathVariable long id, @RequestBody UserUpdateReq req) {
        return userService.update(id, req);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();   // 204
    }
}
```

```java
// (2) CORS 글로벌 설정
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:5173", "https://myapp.com")
            .allowedMethods("GET", "POST", "PUT", "PATCH", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

```java
// (3) 전역 예외 (Q&A 형식)
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(EntityNotFoundException e) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", e.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> validation(MethodArgumentNotValidException e) {
        Map<String, String> errors = e.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
        return ResponseEntity.badRequest().body(errors);
    }
}
```

## 면접 한 줄 답변
- **REST Stateless 의미?** → 서버가 클라이언트 상태 기억 X. 매 요청에 인증 정보 동봉. 수평 확장·캐시 용이.
- **PUT vs PATCH?** → PUT 전체 교체 (멱등), PATCH 부분 수정.
- **200 통일 + success 필드의 문제?** → HTTP 상태 코드 의미 시스템 무력화. 캐시·모니터링·라이브러리 자동화 손해.
- **REST 한계?** → "동사적" 액션 (예: 결제 환불) 표현 어색. 일부는 RPC 가 자연스럽기도.

---

# 2. Quick Reference (실무 복붙)

## RESTful URL 원칙

```
/api/users                          GET    - 전체 조회
/api/users                          POST   - 생성
/api/users/{id}                     GET    - 단건 조회
/api/users/{id}                     PUT    - 전체 교체
/api/users/{id}                     PATCH  - 부분 수정
/api/users/{id}                     DELETE - 삭제

/api/users/{id}/posts               GET    - 사용자의 글 목록
/api/users/{id}/posts/{postId}      GET    - 단건
```

**원칙**:
- **명사** (`users`, `boards`), 동사 X (`getUser`)
- **복수형** (`/users` not `/user`)
- **계층 구조** (`/users/{id}/posts/{postId}`)
- **동작은 HTTP 메서드**

## HTTP 메서드 의미

| 메서드 | 안전 | 멱등 | 용도 |
|--|--|--|--|
| **GET** | O | O | 조회 |
| **HEAD** | O | O | 헤더만 |
| **OPTIONS** | O | O | CORS preflight |
| **POST** | X | X | 생성 (id 자동) |
| **PUT** | X | O | 전체 교체 |
| **PATCH** | X | (보통 X) | 부분 수정 |
| **DELETE** | X | O | 삭제 |

## HTTP 상태 코드

| 코드 | 의미 | 사용 |
|--|--|--|
| **200** OK | 일반 성공 | GET |
| **201** Created | 자원 생성 + Location 헤더 | POST |
| **204** No Content | 본문 없음 | DELETE, PUT (옵션) |
| **301** Moved Permanently | 영구 리다이렉트 | URL 변경 |
| **302** Found | 임시 리다이렉트 | sendRedirect |
| **400** Bad Request | 잘못된 요청 | Validation 실패 |
| **401** Unauthorized | 인증 실패 | 토큰 없음/만료 |
| **403** Forbidden | 권한 없음 | 인증은 됐지만 권한 X |
| **404** Not Found | 자원 없음 | id 조회 실패 |
| **405** Method Not Allowed | 메서드 불일치 | GET 자리에 POST |
| **409** Conflict | 충돌 | UNIQUE 위반 |
| **415** Unsupported Media Type | Content-Type 불일치 | XML 인데 JSON |
| **422** Unprocessable Entity | 의미 오류 | 비즈니스 규칙 위반 |
| **429** Too Many Requests | Rate limit | 요청 횟수 초과 |
| **500** Internal Server Error | 서버 예외 | NPE 등 |
| **502** Bad Gateway | 게이트웨이 오류 | Nginx → 죽은 백엔드 |
| **503** Service Unavailable | 서비스 불가 | 점검·과부하 |

## ResponseEntity 패턴

```java
// 200 + body
return ResponseEntity.ok(data);

// 201 + Location + body
return ResponseEntity
    .created(URI.create("/api/users/" + id))
    .body(saved);

// 204
return ResponseEntity.noContent().build();

// 400
return ResponseEntity.badRequest().body(errors);

// 404
return ResponseEntity.notFound().build();

// 헤더 + 상태 + body
return ResponseEntity.status(200)
    .header("X-Total-Count", String.valueOf(total))
    .header("X-Page", String.valueOf(page))
    .body(items);
```

## CORS

```java
// 글로벌 (WebMvcConfigurer)
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:5173")
            .allowedMethods("GET", "POST", "PUT", "PATCH", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)        // 쿠키 허용
            .maxAge(3600);                 // preflight 캐시 (초)
    }
}

// 컨트롤러별
@CrossOrigin(origins = "http://localhost:5173", allowCredentials = "true")
@RestController
public class BoardApi { ... }

// Spring Security 환경
@Bean
public SecurityFilterChain security(HttpSecurity http) throws Exception {
    http.cors(Customizer.withDefaults())   // CORS 활성화
        .csrf(c -> c.disable());           // REST API 면 CSRF off
    return http.build();
}
```

⚠️ `allowedOrigins("*")` + `allowCredentials(true)` 는 호환 X.

## 버저닝

```java
// URI 방식 (가장 흔함)
@RequestMapping("/api/v1/users")        // v1
@RequestMapping("/api/v2/users")        // v2 (breaking change)

// 헤더 방식
@RequestMapping(value = "/api/users",
    headers = "X-API-Version=v1")

// Accept 헤더
@RequestMapping(value = "/api/users",
    produces = "application/vnd.myapi.v1+json")
```

**Deprecation**:
```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

## 페이지네이션 응답

```java
@GetMapping
public PageResult<BoardListItem> list(
        @RequestParam(defaultValue = "1") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(required = false) String keyword) {
    return service.search(page, size, keyword);
}

public record PageResult<T>(
    List<T> items,
    int total,
    int page,
    int size,
    boolean hasNext
) {}
```

또는 헤더로:
```java
return ResponseEntity.ok()
    .header("X-Total-Count", String.valueOf(total))
    .header("X-Has-Next", String.valueOf(hasNext))
    .body(items);
```

## 표준 에러 응답

```java
public record ErrorResponse(
    String code,           // "NOT_FOUND"
    String message,        // 사용자용 메시지
    String requestId,      // 로그 추적
    Instant timestamp
) {}

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(EntityNotFoundException e,
                                                    HttpServletRequest req) {
        return ResponseEntity.status(404).body(new ErrorResponse(
            "NOT_FOUND",
            e.getMessage(),
            (String) req.getAttribute("requestId"),
            Instant.now()
        ));
    }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| POST 자원 생성에 200 OK | 201 Created + Location |
| DELETE 후 body 반환 | 204 No Content |
| 200 으로 통일 + success 필드 | HTTP 상태 코드 정확히 |
| `@RequestBody` 에 GET | GET 은 body 없음 → @RequestParam |
| stacktrace 응답 노출 | 사용자엔 일반 메시지 |
| CORS `*` + credentials | 명시적 origin |
| 401 vs 403 혼동 | 401=인증 실패, 403=권한 부족 |
| URI 에 동사 | 명사 + HTTP 메서드 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
REST API
│
├── [A] REST 원칙
│   ├── 자원 = 명사 (복수형)
│   ├── 동작 = HTTP 메서드
│   ├── Stateless
│   ├── 계층 구조
│   └── HATEOAS (선택)
│
├── [B] HTTP 메서드
│   ├── 안전 (GET/HEAD/OPTIONS)
│   ├── 멱등 (PUT/DELETE)
│   ├── PUT vs PATCH
│   └── POST 의 의미
│
├── [C] 상태 코드
│   ├── 2xx (200/201/204)
│   ├── 3xx (301/302)
│   ├── 4xx (400/401/403/404/409/415/429)
│   └── 5xx (500/502/503)
│
├── [D] Spring 매핑
│   ├── @RestController
│   ├── @RequestBody / @PathVariable / @RequestParam
│   ├── ResponseEntity
│   └── HttpMessageConverter
│
├── [E] CORS
│   ├── Same-Origin Policy
│   ├── Preflight (OPTIONS)
│   ├── Allow-Origin / Methods / Headers / Credentials
│   └── Spring Security 통합
│
├── [F] 버저닝
│   ├── URI (/v1/, /v2/)
│   ├── Header (Accept)
│   ├── Query (?v=1)
│   └── Deprecation / Sunset
│
└── [G] 에러 처리
    ├── @RestControllerAdvice
    ├── ErrorResponse (code, message)
    ├── 보안 (stack 숨김)
    └── requestId 로 로그 추적
```

## 학습 진도 체크리스트

### A. REST
- [ ] 자원·동작 분리
- [ ] Stateless 의 의미
- [ ] PUT vs PATCH

### B. 상태 코드
- [ ] 201 + Location 헤더
- [ ] 204 No Content (DELETE)
- [ ] 401 vs 403 차이
- [ ] 409 Conflict (UNIQUE)

### C. Spring
- [ ] 4 파라미터 어노테이션
- [ ] ResponseEntity 빌더
- [ ] HttpMessageConverter

### D. CORS
- [ ] Preflight OPTIONS
- [ ] addCorsMappings
- [ ] Vite proxy 대안

### E. 버저닝
- [ ] URI 방식
- [ ] Deprecation 헤더
- [ ] v1 / v2 동시 운영

### F. 에러
- [ ] 표준 ErrorResponse
- [ ] requestId 추적
- [ ] OWASP 보안 (stack 숨김)

## 연관 강의

```
5강 MVC1            -> Controller
6강 MVC2            -> JSON / Validation
11강 종합 실습      -> 통합
12강 REST API       <- 현재 위치
14강 CORS PJT       -> CORS + 페이지네이션 PJT
Front 1강 Vue       -> 클라이언트 (CORS 마주침)
```

→ 다음 (Spring Batch) 에서 **대용량 일괄 처리**.
