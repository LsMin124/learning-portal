# Filter — 치트시트

> 21p 슬라이드 · 모든 요청·응답 전후 공통 처리 (인코딩·인증·CORS·로깅).
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Filter** = Servlet 호출 전후 가로채기. 모든 요청/응답 공통 처리.
2. **체인 구조**: `Filter1 → Filter2 → Filter3 → Servlet → Filter3 → Filter2 → Filter1`
3. **`chain.doFilter()` 안 호출하면 Servlet 안 감** (인증 거부 시 활용)
4. **흔한 용도**: 인코딩 / 인증 / CORS / GZIP / 로깅 / XSS 방어
5. **`@WebFilter("/path")`** 또는 `web.xml` 또는 Spring `FilterRegistrationBean`
6. **순서**: `web.xml` 의 선언 순서 / Spring 은 `setOrder()`

## 가장 중요한 코드 3개

```java
// (1) 인코딩 Filter (가장 흔함)
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
```

```java
// (2) 인증 Filter
@WebFilter("/mypage/*")
public class AuthFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpReq = (HttpServletRequest) req;
        HttpServletResponse httpRes = (HttpServletResponse) res;

        HttpSession session = httpReq.getSession(false);
        if (session == null || session.getAttribute("loginUser") == null) {
            httpRes.sendRedirect("/login");
            return;                              // chain.doFilter 호출 안 함
        }
        chain.doFilter(req, res);                // 통과
    }
}
```

```java
// (3) 응답 시간 측정 + 로깅
@WebFilter("/*")
public class LoggingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        long start = System.currentTimeMillis();
        try {
            chain.doFilter(req, res);
        } finally {
            HttpServletRequest httpReq = (HttpServletRequest) req;
            log.info("{} {} - {}ms",
                httpReq.getMethod(), httpReq.getRequestURI(),
                System.currentTimeMillis() - start);
        }
    }
}
```

## 면접 한 줄 답변
- **Filter vs Interceptor?** → Filter 는 Servlet 표준 (앞단), Interceptor 는 Spring (컨트롤러 진입). Filter 가 더 앞 + Spring 객체 접근 X.
- **doFilter() 안 호출하면?** → Servlet 까지 안 감. 인증 실패 시 응답을 직접 작성하고 return.
- **Filter 순서는?** → web.xml 의 mapping 순서 / Spring 의 `setOrder()`.
- **Filter 의 장점?** → 횡단 관심사 (인코딩·인증·CORS) 를 Servlet 마다 반복 X.

---

# 2. Quick Reference (실무 복붙)

## Filter 인터페이스

```java
public interface Filter {
    default void init(FilterConfig config) throws ServletException { }
    void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException;
    default void destroy() { }
}
```

## 등록 (3 방법)

```java
// 1. @WebFilter (Servlet 3.0+)
@WebFilter(urlPatterns = "/*", filterName = "encoding")
public class EncodingFilter implements Filter { ... }

// 2. web.xml
<filter>
    <filter-name>encoding</filter-name>
    <filter-class>com.study.EncodingFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>encoding</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>

// 3. Spring Boot FilterRegistrationBean
@Bean
public FilterRegistrationBean<EncodingFilter> encodingFilter() {
    FilterRegistrationBean<EncodingFilter> bean = new FilterRegistrationBean<>();
    bean.setFilter(new EncodingFilter());
    bean.addUrlPatterns("/*");
    bean.setOrder(1);                    // 순서
    return bean;
}
```

## Filter Chain

```
Request
   ↓
[EncodingFilter.doFilter]      pre
   ↓ chain.doFilter()
[AuthFilter.doFilter]          pre
   ↓ chain.doFilter()
[LoggingFilter.doFilter]       pre
   ↓ chain.doFilter()
[Servlet]
   ↑
[LoggingFilter]                post
   ↑
[AuthFilter]                   post
   ↑
[EncodingFilter]               post
   ↓
Response
```

## 전/후 처리 패턴

```java
public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
        throws IOException, ServletException {

    // === PRE (요청 전 처리) ===
    long start = System.currentTimeMillis();
    log.info("진입");

    // === 다음 Filter 또는 Servlet 으로 ===
    chain.doFilter(req, res);

    // === POST (응답 후 처리) ===
    log.info("응답 시간: {} ms", System.currentTimeMillis() - start);
}
```

## 차단 (인증 거부)

```java
HttpServletRequest httpReq = (HttpServletRequest) req;
HttpServletResponse httpRes = (HttpServletResponse) res;

if (!isAuthenticated(httpReq)) {
    // 응답 직접 작성
    httpRes.setStatus(401);
    httpRes.setContentType("application/json;charset=UTF-8");
    httpRes.getWriter().write("{\"error\":\"Unauthorized\"}");
    return;                                    // chain.doFilter 호출 X
}
chain.doFilter(req, res);
```

## URL 패턴

