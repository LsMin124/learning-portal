# Spring MVC 2 — 요청 파라미터 심화 · 예외처리 · File Upload/Download

> **이 강의는 무엇인가**: MVC1 의 기본 위에 ① 쿠키·세션·리다이렉트 데이터 전달 (요청 파라미터 심화), ② `@ControllerAdvice` 로 전역 예외 처리 + 커스텀 예외 설계, ③ MultipartFile 로 파일 업로드 + AbstractView 로 파일 다운로드.
> **왜 배우는가**: 실무 게시판·관리자·결제 시스템의 90% 가 이 3가지 (세션 로그인·전역 예외·파일) 를 사용. 어노테이션 한 줄로 풀리는 마법의 뒷동작 + 자주 빠지는 함정 모두 익혀야 운영 시 버그 없이 굴러간다.

---

## 들어가기 전에

- **선수**: Spring MVC 1 (Controller·Service·DAO 분리, `@RequestParam`/`@PathVariable`), JSP, Cookie/Session 강의.
- **마인드셋**: "예외는 발생할 수 있는 게 아니라 발생한다" 라는 전제. 어디서 받을지·어떻게 사용자에게 보여줄지 미리 설계.

---

# Part A. 요청 파라미터 처리 심화

## 1. `@CookieValue` — 쿠키 자동 바인딩

```java
@GetMapping("/welcome")
public String welcome(@CookieValue(value = "lastVisit", required = false) String lastVisit,
                       Model model) {
    model.addAttribute("lastVisit", lastVisit);
    return "welcome";
}
```

쿠키 이름과 변수가 자동 매칭. `required = false` 로 쿠키 없는 신규 사용자도 처리.

쿠키 굽는 쪽:
```java
@PostMapping("/login")
public String login(HttpServletResponse res) {
    Cookie c = new Cookie("lastVisit", LocalDateTime.now().toString());
    c.setMaxAge(60 * 60 * 24 * 7);   // 7일
    c.setHttpOnly(true);              // JS 접근 차단
    c.setPath("/");
    res.addCookie(c);
    return "redirect:/";
}
```

## 2. `@SessionAttribute` — 세션 자동 바인딩

```java
// 세션에 데이터 적재 (로그인 처리)
@PostMapping("/login")
public String login(@ModelAttribute LoginForm form, HttpSession session) {
    User u = userService.authenticate(form);
    session.setAttribute("loginUser", u);
    return "redirect:/";
}

// 세션에서 자동 추출
@GetMapping("/mypage")
public String mypage(@SessionAttribute(name = "loginUser", required = false) User user,
                      Model model) {
    if (user == null) return "redirect:/login";
    model.addAttribute("user", user);
    return "mypage";
}
```

`HttpSession` 직접 받아 `getAttribute` 호출하는 보일러플레이트 제거.

## 3. `@ModelAttribute` 메서드 — 모든 핸들러에 공통 데이터

```java
@Controller
@RequestMapping("/board")
public class BoardController {

    // 컨트롤러의 모든 핸들러 메서드 실행 전에 자동 호출
    @ModelAttribute("categories")
    public List<Category> categories() {
        return categoryService.findAll();
    }

    @GetMapping("/list")
    public String list(Model model) {
        // 여기서 categories 는 이미 model 에 들어가 있음
        model.addAttribute("boards", boardService.findAll());
        return "board/list";
    }
}
```

검색 필터·카테고리·로그인 사용자 등 **모든 페이지에 필요한 공통 데이터** 를 한 번에.

## 4. `RedirectAttributes` — 리다이렉트 데이터 전달

```java
@PostMapping("/board")
public String create(@ModelAttribute BoardDto dto, RedirectAttributes ra) {
    boardService.create(dto);

    // 1) URL 쿼리 스트링 (페이지 상태 유지용)
    ra.addAttribute("page", 1);
    // → redirect:/board/list?page=1

    // 2) Flash Attribute - 1회용 (메시지·결과 알림)
    ra.addFlashAttribute("message", "등록 완료");
    // → 다음 요청에서 ${message} 로 1번만 접근 가능, 새로고침 시 사라짐

    return "redirect:/board/list";
}
```

