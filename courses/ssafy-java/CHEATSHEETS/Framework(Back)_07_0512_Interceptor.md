# Interceptor — 치트시트

> 33p 슬라이드 · Spring 의 컨트롤러 진입 전후 가로채기.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Interceptor** = DispatcherServlet 안, Controller 진입 직전·후 가로채기
2. **3 메서드**: `preHandle` (전, false 면 차단) / `postHandle` (후, View 전) / `afterCompletion` (View 까지 끝난 후)
3. **Filter vs Interceptor**: Filter 는 Servlet 표준 (앞단, Spring 객체 X), Interceptor 는 Spring MVC (HandlerMethod 접근)
4. **인증·로깅·권한** 의 대표적 위치 (특히 인증)
5. **`WebMvcConfigurer.addInterceptors()`** 로 등록 + `addPathPatterns` / `excludePathPatterns`
6. **`@AdminOnly` 어노테이션 + HandlerMethod.getMethodAnnotation()** 으로 메서드별 권한

## 가장 중요한 코드 3개

```java
// (1) JWT 인증 Interceptor
@Component
@RequiredArgsConstructor
public class JwtAuthInterceptor implements HandlerInterceptor {

    private final JwtParser jwt;

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        if (!(handler instanceof HandlerMethod hm)) return true;
        if (hm.hasMethodAnnotation(Public.class)) return true;       // @Public 통과

        String header = req.getHeader("Authorization");
        if (header == null || !header.startsWith("Bearer ")) {
            res.setStatus(401);
            return false;                                            // 차단
        }
        try {
            User user = jwt.parse(header.substring(7));
            req.setAttribute("loginUser", user);
            return true;
        } catch (JwtException e) {
            res.setStatus(401);
            return false;
        }
    }
}
```

```java
// (2) 등록
@Configuration
@RequiredArgsConstructor
public class WebMvcConfig implements WebMvcConfigurer {

    private final JwtAuthInterceptor jwtInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(jwtInterceptor)
            .addPathPatterns("/api/**")
            .excludePathPatterns("/api/auth/**", "/api/public/**")
            .order(1);
    }
}
```

```java
// (3) 권한 확인 (@AdminOnly 어노테이션)
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface AdminOnly {}

@Component
public class RoleInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        if (!(handler instanceof HandlerMethod hm)) return true;
        if (!hm.hasMethodAnnotation(AdminOnly.class)) return true;

        User user = (User) req.getAttribute("loginUser");
        if (user == null || !user.isAdmin()) {
            res.setStatus(403);
            return false;
        }
        return true;
    }
}

// 사용
@DeleteMapping("/{id}")
@AdminOnly
public ResponseEntity<Void> delete(@PathVariable long id) { ... }
```

## 면접 한 줄 답변
- **Filter vs Interceptor?** → Filter 는 Servlet 표준 (앞단, Spring Bean 접근 X), Interceptor 는 Spring MVC (HandlerMethod 접근 + DI).
- **3 메서드의 시점?** → preHandle (전, false 면 차단) / postHandle (Controller 후 View 전) / afterCompletion (View 까지 끝난 후, 항상).
- **Interceptor 의 흔한 용도?** → 인증, 권한, 로깅, 요청 ID 발급, MDC 설정.
- **Spring Security 와 Interceptor?** → Security 는 Filter 기반. Interceptor 는 비즈니스 인증 (Security 없이) 또는 추가 가공.

---

# 2. Quick Reference (실무 복붙)

## HandlerInterceptor 인터페이스

```java
public interface HandlerInterceptor {

    // Controller 진입 전 (false 면 진입 차단)
    default boolean preHandle(HttpServletRequest req, HttpServletResponse res,
                               Object handler) throws Exception {
        return true;
    }

    // Controller 종료 후, View 렌더 전
    default void postHandle(HttpServletRequest req, HttpServletResponse res,
                             Object handler, ModelAndView modelAndView) throws Exception { }

    // View 렌더까지 끝난 후 (예외 발생해도 호출)
    default void afterCompletion(HttpServletRequest req, HttpServletResponse res,
                                  Object handler, Exception ex) throws Exception { }
}
```

