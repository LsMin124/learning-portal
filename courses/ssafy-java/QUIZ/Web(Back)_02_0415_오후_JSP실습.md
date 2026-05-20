# JSP 실습 - 퀴즈

> 14문항. 개념·적용·디버그·면접. JSP 변환·내장 객체·액션 태그·EL/JSTL.

---

### Q1. (적용) Servlet 의 `out.println("<h1>" + name + "</h1>")` 를 JSP 로 변환하시오.

<details><summary>정답</summary>

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<h1>${name}</h1>
```

또는 스크립틀릿:
```jsp
<h1><%= name %></h1>
```

EL 이 권장. 자동 XSS 회피 + 가독성 우월 + getter 자동 호출.

</details>

### Q2. (개념) Servlet → JSP 변환 시 책임 분리는 어떻게 되나?

<details><summary>정답</summary>

- **Servlet (Controller)**: HTTP 요청 받기 → Service 호출 → 데이터 준비 (`req.setAttribute`) → JSP 로 forward
- **JSP (View)**: 화면 출력만 (`${...}` EL + JSTL 반복·조건)

이 분리가 디자이너·개발자 협업의 기본.

**MVC 의 의미**:
- Model = JavaBean (Board, User)
- View = JSP (HTML + EL/JSTL)
- Controller = Servlet (또는 Spring `@Controller`)

</details>

### Q3. (개념) JSP 의 9가지 내장 객체 (Implicit Objects) 정리.

<details><summary>정답</summary>

JSP 가 자동으로 만들어주는 변수 9개:

| 내장 객체 | 자바 타입 | 역할 |
|--|--|--|
| `request` | HttpServletRequest | 요청 정보, 파라미터, attribute |
| `response` | HttpServletResponse | 응답 헤더·상태 코드 설정 |
| `session` | HttpSession | 세션 데이터 |
| `application` | ServletContext | 앱 전체 공유 데이터 |
| `out` | JspWriter | 출력 스트림 (`out.println` 등) |
| `pageContext` | PageContext | 모든 scope 통합 접근 |
| `page` | Object (this) | JSP 페이지 자체 |
| `config` | ServletConfig | JSP 설정 |
| `exception` | Throwable | 에러 페이지 (`isErrorPage="true"` 일 때만) |

**사용 예 (스크립틀릿)**:
```jsp
<%
    String user = (String) session.getAttribute("loginUser");
    if (user != null) {
        out.println("환영 " + user);
    }
%>
```

→ 현대 JSP 는 스크립틀릿 대신 **EL + JSTL** 사용. 그래도 9 객체의 존재는 알아둬야 디버깅 가능.

</details>

### Q4. (개념) JSP 의 컴파일 과정 - .jsp 가 어떻게 실행되나?

<details><summary>정답</summary>

```
list.jsp
   ↓ (Tomcat 의 Jasper 컴파일러)
list_jsp.java       (Servlet 코드 자동 생성)
   ↓ (javac)
list_jsp.class      (서블릿 클래스)
   ↓ (요청 들어오면)
HttpServlet.service() 실행
```

**핵심**: **JSP 는 결국 Servlet**. Tomcat 이 첫 요청 시 자동 변환.

**확인 방법** (개발 시):
```
$TOMCAT_HOME/work/Catalina/localhost/myapp/org/apache/jsp/
└── list_jsp.java     (자동 생성된 자바 파일)
```

**변환 시점**:
- 첫 요청 시: 변환 + 컴파일 + 실행 (느림)
- 두 번째부터: 캐시된 .class 실행 (빠름)
- .jsp 수정 → 자동 재변환·재컴파일

**EL 표현식 변환**:
- `${board.title}` → `${pageContext.findAttribute("board").getTitle()}` 형태로 변환
- JSTL → 해당 자바 메서드 호출

**개발자 도구**: IntelliJ 의 "View JSP source" 로 생성된 자바 코드 확인 가능 → 동작 이해에 좋음.

</details>

### Q5. (개념) 액션 태그 - `<jsp:include>`, `<jsp:forward>`, `<jsp:useBean>` 의 역할?

<details><summary>정답</summary>

**`<jsp:include>` - 동적 include**:
```jsp
<jsp:include page="header.jsp" />
<jsp:include page="content.jsp">
    <jsp:param name="title" value="목록" />
