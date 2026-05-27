# Chapter 2: Application Layer — 학습 노트

> *Computer Networking: A Top-Down Approach* (Kurose & Ross, 8th Global Edition, 2021) **Chapter 2** (책 p.113~212).
> 2장은 *top-down 의 첫 layer*. 우리가 매일 사용하는 **HTTP, DNS, SMTP, BitTorrent, video streaming** 의 동작 + 그 *protocol 의 모양*. 1장의 *application 동기* 가 여기서 본격적으로 풀린다.

## 들어가기 전에

- **선수 지식**: 1장 (encapsulation, protocol 의 3요소, host/router/ISP), HTTP·DNS 의 *명칭 정도* 익숙
- **학습 목표**
  1. **Application architecture** — *client-server* vs *peer-to-peer (P2P)*
  2. **Transport service 의 4 요구** — reliable transfer, throughput, timing, security
  3. **HTTP** — *stateless* protocol, persistent vs non-persistent, HTTP/1.1 vs HTTP/2 vs HTTP/3
  4. **Cookie + Web cache + CDN** — *stateless* 위에 *stateful* 구축
  5. **DNS** — distributed hierarchical database. iterative vs recursive query
  6. **Email** — SMTP (push) + IMAP/POP (pull)
  7. **P2P** — BitTorrent 의 *fairness* mechanism + tit-for-tat
  8. **Video streaming** — DASH + adaptive bitrate
  9. **Socket programming** — TCP/UDP 의 *Python API*
- **예상 학습 시간**: 200~240분
- **이 장의 사용법** — *protocol 의 모양* 을 *실제 헤더 byte* 로 보면 잊을 수 없음. `curl -v`, `dig`, `nslookup`, Wireshark 가 가장 좋은 학습 도구.

---

## 1. Principles of Network Applications

### 1.1 Application Architecture — 두 가지 모델

#### Client-Server

> *server* 는 *always-on*, *fixed IP*. *client* 가 *server 에게 request*.

![Figure 2.1 — Client-server vs P2P. 책 p.85](/courses/networking/figures/ch02/fig-2-1.png)

전형 — Web (HTTP), Email (SMTP), Streaming (Netflix), Cloud service.

**특징**:
- *Asymmetric* — server 는 *서비스 제공*, client 는 *서비스 소비*
- *Scalability* — 큰 server farm (Google: 수십만 server) + load balancer
- 사용자는 *서로 직접 통신 안 함* — 항상 *server 경유*

**Server farm** 의 운영:
- 단일 datacenter 의 수만~수십만 server
- *DNS-based load balancing* — 같은 hostname 의 IP 가 *여러 개*
- *CDN* (Content Delivery Network) — geographic distribution

#### Peer-to-Peer (P2P)

> *Server 없음*. *Peers (= end systems)* 가 *서로 직접 통신*.

전형 — BitTorrent (file sharing), Skype 원래 (P2P calling), Bitcoin / Ethereum (blockchain).

**특징**:
- *Self-scalability* — 사용자 N 명이 늘면 *capacity 도 N 명만큼 증가* (서로 upload). server-client 의 *N 명 server 부하 ↑* 와 반대.
- *결점*: NAT/firewall 통과 어려움, *churn* (peer 들어왔다 나갔다), 보안

#### Hybrid (실제 산업)

순수 P2P 는 드물고 *hybrid*:
- Skype: P2P + central directory (login + NAT traversal)
- WhatsApp: client-server (E2E encryption 만 P2P 같이)
- BitTorrent: P2P + *tracker* (peer 찾기)

### 1.2 Process Communication

#### Process = *running program*

같은 host 안의 *프로세스* 들 — OS 가 IPC (inter-process communication) 로 통신.
다른 host 의 *프로세스* 들 — *network 의 message 교환*.

#### Socket — *door* between application and network

![Figure 2.3 — Application process, socket, transport protocol. 책 p.88](/courses/networking/figures/ch02/fig-2-3.png)

Socket 의 비유:
- *Application process* = *집 안의 거주자*
- *Socket* = *집의 현관문*
- *Transport infrastructure* = *우체국 + 도로*

Socket 으로 application 이 *transport service* 사용. socket API 는 *OS 가 제공*.

#### Addressing — *host + process* 식별

두 단계:
1. **Host address** — IP address (32-bit IPv4, 128-bit IPv6)
2. **Process identifier** — port number (16-bit, 0~65535)

*Well-known ports*:
- 22: SSH
- 25: SMTP
- 53: DNS
- 80: HTTP
- 443: HTTPS
- 3306: MySQL
- 5432: PostgreSQL
- 6379: Redis
- 27017: MongoDB

### 1.3 Transport Service 의 4 가지 요구

application 마다 transport 에 *다른 요구*:

#### (1) Reliable Data Transfer

> 모든 byte 가 *손실 없이, 순서대로* 도착.

- *필요*: file transfer, email, web (HTTP body) — *한 byte 도 손실되면 안 됨*
- *불필요*: real-time audio/video — 일부 loss 보다 *시간 우선*

#### (2) Throughput

> *초당 bit 전송량*.

- *Bandwidth-sensitive* — 영상 통화 (특정 throughput 보장 필요)
- *Elastic* — email, file transfer (throughput 다양해도 OK)

