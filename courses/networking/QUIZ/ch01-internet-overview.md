# Ch 1 Computer Networks and the Internet — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

## 개념

### Q1. Packet vs Circuit switching

각 *3 가지 사용 사례* + 왜 적합한가.

<details><summary>답</summary>

**Packet switching** — Internet 의 표준:
1. *Web browsing* — bursty (페이지 로딩 후 idle, click 시 burst)
2. *Email* — 가끔만 송수신
3. *Video streaming* — 끊겨도 buffer 가 흡수

→ *Statistical multiplexing* 으로 여러 사용자의 *peak 합* 보다 적은 capacity 도 OK.

**Circuit switching** — 전통 전화망:
1. *전화 (음성)* — 일정한 bitrate, *delay-sensitive*
2. *전용회선 (leased line)* — bank 의 ATM network
3. *비행기 air traffic control* — 신호 *보장 필수*

→ *Bandwidth + delay 보장* — packet switching 의 *불확정성* 못 받음.

**현대 산업**:
- VoIP (Skype, WhatsApp): packet switching + QoS + jitter buffer 로 음성 OK
- *Pure circuit* 은 거의 사라짐 — packet 위의 *guaranteed service* (MPLS, dedicated VLAN) 가 대체

</details>

### Q2. Top-down approach 의 *학습적 이점*

Kurose 책의 *top-down* (vs bottom-up) 의 *3 가지 장점*.

<details><summary>답</summary>

1. **Motivation 우선** — application 의 *실제 요구* (HTTP page load, video stream) 부터 시작 → "왜 이 protocol 이 필요한가" 의 *맥락* 명확.

2. **Familiar territory** — 학생이 *web, email* 같은 친숙한 것부터. *layer 의 추상* 이 자연스럽게 이해됨.

3. **Service abstraction** — 위 layer 가 *아래 layer 의 service* 만 보고 짜는 *원칙* 이 명확. Bottom-up 은 *기술* 부터 가르치니 application 동기 늦게 와 흐려짐.

**Bottom-up 의 장점** (전통 교과서):
- *Layered build-up* — 작은 piece 부터 *큰 system* 으로
- *Engineering 관점* — 실제 design 의 순서

**현실** — 모범적 학생은 두 방향을 *모두* 본다. Tanenbaum (bottom-up) + Kurose (top-down) 같이 보는 게 추천.

</details>

### Q3. Layered architecture 의 trade-off

Layer 분리의 *장점 3* + *단점 1*.

<details><summary>답</summary>

**장점**:

1. **Modularity** — 한 layer 변경 시 *다른 layer 영향 X* (예: WiFi 신기술 도입에 TCP 코드 안 바꿈).
2. **Independent development** — 각 layer 별 *전문가 팀* 이 독립적으로 작업.
3. **Reusability** — 같은 layer 가 *다른 시스템* 에서 재사용 (IP layer 가 WiFi + Ethernet + cellular 위에서 동작).

**단점**:

1. **Performance overhead** — 각 layer 마다 *header 추가* + *processing*. *cross-layer optimization* 어려움 (예: wireless 에서 TCP 가 congestion 으로 오해석).

**Cross-layer 의 실제 적용 사례**:
- *Wireless TCP* — link layer 의 retransmission 을 TCP 에 *숨김* (snoop protocol)
- *DASH* — application 이 transport 의 congestion 신호로 video bitrate 조정
- *QUIC* — Transport + Crypto + Application 의 *경계 허물기*

이게 *clean layer 의 한계*. modern protocol 들은 *느슨한 layering*.

</details>

### Q4. Encapsulation 의 정확한 의미

Sender 의 packet 이 *5 layer 어떻게 변하는가*.

<details><summary>답</summary>

**Outbound flow (위→아래)**:

```
Layer 5 (App):       message = "GET / HTTP/1.1\r\n..."
                     
Layer 4 (Transport): [TCP header | message]
                     ↓ "segment"
                     [SrcPort=12345, DstPort=80, Seq=1, ...]
                     
Layer 3 (Network):   [IP header | TCP header | message]
                     ↓ "datagram"
                     [SrcIP=10.0.0.5, DstIP=93.184.216.34, TTL=64, ...]
                     
Layer 2 (Link):      [Eth header | IP header | TCP header | message | Eth trailer]
                     ↓ "frame"
                     [SrcMAC, DstMAC, Type=0x0800, ..., CRC32]
                     
Layer 1 (Physical):  bits (signal on wire/wireless)
```

