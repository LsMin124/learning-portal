# CORS · Pagination · Full-Text Search — 퀴즈

> 18문항. 개념·적용·디버그·면접.

---

## Part A. CORS

### Q1. (개념) "Same-Origin" 의 세 가지 구성 요소는?

<details><summary>정답</summary>

**protocol + host + port**. 셋 중 하나라도 다르면 다른 출처. `http://a.com` vs `https://a.com` 도, `a.com:80` vs `a.com:8080` 도 다른 출처.

</details>

### Q2. (개념) 슬라이드가 제시한 CORS 해결 4가지 방법을 나열하시오.

<details><summary>정답</summary>

① **서버 측 프록시 설정** — 개발 서버가 백엔드로 대리 전달 (개발용)
② **서버 측 CORS 설정** — 응답 헤더에 `Access-Control-Allow-*` 명시 (표준)
③ **클라이언트 측 설정** — `withCredentials` 등 (제한적)
④ **Framework·Library 지원** — Spring 의 `@CrossOrigin`, `WebMvcConfigurer` (사실 ②의 편의 래퍼)

실무는 거의 ② + ④ 조합.

</details>

### Q3. (개념) CORS 에러는 클라이언트와 서버 중 어느 쪽에서 발생하나? 서버 로그에는 200 OK 인데도 에러인 이유?

<details><summary>정답</summary>

**브라우저(클라이언트)** 에서 발생. 서버는 응답을 정상적으로 200 으로 보냈으나, 브라우저가 응답 헤더에 `Access-Control-Allow-Origin` 가 없거나 일치하지 않으면 JS 에 응답을 넘기지 않고 차단. curl/Postman 같은 비-브라우저 클라이언트는 영향 없음.

</details>

### Q4. (적용) 다음 요청이 preflight 를 발생시키는가? 이유는?

```js
fetch('http://api.example.com/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ...' },
  body: JSON.stringify({ name: 'kim' })
});
```

<details><summary>정답</summary>

**발생함**. ① `Content-Type: application/json` 은 단순 요청 허용 타입 아님 ② `Authorization` 은 커스텀 헤더. → OPTIONS preflight 후 본 POST.

</details>

### Q5. (디버그) Spring 에서 다음 설정 후에도 CORS 에러:

```java
.allowedOrigins("*")
.allowCredentials(true);
```

브라우저 콘솔:
```
The value of 'Access-Control-Allow-Origin' header in the response must not be the wildcard
'*' when the request's credentials mode is 'include'.
```

<details><summary>정답</summary>

`allowedOrigins("*")` 와 `allowCredentials(true)` **양립 불가**. 해결:

```java
.allowedOrigins("http://localhost:5173", "https://myapp.com")
// 또는
.allowedOriginPatterns("*").allowCredentials(true)
```

</details>

### Q6. (디버그) Spring Security + CORS 설정 모두 했는데 preflight 가 401. 원인과 해결?

<details><summary>정답</summary>

Security 가 OPTIONS 요청까지 인증을 요구. 해결:

```java
http
  .cors(Customizer.withDefaults())                          // CorsFilter 활성
  .authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll() // preflight 허용
    .anyRequest().authenticated());
```

</details>

### Q7. (적용) `Location` 헤더를 응답으로 보냈는데 JS 에서 `response.headers.get('Location')` 이 null. 이유와 해결?

<details><summary>정답</summary>

브라우저는 CORS 응답에서 기본적으로 안전한 헤더만 JS 에 노출. `Location` 은 포함 안 됨.

```java
.exposedHeaders("Location", "X-Total-Count")
```

</details>

---

## Part B. Pagination

### Q8. (개념) 수동 페이지네이션의 `PageInfo` 가 가져야 하는 5개 필드와 각 계산식?

<details><summary>정답</summary>

```
page        : 현재 페이지 (1-indexed, 클라이언트가 보냄)
size        : 페이지당 건수 (클라이언트가 보냄)
totalCount  : 전체 데이터 수 (DB COUNT 결과)
offset      : (page - 1) * size
totalPage   : Math.ceil(totalCount / size)
```

생성자에서 page/size/totalCount 받아 offset/totalPage 자동 계산.

</details>

### Q9. (적용) MyBatis 의 단일 파라미터 제약을 우회해 검색조건(SearchCondition)과 PageInfo 를 함께 전달하는 방법 2가지?

<details><summary>정답</summary>

**방법 1: Wrapper DTO**
```java
@Data
public class SearchConditionWithPage {
    private SearchCondition condition;
    private PageInfo pageInfo;
}
```
XML 에서 `#{condition.word}`, `#{pageInfo.offset}` 으로 중첩 접근.

**방법 2: Map**
```java
Map<String, Object> param = new HashMap<>();
param.put("condition", condition);
param.put("pageInfo",  pageInfo);
```
XML 에서 `#{condition.word}` 동일하게 접근.

DTO 가 더 타입 안전.

</details>

### Q10. (디버그) 검색했는데 다음 페이지로 가니 빈 화면. 검색 전엔 정상.

<details><summary>정답</summary>

