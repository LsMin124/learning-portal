# Ch 6 Link Layer and LANs

> Kurose & Ross 의 Ch 6. *Network layer 의 한 hop 아래* — link 의 *frame 단위 통신*. 같은 *physical medium* 의 *neighbor 간 데이터 전달*.

---

## §0 도입 — *마지막 한 hop, 같은 선을 나눠 쓰는 법*

> **핵심 한 문장**: network layer 가 "어느 router 로?"를 풀었다면, link layer 는 *바로 옆 노드까지* datagram 을 frame 에 담아 실제 *물리 매체* 위로 보내는 일 — 그리고 그 매체를 여럿이 *공유* 할 때 누가 언제 말할지를 정하는 *multiple access*(§3)가 6장의 심장이다.

먼저 link 가 주는 service(framing·error detection·신뢰성)와 CRC 같은 *오류 검출*(§2)을 본다. 그다음 핵심 난제 — 한 선을 여럿이 쓰면 충돌한다 — 를 푸는 *multiple access protocol*: 유선의 CSMA/CD 와 무선의 CSMA/CA 가 *왜 갈라지는지* 가 7장 wireless 로 이어진다.

실세계의 LAN 은 *Ethernet + switch*(§5)다. switch 의 self-learning·MAC table, 그리고 ARP(§4)가 IP↔MAC 를 잇는다. *VLAN*(§6)·*MPLS*(§7)는 이 LAN 을 논리적으로 쪼개고 빠르게 forwarding 하는 진화다.

마지막 *datacenter networking*(§8, spine-leaf)은 server↔server 의 east-west 트래픽을 위한 현대 LAN 의 극한으로, 클라우드 인프라의 바닥을 이룬다.

---

## 들어가기 전에

- **선수 지식**: 4~5장(IP datagram, forwarding), 2진수·다항식 나눗셈(CRC) 기초, 1장 encapsulation
- **학습 목표**
  1. **Link layer 의 역할** — framing·error detection·multiple access
  2. **Error detection** — parity·checksum·CRC
  3. **Multiple access protocols** — 공유 medium 의 충돌 회피
  4. **LAN** — Ethernet·switch·ARP·VLAN
  5. **MPLS** — link 와 network layer 사이
  6. **Datacenter networking** — spine-leaf, east-west
- **예상 학습 시간**: 150~200분

---

## §1 Link layer 의 *역할*

![Figure 6.1 — wireless host 와 server 사이 6개 link-layer hop. 책 p.451](/courses/networking/figures/ch06/fig-6-1.png)

> 직관: 한 통신 경로는 *서로 다른 link*(WiFi·Ethernet·광)들의 연속이다. 각 hop 마다 link layer 가 datagram 을 그 link 에 맞는 frame 으로 새로 감싸 다음 노드로 넘긴다.

Network layer 의 datagram 은 *수많은 link* 거침:
- Host → router 1 — Ethernet
- Router 1 → router 2 — 광섬유 (SONET)
- Router 2 → router 3 — 위성
- ...
- Router N → host — WiFi

**각 link 마다**:
- Frame 으로 datagram 감쌈
- Medium 위 전송
- Error detect (+ correct)
- Neighbor 의 medium 접근 조율

**Link layer service**:
1. **Framing**
2. **Link access** — medium 공유 시 누가 transmit
3. **Reliable delivery** (option)
4. **Error detection + correction**

### §1.1 Link 종류

| Type | 의미 |
|--|--|
| Point-to-point | 두 endpoint만 (PPP, SONET) |
| Broadcast | 공유 medium (Ethernet, WiFi) |

### §1.2 구현 위치

- **NIC** (Network Interface Card) 의 hardware
- Frame parsing, error check, MAC addressing
- *CPU 일* 최소화 — line rate

---

## §2 Error detection

### §2.1 *왜* 필요

Link 의 physical medium 이 *완벽 아님*:
- 광섬유 — < $10^{-15}$ BER
- 동선 — $10^{-9}$ BER
- 무선 — $10^{-3} \sim 10^{-6}$ BER

