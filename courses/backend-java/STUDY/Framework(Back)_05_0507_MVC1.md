# Spring MVC 1 — MVC 패턴 · Spring Web MVC · 3-Tier 아키텍처

> **이 강의는 무엇인가**: 웹 개발의 표준 패턴 **MVC** 의 의미와, Spring 이 이를 어떻게 구현했는지 (DispatcherServlet, HandlerMapping, HandlerAdapter, ViewResolver), 그리고 실무의 **3-Tier 아키텍처(Controller / Service / DAO)** 로 책임을 어떻게 나누는지.
> **왜 배우는가**: 이후 모든 웹 개발의 기반. 어디서 무엇을 받아 어디로 보내고 어디서 DB 와 연결되는지의 큰 그림. `@Controller` 한 줄로 라우팅이 되는 마법의 정체.

---

## 들어가기 전에

- **선수**: 서블릿/JSP, Spring DI, Spring Boot 강의의 Mini MVC 직접 구현.
- **마인드셋**: "데이터·화면·제어가 한 클래스에 있으면 안 됨" 이라는 책임 분리 의식.

---

# Part A. MVC 패턴

## 1. 왜 MVC 인가 — Servlet 만 쓸 때의 한계

```
       Servlet 만 쓰면

   +-------------------------+
   |   HelloServlet           |
   |   - 비즈니스 로직 (10줄)   |
   |   - DB 접근 (15줄)        |
   |   - HTML 출력 (50줄)      |
   |   - 검증·예외 처리 (10줄)  |
   +-------------------------+  ← 85줄, 한 클래스에 4개 책임
```

**문제**:
- 비즈니스 로직과 화면 출력이 섞임 → 디자이너·개발자 협업 불가
- 한 변경이 여러 책임에 영향
- 테스트 불가 — 서블릿 컨테이너 없이 호출 불가
- 같은 화면을 여러 서블릿에서 재사용 못 함

## 2. MVC 패턴의 책임 분리

```
   +------------------------------------------+
   |  Model - 데이터와 비즈니스 로직             |
   |   • DTO, Entity, Service, DAO            |
   |   • UI 무관                              |
   +------------------------------------------+
   |  View - 사용자에게 보여줄 화면 (UI)         |
   |   • JSP, Thymeleaf, JSON                 |
   |   • 비즈니스 로직 모름                     |
   +------------------------------------------+
   |  Controller - Model 과 View 의 연결       |
   |   • 요청 받고 Model 호출 → View 결정      |
   |   • 비즈니스 로직 X (Service 에 위임)     |
   +------------------------------------------+
```

**얻는 것**:
- Model 은 UI 무관 → 콘솔/모바일/웹에 재사용
- View 는 데이터만 받음 → 디자이너가 독립적으로 작업
- Controller 는 얇음 → 비즈니스 로직 변경에 무관

---

# Part B. Spring Web MVC 개요

## 3. 전체 흐름 — DispatcherServlet 부터 View 까지

```
[Client]
    | ① HTTP 요청
    ▼
[DispatcherServlet (FrontController)]
    |
    | ② HandlerMapping 에 "이 요청 누가 처리?" 질의
    ▼
[HandlerMapping]
    | ③ 매칭된 Controller + method 반환
    |    (예: HelloController.hello())
    ▼
[HandlerAdapter]
    | ④ Controller 메서드를 적절한 방식으로 호출
    |    (어떤 파라미터·반환 타입이든 통일된 인터페이스로)
    ▼
[Controller]
    | ⑤ 비즈니스 로직 (Service 위임)
    |   Model 에 데이터 add
    |   View 이름 반환 ("home")
    ▼
[ViewResolver]
    | ⑥ "home" → "/WEB-INF/views/home.jsp" 변환
    ▼
[View (JSP)]
    | ⑦ Model 데이터로 HTML 렌더
    ▼
[Client] HTTP 응답
```

각 컴포넌트의 책임:

