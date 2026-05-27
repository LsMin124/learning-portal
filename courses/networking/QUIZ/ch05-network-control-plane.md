# Ch 5 Network Layer: Control Plane — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. Link State vs Distance Vector

각 algorithm 의 *정보, update, convergence* 차이?

<details><summary>답</summary>

| | LS | DV |
|--|--|--|
| 정보 | *전체 topology* | *이웃만* |
| Update | 모든 변경 broadcast | cost 변경만 이웃에게 |
| Algorithm | Dijkstra | Bellman-Ford |
| Convergence | 빠름 | 느림 (count-to-infinity) |
| Memory | 큼 | 작음 |
| 대표 | OSPF, IS-IS | RIP, EIGRP |

**시사**: LS 의 complete info 가 fast convergence, DV 의 local info 가 simple + scalable.

</details>

### Q2. AS hierarchy

Internet 의 routing 이 *왜 hierarchical*?

<details><summary>답</summary>

**Flat routing 의 문제**:
- 수십만 router → memory 폭발
- Flooding message 폭발
- Convergence 매우 느림
- *Administrative autonomy* 침해

**AS 해결**:
- 같은 admin control 의 router 묶음
- **Intra-AS**: OSPF/IS-IS (빠른 convergence)
- **Inter-AS**: BGP (policy-based)

→ Internet 의 scale + autonomy.

**AS 종류**: Stub (1 link) / Multi-homed (여러, no transit) / Transit (통과 traffic).

</details>

### Q3. OSPF area 의 의미

큰 ISP 의 area 0, 1, 2, 3. Area 1 ↔ area 2 통신 경로?

<details><summary>답</summary>

OSPF area 는 *hub-and-spoke*:
- Area 0 (backbone) = hub
- Non-backbone area = spoke

**Area 1 → area 2 경로**:
1. Area 1 router → ABR(1↔0)
2. Backbone area 0 routing
3. ABR(0↔2) → area 2 router

→ *항상 area 0 경유*. Area 1 ↔ area 2 직접 link 가 있어도 OSPF 는 *backbone* 사용.

**왜**: loop 방지, LSA flooding 범위 제한, hierarchy 단순화.

</details>

### Q4. BGP attribute 의 의미

같은 destination 의 4 path:

| Path | LOCAL_PREF | AS_PATH | MED |
|--|--|--|--|
| P1 | 200 | 100, 200 | 50 |
| P2 | 200 | 100, 200, 300 | 20 |
| P3 | 100 | 100 | 30 |
| P4 | 150 | 100, 400 | 10 |

어느 path 선택?

<details><summary>답</summary>

**Step 1 — Highest LOCAL_PREF**:
- P1, P2 = 200 (남음)
- P3, P4 탈락

**Step 2 — Shortest AS_PATH**:
- P1 = 2 hop
- P2 = 3 hop
- → **P1 선택**

**시사**:
- LOCAL_PREF 가 가장 강력
- AS_PATH length 가 2nd
- MED 는 *4단계* — 영향 적음

</details>

### Q5. Dijkstra 계산

**Topology**:
```
    A----2----B
    |  \      |
    1   3     2
    |    \    |
    C----1----D
```

Source = A. 모든 vertex 의 *최단 cost + path*?

<details><summary>답</summary>

**Initial**: D(A)=0, D(B)=2, D(C)=1, D(D)=3

| Step | N' | D(B) | D(C) | D(D) |
|--|--|--|--|--|
| 0 | {A} | 2 | 1 | 3 |
| 1 | +C | 2 | 1 | min(3, 1+1) = 2 |
| 2 | +B, +D | 2 | 1 | 2 |

**최단 경로**:
- A→B: cost 2 (직접)
- A→C: cost 1 (직접)
- A→D: cost 2 (A→C→D)

**Verify**: A→D 직접 = 3, A→B→D = 4, A→C→D = 2 ✓ 최단.

</details>

### Q6. BGP 의 count-to-infinity 방지

BGP 는 path-vector — AS_PATH 전체 유지. count-to-infinity 회피?

<details><summary>답</summary>