→ Frame 에 error detection code 부착.

### §2.2 Parity bit

**Single parity**:
- 1 개 추가, *bit 1 개수* 가 *짝수* 되게
- 1 bit error 검출
- 2 bit error — *cancel out* 으로 미검출

**2-D parity**:
- Matrix 의 row + column parity
- 1 bit error — 위치 + correction
- 2 bit error — 검출만

### §2.3 Internet checksum

- 16-bit one's complement sum
- Software 빠름
- 보호 약함

### §2.4 CRC

![Figure 6.6 — CRC. 책 p.459](/courses/networking/figures/ch06/fig-6-6.png)

> 직관: 데이터 D 뒤에 r비트 CRC R 을 붙여, 전체 `D·2^r XOR R` 가 생성 다항식 G 로 *나누어떨어지게* 만든다. 수신측이 G 로 나눠 나머지가 0 이 아니면 오류 — burst error 검출에 강하다.

**원리**:
- Frame data $D$ 와 generator $G$ 의 나눗셈
- *나머지* 가 CRC bit
- Receiver 가 $D + CRC$ 를 $G$ 로 나눠 *나머지 0* 인지

**예**:
- $D = 101110$, $G = 1001$
- $D \cdot 2^3 = 101110000$
- $101110000 \div 1001$ = remainder $011$
- Frame = $101110011$

**Property**:
- r-bit CRC 는 r bit burst error 모두 검출
- 2 bit error 검출 (잘 설계된 G)
- Long burst 도 확률적 검출

**표준**:
- CRC-32 (Ethernet, ZIP) — 4 byte
- CRC-CCITT (HDLC) — 2 byte
- CRC-16 (Modbus, USB) — 2 byte

### §2.5 FEC — Forward Error Correction

- *Error 발생 시 receiver 가 복원*
- Hamming, Reed-Solomon, LDPC, Turbo
- 30~50% overhead
- *Loss-sensitive* link (위성, 무선, optical)

**산업**:
- 4G/5G — LDPC
- DVD/CD — Reed-Solomon
- WiFi — convolutional + Viterbi

---

## §3 Multiple access protocols

### §3.1 *문제*

공유 medium 에 여러 노드 동시 송신 → **충돌**.

→ MAC (Medium Access Control) 이 *누가 언제 송신* 결정.

### §3.2 *3 부류*

![Figure 6.8 — 다양한 multiple access 채널. 책 p.462](/courses/networking/figures/ch06/fig-6-8.png)

> 직관: 케이블(shared wire)·WiFi(shared wireless)·위성, 심지어 *칵테일 파티* 까지 — 하나의 매체를 여럿이 나눠 쓰는 모든 상황이 같은 문제다: "누가 언제 말할 것인가".

**1. Channel partitioning** — 시간/주파수/code 나눔. 충돌 없음, 효율 ↓.
**2. Random access** — 충돌 허용 + 재전송. 효율 ↑ (light), 불안정 (heavy).
**3. Taking turns** — Token / polling. Predictable, 복잡.

### §3.3 Channel partitioning

**TDMA**: 시간 slot. (2G GSM)
**FDMA**: 주파수 band. (위성, 무선)
**CDMA**: Unique code, 모두 동시. (3G, GPS)

### §3.4 ALOHA

**Pure ALOHA** (Hawaii, 1971):
- 원할 때 송신, 충돌 시 random delay 후 재시도
- Max throughput = $1/(2e) \approx 0.18$

**Slotted ALOHA**:
- Slot 안에서만 송신 시작
- Max throughput = $1/e \approx 0.37$

### §3.5 CSMA

![Figure 6.13 — CSMA/CD (collision detection). 책 p.472](/courses/networking/figures/ch06/fig-6-13.png)

> 직관: 두 노드가 *동시에* 보내 신호가 겹치면(space-time 다이어그램의 교차), 전송 중 들으며 충돌을 *감지하는 즉시 중단*(abort)한다 — 유선의 full-duplex 청취가 가능해 CSMA/CD 가 성립한다.

