# Ch 3 Transport Layer — 치트시트

> Transport service / UDP / TCP / Reliable transfer / Congestion control.

## §1 Transport service 한눈에

| | UDP | TCP |
|--|--|--|
| Connection | No | 3-way handshake |
| Reliability | No | ACK + retransmit |
| Order | No | Sequence number |
| Flow control | No | rwnd |
| Congestion control | No | cwnd (AIMD) |
| Header | 8 B | 20+ B |
| Checksum | Optional | Mandatory |
| Multiplexing | (dst port, dst IP) | 4-tuple |

## §2 UDP segment 구조 (8 byte header)

```
| Source Port (16) | Dest Port (16) |
| Length     (16)  | Checksum (16)  |
| Data ...                          |
```

- *Length*: header + data byte 수
- *Checksum*: 1's complement of 1's complement sum

## §3 TCP segment 구조 (20+ byte header)

```
| Source Port (16)   | Dest Port (16)            |
| Sequence Number (32)                           |
| ACK Number      (32)                           |
| HL(4)|Rsvd|Flags(8)| rwnd (16)                |
| Checksum (16)      | Urgent Pointer (16)       |
| Options (variable)                             |
| Data                                           |
```

**Flags**: URG, ACK, PSH, RST, SYN, FIN

## §4 Reliable Data Transfer 의 evolution

| Version | Channel 가정 | 기법 |
|--|--|--|
| rdt 1.0 | 완벽 | 그냥 전송 |
| rdt 2.0 | bit error | ACK/NAK + checksum |
| rdt 2.1 | (2.0 의 ACK 손상) | seq 0/1 |
| rdt 2.2 | (NAK 제거) | dup ACK |
| **rdt 3.0** | bit error + loss | + timer + retransmit |

## §5 Pipelined RDT — GBN vs SR

| | Go-Back-N | Selective Repeat |
|--|--|--|
| Receiver buffer | No (cumulative ACK) | Yes (per-packet) |
| Sender retransmit | All from lost | Only lost one |
| ACK | Cumulative | Individual |
| Bandwidth 효율 | Bad on loss | Good |
| Memory | Sender N | Both ~N |

TCP 는 *GBN + SR hybrid* — cumulative ACK + SACK (Selective ACK option).

## §6 TCP 3-way handshake

```
Client          Server
  | SYN, seq=x      |
  |---------------->|
  |                 |
  |  SYN-ACK, seq=y |
  |  ack=x+1        |
  |<----------------|
  |                 |
  | ACK, ack=y+1    |
  |---------------->|
  |     (+ data)    |
```

*SYN 도 seq 1 consume*. 첫 data byte 는 seq = x+1.

## §7 RTT estimation — EWMA

$$EstimatedRTT = (1-\alpha) \cdot EstimatedRTT + \alpha \cdot SampleRTT$$

$$DevRTT = (1-\beta) \cdot DevRTT + \beta \cdot |SampleRTT - EstimatedRTT|$$

$$Timeout = EstimatedRTT + 4 \cdot DevRTT$$

Default: $\alpha = 0.125$, $\beta = 0.25$.

**Karn 의 규칙**: Retransmitted segment 의 RTT 는 *EstimatedRTT 계산 제외*.

## §8 Fast retransmit

- *3 dup ACK* → 즉시 재전송 (timeout 안 기다림)
- ssthresh = cwnd / 2
- cwnd = ssthresh + 3 MSS  (3 packet 이 buffer 를 떠남)
- → *Fast recovery* 진입

## §9 Flow control vs Congestion control

| | Flow | Congestion |
|--|--|--|
| 보호 대상 | Receiver buffer | Network |
| 제어 변수 | rwnd | cwnd |
| Signal | rwnd field in ACK | Loss / RTT / ECN |
| Sender 결정 | $\min(cwnd, rwnd)$ |

## §10 TCP congestion control — phases

