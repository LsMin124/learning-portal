# Ch 2 Application Layer — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. Client-Server vs P2P 의 *근본 차이*

각 architecture 가 *왜 다른 scaling 특성* 을 갖나.

<details><summary>답</summary>

**Client-Server**:
- Server 가 *유일한 source*. N 사용자 → server upload bandwidth 의 *N 배* 부하
- *Vertical scaling* (server farm) 또는 *CDN* 으로 분산

**P2P**:
- 각 peer 가 *동시에 source + sink*. 새 peer 가 *capacity 도 추가*
- *Self-scaling* — N 사용자가 N 추가 upload capacity 가짐

**수학적 차이**:
- C-S distribution time: $\max(NF/u_s, F/d_{min})$ — N 에 linear
- P2P: $\max(F/u_s, F/d_{min}, NF/(u_s + \sum u_i))$ — N 에 sub-linear

→ 대규모 file 배포는 P2P 압도. *real-time + login + 보안* 은 C-S 우월. 산업은 hybrid.

</details>

### Q2. Transport service 4 요구 — Application 분류

다음 application 의 *4 요구* (reliable, throughput, timing, security) 평가:

1. 화상회의 (Zoom)
2. Online banking
3. Online RPG (League of Legends)
4. Cloud file backup (Dropbox)

<details><summary>답</summary>

| App | Reliable | Throughput | Timing | Security |
|--|--|--|--|--|
| Zoom | partial (concealment OK) | 2~4 Mbps | **< 150ms** | **TLS + SRTP** |
| Banking | **strict** | small | < 1s | **strict TLS + 2FA** |
| LoL | partial | small | **< 50ms** | basic |
| Dropbox | **strict** | bw 만큼 | tolerant | TLS + at-rest |

산업 — *서비스마다 protocol 다르게*. *one-size-fits-all 없음*.

</details>

### Q3. HTTP 1.0 vs 1.1 의 RTT 계산

10 object (각 100 KB), RTT 50ms, link 10 Mbps.

<details><summary>답</summary>

**Per object transmission**: $100KB \times 8 / 10Mbps = 80$ ms.

**(a) HTTP/1.0 — non-persistent**:
- Per object: TCP handshake (50) + req (50) + trans (80) = **180 ms**
- 10 sequential: **1800 ms**

**(b) HTTP/1.1 — persistent + pipelining**:
- TCP handshake 50ms 한 번
- All requests *one RTT* (50ms)
- 10 transmissions back-to-back: 800ms
- Total: **900 ms**

→ **2x 빨라짐**. HTTP/2 multiplexing 은 더.

</details>

### Q4. DNS query latency

첫 query, cache miss. RTT: host↔local 10ms, local↔root 100ms, local↔TLD 50ms, local↔auth 30ms.

<details><summary>답</summary>

**Iterative**:
- Host→Local 10 + Local→Root→Local 200 + Local→TLD→Local 100 + Local→Auth→Local 60 + Local→Host 10
- Total = **380 ms**

이제 HTTP request 시작 — 추가 ~100ms (TCP) + ~100ms (req) → *전체 580ms* 후 first byte.

**Subsequent (cache hit)**: 10ms only.

→ DNS *caching 가치 절대적*.

</details>

### Q5. Cookie 보안 함정

다음의 문제 + 수정.
```
Set-Cookie: session_id=abc123; Path=/
```

<details><summary>답</summary>

**문제**:
1. **HttpOnly 없음** — JS 로 읽기 → XSS 시 session 탈취
2. **Secure 없음** — HTTP 평문 전송. cafe WiFi 도청 가능
3. **SameSite 없음** — CSRF 취약
4. **Max-Age 없음** — session cookie (browser 닫으면 사라짐)

**수정**:
```
Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=86400
```

추가: token rotation, CSP, server-side session 권장.

</details>

### Q6. CDN 효율 — Cache hit ratio

1M req/day, 100KB per object, hit ratio 95%. Origin offload + bandwidth 절약?

<details><summary>답</summary>

- Origin requests = 5% × 1M = **50k/day**
- Origin offloaded = 950k requests
- Bandwidth saved = 950k × 100KB = **95 GB/day**
- $10/TB egress 면 ~$1k/month 절약

**Hit ratio 산업 기준**:
- Static-only: 95%+
- Mixed (e-commerce): 60~70%
- Dynamic-heavy: 20~30%

**개선**: 정확한 Cache-Control, smart routing, edge logic (Cloudflare Workers).

</details>

### Q7. SMTP 흐름 — Alice → Bob

`alice@example.com` → `bob@gmail.com` 의 *전체 flow*.

<details><summary>답</summary>

```
[1] Alice MUA → example.com outgoing (TCP 587 + TLS)
[2] outgoing 의 DNS MX query → gmail-smtp-in.l.google.com
[3] outgoing → Google MTA (TCP 25 + STARTTLS)
[4] Google: SPF/DKIM/DMARC check, spam filter
[5] Bob mailbox at Google
[6] Bob MUA ← IMAP/HTTPS pull
```

