# Chapter 3: Transport Layer — 학습 노트

> *Computer Networking: A Top-Down Approach* (Kurose & Ross, 8th Global Edition, 2021) **Chapter 3** (책 p.213~334, 책에서 가장 두꺼운 챕터).
> 3장은 *process-to-process* 통신의 *abstraction*. **UDP** (minimal) vs **TCP** (full-featured). *Reliable data transfer*, *flow control*, *congestion control* 의 fundamental.

## 들어가기 전에

- **선수 지식**: 1~2장 (IP, encapsulation, socket, HTTP)
- **학습 목표**
  1. **Transport service** — host-to-host (network layer) → process-to-process (transport)
  2. **Multiplexing/demultiplexing** — port 로 process 식별
  3. **UDP** — connectionless, *minimal* transport
  4. **Reliable Data Transfer (RDT)** — sequence number, ACK, timeout 의 *원리부터* 구축
  5. **Pipelined RDT** — Go-Back-N vs Selective Repeat
  6. **TCP** — connection-oriented, byte-stream, full-duplex. *handshake, segment, flow control*
  7. **Congestion control** — TCP Reno, CUBIC, BBR
  8. **QUIC** — modern transport over UDP. HTTP/3 의 기반
- **예상 학습 시간**: 240~300분 (책에서 *가장 어려운* 챕터 중 하나)

---

## 1. Transport Layer 의 역할

### 1.1 Process-to-Process Delivery

> Network layer (IP) 는 *host-to-host* delivery. Transport 는 *process-to-process*.

같은 host 의 *여러 process* (browser, email, IDE) 가 동시에 network 사용 → *어떤 segment 가 어떤 process 로*?

해결 — **port number** + *multiplexing/demultiplexing*.

### 1.2 Multiplexing / Demultiplexing

![Figure 3.2 — Multiplexing + demultiplexing. 책 p.219](/courses/networking/figures/ch03/fig-3-2.png)

**Multiplexing** (sender):
- 여러 process 의 message 를 *transport layer* 에서 *header 추가* + *combine*

**Demultiplexing** (receiver):
- Incoming segment 의 *header (port)* 보고 *적절한 socket 으로 전달*

#### UDP — Connectionless demux

- *(dst IP, dst port)* 로만 식별
- 같은 *(dst IP, dst port)* 면 *모두 같은 socket*
- *Source 무관* — broadcast 도 가능

#### TCP — Connection-oriented demux

- *(src IP, src port, dst IP, dst port)* 4-tuple 로 식별
- 다른 source 면 *다른 socket* — server 가 *수만 connection* 동시 처리 가능
- *Web server* 가 한 port (80) 로 *수만 client* 받는 비결

### 1.3 Transport 의 *2가지* — UDP vs TCP

| | UDP | TCP |
|--|--|--|
| Connection | connectionless | 3-way handshake |
| Reliability | none | full (retransmission) |
| Order | none | preserved |
| Flow control | none | sliding window |
| Congestion control | none | AIMD + slow start |
| Header | 8 bytes | 20+ bytes |
| Use | DNS, VoIP, gaming | HTTP, file transfer, email |

---

## 2. UDP — Connectionless Transport

### 2.1 UDP 의 *minimal* 서비스

> RFC 768 (1980). 가장 단순한 transport. *best-effort delivery*.

UDP 가 하는 일:
- *Multiplexing/demuxing* (port)
- *Light error detection* (checksum)

UDP 가 *안 하는* 일:
- Connection setup
- Retransmission
- Ordering
- Flow control
- Congestion control

### 2.2 UDP Segment Structure

![Figure 3.7 — UDP segment header (8 bytes). 책 p.229](/courses/networking/figures/ch03/fig-3-7.png)

```
0      16      32 bits
+-------+-------+
| src   | dst   |  ← port numbers (16-bit each)
| port  | port  |
+-------+-------+
| length| chk   |  ← length (segment 전체), checksum
+-------+-------+
| data...       |
+---------------+
```

- *Length*: header + data 의 byte 수
- *Checksum*: 16-bit one's complement sum (error detection)

