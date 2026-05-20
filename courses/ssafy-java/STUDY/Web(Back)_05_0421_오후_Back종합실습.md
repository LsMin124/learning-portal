# Web Back 종합실습 - 1~5강 통합 미니 게시판

> **이 강의는 무엇인가**: 6페이지 짜리 실습 가이드. Web Back 트랙(Servlet → JSP → Cookie/Session → EL/JSTL → Filter) 1~5강에서 배운 모든 것을 **하나의 미니 게시판** 으로 통합 구현.
> **왜 배우는가**: 각 강의 개념을 따로 익혔지만 실무는 모두 결합해서 동작. 한 프로젝트로 묶어보면서 "왜 이런 분리가 필요한지" 체감.

---

## 들어가기 전에

- **선수**: Servlet/JSP/Cookie&Session/EL·JSTL/Filter 5강 전체.
- **마인드셋**: "각 컴포넌트의 책임이 어디서 끝나고 어디서 시작하는지" 의 경계 의식.

---

## 1. 실습 목표 - 게시판 1개에 들어가는 5가지 요소

| 강의 | 실습 요소 |
|--|--|
| Servlet (1강) | CRUD 진입점 - `BoardListServlet`, `BoardDetailServlet`, `BoardWriteServlet` |
| JSP (2강) | view - `list.jsp`, `detail.jsp`, `form.jsp` (Controller / View 분리) |
| Cookie/Session (3강) | 로그인 세션 + 자동 로그인 쿠키 |
| EL/JSTL (4강) | `<c:forEach>` 반복, `${board.title}` 출력, `fn:escapeXml` XSS 방어 |
| Filter (5강) | EncodingFilter (UTF-8), AuthFilter (로그인 검증), 404·500 에러 페이지 |

---

## 2. 프로젝트 구조

```
src/main/
├── java/com/example/
│   ├── filter/
│   │   ├── EncodingFilter.java         (5강)
│   │   ├── AuthFilter.java             (5강 + 3강)
│   │   └── LoggingFilter.java          (5강)
│   ├── listener/
│   │   └── AppLifecycleListener.java   (5강 - DB 풀)
│   ├── servlet/
│   │   ├── BoardListServlet.java       (1강)
│   │   ├── BoardDetailServlet.java
│   │   ├── BoardFormServlet.java
│   │   ├── BoardWriteServlet.java
│   │   ├── BoardDeleteServlet.java
│   │   ├── LoginServlet.java           (1강 + 3강)
│   │   └── LogoutServlet.java
│   ├── service/
│   │   ├── BoardService.java
│   │   └── UserService.java
│   ├── dao/
│   │   ├── BoardDao.java
│   │   └── UserDao.java
│   ├── dto/
│   │   ├── Board.java
│   │   └── User.java
│   └── exception/
│       └── NotFoundException.java      (5강)
└── webapp/
    ├── WEB-INF/
    │   ├── web.xml                     (5강 - error-page)
    │   └── views/                      (2강 - JSP 보호)
    │       ├── board/
    │       │   ├── list.jsp            (2강 + 4강 - EL/JSTL)
    │       │   ├── detail.jsp
    │       │   └── form.jsp
    │       ├── login.jsp
    │       └── error/
    │           ├── 404.jsp
    │           └── 500.jsp
    ├── css/style.css
    └── js/main.js
```

---

## 3. 통합 흐름 - 로그인 → 게시판 작성

```
[브라우저]
   | ① GET /login
   ▼
[Servlet 컨테이너]
   |
   ▼ EncodingFilter (UTF-8)
   ▼ LoggingFilter (시간 측정 시작)
   ▼ AuthFilter (login 페이지는 통과)
   |
   ▼ LoginServlet.doGet()
   |   → forward /WEB-INF/views/login.jsp
   |
   ▼ login.jsp (EL/JSTL)
   |
[브라우저]
   | ② POST /login (id, pwd, remember)
   ▼
   ▼ EncodingFilter
   ▼ LoggingFilter
   ▼ AuthFilter (login 통과)
   |
   ▼ LoginServlet.doPost()
   |   → userService.authenticate()
   |   → session.setAttribute("loginUser", user)
   |   → (remember 시) Cookie REMEMBER_TOKEN
   |   → sendRedirect("/board")
   |
[브라우저]
   | ③ GET /board (자동, redirect 결과)
   ▼
   ▼ EncodingFilter
   ▼ LoggingFilter
   ▼ AuthFilter (loginUser 있음 → 통과)
   |
   ▼ BoardListServlet.doGet()
   |   → boardService.findAll()
   |   → req.setAttribute("boards", ...)
   |   → forward /WEB-INF/views/board/list.jsp
   |
   ▼ list.jsp (EL/JSTL + Cookie 표시)
   |
[브라우저]
```

