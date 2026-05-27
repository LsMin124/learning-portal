# Chapter 1: Computer Networks and the Internet — 학습 노트

> *Computer Networking: A Top-Down Approach* (Kurose & Ross, 8th Global Edition, 2021) **Chapter 1** (책 p.33~112).
> 1장은 책 전체의 *지도*. **Top-down approach** — application 부터 시작해 link layer 까지 내려가는 책의 *철학* 을 소개. 이후 2~6장이 각 layer 의 상세.

## 들어가기 전에

- **선수 지식**: 컴퓨터 사용 경험, 기본 TCP/IP / HTTP 용어 익숙
- **학습 목표**
  1. *Internet 의 정의* — "network of networks", end systems + links + routers
  2. **Network edge** — host, access network (DSL, cable, fiber, WiFi, cellular)
  3. **Network core** — *packet switching* vs *circuit switching*
  4. **Performance metrics** — *delay* (4종), *loss*, *throughput*
  5. **Protocol stack 5 layers** — application / transport / network / link / physical
  6. **Encapsulation** — 각 layer 가 header 추가
  7. *Security* 의 4 가지 위협 형태
- **예상 학습 시간**: 120~150분

---

## 1. What Is the Internet?

### 1.1 Nuts-and-Bolts View

> *수십억 개의 connected computing devices*

**Components**:
- **End systems / hosts**: PC, smartphone, IoT device, server
- **Communication links**: copper, fiber, radio
- **Packet switches**: routers, link-layer switches
- **ISP (Internet Service Provider)**: tier-1 (Sprint, AT&T), regional, access

![Figure 1.1 — Internet 의 일부 구성요소. 책 p.3](/courses/networking/figures/ch01/fig-1-1.png)

### 1.2 Services View

> *applications 에 서비스를 제공* 하는 infrastructure

- *Distributed applications* — 여러 host 에서 동시 실행 (web, email, streaming, games)
- *Application Programming Interface (API)* — host 가 *Internet 에 어떻게 access* 하는지 정의 — *socket interface*

### 1.3 What's a Protocol?

> *Protocol* = 두 entity 사이의 *통신 규칙*

![Figure 1.2 — 사람의 protocol vs 컴퓨터 network protocol. 책 p.7](/courses/networking/figures/ch01/fig-1-2.png)

핵심:
- *Format* — message 의 모양
- *Order* — message 송수신 순서
- *Actions* — 송수신 시 *어떻게 처리*

예 — HTTP request/response:
```
GET / HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: text/html
<html>...
```

---

## 2. Network Edge

### 2.1 End Systems

= **hosts**:
- *Client*: 일반 PC, mobile (대부분)
- *Server*: data center 의 서비스 (Google, AWS)

![Figure 1.3 — End system 간 통신. 책 p.10](/courses/networking/figures/ch01/fig-1-3.png)

### 2.2 Access Networks

end system 을 *Internet 에 연결* 하는 *first-hop network*:

![Figure 1.4 — Access network 들. 책 p.12](/courses/networking/figures/ch01/fig-1-4.png)

| 종류 | 속도 | 기술 |
|--|--|--|
| **DSL** | 5~50 Mbps | 전화선 (copper twisted pair) |
| **Cable / HFC** | 100 Mbps~Gbps | TV 동축 케이블 |
| **FTTH / PON** | 1 Gbps+ | 광섬유 |
| **Ethernet (학교/회사)** | 100 Mbps~10 Gbps | UTP, fiber |
| **WiFi** | ~100 Mbps~Gbps | 무선 LAN (IEEE 802.11) |
| **Cellular (4G/5G)** | 10 Mbps~Gbps | mobile carrier |

![Figure 1.5 — DSL Internet access. 책 p.13](/courses/networking/figures/ch01/fig-1-5.png)
![Figure 1.6 — Cable (HFC) access. 책 p.14](/courses/networking/figures/ch01/fig-1-6.png)
![Figure 1.7 — FTTH with PON. 책 p.16](/courses/networking/figures/ch01/fig-1-7.png)

### 2.3 Physical Media

| Media | 특성 |
|--|--|
| Twisted-pair copper | 저가, 가까운 거리 |
| Coaxial cable | TV, broadband |
| Fiber-optic | 매우 빠름, 거리 영향 적음 |
| Radio | wireless, 신호 약해짐 |

