# Servlet — 퀴즈

> 16문항. 개념·적용·디버그·면접. 4부(웹 프로그래밍·Servlet 개념·실습·FrontController) 골고루.

---

### Q1. (개념) WAS 와 Web Server 의 차이?

<details><summary>정답</summary>

- **Web Server** (Apache, nginx): 정적 파일(HTML/CSS/JS/이미지) 응답
- **WAS** (Tomcat, Jetty): 자바 코드 실행해 동적 응답 생성

WAS 는 Web Server 기능도 포함하지만, 정적 파일은 Web Server 가 더 효율적이라 운영에선 nginx + Tomcat 나란히 배치하기도.

</details>

### Q2. (개념) HTTP 가 "Stateless" 라는 게 무슨 의미?

<details><summary>정답</summary>

**서버가 클라이언트 상태를 기억하지 않음** — 각 요청이 독립적. 그래서 로그인 유지·장바구니 등을 위해 **쿠키·세션** 같은 보조 메커니즘 필요.

</details>

### Q3. (개념) Servlet 의 생명주기 4단계?

<details><summary>정답</summary>

1. **객체 생성** (Tomcat 이 1번)
2. **`init()`** (1번 — 초기화)
3. **`service()` → `doGet`/`doPost`/...** (매 요청)
4. **`destroy()`** (1번 — Tomcat 종료 시)

</details>

### Q4. (개념) Servlet 은 왜 싱글톤이고, 그게 멀티스레드 환경에서 무엇을 의미하나?

<details><summary>정답</summary>

Tomcat 은 한 Servlet 클래스당 객체 1개만 생성 → 여러 요청이 같은 객체를 공유하면서 각자 스레드에서 실행.

**의미**: **인스턴스 필드는 thread-safe 하지 않음** → 사용자 데이터를 필드에 저장하면 race condition. 메서드 로컬 변수만 사용해야.

</details>

### Q5. (적용) 다음 form 의 입력을 받는 Servlet 의 `doPost`?

```html
<form method="POST" action="/login">
    <input name="id">
    <input name="password" type="password">
</form>
```

<details><summary>정답</summary>

```java
@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        req.setCharacterEncoding("UTF-8");

        String id = req.getParameter("id");
        String pwd = req.getParameter("password");

        if (userService.authenticate(id, pwd)) {
            req.getSession().setAttribute("loginUser", id);
            res.sendRedirect("/welcome");
        } else {
            req.setAttribute("error", "로그인 실패");
            req.getRequestDispatcher("/login.jsp").forward(req, res);
        }
    }
}
```

POST-Redirect-GET 패턴 적용 (로그인 성공 시 redirect).

</details>

### Q6. (개념) forward 와 redirect 의 차이 3가지?

<details><summary>정답</summary>

| 항목 | forward | redirect |
|--|--|--|
| URL 변경 | 안 바뀜 | 바뀜 |
| request 객체 | 같은 객체 유지 (`setAttribute` 공유) | 새 객체 (데이터 안 넘어감) |
| HTTP 요청 수 | 1번 | 2번 |
| 사용 시점 | 같은 작업 연속·검색결과 | POST-Redirect-GET·URL 변경 필요 |

</details>

### Q7. (적용) 한글 파라미터·응답 모두 깨지는 코드를 수정하시오.

```java
protected void doPost(HttpServletRequest req, HttpServletResponse res) {
    String name = req.getParameter("name");
    res.getWriter().println("<h1>" + name + "</h1>");
}
```

<details><summary>정답</summary>

```java
protected void doPost(HttpServletRequest req, HttpServletResponse res)
        throws ServletException, IOException {

    req.setCharacterEncoding("UTF-8");                          // ① 요청 인코딩
    res.setContentType("text/html;charset=UTF-8");              // ② 응답 인코딩

    String name = req.getParameter("name");
    res.getWriter().println("<h1>" + escapeHtml(name) + "</h1>"); // ③ XSS escape
}
```

3가지 모두 필요. ③ 은 사용자 입력을 그대로 HTML 에 출력할 때 항상.

</details>

### Q8. (개념) POST-Redirect-GET 패턴이 풀어주는 문제는?

<details><summary>정답</summary>

**F5(새로고침) 시 form 재제출** → 중복 등록. POST 후 forward 로 view 응답하면 브라우저가 그 응답을 POST 결과로 기억 → F5 시 다시 form 제출.

POST 후 `sendRedirect(...)` 로 GET 요청을 새로 만들면 F5 시 GET 재시도라 안전.

</details>

### Q9. (디버그) `res.getWriter()` 와 `res.getOutputStream()` 을 같이 썼더니 `IllegalStateException`. 이유?

<details><summary>정답</summary>

두 메서드는 **동시에 사용 불가**. 응답 본문은 하나의 스트림 — 어느 한쪽으로 통일해야.

- **텍스트 (HTML/JSON)**: `getWriter()`
- **바이너리 (파일·이미지)**: `getOutputStream()`

이미 한 쪽을 호출한 후 다른 쪽을 호출하면 예외.

</details>

### Q10. (적용) `@WebServlet` 으로 여러 URL 패턴을 매핑하고 기동 시 초기화하시오.

<details><summary>정답</summary>

```java
@WebServlet(
    urlPatterns = {"/hello", "/welcome", "/greet/*"},
    loadOnStartup = 1
)
public class HelloServlet extends HttpServlet {
    @Override
    public void init() throws ServletException {
        // 무거운 초기화 (DB 풀, 캐시 워밍 등)
    }
}
```

`loadOnStartup` 으로 Tomcat 기동 시 미리 객체 생성 (첫 요청 지연 X). 패턴 매칭: `/hello` 정확 매치, `/greet/*` prefix 매치.

