# Spring Batch — 대용량 일괄 처리

> **이 강의는 무엇인가**: 매일 새벽 100만 건 통계 계산, 월말 정산, 데이터 마이그레이션처럼 **순차적 대량 처리** 를 안전하게 돌리는 Spring 의 배치 프레임워크.
> **왜 배우는가**: 실시간 API 만 짜다 보면 야간 배치 만들 일이 옴. 무방비로 만들면 OOM, 중간 실패 복구 불가, 진행률 모름.

---

## 들어가기 전에

- **선수**: Spring Boot, DI, Transaction.
- **환경**: `spring-boot-starter-batch` + 메타 DB (배치 실행 이력 기록).

---

## 핵심 개념

### 1. Job · Step · Tasklet/Chunk

```
Job
 +- Step 1 (어제 주문 집계)     ← Chunk
 +- Step 2 (이메일 큐 적재)      ← Tasklet
 +- Step 3 (FTP 업로드)         ← Tasklet
```

**Tasklet** = 한 번 실행 코드, **Chunk** = `read → process → write` 반복.

### 2. Chunk 패턴 — 핵심

```
[Reader] N개 read → [Processor] 각각 변환 → [Writer] 묶음 write
```

- N 개씩 메모리 → OOM 방지
- N 개 단위 트랜잭션 → 실패 시 마지막 성공 chunk 다음부터 재시작
- N(=chunkSize) 보통 100~1000

### 3. 첫 Job

```java
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
            .<Order, DailyStat>chunk(500, txm)             // ①
            .reader(orderReader())
            .processor(new OrderToDailyStat())
            .writer(statWriter())
            .build();
    }

    @Bean @StepScope                                       // ②
    public ItemReader<Order> orderReader() {
        return new MyBatisCursorItemReaderBuilder<Order>()
            .queryId("...findYesterday")
            .build();
    }
}
```

① chunk(500, txm) — 500 read → 500 process → 한 번에 write + commit. 실패 시 그 chunk 만 rollback.
② `@StepScope` — Step 실행마다 새 빈, JobParameters 주입 가능.

### 4. JobParameters & 재시작

```java
JobParameters params = new JobParametersBuilder()
    .addString("date", "2024-01-15")
    .addLong("run.id", System.currentTimeMillis())     // 중복 방지
    .toJobParameters();
jobLauncher.run(orderStatsJob, params);
```

같은 파라미터로 한 번만 성공 가능. 실패는 마지막 실패 지점부터 재시작.

### 5. 메타 테이블

`BATCH_JOB_INSTANCE`, `BATCH_JOB_EXECUTION`, `BATCH_STEP_EXECUTION` 등 자동 생성. 운영자가 진행 상태 조회.

### 6. 다단 Step / 분기

```java
@Bean
public Job multiJob() {
    return new JobBuilder("multi", jobRepo)
        .start(step1()).next(step2()).next(step3())
        .build();
}

// 조건 분기
.start(step1())
  .on("FAILED").to(failHandlingStep())
  .from(step1()).on("*").to(step2())
  .end()
```

### 7. 스케줄링

Spring Batch 자체엔 스케줄러 없음. `@Scheduled`, Quartz, k8s CronJob, Airflow 등과 결합.

```java
@Component @RequiredArgsConstructor
public class BatchScheduler {
    private final JobLauncher launcher;
    private final Job orderStatsJob;

    @Scheduled(cron = "0 0 3 * * *")
    public void run() throws Exception {
        launcher.run(orderStatsJob, new JobParametersBuilder()
            .addLong("ts", System.currentTimeMillis())
            .toJobParameters());
    }
}
```

`@EnableScheduling` 메인 클래스 필수.

---

## 코드 깊게 들여다보기

CSV → DB 마이그레이션 (가장 흔한 패턴):

```java
@Bean
public Step importStep() {
    return new StepBuilder("import", jobRepo)
        .<UserCsv, User>chunk(1000, txm)
        .reader(csvReader())
        .processor(new UserCsvToEntity())
        .writer(userJpaWriter())
        .faultTolerant()
            .skip(BindException.class)             // 파싱 실패 스킵
            .skipLimit(50)
        .listener(new SkipListener<UserCsv, User>() {
            @Override public void onSkipInRead(Throwable t) { log.warn("skip read {}", t.getMessage()); }
            @Override public void onSkipInProcess(UserCsv it, Throwable t) { log.warn("skip {}", it); }
        })
        .build();
}

@Bean @StepScope
public FlatFileItemReader<UserCsv> csvReader(@Value("#{jobParameters['file']}") String path) {
    return new FlatFileItemReaderBuilder<UserCsv>()
        .name("csv")
        .resource(new FileSystemResource(path))
        .delimited().names("id","name","email")
        .targetType(UserCsv.class)
        .linesToSkip(1)                            // 헤더
        .build();
}
```

500MB CSV 도 메모리 5MB 정도로 처리. 50개 행 깨져도 나머지 OK. 중간에 죽어도 마지막 chunk 다음부터.

---

## 실전 패턴 / 자주 빠지는 함정

- ❌ `chunk(1)` → 트랜잭션 오버헤드 폭증.
  ✅ 100~1000.
- ❌ `findAll()` 후 처리 → OOM.
  ✅ Cursor 기반 Reader.
- ❌ 같은 JobParameters 재실행 → `JobInstanceAlreadyCompleteException`.
  ✅ run.id 같은 unique.
- ❌ `@StepScope` 누락 → JobParameters 못 받음.
- ❌ 읽기·쓰기 같은 DB 트랜잭션 → 락 경합.
  ✅ Reader 별도.

---

## 다음 강의로 가기 전 자가점검

1. Chunk 패턴이 OOM 과 재시작 둘 다 해결하는 원리?
2. 같은 JobParameters 로 두 번 실행하면?
3. `@StepScope` 없이 `@Value("#{jobParameters['file']}")` 쓰면?
4. faultTolerant + skip 효과?

<details><summary>풀이</summary>

1. N 개씩만 메모리 → OOM 방지. N 개 단위 트랜잭션 + 메타 테이블 진행 위치 기록 → 재실행 시 다음 chunk 부터.
2. `JobInstanceAlreadyCompleteException`. 성공한 Job 은 재실행 불가. 실패 시는 재시작.
3. JobParameters 가 Bean 생성 시점에 없음 → 에러/null. `@StepScope` 가 Step 시작 시 지연 생성.
4. 특정 예외(파싱 에러) 행 건너뛰고 계속. skipLimit 초과 시 Job 실패. 품질 불완전 ETL 에 필수.

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1~5 표지·왜 Batch | §1 |
| p.6~15 Job/Step/Chunk | §2, §3 |
| p.16~25 JobParameters·메타 | §4, §5 |
| p.26~37 분기·스케줄 | §6, §7 |
| p.38~47 실습 CSV | 코드 |

_단독 학습 가능 노트._
