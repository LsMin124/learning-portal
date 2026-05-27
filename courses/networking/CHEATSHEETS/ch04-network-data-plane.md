# Ch 4 Network Layer: Data Plane — 치트시트

> Router 내부 / IPv4 / NAT / DHCP / IPv6 / SDN.

## §1 Data plane vs Control plane

| | Data plane | Control plane |
|--|--|--|
| 위치 | Router 내부 (HW) | 분산 또는 SDN controller |
| 단위 | ns | ms~s |
| 결정 | Forwarding (lookup) | Routing (algorithm) |
| 구현 | TCAM, ASIC | Software |

## §2 Router 4 component

```
       Input ports → Switching Fabric → Output ports
            ↑                                  ↓
            ←────── Routing Processor ─────────
```

## §3 Longest Prefix Match

| Prefix | Action |
|--|--|
| 11001000 00010111 00010000 /21 | port 0 |
| 11001000 00010111 00011000 /24 | port 1 |
| 그 외 | port 3 |

→ *Most specific* (longest) 우선.

**구현**:
- **TCAM** — 0/1/X, parallel lookup, 1 ns
- **Multi-bit trie** — software

## §4 Switching fabric 3 방식

| | 동작 | Bandwidth |
|--|--|--|
| Memory | CPU read+write | < bus/2 |
| Bus | 단일 bus | bus speed |
| Crossbar | N×N matrix, parallel | N × line rate |

HOL → VOQ 로 해결.

## §5 Buffer + AQM

**고전**: $B = RTT \cdot C$ (BDP)

**현대 small buffer**: $B = RTT \cdot C / \sqrt{N}$

**Bufferbloat** = 큰 buffer → 큰 queueing delay.

**AQM**:
- RED (1993) — random early drop
- CoDel (2012) — delay-based
- FQ-CoDel, CAKE — fair queueing + CoDel

## §6 IPv4 header (20+ byte)

```
| Ver(4) | HL(4) | DSCP(6) | ECN(2) | Total Length (16) |
| Identification (16)       | Flags(3) | Frag Offset (13) |
| TTL (8)         | Protocol(8) | Header Checksum (16)   |
| Source IP (32)                                          |
| Destination IP (32)                                     |
```

Protocol: TCP=6, UDP=17, ICMP=1.

## §7 Fragmentation 예

5000 byte → MTU 1500:

| Frag | Data | Offset | MF |
|--|--|--|--|
| 1 | 1480 | 0 | 1 |
| 2 | 1480 | 185 | 1 |
| 3 | 1480 | 370 | 1 |
| 4 | 540 | 555 | 0 |

→ 한 frag loss = 전체 drop. PMTUD 가 회피.

## §8 IPv4 special ranges

| Range | 용도 |
|--|--|
| 10.0.0.0/8 | Private (large) |
| 172.16.0.0/12 | Private (medium) |
| 192.168.0.0/16 | Private (home) |
| 127.0.0.0/8 | Loopback |
| 169.254.0.0/16 | Link-local |
| 224.0.0.0/4 | Multicast |
| 0.0.0.0/0 | Default route |

## §9 CIDR — 임의 prefix

| Host 수 | Prefix |
|--|--|
| 254 | /24 |
| 510 | /23 |
| 1022 | /22 |
| 2046 | /21 |
| 65534 | /16 |

Usable = $2^{32-x} - 2$.

## §10 DHCP — DORA

```
Client                  DHCP Server
  | Discover (broadcast)  |
  |---------------------->|
  |       Offer           |
  |<----------------------|
  | Request               |
  |---------------------->|
  |       Ack             |
  |<----------------------|
```

Lease: T1 (50%) → T2 (87.5%) → T3 (100%).

## §11 NAT 동작

```
192.168.1.10:50001 → 1.2.3.4:60001 → google.com:443
                  ↑ NAT 변환
```

Table: `(internal IP, port) ↔ (public IP, external port)`.

**Traversal**: STUN (외부 addr 발견) / TURN (relay) / ICE (조합).

## §12 IPv6 header (40 byte fixed)