| 컴포넌트 | 책임 |
|--|--|
| **DispatcherServlet** | 모든 요청 진입점. 흐름 조율 |
| **HandlerMapping** | URL → Controller 매핑 |
| **HandlerAdapter** | 다양한 Controller 형태를 통일된 호출로 |
| **Controller** | 비즈니스 로직 호출 + View 결정 |
| **ViewResolver** | View 이름 → 실제 경로 |
| **View** | 데이터로 HTML 렌더 |

## 4. HandlerAdapter — 어댑터 패턴의 마법

**어댑터 패턴**: 서로 다른 인터페이스를 가진 것을 연결해주는 변환기 (110V ↔ 220V 같은 돼지코).

```
   요청을 처리하는 Controller 는 형태가 다양:
   - Spring 2: Controller 인터페이스 구현체
   - Spring 3+: @Controller + @RequestMapping 메서드
   - 함수형: HandlerFunction (WebFlux)

   DispatcherServlet 이 이 모든 형태를 어떻게 호출?
```

**HandlerAdapter** 가 중간 변환기 역할:
- `SimpleControllerHandlerAdapter` — 옛 인터페이스 방식
- `RequestMappingHandlerAdapter` — 어노테이션 방식 (실무)
- `HandlerFunctionAdapter` — 함수형

→ Controller 가 어떤 형태든 DispatcherServlet 은 통일된 방식으로 호출.

## 5. View 와 ViewResolver

```java
// Controller
@GetMapping("/home")
public String home(Model model) {
    model.addAttribute("title", "홈");
    return "home";           // 논리 view 이름
}
```

```properties
# ViewResolver 설정
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
```

→ "home" → `/WEB-INF/views/home.jsp` 자동 변환.

**ViewResolver 종류**:
- `InternalResourceViewResolver` — JSP
- `ThymeleafViewResolver` — Thymeleaf
- `JsonViewResolver` — JSON 응답
- `MarsupialViewResolver` — Mustache 등

---

# Part C. 3-Tier 아키텍처

## 6. 책임을 3계층으로 나누기

```
[클라이언트 요청]
    |
    ▼
Presentation Layer  - @Controller
    · 요청 받음
    · 파라미터 검증·변환
    · Service 호출
    · View 결정
    |
    ▼
Business Layer       - @Service
    · 비즈니스 로직
    · 트랜잭션 경계
    · 여러 DAO 조합
    |
    ▼
Data Access Layer   - @Repository
    · SQL·DB 접근만
    · CRUD
    |
    ▼
[DB]
```

**SRP (단일 책임 원칙) 준수**: 각 계층은 한 가지 책임만.

## 7. 계층별 구현 — Controller

```java
@Controller
@RequiredArgsConstructor
public class BoardController {

    private final BoardService boardService;

    @GetMapping("/board/list")
    public String list(Model model) {
        List<Board> boards = boardService.findAll();   // Service 호출
        model.addAttribute("boards", boards);
        return "board/list";
    }

    @PostMapping("/board")
    public String create(@ModelAttribute BoardDto dto) {
        boardService.create(dto);
        return "redirect:/board/list";
    }
}
```

**Controller 의 일**:
- HTTP 요청 받기 (`@GetMapping`, `@PostMapping`)
- 파라미터 바인딩 (`@RequestParam`, `@PathVariable`, `@ModelAttribute`)
- Service 호출
- Model 에 데이터 적재
- View 이름 반환 (또는 redirect)

**Controller 의 일이 아닌 것**:
- ❌ SQL 직접 작성 → DAO
- ❌ 복잡한 비즈니스 로직 → Service
- ❌ 트랜잭션 관리 → Service 에 `@Transactional`

## 8. 계층별 구현 — Service

```java
@Service
@Transactional
@RequiredArgsConstructor
public class BoardService {

    private final BoardDao boardDao;
    private final UserDao  userDao;

    public List<Board> findAll() {
        return boardDao.findAll();
    }

    public void create(BoardDto dto) {
        // 1) 비즈니스 검증
        if (dto.getTitle().length() > 100) {
            throw new IllegalArgumentException("제목 100자 이하");
        }
        // 2) 여러 DAO 조합
        User writer = userDao.findById(dto.getWriterId());
        Board board = Board.from(dto, writer);
        // 3) DAO 호출
        boardDao.insert(board);
    }
}
```

