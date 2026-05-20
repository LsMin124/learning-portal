# Filter — Listener · Filter · Exception 처리

> **이 강의는 무엇인가**: 서블릿 컨테이너의 3가지 횡단 처리 도구. ① **Listener** - 앱 시작/종료·세션·요청의 생명주기 이벤트 감지, ② **Filter** - 모든 요청·응답의 전/후 가로채기, ③ **Exception 처리** - 에러 페이지 매핑.
> **왜 배우는가**: 인코딩·인증·로깅·CORS·에러 페이지 - 모두 서블릿 단계에서 처리해야 효율적. Spring Security 도 본질은 Filter. Spring Boot 도 결국 이 표준 위에서 동작.

---

## 들어가기 전에

- **선수**: Servlet 강의 (라이프사이클·요청/응답), JSP 강의.
- **마인드셋**: "공통 처리는 한 곳에 모아라" - 매 서블릿에 반복 코드 쓰지 않기.

---

# Part A. Listener

## 1. Listener 의 정의

```
서블릿 컨테이너가 특정 이벤트 발생 시 자동 실행하는 처리용 객체

이벤트 종류:
  · ServletContextListener        - 앱 시작/종료
  · HttpSessionListener           - 세션 생성/소멸
  · ServletRequestListener        - 요청 시작/종료
  · ServletContextAttributeListener - 컨텍스트 attribute 변경
  · HttpSessionAttributeListener  - 세션 attribute 변경
  · ServletRequestAttributeListener - 요청 attribute 변경
  · HttpSessionBindingListener    - 객체가 세션에 묶임/풀림
  · HttpSessionActivationListener - 세션이 직렬화/역직렬화 (분산 환경)
```

## 2. ServletContextListener - 앱 라이프사이클

```java
@WebListener
public class AppLifecycleListener implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        // 앱 시작 시 1번
        System.out.println("애플리케이션 시작");
        // DB 풀 초기화, 캐시 워밍, 외부 서비스 연결 등
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        // 앱 종료 시 1번
        System.out.println("애플리케이션 종료");
        // 자원 해제, 진행 중 작업 cleanup
    }
}
```

## 3. HttpSessionListener - 활성 세션 수 추적

```java
@WebListener
public class SessionCounterListener implements HttpSessionListener {

    private static final AtomicInteger active = new AtomicInteger(0);

    @Override
    public void sessionCreated(HttpSessionEvent se) {
        int now = active.incrementAndGet();
        se.getSession().getServletContext().setAttribute("activeSessions", now);
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        int now = active.decrementAndGet();
        se.getSession().getServletContext().setAttribute("activeSessions", now);
    }
}
```

JSP 에서 `${applicationScope.activeSessions}` 로 현재 접속자 수 표시.

## 4. Listener 등록 - 2가지 방법

**방법 1: 어노테이션 (권장)**
```java
@WebListener
public class MyListener implements ServletContextListener { ... }
```

**방법 2: web.xml**
```xml
<listener>
    <listener-class>com.example.AppLifecycleListener</listener-class>
</listener>
```

---

# Part B. Filter

## 5. Filter 의 정의·위치

```
[클라이언트]
    | HTTP 요청
    ▼
[Servlet Container - Tomcat]
    |
    ▼
Filter Chain                ← Filter 들이 체인으로 실행
    · Filter 1
    · Filter 2
    · Filter 3
    |
    ▼
DispatcherServlet / 서블릿
    |
    ▼
Controller / 비즈니스 로직
```

**Filter 의 본질**:
- **서블릿 표준 인터페이스** (`jakarta.servlet.Filter`)
- **DispatcherServlet 도달 전/후** 에서 요청·응답을 가로챔
- Spring 무관 - 모든 서블릿 기반 웹 앱에서 동작

## 6. Filter 작성

