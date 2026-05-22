# JSP — 개념 · 기본 태그 · 페이지 이동

> **이 강의는 무엇인가**: HTML 본문에 자바 코드를 삽입해 서버에서 동적 페이지를 생성하는 **JSP(Jakarta Server Pages)** 의 문법·동작 원리·생명주기. 그리고 페이지 간 이동 방식 2가지(forward/redirect).
> **왜 배우는가**: Spring 의 view 기술로 여전히 한국 SI 의 표준. JPA/MVC 보다 위 계층에서 화면을 그리는 단계 — 원리를 모르면 EL/JSTL 도 마법으로 보인다.

---

## 들어가기 전에

- **선수**: Servlet (Servlet 의 생명주기·request/response), HTML 기본.
- **마인드셋**: "JSP 도 결국 Servlet 이다" — JSP 의 모든 문법이 컴파일 후 Servlet 의 자바 코드가 됨.

---

# Part A. JSP 개념

## 1. JSP 의 정의

- **Jakarta Server Pages** (옛 JavaServer Pages)
- Servlet 표준 기반의 웹 애플리케이션 개발 언어
- **HTML 안에 Java 를 삽입** 해 동적 페이지 생성
- 실행 시 **Servlet 으로 변환된 후 컴파일** → 실행

**Servlet vs JSP — 같은 일을 다른 방식으로**:

```java
// Servlet - HTML 출력이 어색
out.println("<html>");
out.println("<body>");
out.println("<h1>Hello, " + name + "</h1>");
out.println("</body>");
out.println("</html>");
```

```jsp
<!-- JSP - HTML 중심 -->
<html>
<body>
    <h1>Hello, <%= name %></h1>
</body>
</html>
```

**JSP 가 더 자연스러운 경우**: HTML 위주에 동적 부분이 적을 때.
**Servlet 이 더 자연스러운 경우**: 로직 위주에 HTML 이 적을 때.

## 2. JSP 변환·실행 흐름

```
[작성된 JSP]                hello.jsp

      | ① 첫 요청 시 (또는 변경 감지)
      ▼
[변환] JSP → Servlet 자바 코드 (hello_jsp.java)
      |
      ▼
[컴파일] .java → .class (hello_jsp.class)
      |
      ▼
[Servlet 실행] doGet/doPost 호출
      |
      ▼
[응답] HTML 클라이언트로

--------------------------------

이후 요청부터는 이미 생성된 .class 재사용 (변환·컴파일 안 함)
```

**확인 방법**: Tomcat 의 `work/Catalina/localhost/...` 디렉토리에 변환된 `.java` 파일이 있음. 열어보면 자바 코드로 보이는 JSP.

## 3. JSP 의 생명주기

```
1) 변환 (Translation)           - .jsp → .java (첫 요청 또는 수정 시)
    |
    ▼
2) 컴파일 (Compilation)          - .java → .class
    |
    ▼
3) Load 및 객체 생성             - 클래스 로딩
    |
    ▼
4) jspInit()                     - 1번만 (초기화)
    |
    ▼
5) _jspService()                 - 매 요청 (doGet/doPost 의 JSP 버전)
    |
    | (Tomcat 종료 또는 JSP 수정 시)
    ▼
6) jspDestroy()                  - 1번만 (정리)
```

Servlet 의 생명주기와 똑같음 (init/service/destroy 가 jspInit/_jspService/jspDestroy 로 이름만 다름). JSP 도 본질은 Servlet.

---

# Part B. JSP 기본 태그

## 4. 5가지 스크립팅 요소

```jsp
<%-- 1) 주석 (Comment) - 클라이언트에 안 보임 --%>

<%@ ... %>             <%-- 2) 지시자 (Directive) --%>

<% ... %>              <%-- 3) 스크립틀릿 (Scriptlet) - 자바 코드 --%>

<%= ... %>             <%-- 4) 표현식 (Expression) - 값 출력 --%>

<%! ... %>             <%-- 5) 선언문 (Declaration) - 멤버 변수·메서드 --%>
```

## 5. 주석 (Comment)

```jsp
<!-- 1) HTML 주석 - 클라이언트가 소스 보기 하면 보임 -->

<%-- 2) JSP 주석 - 클라이언트에 안 보임 (서버에서만) --%>
```

**민감 정보는 반드시 JSP 주석** (`<%--`). HTML 주석은 브라우저 개발자 도구로 누구나 볼 수 있음.

