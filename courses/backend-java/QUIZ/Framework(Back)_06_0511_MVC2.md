# Spring MVC 2 — 퀴즈

> 16문항. 개념·적용·디버그·면접. 4부(요청 파라미터 심화·예외처리·File Upload·Download) 골고루.

---

## Part A. 요청 파라미터 심화

### Q1. (개념) `@CookieValue` 와 `@SessionAttribute` 의 차이?

<details><summary>정답</summary>

- **`@CookieValue`**: 브라우저의 쿠키 헤더에서 추출 (`Cookie: name=value`). 클라이언트 저장.
- **`@SessionAttribute`**: HttpSession 에서 추출 (`session.getAttribute(...)`). 서버 저장.

쿠키는 만료/삭제까지 유지(클라이언트 통제), 세션은 세션 만료(보통 30분)까지 서버에 유지.

</details>

### Q2. (적용) 로그인된 사용자만 마이페이지 접근하게 하는 핸들러?

<details><summary>정답</summary>

```java
@GetMapping("/mypage")
public String mypage(@SessionAttribute(name = "loginUser", required = false) User user,
                      Model model) {
    if (user == null) return "redirect:/login";
    model.addAttribute("user", user);
    return "mypage";
}
```

`required = false` 로 비로그인도 받고 컨트롤러에서 분기. (또는 인터셉터로 분리)

</details>

### Q3. (개념) `RedirectAttributes.addAttribute()` 와 `addFlashAttribute()` 의 차이?

<details><summary>정답</summary>

| 메서드 | 데이터 위치 | 유지 |
|--|--|--|
| `addAttribute(k, v)` | 다음 URL 의 쿼리 스트링 (`?k=v`) | 새로고침 시에도 유지 |
| `addFlashAttribute(k, v)` | 세션 (1회용) | 다음 요청 1번만, 새로고침 시 사라짐 |

페이지 상태(페이지 번호 등) 은 `addAttribute`, 일회성 메시지(등록 완료 등) 는 `addFlashAttribute`.

</details>

### Q4. (적용) 컨트롤러의 모든 핸들러에서 카테고리 목록을 model 에 자동으로 넣으시오.

<details><summary>정답</summary>

```java
@Controller
@RequestMapping("/board")
@RequiredArgsConstructor
public class BoardController {

    private final CategoryService categoryService;

    @ModelAttribute("categories")
    public List<Category> categories() {
        return categoryService.findAll();
    }

    @GetMapping("/list")
    public String list(Model model) {
        // categories 는 이미 model 에 있음
        model.addAttribute("boards", boardService.findAll());
        return "board/list";
    }
}
```

`@ModelAttribute` 메서드는 같은 컨트롤러의 모든 핸들러 전에 자동 실행.

</details>

---

## Part B. 예외처리

### Q5. (개념) 예외 처리 우선순위 4단계는?

<details><summary>정답</summary>

1. **메서드 단위** — try/catch (즉시 처리, 잘 안 씀)
2. **컨트롤러 단위** — `@ExceptionHandler` (같은 컨트롤러만)
3. **전역** — `@ControllerAdvice` + `@ExceptionHandler` (실무 표준)
4. **서블릿 컨테이너** — `web.xml` `<error-page>` (마지막 수단)

위에서 아래로 가며 처리되지 않은 예외만 다음 단계로 전파.

</details>

### Q6. (개념) `@ControllerAdvice` 와 `@RestControllerAdvice` 의 차이?

<details><summary>정답</summary>

- **`@ControllerAdvice`**: view 이름 반환 → JSP/Thymeleaf 페이지로 응답
- **`@RestControllerAdvice`** = `@ControllerAdvice` + `@ResponseBody`: 객체 반환 → JSON 직렬화

웹 페이지 서버엔 `@ControllerAdvice` + view 이름, REST API 서버엔 `@RestControllerAdvice` + `ResponseEntity<ErrorResponse>`.

</details>

### Q7. (적용) 전역 예외 핸들러를 작성하시오.
- `NotFoundException` → `error/404` view
- 모든 예외 → `error/500` view + 로그

<details><summary>정답</summary>

```java
@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public String notFound(NotFoundException e, Model model) {
        model.addAttribute("message", e.getMessage());
        return "error/404";
    }

    @ExceptionHandler(Exception.class)
    public String all(Exception e, Model model) {
        log.error("unhandled", e);
        model.addAttribute("message", "서버 오류");
        return "error/500";
    }
}
```

Spring 이 자동으로 **가장 구체적인 핸들러부터** 매칭 → `NotFoundException` 이 먼저 잡힘.

</details>

### Q8. (개념) 커스텀 예외를 `RuntimeException` 상속으로 만드는 이유 2가지?

<details><summary>정답</summary>

1. **`throws` 강제 안 됨** — 메서드 시그니처가 깨끗해짐. checked exception 은 모든 호출자가 `throws` 명시 또는 try/catch 강제.
2. **`@Transactional` 의 기본 롤백 대상** — Spring 의 `@Transactional` 은 RuntimeException 만 자동 롤백. checked exception 은 `@Transactional(rollbackFor = Exception.class)` 명시 필요.

추가: 비즈니스 예외는 "에러 처리를 강제할 만큼 예상 가능한가" 보다 "비즈니스 흐름의 자연스러운 일부" 인 경우가 많아 unchecked 가 적합.

</details>

### Q9. (디버그) `@ControllerAdvice` 의 핸들러가 작동하지 않음. REST API 컨트롤러 상황. 원인?

<details><summary>정답</summary>

