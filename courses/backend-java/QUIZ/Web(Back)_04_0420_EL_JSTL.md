# EL & JSTL — 퀴즈

> 14문항. 개념·적용·디버그·면접.

---

### Q1. (개념) EL 이 JSP 의 스크립트 표현식(`<%= %>`) 을 대체할 때 얻는 이점 3가지?

<details><summary>정답</summary>

1. **가독성** - HTML 과 자바 코드 안 섞임
2. **null 안전** - `${user.address.city}` 가 NPE 없이 빈 문자열 반환
3. **자동 형변환** - `${param.age + 1}` 처럼 문자열 → 숫자 자동
4. **자동 scope 탐색** - 어느 scope 에 있는지 명시 불필요

</details>

### Q2. (개념) EL 의 4가지 scope 자동 탐색 순서?

<details><summary>정답</summary>

**page → request → session → application** 순. 같은 이름이 여러 scope 에 있으면 **좁은 scope 가 우선** (page 가 가장 먼저 매칭).

명시적으로 특정 scope 지정: `${requestScope.user}`, `${sessionScope.loginUser}`.

</details>

### Q3. (적용) `${user.name}` 이 실제로 호출하는 코드는?

<details><summary>정답</summary>

```java
user.getName()
```

JavaBeans property 표기 - EL 이 `getXxx()` 메서드를 자동 호출. boolean 인 경우 `isXxx()` 도 시도.

`user` 가 null 이면 NPE 안 나고 빈 문자열.

</details>

### Q4. (개념) EL 의 `empty` 가 true 반환하는 경우는?

<details><summary>정답</summary>

1. **null**
2. **빈 컬렉션** (`new ArrayList<>()`, 빈 Map)
3. **빈 문자열** (`""`)
4. **빈 배열** (`new int[0]`)

**숫자 0 은 empty 가 아님** (false). `${empty 0}` → false.

</details>

### Q5. (개념) JSTL 의 5가지 라이브러리 중 실무에서 자주 쓰는 3가지?

<details><summary>정답</summary>

| 라이브러리 | 접두사 | 용도 |
|--|--|--|
| **Core** | `c` | 변수·조건·반복·redirect (가장 자주!) |
| **Format** | `fmt` | 숫자·날짜·국제화 |
| **Functions** | `fn` | 문자열 함수 (length, contains, escapeXml) |

XML 과 SQL 은 거의 안 씀 (SQL 은 JSP 에서 직접 DB 호출이라 안티패턴).

</details>

### Q6. (적용) 게시글 목록을 `<c:forEach>` 로 출력하시오. 1-based 번호 표시.

<details><summary>정답</summary>

```jsp
<c:forEach var="b" items="${boards}" varStatus="s">
    <tr>
        <td>${s.count}</td>           <%-- 1-based --%>
        <td>${b.title}</td>
        <td>${b.writer}</td>
    </tr>
</c:forEach>
```

`varStatus.count` = 1-based, `varStatus.index` = 0-based, `.first`/`.last` 도 가능.

</details>

### Q7. (적용) 사용자 역할(`ADMIN`/`USER`/`GUEST`) 에 따라 다른 메시지 표시.

<details><summary>정답</summary>

```jsp
<c:choose>
    <c:when test="${user.role == 'ADMIN'}">
        <p>관리자 환영</p>
    </c:when>
    <c:when test="${user.role == 'USER'}">
        <p>회원 환영</p>
    </c:when>
    <c:otherwise>
        <p>방문자 환영</p>
    </c:otherwise>
</c:choose>
```

</details>

### Q8. (적용) 사용자 댓글을 안전하게 출력 (XSS 방어).

<details><summary>정답</summary>

```jsp
<%@ taglib prefix="fn" uri="jakarta.tags.functions" %>

<p>${fn:escapeXml(comment.content)}</p>
```

또는:
```jsp
<c:out value="${comment.content}" />   <%-- 기본 escape=true --%>
```