</jsp:include>
<jsp:include page="footer.jsp" />
```
- **런타임에** 다른 JSP 결과를 포함
- 호출된 JSP 가 실행되어 그 결과만 가져옴

**`<%@ include %>` - 정적 include (디렉티브)**:
```jsp
<%@ include file="header.jsp" %>
```
- **컴파일 타임에** 소스 코드 자체를 합침
- 변수 공유 가능, 빠름

| | `<jsp:include>` | `<%@ include %>` |
|--|--|--|
| 시점 | 런타임 | 컴파일 타임 |
| 변수 공유 | X (독립 실행) | O |
| 자주 바뀜 | 적합 | 부적합 (재컴파일 필요) |
| 성능 | 약간 느림 | 빠름 |

**`<jsp:forward>` - 요청 전달**:
```jsp
<jsp:forward page="login.jsp" />
<!-- request.getRequestDispatcher("login.jsp").forward(...) 와 동일 -->
```

**`<jsp:useBean>` - JavaBean 인스턴스화 (옛 스타일)**:
```jsp
<jsp:useBean id="board" class="com.example.Board" scope="request"/>
<jsp:setProperty name="board" property="*"/>     <!-- 폼 파라미터 자동 매핑 -->
```
- 현대는 Spring `@ModelAttribute` 가 대체
- 레거시 JSP 에서만 보임

→ 실무: `<jsp:include>` 와 `<%@ include %>` 만 알아도 충분.

</details>

### Q6. (적용) Servlet 에서 List 를 JSP 로 넘기는 코드.

<details><summary>정답</summary>

```java
@WebServlet("/boards")
public class BoardListServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        List<Board> boards = boardService.findAll();
        req.setAttribute("boards", boards);
        req.getRequestDispatcher("/WEB-INF/views/board/list.jsp")
           .forward(req, res);
    }
}
```

JSP 에서:
```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>

<table>
    <c:forEach var="b" items="${boards}">
        <tr>
            <td>${b.id}</td>
            <td><a href="/boards/${b.id}">${b.title}</a></td>
            <td>${b.writer}</td>
            <td>${b.createdAt}</td>
        </tr>
    </c:forEach>
</table>
```

**핵심**:
- Servlet: `setAttribute` 로 데이터 전달 → forward
- JSP: `${boards}` 로 받아서 `<c:forEach>` 반복
- 단방향 - Servlet 이 데이터 준비, JSP 는 표시만

</details>

### Q7. (개념) JSP 파일을 `/WEB-INF/views/` 안에 두는 보안 이유?

<details><summary>정답</summary>

`WEB-INF/` 아래 자원은 **외부에서 직접 URL 로 접근 불가** (Tomcat 의 기본 보안 정책).

사용자가 `https://example.com/list.jsp` 로 직접 요청하면:
- `webapp/list.jsp` (루트) → 접근 가능 → Controller 우회 + 인증 검증 우회
- `webapp/WEB-INF/views/list.jsp` → 404 → Controller 통해서만 접근 가능

**구조**:
```
webapp/
├── static/             (외부 접근 가능 - CSS, JS, 이미지)
│   └── style.css
└── WEB-INF/
    ├── web.xml         (외부 접근 불가)
    ├── lib/
    └── views/
        ├── board/
        │   ├── list.jsp
        │   └── detail.jsp
        └── login.jsp
```

**왜 중요?**:
- 인증 안 한 사용자가 `/views/admin.jsp` 직접 호출 → 권한 검증 우회 가능성
- Service/DAO 호출 안 거치고 JSP 만 렌더 → 빈 데이터로 깨진 화면 또는 정보 누출

→ Spring Boot 도 `src/main/webapp/WEB-INF/views/` 또는 `templates/` 에 둠.

