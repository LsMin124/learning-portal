# Spring Boot — 치트시트

> 51p 슬라이드 · Spring 의 설정 자동화 + Starter + 내장 톰캣.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Spring Boot** = Spring + 자동 설정 + Starter + 내장 톰캣
2. **`@SpringBootApplication`** = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`
3. **Starter 의존성** 한 줄로 라이브러리 묶음 (`spring-boot-starter-web` → Tomcat + Jackson + MVC)
4. **내장 톰캣** = WAR 배포 불필요, `java -jar app.jar` 한 줄로 실행
5. **`application.yml`** 외부 설정 + Profile 분리 (dev / prod)
6. **Actuator** 로 운영 모니터링 (`/actuator/health`, `/actuator/metrics`)

## 가장 중요한 코드 3개

```java
// (1) 메인 클래스
@SpringBootApplication
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}
```

```yaml
# (2) application.yml + profile
spring:
  profiles:
    active: ${SPRING_PROFILE:dev}     # 기본 dev

server.port: 8080

---
spring.config.activate.on-profile: dev
spring.datasource.url: jdbc:mysql://localhost:3306/dev_db
spring.datasource.password: 1234

---
spring.config.activate.on-profile: prod
spring.datasource.url: jdbc:mysql://prod:3306/prod_db
spring.datasource.password: ${DB_PASSWORD}     # 환경변수
```

```xml
<!-- (3) pom.xml - Starter 의존성 -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>3.0.3</version>
    </dependency>
</dependencies>
```

## 면접 한 줄 답변
- **Spring vs Spring Boot?** → Spring 은 프레임워크, Boot 는 Spring 설정 자동화 + Starter + 내장 톰캣 → 빠른 시작.
- **`@SpringBootApplication` 의 구성?** → Configuration + EnableAutoConfiguration + ComponentScan.
- **Auto Configuration 동작?** → classpath 의 jar 보고 `@ConditionalOnClass` 등으로 자동 빈 등록.
- **`java -jar app.jar` 가 가능한 이유?** → Spring Boot Maven Plugin 이 fat jar (모든 의존성 포함 + 내장 톰캣) 생성.

---

# 2. Quick Reference (실무 복붙)

## @SpringBootApplication 의 구성

```java
@SpringBootApplication
// = @SpringBootConfiguration  (= @Configuration)
//   @EnableAutoConfiguration  (자동 설정)
//   @ComponentScan            (현재 패키지 + 하위 스캔)
public class MyApp { }
```

**주의**: 메인 클래스가 **루트 패키지** 에 있어야 모든 하위 패키지 스캔.

```
com.study.app/
├── MyApp.java           <- 여기 (루트)
├── controller/
├── service/
└── dao/
```

## Starter 의존성

| Starter | 포함 |
|--|--|
| `spring-boot-starter-web` | Tomcat + Spring MVC + Jackson |
| `spring-boot-starter-data-jpa` | JPA + Hibernate |
| `spring-boot-starter-jdbc` | JDBC + HikariCP |
| `mybatis-spring-boot-starter` | MyBatis + Spring 통합 |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-validation` | Bean Validation |
| `spring-boot-starter-actuator` | 모니터링 |
| `spring-boot-starter-test` | JUnit + Mockito + Spring Test |
| `spring-boot-starter-thymeleaf` | Thymeleaf 템플릿 |

## application.yml 핵심 설정

```yaml
# 서버
server:
  port: 8080
  servlet:
    context-path: /api
  tomcat:
    threads.max: 200
    max-connections: 8192

# 데이터소스
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb?serverTimezone=Asia/Seoul
    username: root
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5

# JPA
spring.jpa:
  hibernate.ddl-auto: validate           # 운영
  properties.hibernate.format_sql: true
  show-sql: false

# MyBatis
mybatis:
  mapper-locations: classpath:mapper/*.xml
  configuration:
    map-underscore-to-camel-case: true   # user_name -> userName
    cache-enabled: false

# 로깅
logging:
  level:
    root: INFO
    com.study: DEBUG
    org.hibernate.SQL: DEBUG
  file.name: logs/app.log
  pattern.console: "%d{HH:mm:ss} %-5level %logger{30} - %msg%n"

# Jackson
spring.jackson:
  date-format: yyyy-MM-dd HH:mm:ss
  time-zone: Asia/Seoul
  default-property-inclusion: non_null
```

## Profile 분리

```yaml
# 공통
spring.profiles.active: ${SPRING_PROFILE:dev}

---
spring.config.activate.on-profile: dev
spring.datasource.url: jdbc:mysql://localhost:3306/dev_db
logging.level.root: DEBUG

---
spring.config.activate.on-profile: prod
spring.datasource.url: jdbc:mysql://prod-host:3306/prod_db
spring.datasource.password: ${DB_PASSWORD}
logging.level.root: INFO
```

```bash
# 실행
java -jar app.jar                                  # 기본 (dev)
SPRING_PROFILE=prod java -jar app.jar              # prod
java -jar app.jar --spring.profiles.active=prod    # 또 다른 방법
```

## Actuator (운영 모니터링)

```yaml
management:
  endpoints.web.exposure.include: health, info, metrics, prometheus
  endpoint:
    health.show-details: when_authorized
    metrics.enabled: true
```

