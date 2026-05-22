# JSP — 치트시트

> 25p 슬라이드 · Java Server Pages, HTML 안에 자바.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **JSP = 결국 Servlet** (Tomcat 의 Jasper 가 자동 변환·컴파일)
2. **스크립틀릿 `<% %>` 대신 EL `${}` + JSTL `<c:...>`** 가 현대 권장
3. **9 내장 객체**: request, response, session, application, out, pageContext, page, config, exception
4. **page 디렉티브** 로 인코딩·import (`<%@ page contentType="text/html;charset=UTF-8" %>`)
5. **EL 4 스코프**: page < request < session < application (좁은 곳부터 검색)
6. **`/WEB-INF/views/` 안에 두기** → 외부 직접 접근 차단 (보안)

## 가장 중요한 코드 3개

```jsp
<%-- (1) 표준 JSP 헤더 + EL/JSTL --%>
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
<%-- (2) 조건부 렌더 --%>
<c:choose>
  <c:when test="${empty sessionScope.loginUser}">
    <a href="/login">로그인</a>
  </c:when>
  <c:otherwise>
    환영 ${sessionScope.loginUser.nickname}
    <a href="/logout">로그아웃</a>
  </c:otherwise>
</c:choose>
```

```jsp
<%-- (3) include + 폼 + XSS escape --%>
<jsp:include page="header.jsp"/>
<form method="post" action="/board">
  <input name="title" value="${board.title}"/>
  <textarea name="content"><c:out value="${board.content}"/></textarea>
  <button type="submit">저장</button>
</form>
```

## 면접 한 줄 답변
- **JSP vs Servlet?** → JSP 는 HTML 중심, Servlet 은 자바 중심. JSP 도 결국 Servlet 으로 변환.
- **EL 의 이점?** → 자바 코드 안 들어가서 디자이너 협업 가능 + XSS 자동 회피.
- **스크립틀릿이 비권장인 이유?** → HTML 안에 자바 섞임 → 유지보수·테스트 어려움.
- **`${user}` 못 찾는 이유?** → Servlet 에서 setAttribute 누락 / EL 비활성 / getter 없음.

---

# 2. Quick Reference (실무 복붙)

## 표준 JSP 헤더

```jsp
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<%@ page import="java.util.*, com.study.dto.*" %>
```

## 9 내장 객체

| 객체 | 자바 타입 | 역할 |
|--|--|--|
| `request` | HttpServletRequest | 요청·파라미터·attribute |
| `response` | HttpServletResponse | 응답 설정 |
| `session` | HttpSession | 세션 |
| `application` | ServletContext | 앱 전체 공유 |
| `out` | JspWriter | 출력 |
| `pageContext` | PageContext | 모든 scope 통합 |
| `page` | Object | JSP 자신 |
| `config` | ServletConfig | 설정 |
| `exception` | Throwable | `isErrorPage="true"` 일 때만 |

## 스크립트 요소 (가능한 안 쓰기)

```jsp
<%! private int count = 0; %>            <%-- 선언 (필드) --%>
<%  int x = 10; %>                        <%-- 스크립틀릿 (메서드 안 코드) --%>
<%= x + 1 %>                              <%-- 표현식 (출력) --%>
<%-- 주석 (서버측, 클라이언트 안 봄) --%>
```

→ 현대는 모두 EL/JSTL 로 대체.

## EL (Expression Language)

```jsp
${board.title}                            <%-- getter 자동 호출 --%>
${1 + 2}                                  <%-- 산술 --%>
${empty list}                             <%-- null 또는 size 0 --%>
${user.role == 'ADMIN'}                   <%-- 비교 --%>
${a and b or c}                           <%-- 논리 --%>

<%-- 4 scope 명시 --%>
${pageScope.x}
${requestScope.x}
${sessionScope.x}
${applicationScope.x}

<%-- 파라미터·쿠키·헤더 --%>
${param.id}
${paramValues.tags}
${header['User-Agent']}
${cookie.JSESSIONID.value}
```

## JSTL Core 태그 (`<c:>`)

```jsp
<c:set var="x" value="10"/>
<c:remove var="x"/>

<c:if test="${board != null}">
  ...
</c:if>

<c:choose>
  <c:when test="${user.role == 'ADMIN'}">관리자</c:when>
  <c:when test="${user.role == 'USER'}">일반</c:when>
  <c:otherwise>익명</c:otherwise>
</c:choose>

<c:forEach var="b" items="${boards}" varStatus="status">
  ${status.index} : ${b.title}
</c:forEach>

<c:forEach var="i" begin="1" end="10" step="1">
  ${i}
</c:forEach>

<c:url var="link" value="/boards/${b.id}"/>
<a href="${link}">상세</a>

<c:out value="${userInput}"/>             <%-- XSS escape --%>

<c:redirect url="/login"/>
```

