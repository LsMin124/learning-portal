# Spring MVC 2 — 치트시트

> 32p 슬라이드 · MVC 심화. JSON 응답·예외·파일 업로드·Validation.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **HttpMessageConverter** 가 자바 객체 ↔ JSON 자동 변환 (Jackson)
2. **`@RestController` + `ResponseEntity`** = REST API 의 표준 패턴
3. **`@Valid` + Bean Validation** 으로 입력 검증, 실패 시 `MethodArgumentNotValidException`
4. **`@RestControllerAdvice`** 로 전역 예외 처리 (try-catch 컨트롤러에 X)
5. **`MultipartFile`** 로 파일 업로드 받음, 실제 저장은 S3/스토리지 + URL 만 DB
6. **HTTP 상태 코드 정확히**: 200 / 201 (Created) / 204 (No Content) / 400 / 401 / 403 / 404 / 500

## 가장 중요한 코드 3개

```java
// (1) REST API + Validation + 응답
@RestController
@RequestMapping("/api/boards")
@RequiredArgsConstructor
public class BoardApi {

    private final BoardService service;

    @PostMapping
    public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req) {
        Board saved = service.create(req);
        return ResponseEntity
            .created(URI.create("/api/boards/" + saved.getId()))
            .body(saved);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();   // 204
    }
}
```

```java
// (2) 전역 예외 처리
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> validation(
            MethodArgumentNotValidException e) {
        Map<String, String> errors = e.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
        return ResponseEntity.badRequest().body(errors);
    }

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(EntityNotFoundException e) {
        return ResponseEntity.status(404).body(new ErrorResponse("NOT_FOUND", e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> fallback(Exception e) {
        log.error("Unhandled", e);
        return ResponseEntity.status(500).body(new ErrorResponse("INTERNAL", "서버 오류"));
    }
}
```

```java
// (3) 파일 업로드
@PostMapping("/upload")
public ResponseEntity<String> upload(@RequestParam("file") MultipartFile file) throws IOException {
    String filename = UUID.randomUUID() + "_" + file.getOriginalFilename();
    Path path = Paths.get("/uploads", filename);
    file.transferTo(path);
    return ResponseEntity.ok("/uploads/" + filename);
}
```

## 면접 한 줄 답변
- **HttpMessageConverter 의 역할?** → 자바 객체 ↔ HTTP body (JSON/XML) 변환. Jackson 이 기본.
- **@RestController vs ResponseEntity?** → @RestController 는 모든 메서드 자동 @ResponseBody. ResponseEntity 로 상태·헤더 제어.
- **전역 예외 처리의 이점?** → 컨트롤러에 try-catch 반복 X + 일관된 에러 응답 + 운영 로깅 통합.
- **파일을 DB BLOB 에 저장?** → 비권장. URL 만 DB, 실체는 S3 등 객체 스토리지.

---

# 2. Quick Reference (실무 복붙)

## HttpMessageConverter

```java
// 자동 변환 (Jackson)
@RestController
public class BoardApi {

    @PostMapping("/api/boards")
    public Board create(@RequestBody BoardReq req) {   // JSON -> Java
        return service.create(req);                     // Java -> JSON
    }
}
```

설정:
```yaml
spring.jackson:
  date-format: yyyy-MM-dd HH:mm:ss
  time-zone: Asia/Seoul
  default-property-inclusion: non_null     # null 필드 제외
  property-naming-strategy: SNAKE_CASE     # userName -> user_name
```

## ResponseEntity

```java
// 200 OK
return ResponseEntity.ok(data);

// 201 Created + Location
return ResponseEntity
    .created(URI.create("/api/boards/" + id))
    .body(saved);

// 204 No Content (DELETE)
return ResponseEntity.noContent().build();

// 400 Bad Request
return ResponseEntity.badRequest().body(errors);

// 404 Not Found
return ResponseEntity.notFound().build();

// 헤더 + 상태 + 본문
return ResponseEntity.status(HttpStatus.OK)
    .header("X-Total-Count", String.valueOf(total))
    .contentType(MediaType.APPLICATION_JSON)
    .body(list);
```

## Bean Validation

```java
public record BoardCreateReq(
    @NotBlank @Size(max = 200) String title,
    @NotBlank String content,
    @Email String email,
    @Positive Integer count,
    @Pattern(regexp = "[A-Z]+") String code
) {}

@PostMapping
public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req) {
    // 검증 실패 시 MethodArgumentNotValidException 자동 발생
}
```

자주 쓰는 어노테이션:
- `@NotNull` / `@NotEmpty` / `@NotBlank`
- `@Size(min, max)` / `@Min` / `@Max` / `@Positive`
- `@Email` / `@Pattern(regexp)`
- `@Past` / `@Future`
- `@Valid` (중첩 객체)

## 전역 예외 처리

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 1. Validation 실패
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> validation(MethodArgumentNotValidException e) {
        Map<String, String> errors = new HashMap<>();
        e.getBindingResult().getFieldErrors().forEach(err ->
            errors.put(err.getField(), err.getDefaultMessage()));
        return ResponseEntity.badRequest().body(errors);
    }

    // 2. JSON 파싱 실패
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> badJson(HttpMessageNotReadableException e) {
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("INVALID_JSON", "JSON 형식 오류"));
    }

    // 3. 비즈니스 예외
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(EntityNotFoundException e) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", e.getMessage()));
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> forbidden(AccessDeniedException e) {
        return ResponseEntity.status(403)
            .body(new ErrorResponse("FORBIDDEN", "권한 없음"));
    }

    // 4. Fallback (반드시 마지막)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> unhandled(Exception e) {
        log.error("Unhandled", e);
        return ResponseEntity.status(500)
            .body(new ErrorResponse("INTERNAL_ERROR", "서버 오류"));
    }
}

