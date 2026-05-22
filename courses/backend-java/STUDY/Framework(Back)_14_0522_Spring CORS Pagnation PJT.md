# Framework(Back) 관통 PJT — CORS · Pagination · Full-Text Search

> **이 강의는 무엇인가**: 프론트와 백엔드를 실제로 연결할 때 가장 자주 발을 거는 ① **CORS** 의 4가지 해결법, ② 게시판의 표준 기능인 **Pagination** 을 수동 구현 → Spring Data Commons 로 진화시키는 흐름, ③ `LIKE '%키워드%'` 의 한계를 풀어내는 **Full-Text Search** (N-gram + MATCH/AGAINST + UNION).
> **왜 배우는가**: AJAX/Fetch 로 API 호출하는 순간 무조건 마주치는 CORS, 데이터 100건만 넘어가도 필수인 페이지네이션, 검색 기능이 있는 모든 프로젝트의 핵심인 FTS — 세 가지 모두 "실무 첫 주에 막히는 항목 TOP 3" 다.

---

## 들어가기 전에

- **선수**: Spring MVC, MyBatis(`<where>`, `<if>` 동적 쿼리), REST API 기초.
- **마인드셋**:
  - CORS 는 **서버 결함이 아니라 브라우저의 안전장치**. 그래서 "허용" 정책을 명시해줘야 한다.
  - 페이지네이션은 **수동 → Spring Data Commons** 로 진화 단계가 명확. 처음엔 직접 만들어보고 그 다음 추상화의 가치를 체감.
  - FTS 는 **데이터 수천 건까지는 LIKE 로 OK**. 수십만 건부터 필요. "오버엔지니어링 피하기".

---

# Part A. CORS

## 1. 왜 CORS 가 존재하는가

브라우저의 **Same-Origin Policy (SOP, 동일 출처 정책)** 은 한 사이트의 JS 가 다른 출처의 리소스에 자유롭게 접근하는 것을 막는다. 없으면 악성 페이지가 사용자의 은행 세션을 이용해 돈을 빼낼 수 있다.

**출처(Origin)** = `protocol + hostname + port` 의 조합.

```
https : // www.example.com : 8080 / path?q=v#hash
+-+-+  +-----+-----+ +-+-+
protocol     host     port
+------------ Origin ---------+
```

| URL 1 | URL 2 | 동일 출처? |
|--|--|--|
| `https://a.com/x` | `https://a.com/y` | ✓ |
| `https://a.com` | `http://a.com` | ✗ (protocol 다름) |
| `https://a.com` | `https://api.a.com` | ✗ (host 다름) |
| `https://a.com:80` | `https://a.com:8080` | ✗ (port 다름) |

## 2. 실무에서 CORS 가 터지는 전형적 시나리오

```
[브라우저] http://localhost:5500 (Live Server 로 index.html 호스팅)
   |
   | fetch('http://localhost:8080/api-board/board')
   ▼
[Spring]   http://localhost:8080
```

출처가 다름 (port 5500 ≠ 8080) → 브라우저 콘솔에 빨간 에러:

```
Access to fetch at 'http://localhost:8080/api-board/board'
from origin 'http://localhost:5500' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

> 주의: **서버 로그에는 200 OK 로 보임**. 응답은 도착했으나 브라우저가 JS 에 전달을 거부한 것. 그래서 백엔드 개발자가 "내 API 는 잘 도는데?" 라고 답하면 안 됨.

## 3. CORS 해결 4가지 방법 (슬라이드 핵심)

```
① 서버 측 프록시 설정
   · 개발 서버(Vite/Live Server)가 백엔드로 대리 전달
   · 브라우저 입장에서는 동일 출처로 보임
   · 개발 환경에서 유용. 운영엔 부적합

② 서버 측 CORS 설정
   · 응답 헤더에 Access-Control-Allow-* 명시
   · 가장 표준적·일반적

③ 클라이언트 측 설정
   · withCredentials 등 옵션
   · 서버 설정을 못 바꿀 때 사용

④ Framework·Library 지원
   · Spring 의 @CrossOrigin, WebMvcConfigurer
   · 사실 ②의 편의 래퍼

   ↓
실무는 거의 ② + ④ 조합
```

### ① 서버 측 프록시 (개발 환경)

```
브라우저  --①-- GET http://localhost:5500/api/board
                         |
                         ▼ (proxy forward)
                  http://localhost:8080/api/board (실제 Spring)
                         |
                  응답  <---------
