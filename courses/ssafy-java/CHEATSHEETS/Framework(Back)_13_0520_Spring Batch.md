# Spring Batch — 치트시트

> 47p 슬라이드 · 대용량 일괄 처리 (야간 정산·데이터 마이그레이션·ETL).
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **Job → Step → (Tasklet 또는 Chunk)** 의 3 단계 구조
2. **Chunk** = read → process → write 를 N 개씩. OOM 방지 + 재시작 보장
3. **JobParameters + run.id** 로 매번 새 JobInstance (성공한 Job 재실행 차단)
4. **`@StepScope`** + `@Value("#{jobParameters['file']}")` 로 런타임 파라미터 주입
5. **`faultTolerant().skip()`** 로 일부 행 깨져도 계속, **`retry()`** 로 일시적 에러 재시도
6. **메타 테이블** 자동 생성 → 진행 상황·재시작 추적

## 가장 중요한 코드 3개

```java
// (1) Job + Step + Chunk
@Configuration @RequiredArgsConstructor
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
            .<Order, DailyStat>chunk(500, txm)        // 500 개씩
            .reader(orderReader(null))
            .processor(new OrderToDailyStat())
            .writer(statWriter())
            .build();
    }

    @Bean @StepScope
    public JdbcCursorItemReader<Order> orderReader(
            @Value("#{jobParameters['date']}") String date) {
        return new JdbcCursorItemReaderBuilder<Order>()
            .name("orderReader")
            .dataSource(ds)
            .sql("SELECT * FROM orders WHERE DATE(created_at) = ?")
            .preparedStatementSetter(ps -> ps.setString(1, date))
            .rowMapper(new OrderRowMapper())
            .fetchSize(1000)
            .build();
    }
}
```

```java
// (2) JobParameters + 실행
@Component @RequiredArgsConstructor
public class BatchScheduler {
    private final JobLauncher launcher;
    private final Job orderStatsJob;

    @Scheduled(cron = "0 0 3 * * *")     // 매일 새벽 3시
    public void runDaily() throws Exception {
        JobParameters params = new JobParametersBuilder()
            .addString("date", LocalDate.now().minusDays(1).toString())
            .addLong("run.id", System.currentTimeMillis())     // 유일성
            .toJobParameters();
        launcher.run(orderStatsJob, params);
    }
}
```

```java
// (3) faultTolerant + skip + retry
@Bean
public Step importStep() {
    return new StepBuilder("import", jobRepo)
        .<UserCsv, User>chunk(1000, txm)
        .reader(csvReader())
        .processor(csvToUser())
        .writer(userWriter())
        .faultTolerant()
            .skip(BindException.class)              // 파싱 실패 스킵
            .skipLimit(50)
            .retry(DeadlockLoserDataAccessException.class)
            .retryLimit(3)
        .build();
}
```

## 면접 한 줄 답변
- **Chunk 패턴이 OOM 과 재시작 둘 다 해결?** → N 개씩만 메모리, 메타 테이블에 진행 위치 저장.
- **같은 JobParameters 로 두 번?** → `JobInstanceAlreadyCompleteException`. `run.id` 로 새 인스턴스.
- **@StepScope 가 없으면?** → JobParameters 가 Bean 생성 시점에 없음 → null. Step 시작 시 지연 생성.
- **Spring Batch 자체엔 스케줄러 없음?** → 관심사 분리. `@Scheduled`, Quartz, k8s CronJob, Airflow 와 조합.

---

# 2. Quick Reference (실무 복붙)

## Job · Step · Chunk 구조

```
Job (전체 배치 작업)
 ├── Step 1 (어제 주문 집계)        <- Chunk
 ├── Step 2 (이메일 큐 적재)         <- Tasklet
 └── Step 3 (S3 업로드)              <- Tasklet
```

**Tasklet vs Chunk**:
- Tasklet: 한 번 실행 (디렉터리 정리, API 호출)
- Chunk: `read → process → write` N 개씩 반복 (대량 처리)

## Job 정의

```java
@Configuration @RequiredArgsConstructor
public class MyJobConfig {
    private final JobRepository jobRepo;
    private final PlatformTransactionManager txm;

    @Bean
    public Job myJob() {
        return new JobBuilder("myJob", jobRepo)
            .start(step1())
            .next(step2())            // 순차 실행
            .build();
    }
}
```

## Chunk Step

