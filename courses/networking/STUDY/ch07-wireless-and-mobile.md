# Ch 7 Wireless and Mobile Networks

> Kurose & Ross 의 Ch 7. *Wireless link* 의 특성 + *mobile host 의 routing/handover*. 2026 의 *WiFi 7 + 5G + Starlink* 시대 의 *physical layer 의 정점*.

이 장의 무게중심:
1. **Wireless link 특성** — 왜 wired 와 *근본적으로 다른가*
2. **802.11 (WiFi)** — *home + enterprise WLAN* 표준
3. **Cellular network** — 4G LTE / 5G / 6G 진화
4. **Mobility** — host 가 움직여도 IP 유지
5. **Wireless 가 상위 layer 에 미치는 영향**

---

## §1 Wireless link 의 *특성*

Wired 와 *근본적으로 다름*. 단순 cable 의 무선 버전 아님.

### §1.1 신호 약화 (path loss)

$$P_r \propto \frac{P_t}{d^n}$$

- $n = 2$ (자유공간)
- $n = 3 \sim 5$ (실내, 도시)

→ 거리 2배 시 신호 4~32배 약화.

### §1.2 Multipath fading

신호가 벽, 가구 에 반사 → 여러 path 도착. 각 path 의 phase 차이 → constructive/destructive interference. → 같은 위치라도 시간에 따라 signal 변동 (Rayleigh fading).

**해결**:
- **MIMO** — 여러 antenna 가 multipath 유리하게 사용
- **Diversity** — 같은 데이터 여러 path
- **OFDM** — narrow subcarriers, 각 subcarrier 가 flat fading

### §1.3 SNR

$$\text{SNR} = \frac{P_{signal}}{P_{noise}} \text{ (dB)}$$

| SNR | 의미 |
|--|--|
| 0 dB | signal = noise (안 됨) |
| 10 dB | 10x noise (간신히) |
| 20 dB | 100x noise (good) |
| 40 dB | 10000x noise (excellent) |

**Shannon capacity**:
$$C = B \cdot \log_2(1 + SNR)$$

WiFi 5: B=80 MHz, SNR=30 dB → C ≈ 800 Mbps. 실제 ~700 Mbps.

### §1.4 Interference

같은 frequency band 의 다른 송신자:
- 2.4 GHz — Bluetooth, 전자레인지, baby monitor
- 5 GHz — radar (DFS 의무)
- 6 GHz (WiFi 6E) — 새 band

**SINR** = signal-to-interference-plus-noise ratio.

### §1.5 Hidden node 문제

A, B 가 서로 못 들음 (멀리), 둘 다 C 통신 → 둘이 *동시 transmit* → C 에서 충돌. A, B 가 *충돌 안 보임* → retry 안 함.

**해결 — RTS/CTS**:
- A: RTS to C
- C: CTS broadcast
- B: CTS 들음 → silent
- A 만 transmit

### §1.6 Exposed node 문제

A→B 통신 중 C 가 D 에 transmit 하려 함. C 가 A 신호 들음 (busy) → C 가 *불필요 wait*. 실제 A→B 와 C→D 는 *충돌 안 함*.

**해결**: directional antenna, beamforming (MIMO).

---

## §2 Wireless link 표준 비교

| 표준 | 범위 | 속도 | 사용 |
|--|--|--|--|
| Bluetooth | 10 m | 1~3 Mbps | PAN, IoT |
| WiFi 6 | 100 m | 9.6 Gbps | LAN |
| WiFi 7 (2024) | 100 m | 46 Gbps | LAN |
| 4G LTE | 수 km | 100 Mbps | Cellular |
| 5G NR | 수 km | 10 Gbps | Cellular |
| 5G mmWave | 500 m | 20 Gbps | Cellular dense |
| Starlink | 글로벌 | 100~300 Mbps | LEO satellite |
| LoRa | 10 km | 50 kbps | IoT |
| NB-IoT | 수 km | 250 kbps | IoT cellular |

---

## §3 802.11 — WiFi

### §3.1 표준 진화

| 표준 | 발표 | Speed | Band |
|--|--|--|--|
| 802.11 (legacy) | 1997 | 2 Mbps | 2.4 GHz |
| 802.11a | 1999 | 54 Mbps | 5 GHz |
| 802.11b | 1999 | 11 Mbps | 2.4 GHz |
| 802.11g | 2003 | 54 Mbps | 2.4 GHz |
| 802.11n (WiFi 4) | 2009 | 600 Mbps | 2.4/5 GHz, MIMO |
| 802.11ac (WiFi 5) | 2013 | 6.9 Gbps | 5 GHz, MU-MIMO |
| 802.11ax (WiFi 6) | 2019 | 9.6 Gbps | 2.4/5 GHz, OFDMA |
| 802.11ax (WiFi 6E) | 2020 | 9.6 Gbps | + 6 GHz |
| 802.11be (WiFi 7) | 2024 | 46 Gbps | 2.4/5/6 GHz, 320 MHz |

### §3.2 Architecture

