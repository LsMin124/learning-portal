# Ch 5 Network Layer: Control Plane

> Kurose & Ross 의 Ch 5. *Network layer 의 다른 면* — routing algorithm 이 forwarding table 을 *어떻게 만드나*. Data plane (Ch 4) 의 *upstream*.

---

## §0 도입 — *forwarding table 은 누가 채우는가*

> **핵심 한 문장**: 4장의 router 가 빠르게 *forwarding* 하려면 먼저 누군가 forwarding table 을 *채워야* 하고, 5장의 control plane 이 바로 그 일 — "A 에서 B 로 가는 최선의 경로"를 *계산* 하는 routing algorithm 과, 그것을 운영하는 protocol(OSPF·BGP)·architecture(SDN)의 이야기다.

두 고전 알고리즘이 출발점이다 — 전체 지도를 알고 Dijkstra 를 푸는 *link state*(§2)와, 이웃의 소문만 듣고 수렴하는 *distance vector*(§3, Bellman-Ford). 이 둘의 성질이 곧 실제 protocol 의 성질이 된다.

규모가 커지면 *AS* 단위로 쪼갠다(§4): AS *안* 은 OSPF(§5)가 최단경로로, AS *사이* 는 BGP(§6)가 *정책* 으로 잇는다. BGP 는 성능이 아니라 "누구와 거래하는가"를 라우팅하는, Internet 을 붙이는 *접착제* 다.

마지막으로 *SDN*(§7)은 control 을 router 에서 떼어 중앙 controller 로 옮기고, NETCONF·YANG·telemetry(§8~§9)가 그 network 를 *선언적으로* 운영하는 현대적 관리법이다.

---

## 들어가기 전에

- **선수 지식**: 4장(forwarding table, longest prefix match, SDN data plane), 그래프 최단경로(Dijkstra/Bellman-Ford) 기초
- **학습 목표**
  1. **Routing algorithm** — link state vs distance vector
  2. **Intra-AS routing** — OSPF(area, LSA)
  3. **Inter-AS routing** — BGP, *Internet 의 접착제*
  4. **SDN control plane** — OpenFlow / ONOS / OpenDaylight
  5. **Network management** — SNMP / NETCONF / YANG / Telemetry
- **예상 학습 시간**: 150~200분

---

## §1 Routing 의 *문제 설정*

Network 를 *graph* 로 모델링:
- **Vertex** = router
- **Edge** = link
- **Edge cost** = 1 (hop count), bandwidth, latency, administrative weight

**Task**: source A → destination B 의 *least-cost path*.

![Figure 5.3 — network 의 추상 graph 모델. 책 p.381](/courses/networking/figures/ch05/fig-5-3.png)

> 직관: routing 은 결국 *graph 최단경로* 문제다 — router=vertex, link=edge, 숫자=cost. 이 추상화 위에서 Dijkstra(LS)·Bellman-Ford(DV)가 돈다.

### §1.1 Cost 의 의미

Cost 의 종류:
- **Hop count** — 가장 단순
- **Bandwidth 역수** — 빠른 link 가 low cost (OSPF default)
- **Latency** — delay-sensitive (게임, 음성)
- **Loss rate** — unreliable 회피
- **Administrative weight** — operator 의 *수동 설정*

**Composite metric** (Cisco EIGRP):
$$\text{Cost} = K_1 \cdot BW + K_2 \cdot \frac{BW}{256-Load} + K_3 \cdot Delay + ...$$

→ 현실의 cost = *operator policy 의 표현*.

### §1.2 Routing algorithm 의 *2 부류*

![Figure 5.1 — Per-router control — 라우터마다 routing algorithm. 책 p.378](/courses/networking/figures/ch05/fig-5-1.png)

> 직관: 전통 방식은 *각 router 안에* routing algorithm 이 들어 있어, 이웃과 메시지를 주고받아 *스스로* forwarding table 을 만든다. OSPF·BGP 가 이 분산 모델이다.

