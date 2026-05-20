# Spring Interceptor — Filter · Filter 실습 · Interceptor · Interceptor 실습

> **이 강의는 무엇인가**: 요청을 가로채 부가 작업을 수행하는 두 메커니즘 **Filter** (서블릿 표준) 와 **Interceptor** (Spring MVC). 둘의 위치·차이·언제 어느 걸 쓰는지.
> **왜 배우는가**: 인증·인가·로깅·인코딩 같은 공통 처리를 컨트롤러 메서드마다 반복하면 코드가 망가진다. Filter/Interceptor 가 그걸 한 곳으로 모으는 표준 도구. AOP 와 함께 "횡단 관심사" 분리의 3대 무기.

---

## 들어가기 전에

- **선수**: Servlet 기초 (`Filter`, `HttpServletRequest/Response`), Spring MVC (DispatcherServlet, HandlerMapping), AOP 기초.
- **마인드셋**: "어느 시점에 어떤 정보를 가지고 가로챌 수 있는가" 의 차이를 의식. 같은 일을 다른 위치에서 할 수 있을 때, 가장 적합한 위치를 선택.

---

# Part A. Filter

## 1. Filter 의 정의와 위치

```
[클라이언트]
    | HTTP 요청
    ▼
[Servlet Container - Tomcat]
    |
    ▼
Filter Chain                   ← Filter 들이 체인으로 실행
    · Filter 1
    · Filter 2
    · Filter 3
    |
    ▼
DispatcherServlet              ← Spring MVC 의 영역
    |
    ▼
HandlerInterceptor             ← Interceptor 는 여기 (다음 Part)
    |
    ▼
Controller                     ← 비즈니스 로직 진입
```

**Filter 의 본질**:
- 서블릿 컨테이너(Tomcat)가 관리하는 **서블릿 표준** (`javax.servlet.Filter`)
- DispatcherServlet **도달 전/후** 에서 요청·응답을 가로챔
- Spring 무관 — 모든 서블릿 기반 웹 앱에서 동작

## 2. Filter Chain

```
[요청]
   |
   ▼
[Filter 1] doFilter()
   |
   | chain.doFilter(req, res)   ← 다음 필터로 위임
   ▼
[Filter 2] doFilter()
   |
   | chain.doFilter(req, res)
   ▼
[Filter 3] doFilter()
   |
   | chain.doFilter(req, res)
   ▼
[DispatcherServlet → Controller]
   |
   ▲  ← 응답이 역순으로 거슬러 올라옴
[Filter 3] (응답 후처리)
   ▲
[Filter 2]
   ▲
[Filter 1]
   ▲
[클라이언트 응답]
```

**Filter Chain** 의 특징:
- 여러 필터가 **체인** 형태로 연결
- 각 필터는 `chain.doFilter()` 호출로 다음 필터에 위임
- 호출 안 하면 **요청 자체가 막힘** (인증 실패 시 등)

## 3. Filter 작성 — 표준 인터페이스

```java
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;

@Component
public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig config) throws ServletException {
        System.out.println("LoggingFilter 초기화");
    }

    @Override
    public void doFilter(ServletRequest request,
                          ServletResponse response,
                          FilterChain chain) throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        long start = System.currentTimeMillis();

        // 요청 전 처리
        System.out.println("[Before] " + req.getMethod() + " " + req.getRequestURI());

        // 다음 필터/컨트롤러로 위임
        chain.doFilter(request, response);

        // 응답 후 처리
        long elapsed = System.currentTimeMillis() - start;
        System.out.println("[After ] " + req.getRequestURI() + " " + elapsed + " ms");
    }

    @Override
    public void destroy() {
        System.out.println("LoggingFilter 종료");
    }
}
```

**3가지 생명주기 메서드**:
- `init()` — 컨테이너 기동 시 1번 (초기화)
- `doFilter()` — 매 요청마다 (실제 동작)
- `destroy()` — 컨테이너 종료 시 1번 (정리)

