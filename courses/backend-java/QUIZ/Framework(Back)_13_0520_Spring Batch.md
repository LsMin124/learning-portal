# Spring Batch - 퀴즈

> 14문항. 개념·적용·디버그·면접. Job / Step / Tasklet / Chunk / Reader-Processor-Writer.

---

### Q1. (개념) Spring Batch 의 핵심 단위 4가지 (Job, Step, Tasklet, Chunk) 와 관계?

<details><summary>정답</summary>

```
Job (가장 큰 단위 - 하나의 배치 작업)
 +- Step 1 (어제 주문 집계)        <- Chunk 방식
 +- Step 2 (이메일 큐 적재)         <- Tasklet 방식
 +- Step 3 (FTP 업로드)            <- Tasklet 방식
```

| 단위 | 역할 |
|--|--|
| **Job** | 하나의 배치 작업 단위 (예: "야간 정산") |
| **Step** | Job 안의 단계 (Job 은 1개 이상의 Step) |
| **Tasklet** | 한 번 실행되는 코드 (디렉터리 정리, API 호출) |
| **Chunk** | `read → process → write` 를 N 개씩 반복 |

**Step 의 두 방식**:
- **Tasklet 방식**: 단순한 단일 작업 (`@Bean` 의 `Tasklet` 인터페이스)
- **Chunk 방식**: 대량 데이터를 N 개씩 처리 (가장 자주 사용)

→ 보통 Job 1개 + Step 1~5개. Step 내부는 대부분 Chunk.

</details>

### Q2. (개념) Chunk 패턴이 OOM (Out Of Memory) 과 재시작 둘 다 해결하는 원리?

<details><summary>정답</summary>

**Chunk 동작**:
```
Reader: 1개씩 read --(N번)--> [N개 모임]
                                 ↓
Processor: 각각 변환
                                 ↓
Writer: N 개 한 번에 write + 트랜잭션 commit
```

**OOM 방지**:
- 100만 건 전체를 메모리에 안 올림 → N (=500) 개씩만
- Reader 는 **Cursor 기반** → DB 에서 fetch size 만큼만 가져옴
- 메모리 사용량 = `chunk size x 한 행 크기` (일정)

**재시작 보장**:
- N 개 write 후 **트랜잭션 commit** → 메타 테이블 (`BATCH_STEP_EXECUTION`) 에 진행 위치 기록
- 중간에 죽어도 `read_count` 와 `write_count` 가 저장됨
- 같은 Job 재실행 시 → **마지막 성공한 chunk 다음부터** 자동 시작

**예시**:
- 100만 건 처리 중 60만 건째 죽음
- 메타 테이블: `read_count = 600000`, `write_count = 600000`
- 재실행 → 600001 번째부터 시작 → 처음부터 다시 안 돌림

→ Spring Batch 의 가장 큰 가치. 이게 없으면 매번 처음부터 다시.

</details>

### Q3. (개념) Tasklet vs Chunk - 언제 무엇을 선택?

<details><summary>정답</summary>

| | Tasklet | Chunk |
|--|--|--|
| **반복** | 한 번 실행 | 데이터 N 개씩 반복 |
| **사용 예** | 디렉터리 정리, API 호출, 알림 발송 | 100만 건 처리, ETL, 통계 집계 |
| **트랜잭션** | 메서드 전체 1개 | N 개마다 별도 |
| **재시작** | 처음부터 | 마지막 chunk 다음부터 |

**Tasklet 예**:
```java
@Bean
public Step cleanupStep() {
    return new StepBuilder("cleanup", jobRepo)
        .tasklet((contribution, chunkContext) -> {
            // 임시 디렉터리 비우기
            FileUtils.cleanDirectory(new File("/tmp/batch"));
            return RepeatStatus.FINISHED;
        }, txm)
        .build();
}
```

**Chunk 예**:
```java
@Bean
public Step aggregateStep() {
    return new StepBuilder("aggregate", jobRepo)
        .<Order, DailyStat>chunk(500, txm)        // 500개씩 한 트랜잭션
        .reader(orderReader())
        .processor(orderProcessor())
        .writer(statWriter())
        .build();
}
```

