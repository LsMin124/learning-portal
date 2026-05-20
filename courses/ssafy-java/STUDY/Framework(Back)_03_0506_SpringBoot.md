# Spring Boot — Legacy MVC 직접 구현 · Spring Boot 등장 · 프로젝트 · JSP

> **이 강의는 무엇인가**: Spring MVC 가 어떻게 동작하는지 **직접 미니 MVC 프레임워크를 만들어보고** (FrontController, HandlerMapping, Controller 인터페이스, ViewResolver), 그 복잡한 설정을 자동화한 **Spring Boot** 가 어떻게 "그냥 실행" 가능한 환경을 제공하는지, 그리고 Spring Boot 에서 JSP 로 웹 페이지를 띄우는 첫 실습.
> **왜 배우는가**: `@Controller` 한 줄로 라우팅이 되는 건 마법이 아니다. 그 뒤에 FrontController + HandlerMapping + ViewResolver 라는 패턴이 있고, Spring Boot 는 거기에 자동 설정 + 내장 서버 + 의존성 starter 를 붙인 것. 원리를 이해해야 트러블슈팅할 수 있다.

---

## 들어가기 전에

- **선수**: 서블릿 기본(`HttpServlet`, `doGet/doPost`), `web.xml`, JSP, Spring DI.
- **마인드셋**: "왜 매번 새 서블릿을 만들지 않는가" 라는 질문에서 출발. 모든 요청을 한 곳(FrontController) 으로 받고, 그 뒤에서 라우팅하는 게 핵심.

---

# Part A. Spring Legacy Web — Mini MVC 직접 구현

## 1. 왜 직접 만드는가

```
                Servlet 시대의 문제

   요청 1  → HelloServlet      → forward("/hello.jsp")
   요청 2  → ListServlet        → forward("/list.jsp")
   요청 3  → DetailServlet      → forward("/detail.jsp")
   요청 N  → ... 서블릿 N개 ...

   web.xml 에 매핑 N개. 공통 로직(로깅·인코딩·인증) 도 N번 작성.
   서블릿 = 비즈니스 로직 + view forward + 공통 부가 처리 한 곳에 섞임.
```

**Spring MVC 의 발상**:
- 모든 요청을 받는 **하나의 FrontController** (DispatcherServlet)
- URL 별로 처리할 객체를 매핑한 **HandlerMapping**
- 비즈니스 로직만 담는 **Controller 인터페이스**
- 뷰 이름을 실제 경로로 바꾸는 **ViewResolver**

이걸 직접 만들어보면 Spring MVC 가 그렇게 마법 같지 않다.

## 2. STEP 1 — URL 경로 추출

```java
String uri         = request.getRequestURI();       // "/MVC_03day/hello"
String contextPath = request.getContextPath();      // "/MVC_03day"
String path        = uri.substring(contextPath.length());  // "/hello"
```

| 메서드 | 의미 |
|--|--|
| `getRequestURI()` | 전체 URI (`/contextPath/path`) |
| `getContextPath()` | 컨텍스트 경로 (`/MVC_03day` 등) |
| 직접 substring | 실제 경로 추출 |

## 3. STEP 2 — FrontController + HandlerMapping

**FrontController** 하나로 모든 요청 통합:

```java
@WebServlet("/*")
public class DispatcherServlet extends HttpServlet {

    private final HandlerMapping mapping = new HandlerMapping();
    private final ViewResolver   vr      = new ViewResolver("/WEB-INF/views/", ".jsp");

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // ① URL 추출
        String path = req.getRequestURI().substring(req.getContextPath().length());

        // ② Controller 찾기
        Controller controller = mapping.getController(path);

        // ③ Controller 실행 → View 이름 반환
        String viewName = controller.handleRequest(req, res);

        // ④ ViewResolver 로 실제 경로 변환 → forward
        String viewPath = vr.resolve(viewName);
        req.getRequestDispatcher(viewPath).forward(req, res);
    }
}
```

**HandlerMapping** — URL → Controller 매핑:

