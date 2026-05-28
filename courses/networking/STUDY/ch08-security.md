# Ch 8 Security in Computer Networks

> Kurose & Ross 의 Ch 8. *Network security 의 종합* — cryptography 부터 *firewall, IDS, operational security* 까지. 2026 의 *AI-based attack + post-quantum* 시대 의 *방어 architecture*.

이 장의 무게중심:
1. **Cryptography 기초** — symmetric, asymmetric, hash
2. **Authentication + integrity** — MAC, digital signature
3. **PKI** — public key 의 trust
4. **TLS** — *web security 의 표준*
5. **IPsec + VPN** — network layer 보안
6. **Wireless 보안** — WEP/WPA/WPA2/WPA3
7. **Firewall, IDS/IPS, DDoS 방어**
8. **Operational security** — zero trust, secret 관리

---

## §1 Network security 의 *4 요구*

**CIA + 1**:

| 요구 | 의미 |
|--|--|
| **Confidentiality** | 도청 방지 — encryption |
| **Integrity** | 변조 방지 — MAC, hash |
| **Authentication** | 누구인지 확인 — digital signature, certificate |
| **Availability** | DoS 방지 — rate limit, redundancy |
| **Non-repudiation** | 부인 방지 — digital signature |

→ Network security 의 모든 protocol 이 이 5 가지 의 조합.

---

## §2 Symmetric key cryptography

### §2.1 기본 원리

같은 key 로 encrypt + decrypt:
$$C = E_K(P), \quad P = D_K(C)$$

- 두 측이 같은 key K 공유
- Encrypt + decrypt 빠름 (HW + SW)
- *Key 분배* 의 문제

### §2.2 알고리즘

**Block cipher**:

| | Block size | Key size | 발표 |
|--|--|--|--|
| DES | 64 bit | 56 bit | 1977 (broken) |
| 3DES | 64 bit | 168 bit | 1995 (deprecated) |
| AES-128 | 128 bit | 128 bit | 2001 (표준) |
| AES-256 | 128 bit | 256 bit | 2001 (high security) |

**Stream cipher**:
- RC4 (1987, broken)
- ChaCha20 (2008, 현대)

### §2.3 Mode of operation

| Mode | 동작 | 특징 |
|--|--|--|
| ECB | 각 block 독립 | *Pattern 노출 — 절대 사용 X* |
| CBC | 이전 ciphertext 와 XOR 후 encrypt | 표준, sequential |
| CTR | Counter encrypt + plaintext XOR | Parallel, seek 가능 |
| GCM | CTR + integrity | AEAD |
| CCM | CBC-MAC + CTR | AEAD, IoT |
| ChaCha20-Poly1305 | ChaCha20 + Poly1305 MAC | TLS 1.3 표준 |

**AEAD**: encryption + integrity 한 번. Modern 표준 (TLS 1.3, WireGuard).

### §2.4 AES 의 의미

- NIST 표준 (2001), Belgian Rijndael
- *모든 modern crypto 의 기본*
- Hardware support — AES-NI, ARM crypto
- Software 수십 GB/s

---

## §3 Asymmetric (public key) cryptography

### §3.1 기본 원리

각 측이 2 key — public (공개) + private (비밀).

**Encryption**: Sender 가 receiver public key 로 encrypt → receiver private 으로 decrypt.
**Digital signature**: Signer 가 private 으로 sign → verifier 가 public 으로 verify.

### §3.2 알고리즘

| | Key size | 특징 | 발표 |
|--|--|--|--|
| **RSA** | 2048~4096 bit | Factorization | 1977 |
| **DH** | 2048+ bit | Discrete log | 1976 |
| **ECC** | 256~384 bit | Elliptic curve | 1985 |
| **ECDH, ECDSA** | 256 bit | DH/sig with ECC | 1990s |
| **Ed25519** | 256 bit | EdDSA + Curve25519 | 2011 |

