# Ch 3 Transport Layer — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. UDP vs TCP — Application 별 선택

다음 4 app 에 *적절한 transport* + 이유.

<details><summary>답</summary>

| App | Transport | 이유 |
|--|--|--|
| DNS query | **UDP** | Small message, app 의 retry, handshake 비용 회피 |
| VoIP / Zoom audio | **UDP** (RTP) | Loss > delay (concealment OK, retransmit 늦음) |
| File download | **TCP** | Reliable, ordered. Throughput 만 중요 |
| Online MMO (LoL) | **UDP + custom** | Low latency 우선, state delta 의 loss tolerable |

**결정 규칙**:
1. *한 byte 손실 OK?* → UDP
2. *< 100ms 필수?* → UDP
3. *Small message + app 의 retry?* → UDP
4. 그 외 → TCP

산업 trend — QUIC 가 *UDP 위 reliable* — TCP 대안.

</details>

### Q2. Multiplexing 의 *근본 차이* — TCP vs UDP

Web server (port 80) 가 동시 100 client. UDP DNS server (port 53) 가 100 query. socket 구조 + 처리 방식 차이.

<details><summary>답</summary>

**TCP web server**:
- *(client IP, client port, 80, server IP)* 4-tuple → *별도 socket*
- 100 client = **100 socket**
- *Connection 별 독립* state

**UDP DNS server**:
- *(53, server IP)* 2-tuple → *단일 socket*
- 100 query 가 *같은 socket queue* 로
- Server: read → process → response (sender 주소 별도 추출)

**왜 다른가**:
- TCP: connection-oriented → state per connection
- UDP: stateless → single socket

**산업 시사**:
- TCP server: epoll/async 로 N socket 관리
- UDP server: 단순 read-loop. Client tracking 은 *app 책임*

</details>

### Q3. Stop-and-wait utilization 계산

10 Gbps link, 50 ms RTT, 1500 byte packet. Stop-and-wait utilization?

<details><summary>답</summary>

$d_{trans} = 1500 \times 8 / 10^{10} = 1.2 \text{ μs}$

$$U = \frac{d_{trans}}{RTT + d_{trans}} = \frac{1.2 \text{ μs}}{50 \text{ ms} + 1.2 \text{ μs}} \approx 0.000024 = 0.0024\%$$

10 Gbps link 의 *0.0024%* — 거의 활용 불가.

**Pipelined (window N)**:
$U \approx N \cdot d_{trans} / RTT$ (RTT ≫ $d_{trans}$)

링크 활용하려면 $N \cdot 1.2 \text{ μs} \geq 50 \text{ ms}$ → $N \geq 41,667$ packets in-flight.

이게 **BDP** = $10^{10} \times 0.05 = 5 \times 10^8$ bit = **62.5 MB**.

→ TCP window 가 *62.5 MB+* 여야 link 활용. Default 64 KB 는 *1000x 부족*. *Window scaling option* 필수.

</details>

### Q4. TCP 3-way handshake + first data — Sequence number 추적

다음의 정확한 seq + ack:
- Client SYN, seq=1000
- Server SYN-ACK, seq=5000
- Client ACK + data "Hello" (5 bytes)
- Server response "Hi" (2 bytes)
- Client final ACK

<details><summary>답</summary>

```
1. C → S: SYN, seq=1000             (no data, SYN consume 1)
2. S → C: SYN-ACK, seq=5000, ack=1001
3. C → S: ACK, seq=1001, ack=5001, data="Hello"
   (byte 1001..1005 = "Hello")
4. S → C: ACK, seq=5001, ack=1006, data="Hi"
   (received through 1005, next expected 1006)
5. C → S: ACK, seq=1006, ack=5003
   (received 5001..5002)
```

**주의**:
- *SYN 도 seq 1 consume* → 처음 ack = seq + 1
- 그 후 *data byte 수* 만큼 seq 증가
- *Initial seq number = random* (보안 — TCP hijacking 방어)
- *Wrap-around* — 2^32 ≈ 4 GB 이후 회전. *PAWS* option 으로 보호

</details>

### Q5. EWMA RTT estimation

EstimatedRTT = 100 ms, DevRTT = 20 ms. 새 sample 130 ms. 새 EstimatedRTT + Timeout?

<details><summary>답</summary>

$$EstimatedRTT_{new} = 0.875 \times 100 + 0.125 \times 130 = 87.5 + 16.25 = 103.75 \text{ ms}$$

$$DevRTT_{new} = 0.75 \times 20 + 0.25 \times |130 - 100| = 15 + 7.5 = 22.5 \text{ ms}$$

$$Timeout = EstimatedRTT + 4 \times DevRTT = 103.75 + 90 = 193.75 \text{ ms}$$

**시사**:
- EstimatedRTT 가 *smooth* — outlier 하나의 영향 작음
- DevRTT 가 *jitter* 측정 — variance 큰 link 에 *큰 timeout margin*
- 4 × DevRTT 는 *false retransmission* 회피 — *Karn-Partridge* 의 표준
- Karn 의 추가 규칙: *retransmitted segment 의 RTT* 는 *EstimatedRTT 계산에 미사용*