## 3 메서드의 시점

```
[Request]
   ↓
[Filter]
   ↓
[DispatcherServlet]
   ↓
[preHandle]                    <- 1
   ↓ true 면 진행
[Controller]
   ↓
[postHandle]                   <- 2 (Controller 후, View 전)
   ↓
[View 렌더]
   ↓
[afterCompletion]              <- 3 (항상 호출, 예외 발생 시에도)
   ↓
[Response]
```

## 등록 (WebMvcConfigurer)

```java
@Configuration
@RequiredArgsConstructor
public class WebMvcConfig implements WebMvcConfigurer {

    private final AuthInterceptor authInterceptor;
    private final LoggingInterceptor loggingInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 로깅 (모든 요청)
        registry.addInterceptor(loggingInterceptor)
            .addPathPatterns("/**")
            .order(1);

        // 인증 (API 만)
        registry.addInterceptor(authInterceptor)
            .addPathPatterns("/api/**")
            .excludePathPatterns(
                "/api/auth/**",         // 로그인·가입
                "/api/public/**",       // 공개 API
                "/static/**", "/error", "/favicon.ico"
            )
            .order(2);
    }
}
```

## HandlerMethod 활용

```java
@Override
public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
    if (!(handler instanceof HandlerMethod hm)) return true;
    // 정적 자원 등은 HandlerMethod 가 아님

    // 메서드 어노테이션
    if (hm.hasMethodAnnotation(Public.class)) return true;
    AdminOnly admin = hm.getMethodAnnotation(AdminOnly.class);
    if (admin != null) {
        // 권한 체크
    }

    // 클래스 어노테이션
    if (hm.getBeanType().isAnnotationPresent(RestController.class)) {
        // REST API 면 JSON 응답
    }

    // 메서드 정보
    String methodName = hm.getMethod().getName();
    Class<?> beanType = hm.getBeanType();

    return true;
}
```

## 요청 ID + MDC (로그 추적)

```java
@Component
@Slf4j
public class RequestIdInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        String requestId = UUID.randomUUID().toString().substring(0, 8);
        MDC.put("requestId", requestId);                   // 로그 패턴에 자동 포함
        req.setAttribute("requestId", requestId);
        res.setHeader("X-Request-ID", requestId);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest req, HttpServletResponse res,
                                Object handler, Exception ex) {
        MDC.clear();
    }
}
```

```yaml
# logback - MDC 변수 사용
logging.pattern.console: "%d{HH:mm:ss} [%X{requestId}] %-5level %logger - %msg%n"
```

## 시간 측정 + 슬로 알람

```java
@Component @Slf4j
public class TimingInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        req.setAttribute("startTime", System.currentTimeMillis());
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest req, HttpServletResponse res,
                                 Object handler, Exception ex) {
        long start = (long) req.getAttribute("startTime");
        long elapsed = System.currentTimeMillis() - start;
        if (elapsed > 1000) {
            log.warn("SLOW: {} {} - {}ms", req.getMethod(), req.getRequestURI(), elapsed);
        }
    }
}
```

## Filter vs Interceptor

| | Filter | Interceptor |
|--|--|--|
| **표준** | Servlet (`javax.servlet`) | Spring MVC |
| **위치** | DispatcherServlet 앞 | DispatcherServlet 안 |
| **HandlerMethod 접근** | X (raw 요청) | O (어노테이션·메서드) |
| **Spring DI** | (Boot 의 `FilterRegistrationBean` 사용) | 자연스러움 |
| **비동기·정적 자원** | 영향 받음 | DispatcherServlet 경유만 |
| **용도** | 인코딩·CORS·CSRF (Security) | 인증·로깅·MDC |

→ **둘 다 인증 가능**. 토큰 검증은 Filter (Security 기본), 비즈니스 권한은 Interceptor.

## @AuthenticationPrincipal 패턴 (커스텀)

