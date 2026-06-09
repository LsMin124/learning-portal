# Ch 4 Network Layer: Data Plane

> Kurose & Ross 의 Ch 4. *Network layer 의 두 면 중 data plane* — packet 의 입력 → 처리 → 출력 의 *router 내부 동작*. Control plane (routing protocol, table 생성) 은 Ch 5.

---

## §0 도입 — *packet 하나가 router 를 통과하는 수 나노초*

> **핵심 한 문장**: Network layer 의 일은 단 하나 — datagram 을 출발 host 에서 목적 host 로 옮기는 것 — 이고, 4장은 그중 *data plane*, 즉 router *내부* 에서 packet 이 입력 → table lookup → switching → 출력으로 빠져나가는 *수 나노초* 의 기계장치를 들여다본다(경로를 *계산* 하는 control plane 은 §5장).

router 의 핵심은 *forwarding table* 과 *longest prefix match*(§3), 그리고 그 lookup 을 line-speed 로 처리하는 input/output port·switching fabric 의 4 component(§2)다. 여기서 "어떻게 충분히 빠른가"가 hardware 설계의 전부다.

그 위에 *IPv4 의 실제 운영*(§3~§6) — datagram format, 주소 체계와 CIDR, DHCP, NAT, fragmentation — 이 얹힌다. NAT 와 IPv6(§7)는 모두 "IPv4 주소가 부족하다"는 *한 압력* 에서 갈라져 나온 두 답이다.

마지막 *generalized forwarding*(§9, OpenFlow→P4)은 "destination IP 만 보던" router 를 "임의 field 를 match 해 임의 action 을 하는" programmable 장치로 일반화하며, §5장 SDN 의 다리가 된다.

---

## 들어가기 전에

- **선수 지식**: 1장(packet switching, encapsulation, 5-layer), 2~3장(IP·port 의 쓰임), 2진수/CIDR 비트 연산
- **학습 목표**
  1. **Data plane vs control plane 분리** — SDN 이전/이후의 architecture
  2. **Router 내부 4 component** — input port·switching fabric·output port·routing processor
  3. **IPv4 의 실제 운영** — datagram·주소/CIDR·DHCP·NAT·fragmentation
  4. **IPv6** — *왜 만들었고, 왜 전환이 아직 안 끝났나*
  5. **Generalized forwarding** — OpenFlow → P4 의 match-action
- **예상 학습 시간**: 150~200분

---

## §1 Network layer 의 *두 plane*

Network layer 의 task = host A 의 datagram 을 host B 에게 전달. 이를 위한 *2 가지 일*:

| | Data plane | Control plane |
|--|--|--|
| 무엇 | 각 router 의 *forwarding 결정* | *route 의 계산* |
| 시간 단위 | *nanosecond* (per packet) | *millisecond~second* (per route change) |
| 위치 | 각 router 내부 | router 분산 (traditional) 또는 *중앙 controller* (SDN) |
| 동작 | Forwarding table lookup → output port | Routing algorithm → forwarding table 생성 |
| 비유 | *교차로에서 차를 안내* | *지도 작성 + 업데이트* |

![Figure 4.1 — Network layer — host·router 의 계층. 책 p.304](/courses/networking/figures/ch04/fig-4-1.png)

> 직관: network layer 는 *모든 host 와 모든 router* 가 구현하는 유일한 계층이다. End system 은 5계층 전부를, router 는 network 까지(아래 link·physical 포함)를 갖는다 — 그래서 datagram 이 host→router→…→host 로 *계층을 오르내리며* 전달된다.

### §1.1 Forwarding vs Routing

- **Forwarding** = router 의 *하나의 packet* 처리. *local + 빠름*.
- **Routing** = network 의 *source → destination 경로* 결정. *global + 느림*.

비유:
- Forwarding = 교차로 의 *직진/좌회전* 결정
- Routing = 출발 → 도착 의 *전체 경로* 계획

### §1.2 Traditional vs SDN

**Traditional** (1980~2010s):
- 각 router 가 *control + data plane* 동시
- Routing protocol (OSPF, BGP) 이 *분산 메시지*
- 장: scalable, robust. 단: 복잡, 변경 어려움, vendor-locked.