| 메서드 | 용도 | 노출 |
|--|--|--|
| `addAttribute(key, value)` | 다음 URL 의 쿼리 스트링 | URL 에 보임 |
| `addFlashAttribute(key, value)` | 1회용 메시지 | URL 에 안 보임, 새로고침 시 사라짐 |

---

# Part B. 예외처리

## 5. 왜 예외처리가 필요한가

```java
@GetMapping("/board/{id}")
public String detail(@PathVariable int id, Model model) {
    Board b = boardService.findById(id);   // null 가능
    model.addAttribute("board", b);
    return "board/detail";                  // → JSP 에서 NPE
}
```

문제:
- `null` 이 view 까지 도달 → JSP 에서 NullPointerException → "500 Internal Server Error" 페이지
- 사용자에게 의미 있는 메시지 못 줌
- 스택 트레이스 노출 시 보안 사고

→ **예외를 비즈니스 의미로 변환 + 적절한 화면으로 안내** 가 필요.

## 6. 예외 처리 우선순위 계층

```
   ① 메서드 단위
        ▼
   메서드 안의 try/catch        - 즉시 처리 (잘 안 씀)

   ② 컨트롤러 단위
        ▼
   @ExceptionHandler             - 같은 컨트롤러의 예외만 처리

   ③ 전역
        ▼
   @ControllerAdvice +           - 모든 컨트롤러의 예외 처리
   @ExceptionHandler              (실무 표준)

   ④ 서블릿 컨테이너
        ▼
   web.xml <error-page>           - 마지막 수단 (잘 안 씀)
```

위에서 아래로 가며 처리되지 않은 예외만 다음 단계로 전파. 가장 가까운 핸들러가 처리.

## 7. 컨트롤러 단위 — `@ExceptionHandler`

```java
@Controller
public class BoardController {

    @GetMapping("/board/{id}")
    public String detail(@PathVariable int id, Model model) {
        Board b = boardService.findById(id);
        if (b == null) throw new NotFoundException("게시글 없음: " + id);
        model.addAttribute("board", b);
        return "board/detail";
    }

    // 이 컨트롤러에서 NotFoundException 발생 시 자동 호출
    @ExceptionHandler(NotFoundException.class)
    public String handleNotFound(NotFoundException e, Model model) {
        model.addAttribute("message", e.getMessage());
        return "error/404";
    }
}
```

**한계**: 같은 컨트롤러의 예외만 처리. 모든 컨트롤러에 공통 적용하려면 다음 단계.

## 8. 전역 단위 — `@ControllerAdvice`

```java
@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public String handleNotFound(NotFoundException e, Model model) {
        model.addAttribute("message", e.getMessage());
        return "error/404";
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public String handleBadRequest(IllegalArgumentException e, Model model) {
        model.addAttribute("message", e.getMessage());
        return "error/400";
    }

    @ExceptionHandler(Exception.class)   // 모든 예외의 최후의 보루
    public String handleAll(Exception e, Model model) {
        log.error("unhandled", e);
        model.addAttribute("message", "서버 오류");
        return "error/500";
    }
}
```

**REST API 용은 `@RestControllerAdvice`**:

```java
@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> notFound(NotFoundException e) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", e.getMessage()));
    }
}
```

## 9. 커스텀 예외 설계

```java
// 1) 비즈니스 예외 base
public abstract class BusinessException extends RuntimeException {
    public BusinessException(String message) { super(message); }
}

// 2) 구체적 예외
public class NotFoundException extends BusinessException {
    public NotFoundException(String message) { super(message); }
}

public class DuplicateException extends BusinessException {
    public DuplicateException(String message) { super(message); }
}

public class AccessDeniedException extends BusinessException {
    public AccessDeniedException() { super("권한 없음"); }
}
```

