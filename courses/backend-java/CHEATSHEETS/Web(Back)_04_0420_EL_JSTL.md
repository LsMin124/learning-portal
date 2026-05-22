# EL · JSTL — 치트시트

> 16p 슬라이드 · JSP 의 자바 코드 제거 도구.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **EL** = `${...}` JSP 표현. 자바 코드 없이 값·연산
2. **EL 4 scope 검색**: page → request → session → application
3. **`empty` 연산자** = null 또는 size 0 (가장 자주 씀)
4. **JSTL Core**: `c:if` / `c:choose` / `c:forEach` / `c:set` / `c:out` (XSS escape)
5. **JSTL fmt**: 날짜·숫자 포맷 (`fmt:formatDate`, `fmt:formatNumber`)
6. **`<c:out value="${userInput}"/>` 로 XSS 자동 방어** (직접 `${}` 는 위험할 수 있음)

## 가장 중요한 코드 3개

```jsp
<%-- (1) 표준 헤더 + 기본 패턴 --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c"   uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>

<c:if test="${not empty boards}">
  <c:forEach var="b" items="${boards}" varStatus="s">
    <p>${s.index + 1}. <c:out value="${b.title}"/>
       (<fmt:formatDate value="${b.createdAt}" pattern="yyyy-MM-dd"/>)</p>
  </c:forEach>
</c:if>
```

```jsp
<%-- (2) 조건 분기 --%>
<c:choose>
  <c:when test="${user.role == 'ADMIN'}">관리자 메뉴</c:when>
  <c:when test="${user.role == 'USER'}">일반 메뉴</c:when>
  <c:otherwise>로그인 필요</c:otherwise>
</c:choose>
```

```jsp
<%-- (3) URL + 파라미터 + 페이지네이션 --%>
<c:forEach var="i" begin="1" end="${totalPages}">
  <c:url var="pageUrl" value="/board">
    <c:param name="page" value="${i}"/>
    <c:param name="keyword" value="${param.keyword}"/>
  </c:url>
  <a href="${pageUrl}">${i}</a>
</c:forEach>
```

## 면접 한 줄 답변
- **EL 의 이점?** → 자바 코드 제거 + getter 자동 호출 + null 안전 (`${user.name}` 이 null 이어도 에러 X, 빈 출력).
- **`${user.name}` 이 호출하는 것?** → `user.getName()` 자동 호출 (JavaBean 규약).
- **`c:out` 을 쓰는 이유?** → XSS 자동 escape. 사용자 입력을 `${}` 직접 사용은 위험.
- **`empty` 연산자?** → null 또는 컬렉션 size 0. 가장 자주 쓰는 조건.

---

# 2. Quick Reference (실무 복붙)

## EL 기본 문법

```jsp
${board.title}                    <%-- getter (board.getTitle()) --%>
${board['title']}                 <%-- 동일, 동적 키 가능 --%>
${list[0]}                        <%-- 배열·리스트 인덱스 --%>
${map['key']}                     <%-- 맵 --%>
${user.address.city}              <%-- 중첩 (NPE 안전) --%>
```

## EL 연산자

```jsp
<%-- 산술 --%>
${1 + 2}  ${a - b}  ${a * b}  ${a / b}  ${a % b}

<%-- 비교 --%>
${a == b}  ${a != b}  ${a < b}  ${a > b}  ${a <= b}  ${a >= b}
${a eq b}  ${a ne b}  ${a lt b}  ${a gt b}  ${a le b}  ${a ge b}

<%-- 논리 --%>
${a && b}  ${a || b}  ${!a}
${a and b}  ${a or b}  ${not a}

<%-- 비어있음 --%>
${empty list}                     <%-- null, "", size 0 --%>
${not empty user}

<%-- 삼항 --%>
${user != null ? user.name : '익명'}
```

## EL 내장 객체

```jsp
${param.id}                       <%-- request.getParameter("id") --%>
${paramValues.tags}               <%-- String[] --%>
${header['User-Agent']}           <%-- 헤더 --%>
${cookie.JSESSIONID.value}        <%-- 쿠키 --%>
${initParam.appName}              <%-- web.xml context-param --%>

<%-- 4 scope --%>
${pageScope.x}
${requestScope.user}
${sessionScope.loginUser}
${applicationScope.config}

<%-- pageContext (모든 scope + 메타) --%>
${pageContext.request.contextPath}    <%-- /myapp --%>
${pageContext.request.method}         <%-- GET / POST --%>
${pageContext.session.id}             <%-- JSESSIONID --%>
```

## JSTL Core (`<c:>`)

```jsp
<%-- 변수 --%>
<c:set var="x" value="10" scope="request"/>
<c:remove var="x"/>

<%-- 조건 --%>
<c:if test="${empty list}">
  결과 없음
</c:if>

<c:choose>
  <c:when test="${user.role == 'ADMIN'}">관리자</c:when>
  <c:when test="${user.role == 'USER'}">일반</c:when>
  <c:otherwise>익명</c:otherwise>
</c:choose>

<%-- 반복 --%>
<c:forEach var="b" items="${boards}" varStatus="status">
  ${status.index}     <%-- 0-base --%>
  ${status.count}     <%-- 1-base --%>
  ${status.first}     <%-- 첫 행? --%>
  ${status.last}      <%-- 마지막? --%>
  ${b.title}
</c:forEach>

<c:forEach var="i" begin="1" end="10" step="2">
  ${i}
</c:forEach>

<%-- URL + 파라미터 --%>
<c:url var="link" value="/board/detail">
  <c:param name="id" value="${b.id}"/>
</c:url>
<a href="${link}">상세</a>

<%-- 출력 (XSS escape) --%>
<c:out value="${userInput}" default="(없음)"/>

<%-- 리다이렉트 --%>
<c:redirect url="/login"/>

<%-- 예외 처리 --%>
<c:catch var="err">
  ...
</c:catch>
<c:if test="${err != null}">에러: ${err.message}</c:if>
```

