# Ch 6 Link Layer and LANs — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. Link layer 의 4 service

각 service 가 *언제 필요* 한가?

<details><summary>답</summary>

| Service | 필요한 경우 |
|--|--|
| Framing | 모든 link |
| Link access (MAC) | *공유 medium* (Ethernet, WiFi). Point-to-point 불필요 |
| Reliable delivery | Error-prone link (무선). 광섬유 는 TCP 가 충분 |
| Error detection + correction | 모든 link |

**시사**:
- *무선 link* 의 높은 error rate — link layer reliability 가 *경제적*
- 802.11 ARQ — frame loss 즉시 재전송, TCP 의 RTT 보다 빠름

</details>

### Q2. CSMA/CD vs CSMA/CA 의 *근본 차이*

*왜* 무선 은 CD 안 쓰고 CA 쓰는가?

<details><summary>답</summary>

**CSMA/CD — wired**:
- *Full-duplex 가능* — transmit + receive 동시
- 송신 중 channel listen → 충돌 감지
- 충돌 시 jam signal + 즉시 중단

**CSMA/CA — wireless**:
- *Full-duplex 불가* — *near-far 문제*
  - 자기 송신 신호 가 훨씬 강함 — 다른 신호 안 들림
- 충돌 감지 불가능
- 대신 *예약* 으로 회피:
  - **RTS** (Request to Send)
  - **CTS** (Clear to Send) — 모든 receiver 에 broadcast
  - 다른 노드 들이 silent

**시사**:
- CSMA/CD = 충돌 후 빠른 복구
- CSMA/CA = 충돌 전 예방
- 무선 *hidden node* 문제 — RTS/CTS 가 일부 해결

</details>

### Q3. ARP 의 *왜 broadcast*

ARP request 가 *broadcast* 인데 reply 는 *unicast*. 이유?

<details><summary>답</summary>

**Request broadcast 이유**:
- Requester 가 target 의 MAC 모름
- 어디로 unicast 할지 모름

**Reply unicast 이유**:
- Request 에 *requester MAC 포함*
- Reply 가 requester MAC 알고 있음
- Unicast 가 효율

**시사**:
- Broadcast 의 비용 — LAN 의 모든 device 가 frame 처리
- 큰 LAN — broadcast 부담 ↑ → VLAN 분할
- *Gratuitous ARP* — 자기 IP-MAC 매핑 broadcast (시작/이동 시)

**보안**: Reply 도 결국 spoof 가능 — ARP 의 근본 취약. DAI, 802.1X 로 보호.

</details>

### Q4. Switch vs Router forwarding 차이

Same LAN vs different LAN — packet 의 MAC 변화?

<details><summary>답</summary>

**Same LAN** — `A (192.168.1.10)` → `B (192.168.1.20)`:
- A: ARP B → MAC 학습
- Frame: src=A 의 MAC, dst=B 의 MAC
- Switch 가 MAC table 로 forward
- *모든 hop 의 MAC 같음*

**Different LAN** — `A → C (10.0.0.50)`:
- A: gateway router 의 MAC 학습 (ARP)
- Frame 1: src=A 의 MAC, dst=router 의 MAC
- Router 가 frame MAC 분해, IP 보고, 새 link ARP
- Frame 2: src=router MAC, dst=C MAC
- *각 hop 의 MAC 다름*

**시사**:
- *IP* = end-to-end 동일
- *MAC* = hop-by-hop 변경
- Router = MAC layer boundary
- Switch = MAC layer 안에서 forwarding

</details>

### Q5. ALOHA throughput

10 노드, 각 50 ms 마다 5 ms transmission. Slotted ALOHA throughput?

<details><summary>답</summary>

**Offered load**:
- 노드 당 rate = 5/50 = 0.1
- 10 노드 → G = 1.0

**Slotted ALOHA**:
$$S = G \cdot e^{-G}$$

G = 1 → $S = 1 \cdot e^{-1} \approx 0.368$ → **36.8%**.

**검증**:
- Max throughput = $1/e \approx 0.37$ at G = 1
- G > 1 → throughput 감소 (충돌 폭증)

**시사**:
- Slotted ALOHA = light load 에만 효율
- Heavy load → CSMA 가 더 효율

</details>

### Q6. CRC 계산

Data $D = 1101011011$, Generator $G = 10011$. CRC + 전송 frame?

<details><summary>답</summary>

**Step 1**: $D \cdot 2^4 = 11010110110000$ (G degree 4 → 4 zero 추가)

**Step 2**: Binary division of $D \cdot 2^4$ by $G$ (XOR-based):

```
 11010110110000 ÷ 10011
   10011
   -----
    10011...
    (long division)
   →  remainder 1110
```

**결과**: CRC = `1110`. 전송 frame = $D + CRC$ = `11010110111110`.

**Verification** — receiver: frame ÷ G → remainder 0 (no error).

**산업**:
- Ethernet CRC-32 (G degree 32) — 4 byte CRC
- Hardware 빠른 계산
- 32 bit burst 까지 검출

</details>

### Q7. Switch MAC table 크기

100 host LAN, 각 active flow 10. Switch MAC table 필요 size?

<details><summary>답</summary>

**MAC table entry = per MAC**, not per flow.

→ Table size = **100 entry**.

**Per entry**: MAC (6B) + port (2B) + TTL (4B) + flags ≈ 16 byte.

**Total**: 100 × 16 = 1.6 KB.

**산업 capacity**:
- Cisco Catalyst 9200: 16k MAC
- Arista 7050: 288k MAC
- Cisco Nexus high-end: 1M+