```java
public class HandlerMapping {
    private final Map<String, Controller> map = new HashMap<>();

    public HandlerMapping() {
        map.put("/hello", new HelloController());
        map.put("/list",  new ListController());
    }

    public Controller getController(String path) {
        return map.get(path);
    }
}
```

## 4. STEP 3 — Controller 인터페이스 (서블릿 상속 탈출)

```java
public interface Controller {
    String handleRequest(HttpServletRequest req, HttpServletResponse res);
}

public class HelloController implements Controller {
    @Override
    public String handleRequest(HttpServletRequest req, HttpServletResponse res) {
        req.setAttribute("message", "Hello, World!");
        return "hello";   // 논리 view 이름 (확장자·경로 없음)
    }
}
```

**HttpServlet 상속에서 해방되며 얻는 것**:
- `service()`, `init()`, `destroy()`, `getServletConfig()` 등 안 써도 됨
- 비즈니스 로직만 남음 → 테스트 가능 (서블릿 컨테이너 없이 호출 가능)
- 인터페이스라 다형성 활용 + Mock 주입 쉬움

## 5. STEP 4 — ViewResolver (뷰 경로 자동화)

```java
public class ViewResolver {
    private final String prefix;
    private final String suffix;

    public ViewResolver(String prefix, String suffix) {
        this.prefix = prefix;   // "/WEB-INF/views/"
        this.suffix = suffix;   // ".jsp"
    }

    public String resolve(String viewName) {
        return prefix + viewName + suffix;
        // "hello" → "/WEB-INF/views/hello.jsp"
    }
}
```

**얻는 것**:
- Controller 는 `"hello"` 만 반환 → 실제 경로는 신경 안 씀
- 템플릿 엔진 변경 시 (`Thymeleaf`, `Mustache`) ViewResolver 만 교체

## 6. 미니 MVC 의 완성 흐름도

```
[요청 /hello] ---------->  DispatcherServlet
                              |
                              | ① URL 추출: "/hello"
                              ▼
                          HandlerMapping
                              | ② "/hello" → HelloController
                              ▼
                          HelloController
                              | ③ handleRequest() 실행
                              |   - 비즈니스 로직
                              |   - model.addAttribute
                              |   - return "hello"
                              ▼
                          ViewResolver
                              | ④ "hello" → "/WEB-INF/views/hello.jsp"
                              ▼
                          forward → hello.jsp 렌더
                              |
                              ▼
                          [응답 HTML]
```

> 이게 그대로 Spring MVC 의 동작. `DispatcherServlet` 도 정확히 이 일을 한다. `@Controller`, `@RequestMapping` 은 우리가 직접 HashMap 으로 만든 HandlerMapping 의 어노테이션 기반 자동화 버전.

---

# Part B. Spring Boot — 자동화의 자동화

## 7. Spring 의 복잡함

Spring 만 쓰면:
- `web.xml` 작성
- `applicationContext.xml` 설정
- DispatcherServlet 등록
- ViewResolver 설정
- DataSource·TransactionManager·HandlerMapping 빈 등록
- 톰캣 별도 설치 + 배포

→ **개발자 생산성 저하 + 디버깅 어려움 + 중복 코드**.

## 8. Spring Boot 의 핵심 가치

```
                Spring               Spring Boot
                -------              ------------
 설정             XML 100줄+          @SpringBootApplication 한 줄
 서버             톰캣 별도 설치       내장 (jar 실행만)
 의존성           버전 직접 명시       starter 가 자동 조합
 운영 도구        직접 구축           actuator 내장
```

**4가지 자동화**:
1. **자동 설정 (Auto-configuration)**: 클래스패스에 있는 라이브러리를 보고 기본 설정 적용
2. **Starter 의존성**: `spring-boot-starter-web` 한 줄로 Spring MVC + Tomcat + Jackson 등 자동
3. **내장 서버**: jar 안에 톰캣이 들어가서 `java -jar app.jar` 로 실행
4. **Production Ready**: actuator 로 health/metrics/env 등 즉시 노출

