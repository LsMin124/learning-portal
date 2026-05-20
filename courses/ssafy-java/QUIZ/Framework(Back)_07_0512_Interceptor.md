# Filter & Interceptor — 퀴즈

> 15문항. 개념·적용·디버그·면접. 3부(Filter·Interceptor·Filter vs Interceptor) 골고루.

---

## Part A. Filter

### Q1. (개념) Filter 와 Interceptor 의 가장 큰 위치 차이는?

<details><summary>정답</summary>

- **Filter**: DispatcherServlet **밖** — 서블릿 컨테이너(Tomcat) 가 관리. Spring 무관.
- **Interceptor**: DispatcherServlet **안** — Spring MVC 가 관리.

Filter 가 더 낮은 층 (HTTP 직접), Interceptor 가 더 높은 층 (Controller 접근 가능).

</details>

### Q2. (개념) Filter Chain 에서 `chain.doFilter()` 를 호출하지 않으면?

<details><summary>정답</summary>

**요청이 다음 필터/컨트롤러로 전달 안 됨** → 빈 응답 또는 사용자에게 응답 없음.

인증 실패 시 의도적으로 안 호출하기도 하지만, 그 경우 인터셉터에서 직접 응답(`response.sendRedirect` 또는 `response.setStatus`) 을 작성해야 함.

</details>

### Q3. (적용) 요청 처리 시간을 로깅하는 Filter 를 작성하시오.

<details><summary>정답</summary>

```java
@Component
public class TimingFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                          ServletResponse response,
                          FilterChain chain) throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        long start = System.currentTimeMillis();

        chain.doFilter(request, response);   // ⚠ 반드시 호출

        long elapsed = System.currentTimeMillis() - start;
        System.out.println(req.getRequestURI() + " " + elapsed + " ms");
    }
}
```

`doFilter` 의 try/finally 로 예외 발생 시에도 측정하면 더 안전.

</details>

### Q4. (개념) Filter 의 3가지 생명주기 메서드와 각 시점?

<details><summary>정답</summary>

- **`init(FilterConfig)`** — 컨테이너 기동 시 **1번**. 초기 설정 로드.
- **`doFilter(req, res, chain)`** — **매 요청마다**. 실제 동작.
- **`destroy()`** — 컨테이너 종료 시 **1번**. 자원 정리.

`init`/`destroy` 는 default 메서드라 필수 아님.

</details>

### Q5. (적용) Spring Boot 에서 Filter 를 특정 URL 패턴에만 등록하는 방법?

<details><summary>정답</summary>

**`FilterRegistrationBean`** 권장:

```java
@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<TimingFilter> timingFilter() {
        FilterRegistrationBean<TimingFilter> reg = new FilterRegistrationBean<>();
        reg.setFilter(new TimingFilter());
        reg.addUrlPatterns("/api/*");      // 특정 패턴
        reg.setOrder(1);
        return reg;
    }
}
```

`@Component` 만 붙이면 `/*` 모든 URL 에 적용되어 의도와 다를 수 있음.

</details>

---

## Part B. Interceptor

### Q6. (개념) HandlerInterceptor 의 3가지 메서드와 각 시점?

<details><summary>정답</summary>

- **`preHandle`** — Controller 실행 **전**. `return true` 통과, `false` 차단.
- **`postHandle`** — Controller 실행 **후, View 렌더 전**. ModelAndView 수정 가능.
- **`afterCompletion`** — View 렌더 완료 후. **예외 발생해도 호출**. 자원 정리.

모두 default 메서드 — 필요한 것만 오버라이드.

</details>

### Q7. (적용) `WebMvcConfigurer` 에 Interceptor 를 등록하시오.

<details><summary>정답</summary>

```java
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final LoginCheckInterceptor loginCheckInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginCheckInterceptor)
                .addPathPatterns("/admin/**", "/mypage/**")
                .excludePathPatterns("/login", "/signup", "/css/**", "/js/**")
                .order(1);
    }
}
```

핵심 메서드: `addPathPatterns`, `excludePathPatterns`, `order`.

</details>

### Q8. (디버그) `preHandle` 이 `false` 를 반환했는데 빈 응답이 나감. 원인?

<details><summary>정답</summary>

`false` 반환 시 **Controller 가 실행되지 않으므로 응답을 누가도 안 보냄**. 인터셉터 안에서 직접 응답을 작성해야.

```java
@Override
public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
    if (notAuthenticated()) {
        res.sendRedirect("/login");          // 또는
        // res.setStatus(401);
        // res.getWriter().write("...");
        return false;
    }
    return true;
}
```

</details>

### Q9. (개념) 다중 Interceptor 의 실행 순서 패턴?

<details><summary>정답</summary>

**등록 순서대로 preHandle, 역순으로 postHandle / afterCompletion** (스택처럼).

```
등록: L1 → L2 → L3

preHandle:       L1 → L2 → L3
[Controller 실행]
postHandle:      L3 → L2 → L1   ← 역순
afterCompletion: L3 → L2 → L1   ← 역순
```