**CSMA**: 송신 전 carrier sense.

**CSMA/CD** (Collision Detection):
- 송신 *중* 충돌 감지
- 충돌 즉시 송신 중단
- Ethernet (옛 hub 시대)

**CSMA/CA** (Collision Avoidance):
- 충돌 감지 불가 (무선)
- RTS/CTS 예약
- WiFi

### §3.6 Binary exponential backoff

```
n = 0
while collision:
    wait random(0, 2^n - 1) slot times
    n = min(n + 1, 10)
    transmit
n=16 → give up
```

**Slot time**:
- Ethernet 10 Mbps: 51.2 μs
- Ethernet 100 Mbps: 5.12 μs
- Ethernet 1 Gbps: 4.096 μs

### §3.7 Taking turns

**Token ring** (옛, IEEE 802.5): token 순환.
**Polling** (Bluetooth, master-slave): master 가 slave query.

현대: switched Ethernet + centralized WiFi AP = *random access + 중앙 조율*.

---

## §4 LAN addressing — MAC

### §4.1 MAC address

- **48 bit** = 6 byte
- *Globally unique*
- 예: `00:1A:2B:3C:4D:5E`
- *Hardware burned*

**Format**:
- First 24 bit = OUI (vendor)
- Last 24 bit = NIC serial

**Special**:
- `FF:FF:FF:FF:FF:FF` = broadcast
- `01:00:5E:...` = IPv4 multicast
- `33:33:...` = IPv6 multicast

### §4.2 IP vs MAC

![Figure 6.17 — LAN 의 각 interface 는 IP + MAC 둘 다 가진다. 책 p.481](/courses/networking/figures/ch06/fig-6-17.png)

> 직관: 모든 adapter 는 *MAC 주소*(link layer, 영구)와 *IP 주소*(network layer, 위치)를 동시에 가진다. 같은 subnet 안 통신은 MAC 으로, subnet 을 넘으면 router 가 IP 로 중계한다.

| | IP | MAC |
|--|--|--|
| Layer | Network | Link |
| Scope | Global | Local link |
| 길이 | 32/128 bit | 48 bit |
| 할당 | DHCP, manual | Hardware fixed |
| 변경 | OK | Fixed (대부분) |

비유: IP = 집 주소, MAC = 방번호.

### §4.3 ARP

**Task**: IP → MAC 변환 (같은 LAN 내).

**예** — `192.168.1.10` → `192.168.1.20`:
1. ARP cache 확인 → 없음
2. ARP request broadcast: "192.168.1.20 의 MAC?"
3. `192.168.1.20` ARP reply: "AA:BB:CC:DD:EE:FF"
4. Cache 추가, frame 송신

**Cache entry**: IP — MAC, TTL (수 분), Type (static/dynamic).

### §4.4 ARP 보안

**ARP spoofing**:
- Attacker 가 가짜 ARP reply broadcast
- "Gateway MAC = 내 MAC"
- MITM

**방어**:
- Static ARP (특정 device)
- DHCP snooping + Dynamic ARP Inspection (DAI)
- 802.1X authentication
- VPN

---

## §5 Ethernet

### §5.1 *Dominant LAN* 의 역사

| 시기 | 명칭 | Speed |
|--|--|--|
| 1973 | Xerox PARC | 2.94 Mbps |
| 1980 | DIX | 10 Mbps |
| 1983 | 802.3 | 10 Mbps |
| 1995 | Fast Ethernet | 100 Mbps |
| 1998 | Gigabit | 1 Gbps |
| 2002 | 10 GbE | 10 Gbps |
| 2010 | 40, 100 GbE | |
| 2020 | 400 GbE | |
| 2025 | 800 GbE | |

→ 50 년 진화, *800 Gbps* 도달.

### §5.2 Ethernet frame format

![Figure 6.20 — Ethernet frame 구조. 책 p.486](/courses/networking/figures/ch06/fig-6-20.png)