```
| Ver(4) | Traffic Class(8) | Flow Label (20)        |
| Payload Length (16) | Next Header(8) | Hop Limit(8)|
| Source IP (128)                                    |
| Destination IP (128)                               |
```

## §13 IPv4 vs IPv6

| | IPv4 | IPv6 |
|--|--|--|
| Header | 20+ (variable) | 40 (fixed) |
| Address | 32 bit | 128 bit |
| Fragmentation | router | endpoint only |
| Checksum | yes | no |
| Broadcast | yes | no (multicast 만) |

## §14 IPv6 주요 prefix

| | 용도 |
|--|--|
| `::1` | Loopback |
| `fe80::/10` | Link-local |
| `fc00::/7` | Unique local |
| `2000::/3` | Global unicast |
| `ff00::/8` | Multicast |

## §15 IPv6 전환 전략

| 방식 | 동작 |
|--|--|
| Dual stack | v4+v6 동시. DNS A/AAAA. Happy eyeballs |
| Tunneling | v6 in v4 (6to4, Teredo) |
| Translation | NAT64 |

**Adoption 2025**: Global ~45%, India 70%, Korea 12%.

## §16 ICMP message type

| Type | Code | 의미 |
|--|--|--|
| 0 | 0 | Echo reply |
| 3 | 0~4 | Unreachable |
| 8 | 0 | Echo request |
| 11 | 0 | TTL expired |
| 12 | 0 | IP header bad |

## §17 SDN — OpenFlow

| Match | Counter | Action |
|--|--|--|
| dst MAC, in_port | count | Forward port N |
| TCP port = 80 | | Send to controller |
| (no match) | | Drop |

Action: forward / drop / modify / send-to-controller / encapsulate.

**P4**: switch parser 자체 프로그램 가능.

## §18 산업의 SDN

| 회사 | 적용 |
|--|--|
| Google B4 | Datacenter backbone, 95% utilization |
| Facebook Fabric | Datacenter spine-leaf |
| Microsoft Azure | Datacenter SDN |
| Cisco Viptela | SD-WAN |
| VMware NSX | Datacenter overlay |

## §19 Middlebox 종류

| | 용도 |
|--|--|
| NAT | 주소 변환 |
| Firewall | 패킷 필터 |
| IDS/IPS | 침입 탐지 |
| Load balancer | 부하 분산 |
| WAN optimizer | 압축, dedup |
| Proxy | HTTP/SOCKS |
| DPI | 패킷 검사 |

End-to-end principle 와 충돌 → ossification 의 원인.

## §20 Tool 모음

| Tool | 용도 |
|--|--|
| `ip route`, `ip addr` | 라우팅/주소 |
| `traceroute`, `mtr` | 경로 추적 |
| `ping`, `ping6` | 도달 확인 |
| `tcpdump`, `wireshark` | Packet capture |
| `dhclient`, `dhcpcd` | DHCP client |
| `iptables`, `nftables` | 방화벽 |

## §21 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Router = layer 3 만 | 현대는 layer 4~7 까지 |
| Routing = forwarding | 계산 vs 처리 |
| IP = reliable | Best-effort |
| NAT = security | 부가 보안만 |
| IPv6 = IPv4 확장 | 별도 protocol |
| TTL = seconds | Hop count |

## §22 핵심 mindmap

```
Network Layer Data Plane
├── Forwarding (per packet, ns)
│   └── Longest prefix match
├── Router internal
│   ├── Input port (parse, lookup)
│   ├── Switching fabric (Memory/Bus/Crossbar)
│   ├── Output port (queue, schedule)
│   └── Routing processor
├── IPv4
│   ├── Header (20+ byte)
│   ├── Addressing (CIDR)
│   ├── Fragmentation
│   ├── DHCP (DORA)
│   └── NAT (private ↔ public)
├── IPv6
│   ├── 128 bit address
│   └── Dual stack 전환
├── ICMP (ping, traceroute)
└── SDN (OpenFlow, P4)
```

## §23 1-line summary

> **Data plane = router 의 *packet 처리 hardware*. IPv4 = best-effort + NAT + DHCP 의 실제 운영. IPv6 = 느린 전환. SDN 의 OpenFlow/P4 가 programmable network 의 미래.**
