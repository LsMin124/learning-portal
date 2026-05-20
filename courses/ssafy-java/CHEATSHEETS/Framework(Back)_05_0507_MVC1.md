# Spring MVC 1 — 치트시트

> 42p 슬라이드 · Spring 의 Web 모듈, DispatcherServlet 기반 요청 처리.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **DispatcherServlet** = 모든 요청을 받는 단일 진입점 (Front Controller 패턴)
2. **요청 처리 흐름**: Filter → DispatcherServlet → HandlerMapping → Controller → ViewResolver → View
3. **`@Controller` + `@GetMapping`** = Servlet 의 `@WebServlet` + `doGet` 대체
4. **Model.addAttribute(...) → JSP**, return "view-name" → ViewResolver 가 경로 합침
5. **`@PathVariable`, `@RequestParam`, `@ModelAttribute`** 로 파라미터 자동 매핑
6. **3-Tier**: Controller (HTTP) → Service (비즈니스 + Tx) → DAO/Mapper (SQL)

## 가장 중요한 코드 3개

```java
// (1) 기본 Controller
@Controller
@RequestMapping("/boards")
@RequiredArgsConstructor
public class BoardController {

    private final BoardService service;

    @GetMapping                                  // GET /boards
    public String list(Model model) {
        model.addAttribute("boards", service.findAll());
        return "board/list";                     // /WEB-INF/views/board/list.jsp
    }

    @GetMapping("/{id}")                         // GET /boards/42
    public String detail(@PathVariable long id, Model model) {
        model.addAttribute("board", service.findById(id));
        return "board/detail";
    }

    @PostMapping                                 // POST /boards
    public String create(@ModelAttribute BoardForm form) {
        service.insert(form);
        return "redirect:/boards";               // PRG
    }
}
```

```java
// (2) 3-Tier
@Controller @RequiredArgsConstructor
public class BoardController {              // HTTP
    private final BoardService service;
}

@Service @RequiredArgsConstructor
public class BoardService {                 // 비즈니스 + Tx
    private final BoardMapper mapper;

    @Transactional(readOnly = true)
    public List<Board> findAll() { return mapper.findAll(); }
}

@Mapper                                      // Spring 이 자동 구현체 생성
public interface BoardMapper {              // SQL
    @Select("SELECT * FROM boards")
    List<Board> findAll();
}
```

```yaml
# (3) application.yml - ViewResolver
spring.mvc.view:
  prefix: /WEB-INF/views/
  suffix: .jsp
# return "board/list" -> /WEB-INF/views/board/list.jsp
```

## 면접 한 줄 답변
- **DispatcherServlet 의 역할?** → Front Controller. 모든 요청을 받아서 적절한 Controller 로 위임.
- **MVC 패턴의 의미?** → Model (데이터) / View (화면) / Controller (요청 처리). 책임 분리.
- **`return "redirect:/boards"` vs `return "boards"`?** → redirect: 302 응답 (PRG), 그냥은 forward (ViewResolver).
- **@RequestParam vs @PathVariable?** → 쿼리스트링 (`?id=42`) vs URL 경로 (`/users/42`).

---

# 2. Quick Reference (실무 복붙)

## 요청 처리 흐름

```
[Client]
   ↓ HTTP
[Filter] (인코딩, 인증)
   ↓
[DispatcherServlet]            <- Front Controller (Spring 핵심)
   ↓
[HandlerMapping]               <- @RequestMapping 매칭
   ↓
[HandlerInterceptor.preHandle]
   ↓
[Controller 메서드 호출]
   ↓
[Service]
   ↓
[Mapper/DAO -> DB]
   ↓
[Controller 반환 (view-name)]
   ↓
[ViewResolver]                 <- prefix + view + suffix
   ↓
[View 렌더 (JSP)]
   ↓
[HandlerInterceptor.postHandle]
   ↓
[Filter]
   ↓
[Response]
```

## 매핑 어노테이션