```java
@Bean
public Step aggregateStep() {
    return new StepBuilder("aggregate", jobRepo)
        .<Order, DailyStat>chunk(500, txm)        // 500 개씩 1 트랜잭션
        .reader(orderReader())
        .processor(new OrderToDailyStat())
        .writer(statWriter())
        .build();
}
```

**chunk size 권장**: 100 ~ 1000 (너무 작으면 트랜잭션 오버헤드, 너무 크면 메모리)

## Tasklet Step

```java
@Bean
public Step cleanupStep() {
    return new StepBuilder("cleanup", jobRepo)
        .tasklet((contribution, chunkContext) -> {
            FileUtils.cleanDirectory(new File("/tmp/batch"));
            return RepeatStatus.FINISHED;
        }, txm)
        .build();
}
```

## ItemReader 종류

```java
// (1) CSV (FlatFile)
@Bean @StepScope
public FlatFileItemReader<UserCsv> csvReader(
        @Value("#{jobParameters['file']}") String path) {
    return new FlatFileItemReaderBuilder<UserCsv>()
        .name("csvReader")
        .resource(new FileSystemResource(path))
        .delimited().names("id", "name", "email")
        .targetType(UserCsv.class)
        .linesToSkip(1)
        .build();
}

// (2) JDBC Cursor (DB 단일 스레드)
@Bean
public JdbcCursorItemReader<Order> jdbcReader(DataSource ds) {
    return new JdbcCursorItemReaderBuilder<Order>()
        .name("orderReader")
        .dataSource(ds)
        .sql("SELECT * FROM orders WHERE created_at >= ?")
        .preparedStatementSetter(ps -> ps.setDate(1, ...))
        .rowMapper(new OrderRowMapper())
        .fetchSize(1000)
        .build();
}

// (3) MyBatis Cursor
@Bean
public MyBatisCursorItemReader<Order> mybatisReader(SqlSessionFactory sqlSessionFactory) {
    return new MyBatisCursorItemReaderBuilder<Order>()
        .sqlSessionFactory(sqlSessionFactory)
        .queryId("OrderMapper.findByDate")
        .build();
}
```

## ItemProcessor (변환·필터링)

```java
@Component
public class OrderToDailyStat implements ItemProcessor<Order, DailyStat> {
    @Override
    public DailyStat process(Order item) {
        if (item.getAmount() < 1000) return null;     // null = 필터링
        return new DailyStat(item.getDate(), item.getAmount());
    }
}
```

## ItemWriter

```java
// JDBC
@Bean
public JdbcBatchItemWriter<DailyStat> jdbcWriter(DataSource ds) {
    return new JdbcBatchItemWriterBuilder<DailyStat>()
        .dataSource(ds)
        .sql("INSERT INTO daily_stats (date, amount) VALUES (:date, :amount)")
        .beanMapped()
        .build();
}

// JPA
@Bean
public JpaItemWriter<User> jpaWriter(EntityManagerFactory emf) {
    return new JpaItemWriterBuilder<User>()
        .entityManagerFactory(emf)
        .build();
}
```

## JobParameters

```java
JobParameters params = new JobParametersBuilder()
    .addString("date", "2026-05-20")
    .addLong("run.id", System.currentTimeMillis())   // 유일성
    .addDate("startDate", new Date())
    .addDouble("rate", 1.5)
    .toJobParameters();

jobLauncher.run(orderStatsJob, params);
```

**규칙**:
- 같은 파라미터 조합 = 같은 JobInstance (성공한 Job 재실행 불가)
- 실패한 Job 은 같은 파라미터로 재실행 가능 (마지막 실패 chunk 부터)
- 의도적 재실행은 `run.id` 같은 unique key

## @StepScope (JobParameters 주입)

```java
@Bean
@StepScope                                              // 핵심!
public ItemReader<Order> orderReader(
        @Value("#{jobParameters['date']}") String date) {
    // date 가 Step 실행 시점에 주입됨
}
```

⚠️ `@StepScope` 없으면 Bean 생성 시점에 JobParameters 없음 → null.

## faultTolerant (결함 허용)