### 2.3 UDP 의 사용 사례

| App | 왜 UDP |
|--|--|
| **DNS** | Small query, retry 가 app 책임. handshake 비용 회피 |
| **VoIP / Video conf** | Loss > delay (concealment 가능, retransmission 늦음) |
| **Online games** | Real-time state sync. 오래된 packet 무가치 |
| **DHCP, SNMP** | Network management, broadcast |
| **NTP** | Time sync, small message |
| **QUIC** | 자체 reliability + congestion control, UDP 는 transport |

### 2.4 UDP Checksum

> 16-bit one's complement sum of segment header + data + pseudo-header (src/dst IP, protocol).

수신 측:
- 같은 calculation → result *모두 1* 이어야 (no error)
- 다른 결과 → error 감지 → segment drop

*Note*: end-to-end checksum (link-layer 의 Ethernet CRC 와 별개). *application 안의 bit-flip* 도 검출.

> **함정 1**: UDP checksum 이 *모든 error* 잡지 못함. *2 bit flip 이 cancel* 가능. 진정한 reliability 는 app 책임.

---

## 3. Principles of Reliable Data Transfer

### 3.1 RDT 의 목표

> *Unreliable channel* (loss, error, reorder) 위에서 *reliable byte stream* 제공.

![Figure 3.8 — RDT 의 abstraction. 책 p.232](/courses/networking/figures/ch03/fig-3-8.png)

#### 진화적 설계

채널 가정을 *점진적으로 어렵게*:
- **rdt 1.0**: 완벽 채널 (loss/error 없음)
- **rdt 2.0**: bit error 만
- **rdt 2.1, 2.2**: 위 + corrupted ACK
- **rdt 3.0**: + packet loss
- **TCP**: + reorder, duplicate, congestion

### 3.2 rdt 1.0 — Perfect Channel

```
sender: send packet
receiver: extract data, deliver to upper layer
```

trivial. Channel 의 *가정 약화* 가 핵심 학습.

### 3.3 rdt 2.0 — Bit Errors

채널이 *bit 를 corrupt*. 어떻게 *retransmission* 시켜?

**해결책**:
- *Checksum* 으로 error 감지
- *ACK / NAK* (acknowledgment / negative)
- 받은 sender 의 *retransmit on NAK*

![Figure 3.10 — rdt 2.0 의 FSM. 책 p.234](/courses/networking/figures/ch03/fig-3-10.png)

문제 — *ACK/NAK 자체가 corrupt* 면?

### 3.4 rdt 2.1 — Sequence Number

> Packet 에 *sequence number* (0 또는 1) 추가.

만약 ACK 가 corrupt → sender 가 *그냥 retransmit*. Receiver 가 *같은 seq 의 packet* 받으면 *duplicate* 로 감지, ACK 만 다시 보냄.

stop-and-wait 의 *최소 필요 sequence number = 2* (0, 1 alternating).

### 3.5 rdt 3.0 — Packet Loss

> Packet 또는 ACK 가 *완전히 사라짐*.

**해결책** — **Timer**:
- Sender 가 *send 후 timer 시작*
- *Timeout* 전 ACK 받으면 OK
- *Timeout* 후 ACK 없으면 → retransmit
- *Duplicate 수신* 은 receiver 가 sequence number 로 처리

![Figure 3.16 — rdt 3.0 의 sender FSM. 책 p.243](/courses/networking/figures/ch03/fig-3-16.png)

#### Stop-and-Wait 의 *치명적 비효율*

매 packet 마다 *RTT + transmission* 대기. *link 활용률 매우 낮음*.

**예제 계산** (책 Kurose 8e p.246):
- L = 1000 bytes (8000 bits)
- R = 1 Gbps
- RTT = 30 ms

$d_{trans} = 8000 / 10^9 = 8$ μs.

Utilization:
$$U_{sender} = \frac{d_{trans}}{RTT + d_{trans}} = \frac{8 \text{ μs}}{30 \text{ ms} + 8 \text{ μs}} \approx 0.000267 = 0.027\%$$

