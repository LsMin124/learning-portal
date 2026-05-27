# Ch 7 Wireless and Mobile — 치트시트

> Wireless link / WiFi / Cellular / Mobility / TCP 영향.

## §1 Wireless link 특성

| 특성 | 의미 |
|--|--|
| Path loss | $P_r \propto P_t / d^n$, $n=2 \sim 5$ |
| Multipath fading | 반사 path 의 phase 차이 (Rayleigh) |
| Interference | 같은 band 의 다른 송신자 |
| SNR | $P_{signal} / P_{noise}$, dB |
| Shannon C | $B \cdot \log_2(1 + SNR)$ |

## §2 Hidden vs Exposed node

| | Hidden | Exposed |
|--|--|--|
| 상황 | A, B 못 들음, 둘 다 C 통신 | C 가 A 신호 들음, 다른 receiver |
| 결과 | C 충돌 | 불필요 wait |
| 해결 | RTS/CTS | Directional antenna |

## §3 Wireless 표준

| 표준 | 범위 | 속도 |
|--|--|--|
| Bluetooth | 10 m | 1~3 Mbps |
| WiFi 6 | 100 m | 9.6 Gbps |
| WiFi 7 | 100 m | 46 Gbps |
| 4G LTE | km | 100 Mbps |
| 5G NR | km | 10 Gbps |
| 5G mmWave | 500 m | 20 Gbps |
| Starlink | 글로벌 | 100~300 Mbps |
| LoRa | 10 km | 50 kbps |
| NB-IoT | km | 250 kbps |

## §4 802.11 진화

| 표준 | 발표 | Speed | Band |
|--|--|--|--|
| 802.11 | 1997 | 2 Mbps | 2.4 GHz |
| 802.11a | 1999 | 54 Mbps | 5 GHz |
| 802.11b | 1999 | 11 Mbps | 2.4 GHz |
| 802.11g | 2003 | 54 Mbps | 2.4 GHz |
| 802.11n (4) | 2009 | 600 Mbps | 2.4/5, MIMO |
| 802.11ac (5) | 2013 | 6.9 Gbps | 5, MU-MIMO |
| 802.11ax (6) | 2019 | 9.6 Gbps | OFDMA |
| 802.11ax (6E) | 2020 | + 6 GHz | |
| 802.11be (7) | 2024 | 46 Gbps | 320 MHz |

## §5 BSS, ESS, SSID

| 용어 | 의미 |
|--|--|
| BSS | 1 AP + clients |
| ESS | 여러 BSS (same SSID) |
| SSID | Network name |
| BSSID | AP MAC |

## §6 802.11 frame

```
| Frame Ctrl | Duration | Addr1 | Addr2 | Addr3 | SeqCtrl | Addr4 | Data | FCS |
```

4 address — Station↔AP↔Internet, AP↔AP (mesh).

## §7 CSMA/CA + RTS/CTS

```
1. Carrier sense — idle?
2. DIFS wait
3. Random backoff
4. RTS → SIFS → CTS → SIFS → Data
5. SIFS → ACK
```

**Timing**:
- SIFS = 10 μs
- DIFS = 50 μs
- Slot = 20 μs (802.11g)

## §8 802.11 association

| Step | 의미 |
|--|--|
| Beacon | AP 주기 broadcast |
| Probe req | Device 검색 |
| Probe resp | AP 응답 |
| Auth | open/shared |
| Association | 결합 |
| EAP (Ent) | 802.1X |
| DHCP | IP 받음 |

## §9 보안

| 표준 | 발표 | 보안 |
|--|--|--|
| WEP | 1997 | *Broken* (5s) |
| WPA | 2003 | TKIP, 임시 |
| WPA2 | 2004 | AES, KRACK 2017 |
| WPA3 | 2018 | SAE, forward secrecy |

## §10 WPA3

- **SAE** (Dragonfly) — offline dict 방어
- **Forward secrecy**
- **192-bit suite** (GCMP-256, SHA-384)
- **OWE** — open network encryption

## §11 802.11 Roaming

| 표준 | 효과 |
|--|--|
| Classical | DHCP 재실행, 끊김 |
| 802.11r (FT) | < 50 ms |
| 802.11k | Neighbor awareness |
| 802.11v | BSS transition mgmt |

## §12 Cellular 진화