## 4. Spring Boot 에서 Filter 등록

방법 1: `@Component` + `@WebFilter`
```java
@Component
@WebFilter("/*")                    // URL 패턴
public class LoggingFilter implements Filter { ... }
```

방법 2: `FilterRegistrationBean` (권장)
```java
@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<LoggingFilter> loggingFilter() {
        FilterRegistrationBean<LoggingFilter> reg = new FilterRegistrationBean<>();
        reg.setFilter(new LoggingFilter());
        reg.addUrlPatterns("/api/*");
        reg.setOrder(1);              // 순서 (낮을수록 먼저)
        return reg;
    }
}
```

`FilterRegistrationBean` 이 권장되는 이유: URL 패턴·순서·initParam 등 세밀 제어 가능.

## 5. Filter 활용 사례

| 사례 | 위치 | 이유 |
|--|--|--|
| **요청·응답 로깅** | Filter | 모든 요청에 공통 적용 |
| **CORS 처리** | Filter | DispatcherServlet 전에 처리해야 |
| **인코딩 설정** | Filter (`CharacterEncodingFilter`) | 컨트롤러 도달 전 |
| **인증 (Spring Security)** | Filter | SecurityFilterChain 도 결국 Filter |
| **요청 body 캐싱** | Filter | 여러 번 읽으려면 wrapping |
| **압축 (Gzip)** | Filter | 응답 body 변환 |

---

# Part B. Interceptor

## 6. Interceptor 의 정의와 위치

```
[DispatcherServlet]
       |
       ▼ HandlerMapping 으로 Controller 찾음
       |
       ▼
[Interceptor.preHandle()]   ← Controller 호출 직전
       |
       ▼
[Controller] @GetMapping 메서드 실행
       |
       ▼
[Interceptor.postHandle()]  ← Controller 실행 후, View 렌더 전
       |
       ▼
[View 렌더]
       |
       ▼
[Interceptor.afterCompletion()] ← 응답 완료 후 (예외 발생해도)
```

**Interceptor 의 본질**:
- **Spring MVC 의 영역** — DispatcherServlet 이 관리
- Controller 호출 **직전/직후/응답 후** 의 3가지 시점에 끼어듦
- Spring 의 `HandlerInterceptor` 인터페이스 구현

## 7. HandlerInterceptor 의 3가지 메서드

```java
@Component
public class MyInterceptor implements HandlerInterceptor {

    // 1) Controller 실행 직전
    //    return true → 통과, false → 중단
    @Override
    public boolean preHandle(HttpServletRequest req,
                              HttpServletResponse res,
                              Object handler) throws Exception {
        // 인증 검사, 로깅, 권한 확인 등
        return true;
    }

    // 2) Controller 실행 후, View 렌더 전
    //    ModelAndView 에 접근 가능 → 모델 수정 가능
    @Override
    public void postHandle(HttpServletRequest req,
                            HttpServletResponse res,
                            Object handler,
                            ModelAndView mav) throws Exception {
        // 공통 모델 추가, 로깅 등
    }

    // 3) 응답 완료 후 (View 렌더까지 끝)
    //    예외 발생해도 호출됨
    @Override
    public void afterCompletion(HttpServletRequest req,
                                 HttpServletResponse res,
                                 Object handler,
                                 Exception ex) throws Exception {
        // 자원 해제, 최종 로깅, 예외 추적 등
    }
}
```

**모두 default 메서드** — 필요한 메서드만 골라 오버라이드.

## 8. Interceptor 등록 — `WebMvcConfigurer`