> **오해 금지**: Spring Boot 는 **새로운 프레임워크가 아니다**. Spring 을 "그냥 실행" 가능하게 해주는 도구.

## 9. "Just Run" 의 의미

```java
@SpringBootApplication
public class HelloSpringBootApplication {
    public static void main(String[] args) {
        SpringApplication.run(HelloSpringBootApplication.class, args);
    }
}
```

`main()` 한 줄로:
1. Spring Container 빌드
2. 내장 톰캣 8080 포트 기동
3. DispatcherServlet 등록
4. 컴포넌트 스캔 → 모든 `@Component` 등 빈 등록
5. 자동 설정 (DB, Jackson, Validation 등)

→ `java -jar app.jar` 또는 IDE 의 Run.

**`@SpringBootApplication` 안에 포함된 3가지**:
- `@Configuration` — 자바 설정 클래스로 인식
- `@EnableAutoConfiguration` — 자동 설정 활성화
- `@ComponentScan` — 같은 패키지부터 컴포넌트 스캔

---

# Part C. Spring Boot 프로젝트 생성

## 10. start.spring.io — Spring Initializr

```
https://start.spring.io/

[Project]      Maven / Gradle
[Language]     Java
[Spring Boot]  3.x.x (최신 안정)
[Project Metadata]
  Group:        com.example
  Artifact:     demo
  Name:         demo
  Package name: com.example.demo
  Packaging:    Jar / War
  Java:         17 / 21

[Dependencies] ADD DEPENDENCIES...
  ✓ Spring Web              ← MVC + Tomcat
  ✓ Spring Boot DevTools    ← 핫 리로드
  ✓ Lombok                  ← 보일러플레이트 제거
  ✓ Spring Data JPA / MyBatis Framework
  ✓ MySQL Driver

[GENERATE]    → demo.zip 다운로드
```

## 11. 핵심 starter 의존성 5종

| starter | 포함 |
|--|--|
| `spring-boot-starter-web` | Spring MVC + 내장 Tomcat + Jackson |
| `spring-boot-starter-data-jpa` | Spring Data JPA + Hibernate + JDBC |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-test` | JUnit + Mockito + AssertJ + Spring Test |
| `spring-boot-starter-actuator` | 운영 모니터링 엔드포인트 |

## 12. STS / IntelliJ 에서 프로젝트 생성

**STS (Spring Tool Suite)**:
- File → New → Spring Starter Project
- 위 화면과 동일한 form
- Finish → 자동으로 의존성 다운로드

**IntelliJ Ultimate**:
- File → New Project → Spring Initializr (내장 wizard 또는 web)
- Community 는 `start.spring.io` 에서 직접 다운로드 후 import

## 13. Spring Boot Project 디렉토리

```
demo/
+-- pom.xml                              ← Maven 설정
+-- src/
|   +-- main/
|   |   +-- java/
|   |   |   +-- com/example/demo/
|   |   |       +-- DemoApplication.java ← @SpringBootApplication
|   |   +-- resources/
|   |       +-- application.properties   ← 설정 (또는 .yml)
|   |       +-- static/                  ← CSS, JS, 이미지
|   |       +-- templates/               ← Thymeleaf 템플릿
|   +-- test/
|       +-- java/
+-- target/                              ← 빌드 결과 .jar
```

## 14. 실행 방법

| 방법 | 명령 |
|--|--|
| IDE | 메인 클래스 우클릭 → Run As → Spring Boot App |
| Maven | `mvn spring-boot:run` |
| jar | `mvn package` → `java -jar target/demo-0.0.1-SNAPSHOT.jar` |

기동 시 콘솔에 ASCII 배너 + `Started DemoApplication in N seconds`.

---

# Part D. Spring Boot 에서 JSP 사용

## 15. JSP 사용 시 추가 의존성

기본 Spring Boot 는 Thymeleaf 권장. JSP 쓰려면:

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.apache.tomcat.embed</groupId>
    <artifactId>tomcat-embed-jasper</artifactId>      <!-- JSP 엔진 -->
</dependency>
<dependency>
    <groupId>jakarta.servlet.jsp.jstl</groupId>
    <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
</dependency>
<dependency>
    <groupId>org.glassfish.web</groupId>
    <artifactId>jakarta.servlet.jsp.jstl</artifactId>
</dependency>
```

