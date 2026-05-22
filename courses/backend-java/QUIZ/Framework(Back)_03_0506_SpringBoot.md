# Spring Boot — 퀴즈

> 16문항. 개념·적용·디버그·면접. 4부(Mini MVC·Spring Boot 등장·프로젝트·JSP) 골고루.

---

## Part A. Mini MVC 원리

### Q1. (개념) FrontController 패턴이 풀어주는 본질적 문제는?

<details><summary>정답</summary>

매 페이지마다 서블릿을 새로 만들고 `web.xml` 에 매핑하는 중복. 모든 요청을 한 곳에서 받고 그 뒤에서 라우팅 → 공통 부가 처리(로깅·인증·인코딩) 를 한 곳에 통합.

</details>

### Q2. (적용) 다음 URL 추출 코드의 빈 칸을 채우시오.

```java
String uri         = ___;            // "/MVC_03day/hello"
String contextPath = ___;            // "/MVC_03day"
String path        = ___;            // "/hello"
```

<details><summary>정답</summary>

```java
String uri         = request.getRequestURI();
String contextPath = request.getContextPath();
String path        = uri.substring(contextPath.length());
```

</details>

### Q3. (개념) HandlerMapping 의 역할을 한 줄로?

<details><summary>정답</summary>

**URL → 처리할 Controller 매핑**. `/hello` 요청 시 `HelloController` 를 반환. Spring 의 `RequestMappingHandlerMapping` 은 `@RequestMapping` 어노테이션을 스캔해서 같은 역할을 자동화한 것.

</details>

### Q4. (개념) Controller 가 `HttpServlet` 을 상속하지 않고 인터페이스로 정의하는 이유?

<details><summary>정답</summary>

- 서블릿 상속의 무거움 제거 (`service`/`init`/`destroy` 등 강제 안 받음)
- 비즈니스 로직만 남음 → 테스트 가능 (서블릿 컨테이너 없이 호출)
- 다형성 활용 + Mock 주입 쉬움
- View forward 책임 분리 (Controller 는 view 이름만 반환)

</details>

### Q5. (적용) ViewResolver 가 없으면 Controller 가 추가로 작성해야 하는 코드는?

<details><summary>정답</summary>

```java
// ViewResolver 있을 때
return "hello";  // 끝

// ViewResolver 없을 때
req.setAttribute("...", ...);
req.getRequestDispatcher("/WEB-INF/views/hello.jsp")
   .forward(req, res);
return null;
```

실제 파일 경로를 직접 적고, `RequestDispatcher` 로 forward 직접 호출.

</details>

---

## Part B. Spring Boot 등장

### Q6. (개념) Spring Boot 의 4가지 자동화 핵심은?

<details><summary>정답</summary>

1. **자동 설정 (Auto-configuration)** — 클래스패스 라이브러리 보고 기본 설정 적용
2. **Starter 의존성** — `spring-boot-starter-web` 한 줄로 MVC+Tomcat+Jackson 자동
3. **내장 서버** — jar 안 톰캣, `java -jar` 로 실행
4. **Production Ready** — actuator 로 health/metrics/env 즉시 노출

</details>

### Q7. (개념) `@SpringBootApplication` 안에 포함된 3가지 어노테이션과 각 역할?

<details><summary>정답</summary>

| 어노테이션 | 역할 |
|--|--|
| `@Configuration` | 자바 설정 클래스로 인식 |
| `@EnableAutoConfiguration` | 자동 설정 활성화 (라이브러리 보고 기본 설정 적용) |
| `@ComponentScan` | 같은 패키지부터 컴포넌트 스캔 |

이 3가지 덕분에 한 줄로 Spring 컨테이너·Web·자동 설정이 모두 시작됨.

</details>

### Q8. (면접) "Spring Boot 는 새로운 프레임워크인가요?"

<details><summary>정답</summary>

**아니다**. Spring Boot 는 Spring Framework 를 더 쉽게 쓰게 해주는 **개발 도구·메타 프레임워크**. 내부적으로 Spring 의 IoC 컨테이너·DI·AOP·MVC 가 그대로 작동. Spring Boot 는 거기에 자동 설정 + starter + 내장 서버 + 운영 도구를 묶은 패키지.

원리(DI/AOP/PSA) 를 모르고 Spring Boot 만 쓰면 트러블슈팅이 막힘.

</details>

---

## Part C. 프로젝트 생성·실행

### Q9. (개념) start.spring.io 의 핵심 starter 5가지와 각 포함 내용?

<details><summary>정답</summary>

