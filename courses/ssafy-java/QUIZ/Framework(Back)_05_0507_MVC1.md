# Spring MVC 1 — 퀴즈

> 16문항. 개념·적용·디버그·면접. 4부(MVC 패턴·Web MVC 개요·3-Tier·MVC 구현) 골고루.

---

### Q1. (개념) MVC 패턴의 3 컴포넌트와 각 책임?

<details><summary>정답</summary>

- **Model**: 데이터 + 비즈니스 로직. DTO/Entity/Service/DAO. UI 무관.
- **View**: 사용자에게 보여줄 UI. JSP/Thymeleaf/JSON. 비즈니스 로직 모름.
- **Controller**: Model 과 View 의 연결. 요청 받아 Model 호출 + View 결정. 비즈니스 로직 X.

</details>

### Q2. (개념) Spring Web MVC 요청 처리 흐름 6단계?

<details><summary>정답</summary>

1. Client → **DispatcherServlet** (FrontController)
2. DispatcherServlet → **HandlerMapping** 에 "이 요청 누가 처리?" 질의
3. HandlerMapping → 매칭된 Controller 반환
4. **HandlerAdapter** 가 Controller 메서드 호출
5. Controller 가 비즈니스 로직 호출 + Model 적재 + View 이름 반환
6. **ViewResolver** 로 view 이름 → 실제 경로 → **View** 가 HTML 렌더 → Client

</details>

### Q3. (개념) HandlerAdapter 가 풀어주는 문제는?

<details><summary>정답</summary>

**다양한 Controller 형태를 DispatcherServlet 이 통일된 인터페이스로 호출** 하는 어댑터 패턴.

- 옛 인터페이스 기반 Controller
- `@Controller` + `@RequestMapping` 어노테이션 방식
- 함수형 HandlerFunction (WebFlux)

각 형태마다 HandlerAdapter 가 따로 있고, DispatcherServlet 은 이걸 통해 어떤 형태든 호출.

</details>

### Q4. (개념) 3-Tier 아키텍처의 3계층과 각 책임?

<details><summary>정답</summary>

| 계층 | 어노테이션 | 책임 |
|--|--|--|
| Presentation | `@Controller` | 요청·응답, 파라미터 변환, View 결정 |
| Business | `@Service` | 비즈니스 로직, 트랜잭션 경계, 여러 DAO 조합 |
| Data Access | `@Repository` | SQL·DB 접근만, CRUD |

SRP(단일 책임 원칙) 준수 — 각 계층은 한 가지 책임.

</details>

### Q5. (적용) 다음 컨트롤러의 메서드를 5가지 HTTP 메서드별 어노테이션으로 작성하시오.

```
GET    /board/list        → 목록
POST   /board             → 등록
GET    /board/{id}        → 상세
PUT    /board/{id}        → 수정
DELETE /board/{id}        → 삭제
```

<details><summary>정답</summary>

```java
@Controller
@RequestMapping("/board")
public class BoardController {

    @GetMapping("/list")
    public String list() { ... }

    @PostMapping
    public String create() { ... }

    @GetMapping("/{id}")
    public String detail(@PathVariable int id) { ... }

    @PutMapping("/{id}")
    public String update(@PathVariable int id) { ... }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable int id) { ... }
}
```

</details>

### Q6. (개념) `@RequestParam` 과 `@PathVariable` 의 차이? 각 예시는?

<details><summary>정답</summary>

- **`@RequestParam`**: 쿼리 스트링 또는 form 의 키-값
  - 예: `GET /search?keyword=spring&page=1` → `@RequestParam String keyword`
- **`@PathVariable`**: URL 경로 일부
  - 예: `GET /board/42` + `@GetMapping("/board/{id}")` → `@PathVariable int id`

REST API 의 자원 식별엔 `@PathVariable`, 검색·필터엔 `@RequestParam`.

</details>

