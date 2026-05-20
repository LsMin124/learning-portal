# Servlet — 웹 프로그래밍 · Servlet 개념 · 실습 · FrontController

> **이 강의는 무엇인가**: HTTP 요청을 자바 객체로 다루는 표준 기술 **Servlet** 의 동작 원리. 웹 프로그래밍의 큰 그림부터 Servlet 등록·라이프사이클·FrontController 패턴까지.
> **왜 배우는가**: Spring MVC 의 모든 것이 Servlet 위에 만들어졌다. `DispatcherServlet` 부터 `HttpServletRequest/Response` 까지 — 원리를 모르면 Spring 의 추상화가 마법으로 보임.

---

## 들어가기 전에

- **선수**: Java OOP, HTTP 기본 (요청·응답·상태코드 정도), HTML.
- **마인드셋**: "HTTP 는 단순한 텍스트 프로토콜, Servlet 은 그걸 자바 객체로 다루는 도구" 라는 본질 의식.

---

# Part A. 웹 프로그래밍

## 1. 정적 페이지 vs 동적 페이지

```
   정적 페이지 (Static Web)              동적 페이지 (Dynamic Web)
   ---------------------              ------------------------

   [Client] --GET /index.html--> [Server]
   [Client] <--HTML 그대로------ [Server]
                                       [Server (WAS)]
                                        |
                                        ▼ 자바 코드 실행
                                       [DB·Logic]
                                        |
                                        ▼ HTML 동적 생성
   [Client] <----HTML----------  [Server]
```

| | 정적 | 동적 |
|--|--|--|
| 응답 | 파일 그대로 | 코드 실행 결과 |
| 서버 | Web Server (Apache, nginx) | WAS (Tomcat, Jetty) |
| 사용자별 | 모두 동일 | 다름 (로그인·검색·필터) |

**WAS (Web Application Server)** — Tomcat 같은 서블릿 컨테이너가 Java 코드를 실행해 동적 응답 생성.

## 2. 클라이언트-서버 + HTTP 흐름

```
[Browser]                            [Web Server / WAS]
   |
   | ① HTTP Request
   |  GET /board?id=42 HTTP/1.1
   |  Host: example.com
   |  Accept: text/html
   |  Cookie: JSESSIONID=...
   |
   +-------------------------------->
   |                                      ② 요청 분석·DB 조회·HTML 생성
   |
   | ③ HTTP Response
   |  HTTP/1.1 200 OK
   |  Content-Type: text/html
   |  Set-Cookie: ...
   |
   |  <html>...
   | <--------------------------------
   |
   ▼ HTML 렌더
[화면]
```

**HTTP 의 특징**:
- **무상태 (Stateless)** — 매 요청이 독립적, 서버가 클라 상태 안 기억 (그래서 쿠키·세션 필요)
- **단방향** — 클라가 요청, 서버가 응답. 서버가 먼저 보낼 수 없음 (WebSocket 으로 보완)
- **텍스트 기반** — 사람도 읽을 수 있는 평문 (HTTP/2 부턴 이진)

---

# Part B. Servlet 개념

## 3. Servlet 정의

- **Server + Applet** 합성어
- **WAS 에서 실행되는 Java 프로그램** — HTTP 요청을 받고 응답을 생성
- **웹페이지를 동적으로 생성** (HTML 을 자바 코드로 만들어 보냄)
- 유지보수성·재활용성 우수 — 라이브러리·DB 자유 활용

```
[Browser] --GET /hello--> [Tomcat]
                              |
                              ▼ 매핑된 Servlet 찾기
                          HelloServlet.doGet()
                              |
                              ▼ HTML 생성
                          response.getWriter()
                                .println("<h1>Hello</h1>")
                              |
                              ▼
[Browser] <----HTML------ [Tomcat]
```

## 4. Servlet 의 생명주기 (Lifecycle)

```
서블릿 클래스
    |
    | ① 클라가 처음 요청
    ▼
[Tomcat 이 객체 생성]    ← 1번만
    |
    ▼
init()                   ← 1번만 (초기화)
    |
    ▼
service()                ← 매 요청
    +-> doGet / doPost / doPut / doDelete ...
    (요청 1, 요청 2, ..., 요청 N - 모두 같은 객체 + 자체 스레드)
    |
    | (Tomcat 종료 또는 서블릿 제거 시)
    ▼
destroy()                ← 1번만 (정리)
```