→ "데이터 처리" 면 Chunk. "단일 액션" 이면 Tasklet.

</details>

### Q4. (적용) `orderStatsJob` 을 Job + Step + Chunk 로 정의.

<details><summary>정답</summary>

```java
@Configuration
@RequiredArgsConstructor
public class OrderStatsJobConfig {
    private final JobRepository jobRepo;
    private final PlatformTransactionManager txm;

    @Bean
    public Job orderStatsJob() {
        return new JobBuilder("orderStatsJob", jobRepo)
            .start(aggregateStep())
            .build();
    }

    @Bean
    public Step aggregateStep() {
        return new StepBuilder("aggregate", jobRepo)
            .<Order, DailyStat>chunk(500, txm)         // 500 개씩
            .reader(orderReader())                      // Order 읽기
            .processor(new OrderToDailyStat())          // 변환
            .writer(statWriter())                       // DB 저장
            .build();
    }

    @Bean
    @StepScope                                          // JobParameters 주입 위함
    public ItemReader<Order> orderReader(
            @Value("#{jobParameters['date']}") String date) {
        return new MyBatisCursorItemReaderBuilder<Order>()
            .queryId("OrderMapper.findByDate")
            .parameterValues(Map.of("date", date))
            .sqlSessionFactory(sqlSessionFactory)
            .build();
    }

    @Bean
    public ItemWriter<DailyStat> statWriter() { ... }
}
```

**핵심**:
- `chunk(500, txm)` - 500 개씩 read → process → write → commit
- 제네릭 `<Order, DailyStat>` - Reader/Processor 입력 타입 → Writer 출력 타입
- `@StepScope` - Step 실행 시점에 Bean 생성 (JobParameters 접근 가능)

</details>

### Q5. (적용) JobParameters 생성과 unique 보장 (`run.id`).

<details><summary>정답</summary>

```java
JobParameters params = new JobParametersBuilder()
    .addString("date", "2026-05-19")               // 비즈니스 파라미터
    .addLong("run.id", System.currentTimeMillis()) // 유일성 보장 키
    .toJobParameters();

JobExecution exec = jobLauncher.run(orderStatsJob, params);
```

**JobParameters 의 역할**:
- Job 실행을 식별하는 키 (date, batch_type 등)
- Spring Batch 가 **동일한 파라미터 조합은 한 번만 성공 가능** 으로 관리

**`run.id` 가 필요한 이유**:
- 같은 날짜 (`date=2026-05-19`) 로 재실행하고 싶을 때
- 운영 사고로 같은 날 두 번 돌려야 할 때
- `System.currentTimeMillis()` 가 매번 다른 값 → 항상 새 JobInstance

**파라미터 종류**:
- `addString(key, value)`
- `addLong(key, value)`
- `addDate(key, date)`
- `addDouble(key, value)`

**식별성 제외** (선택):
```java
.addLong("run.id", System.currentTimeMillis(), false)   // 식별성 false
```

</details>

### Q6. (디버그) 같은 JobParameters 로 Job 을 두 번 실행하면 어떻게 되나?

<details><summary>정답</summary>

```java
// 첫 실행 - 성공
jobLauncher.run(job, new JobParametersBuilder()
    .addString("date", "2026-05-19").toJobParameters());

// 두 번째 실행 - 같은 파라미터
jobLauncher.run(job, new JobParametersBuilder()
    .addString("date", "2026-05-19").toJobParameters());
// -> JobInstanceAlreadyCompleteException
```

**규칙**:

| 첫 실행 상태 | 같은 파라미터 재실행 |
|--|--|
| **COMPLETED** (성공) | `JobInstanceAlreadyCompleteException` - **불가** |
| **FAILED** (실패) | **가능** - 마지막 실패 지점부터 재시작 |
| **STOPPED** (중단) | 가능 - 재시작 |