```java
// Interceptor 에서 req.setAttribute("loginUser", user)
// Controller 에서 직접 받기

@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface LoginUser {}

@Component
public class LoginUserResolver implements HandlerMethodArgumentResolver {

    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        return parameter.hasParameterAnnotation(LoginUser.class)
            && parameter.getParameterType().equals(User.class);
    }

    @Override
    public Object resolveArgument(MethodParameter param, ModelAndViewContainer mavc,
                                   NativeWebRequest req, WebDataBinderFactory df) {
        HttpServletRequest httpReq = req.getNativeRequest(HttpServletRequest.class);
        return httpReq.getAttribute("loginUser");
    }
}

// 등록
@Override
public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
    resolvers.add(loginUserResolver);
}

// 사용
@GetMapping("/mypage")
public ResponseEntity<User> mypage(@LoginUser User user) {
    return ResponseEntity.ok(user);
}
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `preHandle` 에서 false 반환 안 함 → 차단 안 됨 | `return false` + 응답 작성 |
| HandlerMethod 캐스팅 누락 | `instanceof HandlerMethod` 체크 |
| MDC.clear() 누락 → 스레드 풀에서 누수 | `afterCompletion` 에서 clear |
| Path 패턴 `/api/**` 인데 `excludePathPatterns` 누락 → 로그인 자체도 차단 | `/api/auth/**` 제외 |
| Interceptor 빈 등록 안 함 | `@Component` 또는 직접 new |
| Filter 와 Interceptor 둘 다 인증 | 한 곳만 (보통 Spring Security) |
| afterCompletion 의 ex 활용 X | 에러 로깅에 활용 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Interceptor (33p)
│
├── [A] HandlerInterceptor
│   ├── preHandle (전, boolean)
│   ├── postHandle (Controller 후, View 전)
│   └── afterCompletion (전체 끝)
│
├── [B] 등록
│   ├── WebMvcConfigurer.addInterceptors
│   ├── addPathPatterns / excludePathPatterns
│   ├── order (순서)
│   └── 빈 주입 (DI)
│
├── [C] HandlerMethod 활용
│   ├── hm.getMethodAnnotation(X.class)
│   ├── hm.hasMethodAnnotation(X.class)
│   ├── hm.getBeanType()
│   └── 정적 자원 구분
│
├── [D] 주요 용도
│   ├── 인증 (JWT, Session)
│   ├── 권한 (@AdminOnly)
│   ├── 로깅 (요청 ID, 시간 측정)
│   ├── MDC (로그 추적)
│   └── 트래픽 통계
│
├── [E] 차단·통과
│   ├── return true (통과)
│   ├── return false + 응답 (차단)
│   └── 응답 상태 (401, 403)
│
├── [F] ArgumentResolver 패턴
│   ├── @LoginUser 커스텀
│   ├── 인터셉터의 attribute → 메서드 인자
│   └── @AuthenticationPrincipal 흉내
│
└── [G] vs Filter
    ├── Filter: Servlet 표준 (앞)
    ├── Interceptor: Spring MVC (안)
    └── 선택 기준
```

## 학습 진도 체크리스트

### A. 기본
- [ ] HandlerInterceptor 의 3 메서드
- [ ] preHandle false 반환 효과
- [ ] afterCompletion 의 ex 인자

### B. 등록
- [ ] WebMvcConfigurer 구현
- [ ] addPathPatterns + excludePathPatterns
- [ ] order 로 순서 제어

### C. HandlerMethod
- [ ] HandlerMethod 캐스팅
- [ ] 메서드 어노테이션 조회
- [ ] @AdminOnly 커스텀 어노테이션

### D. 실무
- [ ] JWT 인증 Interceptor
- [ ] 요청 ID + MDC
- [ ] 슬로 알람 (시간 측정)

### E. ArgumentResolver
- [ ] @LoginUser 커스텀
- [ ] HandlerMethodArgumentResolver
- [ ] req.attribute → 메서드 인자

### F. 비교
- [ ] Filter vs Interceptor 선택
- [ ] Spring Security 와 통합

## 연관 강의

```
5강 MVC1            -> Controller
6강 MVC2            -> 예외 처리
7강 Interceptor     <- 현재 위치
8강 MyBatis         -> Mapper
11강 종합 실습      -> 통합
12강 REST API       -> 인증
```

→ 다음 (MyBatis) 에서 **SQL 매퍼 + Spring 통합**.