| 세대 | 발표 | 특징 |
|--|--|--|
| 1G | 1980s | Analog voice |
| 2G | 1991 | GSM/CDMA, SMS |
| 3G | 2001 | Data 384 kbps |
| 4G LTE | 2009 | All-IP, 100 Mbps |
| 5G NR | 2019 | mmWave, < 1 ms |
| 6G | 2030~ | Tbps, AI-native |

## §13 4G LTE architecture

```
[UE] ↔ [eNB] ↔ [EPC] ↔ [Internet]
```

| Component | 역할 |
|--|--|
| UE | Phone |
| eNB / gNB | Base station |
| MME | Mobility mgmt |
| S-GW / P-GW | Data plane |
| HSS | Subscriber DB |

## §14 5G 의 3 use case

| | 요구 | 응용 |
|--|--|--|
| eMBB | > 10 Gbps | 4K/8K, AR/VR |
| URLLC | < 1 ms, 99.999% | 자율주행, telemedicine |
| mMTC | $10^6$/km² | IoT, smart city |

## §15 Network slicing

같은 physical 의 multiple virtual:
- Slice 1: eMBB
- Slice 2: URLLC
- Slice 3: mMTC

→ SDN + NFV cellular.

## §16 Cell handover

| | 의미 |
|--|--|
| Soft | 두 cell 동시 (CDMA) |
| Hard | 순차 (GSM, LTE), < 100 ms |
| Dual connectivity | 4G + 5G 동시 |
| Make-before-break | 끊김 없음 |

## §17 Mobile IP

- Home Agent + Foreign Agent + Care-of address
- IP-in-IP tunnel
- Triangle routing — 거의 안 씀

## §18 실제 mobility

| 방식 | 특징 |
|--|--|
| Cellular handover | PDP context 유지 |
| WiFi roaming | Controller 관리 |
| MPTCP | 여러 interface |
| QUIC migration | Connection ID IP 무관 |
| Mosh | SSH 의 mobile-aware UDP |

## §19 TCP wireless 적응

| | Reno (옛) | CUBIC/BBR | QUIC |
|--|--|--|--|
| Loss 해석 | Always congestion | Rate-based | Migration |
| Wireless | 잘못 감소 | 적응 | 끊김 없음 |

## §20 Adaptive bitrate

DASH/HLS:
- 짧은 chunk (2~10s)
- Bandwidth 측정 → quality 선택
- Low (240p) ↔ High (4K)

## §21 Edge computing

| | Latency |
|--|--|
| WiFi | 5~50 ms |
| 4G | 30~100 ms |
| 5G URLLC | 1~10 ms |

| Edge | 용도 |
|--|--|
| CDN (Cloudflare) | Static content |
| AWS Wavelength | Compute |
| Edge inference | ML |

## §22 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| WiFi = LAN | Link layer 의 friction |
| 5G = 빠른 4G | mmWave, slicing 새 architecture |
| WPA2 = secure | KRACK |
| Mobile IP = standard | 안 씀 |
| Wireless loss = congestion | TCP 잘못 |
| Cell = hexagonal | 실제 irregular |
| MIMO = always better | Low SNR 효과 적음 |

## §23 핵심 mindmap

```
Wireless & Mobile
├── Wireless link 특성
│   ├── Path loss
│   ├── Multipath fading
│   └── Shannon C
├── 802.11 (WiFi)
│   ├── Standards (a/b/g/n/ac/ax/be)
│   ├── BSS/ESS/SSID
│   ├── CSMA/CA + RTS/CTS
│   ├── 보안 (WEP→WPA→WPA2→WPA3)
│   └── Roaming (802.11r)
├── Cellular
│   ├── 1G → 5G → 6G
│   ├── eNB / gNB / EPC
│   └── Handover (soft/hard)
├── 5G
│   ├── eMBB / URLLC / mMTC
│   └── Network slicing
├── Mobility
│   ├── Mobile IP (옛)
│   ├── Cellular handover
│   ├── QUIC migration
│   └── MPTCP
└── 상위 layer 영향
    ├── TCP (Reno→CUBIC/BBR)
    ├── Adaptive bitrate
    └── Edge computing
```

## §24 1-line summary

> **Wireless link 의 *path loss + multipath + interference* 가 wired 와 근본 차이. WiFi 의 CSMA/CA + RTS/CTS, cellular 의 cell + handover. 5G 의 eMBB/URLLC/mMTC. Mobility 의 application-level handling (QUIC). Wireless 가 TCP, streaming, edge 의 모든 stack 영향.**
