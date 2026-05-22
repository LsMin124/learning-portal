# REST API — Spring 으로 제대로 만들기 (5/19 강의)

> ⚠️ **참고**: 5/19 슬라이드 PDF 가 5/18 Spring 종합실습과 byte 동일한 중복본으로 캡처되어 원본 슬라이드 부재. 본 노트는 그 결손을 메우는 REST API 표준 학습 자료로, 5/19 자리에 정식 편성.
>
> **이 강의는 무엇인가**: HTTP 위에 자원을 다루는 표준 스타일 **REST** 의 원칙과, Spring MVC 의 `@RestController` / `ResponseEntity` / 검증 / 예외 처리 / 문서화로 그걸 실제로 짜는 법.
>
> **왜 배우는가**: 모든 모던 백엔드의 외부 인터페이스 90% 가 REST API. 일관된 API 는 클라이언트(웹/모바일/외부 시스템) 개발 속도·디버깅·문서화를 좌우. Spring CORS/Pagination 강의(5/22) 와 같이 보면 좋다.

---

## 들어가기 전에

- **선수**: Spring MVC 1·2, MyBatis (CRUD 한 번은 해본 가정).
- **마인드셋**: REST 는 "프로토콜"이 아니라 **스타일 가이드**. 강제는 없지만 안 지키면 클라이언트가 매번 헤맨다.

---

## 1. REST 의 6가지 원칙 (Roy Fielding 논문 요약)

| 원칙 | 의미 | 실무 |
|--|--|--|
| Client-Server | 클라이언트와 서버 분리 | 당연 |
| Stateless | 요청에 모든 정보. 서버가 클라 상태 안 기억 | 인증은 토큰/세션 |
| Cacheable | 응답에 캐시 가능 여부 명시 | `Cache-Control` 헤더 |
| Uniform Interface | 자원 식별·표현·자기 기술 메시지·HATEOAS | URI/HTTP 메서드/JSON/링크 |
| Layered System | 중간 프록시·게이트웨이 가능 | LB, CDN, API Gateway |
| (옵션) Code on Demand | 서버가 클라에 코드 전송 | JS 응답 — 거의 안 씀 |

실무에선 처음 4개 + URI·HTTP 메서드 컨벤션 = 충분.

## 2. 자원 중심 URI 설계

```
✓  GET    /api/boards               게시판 목록
✓  GET    /api/boards/42            특정 게시글
✓  POST   /api/boards               새 게시글
✓  PATCH  /api/boards/42            특정 게시글 수정
✓  DELETE /api/boards/42            특정 게시글 삭제
✓  GET    /api/boards/42/comments   42번 글의 댓글 목록

✗  GET    /api/getBoards            동사 X
✗  POST   /api/deleteBoard?id=42    동사 + 잘못된 메서드
✗  GET    /api/board_get/42         스네이크 케이스 X (관습은 kebab-case)
```

규칙: **명사(복수형)**, 계층 구조 = URL 경로, 동작 = HTTP 메서드.

## 3. HTTP 메서드 의미

| 메서드 | 의미 | 멱등 | 안전 |
|--|--|--|--|
| GET | 조회 | ✓ | ✓ |
| HEAD | 조회 헤더만 | ✓ | ✓ |
| OPTIONS | 허용 메서드 질의 | ✓ | ✓ |
| POST | 생성·임의 작업 | ✗ | ✗ |
| PUT | 전체 교체 | ✓ | ✗ |
| PATCH | 부분 수정 | ✗ (보통) | ✗ |
| DELETE | 삭제 | ✓ | ✗ |

**멱등**: 같은 요청을 N 번 보내도 결과 동일. 재시도 안전. **안전**: 서버 상태 변경 안 함.

## 4. HTTP 상태 코드 — 의미가 분명한 것만 골라 쓰기

| 코드 | 의미 | 언제 |
|--|--|--|
| 200 OK | 일반 성공 | GET 성공 |
| 201 Created | 자원 생성됨 | POST 후 (응답에 `Location` 헤더) |
| 204 No Content | 성공·응답 본문 없음 | DELETE 후 |
| 400 Bad Request | 클라 입력 오류 | 검증 실패 |
| 401 Unauthorized | 인증 안 됨 | 로그인 필요 |
| 403 Forbidden | 권한 없음 | 인증은 됐는데 권한 X |
| 404 Not Found | 자원 없음 | id 잘못 |
| 409 Conflict | 충돌 | 중복 가입, 동시 수정 |
| 422 Unprocessable Entity | 의미 오류 | 형식은 맞는데 비즈니스 위반 |
| 500 Internal Server Error | 서버 오류 | 예기치 못한 예외 |
| 503 Service Unavailable | 서버 일시 불가 | 점검·과부하 |

