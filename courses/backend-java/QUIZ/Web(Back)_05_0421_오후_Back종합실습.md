# Back 종합 실습 - 퀴즈

> 14문항. 1~5강(Servlet · JSP · Cookie/Session · EL/JSTL · Filter) 통합 시나리오.

---

### Q1. (개념) Web Back 1~5강 각 구성요소가 한 게시판 프로젝트에서 맡는 책임을 한 줄씩 정리.

<details><summary>정답</summary>

- **Servlet (1강)**: Controller. CRUD 진입점·요청 파싱·forward/redirect.
- **JSP (2강)**: View. HTML 렌더링. `WEB-INF/views/` 안에서 forward 통해서만 접근.
- **Cookie/Session (3강)**: 상태. 로그인 세션(서버), 자동 로그인 쿠키(클라).
- **EL/JSTL (4강)**: View 표현식·반복·조건. JSP 안 자바 코드 제거.
- **Filter (5강)**: 공통 횡단 관심사. 인코딩·인증·로깅·에러 페이지.

</details>

### Q2. (개념) `EncodingFilter` 와 `AuthFilter` 등록 순서 바꾸면?

<details><summary>정답</summary>

Auth 가 먼저면 한글 로그인 ID·에러 메시지가 깨질 수 있음. **인코딩은 모든 처리 앞에**.

순서 보장: `@WebFilter` 만으로는 컨테이너 의존 → web.xml `<filter-mapping>` 순서 또는 `FilterRegistrationBean.setOrder(int)`.

</details>

### Q3. (개념) 새로고침해도 같은 글이 두 번 등록되지 않게 하는 패턴 이름과 흐름?

<details><summary>정답</summary>

**PRG (POST-Redirect-GET)**.

```
[브라우저] --POST /board/write--> [Servlet]
                                       | insert
                                       | sendRedirect("/board")
[브라우저] <--302 Location: /board--   |
[브라우저] --GET /board--> [Servlet] --forward--> list.jsp
```

마지막 요청이 GET 이라 F5 시 멱등. forward 면 form 데이터 재전송 → 중복 등록.

</details>

### Q4. (적용) `/board/list` 비로그인 허용, `/board/write` 만 막으려면?

<details><summary>정답</summary>

**방법 1: urlPatterns 명시**
```java
@WebFilter(urlPatterns = {"/board/write/*", "/board/edit/*", "/mypage/*"})
public class AuthFilter implements Filter { ... }
```

**방법 2: 모든 요청 + whitelist**
```java
@WebFilter("/*")
public class AuthFilter implements Filter {
    private static final Set<String> PUBLIC =
        Set.of("/", "/login", "/signup", "/board/list", "/board/detail", "/css", "/js");
    // PUBLIC startsWith → chain.doFilter
}
```

규모 커질수록 방법 1 이 명시적이고 안전.

</details>

### Q5. (적용) 글 작성자만 수정 가능하게 서버 검증 (Authorization)?

<details><summary>정답</summary>

**Servlet 단계**:
```java
Long userId = (Long) session.getAttribute("userId");
Board b = boardDao.findById(id);
if (b == null) throw new NotFoundException();
if (!b.getWriterId().equals(userId)) throw new ForbiddenException();
```

**또는 SQL WHERE 절**:
```sql
UPDATE boards SET title=?, content=? WHERE id = ? AND writer_id = ?
```
영향 행 0 이면 본인 아님 → 거절.

⚠️ **클라이언트 hidden field 의 writerId 신뢰 금지**. 항상 세션의 userId 와 DB 의 writerId 만으로 비교.

</details>

### Q6. (디버그) 같은 글 새로고침마다 조회수 증가 버그. 쿠키로 막기?

<details><summary>정답</summary>

```java
String ckName = "viewed_" + boardId;
boolean already = req.getCookies() != null && Arrays.stream(req.getCookies())
    .anyMatch(c -> c.getName().equals(ckName));
if (!already) {
    boardDao.incrementView(boardId);
    Cookie c = new Cookie(ckName, "1");
    c.setMaxAge(60 * 60 * 24);   // 1일
    c.setPath("/");
    resp.addCookie(c);
}
```

대규모면 **Redis** 의 `SETNX viewed:{boardId}:{userId} EX 86400` 권장.

</details>

### Q7. (디버그) JSP `<h1>${board.title}</h1>` 에서 XSS. 한 줄 수정?

<details><summary>정답</summary>

```jsp
<h1><c:out value="${board.title}"/></h1>
```

또는:
```jsp
<%@ taglib prefix="fn" uri="jakarta.tags.functions" %>
<h1>${fn:escapeXml(board.title)}</h1>
```

`${board.title}` 만은 escape 안 함 → `<script>` 삽입 가능 → XSS.

</details>

### Q8. (적용) 비로그인 사용자가 `/board/write` GET. 로그인 후 원래 페이지로 돌아오게?

<details><summary>정답</summary>

```java
// AuthFilter
session.setAttribute("returnUrl", req.getRequestURI());
resp.sendRedirect(req.getContextPath() + "/login");

// LoginServlet doPost 끝
String returnUrl = (String) session.getAttribute("returnUrl");
session.removeAttribute("returnUrl");
resp.sendRedirect(returnUrl != null ? returnUrl : req.getContextPath() + "/");
```

⚠️ `returnUrl` 외부 URL (`http://evil.com`) 허용 시 **Open Redirect** 취약. 같은 도메인·contextPath 검증 필요.