| Phase | 진입 조건 | 행동 |
|--|--|--|
| Slow start | 시작, timeout 후 | cwnd ×= 2 per RTT (exponential) |
| Congestion avoidance | cwnd ≥ ssthresh | cwnd += 1 MSS per RTT (linear, AIMD) |
| Fast recovery | 3 dup ACK 후 | cwnd = ssthresh, AI 시작 |

**Loss 시**:
- *Timeout*: ssthresh = cwnd/2, cwnd = 1, slow start
- *3 dup ACK*: ssthresh = cwnd/2, cwnd = ssthresh, AI (fast recovery)

## §11 Mathis equation

steady-state TCP throughput:

$$T \approx \frac{MSS}{RTT \cdot \sqrt{p}} \cdot C$$

$C \approx 1.22$ (Reno) 또는 *CUBIC 의 변형 식*.

| Loss prob | Throughput 비례 |
|--|--|
| $10^{-2}$ | × 10 |
| $10^{-4}$ | × 100 |
| $10^{-6}$ | × 1000 |

**시사** — 1% loss 가 *10x throughput 감소*. *< 0.01% loss link* 필수.

## §12 TCP 변종 — Reno / CUBIC / BBR

| | Reno | CUBIC | BBR |
|--|--|--|--|
| 발표 | 1990 | 2008 | 2016 |
| Signal | Loss | Loss | RTT + BW |
| Growth | Linear | Cubic | Model-based |
| Bufferbloat | 악화 | 악화 | **개선** |
| Default OS | (legacy) | Linux | YouTube/Google |
| Long fat pipe | Poor | OK | **Excellent** |

## §13 QUIC — 차세대 transport

| 특징 | QUIC | TCP |
|--|--|--|
| 위 layer | UDP | IP |
| 연결 시간 | *0~1 RTT* | 1.5 RTT |
| Stream | 다중 | 단일 (HoL block) |
| Encryption | 의무 (TLS 1.3 통합) | 별도 TLS |
| Migration | *연결 ID* 로 IP 변경 OK | 불가 |
| HTTP/3 | ✓ | ✗ |

## §14 Tool 모음

| Tool | 용도 |
|--|--|
| `ss -i` | TCP state, cwnd, rwnd 실시간 |
| `tcpdump` | Packet capture |
| `wireshark` | Visual analysis |
| `iperf3` | Throughput 측정 |
| `netstat -an` | Connection list |
| `sysctl net.ipv4.tcp_*` | TCP tuning |

## §15 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| UDP = unreliable, 그래서 쓸모 X | DNS/VoIP/Gaming 의 적합 선택 |
| TCP = 항상 reliable | *connection 끊기면* in-flight 데이터 손실 |
| RTT timeout = 항상 좋음 | Fast retransmit 이 *훨씬* 빠른 recovery |
| Window size = 자동 | *BDP* 보다 작으면 link 안 채움 |
| Slow start = 느림 | exponential, *수십 RTT 안에 link 채움* |
| AIMD = unfair | RTT 같으면 fair, 다르면 unfair |

## §16 핵심 mindmap

```
Transport Layer
├── UDP — connectionless, no reliability
│   └── header 8B, checksum
├── Reliable transfer
│   ├── rdt 1.0 → 3.0
│   └── Pipelined: GBN vs SR
├── TCP
│   ├── 3-way handshake
│   ├── seq / ack number
│   ├── RTT EWMA
│   ├── Fast retransmit (3 dup ACK)
│   └── Flow control (rwnd)
├── Congestion control
│   ├── Slow start
│   ├── Congestion avoidance (AIMD)
│   ├── Fast recovery
│   └── Variants: Reno / CUBIC / BBR
└── QUIC
    └── UDP + TLS 1.3 + multi-stream
```

## §17 1-line summary

> **Transport layer 는 *process 간 reliable + ordered 통신* 의 추상화. TCP 의 *AIMD congestion control* + *RTT-based timeout* + *flow control* 의 협주. QUIC 가 *연결 시간 + multiplexing + migration* 의 차세대.**
