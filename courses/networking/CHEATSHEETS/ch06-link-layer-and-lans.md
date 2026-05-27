# Ch 6 Link Layer and LANs — 치트시트

> Framing / Error detection / Multiple access / MAC / Ethernet / VLAN / MPLS / Datacenter.

## §1 Link layer service

| Service | 의미 |
|--|--|
| Framing | bit → frame |
| Link access (MAC) | 공유 medium access 제어 |
| Reliable delivery (option) | Link 위 retransmit |
| Error detection + correction | CRC, FEC |

## §2 Link 종류

| Type | 의미 |
|--|--|
| Point-to-point | 두 endpoint (PPP, SONET) |
| Broadcast | 공유 medium (Ethernet, WiFi) |

## §3 Error detection 방법

| 방법 | Overhead | 검출력 |
|--|--|--|
| Parity 1 bit | 1 bit | 1 error |
| 2D parity | sqrt(n) | 1 correction, 2 detect |
| Internet checksum | 16 bit | 1's complement sum |
| CRC-32 | 32 bit | 32-bit burst 모두 |
| FEC (LDPC, RS) | 30~50% | error correction |

## §4 Multiple access 3 부류

| 부류 | 예 | 특징 |
|--|--|--|
| Channel partitioning | TDMA, FDMA, CDMA | 충돌 없음, idle 비효율 |
| Random access | ALOHA, CSMA | 효율 ↑ (light), 불안정 (heavy) |
| Taking turns | Token ring, Polling | Predictable, 복잡 |

## §5 ALOHA throughput

| | Max |
|--|--|
| Pure ALOHA | $1/(2e) \approx 0.18$ |
| Slotted ALOHA | $1/e \approx 0.37$ |

## §6 CSMA 변종

| | CSMA/CD | CSMA/CA |
|--|--|--|
| 환경 | Wired | Wireless |
| 충돌 감지 | 가능 | 불가 |
| 방식 | Listen + abort | RTS/CTS 예약 |
| Backoff | Binary exponential | + DIFS, SIFS |

## §7 CSMA/CD backoff

```
n = 0
while collision:
    wait random(0, 2^n - 1) slot
    n = min(n + 1, 10)
    transmit
n=16 → give up
```

**Slot time**:
- 10 Mbps: 51.2 μs
- 100 Mbps: 5.12 μs
- 1 Gbps: 4.096 μs

## §8 MAC address

- 48 bit = 6 byte
- OUI (24) + serial (24)
- 예: `00:1A:2B:3C:4D:5E`
- `FF:FF:FF:FF:FF:FF` = broadcast
- `01:00:5E:...` = IPv4 multicast
- `33:33:...` = IPv6 multicast

## §9 IP vs MAC

| | IP | MAC |
|--|--|--|
| Layer | Network (3) | Link (2) |
| Scope | Global | Local link |
| 길이 | 32/128 bit | 48 bit |
| 할당 | DHCP, manual | Hardware |
| 변경 | OK | Fixed |

## §10 ARP

**Task**: IP → MAC.

```
Sender (192.168.1.10)              All hosts in LAN
  | ARP request (broadcast)        |
  |    "Who has 192.168.1.20?"     |
  |------------------------------->|
  | ARP reply (unicast)            |
  |    "192.168.1.20 = AA:BB:..."  |
  |<-------------------------------|
```

Cache: IP — MAC — TTL (default ~5 min).

## §11 ARP 보안

| 공격 | 방어 |
|--|--|
| ARP spoofing | DAI |
| ARP poisoning | DHCP snooping + DAI |
| Gateway spoofing | Static ARP for gateway |
| MITM | 802.1X, VPN |

## §12 Ethernet 역사

| 시기 | Speed |
|--|--|
| 1973 | 2.94 Mbps |
| 1980 | 10 Mbps |
| 1995 | 100 Mbps |
| 1998 | 1 Gbps |
| 2002 | 10 Gbps |
| 2010 | 40/100 Gbps |
| 2020 | 400 Gbps |
| 2025 | 800 Gbps |

## §13 Ethernet frame

```
| Preamble(7B) | SFD(1B) | Dst MAC(6B) | Src MAC(6B) |
| EtherType(2B) | Data(46~1500B) | CRC(4B) |
```

EtherType:
- 0x0800 IPv4
- 0x0806 ARP
- 0x86DD IPv6
- 0x8100 802.1Q

