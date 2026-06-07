# Chapter 1: Computer Networks and the Internet — 학습 노트

> *Computer Networking: A Top-Down Approach* (Kurose & Ross, 8th Global Edition, 2021) **Chapter 1** (책 p.33~112).
> 1장은 책 전체의 *지도*. **Top-down approach** — application 부터 시작해 link layer 까지 내려가는 책의 *철학* 을 소개. 이후 2~6장이 각 layer 의 상세.

---

## §0 도입 — *가장 가까운 곳부터 한 겹씩 벗긴다*

> **핵심 한 문장**: Internet 은 중앙 통제자 없이 ISP 들이 자발적으로 연결된 *network of networks* 이고, best-effort 로 packet 을 나르는 이 거대한 시스템을 이 책은 *너에게 가장 가까운 application layer 부터* 아래로 한 겹씩 벗겨 내려간다(top-down).

1장은 Internet 을 두 시선으로 본다 — 부품 목록(host·link·router·ISP)으로 보는 *nuts-and-bolts* 관점(§1)과, 분산 application 에 service 를 파는 *infrastructure* 관점. 그 둘을 잇는 약속이 *protocol* — format·order·actions(§1.3) 이다.

핵심 긴장은 §3 의 한 질문에 응축된다: 회선을 미리 잡는 *circuit switching* 과 쪼개서 통계적으로 나눠 쓰는 *packet switching* 중 무엇이 이기는가. "bursty 트래픽엔 packet" 이라는 답이 곧 Internet 의 설계 철학이고, §4 의 *4가지 delay* 와 throughput 은 그 철학의 *비용* 을 정량화한다.

마지막으로 §5 의 *5-layer stack + encapsulation* 은 이 책의 목차 그 자체다. 1장은 답을 주는 장이 아니라, *2~8장에서 만날 모든 어휘의 지도* 를 먼저 펼쳐 두는 장이다.

---

## 들어가기 전에

- **선수 지식**
  - 컴퓨터 사용 경험, 기본 TCP/IP / HTTP 용어 익숙
  - 단위: bit/byte (1 byte = 8 bits), Kbps/Mbps/Gbps (전송속도 = 10^3, 10^6, 10^9 bps), KB/MB/GB (저장 용량 = 10^3, 10^6, 10^9 bytes)
  - 시간 단위: μs (10^-6), ms (10^-3)
- **학습 목표**
  1. **Internet 의 두 정의** — nuts-and-bolts (구성요소) vs services (분산 app 의 기반)
  2. **Network edge** — host, access network (DSL, cable, fiber, WiFi, cellular) 의 *기술 별 속도와 매체*
  3. **Network core** — *packet switching* vs *circuit switching* 의 *수학적 trade-off*
  4. **Performance** — *4 delay*, *traffic intensity*, *throughput* 의 *정량 분석*
  5. **Protocol stack 5 layers** — 각 layer 의 service, encapsulation 의 mechanism
  6. **Security** 4 threats — malware, DDoS, sniffing, spoofing
  7. *Internet 의 *진화 과정* — packet switching 이론 → ARPANET → WWW → cloud → 5G/IoT
- **예상 학습 시간**: 150~200분
- **이 장의 사용법** — 1장은 *모든 후속 장의 어휘 사전*. 처음엔 *큰 그림* 위주, 익숙해진 후 *각 절의 수치 계산* 까지 직접 풀어볼 것.

---

## §1 What Is the Internet?

### §1.1 Nuts-and-Bolts View — *구성요소* 관점

> *수십억 개의 connected computing devices*

핵심 요소:

| 구성요소 | 역할 | 예시 |
|--|--|--|
| **End systems** (= *hosts*) | application 실행 주체 | PC, 스마트폰, IoT 센서, server |
| **Communication links** | bit 를 *물리적으로* 전달 | copper twisted-pair, coaxial, fiber-optic, terrestrial radio, satellite |
| **Packet switches** | packet 을 *다음 link* 로 forward | *router* (network layer), *link-layer switch* (= L2 switch) |
| **ISP (Internet Service Provider)** | end system 의 *연결 + transit* | tier-1 (Sprint, AT&T, NTT), regional (KT, SK Broadband), access (지역 cable) |

**End system** vs **router** 의 결정적 차이:
- *End system* 이 *application 실행* (HTTP 요청 생성, response 처리)
- *Router* 는 *transit only* — application 모름, *packet header 의 IP 주소* 만 보고 forward

![Figure 1.1 — Internet 의 일부 구성요소. 책 p.3](/courses/networking/figures/ch01/fig-1-1.png)

> 그림 1.1 의 핵심 — *end system 끼리 직접* 통신 안 함. 항상 *수많은 router + link* 를 거침. 사용자는 이 과정을 *모름* — protocol 의 *abstraction* 덕분.

**Internet 의 protocol 표준화 — IETF**

- **IETF (Internet Engineering Task Force)** — open community, 누구나 참여
- **RFC (Request for Comments)** — 표준 문서. 1969년부터 9000+ RFC
  - RFC 791 (IP), RFC 793 (TCP), RFC 9110 (HTTP semantics) 등 *모든 핵심 protocol*
- *Rough consensus and running code* 원칙 — 이론보다 *실제 구현 + 다수 합의*

### §1.2 Services View — *분산 application 의 기반*

> *applications 에 서비스를 제공* 하는 infrastructure

같은 시스템을 *application 관점* 으로 봄:
- *Distributed application* — 여러 host 에서 *동시 협업* 하며 동작 (web, email, social media, streaming, online games, video conference, IoT, cloud apps)
- *Application Programming Interface (API)* — host 가 *Internet 에 어떻게 access* 할지 정의 → **socket interface** (2장)

이 *두 view (nuts-and-bolts + services)* 가 책 전체의 *두 축*:
- *내려가며* (bottom up): 구성요소 → 동작 mechanism
- *올라가며* (top down): application 의 service 요구 → 그것을 *어떻게 만족* 시키나

### §1.3 What's a Protocol? — *통신 규칙*

> *Protocol* = 두 entity 사이의 *통신 규칙*

세 요소:
- **Format** — message 의 *모양* (어떤 byte 가 어떤 의미)
- **Order** — message 송수신의 *순서* (먼저 SYN, 다음 SYN-ACK, ...)
- **Actions** — message 송수신 시 *어떻게 반응*

![Figure 1.2 — 사람의 protocol vs 컴퓨터 network protocol. 책 p.7](/courses/networking/figures/ch01/fig-1-2.png)

#### 인간 인사 protocol vs HTTP

| | 인간 인사 | HTTP |
|--|--|--|
| Open | "Hi" | TCP 3-way handshake |
| Request | "What's the time?" | `GET / HTTP/1.1` |
| Response | "It's 2 o'clock" | `HTTP/1.1 200 OK` + body |
| Close | "Bye" | TCP FIN |

