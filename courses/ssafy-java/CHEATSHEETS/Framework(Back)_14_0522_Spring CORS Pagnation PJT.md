# Spring CORS · Pagination PJT — 치트시트

> 36p 슬라이드 · CORS + 페이지네이션 통합 PJT.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Same-Origin Policy**: 다른 origin (포트·도메인) 으로의 JS fetch 차단 → CORS 로 허용
2. **CORS 헤더**: `Access-Control-Allow-Origin/Methods/Headers/Credentials`
3. **Preflight**: 비표준 메서드/헤더 시 OPTIONS 요청 먼저
4. **페이지네이션 2 방식**: OFFSET (`LIMIT ? OFFSET ?`) vs 키셋 (`WHERE id < ?`)
5. **OFFSET 깊으면 느림** → 큰 데이터는 키셋
6. **PageResult 표준**: items + total + page + size + hasNext

## 가장 중요한 코드 3개

```java
// (1) CORS 설정
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:5173", "https://myapp.com")
            .allowedMethods("GET", "POST", "PUT", "PATCH", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

```java
// (2) 페이지네이션 (OFFSET 방식)
@RestController @RequestMapping("/api/boards")
@RequiredArgsConstructor
public class BoardApi {
    private final BoardService service;

    @GetMapping
    public PageResult<BoardListItem> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String keyword) {
        return service.search(page, size, keyword);
    }
}

@Service @RequiredArgsConstructor
public class BoardService {
    @Transactional(readOnly = true)
    public PageResult<BoardListItem> search(int page, int size, String keyword) {
        int offset = (page - 1) * size;
        List<BoardListItem> items = mapper.search(keyword, size, offset);
        int total = mapper.count(keyword);
        return new PageResult<>(items, total, page, size);
    }
}
```

```sql
-- (3) 키셋 페이지네이션 (큰 데이터)
-- 첫 페이지
SELECT * FROM boards ORDER BY id DESC LIMIT 10;

-- 다음 페이지 (lastId = 12340)
SELECT * FROM boards
WHERE  id < 12340
ORDER BY id DESC LIMIT 10;
```

## 면접 한 줄 답변
- **CORS 가 왜 생김?** → 브라우저의 Same-Origin Policy (보안). 다른 origin 의 JS 가 임의 fetch 못 하게.
- **Preflight OPTIONS?** → 비표준 메서드/헤더 시 브라우저가 "허용되나?" 확인. `maxAge` 로 캐시.
- **OFFSET 깊을 때 느린 이유?** → DB 가 앞 OFFSET 행을 모두 읽고 버림. 키셋 페이지네이션 (`WHERE id < ?`) 으로 일정 속도.
- **`allowCredentials(true)` + `allowedOrigins("*")` 안 됨?** → 보안 위험. 명시적 origin 만 가능.

---

# 2. Quick Reference (실무 복붙)

## CORS 동작

```
[Browser]                              [Backend]
                                       (localhost:8080)
http://localhost:5173

  POST /api/boards
  Origin: http://localhost:5173
  ↓
                                       1. Preflight (비표준 시)
  OPTIONS /api/boards
  Access-Control-Request-Method: POST
  Access-Control-Request-Headers: Authorization
  ↓
                                       응답:
                                       Access-Control-Allow-Origin: http://localhost:5173
                                       Access-Control-Allow-Methods: POST
                                       Access-Control-Allow-Headers: Authorization
                                       Access-Control-Max-Age: 3600
  ↓
  실제 POST 요청
  ↓
                                       응답:
                                       Access-Control-Allow-Origin: http://localhost:5173
```

## CORS 설정 (Spring)

```java
// 1. 글로벌
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins(
                "http://localhost:5173",       // 개발
                "https://myapp.com"             // 운영
            )
            .allowedMethods("GET", "POST", "PUT", "PATCH", "DELETE")
            .allowedHeaders("*")
            .exposedHeaders("X-Total-Count", "X-Has-Next")   // JS 가 읽을 수 있는 응답 헤더
            .allowCredentials(true)             // 쿠키 허용
            .maxAge(3600);                      // preflight 캐시 (초)
    }
}