**DV count-to-infinity 원인**: 이웃 간 *옛 정보 cache* — path 가 어디 거치는지 모름 → loop 가능.

**BGP path-vector**:
- 각 route 가 *완전한 AS_PATH* 동반
- Router 가 *자기 AS 가 path 에 있는지* 즉시 확인
- 있으면 *reject* — loop 회피

**예**:
- AS 100 receives: "10.0.0.0/24 via AS_PATH [200, 300, 100]"
- AS 100 자신이 path 에 있음 → 즉시 reject

→ Count-to-infinity 의 근본 원인 (옛 정보 caching) 을 path 명시 로 해결.

**대가**: AS_PATH 의 공간 + bandwidth, processing 부담. 그러나 *correctness* 가 더 중요.

</details>

### Q7. ECMP

OSPF 가 source ↔ dest 사이 3 개의 equal-cost path 발견. Packet 분산?

<details><summary>답</summary>

**ECMP**: 같은 cost 의 multiple path *모두 사용*.

**분산 방식**:

**1. Per-flow hashing** (표준):
- Hash(src IP, dst IP, src port, dst port, protocol) → path index
- 같은 flow → 같은 path (순서 유지)
- 다른 flow → 다른 path (분산)
- 5-tuple hash, RFC 2992

**2. Per-packet round-robin** (옛):
- 패킷 단위 분산
- *Reordering* → TCP throughput 하락
- 거의 안 씀

**3. Adaptive**:
- Link utilization 기반
- Cisco PfR, Juniper RDM

**시사**:
- Bandwidth 증가 이점
- 그러나 *one flow = one path* — single flow throughput = single path 한계
- Multi-stream (iperf3 -P 8) 이 full bandwidth 활용

</details>

### Q8. BGP convergence

세계의 prefix `198.51.100.0/24` 가 BGP withdraw. 전 세계 router 학습까지 평균 시간?

<details><summary>답</summary>

**Phase 1 — Withdrawal 전파** (수 초~수십 초):
- Origin → 이웃 → 전파
- Update 의 propagation delay 평균 ~30s

**Phase 2 — Path exploration** (분):
- 일부 AS 가 다른 path (백업) 시도
- *Path hunting* — 길이 짧은 → 긴 path
- 옛 path advertise 잔재 → 반복 update

**Phase 3 — Stable** (수 분):
- 모든 path converge

**Total**: 평균 **3 분 ~ 30 분** (RIPE NCC 측정).

**산업 시사**:
- BGP 변경 조심 — 분 단위 영향
- *MRAI* (default 30s) — 변경 빈도 제한
- *Route flap damping* — 빠른 flap router 처벌

**Facebook 2021 outage**: 6 시간 — internal BGP 도 같은 convergence 문제.

</details>

### Q9. 디버그 — Routing loop

`traceroute google.com`:
```
 5  10.0.0.1   1ms
 6  10.0.0.2   1ms
 7  10.0.0.1   1ms
 8  10.0.0.2   1ms
 9  *  *  *
```

원인 + 해결.

<details><summary>답</summary>

**Routing loop 진단**.

**원인**:
1. Routing protocol bug — DV count-to-infinity
2. Misconfigured static route
3. BGP path 이상 — split horizon 위반
4. Control/data plane 불일치
5. MPLS LSP loop

**확인**:
- `show ip route google.com` (Cisco) / `show route` (Juniper)
- BGP/OSPF table 의 next hop
- Static route

**해결**:
1. *즉시* — TTL=0 → drop. 사용자 영향은 timeout
2. *임시* — loop router 의 static route 수정
3. *영구* — routing protocol 정정 (OSPF re-flood, BGP filter)

**예방**:
- Static route 최소화
- *Route filter* on AS boundary
- *Looking glass*, RIPE Atlas monitoring
- 기본 TTL=64 — 무한 loop 가 몇 초 안에 drop

</details>

### Q10. 디버그 — OSPF adjacency 안 됨

두 router 같은 link, OSPF adjacency 안 형성. 진단.

<details><summary>답</summary>

