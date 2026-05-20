# EL & JSTL — 스크립틀릿과 작별

> **이 강의는 무엇인가**: JSP 안에 자바 코드(`<% %>`) 가 섞이면 가독성·보안·재사용 모두 망가진다. 이를 풀어주는 두 도구: **EL (Expression Language)** - 값 접근 표현식, **JSTL (JSP Standard Tag Library)** - 제어 흐름·포맷·국제화 태그.
> **왜 배우는가**: 모던 JSP 의 표준 사용 패턴. Thymeleaf 와도 사상은 같음 (선언적 표기). 면접에서 `${}` `<c:forEach>` 못 쓰면 모던 JSP 개발 못 함.

---

## 들어가기 전에

- **선수**: JSP 강의 (스크립팅 요소·기본 객체 영역), Cookie/Session (Scope 의 이해).
- **마인드셋**: "JSP 는 view, 자바는 controller/service" 의 명확한 분리. 자바 코드를 JSP 에서 추방.

---

# Part A. EL (Expression Language)

## 1. EL 의 정의·목적

```jsp
<%-- ❌ 스크립틀릿 + 표현식 - 가독성 ↓ --%>
<%
    User user = (User) request.getAttribute("user");
%>
<h1>안녕하세요, <%= user.getName() %>님</h1>
<p>나이: <%= user.getAge() %></p>

<%-- ✅ EL - 깔끔 --%>
<h1>안녕하세요, ${user.name}님</h1>
<p>나이: ${user.age}</p>
```

**EL 의 본질**:
- JSP 안 데이터를 다루는 **표현식 전용 미니 언어**
- 4가지 Scope 자동 탐색
- 자동 형변환 + null 안전
- `${...}` (즉시) 와 `#{...}` (지연 - 거의 안 씀)

## 2. EL 구문 4가지

```jsp
${expr}                        <%-- 즉시 평가 (대부분 사용) --%>
#{expr}                        <%-- 지연 평가 (JSF 외 잘 안 씀) --%>

${user.name}                   <%-- property 접근: user.getName() --%>
${user["name"]}                <%-- 동일 (key 표기) --%>
${list[0]}                     <%-- 인덱스 --%>
${map["key"]}                  <%-- Map 접근 --%>
${user.address.city}           <%-- 중첩 - user.getAddress().getCity() --%>

${a + b}                       <%-- 산술 --%>
${a > 0 ? "양수" : "음수"}      <%-- 삼항 --%>
${not empty list}              <%-- 빈 체크 (가장 자주!) --%>
${list.size()}                 <%-- 메서드 호출 (EL 3.0+) --%>
```

## 3. EL 내장 객체 (Implicit Objects)

```jsp
${param.id}                    <%-- request.getParameter("id") --%>
${paramValues.hobbies}         <%-- request.getParameterValues("hobbies") --%>

${header["User-Agent"]}        <%-- request.getHeader("User-Agent") --%>
${cookie.theme.value}          <%-- 쿠키 "theme" 의 값 --%>

${pageScope.x}                 <%-- pageContext.getAttribute(x, PAGE_SCOPE) --%>
${requestScope.x}              <%-- request.getAttribute("x") --%>
${sessionScope.x}              <%-- session.getAttribute("x") --%>
${applicationScope.x}          <%-- application.getAttribute("x") --%>

${pageContext.request.requestURI}     <%-- 풀 객체 접근 --%>
${pageContext.session.id}             <%-- JSESSIONID --%>
${initParam.dbUrl}             <%-- web.xml 의 context-param --%>
```

## 4. EL 의 자동 Scope 탐색

```jsp
${user}     <%-- page → request → session → application 순으로 탐색 --%>
```

**모호성 피하기**: 명시적 scope 사용.
```jsp
${requestScope.user}     <%-- request 만 찾음 --%>
${sessionScope.user}     <%-- session 만 --%>
```

같은 이름이 여러 scope 에 있으면 좁은 scope 가 우선.

## 5. EL 의 안전성

```jsp
<%-- null 안전 - NullPointerException 안 남 --%>
${user.address.city}            <%-- user 가 null 이면 그냥 빈 문자열 --%>

<%-- 빈 체크 --%>
${empty list}                   <%-- list 가 null 또는 size 0 → true --%>
${not empty list}               <%-- 비어있지 않으면 true --%>

<%-- 자동 형변환 --%>
${param.age + 1}                <%-- "25" → 25 + 1 = 26 --%>
```