1 Gbps link 의 *0.03% 만 활용*. 매우 낭비.

→ **Pipelined RDT** 필요.

---

## 4. Pipelined Reliable Data Transfer

### 4.1 Pipelining 의 *효율 향상*

여러 *unacknowledged packet* 동시 in-flight:

![Figure 3.18 — Pipelined transmission. 책 p.247](/courses/networking/figures/ch03/fig-3-18.png)

Window size N 으로 *N packet 동시 in-flight*:

$$U = \min\left( \frac{N \cdot d_{trans}}{RTT + d_{trans}}, 1 \right)$$

예: N=3 → 위 예제의 utilization 0.08% (여전히 낮음). N 커야 link 활용.

이 *N* 이 *bandwidth-delay product (BDP)* 까지 도달해야 link 의 *full bandwidth* 활용.

### 4.2 Go-Back-N (GBN)

> Sender 가 *N 까지 unack* 가능. Receiver 가 *cumulative ACK* — "이 seq 까지 모두 받았음".

#### Sender 동작

- *Window* `[base, base + N - 1]` 안의 packet 전송
- Timer 는 *oldest unack packet* 의
- *Timeout* → window 의 *모든 unack packet* 재전송

#### Receiver 동작

- *Expected seq* 와 다른 packet 도착 → *discard + re-ACK 마지막 in-order*
- Cumulative ACK — "이 seq 까지 모두 OK"

#### 효율

- *Burst loss* 시 *모든 후속 packet 재전송* → 낭비

### 4.3 Selective Repeat (SR)

> Receiver 가 *out-of-order packet* 도 *buffer*. 각 packet 의 *개별 ACK*.

#### Sender 동작

- 각 packet 의 *individual timer*
- *Timeout 한 packet 만* 재전송

#### Receiver 동작

- Out-of-order packet 도 *buffer*
- *Missing packet* 도착 시 *deliver up to highest in-order*

#### Comparison

| | Go-Back-N | Selective Repeat |
|--|--|--|
| Receiver buffer | 없음 | window size N |
| Timer | 1 (oldest) | N (per packet) |
| Loss 대응 | window 전체 retransmit | 잃은 것만 |
| Complexity | 간단 | 복잡 |
| 효율 | low loss rate 에 OK | high loss rate 에 우월 |

**TCP** 는 *둘의 hybrid* — cumulative ACK + selective retransmission (SACK).

---

## 5. TCP — Transmission Control Protocol

### 5.1 TCP 의 특성

> RFC 793 (1981, 옛). 현대는 RFC 9293 (2022 consolidated). *Internet 의 가장 핵심 protocol*.

- **Connection-oriented** — handshake 후 통신
- **Byte stream** — message boundary 없음 (UDP 와 다름)
- **Full-duplex** — 양방향 동시
- **Point-to-point** — broadcast 안 됨
- **Reliable + ordered** — 모든 byte 가 *손실 없이 순서대로*
- **Flow control** — receiver buffer overflow 방지
- **Congestion control** — network congestion 회피

### 5.2 TCP Segment Structure

![Figure 3.29 — TCP segment header. 책 p.262](/courses/networking/figures/ch03/fig-3-29.png)

```
0       16       32 bits
+-------+--------+
| src   | dst    |   port (16-bit)
+-------+--------+
| sequence number       | (32-bit)
+----------------------+
| acknowledgment number | (32-bit)
+--+----+--+--+--+--+--+
| HL | rsv | flags | rwnd | flags: URG/ACK/PSH/RST/SYN/FIN
+--+----+--+--+--+--+--+
| checksum   | urgent ptr |
+------+-----+-----+------+
| options (up to 40 bytes) |
+--------------------------+
| data...                  |
+--------------------------+
```

핵심 field:
- **Sequence number** — 첫 byte 의 *stream offset*
- **Acknowledgment number** — 받은 *다음 expected* byte
- **Receive window (rwnd)** — receiver 의 *남은 buffer*
- **Flags**: SYN (open), FIN (close), RST (reset), ACK (ack valid), PSH (push to app), URG