**왜 이 정책?**:
- 야간 배치가 한 번 성공했는데 또 돌리면 → 중복 집계, 이메일 두 번 발송 등 사고
- "같은 작업 = 한 번만 성공" 을 프레임워크가 강제

**우회 (의도적 재실행)**:
```java
// run.id 로 다른 인스턴스 만들기
.addLong("run.id", System.currentTimeMillis())

// 또는 다른 식별 파라미터
.addString("retry", "v2")
```

**디버깅 시 메타 테이블 확인**:
```sql
SELECT * FROM BATCH_JOB_INSTANCE WHERE JOB_NAME = 'orderStatsJob';
SELECT * FROM BATCH_JOB_EXECUTION ORDER BY START_TIME DESC LIMIT 10;
```

</details>

### Q7. (적용) `@StepScope` + `@Value("#{jobParameters['file']}")` 패턴으로 JobParameters 주입.

<details><summary>정답</summary>

```java
@Bean
@StepScope                                              // 핵심
public FlatFileItemReader<UserCsv> csvReader(
        @Value("#{jobParameters['file']}") String path  // SpEL 로 JobParameters 주입
) {
    return new FlatFileItemReaderBuilder<UserCsv>()
        .name("csvReader")
        .resource(new FileSystemResource(path))
        .delimited().names("id", "name", "email")
        .targetType(UserCsv.class)
        .linesToSkip(1)
        .build();
}
```

**실행**:
```java
JobParameters params = new JobParametersBuilder()
    .addString("file", "/data/users_20260519.csv")
    .addLong("run.id", System.currentTimeMillis())
    .toJobParameters();
jobLauncher.run(importJob, params);
```

**`@StepScope` 의 의미**:
- Bean 생성을 **Step 시작 시점까지 지연**
- Step 마다 새 Bean 인스턴스 → JobParameters 가 그때 사용 가능
- 같은 Job 의 여러 Step 도 각자 다른 Bean

**SpEL 표현식**:
- `#{jobParameters['key']}` - JobParameters
- `#{jobExecutionContext['key']}` - Job 단위 공유 데이터
- `#{stepExecutionContext['key']}` - Step 단위 공유 데이터

</details>

### Q8. (디버그) `@StepScope` 없이 `@Value("#{jobParameters['file']}")` 사용 시 발생하는 문제?

<details><summary>정답</summary>

**문제 코드**:
```java
@Bean       // @StepScope 누락
public FlatFileItemReader<UserCsv> csvReader(
        @Value("#{jobParameters['file']}") String path) {
    return new FlatFileItemReaderBuilder<UserCsv>()
        .resource(new FileSystemResource(path))   // path = null
        .build();
}
```

**증상**:
- **Bean 생성 시점**: Spring Boot 시작 → ApplicationContext 초기화 → 모든 `@Bean` 메서드 호출
- 이때 **JobParameters 는 아직 없음** (Job 이 실행되지 않음)
- `#{jobParameters['file']}` → null
- `new FileSystemResource(null)` → 에러 또는 Reader 가 null 경로로 생성

**에러 메시지** (Spring Batch 버전마다 다름):
```
Caused by: org.springframework.expression.spel.SpelEvaluationException:
EL1008E: Property or field 'jobParameters' cannot be found on object of type ...
```

**해결**: `@StepScope` 또는 `@JobScope` 추가.
- `@StepScope` - Step 실행 시점에 새 Bean
- `@JobScope` - Job 실행 시점에 새 Bean (Step 들이 공유)

**왜 일반 `@Scope("prototype")` 가 아닌가**:
- prototype 은 의존성 주입 시점에 새로 생성 (Spring 컨텍스트 안에서)
- `@StepScope` 는 **Spring Batch 의 Step 생명주기** 와 연결 → JobParameters 접근 보장

</details>

### Q9. (적용) `faultTolerant()` + `skip` + `retry` 패턴.

<details><summary>정답</summary>