스크립틀릿의 `(User) request.getAttribute("user").getAddress().getCity()` 같은 NPE 위험 코드를 EL 이 안전하게 처리.

---

# Part B. JSTL (JSP Standard Tag Library)

## 6. JSTL 의 정의·필요성

```jsp
<%-- ❌ 스크립틀릿 - 조건/반복 처리 --%>
<%
    if (boards != null && !boards.isEmpty()) {
        for (Board b : boards) {
%>
            <tr><td><%= b.getId() %></td><td><%= b.getTitle() %></td></tr>
<%
        }
    }
%>

<%-- ✅ JSTL - 깔끔 --%>
<c:if test="${not empty boards}">
    <c:forEach var="b" items="${boards}">
        <tr><td>${b.id}</td><td>${b.title}</td></tr>
    </c:forEach>
</c:if>
```

## 7. JSTL 라이브러리 5종

| 라이브러리 | 접두사 | 용도 |
|--|--|--|
| **Core** | `c` | 변수·조건·반복·redirect (가장 자주!) |
| **Format** | `fmt` | 숫자·날짜·메시지·국제화 |
| **Functions** | `fn` | 문자열 함수 (`fn:length`, `fn:contains`) |
| **XML** | `x` | XML 파싱·변환 (잘 안 씀) |
| **SQL** | `sql` | DB 쿼리 (안티패턴 - 안 씀) |

실무는 거의 **Core + Format + Functions**.

## 8. JSTL 의존성 + 선언

```xml
<!-- pom.xml (Spring Boot) -->
<dependency>
    <groupId>jakarta.servlet.jsp.jstl</groupId>
    <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
</dependency>
<dependency>
    <groupId>org.glassfish.web</groupId>
    <artifactId>jakarta.servlet.jsp.jstl</artifactId>
</dependency>
```

```jsp
<%-- JSP 첫 줄 - taglib 디렉티브 --%>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<%@ taglib prefix="fn"  uri="jakarta.tags.functions" %>
```

## 9. Core 태그 - 가장 자주 쓰는 7가지

```jsp
<%-- 1) <c:set> - 변수 설정 --%>
<c:set var="totalPrice" value="${price * quantity}" />

<%-- 2) <c:if> - 조건 (else 없음) --%>
<c:if test="${user.role == 'ADMIN'}">
    <a href="/admin">관리자 페이지</a>
</c:if>

<%-- 3) <c:choose> + <c:when> + <c:otherwise> - if-else --%>
<c:choose>
    <c:when test="${user.role == 'ADMIN'}">관리자</c:when>
    <c:when test="${user.role == 'WRITER'}">작성자</c:when>
    <c:otherwise>일반 회원</c:otherwise>
</c:choose>

<%-- 4) <c:forEach> - 반복 (List, Array) --%>
<c:forEach var="b" items="${boards}" varStatus="status">
    <tr>
        <td>${status.index + 1}</td>       <%-- 0-indexed --%>
        <td>${status.count}</td>            <%-- 1-indexed --%>
        <td>${b.title}</td>
        <td>${status.first ? '첫번째' : ''}</td>
        <td>${status.last ? '마지막' : ''}</td>
    </tr>
</c:forEach>

<%-- 5) <c:forEach> - 숫자 범위 --%>
<c:forEach var="i" begin="1" end="10" step="1">
    <li>${i}</li>
</c:forEach>

<%-- 6) <c:url> - URL 안전하게 생성 --%>
<a href="<c:url value='/board/${board.id}' />">상세</a>
<%-- contextPath + URL 인코딩 자동 --%>

<%-- 7) <c:redirect> - 클라이언트 redirect --%>
<c:if test="${empty sessionScope.loginUser}">
    <c:redirect url="/login" />
</c:if>
```

## 10. Format 태그 - 숫자·날짜 포맷