**Inbound flow (아래→위)**: 각 layer 가 *자기 header 벗기고* 위로 전달.

**Router 의 처리**:
- 받은 frame → Eth header *벗김*
- IP header 확인 → routing 결정
- 새 frame 으로 다시 *encapsulation* (다른 link 의 MAC)
- 즉 router 는 *layer 3 까지만* 봄

**Switch 의 처리**:
- Eth frame 의 *destination MAC* 만 봄
- *layer 2 만*. IP/TCP 내용 모름

이 *header 의 nesting* 이 *encapsulation* 의 의미.

</details>

## 계산

### Q5. Transmission vs Propagation delay

서울-뉴욕 (8000 km), link bandwidth 1 Gbps, 1 KB packet. 두 delay 비교.

<details><summary>답</summary>

**Transmission delay**:
- $d_{trans} = L / R$ = (1KB × 8 bits/byte) / (1 Gbps) = 8000 / 10^9 = **8 μs**

**Propagation delay**:
- $d_{prop} = d / s$ = 8000 km / (2×10^8 m/s) = 8×10^6 / 2×10^8 = **0.04 sec = 40 ms**

**비율**: prop / trans ≈ **5000x**.

→ 장거리 + 빠른 link 에선 *propagation 이 압도*. RTT 가 80ms. *transmission 은 무시 가능*.

**시사**:
- Web page (수십 KB) 의 *수십 round trip* → propagation dominant
- *물리적 거리* 가 latency 의 lower bound
- CDN 의 의미 — *physically closer* edge server 로 propagation 줄임

**참고 (in-rack vs cross-region)**:
- 같은 rack: ~0.1 ms
- 같은 datacenter: ~1 ms
- 같은 region (cross-AZ): ~5 ms
- 다른 region: 50~150 ms
- 다른 대륙: 150~300 ms

</details>

### Q6. Bandwidth-Delay Product

서버 → 클라이언트 (link 100 Mbps, RTT 100 ms). *얼마나 데이터가 "in flight"* 일 수 있나?

<details><summary>답</summary>

**Bandwidth-Delay Product (BDP)**:

$$BDP = \text{bandwidth} \times \text{RTT}$$

= 100 Mbps × 0.1 s = 10 Mb = **1.25 MB**

이게 *최대 in-flight 데이터* — TCP window size 가 *이 정도 또는 더 커야* link 가 fully utilized.

**TCP 의 함의**:
- TCP default window = 64 KB (옛 stack)
- 64 KB / 100ms = 5 Mbps — 100 Mbps link 의 *5% 만 활용*
- *Window scaling option* (RFC 1323) 으로 1 GB+ window 가능
- 현대 Linux/Windows 가 *자동 tuning*

**LFN (Long Fat Network)**:
- High BDP network — 위성, 대륙간
- 큰 window 필요
- TCP 의 *slow start* 가 fully ramp up 까지 *많은 RTT* 걸림 — 짧은 connection 엔 unfair

이게 *QUIC* 가 *0-RTT* 와 *aggressive window 조절* 로 해결하는 부분.

</details>

### Q7. Queue 의 traffic intensity

Router 의 link bandwidth 100 Mbps, packet 평균 size 1500 bytes, 평균 도착률 7500 pps. Queue 안정?

<details><summary>답</summary>

**Traffic intensity 계산**:

$$\rho = \frac{La}{R}$$

- L = 1500 bytes × 8 bits/byte = 12,000 bits
- a = 7500 packets/sec
- R = 100,000,000 bps

$$\rho = \frac{12000 \times 7500}{10^8} = \frac{9 \times 10^7}{10^8} = 0.9$$

**ρ = 0.9** → 안정하지만 *queue delay 폭증 영역*.

| ρ | Queue 상태 |
|--|--|
| 0~0.5 | 안정, delay 무시 가능 |
| 0.5~0.8 | 약간의 queue |
| 0.8~1.0 | delay 폭증 (M/M/1 queue model 의 ρ/(1-ρ) curve) |
| 1.0+ | 무한 성장, *loss* 시작 |

ρ=0.9 에서 평균 queue length ≈ ρ/(1-ρ) = 9 packets, delay 도 *링크 capacity 의 9x packet transmission time*.