| | Link State (LS) | Distance Vector (DV) |
|--|--|--|
| 정보 | *전체 topology* | *이웃만* |
| Update | 모든 변경 broadcast | cost 변경만 이웃에게 |
| Algorithm | Dijkstra (centralized) | Bellman-Ford (distributed) |
| Convergence | 빠름 | 느림 (count-to-infinity) |
| Memory | 큼 (전체 topology) | 작음 |
| 대표 | OSPF, IS-IS | RIP, EIGRP |

---

## §2 Link State routing — Dijkstra

### §2.1 동작 단계

각 router 가:
1. **Discover neighbor** — Hello packet 으로 이웃 + cost 학습
2. **Flood link state** — 모든 router 에 자신의 link state 전파
3. **Compute shortest path** — Dijkstra 의 *local 계산*
4. **Forward** — 결과 path 의 next hop 을 forwarding table 에

### §2.2 Dijkstra algorithm

**Pseudocode**:
```
N' = {s}
D(s) = 0
for v ∈ V \ {s}:
    D(v) = c(s, v) if neighbor, else ∞

repeat:
    find w ∉ N' with min D(w)
    add w to N'
    for v ∉ N', neighbor of w:
        D(v) = min(D(v), D(w) + c(w, v))
until N' = V
```

**Complexity**: $O(V^2)$ (basic), $O((V+E) \log V)$ (priority queue).

### §2.3 예시

**Topology**:
```
A --2-- B --1-- C
|       |       |
3       2       4
|       |       |
D --1-- E --3-- F
```

**Run from A**:
| Step | N' | D(B) | D(C) | D(D) | D(E) | D(F) |
|--|--|--|--|--|--|--|
| 0 | {A} | 2 | ∞ | 3 | ∞ | ∞ |
| 1 | +B | 2 | 3 | 3 | 4 | ∞ |
| 2 | +C | | 3 | 3 | 4 | 7 |
| 3 | +D | | | 3 | 4 | 7 |
| 4 | +E | | | | 4 | 7 |
| 5 | +F | | | | | 7 |

→ 최단: A → B → C → F (cost 7).

![Figure 5.4 — node u 의 least-cost path tree 와 forwarding table. 책 p.386](/courses/networking/figures/ch05/fig-5-4.png)

> 직관: Dijkstra 의 결과는 source(u) 를 뿌리로 한 *최단경로 트리* — 각 destination 의 *첫 link* 만 추리면 그대로 forwarding table 이 된다.

### §2.4 LS 의 *문제*

**Oscillation**:
- Cost 가 load 기반이면 (예: utilization)
- Path 변경 → load 변화 → 다른 path 선택 → 또 변화...
- 안정 안 됨

**해결**:
- *Stable cost* (bandwidth 같은 정적)
- *Damping* — 변경 빈도 제한

**Flooding cost**: $O(N \cdot E)$ message.

**Convergence**: 수 초 ~ 수십 초. Cisco OSPF *Fast convergence* — sub-second.

---

## §3 Distance Vector routing — Bellman-Ford

### §3.1 Bellman-Ford 방정식

각 router x 가 destination y 에 대해:
$$D_x(y) = \min_v \{c(x, v) + D_v(y)\}$$

→ *Distributed* — 이웃 정보만으로 계산.

### §3.2 동작

```
Initialize:
  D_x(y) = c(x, y) if direct neighbor, else ∞

On change / periodically:
  send D_x to neighbors
  on receive D_v from v:
    for each y:
      D_x(y) = min over w of {c(x,w) + D_w(y)}
    if change → notify neighbors
```

### §3.3 예시

**Topology**: A — 1 — B — 2 — C.

**Initial**:
- A: D(B)=1, D(C)=∞
- B: D(A)=1, D(C)=2
- C: D(B)=2, D(A)=∞

**Round 1**:
- A receives D(B) → D(C) = 1+2 = 3
- C receives D(B) → D(A) = 2+1 = 3

**Converged**:
- A: D(B)=1, D(C)=3
- B: D(A)=1, D(C)=2
- C: D(A)=3, D(B)=2

### §3.4 Count-to-infinity 문제

![Figure 5.7 — link cost 변화. 책 p.393](/courses/networking/figures/ch05/fig-5-7.png)

