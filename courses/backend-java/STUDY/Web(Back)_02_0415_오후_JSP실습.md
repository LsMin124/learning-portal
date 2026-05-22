# JSP 실습 — Servlet → JSP 변환 + 미니 CRUD

> **이 강의는 무엇인가**: 6페이지짜리 실습 가이드. 새 개념 없이 **JSP 강의에서 배운 문법을 손에 익히는** 시간. ① 이전에 작성한 Servlet 코드를 JSP 로 바꿔보고, ② 간단한 게시판 CRUD 와 ③ 회원 CRUD 를 JSP 로 직접 작성.
> **왜 배우는가**: Servlet 의 `out.println` 으로 HTML 출력하던 코드를 JSP 로 변환하면서 "JSP 가 결국 Servlet" 임을 체감. EL/JSTL 강의(다음 회차) 의 자연스러운 디딤돌.

---

## 들어가기 전에

- **선수**: Servlet 강의 + JSP 강의의 5가지 스크립팅 요소·4가지 페이지 이동.
- **마인드셋**: "실습은 머리로 익히는 게 아니라 손으로 익히는 것". 30분 코딩이 30분 강의보다 가치 있다.

---

## 1. 실습 1 — Servlet → JSP 변환 패턴

### Before — Servlet 으로 HTML 출력

```java
@WebServlet("/users")
public class UserListServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {

        req.setCharacterEncoding("UTF-8");
        res.setContentType("text/html;charset=UTF-8");

        List<User> users = userService.findAll();

        try (PrintWriter out = res.getWriter()) {
            out.println("<!DOCTYPE html>");
            out.println("<html><body>");
            out.println("<h1>사용자 목록</h1>");
            out.println("<ul>");
            for (User u : users) {
                out.println("<li>" + u.getName() + " (" + u.getEmail() + ")</li>");
            }
            out.println("</ul>");
            out.println("</body></html>");
        }
    }
}
```

→ HTML 출력이 자바 문자열로 묻혀 가독성 떨어짐.

### After — Servlet (Controller) + JSP (View) 분리

```java
// Servlet 은 Controller 역할만
@WebServlet("/users")
public class UserListServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {

        req.setCharacterEncoding("UTF-8");
        List<User> users = userService.findAll();
        req.setAttribute("users", users);
        req.getRequestDispatcher("/WEB-INF/views/user/list.jsp")
           .forward(req, res);
    }
}
```

```jsp
<%-- /WEB-INF/views/user/list.jsp --%>
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head><title>사용자 목록</title></head>
<body>
    <h1>사용자 목록</h1>
    <ul>
        <c:forEach var="u" items="${users}">
            <li>${u.name} (${u.email})</li>
        </c:forEach>
    </ul>
</body>
</html>
```

**변환의 효과**:
- HTML 이 HTML 답게 보임 (디자이너·퍼블리셔 협업 가능)
- Servlet 은 **요청 → 데이터 → forward** 만 (책임 분리)
- 화면 변경 시 자바 재컴파일 X

---

## 2. 실습 2 — 게시판 CRUD JSP 미니 예제

### 5개 핸들러 + 5개 JSP

```
URL                          Servlet (Controller)          JSP (View)
-------------------------    --------------------------    ---------------------
GET  /board                  BoardListServlet              /board/list.jsp
GET  /board/{id}             BoardDetailServlet            /board/detail.jsp
GET  /board/write            BoardFormServlet              /board/form.jsp
POST /board                  BoardWriteServlet → redirect  (없음)
POST /board/{id}/delete      BoardDeleteServlet → redirect (없음)
```

### list.jsp — `<c:forEach>` 로 반복

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<html>
<body>
    <h1>게시판</h1>
    <a href="/board/write">새 글</a>
    <table border="1">
        <tr><th>ID</th><th>제목</th><th>작성자</th></tr>
        <c:forEach var="b" items="${boards}">
            <tr>
                <td>${b.id}</td>
                <td><a href="/board/${b.id}">${b.title}</a></td>
                <td>${b.writer}</td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
```

### form.jsp — 등록/수정 공용

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<html>
<body>
    <h1>${empty board ? '새 글 작성' : '수정'}</h1>
    <form method="POST" action="${empty board ? '/board' : '/board/'.concat(board.id)}">
        <input name="title"   value="${board.title}"   required>
        <textarea name="content">${board.content}</textarea>
        <input name="writer"  value="${board.writer}"  required>
        <button>저장</button>
    </form>
</body>
</html>
```

### detail.jsp — 상세 + 삭제 버튼

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<html>
<body>
    <h1>${board.title}</h1>
    <p>작성자: ${board.writer}</p>
    <pre>${board.content}</pre>

    <a href="/board/${board.id}/edit">수정</a>
    <form method="POST" action="/board/${board.id}/delete" style="display:inline">
        <button>삭제</button>
    </form>
    <a href="/board">목록</a>