> 두 protocol 모두 *순서* + *형식* + *행동* 의 *합의*. 한쪽이 어기면 통신 실패.

#### 실제 HTTP 예제

```
[Client → Server]
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Connection: keep-alive

[Server → Client]
HTTP/1.1 200 OK
Date: Mon, 27 May 2026 10:00:00 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1234
Connection: keep-alive

<!DOCTYPE html>
<html>...
```

- *Format* — `METHOD URI HTTP/VERSION\r\n`, 그 다음 header 줄들, 빈 줄, body
- *Order* — client 가 request 보내고 *서버 응답 대기*. 그 후 다음 request
- *Actions* — server 가 `200 OK` 반환, 또는 `404 Not Found`, `500 Internal Server Error` 등 *적절한 status code*

이 *3 요소* 패턴이 *모든 network protocol* 에 동일.

---

## §2 Network Edge — *사용자 쪽*

### §2.1 End Systems

= **hosts**. 두 카테고리:

| 종류 | 특징 | 예시 |
|--|--|--|
| **Client** | 대부분의 시간 *idle*, 가끔 request. *consumer* | PC 브라우저, 스마트폰 앱 |
| **Server** | 24/7 운영, 대량 request 처리. *producer* | Google 검색 서버, AWS EC2, CDN edge |

![Figure 1.3 — End system 간 통신. 책 p.10](/courses/networking/figures/ch01/fig-1-3.png)

*Client-server* model 이 *압도적 다수* — web, email, social media. 일부는 *P2P* (BitTorrent, 일부 messaging).

**Modern blur** — *cloud computing* 이 server-client 의 모호화:
- *Server 그 자체가 cloud 의 VM* → AWS/Azure/GCP 가 운영
- *Edge computing* — server 가 *사용자 가까이* (Cloudflare Workers, AWS Lambda@Edge)
- *Mobile-as-server* — 스마트폰이 *photo 공유의 source* (P2P 특성)

### §2.2 Access Networks — *Internet 연결의 첫 hop*

end system 을 *Internet 의 첫 router* (edge router) 에 연결하는 *first-hop* network.

![Figure 1.4 — Access network 들. 책 p.12](/courses/networking/figures/ch01/fig-1-4.png)

#### 가정용 access network 비교

| 기술 | 속도 (down/up) | Media | 공유 방식 | 비고 |
|--|--|--|--|--|
| **DSL** (Digital Subscriber Line) | 5~50 Mbps / 1~10 Mbps | telephone copper twisted-pair | dedicated line | DSLAM 이 ISP 측 모뎀 |
| **Cable / HFC** (Hybrid Fiber-Coax) | 100M~1Gbps / 20~50 Mbps | TV coaxial cable + fiber | shared (이웃과 공유) | peak 시간 슬로다운 가능 |
| **FTTH / PON** (Fiber To The Home) | 1~10 Gbps / 1~10 Gbps | optical fiber | shared (PON tree) | 한국·일본 보편 |
| **Ethernet** (학교/회사) | 100M / 1G / 10G | UTP, fiber | dedicated switch port | LAN |
| **WiFi** (802.11) | 11M~10 Gbps | radio (2.4/5/6 GHz) | shared (AP 의 cell) | 무선 LAN |
| **4G / 5G** | 10M~10 Gbps | radio (700MHz~mmWave) | shared (cell tower) | mobile carrier |

**Asymmetric 의 본질**:
- DSL/Cable 이 *down >> up* 인 이유 — *전통 web 의 read-heavy* 패턴
- 모던 cloud / video upload / WFH 이 *upload* 도 중요 → *symmetric fiber* 가 증가

![Figure 1.5 — DSL Internet access. 책 p.13](/courses/networking/figures/ch01/fig-1-5.png)

#### DSL 의 동작

- 가정의 *전화선* (copper) 위에 *3 frequency band* 모듈레이션:
  1. *Voice* (0~4 kHz) — 전통 전화
  2. *Upstream data* (4~50 kHz)
  3. *Downstream data* (50 kHz~1 MHz)
- 가정 측 *splitter* 가 voice/data 분리
- ISP 측 *DSLAM* (DSL Access Multiplexer) 이 여러 가정의 DSL 을 *수렴* 후 backbone 으로

거리 제약 — DSLAM 으로부터 *수 km 이내* (copper 신호 감쇠). 미국 일부 시골이 DSL 못 받는 이유.

![Figure 1.6 — Cable (HFC) access. 책 p.14](/courses/networking/figures/ch01/fig-1-6.png)

#### Cable (HFC) 의 동작

- *Headend* 의 fiber → 동네의 *fiber node* → 각 가정의 *coaxial cable*
- 한 fiber node 가 *수백 가구* 공유 → *peak 시간* slowdown
- **CMTS** (Cable Modem Termination System) 이 cable modem 들을 *수렴*
- TV 신호 + Internet 데이터를 *같은 cable* 에 frequency 분할

> *Cable 의 shared 특성* — 옆집이 *대량 다운로드* 중이면 내 속도도 영향. DSL 은 dedicated 라 영향 없음.

![Figure 1.7 — FTTH with PON. 책 p.16](/courses/networking/figures/ch01/fig-1-7.png)

#### FTTH — *Fiber To The Home*

- ISP 의 *OLT* (Optical Line Terminal) → optical splitter → 각 가정의 *ONT* (Optical Network Terminal)
- **PON** (Passive Optical Network): splitter 가 *active component 없음* → 저비용
- 한국은 *FTTH 보급률 세계 1위* (~75%). 일본 도 유사.

#### Wireless 의 두 종류

| 측면 | WiFi (802.11) | Cellular (4G/5G) |
|--|--|--|
| 범위 | 수 m ~ 100m | 수 km |
| 주파수 | 2.4 / 5 / 6 GHz (free) | licensed band (700 MHz ~ mmWave) |
| 인증 | 비밀번호 | SIM (carrier 인증) |
| 비용 | 무료 (전기료만) | 통신비 |
| 사용 | 가정·사무실 | 야외·이동 |

5G 의 *3 가지 use case*:
- *eMBB* (enhanced Mobile Broadband) — 빠른 download (1 Gbps+)
- *URLLC* (Ultra-Reliable Low-Latency Communication) — < 1ms latency (자율주행, 의료)
- *mMTC* (massive Machine-Type Communication) — 수십만 IoT 동시 연결

### §2.3 Physical Media — *bit 가 흐르는 매체*

#### Guided media (line-bound)

| Media | 대역폭 | 거리 | 비용 | 사용 |
|--|--|--|--|--|
| **Twisted-pair copper** (UTP) | 100M~10G | < 100m (Cat6+) | 저가 | LAN, DSL |
| **Coaxial cable** | 100M+ | 수 km | 중간 | cable TV, HFC |
| **Multi-mode fiber** | 10G+ | < 2 km | 중간 | datacenter LAN |
| **Single-mode fiber** | 100G~Tbps | 80+ km | 고가 | backbone, submarine cable |