### Q7. (적용) POST form 으로 다음 필드를 받는 Controller?

```html
<form method="POST" action="/board">
    <input name="title">
    <input name="content">
    <input name="writerId">
</form>
```

<details><summary>정답</summary>

```java
@Data
public class BoardDto {
    private String title;
    private String content;
    private long   writerId;
}

@PostMapping("/board")
public String create(@ModelAttribute BoardDto dto) {
    boardService.create(dto);
    return "redirect:/board/list";
}
```

`@ModelAttribute` 는 form 의 name 과 DTO 필드명을 매칭해 자동 바인딩. Spring 4.3+ 는 객체 파라미터에서 `@ModelAttribute` 생략 가능.

</details>

### Q8. (개념) POST-Redirect-GET 패턴이 풀어주는 문제는?

<details><summary>정답</summary>

**F5(새로고침) 누르면 form 재제출** 문제. POST 후 view 를 그대로 렌더하면 브라우저가 그 페이지를 POST 응답으로 기억 → F5 시 "form 재제출하시겠습니까?" + 그대로 진행 시 **중복 등록**.

POST 후 `redirect:/board/list` 로 보내면 브라우저가 GET 요청을 새로 만듦 → F5 시 GET 재시도라 안전.

</details>

### Q9. (디버그) `@ResponseBody` 없이 객체를 반환했더니 view 못 찾는 오류. 원인과 해결?

<details><summary>정답</summary>

**원인**: `@Controller` 메서드의 반환값은 기본적으로 view 이름. 객체 반환 시 객체의 `toString()` 을 view 이름으로 해석 → 그런 view 없음 → 404.

**해결**:
- 단일 메서드: `@ResponseBody` 추가
- 클래스 전체가 API 면: `@RestController` (= `@Controller` + `@ResponseBody`)

```java
@GetMapping("/api/me")
@ResponseBody
public User me() { return currentUser; }     // JSON 직렬화
```

</details>

### Q10. (적용) 다음 controller 를 3-Tier 로 분리하시오.

```java
@Controller
public class BoardController {
    @Autowired private JdbcTemplate jdbc;

    @PostMapping("/board")
    public String create(@RequestParam String title) {
        if (title.length() > 100) throw new RuntimeException("길이 초과");
        jdbc.update("INSERT INTO board(title) VALUES (?)", title);
        return "redirect:/board";
    }
}
```

<details><summary>정답</summary>

```java
// Controller — 요청만
@Controller
@RequiredArgsConstructor
public class BoardController {
    private final BoardService boardService;

    @PostMapping("/board")
    public String create(@RequestParam String title) {
        boardService.create(title);
        return "redirect:/board";
    }
}

// Service — 비즈니스 로직 + 트랜잭션
@Service
@RequiredArgsConstructor
@Transactional
public class BoardService {
    private final BoardDao boardDao;

    public void create(String title) {
        if (title.length() > 100)
            throw new IllegalArgumentException("제목 100자 이하");
        boardDao.insert(title);
    }
}

// DAO — SQL 만
@Repository
@RequiredArgsConstructor
public class BoardDao {
    private final JdbcTemplate jdbc;

    public void insert(String title) {
        jdbc.update("INSERT INTO board(title) VALUES (?)", title);
    }
}
```

3 계층 분리 + DI + 트랜잭션 + 검증 책임 분리.

</details>

### Q11. (디버그) `@RequestParam String keyword` 인데 호출 시 400 에러. 원인?

<details><summary>정답</summary>

`@RequestParam` 은 기본 `required = true`. 파라미터 누락 시 400.

**해결**:
```java
// 선택 사항으로
@RequestParam(required = false) String keyword

// 또는 기본값
@RequestParam(defaultValue = "") String keyword

// 또는 Optional 로
@RequestParam Optional<String> keyword
```

</details>

### Q12. (디버그) `@PathVariable int id` 인데 null. 원인 후보?

<details><summary>정답</summary>