| 메서드 | 시점 | 횟수 |
|--|--|--|
| `init(ServletConfig)` | 첫 요청 시 객체 생성 후 | **1번** |
| `service(req, res)` | 매 요청마다 (Tomcat 이 호출) | N번 |
| `doGet`/`doPost`/`doPut`/`doDelete` | service 가 메서드별 분기 호출 | N번 |
| `destroy()` | Tomcat 종료 / 서블릿 제거 시 | **1번** |

**중요**: Servlet 은 **싱글톤** — Tomcat 이 한 클래스당 객체 1개만 생성. 멀티스레드 환경 → **인스턴스 필드는 thread-safe 하지 않음** (각 요청은 자체 스레드).

## 5. Servlet 작성 — 표준

```java
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;

@WebServlet("/hello")        // URL 매핑 (Servlet 3.0+)
public class HelloServlet extends HttpServlet {

    @Override
    public void init() throws ServletException {
        System.out.println("HelloServlet 초기화");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // 1) 요청 파라미터
        String name = req.getParameter("name");

        // 2) 응답 설정
        res.setContentType("text/html;charset=UTF-8");

        // 3) HTML 출력
        try (PrintWriter out = res.getWriter()) {
            out.println("<html><body>");
            out.println("<h1>Hello, " + name + "</h1>");
            out.println("</body></html>");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        // POST 처리
    }

    @Override
    public void destroy() {
        System.out.println("HelloServlet 종료");
    }
}
```

**`HttpServletRequest` 의 주요 메서드**:
| 메서드 | 의미 |
|--|--|
| `getParameter("name")` | 쿼리/폼 파라미터 |
| `getParameterValues("hobbies")` | 다중 값 (체크박스) |
| `getMethod()` | "GET", "POST" 등 |
| `getRequestURI()` | "/contextPath/path" |
| `getContextPath()` | "/contextPath" |
| `getServletPath()` | 매핑된 경로 |
| `getHeader("User-Agent")` | 요청 헤더 |
| `getCookies()` | 모든 쿠키 |
| `getSession()` | 세션 (없으면 생성) |
| `setAttribute("key", value)` | request scope 에 데이터 |
| `getRequestDispatcher(...).forward(...)` | 서버 내부 forward |

**`HttpServletResponse` 의 주요 메서드**:
| 메서드 | 의미 |
|--|--|
| `setContentType("text/html;charset=UTF-8")` | 응답 MIME + 인코딩 |
| `setStatus(200)` | 상태 코드 |
| `setHeader("X-Custom", "v")` | 응답 헤더 |
| `addCookie(cookie)` | 쿠키 굽기 |
| `getWriter()` | 텍스트 출력 (`PrintWriter`) |
| `getOutputStream()` | 바이너리 (파일·이미지) |
| `sendRedirect("/path")` | 302 redirect |

## 6. Servlet 등록 — 2가지 방법

### 방법 1: `@WebServlet` 어노테이션 (Servlet 3.0+, 권장)

```java
@WebServlet(urlPatterns = {"/hello", "/welcome"}, loadOnStartup = 1)
public class HelloServlet extends HttpServlet { ... }
```

`loadOnStartup = 1` — Tomcat 기동 시 미리 객체 생성 (첫 요청 지연 X).

### 방법 2: `web.xml` (옛 방식)

```xml
<web-app>
    <servlet>
        <servlet-name>hello</servlet-name>
        <servlet-class>com.example.HelloServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>hello</servlet-name>
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
</web-app>
```

레거시 프로젝트 유지보수용. 새 프로젝트는 어노테이션.

---

# Part C. Servlet 실습 — 페이지 이동 방식 2가지

## 7. forward (서버 내부 이동)

```java
@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        String id = req.getParameter("id");
        String pwd = req.getParameter("password");

        if (userService.authenticate(id, pwd)) {
            req.setAttribute("user", id);              // request scope 에 데이터
            req.getRequestDispatcher("/welcome.jsp")
               .forward(req, res);                    // 서버 내부 이동
        } else {
            req.getRequestDispatcher("/login.jsp").forward(req, res);
        }
    }
}
```

**forward 의 특징**:
- 서버 내부에서 다른 자원으로 제어 위임
- **URL 안 바뀜** (브라우저는 모름)
- **같은 request 객체** 유지 → `setAttribute` 데이터 공유
- HTTP 요청 1번

## 8. redirect (클라이언트 새 요청)

```java
@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // ... 로그인 처리
        res.sendRedirect("/welcome");      // 302 + Location 헤더
    }
}
```

**redirect 의 특징**:
- 응답 헤더 `Location: /welcome` + 상태 302 보냄
- 브라우저가 받아 **새 GET 요청** 발생
- **URL 바뀜**
- 새 request 객체 → 이전 데이터 안 넘어감
- HTTP 요청 2번