**OSPF adjacency 조건**:
1. Same area
2. Same authentication
3. Same hello/dead interval
4. Same MTU
5. Same network mask
6. Same area type

**진단**:
- Cisco: `show ip ospf neighbor`
- Juniper: `show ospf neighbor`
- Debug: `debug ip ospf hello`

**원인 + 해결**:

| 원인 | 해결 |
|--|--|
| Area mismatch | Area 일치 |
| Authentication mismatch | Key/type 일치 |
| Hello/dead interval | Default 10/40s, 동기화 |
| MTU mismatch | `ip ospf mtu-ignore` 또는 양쪽 일치 |
| Mask mismatch | Subnet mask 일치 |
| Link down | Physical/link layer 확인 |
| Firewall block | Protocol 89 허용 |
| Multicast block | 224.0.0.5, 224.0.0.6 허용 |
| Same router ID | 다른 ID |

**Best practice**:
- Loopback 사용 (physical port down 영향 회피)
- Router ID 명시
- *Passive interface* — 외부 link 의 OSPF 차단

</details>

### Q11. 면접 — *왜 BGP 가 *느린데도* 쓰나*?

"BGP 가 분 단위 convergence 면 너무 느린데 왜?"

<details><summary>답</summary>

**BGP 느림 이유**:
1. Policy 평가 비용 (LOCAL_PREF, MED, community)
2. Path-vector update size 처리
3. MRAI — *의도적* slowness (flap 방지)
4. Route flap damping

**왜 안 바꾸나**:

**1. Scalability**:
- 전 세계 ~800K route, 70K AS
- Faster algorithm = higher update rate = router CPU burst
- 현재의 slow but stable 이 capacity 적합

**2. Backwards compatibility**:
- 모든 ISP 가 BGP — upgrade 동기화 불가
- 부분 upgrade 의 interoperability 어려움

**3. Policy expressiveness**:
- BGP policy 표현력 완전
- 대안의 expressiveness 입증 없음

**4. Operational maturity**:
- 30+ 년 의 tool, expertise, vendor support
- 전환 비용 막대

**현재 진행**:
- BGP 확장 — RPKI (보안), BGPsec (path 서명), BGP-LS (link state)
- 완전 대체 현실적 없음

> BGP 가 *완벽 아님*. 그러나 *Internet scale 의 정책 routing* 의 *현실적 유일 답*. 분 단위 convergence = stability 의 대가.

</details>

### Q12. 면접 — *SDN 이 enterprise 에 안 퍼지는 이유*?

"Google 은 SDN, 우리는 도입 검토. *왜 안 하는 회사 많냐* 사장이 묻는다."

<details><summary>답</summary>

**SDN enterprise 채택 부진 이유**:

**1. 운영자 skill gap**:
- 전통 CLI vs SDN programmer
- Network + software engineer hybrid 인재 부족
- 재교육 비용 ↑

**2. Vendor lock-in 의 *반대*** 부담:
- 전통 CLI = vendor 의 고정 운영
- SDN 의 vendor-agnostic = 좋은 점, 그러나 *통합 책임 자기*
- 한 vendor 의 throat-to-choke = 책임 회피

**3. Application 성숙도**:
- SDN northbound API = 잘 만든 network app 필요
- Open source SDN app 의 enterprise feature 부족

**4. 보안 + reliability 우려**:
- Controller SPOF — backup/failover 검증 필요
- Software bug = 전체 network 영향
- Enterprise risk averse

**5. ROI 명확성**:
- Google SDN = trillion-dollar 회사의 *수십% 절감*
- Enterprise 100 switch = 효과 작음 + 비용 큼
- *SD-WAN* 은 enterprise 채택 — traffic engineering 가치

**6. Hybrid 현실**:
- 완전 SDN = 적음
- 부분 SDN (overlay, SD-WAN) = 보통

> SDN 가치는 datacenter scale 이상. Enterprise 의 cost-benefit + operations 변화 비용 불일치. *SD-WAN* 같은 partial SDN 이 현실적. Pure SDN 은 Google/Facebook scale 의 사치.

</details>