200/201/204 + 400/401/403/404 + 500 만 잘 써도 90% 커버.

## 5. Spring MVC 에서의 REST 구현

```java
@RestController                          // = @Controller + @ResponseBody
@RequestMapping("/api/boards")
@RequiredArgsConstructor
public class BoardApi {
    private final BoardService service;

    @GetMapping
    public PageResult<BoardListItem> list(@ModelAttribute BoardSearchCond cond) {
        return service.search(cond);
    }

    @GetMapping("/{id}")
    public Board one(@PathVariable long id) {
        return service.get(id);
    }

    @PostMapping
    public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req) {
        Board saved = service.create(req);
        return ResponseEntity
            .created(URI.create("/api/boards/" + saved.getId()))
            .body(saved);                            // 201 + Location
    }

    @PatchMapping("/{id}")
    public Board update(@PathVariable long id, @RequestBody @Valid BoardUpdateReq req) {
        return service.update(id, req);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();   // 204
    }
}
```

**핵심**:
- `@RestController` → 메서드 반환값이 JSON 직렬화 (Jackson)
- HTTP 메서드 어노테이션(`@GetMapping` 등) 으로 REST 컨벤션 시각화
- 상태 코드·헤더 제어가 필요한 곳만 `ResponseEntity`, 평범한 200 응답은 객체 직접 반환

## 6. 요청 본문 검증 — Bean Validation

```java
public record BoardCreateReq(
    @NotBlank @Size(max = 200) String title,
    @NotBlank String content,
    @Size(max = 10) List<@NotBlank @Size(max = 20) String> tags
) {}
```

컨트롤러:
```java
@PostMapping
public ResponseEntity<Board> create(@RequestBody @Valid BoardCreateReq req) { ... }
```

`@Valid` 실패 시 `MethodArgumentNotValidException` 자동 throw → `@RestControllerAdvice` 에서 400 응답으로 변환.

자주 쓰는 검증:
- `@NotNull` / `@NotBlank` / `@NotEmpty`
- `@Size(min, max)` (문자열/컬렉션 길이)
- `@Min` / `@Max` / `@Positive` / `@Negative`
- `@Email` / `@Pattern(regexp = ...)`
- `@Past` / `@Future` (날짜)
- 커스텀 제약: `@Constraint` + Validator 클래스

## 7. 전역 예외 → 표준 응답 변환

```java
public record ErrorResponse(String code, String message, Map<String, String> details) { }

@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> validation(MethodArgumentNotValidException e) {
        Map<String, String> details = e.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("VALIDATION_FAILED", "입력값이 올바르지 않습니다", details));
    }

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(NotFoundException e) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", e.getMessage(), null));
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> forbidden(AccessDeniedException e) {
        return ResponseEntity.status(403)
            .body(new ErrorResponse("FORBIDDEN", "권한이 없습니다", null));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> unknown(Exception e) {
        log.error("unhandled", e);
        return ResponseEntity.status(500)
            .body(new ErrorResponse("INTERNAL_ERROR", "서버 오류", null));
    }
}
```

**원칙**:
- 클라이언트는 **`code` 필드로 분기** (`message` 는 사용자 표시용, 변경 가능)
- 민감 정보 노출 금지 (스택트레이스, 내부 경로)
- 로깅은 500 만 ERROR, 4xx 는 WARN/INFO

