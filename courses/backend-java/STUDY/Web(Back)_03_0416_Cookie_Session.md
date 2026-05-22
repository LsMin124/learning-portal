# Cookie & Session — HTTP · Cookie · JSP 기본객체 영역 · Session

> **이 강의는 무엇인가**: HTTP 의 무상태(stateless) 한계 위에 "이 요청이 누구의 것인가" 를 식별하는 두 메커니즘 - **쿠키 (클라이언트 저장)** 와 **세션 (서버 저장)**. 그리고 JSP 의 4가지 기본객체 영역 (Scope) 의 차이.
> **왜 배우는가**: 로그인·장바구니·자동 로그인·CSRF 토큰 - 모두 쿠키/세션 위에 만들어짐. Spring Security 도 본질은 세션 (또는 토큰) 기반. 원리 모르면 디버깅 막힘.

---

## 들어가기 전에

- **선수**: Servlet 강의 (request/response), JSP 강의 (스크립팅 요소·기본 객체).
- **마인드셋**: "HTTP 는 본래 상태가 없다. 상태가 필요한 모든 기능은 추가 메커니즘이다" 라는 본질 의식.

---

# Part A. HTTP

## 1. HTTP 의 핵심 특징

```
HTTP (Hyper Text Transfer Protocol)
  · 무상태 (Stateless)         - 서버가 클라 상태 안 기억
  · 단방향 (Request/Response)  - 클라가 시작, 서버가 응답
  · 비연결성 (Connectionless)  - 응답 후 연결 끊김 (HTTP/1.1+ keep-alive 로 완화)
  · 텍스트 기반                - 사람도 읽을 수 있음
```

**무상태가 만드는 문제**:
- 로그인 후 다음 요청 시 누군지 어떻게 알아? - 매번 ID/비밀번호 보낼 수 없음
- 장바구니에 담은 상품을 다음 페이지에서 어떻게 유지?
- 페이지 N 의 검색 조건을 페이지 N+1 에서 유지?

→ **쿠키·세션** 같은 보조 메커니즘 필요.

## 2. HTTP 요청·응답 구조

```
[요청 - Request]                       [응답 - Response]

GET /board?id=42 HTTP/1.1              HTTP/1.1 200 OK
Host: example.com                      Content-Type: text/html;charset=UTF-8
Accept: text/html                      Content-Length: 1234
Cookie: JSESSIONID=ABC123              Set-Cookie: theme=dark; Max-Age=86400
User-Agent: Mozilla/5.0...

(빈 줄)                                  (빈 줄)
                                       <html>...</html>
```

| 부분 | 의미 |
|--|--|
| 시작줄 | 메서드·URL·버전 / 버전·상태코드·이유 |
| 헤더 | 메타데이터 (Cookie, Accept, Authorization 등) |
| 빈 줄 | 헤더와 본문 구분 |
| 본문 | 데이터 (POST body, 응답 HTML 등) |

## 3. 주요 HTTP 메서드

| 메서드 | 의미 | 멱등 | 본문 |
|--|--|--|--|
| GET | 조회 | ✓ | ✗ (쿼리스트링) |
| POST | 생성·작업 | ✗ | ✓ |
| PUT | 전체 교체 | ✓ | ✓ |
| PATCH | 부분 수정 | ✗ | ✓ |
| DELETE | 삭제 | ✓ | ✗ |
| HEAD | 헤더만 | ✓ | ✗ |
| OPTIONS | 허용 메서드 | ✓ | ✗ |

## 4. 주요 HTTP 상태 코드

| 코드 | 의미 |
|--|--|
| 200 OK | 성공 |
| 201 Created | 생성됨 (POST 후 + Location 헤더) |
| 204 No Content | 성공·본문 없음 (DELETE 후) |
| 301 Moved Permanently | 영구 이동 |
| 302 Found | 임시 이동 (redirect) |
| 304 Not Modified | 캐시 활용 |
| 400 Bad Request | 클라 입력 오류 |
| 401 Unauthorized | 인증 안 됨 |
| 403 Forbidden | 권한 없음 |
| 404 Not Found | 자원 없음 |
| 500 Internal Server Error | 서버 오류 |
| 503 Service Unavailable | 서비스 일시 불가 |

---

# Part B. Cookie

## 5. 쿠키의 정체

```
[클라이언트]                        [서버]
    |
    |  ① POST /login (id, pwd)
    +------------------------------>
    |
    |  ② 응답: Set-Cookie: JSESSIONID=ABC; ...
    |          Set-Cookie: theme=dark; Max-Age=86400
    | <------------------------------
    |
    |  (브라우저가 쿠키 저장)
    |
    |  ③ GET /mypage
    |    Cookie: JSESSIONID=ABC; theme=dark   ← 자동 동봉
    +------------------------------>
    |
    |  ④ 서버가 Cookie 헤더 보고 사용자 식별
    | <------------------------------
```