#### Unguided media (wireless)

| 종류 | 대역폭 | 거리 |
|--|--|--|
| Terrestrial radio (WiFi, cellular) | ~Gbps | m~km |
| Satellite | Mbps~Gbps | 무선 + 250ms RTT (geostationary), 50ms (LEO: Starlink) |
| mmWave (5G, WiFi 6E) | 10 Gbps+ | <100m, 장애물 약함 |

> **함정 1**: wireless 가 "더 편리해서" 항상 우월하다는 오해. *대역폭·신뢰성·latency* 모두 wired 가 보통 우월. wireless 는 *이동성/배선 어려움* 의 trade-off.

---

## §3 Network Core — *Internet 의 중심*

### §3.1 Packet Switching — Internet 의 핵심

![Figure 1.10 — Network core. 책 p.22](/courses/networking/figures/ch01/fig-1-10.png)

> Source 가 application message 를 *packet 으로 쪼갬*, 각 packet 이 *router 들* 을 거쳐 destination 으로.

#### 왜 packet 으로 쪼개나?

원본 message 가 *수 GB* (예: 영화 파일) 면:
- *통째로* 보내면 한 router 가 *전체 받을 때까지 다음 안 보냄* → 매우 느림
- *작은 packet* 으로 나눠 보내면 *pipelining* — 첫 packet 이 router B 에 도착하는 동안 두 번째 packet 이 router A 에서 처리

#### Store-and-forward Transmission

> Router 가 *전체 packet 을 받은 후* 다음 link 로 forward.

![Figure 1.11 — Store-and-forward. 책 p.24](/courses/networking/figures/ch01/fig-1-11.png)

전송 시간 계산 (L bits packet, R bps link, 2-hop):
- Source → router 1 의 transmission: $L/R$
- Router 1 이 *모두 받음* 후 → router 2: $L/R$
- Router 2 → destination: $L/R$
- **Total end-to-end** = $3 \cdot L/R$ (3-hop 가정)

일반화: N hop 의 *one packet end-to-end delay* = $N \cdot L/R$ (transmission 만, propagation 무시).

#### 구체 계산 예

L = 1500 bytes (= 12,000 bits), R = 100 Mbps (= 10^8 bps), N = 5 hop:
- $L/R$ = 12,000 / 10^8 = **120 μs** per hop
- Total = 5 × 120 = **600 μs**

매우 짧음 — 그러나 *수 천 packet* 의 file transfer 면 누적.

![Figure 1.12 — Packet switching. 책 p.25](/courses/networking/figures/ch01/fig-1-12.png)

#### Queueing Delay + Packet Loss

- Router 가 *output buffer* (queue) 보유 — 같은 출구 link 로 갈 packet 들이 *대기*
- 도착 packet > 처리 능력 → buffer full → **packet drop**
- *Tail drop* (가장 흔함): 새 packet 도착 시 buffer full 이면 *drop*. *RED* (Random Early Detection) 같은 정교한 policy 도 존재

**Queueing 의 본질** — Internet 이 *statistical multiplexing* 으로 *효율* 얻는 대가:
- Bursty source 들이 *합쳤을 때* 의 평균 부하 < sum of peaks
- 같은 link 를 *여러 source 가 공유* 가능
- 그러나 *동시 burst* 시 queue 폭증

### §3.2 Statistical Multiplexing 의 *수학적 이득*

> 책의 핵심 통찰 (p.30 예제).

#### 시나리오 1 — Circuit switching

- 사용자 10명, 각자 *peak 100 kbps* (10% 시간), idle 90%
- Circuit switching: 각자 *100 kbps 예약* → total *1 Mbps* link 필요
- 사용자 평균 활용: $10 \times 100 \text{kbps} \times 0.1 = 100$ kbps = 10% efficient

#### 시나리오 2 — Packet switching

- 같은 사용자 10명, 같은 1 Mbps link
- 통계적으로 *동시에 활성인 사용자 수* (Binomial(10, 0.1)):
  - P(10명 동시) = $0.1^{10} \approx 10^{-10}$ — 무시 가능
  - P(11명 이상) = 0 — 사용자 10명 한도
- *동시 활성* 이 *대부분 < 4명* (binomial 분포의 tail)
- → *1 Mbps link 가 10 사용자 충분*. circuit 보다 *10x efficient*.

> Internet 이 *packet switching 채택* 결정적 이유 — *bursty traffic 의 통계* 가 *statistical multiplexing* 으로 큰 효율.

### §3.3 Circuit Switching — 전통 전화망

![Figure 1.13 — Circuit switching. 책 p.27](/courses/networking/figures/ch01/fig-1-13.png)

> 두 end system 사이 *전용 회선* (circuit) 을 *예약*. 통신 동안 *bandwidth 보장*.

전화의 3 단계:
1. **Setup** — sender 가 network 에 *경로 + bandwidth* 요청. 모든 중간 switch 가 *resources 예약*
2. **Transfer** — 음성/data 전송. *예약된 자원만 사용*
3. **Teardown** — 통화 종료, 자원 해제

#### FDM vs TDM

![Figure 1.14 — FDM vs TDM. 책 p.29](/courses/networking/figures/ch01/fig-1-14.png)

**Frequency-Division Multiplexing (FDM)**:
- 한 link 의 *주파수 대역* 을 N 개 채널로 분할
- 각 사용자가 *전용 frequency*
- 라디오 방송, 옛 전화 trunk

**Time-Division Multiplexing (TDM)**:
- 한 link 의 *시간* 을 N 개 *time slot* 로 분할
- 각 사용자가 *주기적으로* 하나의 slot
- ISDN, T1, T3 (북미 표준)

#### Packet vs Circuit — 종합 비교

| 측면 | Packet switching | Circuit switching |
|--|--|--|
| 자원 할당 | on-demand (statistical mux) | 예약 (reservation) |
| Setup 비용 | 없음 (connectionless) | RTT 단위 비용 |
| Bandwidth 보장 | 없음 (best effort) | 보장 (예약된 만큼) |
| Bursty traffic 효율 | **매우 우수** | 비효율 (peak 예약 → idle 낭비) |
| Continuous traffic | OK (queue 위험) | 매우 우수 (jitter 없음) |
| Latency 보장 | 없음 (queue 변동) | 있음 (예약된 path) |
| Loss | queue overflow 시 | 거의 없음 |
| 복잡성 (router) | 간단 (header 만 보고 forward) | 복잡 (call state 관리) |
| 사용 | Internet | PSTN, ATM, 일부 leased line |

> **함정 2**: "packet > circuit" 의 단순 결론. 사실은 *trade-off*. 5G 의 *URLLC* (1ms latency 보장) 은 *근본적으로 circuit-like* 자원 예약. *DiffServ, MPLS* 도 packet 위에서 *circuit 의 일부 특성* 모방.