</details>

### Q8. (적용) 등록 처리 후 redirect 로 보내는 Servlet (POST-Redirect-GET 패턴).

<details><summary>정답</summary>

```java
@WebServlet("/board")
public class BoardServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {
        // 목록 표시
        req.setAttribute("boards", boardService.findAll());
        req.getRequestDispatcher("/WEB-INF/views/board/list.jsp")
           .forward(req, res);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {
        req.setCharacterEncoding("UTF-8");      // 한글 처리

        Board b = new Board();
        b.setTitle(req.getParameter("title"));
        b.setContent(req.getParameter("content"));
        boardService.insert(b);

        res.sendRedirect("/board");             // 등록 후 GET 으로 리다이렉트
    }
}
```

**POST-Redirect-GET 패턴**:
- POST 응답을 직접 보내면 → 사용자가 F5 누르면 같은 폼 다시 제출 (중복 등록)
- 302 redirect → 브라우저가 GET 으로 다시 요청 → F5 안전

```
[브라우저]                    [서버]
   |  POST /board              |
   |--------------------->     |
   |                           | INSERT
   |  302 Redirect /board      |
   |<---------------------    |
   |                           |
   |  GET /board               |
   |--------------------->     |
   |                           | SELECT
   |  200 OK + 목록 HTML       |
   |<---------------------    |
```

→ 모든 form 제출 후엔 redirect. forward 는 GET 결과 표시용에만.

</details>

### Q9. (개념) 한글 입력 처리 - request 와 response 의 인코딩 설정.

<details><summary>정답</summary>

**문제**: 폼에서 한글 입력 시 `???` 또는 깨진 글자 출력.

**해결 - 3 단계**:

**1. JSP 페이지 인코딩** (한글 HTML 응답):
```jsp
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
```

**2. Servlet 의 요청 디코딩** (한글 파라미터 받기):
```java
@Override
protected void doPost(HttpServletRequest req, HttpServletResponse res)
        throws IOException, ServletException {
    req.setCharacterEncoding("UTF-8");      // 핵심 - getParameter 전에
    String title = req.getParameter("title");
    // ...
}
```

⚠️ `setCharacterEncoding` 은 **`getParameter` 호출 전에** 실행해야 효과.

**3. Servlet 의 응답 인코딩**:
```java
res.setContentType("text/html;charset=UTF-8");
```

**Filter 로 일괄 처리 (권장)**:
```java
@WebFilter("/*")
public class EncodingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        req.setCharacterEncoding("UTF-8");
        res.setCharacterEncoding("UTF-8");
        chain.doFilter(req, res);
    }
}
```
→ 매 Servlet 마다 반복 안 함.

**Tomcat 8 부터** GET 요청은 기본 UTF-8 (server.xml 의 URIEncoding) 이라 POST 만 신경.

</details>

### Q10. (개념) EL 의 4가지 스코프와 우선순위.

<details><summary>정답</summary>

EL `${name}` 은 4 가지 scope 를 **순서대로** 검색:

| Scope | 명시 접근 | 범위 |
|--|--|--|
| **page** | `${pageScope.name}` | 현재 JSP 페이지만 |
| **request** | `${requestScope.name}` | 같은 요청 (forward 까지) |
| **session** | `${sessionScope.name}` | 사용자별 세션 |
| **application** | `${applicationScope.name}` | 앱 전체 (모든 사용자) |

**검색 순서**: page → request → session → application (좁은 곳부터)

**예**:
```java
// Servlet
req.setAttribute("user", userA);            // request scope
session.setAttribute("user", userB);        // session scope

// JSP
${user}            // userA (request 가 먼저 발견)
${requestScope.user}    // userA
${sessionScope.user}    // userB
```

**파라미터 접근**:
- `${param.id}` - 단일 파라미터 (URL `?id=42`)
- `${paramValues.tags}` - 다중값 파라미터 (`?tags=a&tags=b`)
- `${header['User-Agent']}` - HTTP 헤더
- `${cookie.JSESSIONID.value}` - 쿠키