```java
@Bean
public Step importStep() {
    return new StepBuilder("import", jobRepo)
        .<UserCsv, User>chunk(1000, txm)
        .reader(csvReader())
        .processor(csvToUser())
        .writer(userWriter())

        .faultTolerant()
            .skip(BindException.class)              // 파싱 실패 스킵
            .skip(DataIntegrityViolationException.class)
            .skipLimit(50)                          // 최대 50건

            .retry(DeadlockLoserDataAccessException.class)
            .retryLimit(3)

        .listener(new SkipListener<UserCsv, User>() {
            @Override
            public void onSkipInProcess(UserCsv item, Throwable t) {
                log.warn("Skip: {} - {}", item, t.getMessage());
            }
        })
        .build();
}
```

## 다단 Step 조건 분기

```java
@Bean
public Job multiJob() {
    return new JobBuilder("multi", jobRepo)
        .start(validateStep())
            .on("FAILED").to(notifyStep())          // 실패 시 알림
        .from(validateStep()).on("*").to(processStep())
            .next(finalStep())
        .end()
        .build();
}
```

## 메타 테이블

```sql
-- Spring Boot 자동 생성
BATCH_JOB_INSTANCE           -- Job + JobParameters 조합
BATCH_JOB_EXECUTION          -- 실제 실행 (성공/실패/시간)
BATCH_JOB_EXECUTION_PARAMS   -- 실행 시 JobParameters
BATCH_STEP_EXECUTION         -- Step 진행 (read/write count)
BATCH_STEP_EXECUTION_CONTEXT -- 재시작용 컨텍스트

-- 조회
SELECT * FROM BATCH_JOB_EXECUTION ORDER BY START_TIME DESC LIMIT 10;
```

## 스케줄러 결합

```java
// 1. @Scheduled (간단)
@Scheduled(cron = "0 0 3 * * *")
public void run() { jobLauncher.run(myJob, params); }

// 2. Quartz (클러스터)
// 3. k8s CronJob (인프라)
// 4. Airflow (DAG)
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| chunk(1) → 트랜잭션 오버헤드 | 100~1000 |
| findAll() 후 처리 → OOM | Cursor-based Reader |
| 같은 JobParameters 재실행 → 에러 | run.id 추가 |
| @StepScope 누락 → JobParameters null | Step 단위 Bean 에 @StepScope |
| 읽기·쓰기 같은 DB 트랜잭션 → 락 | Reader 별도 |
| meta 테이블 미생성 | Spring Boot 자동 (필요 시 `spring.batch.jdbc.initialize-schema: always`) |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Spring Batch (47p)
│
├── [A] 구조
│   ├── Job
│   ├── Step (1 ~ N)
│   ├── Tasklet (한 번)
│   └── Chunk (N 개씩)
│
├── [B] Chunk
│   ├── Reader (DB / CSV / Mybatis)
│   ├── Processor (변환·필터)
│   ├── Writer (DB / 파일)
│   └── chunk size (100~1000)
│
├── [C] JobParameters
│   ├── addString / addLong / addDate
│   ├── run.id (유일성)
│   ├── JobInstance 식별
│   └── @StepScope 주입
│
├── [D] 재시작·결함 허용
│   ├── 메타 테이블 (BATCH_*)
│   ├── faultTolerant
│   ├── skip / skipLimit
│   ├── retry / retryLimit
│   └── SkipListener
│
├── [E] 다단 Step
│   ├── next (순차)
│   ├── on / to (조건 분기)
│   └── ExitStatus
│
├── [F] 스케줄링
│   ├── @Scheduled (간단)
│   ├── Quartz (클러스터)
│   ├── k8s CronJob
│   └── Airflow (DAG)
│
└── [G] 운영
    ├── 메타 테이블 모니터링
    ├── Spring Batch Admin
    ├── 로깅 / 알람
    └── 재실행 정책
```

## 학습 진도 체크리스트

- [ ] Job/Step/Tasklet/Chunk 차이
- [ ] Chunk 의 OOM 방지 + 재시작 원리
- [ ] @StepScope 의 의미
- [ ] JobParameters + run.id
- [ ] Cursor-based Reader 사용
- [ ] faultTolerant skip / retry
- [ ] 메타 테이블로 진행 모니터링
- [ ] @Scheduled 와의 결합

## 연관 강의

```
1~11강 Framework Back -> Spring 기본
12강 REST API         -> API 심화
13강 Spring Batch     <- 현재 위치
14강 CORS PJT         -> 전체 PJT
```

→ 다음 (CORS PJT) 에서 **CORS + 페이지네이션 통합**.