**Service 의 일**:
- 비즈니스 로직 (검증·계산·정책)
- **트랜잭션 경계** (`@Transactional`)
- 여러 DAO 조합
- 도메인 객체 변환

## 9. 계층별 구현 — DAO (Repository)

```java
public interface BoardDao {
    void insert(Board board);
    Board findById(int id);
    List<Board> findAll();
    void update(Board board);
    void delete(int id);
}

@Repository
@RequiredArgsConstructor
public class BoardDaoImpl implements BoardDao {

    private final JdbcTemplate jdbc;   // 또는 MyBatis SqlSession

    @Override
    public void insert(Board board) {
        jdbc.update(
            "INSERT INTO board(title, content, writer_id) VALUES (?, ?, ?)",
            board.getTitle(), board.getContent(), board.getWriterId()
        );
    }
}
```

**`@Repository` 의 특별한 기능**: DB 예외(`SQLException`) 를 Spring 의 `DataAccessException` 계층으로 변환 → 비즈니스 코드는 JDBC/JPA 차이 안 신경.

---

# Part D. Spring Web MVC 구현 어휘

## 10. `@Controller` + `@RequestMapping`

```java
@Controller
@RequestMapping("/board")               // 클래스 레벨 prefix
public class BoardController {

    @GetMapping("/list")                // 메서드 레벨 (Spring 4.3+)
    public String list() { ... }

    @PostMapping("")
    public String create() { ... }

    @GetMapping("/{id}")
    public String detail(@PathVariable int id) { ... }

    @PutMapping("/{id}")
    public String update(@PathVariable int id) { ... }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable int id) { ... }
}
```

**`@RequestMapping` 의 단축형 5종** (HTTP 메서드별):
- `@GetMapping`
- `@PostMapping`
- `@PutMapping`
- `@PatchMapping`
- `@DeleteMapping`

## 11. 파라미터 바인딩 어휘

```java
// 1) @RequestParam - 쿼리 스트링 / form
// GET /search?keyword=spring&page=1
@GetMapping("/search")
public String search(@RequestParam String keyword,
                       @RequestParam(defaultValue = "1") int page,
                       @RequestParam(required = false) String category) { ... }

// 2) @PathVariable - URL 경로 변수
// GET /board/42
@GetMapping("/board/{id}")
public String detail(@PathVariable int id) { ... }

// 3) @ModelAttribute - 객체 자동 바인딩 (form submit)
// POST /board (title=...&content=...)
@PostMapping("/board")
public String create(@ModelAttribute BoardDto dto) { ... }

// 4) @RequestBody - JSON 본문
// POST /api/board { "title": "...", "content": "..." }
@PostMapping("/api/board")
@ResponseBody
public Board create(@RequestBody BoardDto dto) { ... }

// 5) @RequestHeader / @CookieValue
@GetMapping("/info")
public String info(@RequestHeader("User-Agent") String ua,
                    @CookieValue("JSESSIONID") String sid) { ... }

// 6) HttpServletRequest / HttpSession 등 서블릿 API 직접
@GetMapping("/raw")
public String raw(HttpServletRequest req, HttpSession session) { ... }
```

## 12. Model 과 view 반환 패턴