---

## 4. 실습 핵심 코드

```java
// === EncodingFilter ===
@WebFilter("/*")
public class EncodingFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        req.setCharacterEncoding("UTF-8");
        res.setCharacterEncoding("UTF-8");
        chain.doFilter(req, res);
    }
}

// === AuthFilter ===
@WebFilter("/*")
public class AuthFilter implements Filter {
    private static final Set<String> PUBLIC = Set.of("/login", "/signup", "/css", "/js");

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        String path = req.getRequestURI().substring(req.getContextPath().length());
        if (PUBLIC.stream().anyMatch(path::startsWith)) {
            chain.doFilter(request, response);
            return;
        }

        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("loginUser") == null) {
            res.sendRedirect(req.getContextPath() + "/login");
            return;
        }
        chain.doFilter(request, response);
    }
}

// === BoardListServlet ===
@WebServlet("/board")
public class BoardListServlet extends HttpServlet {
    private BoardService service;

    @Override
    public void init() {
        service = (BoardService) getServletContext().getAttribute("boardService");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {
        List<Board> boards = service.findAll();
        req.setAttribute("boards", boards);
        req.getRequestDispatcher("/WEB-INF/views/board/list.jsp").forward(req, res);
    }
}

// === BoardWriteServlet (POST-Redirect-GET) ===
@WebServlet("/board/write")
public class BoardWriteServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {
        Board b = new Board();
        b.setTitle(req.getParameter("title"));
        b.setContent(req.getParameter("content"));
        User loginUser = (User) req.getSession().getAttribute("loginUser");
        b.setWriter(loginUser.getId());

        boardService.insert(b);
        res.sendRedirect(req.getContextPath() + "/board");   // PRG
    }
}
```

```jsp
<%-- /WEB-INF/views/board/list.jsp --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<%@ taglib prefix="fn"  uri="jakarta.tags.functions" %>

<!DOCTYPE html>
<html>
<head><title>게시판</title></head>
<body>
    <h1>안녕하세요, ${sessionScope.loginUser.name}님!</h1>
    <a href="<c:url value='/logout' />">로그아웃</a>

    <h2>게시판 (${fn:length(boards)}건)</h2>

    <c:choose>
        <c:when test="${empty boards}">
            <p>게시글이 없습니다.</p>
        </c:when>
        <c:otherwise>
            <table>
                <c:forEach var="b" items="${boards}" varStatus="s">
                    <tr>
                        <td>${s.count}</td>
                        <td>
                            <a href="<c:url value='/board/${b.id}' />">
                                ${fn:escapeXml(b.title)}
                            </a>
                        </td>
                        <td>${b.writer}</td>
                        <td>
                            <fmt:formatDate value="${b.regDate}" pattern="yyyy-MM-dd" />
                        </td>
                    </tr>
                </c:forEach>
            </table>
        </c:otherwise>
    </c:choose>

    <a href="<c:url value='/board/write' />">새 글</a>
</body>
</html>
```

```xml
<!-- web.xml -->
<web-app>
    <error-page>
        <error-code>404</error-code>
        <location>/error/404.jsp</location>
    </error-page>
    <error-page>
        <error-code>500</error-code>
        <location>/error/500.jsp</location>
    </error-page>
    <error-page>
        <exception-type>java.lang.Exception</exception-type>
        <location>/error/general.jsp</location>
    </error-page>
</web-app>
```

---

## 5. 실습 체크리스트