### §3.4 Network of Networks — ISP 의 계층 구조

![Figure 1.15 — ISP 의 상호연결. 책 p.34](/courses/networking/figures/ch01/fig-1-15.png)

#### ISP 의 4 tier

| Tier | 특징 | 예시 |
|--|--|--|
| **Tier-1** | 글로벌 backbone. 다른 tier-1 와 *peer* (대등 교환, 무료). | Sprint, AT&T, NTT, Tata, Telia |
| **Regional / Tier-2** | 국가 단위. tier-1 에 *transit fee* 지불. tier-2 끼리 peering 가능. | KT, SK Broadband (한국) |
| **Access / Tier-3** | local. 사용자에게 *마지막 1마일*. | 동네 cable, 작은 ISP |
| **Content Provider** | *자기 backbone*. Google·Facebook·Netflix 가 *tier-1 만큼* 큰 자체 network | Google Cloud Network, Netflix Open Connect |

#### Peering vs Transit

- **Peering**: 두 ISP 가 *서로 트래픽 교환* (무료). 둘이 *비슷한 규모* 일 때
- **Transit**: 작은 ISP 가 큰 ISP 에 *비용 지불* — 큰 ISP 가 *나머지 Internet 으로 forward*

#### IXP — Internet Exchange Point

- 여러 ISP 가 *물리적으로 한 곳* 에 모임
- 직접 peering 으로 *transit 비용 절약*
- 대표: AMS-IX (암스테르담), DE-CIX (프랑크푸르트), Equinix IBX (전 세계), KINX (한국)

#### 현대 트렌드 — *Flattening*

- Content provider (Netflix, Google) 가 *자체 backbone* + *peer with all major ISP*
- → 전통 tier-1 의 *transit 수익* 감소
- 사용자 traffic 의 *대다수가 한두 hop 안* — Netflix 의 *Open Connect* 가 ISP datacenter 안에

---

## §4 Delay, Loss, and Throughput — *성능의 정량 분석*

### §4.1 Nodal Delay — 4 가지 구성요소

![Figure 1.16 — Nodal delay 의 종류. 책 p.36](/courses/networking/figures/ch01/fig-1-16.png)

> 한 router 에서 packet 이 *겪는 총 지연*:

$$d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$$

#### (1) Processing delay $d_{proc}$

- Header 검사, error check (checksum), routing table lookup
- 보통 **microsecond 단위** (high-end router)
- 거의 *일정* — variance 작음
- 대부분의 분석에서 *무시* 가능

#### (2) Queueing delay $d_{queue}$

- Output buffer 에서 *앞 packet 들이 전송* 되는 동안 대기
- **가장 가변적** — traffic intensity 에 강하게 의존
- 0 ~ 수십 ms ~ 수 초 변동

#### (3) Transmission delay $d_{trans} = L / R$

- *Packet 을 link 에 밀어내는* 시간
- L = packet size (bits), R = link bandwidth (bps)
- "*store-and-forward 의 store 시간*"
- **link 속도 의존, packet 크기 의존**

예: 1500 byte packet, 100 Mbps link → $d_{trans} = 12000 / 10^8 = 120$ μs

#### (4) Propagation delay $d_{prop} = d / s$

- bit 가 *link 위를 물리적으로 이동* 하는 시간
- d = link 거리 (m), s = 전파 속도 (~2×10^8 m/s in copper/fiber)
- **거리 의존, link 속도 무관**

예: 11,000 km (서울 ↔ 뉴욕, great-circle distance) → $d_{prop} = 1.1 \times 10^7 / (2 \times 10^8) = 55$ ms

#### 핵심 비교

| Delay | 의존 요소 | 단위 | 비고 |
|--|--|--|--|
| Processing | router 성능 | μs | 거의 일정 |
| Queueing | traffic intensity | 0~s | 가장 가변 |
| Transmission | packet size / link rate | μs~ms | 결정적 |
| Propagation | 거리 / 매체 속도 | μs~ms | 거리 함수 |

> *Trans 와 prop 의 흔한 혼동* — trans 는 "packet 이 link 위에 *들어가는 시간*", prop 은 "*들어간 후 끝까지 이동* 하는 시간". 비유: 자동차 *toll booth 통과* (trans) + *고속도로 운전* (prop).

### §4.2 Caravan 비유 (책의 명물)

![Figure 1.17 — Toll booth 의 자동차 행렬 비유. 책 p.38](/courses/networking/figures/ch01/fig-1-17.png)

10 대 자동차의 caravan, 100 km 떨어진 toll booth 2개:
- *Toll booth* = router (transmission)
- *자동차 1대* = bit (또는 packet)
- *Caravan 전체* = packet (또는 message)
- *고속도로* = link (propagation)

각 toll booth 가 *12초/car*. 첫 booth 통과 → 100 km 운전 (100 km/h = 1 시간) → 둘째 booth 통과.

#### 두 시나리오

**A. 첫 booth 통과 후 *전체 caravan* 둘째 booth 출발**:
- 첫 booth: 10 × 12 = 2분
- 운전: 1 시간
- 둘째 booth: 2분
- **Total: 1시간 4분**

이게 *store-and-forward* — 첫 booth 가 *전체 받음* 후 다음.

**B. 첫 booth 통과 *즉시* 다음 toll booth 출발 (= cut-through)**:
- 첫 booth: 2분 (caravan 전체)
- 자동차 1대가 *통과 직후 운전 시작*
- 마지막 자동차가 두 번째 toll 도착: 2분 + 1시간 = 1시간 2분
- 둘째 booth 통과: 2분
- **Total: 1시간 4분** (같음, 단 *first byte 도달* 은 더 빠름)

**비유의 교훈**:
- *Caravan 길이* (packet size) > *highway 속도 × toll 시간 차이* 면 store-and-forward 가 자연스러움
- Internet 의 *cut-through switching* (옛 Myrinet) 은 store-and-forward 보다 *살짝 빠름*, 그러나 error 처리 어려움 → 현대 router 는 *store-and-forward 가 표준*

### §4.3 Traffic Intensity 와 Queueing

![Figure 1.18 — Traffic intensity 의 queuing delay 영향. 책 p.40](/courses/networking/figures/ch01/fig-1-18.png)

**Traffic intensity**:

$$\rho = \frac{L \cdot a}{R}$$

- L: 평균 packet size (bits)
- a: 평균 arrival rate (packets/sec)
- R: link bandwidth (bps)

해석:
- $\rho$ = "도착 부하" / "처리 능력"
- $\rho < 1$: queue 안정 (장기적으로 비워짐)
- $\rho \to 1$: queue 폭증 (M/M/1 모델의 *avg delay* = $\rho/(1-\rho) \cdot$ service time)
- $\rho > 1$: queue 무한 성장 → 결국 buffer overflow → *packet loss*

#### M/M/1 queue 의 평균 delay