### 5.3 Sequence Number — Byte-stream

> TCP 의 *seq 는 byte 단위*, segment 단위가 아님.

예: 500,000 byte file, MSS=1000:
- Segment 1: seq=0, 1000 bytes
- Segment 2: seq=1000, 1000 bytes
- Segment 3: seq=2000, 1000 bytes
- ...

ACK 도 byte 단위. *"seq 1000 까지 모두 받음, 다음 1001 보내"*.

### 5.4 TCP Connection Establishment — 3-way Handshake

![Figure 3.39 — TCP 3-way handshake. 책 p.281](/courses/networking/figures/ch03/fig-3-39.png)

```
Client                              Server
  |                                   |
  |---- SYN, seq=x ------------------>|
  |                                   |
  |<--- SYN-ACK, seq=y, ack=x+1 ------|
  |                                   |
  |---- ACK, seq=x+1, ack=y+1 ------>|
  |                                   |
  | (이제 data 전송 가능)              |
```

3 step:
1. Client → Server: SYN. *client's initial seq* (random).
2. Server → Client: SYN-ACK. *server's initial seq* (random) + *ack client seq + 1*.
3. Client → Server: ACK. *ack server seq + 1*.

**RTT cost** — 1 RTT 후 *3rd step + data* 가능 (실은 3rd step 에 data piggyback OK).

#### Why 3 steps?

- 2 step 만 으로는 *delayed packet* 이 *fake connection* 시작 위험
- 3 step 으로 *양쪽이 서로의 SYN 받음 확인*

### 5.5 TCP Connection Termination — 4-way Handshake

```
Client                              Server
  |---- FIN ---------------------->|
  |<--- ACK -----------------------|
  |  (server 가 data 마저 send)     |
  |<--- FIN -----------------------|
  |---- ACK ---------------------->|
  |  (TIME_WAIT 2*MSL)            |
```

*Full-duplex* 이라 *양방향 close* 각각 처리. **TIME_WAIT** 2*MSL (= 2 분, 최대 segment lifetime) 동안 *delayed packet 흡수*.

### 5.6 TCP RTT 추정 + Timer

#### EWMA — Exponentially Weighted Moving Average

각 segment 의 *measured RTT* 로:

$$EstimatedRTT = (1 - \alpha) \cdot EstimatedRTT + \alpha \cdot SampleRTT$$

- 보통 $\alpha = 0.125$
- *Smooth estimate* — outlier 영향 적음

**RTT 변동 (DevRTT)**:

$$DevRTT = (1-\beta) \cdot DevRTT + \beta \cdot |SampleRTT - EstimatedRTT|$$

- $\beta = 0.25$

**Timeout**:

$$TimeoutInterval = EstimatedRTT + 4 \cdot DevRTT$$

*Margin 4 × DevRTT* — variance 가 큰 link 에 더 큰 timeout.

### 5.7 Fast Retransmit

> *Timeout 기다리지 않고* loss 빠르게 감지.

![Figure 3.36 — Fast retransmit. 책 p.278](/courses/networking/figures/ch03/fig-3-36.png)

**Mechanism — duplicate ACK**:
- Receiver 가 *out-of-order packet* 받으면 *마지막 in-order seq* 의 *ACK 재전송*
- Sender 가 *3 duplicate ACK* 받으면 → "다음 expected packet 잃었다" 판단
- *Timeout 안 기다리고 즉시 retransmit*

→ Timeout (보통 ~3 RTT) 보다 *훨씬 빠른 recovery*.

### 5.8 TCP Flow Control

> Receiver 의 *buffer overflow* 방지.

![Figure 3.38 — TCP flow control. 책 p.280](/courses/networking/figures/ch03/fig-3-38.png)

**rwnd** (receive window):
- Receiver 가 매 ACK 마다 *남은 buffer size 알림*
- Sender 가 *그 한도 안* 에서만 transmission

```
rwnd = BufferSize - (LastByteRcvd - LastByteRead)
```

- Receiver application 이 *느리게 read* 하면 → buffer 차오름 → rwnd 줄어듦
- Sender 가 *throttle*