#### (3) Timing — *Low latency*

> 한 packet 의 *전송 + 수신 시간* 의 한계.

- *Interactive games, telephony* — < 100ms RTT (사람의 *지각 한계*)
- *Web* — < 1 sec page load (사용자 *체감 임계*)
- *Email, batch download* — 분 단위 OK

#### (4) Security

> 암호화 + 인증.

- *Banking, login* — TLS 필수
- *Public information* — 옵션, but 현대는 *encrypted-by-default*

### 1.4 Internet Transport Service — TCP vs UDP

![Figure 2.4 — Internet transport protocol 의 service requirement 비교. 책 p.92](/courses/networking/figures/ch02/fig-2-4.png)

| Application | Reliable | Throughput | Timing | Protocol |
|--|--|--|--|--|
| File transfer (FTP, HTTP) | yes | elastic | tolerant | **TCP** |
| Email | yes | elastic | tolerant | **TCP** |
| Web (HTTP) | yes | elastic | < 1s | **TCP** (HTTP/3 는 QUIC) |
| Streaming video | no (some loss OK) | many Mbps | tolerant | **TCP** (with buffer) |
| Interactive game | no | few kbps | < 100ms | **UDP** |
| VoIP / video conf | no | few kbps | < 100ms | **UDP** (RTP) |
| DNS | no | n/a | < 100ms | **UDP** (small) |

**TCP** 가 *대다수* 의 application — reliability + congestion control 의 가치.
**UDP** 는 *latency-critical* + *small message* 만.

> **함정 1**: "UDP 가 빠르다" 의 오해. 실제 *TCP setup overhead* 가 작음 — 1 RTT (HTTP/2) 또는 0 RTT (HTTP/3 + TLS resumption). UDP 가 "빠른" 건 *congestion control 부재* 의 결과 — 부하 시 *unfair*.

---

## 2. The Web and HTTP

### 2.1 Web 의 구조

#### Web page = *base HTML* + *referenced objects*

```
http://example.com/index.html
  ↓ HTML 파싱
  ├── <img src="logo.png">
  ├── <link rel="stylesheet" href="style.css">
  ├── <script src="main.js">
  └── ... (다른 image, video, font)
```

전형 web page = 1 HTML + 수십~수백 *referenced objects*.

#### URL — *Uniform Resource Locator*

```
https://www.example.com:443/path/to/page?query=1#section
└─┬─┘ └──────┬───────┘└┬┘└──────┬───────┘└──┬───┘└──┬──┘
scheme   hostname    port    path        query  fragment
```

- *scheme* — protocol (http, https, ftp, ws)
- *hostname* — DNS 로 IP 해석
- *port* — 생략 시 *scheme 의 default* (http=80, https=443)
- *path* — server 의 *resource path*
- *query* — `?key=value&key2=value2`
- *fragment* — client-side only (browser 의 *anchor*)

### 2.2 HTTP 의 동작

> **HTTP** = HyperText Transfer Protocol. *Web 의 application-layer protocol*. RFC 9110 (2022 reorganized).

![Figure 2.6 — HTTP request/response. 책 p.97](/courses/networking/figures/ch02/fig-2-6.png)

#### Stateless

> HTTP server 는 *client 의 이전 요청을 기억하지 않음*.

각 request 가 *독립* — server 는 *과거 request* 와 무관하게 처리.

**시사**:
- Server 가 *상태 관리 부담* 없음 → scalable
- 그러나 *세션* (로그인) 이 필요 → *cookie* 로 우회 (§2.4)

#### Non-persistent HTTP — HTTP/1.0

각 *object* 마다 *별도 TCP connection*:

```
1. Client → Server: TCP handshake (1 RTT)
2. Client → Server: HTTP GET /index.html
3. Server → Client: HTTP response
4. TCP close
5. Client → Server: TCP handshake (1 RTT)  ← 같은 server!
6. Client → Server: HTTP GET /logo.png
7. ...
```

**문제**: object 10개 면 *10 × (1 TCP handshake + 1 HTTP request) = 20 RTT*. 매우 느림.

**Response time** for one object:
$$\text{Total} = 2 \text{ RTT} + \text{file transmission time}$$
- 1 RTT: TCP handshake
- 1 RTT: HTTP request + first byte
- file: $L/R$

#### Persistent HTTP — HTTP/1.1

> *같은 TCP connection* 으로 여러 object.

![Figure 2.7 — Persistent HTTP. 책 p.100](/courses/networking/figures/ch02/fig-2-7.png)

```
1. Client → Server: TCP handshake (1 RTT)
2. Client → Server: GET /index.html
3. Server → Client: response
4. (HTML 파싱 후) Client → Server: GET /logo.png  ← 같은 connection!
5. Server → Client: response
6. ... 더 많은 요청 ...
7. TCP close (idle timeout 후)
```

**With pipelining**:
- Client 가 *response 기다리지 않고* 다음 request 즉시 send
- *parallel* 요청 — even faster

HTTP/1.1 default — persistent + pipelining. 거의 모든 modern browser.

### 2.3 HTTP Message Format

#### Request