```java
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final LoginCheckInterceptor loginCheckInterceptor;
    private final LoggingInterceptor    loggingInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 1) 로깅 (모든 경로)
        registry.addInterceptor(loggingInterceptor)
                .addPathPatterns("/**")
                .order(1);

        // 2) 로그인 체크 (보호된 경로만)
        registry.addInterceptor(loginCheckInterceptor)
                .addPathPatterns("/admin/**", "/mypage/**")
                .excludePathPatterns("/login", "/signup", "/css/**", "/js/**")
                .order(2);
    }
}
```

**핵심 메서드**:
- `addPathPatterns(...)` — 적용 경로 (Ant 패턴)
- `excludePathPatterns(...)` — 제외 경로
- `order(int)` — 실행 순서 (낮을수록 먼저)

## 9. 다중 Interceptor 실행 순서

```
등록 순서대로 preHandle, 역순으로 postHandle/afterCompletion

[등록 순서]  L1 → L2 → L3

[preHandle  순서]   L1 → L2 → L3
[Controller 실행]
[postHandle 순서]   L3 → L2 → L1     ← 역순!
[afterCompletion]   L3 → L2 → L1     ← 역순!
```

이유: 후속 인터셉터가 이전 인터셉터의 결과를 보고 추가 작업 가능. **스택처럼 동작**.

## 10. preHandle 의 return 값

```java
@Override
public boolean preHandle(HttpServletRequest req, ...) {
    User user = (User) req.getSession().getAttribute("loginUser");
    if (user == null) {
        res.sendRedirect("/login");
        return false;    // ⚠ 컨트롤러 실행 차단!
    }
    return true;         // ✅ 통과
}
```

- `return true` — Controller 호출
- `return false` — Controller 실행 안 함 + 응답은 인터셉터에서 직접 작성해야 (안 하면 빈 응답)

---

# Part C. Filter vs Interceptor 비교

## 11. 한 표로 정리

| 비교 | Filter | Interceptor |
|--|--|--|
| **관리 주체** | 서블릿 컨테이너 (Tomcat) | Spring MVC (DispatcherServlet) |
| **위치** | DispatcherServlet **밖** | DispatcherServlet **안** |
| **Spring 빈 주입** | 어려움 (`FilterRegistrationBean` 필요) | 쉬움 (`@Component` + `WebMvcConfigurer`) |
| **HandlerMethod 접근** | ❌ | ✅ (`Object handler` 파라미터) |
| **ModelAndView 접근** | ❌ | ✅ (postHandle 에서) |
| **응답 body 변환** | ✅ (Wrapper 로) | ❌ (안 됨) |
| **URL 패턴** | 서블릿 패턴 | Ant 패턴 (`/admin/**`) |
| **언제 쓰나** | 인코딩·CORS·로깅·인증(Security) | 권한 검사·로깅·model 추가 |

## 12. 둘 다 쓸 때의 순서

```
[요청]
   |
   ▼ Filter Chain (Tomcat 영역)
   |
   ▼ DispatcherServlet
   |
   ▼ Interceptor.preHandle (Spring MVC 영역)
   |
   ▼ Controller
   |
   ▼ Interceptor.postHandle
   |
   ▼ View 렌더
   |
   ▼ Interceptor.afterCompletion
   |
   ▼ Filter Chain (응답 후처리)
   |
   ▼ [응답]
```

큰 그림: **Filter 가 더 넓고 낮은 층, Interceptor 가 더 좁고 높은 층**.

## 13. AOP 와의 관계

| 메커니즘 | 위치 | 무엇을 가로채나 |
|--|--|--|
| **Filter** | 서블릿 컨테이너 | HTTP 요청·응답 |
| **Interceptor** | Spring MVC | 컨트롤러 메서드 호출 |
| **AOP** | 어디든 (메서드 호출) | 모든 Spring 빈의 메서드 |

```
              요청 도착
                 |
                 ▼
              [Filter]
                 |
                 ▼
         [Interceptor]
                 |
                 ▼
        [Controller 메서드]
                 |      ↕ AOP (메서드 단위)
                 ▼
        [Service 메서드]
                 |      ↕ AOP (트랜잭션 등)
                 ▼
           [DAO 메서드]
                 |      ↕ AOP (캐시 등)
                 ▼
                DB
```

