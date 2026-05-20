# Servlet — 치트시트

> 32p 슬라이드 · Java Web 의 가장 낮은 표준 API.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Servlet** = 자바로 HTTP 요청을 처리하는 표준 API (`javax.servlet` / `jakarta.servlet`)
2. **doGet** = 조회, **doPost** = 변경 (생성·수정·삭제)
3. **`@WebServlet("/path")`** 어노테이션 또는 `web.xml` 로 매핑
4. **요청 처리**: `HttpServletRequest` (파라미터·헤더·세션) → 비즈니스 → `HttpServletResponse` (상태·헤더·본문)
5. **forward vs redirect**: forward = 서버 내 이동 (URL 그대로), redirect = 브라우저 재요청 (URL 바뀜)
6. **Servlet 컨테이너 (Tomcat)** 이 매 요청마다 스레드 풀에서 처리 → 인스턴스 1개 공유, 필드 사용 금지

## 가장 중요한 코드 3개

```java
// (1) 기본 Servlet
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        res.setContentType("text/html;charset=UTF-8");
        res.getWriter().println("<h1>Hello " + req.getParameter("name") + "</h1>");
    }
}

// (2) POST → 처리 → redirect (PRG)
@WebServlet("/board")
public class BoardServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");           // 한글
        boardService.insert(new Board(req.getParameter("title")));
        res.sendRedirect("/board");                  // F5 안전
    }
}

// (3) JSP 로 forward (데이터 전달)
List<Board> boards = boardService.findAll();
req.setAttribute("boards", boards);
req.getRequestDispatcher("/WEB-INF/views/board/list.jsp")
   .forward(req, res);
```

## 면접 한 줄 답변
- **Servlet vs Spring MVC?** → Spring MVC 의 `DispatcherServlet` 도 결국 Servlet. Spring 이 라우팅·파라미터·예외 처리를 어노테이션으로 추상화.
- **forward vs redirect?** → forward 는 서버 내 (URL 유지, 같은 request), redirect 는 302 응답 → 브라우저 재요청 (URL 바뀜, 새 request).
- **doGet vs doPost?** → 의미는 HTTP 메서드대로. GET=조회, POST=변경. POST 후엔 PRG 로 redirect.
- **Servlet 의 스레드 안전성?** → 인스턴스는 1개·여러 스레드 공유. 인스턴스 필드 X, 메서드 지역 변수만.

---

# 2. Quick Reference (실무 복붙)

## Servlet 등록 (3 방법)

```java
// 1. 어노테이션 (Servlet 3.0+, 권장)
@WebServlet("/hello")
public class HelloServlet extends HttpServlet { ... }

// 2. web.xml
<servlet>
    <servlet-name>hello</servlet-name>
    <servlet-class>com.ssafy.HelloServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>hello</servlet-name>
    <url-pattern>/hello</url-pattern>
</servlet-mapping>

// 3. Spring Boot 의 ServletRegistrationBean
@Bean
public ServletRegistrationBean<HelloServlet> hello() {
    return new ServletRegistrationBean<>(new HelloServlet(), "/hello");
}
```

## URL 패턴

```
/exact          - /exact 만
/api/*          - /api 로 시작 (와일드카드)
*.do            - .do 로 끝
/               - 기본 (다른 매칭 없을 때)
```

## HttpServletRequest

```java
// 파라미터
req.getParameter("name");                    // String (없으면 null)
req.getParameterValues("tags");              // String[] (다중값)
req.getParameterMap();                       // Map<String, String[]>

// 헤더
req.getHeader("User-Agent");
req.getHeaders("Accept");                    // Enumeration
req.getMethod();                              // "GET" / "POST"
req.getRequestURI();                          // /path?query 제외
req.getRequestURL();                          // 전체 URL

// 세션·쿠키
HttpSession session = req.getSession();      // 없으면 생성
session.setAttribute("user", user);
Cookie[] cookies = req.getCookies();

// 속성 (Servlet 간 데이터 전달)
req.setAttribute("boards", list);
List<Board> list = (List<Board>) req.getAttribute("boards");

// 인코딩
req.setCharacterEncoding("UTF-8");          // getParameter 전에!
```

## HttpServletResponse

```java
// 상태
res.setStatus(200);
res.sendError(404, "Not Found");

// 헤더
res.setContentType("text/html;charset=UTF-8");
res.setHeader("Cache-Control", "no-store");
res.addCookie(new Cookie("name", "value"));

// 본문
res.getWriter().println("<h1>Hello</h1>");   // 텍스트
res.getOutputStream().write(bytes);           // 바이너리

// 리다이렉트
res.sendRedirect("/login");                   // 302
res.sendRedirect("https://...");
```

## forward vs redirect

