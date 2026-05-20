# Cookie & Session — 퀴즈

> 16문항. 개념·적용·디버그·면접. 4부(HTTP·Cookie·JSP Scope·Session) 골고루.

---

### Q1. (개념) HTTP 가 stateless 임을 보완하는 메커니즘 2가지?

<details><summary>정답</summary>

**쿠키 (Cookie)** + **세션 (Session)**. 쿠키는 클라이언트가 자동으로 매 요청에 동봉, 세션은 서버 메모리에 저장 + JSESSIONID 쿠키로 식별.

</details>

### Q2. (개념) Cookie 와 Session 의 가장 큰 차이?

<details><summary>정답</summary>

**저장 위치**: Cookie 는 **클라이언트(브라우저)**, Session 은 **서버(메모리)**.

파생 차이:
- 보안: 쿠키는 사용자 수정 가능, 세션은 서버만 접근
- 용량: 쿠키 ~4KB, 세션 무제한
- 전송: 쿠키는 매 요청 헤더에 자동, 세션은 JSESSIONID 만

</details>

### Q3. (개념) `HttpOnly` 쿠키 속성의 의미와 왜 필요한가?

<details><summary>정답</summary>

**JS 에서 `document.cookie` 로 접근 불가** - XSS 공격 방어. 공격자가 페이지에 JS 를 주입해도 인증 쿠키를 훔칠 수 없음.

```java
Cookie c = new Cookie("JSESSIONID", "...");
c.setHttpOnly(true);    // ⚠ 인증·세션 쿠키엔 필수
```

</details>

### Q4. (개념) `Secure` 와 `SameSite` 쿠키 속성?

<details><summary>정답</summary>

- **`Secure=true`**: HTTPS 에서만 전송 (HTTP 로는 안 보냄). 평문 노출 방지.
- **`SameSite=Strict`**: 같은 사이트 요청에만 전송 (CSRF 강력 방어)
- **`SameSite=Lax`** (기본): 안전한 메서드(GET)는 cross-site OK, 위험한 메서드(POST)는 차단
- **`SameSite=None`**: 모든 cross-site OK (`Secure=true` 필수)

</details>

### Q5. (적용) 7일짜리 다크모드 쿠키를 굽는 코드?

<details><summary>정답</summary>

```java
Cookie c = new Cookie("theme", "dark");
c.setMaxAge(60 * 60 * 24 * 7);   // 7일 (초)
c.setPath("/");
c.setHttpOnly(false);             // 이 쿠키는 JS 에서 읽어야 (테마 적용)
c.setSecure(true);                // 운영 환경
res.addCookie(c);
```

JSP 에선 `${cookie.theme.value}` 또는 JS 에서 `document.cookie.match(/theme=(\w+)/)`.

</details>

### Q6. (적용) 쿠키를 삭제하는 코드는?

<details><summary>정답</summary>

`Max-Age=0` 으로 같은 이름·경로의 쿠키를 다시 굽기:

```java
Cookie c = new Cookie("theme", "");
c.setMaxAge(0);
c.setPath("/");
res.addCookie(c);
```

브라우저가 받자마자 즉시 삭제.

</details>

### Q7. (개념) JSP 의 4가지 Scope 와 각 범위?

<details><summary>정답</summary>

| Scope | 범위 |
|--|--|
| `page` | 현재 JSP 페이지 안 |
| `request` | 한 요청-응답 (forward 시 유지, redirect 시 X) |
| `session` | 한 사용자의 브라우저 닫기까지 |
| `application` | 서버 전체 (모든 사용자 공유) |

EL `${var}` 는 page → request → session → application 순으로 탐색.

</details>

### Q8. (적용) Servlet 에서 로그인한 사용자를 세션에 저장하는 코드?

<details><summary>정답</summary>

```java
User user = userService.authenticate(id, pwd);
HttpSession session = req.getSession();
session.setAttribute("loginUser", user);
session.setMaxInactiveInterval(60 * 30);   // 30분 비활성 만료
```

JSP 에서 `${sessionScope.loginUser.name}` 으로 접근.

</details>

### Q9. (개념) `req.getSession()` 과 `req.getSession(false)` 의 차이? 어느 걸 언제?

<details><summary>정답</summary>

- `getSession()` = `getSession(true)`: 세션 없으면 **새로 생성**
- `getSession(false)`: 없으면 **null 반환**

**언제 false?** 로그인 확인 등 조회만 할 때 - 봇이 호출해도 빈 세션 객체 안 만들어서 메모리 절약.

```java
HttpSession s = req.getSession(false);
if (s == null || s.getAttribute("loginUser") == null) {
    res.sendRedirect("/login");
    return;
}
```

</details>

### Q10. (적용) 로그아웃 처리 — 세션 + 자동로그인 쿠키 모두 정리.

<details><summary>정답</summary>

```java
@WebServlet("/logout")
public class LogoutServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {
        // 1) 세션 무효화
        HttpSession session = req.getSession(false);
        if (session != null) session.invalidate();

        // 2) 자동 로그인 쿠키 삭제
        Cookie c = new Cookie("REMEMBER_TOKEN", "");
        c.setMaxAge(0);
        c.setPath("/");
        res.addCookie(c);

        res.sendRedirect("/");
    }
}
```