**SMTP submission** (587): authenticated.
**SMTP relay** (25): no auth, *SPF/DKIM 으로 위장 방지*.

현대 강화: MTA-STS (DNS 로 TLS 강제), DKIM signing, DMARC reject.

</details>

### Q8. BitTorrent unchoking

5 peer 의 upload to me: B=100KB/s, C=50, D=20, E=0 (free rider).

<details><summary>답</summary>

**Algorithm**:
1. Sort by upload to me (desc): B, C, D, E
2. Top K (=4) unchoke: B, C, D, E
3. + 1 random optimistic (rotation 30s)

**큰 swarm** (10+):
- Top 4 만 unchoke
- 나머지는 choked (no upload)
- Optimistic 1 명에게 random 기회

**Tit-for-tat 의 결과**:
- E (free rider) → upload 안 함 → A 도 E choke
- B (best uploader) ↔ A 상호 우선 upload (fastest)
- Random optimistic → 새 peer F 에게 시작 기회

경제학적 — *repeated game* 의 *cooperation > defection*.

</details>

### Q9. 디버그 — Page 가 *천천히* 로드

다른 사용자보다 5초 느림. 진단.

<details><summary>답</summary>

**Chrome DevTools Network tab**:

| Metric | 의심 |
|--|--|
| DNS lookup > 100ms | ISP DNS 느림. 1.1.1.1 사용 |
| Initial Connection > 100ms | server 멀거나 부하. CDN 사용 |
| SSL > 100ms | TLS 1.3, session resumption |
| TTFB > 500ms | server 처리 느림. caching, DB index |
| Content Download 느림 | 큰 파일. WebP, compression |

**기타**:
- Render-blocking CSS/JS → `async`, `defer`
- Third-party scripts (analytics, ads) → block or lazy
- HTTP/1.1 → HTTP/2 또는 HTTP/3
- Cache headers 정확히

**Tools**: WebPageTest, Lighthouse, Chrome DevTools.

</details>

### Q10. 디버그 — DNS 갱신 안 됨

IP 변경 후 일부 사용자만 새 IP 봄. 원인 + 대응.

<details><summary>답</summary>

**원인 — DNS caching**:
- ISP recursive resolver 의 *TTL 동안* 옛 IP 반환
- Browser cache (수 분~1시간)
- OS cache

**즉시 대응**:
- 사용자: `ipconfig /flushdns` (Win), `sudo killall -HUP mDNSResponder` (Mac)
- 변경 *24h 전* TTL 60초로 단축

**영구 회피**:
- DNS LB (Route 53, Cloudflare LB) — 짧은 TTL
- Anycast IP — IP 안 바꾸고 backend 만
- Reverse proxy — public IP 고정, internal 만 변경

산업 — DNS 변경은 *최후 수단*. abstraction layer (LB, proxy, anycast) 위에서.

</details>

### Q11. 면접 — *Why HTTPS by default?*

"Performance 영향 있는데 왜 모두 HTTPS?"

<details><summary>답</summary>

**현대 = performance 영향 거의 없음**:
- TLS 1.3: 1 RTT, 0-RTT for resumption
- AES-NI hardware accel — CPU < 1%
- HTTP/2 + HTTPS > HTTP/1.1 plaintext

**필수 이유**:
1. **Confidentiality** — 평문 traffic 도청 가능 (cafe WiFi, ISP, gov)
2. **Integrity** — middleman 의 content 수정 (광고, malware injection)
3. **Authentication** — DNS spoofing, MITM 방어
4. **Regulatory** — GDPR, PCI-DSS, HIPAA
5. **SEO** — Google 우선
6. **Modern features** — HTTP/2/3, Service Workers, Push 가 *HTTPS 필수*

**비용**: 무료 (Let's Encrypt + certbot, 5분 setup).

답 핵심 — "Performance 우려는 *옛 frame*. 현대 HTTPS 가 plaintext 보다 빠름. *비용 ~0*."

</details>

### Q12. 면접 — *DoH 의 trade-off*

"DNS over HTTPS 가 privacy 좋다는데 단점은?"

<details><summary>답</summary>

**이점**: ISP 도청 방지, spoofing 방지, port 443 (firewall 우회)

**단점/논쟁**:

1. **Centralization** — Cloudflare 1.1.1.1, Google 8.8.8.8 에 *전 세계 query* 집중
2. **Enterprise 제어 약화** — DNS-based filtering, threat detection 불가
3. **Parental control** — 가정 DNS filter 우회
4. **Performance overhead** — HTTPS handshake (caching 으로 완화)
5. **Malware C2 도청 어려움** — 새 attack surface

**산업**:
- Firefox: default DoH
- Chrome: opt-in
- Apple: Encrypted DNS
- 일부 국가 법적 차단

**미래** — ECH (Encrypted Client Hello) — SNI 도 암호화 → fully encrypted browsing.

답 핵심 — "DoH 의 privacy 가치는 명백. 그러나 enterprise/parental control 약화. *trade-off 분명*. *완벽한 답 없음*."

</details>