```java
// forward (서버 내 이동, URL 유지, request 공유)
req.setAttribute("data", data);
req.getRequestDispatcher("/WEB-INF/views/list.jsp").forward(req, res);

// redirect (302 응답, URL 바뀜, 새 request)
res.sendRedirect("/login");
res.sendRedirect(req.getContextPath() + "/board");   // 컨텍스트 안전
```

| | forward | redirect |
|--|--|--|
| 시점 | 서버 내 | 브라우저 재요청 |
| URL | 그대로 | 바뀜 |
| request | 공유 (`setAttribute`) | 새로 |
| 외부 URL | X | O |
| 용도 | View 렌더 | POST 후, 다른 도메인 |

## 라이프사이클

```
init()      <- 첫 요청 또는 시작 시 1번
service()   <- 매 요청 (HTTP 메서드별로 doGet/doPost 호출)
  -> doGet / doPost
destroy()   <- 종료 시 1번
```

```java
@Override
public void init() throws ServletException {
    // DB 커넥션 풀 초기화 등
}

@Override
public void destroy() {
    // 자원 해제
}
```

## 한글 처리 (3 단계)

```java
// 1. JSP 페이지 인코딩
<%@ page contentType="text/html;charset=UTF-8" %>

// 2. 요청 디코딩 (getParameter 전에)
req.setCharacterEncoding("UTF-8");

// 3. 응답 인코딩
res.setContentType("text/html;charset=UTF-8");
```

Filter 로 일괄 처리 권장.

## 에러 페이지

```xml
<!-- web.xml -->
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
| 인스턴스 필드 사용 → 스레드 안전성 X | 메서드 지역 변수만 |
| 한글 깨짐 | `setCharacterEncoding("UTF-8")` (getParameter 전) |
| `sendRedirect` 후 코드 계속 실행 | 명시적 `return` |
| POST 후 forward → F5 중복 등록 | redirect (PRG) |
| 직접 `/views/list.jsp` 접근 | `/WEB-INF/views/` 안에 두면 차단 |
| `getWriter()` + `getOutputStream()` 같이 | 둘 중 하나만 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Servlet (32p)
│
├── [A] 등록
│   ├── @WebServlet (3.0+)
│   ├── web.xml
│   └── URL 패턴 (정확 / * / *.확장자)
│
├── [B] HttpServletRequest
│   ├── 파라미터 (getParameter / Map)
│   ├── 헤더 (getHeader)
│   ├── 세션 (getSession)
│   ├── 쿠키 (getCookies)
│   └── 속성 (setAttribute / getAttribute)
│
├── [C] HttpServletResponse
│   ├── 상태 (setStatus / sendError)
│   ├── 헤더 (setContentType / addCookie)
│   ├── 본문 (getWriter / getOutputStream)
│   └── 리다이렉트 (sendRedirect)
│
├── [D] HTTP 메서드 처리
│   ├── doGet (조회)
│   ├── doPost (변경)
│   ├── doPut / doDelete (REST)
│   └── service (디스패치)
│
├── [E] 이동 방식
│   ├── forward (서버 내, URL 유지)
│   ├── redirect (302, 새 request)
│   └── PRG 패턴 (POST -> Redirect -> GET)
│
├── [F] 라이프사이클
│   ├── init (1번)
│   ├── service (매 요청)
│   └── destroy (1번)
│
└── [G] 운영
    ├── 한글 처리 (3 단계)
    ├── 에러 페이지 (web.xml)
    ├── 스레드 안전성 (필드 X)
    └── WEB-INF 보안
```

## 학습 진도 체크리스트

### A. 등록·라우팅
- [ ] `@WebServlet` 어노테이션
- [ ] URL 패턴 종류
- [ ] web.xml 의 servlet-mapping

### B. 요청·응답
- [ ] getParameter / setAttribute
- [ ] setContentType / sendRedirect
- [ ] 한글 인코딩 3 단계

### C. 이동
- [ ] forward vs redirect 의미·시점
- [ ] PRG (POST → Redirect → GET)
- [ ] WEB-INF 보안 정책

### D. 라이프사이클
- [ ] init / service / destroy
- [ ] 스레드 안전성 (인스턴스 공유)
- [ ] 인스턴스 필드 금지

### E. 디버깅
- [ ] 한글 깨짐 원인 찾기
- [ ] 에러 페이지 매핑
- [ ] 세션·쿠키 검사

## 연관 강의

```
1강 Servlet         <- 현재 위치
2강 JSP             -> 화면 출력 분리
3강 Cookie/Session  -> 상태 유지
4강 EL/JSTL         -> JSP 깔끔하게
5강 Filter          -> 공통 처리
6강 종합 실습       -> 게시판 CRUD
Framework 1~11강    -> Spring MVC 로 추상화
```

→ 다음 (JSP) 에서 **화면 출력을 Servlet 에서 분리**.