</details>

### Q11. (디버그) `getParameter("hobbies")` 가 한 값만 반환. 폼에는 체크박스 여러 개. 원인?

<details><summary>정답</summary>

`getParameter` 는 **첫 번째 값만** 반환. 다중 값은 `getParameterValues("hobbies")`:

```html
<input type="checkbox" name="hobbies" value="reading">
<input type="checkbox" name="hobbies" value="coding">
<input type="checkbox" name="hobbies" value="gaming">
```

```java
String[] hobbies = req.getParameterValues("hobbies");   // 다중 값
// String single = req.getParameter("hobbies");          // 첫 번째만
```

</details>

### Q12. (적용) FrontController 패턴으로 `/board/list`, `/board/detail`, `/board/write` 를 처리하시오.

<details><summary>정답</summary>

```java
@WebServlet("/board/*")
public class BoardFrontController extends HttpServlet {

    private final Map<String, Controller> handlers = Map.of(
        "/list",   new ListController(),
        "/detail", new DetailController(),
        "/write",  new WriteController()
    );

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        req.setCharacterEncoding("UTF-8");

        String path = req.getRequestURI()
                          .substring(req.getContextPath().length() + "/board".length());

        Controller c = handlers.get(path);
        if (c == null) { res.sendError(404); return; }

        String view = c.handle(req, res);

        if (view.startsWith("redirect:")) {
            res.sendRedirect(view.substring("redirect:".length()));
        } else {
            req.getRequestDispatcher("/WEB-INF/views/" + view + ".jsp")
               .forward(req, res);
        }
    }
}

public interface Controller {
    String handle(HttpServletRequest req, HttpServletResponse res);
}
```

</details>

### Q13. (디버그) Tomcat 기동 시 Servlet 의 `init()` 이 호출되지 않음. 첫 요청 시 늦게 호출됨. 원인?

<details><summary>정답</summary>

기본 동작은 **lazy initialization** — 첫 요청 시점에 객체 생성 + `init` 호출. 기동 시 미리 호출하려면:

```java
@WebServlet(urlPatterns = "/hello", loadOnStartup = 1)
```

또는 `web.xml` 의 `<load-on-startup>1</load-on-startup>`. 숫자가 작을수록 먼저.

DB 풀 초기화 등 무거운 작업이 있으면 `loadOnStartup` 필수.

</details>

### Q14. (면접) "Servlet 이 싱글톤이라는 게 무슨 의미인지, 실무에서 어떤 주의가 필요한지 설명하시오."

<details><summary>정답</summary>

**의미**: Tomcat 이 한 Servlet 클래스당 객체 1개만 생성 → 모든 요청이 같은 객체 공유.

**멀티스레드 환경**: 각 요청은 자체 스레드 → 동시에 같은 인스턴스 필드 접근 가능.

**주의**:
1. **인스턴스 필드에 사용자 데이터 X** — `private String currentUser` 같은 거 절대 금지. race condition.
2. **메서드 로컬 변수만** — 각 스레드의 스택에 별도 존재, 안전.
3. **공유 상태가 필요하면 동기화** — `ConcurrentHashMap`, `AtomicInteger` 등 thread-safe 자료구조.
4. **DB 풀 같은 자원은 thread-safe 보장된 라이브러리 사용** — HikariCP 등.

이 원칙이 그대로 Spring 의 빈에도 적용됨 (Spring 빈도 기본 싱글톤).

</details>

### Q15. (면접) "FrontController 패턴이 Spring MVC 와 어떻게 연결되나요?"

<details><summary>정답</summary>

**Spring 의 `DispatcherServlet` 이 정확히 FrontController 의 구현체**.

```
[옛 Servlet 시대]
  서블릿 N개 + web.xml 매핑 N개

[FrontController 패턴 (수동)]
  단일 진입점 + HashMap 라우팅 + Controller 인터페이스

[Spring MVC]
  DispatcherServlet + HandlerMapping (자동) + @Controller (어노테이션)
```

Spring 은 같은 패턴을 **어노테이션·자동 등록·자동 설정** 으로 자동화한 것:
- `@Controller` + `@RequestMapping` → HandlerMapping 자동 구축
- View 이름 → ViewResolver 가 자동 변환
- 파라미터 바인딩 → `@RequestParam` 으로 자동

원리(FrontController)를 알면 Spring 의 추상화가 마법이 아닌 자연스러운 진화로 보임.

</details>

### Q16. (면접) "Servlet 에서 한글이 깨지는 모든 경우와 해결책을 정리하시오."

<details><summary>정답</summary>

**한글 깨짐 4가지 시점**:

1. **요청 파라미터 (POST body)**:
   ```java
   req.setCharacterEncoding("UTF-8");   // doPost 첫 줄
   ```

2. **요청 파라미터 (GET query)**: Tomcat 8+ 는 기본 UTF-8. 옛 Tomcat 은 `server.xml` 의 `URIEncoding="UTF-8"` 설정 필요.

3. **응답 본문**:
   ```java
   res.setContentType("text/html;charset=UTF-8");
   res.setCharacterEncoding("UTF-8");
   ```

4. **JSP 페이지**:
   ```jsp
   <%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
   ```

추가:
- **HTML 의 `<meta charset="UTF-8">`** — 브라우저 인코딩 힌트
- **DB 연결 URL 에 `useUnicode=true&characterEncoding=UTF-8`** — DB 통신 인코딩
- **`web.xml` 의 `CharacterEncodingFilter`** — 모든 요청에 자동 적용 (가장 깔끔)

```xml
<filter>
    <filter-name>encodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
        <param-name>encoding</param-name>
        <param-value>UTF-8</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>encodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

</details>
