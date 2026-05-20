# Cookie · Session — 치트시트

> 30p 슬라이드 · HTTP stateless 위에서 상태 유지.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **HTTP 는 stateless** → 클라이언트 식별을 위해 Cookie / Session 필요
2. **Cookie**: 브라우저에 저장 (클라이언트 측). 작고, 보안에 약함
3. **Session**: 서버에 저장 + JSESSIONID 쿠키로 식별. 큰 데이터, 보안 OK
4. **로그인 직후 `request.changeSessionId()`** 호출 (Session Fixation 방어)
5. **민감 쿠키엔 `HttpOnly` + `Secure` + `SameSite=Lax`**
6. **로그아웃**: `session.invalidate()` + 로그인 쿠키 삭제 (`MaxAge=0`)

## 가장 중요한 코드 3개

```java
// (1) 로그인
User user = userService.login(id, pw);
if (user != null) {
    req.changeSessionId();                         // Session Fixation 방어
    HttpSession session = req.getSession();
    session.setAttribute("loginUser", user);
    res.sendRedirect("/");
}

// (2) 쿠키 보안
Cookie cookie = new Cookie("remember", token);
cookie.setHttpOnly(true);                          // JS 접근 차단 (XSS 방어)
cookie.setSecure(true);                            // HTTPS only
cookie.setPath("/");
cookie.setMaxAge(7 * 24 * 60 * 60);                // 7일
res.addCookie(cookie);
// SameSite 는 Servlet API 직접 지원 X -> setHeader 로
res.setHeader("Set-Cookie",
    "remember=" + token + "; HttpOnly; Secure; SameSite=Lax; Path=/");

// (3) 로그아웃
HttpSession session = req.getSession(false);
if (session != null) session.invalidate();
Cookie c = new Cookie("remember", "");
c.setMaxAge(0); c.setPath("/");
res.addCookie(c);
res.sendRedirect("/");
```

## 면접 한 줄 답변
- **Cookie vs Session?** → Cookie 는 클라이언트 저장 (작고 노출), Session 은 서버 저장 (큰 데이터, 안전).
- **JSESSIONID 가 뭐?** → 서버가 세션 객체를 식별하기 위한 쿠키. 클라이언트가 매 요청 동봉.
- **Session Fixation 공격?** → 공격자가 만든 세션 ID 를 피해자가 사용하게 만듦. 로그인 직후 `changeSessionId()` 로 ID 재발급.
- **HttpOnly 의 의미?** → JS 의 `document.cookie` 로 접근 차단. XSS 공격 시 쿠키 탈취 방어.

---

# 2. Quick Reference (실무 복붙)

## Cookie API

```java
// 생성
Cookie cookie = new Cookie("name", "value");
cookie.setMaxAge(3600);                  // 초 단위 (음수=세션, 0=삭제)
cookie.setPath("/");                     // 경로
cookie.setDomain(".example.com");        // 도메인
cookie.setHttpOnly(true);                // JS 접근 차단
cookie.setSecure(true);                  // HTTPS only
res.addCookie(cookie);

// 읽기
Cookie[] cookies = req.getCookies();
if (cookies != null) {
    for (Cookie c : cookies) {
        if ("name".equals(c.getName())) {
            String value = c.getValue();
        }
    }
}

// 삭제
Cookie del = new Cookie("name", "");
del.setMaxAge(0);
del.setPath("/");                        // 생성 시와 같은 path
res.addCookie(del);
```

## Cookie 보안 속성

| 속성 | 의미 |
|--|--|
| **HttpOnly** | JS `document.cookie` 접근 차단 (XSS 방어) |
| **Secure** | HTTPS only (HTTP 면 전송 안 함) |
| **SameSite** | `Strict` / `Lax` / `None` (CSRF 방어) |
| **Domain** | 적용 도메인 |
| **Path** | 적용 경로 |
| **MaxAge** | 만료 시간 (초) |

```java
// SameSite 는 Servlet 표준 API X -> Set-Cookie 헤더 직접
res.setHeader("Set-Cookie",
    "JSESSIONID=" + id + "; HttpOnly; Secure; SameSite=Lax; Path=/");
```

## Session API

```java
// 세션 생성/조회
HttpSession session = req.getSession();      // 없으면 생성
HttpSession session = req.getSession(false); // 없으면 null

// 속성
session.setAttribute("loginUser", user);
User u = (User) session.getAttribute("loginUser");
session.removeAttribute("loginUser");

// 메타
session.getId();                              // JSESSIONID
session.getCreationTime();                    // 생성 시각
session.getLastAccessedTime();                // 마지막 접근
session.isNew();                              // 새 세션?

// 타임아웃
session.setMaxInactiveInterval(30 * 60);     // 30분
session.invalidate();                         // 즉시 만료
```