**SDN** (2010~):
- *Remote controller* 가 control plane 통합 담당
- Router 는 *data plane 만* — *dumb pipe + match-action*
- Southbound protocol = OpenFlow
- 장: 중앙 제어, programmable. 단: controller 가 SPOF 가능.

**산업 현실 (2026)**:
- Datacenter 내부: SDN 표준 (Google B4, Facebook Fabric)
- Enterprise WAN: SD-WAN
- ISP backbone: traditional + 부분 SDN

### §1.3 Network service model — best-effort

IP 의 service:
- **Best-effort delivery** — try 만. *no guarantee*.

IP 가 *보장 안 하는 것*:
- 도착 (loss 가능)
- 순서 (out-of-order)
- Timing (delay variable)
- Bandwidth
- Error-free (corruption)

→ TCP 가 위에서 reliable 보장. UDP 는 *그대로 노출*.

**대안 service models (역사)**:
- ATM CBR (1990s) — 음성/영상 의 bandwidth + delay 보장. 실패.
- IntServ/RSVP (1994) — per-flow. *scalability* 부족. 실패.
- DiffServ (1998) — per-class. *부분 채택* (DSCP field).

→ 현실 = best-effort + 위 layer 의 보장. *단순함의 승리*.

---

## §2 Router 의 *내부 구조*

```
       Input ports → Switching Fabric → Output ports
            ↑                                  ↓
            ←────── Routing Processor ─────────
                    (control plane)
```

![Figure 4.4 — Router 내부 구조 (architecture). 책 p.311](/courses/networking/figures/ch04/fig-4-4.png)

> 직관: 윗부분(routing processor)이 *control plane*(software, ms~s), 아랫부분(input port·switch fabric·output port)이 *data plane*(hardware, ns). packet 은 아래쪽 고속 경로로만 흐르고, 경로 계산은 위에서 따로 일어난다.

### §2.1 Input port

3 단계 처리:

![Figure 4.5 — Input port 처리 단계. 책 p.314](/courses/networking/figures/ch04/fig-4-5.png)

> 직관: line termination(신호→bit) → link 처리(decapsulation) → *lookup·forwarding·queuing*. 마지막 단계의 forwarding table lookup 이 longest prefix match 로 출력 port 를 정하는 핵심이며, line-speed 를 맞추려 TCAM 으로 한다.

1. **Physical layer** — Line termination, signal → bit
2. **Link layer** — Frame parsing, bit → frame (Ethernet, PPP, SONET)
3. **Network layer (forwarding)** — Destination IP 추출 → table lookup → output port

**Longest prefix match (LPM)** — 예:

| Prefix | Output port |
|--|--|
| 11001000 00010111 00010000 / 21 | 0 |
| 11001000 00010111 00011000 / 24 | 1 |
| 11001000 00010111 00011000 00111100 / 32 | 2 |
| 그 외 | 3 |

Destination `11001000 00010111 00011000 10101010` 입력:
- /21 match: OK
- /24 match: OK (더 길음)
- /32 match: no
- Longest = /24 → port **1**

*Why longest 우선*: more specific = more accurate. /24 = 256 IP, /32 = single IP — 더 specific 우선.

**LPM 구현**:
- **TCAM** (Ternary CAM): 0/1/X. *parallel lookup*, 1 ns 단위, 100 Gbps line 처리. 비싸지만 *고정 latency*.
- **Multi-bit trie**: software/ASIC. 메모리 trade-off.

### §2.2 Switching fabric

3 가지 방식:

![Figure 4.6 — Switching fabric 3 방식. 책 p.317](/courses/networking/figures/ch04/fig-4-6.png)

> 직관: *memory*(CPU 경유, 1세대) → *bus*(공유 버스, 한 번에 1 packet) → *crossbar/interconnection*(N×N, 서로 다른 입출력 쌍 동시 전송). 위로 갈수록 병렬도가 높아 Tbps 가 가능하다.

**1. Memory (1st gen)**:
- Input → CPU → memory write → output read
- *CPU bandwidth* bottleneck (한 packet 씩)
- 옛 router. 현대 X.

**2. Bus (2nd gen)**:
- 단일 bus
- Bus bandwidth 가 N × line rate
- 한 시점 one packet
- 중급 router