## 16. ViewResolver 설정 — `application.properties`

```properties
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
```

→ Controller 의 `return "hello"` 가 `/WEB-INF/views/hello.jsp` 로 변환.

## 17. HelloController 작성

```java
package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import jakarta.servlet.http.HttpServletRequest;

@Controller
public class HelloController {

    @GetMapping("/hello")
    public String hello(HttpServletRequest req) {
        req.setAttribute("message", "Hello, Spring Boot!");
        return "hello";   // → /WEB-INF/views/hello.jsp
    }
}
```

## 18. hello.jsp 작성

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head><title>Hello</title></head>
<body>
    <h1>${message}</h1>
</body>
</html>
```

위치: `src/main/webapp/WEB-INF/views/hello.jsp` (Spring Boot 의 JSP 관습 경로).

## 19. 등록된 Bean 확인 — ApplicationContext

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        ApplicationContext ctx = SpringApplication.run(DemoApplication.class, args);

        // 등록된 빈 이름 모두 출력
        for (String name : ctx.getBeanDefinitionNames()) {
            System.out.println(name);
        }
    }
}
```

기동 시 콘솔에 수십 개 빈 (Spring 의 내부 + 자동 설정 + 우리 빈) 모두 출력.

자주 보이는 자동 빈:
- `internalConfigurationAnnotationProcessor`
- `internalAutowiredAnnotationProcessor`
- `internalCommonAnnotationProcessor`
- `dispatcherServlet`
- `tomcatServletWebServerFactory`

이 빈들이 우리가 손대지 않아도 자동 설정의 결과로 등록되어 있다는 게 Spring Boot 의 핵심.

---

## 20. 코드 깊게 — 풀스택 Hello World

```java
// === Application 메인 ===
@SpringBootApplication
public class HelloApplication {
    public static void main(String[] args) {
        SpringApplication.run(HelloApplication.class, args);
    }
}

// === Controller ===
@Controller
@RequiredArgsConstructor
public class HelloController {

    @GetMapping("/")
    public String index() {
        return "redirect:/hello";
    }

    @GetMapping("/hello")
    public String hello(Model model) {
        model.addAttribute("message", "Hello, Spring Boot!");
        model.addAttribute("time",    LocalDateTime.now());
        return "hello";
    }

    @GetMapping("/api/greet")
    @ResponseBody
    public Map<String, String> greet() {
        return Map.of("greeting", "안녕하세요");
    }
}
```

```jsp
<!-- /WEB-INF/views/hello.jsp -->
<%@ page contentType="text/html;charset=UTF-8" %>
<html>
<head><title>${message}</title></head>
<body>
    <h1>${message}</h1>
    <p>now: ${time}</p>
    <a href="/api/greet">API 호출</a>
</body>
</html>
```

```properties
# application.properties
server.port=8080
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
spring.devtools.livereload.enabled=true
```

실행 → 브라우저 `http://localhost:8080/hello` → "Hello, Spring Boot!" + 시간.

---

## 21. 실전 패턴 / 자주 빠지는 함정

### Mini MVC / Spring MVC 원리
- ❌ 매 페이지마다 새 서블릿 + `web.xml` 매핑 ✅ FrontController 패턴
- ❌ Controller 가 `HttpServlet` 상속 ✅ Controller 인터페이스 (또는 `@Controller`)
- ❌ Controller 가 직접 `forward(jsp 경로)` ✅ 논리 view 이름 + ViewResolver

### Spring Boot
- ❌ Spring Boot 가 새 프레임워크라 생각 ✅ Spring 의 자동화 도구
- ❌ jar 와 war 패키징 차이 무시 ✅ jar = 내장 톰캣, war = 외부 WAS 배포
- ❌ `application.properties` 와 `application.yml` 혼용 ✅ 한 가지 선택 (yml 가독성 좋음)
- ❌ `@SpringBootApplication` 의 위치를 deep 패키지에 둠 → 컴포넌트 스캔 누락 ✅ **루트 패키지**에 두기