```

Vite 의 `vite.config.js`:
```js
export default {
  server: {
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true }
    }
  }
}
```

브라우저는 **자기 출처(`localhost:5500`)** 로만 요청 → SOP 위반 없음. 운영에선 nginx 가 같은 역할.

### ② 서버 측 CORS 설정 (가장 표준)

```
[브라우저]                        [Spring]
    |
    | ① OPTIONS /api/board  ← preflight (출처 다를 때 자동)
    |   Origin: http://localhost:5500
    |   Access-Control-Request-Method: PATCH
    +-------------------------->
    |                            +- ② preflight 응답
    |                            |  Access-Control-Allow-Origin: localhost:5500
    | <--------------------------+  Access-Control-Allow-Methods: GET,POST,PATCH
    |                            |  Access-Control-Max-Age: 3600
    | ③ 본 요청 PATCH /api/board
    +-------------------------->
    | <----  200 OK + 데이터
```

**Preflight 가 발생하는 조건** (하나라도 만족):
- 메서드가 GET/HEAD/POST 이외 (PUT/PATCH/DELETE)
- `Content-Type` 이 `application/json` 등 단순 타입 외
- 커스텀 헤더 존재 (`Authorization`, `X-CSRF-Token` 등)

## 4. Spring 의 CORS 설정 — 2가지 방법

### 방법 1: `@CrossOrigin` (컨트롤러/메서드 단위)

```java
@CrossOrigin(
    origins = {"http://localhost:5500", "http://localhost:5173"},
    allowedHeaders = "*",
    methods = {RequestMethod.GET, RequestMethod.POST}
)
@RestController
@RequestMapping("/api")
public class BoardRestController {
    // 이 컨트롤러의 모든 핸들러에 적용
}
```

**특징**:
- 컨트롤러·메서드 단위 세밀 제어
- 클래스에 붙이면 모든 메서드에 적용, 메서드에 붙이면 메서드만
- 속성 비우면 (`origins = {}`) Spring 기본 정책 사용 (`*`)
- `@AliasFor("value")` 로 `origins` 와 `value` 가 동일

**언제 쓰나**: 일부 엔드포인트만 다른 출처에 열고 싶을 때 (예: `/public/**` 은 모두 허용, `/admin/**` 은 특정 도메인만).

### 방법 2: `WebMvcConfigurer` (전역, 권장)

```java
@Configuration
public class WebCorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")                              // 적용 경로
                .allowedOrigins(                                    // 허용 출처 (명시)
                    "http://localhost:5500",
                    "http://localhost:5173"
                )
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")                                // 모든 요청 헤더 허용
                .allowCredentials(true)                             // 쿠키·인증 허용
                .maxAge(3600);                                      // preflight 캐시 1시간
    }
}
```

**모든 옵션은 `@CrossOrigin` 의 속성과 1:1 대응**. 전역에서 일관 정책을 두는 게 보안·운영에 유리.

### 핵심 응답 헤더 정리

| 헤더 | 의미 |
|--|--|
| `Access-Control-Allow-Origin` | 허용 출처. `*` 또는 명시. credentials 동반 시 `*` 불가 |
| `Access-Control-Allow-Methods` | 허용 메서드 (preflight 응답에만) |
| `Access-Control-Allow-Headers` | 허용 요청 헤더 |
| `Access-Control-Allow-Credentials` | `true` → 쿠키·인증 헤더 동반 허용 |
| `Access-Control-Max-Age` | preflight 캐시 (초) |
| `Access-Control-Expose-Headers` | JS 에서 읽을 수 있는 응답 헤더 (기본은 안전 헤더만 노출) |

## 5. CORS 디버깅 5단계

1. **브라우저 콘솔 빨간 메시지의 정확한 문장** 읽기 — Origin/Method/Header 중 무엇이 막혔는지 명시됨
2. **Network 탭에서 OPTIONS preflight 응답** 확인 — 200 인지, `Access-Control-Allow-Origin` 등 헤더 다 있는지
3. `allowedOrigins("*")` 와 `allowCredentials(true)` 동시 사용 여부 — 브라우저가 무시함
4. **Spring Security 사용 중이면 CorsFilter 가 가장 앞에 있는지** + OPTIONS 가 permitAll 인지
5. 응답이 정상인데 JS 에서 헤더 못 읽으면 `exposedHeaders` 누락 (예: `Location`)

## 6. CORS 와 Spring Security 의 함정

Spring Security 가 활성화돼 있으면 OPTIONS preflight 가 인증을 요구해 401 로 떨어진다.

```java
@Bean
public CorsFilter corsFilter() {
    CorsConfiguration cfg = new CorsConfiguration();
    cfg.setAllowedOrigins(List.of("http://localhost:5500"));
    cfg.setAllowedMethods(List.of("GET", "POST", "PATCH", "DELETE", "OPTIONS"));
    cfg.setAllowedHeaders(List.of("*"));
    cfg.setAllowCredentials(true);

    UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/api/**", cfg);
    return new CorsFilter(src);
}

@Bean
public SecurityFilterChain chain(HttpSecurity http) throws Exception {
    return http
        .cors(Customizer.withDefaults())                            // ① CORS 필터 활성
        .csrf(csrf -> csrf.disable())
        .authorizeHttpRequests(a -> a
            .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll() // ② preflight 통과
            .anyRequest().authenticated()
        )
        .build();
}
```

---

# Part B. Pagination

## 7. 왜 페이지네이션인가

| 문제 | 영향 |
|--|--|
| 1만 건 한 번에 응답 | 5MB+ JSON. 네트워크·메모리·렌더 모두 죽음 |
| DB 풀스캔 | 인덱스 있어도 결과셋이 크면 디스크 IO 폭증 |
| UX | 사용자는 한 화면에 10~20건이면 충분. 무한 스크롤도 결국 페이지 단위 |

→ 클라이언트가 "몇 번째 페이지의 몇 개" 만 요청 + 서버는 `LIMIT/OFFSET`.

## 8. 응답 표준 — Content + PageInfo 패키지

```json
{
  "status": "success",
  "data": {
    "content": [
      { "id": 1, "title": "1번째 게시글", "author": "홍길동" },
      { "id": 2, "title": "2번째 게시글", "author": "김철수" }
    ],
    "pageInfo": {
      "currentPage": 1,
      "pageSize": 10,
      "totalElements": 154,
      "totalPages": 16
    }
  }
}
```

`content` 와 `pageInfo` 를 함께 내려야 클라이언트가 페이지 네비게이션을 그릴 수 있다.

## 9. 순수 Java 수동 페이지네이션 — PageInfo DTO

```java
@Data
public class PageInfo {
    private int page;          // 현재 페이지 (1-indexed)
    private int size;          // 페이지당 건수
    private int totalCount;    // DB COUNT(*) 결과
    private int offset;        // = (page - 1) * size
    private int totalPage;     // = ceil(totalCount / size)

    public PageInfo(int page, int size, int totalCount) {
        this.page = page;
        this.size = size;
        this.totalCount = totalCount;
        this.offset = (page - 1) * size;
        this.totalPage = (int) Math.ceil((double) totalCount / size);
    }
}
```

생성자 한 번에 모든 파생값 계산 → 컨트롤러·뷰에서 그냥 쓰기만 하면 됨.

## 10. 수동 페이지네이션 — 5단계 데이터 흐름

```
[클라이언트]
    | GET /api-board/board?page=2&size=10
    ▼
[Controller]
    | @RequestParam page, size 수신
    ▼
[Service]
    | ① int totalCount = boardDao.count(condition)
    |      ↓
    |   DB: SELECT COUNT(*) FROM board
    |
    | ② PageInfo pageInfo = new PageInfo(page, size, totalCount)
    |      ↓
    |   offset = (page-1)*size = 10
    |   totalPage = ceil(totalCount/size)
    |
    | ③ List<Board> list = boardDao.selectList(pageInfo)
    |      ↓
    |   DB: SELECT * FROM board ORDER BY id DESC LIMIT 10, 10
    ▼
[Service 반환]
    | Map.of("list", list, "pageInfo", pageInfo)
    ▼
[Controller → JSON 응답]
```

## 11. 수동 페이지네이션 — Mapper XML

```xml
<!-- ① 전체 건수 -->
<select id="count" parameterType="SearchCondition" resultType="int">
    SELECT COUNT(*) FROM board
</select>

<!-- ② LIMIT 페이징 -->
<select id="selectList" parameterType="SearchConditionWithPage"
                                resultType="Board">
    SELECT id, title, writer, content,
           reg_date AS regDate, view_cnt AS viewCnt
    FROM board
    ORDER BY id DESC
    LIMIT #{pageInfo.offset}, #{pageInfo.size}
</select>
```

**MyBatis 단일 파라미터 제약 우회 — Wrapper DTO**:

```java
@Data
public class SearchConditionWithPage {
    private SearchCondition condition;  // key, word
    private PageInfo pageInfo;          // offset, size
}
```

XML 안에서 `#{pageInfo.offset}` 처럼 `.` 으로 중첩 접근.

또는 `Map`:
```java
Map<String, Object> param = new HashMap<>();
param.put("condition", condition);
param.put("pageInfo",  pageInfo);
```

## 12. 검색 + 페이지네이션 결합 (심화)

검색했는데 빈 페이지가 나오면? 전체 건수(`totalCount`) 가 검색 무관하게 계산되기 때문. **COUNT 와 SELECT 두 쿼리에 동일한 검색 조건을 적용** 해야 한다.

```xml
<!-- ① COUNT 쿼리에도 검색 조건 -->
<select id="count" parameterType="SearchCondition" resultType="int">
    SELECT COUNT(*) FROM board
    <where>
        <if test="word != null and word != ''">
            ${key} LIKE CONCAT('%', #{word}, '%')
        </if>
    </where>
</select>

<!-- ② SELECT 쿼리에 검색 + LIMIT -->
<select id="selectList" parameterType="SearchConditionWithPage"
                                resultType="Board">
    SELECT id, title, writer, content,
           reg_date AS regDate, view_cnt AS viewCnt
    FROM board
    <where>
        <if test="condition.word != null and condition.word != ''">
            ${condition.key} LIKE CONCAT('%', #{condition.word}, '%')
        </if>
    </where>
    ORDER BY id DESC
    LIMIT #{pageInfo.offset}, #{pageInfo.size}
</select>
```

> **`${key}` vs `#{word}` 의 차이**: `${}` 는 문자열 치환 (SQL injection 위험, 칼럼명 동적 지정 용도). `#{}` 는 PreparedStatement 의 `?` 바인딩 (안전, 값 전달 용도). 칼럼명을 동적으로 받을 때 `${key}` 를 쓰지만 화이트리스트 검증 필수!

## 13. 수동 페이지네이션 — Controller / Service 전체

```java
// Controller
@GetMapping("/board")
public ResponseEntity<Map<String, Object>> listPaged(
        @ModelAttribute SearchCondition condition,
        @RequestParam(defaultValue = "1")  int page,
        @RequestParam(defaultValue = "10") int size) {
    Map<String, Object> result = boardService.getBoardListPaged(condition, page, size);
    return ResponseEntity.ok(result);
}

// Service
@Override
public Map<String, Object> getBoardListPaged(SearchCondition condition, int page, int size) {
    // ① 전체 건수
    int totalCount = boardDao.count(condition);
    // ② PageInfo (offset, totalPage 자동 계산)
    PageInfo pageInfo = new PageInfo(page, size, totalCount);
    // ③ 현재 페이지 데이터
    SearchConditionWithPage param = new SearchConditionWithPage(condition, pageInfo);
    List<Board> list = boardDao.selectList(param);
    return Map.of("list", list, "pageInfo", pageInfo);
}
```

## 14. Spring Data Commons — 페이지네이션 추상화

위 수동 구현의 보일러플레이트(`PageInfo`, offset 계산, `totalPage` 계산) 를 **완전히 제거** 해주는 표준 추상화.

**3대 핵심 인터페이스**:

| 인터페이스 | 역할 | 비고 |
|--|--|--|
| `Pageable` | **요청** — page·size·sort 를 묶음 | 컨트롤러가 받음 |
| `Page<T>` | **응답** — content + 메타데이터 | totalElements/totalPages/isFirst/isLast 자동 |
| `PageImpl<T>` | `Page<T>` 의 구현체 | `new PageImpl<>(list, pageable, total)` |

```java
@GetMapping("/board")
public Page<Board> list(
    @PageableDefault(size = 10, page = 0, sort = "id", direction = Sort.Direction.DESC)
    Pageable pageable
) {
    return boardService.getBoardList(pageable);
}
```

요청: `GET /board?page=0&size=10&sort=id,desc`

> ⚠ **0-indexed 주의**: Spring Data 의 `page` 파라미터는 **0부터** 시작. 사용자 표시는 1-indexed 인데 내부는 0-indexed 라 변환 필요. `setOneIndexedParameters(true)` 옵션 또는 컨트롤러에서 명시 변환.

## 15. Spring Data Commons — 의존성 (MyBatis 환경)

JPA 환경엔 자동 포함되지만, **MyBatis 만 쓸 땐 별도 추가**:

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-commons</artifactId>
</dependency>
```

핵심 import:
```java
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
```

## 16. Spring Data Commons 도입 효과 (Before/After)

### Before — 수동

```java
int totalCount = boardDao.count(condition);
PageInfo pageInfo = new PageInfo(page, size, totalCount);   // 직접 계산
SearchConditionWithPage param = new SearchConditionWithPage(condition, pageInfo);
List<Board> list = boardDao.selectList(param);
return Map.of("list", list, "pageInfo", pageInfo);
```

### After — Spring Data

```java
int totalCount = boardDao.count(condition);
long offset = pageable.getOffset();                          // 내장 계산
int  size   = pageable.getPageSize();
List<Board> list = boardDao.selectList(offset, size);
return new PageImpl<>(list, pageable, totalCount);          // totalPages 등 자동
```

**효과**:
- `PageInfo` DTO 수동 작성·유지보수 ❌
- `totalPage` 계산 수식 직접 ❌
- 응답 JSON 의 메타데이터 직렬화 ❌ → Spring 이 알아서

## 17. 검색 + 페이지네이션 + Spring Data 통합 (MyBatis)

```java
// Controller
@GetMapping("/board")
public ResponseEntity<Page<Board>> listPaged(
        @ModelAttribute SearchCondition condition,
        @PageableDefault(size = 10) Pageable pageable) {

    // ① 검색조건과 Pageable 을 하나로 묶어서 Mapper 에 전달
    //    (MyBatis 의 단일 파라미터 제약 우회)
    RequestList<SearchCondition> req = RequestList.<SearchCondition>builder()
        .data(condition)
        .pageable(pageable)
        .build();

    // ② 전체 건수 (검색 조건 적용)
    int total = boardDao.count(condition);
    // ③ 데이터 조회 (검색 + 페이징)
    List<Board> list = boardDao.selectPaged(req);
    // ④ 표준 Page 객체 반환
    return ResponseEntity.ok(new PageImpl<>(list, pageable, total));
}
```

```xml
<select id="selectPaged" parameterType="RequestList" resultType="Board">
    SELECT * FROM board
    <where>
        <if test="data.key != null">
            <!-- 중첩 접근: req.data.key, req.data.word -->
            ${data.key} LIKE CONCAT('%', #{data.word}, '%')
        </if>
    </where>
    ORDER BY id DESC
    LIMIT #{pageable.offset}, #{pageable.pageSize}
</select>
```

**학습 포인트**:
1. MyBatis XML 안에서 DTO 의 속성에 `.` 으로 접근 (`data.key`, `pageable.offset`)
2. 두 객체를 한 번에 넘기려면 Wrapper DTO 로 감쌈
3. `Pageable` 의 `offset()`/`pageSize()` 가 내장 메서드라 따로 계산할 필요 없음

---

# Part C. Full-Text Search (Appendix)

## 18. LIKE 검색의 한계

```sql
SELECT * FROM board WHERE title LIKE '%스프링%';
```

| 데이터 | 응답 시간 |
|--|--|
| 1,000 건 | < 10ms |
| 10,000 건 | ~50ms |
| 100,000 건 | ~500ms |
| 1,000,000 건 | ~5s ⚠ |

**원인**: `%키워드%` 는 **인덱스를 못 탄다** (prefix `키워드%` 만 인덱스 가능). 풀 테이블 스캔.

## 19. Full-Text Search 의 아이디어 — 역인덱스

기존: "문서 중심" — Doc 1 의 내용을 다 읽는다.
FTS: **"단어 중심"** — 단어별로 어떤 문서에 있는지를 사전(역인덱스) 으로 미리 만들어 둔다.

```
+------------------+         +--------------------+
|  기존 테이블        |         |   역인덱스 사전        |
| (문서 중심)         |         |  (단어 중심)         |
+------------------+         +--------------------+
| Doc 1: 스프링 부트   |  --→   | "스프링"  → [1, 2] |
| Doc 2: 스프링 시작   |         | "부트"   → [1, 3] |
| Doc 3: 부트 시작    |         | "시작"   → [2, 3] |
+------------------+         +--------------------+

"부트" 검색 시 사전에서 즉시 [1, 3] 추출 → 두 문서만 열어보면 끝
```

데이터 100만 건이라도 사전 한 번 조회 = O(log n).

## 20. 한국어 검색의 핵심 — N-gram 파서

영어는 공백 단위로 단어를 자르면 되는데, 한국어는:
- 띄어쓰기 불규칙
- 조사·어미 변화 다양
- 부분 검색 빈번 ("스프링" 으로 "스프링부트" 도 찾고 싶음)

→ **N-gram (기본 2글자 단위로 기계적 분할)** 이 해답.

```
원본:    "스프링부트"
2-gram:  스프, 프링, 링부, 부트
역인덱스: 스프 → [1, 2]
         프링 → [1, 2]
         링부 → [1]
         부트 → [1]
         링시 → [2]
         시작 → [2]
```

**오타 강건성**: 사용자가 "프링" 만 검색해도 사전에 있으므로 매칭. 띄어쓰기 무관.

## 21. MySQL Full-Text Index 적용 (DDL)

```sql
-- 게시판 제목·내용 FTS 인덱스
ALTER TABLE board
ADD FULLTEXT INDEX ft_idx_board (title, content)
WITH PARSER ngram;

-- 댓글 내용 FTS 인덱스
ALTER TABLE comment
ADD FULLTEXT INDEX ft_comment_content (content)
WITH PARSER ngram;
```

`WITH PARSER ngram` 이 핵심 — 한국어용. 기본 파서는 공백 기준이라 한국어에 부적합.

## 22. MATCH/AGAINST + UNION — 통합 검색

```xml
<select id="searchUnion" parameterType="string" resultType="Board">
    <!-- ① 게시글 본문에서 검색 -->
    SELECT DISTINCT b.id, b.title, b.writer, b.content,
                    b.reg_date  AS regDate,
                    b.view_cnt  AS viewCnt
    FROM board b
    WHERE MATCH(b.title, b.content) AGAINST(#{word})

    UNION

    <!-- ② 댓글에 검색어가 포함된 게시글 -->
    SELECT DISTINCT b.id, b.title, b.writer, b.content,
                    b.reg_date  AS regDate,
                    b.view_cnt  AS viewCnt
    FROM board b
    INNER JOIN comment c ON b.id = c.board_id
    WHERE MATCH(c.content) AGAINST(#{word})

    ORDER BY id DESC
</select>
```

**왜 UNION?**
- 본문에만 있는 글, 댓글에만 있는 글, 둘 다 있는 글을 모두 노출
- `UNION` 은 중복 자동 제거 (둘 다 매칭된 게시글은 1번만)
- 정렬은 마지막에 한 번

**MATCH/AGAINST 문법**:
- `MATCH(col1, col2, ...) AGAINST('검색어')` — 자연어 모드 (기본)
- `MATCH(...) AGAINST('+필수 -제외' IN BOOLEAN MODE)` — 불리언 모드
- `MATCH(...) AGAINST('검색어' WITH QUERY EXPANSION)` — 연관 단어 자동 확장

## 23. MySQL FTS vs Elasticsearch — 선택 기준

| 비교 기준 | MySQL FTS | Elasticsearch |
|--|--|--|
| 시스템 복잡도 | 매우 낮음 (DB 일체형) | 매우 높음 (별도 클러스터) |
| 인프라 | 기존 DB 그대로 | 추가 서버 + 동기화 파이프라인 |
| 분석기 | N-gram (기계적 분할) | Nori 형태소 분석기 (문맥·동의어) |
| 성능 | 수백만 건까지 OK | 수억 건도 분산 처리 |
| 권장 시점 | 초·중기 서비스, 게시판 | 대규모 포털·쇼핑몰·로그 분석 |

> **"오버엔지니어링을 피하자"** — 수천 건 게시판에 Elasticsearch 도입하는 건 망치로 파리 잡기. 초기엔 MySQL FTS, 트래픽·데이터 성장 후 마이그레이션.

---

## 24. 코드 깊게 — CORS + Pagination + 검색 + FTS 풀스택

```java
// === CORS ===
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry r) {
        r.addMapping("/api/**")
         .allowedOrigins("http://localhost:5500")
         .allowedMethods("GET", "POST", "PATCH", "DELETE", "OPTIONS")
         .exposedHeaders("Location")
         .allowCredentials(true)
         .maxAge(3600);
    }
}

// === DTO ===
@Data
public class SearchCondition {
    private String key;   // 검색 칼럼 (title, writer, content)
    private String word;  // 검색어
}

// === Controller ===
@RestController
@RequestMapping("/api/board")
@RequiredArgsConstructor
public class BoardApi {
    private final BoardService service;

    @GetMapping
    public ResponseEntity<Page<Board>> list(
            @ModelAttribute SearchCondition cond,
            @PageableDefault(size = 10, sort = "id",
                             direction = Sort.Direction.DESC) Pageable pageable) {
        return ResponseEntity.ok(service.search(cond, pageable));
    }

    @GetMapping("/fts")
    public ResponseEntity<List<Board>> fts(@RequestParam String word) {
        return ResponseEntity.ok(service.fullTextSearch(word));
    }
}

// === Service ===
@Service @RequiredArgsConstructor
public class BoardServiceImpl implements BoardService {
    private final BoardDao boardDao;

    @Override
    public Page<Board> search(SearchCondition cond, Pageable pageable) {
        int total = boardDao.count(cond);
        List<Board> list = (total == 0)
            ? List.of()
            : boardDao.selectPaged(
                RequestList.<SearchCondition>builder()
                    .data(cond).pageable(pageable).build());
        return new PageImpl<>(list, pageable, total);
    }

    @Override
    public List<Board> fullTextSearch(String word) {
        return boardDao.searchUnion(word);
    }
}
```

**관전 포인트**:
- CORS, 검색, 페이징, FTS 가 각각 책임이 분리됨
- `Page<Board>` 반환 → totalElements/totalPages 자동 직렬화
- `total == 0` 빈 결과 조기 반환으로 LIMIT 0 쿼리도 생략

---

## 25. 실전 패턴 / 자주 빠지는 함정

### CORS
- ❌ `allowedOrigins("*")` + `allowCredentials(true)` — 양립 불가
  ✅ 명시 출처 나열, 또는 `allowedOriginPatterns("*")` + credentials
- ❌ 운영에서도 모든 출처 허용 → CSRF 의 발판
  ✅ 환경별 (dev/staging/prod) 출처 분리
- ❌ Spring Security 사용 중 preflight 401 → 인증 요구로 OPTIONS 가 막힘
  ✅ CorsFilter 를 SecurityFilterChain 앞에 + OPTIONS permitAll
- ❌ `Location` 같은 응답 헤더를 JS 에서 못 읽음 → `exposedHeaders` 누락
  ✅ 명시
- ❌ 운영 nginx 가 OPTIONS 가로채서 Spring 까지 안 옴
  ✅ 게이트웨이/프록시 CORS 도 확인

### Pagination
- ❌ `LIMIT 100000, 20` 같은 큰 offset → DB 가 앞 100k 행 스캔
  ✅ keyset (cursor) 페이지네이션 — `WHERE id < lastSeenId`
- ❌ `size` 검증 안 함 → 클라가 `size=999999` 보내면 서버 다운
  ✅ `@Max(100)` 등
- ❌ `ORDER BY` 없는 LIMIT → 페이지마다 순서 들쭉날쭉
  ✅ 인덱스 있는 컬럼으로 정렬
- ❌ 0-based / 1-based 혼용
  ✅ DTO/Pageable 의 `offset()` 메서드로 한 곳에서만 변환
- ❌ 검색 조건이 `COUNT` 쿼리엔 안 들어감 → 검색해도 totalPages 그대로
  ✅ COUNT 와 SELECT 두 쿼리에 동일 조건

### FTS
- ❌ `WITH PARSER ngram` 안 줌 → 한국어가 거의 매칭 안 됨
  ✅ 한국어 데이터엔 필수
- ❌ FULLTEXT INDEX 생성 후 기존 데이터에 자동 적용 안 된다고 착각
  ✅ ALTER 시 자동 색인. 단 대용량은 시간 걸림
- ❌ `MATCH(col)` 의 칼럼이 FULLTEXT INDEX 와 정확히 일치 안 함
  ✅ `(title, content)` 로 인덱스 만들었으면 `MATCH(title, content)` 로 검색
- ❌ 모든 검색을 FTS 로 → 정확한 ID/번호 검색까지 FTS
  ✅ 사용자 입력 종류에 따라 분기

### 트러블슈팅 시나리오

| 증상 | 원인 | 해결 |
|--|--|--|
| CORS 에러: `No 'Access-Control-Allow-Origin'` | 서버 CORS 미설정 | `WebMvcConfigurer.addCorsMappings` 추가 |
| preflight 401 | Security 가 OPTIONS 차단 | OPTIONS permitAll |
| `Pageable` 의 page 가 항상 0 | 0-indexed 인 줄 모름 | 의도 확인 + 변환 |
| `Page<T>` JSON 직렬화 시 무한 루프 | 양방향 연관관계 | `@JsonIgnore` 또는 DTO 변환 |
| MyBatis `${data.key}` 가 안 풀림 | parameterType 의 필드명과 안 맞음 | DTO 필드명 정확히 |
| FTS 결과 0건 | ngram 파서 누락 또는 검색어 짧음 (기본 최소 2자) | `WITH PARSER ngram`, `innodb_ft_min_token_size` 조정 |
| UNION 결과에 정렬이 안 됨 | 각 SELECT 의 ORDER BY 는 무시됨 | 마지막에 한 번 ORDER BY |

---

## 26. 자가점검

1. CORS preflight 가 발생하는 조건 3가지를 한 줄씩.
2. `@CrossOrigin` 과 `WebMvcConfigurer` 둘 중 운영에서 권장되는 건? 이유는?
3. `allowedOrigins("*")` + `allowCredentials(true)` 가 동시에 안 되는 이유?
4. 수동 페이지네이션의 `PageInfo` 가 가져야 하는 5개 필드?
5. Spring Data Commons 의 `Pageable` 의 `page` 가 0-indexed 인 이유는 학습용으로 잠시 외워야 하나? 더 깊은 이유는?
6. 검색 + 페이지네이션에서 빈 페이지가 나오는 원인은?
7. FTS 가 LIKE 보다 빠른 핵심 원리는?
8. 한국어 검색에서 N-gram 파서가 필수인 이유?

<details><summary>풀이</summary>

1. ① 메서드가 GET/HEAD/POST 외 ② `Content-Type` 이 단순 타입 외 ③ 커스텀 헤더 존재
2. **`WebMvcConfigurer`**. 일관된 전역 정책 + 한 곳에서 관리 + 보안 감사 용이. `@CrossOrigin` 은 일부 예외 엔드포인트에만.
3. 브라우저가 보안상 거부 — credentials 동반 요청은 출처를 명시해야 안전. `*` 은 "아무 출처나 OK" 라 인증정보 유출 위험이 너무 큼.
4. `page, size, totalCount, offset, totalPage`
5. 컴퓨터 과학적 관습 (배열 인덱스). 0-based 가 offset 계산이 깔끔 (`offset = page * size`, 1-based 면 `(page-1) * size`). 단, 사용자 노출에선 1-based 가 친숙.
6. `COUNT` 쿼리에 검색 조건 미적용 → `totalPages` 가 검색 결과보다 크게 계산되어 빈 페이지로 이동 가능. 두 쿼리에 동일 조건 적용 필수.
7. **역인덱스** — 단어 → 문서 매핑을 사전으로 미리 만들어 둠. 검색 시 사전 한 번 조회로 매칭 문서 즉시 추출. LIKE 의 풀스캔과 달리 O(log n).
8. 한국어는 띄어쓰기 불규칙 + 부분 검색 필요. 공백 기반 토크나이저는 작동 안 함. N-gram 은 기계적으로 2글자씩 잘라 모든 부분 문자열을 색인 → 오타·부분 검색에 강건.

</details>

---

## 27. 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1 ~ p.3 표지·학습목표 | 들어가기 전에 |
| p.4 ~ p.13 CORS (개념·4가지 해결·@CrossOrigin·WebMvcConfigurer·실습) | §1 ~ §6 (Part A) |
| p.14 (Spring Board 추가 개발 표지) | 강의 외 실습 시간 |
| p.15 ~ p.23 페이지네이션 (개념·수동 구현·검색 결합) | §7 ~ §13 |
| p.24 ~ p.27 Spring Data Commons (Pageable·Page·PageImpl·통합) | §14 ~ §17 |
| p.28 ~ p.33 Full-Text Search (역인덱스·N-gram·MATCH/UNION·ES 비교) | §18 ~ §23 (Part C) |
| p.34 ~ p.35 PJT 소개 (관통 명세서) | (강의 외 자료 별도) |
| p.36 마무리 | (생략) |

_총 36p 슬라이드의 모든 학습 주제 커버. CORS 4가지 해결법, MyBatis 검색+페이징 통합, Full-Text Search 부록 모두 반영._