</details>

### Q6. AIMD sawtooth cycle — bytes per cycle

steady-state TCP. 한 cycle 에 *cwnd* 가 32 KB → 64 KB → 32 KB. MSS = 1500 byte. Cycle 의 *bytes transferred*?

<details><summary>답</summary>

**Cycle 구성**:
- cwnd = 32 KB (직전 loss 후 ssthresh/2 에서 시작)
- *Linear ↑* — 1 MSS per RTT
- cwnd = 64 KB 에서 *loss* → halve → 다시 32 KB

**RTT 수** = (64 - 32) / 1.5 KB ≈ *21 RTT*

**Average cwnd** = (32 + 64) / 2 = **48 KB**

**Cycle bytes** = 21 × 48 KB ≈ **1 MB**

**Mathis equation** 검증:
$$T \approx \frac{MSS}{RTT \sqrt{p}}$$

p (loss prob) = 1 / 1 MB ≈ $10^{-6}$ → $T \approx 1.5 \text{ KB} / (RTT \cdot 10^{-3}) = 1.5 \text{ MB} / RTT$.

→ TCP throughput 이 *loss 의 $1/\sqrt{p}$ 의존* — small loss 에 매우 sensitive.

**산업 시사** — 1% loss 가 *throughput 의 10x 감소*. 좋은 link 의 *< 0.01% loss* 가 핵심.

</details>

### Q7. Congestion control vs Flow control — 동시 작동

Server 가 5 GB file 전송. Client read 느림. Server 의 *throughput 제한*?

<details><summary>답</summary>

**두 가지 제한 동시 적용**:

**Flow control (rwnd)** — *receiver 보호*:
- Client buffer 가 *full* → ACK 의 *rwnd 감소*
- Server 가 *rwnd 만큼만* 전송

**Congestion control (cwnd)** — *network 보호*:
- Network 의 congestion → loss
- Server 가 *cwnd 감소*

**Effective window**:
$$\text{window} = \min(rwnd, cwnd)$$

**이 시나리오**:
- *Client read 느림* → rwnd ↓ 
- *Network 빠름* → cwnd ↑
- Dominant = *rwnd* (flow control)
- Server 가 *client read 속도에 throttle*

**Zero-window probing**:
- rwnd = 0 시 server 가 *주기적 1-byte probe* 보냄
- Client 가 read 후 rwnd open 되면 *probe response* 로 알림

**산업 사례**:
- HTTP server 가 slow mobile client 에 *file 보낼 때* — flow control 이 dominant
- 빠른 client 에 large file → cwnd 이 dominant

</details>

### Q8. Fast retransmit vs Timeout 의 recovery

Sender 가 1 MB 전송 중 packet #5 손실. Receiver 가 6, 7, 8 받음.

(a) Receiver 응답
(b) Sender recovery 동작

<details><summary>답</summary>

**(a) Receiver**:
- Packet 6 (out-of-order) → cumulative ACK 50000 *재전송*
- Packet 7 → 또 ACK 50000
- Packet 8 → 또 ACK 50000

→ Receiver 가 *3 dup ACK*.

**(b) Sender — Fast retransmit**:
- 3 dup ACK 도착 → *timeout 안 기다리고* packet 5 재전송
- ssthresh = cwnd / 2
- cwnd = ssthresh + 3 MSS  (3 packets 가 receiver 에 도착 = buffer 에서 떠남)
- *Fast recovery* → Congestion avoidance 진입

**비교 — Timeout 방식**:
- *Timeout* (보통 3+ RTT) 까지 대기
- ssthresh = cwnd / 2
- cwnd = 1 MSS → *slow start 부터*
- Recovery *훨씬 느림*

→ Fast retransmit 의 *RTT 단위 recovery* vs Timeout 의 *seconds 단위*. Severe congestion (multi packet loss) 만 timeout 으로.

</details>

### Q9. 디버그 — Throughput 이 *너무 낮음*

Same datacenter (RTT 1 ms), 10 Gbps link. iperf3 single stream 1 Gbps. 원인?

<details><summary>답</summary>

**1. TCP window vs BDP**:
- BDP = $10^{10} \times 10^{-3}$ = 1.25 MB
- Linux default rwnd ~4 MB → OK
- 그러나 *app buffer* 작거나 *slow read* 면 window 못 채움
- `ss -i` 로 cwnd, rwnd 확인

**2. CPU bottleneck**:
- iperf3 *single thread* → 1 core 만
- 10 Gbps 처리에 *4+ core* 필요
- 해결: `iperf3 -P 4` (parallel streams)

**3. MTU**:
- Default 1500 byte → per-packet header overhead
- Jumbo frame 9000 byte → throughput ↑ 30~50%
- *모든 hop* 이 jumbo 지원해야

**4. TCP variant**:
- *Reno* 의 느린 ramp up
- *CUBIC* (Linux default) 또는 *BBR*
- `sysctl net.ipv4.tcp_congestion_control`

**5. NIC offloading**:
- TSO/GSO/GRO 활성
- `ethtool -k eth0`

