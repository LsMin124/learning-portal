# Back 종합실습 — 치트시트

> 6p 슬라이드 · Web Backend 1~5강 통합 게시판 (Servlet + JSP + Cookie/Session + EL/JSTL + Filter).
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **레이어**: Filter → Servlet → Service → DAO → DB (인메모리 BoardStore)
2. **공통 처리**: 인코딩 Filter + 인증 Filter
3. **PRG 패턴**: POST → Redirect → GET (F5 안전)
4. **본인 글만 수정/삭제**는 Service 에서 검증
5. **로그아웃**: `session.invalidate()` + 로그인 쿠키 삭제
6. **모든 사용자 출력은 `<c:out>`** (XSS 방어)

## 가장 중요한 코드 3개

```java
// (1) 프로젝트 구조
src/main/java/
├── filter/
│   ├── EncodingFilter      (@WebFilter("/*"))
│   └── AuthFilter           (@WebFilter("/mypage/*"))
├── listener/
│   └── AppListener          (@WebListener) - 초기화
├── servlet/
│   ├── BoardListServlet     (@WebServlet("/boards"))
│   ├── BoardWriteServlet    (@WebServlet("/boards/write"))
│   └── LoginServlet
├── service/
│   └── BoardService
└── dao/
    └── BoardStore           (인메모리, 추후 DB)
```

```java
// (2) BoardWriteServlet (PRG)
@WebServlet("/boards/write")
public class BoardWriteServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        req.getRequestDispatcher("/WEB-INF/views/board/form.jsp").forward(req, res);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        User user = (User) req.getSession().getAttribute("loginUser");

        Board b = new Board();
        b.setTitle(req.getParameter("title"));
        b.setContent(req.getParameter("content"));
        b.setWriterId(user.getId());                   // 서버에서 검증

        boardService.insert(b);
        res.sendRedirect("/boards");                   // PRG
    }
}
```

```jsp
<%-- (3) list.jsp - JSTL + EL --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>

<c:forEach var="b" items="${boards}">
  <article>
    <h3><a href="/boards/${b.id}"><c:out value="${b.title}"/></a></h3>
    <small>by ${b.writer} | <fmt:formatDate value="${b.createdAt}" pattern="yyyy-MM-dd"/></small>
  </article>
</c:forEach>
```

## 면접 한 줄 답변
- **종합실습의 5강 결합 학습 사례?** → URL 매핑(1) + View 분리(2) + 로그인(3) + 화면 EL/JSTL(4) + 공통 처리(5).
- **PRG 가 왜 필요?** → POST 후 forward 시 F5 누르면 중복 등록. redirect 로 GET 새 요청 → 안전.
- **인메모리 BoardStore 의 thread safety?** → `ConcurrentHashMap` 또는 `synchronized`. 추후 DB 로 가면 자동.
- **Spring MVC 이식 시 변경점?** → `@WebServlet` → `@Controller`, `req.setAttribute` → `Model`, Filter → Interceptor.

---

# 2. Quick Reference (실무 복붙)

## Filter 적용

```java
// 1. 인코딩 (모든 요청)
@WebFilter("/*")
public class EncodingFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        req.setCharacterEncoding("UTF-8");
        res.setCharacterEncoding("UTF-8");
        chain.doFilter(req, res);
    }
}

// 2. 인증 (보호 영역)
@WebFilter("/boards/write")
public class AuthFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpReq = (HttpServletRequest) req;
        HttpSession session = httpReq.getSession(false);

        if (session == null || session.getAttribute("loginUser") == null) {
            ((HttpServletResponse) res).sendRedirect("/login?returnUrl="
                + URLEncoder.encode(httpReq.getRequestURI(), "UTF-8"));
            return;
        }
        chain.doFilter(req, res);
    }
}
```

## 게시글 목록 (Servlet)

```java
@WebServlet("/boards")
public class BoardListServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        String keyword = req.getParameter("keyword");
        List<Board> boards = boardService.search(keyword);

        req.setAttribute("boards", boards);
        req.setAttribute("keyword", keyword);
        req.getRequestDispatcher("/WEB-INF/views/board/list.jsp").forward(req, res);
    }
}
```

## 게시글 작성 폼

```jsp
<%-- form.jsp --%>
<form method="post" action="/boards/write">
  <label>제목 <input type="text" name="title" required maxlength="200"/></label>
  <label>본문 <textarea name="content" required></textarea></label>
  <button type="submit">저장</button>
  <a href="/boards">취소</a>
</form>
```

## 게시글 상세 + 조회수 (쿠키)

```java
@WebServlet("/boards/detail")
public class BoardDetailServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        long id = Long.parseLong(req.getParameter("id"));

        // 쿠키로 중복 조회 방지
        String cookieName = "viewed_" + id;
        boolean alreadyViewed = false;
        Cookie[] cookies = req.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if (cookieName.equals(c.getName())) { alreadyViewed = true; break; }
            }
        }
        if (!alreadyViewed) {
            boardService.incrementView(id);
            Cookie c = new Cookie(cookieName, "1");
            c.setMaxAge(24 * 60 * 60);
            c.setPath("/");
            res.addCookie(c);
        }

        req.setAttribute("board", boardService.findById(id));
        req.getRequestDispatcher("/WEB-INF/views/board/detail.jsp").forward(req, res);
    }
}
```