```xml
<!-- web.xml 글로벌 세션 타임아웃 -->
<session-config>
    <session-timeout>30</session-timeout>   <!-- 분 단위 -->
</session-config>
```

## 로그인 흐름

```java
@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        String id = req.getParameter("id");
        String pw = req.getParameter("password");

        User user = userService.authenticate(id, pw);   // bcrypt 검증
        if (user == null) {
            req.setAttribute("error", "ID/비밀번호 확인");
            req.getRequestDispatcher("/WEB-INF/views/login.jsp").forward(req, res);
            return;
        }

        req.changeSessionId();                          // Fixation 방어
        HttpSession session = req.getSession();
        session.setAttribute("loginUser", user);
        session.setMaxInactiveInterval(30 * 60);

        // returnUrl 처리 (Open Redirect 방어)
        String returnUrl = req.getParameter("returnUrl");
        if (returnUrl == null || !returnUrl.startsWith("/")) {
            returnUrl = "/";
        }
        res.sendRedirect(returnUrl);
    }
}
```

## 로그아웃

```java
@WebServlet("/logout")
public class LogoutServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session != null) {
            session.invalidate();
        }

        // 로그인 쿠키도 삭제
        Cookie del = new Cookie("remember", "");
        del.setMaxAge(0);
        del.setPath("/");
        res.addCookie(del);

        res.sendRedirect("/");
    }
}
```

## 인증 가드 (Filter)

```java
@WebFilter("/mypage/*")
public class AuthFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpReq = (HttpServletRequest) req;
        HttpServletResponse httpRes = (HttpServletResponse) res;

        HttpSession session = httpReq.getSession(false);
        if (session == null || session.getAttribute("loginUser") == null) {
            httpRes.sendRedirect("/login?returnUrl="
                + URLEncoder.encode(httpReq.getRequestURI(), "UTF-8"));
            return;
        }
        chain.doFilter(req, res);
    }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| 쿠키 삭제 시 path 다름 | 생성 시와 같은 path 명시 |
| HttpOnly 누락 → XSS 쿠키 탈취 | `setHttpOnly(true)` |
| HTTPS 인데 Secure 누락 | `setSecure(true)` |
| 로그인 후 changeSessionId X | Session Fixation 위험 |
| returnUrl 외부 URL 허용 | startsWith("/") 검증 |
| session 에 대량 데이터 저장 | DB / Redis 로 |
| 세션 타임아웃 안 설정 | 30분 정도가 일반적 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Cookie · Session (30p)
│
├── [A] HTTP 와 상태
│   ├── stateless 의 의미
│   ├── 클라이언트 식별 필요성
│   └── Cookie vs Session 비교
│
├── [B] Cookie
│   ├── 생성·읽기·삭제
│   ├── 보안 속성 (HttpOnly, Secure, SameSite)
│   ├── MaxAge / Path / Domain
│   └── 용도 (자동 로그인, 조회 중복 방지)
│
├── [C] Session
│   ├── HttpSession API
│   ├── JSESSIONID 쿠키
│   ├── setMaxInactiveInterval
│   └── invalidate
│
├── [D] 로그인 흐름
│   ├── 인증 (bcrypt)
│   ├── changeSessionId (Fixation 방어)
│   ├── setAttribute("loginUser")
│   └── returnUrl 검증
│
├── [E] 인증 가드
│   ├── Filter (JSP/Servlet)
│   ├── Interceptor (Spring)
│   └── Spring Security
│
└── [F] 보안
    ├── Session Fixation
    ├── XSS (HttpOnly)
    ├── CSRF (SameSite)
    ├── Open Redirect (returnUrl)
    └── Session Hijacking (Secure HTTPS)
```

## 학습 진도 체크리스트

### A. Cookie
- [ ] 생성·읽기·삭제 패턴
- [ ] HttpOnly / Secure / SameSite 속성
- [ ] MaxAge (음수/0/양수) 의미

### B. Session
- [ ] HttpSession API
- [ ] JSESSIONID 의 역할
- [ ] 타임아웃 설정 (Java + web.xml)

### C. 로그인
- [ ] changeSessionId 의 역할
- [ ] returnUrl 의 Open Redirect 위험
- [ ] 로그아웃 시 invalidate + 쿠키 삭제

### D. 보안
- [ ] Session Fixation 공격 + 방어
- [ ] XSS 와 HttpOnly
- [ ] CSRF 와 SameSite
- [ ] HTTPS + Secure 쿠키

## 연관 강의

```
1강 Servlet         -> req/res 객체
2강 JSP             -> ${sessionScope.user}
3강 Cookie/Session  <- 현재 위치
4강 EL/JSTL         -> View 에서 세션 접근
5강 Filter          -> 인증 가드 공통 처리
Framework 7강 Interceptor -> Spring 인증
```

→ 다음 (EL/JSTL) 에서 **View 에서 세션·쿠키 깔끔하게**.
