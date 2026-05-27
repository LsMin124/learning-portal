# Ch 7 Wireless and Mobile — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. Wireless link 의 근본 특성

Wired 와 *왜* 다른가? 3 가지 특성 + 영향.

<details><summary>답</summary>

**1. Path loss**: $P_r \propto P_t / d^n$ ($n=2 \sim 5$). 거리 2배 → 4~32배 약화.

**2. Multipath fading**: 반사 path 의 phase 차이 → constructive/destructive. *시간에 따라 SNR 변동* (Rayleigh).

**3. Interference**: 같은 frequency 의 다른 송신자. *SINR* 로 측정.

**영향**:
- Bandwidth 변동 → adaptive bitrate streaming
- Loss 변동 → TCP 적응 (BBR, QUIC)
- Latency 변동 → edge computing
- Throughput < Shannon — modulation 한계

</details>

### Q2. Hidden node + RTS/CTS

A↔C, B↔C 가능, A↔B 불가. Hidden 충돌 + 해결.

<details><summary>답</summary>

**시나리오**:
- A→C transmit
- B 가 A 신호 못 들음 → idle 로 인식 → B→C transmit
- C 에서 충돌
- A, B 충돌 안 보임 → ACK 없음 → 재전송

**RTS/CTS 해결**:
- A: RTS to C
- C: CTS *broadcast* (모두 들음)
- B 가 CTS 들음 → silent
- A 만 transmit

**시사**:
- CTS broadcast 가 핵심
- RTS/CTS overhead — small frame 에 비효율
- 802.11 default: RTS threshold 2347 byte

</details>

### Q3. WPA2 KRACK vs WPA3

WPA2 결함 + WPA3 근본 개선?

<details><summary>답</summary>

**WPA2 KRACK** (2017):
- 4-way handshake 3rd message replay
- Nonce reset → key + nonce 재사용 → plaintext recovery
- 모든 device 영향 (Linux/Android/Win/iOS)

**WPA3 개선**:

**1. SAE** (Dragonfly):
- WPA2 PSK = handshake hash leak → offline dictionary
- SAE = *offline attack 불가능*
- 약한 패스워드 도 안전

**2. Forward secrecy**: 옛 key 누설 → 옛 traffic 안전.

**3. 192-bit suite**: GCMP-256, SHA-384 (enterprise).

**4. OWE**: Open network 도 encryption.

산업: WiFi Alliance 2018 부터 WPA3 의무.

</details>

### Q4. 5G 의 3 use case

eMBB / URLLC / mMTC 의 요구 + 응용?

<details><summary>답</summary>

**eMBB** (Enhanced Mobile Broadband):
- > 10 Gbps peak, > 100 Mbps cell edge
- 4K/8K, AR/VR, cloud gaming
- mmWave + massive MIMO + 256-QAM

**URLLC** (Ultra-Reliable Low-Latency):
- < 1 ms latency, 99.999% reliability
- 자율주행 V2X, factory automation, telemedicine
- Short TTI, grant-free uplink, redundancy

**mMTC** (massive MTC):
- $10^6$ device/km², 10+ year battery
- Smart city, agriculture, smart meter
- NB-IoT, LTE-M, NR-Light

**Network slicing**:
- 한 physical network 의 3 slice 동시
- Isolated SLA per slice
- 5G first-class

</details>

### Q5. Shannon capacity

5G mmWave, B=400 MHz, SNR=25 dB. C?

<details><summary>답</summary>

**Shannon-Hartley**:
$$C = B \cdot \log_2(1 + SNR)$$

**SNR linear**: $SNR = 10^{25/10} = 316.23$

**계산**:
$$\log_2(317.23) \approx 8.31$$
$$C \approx 4 \times 10^8 \cdot 8.31 \approx 3.32 \text{ Gbps}$$

**실제 5G mmWave**: peak ~10 Gbps (multi-band). Shannon limit per band ~3 Gbps.

**시사**:
- B linear 영향
- SNR log 영향 — 작은 효과
- mmWave 의 큰 B 가 5G 의 throughput 비결
- 단 mmWave path loss 큼 → short range

</details>

### Q6. CSMA/CA timing

802.11g. DIFS=50μs, SIFS=10μs, slot=20μs, CW=31. 최악 latency?

<details><summary>답</summary>

**Best** (no contention):
- DIFS 50 + T + SIFS 10 + ACK ≈ 100 μs + T

**Worst** (max backoff):
- DIFS 50 + CW × slot = 50 + 31×20 = **670 μs**
- + T + SIFS 10 + ACK ≈ 100 μs

**Total worst** ≈ **770 μs + T**.

**시사**:
- Heavy load — backoff dominant
- WiFi 6 OFDMA → multi-user 동시, backoff 회피
- WiFi 7 MLO → 동시 multi-band

</details>

### Q7. Multipath fading

Coherence time = 10 ms. Packet = 1 ms. Same fade 안 packet 수?

<details><summary>답</summary>

10 packet (10 ms / 1 ms).

**Fading-aware schedule**:
- Good fade — 많은 packet (high SNR 활용)
- Bad fade — 기다림 또는 robust modulation
- Opportunistic scheduling — best user 선택

**Feedback 지연**:
- CSI 수 ms 지연
- 10 ms coherence 에서 유의미

**산업**:
- 4G LTE CQI — 매 ms feedback
- 5G beam management — near-real-time
- MIMO 의 diversity — 다른 antenna 의 fade 무관

</details>

### Q8. Cell handover 시간

LTE handover 각 단계 5 ms. Total?

<details><summary>답</summary>