---

## 3. Network Core

### 3.1 Packet Switching — Internet 의 핵심

![Figure 1.10 — Network core. 책 p.22](/courses/networking/figures/ch01/fig-1-10.png)

> Source 가 message 를 *packet* 으로 쪼개고, 각 packet 이 *router* 들을 거쳐 destination 으로.

**Store-and-forward transmission**:
- Router 가 *전체 packet 을 받은 후* 다음 link 로 forward
- Packet 의 *전송 시간* = L (bits) / R (bps)
- 전체 *2-hop end-to-end delay* = 2L/R

![Figure 1.11 — Store-and-forward. 책 p.24](/courses/networking/figures/ch01/fig-1-11.png)
![Figure 1.12 — Packet switching. 책 p.25](/courses/networking/figures/ch01/fig-1-12.png)

**Queuing delay + loss**:
- Router 가 *output buffer* 보유
- 도착 packet > 처리 능력 → buffer full → *packet drop*

### 3.2 Circuit Switching — 전화망의 방식

![Figure 1.13 — Circuit switching. 책 p.27](/courses/networking/figures/ch01/fig-1-13.png)

> 두 end system 사이 *전용 회선* (circuit) 을 *예약*. 통신 동안 *bandwidth 보장*.

- **FDM (Frequency-Division Multiplexing)** — frequency 대역 분할
- **TDM (Time-Division Multiplexing)** — time slot 분할

![Figure 1.14 — FDM vs TDM. 책 p.29](/courses/networking/figures/ch01/fig-1-14.png)

**Packet vs Circuit**:

| | Packet | Circuit |
|--|--|--|
| 자원 할당 | on-demand, statistical multiplexing | 예약 (reservation) |
| 효율 | 평균 부하 ↓ 시 우수 | 일정 부하에 우수 |
| 보장 | best effort | bandwidth 보장 |
| 사용 | Internet | 옛 전화망 (PSTN) |

> Internet 이 *packet switching 채택* 이유 — *bursty* traffic 에 효율적 + 단순한 router.

### 3.3 ISP 의 계층 — Network of Networks

![Figure 1.15 — ISP 의 상호연결. 책 p.34](/courses/networking/figures/ch01/fig-1-15.png)

- **Tier-1 ISP** — 다른 모든 tier-1 와 *peer* (대등 교환). 글로벌 backbone.
- **Regional ISP** — tier-1 에 *transit* 비용 지불
- **Access ISP** — 사용자에게 *마지막 1마일* 제공
- **IXP (Internet Exchange Point)** — ISP 들이 *peering* 하는 물리 위치
- **Content provider** (Google, Netflix) — 자기 *private network* + CDN

---

## 4. Delay, Loss, Throughput

### 4.1 Nodal Delay 의 4 종

![Figure 1.16 — Nodal delay 의 종류. 책 p.36](/courses/networking/figures/ch01/fig-1-16.png)

$$d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$$

- **Processing delay** ($d_{proc}$): packet header 검사, error check. *microsecond*
- **Queuing delay** ($d_{queue}$): buffer 에서 대기. *traffic intensity 의존, 가장 가변*
- **Transmission delay** ($d_{trans} = L/R$): packet 을 link 에 *밀어내는* 시간
- **Propagation delay** ($d_{prop} = d/s$): bit 가 link 위를 *물리적으로 이동* 하는 시간 (s ≈ 2×10⁸ m/s)

### 4.2 Caravan 비유 (책의 명물)

![Figure 1.17 — Toll booth 의 자동차 행렬 비유. 책 p.38](/courses/networking/figures/ch01/fig-1-17.png)

- *toll booth* = router (transmission)
- *자동차* = bit
- *도로* = link (propagation)

→ propagation = *highway 운전 시간*, transmission = *toll 통과 시간*.

### 4.3 Traffic Intensity 와 Queuing

![Figure 1.18 — Traffic intensity 의 queuing delay 영향. 책 p.40](/courses/networking/figures/ch01/fig-1-18.png)

- Traffic intensity $\rho = La/R$
  - L: packet size (bits)
  - a: average arrival rate (pps)
  - R: link bandwidth (bps)