```
GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0 (Macintosh; ...) Chrome/120.0\r\n
Accept: text/html,application/xhtml+xml\r\n
Accept-Language: ko-KR,ko;q=0.9\r\n
Accept-Encoding: gzip, deflate, br\r\n
Cookie: session_id=abc123; user_pref=dark\r\n
Connection: keep-alive\r\n
\r\n
[body — POST/PUT 에 있음]
```

![Figure 2.8 — HTTP request message format. 책 p.101](/courses/networking/figures/ch02/fig-2-8.png)

#### Response

```
HTTP/1.1 200 OK\r\n
Date: Mon, 27 May 2026 10:00:00 GMT\r\n
Server: nginx/1.22.0\r\n
Content-Type: text/html; charset=utf-8\r\n
Content-Length: 1234\r\n
Last-Modified: Sun, 26 May 2026 12:00:00 GMT\r\n
ETag: "abc123-def456"\r\n
Cache-Control: max-age=3600\r\n
Set-Cookie: session_id=xyz789; HttpOnly; Secure\r\n
\r\n
<!DOCTYPE html>
<html>...
```

![Figure 2.9 — HTTP response message format. 책 p.103](/courses/networking/figures/ch02/fig-2-9.png)

#### Methods

| Method | 의도 | Idempotent | Cacheable |
|--|--|--|--|
| **GET** | resource 조회 | yes | yes |
| **HEAD** | header 만 (body 없이) | yes | yes |
| **POST** | resource 생성, action | no | only with explicit |
| **PUT** | resource 전체 replace | yes | no |
| **DELETE** | resource 삭제 | yes | no |
| **PATCH** | resource 부분 update | no | no |
| **OPTIONS** | server 지원 method | yes | no |

> *Idempotent* — 같은 request 를 *여러 번* 보내도 *결과 동일*. retry 안전.

#### Status Codes

| Range | 의미 | 대표 |
|--|--|--|
| 1xx | Informational | 100 Continue, 101 Switching Protocols |
| 2xx | Success | **200 OK**, 201 Created, 204 No Content |
| 3xx | Redirection | **301 Moved Permanently**, 302 Found, **304 Not Modified** |
| 4xx | Client error | **400 Bad Request**, 401 Unauthorized, **403 Forbidden**, **404 Not Found**, 429 Too Many Requests |
| 5xx | Server error | **500 Internal Server Error**, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

### 2.4 User-Server State: Cookies

> *HTTP is stateless*. But *web app needs login, cart, preferences*. → **cookie**.

![Figure 2.10 — Cookie 의 흐름. 책 p.106](/courses/networking/figures/ch02/fig-2-10.png)

4 단계:
1. Server 가 `Set-Cookie: id=abc123` header 반환
2. Browser 가 *cookie 저장*
3. 같은 server 의 *다음 request* 마다 `Cookie: id=abc123` 자동 첨부
4. Server 가 cookie 로 *user 식별*, back-end DB 조회

#### Cookie 의 사용처

- *Authentication* — login session
- *Shopping cart* — 비로그인 사용자의 장바구니
- *Preferences* — language, dark mode
- *Tracking* — analytics, advertising

#### Cookie 의 *flag*

```
Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Strict; Max-Age=86400
```

- **HttpOnly** — JS `document.cookie` 로 접근 못 함 (XSS 방어)
- **Secure** — HTTPS 만 전송
- **SameSite=Strict/Lax/None** — cross-site 요청 시 *전송 여부* (CSRF 방어)
- **Max-Age / Expires** — 만료

> **Cookie 의 윤리** — *3rd-party cookie* (광고용) 가 privacy 침해. Safari/Firefox 가 *block by default*. Chrome 의 *Privacy Sandbox* 가 대체 모색.

### 2.5 Web Caching

> **Web cache** (= **proxy server**) 가 *client 와 origin server 사이* 에서 자주 요청되는 resource 를 *캐시*.

![Figure 2.11 — Web cache (proxy server). 책 p.109](/courses/networking/figures/ch02/fig-2-11.png)

#### 동작

1. Client → cache: HTTP GET /index.html
2. Cache 가 *local 에 있나* 확인:
   - **HIT**: cache 의 copy 반환. *Fast*.
   - **MISS**: origin server → cache → client. 다음 요청부터 HIT.

#### 효과

- *Response time 단축* — origin RTT 보다 cache RTT 짧음 (특히 institutional cache)
- *Bandwidth 절약* — institutional → origin 의 *outbound traffic* 감소
- *Server load 분산* — origin 의 부담 ↓

#### Conditional GET — *staleness* 검증

cache 의 *옛 copy* 가 *유효한가* 확인:

```
[Cache → Origin]
GET /index.html HTTP/1.1
If-Modified-Since: Sun, 26 May 2026 12:00:00 GMT
```

Origin 응답:
- 변경 없음: `304 Not Modified` (body 없이) → cache 가 *옛 copy* 사용
- 변경: `200 OK` + 새 body → cache 가 *교체*

ETag (entity tag) 도 같은 역할 — opaque hash 비교.

### 2.6 HTTP/2 와 HTTP/3

#### HTTP/2 (RFC 7540, 2015)

문제 — HTTP/1.1 의 *head-of-line blocking*: pipelining 에서 *앞 response 가 늦으면* 뒤 모두 대기.