</body>
</html>
```

---

## 3. 실습 3 — 회원 CRUD

게시판과 거의 동일한 구조. 차이는:
- `User` DTO (id, email, password, name, role)
- 비밀번호 처리 (입력 시 `<input type="password">`, 출력 시 마스킹 또는 표시 안 함)
- 권한 검증 (관리자만 회원 목록 접근)

```jsp
<%-- /user/list.jsp (관리자용) --%>
<c:if test="${sessionScope.loginUser.role != 'ADMIN'}">
    <c:redirect url="/" />
</c:if>

<table>
    <c:forEach var="u" items="${users}">
        <tr>
            <td>${u.id}</td>
            <td>${u.email}</td>
            <td>${u.name}</td>
            <td>${u.role}</td>
            <%-- 비밀번호는 절대 표시 X --%>
        </tr>
    </c:forEach>
</table>
```

---

## 4. 실습 체크리스트

- ☑ Servlet 의 `req.setAttribute("key", value)` 가 JSP 에서 `${key}` 로 접근 가능 확인
- ☑ JSP 안에서 자바 코드(`<% %>`) 대신 EL (`${...}`) 사용
- ☑ 반복은 `<c:forEach>`, 조건은 `<c:if>` / `<c:choose>`
- ☑ POST 후 redirect (POST-Redirect-GET) 적용 — F5 새로고침 시 중복 등록 방지
- ☑ JSP 파일을 `/WEB-INF/views/` 아래에 두기 (직접 URL 접근 차단)
- ☑ 한글 안 깨짐 확인 (`pageEncoding="UTF-8"` + `req.setCharacterEncoding("UTF-8")`)

---

## 5. 자주 빠지는 함정

- ❌ JSP 안에 직접 DB 호출 ✅ Servlet → Service → JSP 분리
- ❌ JSP 파일을 `webapp/` 루트에 둠 → 사용자가 `/list.jsp` 로 직접 접근 가능 ✅ `WEB-INF/views/` 안에
- ❌ POST 후 forward 로 list view → F5 중복 ✅ `res.sendRedirect(...)`
- ❌ `<% %>` 스크립틀릿 남발 ✅ EL/JSTL 우선
- ❌ HTML 출력에 사용자 입력 그대로 → XSS ✅ JSTL 의 `<c:out>` 또는 `${fn:escapeXml(...)}`
- ❌ 한글 form 제출 후 깨짐 ✅ `req.setCharacterEncoding("UTF-8")` 첫 줄에

---

## 6. 자가점검

1. Servlet 으로 작성한 HTML 출력 코드를 JSP 로 옮길 때 무엇이 바뀌나?
2. JSP 가 `WEB-INF/views/` 안에 있어야 하는 보안 이유는?
3. 게시판 등록 처리(POST /board) 후 `redirect:/board` 로 보내는 이유?
4. JSP 안에 `<% %>` 대신 EL/JSTL 을 쓰는 이유?

<details><summary>풀이</summary>

1. (a) `out.println` 같은 자바 코드가 사라짐. (b) Servlet 은 데이터 준비만, JSP 는 화면만 책임. (c) Controller (Servlet) → View (JSP) 책임 분리. (d) 디자이너·퍼블리셔 협업 가능.
2. **`WEB-INF/` 안 자원은 외부에서 직접 URL 로 접근 불가** (Tomcat 의 기본 보안 정책). 사용자가 `/list.jsp` 로 직접 접근하면 컨트롤러 거치지 않고 빈 화면이 떠서, 데이터 흐름 + 인증 검증을 우회.
3. **F5 시 form 재제출** 방지 (POST-Redirect-GET). POST 응답을 JSP 로 forward 하면 브라우저가 그 응답을 POST 결과로 기억 → F5 시 다시 form 제출 → 중복 등록. redirect 면 GET 요청 새로 → F5 안전.
4. (a) 가독성 — HTML 과 자바 코드 안 섞임. (b) 스크립틀릿은 JSP 클래스의 메서드 안 코드라 디버깅 어려움. (c) 디자이너 친화 — EL/JSTL 은 HTML 비슷한 문법. (d) 보안 — EL 의 `${fn:escapeXml(...)}` 등으로 XSS 자동 방어.

</details>

---

## 7. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 실습 예제 (게시판·회원 CRUD·Servlet → JSP 변환) | §1, §2, §3 (실습 가이드 전체) |
| p.6 마무리 | (생략) |

_6p 슬라이드의 실습 가이드를 손에 익히기 좋게 구체 예제로 확장._