## JSTL fmt 태그 (`<fmt:>`)

```jsp
<fmt:formatDate value="${board.createdAt}" pattern="yyyy-MM-dd HH:mm"/>
<fmt:formatNumber value="${price}" pattern="#,###"/>
<fmt:formatNumber value="${rate}" type="percent"/>
```

## 액션 태그 (`<jsp:>`)

```jsp
<%-- 동적 include (런타임) --%>
<jsp:include page="header.jsp">
  <jsp:param name="title" value="목록"/>
</jsp:include>

<%-- 정적 include (컴파일 타임, 디렉티브) --%>
<%@ include file="header.jsp" %>

<%-- forward --%>
<jsp:forward page="login.jsp"/>

<%-- JavaBean (옛 스타일) --%>
<jsp:useBean id="board" class="com.study.Board" scope="request"/>
<jsp:setProperty name="board" property="*"/>
```

## 디렉티브

```jsp
<%@ page contentType="text/html;charset=UTF-8"
         pageEncoding="UTF-8"
         import="java.util.*"
         session="true"
         isErrorPage="false"
         errorPage="/WEB-INF/views/error.jsp" %>

<%@ include file="header.jsp" %>

<%@ taglib prefix="c" uri="jakarta.tags.core" %>
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `${board.title}` 그대로 출력 | EL 비활성 / Servlet setAttribute 누락 / getter 없음 |
| `<c:forEach>` 그대로 출력 | taglib 선언 + JSTL 의존성 |
| `<` 깨짐 | `&lt;` 또는 CDATA |
| 한글 깨짐 | `page contentType + pageEncoding` |
| JSP 직접 URL 접근 | `/WEB-INF/views/` |
| 스크립틀릿 남발 | EL/JSTL |
| `${user.password}` 노출 | DTO 분리, getter 빼기 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
JSP (25p)
│
├── [A] JSP = Servlet
│   ├── Jasper 컴파일 (.jsp -> .java -> .class)
│   ├── 첫 요청 시 변환 (느림)
│   └── 캐시된 .class 실행 (빠름)
│
├── [B] 내장 객체 9
│   ├── request / response / session / application
│   ├── out / pageContext
│   └── page / config / exception
│
├── [C] 스크립트 요소 (비권장)
│   ├── 선언 <%! %>
│   ├── 스크립틀릿 <% %>
│   └── 표현식 <%= %>
│
├── [D] EL (Expression Language)
│   ├── getter 자동 호출
│   ├── 4 scope (page/request/session/application)
│   ├── 파라미터·쿠키·헤더
│   └── 산술·비교·논리
│
├── [E] JSTL
│   ├── Core (c:if, c:forEach, c:choose, c:out)
│   ├── fmt (날짜·숫자 포맷)
│   └── XSS escape (c:out)
│
├── [F] 액션 태그
│   ├── jsp:include (동적)
│   ├── @include (정적)
│   ├── jsp:forward
│   └── jsp:useBean (옛)
│
└── [G] 운영
    ├── WEB-INF 보안
    ├── 한글 인코딩
    ├── 에러 페이지
    └── ViewResolver (Spring)
```

## 학습 진도 체크리스트

### A. 기초
- [ ] JSP 가 Servlet 으로 변환
- [ ] 9 내장 객체 + 역할
- [ ] page 디렉티브 옵션

### B. EL/JSTL
- [ ] EL 4 scope 검색 순서
- [ ] `c:forEach` 반복
- [ ] `c:choose/when/otherwise`
- [ ] `c:out` XSS escape
- [ ] fmt:formatDate

### C. 액션
- [ ] jsp:include vs @include 차이
- [ ] jsp:forward
- [ ] WEB-INF 보안 정책

### D. 디버깅
- [ ] `${...}` 안 풀리는 원인 3가지
- [ ] `<c:forEach>` 그대로 출력 → taglib
- [ ] XML escape (&lt;)

## 연관 강의

```
1강 Servlet        -> HTTP 요청 처리
2강 JSP            <- 현재 위치
2강 JSP 실습       -> 게시판 화면
3강 Cookie/Session -> 상태 유지
4강 EL/JSTL        -> JSP 깔끔하게 (심화)
Framework 5강 MVC1 -> Spring + JSP
```

→ 다음 (JSP 실습) 에서 **게시판 화면 작성**.