> 직관: y–x link 가 4→60 으로 *나빠지면*, DV 는 이웃의 *옛 정보* 에 기대 cost 를 1씩 찔끔찔끔 올린다(count-to-infinity). 반대로 좋아질 땐 즉시 수렴 — DV 는 *나쁜 소식에 느리다*.

**Topology**: A — 1 — B — 1 — C. Link B-C fail.

C fail 감지 *전*:
- B 가 A 에 "C까지 cost 2 (via A?)" — A 의 옛 정보에 의존
- A 가 B 에 "C 까지 cost 3 (via B)" — 옛 정보 송신
- 서로 *옛 정보 cache* 로 cost 천천히 증가

→ **count to infinity**. 이름 그대로 cost 가 무한대로 ramp up.

**해결**:
1. **Split horizon** — 학습한 이웃에게 *그 정보 안 보냄*
2. **Poison reverse** — *반대 방향* 으로 D=∞ 명시
3. **Hold-down timer** — 변경 직후 수십 초 무시

→ RIP 가 모든 trick 사용. 그래도 *느림*.

---

## §4 Hierarchical routing — AS

### §4.1 *왜* hierarchy

Internet 의 수십만 router. 모두 *전체 topology* → 메모리 + flooding + convergence 폭발.

또한 *administrative autonomy* — 각 ISP 의 *자기 정책*.

**해결 — Autonomous System (AS)**:
- 같은 *administrative control* 의 router 묶음
- AS 내부: intra-AS
- AS 사이: inter-AS

![Figure 5.8 — 3개 autonomous system 으로 구성된 network. 책 p.401](/courses/networking/figures/ch05/fig-5-8.png)

> 직관: Internet 은 AS(같은 관리주체의 router 묶음)들의 network 다. AS *내부* 는 intra-AS(OSPF)로, AS *사이* 는 inter-AS(BGP)로 라우팅 — 이 분리가 확장성과 정책 자율성을 준다.

### §4.2 AS 의 종류

| Type | 의미 | 예 |
|--|--|--|
| **Stub** | 한 AS 와만 연결 | Small enterprise |
| **Multi-homed** | 여러 AS, transit X | Medium enterprise |
| **Transit** | 통과 traffic 운반 | Tier-1/2 ISP |

### §4.3 ASN

- **16-bit** (옛): 0~65535
- **32-bit** (현재): 0~4294967295
- Private: 64512~65534 (16-bit)

**Tier**:
- **Tier 1**: 다른 Tier 1 과 *peering*, 비용 안 냄. ~15 회사
- **Tier 2**: Tier 1 에 transit fee 지불
- **Tier 3**: ISP, content provider

---

## §5 Intra-AS routing — OSPF

### §5.1 OSPF 특징

- **Link State**
- IETF 표준 (RFC 2328 v2, RFC 5340 v3)
- *Hierarchy* — area
- *Authentication* — md5, key chain
- *ECMP* — equal-cost multi-path
- *Multicast* — flood 효율

### §5.2 OSPF area

**Backbone area** (area 0):
- 모든 non-backbone 이 area 0 통해 통신
- *Hub-and-spoke*

**Non-backbone**:
- Stub area, NSSA, Totally stubby 변종
- External route 가 summary 로

**ABR** (Area Border Router):
- *Multiple area 에 속하는 router*
- Summary LSA 생성

**예 — 큰 ISP**:
```
       Area 0 (backbone)
       /    |     \
    ABR1  ABR2   ABR3
     |     |      |
   Area 1 Area 2 Area 3
```

### §5.3 LSA — Link State Advertisement

| LSA Type | 의미 |
|--|--|
| Type 1 | Router LSA (own links) |
| Type 2 | Network LSA (broadcast network) |
| Type 3 | Summary LSA (inter-area) |
| Type 4 | ASBR Summary |
| Type 5 | AS External (BGP route) |

### §5.4 OSPF metric

Default: $\text{cost} = 10^8 / BW$ (bps).

| Link | Cost |
|--|--|
| 10 Gbps | 1 |
| 1 Gbps | 10 |
| 100 Mbps | 100 |

→ 빠른 link 가 low cost → 우선 선택.