해결:
- **Binary framing** — text 가 아닌 *binary frame*
- **Multiplexing** — 한 TCP connection 안 *여러 stream* 병렬
- **Server push** — server 가 *요청 안 한 resource* 미리 push
- **Header compression** (HPACK) — 반복되는 header byte 절약

여전한 문제 — TCP layer 의 *head-of-line blocking*. 한 packet loss 가 *모든 stream* 의 진행 차단.

#### HTTP/3 (RFC 9114, 2022)

해결책 — *transport 자체 교체*:
- **QUIC over UDP** (3장) — UDP 위 *user-space transport*
- 각 QUIC stream 이 *독립* — 한 stream loss 가 *다른 stream 영향 X*
- **0-RTT** — TLS resumption 시 첫 byte 와 함께 application data

산업 채택:
- 2026 현재 Google, Cloudflare, Facebook, Akamai 가 *HTTP/3 default*
- Chrome/Firefox/Safari 모두 지원
- 약 30~50% 의 web traffic 이 HTTP/3 (CDN 통해)

### 2.7 CDN — Content Delivery Networks

![Figure 2.27 — CDN 의 architecture. 책 p.154](/courses/networking/figures/ch02/fig-2-27.png)

#### 동기

- *Geographic distance* → propagation delay
- *Single origin* → bandwidth bottleneck
- *Single point of failure*

#### 동작

CDN provider (Akamai, Cloudflare, Fastly, AWS CloudFront) 가:
1. 전 세계 *수백~수천 PoP* (Point of Presence) 운영
2. *Origin content* 를 PoP 에 *replicate*
3. *DNS-based routing* 으로 *사용자 가까운 PoP* 로 routing
4. *Anycast* — 같은 IP 가 *여러 PoP 에 announce*. BGP 가 가장 가까운 곳으로

#### CDN 의 이점

| 이점 | 의미 |
|--|--|
| Latency | 사용자 ↔ PoP 의 distance ↓ |
| Bandwidth | origin 의 부담 분산 |
| Availability | PoP 실패 시 다른 PoP fallback |
| DDoS mitigation | 대량 traffic 흡수 |
| TLS termination | 각 PoP 가 TLS 처리, origin 은 plain |

#### Industry stats

- *Netflix*: 95% 의 video traffic 이 *Open Connect* (자체 CDN) 의 ISP 안 server
- *Cloudflare*: 전 세계 internet traffic 의 ~20% 처리
- *Latency reduction*: 평균 ~50% (200ms → 100ms)

---

## 3. DNS — The Internet's Directory Service

### 3.1 Hostname ↔ IP Address

> *Human-readable name* (www.google.com) ↔ *machine address* (142.250.46.110).

이걸 *DNS* 가 처리.

#### DNS 의 추가 service

- *Hostname canonicalization* — `www.example.com` 와 `example.com` 의 별칭 처리
- *Mail server aliasing* — MX record
- *Load distribution* — 같은 name 의 *여러 IP*
- *Geo-routing* — region 별 다른 IP

### 3.2 Distributed, Hierarchical Database

> *Single central server* 는 *single point of failure* + *너무 먼 거리* + *부하* + *유지보수*.

→ **분산 + 계층** 설계.

![Figure 2.18 — DNS server 의 계층. 책 p.127](/courses/networking/figures/ch02/fig-2-18.png)

#### 3 tier 계층

**Root DNS servers** (13개 logical, 수백 physical):
- *Top of hierarchy*. 모든 TLD server 의 위치 보유
- IPv4 anycast 로 *전 세계 분산*
- `a.root-servers.net` ~ `m.root-servers.net`

**Top-Level Domain (TLD) servers**:
- `.com`, `.org`, `.net`, `.kr`, `.io` 등의 TLD
- Verisign 이 `.com`, `.net` 관리. PIR 이 `.org`. 국가는 ccTLD (`.kr`, `.jp` 등)

**Authoritative DNS servers**:
- 한 organization 의 *권위 record*
- `google.com` 의 authoritative server 는 *Google 이 운영*
- 작은 사이트는 *cloud DNS service* (AWS Route 53, Cloudflare DNS, Google Cloud DNS) 위탁

#### Local DNS server

- 사용자 host 의 *직접 query 상대*
- 보통 *ISP 또는 organization* 이 운영 (e.g., KT 의 `168.126.63.1`)
- Public resolver: Google `8.8.8.8`, Cloudflare `1.1.1.1`
- *Cache* 보유 — 자주 요청되는 name 의 결과 *짧은 TTL 동안* 저장

### 3.3 DNS Query — Iterative vs Recursive

![Figure 2.19 — Iterative + recursive query. 책 p.128](/courses/networking/figures/ch02/fig-2-19.png)

#### Iterative query

```
Host → Local DNS: "www.example.com IP?"
Local → Root: "www.example.com?"
Root → Local: "Don't know, ask .com TLD at IP X"
Local → .com TLD: "www.example.com?"
.com TLD → Local: "Don't know, ask example.com auth at IP Y"
Local → example.com auth: "www.example.com?"
example.com auth → Local: "It's 93.184.216.34"
Local → Host: "93.184.216.34"
```

*Local DNS* 가 *모든 query 의 hub*. 4 step.

#### Recursive query