```java
@Bean
public Step importStep() {
    return new StepBuilder("import", jobRepo)
        .<UserCsv, User>chunk(1000, txm)
        .reader(csvReader())
        .processor(csvToUser())
        .writer(userJpaWriter())

        .faultTolerant()                              // 핵심 - 결함 허용
            .skip(BindException.class)                // CSV 파싱 실패는 건너뛰기
            .skip(DataIntegrityViolationException.class)   // DB UNIQUE 위반도
            .skipLimit(50)                            // 최대 50건까지

            .retry(DeadlockLoserDataAccessException.class) // 데드락은 재시도
            .retryLimit(3)                            // 3번까지

        .listener(new SkipListener<UserCsv, User>() {
            @Override
            public void onSkipInRead(Throwable t) {
                log.warn("Skip read: {}", t.getMessage());
            }
            @Override
            public void onSkipInProcess(UserCsv item, Throwable t) {
                log.warn("Skip process: {} - {}", item, t.getMessage());
            }
        })
        .build();
}
```

**효과**:
- `skip` - 특정 예외 행을 건너뛰고 계속 진행 (skipLimit 초과 시 Job 실패)
- `retry` - 특정 예외에 자동 재시도 (락 경합, 일시적 네트워크 에러)
- `SkipListener` - 건너뛴 데이터 로깅 / 별도 파일에 기록

**ETL 시나리오 (가장 흔한 용례)**:
- 100만 건 CSV 중 100건 깨진 데이터 → 100건 건너뛰고 999,900 건 처리 OK
- 모니터링 알람: skip 100건 초과 시 알람

**주의**:
- skip 너무 많으면 → 데이터 품질 문제 무시
- retry 너무 많으면 → 진짜 에러 늦게 발견

</details>

### Q10. (적용) CSV → DB 마이그레이션 패턴 (FlatFileItemReader).

<details><summary>정답</summary>

```java
@Bean
@StepScope
public FlatFileItemReader<UserCsv> csvReader(
        @Value("#{jobParameters['file']}") String path) {
    return new FlatFileItemReaderBuilder<UserCsv>()
        .name("csvReader")
        .resource(new FileSystemResource(path))
        .delimited()
            .delimiter(",")
            .names("id", "name", "email")            // CSV 컬럼 -> 필드
        .targetType(UserCsv.class)                   // POJO 매핑
        .linesToSkip(1)                              // 헤더 제외
        .encoding("UTF-8")
        .build();
}

@Bean
public ItemProcessor<UserCsv, User> csvToUser() {
    return csv -> {
        User u = new User();
        u.setId(csv.getId());
        u.setName(csv.getName());
        u.setEmail(csv.getEmail());
        u.setCreatedAt(LocalDateTime.now());
        return u;
    };
}

@Bean
public ItemWriter<User> userJpaWriter(EntityManagerFactory emf) {
    return new JpaItemWriterBuilder<User>()
        .entityManagerFactory(emf)
        .build();
}

@Bean
public Step importStep() {
    return new StepBuilder("import", jobRepo)
        .<UserCsv, User>chunk(1000, txm)
        .reader(csvReader(null))
        .processor(csvToUser())
        .writer(userJpaWriter(emf))
        .build();
}
```

**효과**:
- 500MB CSV 도 메모리 5MB 정도로 처리 (Cursor 기반)
- 1000 건씩 트랜잭션 → 중간 실패 시 그 chunk 만 롤백
- 1000 건마다 commit → 진행률 측정 가능

**다른 Reader 들**:
- `FlatFileItemReader` - CSV, TSV, 고정 길이 파일
- `JdbcCursorItemReader` - JDBC 결과셋
- `JpaCursorItemReader` - JPA 쿼리
- `MyBatisCursorItemReader` - MyBatis Mapper
- `MultiResourceItemReader` - 여러 파일

</details>

### Q11. (개념) chunk size 선택 기준?

<details><summary>정답</summary>

**기본 권장**: 100 ~ 1000.

**너무 작으면 (`chunk(1)`)**:
- 트랜잭션 오버헤드 폭증 (행마다 commit)
- 1만 건 = 1만 번 트랜잭션 = 매우 느림
- 메타 테이블 쓰기도 chunk 단위 → 부하