**쿠키의 본질**: **서버가 클라이언트에 저장하라고 보낸 작은 문자열 데이터**. 브라우저가 자동으로:
- 받으면 저장
- 같은 도메인으로 요청 시 자동 동봉

## 6. 쿠키의 사용 목적

| 용도 | 예 |
|--|--|
| **세션 관리** | 로그인 상태(JSESSIONID), 장바구니 |
| **개인화** | 다크모드, 언어 설정 |
| **추적·분석** | 방문 패턴, 마지막 접속 시각 |
| **광고 타겟팅** | 관심사 기반 (privacy 이슈) |

## 7. Servlet 에서 쿠키 굽기

```java
@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // ... 인증 ...

        // 쿠키 생성
        Cookie c = new Cookie("user_pref_theme", "dark");
        c.setMaxAge(60 * 60 * 24 * 7);   // 7일 (초)
        c.setPath("/");                   // 모든 경로에서 전송
        c.setHttpOnly(true);              // JS 접근 차단 (XSS 방어)
        c.setSecure(true);                // HTTPS 에서만 (운영 환경)

        res.addCookie(c);
        res.sendRedirect("/");
    }
}
```

**쿠키의 주요 속성**:

| 속성 | 의미 |
|--|--|
| `name` / `value` | 키-값 |
| `Max-Age` | 만료 (초). 양수=유지, 0=즉시 삭제, 음수=세션 쿠키 |
| `Expires` | 만료 일시 (Max-Age 와 택일) |
| `Path` | 어떤 경로에서 전송 (`/` = 전부) |
| `Domain` | 어떤 도메인에서 전송 |
| `HttpOnly` | JS 접근 차단 (XSS 방어) |
| `Secure` | HTTPS 에서만 전송 |
| `SameSite` | Strict/Lax/None - CSRF 방어 |

## 8. Servlet 에서 쿠키 읽기

```java
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse res) {
    Cookie[] cookies = req.getCookies();
    if (cookies == null) return;   // 쿠키 하나도 없음

    String theme = "light";   // 기본값
    for (Cookie c : cookies) {
        if ("user_pref_theme".equals(c.getName())) {
            theme = c.getValue();
            break;
        }
    }
    req.setAttribute("theme", theme);
}
```

JSP 에선 `@CookieValue` 또는 `${cookie.user_pref_theme.value}` 로 간단히.

## 9. 쿠키의 한계 - 왜 세션이 필요한가

| 문제 | 영향 |
|--|--|
| **클라이언트 저장** | 사용자가 임의로 수정 가능 |
| **HTTP 헤더 전송** | 매 요청마다 전송 → 크기 제한 (~4KB) |
| **평문** | HTTPS 안 쓰면 노출 |
| **민감 정보 부적합** | 비밀번호·신용카드 절대 X |

→ 민감한 데이터는 **서버에 저장 (세션)** + **쿠키로는 세션 ID 만 주고받기**.

---

# Part C. JSP 기본 객체 영역 (Scope)

## 10. 4가지 Scope

```
[좁은 범위 ← → 넓은 범위]

page  <  request  <  session  <  application

· page         - 현재 JSP 페이지 안에서만
· request      - 한 요청-응답 사이클 동안 (forward 시 유지, redirect 시 사라짐)
· session      - 한 사용자의 브라우저 닫기까지
· application  - 서버 전체 (모든 사용자 공유)
```

## 11. Scope 사용

```jsp
<%-- page scope --%>
<%
    pageContext.setAttribute("pageVar", "값", PageContext.PAGE_SCOPE);
%>
${pageScope.pageVar}

<%-- request scope --%>
<%
    request.setAttribute("reqVar", "값");
%>
${requestScope.reqVar}

<%-- session scope --%>
<%
    session.setAttribute("loginUser", user);
%>
${sessionScope.loginUser.name}

<%-- application scope --%>
<%
    application.setAttribute("totalVisits", 1234);
%>
${applicationScope.totalVisits}
```

**EL 의 자동 탐색 순서**: `${var}` 는 page → request → session → application 순으로 탐색.

명시적 스코프(`${requestScope.var}`) 가 모호성 피하기에 좋다.

## 12. Scope 선택 가이드

| 데이터 종류 | Scope |
|--|--|
| 한 페이지 안 임시 변수 | page |
| Servlet → JSP forward 데이터 | request |
| 로그인 상태·장바구니·개인 설정 | session |
| 전역 카운터·공통 설정 | application |

---

# Part D. Session

## 13. 세션의 정체

