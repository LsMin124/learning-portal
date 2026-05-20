# JSP 실습 — 치트시트

> 6p 실습 강의 · Servlet 게시판을 JSP 로 분리.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 5줄
1. **Servlet 의 `out.println("<html>...")` 를 JSP 로 분리** → 화면 출력 코드 가독성 회복
2. **데이터 흐름**: Servlet (`setAttribute`) → forward → JSP (`${attr}`)
3. **POST 후엔 redirect** (PRG 패턴, F5 안전)
4. **`/WEB-INF/views/` 안에 JSP 둠** → 외부 직접 접근 차단
5. **로그인 가드**는 Filter/Interceptor 로 (JSP 안의 스크립틀릿 X)

## 가장 중요한 코드 3개

```java
// (1) Servlet (Controller) - 데이터 준비
@WebServlet("/board")
public class BoardServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        req.setAttribute("boards", boardService.findAll());
        req.getRequestDispatcher("/WEB-INF/views/board/list.jsp")
           .forward(req, res);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        boardService.insert(new Board(req.getParameter("title")));
        res.sendRedirect("/board");          // PRG
    }
}
```

```jsp
<%-- (2) JSP (View) - 화면 출력만 --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>

<table>
  <c:forEach var="b" items="${boards}">
    <tr>
      <td>${b.id}</td>
      <td><a href="/boards/${b.id}">${b.title}</a></td>
    </tr>
  </c:forEach>
</table>
```

```jsp
<%-- (3) 로그인 가드 (인터셉터로 옮기는 게 좋음) --%>
<c:if test="${empty sessionScope.loginUser}">
  <c:redirect url="/login"/>
</c:if>
```

## 면접 한 줄 답변
- **Servlet 만으로 했을 때의 문제?** → `out.println("<html>...")` 같은 HTML 이 자바 문자열에 묻혀 가독성·디자이너 협업 X.
- **JSP 로 분리의 이점?** → HTML 가독성 회복 + 책임 분리 (C/V) + 변경 시 재컴파일 X + EL XSS 방어.
- **Spring MVC 로 가면 뭐가 바뀜?** → `@WebServlet` → `@GetMapping`, `req.setAttribute` → `Model.addAttribute`, `getRequestDispatcher` → return ViewName.
- **POST 후 forward 안 되는 이유?** → F5 시 같은 폼 다시 제출 → 중복 등록. PRG 로.

---

# 2. Quick Reference (실무 복붙)

## Servlet → JSP MVC 패턴

```
[Client]
  POST /board
  ↓
[Servlet doPost]                <- Controller
  - setCharacterEncoding
  - getParameter
  - Service 호출
  - sendRedirect (PRG)
  ↓
[Client] GET /board
  ↓
[Servlet doGet]                 <- Controller
  - Service 조회
  - setAttribute
  - forward
  ↓
[JSP list.jsp]                  <- View
  - ${boards}
  - <c:forEach>
```

## CRUD Servlet 골격

```java
@WebServlet("/board")
public class BoardServlet extends HttpServlet {

    private final BoardService service = new BoardService();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        String action = req.getParameter("action");
        if ("detail".equals(action)) {
            long id = Long.parseLong(req.getParameter("id"));
            req.setAttribute("board", service.findById(id));
            req.getRequestDispatcher("/WEB-INF/views/board/detail.jsp").forward(req, res);
        } else {
            req.setAttribute("boards", service.findAll());
            req.getRequestDispatcher("/WEB-INF/views/board/list.jsp").forward(req, res);
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        Board b = new Board();
        b.setTitle(req.getParameter("title"));
        b.setContent(req.getParameter("content"));
        service.insert(b);
        res.sendRedirect("/board");
    }
}
```

## JSP 목록 화면

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>

<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>게시판</title></head>
<body>
<h1>게시판</h1>

<c:if test="${not empty sessionScope.loginUser}">
  환영 ${sessionScope.loginUser.nickname}
  <a href="/logout">로그아웃</a>
</c:if>