**커스텀 예외의 가치**:
- 의미 있는 이름 (`NotFoundException` vs `Exception`)
- 전역 핸들러에서 한 번에 묶어 처리
- 비즈니스 로직에서 자연스러운 흐름 표현

**RuntimeException 상속** 권장 이유:
- `throws` 선언 강제 안 됨 → 메서드 시그니처 깨끗
- Spring 의 `@Transactional` 이 기본적으로 RuntimeException 만 롤백

---

# Part C. File Upload

## 10. HTML 폼 설정

```html
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="text" name="title">
    <input type="file" name="file">
    <input type="file" name="files" multiple>   <!-- 다중 -->
    <button>업로드</button>
</form>
```

**`enctype="multipart/form-data"` 필수**. 기본 `application/x-www-form-urlencoded` 는 파일 전송 불가.

## 11. Spring 의 `MultipartFile`

```java
@Controller
@RequiredArgsConstructor
public class UploadController {

    private final FileService fileService;

    @PostMapping("/upload")
    public String upload(@RequestParam String title,
                          @RequestParam("file") MultipartFile file) throws IOException {

        if (file.isEmpty()) {
            throw new IllegalArgumentException("파일을 선택하세요");
        }

        String originalName = file.getOriginalFilename();
        String savedName = fileService.save(file);

        return "redirect:/upload-result";
    }

    // 다중 파일
    @PostMapping("/upload-multi")
    public String uploadMulti(@RequestParam("files") List<MultipartFile> files) {
        for (MultipartFile f : files) {
            if (!f.isEmpty()) fileService.save(f);
        }
        return "redirect:/upload-result";
    }
}
```

**`MultipartFile` 의 주요 메서드**:
| 메서드 | 의미 |
|--|--|
| `getOriginalFilename()` | 클라이언트에서 보낸 원본 파일명 |
| `getContentType()` | MIME 타입 (`image/png` 등) |
| `getSize()` | 바이트 크기 |
| `getBytes()` | 전체 내용을 byte[] 로 |
| `getInputStream()` | 스트림으로 (큰 파일에 유리) |
| `transferTo(File dest)` | 파일로 즉시 저장 |
| `isEmpty()` | 빈 업로드 (사용자가 파일 선택 안 함) |

## 12. FileService — 저장 로직 분리

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class FileService {

    @Value("${file.upload-dir}")
    private String uploadDir;

    public String save(MultipartFile file) throws IOException {
        // 1) 원본 파일명 (보안 위해 그대로 안 씀)
        String original = file.getOriginalFilename();
        String ext = getExtension(original);

        // 2) UUID 로 새 이름 (충돌·추측 방지)
        String saved = UUID.randomUUID() + "." + ext;

        // 3) 디렉토리 보장
        File dir = new File(uploadDir);
        if (!dir.exists()) dir.mkdirs();

        // 4) 저장
        File dest = new File(dir, saved);
        file.transferTo(dest);

        log.info("file saved: {} -> {}", original, saved);
        return saved;
    }

    private String getExtension(String filename) {
        int idx = filename.lastIndexOf('.');
        return (idx == -1) ? "" : filename.substring(idx + 1);
    }
}
```

```properties
# application.properties
file.upload-dir=/var/uploads
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=50MB
```

## 13. 업로드 보안 체크리스트

| 체크 | 이유 |
|--|--|
| 원본 파일명 그대로 안 씀 | path traversal (`../../../etc/passwd`) 방지 |
| UUID 등 추측 불가 이름 | 다른 사용자 파일 직접 URL 접근 방지 |
| 확장자 화이트리스트 | `.exe`/`.sh`/`.jsp` 업로드 차단 |
| ContentType 검증 | MIME 위조 차단 |
| 크기 제한 | DoS 방지 (`spring.servlet.multipart.max-file-size`) |
| webroot 밖 저장 | 직접 URL 접근 차단 |

---

# Part D. File Download

## 14. 가장 간단한 방법 — `ResponseEntity<Resource>`

```java
@GetMapping("/download/{filename}")
public ResponseEntity<Resource> download(@PathVariable String filename) throws IOException {
    File file = new File(uploadDir, filename);
    if (!file.exists()) throw new NotFoundException("파일 없음");

    Resource resource = new FileSystemResource(file);

    return ResponseEntity.ok()
        .contentType(MediaType.APPLICATION_OCTET_STREAM)
        .header(HttpHeaders.CONTENT_DISPOSITION,
                "attachment; filename=\"" + URLEncoder.encode(filename, "UTF-8") + "\"")
        .body(resource);
}
```

**`Content-Disposition` 헤더**: `attachment` 면 다운로드 다이얼로그, `inline` 이면 브라우저에서 직접 표시(이미지·PDF).

## 15. `AbstractView` 상속 방식 (강의 슬라이드 방식)

```java
public class FileDownloadView extends AbstractView {