```
[사용자 A 브라우저]                    [서버]
    |
    |  ① 첫 접속 (쿠키 없음)
    +---------------------------------->
    |
    |  ② 서버가 세션 객체 생성 (메모리)
    |     id=SESS-AAA, 빈 데이터
    |     응답에 Set-Cookie: JSESSIONID=SESS-AAA
    | <----------------------------------
    |
    |  ③ 로그인 POST
    |     Cookie: JSESSIONID=SESS-AAA  ← 자동 동봉
    +---------------------------------->
    |     서버: 세션 SESS-AAA 에 loginUser 저장
    | <----------------------------------
    |
    |  ④ 이후 모든 요청에 Cookie 자동 동봉
    |     → 서버가 같은 세션 객체 사용
    +---------------------------------->
```

**세션의 본질**:
- **서버 메모리에 저장된 객체**
- **JSESSIONID** 쿠키로 식별
- 사용자별 별도 세션 객체

## 14. 세션 사용

```java
// 데이터 저장
HttpSession session = req.getSession();
session.setAttribute("loginUser", user);
session.setMaxInactiveInterval(60 * 30);   // 30분 비활성 시 만료

// 데이터 읽기
User loginUser = (User) session.getAttribute("loginUser");

// 데이터 제거
session.removeAttribute("loginUser");

// 세션 전체 무효화 (로그아웃)
session.invalidate();
```

JSP 에선 `${sessionScope.loginUser}` 또는 `<%= session.getAttribute("loginUser") %>`.

## 15. `req.getSession()` vs `req.getSession(false)`

```java
HttpSession s1 = req.getSession();          // 없으면 새로 생성
HttpSession s2 = req.getSession(true);      // 같음
HttpSession s3 = req.getSession(false);     // 없으면 null
```

- 로그인 검증 등에선 **`false`** - 세션 없는 사용자에게 빈 세션 만들지 않음
- 데이터 저장이 필요할 때만 기본 (`true`)

## 16. 세션 vs 쿠키 비교

| 항목 | 쿠키 | 세션 |
|--|--|--|
| 저장 위치 | 클라이언트 | 서버 |
| 보안 | 낮음 (사용자 수정 가능) | 높음 (서버만 접근) |
| 용량 | ~4KB | 무제한 (서버 메모리) |
| 만료 | Max-Age/Expires | 비활성 타임아웃 (보통 30분) |
| 매 요청 전송 | 자동 (헤더) | JSESSIONID 만 (식별자) |
| 도메인 격리 | 도메인 단위 | 서버 단위 |

**실무 패턴**:
- 민감 정보 → 세션
- 환경 설정·개인화 (theme, language) → 쿠키
- 자동 로그인 → 쿠키 (refresh token) + 세션 (access token)

---

## 17. 코드 깊게 - 로그인 + 자동 로그인 풀스택

```java
@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        req.setCharacterEncoding("UTF-8");
        String id = req.getParameter("id");
        String pwd = req.getParameter("password");
        boolean remember = "on".equals(req.getParameter("remember"));

        User user = userService.authenticate(id, pwd);
        if (user == null) {
            req.setAttribute("error", "로그인 실패");
            req.getRequestDispatcher("/login.jsp").forward(req, res);
            return;
        }

        // 1) 세션에 로그인 상태 저장
        HttpSession session = req.getSession();
        session.setAttribute("loginUser", user);
        session.setMaxInactiveInterval(60 * 30);   // 30분

        // 2) 자동 로그인 체크 시 쿠키
        if (remember) {
            String token = userService.issueRememberToken(user.getId());
            Cookie c = new Cookie("REMEMBER_TOKEN", token);
            c.setMaxAge(60 * 60 * 24 * 30);   // 30일
            c.setPath("/");
            c.setHttpOnly(true);
            c.setSecure(true);
            res.addCookie(c);
        }

        res.sendRedirect("/");
    }
}

@WebServlet("/logout")
public class LogoutServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // 1) 세션 무효화
        HttpSession session = req.getSession(false);
        if (session != null) session.invalidate();

        // 2) 쿠키 삭제 (Max-Age=0)
        Cookie c = new Cookie("REMEMBER_TOKEN", "");
        c.setMaxAge(0);
        c.setPath("/");
        res.addCookie(c);

        res.sendRedirect("/");
    }
}
```

---

## 18. 실전 패턴 / 자주 빠지는 함정

### Cookie
- ❌ 비밀번호·신용카드를 쿠키에 저장 ✅ 절대 X. 세션 또는 토큰.
- ❌ `HttpOnly` 없는 쿠키 → XSS 로 JS 가 훔침 ✅ `HttpOnly=true`
- ❌ `Secure` 없이 HTTPS 환경 → 평문 노출 ✅ 운영 환경엔 필수
- ❌ `SameSite=None` 으로 두면 CSRF 취약 ✅ `Lax` 또는 `Strict`
- ❌ 쿠키 한글 깨짐 ✅ `URLEncoder.encode(value, "UTF-8")`