**`COUNT` 쿼리에 검색 조건이 안 들어감** → `totalPages` 가 검색 전 전체 건수 기준으로 크게 계산 → 실제론 결과가 적어서 빈 페이지.

해결: COUNT 와 SELECT 두 쿼리 모두에 동일한 `<where>` + `<if>` 조건 적용.

</details>

### Q11. (개념) Spring Data Commons 의 3대 핵심 인터페이스와 각 역할?

<details><summary>정답</summary>

| 인터페이스 | 역할 |
|--|--|
| `Pageable` | 요청 — page/size/sort 묶음 |
| `Page<T>` | 응답 — content + 메타데이터 (totalElements/totalPages/isFirst/isLast) |
| `PageImpl<T>` | `Page<T>` 의 구현체 — `new PageImpl<>(list, pageable, total)` |

</details>

### Q12. (적용) Spring Data Commons 의 `Pageable` 을 받아 검색+페이지를 처리하는 컨트롤러 작성.

<details><summary>정답</summary>

```java
@GetMapping("/board")
public ResponseEntity<Page<Board>> list(
        @ModelAttribute SearchCondition cond,
        @PageableDefault(size = 10, sort = "id",
                         direction = Sort.Direction.DESC) Pageable pageable) {
    return ResponseEntity.ok(boardService.search(cond, pageable));
}
```

요청: `GET /board?page=0&size=10&sort=id,desc&key=title&word=spring`

</details>

### Q13. (개념) MyBatis 만 쓰는 환경에서 Spring Data Commons 의 `Pageable` 을 쓰려면 무엇이 필요한가?

<details><summary>정답</summary>

`spring-data-commons` 의존성을 **명시 추가** 해야 한다 (JPA 환경엔 자동 포함, MyBatis 만 쓸 땐 자동 안 됨).

```xml
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-commons</artifactId>
</dependency>
```

</details>

### Q14. (디버그) Spring Data 의 `Pageable` 로 `?page=1` 보냈는데 응답은 첫 페이지가 나옴. 원인?

<details><summary>정답</summary>

**`Pageable` 은 0-indexed** — `page=1` 은 두 번째 페이지. 첫 페이지가 나온 게 아니라 두 번째인데 데이터가 적어서 그렇게 보였을 수 있음. 또는 1-indexed 라 착각.

해결:
- 사용자 친화적이고 싶으면 `PageableHandlerMethodArgumentResolver.setOneIndexedParameters(true)` 설정
- 또는 컨트롤러에서 `int page = Math.max(0, externalPage - 1)` 명시 변환

</details>

---

## Part C. Full-Text Search

### Q15. (개념) `LIKE '%keyword%'` 가 인덱스를 못 타는 이유?

<details><summary>정답</summary>

인덱스는 **prefix(앞부분)** 기준으로 정렬됨. `keyword%` (prefix) 는 인덱스 사용 가능, `%keyword` 또는 `%keyword%` (suffix 또는 부분 일치) 는 인덱스 무용 → 풀 테이블 스캔.

</details>

### Q16. (개념) FTS 의 "역인덱스(Inverted Index)" 가 빠른 이유를 한 단락으로?

<details><summary>정답</summary>

기존 테이블은 "문서 중심"(Doc → Content) 이라 키워드 검색 시 모든 문서를 열어 본문을 읽어야 함. **역인덱스는 "단어 중심"(Word → [Doc IDs])** 사전을 미리 구축. 검색 시 사전에서 단어 한 번 조회로 매칭 문서 ID 목록을 즉시 추출 → 이후 그 ID 들만 조회. 100만 건이라도 O(log n).

</details>

### Q17. (적용) 게시판 `title`, `content` 칼럼에 한국어 FTS 인덱스를 추가하는 DDL?

<details><summary>정답</summary>

```sql
ALTER TABLE board
ADD FULLTEXT INDEX ft_idx_board (title, content)
WITH PARSER ngram;
```

`WITH PARSER ngram` 이 핵심 — 한국어용. 기본 파서는 공백 기반이라 한국어에 부적합.

</details>

### Q18. (면접) "현재 게시판은 1만 건. 검색 기능에 MySQL FTS 와 Elasticsearch 중 어느 걸 쓰시겠어요?"

<details><summary>정답</summary>

**MySQL FTS**. 이유:
1. **데이터 규모** — 1만 건은 LIKE 만으로도 빠르지만, 미래 성장 대비해 FTS 도입은 합리적. ES 는 오버킬.
2. **인프라 비용** — ES 는 별도 클러스터 + 데이터 동기화 파이프라인. 1만 건에 안 맞음.
3. **운영 복잡도** — DB 일체형 FTS 는 백업·복구·모니터링이 기존 DB 와 동일. ES 는 새 운영 스킬 필요.
4. **N-gram 한국어 검색** 이면 사용자가 체감하는 검색 품질도 충분.

ES 로 전환할 시점:
- 데이터 100만 건 이상 + 동시 검색 요청 폭증
- 형태소 분석·동의어·자동완성·랭킹 등 고급 기능 필요
- 별도 분석 인프라 (Kibana 등) 활용 계획

원칙: **오버엔지니어링을 피하자**. 망치로 파리 잡지 않기.

</details>
