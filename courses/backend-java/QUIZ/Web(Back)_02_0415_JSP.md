# JSP — 퀴즈

> 16문항 · 개념 5 · 적용 4 · 디버그 3 · 면접 4.

---

## A. 개념

### Q1. JSP 가 컨테이너에서 실행되는 메커니즘을 3단계로?

<details><summary>정답</summary>

1. **변환**: `.jsp` → `.java` (서블릿 소스 자동 생성)
2. **컴파일**: `.java` → `.class`
3. **로딩·실행**: 클래스 로드 후 매 요청마다 `_jspService()` 호출

첫 요청만 1·2 수행, 이후는 캐시.

</details>

### Q2. JSP 4가지 스크립트 요소를 표기·변환 위치로?

<details><summary>정답</summary>

| 표기 | 이름 | 변환 위치 |
|--|--|--|
| `<%! ... %>` | 선언 | 클래스 멤버 |
| `<% ... %>` | 스크립틀릿 | `_jspService` 본문 |
| `<%= ... %>` | 표현식 | `out.print(...)` |
| `<%-- ... --%>` | JSP 주석 | 변환 시 제거 |

</details>

### Q3. JSP 내장 객체 9개?

<details><summary>정답</summary>

`request`, `response`, `session`, `application`, `out`, `pageContext`, `config`, `page`, `exception` (`isErrorPage=true` 시).

</details>

### Q4. 4가지 스코프와 기간?

<details><summary>정답</summary>

| 스코프 | 객체 | 기간 |
|--|--|--|
| `page` | `pageContext` | 현재 JSP 한 번 처리 |
| `request` | `request` | 한 요청-응답 |
| `session` | `session` | 한 사용자 브라우저 세션 |
| `application` | `application` | 앱 전체 |

EL `${name}` 탐색 순서도 이 순.

</details>

### Q5. `<%@ include %>` vs `<jsp:include>` 차이?

<details><summary>정답</summary>

- `<%@ include file="x.jsp" %>` — **변환 시점** 합치기 (정적)
- `<jsp:include page="x.jsp"/>` — **요청 시점** 별도 실행 후 결과 합치기 (동적). `<jsp:param>` 으로 파라미터 전달 가능.

자주 바뀌거나 파라미터화 = 후자.

</details>

---

## B. 적용

### Q6. 다음 JSP 출력?

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<% int x = 10; %>
<p><%= x * 3 %></p>
<%-- <%= x %> --%>
```

<details><summary>정답</summary>

```html
<p>30</p>
```

세 번째 `<%= x %>` 는 JSP 주석 안 → 변환 시 제거.

</details>

### Q7. 다음 스크립틀릿을 EL+JSTL 로?

```jsp
<%
  String name = request.getParameter("name");
  if (name != null && !name.isEmpty()) {
%>
  <h1>Hello, <%= name %></h1>
<% } else { %>
  <p>Please enter name</p>
<% } %>
```

<details><summary>정답</summary>

```jsp
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<c:choose>
  <c:when test="${not empty param.name}">
    <h1>Hello, <c:out value="${param.name}"/></h1>
  </c:when>
  <c:otherwise>
    <p>Please enter name</p>
  </c:otherwise>
</c:choose>
```

`<c:out>` 가 XSS escape.

</details>

### Q8. Servlet 에서 `request.setAttribute("user", userObj)` 후 forward. JSP 에서 EL 표기 두 가지?

<details><summary>정답</summary>

```jsp
${user}                  <%-- 자동 탐색 --%>
${requestScope.user}      <%-- 명시 --%>
```

세션에 같은 이름 있을 가능성 있으면 명시가 안전.

</details>

### Q9. forward 후 URL 은?

```java
req.setAttribute("ok", true);
req.getRequestDispatcher("/result.jsp").forward(req, resp);
```

<details><summary>정답</summary>

원래 요청 URL 그대로 (예: `/process`). forward 는 서버 내부 이동 — 브라우저 모름. URL 바꾸려면 `sendRedirect`.

</details>

---

## C. 디버그

### Q10. `${user.name}` 이 그대로 글자로 출력. 왜?

<details><summary>정답</summary>

JSP 2.4 이하(`web.xml version="2.4"`) 에서 EL 비활성. 또는 `<%@ page isELIgnored="true" %>` 가 어딘가 설정.

해결: `<web-app version="6.0">` (Jakarta EE 10) 또는 `isELIgnored="false"`.

</details>

### Q11. `<c:forEach var="b" items="${boards}">` 가 NPE. 원인?

<details><summary>정답</summary>

`${boards}` 가 null. 컨트롤러가 `setAttribute("boards", ...)` 안 했거나 이름 오타. `<c:forEach>` 자체는 null 도 빈 컬렉션처럼 처리(조용히 0회) — NPE 가 났다면 다른 코드(`${boards.size()}` 등) 에서.

</details>

### Q12. forward 후 `response.sendRedirect` 호출하면?

<details><summary>정답</summary>

`IllegalStateException`. 이미 응답이 위탁된 후라 다시 못 씀. forward 와 redirect 는 둘 중 하나만.

</details>

---

## D. 면접·설계

### Q13. 왜 현대 Spring 이 JSP 대신 Thymeleaf 를 쓰나?

<details><summary>모범 답안</summary>

1. **자연 HTML**: Thymeleaf 템플릿이 그대로 브라우저에서 열림, 디자이너 IDE 없이 수정 가능
2. **비파괴적 표현식**: `th:text`, `th:if` 어트리뷰트 기반
3. **타입 안전**: 컴파일 시 검증
4. **레이아웃·프래그먼트**: `th:replace` 가 깔끔
5. **레거시 부담 X**: JSP 는 스크립틀릿+EL+JSTL+태그 라이브러리 누적

회사 표준이 JSP 면 거기 맞추는 게 우선.

</details>

### Q14. `/WEB-INF/views/` 아래 두는 보안 이유?

<details><summary>모범 답안</summary>

`WEB-INF` 아래 리소스는 컨테이너가 브라우저 직접 요청 차단. JSP 에 접근하려면 반드시 컨트롤러 forward 거쳐야 → MVC 분리 강제 + 인증/권한 체크 보장.

</details>

### Q15. `session.invalidate()` vs `removeAttribute`?

<details><summary>정답</summary>

- `removeAttribute("user")` — 세션은 유지, 특정 attribute 만 삭제
- `invalidate()` — 세션 자체 파괴, 모든 attribute + 세션 ID 무효. 로그아웃

`invalidate` 후 `getSession()` 부르면 새 세션 생성.

</details>

### Q16. 스크립틀릿이 안티패턴인 5가지 이유?

<details><summary>모범 답안</summary>

1. **테스트 불가** — 자바 코드를 JSP 안에 박으면 단위 테스트 어려움
2. **재사용 불가** — JSP 단위로 묶임
3. **디버깅 난해** — 생성된 서블릿의 라인 번호 ≠ JSP 라인 번호
4. **디자이너 협업 불가** — 자바 코드에 막힘
5. **유지보수성 ↓** — HTML+자바 섞여 인지 부하

해결: EL + JSTL 또는 Thymeleaf.

</details>