</details>

### Q11. (디버그) 로그인 직후 다른 요청에 세션이 안 보임. 원인?

<details><summary>정답</summary>

원인 후보:
1. **쿠키 브라우저 차단** - Privacy 설정·시크릿 모드
2. **`SameSite=Strict`** + 다른 사이트에서 진입 → 쿠키 안 보냄
3. **다른 도메인** - `localhost:8080` 으로 로그인 후 `127.0.0.1:8080` 접근 (브라우저 입장에선 다른 도메인)
4. **`Secure=true` 쿠키 + HTTP 환경** - 안 받음
5. **로드밸런서 sticky session 미설정** - 다음 요청이 다른 서버로

브라우저 개발자 도구 > Application > Cookies 에서 JSESSIONID 존재 확인.

</details>

### Q12. (디버그) `${sessionScope.loginUser}` 가 빈 값. 코드는 `session.setAttribute("loginUser", user)`. 원인?

<details><summary>정답</summary>

1. **attribute 이름 오타** - 정확히 `loginUser` 여야
2. **세션이 invalidate 됨** - 다른 곳에서 `session.invalidate()` 호출
3. **세션 타임아웃** - `maxInactiveInterval` 지남
4. **다른 세션** - 쿠키가 안 보내져서 매번 새 세션 생성됨

브라우저 개발자 도구로 JSESSIONID 가 매 요청마다 같은지 확인.

</details>

### Q13. (개념) 비밀번호를 쿠키에 저장하면 안 되는 이유 3가지?

<details><summary>정답</summary>

1. **클라이언트 저장** - 사용자가 직접 수정 가능. 로컬에서 파일로 추출 가능
2. **HTTP 헤더 평문 전송** - HTTPS 없으면 네트워크에서 도청 가능
3. **XSS 취약** - `HttpOnly` 없으면 악성 JS 가 훔침

비밀번호는 **로그인 시 한 번만 검증** 후 세션 ID 만 쿠키로. 비밀번호는 서버 DB 에 **해시(BCrypt) 로만** 저장.

</details>

### Q14. (면접) "Session 과 JWT 토큰 중 어느 것을 인증에 쓰겠습니까?"

<details><summary>정답</summary>

**상황별 선택**:

**Session 추천**:
- 모놀리식·중규모 웹 앱
- 로그아웃 즉시 무효화가 중요 (서버에서 invalidate)
- 세션에 풍부한 상태 (장바구니·진행 중 작업) 보관

**JWT 추천**:
- MSA·SPA·모바일
- Stateless 가 중요 (서버 메모리 안 씀, 수평 확장 쉬움)
- Cross-domain·다양한 클라이언트 (브라우저·앱·API)

**현실**: 둘 다 쓰는 게 흔함 - Refresh Token (서버 검증 가능) + Access Token (JWT, stateless). 또는 Spring Session Redis 로 세션도 stateless 화.

</details>

### Q15. (면접) "멀티 서버 환경에서 세션이 깨지는 이유와 해결 3가지?"

<details><summary>정답</summary>

**문제**: 서버 A 에서 만든 세션을 다음 요청이 서버 B 로 가면 모름.

**해결 3가지**:
1. **Sticky Session** - 로드밸런서가 같은 사용자를 같은 서버로 보냄. 가장 쉬움. 단점: 서버 하나 죽으면 세션 다 잃음
2. **외부 세션 저장소** - Redis/Memcached 에 세션 저장. Spring Session Redis 가 표준. 모든 서버가 같은 저장소 보니까 OK
3. **Stateless 토큰** - JWT 등으로 세션 자체를 안 씀. 토큰 안에 사용자 정보 다 들어있어 서버 어디로 가든 동작

실무는 보통 ② Redis. ③ 은 MSA 환경.

</details>

### Q16. (면접) "쿠키와 세션의 보안 위협 + 방어 패턴을 정리하시오."

<details><summary>정답</summary>

**쿠키 보안 위협**:
- **XSS** (Cross-Site Scripting) - 악성 JS 가 쿠키 훔침 → `HttpOnly=true`
- **CSRF** (Cross-Site Request Forgery) - 다른 사이트가 사용자 쿠키로 요청 위조 → `SameSite=Lax/Strict` + CSRF 토큰
- **MITM** (Man-in-the-Middle) - 네트워크에서 평문 도청 → `Secure=true` + HTTPS

**세션 보안 위협**:
- **세션 하이재킹** - JSESSIONID 노출 → HttpOnly+Secure+SameSite
- **세션 고정 (Session Fixation)** - 공격자가 세션 ID 를 사용자에게 강요 → 로그인 시 `session.invalidate()` 후 새 세션
- **세션 무한 메모리** - 봇이 무한 생성 → `getSession(false)` + 짧은 만료

**종합 패턴**:
```java
Cookie c = new Cookie("JSESSIONID", "...");
c.setHttpOnly(true);
c.setSecure(true);                       // HTTPS
// SameSite=Lax 는 Tomcat context.xml 또는 Spring config
```

</details>