## 6. 지시자 (Directive) — 3가지

```jsp
<%-- 1) page - 페이지 전체 설정 --%>
<%@ page language="java"
        contentType="text/html;charset=UTF-8"
        pageEncoding="UTF-8"
        import="java.util.*, java.time.*"
        errorPage="/error.jsp" %>

<%-- 2) include - 다른 JSP 합치기 (컴파일 시점) --%>
<%@ include file="header.jsp" %>

<%-- 3) taglib - 커스텀 태그 라이브러리 사용 --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
```

**`page` 디렉티브의 주요 속성**:
| 속성 | 의미 |
|--|--|
| `language` | 스크립트 언어 (`java` 만 가능) |
| `contentType` | 응답 MIME + 인코딩 |
| `pageEncoding` | 파일 자체의 인코딩 |
| `import` | 자바 패키지 import |
| `errorPage` | 예외 발생 시 이동할 페이지 |
| `isErrorPage` | 이 페이지가 에러 페이지인가? |
| `session` | 세션 사용 여부 (기본 true) |

## 7. 스크립틀릿 (Scriptlet) — `<% ... %>`

```jsp
<%
    String name = request.getParameter("name");
    int age = 25;
    if (name == null) name = "guest";
%>
```

- 자바 코드를 그대로 작성
- 변환 후 `_jspService()` 메서드 안에 들어감 → **로컬 변수**
- 가독성 나빠서 **현대 JSP 에선 EL/JSTL 로 대체**

## 8. 표현식 (Expression) — `<%= ... %>`

```jsp
<h1>안녕하세요, <%= name %></h1>
<p>나이: <%= age %></p>
<p>현재 시각: <%= new java.util.Date() %></p>
```

- 결과 값을 **응답에 출력**
- 변환 후 `out.println(...)` 으로 변환
- **세미콜론 X**

## 9. 선언문 (Declaration) — `<%! ... %>`

```jsp
<%!
    // 클래스 멤버 - 매 요청 사이 공유 (싱글톤 주의!)
    private int counter = 0;

    public int increment() {
        return ++counter;
    }
%>

<p>방문 수: <%= increment() %></p>
```

- **클래스 레벨 멤버 변수·메서드** 선언
- ⚠ **싱글톤 인스턴스의 인스턴스 필드** — thread-unsafe. 사용자별 데이터에 쓰면 race condition. **거의 안 씀**

---

# Part C. 페이지 이동

## 10. 4가지 페이지 이동 방식

```
       1) <jsp:forward>       ← 서버 내부 forward (JSP 액션)
       2) <jsp:include>       ← 다른 JSP 합치기 (실행 시점)
       3) response.sendRedirect ← 클라이언트 redirect
       4) <a href>            ← 클라이언트 클릭 후 이동 (사용자 액션)
```

## 11. `<jsp:forward>` — 서버 내부 forward

```jsp
<%-- /check.jsp --%>
<%
    String role = (String) session.getAttribute("role");
    if ("ADMIN".equals(role)) {
%>
        <jsp:forward page="/admin.jsp">
            <jsp:param name="from" value="check" />
        </jsp:forward>
<%
    } else {
%>
        <jsp:forward page="/user.jsp" />
<%
    }
%>
```

**특징**:
- 서버 내부에서 다른 JSP/Servlet 으로 제어 위임
- URL 안 바뀜 (브라우저는 모름)
- request 객체 유지 → `setAttribute` 데이터 공유
- `<jsp:param>` 으로 추가 파라미터

**Servlet 의 `req.getRequestDispatcher(...).forward(req, res)` 와 같음**.

## 12. `<jsp:include>` — 동적 include

```jsp
<%-- /layout.jsp --%>
<html>
<body>
    <jsp:include page="/header.jsp" />     <%-- 실행 시점에 합쳐짐 --%>

    <main>본문 내용</main>

    <jsp:include page="/footer.jsp">
        <jsp:param name="year" value="2025" />
    </jsp:include>
</body>
</html>
```

**`<jsp:include>` vs `<%@ include %>`**:

