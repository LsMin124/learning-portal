# Ch 1 Internet Overview — 치트시트

## TL;DR

- **Internet** = network of networks. End systems + links + routers + ISPs
- **Top-down approach** — Application → Transport → Network → Link → Physical
- **Packet switching** (Internet) vs **Circuit switching** (전화망)
- **4 delay**: processing + queuing + transmission + propagation
- **Bottleneck link** 이 throughput 결정
- **Encapsulation** — 각 layer header 추가 (message → segment → datagram → frame → bits)
- **Security threats**: malware / DDoS / sniffing / IP spoofing

---

## Quick Reference

### 표 1. Internet 의 정의

| 측면 | 내용 |
|--|--|
| Nuts-and-bolts | end systems + links + routers + ISPs |
| Services | distributed app 에 service 제공 |
| Protocol | format + order + actions |

### 표 2. Access network

| 종류 | 속도 | Media |
|--|--|--|
| DSL | 5~50 Mbps | copper |
| Cable (HFC) | 100M~Gbps | coax |
| FTTH (PON) | 1 Gbps+ | fiber |
| Ethernet (LAN) | 100M~10G | UTP/fiber |
| WiFi (802.11) | ~100M~Gbps | radio |
| Cellular (4G/5G) | 10M~Gbps | radio |

### 표 3. Switching

| | Packet | Circuit |
|--|--|--|
| 자원 | on-demand (statistical mux) | 예약 |
| 효율 | bursty 우수 | 일정 부하 우수 |
| 보장 | best effort | bandwidth 보장 |
| 사용 | Internet | 옛 전화망 |

### 표 4. 4 Delay

$$d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$$

| Delay | 정의 | 단위 |
|--|--|--|
| Processing | header 검사, error check | μs |
| Queuing | buffer 대기 (가장 가변) | ms~s |
| Transmission | L/R (link push out) | μs~ms |
| Propagation | d/s (물리 이동) | ms (장거리) |

**Traffic intensity**: $\rho = La/R$. $\rho \to 1$ 에서 queue 폭주.

### 표 5. Throughput

- $T = \min(\text{link bandwidths along path})$ — **bottleneck**
- TCP throughput: limited by *BDP* + *loss* (Mathis: $T \approx MSS / (RTT \sqrt{loss})$)

### 표 6. Internet Protocol Stack

| Layer | 단위 | Protocol | 주소 |
|--|--|--|--|
| Application | message | HTTP, DNS, SMTP | URL, hostname |
| Transport | segment | TCP, UDP | port (16-bit) |
| Network | datagram | IP, ICMP | IP address (32/128-bit) |
| Link | frame | Ethernet, WiFi | MAC (48-bit) |
| Physical | bits | UTP, fiber, radio | — |

### 표 7. Switch vs Router

| | Switch | Router |
|--|--|--|
| Layer | 2 (link) | 3 (network) |
| 주소 | MAC | IP |
| Domain | one LAN | inter-network |
| Decision | MAC table | routing table |
| 예시 | Cisco switch | Cisco router |

### 표 8. Security threats

| 위협 | 방어 |
|--|--|
| Malware (virus/worm/trojan) | antivirus, sandboxing, patch |
| DDoS (flood, syn-flood) | CDN, rate limiting, capacity |
| Packet sniffing | TLS, end-to-end 암호화 |
| IP spoofing | ingress filtering, auth |

---

## Mind Map

```
1장 Computer Networks and the Internet
├─ 1. What Is the Internet?
│   ├─ Nuts-and-bolts (hosts + links + routers + ISPs)
│   ├─ Services (distributed app)
│   └─ Protocol (format + order + actions)
├─ 2. Network Edge
│   ├─ Hosts (client / server)
│   └─ Access network (DSL/Cable/FTTH/Ethernet/WiFi/Cellular)
├─ 3. Network Core
│   ├─ Packet switching (store-and-forward, queue, loss)
│   ├─ Circuit switching (FDM/TDM)
│   └─ ISP hierarchy (tier-1 / regional / access / IXP)
├─ 4. Performance
│   ├─ 4 delay (proc + queue + trans + prop)
│   ├─ Traffic intensity ρ = La/R
│   ├─ Bottleneck throughput
│   └─ BDP = bandwidth × RTT
├─ 5. Layered Architecture
│   ├─ 5 layers (App/Trans/Net/Link/Phys)
│   ├─ Encapsulation (header 추가)
│   └─ Switch vs Router
├─ 6. Security
│   ├─ Malware, DDoS, sniffing, spoofing
│   └─ → Ch 8
└─ 7. History (ARPANET → WWW → Cloud)
```

---

## 1-line summary

| 절 | 한 줄 |
|--|--|
| 1 | Internet = network of networks. Protocol = format + order + actions |
| 2 | Edge = host + access network (DSL/Cable/FTTH/WiFi/Cellular) |
| 3 | Core = packet switching, store-and-forward, ISP hierarchy |
| 4 | 4 delay = proc + queue + trans + prop. Bottleneck = throughput |
| 5 | 5 layer stack, encapsulation, switch (L2) vs router (L3) |
| 6 | Security threats: malware / DDoS / sniffing / spoofing |
| 7 | ARPANET → WWW → broadband → mobile → cloud → 5G/IoT |
