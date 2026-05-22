# Filter (Listener · Filter · Exception) — 퀴즈

> 14문항. 개념·적용·디버그·면접.

---

### Q1. (개념) Listener·Filter·Interceptor 의 위치 차이?

<details><summary>정답</summary>

- **Listener**: 이벤트 감지 (앱 시작·세션·요청 생명주기). 서블릿 컨테이너 영역.
- **Filter**: DispatcherServlet **밖** (서블릿 컨테이너). 모든 요청 가로채기.
- **Interceptor**: DispatcherServlet **안** (Spring MVC). Controller 핸들러 호출 전후.

Filter 가 가장 낮은 층, Interceptor 가 가장 높은 층.

</details>

### Q2. (개념) `ServletContextListener` 의 두 메서드와 각 시점?

<details><summary>정답</summary>

- `contextInitialized(ServletContextEvent)` - **앱 시작 시 1번**. DB 풀 초기화, 캐시 워밍, 외부 서비스 연결.
- `contextDestroyed(ServletContextEvent)` - **앱 종료 시 1번**. 자원 해제, 진행 중 작업 cleanup.

</details>

### Q3. (적용) 활성 세션 수를 추적하는 `HttpSessionListener` 작성.

<details><summary>정답</summary>

```java
@WebListener
public class SessionCounter implements HttpSessionListener {
    private static final AtomicInteger active = new AtomicInteger(0);

    @Override
    public void sessionCreated(HttpSessionEvent se) {
        se.getSession().getServletContext()
          .setAttribute("activeSessions", active.incrementAndGet());
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        se.getSession().getServletContext()
          .setAttribute("activeSessions", active.decrementAndGet());
    }
}
```

JSP 에서 `${applicationScope.activeSessions}` 로 접근.

</details>

### Q4. (개념) Filter Chain 에서 `chain.doFilter()` 를 호출하지 않으면?

<details><summary>정답</summary>

**요청이 다음 필터/서블릿으로 안 감** → 빈 응답 또는 사용자에게 응답 없음.

인증 실패 시 의도적으로 호출 안 함 + 직접 응답:
```java
res.sendRedirect("/login");
return;     // chain.doFilter() 호출 안 함
```

</details>

### Q5. (적용) 모든 요청에 UTF-8 인코딩을 적용하는 Filter?

<details><summary>정답</summary>