**왜 `pageScope.user` 대신 `${user}`?**:
- 짧게 쓸 수 있음
- 같은 이름이면 좁은 scope 우선
- 모호하면 명시 (`${requestScope.user}`)

→ "왜 이 값이 안 나오지?" 디버깅 시 명시적 scope 접근이 좋음.

</details>

### Q11. (디버그) JSP 에서 `${board.title}` 이 그대로 출력됨 (값 안 풀림). 원인?

<details><summary>정답</summary>

**1. EL 비활성** - 옛 JSP 또는 페이지 설정 누락:
```jsp
<%@ page isELIgnored="false" %>
```
또는 web.xml 에서 `<el-ignored>true</el-ignored>` 가 설정됨.

**2. `board` 가 어떤 scope 에도 없음** - Servlet 에서 `setAttribute("board", b)` 호출 누락:
```java
// Servlet 에서
Board b = boardService.findById(id);
req.setAttribute("board", b);     // 이거 누락하면 ${board} = null
req.getRequestDispatcher("/WEB-INF/views/detail.jsp").forward(req, res);
```

**3. `Board` 클래스에 getter 없음** - EL 은 `getTitle()` 호출하는데 없으면 빈 값:
```java
public class Board {
    private String title;
    public String getTitle() { return title; }   // 필수
    // 또는 record (자동 getter 와는 다름 - record 는 title() 메서드, EL 은 자동 인식)
}
```

**4. 직접 URL 로 JSP 호출** - Servlet 거치지 않으면 attribute 가 없음:
```
잘못된: http://localhost/board/detail.jsp        (직접)
올바른: http://localhost/board?id=42             (Servlet 거침)
```
→ Q7 의 WEB-INF 정책이 이걸 막아줌.

**디버깅 순서**:
1. EL 비활성 의심 → `${1+1}` 출력 → 2 안 나오면 EL 자체 문제
2. 다른 변수도 안 나오면 → scope 문제 (Servlet 검증)
3. 다른 건 되는데 `${board.title}` 만 안 되면 → getter 또는 NPE

</details>

### Q12. (디버그) `<c:forEach>` 가 그대로 출력됨. 원인?

<details><summary>정답</summary>

JSTL 태그 라이브러리 import 누락 + 의존성 누락.

**해결 1: JSP 첫 줄에 taglib 선언**:
```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>     <!-- 핵심 -->
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>    <!-- 포맷팅 -->

<c:forEach var="b" items="${boards}">
    ${b.title}
</c:forEach>
```

**해결 2: 의존성 추가** (Spring Boot `pom.xml`):
```xml
<dependency>
    <groupId>jakarta.servlet.jsp.jstl</groupId>
    <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
</dependency>
<dependency>
    <groupId>org.glassfish.web</groupId>
    <artifactId>jakarta.servlet.jsp.jstl</artifactId>
</dependency>
```

**URI 주의** (Jakarta EE 9 부터):
- 옛: `http://java.sun.com/jsp/jstl/core`
- 새: `jakarta.tags.core`

**자주 쓰는 JSTL 태그**:
```jsp
<c:if test="${board != null}">...</c:if>

<c:choose>
    <c:when test="${user.role == 'ADMIN'}">관리자</c:when>
    <c:otherwise>일반</c:otherwise>
</c:choose>

<c:forEach var="b" items="${boards}" varStatus="status">
    ${status.index} : ${b.title}     <!-- 인덱스 접근 -->
</c:forEach>

<c:url var="link" value="/boards/${b.id}"/>     <!-- URL 만들기 -->
<a href="${link}">상세</a>

<c:out value="${userInput}"/>     <!-- XSS 자동 escape -->
```

</details>

### Q13. (적용) JSP 에서 로그인 안 한 사용자를 `/login` 으로 보내는 가드.

<details><summary>정답</summary>

**스크립틀릿 방식**:
```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%
    if (session.getAttribute("loginUser") == null) {
        response.sendRedirect("/login");
        return;     // 명시적 return - 안 하면 JSP 가 계속 실행됨
    }
%>
<h1>마이페이지</h1>
```