**4G LTE steps**:
1. Measurement (UE → src eNB) — 5 ms
2. Decision — 5 ms
3. Request (src → tgt eNB) — 5 ms
4. ACK — 5 ms
5. Command (src → UE) — 5 ms
6. Random access (target) — 5~10 ms
7. UE context setup — 5 ms

**Total**: ~30~40 ms.

**5G 개선**:
- Conditional handover — 사전 준비
- Dual connectivity — old+new 동시
- → < 10 ms

**Make-before-break**: 끊김 없음 (soft handover 효과).

**산업**: VoIP, video conf 의 seamless. Train, high-speed → 5G NTN + LEO 위성.

</details>

### Q9. 디버그 — WiFi 가 *간헐 느림*

원인 + 진단.

<details><summary>답</summary>

**원인**:

**1. Channel 간섭**: 2.4 GHz 의 Bluetooth, 전자레인지, 같은 채널 AP. 해결: 5/6 GHz.

**2. Signal 약함**: RSSI < -70 dBm. 해결: AP 위치, mesh.

**3. AP overload**: 많은 device, air time share 부족. 해결: more AP, dual band.

**4. Channel congestion**: 2.4 GHz 의 3 non-overlapping 채널 (1, 6, 11). 해결: 5 GHz.

**5. Old standard**: 802.11b/g 의 *slow rate* 강요. 해결: 802.11n+ 만 허용.

**6. TCP wireless 적응**: Reno 의 잘못 감소. 해결: CUBIC, BBR.

**7. Hidden node**: RTS/CTS threshold 조정.

**8. Roaming**: sticky 문제. 해결: band steering, load balance.

**진단**:
1. `iperf3 -c server` — throughput
2. `ping router` — latency, loss
3. WiFi analyzer — channel + signal
4. `tcpdump -i wlan0`

</details>

### Q10. 디버그 — Mobile app background drain

Network 측면 진단 + 해결.

<details><summary>답</summary>

**Cellular radio state**:
- Idle — low power
- Connected — high power
- Transition 시 high state, inactivity timer 후 idle
- 짧은 packet 빈도 ↑ → 항상 high → drain

**진단**:
- iOS: Settings → Battery → 24h
- Android: Settings → Battery → background
- Packet trace: Console.app, `adb shell dumpsys connectivity`
- mitmproxy, Charles Proxy

**흔한 패턴**:
- Frequent heartbeat (짧은 keep-alive)
- Polling (no push)
- Analytics background send
- Poorly batched push

**해결**:
- **Push** (FCM, APNs) — server trigger 시에만
- **Batching** — 주기적 통신 묶음
- **Doze mode** (Android) — deep sleep
- **Background fetch policy** 준수

**Cellular vs WiFi**:
- Cellular: radio transition 비용 큼
- WiFi: 가벼움
- → WiFi 에서 더 aggressive

</details>

### Q11. 면접 — *5G 가 한국에서 안 빠른 이유*?

"5G *광고 만 화려*. 4G 와 차이 없어. 왜?"

<details><summary>답</summary>

**광고 vs 현실 (Korea 2025)**:
- 광고: 10 Gbps, < 1 ms
- 현실: 200~500 Mbps, 30~50 ms

**Why?**:

**1. mmWave deploy 부족**:
- 진짜 5G 속도 = mmWave (24~100 GHz)
- 한국 의 mmWave 부진 — sub-6 GHz (3.5 GHz) deploy

**2. NSA vs SA**:
- *NSA* (Non-Standalone): 5G NR + 4G core — 한국 의 대부분
- *SA*: 5G NR + 5G core — true features (URLLC, slicing)
- NSA = 4G+ 수준

**3. Backbone 한계**:
- 5G radio 빠른데 backbone bottleneck
- Server 처리 + internet latency

**4. Cell density 부족**:
- mmWave short range — coverage hole

**5. Device 한계**:
- 옛 폰 의 mmWave 미지원
- mmWave 의 큰 power 소비

**6. Application low utilization**:
- 일상 의 대부분 수십 Mbps 면 충분
- *User-perceivable 한계* 도달

**언제 진짜**: stadium, airport, industrial 5G, cloud gaming, AR/VR.

> 광고 = mmWave 잠재력. 현실 = sub-6 GHz NSA = 4G+. 진짜 5G 는 2030~6G 의 industrial use case 에서.

</details>

### Q12. 면접 — *QUIC connection migration*

"어떤 차별?"

<details><summary>답</summary>

**TCP mobility 한계**:

**TCP = 5-tuple** (src IP, src port, dst IP, dst port, protocol).
- One bit 변경 = new connection
- WiFi → cellular, VPN external IP 변경, NAT port 변경 → 끊김

**QUIC 해결 — Connection ID**:

- Connection ID 가 *IP 와 무관*
- Server, client 각자의 connection ID
- Packet 의 connection ID 로 routing

**Migration 동작**:
1. Phone IP 변경 (WiFi → 5G)
2. Phone 이 옛 connection ID 로 send
3. Server 가 ID 인식 → 기존 state 사용
4. *데이터 손실 없음*

**보안**:
- Path validation — 새 path 의 진짜 client 검증
- Spoofing 방어

**산업**:
- YouTube, Google — seamless WiFi/cellular 전환
- HTTP/3 = QUIC + HTTP — modern web
- Mobile app — 끊김 없는 download

**Trade-off**:
- UDP overhead — kernel 미숙
- Encryption 의무 — visibility 부족
- Connection ID tracking — privacy 우려
- Middlebox 의 ID 추적 불가

> TCP 의 5-tuple binding 의 mobility 한계. QUIC 의 connection ID 가 IP 무관 — WiFi ↔ cellular seamless. HTTP/3 의 근본 진보. Mobile-first internet 의 필수.

</details>