## 9. forward vs redirect — 선택 기준

```
   언제 forward?                       언제 redirect?
   ---------------                    ----------------
   • 같은 작업의 연속                   • POST 후 (PRG 패턴)
   • request 데이터 유지 필요           • URL 변경되어야
   • 검색·페이지네이션 결과 표시         • 다른 도메인 이동
   • 사용자가 새로고침 시 부담 없음      • F5 부담 줄임
```

**POST-Redirect-GET (PRG) 패턴**:
```
   ❌  POST /board (form 등록)
       ↓ forward 로 /board/list 응답
       사용자 F5 → form 재제출 → 중복 등록!

   ✅  POST /board (form 등록)
       ↓ 302 redirect → /board/list
       브라우저가 GET /board/list 새 요청
       사용자 F5 → GET 재시도라 안전
```

---

# Part D. FrontController 패턴

## 10. 매 페이지마다 서블릿 → 폭발

```
Servlet 시대의 문제

  요청 1  →  @WebServlet("/hello")    HelloServlet      → hello.jsp
  요청 2  →  @WebServlet("/list")     ListServlet       → list.jsp
  요청 3  →  @WebServlet("/detail")   DetailServlet     → detail.jsp
  요청 N  →  ... 서블릿 N개 ...

문제:
- 매 메서드에 인코딩 설정 (`req.setCharacterEncoding("UTF-8")`) 반복
- 로그인 검증 반복
- 공통 헤더 설정 반복
- 라우팅 로직이 분산 → 추적 어려움
```

## 11. FrontController 패턴

```
  요청들 -> [DispatcherServlet] --> HandlerMapping --> Controller --> JSP

   모든 요청을 하나의 진입점이 받고, 그 뒤에서 라우팅
```

```java
@WebServlet("/*")                       // 모든 요청
public class FrontController extends HttpServlet {

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // ① 인코딩 (한 곳에서)
        req.setCharacterEncoding("UTF-8");

        // ② URL 추출
        String path = req.getRequestURI().substring(req.getContextPath().length());

        // ③ Controller 결정
        Controller controller = HandlerMapping.get(path);

        // ④ Controller 실행
        String view = controller.handleRequest(req, res);

        // ⑤ View 로 forward
        req.getRequestDispatcher("/WEB-INF/views/" + view + ".jsp")
           .forward(req, res);
    }
}
```

**얻는 것**:
- 공통 부가 처리 (인코딩·로깅·인증) 한 곳에 통합
- 라우팅 로직 한 곳에 모음
- Controller 는 비즈니스 로직만

이게 바로 **Spring MVC 의 `DispatcherServlet`** 의 원형. Spring 은 이 패턴을 자동화 + 어노테이션화한 것.

---

## 12. 코드 깊게 — 미니 게시판

```java
// === HelloServlet 단순 예제 ===
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        req.setCharacterEncoding("UTF-8");
        res.setContentType("text/html;charset=UTF-8");

        String name = req.getParameter("name");
        if (name == null || name.isBlank()) name = "익명";

        try (PrintWriter out = res.getWriter()) {
            out.println("<!DOCTYPE html>");
            out.println("<html><head><title>Hello</title></head><body>");
            out.println("<h1>안녕하세요, " + name + "!</h1>");
            out.println("</body></html>");
        }
    }
}

// === FrontController 미니 예제 ===
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

        String path = req.getRequestURI().substring(
            req.getContextPath().length() + "/board".length());

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

// === Controller 인터페이스 ===
public interface Controller {
    String handle(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException;
}

@RequiredArgsConstructor
public class ListController implements Controller {
    @Override
    public String handle(HttpServletRequest req, HttpServletResponse res) {
        List<Board> boards = boardService.findAll();
        req.setAttribute("boards", boards);
        return "board/list";
    }
}
```

---

## 13. 실전 패턴 / 자주 빠지는 함정

### Servlet 기본
- ❌ Servlet 인스턴스 필드에 사용자 상태 저장 → **싱글톤** 이라 race condition ✅ 메서드 로컬 변수만
- ❌ `req.getParameter("name")` 결과를 한글 깨짐 ✅ `req.setCharacterEncoding("UTF-8")` 가장 먼저
- ❌ 응답 출력 후 redirect → 이미 committed 라 에러 ✅ redirect 는 출력 전

### 등록
- ❌ `@WebServlet` + `web.xml` 동시 매핑 → 충돌 ✅ 한 가지 선택
- ❌ `loadOnStartup` 안 줘서 첫 요청 지연 (init 무거울 때) ✅ `loadOnStartup = 1`