</details>

### Q9. (디버그) 인메모리 `BoardStore` 싱글톤 thread safety?

<details><summary>정답</summary>

```java
public class BoardStore {
    private static final BoardStore I = new BoardStore();
    public static BoardStore get() { return I; }

    private final List<Board> list = Collections.synchronizedList(new ArrayList<>());
    private final AtomicLong seq = new AtomicLong();

    public long add(Board b) {
        long id = seq.incrementAndGet();
        b.setId(id);
        list.add(b);
        return id;
    }
}
```

`synchronizedList` + `AtomicLong`. 또는 `ConcurrentHashMap<Long, Board>`. **운영은 결국 DB**.

</details>

### Q10. (적용) 로그아웃 시 세션과 자동 로그인 쿠키 둘 다 정리하기.

<details><summary>정답</summary>

```java
@WebServlet("/logout")
public class LogoutServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException {
        // 1. 세션 무효화
        HttpSession session = req.getSession(false);
        if (session != null) session.invalidate();

        // 2. 자동 로그인 쿠키 삭제
        Cookie c = new Cookie("REMEMBER_TOKEN", "");
        c.setMaxAge(0);
        c.setPath("/");
        c.setHttpOnly(true);
        res.addCookie(c);

        // 3. DB 에 저장된 remember token 도 삭제 (보안 강화)
        // userDao.clearRememberToken(userId);

        res.sendRedirect(req.getContextPath() + "/");
    }
}
```

세션만 정리하고 쿠키 안 지우면 다음 요청 시 다시 자동 로그인 → 의도 위반.

</details>

### Q11. (적용) Service → DAO 사이에 트랜잭션을 (Spring 없이) 수동 적용.

<details><summary>정답</summary>

```java
public class BoardService {
    private final DataSource ds;

    public void writeWithAttachments(Board b, List<Attachment> files) throws SQLException {
        try (Connection con = ds.getConnection()) {
            con.setAutoCommit(false);
            try {
                long id = boardDao.insert(con, b);
                for (Attachment f : files) {
                    f.setBoardId(id);
                    attachmentDao.insert(con, f);
                }
                con.commit();
            } catch (Exception e) {
                con.rollback();
                throw e;
            }
        }
    }
}
```

DAO 가 Connection 받는 형태. 또는 ThreadLocal<Connection>. Spring 의 `@Transactional` 이 이걸 다 자동화.

</details>

### Q12. (디버그) `BoardListServlet` 의 `init()` 에서 `getServletContext().getAttribute("boardService")` 가 null.

<details><summary>정답</summary>

**ServletContextListener 가 등록 안 됐거나 순서 문제**.

```java
@WebListener
public class AppLifecycleListener implements ServletContextListener {
    @Override
    public void contextInitialized(ServletContextEvent sce) {
        DataSource ds = createDataSource();
        BoardService service = new BoardService(ds);
        sce.getServletContext().setAttribute("boardService", service);
    }
}
```

확인:
1. `@WebListener` 또는 `web.xml` 의 `<listener>` 등록
2. `contextInitialized` 가 모든 Servlet `init()` 보다 먼저 실행됨 (보장됨)
3. 속성 이름 오타 (`boardService` vs `BoardService`)

</details>

### Q13. (면접) 한 미니 게시판 구현에서 5강의 컴포넌트 결합이 왜 좋은 학습 사례인가?

<details><summary>정답</summary>

1. **책임 분리 체감**: Servlet=Controller, JSP=View, Service=Logic, DAO=Storage. 각 변경이 다른 곳에 영향 없음.
2. **MVC 패턴의 실증**: 디자이너가 JSP 만 수정해도 컴파일 불필요. 백엔드 변경해도 view 영향 없음.
3. **횡단 관심사 분리**: 인증을 모든 Servlet 에 흩뿌리지 않고 Filter 1개로 처리. AOP 의 직관적 선행.
4. **상태 관리의 두 축**: 서버(Session) vs 클라(Cookie). 보안과 UX 의 trade-off.
5. **Spring 의 동기**: 이 구조를 더 우아하게(`@Controller`, `@Autowired`, `@Transactional`) 만든 게 Spring. 왜 Spring 이 필요한지 체감.

</details>

### Q14. (면접) "이 구조를 그대로 Spring MVC 로 옮기면 무엇이 바뀌나?"

<details><summary>정답</summary>

```
[Servlet 구조]                          [Spring MVC 구조]
@WebServlet("/board")              ->   @Controller + @RequestMapping("/board")
HttpServletRequest 직접 파싱       ->   @RequestParam, @ModelAttribute, @PathVariable
req.setAttribute + forward         ->   Model + return "board/list"
HttpSession 직접                   ->   @SessionAttribute, @SessionScope
@WebFilter (서블릿 표준)           ->   HandlerInterceptor (Spring) + Filter (그대로 가능)
ServletContextListener             ->   @PostConstruct on @Configuration
수동 Connection / Transaction      ->   @Transactional + DataSourceTransactionManager
new Service(new Dao())             ->   @Autowired (DI Container)
web.xml <error-page>               ->   @ControllerAdvice + @ExceptionHandler
```

**유지**: HTTP 표준 (Cookie, Session, EL/JSTL, Filter) 은 그대로. Spring 은 그 위에 추상화.

**바뀌는 멘탈모델**: "객체를 직접 만들고 연결한다" -> "선언만 하면 컨테이너가 연결해 준다" (IoC).

</details>
