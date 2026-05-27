# Ch 4 Network Layer: Data Plane — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. Data plane vs Control plane

각각 *어디서, 얼마나 빨리, 무엇* 결정?

<details><summary>답</summary>

| | Data plane | Control plane |
|--|--|--|
| 어디 | *Router 내부* (forwarding HW) | 분산 (router 간) 또는 *중앙 controller* (SDN) |
| 속도 | *ns 단위* (per packet) | *ms~s* (per route change) |
| 무엇 | Forwarding table lookup → output port | Routing algorithm → forwarding table 생성 |

**시사**:
- Data plane = *hardware* (TCAM, ASIC) — line rate
- Control plane = *software* — flexible
- SDN 핵심: control plane 중앙화 + OpenFlow

</details>

### Q2. Longest prefix match

Forwarding table:

| Prefix | Output port |
|--|--|
| 200.23.16.0/20 | A |
| 200.23.16.0/23 | B |
| 200.23.18.0/24 | C |
| 그 외 | D |

Destination `200.23.18.50` 의 forwarding 결과?

<details><summary>답</summary>

- /20 (200.23.16.0~200.23.31.255): 포함 → **match**
- /23 (200.23.16.0~200.23.17.255): 포함 안 됨 → **no match**
- /24 (200.23.18.0~200.23.18.255): 포함 → **match**
- 그 외: match

Match: /20, /24, default. **Longest = /24** → port **C**.

</details>

### Q3. Subnet 계산

회사가 1000 host 필요. /22 prefix 의 usable host 수 + broadcast address?

<details><summary>답</summary>

/22 = 32 - 22 = **10 bit host** = $2^{10}$ = **1024 addresses**.

Usable = 1024 - 2 = **1022**.

**예 `192.168.4.0/22`**:
- Network: `192.168.4.0`
- Range: `192.168.4.0 ~ 192.168.7.255`
- Broadcast: `192.168.7.255`
- Usable: `192.168.4.1 ~ 192.168.7.254`
- Mask: `255.255.252.0`

**선택 이유**: /23 = 510 부족, /22 = 1022 적합, /21 = 2046 낭비.

</details>

### Q4. Fragmentation 계산

5000 byte IPv4 datagram (header 20 + data 4980) 이 MTU 1500 link 통과.

<details><summary>답</summary>

Fragment data size = 1500 - 20 = 1480 byte. Offset unit = 8 byte.

- Frag 1: data 1480, offset=0, MF=1
- Frag 2: data 1480, offset=185, MF=1
- Frag 3: data 1480, offset=370, MF=1
- Frag 4: data 540 (4980 - 4440), offset=555, MF=0

**문제점**:
- Frag 1 loss → 4 fragment 모두 waste
- 4 packet 의 각자 routing → reordering

→ PMTUD 로 *애초에 작은 packet* 이 효율적.

</details>

### Q5. NAT 동작 추적

`192.168.1.10` browser → `93.184.216.34:443` HTTPS request.

NAT public IP = `1.2.3.4`. NAT table: `(192.168.1.10:50001) ↔ (1.2.3.4:60001)`.

(a) Browser outbound packet src/dst?
(b) NAT → Internet packet src/dst?
(c) Server 응답 packet src/dst?
(d) NAT → browser packet src/dst?

<details><summary>답</summary>

**(a)**: src=`192.168.1.10:50001`, dst=`93.184.216.34:443`
**(b)**: src=`1.2.3.4:60001`, dst=`93.184.216.34:443`
**(c)**: src=`93.184.216.34:443`, dst=`1.2.3.4:60001`
**(d)**: src=`93.184.216.34:443`, dst=`192.168.1.10:50001`

**주의**: TCP/UDP *port* 가 NAT key. Symmetric NAT 은 server 마다 다른 external port.

</details>

### Q6. Switching fabric throughput

10 port × 10 Gbps. 각 fabric 의 max throughput?

<details><summary>답</summary>

**(a) Memory**: CPU read+write → 2x bandwidth. 100 Gbps bus → *50 Gbps fabric*.

**(b) Bus**: 100 Gbps bus → 100 Gbps total.

**(c) Crossbar (no HOL)**: parallel, N×line rate = **100 Gbps**.

**(d) Crossbar (HOL, no VOQ)**: head-of-line block → throughput ~58% (classical result) → **58 Gbps**.

→ VOQ + iSLIP scheduler 가 HOL 해결.

</details>

### Q7. IPv6 의 throughput 차이

IPv4 와 IPv6 의 *throughput 차이* 가능한 원인?

<details><summary>답</summary>

**Header overhead**:
- IPv4: 20 byte
- IPv6: 40 byte

1500 MTU payload (TCP 포함):
- IPv4: 1460
- IPv6: 1440

→ IPv6 ~1.4% efficiency 하락.

**그러나 IPv6 가 빠를 수도**:
1. No router fragmentation → latency ↓
2. No checksum → router 처리 빠름
3. NAT 회피 → direct connection
4. Vendor 의 IPv6 fast path