### forward vs redirect
- ❌ POST 후 forward 로 list view → F5 시 중복 등록 ✅ POST-Redirect-GET
- ❌ redirect 후 `setAttribute` 데이터 기대 → 새 request 라 없음 ✅ session 또는 query string
- ❌ forward 인데 URL 바뀔 거라 기대 ✅ URL 그대로 (forward 특성)

### 보안·인코딩
- ❌ 한글 응답이 깨짐 ✅ `setContentType("text/html;charset=UTF-8")`
- ❌ `getWriter` 와 `getOutputStream` 동시 사용 → IllegalStateException ✅ 둘 중 하나만
- ❌ HTML 출력 시 사용자 입력 그대로 → XSS ✅ HTML escape (`StringEscapeUtils.escapeHtml4`)

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| 한글 파라미터 깨짐 | encoding 설정 누락 | `req.setCharacterEncoding("UTF-8")` 첫 줄에 |
| `getParameter` 가 null | 파라미터 이름 오타 또는 form `name` 누락 | 정확히 매칭 |
| 한글 응답 깨짐 | Content-Type 누락 | `setContentType("text/html;charset=UTF-8")` |
| `IllegalStateException: getOutputStream() already called` | writer 와 outputstream 동시 사용 | 하나만 사용 |
| F5 시 중복 POST | POST 후 forward | POST-Redirect-GET |
| `404` — `/hello` 안 잡힘 | `@WebServlet` 누락 또는 URL 패턴 오타 | 정확히 매칭 |
| Tomcat 시작 시 init 안 호출 | `loadOnStartup` 없음 | 1+ 로 설정 |
| Servlet 의 static 필드가 멀티스레드에서 race condition | 싱글톤 + thread-unsafe | 로컬 변수 사용 |

---

## 14. 자가점검

1. WAS 와 Web Server 의 차이?
2. HTTP 가 "Stateless" 라는 게 무슨 의미?
3. Servlet 의 생명주기 4단계?
4. Servlet 은 왜 싱글톤이고, 그게 멀티스레드 환경에서 무엇을 의미하는가?
5. forward 와 redirect 의 차이 3가지?
6. POST-Redirect-GET 패턴이 풀어주는 문제는?
7. FrontController 패턴이 풀어주는 본질적 문제?

<details><summary>풀이</summary>

1. **Web Server**: 정적 파일 응답 (Apache, nginx). **WAS**: 자바 코드 실행해 동적 응답 생성 (Tomcat, Jetty). WAS 는 Web Server 기능도 포함하지만, 정적 파일은 Web Server 가 더 효율적이라 운영에선 둘을 나란히 두기도.
2. 서버가 클라이언트 상태를 기억하지 않음 — 각 요청은 독립적. 그래서 로그인 유지 등을 위해 쿠키·세션이 필요.
3. (1) Tomcat 이 객체 생성 (1번) → (2) `init()` (1번) → (3) `service()` → `doGet`/`doPost` (매 요청) → (4) `destroy()` (1번).
4. Tomcat 은 한 Servlet 클래스당 객체 1개만 생성 → 여러 요청이 같은 객체를 공유하면서 각자 스레드에서 실행. **인스턴스 필드는 thread-safe 하지 않음** → 사용자 데이터를 필드에 저장하면 race condition.
5. (a) **URL 변경**: forward 안 바뀜, redirect 바뀜. (b) **request 객체**: forward 같은 객체 유지 (`setAttribute` 공유), redirect 새 객체. (c) **HTTP 요청 수**: forward 1번, redirect 2번.
6. **F5 시 form 재제출** 문제. POST 후 forward 로 list view 응답하면 브라우저가 그 응답을 POST 결과로 기억 → F5 시 다시 form 제출 → 중복 등록. redirect 면 GET 요청이 새로 발생하므로 F5 안전.
7. **매 페이지마다 새 서블릿 + `web.xml` 매핑 + 공통 부가 처리 반복**. FrontController 가 모든 요청을 한 진입점에서 받아 인코딩·인증·로깅 등 공통 처리 통합 + 라우팅을 한 곳에서.

</details>

---

## 15. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.17 웹 프로그래밍 (정적/동적·WAS·HTTP) | §1, §2 (Part A) |
| p.18 ~ p.24 Servlet 개념·라이프사이클·작성·등록 | §3 ~ §6 (Part B) |
| p.25 ~ p.30 Servlet 실습·forward vs redirect | §7 ~ §9 (Part C) |
| p.31 ~ p.32 FrontController 패턴 | §10, §11 (Part D) |

_32p 슬라이드 모두 커버._