### §5.5 OSPF 의 *현실*

- 모든 enterprise/ISP 의 표준 intra-AS
- Cisco, Juniper, Arista 지원
- IS-IS 가 ISP 백본에 더 인기 (OSPF 는 enterprise)

---

## §6 Inter-AS routing — BGP

### §6.1 BGP 의 의의

BGP = *Internet 의 접착제*.

- 모든 AS 의 경로 교환
- **Path-vector** protocol (DV 확장)
- *Policy-based routing* — 기술 + 경제 결정

### §6.2 BGP 의 *2 종*

![Figure 5.9 — eBGP 와 iBGP 연결. 책 p.402](/courses/networking/figures/ch05/fig-5-9.png)

> 직관: *eBGP*(굵은 선)는 서로 다른 AS 의 gateway router 끼리, *iBGP*(점선)는 같은 AS 안 router 끼리. 외부에서 배운 경로를 iBGP 로 AS 전체에 퍼뜨린다(full-mesh 또는 route reflector).

**eBGP** (external):
- 다른 AS 와 peering
- TCP 179
- AS path 포함

**iBGP** (internal):
- 같은 AS 내 router 끼리
- *Full mesh* 필요 (또는 route reflector)
- AS path 변경 안 함

### §6.3 BGP message + attribute

**Message**:
- **OPEN** — connection 시작
- **UPDATE** — route 광고/철회
- **KEEPALIVE** — 30s
- **NOTIFICATION** — 오류

**핵심 attribute**:
- **AS_PATH** — 경유 AS 목록. Loop detection + 길이 비교
- **NEXT_HOP** — 다음 hop IP
- **LOCAL_PREF** — local policy (iBGP)
- **MED** — Multi-Exit Discriminator
- **COMMUNITY** — tag (policy 마킹)

### §6.4 BGP route 선택 — 7 step

여러 path 중 *어떤 것* 선택? Cisco order:

1. **Highest LOCAL_PREF** — local policy
2. **Shortest AS_PATH** — hop 수
3. **Origin type** — IGP > EGP > Incomplete
4. **Lowest MED** — origin AS preference
5. **eBGP > iBGP** — external 우선
6. **Lowest IGP cost to NEXT_HOP** — internal
7. **Oldest** — stability
8. **Lowest router ID** — tiebreaker

→ 위에서 아래로. 동률 시 다음.

### §6.5 BGP 의 policy 표현

![Figure 5.13 — 단순 BGP policy 시나리오. 책 p.408](/courses/networking/figures/ch05/fig-5-13.png)

> 직관: provider 는 *돈 안 되는 transit* 을 거른다 — 예컨대 X 는 자기 고객(Y)으로 가는 길만 광고하고 B↔C 간 transit 은 해주지 않는다. BGP 경로는 *기술이 아니라 계약(LOCAL_PREF)* 이 정한다.

**예 — Customer route 우선**:
```
Customer LOCAL_PREF = 200
Peer LOCAL_PREF = 100
Provider LOCAL_PREF = 50
```

→ 같은 destination 에 customer 통해 가는 path 우선 (수익 극대화).

**예 — Outbound traffic engineering**:
- Advertise 시 *AS_PATH prepend* (자기 AS 여러 번)
- 길어진 AS_PATH → 받는 측 다른 path 선호 → traffic 줄어듦

### §6.6 BGP 의 *결함*

**1. Slow convergence**: 분 단위 update. Route flap damping.

**2. Security 없음**:
- AS path 위조 → BGP hijack
- 해결: **RPKI** (Resource PKI), **BGPsec** — 느린 deploy

**3. Policy 불일치** — *valley-free* 위반 시 loop 가능

### §6.7 실제 사고

**Facebook outage** (2021-10-04):
- BGP 변경 실수 → 모든 prefix withdraw
- 외부 도달 *불가능*
- 6 시간 outage, $60M loss

**Pakistan Telecom YouTube hijack** (2008):
- Pakistan ISP 의 *내부 null route* 실수로 eBGP 광고
- 전 세계 YouTube traffic 이 Pakistan 으로
- 1 시간 outage

→ BGP 의 *조심성* + *filter 필수*.