```jsp
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>

<%-- 숫자 --%>
<fmt:formatNumber value="${price}" type="currency" />            <%-- ₩1,234 --%>
<fmt:formatNumber value="${rate}"  type="percent"  />            <%-- 35% --%>
<fmt:formatNumber value="${num}"   pattern="#,###" />            <%-- 1,234,567 --%>

<%-- 날짜 --%>
<fmt:formatDate value="${board.regDate}" pattern="yyyy-MM-dd HH:mm" />
<fmt:formatDate value="${date}"          dateStyle="full" />     <%-- 2025년 5월 19일 월요일 --%>

<%-- 국제화 (i18n) --%>
<fmt:setLocale value="${pageContext.request.locale}" />
<fmt:setBundle basename="messages" />
<fmt:message key="welcome.title" />
```

## 11. Functions 태그 - 문자열 함수

```jsp
<%@ taglib prefix="fn" uri="jakarta.tags.functions" %>

${fn:length(boards)}                                  <%-- 컬렉션 크기 --%>
${fn:toUpperCase(title)}                              <%-- 대문자 --%>
${fn:toLowerCase(title)}                              <%-- 소문자 --%>
${fn:trim(input)}                                     <%-- 양끝 공백 제거 --%>
${fn:contains(content, "스프링")}                      <%-- 포함 --%>
${fn:startsWith(path, "/admin")}                      <%-- 시작 --%>
${fn:replace(text, "old", "new")}                     <%-- 치환 --%>
${fn:split(csv, ",")}                                 <%-- 분리 → 배열 --%>
${fn:join(arr, " ")}                                  <%-- 결합 --%>
${fn:escapeXml(userInput)}                            <%-- XSS 방어! --%>
```

**XSS 방어**: 사용자 입력을 HTML 출력할 땐 항상 `fn:escapeXml`:
```jsp
<p>${fn:escapeXml(comment.content)}</p>
```

또는 `<c:out value="${...}" />` (기본 escape).

---

## 12. 코드 깊게 - EL + JSTL 풀스택 게시판

```jsp
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<%@ taglib prefix="fn"  uri="jakarta.tags.functions" %>

<%-- 로그인 가드 --%>
<c:if test="${empty sessionScope.loginUser}">
    <c:redirect url="/login" />
</c:if>

<!DOCTYPE html>
<html>
<head>
    <title>게시판 (${fn:length(boards)}건)</title>
</head>
<body>

<h1>안녕하세요, ${sessionScope.loginUser.name}님</h1>

<%-- 검색 결과 메시지 --%>
<c:if test="${not empty param.keyword}">
    <p>"${fn:escapeXml(param.keyword)}" 검색 결과: ${fn:length(boards)}건</p>
</c:if>

<%-- 빈 결과 처리 --%>
<c:choose>
    <c:when test="${empty boards}">
        <p>게시글이 없습니다.</p>
    </c:when>
    <c:otherwise>
        <table>
            <tr>
                <th>#</th><th>제목</th><th>작성자</th><th>등록일</th>
            </tr>
            <c:forEach var="b" items="${boards}" varStatus="s">
                <tr>
                    <td>${s.count}</td>
                    <td>
                        <a href="<c:url value='/board/${b.id}' />">
                            ${fn:escapeXml(b.title)}
                        </a>
                        <c:if test="${b.commentCount > 0}">
                            <span>[${b.commentCount}]</span>
                        </c:if>
                    </td>
                    <td>${b.writer}</td>
                    <td>
                        <fmt:formatDate value="${b.regDate}" pattern="yyyy-MM-dd HH:mm" />
                    </td>
                </tr>
            </c:forEach>
        </table>
    </c:otherwise>
</c:choose>

<%-- 페이지네이션 --%>
<nav>
    <c:forEach var="i" begin="1" end="${totalPages}">
        <c:choose>
            <c:when test="${i == currentPage}">
                <strong>${i}</strong>
            </c:when>
            <c:otherwise>
                <a href="<c:url value='/board?page=${i}' />">${i}</a>
            </c:otherwise>
        </c:choose>
    </c:forEach>
</nav>

<%-- 관리자 전용 --%>
<c:if test="${sessionScope.loginUser.role == 'ADMIN'}">
    <a href="<c:url value='/admin' />">관리자 페이지</a>
</c:if>

</body>
</html>
```

스크립틀릿 (`<% %>`) 0줄. 자바 코드 1줄도 없음.

---

## 13. 실전 패턴 / 자주 빠지는 함정