## JSTL fmt (`<fmt:>`)

```jsp
<%-- 날짜 --%>
<fmt:formatDate value="${board.createdAt}" pattern="yyyy-MM-dd HH:mm"/>
<fmt:formatDate value="${board.createdAt}" type="date" dateStyle="long"/>
<fmt:parseDate value="2026-05-20" var="parsed" pattern="yyyy-MM-dd"/>

<%-- 숫자 --%>
<fmt:formatNumber value="${price}" pattern="#,###"/>            <%-- 1,234 --%>
<fmt:formatNumber value="${rate}" type="percent"/>              <%-- 12% --%>
<fmt:formatNumber value="${amount}" type="currency"/>           <%-- 통화 --%>

<%-- 국제화 --%>
<fmt:setLocale value="ko_KR"/>
<fmt:setBundle basename="messages"/>
<fmt:message key="welcome"/>
```

## JSTL Functions (`<fn:>`)

```jsp
<%@ taglib prefix="fn" uri="jakarta.tags.functions" %>

${fn:length(list)}                      <%-- 크기 --%>
${fn:toUpperCase(name)}
${fn:toLowerCase(name)}
${fn:substring(text, 0, 10)}
${fn:contains(text, 'keyword')}
${fn:startsWith(text, 'http')}
${fn:replace(text, ' ', '_')}
${fn:trim(text)}
${fn:split(csv, ',')}
${fn:join(arr, '|')}
${fn:escapeXml(userInput)}              <%-- c:out 과 동일 --%>
```

## 4 Scope 검색 순서

```
${user}  검색 순서:
  1. pageScope
  2. requestScope
  3. sessionScope
  4. applicationScope
  -> 좁은 곳에서 먼저 찾음
```

```jsp
<%-- 명시적 scope --%>
${requestScope.user}              <%-- request 에서만 --%>
${sessionScope.loginUser}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `${user}` 안 풀림 | EL 비활성 / setAttribute 누락 / getter 없음 |
| `<c:forEach>` 그대로 출력 | taglib 선언 + JSTL 의존성 |
| `${userInput}` XSS 위험 | `c:out` 또는 `fn:escapeXml` |
| `<` 깨짐 | `&lt;` 또는 CDATA |
| `<c:if test="${not empty list}">` 두 번 평가 | `<c:set var="hasList" value="${not empty list}"/>` 캐싱 |
| 날짜 형식 안 됨 | `<fmt:formatDate>` 사용 |
| URL 한글 깨짐 | `<c:url>` + `<c:param>` |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
EL · JSTL (16p)
│
├── [A] EL 기본
│   ├── ${expression}
│   ├── . 와 [] 접근
│   ├── getter 자동 호출
│   └── NPE 안전 (null -> "")
│
├── [B] EL 연산
│   ├── 산술 / 비교 / 논리
│   ├── empty / not empty
│   └── 삼항
│
├── [C] EL 내장 객체
│   ├── param / paramValues
│   ├── header / cookie
│   ├── initParam
│   ├── 4 scope (page/request/session/application)
│   └── pageContext
│
├── [D] JSTL Core (c:)
│   ├── set / remove
│   ├── if / choose / when / otherwise
│   ├── forEach (items, begin-end)
│   ├── url / param
│   ├── out (XSS escape)
│   ├── redirect
│   └── catch
│
├── [E] JSTL fmt
│   ├── formatDate / parseDate
│   ├── formatNumber / parseNumber
│   ├── setLocale / setBundle / message
│   └── i18n
│
└── [F] JSTL fn
    ├── length / contains / startsWith
    ├── toUpperCase / substring / replace
    ├── split / join
    └── escapeXml
```

## 학습 진도 체크리스트

### A. EL
- [ ] `${obj.field}` getter 호출 원리
- [ ] 4 scope 검색 순서
- [ ] `empty` / `not empty` 연산자
- [ ] 내장 객체 (param, cookie, pageContext)

### B. JSTL Core
- [ ] c:if / c:choose 차이
- [ ] c:forEach + varStatus
- [ ] c:url + c:param (페이지네이션 링크)
- [ ] c:out 의 XSS 방어

### C. JSTL fmt
- [ ] formatDate 패턴
- [ ] formatNumber (currency, percent)
- [ ] i18n (setLocale + message)

### D. JSTL fn
- [ ] length / contains
- [ ] escapeXml (c:out 대체)

## 연관 강의

```
2강 JSP             -> EL/JSTL 의 기반
3강 Cookie/Session  -> ${sessionScope.user}
4강 EL/JSTL         <- 현재 위치
5강 Filter          -> EL 동작 보장 (인코딩)
Framework 5강 MVC1  -> Spring + JSP + EL/JSTL
```

→ 다음 (Filter) 에서 **공통 처리 분리 (인코딩·인증·로깅)**.