**REST API 컨트롤러는 `@RestControllerAdvice` 필요**. `@ControllerAdvice` 는 view 반환을 가정 → 객체 반환 시 view 못 찾아 다시 예외.

```java
// 교체
@ControllerAdvice    →    @RestControllerAdvice
```

또는 메서드별로 `@ExceptionHandler` + `@ResponseBody` + `ResponseEntity` 반환.

</details>

---

## Part C. File Upload

### Q10. (개념) 파일 업로드 form 에 반드시 있어야 하는 속성은?

<details><summary>정답</summary>

**`enctype="multipart/form-data"`**.

```html
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <button>업로드</button>
</form>
```

기본 `application/x-www-form-urlencoded` 는 파일 전송 불가. 이게 없으면 `MultipartFile` 이 null 또는 비어있음.

</details>

### Q11. (적용) MultipartFile 로 단일 파일 받는 Controller?

<details><summary>정답</summary>

```java
@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) throws IOException {
    if (file.isEmpty()) {
        throw new IllegalArgumentException("파일을 선택하세요");
    }
    String savedName = fileService.save(file);
    return "redirect:/upload-result";
}
```

다중 파일은 `List<MultipartFile>` 또는 `MultipartFile[]`.

</details>

### Q12. (개념) 파일 업로드 시 원본 파일명을 그대로 쓰면 안 되는 보안 이유 2가지?

<details><summary>정답</summary>

1. **Path Traversal** — `../../../etc/passwd` 같은 경로 침투 공격. 사용자가 파일명에 `../` 포함시키면 webroot 밖 파일에 접근/덮어쓰기 가능.
2. **추측 가능한 접근** — 원본 이름은 다른 사용자가 추측해서 직접 URL 접근 가능 (`profile.jpg`, `resume.pdf` 등). UUID 같은 추측 불가 이름이 안전.

추가 위협:
- 같은 이름 파일이 덮어쓰기 됨
- 한글·특수문자로 인한 파일 시스템 호환성 이슈

</details>

### Q13. (디버그) 파일 업로드 시 `MaxUploadSizeExceededException`. 원인과 해결?

<details><summary>정답</summary>

Spring Boot 의 기본 업로드 제한 (1MB) 초과.

해결: `application.properties`
```properties
spring.servlet.multipart.max-file-size=10MB        # 개별 파일
spring.servlet.multipart.max-request-size=50MB     # 전체 요청
```

`-1` 로 설정 시 무제한 (위험).

또한 전역 핸들러에서 우아하게 처리:
```java
@ExceptionHandler(MaxUploadSizeExceededException.class)
public String tooLarge(Model model) {
    model.addAttribute("message", "파일 크기는 10MB 이하여야 합니다");
    return "error/file";
}
```

</details>

---

## Part D. File Download

### Q14. (적용) 가장 간단한 파일 다운로드 API 를 작성하시오.

<details><summary>정답</summary>

```java
@GetMapping("/download/{filename}")
public ResponseEntity<Resource> download(@PathVariable String filename) throws IOException {
    File file = new File(uploadDir, filename);
    if (!file.exists()) throw new NotFoundException("파일 없음");

    Resource resource = new FileSystemResource(file);
    String encoded = URLEncoder.encode(filename, StandardCharsets.UTF_8);

    return ResponseEntity.ok()
        .contentType(MediaType.APPLICATION_OCTET_STREAM)
        .header(HttpHeaders.CONTENT_DISPOSITION,
                "attachment; filename*=UTF-8''" + encoded)
        .body(resource);
}
```

`application/octet-stream` 으로 다운로드 강제, `filename*=UTF-8''` 로 한글 안전.

</details>

### Q15. (디버그) 한글 파일명이 다운로드 시 `?`로 표시. 원인과 해결?

<details><summary>정답</summary>

**원인**: HTTP 헤더는 기본 ISO-8859-1 → 한글이 표현 불가 → `?` 또는 깨짐.

**해결**: RFC 5987 의 `filename*=UTF-8''` 형식 사용.

```java
String encoded = URLEncoder.encode("한글파일.pdf", StandardCharsets.UTF_8);
res.setHeader("Content-Disposition",
    "attachment; filename*=UTF-8''" + encoded);
```

이 형식은 IE/Edge/Chrome/Firefox/Safari 모두 호환. 옛 IE 호환이 필요하면 user-agent 별 분기 처리.

</details>

### Q16. (면접) "파일 업로드 + 다운로드 기능을 만들 때 보안상 고려할 점 5가지를 나열하시오."

<details><summary>정답</summary>

**업로드**:
1. **확장자 화이트리스트** — `.exe`/`.sh`/`.jsp` 등 실행 가능 파일 차단
2. **원본 파일명 안 쓰기** — UUID 등 추측 불가 이름 (Path Traversal 방지)
3. **크기 제한** — DoS 방지 (`max-file-size`)
4. **webroot 밖 저장** — 직접 URL 접근 차단, 인증된 다운로드 컨트롤러를 통해서만 접근
5. **ContentType 검증** — MIME 위조 차단 (단, 헤더는 위조 가능하므로 매직 바이트 검증이 더 안전)

**다운로드**:
6. **다운로드 경로에 사용자 입력 그대로 X** — `../` 침투 방지. 화이트리스트 또는 DB 매핑 ID 사용
7. **권한 검증** — 본인 파일만 다운로드 가능하게 (다른 사용자 ID 추측 차단)
8. **한글 파일명 RFC 5987 인코딩** — 보안은 아니지만 호환성

핵심 원칙: **사용자 입력은 절대 신뢰하지 않음**.

</details>