### EL
- ❌ `${user.getName()}` ✅ `${user.name}` (property 접근 - getter 자동 호출)
- ❌ `${requestScope.user.address.city}` 가 NPE ✅ EL 은 null 안전, 빈 문자열 반환
- ❌ `${empty 0}` 가 false 라고 생각 ✅ EL 의 `empty` 는 null, 빈 컬렉션, 빈 문자열에만 true (0 은 false)
- ❌ `${"hello world".length()}` 동작 안 함 ✅ EL 3.0+ 만 메서드 호출, 그 전엔 `${fn:length(...)}`

### JSTL
- ❌ `<c:if test="${user != null && user.role == 'ADMIN'}">` ✅ `${not empty user and user.role == 'ADMIN'}` (EL 은 `and`/`or`/`not`)
- ❌ `<c:choose>` 안에 `<c:when>` 만 있고 `<c:otherwise>` 없음 ✅ default 처리 명시
- ❌ `<c:forEach>` 안에서 `varStatus` 안 쓰고 index 직접 카운트 ✅ `varStatus.index` (0-based) / `.count` (1-based)
- ❌ URL 직접 만들 때 `/board/${id}` ✅ `<c:url value='/board/${id}' />` (contextPath 자동)

### XSS 방어
- ❌ `${comment.content}` 그대로 ✅ `${fn:escapeXml(comment.content)}` 또는 `<c:out value="${comment.content}" />`
- ❌ 신뢰할 수 없는 데이터(사용자 입력)를 HTML 에 직접 ✅ 항상 escape

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| `${user.name}` 가 그대로 출력 | EL 비활성 또는 JSP 옛 버전 | `<%@ page isELIgnored="false" %>` |
| `<c:forEach>` 가 그대로 출력 | taglib 누락 또는 JSTL 의존성 없음 | `<%@ taglib %>` + pom.xml |
| `${board.title}` 가 빈 값 | scope 에 없음 또는 getter 없음 | `requestScope.board` 확인 + getter |
| `${empty list}` 가 항상 false (실제론 빈 list) | List 가 null 이 아니라 빈 `new ArrayList<>()` 인 경우는 OK; 다른 이유 가능성 | size 확인 |
| 한글이 ?로 출력 | 페이지 인코딩 | `<%@ page pageEncoding="UTF-8" contentType="text/html;charset=UTF-8" %>` |
| XSS 공격 가능 | escape 안 함 | `fn:escapeXml` 또는 `<c:out>` |

---

## 14. 자가점검

1. EL 이 풀어주는 본질적 문제 (스크립틀릿 대비)?
2. EL 의 4가지 scope 자동 탐색 순서?
3. `${user.name}` 이 실제로 호출하는 메서드는?
4. JSTL 의 5가지 라이브러리 중 실무에서 자주 쓰는 것은?
5. XSS 방어를 위한 EL/JSTL 표현 2가지?
6. `<c:if>` 와 `<c:choose>` 의 차이?
7. EL 의 `empty` 가 true 인 경우 3가지?

<details><summary>풀이</summary>

1. **JSP 안의 자바 코드를 추방**. 스크립틀릿(`<% %>`) 없이 데이터 접근·표현 가능 → 가독성·디자이너 협업·NPE 안전·XSS 자동 방어.
2. **page → request → session → application** 순. 같은 이름이 여러 scope 에 있으면 좁은 scope 가 우선.
3. **`user.getName()`** - JavaBeans property 표기. EL 이 `getXxx()` 자동 호출 (boolean 은 `isXxx()` 도).
4. **Core(c)**, **Format(fmt)**, **Functions(fn)**. XML 과 SQL 은 거의 안 씀.
5. (a) `${fn:escapeXml(input)}` (b) `<c:out value="${input}" />`. 사용자 입력을 HTML 에 출력할 땐 항상.
6. **`<c:if>`**: 단순 조건, else 없음. **`<c:choose>` + `<c:when>` + `<c:otherwise>`**: if-else-elseif 다중 분기.
7. (a) null (b) 빈 컬렉션 `[]` 또는 빈 Map `{}` (c) 빈 문자열 `""`. **숫자 0 은 empty 아님**.

</details>

---

## 15. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.10 EL (구문·내장객체·scope 탐색·안전성) | §1 ~ §5 (Part A) |
| p.11 ~ p.15 JSTL (Core·Format·Functions) | §6 ~ §11 (Part B) |
| p.16 마무리 | (생략) |

_16p 슬라이드 모두 커버._