> **Flow control vs Congestion control** — Flow 는 *end-host 의 buffer* 보호. Congestion 은 *network 의 router buffer* 보호. 별개 mechanism.

---

## 6. Principles of Congestion Control

### 6.1 Congestion 의 *비용*

![Figure 3.46 — Throughput vs offered load. 책 p.292](/courses/networking/figures/ch03/fig-3-46.png)

Offered load ↑ → throughput ↑ (까지는 잘 됨). Load > capacity 면:
- *Queue 폭증* → delay 폭증
- *Loss 폭증* → retransmission ↑ → 더 큰 load → *congestion collapse*

이게 **congestion collapse** — 1980년대 NSFNET 의 실제 사고. throughput 이 *0 에 가깝게 떨어짐*.

### 6.2 두 접근

- **End-to-end** — sender 가 *loss/delay 관찰* 후 self-throttle. *TCP 의 방식*.
- **Network-assisted** — router 가 *explicit feedback* 제공 (ECN — Explicit Congestion Notification).

산업 — *대부분 end-to-end*. ECN 은 *complement*.

---

## 7. TCP Congestion Control

### 7.1 *AIMD* — Additive Increase, Multiplicative Decrease

![Figure 3.50 — AIMD 의 sawtooth. 책 p.298](/courses/networking/figures/ch03/fig-3-50.png)

> "*조심스럽게 늘리고, 손실 시 절반*"

Sender 가 *congestion window (cwnd)* 보유:
- *No loss*: cwnd += 1 MSS per RTT (additive increase)
- *Loss*: cwnd /= 2 (multiplicative decrease)

→ *sawtooth* pattern. 결과적 *공정한 sharing*.

### 7.2 TCP Reno — 4 phase

![Figure 3.53 — TCP Reno 의 4 phase. 책 p.302](/courses/networking/figures/ch03/fig-3-53.png)

#### (1) Slow Start

- cwnd = 1 MSS (시작)
- *매 ACK 마다 cwnd += 1 MSS* → *cwnd doubles per RTT* (exponential)
- 빠르게 ramp up

#### (2) Congestion Avoidance

- cwnd ≥ ssthresh (slow start threshold) 에 도달
- *매 RTT 마다 cwnd += 1 MSS* — linear (additive increase)

#### (3) Fast Recovery

- 3 dup ACK 발생 → *light loss*
- ssthresh = cwnd / 2
- cwnd = ssthresh + 3 MSS (3 dup ACK 로 buffer 가 *비어있음*)
- *Congestion avoidance 로 직접 진입*

#### (4) Timeout

- 더 심각한 *loss* (또는 long delay) 가정
- ssthresh = cwnd / 2
- *cwnd = 1 MSS* — slow start 다시 시작

### 7.3 TCP CUBIC — 현대 default

> Linux 의 *default*. *High BDP* network 에 최적화.

cwnd 의 *비선형 증가*:

$$cwnd(t) = C \cdot (t - K)^3 + W_{max}$$

- $W_{max}$: 직전 loss 시 cwnd
- $K$: $W_{max}$ 도달 시간
- $C$: scaling constant

특징:
- *Loss 후 처음엔 빨리* 회복 ($W_{max}$ 가까이)
- *그 후 천천히* probing
- *High-BDP* network 에서 Reno 보다 *훨씬 빠른 recovery*

### 7.4 TCP BBR — 2016년 Google

> Loss 기반이 아닌 *bandwidth + RTT 측정* 기반.

핵심 아이디어:
- *BtlBw* (bottleneck bandwidth) 추정 — packet delivery rate 의 max
- *RTprop* (round-trip propagation) 추정 — RTT 의 min
- Optimal cwnd = BtlBw × RTprop = BDP
- *Loss 안 기다림* — *delay 증가* 가 *congestion 신호*

산업 채택:
- YouTube, Google Cloud — 4% throughput ↑, 14% RTT ↓
- Cloudflare 의 일부
- Linux 4.9+ option

### 7.5 Throughput 식 — Mathis Equation