public record ErrorResponse(String code, String message) {}
```

## 파일 업로드

```java
@PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
public ResponseEntity<UploadRes> upload(
        @RequestParam("file") MultipartFile file,
        @RequestParam(required = false) String description) throws IOException {

    if (file.isEmpty()) {
        return ResponseEntity.badRequest().build();
    }
    if (file.getSize() > 10 * 1024 * 1024) {
        return ResponseEntity.status(413).build();   // Payload Too Large
    }

    String ext = StringUtils.getFilenameExtension(file.getOriginalFilename());
    String filename = UUID.randomUUID() + "." + ext;
    Path target = Paths.get("/uploads", filename);
    Files.createDirectories(target.getParent());
    file.transferTo(target);

    return ResponseEntity.ok(new UploadRes(filename, "/uploads/" + filename));
}
```

```yaml
# 설정
spring.servlet.multipart:
  max-file-size: 10MB
  max-request-size: 50MB
  enabled: true
```

## HTTP 상태 코드 (자주 쓰는 것)

| 코드 | 의미 | 사용 |
|--|--|--|
| **200** | OK | 일반 성공 |
| **201** | Created | POST 자원 생성 (+ Location 헤더) |
| **204** | No Content | DELETE 성공 (본문 없음) |
| **301** | Moved Permanently | 영구 리다이렉트 |
| **302** | Found | 임시 리다이렉트 (sendRedirect) |
| **400** | Bad Request | 잘못된 요청 (Validation 실패) |
| **401** | Unauthorized | 인증 실패 |
| **403** | Forbidden | 권한 없음 |
| **404** | Not Found | 자원 없음 |
| **405** | Method Not Allowed | HTTP 메서드 불일치 |
| **409** | Conflict | 충돌 (UNIQUE 위반 등) |
| **415** | Unsupported Media Type | Content-Type 불일치 |
| **500** | Internal Server Error | 서버 예외 |

## 비동기 (`@Async`)

```java
@SpringBootApplication
@EnableAsync
public class MyApp { }

@Service
public class MailService {
    @Async
    public CompletableFuture<Void> sendAsync(String to) {
        // 별도 스레드에서 실행
        return CompletableFuture.completedFuture(null);
    }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `@RestController` 면서 view name 반환 | `@Controller` 또는 ResponseEntity |
| 전역 핸들러 fallback 빠짐 | `@ExceptionHandler(Exception.class)` 마지막에 |
| Validation 메시지 한국어 | `messages_ko.properties` |
| 파일을 DB BLOB | 비권장 - URL 만 DB |
| 같은 origin 가정 | CORS 명시 설정 |
| 200 으로 통일 + body 의 success 필드 | HTTP 상태 코드 정확히 사용 |
| stacktrace 응답 노출 | 운영에선 일반 메시지 + 로그에 stacktrace |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Spring MVC 2 (32p)
│
├── [A] HttpMessageConverter
│   ├── Jackson (JSON 기본)
│   ├── XML / Form / String
│   ├── @RequestBody / @ResponseBody
│   └── ContentNegotiation
│
├── [B] ResponseEntity
│   ├── 상태 코드
│   ├── 헤더 (Location, Content-Type)
│   ├── 본문 (DTO)
│   └── 빌더 패턴
│
├── [C] Bean Validation
│   ├── @NotBlank / @Size / @Email / @Pattern
│   ├── @Valid (중첩)
│   ├── @Validated (그룹)
│   └── 커스텀 ConstraintValidator
│
├── [D] 예외 처리
│   ├── @ExceptionHandler (메서드 단위)
│   ├── @RestControllerAdvice (전역)
│   ├── 우선순위 (구체적 > 일반)
│   └── 보안 (stacktrace 숨김)
│
├── [E] 파일 업로드
│   ├── MultipartFile
│   ├── consumes MULTIPART_FORM_DATA
│   ├── 크기 제한 (application.yml)
│   └── S3 vs 로컬
│
├── [F] HTTP 상태 코드
│   ├── 2xx (200/201/204)
│   ├── 3xx (301/302)
│   ├── 4xx (400/401/403/404)
│   └── 5xx (500)
│
└── [G] 비동기
    ├── @Async
    ├── @EnableAsync
    └── CompletableFuture
```

## 학습 진도 체크리스트

### A. JSON
- [ ] HttpMessageConverter 동작
- [ ] Jackson 설정 (date-format, snake_case)
- [ ] @ResponseBody 자동 직렬화

### B. ResponseEntity
- [ ] 200/201/204/400/404/500 별 작성
- [ ] Location 헤더 (POST 후)
- [ ] noContent / badRequest 빌더

### C. Validation
- [ ] @Valid 사용
- [ ] 어노테이션 종류 (NotBlank/Size/Email)
- [ ] 검증 실패 시 자동 예외

### D. 예외
- [ ] @RestControllerAdvice 작성
- [ ] 주요 예외 4종 (Validation, JsonParse, BusinessEx, Fallback)
- [ ] 우선순위 (구체적 먼저)

### E. 파일
- [ ] MultipartFile 사용
- [ ] 크기 제한 설정
- [ ] S3 업로드 패턴

### F. 상태 코드
- [ ] 201 vs 200 (POST)
- [ ] 204 (DELETE)
- [ ] 401 vs 403 차이

## 연관 강의

```
5강 MVC1            -> Controller 기본
6강 MVC2            <- 현재 위치
7강 Interceptor     -> 인증
12강 REST API       -> 심화
14강 CORS PJT       -> 통합
```

→ 다음 (Interceptor) 에서 **컨트롤러 진입 전 가로채기 (인증)**.