    public FileDownloadView() {
        setContentType("application/octet-stream");
    }

    @Override
    protected void renderMergedOutputModel(Map<String, Object> model,
                                             HttpServletRequest req,
                                             HttpServletResponse res) throws Exception {
        File file = (File) model.get("file");
        String filename = URLEncoder.encode(file.getName(), "UTF-8");

        res.setContentType(getContentType());
        res.setContentLength((int) file.length());
        res.setHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");

        try (FileInputStream fis = new FileInputStream(file);
             OutputStream os = res.getOutputStream()) {
            FileCopyUtils.copy(fis, os);
            os.flush();
        }
    }
}
```

Controller:
```java
@GetMapping("/download/{filename}")
public ModelAndView download(@PathVariable String filename) {
    File file = new File(uploadDir, filename);
    ModelAndView mav = new ModelAndView(new FileDownloadView());
    mav.addObject("file", file);
    return mav;
}
```

**왜 AbstractView?** 강의 슬라이드 방식. 실무는 `ResponseEntity<Resource>` 가 더 흔하지만, View 시스템에 통합되는 장점이 있음.

## 16. 한글 파일명 인코딩 함정

```java
// ❌ 한글이 깨짐
res.setHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");

// ✅ UTF-8 인코딩
String encoded = URLEncoder.encode(filename, StandardCharsets.UTF_8)
                            .replaceAll("\\+", "%20");  // space 처리
res.setHeader("Content-Disposition", "attachment; filename=\"" + encoded + "\"");

// ✅ 더 정확 - RFC 5987 (브라우저 호환성 ↑)
res.setHeader("Content-Disposition",
    "attachment; filename*=UTF-8''" + URLEncoder.encode(filename, StandardCharsets.UTF_8));
```

브라우저별 인코딩 처리가 다르므로 `filename*=UTF-8''` 형식이 가장 안전.

---

## 17. 코드 깊게 — 게시판 첨부파일 풀스택

```java
// === Entity / DTO ===
@Data
public class BoardDto {
    private int id;
    private String title;
    private String content;
    private MultipartFile attachment;
    private String savedFilename;
    private String originalFilename;
}

// === Custom Exception ===
public class FileException extends BusinessException {
    public FileException(String msg) { super(msg); }
}

// === Service ===
@Service
@RequiredArgsConstructor
@Transactional
public class BoardService {
    private final BoardDao boardDao;
    private final FileService fileService;

    public int create(BoardDto dto) throws IOException {
        // 1) 파일 저장 (있으면)
        if (dto.getAttachment() != null && !dto.getAttachment().isEmpty()) {
            String saved = fileService.save(dto.getAttachment());
            dto.setSavedFilename(saved);
            dto.setOriginalFilename(dto.getAttachment().getOriginalFilename());
        }
        // 2) DB INSERT
        boardDao.insert(dto);
        return dto.getId();
    }
}