Poisson arrival + exponential service time 가정 시:

$$E[d_{queue}] = \frac{\rho}{1-\rho} \cdot \frac{L}{R}$$

#### 수치 예제

R = 1 Mbps, L = 1000 bits, 다양한 a:

| a (pps) | $\rho$ | E[queue delay] |
|--|--|--|
| 500 | 0.5 | 1 × 1ms = 1 ms |
| 800 | 0.8 | 4 × 1ms = 4 ms |
| 900 | 0.9 | 9 × 1ms = 9 ms |
| 950 | 0.95 | 19 × 1ms = 19 ms |
| 990 | 0.99 | 99 × 1ms = 99 ms |

→ $\rho > 0.9$ 부터 *delay 폭주*. 산업 SLO 는 *peak ρ < 0.7* 권장.

### §4.4 End-to-End Delay

전체 path 의 N router + N+1 link:

$$d_{end-to-end} = \sum_{i=1}^{N+1} (d_{trans,i} + d_{prop,i}) + \sum_{i=1}^{N} (d_{proc,i} + d_{queue,i})$$

#### Traceroute

각 hop 의 *delay 측정* 도구:

```bash
traceroute www.google.com
 1  192.168.1.1     1.234 ms   # gateway router
 2  10.0.0.1        5.678 ms   # ISP 첫 router
 3  ...             12.345 ms
 ...
12  142.250.46.110  35.678 ms   # Google
```

**동작 원리** — ICMP/UDP packet 의 *TTL (Time-To-Live)* 1, 2, 3, ... 으로 보내 *각 hop 의 reply* 받음.