steady-state TCP throughput 의 *근사*:

$$T \approx \frac{MSS}{RTT \cdot \sqrt{p}}$$

- p: packet loss rate
- MSS: maximum segment size

이게 *2장의 web latency 예제* 에서 봄. *long fat network* + *small loss* 가 *throughput 매우 제한*.

---

## 8. QUIC — Modern Transport

### 8.1 동기

TCP 의 한계:
- *3-way handshake* 의 1 RTT
- *Head-of-line blocking* — 한 packet loss 가 *모든 stream* 차단
- *TLS 별도 handshake* — 추가 1 RTT
- *Connection migration 어려움* — IP 변경 시 connection 끊김 (mobile 의 WiFi↔cellular)

### 8.2 QUIC 의 해결

> Google 2012 시작, IETF 표준화 2021 (RFC 9000).

특징:
- **UDP 위 user-space** — kernel TCP stack 우회
- **Built-in TLS 1.3** — handshake 1 RTT, 0-RTT resumption
- **Multiplexed streams** — 각 stream 독립 (TCP HOL blocking 해결)
- **Connection ID** — IP 바뀌어도 *connection 유지*
- **Forward error correction** (옵션) — packet loss 일부 회복

### 8.3 QUIC 의 산업 채택

- **HTTP/3** 의 transport
- 2026 현재 *Internet traffic 의 30~50%*
- Google, Cloudflare, Facebook, Akamai 가 *default*
- Chrome, Firefox, Safari 모두 지원

### 8.4 TCP vs QUIC 의 비교

| | TCP | QUIC |
|--|--|--|
| Layer | kernel | user-space |
| Setup | 1 RTT (TCP) + 1 RTT (TLS) = 2 RTT | **1 RTT** (combined) or **0-RTT** (resumption) |
| HOL blocking | yes (TCP level) | **no** (per-stream) |
| Connection migration | new connection needed | **same connection ID** |
| Deployment | OS upgrade | application upgrade |
| Header overhead | ~20 bytes + TLS | similar (encrypted) |

> **함정** — QUIC 의 *kernel 우회* 가 양날의 검. Linux kernel TCP stack 이 *수십년 최적화*. QUIC 의 *user-space* 가 *CPU 부담 더 큼* — bandwidth 가 무한이면 TCP 가 약간 빠름. *latency-bound* workload 에 QUIC 압도.

---

## 자주 빠지는 함정

| # | 함정 | 정정 |
|--|--|--|
| 1 | TCP segment 가 *message boundary* 유지 | byte stream. boundary 무관. *receiver 가 직접 parse* |
| 2 | UDP 가 *언제나 빠름* | TCP handshake 는 1 RTT. UDP 의 advantage 는 *no retransmit*, latency 우선 case 만 |
| 3 | UDP checksum 이 *모든 error 검출* | 16-bit 만 — 2 bit flip cancel 가능. app 책임 |
| 4 | TCP 의 cumulative ACK 가 *Go-Back-N* | TCP 는 *GBN + SR hybrid*. SACK option 으로 selective |
| 5 | Stop-and-wait 가 *현대 TCP* | 옛 옛. 현대는 *pipelined + sliding window* |
| 6 | TCP 의 *fast retransmit* 가 *timeout 기반* | *3 duplicate ACK* 기반. timeout 보다 훨씬 빠름 |
| 7 | Flow control = Congestion control | 별개. Flow = receiver buffer, Congestion = network |
| 8 | AIMD 가 *모든 TCP variant* | Reno 만. CUBIC 은 cubic function, BBR 은 bandwidth-based |
| 9 | TCP 가 *모든 application 에 best* | UDP/QUIC 가 *latency-critical* 에 우월. HTTP/3 이 증명 |
| 10 | 3-way handshake 의 *2 step 으로 충분* | delayed packet 의 *fake connection* 위험 |
| 11 | TIME_WAIT 이 *불필요* | delayed packet 흡수 + *retransmitted FIN* 대응 |
| 12 | QUIC 가 *항상 TCP 보다 빠름* | high-bandwidth + no loss 면 TCP 약간 우월. *latency-bound* 에서 QUIC 압도 |