```
Host → Local DNS: "www.example.com IP?"
Local → Root: "Get me the answer"
Root → .com TLD: "Get me the answer" (root 가 forward)
...
.com TLD → Local: "93.184.216.34"
Local → Host: "93.184.216.34"
```

*Root + TLD 까지 모두 forward*. 부하 ↑ → *root server 가 보통 recursive 거부*.

산업 패턴 — *host → local* 만 recursive, *local → root/TLD* 는 iterative.

### 3.4 DNS Caching

> 모든 *DNS server* 가 *cache* 보유 — 같은 query 의 *반복 비용 절약*.

#### TTL (Time-To-Live)

각 DNS record 가 *TTL* 명시 (예: `3600` = 1 시간):
- *Cache 가 그 시간 동안 record 보유*
- TTL 만료 후 *재query*

**Trade-off**:
- *짧은 TTL* (60초): record 변경 시 *빠른 propagation*. 그러나 *query 부하 ↑*
- *긴 TTL* (1일+): query 부하 ↓. 그러나 *변경 propagation 느림*

산업 — 보통 *5분 ~ 1시간*. *DNS-based load balancing* 의 *redirect* 는 짧은 TTL.

### 3.5 DNS Records — *5 가지 핵심 type*

| Type | 의미 | 예시 |
|--|--|--|
| **A** | hostname → IPv4 | `example.com → 93.184.216.34` |
| **AAAA** | hostname → IPv6 | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | hostname → 다른 hostname (alias) | `www.example.com → example.com` |
| **MX** | mail server for domain | `example.com → mx.example.com (priority 10)` |
| **NS** | authoritative DNS server | `example.com → ns1.example.com` |

추가 (현대):
- **TXT** — text data. SPF, DKIM, domain verification
- **SRV** — service location (port + hostname)
- **CAA** — *어떤 CA* 가 *cert 발급 가능* (보안)
- **PTR** — reverse (IP → hostname)

### 3.6 실용 DNS tool

```bash
# A record query
$ dig www.google.com
;; ANSWER SECTION:
www.google.com.   180   IN   A   142.250.46.4

# 특정 type
$ dig www.google.com AAAA
$ dig google.com MX
$ dig google.com NS

# Trace 전체 query path
$ dig +trace www.google.com

# 특정 nameserver 에 query
$ dig @8.8.8.8 www.google.com

# Reverse DNS
$ dig -x 142.250.46.4
```

### 3.7 DNS 의 취약성

#### DDoS

- 2016 Dyn DNS DDoS — Mirai botnet 으로 Dyn 의 *authoritative server* 공격
- → Twitter, Reddit, GitHub 등 *Dyn 사용 서비스* 마비
- 방어 — Anycast 분산, root server *13 logical/수백 physical*

#### Spoofing / Cache Poisoning

- Attacker 가 *DNS response 위조* → cache 에 잘못된 IP 저장
- 사용자가 *attacker server* 로 redirect
- 방어 — **DNSSEC** (Domain Name System Security Extensions) — *cryptographic signature*

#### Surveillance

- DNS query 가 *평문* (UDP 53) → ISP/정부 가 *모든 hostname* 관찰
- 방어 — **DoH** (DNS over HTTPS, RFC 8484), **DoT** (DNS over TLS, RFC 7858)
- Cloudflare, Quad9, Google 이 *public DoH resolver* 제공

---

## 4. Electronic Mail in the Internet

### 4.1 Email 의 3 가지 component

![Figure 2.14 — Email system 의 구조. 책 p.116](/courses/networking/figures/ch02/fig-2-14.png)

1. **User agents (MUA)** — Gmail web, Outlook, Apple Mail. *읽기/쓰기*
2. **Mail servers (MTA)** — *sender 와 recipient 의 mailbox*. SMTP 로 전송
3. **SMTP** — *mail server 끼리* + *MUA → MTA* 의 protocol

### 4.2 SMTP — Simple Mail Transfer Protocol

> RFC 5321 (2008, 옛 RFC 821 의 update).

#### 동작

```
Sender's MUA → Sender's mail server: SMTP submission (TCP 587, TLS)
Sender's mail server → Recipient's mail server: SMTP (TCP 25)
Recipient pulls from their mail server: IMAP / POP3
```

**ASCII text protocol** (역사적 결정):

```
S: 220 mx.example.com ESMTP ready
C: HELO sender.com
S: 250 mx.example.com Hello
C: MAIL FROM:<alice@sender.com>
S: 250 Sender OK
C: RCPT TO:<bob@example.com>
S: 250 Recipient OK
C: DATA
S: 354 Send message body
C: From: Alice <alice@sender.com>
C: To: Bob <bob@example.com>
C: Subject: Hello
C:
C: Hi Bob, ...
C: .
S: 250 Message accepted
C: QUIT
S: 221 Bye
```

→ 모든 byte 가 *human-readable*. 이게 *디버깅 + 학습 용이*.

### 4.3 IMAP vs POP3 — *mailbox 에서 가져오기*