```java
@Component
@WebFilter("/*")
public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig config) throws ServletException {
        // 컨테이너 기동 시 1번
    }

    @Override
    public void doFilter(ServletRequest request,
                          ServletResponse response,
                          FilterChain chain) throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        long start = System.currentTimeMillis();

        // 요청 전 처리 - 인코딩 설정
        request.setCharacterEncoding("UTF-8");

        // 다음 필터/서블릿으로 위임 (⚠ 반드시!)
        chain.doFilter(request, response);

        // 응답 후 처리 - 로깅
        long elapsed = System.currentTimeMillis() - start;
        System.out.println(req.getRequestURI() + " " + elapsed + " ms");
    }

    @Override
    public void destroy() {
        // 컨테이너 종료 시 1번
    }
}
```

**`chain.doFilter()` 호출 안 하면** → 요청이 다음 단계로 안 감 → 빈 응답.

## 7. Filter 순서 제어

**문제**: `@WebFilter` 만으로는 순서 보장 안 됨 (컨테이너 내부 정렬 규칙에 따름).

**해결 1: web.xml** (가장 명확):
```xml
<filter-mapping>
    <filter-name>encodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
<filter-mapping>
    <filter-name>loggingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
<!-- web.xml 의 매핑 순서대로 실행됨 -->
```

**해결 2: Spring Boot `FilterRegistrationBean`**:
```java
@Bean
public FilterRegistrationBean<EncodingFilter> encodingFilter() {
    FilterRegistrationBean<EncodingFilter> reg = new FilterRegistrationBean<>();
    reg.setFilter(new EncodingFilter());
    reg.addUrlPatterns("/*");
    reg.setOrder(1);              // 낮을수록 먼저
    return reg;
}
```

## 8. Filter 활용 사례

| 사례 | 처리 |
|--|--|
| **인코딩** | `request.setCharacterEncoding("UTF-8")` 매 요청 자동 |
| **로깅** | 요청 시각·소요 시간·메서드·URI 기록 |
| **인증** | 세션 검사 → 미인증 시 차단 |
| **CORS** | 응답 헤더 자동 추가 |
| **압축 (Gzip)** | 응답 body 변환 |
| **CSRF 토큰** | 검증 + 발급 |

---

# Part C. Exception 처리

## 9. web.xml 기반 에러 페이지

```xml
<!-- HTTP 상태 코드 기반 -->
<error-page>
    <error-code>404</error-code>
    <location>/error/404.jsp</location>
</error-page>
<error-page>
    <error-code>500</error-code>
    <location>/error/500.jsp</location>
</error-page>

<!-- 예외 클래스 기반 -->
<error-page>
    <exception-type>java.lang.NullPointerException</exception-type>
    <location>/error/npe.jsp</location>
</error-page>
<error-page>
    <exception-type>java.lang.Exception</exception-type>
    <location>/error/general.jsp</location>
</error-page>
```

**주의 사항**:
- `<location>` 은 **컨텍스트 루트 기준 절대 경로**
- `/WEB-INF/` 안에 넣지 말 것 (직접 접근 차단 폴더)
- HTTP 상태 코드 기반과 예외 클래스 기반 동시 사용 가능

## 10. 에러 페이지 작성

```jsp
<%-- /error/500.jsp --%>
<%@ page contentType="text/html;charset=UTF-8" isErrorPage="true" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>

<!DOCTYPE html>
<html>
<head><title>서버 오류</title></head>
<body>
    <h1>서버 오류가 발생했습니다</h1>
    <p>잠시 후 다시 시도해주세요.</p>

    <%-- 개발 환경에선 에러 정보 표시 (운영은 절대 X) --%>
    <c:if test="${initParam.env == 'dev'}">
        <pre>${exception.message}</pre>
    </c:if>

    <a href="/">홈으로</a>
</body>
</html>
```

`isErrorPage="true"` 가 있어야 `${exception}` 으로 예외 객체 접근.

## 11. Exception 처리 방법 3가지 우선순위