```java
@Controller                             // View 반환 (JSP/Thymeleaf)
@RestController                         // JSON 반환 (= @Controller + @ResponseBody)

@RequestMapping("/api/boards")          // 클래스 레벨 prefix
@GetMapping / @PostMapping / @PutMapping / @PatchMapping / @DeleteMapping

@RequestMapping(value = "/list", method = RequestMethod.GET)  // 옛 스타일

@GetMapping(value = "/{id}", produces = "application/json")
@PostMapping(consumes = "application/json")
```

## 파라미터 어노테이션

| 어노테이션 | 위치 | 예 |
|--|--|--|
| `@PathVariable` | URL 경로 | `GET /users/{id}` |
| `@RequestParam` | 쿼리스트링·form | `GET /users?page=1` |
| `@RequestBody` | HTTP body (JSON) | `POST /users` |
| `@ModelAttribute` | form 또는 query (객체) | `GET /search?keyword=...` |
| `@RequestHeader` | HTTP 헤더 | `Authorization: ...` |
| `@CookieValue` | 쿠키 | `JSESSIONID` |
| `@SessionAttribute` | 세션 | `loginUser` |

```java
@GetMapping("/{id}")
public String detail(
    @PathVariable long id,
    @RequestParam(defaultValue = "1") int page,
    @RequestHeader("User-Agent") String userAgent,
    @SessionAttribute(name = "loginUser", required = false) User user,
    Model model) {
    ...
}
```

## Model · ModelAndView

```java
// Model (가장 흔함)
@GetMapping
public String list(Model model) {
    model.addAttribute("boards", service.findAll());
    model.addAttribute("total", 100);
    return "board/list";
}

// ModelAndView
@GetMapping
public ModelAndView listMV() {
    ModelAndView mv = new ModelAndView("board/list");
    mv.addObject("boards", service.findAll());
    return mv;
}

// Map (DTO 가 객체일 때)
@GetMapping
public String list(Map<String, Object> model) {
    model.put("boards", service.findAll());
    return "board/list";
}
```

## return 값의 의미

```java
@GetMapping("/board/{id}")
public String x(@PathVariable long id) {
    // (1) view name (JSP/Thymeleaf)
    return "board/detail";

    // (2) redirect (302)
    return "redirect:/boards";
    return "redirect:" + req.getContextPath() + "/boards";

    // (3) forward (Servlet forward)
    return "forward:/error";
}

// JSON (@RestController 또는 @ResponseBody)
@GetMapping("/api/board/{id}")
@ResponseBody
public Board api(@PathVariable long id) {
    return service.findById(id);     // JSON 직렬화
}

// ResponseEntity (상태 + 헤더 + body)
@PostMapping
public ResponseEntity<Board> create(@RequestBody BoardReq req) {
    Board saved = service.create(req);
    return ResponseEntity
        .created(URI.create("/api/boards/" + saved.getId()))
        .body(saved);
}
```

## ViewResolver 설정

```yaml
# application.yml
spring.mvc.view:
  prefix: /WEB-INF/views/
  suffix: .jsp
```

→ `return "board/list"` = `/WEB-INF/views/board/list.jsp`

```java
// @Configuration 으로도 가능
@Bean
public InternalResourceViewResolver viewResolver() {
    InternalResourceViewResolver r = new InternalResourceViewResolver();
    r.setPrefix("/WEB-INF/views/");
    r.setSuffix(".jsp");
    return r;
}
```

## 3-Tier 아키텍처

```
[@Controller]              <- HTTP 요청·응답
   ↓ DI
[@Service]                 <- 비즈니스 로직, @Transactional
   ↓ DI
[@Mapper / @Repository]    <- SQL 실행
   ↓
[DB]
```

각 레이어는 자기 위 모름. 교체·테스트 용이.

```java
@Controller @RequiredArgsConstructor
public class BoardController {
    private final BoardService service;  // Service 만 의존
}

@Service @RequiredArgsConstructor
public class BoardService {
    private final BoardMapper mapper;    // Mapper 만 의존
}
```