```java
@WebFilter("/*")                  // 모든 요청
@WebFilter("/api/*")              // /api 로 시작
@WebFilter("/admin/*")            // /admin 로 시작
@WebFilter("*.do")                // .do 확장자
@WebFilter({"/api/*", "/v2/*"})   // 다중
```

## 순서 매기기

```java
// web.xml - filter-mapping 선언 순서대로
<filter-mapping><filter-name>encoding</filter-name></filter-mapping>  // 1
<filter-mapping><filter-name>auth</filter-name></filter-mapping>      // 2
<filter-mapping><filter-name>logging</filter-name></filter-mapping>   // 3

// Spring - setOrder 작은 값이 먼저
@Bean public FilterRegistrationBean<?> f1() { ... .setOrder(1); }
@Bean public FilterRegistrationBean<?> f2() { ... .setOrder(2); }
```

→ 권장 순서: **인코딩 → 로깅 → 인증 → CORS**.

## CORS Filter

```java
@WebFilter("/*")
public class CorsFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletResponse httpRes = (HttpServletResponse) res;
        httpRes.setHeader("Access-Control-Allow-Origin", "http://localhost:5173");
        httpRes.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE");
        httpRes.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
        httpRes.setHeader("Access-Control-Allow-Credentials", "true");

        if ("OPTIONS".equals(((HttpServletRequest) req).getMethod())) {
            httpRes.setStatus(200);
            return;
        }
        chain.doFilter(req, res);
    }
}
```

## XSS Filter (입력 sanitize)

```java
// Wrapper 로 getParameter 오버라이드
public class XssRequestWrapper extends HttpServletRequestWrapper {
    public XssRequestWrapper(HttpServletRequest req) { super(req); }

    @Override
    public String getParameter(String name) {
        String value = super.getParameter(name);
        return value == null ? null : value.replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    }
}

@WebFilter("/*")
public class XssFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        chain.doFilter(new XssRequestWrapper((HttpServletRequest) req), res);
    }
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `chain.doFilter()` 누락 → 요청 안 감 | 통과 시 필수 호출 |
| 차단 시에도 `chain.doFilter()` 호출 → 통과됨 | `return` 으로 끊기 |
| 인코딩 Filter 가 인증 Filter 뒤 → 한글 X | 인코딩이 먼저 |
| URL 패턴 `/*` 인데 정적 자원도 거름 | 정적 자원 제외 (`*.css`, `*.js`) |
| ServletRequest 캐스팅 매번 | HttpServletRequest 로 한 번만 |
| Spring 에서 `@Component Filter` 만 → 등록 X | `FilterRegistrationBean` 으로 명시 등록 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Filter (21p)
│
├── [A] Filter 인터페이스
│   ├── init / doFilter / destroy
│   ├── ServletRequest / Response 캐스팅
│   └── FilterChain
│
├── [B] 등록
│   ├── @WebFilter (어노테이션)
│   ├── web.xml (filter + filter-mapping)
│   └── Spring FilterRegistrationBean
│
├── [C] Filter Chain
│   ├── 체인 동작 (in / out)
│   ├── chain.doFilter() 의 의미
│   └── 순서 (web.xml 또는 setOrder)
│
├── [D] 주요 용도
│   ├── 인코딩 (한글)
│   ├── 인증 / 인가
│   ├── CORS
│   ├── 로깅 / 시간 측정
│   ├── XSS / SQL Injection 사전 차단
│   └── GZIP 압축
│
├── [E] 차단·통과
│   ├── chain.doFilter() 호출 → 통과
│   ├── 호출 안 함 + return → 차단
│   └── 응답 직접 작성 (status, body)
│
└── [F] vs Interceptor
    ├── Filter: Servlet 표준 (앞단)
    ├── Interceptor: Spring (Controller 진입)
    └── 선택: 인코딩=Filter, 비즈니스 인증=Interceptor
```

## 학습 진도 체크리스트

### A. 기본
- [ ] Filter 인터페이스 (init / doFilter / destroy)
- [ ] @WebFilter 어노테이션
- [ ] FilterChain 의 의미

### B. 동작
- [ ] chain.doFilter() 호출/누락 효과
- [ ] pre / post 처리 패턴
- [ ] 응답 직접 작성 (인증 거부)

### C. 순서
- [ ] web.xml mapping 순서
- [ ] Spring setOrder
- [ ] 권장 순서 (인코딩 → 로깅 → 인증 → CORS)

### D. 실전
- [ ] EncodingFilter 작성
- [ ] AuthFilter 작성
- [ ] CORS Filter 작성
- [ ] XSS Wrapper 패턴

### E. 비교
- [ ] Filter vs Interceptor 선택 기준
- [ ] Spring Security 와의 통합

## 연관 강의

```
1강 Servlet         -> req/res 객체
3강 Cookie/Session  -> session.getAttribute("loginUser")
5강 Filter          <- 현재 위치
6강 Back 종합실습   -> 게시판에 Filter 적용
Framework 7강 Interceptor -> Spring 의 Filter 후속
```

→ 다음 (Back 종합실습) 에서 **모든 강의를 통합**.
