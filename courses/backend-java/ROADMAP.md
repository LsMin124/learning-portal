# Java 백엔드 부트캠프 — 학습 로드맵

총 강의 **28개** · 학습 노트 + 퀴즈 + 치트시트 자동 생성됨

---

## 빠른 시작

| 도구 | 명령 |
|---|---|
| 학습 포털 | `python3 -m http.server 8765 --bind 127.0.0.1` → http://127.0.0.1:8765/portal.html |
| 학습 노트 | `STUDY/README.md` |
| 퀴즈 (~14문항/강) | `QUIZ/README.md` |
| 치트시트 인덱스 | `CHEATSHEETS/README.md` |

**포털 4 모드** (단축키 1~4):
- `1 📖 학습` 강의별 깊이 있는 학습 노트 (단독 학습 가능)
- `2 🎯 퀴즈` 강의별 14문항 (개념·적용·디버그·면접)
- `3 📝 치트` TL;DR + Quick Reference + Mind Map (빠른 복습)
- `4 🗺 로드맵` 이 문서

---

## Web Backend

| 날짜 | 강의 | p |
|:-:|:--|--:|
| 04/14 | Web(Back)_01_0414_Servlet | 32 |
| 04/15 | Web(Back)_02_0415_JSP | 25 |
| 04/15 | Web(Back)_02_0415_오후_JSP실습 | 6 |
| 04/16 | Web(Back)_03_0416_Cookie_Session | 30 |
| 04/20 | Web(Back)_04_0420_EL_JSTL | 16 |
| 04/21 | Web(Back)_05_0421_Filter | 21 |
| 04/21 | Web(Back)_05_0421_오후_Back종합실습 | 6 |

## DB

| 날짜 | 강의 | p |
|:-:|:--|--:|
| 04/22 | DB_01_0422_SELECT_기본 | 44 |
| 04/23 | DB_02_0423_SELECT_응용 | 31 |
| 04/27 | DB_03_0427_DDL_DML | 29 |
| 04/28 | DB_04_0428_Join_SubQuery | 43 |
| 04/29 | DB_05_0429_JDBC | 16 |
| 04/30 | DB_06_0430_DB관통PJT | 43 |

## Framework Back (Spring 생태계)

| 날짜 | 강의 | p |
|:-:|:--|--:|
| 05/04 | Framework(Back)_01_0504_Framework | 44 |
| 05/04 | Framework(Back)_02_0504_DI | 37 |
| 05/06 | Framework(Back)_03_0506_SpringBoot | 51 |
| 05/06 | Framework(Back)_04_0506_AOP | 27 |
| 05/07 | Framework(Back)_05_0507_MVC1 | 42 |
| 05/11 | Framework(Back)_06_0511_MVC2 | 32 |
| 05/12 | Framework(Back)_07_0512_Interceptor | 33 |
| 05/13 | Framework(Back)_08_0513_MyBatis | 29 |
| 05/14 | Framework(Back)_09_0514_MyBatis_동적쿼리 | 25 |
| 05/18 | Framework(Back)_11_0518_Spring 종합실습 | 41 |
| 05/19 | Framework(Back)_12_0519_REST_API | - |
| 05/20 | Framework(Back)_13_0520_Spring Batch | 47 |
| 05/22 | Framework(Back)_14_0522_Spring CORS Pagnation PJT | 36 |

## Framework Front

| 날짜 | 강의 | p |
|:-:|:--|--:|
| 05/21 | Framework(Front)_01_0521_Introduction_of_Vue | 41 |

## SW 문제해결

| 날짜 | 강의 | p |
|:-:|:--|--:|
| 04/17 | SW문제해결응용_22_0417_패턴매칭_알고리즘PJT | 68 |

---

## 추천 학습 순서 (의존성 기준)

```
[기초 가정]
 Java 기본·OOP·컬렉션·IO·예외
 HTML/CSS/JS

[Phase 1: 서블릿/JSP]
 Web(Back) 01 Servlet → 02 JSP → 02b JSP실습 → 03 Cookie/Session

[Phase 2: SQL & 데이터 계층]
 DB 01 → 02 → 03 → 04 → 05 → 06        ╮
 Web(Back) 04 EL/JSTL → 05 Filter      │ 병렬 가능
 Web(Back) 05b Back 종합실습             ╯
                  ↓
[Phase 3: 스프링 생태계]
 Framework(Back) 01 Framework → 02 DI → 03 SpringBoot → 04 AOP
                  ↓
 Framework(Back) 05 MVC1 → 06 MVC2 → 07 Interceptor
                  ↓
 Framework(Back) 08 MyBatis → 09 동적쿼리 → 11 종합실습 → 12 REST API → 13 Batch → 14 CORS/Pagination

[Phase 4: 프런트 통합]
 Framework(Front) 01 Vue 입문
```

페이지 분량 차이 크니 시간 배분 유의:
- 짧은(≤25p): 빠른 입문/복습용 (Servlet, JSP실습, DDL/DML, MyBatis, Vue 입문 등)
- 큰(40p+): 핵심 강의, 별도 시간 (SELECT 기본 44p, SpringBoot 51p, MVC1 42p, Spring 종합실습 41p, Batch 47p)
- 가장 큰 분량: 패턴매칭 알고리즘 PJT 68p

---

## 알려진 누락 (코스 LMS 매핑 한계)

| 결손 강의 | 사유 |
|---|---|
| Web(Back)_06_0424_Web(Back)관통PJT | LMS 학습자료 목록에서 S-ID가 다른 컨텐츠를 가리킴 |
| Framework(Back)_10_0515_프로젝트기획PJT | 위와 동일한 LMS 매핑 어긋남 |

---

## 산출물 위치

- `STUDY/{lecture}.md` — 강의별 깊이 있는 학습 노트
- `QUIZ/{lecture}.md` — 14문항 (개념·적용·디버그·면접)
- `CHEATSHEETS/{lecture}.md` — TL;DR + Quick Reference + Mind Map
- `portal.html` — 통합 학습 뷰어 (사이드바·진행도·검색)