> 직관: Preamble(동기) · Dest/Source MAC · Type(상위 protocol) · Data · CRC. type 으로 IP/ARP 를 구분하고, CRC 로 오류를 검출해 *조용히 버린다*(재전송은 상위 몫).

```
| Preamble (7B) | SFD (1B) | Dst MAC (6B) | Src MAC (6B) |
| EtherType (2B) | Data (46~1500B) | CRC (4B) |
```

- **Preamble**: sync (10101010 7회)
- **SFD**: 10101011
- **EtherType**: 0x0800 (IPv4), 0x0806 (ARP), 0x86DD (IPv6)
- **Data**: 46 byte 미만은 padding
- **CRC-32**

**Min frame**: 64 byte (CSMA/CD slot time)
**Max frame**: 1518 byte (jumbo 9000)

### §5.3 Hub vs Switch

| | Hub | Switch |
|--|--|--|
| Layer | Physical | Link |
| Forward | 모든 port | dst port 만 |
| Duplex | Half | Full |
| Collision | CSMA/CD domain | 없음 |
| Bandwidth | Share | Dedicated |

현대 — switch only. Hub 는 박물관.

### §5.4 Switch self-learning

![Figure 6.23 — switch self-learning (MAC 학습). 책 p.493](/courses/networking/figures/ch06/fig-6-23.png)

> 직관: switch 는 들어온 frame 의 *source MAC + 도착 interface* 를 표에 기록한다. 다음에 그 MAC 이 목적지면 *해당 port 로만* 보내고(아니면 flood), 사람 개입 없이 스스로 표를 채운다.

```
Switch MAC table:
| MAC          | Port | TTL |
|--------------|------|-----|
| AA:BB:CC:01  | 1    | 60s |
| AA:BB:CC:02  | 2    | 50s |
```

**Learning**:
1. Frame in (src=MAC, in_port=X)
2. (MAC, X) 추가
3. Dst lookup — 있으면 그 port, 없으면 broadcast

**Aging**: TTL 후 entry 제거 (default 5 분).

### §5.5 Forwarding 종류

- *Known dst* — 해당 port (unicast)
- *Unknown dst* — flood (except in_port)
- *Broadcast* — flood
- *Multicast* — flood (또는 IGMP snooping)

---

## §6 VLAN

### §6.1 *왜* VLAN

![Figure 6.25 — 2개 VLAN 이 설정된 단일 switch. 책 p.498](/courses/networking/figures/ch06/fig-6-25.png)

> 직관: 한 물리 switch 의 port 들을 *논리 그룹*(EE: 2–8, CS: 9–15)으로 나눠, 같은 장비를 쓰면서도 broadcast domain 을 분리한다 — 부서 격리·보안의 기본.

- 같은 switch 의 모든 port = 같은 broadcast domain
- 큰 회사 — 너무 큰 broadcast
- Department 분리
- Security

→ *논리적 분리*.

### §6.2 802.1Q tagging

![Figure 6.27 — 원본 Ethernet frame(위) vs 802.1Q-tagged frame(아래). 책 p.500](/courses/networking/figures/ch06/fig-6-27.png)

> 직관: VLAN trunk 는 frame 에 4 byte *802.1Q tag*(TPID + VLAN ID 등)를 끼워 "이 frame 이 어느 VLAN 소속"인지 표시한다. 내용이 바뀌므로 CRC 는 재계산된다.

```
| Dst MAC | Src MAC | 802.1Q tag | EtherType | Data | CRC |
                    ↓
| 0x8100 (TPID) | PCP(3) | DEI(1) | VLAN ID (12) |
```

- TPID = 0x8100
- PCP = priority (QoS)
- VLAN ID = 12 bit → 4096 (4094 usable)

### §6.3 Trunk vs Access

| | Access | Trunk |
|--|--|--|
| Frame | Untagged | Tagged (802.1Q) |
| VLAN | 1 만 | 여러 |
| 용도 | Endpoint | Switch↔switch |

### §6.4 Native VLAN

Trunk 의 기본 — untagged frame 의 VLAN.