**대응**:
- *Capacity upgrade* — R ↑
- *Load shedding* — 일부 packet drop (RED, fair queueing)
- *QoS* — 중요 traffic 우선
- *Application redirection* — Anycast, load balancing

산업 — datacenter 의 *peak ρ < 0.7* 이 SLO. 그 이상은 tail latency 위험.

</details>

### Q8. 99% reliability 의 *9 추가*

Internet path 의 *5 hops*. 각 hop 의 packet loss 0.1%. End-to-end 의 success rate?

<details><summary>답</summary>

각 hop 의 success rate = 1 - 0.001 = 0.999

5 hops independent assumed:
$$P_{success} = 0.999^5 \approx 0.9950$$

= **99.5% success, 0.5% loss**.

**시사**:
- *단순 곱셈* 으로 reliability 떨어짐
- Internet path 가 *수십 hop* 이면 *cumulative loss* 큼 — TCP 의 retransmission 필요
- *Reliability 추가* 가 *낮은 layer 보다 application layer* 에 우선 (end-to-end argument)

**99 추가**:
- Three 9: 99.9% — 단일 hop, 잘 운영된 link
- Four 9: 99.99% — datacenter network
- Five 9: 99.999% — 전화망 표준 (5분/년 다운)
- Six 9: 99.9999% — 항공 신호

대부분 Internet end-to-end 는 *three~four 9*. *application 의 retry* 로 보강.

</details>

## 디버그

### Q9. ping 의 RTT 가 *spike*

서버 ping RTT 가 *평소 5ms, 갑자기 200ms+ random spike*. 진단.

<details><summary>답</summary>

**가능 원인**:

1. **Buffer bloat** — router buffer 가 *너무 큼* → 큰 queue → 큰 delay. *bufferbloat* 현상. 다른 traffic 이 link 차지하면 모든 packet 의 latency ↑.
   - 진단: `mtr` 로 각 hop 의 latency variance
   - 해결: FQ-CoDel, BBR 같은 *AQM (Active Queue Management)*

2. **WiFi interference / weak signal** — 무선이면 *signal 약함* 또는 *주변 jamming*. Reassociation 시 100ms+.
   - 진단: 유선과 비교
   - 해결: 5GHz/6GHz 채널, AP 가까이

3. **Sleeping host** — power-save mode 의 wakeup
   - 진단: 같은 spike pattern (예: 30s 마다)
   - 해결: disable power-save

4. **ISP의 traffic policing** — *peak 시간* 에 link 포화 → queueing delay 폭증
   - 진단: 시간대 별 latency
   - 해결: ISP 와 plan upgrade

5. **MTU mismatch / fragmentation** — 큰 packet 의 *fragmentation* 으로 처리 추가
   - 진단: `ping -s 1500` vs `ping -s 56`

6. **노이지한 neighbor** (cloud)
   - 진단: cloud provider metric
   - 해결: dedicated tenancy

**진단 도구**:
- `ping`, `mtr`, `traceroute`
- `iperf3` 로 bandwidth test
- `tcpdump` 로 packet 캡처
- ISP 가 제공하는 *latency dashboard* (Google Cloud, AWS)

</details>

### Q10. 디버그 — Throughput 이 link bandwidth 의 10% 만

100 Mbps link 인데 *iperf3 throughput 이 10 Mbps*. 원인?

<details><summary>답</summary>

**가능 원인** + 진단:

1. **TCP window too small**:
   - BDP 보다 작은 window → bandwidth 활용 ↓
   - 진단: `ss -i` (Linux) 의 cwnd, ssthresh, rwnd
   - 해결: window scaling 활성, OS auto-tuning 확인

2. **Packet loss 가 TCP throughput 죽임**:
   - TCP 의 *AIMD* 가 loss 시 cwnd /= 2
   - Even 0.1% loss → 큰 영향
   - Mathis equation: throughput ≈ MSS / (RTT × √loss)
   - 진단: `mtr` 의 packet loss %, link layer 의 retransmission

3. **CPU bottleneck** — 한쪽 host 의 CPU 가 packet processing 못 따라감
   - 진단: top, htop 으로 CPU usage 시 iperf
   - 해결: NIC offload (TSO, GSO, GRO), more cores