**Infrastructure**:
```
                 ↓ Internet
              [Router]
               |
              [AP]
             /  |  \
        [Phone][Laptop][TV]
```

**Ad-hoc**: AP 없이 device 끼리 직접 (옛, 적음).

### §3.3 BSS, ESS, SSID

| 용어 | 의미 |
|--|--|
| BSS | 1 AP + clients |
| ESS | 여러 BSS 묶음 (same SSID) |
| SSID | Network name ("MyWiFi") |
| BSSID | AP 의 MAC |

### §3.4 802.11 frame — 4 address

```
| Frame Control | Duration | Addr1 | Addr2 | Addr3 | SeqCtrl | Addr4 | Data | FCS |
```

**4 address 필요**:
- Station → AP → Internet: Addr1=AP, Addr2=Station, Addr3=dst
- AP → AP (mesh): Addr 4 필요

### §3.5 CSMA/CA + RTS/CTS

```
1. Carrier sense — idle?
2. DIFS wait
3. Random backoff
4. RTS → SIFS → CTS → SIFS → Data
5. SIFS → ACK
```

SIFS < DIFS — ACK 가 우선.

### §3.6 802.11 association

1. **Beacon** — AP 주기적 broadcast
2. **Probe request** — Device 의 검색
3. **Probe response** — AP 응답
4. **Authentication** — open / shared key
5. **Association** — 결합
6. **EAP** (Enterprise) — 802.1X
7. **DHCP** — IP 받음

### §3.7 보안 — WEP / WPA / WPA2 / WPA3

| 표준 | 발표 | 보안 |
|--|--|--|
| WEP | 1997 | *Broken* (5s 안에 크랙) |
| WPA | 2003 | TKIP, 임시 |
| WPA2 | 2004 | AES, 표준 |
| WPA3 | 2018 | SAE |

**WPA2 KRACK** (2017): 4-way handshake replay. 패치됨.

**WPA3 의 개선**:
- SAE (vs WPA2 PSK) — offline dictionary 방어
- Forward secrecy
- 192-bit suite (enterprise)

### §3.8 Roaming + Handover

**Classical**:
1. Signal 약화 → device 가 scan
2. 새 AP → re-association
3. DHCP 재실행 → connection 끊김

**802.11r (Fast BSS Transition, 2008)**:
- Pre-authentication, key 사전 교환
- < 50 ms handover

**802.11k, 11v** — neighbor awareness, BSS transition management.

---

## §4 Cellular network

### §4.1 진화

| 세대 | 발표 | 특징 |
|--|--|--|
| 1G | 1980s | Analog voice |
| 2G | 1991 | Digital (GSM, CDMA) — SMS |
| 3G | 2001 | Data (UMTS) — 384 kbps |
| 4G LTE | 2009 | All-IP, 100 Mbps |
| 5G NR | 2019 | mmWave, < 1 ms, IoT |
| 6G | 2030~ | Terabit/s, AI-native, satellite |

### §4.2 Architecture (4G LTE)

```
[UE] ↔ [eNB] ↔ [EPC] ↔ [Internet]
```

| Component | 역할 |
|--|--|
| UE | User Equipment (phone) |
| eNB / gNB | Base station |
| MME | Mobility management |
| S-GW / P-GW | Data plane |
| HSS | Subscriber database |

**5G 의 control + user plane 분리** — *network slicing* 가능.

### §4.3 Cell

- Hexagonal (이론), irregular (실제)
- *Frequency reuse* — 인접 cell 다른 frequency
- Macrocell (수 km), microcell (수백 m), picocell (실내)
- 5G mmWave — 100~500 m

### §4.4 Handover

**Soft handover** (CDMA): 두 cell 동시 연결, smooth.
**Hard handover** (GSM, LTE): 순차 전환, < 100 ms disconnection. Make-before-break 완화.
**5G Dual connectivity**: 4G + 5G 동시.

### §4.5 5G 의 3 use case

| | 의미 | 예 |
|--|--|--|
| **eMBB** | Enhanced Mobile Broadband | 일반 사용자, 10+ Gbps |
| **URLLC** | Ultra-Reliable Low-Latency | <1ms, 99.999% — 자율주행, telemedicine |
| **mMTC** | massive MTC | 수십만 device/km² — IoT |

### §4.6 Network slicing

같은 physical network 위 여러 virtual network:
- Slice 1: eMBB
- Slice 2: URLLC
- Slice 3: mMTC

→ SDN + NFV 의 cellular 적용.

---

## §5 Mobility — Mobile IP

### §5.1 문제

Host 이동 → IP 변경. 기존 연결 (VoIP call, TCP) 끊김.

### §5.2 Mobile IP (RFC 5944)

**원리**:
- **Home Agent** — host 의 home network router
- **Foreign Agent** — host 의 현재 network router
- **Care-of Address** — foreign 의 임시 IP

**동작**:
1. Host home: 정상
2. Host 이동 → foreign 에 registration
3. Home agent 가 home IP 의 packet 을 care-of 로 tunnel (IP-in-IP)
4. Foreign agent 가 decapsulate