**시사**:
- Datacenter — 수십만 MAC
- Microservices — 각 container MAC → polynomial 폭증
- VXLAN underlay 는 physical MAC 만, overlay 는 host 처리

</details>

### Q8. 802.1Q tag overhead

100 Mbps Ethernet link. 802.1Q tag 추가 시 throughput 감소?

<details><summary>답</summary>

**Tag** = 4 byte 추가.

**1500 byte payload**:
- Untagged: 14 + 1500 + 4 (CRC) = 1518 byte
- Tagged: 14 + 4 + 1500 + 4 = 1522 byte

**Overhead**: 4 / 1518 ≈ **0.26%** (frame level).

**100 Mbps**: ~99.74 Mbps available.

**시사**:
- 미미한 overhead
- 단 minimum frame (64 byte) 도 tag 추가 — 더 큰 비율
- *Q-in-Q* (double tagging) = 8 byte overhead
- *Baby giant frame* 지원 필요 (1522 byte)

</details>

### Q9. 디버그 — Same LAN 통신 안 됨

`192.168.1.10` ↔ `192.168.1.20` 통신 안 됨. 진단.

<details><summary>답</summary>

**Layer 1 — Physical**:
- 케이블, port disable
- `ethtool eth0` — link, speed, duplex

**Layer 2 — Link**:
- Switch port shutdown
- *VLAN mismatch*
- MAC table 오류 — `show mac address-table`
- STP block

**Layer 2.5 — ARP**:
- ARP cache poisoning — `arp -a`
- Gateway MAC 이상 시 spoofing
- `arp -d 192.168.1.20`

**Layer 3 — IP**:
- 다른 subnet — mask 불일치
- IP 충돌 — `arping -D 192.168.1.20`

**Layer 4**:
- Firewall — `iptables -L`

**도구**: `ping`, `traceroute`, `tcpdump -i eth0 host 192.168.1.20`, `arp -a`.

**흔한 원인** (경험): VLAN mismatch (40%) / IP subnet 오류 (30%) / Firewall (20%) / Physical (10%).

</details>

### Q10. 디버그 — Switch broadcast storm

모든 port LED *flash storm*. 원인?

<details><summary>답</summary>

**Broadcast storm 의 주 원인**:

**1. Network loop**:
- Switch A → B → A cycle
- Broadcast frame 의 무한 순환
- Exponential 확산

**해결 — STP**:
- Spanning tree 합의 → loop 회피
- 일부 port = block state
- STP (1990, 30s) → RSTP (수 초) → MSTP (VLAN 별)

**2. STP misconfiguration**:
- Bridge ID 오류
- PortFast 오용 (endpoint 에 사용)
- BPDU filter 오용

**3. Hardware fault**:
- Switch ASIC 의 random flood

**진단**:
- Port mirror + capture
- `show spanning-tree` (Cisco)
- `show interface status` — high broadcast count

**즉시**:
1. Suspicious cable 뽑기
2. STP enable — `spanning-tree mode rapid-pvst`
3. Root bridge 명시
4. BPDU guard on access port

</details>

### Q11. 면접 — *Datacenter 의 RDMA*

"Standard TCP/IP 도 빠른데 왜 RDMA?"

<details><summary>답</summary>

**TCP/IP 의 한계** (datacenter):

**1. Latency**:
- OS stack — 수 μs
- 100 Gbps 의 packet transmission = 0.12 μs
- *OS overhead > transmission*

**2. CPU overhead**:
- TCP 처리 ~ 1 GHz/Gbps
- 100 Gbps = 100 GHz core 부담

**3. Memory copy**:
- Application → kernel → NIC
- 수십 GB/s memory bandwidth

**RDMA 의 해결**:

**1. Zero-copy** — NIC 가 직접 app memory
**2. Kernel bypass** — user-space driver
**3. Hardware offload** — TCP/IP NIC ASIC

**결과**:
- Latency: 5μs → 1μs
- CPU: 25% → 1%
- Throughput: line rate

**산업**:
- Microsoft Azure — RoCE v2 표준
- NVIDIA Mellanox — RDMA NIC 표준
- AWS EFA — RDMA-like
- HPC, ML training, distributed DB

**한계**:
- Lossless network 필요 — PFC 또는 DCQCN
- Operations 복잡

> Datacenter 100 Gbps + μs latency → TCP/IP OS 부담이 bottleneck. RDMA 의 kernel bypass + HW offload 가 physics-bound 도달.

</details>

### Q12. 면접 — *VXLAN trade-off*

"VLAN 4094 부족하면 VXLAN 쓰면 되잖아?"

<details><summary>답</summary>

**VLAN 한계**:
- 12-bit = 4094 usable
- 큰 cloud — 수만 tenant 부족
- Spanning tree 의 slow convergence

**VXLAN 의 해결**:

**1. 24-bit VNI** — 16M VLAN
**2. UDP encapsulation** — flow hash → ECMP load balance
**3. Overlay/underlay 분리** — underlay 변경 → overlay 영향 없음

**Trade-off**:

| | |
|--|--|
| Overhead | 50 byte (~3.3%) |
| MTU | Underlay jumbo (9000) 필요 |
| HW support | NIC offload 필요 |
| Troubleshooting | Overlay/underlay 양쪽 추적 |
| L2 semantic | Broadcast → UDP unicast (semantic 위반) |

**EVPN**:
- BGP EVPN 으로 MAC/IP 학습
- Flood-and-learn 의 unscalable 회피
- Cisco, Arista 표준

> VLAN 4094 부족 → VXLAN 16M 으로 해결. Overhead + MTU + HW + ops 의 trade-off. Cloud DC 표준, 그러나 operations 부담 동반.

</details>