1. **URL 패턴과 변수명 불일치**:
   ```java
   @GetMapping("/board/{boardId}")        // URL 은 boardId
   public String detail(@PathVariable int id) { }   // 변수는 id
   ```
   해결: `@PathVariable("boardId") int id` 또는 변수명을 boardId 로 통일.

2. **자바 컴파일 시 `-parameters` 옵션 누락** → 파라미터 이름 정보 손실 → 매칭 실패.
   해결: `pom.xml` 또는 `build.gradle` 에 `-parameters` 추가, 또는 `@PathVariable("id")` 명시.

</details>

### Q13. (적용) flash attribute 로 redirect 후 메시지를 한 번만 전달하시오.

<details><summary>정답</summary>

```java
@PostMapping("/board")
public String create(@ModelAttribute BoardDto dto, RedirectAttributes ra) {
    boardService.create(dto);
    ra.addFlashAttribute("message", "등록 완료");   // 다음 요청에 1회만 전달
    return "redirect:/board/list";
}
```

`/board/list` 페이지에서 `${message}` 로 접근 가능. 새로고침 시 사라짐 (URL 에 안 노출되고 1회용).

</details>

### Q14. (면접) "왜 Controller 에서 DB 호출을 직접 하지 않고 Service 를 거치나요?"

<details><summary>정답</summary>

1. **단일 책임 원칙(SRP)**: Controller 는 요청·응답만, Service 는 비즈니스 로직만, DAO 는 DB 만.
2. **트랜잭션 경계**: `@Transactional` 을 Service 에 둠. Controller 에 두면 view 렌더 중 예외 시 트랜잭션 상태 모호.
3. **테스트 가능성**: Service 는 HttpServletRequest 없이 호출 가능. Controller 는 MockMvc 필요.
4. **재사용**: 같은 비즈니스 로직을 REST API + 웹 + 배치 등 여러 진입점에서 호출.
5. **여러 DAO 조합**: 한 비즈니스 동작이 여러 DAO 를 호출 → Service 에서 묶음.

</details>

### Q15. (면접) "DispatcherServlet 이 'FrontController' 라 불리는 이유는?"

<details><summary>정답</summary>

**FrontController 디자인 패턴** — 모든 클라이언트 요청을 하나의 진입점(Front) 에서 받아 적절한 핸들러로 분배하는 패턴.

이전 Servlet 시대엔 각 URL 마다 별도 서블릿 + `web.xml` 매핑이 필요했지만, FrontController 는:
- 공통 부가 처리(인증·로깅·인코딩) 를 한 곳에 통합
- 라우팅 로직을 별도 컴포넌트(HandlerMapping) 로 분리
- View 결정도 별도 컴포넌트(ViewResolver) 로 분리

이게 Spring MVC 의 핵심. `DispatcherServlet` 은 정확히 FrontController 의 구현체.

</details>

### Q16. (면접) "`@Service` 클래스 안에서 다른 `@Service` 를 주입받아 쓰는 게 가능한가요?"

<details><summary>정답</summary>

**가능하고, 흔히 쓴다**. 한 비즈니스 동작이 여러 도메인을 다룰 때 자연스럽게 발생.

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final ProductService productService;
    private final PaymentService payService;
    private final NotificationService notifyService;

    @Transactional
    public Order order(OrderRequest req) {
        Product p = productService.lockStock(req.productId(), req.qty());
        Payment pay = payService.charge(req.userId(), p.price());
        Order order = orderDao.insert(...);
        notifyService.sendOrderConfirm(order);
        return order;
    }
}
```

**주의 사항**:
- **순환 참조 금지** — A → B → A 면 빈 생성 시 `BeanCurrentlyInCreationException`
- **트랜잭션 전파 정책**: 호출하는 Service 의 `@Transactional` 이 호출되는 Service 메서드까지 자동 전파 (기본 `REQUIRED`)

</details>