4. **MTU / fragmentation**:
   - jumbo frame 안 쓰면 1500 byte 단위 → header overhead
   - 진단: `ip link show` 의 MTU
   - 해결: 9000 byte jumbo frame (data center 표준)

5. **Half-duplex link** — 옛 hub 에서 *bidirectional* 안 됨
   - 진단: `ethtool eth0` 의 duplex
   - 해결: full-duplex switch

6. **Bottleneck 다른 곳** — link 100Mbps 인데 *path 의 어떤 hop* 이 더 느림
   - 진단: `iperf3` 를 *각 hop* 의 sub-segment 로

**Production tools**:
- `tcptrace` — pcap 분석
- `bcc-tools` (eBPF) — kernel-level metric
- `wireshark` 의 IO Graph

</details>

## 면접

### Q11. CDN 이 *왜 빠른가* — 설명

"Cloudflare / Cloudfront 같은 CDN 이 어떻게 사용자 경험을 빠르게?"

<details><summary>답</summary>

**CDN 의 3 가지 메커니즘**:

1. **Geographic proximity** — 사용자 가까운 *edge server* 에서 응답
   - 서울 사용자 → Cloudflare 의 *서울 PoP* (Point of Presence)
   - propagation delay 50~150ms → 5~20ms

2. **Caching** — 정적 content (이미지, JS, CSS) 를 edge 에 저장
   - origin server 까지 안 가도 됨
   - cache hit ratio 90%+ 흔함

3. **TCP optimization** — edge ↔ origin 사이 *최적화된 connection*
   - persistent connection
   - large window
   - TLS resumption

**부수 효과**:
- DDoS mitigation (대량 트래픽 흡수)
- TLS termination (edge 에서 처리, origin 은 평문)
- Compression, image optimization
- WAF (Web Application Firewall)

**기술 요소**:
- *DNS-based routing* — 같은 hostname 의 IP 가 *region 마다 다름*
- *Anycast* — 같은 IP 가 *여러 server 에 announce*. BGP 가 가장 가까운 곳으로 routing
- *Edge computing* — Cloudflare Workers, AWS Lambda@Edge 가 *코드 실행* 까지 edge 에서

**시사**:
- 1장의 *propagation delay* 가 정의하는 *물리적 lower bound*
- CDN 은 *이 lower bound* 를 *사용자 가까이* 가져옴
- 진정한 *bypass* 가 아니라 *cleverly engineering around* 

</details>

### Q12. 면접 — *layered architecture* 의 가치를 *옆 분야 비유*

"네트워크의 layer 처럼, 다른 engineering 분야에서도 layer abstraction 이 *어떻게 가치* 가 있는가"

<details><summary>답</summary>

**Software stack**:
- *Application code* → *framework* → *language runtime* → *OS* → *hardware*
- 각 layer 가 *위 layer 에 service* 제공. 아래 layer 변경 가능
- Network 의 5 layer 와 *형태적 동일*

**Programming abstraction**:
- *High-level language* (Python) → *bytecode* (CPython) → *machine code* → *CPU instruction*
- 각 layer 가 *아래의 복잡도 숨김*

**Hardware**:
- *Application IC* → *gate-level netlist* → *RTL (Verilog)* → *transistor* → *physics*

**Civil engineering**:
- *완성된 건물* → *층 단위* → *방 단위* → *벽·기둥* → *재료*

**핵심 원칙** (모든 분야 공통):
1. **Information hiding** — 각 layer 가 *implementation detail 숨김*
2. **Standard interface** — *위 ↔ 아래* 의 *명세된 계약*
3. **Independent evolution** — 한 layer 만 *교체·개선* 가능
4. **Reuse** — 같은 layer 가 *다른 system 에서* 재사용
5. **Specialization** — 각 layer 의 *전문화*

**Trade-off** (역시 공통):
- *Performance overhead* — *cross-layer optimization* 어려움
- *Abstraction leak* — 가끔 *아래 layer 의 detail* 이 위로 새어나옴 (예: TCP slow start, GC pause)
- *Debug difficulty* — *어느 layer 의 문제* 인지 식별

답 핵심 — *layering 은 boundary 가 아닌 *contract**. 네트워크 의 5 layer 도 *engineering 의 일반 원칙* 의 한 사례. 어떤 시스템도 *모든 것을 모놀리식* 으로 못 한다.

</details>