- $\rho < 1$: queue 안정. delay 적음
- $\rho \to 1$: delay 폭주 (asymptote)
- $\rho > 1$: queue 무한 성장 → *loss*

### 4.4 Throughput

![Figure 1.19 — File transfer 의 throughput. 책 p.44](/courses/networking/figures/ch01/fig-1-19.png)

> Sender 부터 receiver 까지 *초당 bit 전송량*.

**Bottleneck link** — 경로 위의 *가장 느린 link* 가 throughput 결정.

![Figure 1.20 — End-to-end throughput. 책 p.46](/courses/networking/figures/ch01/fig-1-20.png)

> **함정 1**: high bandwidth ≠ high throughput. 다른 link 가 *병목* 이면 그것이 limit.

---

## 5. Protocol Layers + Encapsulation

### 5.1 Layered Architecture

![Figure 1.21 — 비행기 여행의 계층. 책 p.47](/courses/networking/figures/ch01/fig-1-21.png)
![Figure 1.22 — 비행기 functionality 의 horizontal layering. 책 p.48](/courses/networking/figures/ch01/fig-1-22.png)

> *Modular design* — 각 layer 가 *자기 task* 만, 위 layer 에 *service* 제공.

### 5.2 Internet Protocol Stack — 5 Layers

![Figure 1.23 — Internet protocol stack. 책 p.50](/courses/networking/figures/ch01/fig-1-23.png)

| Layer | 역할 | Protocol 예 |
|--|--|--|
| **Application** | 사용자 application 의 통신 | HTTP, SMTP, DNS, FTP |
| **Transport** | end-to-end *process* 간 통신 | TCP, UDP |
| **Network** | host 간 *routing* | IP, ICMP |
| **Link** | 인접 node 사이 *frame* 전달 | Ethernet, WiFi (802.11), PPP |
| **Physical** | bit 의 *물리적* 전송 | UTP, fiber, radio |

**OSI 7 layer** (참고):
- Application + Presentation + Session + Transport + Network + Link + Physical
- Internet 은 *Presentation, Session* 통합 — application 책임

### 5.3 Encapsulation

![Figure 1.24 — Hosts, routers, link-layer switches + encapsulation. 책 p.52](/courses/networking/figures/ch01/fig-1-24.png)

각 layer 가 *header 추가*:

```
Application:  [data]
Transport:    [TCP header | data]                    ← segment
Network:      [IP header | TCP header | data]        ← datagram
Link:         [Frame header | IP header | TCP header | data | Frame trailer]  ← frame
Physical:     bits...
```

**Switch** vs **Router**:
- Switch (link layer): MAC 주소 기반
- Router (network layer): IP 주소 기반, *layer 3 까지* 확인

---

## 6. Networks Under Attack

> 4 가지 주요 위협:

### 6.1 Malware

- *Virus*: user action 으로 전파 (이메일 첨부 클릭)
- *Worm*: 자동 전파 (취약점 exploit)
- *Trojan*: 정상 program 으로 위장

### 6.2 DoS / DDoS Attack

![Figure 1.25 — DDoS attack. 책 p.56](/courses/networking/figures/ch01/fig-1-25.png)

- **Vulnerability attack** — exploit 으로 service crash
- **Bandwidth flooding** — 대량 packet 으로 link 포화
- **Connection flooding** — TCP SYN flood, 서버의 connection pool 소진

**DDoS** — *수천 botnet* 에서 공격 → mitigation 어려움.

### 6.3 Packet Sniffing

- *Promiscuous* network interface 가 *모든 packet* 캡처
- Wireshark, tcpdump 가 도구
- *Defense*: TLS, end-to-end 암호화

### 6.4 IP Spoofing

- 잘못된 *source IP* 의 packet
- *Defense*: ingress filtering, authentication

→ 8장 (Security) 에서 깊은 처리.

---

## 7. History (간략)

![Figure 1.26 — 초기 packet switch. 책 p.59](/courses/networking/figures/ch01/fig-1-26.png)