Frame: 64 byte min, 1518 byte max (jumbo 9000).

## §14 Hub vs Switch

| | Hub | Switch |
|--|--|--|
| Layer | Physical | Link |
| Forward | All ports | Dst port |
| Duplex | Half | Full |
| Collision | CSMA/CD domain | 없음 |
| Bandwidth | Shared | Dedicated |

## §15 Switch MAC table

| MAC | Port | TTL |
|--|--|--|
| AA:BB:CC:01 | 1 | 60s |

**Self-learning**: src MAC + in_port → table.
**Forwarding**: dst MAC lookup → 해당 port / broadcast.
**Aging**: TTL 후 entry 제거 (5 min default).

## §16 VLAN — 802.1Q

```
| Dst MAC | Src MAC | 802.1Q tag | EtherType | Data | CRC |
                    ↓
| 0x8100 (TPID) | PCP(3) | DEI(1) | VLAN ID (12) |
```

VLAN ID = 12 bit → 4096 (4094 usable).

## §17 Trunk vs Access

| | Access | Trunk |
|--|--|--|
| Frame | Untagged | Tagged |
| VLAN | 1 | 여러 |
| 용도 | Endpoint | Switch↔switch |

## §18 STP

| 변종 | Convergence |
|--|--|
| STP (802.1D) | 30+ s |
| RSTP (802.1w) | 수 초 |
| MSTP (802.1s) | VLAN 별 |

## §19 MPLS

```
| Ethernet | MPLS label (4B) | IP | TCP | Data |
```

**Label**:
- Label (20)
- Traffic class (3)
- S (1, stack bottom)
- TTL (8)

**Forwarding**: ingress 부착 → 중간 swap → egress 제거.

## §20 MPLS 장점

- Label lookup (LPM 보다 빠름)
- Explicit path (RSVP-TE)
- VPN service (L3VPN, EVPN)
- QoS classes

## §21 Datacenter topology

**Spine-leaf**:
```
Spine ── Spine ── Spine
  X       X       X
Leaf    Leaf    Leaf
```

- Every leaf ↔ every spine
- ECMP equal cost
- East-west bandwidth ↑

## §22 East-west

- 전통: north-south
- 현대: east-west = 70~80%
- 이유: microservices, distributed storage, ML

## §23 RDMA

| 구현 | 위 layer |
|--|--|
| InfiniBand | 자체 fabric |
| RoCE | Ethernet |
| iWARP | TCP/IP |

Zero-copy, kernel bypass, HW offload.

## §24 VXLAN

- 24 bit VNI → 16M VLAN
- UDP encapsulation (port 4789)
- Overlay/underlay 분리
- 50 byte overhead
- EVPN control plane (BGP)

## §25 Tool 모음

| Tool | 용도 |
|--|--|
| `ethtool eth0` | NIC status |
| `ip link` | Link state |
| `arp -a`, `ip neigh` | ARP cache |
| `tcpdump -i eth0` | Capture |
| `show mac address-table` | Switch table |
| `show spanning-tree` | STP |

## §26 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Link layer = LAN | Any link |
| MAC = IP | Local vs global |
| Switch = router | Layer 2 vs 3 |
| Hub = switch | 옛 vs 현대 |
| Ethernet = CSMA/CD | 현대 full-duplex 안 씀 |
| VLAN 4096 | 실제 4094 |

## §27 핵심 mindmap

```
Link Layer & LAN
├── Service (framing, MAC, reliable, error)
├── Error detection (CRC, FEC)
├── Multiple access
│   ├── Partitioning (TDMA/FDMA/CDMA)
│   ├── Random (ALOHA, CSMA/CD, CSMA/CA)
│   └── Taking turns (token, polling)
├── Addressing
│   ├── MAC (48 bit)
│   └── ARP (IP → MAC)
├── Ethernet
│   ├── Frame (64~1518)
│   ├── Hub vs Switch
│   └── Self-learning
├── VLAN
│   ├── 802.1Q tag
│   └── VXLAN (16M)
├── MPLS
│   └── Label forwarding
└── Datacenter
    ├── Spine-leaf
    ├── East-west
    └── RDMA
```

## §28 1-line summary

> **Link layer = *한 hop 의 frame 단위 통신*. Multiple access (CSMA) 로 공유 medium 충돌 회피. Switch + VLAN + MPLS 의 LAN 진화. Spine-leaf + RDMA + VXLAN 의 modern datacenter.**
