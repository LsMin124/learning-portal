# Ch 2 Application Layer — 치트시트

## TL;DR

- **Client-Server** (대부분) vs **P2P** (BitTorrent). 산업은 *hybrid*
- **Transport 4 요구**: reliable / throughput / timing / security
- **HTTP**: stateless. HTTP/1.1 persistent → HTTP/2 multiplex → HTTP/3 QUIC
- **Cookie**: stateless 위 *state*. HttpOnly + Secure + SameSite 필수
- **DNS**: 3-tier (Root → TLD → Authoritative) + caching + TTL
- **SMTP** (push) + **IMAP/POP** (pull). SPF/DKIM/DMARC 가 anti-phishing
- **BitTorrent**: rarest first + tit-for-tat. P2P 의 *self-scalability*
- **DASH**: HTTP 위 video streaming + adaptive bitrate
- **CDN**: geographic PoP + cache hit ratio + DDoS mitigation

---

## Quick Reference

### 표 1. Application architecture

| | C-S | P2P | Hybrid |
|--|--|--|--|
| Source | server | peers | both |
| Scale | linear (server bw) | self-scaling | best of both |
| 예시 | Web, email | BitTorrent | Skype, WhatsApp |

### 표 2. Transport service 요구

| App | Reliable | Throughput | Timing | Sec |
|--|--|--|--|--|
| File transfer | ✓ | elastic | tolerant | TLS |
| Email | ✓ | elastic | tolerant | TLS |
| Web | ✓ | elastic | < 1s | TLS |
| Streaming | partial | high | tolerant | TLS |
| VoIP/Game | partial | small | **< 100ms** | basic |
| DNS | no | n/a | < 100ms | DoH |

### 표 3. HTTP version 비교

| | HTTP/1.0 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|--|--|--|--|--|
| Connection | non-persistent | persistent + pipelining | multiplexed | QUIC over UDP |
| Format | text | text | **binary** | binary |
| Head-of-line | yes | yes (TCP-level) | TCP-level still | **resolved** |
| 0-RTT | no | no | no | yes (resumption) |
| Year | 1996 | 1997 | 2015 | 2022 |

### 표 4. HTTP methods

| Method | Idempotent | Cacheable |
|--|--|--|
| GET | ✓ | ✓ |
| HEAD | ✓ | ✓ |
| POST | ✗ | conditional |
| PUT | ✓ | ✗ |
| DELETE | ✓ | ✗ |
| PATCH | ✗ | ✗ |
| OPTIONS | ✓ | ✗ |

### 표 5. Status code 범위

| Range | 의미 | 대표 |
|--|--|--|
| 1xx | Informational | 100, 101 |
| 2xx | Success | 200, 201, 204 |
| 3xx | Redirection | 301, 302, 304 |
| 4xx | Client error | 400, 401, 403, 404, 429 |
| 5xx | Server error | 500, 502, 503, 504 |

### 표 6. Cookie flags

| Flag | 보호 |
|--|--|
| HttpOnly | JS 접근 차단 (XSS) |
| Secure | HTTPS 만 |
| SameSite=Strict/Lax | CSRF |
| Max-Age / Expires | 만료 |

### 표 7. DNS record types

| Type | 의미 |
|--|--|
| A | hostname → IPv4 |
| AAAA | hostname → IPv6 |
| CNAME | alias |
| MX | mail server |
| NS | auth nameserver |
| TXT | SPF, DKIM, verification |
| CAA | cert authority 허가 |

### 표 8. DNS query 흐름

```
Host → Local DNS (recursive)
Local → Root (iterative) — "ask .com TLD at X"
Local → TLD (iterative) — "ask example.com auth at Y"
Local → Auth (iterative) — "answer is 1.2.3.4"
Local → Host: "1.2.3.4"

Cache hit ratio 가 핵심. TTL 따라 cache.
```

### 표 9. Email protocols

| Protocol | 방향 | Port |
|--|--|--|
| SMTP submission | MUA → MTA (send) | 587 (TLS), 25 (legacy) |
| SMTP relay | MTA → MTA | 25 (STARTTLS) |
| IMAP | MUA ← MTA (sync) | 993 (TLS) |
| POP3 | MUA ← MTA (download) | 995 (TLS) |

Anti-phishing 3종:
- **SPF**: 허용 sender IP (TXT)
- **DKIM**: cryptographic signature
- **DMARC**: 정책 + report

### 표 10. BitTorrent 핵심

| 개념 | 의미 |
|--|--|
| Torrent file | metadata + tracker URL |
| Tracker | peer discovery (현대는 DHT) |
| Swarm | 같은 file 의 peers |
| Chunk | file 의 256KB 조각 |
| Rarest first | 드문 chunk 우선 download |
| Tit-for-tat | upload 해주는 peer 우선 |
| Optimistic unchoke | random 1 명에게 기회 |

### 표 11. CDN flow

```
User → DNS query → CDN routing → nearest PoP
                                    ↓
                                 cache hit? 
                                ┌──┴──┐
                              yes      no
                              ↓        ↓
                           response  origin → cache → response
                              
효율: hit ratio 90%+ 산업 표준
```

### 표 12. Socket API

| | TCP (SOCK_STREAM) | UDP (SOCK_DGRAM) |
|--|--|--|
| Server | listen + accept | bind only |
| Client | connect | sendto |
| Send | send | sendto (addr 매번) |
| Recv | recv | recvfrom (addr 반환) |
| Order | stream, ordered | datagram, unordered |
| Reliability | 자동 | app 책임 |

---

## Mind Map

```
2장 Application Layer
├─ 1. Principles
│   ├─ C-S vs P2P vs hybrid
│   ├─ Process communication (socket)
│   └─ Transport requirements (4)
├─ 2. Web + HTTP
│   ├─ Stateless protocol
│   ├─ Persistent + pipelining
│   ├─ Methods + status codes
│   ├─ Cookie (state)
│   ├─ Web cache + conditional GET
│   ├─ HTTP/2 multiplex, HTTP/3 QUIC
│   └─ CDN (proximity + cache)
├─ 3. DNS
│   ├─ 3-tier (root/TLD/auth)
│   ├─ Iterative vs recursive
│   ├─ Caching + TTL
│   ├─ Record types (A/AAAA/CNAME/MX/NS/TXT)
│   └─ Security (DDoS/spoofing/surveillance)
├─ 4. Email
│   ├─ SMTP (push)
│   ├─ IMAP/POP (pull)
│   └─ SPF/DKIM/DMARC (anti-phishing)
├─ 5. P2P (BitTorrent)
│   ├─ Self-scalability
│   ├─ Rarest first
│   └─ Tit-for-tat (anti-freerider)
├─ 6. Streaming (DASH + CDN)
│   ├─ Adaptive bitrate
│   └─ Buffer-based ABR
└─ 7. Socket programming
    ├─ TCP socket (Python)
    └─ UDP socket (Python)
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | C-S vs P2P. Transport 4 요구. TCP=reliable, UDP=fast |
| 2 | HTTP stateless. Persistent + multiplexing. CDN 의 가치 |
| 3 | DNS 3-tier 분산. caching + TTL. DoH 의 privacy |
| 4 | SMTP push + IMAP pull. SPF/DKIM/DMARC anti-phishing |
| 5 | BitTorrent 의 rarest-first + tit-for-tat. P2P scaling |
| 6 | DASH ABR. CDN 의 video distribution |
| 7 | Socket = door. TCP stream vs UDP datagram |