---

## §7 SDN control plane

### §7.1 SDN 의 철학

![Figure 5.2 — logically centralized control. 책 p.379](/courses/networking/figures/ch05/fig-5-2.png)

> 직관: SDN 은 routing 계산을 *원격 controller* 로 모으고, 각 switch 엔 가벼운 control agent(CA)만 둔다. controller 가 전체 view 로 flow table 을 만들어 내려보낸다 — per-router 분산의 반대.

**전통적**: 각 router 가 자기 결정, 분산 message, 복잡.

**SDN**: Controller 가 *전체 view*, 각 switch 의 flow table 원격 설치, 단순 + programmable.

### §7.2 OpenFlow protocol

```
[SDN Controller]
       |
       | OpenFlow (TCP 6653)
   ┌───┴───┐
[OF Switch] [OF Switch] [OF Switch]
```

**Controller → Switch**:
- Flow rule install/modify/delete
- Query statistics
- Send packet (controller 가 직접 packet 생성)

**Switch → Controller**:
- Packet-in (no matching rule)
- Flow stat report
- Asynchronous events

![Figure 5.16 — SDN controller 시나리오 (link-state 변화). 책 p.418](/courses/networking/figures/ch05/fig-5-16.png)

> 직관: link 상태가 바뀌면 ① OpenFlow 로 controller 가 감지 → ②③ link-state·network graph 갱신 → ④ Dijkstra 재계산 → ⑤⑥ 새 flow table 을 switch 들에 설치. control logic 이 switch 밖 *app* 으로 빠진 모습이다.

### §7.3 Northbound API

Application → Controller. REST API:
```
POST /controller/flow
{
  "match": {"in_port": 1, "tcp_dst": 80},
  "action": "forward port 2"
}
```

### §7.4 SDN platform

| Platform | 특징 |
|--|--|
| **ONOS** | Carrier-grade, distributed |
| **OpenDaylight** | Modular, Linux Foundation |
| **Ryu** | Python, 학습용 |
| **Floodlight** | Java, simple |
| **Faucet** | Production OpenFlow |

**산업**:
- Google B4 — datacenter 간 backbone
- Facebook FBOSS — switch OS + SDN
- Microsoft SONiC — open-source switch OS

### §7.5 SDN 의 한계

- **Scalability** — controller cluster (ONOS) 로 해결
- **Latency** — packet-in 의 round trip → *proactive flow installation* 으로 해결
- **SPOF** — controller down → 새 flow 못 만듦. Redundancy 필요

---

## §8 ICMP — Control plane 측면

(Ch 4 §8 에 상세. 여기선 *control* 관점 요약.)

ICMP 의 control plane 역할:
- **Error reporting** — destination unreachable, TTL expired
- **Diagnostic** — ping, traceroute
- **Path MTU discovery** — fragmentation needed
- **Redirect** — better next hop 알림 (옛, 보안 우려로 보통 비활성)

---

## §9 Network management

### §9.1 *왜* 관리

큰 network = 수천 device. 각 device 의:
- 상태 모니터링 (CPU, memory, traffic)
- 설정 변경
- 오류 알림
- 성능 측정

### §9.2 SNMP — 옛 표준

**SNMP** (Simple Network Management Protocol, 1990):
- *Manager + Agent + MIB*
- Agent 가 device 에 위치
- MIB 가 정보 schema

**Message**:
- **GET** — 값 query
- **SET** — 값 변경
- **GETNEXT** — table 순회
- **TRAP** — agent → manager event

**버전**:
- v1 (1990) — community string, *plaintext*
- v2c (1996) — 여전히 plaintext
- **v3** (2002) — authentication + encryption

**한계**: UDP, polling 부담, MIB 의 vendor 종속.

### §9.3 NETCONF + YANG

**NETCONF** (RFC 6241, 2006):
- *TCP/SSH* — reliable + encrypted
- *XML/JSON* message
- *Transaction* — atomic config change
- *Candidate / running / startup* config 분리

**YANG** (RFC 6020, 2010):
- Data modeling language
- MIB 의 후속 — 더 표현력
- Vendor 중립적