---

## 자가점검

1. *Multiplexing/demultiplexing* 의 *UDP 와 TCP 차이* (2-tuple vs 4-tuple).
2. UDP 의 *5 가지 service 부재*.
3. *rdt 2.0 → rdt 3.0* 의 채널 가정 변화 + 각 단계의 *추가 mechanism*.
4. *Stop-and-wait* 의 utilization 식 + 왜 매우 비효율.
5. *Go-Back-N* vs *Selective Repeat* 의 receiver 동작 차이.
6. *TCP segment* 의 핵심 field 5가지.
7. *3-way handshake* 의 sequence number 흐름 + *왜 2 step 으로 부족*.
8. *EWMA RTT estimate* + *timeout interval* 식.
9. *Fast retransmit* 의 *3 duplicate ACK* trigger.
10. *Flow control* (rwnd) vs *Congestion control* (cwnd) 의 차이.
11. *AIMD* 의 4 단계 (slow start, congestion avoidance, fast recovery, timeout) 동작.
12. *Mathis equation* + 그 시사.
13. *QUIC* 의 4 가지 개선 (handshake, HOL, migration, deployment).

### 해답 (간략)

1. UDP: (dst IP, dst port). TCP: (src IP, src port, dst IP, dst port). TCP 는 다른 source 면 다른 socket.
2. Connection setup, retransmission, ordering, flow control, congestion control.
3. 1.0: perfect. 2.0: + bit error → checksum + ACK/NAK. 2.1/2.2: + corrupted ACK → seq num. 3.0: + packet loss → timer.
4. $U = d_{trans}/(RTT + d_{trans})$. 1 Gbps, 30ms RTT, 1500B packet 에서 *0.03%*.
5. GBN: out-of-order drop, cumulative ACK. SR: out-of-order buffer, per-packet ACK.
6. src/dst port, seq number, ack number, flags (SYN/ACK/FIN/RST), receive window.
7. SYN(x) → SYN-ACK(y, ack=x+1) → ACK(ack=y+1). 2 step 만 으로는 delayed packet 이 fake connection 시작 가능.
8. EstimatedRTT = (1-α) EstimatedRTT + α SampleRTT, α=0.125. Timeout = EstimatedRTT + 4 DevRTT.
9. Receiver 의 *cumulative ACK 가 3번 같음* (next expected 가 아직 도착 안 함). *missing packet* 빠르게 retransmit.
10. Flow: receiver buffer 보호 (rwnd). Congestion: network 보호 (cwnd). Sender 는 min(rwnd, cwnd) 한도.
11. Slow start: cwnd doubles per RTT (exponential). Congestion avoidance: +1 MSS per RTT (linear). Fast recovery: 3 dup ACK → ssthresh = cwnd/2, cwnd = ssthresh + 3. Timeout: ssthresh = cwnd/2, cwnd = 1.
12. $T \approx MSS / (RTT \sqrt{p})$. RTT ↑ 또는 loss ↑ 면 throughput 급감.
13. Combined handshake (TCP+TLS in 1 RTT), per-stream multiplexing (HOL 해결), connection ID (IP 변경 OK), user-space (kernel upgrade 불필요).

---

## 다음 학습으로

- **4-5장 (Network Layer)** — TCP 의 *underlying transport* — IP routing, queueing
- **8장 (Security)** — TLS 1.3 의 handshake details + QUIC 의 *built-in* TLS
- **HTTP/3** — QUIC 위의 application
- **CDN performance** — TCP/QUIC 의 *real-world impact*

> *Tools to try*:
> - `tcpdump -i en0 -n 'tcp port 443'` — TCP segment 캡처
> - `ss -i` (Linux) — *현재 TCP* connection 의 cwnd, ssthresh, RTT
> - `tc qdisc add dev eth0 root netem delay 100ms loss 1%` — *artificial RTT/loss* injection
> - `iperf3 -c server` — bandwidth measurement
> - Wireshark 의 *TCP Stream Graph* — sequence number + ACK 시각화