**너무 크면 (`chunk(100000)`)**:
- 메모리 사용량 ↑ (10만 행 한 번에 메모리에)
- 트랜잭션이 길어짐 → DB 락 점유 시간 ↑
- 한 chunk 실패 시 10만 건 롤백 → 시간 낭비
- 재시작 시 마지막 성공 chunk 다음부터 → 단위가 너무 큼

**선택 가이드**:

| 상황 | 권장 chunk size |
|--|--|
| 단순 INSERT (가벼운 변환) | 1000 ~ 5000 |
| 복잡한 비즈니스 로직 | 100 ~ 500 |
| 외부 API 호출 포함 | 10 ~ 50 |
| 메모리 큰 객체 (이미지 등) | 10 ~ 100 |
| 네트워크 통한 원격 DB | 작게 (지연 시간 고려) |

**실험 방법**:
1. 100, 500, 1000, 5000 으로 각각 테스트
2. 처리 시간 vs 메모리 사용량 측정
3. 운영 부하 시뮬레이션

```yaml
# Spring Boot 설정
spring.batch.job.enabled: true
logging.level.org.springframework.batch: INFO    # 진행 로그
```

</details>

### Q12. (디버그) `findAll()` 후 처리 vs Cursor-based Reader. 1억 행 시나리오.

<details><summary>정답</summary>

**안 좋은 코드 (OOM 직행)**:
```java
@Bean
public ItemReader<Order> orderReader() {
    return new IteratorItemReader<>(
        orderRepository.findAll()    // 1억 행 모두 메모리에!
    );
}
```

**문제**:
- JPA `findAll()` 은 결과를 List 로 메모리 적재
- 1억 행 x 1KB = 100GB → OOM 즉시
- 100만 건도 4GB JVM 에서 위험

**Cursor-based Reader (안전)**:
```java
@Bean
public JdbcCursorItemReader<Order> orderReader(DataSource ds) {
    return new JdbcCursorItemReaderBuilder<Order>()
        .name("orderReader")
        .dataSource(ds)
        .sql("SELECT * FROM orders WHERE created_at >= ?")
        .preparedStatementSetter((ps) -> ps.setDate(1, ...))
        .rowMapper(new OrderRowMapper())
        .fetchSize(1000)             // DB 에서 1000행씩 가져옴
        .build();
}
```

**Cursor 동작**:
1. DB 와 Connection 유지 (커서 열림)
2. fetchSize 만큼만 가져와서 메모리에
3. ItemReader 가 1개씩 소비
4. 다 소비하면 fetchSize 만큼 또 가져옴
5. 전체 끝나면 커서 닫음

**메모리**: `fetchSize x 한 행 크기` 만 사용 → 1억 행도 일정.

**Spring Batch Reader 종류**:
- **Cursor-based** (`JdbcCursorItemReader`) - 한 Connection 유지, 빠름
- **Paging-based** (`JdbcPagingItemReader`) - LIMIT OFFSET, 멀티스레드 안전

**대용량 + 멀티스레드** → Paging, **단일 스레드** → Cursor (보통 더 빠름).

</details>

### Q13. (개념) Spring Batch 메타 테이블 + 다단 Step 의 조건 분기 (ExitStatus).

<details><summary>정답</summary>

**메타 테이블** (Spring Boot 자동 생성):

| 테이블 | 역할 |
|--|--|
| `BATCH_JOB_INSTANCE` | Job + JobParameters 조합 (식별성) |
| `BATCH_JOB_EXECUTION` | 실제 Job 실행 (성공/실패/시간) |
| `BATCH_JOB_EXECUTION_PARAMS` | 실행 시 JobParameters 값 |
| `BATCH_STEP_EXECUTION` | Step 실행 (read/write count, commit count) |
| `BATCH_STEP_EXECUTION_CONTEXT` | Step 진행 위치 (재시작용) |