| | **POP3** (Post Office Protocol v3) | **IMAP** (Internet Message Access Protocol) |
|--|--|--|
| RFC | RFC 1939 | RFC 9051 |
| 동작 | *Download + delete* (또는 keep) | *Server-side mailbox*, sync |
| Storage | local | server (cloud) |
| Multi-device | 어려움 | 자연스러움 |
| Folder | 없음 (Inbox 만) | *Server-side folder* |
| 사용 | 옛 desktop client | 현대 web/mobile |

산업 현실 — Gmail, Outlook 365 등은 *IMAP* 표준. POP3 는 *legacy*.

### 4.4 현대의 Email — *이메일 보안 의 진화*

#### SPF (Sender Policy Framework)

- TXT record 에 *허용된 sender IP* 명시
- recipient server 가 *sender IP* 가 SPF 일치하는지 확인

```
example.com.   IN   TXT   "v=spf1 include:_spf.google.com ~all"
```

#### DKIM (DomainKeys Identified Mail)

- Sender 가 *email header + body* 에 *cryptographic signature*
- recipient 가 *sender 의 public key* (DNS TXT) 로 검증

#### DMARC (Domain-based Message Authentication, Reporting & Conformance)

- SPF + DKIM 의 *결과를 어떻게 처리* 정책
- *quarantine / reject / allow*
- *report* 를 sender 에 전송 — sender 가 *forge 탐지*

이 3가지가 *현대 email 의 anti-phishing* 기반. *대형 도메인* (gmail.com, microsoft.com) 은 *전부 적용*.

---

## 5. Peer-to-Peer File Distribution — BitTorrent

### 5.1 P2P 의 *scalability* 우위

#### Client-server 의 distribution time

F = file size, $u_s$ = server upload rate, $d_{min}$ = 최소 client download rate, N = clients.

$$d_{c-s} = \max\left( \frac{NF}{u_s}, \frac{F}{d_{min}} \right)$$

- $u_s$ 가 *bottleneck* — N 명에게 *N 번* upload 해야
- $d_{min}$ 도 limit — 가장 느린 client

#### P2P 의 distribution time

각 peer 가 *동시에 upload*:

$$d_{p2p} = \max\left( \frac{F}{u_s}, \frac{F}{d_{min}}, \frac{NF}{u_s + \sum_i u_i} \right)$$

- 마지막 항 — *모든 upload 합* 으로 N copies 분배
- *peers 가 늘면 upload 도 늘어* — scalability 무한대

![Figure 2.24 — File distribution time: C-S vs P2P. 책 p.140](/courses/networking/figures/ch02/fig-2-24.png)

→ P2P 의 *self-scalability* 가 결정적. *수십만 사용자에게 영화 배포* 같은 케이스에 우월.

### 5.2 BitTorrent — *file sharing 의 표준*

> Bram Cohen, 2001. *P2P file distribution 의 dominant* protocol.

#### Torrent + Tracker

1. *Torrent file* (`.torrent`) — file 의 *metadata* + tracker URL
2. *Tracker* — 어떤 peer 가 어떤 *chunk* 보유하는지 추적 (현대는 *trackerless DHT* 도 사용)
3. *Swarm* — 같은 file 의 *peers 모임*

#### Chunk-based distribution

File 을 *256 KB chunk* 로 분할. 각 chunk 가 *독립* 으로 distribute.

#### Peer 선택 — *Rarest first*

> *얼마나 흔한가* 기준 — *가장 드문 chunk* 먼저 download.

이유:
- 흔한 chunk 는 *나중에도 쉽게* 받을 수 있음
- 드문 chunk 가 *swarm 에서 사라지면* 영원히 못 받음
- *Rarity 우선* 으로 *전체 swarm 의 distribution 균형*

### 5.3 Tit-for-tat — *Incentive*

> "*나에게 upload 해 주는 peer 에게* 더 빨리 upload".

**문제** — *Free rider* (다운만 받고 upload 안 함) 가 시스템 망침.

**해결** — *상호 호혜*:
- A 가 B 에게 upload → B 가 A 에게 *우선* upload
- *Top 4 upload 한 peer* 에게만 우선 (= unchoking)
- *Random optimistic unchoking* — 1명의 random peer 도 우선 (새 peer 가 시작할 기회)

→ *free rider 가 자연스럽게 도태*. P2P 의 *분산 fairness*.

### 5.4 산업의 P2P 응용

- *BitTorrent* — 여전히 유효 (Linux ISO, large data set, archive)
- *IPFS* — Interplanetary File System, *content-addressed* (hash-based)
- *Blockchain* — Bitcoin, Ethereum 의 *peer-to-peer ledger*
- *WebRTC* — browser 간 P2P (video call, file transfer)
- *Cassandra, DynamoDB 의 gossip protocol* — 5장 의 P2P

---

## 6. Video Streaming and CDNs

### 6.1 DASH — Dynamic Adaptive Streaming over HTTP

> *HTTP 위의* video streaming. Netflix, YouTube, Twitch 의 표준.

![Figure 2.25 — DASH 의 동작. 책 p.147](/courses/networking/figures/ch02/fig-2-25.png)

#### 동작

1. Video 를 *수 초 chunk* (보통 2~10초) 로 분할
2. 각 chunk 를 *여러 quality level* 로 encoding (예: 240p, 480p, 720p, 1080p, 4K)
3. **MPD** (Media Presentation Description) — chunk 들의 *URL + metadata*
4. Client 가 *MPD 다운로드* 후, *현재 throughput* 측정하며 *적절한 quality* 선택