- **1961~1972**: Kleinrock 의 packet switching 이론. ARPANET (1969).
- **1972~1980**: TCP/IP 의 시작. Ethernet (Metcalfe 1976).
- **1980~1990**: Internet 의 *naming + numbering* — DNS, IP 주소.
- **1990s**: WWW (Berners-Lee 1991), commercialization, dot-com.
- **2000s~**: broadband 폭증, mobile, social media, cloud.
- **현재**: 5G, IoT, *encrypted-by-default*, content-driven (CDN).

![Figure 1.27 — End-to-end message transport. 책 p.69](/courses/networking/figures/ch01/fig-1-27.png)
![Figure 1.28 — Wireshark screenshot. 책 p.71](/courses/networking/figures/ch01/fig-1-28.png)

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "Internet" = "WWW" | Internet = network of networks. WWW = HTTP-based application 의 하나 |
| 2 | High bandwidth = High throughput | bottleneck link 가 결정 |
| 3 | Packet switching > Circuit switching always | bursty 에 packet, 지속 부하에 circuit |
| 4 | Queueing delay = Propagation delay | 4 종 delay 가 다 다른 원인 |
| 5 | Layer 가 *느슨한* 권고 | 강한 separation. interface 의 *contract* |
| 6 | OSI = Internet protocol stack | OSI 는 7 layer, Internet 은 5 layer |
| 7 | Encapsulation 의 *각 layer 가 자기 layer* 만 봄 | router 는 *layer 3 까지*, switch 는 *layer 2 까지* 확인 |
| 8 | DDoS 가 *흔히 단일 source* | *분산* — 수천 source 의 동시 공격 |
| 9 | Wireshark 의 *패킷 캡처가 항상 OK* | TLS 후 payload 암호화. metadata 만 보임 |
| 10 | Internet 이 *중앙 통제 system* | *no central authority*. ISP 들이 *자발적* 협력 (BGP, IXP) |

---

## 자가점검

1. *Internet* 의 두 가지 정의 (nuts-and-bolts + services).
2. *Protocol* 의 3 요소 (format, order, actions).
3. *Access network* 의 5 종 + 각 속도.
4. *Packet switching* vs *circuit switching* 의 trade-off.
5. *Nodal delay* 의 4 component + 각 정의식.
6. *Traffic intensity* $\rho = La/R$ + $\rho \to 1$ 의 의미.
7. *Bottleneck link* 가 throughput 어떻게 결정.
8. *Internet protocol stack* 5 layer + 각 단위 (segment, datagram, frame).
9. *Encapsulation* 의 *header* 추가 방향.
10. *Router* 와 *switch* 의 *layer 차이*.

### 해답 (간략)

1. Nuts-and-bolts: end systems + links + routers + ISP 의 network of networks. Services: distributed application 에 서비스 제공.
2. Format (message 모양), Order (송수신 순서), Actions (송수신 시 처리).
3. DSL (5-50M), Cable (100M-Gbps), FTTH (1Gbps+), Ethernet (100M-10G), WiFi/Cellular (~100M-Gbps).
4. Packet: bursty traffic 효율, on-demand. Circuit: bandwidth 보장, 일정 부하에 효율.
5. $d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$. proc (header 검사), queue (대기), trans=L/R (link push out), prop=d/s (물리 이동).
6. ρ<1 안정, ρ→1 delay 폭주, ρ>1 loss.
7. 경로의 *가장 느린 link* 가 limit.
8. App (message), Transport (segment), Network (datagram), Link (frame), Physical (bits).
9. Top → bottom 으로 *내려가며 header 추가*. Receiving 은 *반대로 header 벗김*.
10. Router: layer 3 (IP), routing 결정. Switch: layer 2 (MAC), forwarding 만.

---

## 다음 학습으로

- **2장 (Application Layer)** — top-down 의 *첫 layer*. HTTP, SMTP, DNS, P2P
- **3장 (Transport Layer)** — TCP, UDP, reliable data transfer, congestion control
- **4-5장 (Network Layer)** — routing, IP addressing, BGP
- **6장 (Link Layer)** — Ethernet, switching, ARP
- **7-8장 (Wireless, Security)** — WiFi/cellular + cryptography

Top-down approach 의 의미 — *application 의 요구* 부터 시작해 *물리적 구현* 까지 내려감. 1장의 *지도* 가 모든 후속 챕터의 위치를 보여준다.
