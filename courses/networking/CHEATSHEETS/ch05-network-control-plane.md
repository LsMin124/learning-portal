# Ch 5 Network Layer: Control Plane — 치트시트

> Routing algorithm / OSPF / BGP / SDN / Network management.

## §1 Routing 의 모델

| | |
|--|--|
| Vertex | Router |
| Edge | Link |
| Cost | hop / 1/BW / latency / admin weight |

**Task**: source → dest 의 *least-cost path*.

## §2 Link State vs Distance Vector

| | LS | DV |
|--|--|--|
| 정보 | 전체 topology | 이웃만 |
| Update | broadcast | only to neighbors |
| Algorithm | Dijkstra | Bellman-Ford |
| Convergence | 빠름 | 느림 (count-to-infinity) |
| Memory | 큼 | 작음 |
| 대표 | OSPF, IS-IS | RIP, EIGRP |

## §3 Dijkstra

```
N' = {s}
D(s) = 0
D(v) = c(s, v) if neighbor, else ∞

repeat:
    find w ∉ N' with min D(w)
    add w to N'
    for v ∉ N', neighbor of w:
        D(v) = min(D(v), D(w) + c(w, v))
until N' = V
```

**Complexity**: $O(V^2)$ basic, $O((V+E) \log V)$ heap.

## §4 Bellman-Ford 방정식

$$D_x(y) = \min_v \{c(x, v) + D_v(y)\}$$

**Count-to-infinity 해결**:
- Split horizon
- Poison reverse
- Hold-down timer

## §5 AS 종류

| Type | 의미 |
|--|--|
| Stub | 1 link |
| Multi-homed | 여러 link, no transit |
| Transit | 통과 traffic 운반 |

**Tier**:
- Tier 1: peering, 비용 안 냄 (~15 회사)
- Tier 2: Tier 1 에 transit fee
- Tier 3: ISP, content provider

## §6 OSPF — 특징

- Link State
- IETF (RFC 2328 v2, RFC 5340 v3)
- Hierarchy — area
- Authentication
- ECMP
- Multicast (224.0.0.5, 224.0.0.6)

## §7 OSPF area — hub-and-spoke

```
       Area 0 (backbone)
       /    |     \
    ABR1  ABR2   ABR3
     |     |      |
   Area 1 Area 2 Area 3
```

Area 1 ↔ area 2 는 *항상 area 0 경유*.

## §8 OSPF LSA type

| Type | 의미 |
|--|--|
| 1 | Router LSA |
| 2 | Network LSA (broadcast) |
| 3 | Summary LSA (inter-area) |
| 4 | ASBR Summary |
| 5 | AS External |

## §9 OSPF metric

$\text{cost} = 10^8 / BW$

| Link | Cost |
|--|--|
| 10 Gbps | 1 |
| 1 Gbps | 10 |
| 100 Mbps | 100 |

## §10 BGP — 의의

- *Internet 의 접착제*
- Path-vector protocol
- Policy-based routing

## §11 BGP eBGP vs iBGP

| | eBGP | iBGP |
|--|--|--|
| 대상 | 다른 AS | 같은 AS |
| TCP | 179 | 179 |
| AS_PATH | 변경 | 변경 안 함 |
| Topology | 직접 | Full mesh / Route reflector |

## §12 BGP message

| | 의미 |
|--|--|
| OPEN | connection 시작 |
| UPDATE | route 광고/철회 |
| KEEPALIVE | 30s, 연결 유지 |
| NOTIFICATION | 오류 |

## §13 BGP attribute

| | 의미 |
|--|--|
| AS_PATH | 경유 AS 목록, loop detection |
| NEXT_HOP | 다음 hop IP |
| LOCAL_PREF | local policy (iBGP) |
| MED | Multi-Exit Discriminator |
| COMMUNITY | tag (policy 마킹) |

## §14 BGP route 선택 (Cisco order)

1. Highest LOCAL_PREF
2. Shortest AS_PATH
3. Origin: IGP > EGP > Incomplete
4. Lowest MED
5. eBGP > iBGP
6. Lowest IGP cost to NEXT_HOP
7. Oldest
8. Lowest router ID

위에서 아래로. 동률 시 다음.

## §15 BGP policy 예