```java
// 1) String + Model - 가장 일반적
@GetMapping("/home")
public String home(Model model) {
    model.addAttribute("user", currentUser);
    return "home";
}

// 2) ModelAndView - 둘을 함께 객체로
@GetMapping("/home")
public ModelAndView home() {
    ModelAndView mav = new ModelAndView("home");
    mav.addObject("user", currentUser);
    return mav;
}

// 3) redirect: prefix - 다른 URL 로 보냄 (POST-Redirect-GET)
@PostMapping("/board")
public String create(...) {
    boardService.create(...);
    return "redirect:/board/list";    // ← 새 GET 요청 유도
}

// 4) forward: prefix - 서버 내부 forward (URL 안 바뀜)
@GetMapping("/legacy")
public String legacy() {
    return "forward:/new-url";
}

// 5) @ResponseBody - view 가 아니라 직접 응답 body
@GetMapping("/api/me")
@ResponseBody
public User me() { return currentUser; }    // JSON 직렬화
```

## 13. POST-Redirect-GET 패턴

```
   ❌ Bad
   POST /board                --> create 후 그대로 list view 렌더
                                  +- F5 누르면 form 재제출 → 중복 등록!

   ✅ Good (POST-Redirect-GET)
   POST /board                --> 302 redirect + Location: /board/list
        |
        +- 브라우저 --GET /board/list--> list view 렌더
                                     F5 눌러도 안전 (GET 재시도)
```

```java
@PostMapping("/board")
public String create(@ModelAttribute BoardDto dto) {
    boardService.create(dto);
    return "redirect:/board/list";   // ← 패턴 핵심
}
```

---

## 14. 코드 깊게 — 게시판 풀스택

```java
// === Controller ===
@Controller
@RequestMapping("/board")
@RequiredArgsConstructor
public class BoardController {

    private final BoardService boardService;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("boards", boardService.findAll());
        return "board/list";
    }

    @GetMapping("/{id}")
    public String detail(@PathVariable int id, Model model) {
        model.addAttribute("board", boardService.findById(id));
        return "board/detail";
    }

    @GetMapping("/new")
    public String form() { return "board/form"; }

    @PostMapping
    public String create(@ModelAttribute BoardDto dto, RedirectAttributes ra) {
        int newId = boardService.create(dto);
        ra.addFlashAttribute("message", "등록 완료");
        return "redirect:/board/" + newId;
    }

    @GetMapping("/{id}/edit")
    public String editForm(@PathVariable int id, Model model) {
        model.addAttribute("board", boardService.findById(id));
        return "board/form";
    }

    @PostMapping("/{id}")
    public String update(@PathVariable int id, @ModelAttribute BoardDto dto) {
        boardService.update(id, dto);
        return "redirect:/board/" + id;
    }

    @PostMapping("/{id}/delete")
    public String delete(@PathVariable int id) {
        boardService.delete(id);
        return "redirect:/board";
    }
}

// === Service ===
@Service
@Transactional
@RequiredArgsConstructor
public class BoardService {

    private final BoardDao boardDao;

    public List<Board> findAll() { return boardDao.findAll(); }

    public Board findById(int id) {
        Board b = boardDao.findById(id);
        if (b == null) throw new NotFoundException();
        return b;
    }

    public int create(BoardDto dto) {
        if (dto.getTitle().length() > 100)
            throw new IllegalArgumentException("제목 100자 이하");
        Board b = Board.from(dto);
        boardDao.insert(b);
        return b.getId();
    }
}

// === DAO ===
@Repository
@RequiredArgsConstructor
public class BoardDao {

    private final JdbcTemplate jdbc;

    public List<Board> findAll() {
        return jdbc.query("SELECT * FROM board ORDER BY id DESC",
            (rs, n) -> new Board(...));
    }
}
```

---

## 15. 실전 패턴 / 자주 빠지는 함정

### MVC 패턴
- ❌ Controller 에서 SQL 직접 작성 ✅ DAO 에 위임
- ❌ Service 에서 HttpServletRequest 받음 ✅ Controller 에서 파라미터 추출 후 Service 에 전달
- ❌ DAO 에서 비즈니스 검증 ✅ Service 에서

### Spring MVC 어휘
- ❌ `@RequestParam` 의 `required = true` (기본) + 누락 → 400 에러 ✅ `required = false` + `defaultValue` 적절히
- ❌ POST 후 list view 직접 렌더 → F5 시 중복 등록 ✅ POST-Redirect-GET
- ❌ `@ResponseBody` 누락한 채 객체 반환 → 404 (view 못 찾음) ✅ `@ResponseBody` 또는 `@RestController`