```
① 메서드 내 try/catch            (가장 좁음 - 잘 안 씀)
② Servlet 의 catch 블록           (한 서블릿 안)
③ web.xml <error-page>           (모든 서블릿 - 표준)

(Spring 환경에선 추가)
④ @ControllerAdvice + @ExceptionHandler  (Spring 표준)
```

Spring 사용 시엔 4번이 가장 강력. 순수 Servlet 시대엔 3번.

---

## 12. 코드 깊게 - 인증 + 로깅 + 에러 페이지 풀스택

```java
// === 1) ServletContextListener — 앱 시작 시 DB 풀 초기화 ===
@WebListener
public class AppListener implements ServletContextListener {
    @Override
    public void contextInitialized(ServletContextEvent sce) {
        DataSource ds = HikariConfigFactory.create();
        sce.getServletContext().setAttribute("dataSource", ds);
        System.out.println("App started");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        DataSource ds = (DataSource) sce.getServletContext().getAttribute("dataSource");
        if (ds instanceof Closeable c) {
            try { c.close(); } catch (IOException e) { }
        }
    }
}

// === 2) EncodingFilter — 모든 요청 UTF-8 ===
@WebFilter("/*")
public class EncodingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        req.setCharacterEncoding("UTF-8");
        res.setCharacterEncoding("UTF-8");
        chain.doFilter(req, res);
    }
}

// === 3) AuthFilter — 보호 경로 접근 검증 ===
@WebFilter("/admin/*")
public class AuthFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        HttpSession session = req.getSession(false);
        User user = (session != null) ? (User) session.getAttribute("loginUser") : null;

        if (user == null || !"ADMIN".equals(user.getRole())) {
            res.sendRedirect(req.getContextPath() + "/login");
            return;     // ⚠ chain.doFilter() 호출 안 함 = 요청 차단
        }
        chain.doFilter(request, response);
    }
}

// === 4) LoggingFilter — 모든 요청 시간 측정 ===
@WebFilter("/*")
public class LoggingFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {

        long start = System.currentTimeMillis();
        try {
            chain.doFilter(req, res);
        } finally {
            long elapsed = System.currentTimeMillis() - start;
            HttpServletRequest hr = (HttpServletRequest) req;
            System.out.println(hr.getMethod() + " " + hr.getRequestURI() + " " + elapsed + "ms");
        }
    }
}
```

```xml
<!-- 5) web.xml — 에러 페이지 -->
<error-page>
    <error-code>404</error-code>
    <location>/error/404.jsp</location>
</error-page>
<error-page>
    <error-code>500</error-code>
    <location>/error/500.jsp</location>
</error-page>
<error-page>
    <exception-type>java.lang.Exception</exception-type>
    <location>/error/general.jsp</location>
</error-page>
```

---

## 13. 실전 패턴 / 자주 빠지는 함정

### Listener
- ❌ Listener 안에서 무거운 작업 (DB 풀 초기화 100MB 메모리) → 앱 시작 지연
  ✅ 비동기로 시작 또는 lazy init
- ❌ `contextDestroyed` 에서 자원 해제 누락 → 다음 앱 시작 시 충돌
  ✅ try/finally 보장

### Filter
- ❌ `chain.doFilter()` 호출 안 함 → 요청 차단 (의도 외) ✅ 통과시킬 땐 반드시 호출
- ❌ 요청 인코딩 설정을 매 서블릿에서 → 중복 ✅ EncodingFilter 한 곳에서
- ❌ Filter 안에서 Spring Bean 주입 안 됨 → `@Component` 누락 ✅ Spring 관리 Filter
- ❌ Filter 순서가 컨테이너 정렬에 의존 → 예측 불가 ✅ web.xml 또는 `FilterRegistrationBean.setOrder`