**산업**:
- Facebook: IPv6 만 사용 시 throughput 변화 거의 없음
- T-Mobile: IPv6-only network 의 latency 향상

</details>

### Q8. DHCP timing

24h lease. 12h (50%) 시점 renew 성공. 다음 renew 시점?

<details><summary>답</summary>

- T1 = 50% lease (12h) — unicast renew
- T2 = 87.5% (21h) — broadcast renew
- T3 = 100% (24h) — IP 반납

**Renew 성공**: 새 24h lease 가 응답 시점부터. 12h 시점 renew → 새 lease 24h → 다음 renew = *12 + 12 = 24h* 시점.

**실무**:
- Server downtime 9h 이내 OK (12 + 9 = 21h, T2 까지)
- *Persistent lease* — DHCP DB 영구 저장
- *Conflict detection* — ARP probe

</details>

### Q9. 디버그 — `traceroute` 의 별표

`traceroute google.com`:
```
 1  192.168.1.1     1ms
 2  10.50.0.1       5ms
 3  *  *  *
 4  *  *  *
 5  72.14.196.0     20ms
```

3, 4 hop 의 `*` 의미 + 원인?

<details><summary>답</summary>

**`*` = ICMP 응답 없음 (timeout)**.

**원인**:
1. **ICMP block** — router 가 TTL expired 응답 차단 (보안, DDoS 회피)
2. **Rate limiting** — 빠른 traceroute → drop
3. **MPLS tunnel** — TTL 안 decrement, hop 숨김
4. **UDP port filter** — random port 33434+ 차단
5. **ECMP** — packet 마다 다른 path

**진단**:
- `traceroute -I` (ICMP) 또는 `traceroute -T -p 80` (TCP SYN)
- `mtr` — 통계적 hop 분석

→ `*` 는 *경로 단절 아님*, 단지 가시성 없음.

</details>

### Q10. 디버그 — IPv6 dual stack 의 느림

"browser 가 이상하게 느림. IPv6 끄면 정상." 원인 + 해결.

<details><summary>답</summary>

**원인**:
1. **Broken IPv6 connectivity** — DNS AAAA 반환, IPv6 시도 timeout → IPv4 fallback (수 초)
2. **IPv6 path 느림** — ISP 라우팅 비최적화
3. **MTU 문제** — ICMPv6 block → PMTUD 실패 (black hole)
4. **DNS AAAA only** — fallback 없음

**진단**:
```bash
ping6 google.com
dig AAAA google.com
traceroute6 google.com
ping -M do -s 1472 google.com  # MTU
```

**해결**:
1. *IPv6 disable* (임시): `sysctl -w net.ipv6.conf.all.disable_ipv6=1`
2. *Happy Eyeballs* 강화 — Chrome 의 IPv6 timeout 단축
3. *ISP IPv6 path issue 신고*
4. *DNS resolver*: 1.1.1.1, 8.8.8.8

**산업**: Apple Happy Eyeballs v2 (RFC 8305) — 250ms 후 IPv4 시도.

</details>

### Q11. 면접 — *왜 NAT 가 보안 X*?

"NAT 가 있어서 firewall 필요 없잖아?"

<details><summary>답</summary>

**NAT 의 우연한 부가 보안**:
- Inbound direct delivery 불가
- Internal IP 노출 안 됨

**그러나 보안 아님**:
1. **Outbound 자유** — internal malware 가 C2 직접 연결
2. **Inbound initiated** — outbound 가 NAT mapping 만들면 inbound 됨
3. **NAT traversal** — UPnP, STUN, hole punching 으로 뚫림
4. **Application layer attack** — XSS, CSRF, SQL injection 무관
5. **DNS rebinding** — JS 가 internal IP 도달

**Firewall 의 차별**:
- Stateful inspection
- Application layer filtering
- IDS/IPS integration
- Logging + alerting
- Outbound policy

> **NAT 있어도 firewall 필수.** Incidental security 의존 X.

</details>

### Q12. 면접 — SDN 의 보안 trade-off

"SDN central controller SPOF 아니야?"

<details><summary>답</summary>

**SPOF 우려**:
1. Controller down → 새 flow rule 못 만듦
2. Controller 침해 → 전체 network

**Mitigation**:

1. **Redundancy** — active-active, distributed consensus (ONOS, OpenDaylight cluster)
2. **Existing flow rules** — switch flow table = cache, 기존 flow 계속 동작
3. **Fail-open vs fail-closed** — policy 선택
4. **Controller 보안** — TLS auth, RBAC, audit logging, out-of-band

**Traditional 대비**:

| | Traditional | SDN |
|--|--|--|
| SPOF | 각 router (지역적) | Controller (중앙) |
| 변경 속도 | 느림 | 빠름 |
| 침해 영향 | 부분 | 전체 가능 |
| 복구 | 짧음 | controller 복구 필요 |

> SPOF 는 실제 위험. Redundancy + flow cache + fail-open 으로 완화. 대규모 운영자 (Google, Facebook) 는 SDN — *위험 < 운영 효율*.

</details>