### Session
- ❌ Servlet 의 인스턴스 필드에 사용자 상태 저장 ✅ 세션 attribute 사용
- ❌ 세션에 너무 큰 객체 저장 → 메모리 폭증 ✅ ID 만 저장 + DB 조회
- ❌ 로그아웃 시 `invalidate()` 안 호출 ✅ 세션 + 쿠키 모두 정리
- ❌ `getSession()` 호출만으로 세션 자동 생성 → 봇이 호출하면 메모리 폭증 ✅ 조회만 할 땐 `getSession(false)`

### 멀티 서버 환경
- ❌ 세션을 서버 메모리에만 저장 → 로드밸런서 뒤에서 sticky session 필요 ✅ Redis 등 외부 세션 저장소
- ❌ JSESSIONID 가 동일 도메인 다른 서버에서 안 통함 ✅ 외부 세션 저장소 + 일관된 쿠키 도메인

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| 로그인했는데 세션이 다음 요청에 안 보임 | 쿠키 무시 / SameSite 충돌 / 다른 도메인 | 같은 도메인 사용, SameSite 설정 |
| 세션이 자주 끊김 | `maxInactiveInterval` 너무 짧음 | 시간 늘림 또는 자동 갱신 |
| 세션 사용량 증가 | 큰 객체 저장 | ID + DB 조회로 전환 |
| 쿠키가 브라우저에 저장 안 됨 | `Max-Age` 없음 (세션 쿠키) 또는 도메인 불일치 | 명시 |
| HTTPS 환경에서 쿠키 안 받아짐 | `Secure` 없는데 HTTPS | `Secure=true` 추가 |
| `${sessionScope.loginUser}` 가 빈 값 | 세션 attribute 이름 오타 | 정확히 `loginUser` |

---

## 19. 자가점검

1. HTTP 의 "stateless" 특성 때문에 발생하는 문제 3가지?
2. Cookie 와 Session 의 가장 큰 저장 위치 차이는?
3. JSP 의 4가지 Scope 와 각 범위?
4. `req.getSession()` 과 `req.getSession(false)` 의 차이?
5. 비밀번호를 쿠키에 저장하면 안 되는 이유 2가지?
6. 로그아웃 시 해야 할 정리 작업 2가지?
7. 멀티 서버 환경에서 세션이 깨지는 이유와 해결?

<details><summary>풀이</summary>

1. (a) 로그인 상태 유지 어려움 (매번 인증 필요), (b) 장바구니 같은 페이지 간 상태 유지 어려움, (c) 검색 조건·필터 유지 어려움.
2. **Cookie 는 클라이언트(브라우저) 에 저장, Session 은 서버(메모리) 에 저장**. 그래서 쿠키는 사용자가 수정 가능, 세션은 서버만 접근.
3. **page** (현재 JSP) < **request** (한 요청-응답) < **session** (한 사용자 브라우저) < **application** (서버 전체).
4. `getSession()` = `getSession(true)` - 세션 없으면 새로 생성. `getSession(false)` - 없으면 null 반환. 조회만 할 땐 `false` 가 안전 (불필요한 세션 생성 방지).
5. (a) **클라이언트 저장** - 사용자가 임의 수정 가능. (b) **HTTP 헤더 평문 전송** - HTTPS 안 쓰면 네트워크에서 노출. (c) **XSS 취약** - `HttpOnly` 없으면 JS 가 훔침.
6. (a) **`session.invalidate()`** - 서버 세션 객체 무효화. (b) **자동 로그인 쿠키 삭제** - `Max-Age=0` 으로 굽기.
7. **세션이 한 서버 메모리에만 저장** → 다음 요청이 다른 서버로 가면 세션 모름. **해결**: ① Sticky Session (같은 사용자는 같은 서버로 라우팅) ② **Redis 등 외부 세션 저장소** (Spring Session Redis 등) ③ Stateless 토큰 (JWT).

</details>

---

## 20. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.13 HTTP (개념·메서드·상태코드) | §1 ~ §4 (Part A) |
| p.14 ~ p.19 Cookie (개념·사용·한계) | §5 ~ §9 (Part B) |
| p.20 ~ p.24 JSP 기본 객체 영역 (4 Scope) | §10 ~ §12 (Part C) |
| p.25 ~ p.29 Session (개념·사용·세션 vs 쿠키) | §13 ~ §16 (Part D) |
| p.30 마무리 | (생략) |

_30p 슬라이드 모두 커버._