#### Adaptive Bitrate (ABR)

Client-side algorithm:

```python
# 매 chunk 다운로드 후
estimated_bandwidth = chunk_size / download_time
buffer_level = current_buffer_seconds

if buffer_level < THRESHOLD_LOW:
    target_quality = LOWEST  # 끊김 회피
elif buffer_level > THRESHOLD_HIGH and estimated_bandwidth > current_quality_bitrate * 1.5:
    target_quality = NEXT_HIGHER  # 여유 있으면 화질 ↑
else:
    target_quality = CURRENT
```

trade-off:
- *Buffer 가 작으면* → 끊김 (rebuffering) 위험. quality 낮게.
- *Buffer 큼* + *bandwidth 충분* → quality ↑

#### 산업 algorithm

- *Throughput-based* — 단순 bandwidth 측정
- *Buffer-based* — buffer level 만 보고 결정 (Netflix)
- *MPC* (Model Predictive Control) — 미래 N step 예측 후 최적화 (학계)
- *Pensieve* (MIT) — *neural network* 학습한 ABR

### 6.2 CDN 의 video distribution

#### 산업 솔루션

**Netflix Open Connect**:
- *ISP 의 datacenter 안* 에 Netflix 의 server
- ISP 가 *서버 호스팅 무료* + *peering 직접*
- → Netflix traffic 의 95%+ 가 *local*

**YouTube + Google Edge Network**:
- *Google Cloud Network* — tier-1 보다 큰 자체 backbone
- 수만 *edge node* (Google Global Cache)

**Twitch + AWS CloudFront**:
- AWS CloudFront 가 *real-time low-latency*
- *Sub-second* streaming for live

#### 부하 처리

- 큰 event (Super Bowl, K-pop comeback) 시 *수억 동시 시청*
- *Total bitrate* = 동시시청자 × 평균 4 Mbps = *수 Tbps*
- CDN 의 *distributed capacity* 만이 가능

---

## 7. Socket Programming — *직접 만들어 보기*

### 7.1 TCP Socket — Python 예제

#### Server

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 12000))    # 모든 interface, port 12000
server_socket.listen(1)             # backlog 1

print("Server listening on port 12000...")
while True:
    client_sock, addr = server_socket.accept()  # 새 connection 대기
    print(f"Connected from {addr}")
    
    sentence = client_sock.recv(1024).decode()  # 받기
    response = sentence.upper()
    
    client_sock.send(response.encode())         # 보내기
    client_sock.close()
```

#### Client

```python
import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('localhost', 12000))      # server 연결

sentence = input("Input lowercase sentence: ")
client_sock.send(sentence.encode())

modified = client_sock.recv(1024).decode()
print(f"From server: {modified}")

client_sock.close()
```

**동작**:
1. Server 가 *listen socket* 생성, `accept()` 에서 대기
2. Client 가 `connect()` — 3-way handshake
3. Client 가 `send()`, server 가 `recv()`
4. Server 가 `send()`, client 가 `recv()`
5. `close()` — 4-way handshake (TCP FIN)

### 7.2 UDP Socket — Python 예제

#### Server

```python
import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('', 12000))

while True:
    msg, addr = server_sock.recvfrom(1024)     # 받기 (sender 주소 반환)
    response = msg.decode().upper()
    server_sock.sendto(response.encode(), addr) # 답장 (주소 명시)
```

#### Client

```python
import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sentence = input("Input lowercase sentence: ")