### Exception 처리
- ❌ `<error-page>` location 이 `/WEB-INF/` 안 → 접근 불가 ✅ webroot 또는 다른 안전한 경로
- ❌ 운영 환경에서 stack trace 노출 → 보안 사고 ✅ `${exception.message}` 도 운영엔 숨김
- ❌ 모든 예외를 한 페이지로 ✅ 404/500 분리 + 비즈니스 예외 별도
- ❌ Spring 사용 중인데 web.xml `<error-page>` 만 ✅ Spring 은 `@ControllerAdvice`

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| Filter 가 안 호출됨 | `@WebFilter` URL 패턴 오류 또는 컴포넌트 스캔 범위 밖 | 패턴 확인 |
| `chain.doFilter()` 호출했는데 응답 두 번 | doFilter 후 추가로 응답 작성 | 응답 작성 후 return |
| Filter 순서 예측 안 됨 | `@WebFilter` 만 사용 | `web.xml` 또는 `FilterRegistrationBean.setOrder` |
| `${exception}` 가 null in error page | `isErrorPage="true"` 누락 | `<%@ page isErrorPage="true" %>` |
| 404 페이지에 헤더·푸터 안 보임 | 정적 리소스 (`/css/*`) 가 404 차단됨 | 에러 페이지에 정적 리소스 경로 별도 |
| Listener 가 안 호출 | `@WebListener` 누락 또는 web.xml 등록 안 됨 | 어노테이션 또는 XML |

---

## 14. 자가점검

1. Listener·Filter·Interceptor 의 위치 차이?
2. Filter Chain 에서 `chain.doFilter()` 를 호출 안 하면?
3. Filter 와 Interceptor 의 가장 큰 차이?
4. `@WebFilter` 만으로 Filter 순서를 보장할 수 있나?
5. `<error-page>` 의 `<location>` 을 `/WEB-INF/` 안에 두면 안 되는 이유?
6. 에러 페이지에서 예외 객체에 접근하려면 어떤 설정?
7. Listener 의 `ServletContextListener` 활용 사례 2가지?

<details><summary>풀이</summary>

1. **Listener**: 이벤트 감지 (생명주기). **Filter**: DispatcherServlet **밖** (서블릿 컨테이너). **Interceptor**: DispatcherServlet **안** (Spring MVC).
2. **요청이 다음 단계로 안 감** → 빈 응답 또는 사용자에게 응답 없음. 인증 실패 시 의도적으로 안 호출하지만 응답은 직접 작성해야.
3. **Filter 는 서블릿 표준** (Spring 무관, 더 낮은 층), **Interceptor 는 Spring MVC** (Controller 와 HandlerMethod 접근 가능, 더 높은 층).
4. **아니**. `@WebFilter` 만으로는 컨테이너 내부 정렬 규칙에 의존. 명시적으로 순서 보장하려면 `web.xml` 의 `<filter-mapping>` 순서 또는 `FilterRegistrationBean.setOrder`.
5. **`WEB-INF/` 안 자원은 외부 직접 접근 불가** → 사용자가 에러를 보고도 `/WEB-INF/error/500.jsp` 직접 못 봄 (그게 의도). 단, **에러 페이지로 forward 는 되지만** webapp 정적 리소스(CSS·JS) 가 같이 안 와서 깨질 수 있음.
6. **`<%@ page isErrorPage="true" %>`**. 그러면 JSP 의 `exception` 기본 객체로 `${exception.message}` 접근 가능.
7. (a) **DB 풀 초기화** - 앱 시작 시 HikariCP 등 자원 할당. (b) **외부 서비스 연결 종료** - 앱 종료 시 자원 cleanup. (c) **캐시 워밍·통계 시작** 등.

</details>

---

## 15. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.9 Listener (개념·이벤트·등록) | §1 ~ §4 (Part A) |
| p.10 ~ p.16 Filter (개념·작성·순서·활용) | §5 ~ §8 (Part B) |
| p.17 ~ p.20 Exception (`<error-page>`·`isErrorPage`) | §9 ~ §11 (Part C) |
| p.21 마무리 | (생략) |

_21p 슬라이드 모두 커버._