| starter | 포함 |
|--|--|
| `spring-boot-starter-web` | Spring MVC + 내장 Tomcat + Jackson |
| `spring-boot-starter-data-jpa` | Spring Data JPA + Hibernate + JDBC |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-test` | JUnit + Mockito + AssertJ + Spring Test |
| `spring-boot-starter-actuator` | 운영 모니터링 엔드포인트 |

</details>

### Q10. (적용) Spring Boot 애플리케이션을 실행하는 방법 3가지?

<details><summary>정답</summary>

1. **IDE**: 메인 클래스 우클릭 → Run As → Spring Boot App
2. **Maven**: `mvn spring-boot:run`
3. **jar**: `mvn package` → `java -jar target/demo-0.0.1-SNAPSHOT.jar`

배포는 1, 2 는 개발용, 3 이 운영용.

</details>

### Q11. (디버그) Spring Boot 가 기동했는데 `@Controller` 가 등록 안 됨. 원인 후보?

<details><summary>정답</summary>

1. **`@SpringBootApplication` 의 패키지 위치가 너무 깊음** — 컴포넌트 스캔이 같은 패키지 + 하위만 스캔. 메인 클래스를 루트 패키지로 이동
2. **`@Controller` 누락** — 클래스에 어노테이션 부착
3. **다른 `@ComponentScan` 이 범위 좁힘** — `basePackages` 확인

</details>

---

## Part D. JSP 사용

### Q12. (개념) Spring Boot 에서 JSP 를 쓰려면 추가해야 할 의존성과 그 이유?

<details><summary>정답</summary>

**`tomcat-embed-jasper`** — JSP 컴파일 엔진. Spring Boot 의 내장 톰캣은 기본적으로 servlet 만 지원, JSP 를 .java → .class 로 컴파일하는 jasper 가 별도 필요.

추가로 JSTL 쓰면:
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

</details>

### Q13. (적용) `application.properties` 에 ViewResolver 설정?

<details><summary>정답</summary>

```properties
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
```

→ Controller 의 `return "hello"` 가 `/WEB-INF/views/hello.jsp` 로 변환.

</details>

### Q14. (디버그) `@Controller` 로 만들었는데 JSP 가 안 보이고 문자열 그대로 출력 (예: 응답 본문에 "hello" 가 보임). 원인?

<details><summary>정답</summary>

가능한 원인:

1. **`@RestController` 로 잘못 만듦** — `@RestController` = `@Controller` + `@ResponseBody` → 반환값을 JSON/문자열로 직렬화
2. **메서드에 `@ResponseBody` 가 붙어있음**
3. **ViewResolver 미설정** — Spring Boot 가 view 이름을 못 찾아 그대로 출력

해결: `@Controller` 로 변경, `@ResponseBody` 제거, `spring.mvc.view.prefix/suffix` 추가.

</details>

### Q15. (디버그) JSP 파일을 만들었는데 404. 위치를 어디 둬야 하나?

<details><summary>정답</summary>

`src/main/webapp/WEB-INF/views/hello.jsp` (Spring Boot 의 JSP 관습 경로).

`static/` 이나 `resources/` 에 두면 안 됨. **`WEB-INF/`** 아래에 두는 이유:
- 직접 URL 접근 차단 (보안)
- Controller 를 통해서만 접근 가능

추가 함정: jar 패키징 시 `webapp/` 이 포함 안 되므로 **war 패키징** 또는 `<packaging>war</packaging>` 필요.

</details>

### Q16. (면접) "`@Controller` 와 `@RestController` 의 차이를 한 페이지에서 같이 쓸 수 있나요?"

<details><summary>정답</summary>

**같이 쓸 수 있고, 흔히 쓴다**.

```java
@Controller                              // JSP 렌더용
public class HomeController {

    @GetMapping("/home")
    public String home(Model m) {
        m.addAttribute("title", "홈");
        return "home";                   // → home.jsp
    }
}

@RestController                          // JSON API 용
@RequestMapping("/api")
public class ApiController {

    @GetMapping("/users")
    public List<User> users() {
        return userService.list();       // → JSON
    }
}
```

또는 한 컨트롤러 안에서 메서드별 분기:

```java
@Controller
public class MixedController {

    @GetMapping("/page")
    public String page() { return "page"; }    // JSP

    @GetMapping("/api/data")
    @ResponseBody                              // 이 메서드만 JSON
    public Map<String, String> data() { return Map.of("k", "v"); }
}
```

권장: 책임 분리 — JSP 컨트롤러는 `@Controller`, API 는 `@RestController` 로 별도 클래스.

</details>