**선택 기준**:
- HTTP 레벨 처리 → Filter
- Controller 레벨 → Interceptor
- Service/DAO 레벨 → AOP

---

## 14. 코드 깊게 — 로그인 체크 Interceptor 풀스택

```java
// === 어노테이션 - 보호 대상 표시 ===
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LoginRequired { }

// === Interceptor ===
@Component
@Slf4j
public class LoginCheckInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest req,
                              HttpServletResponse res,
                              Object handler) throws Exception {

        // 1) 정적 리소스 등은 HandlerMethod 가 아님
        if (!(handler instanceof HandlerMethod)) return true;
        HandlerMethod hm = (HandlerMethod) handler;

        // 2) @LoginRequired 없으면 통과
        if (!hm.hasMethodAnnotation(LoginRequired.class)) return true;

        // 3) 세션 확인
        HttpSession session = req.getSession(false);
        User user = (session == null) ? null : (User) session.getAttribute("loginUser");
        if (user != null) {
            log.info("Auth OK: {}", user.getUsername());
            return true;
        }

        // 4) 비로그인 처리 - API vs 페이지 구분
        String accept = req.getHeader("Accept");
        if (accept != null && accept.contains("application/json")) {
            res.setStatus(HttpServletResponse.SC_UNAUTHORIZED);   // 401
            res.setContentType("application/json;charset=UTF-8");
            res.getWriter().write("{\"code\":\"UNAUTHORIZED\"}");
        } else {
            res.sendRedirect("/login");
        }
        return false;
    }
}

// === 등록 ===
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final LoginCheckInterceptor loginCheckInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginCheckInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns(
                    "/login", "/signup",
                    "/css/**", "/js/**", "/img/**"
                );
    }
}

// === Controller 사용 ===
@Controller
public class BoardController {

    @LoginRequired                                   // ← 보호
    @PostMapping("/board")
    public String create(@ModelAttribute BoardDto dto) {
        boardService.create(dto);
        return "redirect:/board/list";
    }

    // @LoginRequired 없음 - 비로그인 접근 가능
    @GetMapping("/board/{id}")
    public String detail(@PathVariable int id) {
        return "board/detail";
    }
}
```

---

## 15. 실전 패턴 / 자주 빠지는 함정

### Filter
- ❌ `@Component` 만 붙이고 등록 안 함 → 모든 URL 에 적용되어 의도와 다름 ✅ `FilterRegistrationBean` 으로 명시
- ❌ `chain.doFilter()` 호출 누락 → 요청이 막혀서 빈 응답 ✅ 통과시킬 땐 반드시 호출
- ❌ Filter 안에서 Spring Bean 주입 안 됨 → `@Autowired` 누락 ✅ Spring 이 관리하는 Filter (`@Component`) 로

### Interceptor
- ❌ `preHandle` 에서 `false` 반환 후 응답 안 보냄 → 빈 응답 ✅ redirect·401 등 직접 응답
- ❌ `HandlerMethod` 가드 안 함 → 정적 리소스에서 ClassCastException ✅ `instanceof` 체크
- ❌ Interceptor 안에서 비즈니스 로직 처리 ✅ 검증·로깅만, 비즈니스는 Service 로
- ❌ 다중 Interceptor 의 순서 가정 안 함 ✅ `order()` 명시
- ❌ 정적 리소스를 excludePathPatterns 에 안 넣어 무한 리다이렉트 ✅ `/css/**`, `/js/**`, `/img/**` 제외