**Customer route 우선**:
- Customer LOCAL_PREF = 200
- Peer LOCAL_PREF = 100
- Provider LOCAL_PREF = 50

→ 수익 극대화.

## §16 BGP 사고

| 사건 | 영향 |
|--|--|
| Facebook outage 2021 | BGP withdraw 실수 → 6h, $60M |
| Pakistan YouTube hijack 2008 | null route eBGP 광고 → 1h |
| China Telecom 2010 | 15% Internet traffic 우회 |

→ Filter + RPKI + peer review 필수.

## §17 BGP convergence

- Update 전파 ~30s
- Path exploration 분 단위
- Stable 3~30 분
- MRAI default 30s

## §18 BGP 보안

| 기법 | 효과 |
|--|--|
| **RPKI** | Prefix-origin 검증 |
| **BGPsec** | Path 서명 |
| **MD5 password** | TCP password |
| **Max prefix limit** | 잘못된 router 차단 |

## §19 SDN — OpenFlow

```
[SDN Controller]
       |
       | OpenFlow (TCP 6653)
   ┌───┴───┐
[OF Switch] [OF Switch]
```

**Controller → Switch**: flow rule install/modify/delete, query stat, send packet.
**Switch → Controller**: packet-in, flow stat, async events.

## §20 SDN platform

| Platform | 특징 |
|--|--|
| ONOS | Carrier-grade, distributed |
| OpenDaylight | Modular, Linux Foundation |
| Ryu | Python, 학습용 |
| Floodlight | Java |
| Faucet | Production OpenFlow |

## §21 산업 SDN

| 회사 | 적용 |
|--|--|
| Google B4 | Datacenter backbone, 95% utilization |
| Facebook Fabric | Datacenter spine-leaf |
| Microsoft Azure | Datacenter SDN |
| Cisco Viptela | SD-WAN |
| VMware NSX | Datacenter overlay |

## §22 SNMP vs NETCONF

| | SNMP v3 | NETCONF |
|--|--|--|
| Transport | UDP | TCP/SSH |
| Format | ASN.1 | XML/JSON |
| Schema | MIB | YANG |
| Transaction | No | Yes |
| 보안 | auth + encryption | SSH |
| 현대성 | legacy | modern |

## §23 Telemetry

- Pull (SNMP polling) → Push (device 가 자동 보고)
- **gNMI** (gRPC Network Management Interface)
- Protocol Buffers
- ms 단위 streaming

## §24 Intent-based networking

> "이 customer 의 traffic 이 < 50ms latency"

→ Network 가 자동으로 path + policy.

도구: Cisco ACI, Juniper Apstra, Arista CloudVision.

## §25 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Routing = forwarding | 계산 vs 처리 |
| BGP = 빠름 | 분 단위 |
| LS 항상 최선 | Oscillation 가능 |
| OSPF area 임의 | Area 0 hub 필수 |
| BGP hijack = 옛 | 2024 에도 빈번 |
| SDN = panacea | SPOF, scalability |
| Network mgmt = SNMP | NETCONF + YANG + Telemetry 가 현대 |

## §26 핵심 mindmap

```
Network Layer Control Plane
├── Routing algorithm
│   ├── Link State (Dijkstra) — OSPF, IS-IS
│   └── Distance Vector (Bellman-Ford) — RIP, EIGRP
├── Hierarchy
│   ├── AS — administrative
│   ├── Intra-AS (OSPF area 0 hub)
│   └── Inter-AS (BGP)
├── BGP
│   ├── eBGP / iBGP
│   ├── AS_PATH (path-vector)
│   ├── LOCAL_PREF, MED, COMMUNITY
│   ├── 7-step decision
│   └── Policy + Security (RPKI)
├── SDN
│   ├── OpenFlow (southbound)
│   ├── REST (northbound)
│   └── Controller (ONOS, OpenDaylight)
└── Network management
    ├── SNMP (legacy)
    ├── NETCONF + YANG (modern)
    └── Telemetry (gNMI, push)
```

## §27 1-line summary

> **Control plane = forwarding table *어떻게 만드나*. Link state (OSPF) + Distance vector (BGP) 의 intra/inter-AS 분리. SDN 의 중앙 controller 가 차세대. NETCONF + YANG + Telemetry 가 modern network management.**