// 2. 컨트롤러별
@CrossOrigin(origins = "http://localhost:5173", allowCredentials = "true")
@RestController
public class BoardApi { ... }
```

## CORS + Spring Security

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain security(HttpSecurity http) throws Exception {
        http
            .cors(Customizer.withDefaults())     // CORS 활성화
            .csrf(c -> c.disable())               // REST API 면 CSRF off
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated()
            );
        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration cfg = new CorsConfiguration();
        cfg.setAllowedOrigins(List.of("http://localhost:5173"));
        cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
        cfg.setAllowedHeaders(List.of("*"));
        cfg.setAllowCredentials(true);
        cfg.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/**", cfg);
        return src;
    }
}
```

## 페이지네이션 - OFFSET 방식

```java
// Controller
@GetMapping
public PageResult<BoardListItem> list(
        @RequestParam(defaultValue = "1") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(required = false) String keyword) {
    return service.search(page, size, keyword);
}

// Service
@Transactional(readOnly = true)
public PageResult<BoardListItem> search(int page, int size, String keyword) {
    int offset = (page - 1) * size;
    List<BoardListItem> items = mapper.search(keyword, size, offset);
    int total = mapper.count(keyword);
    return new PageResult<>(items, total, page, size);
}
```

```xml
<!-- Mapper XML -->
<select id="search" resultType="BoardListItem">
    SELECT b.id, b.title, b.view_count, b.created_at, u.nickname AS writer
    FROM   boards b JOIN users u ON u.id = b.user_id
    <where>
        <if test="keyword != null and keyword != ''">
            AND (b.title LIKE CONCAT('%', #{keyword}, '%')
                 OR b.content LIKE CONCAT('%', #{keyword}, '%'))
        </if>
    </where>
    ORDER BY b.id DESC
    LIMIT #{size} OFFSET #{offset}
</select>

<select id="count" resultType="int">
    SELECT COUNT(*) FROM boards
    <where>
        <if test="keyword != null and keyword != ''">
            AND (title LIKE CONCAT('%', #{keyword}, '%')
                 OR content LIKE CONCAT('%', #{keyword}, '%'))
        </if>
    </where>
</select>
```

## 페이지네이션 - 키셋 방식 (큰 데이터)

```java
@GetMapping
public List<Board> list(
        @RequestParam(required = false) Long cursor,
        @RequestParam(defaultValue = "10") int size) {
    return mapper.findByCursor(cursor, size);
}
```

```xml
<select id="findByCursor" resultType="Board">
    SELECT * FROM boards
    <where>
        <if test="cursor != null">AND id &lt; #{cursor}</if>
    </where>
    ORDER BY id DESC
    LIMIT #{size}
</select>
```

| | OFFSET | 키셋 |
|--|--|--|
| **속도** | 페이지가 깊을수록 느림 | 항상 일정 |
| **임의 페이지 이동** | O (5 페이지로 점프) | X (순차만) |
| **UI** | 1, 2, 3, 4, 5 페이지 버튼 | "더 보기" / 무한 스크롤 |
| **사용 예** | 게시판 | SNS 피드, 채팅 |

## PageResult 표준

```java
public record PageResult<T>(
    List<T> items,
    int total,
    int page,
    int size
) {
    public int totalPages() {
        return (int) Math.ceil((double) total / size);
    }
    public boolean hasNext() {
        return page < totalPages();
    }
    public boolean hasPrev() {
        return page > 1;
    }
}
```

응답 예:
```json
{
    "items": [...],
    "total": 1234,
    "page": 3,
    "size": 10,
    "totalPages": 124,
    "hasNext": true,
    "hasPrev": true
}
```

## Vue 클라이언트 (CORS + Pagination)