## 8. Swagger / OpenAPI

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.x</version>
</dependency>
```

기동 후 `/swagger-ui.html` 자동. 어노테이션으로 풍부화:

```java
@Operation(summary = "게시판 목록 조회", description = "페이지네이션 + 검색 지원")
@ApiResponse(responseCode = "200", description = "성공")
@ApiResponse(responseCode = "400", description = "잘못된 파라미터")
@GetMapping
public PageResult<BoardListItem> list(...) { ... }
```

프론트엔드 개발자와의 협업 비용 70% 절감. 운영에선 access 제한 또는 환경별 비활성.

## 9. API 버저닝

```
/api/v1/boards          ← URI 버저닝 (가장 단순, 권장)
/api/boards?v=1         ← 쿼리 파라미터
/api/boards (Header)    ← 헤더 (Accept: application/vnd.myapi.v1+json)
```

Breaking change 만들 때 v2 새로 + v1 유지(deprecation 기간). 대부분 URI 방식이 무난.

---

## 10. 코드 깊게 — 회원·게시판 통합 REST API

회원가입 + 로그인 + 본인 글 수정 까지 한 흐름.

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserApi {
    private final UserService service;
    private final JwtIssuer jwt;

    @PostMapping
    public ResponseEntity<UserView> signup(@RequestBody @Valid SignupReq req) {
        long id = service.signup(req);
        return ResponseEntity
            .created(URI.create("/api/users/" + id))
            .body(service.view(id));
    }

    @PostMapping("/login")
    public TokenResponse login(@RequestBody @Valid LoginReq req) {
        User u = service.authenticate(req.id(), req.password());
        return new TokenResponse(jwt.issue(u), 3600);
    }

    @GetMapping("/me")
    public UserView me(@AuthenticationPrincipal User user) {
        return service.view(user.getId());
    }
}

@RestController
@RequestMapping("/api/boards")
@RequiredArgsConstructor
public class BoardApi {
    private final BoardService service;

    @PatchMapping("/{id}")
    public Board update(@PathVariable long id,
                         @RequestBody @Valid BoardUpdateReq req,
                         @AuthenticationPrincipal User user) {
        return service.updateOwn(id, req, user.getId());
    }
}

public record SignupReq(
    @NotBlank @Size(min = 3, max = 20) String id,
    @Email String email,
    @Size(min = 8, max = 64) String password
) {}

public record LoginReq(@NotBlank String id, @NotBlank String password) {}
public record TokenResponse(String accessToken, long expiresIn) {}
public record UserView(long id, String id_, String nickname, LocalDateTime createdAt) {}
```

**해설**:
- POST /api/users → 가입 = 자원 생성 → 201 + Location
- POST /api/users/login → 토큰 발급 = 동작이지만 POST 가 무난
- GET /me → "현재 인증 사용자의 자원" 관용. id 파라미터 안 받음
- PATCH /api/boards/{id} → 부분 수정 (PUT 은 전체 교체)
- 권한 위반은 Service 가 `AccessDeniedException` throw → 전역 핸들러가 403

---

## 11. 실전 패턴 / 자주 빠지는 함정

- ❌ **`/getBoardList`, `/deleteBoard?id=42`** 같은 동사 URI + 잘못된 메서드.
  ✅ 자원(복수 명사) URI + HTTP 메서드로 동작 표현.
- ❌ **모든 응답 200 OK + body 에 success 필드**.
  ✅ 상태 코드 의미 살리기. 클라이언트 if 분기 단순화.
- ❌ **에러 응답이 매번 다른 구조** (어떤 건 string, 어떤 건 object).
  ✅ `ErrorResponse` 표준 스키마.
- ❌ **검증을 Controller 에서 if 로**.
  ✅ Bean Validation + `@Valid`.
- ❌ **PUT 으로 부분 수정**.
  ✅ PATCH 가 부분, PUT 은 전체 교체 (없는 필드는 null/default).
- ❌ **POST 후 200 OK + 본문에 새 id**.
  ✅ 201 Created + `Location: /api/.../{id}` 헤더.
- ❌ **에러 메시지에 SQL/스택트레이스 노출**.
  ✅ 사용자용 message + 내부용 로그 분리.
- ❌ **응답에 entity 그대로** (비밀번호 해시·내부 플래그 포함).
  ✅ DTO/Response record 로 변환.
- ❌ **버저닝 없이 breaking change 배포**.
  ✅ /v1 → /v2 + deprecation 기간.

---

## 12. 자가점검

1. PUT 과 PATCH 의 차이를 한 문장으로?
2. POST 후 201 응답에 같이 보내야 하는 표준 헤더는?
3. `@RestController` 가 `@Controller` 와 어떻게 다른가?
4. 검증 실패가 어떤 예외로 전파되고, 어디서 응답으로 바뀌는가?

<details><summary>풀이</summary>

1. PUT 은 자원 **전체 교체** (없는 필드는 null/default). PATCH 는 **부분 수정** (보낸 필드만).
2. **`Location`** — 새로 만들어진 자원의 URL.
3. `@RestController` = `@Controller` + `@ResponseBody`. 모든 메서드 반환값이 JSON 직렬화. `@Controller` 는 반환값을 View 이름으로 해석.
4. `@Valid` 실패 시 Spring 이 `MethodArgumentNotValidException` 자동 throw → `@RestControllerAdvice` 의 해당 `@ExceptionHandler` 가 받아 400 + 에러 본문으로 변환.

</details>

---

_보조 학습 노트 — 슬라이드 없음. CORS/Pagination 강의(5/22) 와 함께 보면 좋다._