**6. Socket buffer auto-tuning**:
- `net.ipv4.tcp_rmem`, `tcp_wmem`
- `net.core.rmem_max`, `wmem_max`

**최종 점검**:
```
iperf3 -c server -P 8 -t 30 -w 16M
```
Multi-stream, large window.

</details>

### Q10. 디버그 — TIME_WAIT 폭증

Production server 의 *수만 TIME_WAIT* socket. 원인 + 해결.

<details><summary>답</summary>

**TIME_WAIT 의 의미**:
- Active close 한 측 (FIN 보낸 측) 의 socket 이 *2 × MSL* (~ 1~2 분) 유지
- *Delayed packet 흡수* + *FIN 재전송 응답*

**문제 — Server 의 TIME_WAIT 폭증**:
- *HTTP/1.0* 의 server-side close → server 가 active close
- 또는 *short-lived connection* 패턴
- Port 소진 위험 (max ~60k ephemeral)
- `ss -tan | awk '{print $1}' | sort | uniq -c`

**해결**:

1. **HTTP keep-alive** — connection 재사용
   - HTTP/1.1 의 *default*
   - Idle timeout 길게 (분 단위)

2. **Connection pooling** — app level
   - DB connection pool, HTTP client pool
   - 새 connection 의 *3-way handshake 비용* 회피

3. **net.ipv4.tcp_tw_reuse** — Linux
   - TIME_WAIT socket 의 *port + tuple* 재사용 (outgoing 만)
   - `sysctl -w net.ipv4.tcp_tw_reuse=1`

4. **Port range 확장**:
   - `net.ipv4.ip_local_port_range = 1024 65535`

5. **MSL 단축** (위험):
   - `net.ipv4.tcp_fin_timeout`
   - 너무 짧으면 delayed packet 문제

**Modern best practice**:
- HTTP/2 + HTTP/3 의 *connection multiplexing* → TIME_WAIT 근본 해결
- gRPC, WebSocket 의 *persistent connection*

</details>

### Q11. 면접 — *왜 TCP SYN flood 가 위험*?

SYN flood DDoS 의 mechanism + 방어.

<details><summary>답</summary>

**Attack**:
1. Attacker 가 *대량 SYN* (spoofed source IP) 전송
2. Server 가 SYN-ACK → *half-open connection* 생성, table 에 저장
3. Spoofed IP 라 *ACK 안 도착*
4. Server 의 *half-open table* 가득 → *진짜 client SYN 거부*

→ *Resource exhaustion* attack — bandwidth 가 아닌 *state* 공격.

**Defense**:

**1. SYN cookies** (Bernstein, 1996):
- Server 가 *half-open state 저장 안 함*
- 대신 *initial seq* 를 *cryptographic hash* (client IP, port, time, secret) 로 계산
- 진짜 client 의 ACK 도착 → *seq 검증*
- *Memoryless* — 불가능 attack

**2. Rate limiting**:
- 같은 source IP 의 SYN 빈도 제한
- Distributed DDoS 에 한계

**3. First-SYN drop**:
- 첫 SYN drop → 진짜 client 는 retransmit, bot 은 안 함

**4. DDoS mitigation service**:
- Cloudflare, AWS Shield, Akamai
- Anycast 로 분산 흡수
- Reverse proxy + filter

**산업** — SYN cookies + DDoS service 가 표준. *kernel-level mitigation* + *edge filtering*.

</details>

### Q12. 면접 — Congestion control 의 *fairness 한계*

"같은 link 에 두 TCP — *동일 bandwidth* 분배 되나?"

<details><summary>답</summary>

**Theoretical fairness — AIMD**:
- 같은 *RTT, MSS, variant* → 시간 충분하면 converge to fair share

**실제 unfairness 의 원인**:

1. **RTT 차이** — short RTT 가 cwnd 빨리 증가
   - Mathis: $T \propto 1/RTT$
   - 같은 link 라도 *경로 길이 다르면* unfair

2. **TCP variant 차이** — CUBIC vs Reno
   - CUBIC 의 *aggressive* growth → larger share

3. **Parallel connections** — *N connection* 의 throughput ~ *single 의 N 배*
   - Browser 가 multi-connection 사용 — *single-connection 사용자보다 unfair*

4. **UDP 의 unfairness** — UDP 는 congestion control 없음
   - TCP 를 *짓밟음* (압도)
   - 산업: *DASH over TCP* 표준화, QUIC 의 *responsible CC* 의무

5. **Queue management**:
   - FIFO 는 unfair
   - *Fair queueing* (FQ-CoDel) 의 per-flow isolation
   - Bufferbloat 해결의 한 축

**산업 — net neutrality 논쟁**:
- BitTorrent 의 multi-connection 이 bandwidth 큰 share
- ISP 의 *throttle* 시도 → 법적 분쟁

**답 핵심** — "Theoretical fairness 는 *clean* assumption 의 결과. *현실* 의 RTT/variant/connection-count 의 차이로 *unfair*. *AQM + per-flow fairness* 가 산업 trend. UDP/QUIC 의 *responsible CC* 의무화 진행."

</details>