client_sock.sendto(sentence.encode(), ('localhost', 12000))
msg, _ = client_sock.recvfrom(1024)
print(f"From server: {msg.decode()}")
client_sock.close()
```

#### TCP vs UDP socket 의 차이

| | TCP (SOCK_STREAM) | UDP (SOCK_DGRAM) |
|--|--|--|
| Connection | `listen + accept + connect` 필요 | 없음 |
| Send/recv | `send/recv` (byte stream) | `sendto/recvfrom` (per-datagram) |
| Reliability | 자동 retransmission | application 처리 |
| Order | 자동 정렬 | 임의 순서 |
| Address per message | connection 한 번 | 매 datagram 명시 |

### 7.3 산업 socket API — 더 복잡한 경우

- *Non-blocking + epoll/kqueue* — 한 thread 가 *수천 connection* 처리 (`nginx`, `Node.js`)
- *Thread/process pool* — connection 별 동시 처리
- *Async I/O* — Python `asyncio`, Go goroutines
- *Higher-level frameworks* — Flask, FastAPI, gRPC, WebSocket

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | "UDP > TCP latency" 항상 | TCP setup 은 1 RTT (HTTP/2) 또는 0 RTT (HTTP/3). UDP 의 *no congestion control* 이 부하 시 unfair |
| 2 | HTTP 가 *stateful* | stateless. cookie 가 stateless 위 *위장* |
| 3 | HTTP/1.1 의 *one TCP per object* | 그건 HTTP/1.0. HTTP/1.1 default 는 persistent + pipelining |
| 4 | DNS 가 *single server* | 분산 + 계층 + cache. *13 root logical, 수백 physical* |
| 5 | DNS query 가 *iterative 만* 또는 *recursive 만* | host→local 은 recursive, local→root/TLD 는 iterative. 산업 표준 |
| 6 | Cookie 가 *완전 safe* | XSS, CSRF, 3rd-party tracking. HttpOnly + Secure + SameSite 필수 |
| 7 | P2P 가 *모든 distribution 우월* | NAT/firewall, churn, security 의 trade-off. Hybrid 가 산업 표준 |
| 8 | BitTorrent 가 *불법 전용* | OSS distribution (Linux ISO), large data archive 등 합법 사용 광범위 |
| 9 | Video streaming 이 *RTP 같은 streaming protocol* | 현대는 *HTTP 기반 DASH* — port 80/443 만 사용 → firewall 통과 쉬움 |
| 10 | Socket 의 *one accept = one client* | listen socket 은 *재사용*. accept 가 *새 socket* 반환 |
| 11 | HTTP/2 가 *모든 문제 해결* | TCP head-of-line blocking 여전. HTTP/3 (QUIC) 이 진정 해결 |
| 12 | CDN 의 *caching 만 valuable* | TLS termination, DDoS mitigation, image optimization, WAF 등 다층 가치 |

---

## 자가점검

1. *Client-server* vs *P2P* 의 *3 가지 차이*.
2. *Transport service* 의 4 가지 요구 (reliable, throughput, timing, security).
3. *Socket* 의 비유 (door, mailbox) + *addressing* 의 두 단계.
4. *HTTP non-persistent* 의 RTT 식 + persistent + pipelining 의 개선.
5. HTTP method 의 *idempotent + cacheable* 표.
6. *Cookie* 의 4 가지 flag (HttpOnly, Secure, SameSite, Max-Age).
7. *Web cache* 의 *conditional GET* 동작.
8. HTTP/2 의 *4 가지 개선* + HTTP/3 의 *근본 변화*.
9. *DNS* 의 *3-tier hierarchy* + *iterative vs recursive* query.
10. *5 가지 DNS record type* (A, AAAA, CNAME, MX, NS).
11. *SMTP, IMAP, POP3* 의 역할 분담.
12. *SPF, DKIM, DMARC* — 현대 email 의 anti-phishing 3종.
13. *BitTorrent* 의 *rarest first* + *tit-for-tat*.
14. *DASH* 의 *adaptive bitrate* 결정 logic.
15. *TCP socket* vs *UDP socket* 의 API 차이.

### 해답 (간략)

1. C-S: server always-on/fixed-IP/asymmetric. P2P: peers 직접/self-scalable/churn. Hybrid: 둘 다.
2. Reliable data (file/email), Throughput (audio bw 보장), Timing (interactive <100ms), Security (TLS).
3. Door — application 이 socket 으로 network 접근. Mailbox — incoming message 보관. Addressing — host IP + process port.
4. Non-persistent: 2 RTT/object (TCP handshake + request). Persistent: 1 connection, 1 RTT/object. Pipelining: parallel request.
5. GET/HEAD/PUT/DELETE/OPTIONS = idempotent. GET/HEAD = cacheable. POST/PATCH = neither idempotent nor cacheable by default.
6. HttpOnly (JS 접근 차단), Secure (HTTPS only), SameSite (cross-site 통제), Max-Age (만료).
7. Cache 의 `If-Modified-Since` header → origin 이 304 Not Modified (변경 없음) 또는 200 + new body (변경).
8. HTTP/2: binary framing, multiplexing, server push, header compression. HTTP/3: QUIC over UDP (transport 교체) — TCP head-of-line blocking 제거.
9. Root → TLD → Authoritative. Iterative: host→local 외 모두 step-by-step. Recursive: forward all the way.
10. A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (auth server).
11. SMTP: mail server 끼리 + MUA→MTA 송신 (push). IMAP/POP: MUA 가 MTA 에서 수신 (pull).
12. SPF: 허용 sender IP, DKIM: sender 의 cryptographic signature, DMARC: 정책 + report.
13. Rarest first: swarm 안 *드문 chunk* 우선 download. Tit-for-tat: *upload 해주는 peer* 우선 upload, free rider 도태.
14. Buffer level + estimated bandwidth → quality 결정. low buffer = 낮은 quality, high bandwidth + buffer = 높은 quality.
15. TCP: stream-based, listen+accept+connect, send/recv. UDP: datagram-based, no connection, sendto/recvfrom (주소 매번).

---

## 다음 학습으로

- **3장 (Transport Layer)** — TCP 의 reliable data transfer, congestion control, UDP. *Mathis equation* 의 수학적 derivation.
- **4-5장 (Network Layer)** — IP routing, BGP, *DNS query path 의 underlying routing*.
- **8장 (Security)** — TLS handshake 의 세부, DNSSEC, DKIM 의 cryptography.

> *Tools to try*:
> - `curl -v https://example.com/` — HTTP request 의 *모든 byte* 보기
> - `dig +trace example.com` — DNS query 의 *각 단계* 추적
> - `wireshark` — local network 의 HTTP/DNS packet 캡처
> - `nc -v example.com 80` 후 `GET / HTTP/1.1` 직접 입력 — *raw HTTP* 체험
> - Python `socket` 으로 *간단한 echo server* 구현