// === Controller ===
@Controller
@RequiredArgsConstructor
public class BoardController {
    private final BoardService boardService;

    @PostMapping("/board")
    public String create(@ModelAttribute BoardDto dto, RedirectAttributes ra) throws IOException {
        int id = boardService.create(dto);
        ra.addFlashAttribute("message", "등록 완료");
        return "redirect:/board/" + id;
    }
}

// === Global Exception Handler ===
@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public String notFound(NotFoundException e, Model model) {
        model.addAttribute("message", e.getMessage());
        return "error/404";
    }

    @ExceptionHandler(FileException.class)
    public String fileError(FileException e, Model model) {
        model.addAttribute("message", "파일 처리 오류: " + e.getMessage());
        return "error/file";
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public String tooLarge(Model model) {
        model.addAttribute("message", "파일 크기는 10MB 이하여야 합니다");
        return "error/file";
    }

    @ExceptionHandler(Exception.class)
    public String all(Exception e, Model model) {
        log.error("unhandled", e);
        model.addAttribute("message", "서버 오류");
        return "error/500";
    }
}
```

---

## 18. 실전 패턴 / 자주 빠지는 함정

### 파라미터 처리
- ❌ 컨트롤러에서 `session.getAttribute("loginUser")` + 캐스팅 ✅ `@SessionAttribute User loginUser`
- ❌ 매 페이지에 공통 데이터 직접 add ✅ `@ModelAttribute` 메서드
- ❌ 리다이렉트 후 메시지를 query string 으로 노출 ✅ `addFlashAttribute`

### 예외처리
- ❌ 모든 메서드에 try/catch ✅ `@ControllerAdvice` 전역
- ❌ `Exception` 한 가지로 다 잡음 ✅ 구체적 예외부터 (`NotFoundException` → `BusinessException` → `Exception`)
- ❌ checked exception 으로 비즈니스 예외 만듦 ✅ RuntimeException 상속
- ❌ 예외 메시지에 SQL/스택트레이스 노출 ✅ 사용자 메시지 + log 분리
- ❌ 500 페이지에 디버그 정보 노출 ✅ 운영 환경엔 일반 메시지만

### 파일 업로드
- ❌ 원본 파일명 그대로 저장 → path traversal 취약 ✅ UUID + 화이트리스트 확장자
- ❌ webroot 안에 업로드 → 직접 URL 접근 ✅ webroot 밖 또는 인증 거친 다운로드 컨트롤러
- ❌ `getBytes()` 로 큰 파일 메모리에 ✅ `InputStream` 또는 `transferTo`
- ❌ `enctype="multipart/form-data"` 누락 → 파일 안 옴 ✅ form 에 명시
- ❌ 사용자가 `.jsp`, `.exe` 업로드 → 서버 실행 위험 ✅ 확장자 화이트리스트

### 파일 다운로드
- ❌ 한글 파일명 깨짐 ✅ `URLEncoder.encode + UTF-8`
- ❌ `Content-Type: text/html` 로 두면 브라우저가 열려 함 ✅ `application/octet-stream`
- ❌ 다운로드 경로에 사용자 입력 그대로 사용 → path traversal ✅ 화이트리스트·DB 매핑 ID 사용

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| 파일 업로드 시 `MaxUploadSizeExceededException` | 기본 제한 초과 (1MB) | `spring.servlet.multipart.max-file-size` 설정 |
| `MultipartFile` 이 null | enctype 누락 또는 input name 불일치 | form 의 enctype + name 확인 |
| `@ControllerAdvice` 가 안 잡힘 | REST API 컨트롤러엔 `@RestControllerAdvice` 필요 | 어노테이션 교체 |
| 한글 파일명이 ?로 표시 | UTF-8 인코딩 누락 | `filename*=UTF-8''...` 헤더 |
| 전역 핸들러에서 `Exception.class` 가 다른 핸들러보다 먼저 잡힘 | 우선순위 — Spring 은 가장 구체적인 예외 핸들러 우선 | 구체적 → 일반적 순서 유지 (Spring 이 자동 정렬, 다만 같은 클래스에선 선언 순서) |
| `@SessionAttribute` 가 항상 null | 세션에 그 이름으로 저장 안 됨 | 로그인 처리에서 `session.setAttribute` 호출 확인 |

---

## 19. 자가점검

1. `@CookieValue` 와 `@SessionAttribute` 의 차이?
2. `RedirectAttributes.addAttribute()` 와 `addFlashAttribute()` 의 차이?
3. 예외 처리 우선순위 4단계는?
4. `@ControllerAdvice` 와 `@RestControllerAdvice` 의 차이?
5. 커스텀 예외를 RuntimeException 으로 만드는 이유 2가지?
6. 파일 업로드 form 에 반드시 있어야 하는 속성은?
7. 파일 업로드 시 원본 파일명을 그대로 쓰면 안 되는 보안 이유 2가지?
8. 한글 파일명을 다운로드할 때 깨지는 이유와 해결?

<details><summary>풀이</summary>

1. **`@CookieValue`**: 브라우저의 쿠키 헤더에서 추출 (`Cookie: lastVisit=...`). **`@SessionAttribute`**: HttpSession 에서 추출 (`session.getAttribute("loginUser")`). 쿠키는 클라이언트 저장, 세션은 서버 저장.
2. **`addAttribute`**: 다음 URL 의 **쿼리 스트링**으로 추가 (`?page=1`). 새로고침해도 유지. **`addFlashAttribute`**: **1회용** 데이터 (메시지·결과 알림). URL 에 안 보임, 새로고침 시 사라짐.
3. ① 메서드 try/catch ② 컨트롤러 단위 `@ExceptionHandler` ③ 전역 `@ControllerAdvice` ④ 서블릿 `<error-page>`. 가장 가까운 핸들러가 처리.
4. **`@ControllerAdvice`**: JSP/Thymeleaf 페이지로 응답 (view 반환). **`@RestControllerAdvice`** = `@ControllerAdvice` + `@ResponseBody`: JSON 응답. API 서버엔 후자.
5. ① `throws` 선언 강제 안 됨 → 메서드 시그니처 깨끗. ② Spring 의 `@Transactional` 이 **RuntimeException 만 기본 롤백**. checked exception 은 `@Transactional(rollbackFor = Exception.class)` 필요.
6. **`enctype="multipart/form-data"`**. 기본 `application/x-www-form-urlencoded` 는 파일 전송 불가.
7. ① **Path Traversal** — `../../../etc/passwd` 같은 경로 침투. ② **다른 사용자 파일 추측 접근** — 원본 이름은 추측 가능, UUID 등 추측 불가 이름이 안전.
8. **원인**: HTTP 헤더는 기본 ISO-8859-1 → 한글이 ? 또는 깨짐. **해결**: `URLEncoder.encode(filename, UTF-8)` + `Content-Disposition: attachment; filename*=UTF-8''<인코딩된 이름>` (RFC 5987).

</details>

---

## 20. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.13 Spring Web MVC2 (DTO·쿠키·세션·리다이렉트) | §1 ~ §4 (Part A) |
| p.14 ~ p.19 예외처리 (`@ExceptionHandler`·`@ControllerAdvice`·커스텀 예외) | §5 ~ §9 (Part B) |
| p.20 ~ p.29 File Upload (Multipart·FileService) | §10 ~ §13 (Part C) |
| p.30 ~ p.31 File Download (AbstractView) | §14 ~ §16 (Part D) |
| p.32 마무리·생각해보기 | (생략) |

_32p 슬라이드 모두 커버._