- ☑ 1강 - Servlet 으로 모든 CRUD 진입점 작성
- ☑ 2강 - JSP 가 `WEB-INF/views/` 안에 있고 forward 통해서만 접근
- ☑ 2강 - Servlet 은 Controller, JSP 는 View 만 (분리)
- ☑ 3강 - 로그인 세션 (`session.setAttribute("loginUser", ...)`)
- ☑ 3강 - 자동 로그인 쿠키 (`REMEMBER_TOKEN`, `Max-Age=30 days`)
- ☑ 3강 - 로그아웃 시 `session.invalidate()` + 쿠키 삭제
- ☑ 4강 - JSP 안에 `<% %>` 0줄. EL + JSTL 만.
- ☑ 4강 - 사용자 입력 출력 시 `${fn:escapeXml(...)}` (XSS 방어)
- ☑ 5강 - EncodingFilter 로 모든 요청 UTF-8
- ☑ 5강 - AuthFilter 로 보호 경로 진입 제어
- ☑ 5강 - 404/500 에러 페이지 매핑
- ☑ POST 후 redirect (POST-Redirect-GET)

---

## 6. 실전 패턴 / 빠지는 함정

- ❌ JSP 안에서 직접 DB 호출 ✅ Servlet → Service → DAO 분리
- ❌ form action 에 `/board/write` 하드코딩 ✅ `<c:url value='/board/write' />` (contextPath 자동)
- ❌ POST 후 list view 직접 forward → F5 중복 등록 ✅ `sendRedirect()` (PRG)
- ❌ 사용자 입력 출력에 `${input}` 그대로 → XSS ✅ `${fn:escapeXml(input)}`
- ❌ 로그아웃 시 세션만 invalidate, 쿠키 안 지움 ✅ 둘 다 정리
- ❌ Filter 안에서 `chain.doFilter` 호출 안 하고 응답도 안 보냄 ✅ 둘 중 하나는 반드시
- ❌ JSP 를 webroot 루트에 둠 → 직접 URL 접근 가능 ✅ `WEB-INF/views/`

---

## 7. 자가점검

1. 한 게시판 프로젝트에 5강의 요소가 어떻게 결합되나? 각 1줄 요약.
2. AuthFilter 에서 `/login` 페이지 자신을 어떻게 통과시키나?
3. JSP 를 `WEB-INF/views/` 에 두는 이유?
4. 로그인 후 게시판으로 갈 때 `forward` 보다 `redirect` 가 왜 더 안전?
5. EL/JSTL 만으로 JSP 안 자바 코드를 완전히 제거할 수 있나?

<details><summary>풀이</summary>

1. (1) **Servlet**: Controller (CRUD 진입). (2) **JSP**: View (HTML 렌더). (3) **Cookie/Session**: 로그인 상태 유지. (4) **EL/JSTL**: 자바 코드 없는 view 출력. (5) **Filter**: 인코딩·인증·로깅·에러 페이지 공통 처리.
2. **whitelist 패턴**: `Set<String> PUBLIC = Set.of("/login", "/signup", "/css", "/js")` + URL 이 startsWith 면 통과. 또는 `@WebFilter` 의 url-pattern 을 보호 경로만으로 제한.
3. **외부 직접 접근 차단** - 사용자가 `https://example.com/list.jsp` 로 직접 요청해도 404. Controller 통해서만 접근 가능 → 데이터 흐름·인증 우회 방지.
4. **F5 시 form 재제출** 방지 (POST-Redirect-GET). forward 면 사용자가 새로고침 시 다시 form 데이터 전송 → 중복 등록. redirect 는 GET 요청을 새로 만들므로 F5 안전.
5. **거의 가능**. 단, 특수한 자바 호출 (정적 메서드 등) 은 어렵지만, 일반적인 데이터 출력·반복·조건은 모두 EL/JSTL 로 가능. EL 3.0+ 부턴 메서드 호출도 가능해 더 강력.

</details>

---

## 8. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 온라인 실습실 풀이 (게시판 통합) | §1 ~ §6 (실습 전체) |
| p.6 마무리 | (생략) |

_6p 슬라이드의 실습 가이드를 구체 풀스택 예제로 확장._