**문제**: triangle routing, tunnel overhead. *거의 안 씀*.

### §5.3 실제 mobility

**Cellular mobility**: cell handover 가 PDP context 유지. IP cell network 안에서 stable.

**WiFi roaming**: 같은 WLAN 의 seamless handover. Controller 가 관리.

**Application-level mobility**:
- **MPTCP** (Multipath TCP) — 여러 interface
- **QUIC connection migration** — IP 변경에도 connection 유지
- **Mosh** — SSH 의 mobile-aware (UDP)

### §5.4 Stack 에 미치는 영향

**TCP**: 5-tuple 의 IP 변경 = connection 끊김. → QUIC connection ID 가 해결.
**HTTP**: HTTP/1.1 persistent connection 끊김. Cookie 가 session.
**TLS**: Session resumption (ticket) 으로 re-handshake 회피.

---

## §6 Wireless / Mobile 의 *상위 layer 영향*

### §6.1 TCP 의 wireless 적응

전통 TCP: *loss = congestion* → cwnd 감소.
Wireless loss = bit error (congestion 아님) → cwnd 잘못 감소.

**해결**:
- **Snoop** (옛): base station 이 packet 보관, wireless loss 시 재전송
- **TCP CUBIC / BBR**: rate-based, wireless 적응
- **QUIC**: connection migration

### §6.2 Streaming + adaptive bitrate

Wireless bandwidth 변동:
- WiFi: 100 ↔ 10 Mbps
- Cellular: 100 ↔ 1 Mbps

**DASH/HLS** 의 adaptive bitrate:
- 짧은 chunk (2~10s)
- 매 chunk bandwidth 측정 → quality 선택

### §6.3 Edge computing

Wireless latency 변동:
- WiFi: 5~50 ms
- 4G: 30~100 ms
- 5G URLLC: 1~10 ms

**Edge**: 데이터/compute 를 user 근처:
- CDN (Cloudflare, Akamai) — static
- AWS Wavelength, Verizon 5G Edge — compute
- Edge inference (ML)

→ Latency 수 ms 까지.

---

## §7 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| WiFi = LAN | WiFi 도 *link layer* — Ethernet 의 friction |
| 5G = 빠른 4G | mmWave, slicing, URLLC — 새 architecture |
| WPA2 = secure | KRACK (2017). WPA3 권장 |
| Mobile IP = standard | 산업 안 씀 |
| Wireless loss = congestion | TCP 잘못 — CUBIC/BBR/QUIC 해결 |
| Cell = hexagonal | 실제 irregular |
| MIMO = always better | Low SNR 에 효과 적음 |
| WiFi 6 = WiFi 5 + 빠름 | OFDMA 의 근본 변경 |

---

## §8 자가점검

1. Wireless link 의 3 가지 특성 (wired 와 다른)?
2. Multipath fading + 해결?
3. Hidden + Exposed node 문제?
4. 802.11 의 BSS, ESS, SSID, BSSID?
5. CSMA/CA 의 RTS/CTS 동작?
6. WPA2 vs WPA3?
7. 5G 의 3 use case?
8. Mobile IP 원리 + 안 쓰이는 이유?
9. TCP 가 wireless 에 성능 ↓ 이유?
10. WiFi 6 OFDMA 의 중요성?

<details><summary>모범 답</summary>

1. Path loss ($d^n$), multipath fading, interference. Wired 와 fundamentally 다름.
2. 여러 reflected path 의 phase 차이. MIMO + diversity + OFDM.
3. Hidden: A, B 못 들음, C 충돌. RTS/CTS 해결. Exposed: 불필요 wait. Directional antenna 해결.
4. BSS = 1 AP + clients. ESS = 여러 BSS. SSID = name. BSSID = AP MAC.
5. RTS → CTS broadcast → 다른 노드 silent → Data → ACK. SIFS 가 짧음 (ACK 우선).
6. WPA2: AES, KRACK 취약. WPA3: SAE (offline dict 방어), forward secrecy, 192-bit suite.
7. eMBB (BW), URLLC (latency + reliability), mMTC (massive IoT).
8. Home Agent + Foreign Agent + care-of address, tunnel. Triangle routing, overhead → 안 쓰임. Cellular handover + application-level 대안.
9. Wireless loss = bit error 인데 TCP 가 congestion 으로 해석 → cwnd 잘못 감소. Rate-based CC + QUIC migration.
10. Multi-user — 한 frame 안에 여러 user 의 data. Dense 환경 (공항, stadium) 의 resource sharing 핵심.

</details>

---

## §9 한 줄 요약

> **Wireless link 의 *path loss + multipath fading + interference* 가 wired 와 *근본 차이*. WiFi 의 CSMA/CA + RTS/CTS, cellular 의 macro/micro cell + handover. 5G 의 eMBB/URLLC/mMTC. Mobility 의 *application-level handling* (QUIC migration). Wireless 가 TCP, streaming, edge 의 *모든 stack* 에 영향.**