산업에서 *MTR* (Matt's Traceroute) 가 더 강력 — 지속 ping + statistics.

### §4.5 Throughput

![Figure 1.19 — File transfer 의 throughput. 책 p.44](/courses/networking/figures/ch01/fig-1-19.png)

> Sender 부터 receiver 까지 *초당 bit 전송량*.

두 구분:
- **Instantaneous throughput** — *어떤 한 순간* 의 bps
- **Average throughput** — *전체 file* 의 평균 bps. 보통 이걸 의미.

#### Bottleneck Link

![Figure 1.20 — End-to-end throughput. 책 p.46](/courses/networking/figures/ch01/fig-1-20.png)

> 경로 위의 *가장 느린 link* 가 throughput 결정.

10 hop path 에서 *9 hop 이 10 Gbps*, *1 hop 이 100 Mbps* 면 → throughput 은 100 Mbps.

이게 *Internet path 의 본질적 한계*. *마지막 mile* (가정 access network) 이 보통 bottleneck.

#### Bandwidth ≠ Throughput

- *Bandwidth*: 이론적 최대 (link 의 *제조 spec*)
- *Throughput*: 실제 측정 (다른 traffic, protocol overhead, congestion 영향)

전형적 *throughput/bandwidth* 비율:
- TCP 위 large file transfer: 70~95%
- TCP 위 small request: 10~50% (handshake + slow start overhead)
- UDP video stream: ~95% (congestion control 적음)

#### Bandwidth-Delay Product (BDP)

$$BDP = R \cdot RTT$$

*Link 위 in-flight 데이터의 최대량*. TCP window size 가 *이만큼 또는 더 커야* link 가 fully utilized.

예: 100 Mbps, 100 ms RTT → BDP = 10 Mb = 1.25 MB.

> **Long Fat Networks (LFN)** — high BDP (위성, 대륙간). TCP 의 *default 64 KB window* 로는 *5% 만 활용*. *Window scaling* (RFC 1323) 으로 1 GB+ window 가능.

#### Mathis Equation — TCP throughput 의 *근사*

$$T \approx \frac{MSS}{RTT \cdot \sqrt{p}}$$

- MSS: maximum segment size (보통 1460 bytes)
- p: packet loss rate

해석:
- *RTT 증가* → throughput 반비례 감소
- *Loss 증가* → throughput $1/\sqrt{p}$ 감소 (TCP 의 AIMD 의 결과)
- 즉 *0.01% loss → 1% loss 변화* 가 throughput 을 *10x* 감소

산업 — 같은 link 라도 *지구 반대편 (RTT 200ms)* + *0.1% loss* 면 throughput ≈ MSS / (0.2 × 0.032) ≈ 230 KB/s. 1 Gbps link 라도 *single TCP connection* 이 230 KB/s = 2 Mbps 밖에 못 씀. → *multi-connection* 또는 *QUIC* / *BBR* congestion control 필요.

---

## §5 Protocol Layers + Encapsulation

### §5.1 Layered Architecture — *복잡도 관리*

![Figure 1.21 — 비행기 여행의 계층. 책 p.47](/courses/networking/figures/ch01/fig-1-21.png)
![Figure 1.22 — 비행기 functionality 의 horizontal layering. 책 p.48](/courses/networking/figures/ch01/fig-1-22.png)

비행기 여행 — 절차의 layering:
1. *Ticket* (구매·환불)
2. *Baggage* (체크인·픽업)
3. *Gate* (탑승·하차)
4. *Runway* (이륙·착륙)
5. *Airplane routing* (공중 항로)

각 layer 가 *자기 task* 만, 위 layer 에 *service* 제공. 한 layer 의 *내부* 변경이 다른 layer 영향 X (예: ticket 시스템이 paper → app 으로 바뀌어도 baggage 동일).

#### Layering 의 *5 가지 이점*

1. **Modularity** — 한 layer 변경이 *다른 layer 영향 X*
2. **Independent development** — 각 layer 별 *전문가 팀*
3. **Reusability** — 같은 layer 가 *다른 system* 에서 재사용
4. **Standardization** — *interface 가 명세* 되어 *interoperability*
5. **Conceptual clarity** — 한 번에 *한 layer* 만 생각

### §5.2 Internet Protocol Stack — 5 Layers

![Figure 1.23 — Internet protocol stack. 책 p.50](/courses/networking/figures/ch01/fig-1-23.png)

#### Application Layer

- **역할**: application 끼리 *message 교환*
- **단위**: message
- **주소**: hostname (DNS), URL
- **Protocol**:
  - *HTTP* — web (RFC 9110)
  - *SMTP* — email send (RFC 5321)
  - *IMAP* / *POP3* — email receive
  - *DNS* — name resolution (RFC 1035)
  - *FTP* — file transfer (옛)
  - *WebSocket* — persistent bidirectional (RFC 6455)
  - *gRPC* — RPC over HTTP/2

#### Transport Layer

- **역할**: *end-to-end* (process-to-process) 통신
- **단위**: segment (TCP) or datagram (UDP)
- **주소**: port number (16-bit, 0~65535)
- **Protocol**:
  - *TCP* (Transmission Control Protocol) — 신뢰성, 순서 보장, congestion control. 95% of Internet traffic
  - *UDP* (User Datagram Protocol) — 비신뢰성, 빠름. DNS, VoIP, gaming
  - *QUIC* (over UDP) — modern TCP 대체. HTTP/3 의 transport

#### Network Layer

- **역할**: source host → destination host 의 *routing*
- **단위**: datagram (packet)
- **주소**: IP address (IPv4 32-bit, IPv6 128-bit)
- **Protocol**:
  - *IP* (Internet Protocol) — best-effort delivery (RFC 791)
  - *ICMP* — error/diagnostic (ping, traceroute 의 base)
  - *Routing protocols*: OSPF (intra-AS), BGP (inter-AS)

#### Link Layer

- **역할**: 인접 node (host ↔ router, router ↔ router) 사이 *frame* 전달
- **단위**: frame
- **주소**: MAC address (48-bit, e.g., `00:1A:2B:3C:4D:5E`)
- **Protocol**:
  - *Ethernet* (IEEE 802.3) — wired LAN
  - *WiFi* (IEEE 802.11) — wireless LAN
  - *PPP* — point-to-point (옛 dial-up)
  - *DOCSIS* — cable modem
  - *4G LTE, 5G NR* — cellular

#### Physical Layer

- **역할**: bit 를 *물리적 신호* 로 변환·전송
- **단위**: bit
- **Spec**: UTP, fiber, radio frequency
- *Modulation* (QAM, OFDM 등) — bit ↔ electrical/optical/radio signal

### §5.3 OSI Model (참고) — 7 Layer

| OSI | Internet |
|--|--|
| 7. Application | Application |
| 6. Presentation (data 형식, 암호화) | (app 포함) |
| 5. Session (대화 관리) | (app 포함) |
| 4. Transport | Transport |
| 3. Network | Network |
| 2. Link | Link |
| 1. Physical | Physical |

OSI 의 *Presentation, Session* 은 Internet 에선 *application layer 가 담당*. 학문적 7-layer, 실용 5-layer.

#### TCP/IP 4-layer 모델 (별도 변종)

- *4. Application* (App + Presentation + Session)
- *3. Transport*
- *2. Internet* (Network)
- *1. Link* (Link + Physical)

같은 system 의 *layer count 가 다른* 이유 — 어떤 boundary 를 *명시할지* 의 차이. 모두 *유효한 추상*.

### §5.4 Encapsulation — *Header 의 Nesting*

![Figure 1.24 — Hosts, routers, link-layer switches + encapsulation. 책 p.52](/courses/networking/figures/ch01/fig-1-24.png)

#### Sender 의 packet 흐름 (위→아래)

```
Layer 5 Application:  M (message, e.g. "GET / HTTP/1.1\r\n...")

Layer 4 Transport:    [H_t | M]                          ← segment
                      H_t (TCP header): src port, dst port, seq#, ack#, flags, checksum, ...
                      ~20 bytes

Layer 3 Network:      [H_n | H_t | M]                    ← datagram
                      H_n (IP header): src IP, dst IP, TTL, protocol, checksum, ...
                      ~20 bytes (IPv4) / 40 bytes (IPv6)

Layer 2 Link:         [H_l | H_n | H_t | M | T_l]        ← frame
                      H_l: src MAC, dst MAC, EtherType
                      T_l: CRC32 (error check)
                      Ethernet: 14 + 4 = 18 bytes overhead

Layer 1 Physical:     bits (electrical/optical/radio signal)
```

#### Overhead 계산

작은 packet 의 경우 *header overhead* 가 큼:

1500 byte Ethernet frame 의 구성:
- Ethernet header + trailer: 18 bytes
- IP header: 20 bytes (IPv4)
- TCP header: 20 bytes
- **Total header**: 58 bytes
- *Application data*: 1442 bytes
- *Overhead ratio*: 58 / 1500 ≈ **3.9%**

64 byte (minimum Ethernet frame) 의 경우:
- *Application data*: 6 bytes (!)
- *Overhead ratio*: 58 / 64 ≈ **90%**

→ 작은 packet 은 *극도로 비효율*. *Nagle's algorithm* (TCP 의 작은 packet 결합) 이 이를 완화.

#### Router 의 처리

- 받은 frame → Eth header *벗김*
- IP header *확인* — TTL 감소, checksum 재계산, routing table lookup → 다음 hop 결정
- *새 Ethernet header* 로 다시 *encapsulation* (다음 link 의 MAC 주소)
- → 즉 router 는 *layer 3 까지만* 본다 (TCP/payload 안 봄)

#### Switch vs Router

| | Switch | Router |
|--|--|--|
| Layer | 2 (link) | 3 (network) |
| 주소 | MAC | IP |
| Domain | one LAN (broadcast domain) | inter-network |
| Decision | MAC table (flooding + learning) | routing table (RIB → FIB) |
| Transparent? | yes (host 가 모름) | no (TTL 감소) |
| 사용 | LAN 내부 | LAN 간, 인터넷 |

---

## §6 Networks Under Attack

> 1장의 마지막 큰 주제. 8장 (Security) 의 *맛보기*. 4 가지 위협 유형.

### §6.1 Malware — *악성 코드 침투*

| 유형 | 특징 | 예시 |
|--|--|--|
| **Virus** | user action 으로 전파 (이메일 첨부 클릭, 파일 다운로드) | Macro virus, ILOVEYOU (2000) |
| **Worm** | *자동* 전파, 취약점 exploit | Code Red (2001), WannaCry (2017) |
| **Trojan** | 정상 program 으로 위장. backdoor + spyware 도 | Zeus, Emotet |
| **Ransomware** | data 암호화 + 몸값 요구 | WannaCry, REvil |
| **Botnet** | 감염된 host (= bot) 들의 *원격 제어* network | Mirai (2016, IoT 봇넷) |

**방어**:
- *Antivirus / EDR* — endpoint detection
- *Patching* — OS, application 의 *취약점 fix*
- *Sandboxing* — 의심 코드 격리 실행
- *User education* — phishing 인식

### §6.2 DoS (Denial of Service) / DDoS

![Figure 1.25 — DDoS attack. 책 p.56](/courses/networking/figures/ch01/fig-1-25.png)

> *Service 를 사용 불가* 로 만드는 공격.

**3 가지 종류**:

1. **Vulnerability attack** — exploit 으로 service crash. 예: malformed packet 으로 server kernel panic.
2. **Bandwidth flooding** — 대량 packet 으로 *link 포화*. 사용자 traffic 이 통과 못 함.
3. **Connection flooding** — TCP SYN flood. server 의 *connection pool 소진*. 진짜 사용자 못 접속.

**DDoS** (Distributed) — 수천 botnet 의 *동시 공격*. 단일 source 차단으로 막을 수 없음.

**역사적 사례**:
- 2016: Dyn DNS DDoS (Mirai botnet, 1.2 Tbps) — Twitter/Reddit/Netflix 마비
- 2018: GitHub DDoS (1.35 Tbps, memcached amplification)
- 2023: Google Cloud (398M rps, HTTP/2 rapid reset)

**방어**:
- *CDN 의 흡수* — Cloudflare, AWS Shield 가 *수십 Tbps 대응*
- *Rate limiting* — IP/사용자 단위
- *Ingress filtering* — 의심 source 차단
- *Anycast* — traffic 을 *여러 PoP* 에 분산
- *SYN cookies* — half-open connection 회피

### §6.3 Packet Sniffing — *도청*

- *Promiscuous* network interface 가 *링크 위 모든 packet* 캡처
- 같은 WiFi 의 *다른 사용자* 의 traffic 도 볼 수 있음 (옛 WiFi)
- 도구: **Wireshark**, **tcpdump**, **ettercap**

**방어**:
- *TLS* (Transport Layer Security) — 모든 traffic *end-to-end 암호화*. 2020년대엔 *encrypted-by-default*
- *WPA3* — WiFi 의 *peer-encryption* (옛 WPA2 의 약점 보완)
- *VPN* — 모든 traffic 을 *tunnel* 로

> *TLS 후 packet sniffing 의 한계* — payload 는 *암호화*. 그러나 *metadata* (출발지/목적지 IP, hostname (SNI), packet size, timing) 는 여전히 노출.

### §6.4 IP Spoofing

> 잘못된 *source IP* 를 가진 packet.

**용도**:
- DDoS reflection — *attack target 의 IP* 를 source 로 위장, *DNS/NTP server* 에 query. server 가 *target 에 reply* → amplification
- *Authentication bypass* — IP 기반 ACL 우회

**방어**:
- *Ingress filtering* (BCP 38) — ISP 의 *경계 router* 가 *outgoing packet 의 source IP* 가 *자기 prefix* 인지 검증
- *Authentication 강화* — IP 기반 ACL 회피, 항상 *cryptographic auth* (TLS client cert, OAuth token)

→ 8장 (Security) 에서 *깊은 처리* — cryptography, TLS handshake, IPSec, blockchain.

---

## §7 History of Computer Networking — *진화의 5 era*

![Figure 1.26 — 초기 packet switch. 책 p.59](/courses/networking/figures/ch01/fig-1-26.png)

### §7.1 1961~1972: Packet Switching 의 *탄생*

핵심 인물·사건:
- **Leonard Kleinrock** (MIT, 1961) — packet switching 의 *queuing theory* 기반
- **Paul Baran** (RAND, 1964) — *survivable network* (핵 공격에 견디는 통신망)
- **Donald Davies** (NPL, 1965) — "packet" 용어 창안
- **ARPANET** (1969) — 첫 packet 교환 network. 4 node (UCLA, **SRI** (Stanford Research Institute, 현 SRI International), UCSB, Utah)
- **NCP (Network Control Protocol)** (1972) — ARPANET 의 *첫 host protocol*

### §7.2 1972~1980: 다른 network 들 + Internetworking

- **Ethernet** (1976, Metcalfe + Boggs at Xerox PARC) — LAN의 시작
- **ALOHANET** (1970, 하와이) — wireless packet switching
- **TCP/IP 의 시작** — Vint Cerf + Bob Kahn, "*A Protocol for Packet Network Intercommunication*" (1974)
- *DECNet*, *SNA* (IBM), *XNS* (Xerox) — proprietary networks 의 *전성기*

핵심 통찰 — 어떻게 *서로 다른 network* 를 연결? → *common protocol* (TCP/IP) + *gateway/router*.

### §7.3 1980~1990: 표준화 + 폭증

- **TCP/IP 의 ARPANET 채택** (1983-01-01) — Internet 의 *생일*. NCP → TCP/IP cutover.
- **DNS** (Mockapetris, 1983) — IP 주소 → name. *수동 hosts.txt* 의 한계 해결
- **NSFNET** (1986) — 미국 과학재단 backbone. ARPANET 의 *민간 후속*
- *각종 LAN technology* 정착: Ethernet, Token Ring (IBM), FDDI

### §7.4 1990s: WWW + Commercialization

핵심 사건:
- **WWW 발명** — Tim Berners-Lee, CERN, 1989-1991. HTTP + HTML + URL
- **Mosaic browser** (1993, NCSA) — *graphical browser* 의 시작. 비-기술자도 web 사용
- **Netscape** (1994) — 상용 browser. 1995 IPO 는 dot-com era 의 시작
- **NSFNET 해체** (1995) — 민간 ISP 의 *commercial Internet* 으로 전환
- *dot-com 거품* — 2000년대 초 폭락, 그러나 *infrastructure 는 남음*

기술 발전:
- *PPP* (dial-up modem) — 가정 Internet
- *DSL* + *Cable* — broadband 시작
- *DNS root server* 글로벌 분산
- *Java*, *JavaScript*, *cookies* — 동적 web 의 기반

### §7.5 2000s ~ 현재: Mobile + Cloud + Content

**2000년대**:
- *WiFi 보급* — 가정·카페·공항
- *Web 2.0* — user-generated content (YouTube, Facebook, Twitter)
- *AWS* (2006) — *cloud computing* 의 시작
- *iPhone* (2007) — mobile-first 시대

**2010년대**:
- *4G LTE* — 모바일 broadband
- *CDN 의 보편화* — Akamai, Cloudflare, Fastly
- *HTTPS-by-default* (Let's Encrypt, 2016)
- *Streaming dominance* — Netflix, YouTube 가 Internet traffic 의 50%+

**2020년대 (현재)**:
- *5G* deployment
- *IoT* — 수십억 device (smart home, industrial sensors)
- *Edge computing* — Lambda@Edge, Cloudflare Workers
- *Encrypted-by-default* — HTTPS, DNS-over-HTTPS, encrypted SNI
- *QUIC / HTTP/3* — TCP 의 한계 극복
- *Satellite mega-constellation* — Starlink, OneWeb (LEO 50ms RTT)
- *AI/ML traffic* — LLM API, distributed training

![Figure 1.27 — End-to-end message transport. 책 p.69](/courses/networking/figures/ch01/fig-1-27.png)
![Figure 1.28 — Wireshark screenshot. 책 p.71](/courses/networking/figures/ch01/fig-1-28.png)

### §7.6 *지속되는 원칙*

50년 진화에도 *변하지 않은 것*:
1. **Packet switching** — Kleinrock 의 theory 가 *여전히* 토대
2. **End-to-end argument** — *intelligence at edges*, *dumb middle*
3. **Open standards (IETF)** — proprietary 가 *반복적으로* 패배
4. **Layered architecture** — 5 layer stack 의 *변화 없음*
5. **Best effort delivery** — 보장 없는 *단순한 service* 가 *flexibility* 의 근원

이 *원칙들* 이 *왜 강건한가* — 후속 chapter 들에서 깊이 다룸.

---

## §8 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "Internet" = "WWW" | Internet = network of networks. WWW = HTTP-based application |
| 2 | High bandwidth = High throughput | bottleneck link, protocol overhead, loss 가 결정 |
| 3 | Packet switching > Circuit switching always | bursty 에 packet, 지속·실시간 부하에 circuit |
| 4 | Queueing delay = Propagation delay | 4 종 delay 가 다른 *원인 + 의존 변수* |
| 5 | Trans delay = Prop delay | trans = "link 에 *밀어내는*", prop = "*이동* 하는". link 속도 vs 거리 |
| 6 | Layer 가 *느슨한* 권고 | 강한 separation. interface 의 *contract*. Wireless 같은 cross-layer 는 예외 |
| 7 | OSI = Internet protocol stack | OSI 7 vs Internet 5. *Presentation/Session* 통합 |
| 8 | Encapsulation 의 *각 layer 가 자기 layer* 만 봄 | router 는 layer 3 까지, switch 는 layer 2 까지 |
| 9 | DDoS 가 *흔히 단일 source* | *분산* — 수천 botnet 의 동시 공격 |
| 10 | TLS 후 *완전 안전* | metadata (IP, SNI, packet size, timing) 노출. *Tor*, encrypted SNI 가 추가 layer |
| 11 | Wireshark 의 *패킷 캡처가 항상 OK* | TLS payload 암호화. 또한 *법적 동의* 없는 sniffing 은 illegal |
| 12 | Internet 이 *중앙 통제 system* | *no central authority*. ISP 들의 *자발적* 협력 (BGP, IXP). IANA 의 *coordination*. |
| 13 | "한국 Internet 이 *세계 1위*" | 단순 access speed 만. *latency*, *open Internet*, *fair pricing* 등 다른 지표는 다름 |
| 14 | IPv4 가 *이미 고갈* | regional pool 고갈, 그러나 *recycling + IPv6 dual-stack* 으로 사용 계속 |

---

## §9 자가점검

1. *Internet* 의 두 가지 정의 (nuts-and-bolts + services).
2. *Protocol* 의 3 요소 (format, order, actions).
3. *Access network* 의 5 종 + 각 속도.
4. *Packet switching* vs *circuit switching* 의 *수학적* trade-off (statistical multiplexing 예제).
5. *Nodal delay* 의 4 component + 각 정의식.
6. *Traffic intensity* $\rho = La/R$ + $\rho \to 1$ 에서 queue 의 *수학적* 거동.
7. *Bottleneck link* 가 throughput 어떻게 결정.
8. *BDP* 와 *Mathis equation* 의 의미.
9. *Internet protocol stack* 5 layer + 각 단위 (segment, datagram, frame).
10. *Encapsulation* 의 *header overhead* 가 small packet 에 미치는 영향.
11. *Router* 와 *switch* 의 *layer 차이*.
12. *DDoS* 의 *3 가지 종류* + 각 방어.
13. *IETF + RFC* 의 표준화 process.
14. *Internet 의 지속 원칙* 5 가지.

### 해답 (간략)

1. Nuts-and-bolts: end systems + links + routers + ISP 의 network of networks. Services: distributed application 에 service 제공.
2. Format (message 모양), Order (송수신 순서), Actions (송수신 시 처리).
3. DSL (5-50M, copper, dedicated), Cable (100M-Gbps, coax, shared), FTTH (1Gbps+, fiber), Ethernet (100M-10G, UTP), WiFi/Cellular (~100M-Gbps, radio).
4. 10명 사용자 × 100 kbps × 10% 활성: circuit 은 1 Mbps 예약 (10% efficient), packet 은 1 Mbps 충분 + 동시 10명 확률 거의 0 → bursty 에 우월.
5. $d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$. proc (μs, 일정), queue (가장 가변), trans=L/R (link push), prop=d/s (물리 이동).
6. ρ<1 안정, ρ→1 delay 폭주 (M/M/1: $\rho/(1-\rho) \cdot L/R$), ρ>1 loss.
7. 경로의 *가장 느린 link* 가 limit. high-bandwidth 다른 link 는 도움 안 됨.
8. BDP = R × RTT, link 의 in-flight 데이터. Mathis: $T \approx MSS / (RTT \sqrt{p})$ — loss 의 sqrt 비례 감소.
9. App (message), Transport (segment), Network (datagram), Link (frame), Physical (bits).
10. 58 bytes header. 1500 byte frame 에선 4% overhead, 64 byte 에선 90%. → 작은 packet 비효율.
11. Router: layer 3 (IP), inter-network routing. Switch: layer 2 (MAC), one LAN 안의 forwarding.
12. (a) vulnerability (exploit). (b) bandwidth flooding (link 포화). (c) connection flooding (SYN flood). 방어: CDN, rate limiting, ingress filtering, SYN cookies.
13. IETF 가 open community, RFC 가 표준 문서. *rough consensus + running code* 원칙. 9000+ RFC.
14. (1) packet switching (2) end-to-end argument (3) open standards (4) layered architecture (5) best effort delivery.

---

## §10 다음 학습으로

- **2장 (Application Layer)** — top-down 의 *첫 layer*. HTTP/1.1, HTTP/2, HTTP/3, DNS, SMTP, P2P (BitTorrent), socket programming
- **3장 (Transport Layer)** — TCP 의 reliable data transfer, congestion control (Reno, CUBIC, BBR), UDP, QUIC
- **4-5장 (Network Layer)** — IP addressing (IPv4/IPv6), subnetting, routing protocols (OSPF, BGP), SDN, MPLS
- **6장 (Link Layer)** — Ethernet frame, switching, ARP, VLAN
- **7-8장** — WiFi (802.11), cellular (4G/5G), security (cryptography, TLS, IPSec)

> Top-down approach 의 의미 — *application 의 요구* 부터 시작해 *물리적 구현* 까지 내려감. 1장의 *지도* 가 모든 후속 챕터의 *위치 + 동기* 를 보여준다. 다시 돌아오면서 *각 layer 의 service 가 왜 그런 모양인지* 깊이 이해될 것.

> **공부 팁** — 이 장의 *수식·예제* 는 *암기보다 직접 계산*. 자기 가정의 ISP 속도, RTT (`ping`), traceroute hop 수를 측정하고 위 공식에 *직접 넣어* 보면 *직관이 강해짐*. *Wireshark* 로 자기 HTTP 요청을 *캡처* 해 *5 layer encapsulation* 을 *시각적으로* 보면 잊을 수 없는 학습.

---

## §11 한 줄 요약

> **Internet = 중앙 통제 없는 *network of networks*. *protocol*(format·order·actions)로 말하고, bursty 트래픽을 *packet switching* 으로 통계 다중화한다. 성능은 *4 delay*(proc·queue·trans·prop)와 bottleneck throughput 으로 정량화되고, 전체는 *5-layer stack + encapsulation* 으로 조직된다. 1장은 2~8장 모든 어휘의 *지도* 다.**