**RSA 2048 ≈ ECC 224** — ECC 가 훨씬 작고 빠름. Modern 표준.

### §3.3 왜 asymmetric

**Symmetric 의 문제**: N user → $N(N-1)/2$ key 필요. 처음 어떻게 공유?

**Asymmetric**: 공개 channel 에 public key 게시 → key 분배 없이 통신.

### §3.4 Hybrid encryption

Asymmetric 은 100~1000x 느림.

**Hybrid** (TLS, PGP):
1. Asymmetric 으로 random symmetric key 교환
2. Symmetric (AES) 로 data encrypt

→ Asymmetric trust + Symmetric speed.

---

## §4 Hash + MAC + Digital signature

### §4.1 Hash function

**Property**:
- Fixed output (256 bit SHA-256)
- One-way — hash → input 불가
- Collision resistant
- Avalanche effect

| | Output | 발표 | 상태 |
|--|--|--|--|
| MD5 | 128 bit | 1992 | *Broken* |
| SHA-1 | 160 bit | 1995 | *Broken* (2017) |
| SHA-256 | 256 bit | 2001 | 표준 |
| SHA-3 | 256 bit | 2015 | Quantum-resistant |
| BLAKE2 | 256 bit | 2012 | 빠른 alternative |

### §4.2 HMAC

$$HMAC(K, M) = H((K \oplus opad) || H((K \oplus ipad) || M))$$

**한계**: 두 측 same key 필요, *non-repudiation 없음*.

### §4.3 Digital signature

**Process** (RSA):
1. $S = \text{sign}_{K_{priv}}(\text{hash}(M))$
2. Send (M, S)
3. $\text{verify}_{K_{pub}}(S, \text{hash}(M))$

**왜 hash 먼저**: Asymmetric 느림 — 큰 message sign 부담.

**EdDSA (Ed25519)**: 현대 표준. Faster, smaller, deterministic. TLS 1.3, SSH.

### §4.4 MAC vs Signature

| | MAC (HMAC) | Digital signature |
|--|--|--|
| Key | Symmetric | Asymmetric |
| Speed | 빠름 | 느림 |
| Non-repudiation | X | O |
| 용도 | TLS record, JWT | Email, code signing |

---

## §5 Authentication

### §5.1 Password

**Storage**:
- *Never plaintext*
- Bcrypt, scrypt, Argon2 — *salted + work factor*
- Salt 가 rainbow table 회피

**Transmission**: TLS 안에서만. Never URL parameter.

**Best practice**:
- MFA (password + TOTP/SMS/hardware key)
- Password manager
- *Passkey* (WebAuthn) — passwordless

### §5.2 Challenge-response

**Replay attack 방어 — Nonce**:
1. Server: random nonce $R$
2. Client: $H(R, password)$
3. Server: 같은 계산으로 verify

### §5.3 PKI

**Trust 문제**: "이 public key 가 진짜 google.com 의 것?"