| | `<%@ include file %>` | `<jsp:include page>` |
|--|--|--|
| 시점 | 컴파일 시 (정적) | 실행 시 (동적) |
| 변수 공유 | 가능 (한 파일처럼) | 안 됨 (각자 독립) |
| 파라미터 전달 | 안 됨 | `<jsp:param>` |
| 성능 | 빠름 | 약간 느림 (매 요청마다 include) |
| 용도 | 정적 헤더·푸터 | 동적 변경되는 부분 |

## 13. `response.sendRedirect` — 클라이언트 redirect

```jsp
<%
    if (loginUser == null) {
        response.sendRedirect("/login.jsp");
        return;     // ⚠ JSP 가 계속 실행되지 않도록 명시적 return
    }
%>
```

**Servlet 의 `res.sendRedirect` 와 동일**:
- 응답에 `302 + Location` 보내고 브라우저가 새 GET 요청
- URL 바뀜, request 객체 새로
- HTTP 요청 2번

## 14. `<a href>` — 사용자 클릭

```jsp
<a href="/detail?id=${board.id}">상세 보기</a>
<a href="/login.jsp">로그인</a>
```

- HTML 의 일반 링크
- 사용자가 클릭해야 이동 (자동 아님)
- 페이지 간 자연스러운 네비게이션

## 15. 4가지 이동 방식 비교

| 방식 | URL 변경 | 자동/수동 | request | 시점 |
|--|--|--|--|--|
| `<jsp:forward>` | ❌ | 자동 | 유지 | 서버에서 |
| `<jsp:include>` | ❌ | 자동 | 유지 | 실행 시 합침 |
| `sendRedirect` | ✅ | 자동 | 새로 | 브라우저가 새 요청 |
| `<a href>` | ✅ | 수동 (클릭) | 새로 | 사용자 액션 |

---

## 16. 코드 깊게 — 로그인 + 게시판 풀스택

```jsp
<%-- /login.jsp --%>
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>

<!DOCTYPE html>
<html>
<head><title>로그인</title></head>
<body>
    <h1>로그인</h1>

    <c:if test="${not empty error}">
        <p style="color:red">${error}</p>
    </c:if>

    <form method="POST" action="/auth">
        <input type="text" name="id" placeholder="아이디" required>
        <input type="password" name="password" placeholder="비밀번호" required>
        <button>로그인</button>
    </form>
</body>
</html>
```

```java
// === AuthServlet ===
@WebServlet("/auth")
public class AuthServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        req.setCharacterEncoding("UTF-8");
        String id  = req.getParameter("id");
        String pwd = req.getParameter("password");

        if (userService.authenticate(id, pwd)) {
            req.getSession().setAttribute("loginUser", id);
            res.sendRedirect("/board/list.jsp");          // PRG 패턴
        } else {
            req.setAttribute("error", "로그인 실패");
            req.getRequestDispatcher("/login.jsp").forward(req, res);
        }
    }
}
```

```jsp
<%-- /board/list.jsp --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%
    String user = (String) session.getAttribute("loginUser");
    if (user == null) {
        response.sendRedirect("/login.jsp");
        return;
    }
%>

<jsp:include page="/header.jsp" />

<h1>게시판</h1>
<p>안녕하세요, <%= user %>님</p>

<table>
    <c:forEach var="b" items="${boards}">
        <tr>
            <td>${b.id}</td>
            <td><a href="/detail?id=${b.id}">${b.title}</a></td>
            <td>${b.writer}</td>
        </tr>
    </c:forEach>
</table>

<jsp:include page="/footer.jsp" />
```

---

## 17. 실전 패턴 / 자주 빠지는 함정

### JSP 기본
- ❌ `<%! %>` 에 사용자별 데이터 저장 → 싱글톤 race condition ✅ 스크립틀릿 또는 request scope
- ❌ HTML 주석에 민감 정보 ✅ JSP 주석 (`<%-- --%>`)
- ❌ JSP 안에 비즈니스 로직 (DB 호출 등) ✅ Servlet/Service 에서 처리 후 JSP 는 view 만
- ❌ 스크립틀릿 (`<% %>`) 남발 ✅ EL/JSTL 로 대체

### 인코딩
- ❌ `pageEncoding` 만 설정 + `contentType` 누락 → 응답이 깨짐 ✅ 둘 다 설정
- ❌ JSP 페이지마다 일일이 `<%@ page %>` 작성 ✅ `<%@ include file="common.jsp" %>` 로 공통화