**JSTL 방식 (권장)**:
```jsp
<%@ taglib prefix="c" uri="jakarta.tags.core" %>

<c:if test="${empty sessionScope.loginUser}">
    <c:redirect url="/login"/>
</c:if>

<h1>마이페이지</h1>
<p>환영 ${sessionScope.loginUser.nickname}</p>
```

**실무는 인터셉터/필터 분리 권장**:
```java
@Component
public class AuthInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        if (req.getSession().getAttribute("loginUser") == null) {
            res.sendRedirect("/login");
            return false;
        }
        return true;
    }
}
```

**왜 인터셉터가 좋은가**:
- JSP 마다 코드 반복 X (DRY)
- 비즈니스 로직과 분리
- 로그인 페이지·정적 자원은 제외 가능 (excludePathPatterns)
- Spring Security 면 더 좋음 (`/admin/**` 등)

→ JSP 의 인증 가드는 학습용. 운영은 인터셉터/Security.

</details>

### Q14. (면접) "JSP 실습에서 만든 게시판 CRUD 를 Spring MVC 로 옮기면 무엇이 바뀌나요?"

<details><summary>정답</summary>

| 구분 | Servlet + JSP | Spring MVC + JSP |
|--|--|--|
| 라우팅 | `@WebServlet("/board")` 각각 | `@Controller` + `@GetMapping/@PostMapping` |
| 파라미터 | `req.getParameter("id")` | `@RequestParam`, `@PathVariable`, `@ModelAttribute` |
| 데이터 전달 | `req.setAttribute("board", b)` | `Model.addAttribute("board", b)` |
| Forward | `req.getRequestDispatcher(...).forward(req, res)` | `return "view-name"` (ViewResolver) |
| Redirect | `res.sendRedirect("/board")` | `return "redirect:/board"` |
| DI | new 직접 또는 `@WebServlet` | `@Autowired` + `@RequiredArgsConstructor` |
| 예외 처리 | try-catch 각 메서드 | `@ControllerAdvice` 전역 |
| 인코딩 | 매 Servlet 에 setEncoding | `CharacterEncodingFilter` 자동 |
| 인증 | 메서드 시작에 if 검증 | Interceptor 또는 Spring Security |

**예시 - 같은 기능**:

**Servlet + JSP**:
```java
@WebServlet("/board")
public class BoardServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        long id = Long.parseLong(req.getParameter("id"));
        Board b = boardService.findById(id);
        req.setAttribute("board", b);
        req.getRequestDispatcher("/WEB-INF/views/detail.jsp")
           .forward(req, res);
    }
}
```

**Spring MVC**:
```java
@Controller
@RequiredArgsConstructor
public class BoardController {
    private final BoardService service;

    @GetMapping("/board/{id}")
    public String detail(@PathVariable long id, Model model) {
        model.addAttribute("board", service.findById(id));
        return "board/detail";     // -> /WEB-INF/views/board/detail.jsp
    }
}
```

**본질은 같음** - Spring 이 보일러플레이트를 자동화 + DI/AOP/예외 처리 등 추가.

**왜 Spring MVC 로 가는가**:
1. 라우팅이 어노테이션 한 줄 (메서드별)
2. 파라미터 변환 자동 (`@PathVariable long id` → 자동 `Long.parseLong`)
3. ViewResolver 가 prefix/suffix 자동 (`board/detail` → `/WEB-INF/views/board/detail.jsp`)
4. DI 로 service·dao 주입 자동
5. 테스트 가능 (`@WebMvcTest`)
6. JSON API 와 통합 (`@RestController` 로 갈아끼움 쉬움)

**SSAFY 커리큘럼 의도**: JSP 실습으로 Servlet + JSP 의 기본을 익히고, 그 위에 Spring MVC 가 어떻게 추상화하는지 배움. 기초 없이 Spring 부터 시작하면 "마법" 으로 느껴짐.

</details>