**3. Crossbar / interconnect (3rd gen)**:
- N × N matrix — N input × N output 의 cross-point
- *Parallel* — 다른 input-output 쌍 동시 전송
- Tbps. High-end.
- 단점: **Head-of-line blocking (HOL)**
- 해결: *Virtual Output Queues (VOQ)* — input 이 *output 별 queue*

**Switching speedup**:
- Fabric speed / line rate. *2~4x speedup* 일반.

### §2.3 Output port

Tasks:
1. Switching fabric 에서 수신
2. **Queueing** (output buffer)
3. **Scheduling** (어느 packet 부터)
4. Link layer + physical layer 로 전송

Buffer 가득 차면 → *packet drop* (loss 의 주 원인).

### §2.4 Buffer 크기 의 변천 — Bufferbloat

![Figure 4.10 — Bufferbloat — 가시지 않는 queue. 책 p.324](/courses/networking/figures/ch04/fig-4-10.png)

> 직관: buffer 가 *너무 크면* TCP 가 그것을 가득 채울 때까지 cwnd 를 키워, queue 가 *늘 차 있는* 상태(b)가 된다 → 모든 흐름의 RTT 가 수백 ms 로 폭증. 해결은 *작은 buffer* + AQM(CoDel).

**고전 rule**:
$$B = RTT \cdot C$$
(RTT × link capacity = BDP).

1990s 의 결정 — *internet 의 BDP* 만큼 buffer.

**문제 — bufferbloat (2010~)**:
- Buffer 가 크면 queueing delay 큼
- TCP 가 *buffer full 까지 cwnd 증가* → 큰 RTT → 모든 connection 느려짐
- Home router 의 *수 초 delay*

**현대 권장**:
$$B = \frac{RTT \cdot C}{\sqrt{N}}$$
(N flows. Stanford 2004 의 *small buffer*). 수십 MB → 수 MB.

**AQM (Active Queue Management)**:
- **RED** (Random Early Detection, 1993) — buffer 차기 전 probabilistic drop
- **CoDel** (Controlled Delay, 2012) — *delay 기반* drop
- **PIE** (Proportional Integral Enhanced)
- **FQ-CoDel**, **CAKE** — fair queueing + CoDel

Linux default: FQ-CoDel.

### §2.5 Scheduling discipline

| 방식 | 동작 | 특징 |
|--|--|--|
| FIFO | First-in, first-out | 단순. Fairness 없음 |
| Priority queueing | High class 우선 | Low class starvation 위험 |
| Round Robin | 번갈아 | Fair |
| WFQ | Weight 비례 | 산업 표준 |
| Fair Queueing | Per-flow round-robin | 이상적 fair, 구현 복잡 |

---

## §3 IPv4 datagram

### §3.1 IPv4 header (20+ byte)

![Figure 4.17 — IPv4 datagram 형식. 책 p.331](/courses/networking/figures/ch04/fig-4-17.png)

> 직관: 20 byte 고정부 + 옵션. *Identifier·Flags·Fragmentation offset* 가 fragment 재조립을, *TTL* 이 loop 방지를, *Upper-layer protocol* 이 TCP(6)/UDP(17) 구분을 맡는다. checksum 은 header 만 보호한다.

```
| Version(4) | HL(4)  | DSCP(6) | ECN(2) | Total Length (16) |
| Identification (16)            | Flags(3) | Fragment Offset (13) |
| TTL (8)                | Protocol(8)     | Header Checksum(16)  |
| Source IP (32)                                                  |
| Destination IP (32)                                             |
| Options (variable)                                              |
| Data                                                            |
```