```java
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

또는 Spring 의 `CharacterEncodingFilter` 가 표준.

</details>

### Q6. (적용) `/admin/*` 경로 접근 시 ADMIN 권한만 통과시키는 Filter?

<details><summary>정답</summary>

```java
@WebFilter("/admin/*")
public class AdminAuthFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        HttpSession session = req.getSession(false);
        User user = (session != null) ? (User) session.getAttribute("loginUser") : null;

        if (user == null || !"ADMIN".equals(user.getRole())) {
            res.sendRedirect(req.getContextPath() + "/login");
            return;
        }
        chain.doFilter(request, response);
    }
}
```

</details>

### Q7. (개념) Filter 와 Interceptor 의 가장 큰 차이?

<details><summary>정답</summary>

- **Filter**: 서블릿 표준. DispatcherServlet **밖**. Spring 무관. 모든 요청·응답 객체 직접 다룸.
- **Interceptor**: Spring MVC. DispatcherServlet **안**. `HandlerMethod` 접근 가능. `@LoginRequired` 같은 어노테이션 검사.

선택 기준:
- HTTP 레벨 (인코딩·CORS·압축) → Filter
- Controller 레벨 (권한·model 추가) → Interceptor

</details>

### Q8. (디버그) `@WebFilter` 만으로 Filter 순서를 보장할 수 있나?

<details><summary>정답</summary>

**아니**. `@WebFilter` 만으로는 컨테이너 내부 정렬 규칙에 의존 → 예측 불가.

**명시적 순서 보장**:
- **web.xml** 의 `<filter-mapping>` 순서대로
- Spring Boot 의 **`FilterRegistrationBean.setOrder(int)`** (낮을수록 먼저)

</details>

### Q9. (적용) web.xml 로 404·500 에러 페이지 매핑.

<details><summary>정답</summary>

```xml
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

상태 코드 기반 + 예외 클래스 기반 동시 사용 가능.

</details>

### Q10. (디버그) 에러 페이지에서 `${exception.message}` 가 null. 원인?

<details><summary>정답</summary>

**`isErrorPage="true"` 누락**. JSP 가 일반 페이지로 인식되면 `exception` 기본 객체가 없음.

```jsp
<%@ page contentType="text/html;charset=UTF-8" isErrorPage="true" %>
```

이게 있으면 `${exception}`, `${exception.message}`, `${exception.stackTrace}` 접근 가능.

</details>

### Q11. (디버그) `<error-page>` 의 `<location>` 을 `/WEB-INF/error/500.jsp` 로 했더니 forward 안 됨. 원인?

<details><summary>정답</summary>

**`WEB-INF/` 안 자원은 외부에서 직접 접근 불가** - 에러 페이지로 forward 자체는 가능하지만, **에러 페이지 안의 정적 리소스 (`/css/*`)** 들이 같이 매핑돼서 깨질 수 있음.

해결: 에러 페이지를 `/error/500.jsp` (webroot 직접 자식) 에 두기.

</details>

### Q12. (디버그) Filter 안에서 `@Autowired private UserService userService` 가 null. 원인?

<details><summary>정답</summary>

Filter 가 **Spring 컨테이너 밖에서 생성** 되면 DI 안 됨.

**해결**:
1. **`@Component` 추가**:
   ```java
   @Component
   @WebFilter("/*")
   public class MyFilter implements Filter {
       @Autowired private UserService userService;
   }
   ```

2. **`FilterRegistrationBean` 으로 등록** - Spring 이 빈 생성 후 등록:
   ```java
   @Bean
   public FilterRegistrationBean<MyFilter> myFilter(MyFilter filter) {
       FilterRegistrationBean<MyFilter> reg = new FilterRegistrationBean<>();
       reg.setFilter(filter);
       return reg;
   }
   ```

</details>

### Q13. (면접) "Spring 환경에서도 Filter 가 필요한 경우는?"

<details><summary>정답</summary>

Spring 의 Interceptor·`@ControllerAdvice` 로 처리 못 하는 경우:

1. **DispatcherServlet 이전 처리** - CORS, 인코딩, Gzip 압축, 보안 헤더
2. **응답 body 변환** - Interceptor 는 응답 body 못 만짐. Filter Wrapper 로 가능
3. **Spring Security** - 자체가 Filter Chain 으로 구현됨. 인증·인가가 Spring MVC 진입 전 처리되어야 함
4. **요청 body 여러 번 읽기** - `HttpServletRequestWrapper` 로 캐싱
5. **모든 요청에 공통 (Spring 무관 자원 포함)** - 정적 리소스도 포함하려면 Interceptor 보다 Filter

</details>

### Q14. (면접) "Listener·Filter·Exception 처리·Interceptor·AOP 의 사용 시점을 모두 정리하시오."

<details><summary>정답</summary>

```
[요청 도착]
    |
    ▼
Listener (앱 라이프사이클·세션 이벤트 감지)
    |
    ▼
Filter (HTTP 레벨 - 인코딩·CORS·보안)
    |
    ▼
DispatcherServlet
    |
    ▼
Interceptor (Controller 레벨 - 권한·model)
    |
    ▼
Controller
    | AOP (메서드 레벨 - 트랜잭션·로깅)
    ▼
Service
    | AOP (트랜잭션·캐시)
    ▼
DAO
    |
    ▼
[예외 발생 시]
    ↓
@ControllerAdvice (Spring) 또는 web.xml <error-page> (Servlet)
```

각 레벨이 자기 책임만 처리하면 변경에 강한 시스템.

</details>