### Filter vs Interceptor 선택
- ❌ Filter 에서 Spring 의 `HandlerMethod` 접근 시도 → 불가 ✅ Interceptor 사용
- ❌ Interceptor 에서 응답 body 변환 시도 → 어려움 ✅ Filter Wrapper 사용
- ❌ 인코딩 설정을 Interceptor 에서 → 이미 처리된 후 ✅ Filter (`CharacterEncodingFilter`)

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| Interceptor 가 정적 리소스 요청도 잡음 | `addPathPatterns("/**")` 만 사용 | `excludePathPatterns` 추가 |
| `preHandle` 에서 `false` 반환했는데 응답 없음 | 응답 작성 누락 | redirect 또는 setStatus + body |
| Filter 안에서 `@Autowired` null | Filter 가 컨테이너 밖에서 생성 | `@Component` + `FilterRegistrationBean` |
| 다중 Interceptor 순서가 이상 | `order` 미지정 | 명시적 order |
| `HandlerInterceptor.postHandle` 이 `@ResponseBody` 메서드에서 안 호출 | 응답이 이미 writer 에 쓰여짐 | postHandle 대신 Filter Wrapper 또는 `ResponseBodyAdvice` |
| 무한 리다이렉트 | `/login` 이 excludePathPatterns 에 없음 | 제외 추가 |

---

## 16. 자가점검

1. Filter 와 Interceptor 의 가장 큰 위치 차이는?
2. Filter Chain 에서 `chain.doFilter()` 를 호출 안 하면?
3. HandlerInterceptor 의 3가지 메서드와 각 시점?
4. `preHandle` 이 `false` 를 반환하면?
5. 다중 Interceptor 의 실행 순서 패턴은?
6. Filter, Interceptor, AOP 의 선택 기준?
7. `HandlerMethod` 가드 (`instanceof`) 를 왜 인터셉터에서 자주 쓰나?

<details><summary>풀이</summary>

1. **Filter 는 DispatcherServlet 밖**(서블릿 컨테이너 관리), **Interceptor 는 DispatcherServlet 안**(Spring MVC 관리). 그래서 Filter 가 더 낮은 층, Interceptor 가 더 높은 층.
2. **요청이 다음 필터/컨트롤러로 전달 안 됨** → 빈 응답이 나가거나 사용자 응답 없음. 인증 실패 시 의도적으로 안 호출하기도 함 (응답은 직접 작성).
3. **`preHandle`** (Controller 실행 전) / **`postHandle`** (Controller 실행 후, View 렌더 전) / **`afterCompletion`** (View 렌더 후, 예외 발생해도).
4. **Controller 가 실행되지 않음**. 응답을 인터셉터에서 직접 작성해야 함 (안 하면 빈 응답).
5. **`preHandle` 은 등록 순, `postHandle`/`afterCompletion` 은 역순** (스택처럼). L1→L2→L3 preHandle 후 Controller, L3→L2→L1 postHandle.
6. **HTTP 레벨 (인코딩·CORS·로깅)** = Filter / **Controller 레벨 (권한·model)** = Interceptor / **Service·DAO 레벨 (트랜잭션·캐시)** = AOP.
7. **정적 리소스 요청** (`/css/`, `/js/` 등) 에선 handler 가 `ResourceHttpRequestHandler` 등 `HandlerMethod` 가 아닌 다른 타입. 이를 캐스팅 시도하면 `ClassCastException`. `instanceof` 로 가드.

</details>

---

## 17. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.4 표지·TOC·학습목표 | 들어가기 전에 |
| p.5 ~ p.9 Filter (개념·Chain·구현) | §1 ~ §5 (Part A) |
| p.10 ~ p.14 Filter 실습 | §3, §4 (Part A 적용) |
| p.15 ~ p.24 Interceptor (개념·HandlerInterceptor·등록) | §6 ~ §10 (Part B) |
| p.25 ~ p.29 Filter vs Interceptor 비교 | §11, §12 (Part C) |
| p.30 ~ p.32 Interceptor 실습 (다중 등록) | §9, §14 |
| p.33 마무리 | (생략) |

_33p 슬라이드 모두 커버._