| Endpoint | 의미 |
|--|--|
| `/actuator/health` | 헬스 체크 (LB·k8s) |
| `/actuator/info` | 앱 정보 |
| `/actuator/metrics` | JVM·HTTP·DB 메트릭 |
| `/actuator/prometheus` | Prometheus 포맷 |
| `/actuator/env` | 환경변수 |
| `/actuator/beans` | 등록된 빈 목록 |
| `/actuator/mappings` | URL 매핑 |

## 외부 설정 우선순위 (높은 → 낮은)

```
1. CLI 인자 (--spring.datasource.url=...)
2. System Property (-Dspring.datasource.url=...)
3. 환경변수 (SPRING_DATASOURCE_URL=...)
4. application-{profile}.yml
5. application.yml
6. @PropertySource
```

## 내장 톰캣 vs 외부 WAS

| | 내장 톰캣 | 외부 WAS |
|--|--|--|
| 배포 | `java -jar app.jar` | WAR → Tomcat 디렉토리 |
| 설정 | application.yml | server.xml + 톰캣 |
| 컨테이너 | Docker 단순 | Docker + Tomcat 이미지 |
| 운영 | k8s 친화 | 전통 SSO |

Spring Boot 기본은 내장 톰캣 (또는 Jetty/Undertow 선택).

## 빌드 + 실행

```bash
# Maven
./mvnw clean package         # target/myapp-0.0.1-SNAPSHOT.jar
java -jar target/myapp-0.0.1-SNAPSHOT.jar

# Gradle
./gradlew bootJar
java -jar build/libs/myapp.jar

# 개발 모드 (자동 재시작)
./mvnw spring-boot:run
```

## Docker

```dockerfile
FROM eclipse-temurin:17-jre-alpine
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

```bash
docker build -t myapp .
docker run -p 8080:8080 -e SPRING_PROFILE=prod -e DB_PASSWORD=... myapp
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `@SpringBootApplication` 이 하위 패키지 못 스캔 | 메인 클래스가 루트 패키지에 |
| `application-prod.yml` 의 비밀번호 commit | `${DB_PASSWORD}` 환경변수 |
| Auto Configuration 충돌 | `@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})` |
| Actuator 전체 노출 | `management.endpoints.web.exposure.include` 명시 |
| `application.properties` vs `application.yml` 혼용 | 하나로 통일 |
| Profile 활성화 누락 → 기본 프로필 | `spring.profiles.active` 또는 ENV |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Spring Boot (51p)
│
├── [A] @SpringBootApplication
│   ├── @Configuration
│   ├── @EnableAutoConfiguration
│   ├── @ComponentScan
│   └── 메인 클래스 + main()
│
├── [B] Auto Configuration
│   ├── classpath 기반
│   ├── @ConditionalOnClass / @ConditionalOnProperty
│   ├── spring.factories / AutoConfiguration.imports
│   └── exclude / @AutoConfigureOrder
│
├── [C] Starter
│   ├── web / data-jpa / jdbc
│   ├── security / validation
│   ├── actuator / test
│   └── BOM (Bill of Materials)
│
├── [D] 내장 톰캣
│   ├── 기본 8080
│   ├── server.port / context-path
│   ├── Jetty / Undertow 대체
│   └── java -jar 실행
│
├── [E] 외부 설정
│   ├── application.yml / properties
│   ├── Profile (dev / prod)
│   ├── @Value / @ConfigurationProperties
│   └── 우선순위 (CLI > ENV > yml)
│
├── [F] Actuator
│   ├── /health / /info / /metrics
│   ├── Prometheus 통합
│   ├── 보안 (Spring Security)
│   └── 커스텀 endpoint
│
└── [G] 운영
    ├── 빌드 (mvnw / gradlew bootJar)
    ├── Docker (fat jar 친화)
    ├── Logging (logback)
    └── DevTools (자동 재시작)
```

## 학습 진도 체크리스트

### A. 시작
- [ ] @SpringBootApplication 의 3 구성
- [ ] 메인 클래스의 위치
- [ ] SpringApplication.run() 동작

### B. Starter
- [ ] starter-web 의 포함
- [ ] mybatis-spring-boot-starter 통합
- [ ] starter-test (JUnit + Mockito)

### C. 설정
- [ ] application.yml 구조
- [ ] Profile 분리 (dev/prod)
- [ ] @Value / @ConfigurationProperties

### D. 톰캣
- [ ] 내장 톰캣 vs 외부 WAS
- [ ] server.port / context-path
- [ ] Tomcat 스레드 풀 튜닝

### E. Actuator
- [ ] /actuator/health (LB 헬스 체크)
- [ ] Prometheus + Grafana
- [ ] 보안 적용

### F. 실무
- [ ] mvnw clean package
- [ ] Dockerfile 작성
- [ ] DevTools 자동 재시작

## 연관 강의

```
1강 Framework      -> 개념
2강 DI             -> 빈 관리
3강 SpringBoot     <- 현재 위치
4강 AOP            -> 빈에 프록시
5~6강 MVC          -> Web 모듈
8강 MyBatis        -> mybatis-spring-boot-starter
11강 종합 실습     -> 통합 배포
```

→ 다음 (AOP) 에서 **횡단 관심사 (로깅·트랜잭션)**.