## DTO vs Entity 분리

```java
// Entity (DB 매핑)
public class Board {
    private Long id;
    private String title;
    private String content;
    private Long userId;
    private LocalDateTime createdAt;
}

// 요청 DTO
public record BoardCreateReq(
    @NotBlank String title,
    @NotBlank String content
) {}

// 응답 DTO (민감 필드 제외)
public record BoardResponse(
    Long id,
    String title,
    String writer,           // userId 가 아니라 닉네임
    LocalDateTime createdAt
) {}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `@RestController` 면서 `return "board/list"` | view 이름 그대로 반환 → 404 |
| Controller 에 SQL 직접 | Service → Mapper 로 |
| `@Transactional` 을 Controller 에 | Service 에만 |
| POST 후 view 반환 → F5 중복 | `return "redirect:/boards"` |
| `@RequestParam` 누락 → 400 | `required = false` 또는 `defaultValue` |
| Entity 그대로 응답 → 민감 필드 노출 | DTO 분리 |
| URL 경로 매핑 충돌 | 더 구체적인 매핑이 우선 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Spring MVC 1 (42p)
│
├── [A] DispatcherServlet
│   ├── Front Controller 패턴
│   ├── 단일 진입점
│   ├── HandlerMapping
│   └── ViewResolver
│
├── [B] Controller
│   ├── @Controller (View) / @RestController (JSON)
│   ├── @RequestMapping (클래스/메서드)
│   ├── @GetMapping / @PostMapping / ...
│   └── 메서드 시그니처 (자유로움)
│
├── [C] 파라미터 매핑
│   ├── @PathVariable
│   ├── @RequestParam
│   ├── @ModelAttribute
│   ├── @RequestBody
│   └── @RequestHeader / @CookieValue / @SessionAttribute
│
├── [D] 반환값
│   ├── view name (String)
│   ├── redirect: / forward:
│   ├── @ResponseBody (JSON)
│   ├── ResponseEntity
│   └── ModelAndView
│
├── [E] 3-Tier
│   ├── Controller (HTTP)
│   ├── Service (비즈니스 + Tx)
│   ├── Mapper / DAO (SQL)
│   └── DTO vs Entity
│
└── [F] vs Servlet
    ├── @WebServlet -> @Controller
    ├── req.setAttribute -> Model
    ├── forward -> view name
    └── sendRedirect -> "redirect:/"
```

## 학습 진도 체크리스트

### A. DispatcherServlet
- [ ] Front Controller 패턴
- [ ] 요청 흐름 (Filter → DS → ... → View)
- [ ] HandlerMapping 의 동작

### B. Controller
- [ ] @Controller vs @RestController
- [ ] @RequestMapping 클래스/메서드 레벨
- [ ] HTTP 메서드별 어노테이션

### C. 파라미터
- [ ] @PathVariable / @RequestParam / @ModelAttribute / @RequestBody 선택
- [ ] required / defaultValue
- [ ] DTO 자동 매핑

### D. 반환
- [ ] view name + ViewResolver
- [ ] redirect: vs forward:
- [ ] @ResponseBody → JSON
- [ ] ResponseEntity 활용

### E. 아키텍처
- [ ] 3-Tier 책임 분리
- [ ] DTO 와 Entity 분리
- [ ] Spring MVC 와 Servlet 매핑

## 연관 강의

```
1강 Framework        -> IoC
2강 DI               -> 빈
3강 SpringBoot       -> 자동 설정
4강 AOP              -> 횡단 관심사
5강 MVC1             <- 현재 위치
6강 MVC2             -> 응답 변환·핸들러 깊이
7강 Interceptor      -> 인증
8강 MyBatis          -> Mapper
11강 종합 실습       -> 통합
```

→ 다음 (MVC2) 에서 **응답 변환·예외 처리·파일 업로드**.