**보안**: VLAN hopping (이중 tagging) 회피 — native VLAN 을 *사용 안 하는 VLAN* 으로.

### §6.5 산업

- Datacenter — 수천 VLAN
- 4096 한계 → **VXLAN** (16M VLAN, encapsulation)
- Cloud datacenter 표준

---

## §7 MPLS

### §7.1 *왜* MPLS

![Figure 6.28 — MPLS header (link·network layer 사이). 책 p.502](/courses/networking/figures/ch06/fig-6-28.png)

> 직관: MPLS 는 IP header *앞에* 짧은 *label*(+Exp·S·TTL)을 끼운다. router 는 IP longest-prefix 대신 *label* 만 보고 빠르게 forwarding — "2.5 계층"으로 불리는 이유.

- LPM 보다 빠름
- Explicit path (traffic engineering)
- VPN service
- QoS

### §7.2 동작

```
| Ethernet | MPLS label | IP | TCP | Data |
```

**MPLS label** (4 byte):
- Label (20 bit)
- Traffic class (3 bit)
- S (1 bit, stack bottom)
- TTL (8 bit)

**Forwarding**:
- Ingress: IP packet 에 label 부착
- 중간 router: label swap
- Egress: label 제거, IP forwarding

### §7.3 LDP — Label Distribution Protocol

- LSP (Label Switched Path) 설정
- Hop-by-hop label 합의

### §7.4 RSVP-TE

- Operator 의 explicit path 설정
- Bandwidth reservation
- Backup path fallback

### §7.5 산업

- Tier 1 ISP 표준
- MPLS L3VPN
- Traffic engineering

**SD-WAN 대안**:
- MPLS = 비싸고 inflexible
- Internet + SD-WAN = 저렴 + flexible
- Trend — MPLS 줄이고 Internet 늘림

---

## §8 Datacenter networking

### §8.1 극단

| 항목 | 수치 |
|--|--|
| Server | 100,000+ |
| Switch | 1000+ |
| Link | 100~800 Gbps |
| Latency | < 100 μs (within DC) |
| Bandwidth | Tbps |

### §8.2 Topology

![Figure 6.30 — 계층적 topology 의 datacenter network. 책 p.506](/courses/networking/figures/ch06/fig-6-30.png)

> 직관: border→access→tier-1→tier-2→TOR→server racks 의 트리. 하지만 server↔server(east-west) traffic 이 폭증하며 이 전통 트리의 한계가 드러나고, spine-leaf 로 진화하는 동기가 된다.

**Hierarchical** (옛):
- Core → Aggregation → Edge → Server
- Bandwidth oversubscription
- East-west 부족

**Spine-leaf** (현대):
```
Spine ── Spine ── Spine
  X       X       X
Leaf    Leaf    Leaf
  |      |       |
Server Server Server
```

- Every leaf ↔ every spine — 2 hops
- ECMP equal cost
- Horizontal scaling

### §8.3 East-West traffic

- 전통: north-south (client ↔ server) dominant
- 현대: east-west (server ↔ server) = 70~80%
- 이유: microservices, distributed storage, ML training

### §8.4 RDMA

전통 — OS + TCP — 수 μs latency.

**RDMA**:
- NIC 가 직접 memory access
- OS bypass
- Sub-μs latency

**구현**:
- **InfiniBand** — 자체 fabric (HPC)
- **RoCE** — Ethernet 위
- **iWARP** — TCP/IP 위

### §8.5 현대 datacenter

- **Disaggregation** — storage/compute 분리
- **Programmable switch** (P4, Tofino) — in-network computing
- **Optical switching** — low power, high BW
- **SDN** — 중앙 controller

---

## §9 한 페이지의 packet 흐름

`https://google.com` fetch:

### §9.1 단계

![Figure 6.33 — router 로 연결된 3개 subnet. 책 p.523](/courses/networking/figures/ch06/fig-6-33.png)