신뢰할 수 없는 사용자 입력을 그대로 출력하면 XSS 취약 (`<script>` 삽입 가능).

</details>

### Q9. (적용) 날짜를 "yyyy-MM-dd HH:mm" 포맷으로 출력.

<details><summary>정답</summary>

```jsp
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>

<fmt:formatDate value="${board.regDate}" pattern="yyyy-MM-dd HH:mm" />
```

`type="date"` / `dateStyle="full"` 옵션도 가능.

</details>

### Q10. (적용) URL 안전하게 만들기 — contextPath 포함.

<details><summary>정답</summary>

```jsp
<a href="<c:url value='/board/${board.id}' />">상세</a>
```

`<c:url>` 이 자동으로:
- contextPath 앞에 붙임 (`/myapp/board/42`)
- 파라미터 URL 인코딩
- 세션 추적 URL rewrite (쿠키 비활성 시)

직접 `/board/${id}` 쓰면 contextPath 누락 + URL 인코딩 X.

</details>

### Q11. (디버그) `${user.name}` 이 화면에 그대로 출력됨. 원인?

<details><summary>정답</summary>

1. **EL 비활성** - 옛 JSP 버전 또는 페이지 설정:
   ```jsp
   <%@ page isELIgnored="false" %>
   ```

2. **JSP 페이지가 옛 web.xml 의 `<el-ignored>true</el-ignored>` 영향**:
   ```xml
   <jsp-property-group>
       <el-ignored>false</el-ignored>
   </jsp-property-group>
   ```

3. **JSTL 라이브러리 의존성 누락** (`<c:`/`<fmt:` 류만 해당, EL `${}` 는 무관)

</details>

### Q12. (디버그) `<c:forEach>` 가 그대로 출력. JSP 첫 줄에 `<%@ taglib ... %>` 도 있는데?

<details><summary>정답</summary>

**JSTL 의존성 누락**. taglib 디렉티브는 선언만 하는 것 — 실제 구현은 jar 가 있어야.

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

API + Implementation 둘 다 필요.

</details>

### Q13. (면접) "EL/JSTL 을 쓰면 JSP 안에 자바 코드가 없어지는데, 그게 왜 좋은가요?"

<details><summary>정답</summary>

1. **MVC 분리** - JSP 는 view 만, 자바 로직은 Servlet/Service. 책임 명확.
2. **디자이너·퍼블리셔 협업** - HTML/CSS 위주라 비개발자도 작업 가능. 스크립틀릿이 있으면 못 만짐.
3. **컴파일 에러 줄어듦** - 자바 코드는 컴파일 에러로 깨질 수 있지만 태그는 잘못해도 격리.
4. **재사용·테스트** - JSP 가 단순해져 다른 JSP 와 include 결합 쉬움.
5. **자동 XSS 방어** - `<c:out>` / `fn:escapeXml` 같이 안전한 출력 표준화.
6. **null 안전** - `${user.address.city}` 가 NPE 없이 빈 문자열.

스크립틀릿은 모던 JSP 에선 **거의 금지 수준**.

</details>

### Q14. (면접) "EL/JSTL 과 Thymeleaf 의 사상적 공통점은?"

<details><summary>정답</summary>

**선언적 표기**. 둘 다:
- 자바 코드를 view 에서 추방
- 데이터 접근은 표현식 (`${}` / `[[${}]]`)
- 제어 흐름은 태그·속성 (`<c:forEach>` / `th:each`)
- null 안전
- XSS 자동 방어

차이는 **HTML 유효성**:
- JSP/JSTL: HTML 안 `<c:forEach>` 같은 비표준 태그 → 브라우저가 무시
- Thymeleaf: HTML 표준 속성 (`th:each="b : ${boards}"`) → IDE·디자이너가 HTML 그대로 미리보기 가능

Spring Boot 의 권장은 Thymeleaf 지만 한국 SI 는 여전히 JSP+JSTL 표준.

</details>