### 페이지 이동
- ❌ `sendRedirect` 후 코드 계속 실행 → 이중 응답 시도 ✅ `return;` 명시
- ❌ `<%@ include %>` 와 `<jsp:include>` 혼동 ✅ 정적 = `<%@ include%>`, 동적 = `<jsp:include>`
- ❌ POST 처리 후 `<jsp:forward>` → F5 시 중복 ✅ `sendRedirect` (PRG)

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| 한글 응답 깨짐 | `contentType` 누락 | `<%@ page contentType="text/html;charset=UTF-8" %>` |
| 한글 파일 인코딩 깨짐 | `pageEncoding` 누락 | `pageEncoding="UTF-8"` 추가 |
| `${...}` 가 그대로 출력 | EL 비활성 + 옛 JSP | `<%@ page isELIgnored="false" %>` |
| `<%! %>` 변수가 사용자별로 다른 값 기대했는데 공유됨 | 클래스 멤버 = 싱글톤 | 메서드 로컬 (`<% %>`) 으로 |
| `sendRedirect` 후 `IllegalStateException: Cannot forward...` | 응답 이미 commit | `return;` 추가 |
| `<jsp:include page="header.jsp" />` 의 변수 사용 안 됨 | 동적 include 는 변수 공유 X | `<%@ include file="header.jsp" %>` 로 |
| Tomcat 의 `work/` 폴더에 `.java` 보이는데 변경 사항 반영 안 됨 | JSP 캐시 | `work/` 삭제 + Tomcat 재시작 |

---

## 18. 자가점검

1. JSP 가 실행될 때까지의 흐름 3단계 (변환 → ? → 실행)?
2. JSP 의 5가지 스크립팅 요소와 각 용도?
3. HTML 주석과 JSP 주석의 차이?
4. `<jsp:forward>` 와 `response.sendRedirect()` 의 차이 3가지?
5. `<%@ include file %>` 와 `<jsp:include page>` 의 차이?
6. `<%! %>` 에 데이터 저장하면 왜 안 좋은가?
7. JSP 안에 비즈니스 로직을 두면 안 되는 이유?

<details><summary>풀이</summary>

1. (1) **변환** (.jsp → .java) → (2) **컴파일** (.java → .class) → (3) **실행** (Servlet 으로). 첫 요청 시 또는 JSP 변경 시 1, 2 단계.
2. **주석 `<%--`**: JSP 주석 (클라이언트 X). **지시자 `<%@`**: 페이지 설정 (`page`/`include`/`taglib`). **스크립틀릿 `<%`**: 자바 코드. **표현식 `<%=`**: 값 출력. **선언문 `<%!`**: 클래스 멤버.
3. **HTML 주석**: 클라이언트가 소스 보기 시 보임. **JSP 주석**: 서버에서만 — 클라이언트엔 안 보냄. 민감 정보엔 JSP 주석.
4. (a) **URL**: forward 안 바뀜, redirect 바뀜. (b) **request**: forward 유지, redirect 새 객체. (c) **요청 수**: forward 1, redirect 2.
5. **`<%@ include %>`**: 컴파일 시점에 합쳐짐 (한 파일처럼). 변수 공유 가능. 정적 헤더·푸터. **`<jsp:include>`**: 실행 시점에 합쳐짐. 변수 공유 X. 파라미터 전달 가능. 동적 변경되는 부분.
6. JSP 는 컴파일 후 Servlet (싱글톤) → `<%! %>` 안의 변수는 **클래스 멤버**, 모든 사용자가 공유. **멀티스레드 race condition** + 사용자 A 의 데이터가 사용자 B 에게 보일 수 있음.
7. (a) HTML 과 자바 코드가 섞여 가독성 ↓. (b) JSP 는 매 요청 컴파일 가능성 → 비즈니스 로직 변경 시 재컴파일. (c) **테스트 불가** — 서블릿 컨테이너 필요. (d) **재사용 불가** — JSP 는 view 전용, Service 는 여러 컨트롤러에서 재사용.

</details>

---

## 19. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.9 JSP 개념·변환·생명주기 | §1 ~ §3 (Part A) |
| p.10 ~ p.20 JSP 기본 태그 (주석·지시자·스크립트) | §4 ~ §9 (Part B) |
| p.21 ~ p.24 페이지 이동 (forward·include·redirect·href) | §10 ~ §15 (Part C) |
| p.25 마무리 | (생략) |

_25p 슬라이드 모두 커버._