## 로그인 / 로그아웃

```java
// 로그인
@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        String id = req.getParameter("id");
        String pw = req.getParameter("password");

        User user = userService.login(id, pw);
        if (user == null) {
            req.setAttribute("error", "ID/비밀번호 확인");
            req.getRequestDispatcher("/WEB-INF/views/login.jsp").forward(req, res);
            return;
        }

        req.changeSessionId();
        req.getSession().setAttribute("loginUser", user);

        String returnUrl = req.getParameter("returnUrl");
        if (returnUrl == null || !returnUrl.startsWith("/")) returnUrl = "/";
        res.sendRedirect(returnUrl);
    }
}

// 로그아웃
@WebServlet("/logout")
public class LogoutServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException {
        HttpSession session = req.getSession(false);
        if (session != null) session.invalidate();
        res.sendRedirect("/");
    }
}
```

## BoardStore (인메모리, thread-safe)

```java
public class BoardStore {
    private static final Map<Long, Board> store = new ConcurrentHashMap<>();
    private static final AtomicLong seq = new AtomicLong(0);

    public Board insert(Board b) {
        long id = seq.incrementAndGet();
        b.setId(id);
        b.setCreatedAt(LocalDateTime.now());
        store.put(id, b);
        return b;
    }

    public List<Board> findAll() {
        return store.values().stream()
            .sorted(Comparator.comparing(Board::getId).reversed())
            .collect(Collectors.toList());
    }

    public Board findById(long id) { return store.get(id); }
    public boolean delete(long id) { return store.remove(id) != null; }
}
```

## web.xml 에러 페이지

```xml
<error-page>
    <error-code>404</error-code>
    <location>/WEB-INF/views/error/404.jsp</location>
</error-page>
<error-page>
    <exception-type>java.lang.Exception</exception-type>
    <location>/WEB-INF/views/error/500.jsp</location>
</error-page>
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| POST 후 forward → F5 중복 등록 | redirect (PRG) |
| writerId 를 클라이언트 hidden input | 서버에서 session.user.id |
| 조회수 매 새로고침 증가 | 쿠키 24시간 |
| `${b.title}` 그대로 → XSS | `<c:out>` |
| returnUrl 외부 도메인 → Open Redirect | `startsWith("/")` 검증 |
| BoardStore HashMap | ConcurrentHashMap 또는 synchronized |
| 로그아웃 후 쿠키 남음 | rememberCookie MaxAge=0 |
| Spring MVC 이식 시 처음부터 | 본 실습의 레이어 분리 유지 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Back 종합실습 (6p, 5강 통합)
│
├── [1강 Servlet]
│   ├── @WebServlet URL 매핑
│   ├── doGet / doPost
│   └── forward / redirect
│
├── [2강 JSP]
│   ├── /WEB-INF/views/ 보안
│   ├── ${attr} 데이터 표시
│   └── 폼 (POST /boards/write)
│
├── [3강 Cookie / Session]
│   ├── 로그인 (changeSessionId)
│   ├── 조회수 쿠키 (MaxAge 24h)
│   └── 로그아웃 (invalidate)
│
├── [4강 EL / JSTL]
│   ├── <c:forEach> 반복
│   ├── <c:out> XSS escape
│   └── <fmt:formatDate>
│
├── [5강 Filter]
│   ├── EncodingFilter (/*)
│   ├── AuthFilter (/mypage/*)
│   └── 순서 (인코딩 → 인증)
│
└── [통합]
    ├── PRG 패턴
    ├── 본인 글 검증 (Service)
    ├── 인메모리 → DB (다음 강의)
    └── Spring MVC 이식 비교
```

## 학습 진도 체크리스트

### 1강 Servlet
- [ ] @WebServlet URL 패턴
- [ ] doGet / doPost 의미
- [ ] forward / redirect 선택

### 2강 JSP
- [ ] /WEB-INF/views/ 보안 정책
- [ ] req.setAttribute → ${attr}
- [ ] 폼 + PRG 패턴

### 3강 Cookie/Session
- [ ] 로그인 + changeSessionId
- [ ] 조회수 쿠키 (24h)
- [ ] 로그아웃 invalidate

### 4강 EL/JSTL
- [ ] c:forEach + varStatus
- [ ] c:out XSS escape
- [ ] fmt:formatDate

### 5강 Filter
- [ ] EncodingFilter
- [ ] AuthFilter + returnUrl
- [ ] Filter 순서

### 통합
- [ ] BoardStore thread-safety
- [ ] writerId 서버 검증
- [ ] 자주 빠지는 함정 7개

## 연관 강의

```
Web Back 1~5강     -> 개별 학습
6강 종합실습       <- 현재 위치 (통합)
DB 6강 관통 PJT    -> 인메모리 BoardStore -> DB 로 교체
Framework 5강 MVC1 -> Spring 으로 같은 게시판 재구현
```

→ 다음 (DB 강의) 에서 **BoardStore 를 MySQL 로 교체**.