**CA**:
- Trusted third party (Verisign, Let's Encrypt, DigiCert)
- Certificate 발급, CA digital signature
- OS/browser 의 root CA 미리 보유

**Certificate chain**:
```
Root CA (self-signed)
   └── Intermediate CA
         └── google.com cert
```

**Revocation**:
- CRL — 옛, 큰 list
- OCSP — query
- OCSP stapling — server 가 response 첨부
- Certificate Transparency — public log

### §5.4 Let's Encrypt

- 무료, 자동화 (ACME)
- *90 일* short lifetime — auto-renew
- HTTPS 95%+ 달성 (2025)

---

## §6 TLS

### §6.1 역사

| 버전 | 발표 | 비고 |
|--|--|--|
| SSL 2.0 | 1995 | Broken |
| SSL 3.0 | 1996 | POODLE |
| TLS 1.0 | 1999 | 사용 중지 |
| TLS 1.1 | 2006 | 사용 중지 |
| TLS 1.2 | 2008 | 표준 |
| TLS 1.3 | 2018 | 현재 표준 |

### §6.2 TLS 1.2 handshake

```
Client                       Server
  | ClientHello                 |
  |---------------------------->|
  | ServerHello + Cert + KeyEx  |
  |<----------------------------|
  | KeyEx + ChangeCipher + Fin  |
  |---------------------------->|
  | ChangeCipher + Fin          |
  |<----------------------------|
  | Application data (encrypted)|
```

**2 RTT**.

### §6.3 TLS 1.3 handshake

```
Client                       Server
  | ClientHello + KeyShare      |
  |---------------------------->|
  | ServerHello + Cert + Fin    |
  |<----------------------------|
  | Fin + Data                  |
  |---------------------------->|
```

**1 RTT** — 절반 줄임.

**1.3 개선**:
- 1 RTT (vs 2)
- 0 RTT (resumption)
- Forward secrecy 의무 — ephemeral key
- AEAD only
- 옛 algorithm 제거 (RSA key exchange, CBC, RC4)
- Encrypted SNI (ECH)

### §6.4 Cipher suite 예 (TLS 1.3)

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`

Components: key exchange + auth + encryption + MAC.

### §6.5 HTTPS

| 시기 | HTTPS share |
|--|--|
| 2010 | < 30% |
| 2025 | > 95% |

**Why universal**:
- Confidentiality, integrity, authentication
- Regulatory (GDPR, HIPAA)
- SEO — Google 우선
- Modern features — HTTP/2/3, Service Workers
- Performance — TLS 1.3 fast handshake

---

## §7 IPsec + VPN

### §7.1 IPsec

**Network layer security**.

**2 mode**:
- **Transport**: payload encrypt (host-to-host)
- **Tunnel**: entire IP packet encrypt + 새 header (gateway-to-gateway VPN)

**2 protocol**:
- **AH** — integrity + auth, no encryption (rare)
- **ESP** — encryption + integrity + auth (표준)

**Key exchange — IKE**: phase 1 (secure channel) + phase 2 (IPsec SA).

### §7.2 VPN

| 종류 | 의미 |
|--|--|
| Site-to-site | 본부 ↔ 지사 |
| Remote access | 직원 laptop ↔ 회사 |

**WireGuard** (2018):
- Modern, simple (4000 lines vs OpenVPN 100k)
- ChaCha20, Poly1305, Curve25519, BLAKE2s
- Linux kernel 통합
- 훨씬 빠름

### §7.3 Zero Trust

전통 — perimeter security (firewall 안 안전).

**Zero Trust** — 모든 access verify:
- Internal user 도 매번 인증
- Identity-aware proxy
- Continuous verification

**Google BeyondCorp**:
- VPN 없음
- Identity-based access
- Device trust — managed device 만
- Context-aware policy

---

## §8 Wireless security (요약)

| 표준 | 발표 | 보안 |
|--|--|--|
| WEP | 1997 | *Broken* (Aircrack-ng PTW 2007: 수 분 ~ 1 시간, IV 충분 시) |
| WPA | 2003 | TKIP 임시 |
| WPA2 | 2004 | AES, KRACK 2017 |
| WPA3 | 2018 | SAE, forward secrecy |

**802.1X — Enterprise**: client ↔ AP ↔ RADIUS. EAP variants — EAP-TLS, EAP-PEAP, EAP-TTLS.

---

## §9 Firewall, IDS, IPS

### §9.1 Firewall 종류

| | 동작 | 특징 |
|--|--|--|
| Stateless | Per-packet | 단순, 옛 |
| Stateful | Connection state 추적 | 표준 |
| Application gateway | Application-level (WAF) | Modern |
| NGFW | Stateful + IDS/IPS + DPI | Palo Alto, Fortinet |

### §9.2 IDS

| | 방식 | 장단점 |
|--|--|--|
| Signature-based | Known patterns | 빠름, zero-day 못 잡음 (Snort, Suricata) |
| Anomaly-based | Baseline 학습 | Zero-day, false positive 많음 |

### §9.3 IPS = IDS + blocking

### §9.4 SIEM

- Source log 통합
- Correlation
- Splunk, Elastic, QRadar
- SOAR — automated response

### §9.5 DDoS 방어 (계층)

1. ISP filter — large volume
2. Cloud scrubbing (Cloudflare, AWS Shield)
3. Application layer — rate limit, captcha
4. Auto-scaling

**Anycast** — 분산 흡수.
**Tarpit** — attacker slow down.

---

## §10 Operational security

### §10.1 Secret 관리

**Never hardcode** — git leak.

**Tools**:
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Kubernetes Secrets

**Rotation**: 90 day 또는 event-based.

### §10.2 Logging + Audit

- Centralized (SIEM)
- Immutable
- Privacy — PII redaction
- Retention — regulatory

### §10.3 STRIDE threat model

1. Asset → 2. Threat → 3. Vulnerability → 4. Mitigation → 5. Validation

**STRIDE**:
- **S**poofing
- **T**ampering
- **R**epudiation
- **I**nformation disclosure
- **D**enial of service
- **E**levation of privilege

---

## §11 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| HTTPS 면 secure | Cert validation + cipher strength 도 중요 |
| VPN = privacy 보장 | VPN provider 가 볼 수 있음. Tor 가 진짜 |
| Symmetric vs Asymmetric | Hybrid 가 표준 |
| RSA = 표준 | ECC, EdDSA 가 modern |
| Hash = encryption | One-way vs reversible |
| MD5/SHA-1 = OK | Broken — SHA-256+ 필수 |
| WEP/WPA = security | WPA2 + KRACK 패치 또는 WPA3 |
| Firewall = sufficient | Defense-in-depth |
| Zero Trust = no firewall | 둘 다 |
| Quantum = far future | 2030~ post-quantum migration 시작 |

---

## §12 자가점검

1. CIA + 1 의 5 요구?
2. Symmetric vs Asymmetric?
3. AES-GCM 의 의미?
4. Hybrid encryption 의 *왜*?
5. Hash 의 4 property?
6. Digital signature 의 *왜 hash 먼저*?
7. PKI trust 모델?
8. TLS 1.3 vs 1.2?
9. IPsec transport vs tunnel mode?
10. Zero Trust 의 *왜*?

<details><summary>모범 답</summary>

1. Confidentiality, Integrity, Authentication, Availability, Non-repudiation.
2. Symmetric: 같은 key, 빠름, key 분배 문제. Asymmetric: public/private, 느림, trust 통한 분배.
3. AES + GCM = AEAD (encrypt + integrity 한 번). TLS 1.3 표준.
4. Asymmetric 100~1000x slower. Asymmetric 으로 key 교환, symmetric 으로 data.
5. Fixed output, one-way, collision resistant, avalanche effect.
6. Asymmetric 느림 — 큰 message sign 부담. Hash 의 fixed size 만 sign.
7. CA (trusted third party) 가 cert 발급. OS/browser 의 root CA trust. Chain.
8. 1.3: 1 RTT (vs 2), 0 RTT resumption, forward secrecy 의무, AEAD only, 옛 algorithm 제거.
9. Transport: payload encrypt (host-to-host). Tunnel: 전체 IP packet + 새 header (VPN).
10. Perimeter security 한계 — internal threat 무력. Identity + continuous verification.

</details>

---

## §13 한 줄 요약

> **Network security = CIA + non-repudiation + availability. Symmetric (AES-GCM) + Asymmetric (ECDH, EdDSA) 의 hybrid. TLS 1.3 가 web security 표준. IPsec + WireGuard 의 network layer 보안. Firewall + IDS + Zero Trust 의 defense in depth. Post-quantum 의 다가오는 변화.**