**조회 예**:
```sql
-- 최근 실행 상태
SELECT JOB_NAME, STATUS, START_TIME, END_TIME, EXIT_MESSAGE
FROM BATCH_JOB_EXECUTION
ORDER BY START_TIME DESC LIMIT 10;

-- Step 별 진행
SELECT STEP_NAME, STATUS, READ_COUNT, WRITE_COUNT, COMMIT_COUNT
FROM BATCH_STEP_EXECUTION
WHERE JOB_EXECUTION_ID = ?;
```

**다단 Step 조건 분기**:
```java
@Bean
public Job multiJob() {
    return new JobBuilder("multi", jobRepo)
        .start(validateStep())
            .on("FAILED").to(notifyFailureStep())     // 실패 시 알림
        .from(validateStep()).on("*").to(processStep())   // 성공 시 처리
            .on("COMPLETED WITH SKIPS").to(reportStep())  // 스킵 있으면 리포트
            .from(processStep()).on("*").to(finalStep())  // 그 외는 마무리
        .end()
        .build();
}
```

**ExitStatus 종류**:
- `COMPLETED` - 정상 종료
- `FAILED` - 실패
- `STOPPED` - 중단
- `UNKNOWN` - 알 수 없음
- 커스텀: `step.setExitStatus(new ExitStatus("CUSTOM"))`

→ 운영자가 메타 테이블로 진행 상황 모니터링. 외부 모니터링 도구 (Spring Cloud Data Flow, Spring Batch Admin) 도 이를 활용.

</details>

### Q14. (면접) "Spring Batch 자체엔 스케줄러가 없다. 스케줄링 어떻게 결합?"

<details><summary>정답</summary>

**Spring Batch 가 스케줄러를 안 만든 이유**:
- **관심사 분리**: 스케줄링은 별도 도구의 책임
- 사용자가 필요한 도구 선택 가능

**결합 옵션 4가지**:

**1. `@Scheduled` (Spring 기본)**:
```java
@Component
@RequiredArgsConstructor
public class BatchScheduler {
    private final JobLauncher launcher;
    private final Job orderStatsJob;

    @Scheduled(cron = "0 0 3 * * *")       // 매일 새벽 3시
    public void runDaily() throws Exception {
        launcher.run(orderStatsJob, new JobParametersBuilder()
            .addString("date", LocalDate.now().minusDays(1).toString())
            .addLong("run.id", System.currentTimeMillis())
            .toJobParameters());
    }
}
```
- 메인 클래스에 `@EnableScheduling` 필수
- 장점: 간단, Spring Boot 만으로
- 단점: 단일 인스턴스 (클러스터 환경 X), 영속화 X

**2. Quartz** (엔터프라이즈):
- 클러스터 환경 지원 (여러 서버 중 한 대만 실행)
- 영속화 (서버 재시작해도 스케줄 유지)
- 복잡 (Misfire, 트리거 등)

**3. k8s CronJob** (컨테이너 인프라):
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: order-stats
spec:
  schedule: "0 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: batch
            image: myapp:latest
            command: ["java", "-jar", "app.jar", "--job.name=orderStatsJob"]
          restartPolicy: OnFailure
```
- 인프라 레벨 분리 → 앱 코드에 스케줄 X
- k8s 가 실행·재시작·모니터링
- 단점: k8s 환경 필수

**4. Airflow / Argo Workflows** (DAG 기반):
- 여러 배치 의존성 (A → B → C)
- 시각화된 워크플로우
- 운영자가 GUI 로 재실행
- 대규모 데이터 파이프라인에 적합

**선택 가이드**:

| 상황 | 추천 |
|--|--|
| 작은 단일 서버 | `@Scheduled` |
| 다중 인스턴스 (클러스터) | Quartz |
| k8s 환경 | k8s CronJob |
| 복잡한 DAG (수십 개 배치 의존) | Airflow |

**핵심**: Spring Batch 는 "배치를 실행하는 엔진", 스케줄러는 "언제 실행할지 결정". 둘은 독립적. 이 분리가 유연성을 줌.

</details>