후속 인터셉터가 이전 인터셉터의 결과를 보고 추가 작업 가능.

</details>

### Q10. (적용) `@LoginRequired` 어노테이션이 붙은 메서드만 보호하는 인터셉터?

<details><summary>정답</summary>

```java
@Component
public class LoginCheckInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest req,
                              HttpServletResponse res,
                              Object handler) throws Exception {

        if (!(handler instanceof HandlerMethod)) return true;
        HandlerMethod hm = (HandlerMethod) handler;

        if (!hm.hasMethodAnnotation(LoginRequired.class)) return true;

        HttpSession session = req.getSession(false);
        if (session != null && session.getAttribute("loginUser") != null) {
            return true;
        }
        res.sendRedirect("/login");
        return false;
    }
}
```

핵심 가드:
1. `handler instanceof HandlerMethod` — 정적 리소스 통과
2. `hm.hasMethodAnnotation(...)` — 보호 대상 표시 확인

</details>

### Q11. (디버그) `HandlerMethod` 캐스팅에서 `ClassCastException` 발생. 원인?

<details><summary>정답</summary>

**정적 리소스 (`/css/`, `/js/`, `/img/`) 요청** 시 handler 가 `HandlerMethod` 가 아닌 `ResourceHttpRequestHandler` 등 다른 타입.

해결: `instanceof` 가드.

```java
if (!(handler instanceof HandlerMethod)) {
    return true;
}
HandlerMethod hm = (HandlerMethod) handler;
```

</details>

---

## Part C. Filter vs Interceptor

### Q12. (개념) Filter, Interceptor, AOP 의 선택 기준?

<details><summary>정답</summary>

| 메커니즘 | 위치 | 사용 사례 |
|--|--|--|
| **Filter** | 서블릿 컨테이너 | 인코딩, CORS, 로깅, Spring Security (HTTP 레벨) |
| **Interceptor** | Spring MVC | 권한 검사, 공통 model 추가, 로깅 (Controller 레벨) |
| **AOP** | 모든 메서드 | 트랜잭션, 캐시, 재시도 (Service/DAO 레벨) |

**선택 기준**: 가장 낮은 층(Filter) 부터 시작 → 필요한 정보가 있는 가장 가까운 층 선택.

</details>

### Q13. (디버그) Filter 안에서 `@Autowired private UserService userService;` 인데 null. 원인과 해결?

<details><summary>정답</summary>

Filter 가 **Spring 컨테이너 밖에서 생성** 되면 DI 안 됨. 해결:

1. **Filter 를 빈으로 등록**:
   ```java
   @Component
   public class MyFilter implements Filter {
       @Autowired private UserService userService;
   }
   ```

2. **`FilterRegistrationBean` 으로 등록**:
   ```java
   @Bean
   public FilterRegistrationBean<MyFilter> myFilter(MyFilter filter) {
       FilterRegistrationBean<MyFilter> reg = new FilterRegistrationBean<>();
       reg.setFilter(filter);  // 빈을 받아서 등록
       return reg;
   }
   ```

</details>

### Q14. (면접) "Interceptor 대신 AOP 를 쓸 수도 있나요? 차이는 뭔가요?"

<details><summary>정답</summary>

**둘 다 횡단 관심사 분리 도구이지만 다음 차이**:

| 항목 | Interceptor | AOP |
|--|--|--|
| 대상 | Controller 의 핸들러 메서드만 | 모든 Spring 빈의 메서드 (Controller·Service·DAO) |
| HTTP 정보 | 직접 접근 (Request/Response) | 안 접근 (메서드 인자만) |
| URL 패턴 | 직접 매칭 (`/admin/**`) | Pointcut 표현식 (`execution(...)`) |
| 응답 제어 | preHandle 의 false 로 차단 | Around 에서 proceed 안 하면 차단 |

**선택**:
- HTTP 요청·응답 객체가 필요하면 Interceptor
- 메서드 시그니처·인자·반환값만 필요하면 AOP
- 보통 Controller 레벨은 Interceptor, Service 레벨은 AOP 분담

</details>

### Q15. (면접) "Filter, Interceptor, AOP 를 모두 사용하는 로그인 시스템을 설계한다면?"

<details><summary>정답</summary>

각 레벨별 역할 분담:

```
요청
  │
  ▼
[Filter — Spring Security]   ← JWT 토큰 검증·SecurityContext 적재
  │
  ▼
[Interceptor — LoginCheckInterceptor]   ← URL 기반 추가 권한 (e.g., /admin/**)
  │
  ▼
[Controller]
  │
  ▼ AOP — @PreAuthorize         ← 메서드 단위 세밀한 권한 (역할 기반)
[Service.method()]
  │
  ▼ AOP — @Transactional        ← 트랜잭션
[DAO.method()]
  │
  ▼
DB
```

**역할 분담의 이점**:
- Filter: 인증(누가) — 모든 요청에 공통
- Interceptor: URL 기반 권한 (admin 페이지)
- AOP: 메서드 기반 권한 + 트랜잭션 (Service)

각 레벨이 자기 책임만 → 변경에 강하고 테스트 용이.

</details>