| Field | 의미 |
|--|--|
| Version | 4 (IPv4), 6 (IPv6) |
| HL | Header length (32-bit words). 5 = 20 byte |
| DSCP/ECN | QoS marking |
| Total Length | Header + data, max 65535 byte |
| Identification | Fragment 묶음 ID |
| Flags | DF (Don't Frag), MF (More Frags) |
| Fragment Offset | Fragment 의 위치 (8-byte unit) |
| TTL | Time-to-live. Hop 마다 -1, 0 = drop |
| Protocol | TCP=6, UDP=17, ICMP=1 |
| Checksum | Header 만 (data 는 TCP/UDP) |
| Src/Dst IP | 양 끝 IP |

**Checksum 약점**:
- Header 만 보호 (data 는 TCP/UDP)
- Hop 마다 재계산 (TTL 변경)
- IPv6 는 폐지

### §3.2 Fragmentation

**문제**: 각 link 의 *MTU* 다름.

| Link | MTU |
|--|--|
| Ethernet | 1500 |
| PPPoE (DSL) | 1492 |
| 802.11 (WiFi) | 2304 |
| FDDI | 4352 |
| Jumbo frame | 9000 |

큰 datagram → 작은 MTU link 통과 → *fragment*.

**예** — 4000 byte datagram (header 20 + data 3980) 가 MTU 1500 link 통과:
- Frag 1: 20 + 1480 byte data, offset 0, MF=1, ID=X
- Frag 2: 20 + 1480 byte data, offset 185 (=1480/8), MF=1, ID=X
- Frag 3: 20 + 1020 byte data, offset 370, MF=0, ID=X

**Reassembly**:
- Same ID 의 fragment 모음
- Offset 으로 순서
- All received + MF=0 → reassemble

**문제점**:
- Reassembly timeout → 일부 loss = 전체 drop
- 공격 surface (Teardrop, Ping of Death)

**현대 — Path MTU Discovery (PMTUD)**:
- DF=1 + large packet
- 중간 router 가 *MTU exceed* → ICMP "fragmentation needed"
- Sender 가 *작은 size* 로 재전송
- *Fragmentation 회피*

**IPv6**: router 는 fragment 안 함, endpoint PMTUD 만.

### §3.3 TTL — Time to Live

**의도**: routing loop 시 packet 의 *영원한 순환 방지*.

**동작**:
- Source initial: Linux 64, Win 128, Cisco 255
- Hop 마다 -1
- TTL=0 → drop + ICMP "TTL exceeded"

**활용 — `traceroute`**:
- TTL=1 → first hop 의 ICMP 응답
- TTL=2 → 2nd hop
- TTL=N → destination 의 ICMP "port unreachable"

---

## §4 IPv4 주소체계

### §4.1 주소 구조

32 bit = 4 octet. 표기:
- Dotted decimal: `192.168.1.1`
- Binary: `11000000.10101000.00000001.00000001`

### §4.2 Subnet + CIDR

![Figure 4.20 — 3 router 가 잇는 6 subnet. 책 p.337](/courses/networking/figures/ch04/fig-4-20.png)

> 직관: subnet 은 *router 를 거치지 않고* 서로 직접 닿는 interface 들의 묶음(같은 prefix). router interface 마다 다른 subnet 에 속하므로, 그림의 6개 "섬"이 각각 하나의 subnet 이다.

`192.168.1.0/24`:
- First 24 bits = network ID = `192.168.1`
- Last 8 bits = host ID = `0~255`
- /24 = mask `255.255.255.0`
- Range: `.0 ~ .255`
- Usable host: `.1 ~ .254` (.0 = network, .255 = broadcast)

**CIDR notation** (RFC 1519, 1993):
- `a.b.c.d/x`
- 임의 prefix length

### §4.3 Class → CIDR 의 역사

**원래 (1970s)**:

| Class | Prefix | 범위 | Network 수 | Host 수 |
|--|--|--|--|--|
| A | 0xxxxxxx | 0~127 | 128 | 16M |
| B | 10xxxxxx | 128~191 | 16K | 65K |
| C | 110xxxxx | 192~223 | 2M | 254 |
| D | 1110xxxx | 224~239 | (multicast) | |
| E | 1111xxxx | 240~255 | (reserved) | |

**문제**: 1000 host 필요 → C 부족, B 낭비. 1990s *IP 부족 위기*.

**CIDR (1993)** 의 해결:
- 임의 prefix
- 1000 host = /22 (1022 host)
- *Route aggregation* — 여러 prefix → 하나

![Figure 4.21 — 계층적 주소 배정과 route aggregation. 책 p.339](/courses/networking/figures/ch04/fig-4-21.png)

> 직관: ISP 가 고객들의 prefix 를 *하나의 큰 prefix*(200.23.16.0/20)로 묶어 광고 → Internet 의 routing table 이 작아진다. CIDR 이 이 aggregation 을 가능케 한 핵심 이유다.

### §4.4 Special ranges

| Range | 용도 |
|--|--|
| 10.0.0.0/8 | Private (large org) |
| 172.16.0.0/12 | Private (medium) |
| 192.168.0.0/16 | Private (home/small) |
| 127.0.0.0/8 | Loopback |
| 169.254.0.0/16 | Link-local |
| 224.0.0.0/4 | Multicast |
| 0.0.0.0/0 | Default route |
| 255.255.255.255 | Limited broadcast |

**Private addresses (RFC 1918)**:
- Internet 에 *routable 아님*
- NAT 으로 public IP 변환

### §4.5 IP 할당의 hierarchy

1. **IANA** — 최상위
2. **RIR** — 지역
   - ARIN (북미), RIPE (유럽), APNIC (아태), LACNIC (남미), AFRINIC (아프리카)
3. **ISP**
4. **End user**

**IPv4 고갈**:
- IANA 완전 고갈: *2011-02-03*
- 각 RIR 도 차례 고갈
- 거래시장 — 1 IP ≈ $30~50 (2025)
- *IPv6 필요성*

---

## §5 DHCP — Dynamic Host Configuration Protocol

### §5.1 4-step handshake (DORA)

```
Client (no IP)             DHCP Server (192.168.1.1)
       |
       | DHCP Discover (broadcast 255.255.255.255)
       |--------->
       |
       | DHCP Offer (192.168.1.50, lease 24h, ...)
       <---------|
       |
       | DHCP Request (I want 192.168.1.50)
       |--------->
       |
       | DHCP ACK
       <---------|
       |
   (192.168.1.50 사용)
```

### §5.2 DHCP 제공 정보

- IP address (with lease)
- Subnet mask
- Default gateway
- DNS server
- NTP, domain name 등

### §5.3 Lease + renewal

- 기본 24h (home), 8h (enterprise), 30 min (public WiFi)
- 50% 시점에 *재요청*
- Fail 시 87.5% 에 broadcast renew

### §5.4 DHCP 의 취약점

- **Rogue DHCP** — fake gateway → MITM
- **DHCP starvation** — IP 소진
- 방어: *DHCP snooping* (switch level)

---

## §6 NAT — Network Address Translation

### §6.1 NAT 의 *왜*

문제: IPv4 부족. 가정/회사 모든 device 에 public IP 불가.
해결: *private ↔ public* 변환.

### §6.2 동작

**Topology**:
```
Home (192.168.1.0/24)             Internet
                                     |
192.168.1.10 ─┐                     |
192.168.1.11 ─┼─→ [NAT] ←──→ 1.2.3.4 (public)
192.168.1.12 ─┘
```

**Outbound** (`192.168.1.10:5000` → `google.com:443`):
1. NAT table 매핑 추가: `(192.168.1.10:5000) ↔ (1.2.3.4:60001)`
2. Packet 수정: src=`1.2.3.4:60001`
3. Internet 으로

**Inbound** (`google.com:443` → `1.2.3.4:60001`):
1. NAT lookup: 60001 → `192.168.1.10:5000`
2. Packet 수정: dst=`192.168.1.10:5000`
3. Home 으로

→ 하나의 public IP 로 수천 internal device.

### §6.3 NAT 의 논쟁

**찬성**:
- IPv4 생명연장
- 부가 보안 (internal device direct access 불가)
- 유연성

**반대**:
- *End-to-end principle 위반*
- *P2P 깨짐* (양쪽 NAT 시)
- *Protocol incompatibility* (SIP, FTP, IPsec)
- STUN/TURN/ICE 같은 *NAT traversal* 필요

### §6.4 NAT traversal

**STUN** — Session Traversal Utilities:
- STUN server (`stun.l.google.com:19302`) 에 query
- *External addr* 응답 → public IP/port 인식

**TURN** — Traversal Using Relays:
- *Symmetric NAT* (server 마다 다른 port) 시
- Relay server 가 중계
- Bandwidth 비용 ↑

**ICE** — Interactive Connectivity Establishment:
- STUN + TURN + candidate 선택
- WebRTC 의 기본 signaling
- 가능 하면 직접, 안되면 relay

### §6.5 Carrier-Grade NAT (CGN)

- ISP 가 고객 사이 NAT
- *Double NAT* (가정 + ISP)
- Mobile network 의 기본
- Deep P2P, hosting 의 치명적 영향
- *IPv6 가 유일한 해결*

---

## §7 IPv6

### §7.1 왜 만들었나

1. **IPv4 부족** — $2^{32} \approx 4 \times 10^9$. IoT 시대 부족.
2. **Header 개선** — fragmentation 단순화, checksum 제거.
3. **새 기능** — IPsec built-in, flow label, multicast 표준화.

### §7.2 IPv6 header (40 byte, fixed)

![Figure 4.26 — IPv6 datagram 형식. 책 p.349](/courses/networking/figures/ch04/fig-4-26.png)

> 직관: 40 byte *고정* header — IPv4 의 fragmentation·checksum·options 를 본체에서 걷어내 router 처리를 단순·고속화했다. *Flow label* 로 흐름을 식별하고, 부가 기능은 extension header 로 뺀다.

```
| Version(4)| Traffic Class(8) | Flow Label (20)         |
| Payload Length (16)| Next Header(8) | Hop Limit (8)    |
| Source IP (128)                                        |
| Destination IP (128)                                   |
```

| | IPv4 | IPv6 |
|--|--|--|
| Header 크기 | 20+ (variable) | 40 (fixed) |
| Header field | 12+ | 8 |
| Address | 32 bit | 128 bit |
| Fragmentation | router | endpoint only |
| Checksum | yes | no |
| Options | header field | extension header |
| Broadcast | yes | no (multicast 만) |

### §7.3 IPv6 주소 표기

128 bit = 8 group × 16 bit hex:

`2001:0db8:85a3:0000:0000:8a2e:0370:7334`

**축약**:
1. Leading 0 생략: `2001:db8:85a3:0:0:8a2e:370:7334`
2. *연속 0* 을 `::` (한 번만): `2001:db8:85a3::8a2e:370:7334`

**주요 prefix**:
| Prefix | 용도 |
|--|--|
| `::1` | Loopback |
| `fe80::/10` | Link-local |
| `fc00::/7` | Unique local (private) |
| `2000::/3` | Global unicast |
| `ff00::/8` | Multicast |

**128 bit** = $2^{128} \approx 3.4 \times 10^{38}$. 사실상 무한.

### §7.4 IPv6 전환 의 느림

**문제**: *backwards compatibility 없음*. IPv4 ↔ IPv6 직접 통신 X.

**전환 전략**:

1. **Dual stack** — host 가 IPv4 + IPv6 동시 지원
   - DNS 가 A (v4) + AAAA (v6) 반환
   - *Happy eyeballs* — 둘 다 시도, 빠른 쪽

2. **Tunneling** — IPv6 packet 을 IPv4 안에 (6to4, Teredo, 옛)

![Figure 4.27 — Tunneling — IPv6 를 IPv4 로 감싸기. 책 p.352](/courses/networking/figures/ch04/fig-4-27.png)

> 직관: IPv6 섬(A·B / E·F) 사이에 IPv4 구간(C·D)이 있으면, B 가 IPv6 packet 을 *IPv4 packet 안에 통째로 넣어*(encapsulate) 보내고 끝(E)에서 꺼낸다 — 전환기의 핵심 기법.

3. **Translation (NAT64)** — IPv6 ↔ IPv4 변환

**Adoption 진행도** (Google IPv6 stats, 2025):
- Global: ~45%
- India: 70%
- US: 50%
- Korea: 12%

→ *25 년* 도 전환 미완. Internet 변화 속도 의 사례.

---

## §8 ICMP — Internet Control Message Protocol

### §8.1 ICMP 의 역할

IP 가 best-effort — error 알릴 수단. ICMP = *error + diagnostic*.

ICMP 는 IP *위 layer* — TCP/UDP 와 같은 level. Protocol number = 1.

### §8.2 ICMP message type

| Type | Code | 의미 |
|--|--|--|
| 0 | 0 | Echo reply (ping reply) |
| 3 | 0 | Net unreachable |
| 3 | 1 | Host unreachable |
| 3 | 2 | Protocol unreachable |
| 3 | 3 | Port unreachable |
| 3 | 4 | Fragmentation needed (PMTUD) |
| 8 | 0 | Echo request (ping) |
| 11 | 0 | TTL expired |
| 12 | 0 | IP header bad |

### §8.3 `ping`

1. Source → ICMP Echo Request (type 8)
2. Destination → ICMP Echo Reply (type 0)
3. Source RTT 측정

활용: 연결 확인, latency, loss rate.

### §8.4 `traceroute` — TTL trick

1. UDP/ICMP packet TTL=1 → first hop 의 *TTL expired*
2. TTL=2 → 2nd hop 응답
3. ...
4. TTL=N (destination) → *port unreachable* 응답 (no UDP service)

```
traceroute google.com:
 1  192.168.1.1     1ms
 2  10.50.0.1       5ms  (ISP)
 3  211.0.0.1       15ms
 4  72.14.196.0     20ms (Google)
```

### §8.5 ICMP 보안

- **Ping flood** — DoS
- **Ping of Death** — oversized (옛)
- **Smurf attack** — broadcast + spoof
- **ICMP tunnel** — covert channel

→ 많은 enterprise 가 *ICMP block*. 단 PMTUD 깨짐.

---

## §9 Generalized forwarding + SDN

### §9.1 Traditional 의 한계

Destination-based forwarding — *dst IP 만* 으로 결정.

한계:
- Multi-criteria 불가 (source-based 등)
- Load balancing 어려움
- Service-specific policy 어려움
- Vendor 마다 다른 CLI

### §9.2 Match + Action

일반화: forwarding = `match (any field) → action (any operation)`.

**Match field**:
- IP src/dst
- TCP/UDP port
- VLAN tag
- MAC address
- Ingress port

**Action**:
- Forward to port
- Drop
- Modify header
- Send to controller
- Encapsulate

### §9.3 OpenFlow (2008)

![Figure 4.30 — OpenFlow match-action network (switch 3·host 6·controller). 책 p.357](/courses/networking/figures/ch04/fig-4-30.png)

> 직관: 중앙 *OpenFlow controller* 가 각 switch 의 flow table(match→action)을 채운다. switch 는 dst IP 만 보는 게 아니라 *임의 header field 를 match* 해 forward/drop/modify — destination 기반 forwarding 의 일반화다.

```
[OpenFlow Controller]
       |
       | OpenFlow protocol (TCP 6653)
   ┌───┴───┐
[OF Switch] [OF Switch]
```

**Flow table entry**:
| Match | Counter | Action |
|--|--|--|
| dst MAC = AA:BB:CC, in_port = 1 | (count) | Forward port 2 |
| TCP dst port = 80 | | Send to controller |
| (no match) | | Drop |

**Controller**:
- 모든 switch 의 forwarding 정책 중앙 결정
- Topology discovery
- Path computation
- Policy

### §9.4 P4 — programmable parser

OpenFlow 한계: *fixed header parsing*.

**P4** (2014):
- Switch 의 *parser 자체* 프로그램 가능
- 새 protocol hardware 지원
- *Barefoot Tofino* chip — line rate P4

→ SDN 의 완성.

### §9.5 산업의 SDN

| 회사 | 적용 |
|--|--|
| Google B4 | Datacenter 간 backbone, link utilization 95% (vs 30~40% traditional) |
| Facebook Fabric | Datacenter 내부, spine-leaf |
| Microsoft Azure | Datacenter SDN |
| Cisco Viptela | SD-WAN |
| VMware NSX | Datacenter overlay |

---

## §10 Middlebox 의 *논쟁*

**Middlebox** = network layer functionality 확장 device.

종류:
- NAT
- Firewall
- IDS / IPS
- Load balancer
- WAN optimizer
- Proxy (HTTP, SOCKS)
- DPI (Deep Packet Inspection)

**현실**:
- 어떤 Internet path 든 *수~수십 middlebox* 통과
- 단순 router-only path 거의 없음

**End-to-end principle 와 충돌**:
- Saltzer-Reed-Clark (1984): *복잡 기능은 endpoint, network 은 simple*
- Middlebox 가 이 원칙 위반
- *Network ossification* — 새 protocol deploy 어려움

**예 — QUIC**:
- 모든 정보 encrypted
- Middlebox 가 internal field 못 봄
- 일부 기업 *QUIC block* — HTTP/3 deploy 어려움

→ Internet evolution 의 가장 큰 장벽.

![Figure 4.31 — Internet 의 hourglass — IP 라는 좁은 허리. 책 p.362](/courses/networking/figures/ch04/fig-4-31.png)

> 직관: 위(application·transport)도 아래(link·physical)도 다양하지만, 가운데는 *오직 IP* 하나로 좁다. 이 "narrow waist" 덕에 양쪽이 독립적으로 진화했지만, 동시에 IP 를 바꾸기 어렵게(ossification) 만든 이유이기도 하다.

---

## §11 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Router = layer 3 만 | 현대 router 는 layer 4~7 까지 (firewall, NAT, DPI) |
| Routing = forwarding | Routing 은 경로 계산 (control), forwarding 은 packet 처리 (data) |
| IP = reliable | IP 는 best-effort. TCP 가 reliable 보장 |
| NAT = security | NAT 은 부가 보안. Firewall 이 진짜 |
| IPv6 = IPv4 확장 | 별도 protocol. backwards compatible 아님 |
| Subnet mask = optional | 없으면 forwarding 불가 — network/host 구분 필수 |
| TTL = seconds | *Hop count*. 이름이 misleading |
| Public IP = secure | 노출. firewall + NAT 가 보호 |

---

## §12 자가점검

1. Forwarding 과 routing 의 차이?
2. Router 의 4 component + 역할?
3. Longest prefix match 의 원리?
4. Switching fabric 의 3 방식 + 차이?
5. IPv4 header 의 주요 field?
6. Fragmentation 동작 + 문제점?
7. CIDR 가 *왜* 만들어졌나?
8. DHCP 의 DORA 절차?
9. NAT 의 동작 + 장단점?
10. IPv6 의 *왜* + 전환 의 *느림 원인*?
11. ICMP 의 ping + traceroute 동작?
12. OpenFlow 의 match-action paradigm?

<details><summary>모범 답</summary>

1. Forwarding = 한 router 내 packet 처리 (data plane, ns). Routing = 전체 경로 계산 (control plane, ms~s).
2. Input port (forwarding 결정) / Switching fabric (input → output) / Output port (queueing + scheduling) / Routing processor (control).
3. Forwarding table 의 entry 중 dst 와 *가장 길게 match* 하는 prefix 의 action 적용.
4. (a) Memory — CPU 중계, 느림. (b) Bus — 단일 bus, one packet. (c) Crossbar — N×N matrix, parallel, HOL → VOQ.
5. Version / HL / Total Length / ID + Flags + Offset / TTL / Protocol / Checksum / Src + Dst IP.
6. 큰 datagram 이 작은 MTU link 통과 시 자름. ID 로 묶고 offset 으로 reassembly. 문제: 한 fragment loss = 전체 drop, attack surface. → PMTUD + IPv6 의 endpoint-only.
7. Class A/B/C 의 낭비 + 부족 해결. 임의 prefix length 로 정확한 크기, route aggregation.
8. Discover (broadcast) → Offer → Request → Ack. Lease + renewal.
9. Private ↔ public IP+port 변환. 장: IP 부족 해결, 부가 보안. 단: end-to-end 깨짐, P2P + 일부 protocol 깨짐, STUN/TURN 필요.
10. (a) IPv4 부족, (b) header 단순화. 전환 느림: backwards compat 없음, dual stack 비용, 변경 동력 약함.
11. Ping: Echo Req ↔ Echo Reply, RTT. Traceroute: TTL=1, 2, ... 으로 각 hop 의 TTL expired 받음.
12. Match (any field) → Action (any operation). Controller 중앙 결정. Programmable network.

</details>

---

## §13 다음 학습으로

- **5장 (Network Layer: Control Plane)** — 이 장의 forwarding table 을 *누가 채우나*. OSPF·BGP routing, SDN controller
- **6장 (Link Layer)** — IP datagram 을 한 hop 씩 나르는 *frame*. ARP 가 IP↔MAC 를 잇는다
- **3장 되돌아보기** — NAT·fragmentation 이 TCP/QUIC 에 주는 *실제 영향*

> *Tools to try*: `traceroute`(hop별 TTL), `ip route`/`netstat -rn`(forwarding table), 받은 IP를 `whois`로 prefix 확인, `tcpdump`로 fragment 관찰

---

## §14 한 줄 요약

> **Data plane = router 내부 의 *packet 처리* (forwarding table lookup, switching fabric, queueing). IPv4 = best-effort + NAT + DHCP 의 *실제 운영*. IPv6 = next-gen 의 *느린 전환*. SDN = data + control plane 분리 — programmable network 의 미래.**