> 직관: 한 packet 이 출발 host → switch(같은 subnet, MAC) → router(subnet 경계, IP) → … 로 가며, 매 hop 에서 *frame 은 새로 만들어지고 IP datagram 은 유지* 되는 전 과정의 무대다.

1. **DHCP** — 새 device IP (DORA)
2. **ARP** — gateway MAC
3. **DNS query** — `google.com` → IP
4. **TCP handshake** — google IP:443
5. **TLS handshake** — 인증서 + 키
6. **HTTP request/response** — encrypted

### §9.2 각 layer 의 일

| Layer | 추가 정보 |
|--|--|
| Physical | 신호 → bit |
| Link | Ethernet frame + MAC + CRC |
| Network | IP src/dst |
| Transport | TCP port + seq/ack |
| Application | HTTP method + URL + header |

### §9.3 Header overhead

- Ethernet: 18 byte
- IP: 20 byte
- TCP: 20 byte
- TLS: ~30 byte
- HTTP: ~500 byte

→ 600 byte overhead → small data.

→ HTTP/2/3 의 header compression (HPACK, QPACK) 가치.

---

## §10 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Link layer = LAN | Any link (광섬유, 위성, PPP) |
| MAC = IP | MAC = local, IP = global |
| Switch = router | Switch = layer 2 (MAC), Router = layer 3 (IP) |
| Hub = switch | Hub = physical (옛), switch = link (현대) |
| Ethernet = CSMA/CD | 현대 full-duplex switched 안 씀 |
| MPLS = routing | Label switching — IP 위 |
| VLAN 4096 | 실제 4094 (0, 4095 reserved) |
| MAC 변경 불가 | Software MAC spoof 가능 |

---

## §11 자가점검

1. Link layer 의 *4 service*?
2. Parity vs CRC 차이?
3. CSMA/CD vs CSMA/CA 의 *왜* 다른가?
4. ALOHA throughput?
5. MAC address format + scope?
6. ARP 동작?
7. Switch vs hub 차이?
8. VLAN 의 *왜*?
9. MPLS 의 *왜*?
10. Spine-leaf 의 *왜*?

<details><summary>모범 답</summary>

1. Framing / Link access (MAC) / Reliable delivery (option) / Error detection + correction.
2. Parity = 1 bit, 1 error 검출. CRC = polynomial division, r-bit burst 모두 검출.
3. CSMA/CD = wired full-duplex 가능, transmit 중 listen → 충돌 감지. CSMA/CA = wireless full-duplex 안됨 → RTS/CTS 예약.
4. Pure 18%, Slotted 37% (= 1/e).
5. 48 bit, OUI + serial. Local link scope. Hardware burn.
6. IP → MAC. Broadcast request → unicast reply → cache (TTL).
7. Hub = layer 1 broadcast, half-duplex, collision domain. Switch = layer 2 MAC table, full-duplex, dedicated bandwidth.
8. Broadcast domain 분할, dept 분리, security.
9. Label forwarding (LPM 보다 빠름), explicit path, traffic engineering, VPN.
10. East-west traffic (server ↔ server, 70~80%) 의 equal bandwidth. Microservices, distributed system.

</details>

---

## §12 다음 학습으로

- **7장 (Wireless/Mobile)** — CSMA/CA 가 본격화되는 *무선 link*. 802.11 frame
- **8장 (Security)** — link/LAN 공격(ARP spoofing, MAC flooding)과 802.1X
- **2~3장 되돌아보기** — frame 위 IP/TCP 가 *한 hop* 에서 어떻게 보이나

> *Tools to try*: `arp -a`/`ip neigh`(ARP cache), Wireshark로 Ethernet·ARP frame, `ethtool`(link 속도/duplex), 스위치 MAC table 조회

---

## §13 한 줄 요약

> **Link layer 는 *한 hop* 의 *frame 단위 통신*. Multiple access protocol (CSMA/CD, CSMA/CA) 로 *공유 medium 의 충돌 회피*. Switch + VLAN + MPLS 의 *LAN 진화*. Spine-leaf 의 *east-west datacenter* 가 현대 LAN 의 정점.**