```js
// stores/boards.js
const fetchBoards = async (page = 1, keyword = '') => {
    const res = await fetch(
        `http://localhost:8080/api/boards?page=${page}&keyword=${encodeURIComponent(keyword)}`,
        { credentials: 'include' }    // 쿠키 동봉 (CORS allowCredentials 필요)
    );
    if (!res.ok) throw new Error('Failed');
    return await res.json();          // PageResult<BoardListItem>
};

// 컴포넌트
const { items, total, page, totalPages, hasNext } = await fetchBoards(currentPage, keyword);
```

## Vite Proxy 대안 (개발 시 CORS 우회)

```js
// vite.config.js
export default defineConfig({
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8080',
                changeOrigin: true,
            }
        }
    }
});

// Vue 에서 `/api/boards` 호출 → Vite 가 localhost:8080 으로 프록시 → CORS 발생 X
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `allowedOrigins("*")` + `allowCredentials(true)` | 명시적 origin 만 |
| OFFSET 깊은 페이지에서 느림 | 키셋 페이지네이션 |
| `COUNT(*)` 풀스캔 | 인덱스 또는 캐시 |
| Preflight OPTIONS 캐시 안 함 | maxAge 설정 |
| CORS 응답 헤더 못 읽음 | `exposedHeaders` 명시 |
| 401 후 CORS 헤더 누락 → 정확한 에러 못 봄 | 모든 응답에 CORS 헤더 |
| `LIKE '%k%'` 인덱스 미사용 | FULLTEXT INDEX 또는 Elasticsearch |
| 페이지 번호 1-base vs 0-base 혼동 | API 스펙 명확히 |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
CORS · Pagination PJT (36p)
│
├── [A] Same-Origin Policy
│   ├── 같은 origin (scheme + host + port)
│   ├── JS fetch 차단
│   └── CORS 로 허용
│
├── [B] CORS
│   ├── Access-Control-Allow-Origin
│   ├── Allow-Methods / Headers / Credentials
│   ├── Expose-Headers
│   ├── Max-Age (preflight 캐시)
│   └── Preflight (OPTIONS)
│
├── [C] Spring CORS 설정
│   ├── @CrossOrigin (컨트롤러)
│   ├── WebMvcConfigurer.addCorsMappings (글로벌)
│   ├── CorsConfigurationSource (Security)
│   └── Vite proxy (개발 대안)
│
├── [D] 페이지네이션
│   ├── OFFSET 방식
│   │   ├── LIMIT ? OFFSET ?
│   │   ├── 임의 페이지 이동 O
│   │   └── 깊으면 느림
│   └── 키셋 방식
│       ├── WHERE id < ?
│       ├── 항상 일정 속도
│       └── 순차만 (UI 제약)
│
├── [E] PageResult
│   ├── items / total / page / size
│   ├── totalPages / hasNext
│   └── JSON 응답 표준
│
└── [F] 클라이언트 (Vue)
    ├── fetch + credentials
    ├── 페이지 버튼 (OFFSET)
    ├── 무한 스크롤 (키셋)
    └── 검색 + 페이지네이션 조합
```

## 학습 진도 체크리스트

### A. CORS
- [ ] Same-Origin Policy 의미
- [ ] CORS 헤더 4가지
- [ ] Preflight OPTIONS

### B. Spring 설정
- [ ] addCorsMappings 글로벌
- [ ] @CrossOrigin 컨트롤러별
- [ ] Spring Security 통합

### C. 페이지네이션
- [ ] OFFSET vs 키셋 차이
- [ ] LIMIT/OFFSET 계산 ((page-1) * size)
- [ ] COUNT 쿼리 분리

### D. PageResult
- [ ] 표준 응답 record
- [ ] hasNext / totalPages 계산
- [ ] JSON 응답 형식

### E. 통합
- [ ] Vue + Spring CORS 동작
- [ ] Vite proxy 대안
- [ ] 검색 + 페이지네이션 조합

## 연관 강의

```
12강 REST API       -> API 기본
14강 CORS PJT       <- 현재 위치
Front 1강 Vue       -> 클라이언트
```

→ 다음 (Vue) 에서 **클라이언트 SPA 작성**.