### 3-Tier
- ❌ Controller 가 1000줄 → "fat controller" ✅ Service 추출
- ❌ Service 가 다른 Service 호출 안 하고 직접 DAO 호출 ✅ Service 끼리는 호출해도 됨, 단 순환 참조 주의
- ❌ DTO 와 Entity 안 분리 → DB 스키마가 API 응답에 노출 ✅ DTO 변환 계층 추가

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| 404 — `/board` 안 잡힘 | `@Controller` 누락 또는 컴포넌트 스캔 범위 밖 | 어노테이션 + 패키지 위치 |
| `@RequestParam` 이 null | required = true 인데 파라미터 누락 | defaultValue 또는 required = false |
| F5 누르면 중복 등록 | POST 후 view 직접 렌더 | redirect: 로 리다이렉트 |
| `@ResponseBody` 메서드인데 view 찾으려 함 | `@ResponseBody` 또는 `@RestController` 누락 | 어노테이션 추가 |
| `@PathVariable` 이 null | URL 패턴과 변수명 안 맞음 | `@PathVariable("id") int boardId` 명시 |
| Service 의 `@Transactional` 안 먹힘 | 같은 클래스 안 self-invocation | 다른 빈으로 분리 (AOP 강의 참조) |

---

## 16. 자가점검

1. MVC 패턴의 3 컴포넌트와 각 책임?
2. Spring MVC 의 요청 처리 흐름을 6단계로?
3. HandlerAdapter 가 풀어주는 문제는?
4. 3-Tier 아키텍처의 3계층과 각 책임?
5. `@RequestParam` 과 `@PathVariable` 의 차이?
6. POST-Redirect-GET 패턴이 풀어주는 문제는?
7. `@ResponseBody` 와 `@RestController` 의 관계?

<details><summary>풀이</summary>

1. **Model** (데이터·비즈니스 로직) / **View** (사용자에게 보여줄 UI) / **Controller** (Model 과 View 의 연결).
2. ① Client → DispatcherServlet ② HandlerMapping 으로 Controller 찾기 ③ HandlerAdapter 가 호출 ④ Controller 실행 → Model + View 이름 ⑤ ViewResolver 로 경로 변환 ⑥ View 가 렌더 → Client.
3. **다양한 Controller 형태**(인터페이스/어노테이션/함수형) 를 DispatcherServlet 이 통일된 인터페이스로 호출. 어댑터 패턴.
4. **Presentation (Controller)** — 요청·응답 / **Business (Service)** — 비즈니스 로직·트랜잭션 / **Data Access (DAO)** — DB 접근.
5. **`@RequestParam`**: 쿼리 스트링 또는 form 의 키-값 (`?id=42`). **`@PathVariable`**: URL 경로 일부 (`/board/{id}`).
6. **F5 누르면 form 재제출** 문제. POST 후 redirect 로 GET 새 요청 유도 → F5 누르면 GET 재시도라 안전.
7. **`@ResponseBody`**: 메서드 반환값을 JSON 직렬화 (view 안 거침). **`@RestController`** = `@Controller` + `@ResponseBody` (클래스 단위 모든 메서드에 적용).

</details>

---

## 17. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.9 MVC 패턴 (Servlet 한계·등장) | §1, §2 (Part A) |
| p.10 ~ p.19 Spring Web MVC (DispatcherServlet·HandlerMapping·HandlerAdapter·ViewResolver) | §3 ~ §5 (Part B) |
| p.20 ~ p.27 3-Tier 아키텍처 (Controller·Service·DAO) | §6 ~ §9 (Part C) |
| p.28 ~ p.41 Spring Web MVC 구현 (@Controller·@RequestMapping·파라미터 바인딩) | §10 ~ §13 (Part D) |
| p.42 마무리 | (생략) |

_42p 슬라이드 모두 커버._