<table border="1">
  <tr><th>번호</th><th>제목</th><th>작성일</th></tr>
  <c:forEach var="b" items="${boards}">
    <tr>
      <td>${b.id}</td>
      <td><a href="/board?action=detail&id=${b.id}"><c:out value="${b.title}"/></a></td>
      <td><fmt:formatDate value="${b.createdAt}" pattern="yyyy-MM-dd"/></td>
    </tr>
  </c:forEach>
</table>

<a href="/board?action=write">글쓰기</a>
</body>
</html>
```

## JSP 폼 (글쓰기)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<form method="post" action="/board">
  <input type="hidden" name="action" value="insert"/>

  <label>제목 <input type="text" name="title" required maxlength="200"/></label>
  <label>본문 <textarea name="content" required></textarea></label>

  <button type="submit">저장</button>
  <a href="/board">취소</a>
</form>
```

## 인코딩 3 단계 (한글)

```java
// 1. Servlet 요청 (getParameter 전)
req.setCharacterEncoding("UTF-8");

// 2. Servlet 응답
res.setContentType("text/html;charset=UTF-8");

// 3. JSP page directive
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
```

Filter 로 일괄:
```java
@WebFilter("/*")
public class EncodingFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {
        req.setCharacterEncoding("UTF-8");
        chain.doFilter(req, res);
    }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `${board}` 그대로 출력 | Servlet `setAttribute` 누락 또는 EL 비활성 |
| `<c:forEach>` 그대로 출력 | JSTL 의존성 + taglib 선언 |
| POST → forward + F5 → 중복 등록 | redirect (PRG) |
| 직접 `/WEB-INF/views/list.jsp` 호출 시도 | Servlet 거쳐야 함 (보안) |
| 한글 깨짐 | setCharacterEncoding 위치 (getParameter 전) |
| `<c:out>` 안 쓰고 `${userInput}` 직접 | XSS - `c:out` 으로 escape |
| 스크립틀릿 `<% if ... %>` | `<c:if>` |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
JSP 실습 (6p)
│
├── [A] MVC 분리
│   ├── Servlet (Controller) - 데이터 준비 + forward
│   ├── JSP (View) - 화면 출력
│   └── Model (DTO/Entity)
│
├── [B] 게시판 CRUD
│   ├── 목록 (doGet -> list.jsp)
│   ├── 상세 (doGet?action=detail)
│   ├── 작성 (doGet?action=write -> form.jsp, doPost)
│   ├── 수정 (doPost)
│   └── 삭제 (doPost)
│
├── [C] 데이터 흐름
│   ├── Servlet: setAttribute
│   ├── forward (URL 유지)
│   └── JSP: ${attr}
│
├── [D] 폼 처리
│   ├── POST + setCharacterEncoding
│   ├── getParameter
│   └── PRG (sendRedirect)
│
└── [E] 보안
    ├── WEB-INF/views/ 안에 JSP
    ├── c:out XSS escape
    └── 로그인 가드 (Filter)
```

## 학습 진도 체크리스트

- [ ] Servlet 의 `out.println` 코드를 JSP 로 분리
- [ ] `req.setAttribute` → `${attr}` 데이터 전달
- [ ] forward vs redirect 선택 (조회=forward, 변경=redirect)
- [ ] PRG 패턴 (POST → Redirect → GET)
- [ ] `/WEB-INF/views/` 보안 정책
- [ ] 한글 처리 3 단계
- [ ] EL + JSTL 로 스크립틀릿 제거
- [ ] `c:out` XSS escape
- [ ] Spring MVC 로 옮기면 무엇이 바뀌는지

## 연관 강의

```
1강 Servlet        -> HTTP 요청 처리
2강 JSP            -> 화면 출력 분리
2강 JSP 실습       <- 현재 위치 (게시판 통합)
3강 Cookie/Session -> 로그인 상태
4강 EL/JSTL        -> View 더 깔끔하게
5강 Filter         -> 인코딩·인증 공통 처리
Framework 5강 MVC1 -> Spring 으로 추상화
```

→ 다음 (Cookie/Session) 에서 **로그인 상태 유지**.