### JSP 사용 시
- ❌ JSP 파일을 `static/` 에 둠 ✅ `WEB-INF/views/` 에 (직접 URL 접근 차단)
- ❌ jar 패키징 + JSP 사용 → JSP 인식 안 됨 ✅ war 로 패키징 또는 `<packaging>war</packaging>`
- ❌ ViewResolver 설정 누락 → 404 ✅ `spring.mvc.view.prefix/suffix` 명시

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| 8080 포트 충돌 | 다른 프로세스가 사용 중 | `server.port=8081` 또는 `lsof -i :8080` 으로 종료 |
| 404 — `/hello` 안 잡힘 | `@GetMapping` 누락 또는 컴포넌트 스캔 범위 밖 | `@Controller` + 패키지 위치 확인 |
| JSP 가 텍스트로 출력 | jasper 의존성 누락 또는 ViewResolver 미설정 | `tomcat-embed-jasper` 추가 + `application.properties` |
| 기동은 됐는데 빈이 등록 안 됨 | `@SpringBootApplication` 이 패키지 깊이 있음 | 루트 패키지로 이동 |
| `@RestController` 가 JSP 안 렌더 | `@RestController` 는 `@ResponseBody` 포함 → 문자열 그대로 반환 | `@Controller` + 메서드별 `@ResponseBody` 분리 |
| `mvn spring-boot:run` 인데 변경 사항 반영 안 됨 | devtools 누락 | `spring-boot-devtools` 의존성 추가 |

---

## 22. 자가점검

1. FrontController 패턴이 풀어주는 본질적 문제는?
2. HandlerMapping 의 역할을 한 줄로?
3. ViewResolver 가 없으면 Controller 가 어떤 코드를 더 써야 하나?
4. Spring Boot 가 "Just Run" 가능한 이유 4가지?
5. `@SpringBootApplication` 안에 포함된 3가지 어노테이션은?
6. Spring Boot 에서 JSP 를 쓰려면 추가해야 할 의존성 한 가지는?
7. `@Controller` 와 `@RestController` 가 같이 있는 프로젝트에서 둘의 동작 차이는?

<details><summary>풀이</summary>

1. **요청마다 서블릿을 새로 만들 필요 없음**. 모든 요청을 한 곳에서 받고 그 뒤에서 라우팅 → 공통 부가 처리(로깅·인증·인코딩) 를 한 곳에 통합.
2. **URL → 처리할 Controller 매핑**. `/hello` 요청이 오면 `HelloController` 를 반환하는 등.
3. `return req.getRequestDispatcher("/WEB-INF/views/hello.jsp").forward(req, res);` 같이 **실제 파일 경로**를 직접 적어야 함. ViewResolver 가 있으면 `return "hello"` 만으로 끝.
4. ① 자동 설정 ② starter 의존성 ③ 내장 톰캣 ④ Production Ready (actuator).
5. `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`.
6. `tomcat-embed-jasper` (JSP 엔진). 필요 시 JSTL 도.
7. **`@Controller`**: 반환값을 view 이름으로 해석 → JSP 렌더. **`@RestController`** = `@Controller` + `@ResponseBody`: 반환값을 JSON 직렬화. REST API 엔드포인트엔 `@RestController`, 페이지 렌더링엔 `@Controller`.

</details>

---

## 23. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.3 표지·TOC·학습목표 | 들어가기 전에 |
| p.4 ~ p.22 Spring Legacy Web (Mini MVC 4단계) | §1 ~ §6 (Part A) |
| p.23 ~ p.27 Spring Boot 등장 | §7 ~ §9 (Part B) |
| p.28 ~ p.40 Spring Boot Project 생성·실행 | §10 ~ §14 (Part C) |
| p.41 ~ p.50 Spring Boot JSP·Bean 확인 | §15 ~ §19 (Part D) |
| p.51 마무리 | (생략) |

_51p 슬라이드 모두 커버._