**예**:
```yang
module interfaces {
  container interfaces {
    list interface {
      key "name";
      leaf name { type string; }
      leaf enabled { type boolean; }
      leaf speed { type uint64; }
    }
  }
}
```

### §9.4 Telemetry — push-based

기존 SNMP = *pull* (polling).
Telemetry = *push* — device 가 자동 보고.

- **gRPC + Protocol Buffers** 기반 (gNMI)
- 고빈도 (millisecond)
- Streaming
- 효율적 (bytecode)

산업 — Google, Cisco, Juniper 의 *next-gen monitoring* 표준.

### §9.5 Intent-based networking

**Intent**: "*이 customer 의 traffic 이 < 50ms latency*".

→ Network 이 *자동으로 path + policy* 적용.

도구: Cisco ACI, Juniper Apstra, Arista CloudVision.

→ Network 의 declarative configuration. DevOps + automation 의 정점.

---

## §10 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| Routing = forwarding | 계산 vs 처리 |
| BGP = 빠름 | 분 단위, *slow* |
| LS = 항상 최선 | Oscillation, flooding cost |
| OSPF area = 임의 | Area 0 hub 필수 |
| BGP hijack = 옛 문제 | 2024 에도 수십 hijack/year |
| SDN = panacea | SPOF, scalability |
| Network management = SNMP | NETCONF + YANG + Telemetry 가 현대 |

---

## §11 자가점검

1. LS vs DV 차이?
2. Dijkstra 동작?
3. Bellman-Ford count-to-infinity + 해결?
4. AS 3 종류?
5. OSPF area 의 역할?
6. BGP 의 첫 3 결정 단계?
7. BGP hijack mechanism + 방어?
8. SDN controller 의 northbound + southbound?
9. SNMP v3 vs NETCONF 차이?
10. Intent-based networking?

<details><summary>모범 답</summary>

1. LS = 전체 topology, Dijkstra, fast, OSPF/IS-IS. DV = 이웃만, Bellman-Ford, slow (count-to-infinity), RIP/EIGRP.
2. Source 시작, 매번 *D 가 가장 작은 미방문 vertex* 추가, 이웃 D 갱신. $O((V+E) \log V)$.
3. Link cost 증가 시 이웃 간 옛 정보 cache → cost 천천히 ramp up. 해결: split horizon, poison reverse, hold-down.
4. Stub (1 link), Multi-homed (여러, no transit), Transit (통과 traffic).
5. Hierarchy — area 0 hub, 다른 area 가 backbone 통해 통신. LSA flooding 범위 제한.
6. (1) Highest LOCAL_PREF, (2) Shortest AS_PATH, (3) Origin type IGP > EGP > Incomplete.
7. Attacker AS 가 다른 AS prefix 광고 → traffic 빨아들임. RPKI (prefix-origin 검증), BGPsec (path 서명).
8. Northbound: app ↔ controller (REST). Southbound: controller ↔ switch (OpenFlow).
9. SNMP v3: UDP + auth/encryption + MIB. NETCONF: TCP/SSH + XML + transaction + YANG. NETCONF 가 현대.
10. Operator 가 desired state (intent) 만 명시 — network 이 자동으로 path + policy. Declarative configuration.

</details>

---

## §12 다음 학습으로

- **6장 (Link Layer)** — 계산된 경로의 *한 hop* 을 frame 으로 실현. switch 의 self-learning
- **7장 (Wireless/Mobile)** — host 가 움직일 때의 routing 과 handover
- **4장 되돌아보기** — control plane 이 만든 table 이 data plane 에서 *어떻게 쓰이나*

> *Tools to try*: `traceroute`로 AS 경로 추정, BGP looking glass(`lg.he.net`)로 실제 AS_PATH, `frr`/`bird`로 OSPF·BGP 실습, RIPE Atlas로 경로 관측

---

## §13 한 줄 요약

> **Control plane = forwarding table *어떻게 만드나*. *Link state (OSPF) + Distance vector (BGP)* 의 *intra/inter-AS* 분리. SDN 의 *중앙 controller* 가 차세대. NETCONF + YANG + Telemetry 가 *modern network management*.**
