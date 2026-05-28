# Ch 8 Security — 치트시트

> CIA / Symmetric / Asymmetric / Hash / MAC / PKI / TLS / IPsec / Firewall / Zero Trust.

## §1 CIA + 1 의 5 요구

| | 의미 | 기술 |
|--|--|--|
| Confidentiality | 도청 방지 | AES, ChaCha20 |
| Integrity | 변조 방지 | SHA-256, HMAC |
| Authentication | 누구인지 | Cert, signature, password |
| Availability | DoS 방지 | Rate limit, redundancy, anycast |
| Non-repudiation | 부인 방지 | Digital signature only |

## §2 Symmetric vs Asymmetric

| | Symmetric | Asymmetric |
|--|--|--|
| Key | 같음 | Public + Private |
| Speed | 빠름 | 100~1000x 느림 |
| Key 분배 | 어려움 | 쉬움 |
| Scale | $N(N-1)/2$ | $2N$ |
| Non-repud | X | O |

→ **Hybrid** 가 표준 (TLS, PGP).

## §3 Symmetric algorithm

| | Block | Key | 발표 | 상태 |
|--|--|--|--|--|
| DES | 64 | 56 | 1977 | Broken |
| 3DES | 64 | 168 | 1995 | Deprecated |
| AES-128 | 128 | 128 | 2001 | 표준 |
| AES-256 | 128 | 256 | 2001 | High security |
| RC4 | - | 40~2048 | 1987 | Broken |
| ChaCha20 | - | 256 | 2008 | Modern |

## §4 Mode of operation

| Mode | 동작 | 비고 |
|--|--|--|
| ECB | Block 독립 | *절대 사용 X* |
| CBC | Prev XOR | Sequential |
| CTR | Counter + XOR | Parallel |
| **GCM** | CTR + integrity | **AEAD** |
| CCM | CBC-MAC + CTR | AEAD, IoT |
| ChaCha20-Poly1305 | + MAC | TLS 1.3 |

## §5 Asymmetric algorithm

| | Key size | 특징 |
|--|--|--|
| RSA | 2048~4096 | Factorization |
| DH | 2048+ | Discrete log |
| ECC | 256~384 | Elliptic curve |
| ECDH, ECDSA | 256 | DH/sig with ECC |
| Ed25519 | 256 | EdDSA + Curve25519 |

## §6 RSA vs ECC equivalent

| Symmetric | RSA | ECC |
|--|--|--|
| 80 | 1024 | 160 |
| 112 | 2048 | 224 |
| 128 | 3072 | 256 |
| 192 | 7680 | 384 |
| 256 | 15360 | 521 |

## §7 Hash function

**Property**: Fixed output / One-way / Collision resistant / Avalanche.

| | Output | 발표 | 상태 |
|--|--|--|--|
| MD5 | 128 | 1992 | *Broken* |
| SHA-1 | 160 | 1995 | *Broken* (2017) |
| SHA-256 | 256 | 2001 | 표준 |
| SHA-3 | 256 | 2015 | Quantum-resistant |
| BLAKE2 | 256 | 2012 | 빠름 |

## §8 HMAC

$$HMAC(K, M) = H((K \oplus opad) || H((K \oplus ipad) || M))$$

같은 key 양측 필요. Non-repudiation 없음.

## §9 Digital signature

**Process**:
1. $S = \text{sign}_{K_{priv}}(\text{hash}(M))$
2. Send (M, S)
3. $\text{verify}_{K_{pub}}(S, \text{hash}(M))$

**Hash 먼저**: asymmetric 느림.

**EdDSA**: 현대 표준 (faster, smaller, deterministic).

## §10 MAC vs Signature

| | HMAC | Signature |
|--|--|--|
| Key | Symmetric | Asymmetric |
| Speed | 빠름 | 느림 |
| Non-repud | X | O |
| 용도 | TLS, JWT | Email, code |

## §11 Password hash

| | 발표 | 특징 |
|--|--|--|
| MD5 (no salt) | - | 절대 금지 |
| bcrypt | 1999 | Salted + work factor |
| scrypt | 2009 | Memory-hard |
| **Argon2** | 2015 | GPU 회피 |

**2025 권장**:
- bcrypt cost 12 (250 ms)
- Argon2id memory 64 MB, iter 3

## §12 PKI

```
Root CA (self-signed, OS/browser)
   └── Intermediate CA
         └── Server cert
```

**Revocation**: CRL / OCSP / OCSP stapling / Certificate Transparency.

**Let's Encrypt**: 무료, ACME 자동화, 90 day lifetime, HTTPS 95%+ (2025).

## §13 TLS 역사

| 버전 | 발표 | 비고 |
|--|--|--|
| SSL 2.0 | 1995 | Broken |
| SSL 3.0 | 1996 | POODLE |
| TLS 1.0 | 1999 | 중지 |
| TLS 1.1 | 2006 | 중지 |
| TLS 1.2 | 2008 | 표준 |
| TLS 1.3 | 2018 | 현재 |

## §14 TLS 1.3 handshake

```
Client                       Server
  | ClientHello + KeyShare      |
  |---------------------------->|
  | ServerHello + Cert + Fin    |
  |<----------------------------|
  | Fin + Data                  |
  |---------------------------->|
```

**1 RTT** (vs 2 RTT 1.2). **0 RTT** with resumption.

## §15 TLS 1.3 개선

- 1 RTT
- 0 RTT resumption
- Forward secrecy 의무
- AEAD only
- 옛 algorithm 제거
- Encrypted SNI (ECH)

## §16 Cipher suite (1.3)

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`

## §17 HTTPS adoption

| 시기 | Share |
|--|--|
| 2010 | < 30% |
| 2020 | > 80% |
| 2025 | > 95% |

## §18 IPsec

**Mode**:
- Transport — payload encrypt (host-to-host)
- Tunnel — 전체 IP + 새 header (VPN)

**Protocol**:
- AH — integrity + auth
- ESP — encrypt + integrity + auth (표준)

**Key exchange**: IKE (phase 1 + phase 2).

## §19 VPN

| | 의미 |
|--|--|
| Site-to-site | 본부 ↔ 지사 |
| Remote access | Laptop ↔ 회사 |

**WireGuard** (2018): 4000 lines, ChaCha20 + Poly1305 + Curve25519 + BLAKE2s, kernel.

## §20 Zero Trust

**원칙**:
- Never trust, always verify
- Identity-based
- Continuous verification
- Least privilege

**Google BeyondCorp**:
- No VPN
- Identity-aware proxy (IAP)
- Device trust
- Context-aware policy

## §21 Wireless security

| 표준 | 발표 | 보안 |
|--|--|--|
| WEP | 1997 | Broken (5s) |
| WPA | 2003 | TKIP 임시 |
| WPA2 | 2004 | AES, KRACK 2017 |
| WPA3 | 2018 | SAE, forward secrecy |

**802.1X — Enterprise**: client ↔ AP ↔ RADIUS.

## §22 Firewall 종류

| | 동작 |
|--|--|
| Stateless | Per-packet |
| Stateful | Connection state |
| Application gateway | Application-level (WAF) |
| NGFW | Stateful + IDS/IPS + DPI |

## §23 IDS / IPS / SIEM

| | 특징 |
|--|--|
| IDS signature | Known (Snort, Suricata) |
| IDS anomaly | Baseline, zero-day |
| IPS | IDS + blocking |
| SIEM | Log 통합 (Splunk, Wazuh) |
| SOAR | Automated response |

## §24 DDoS 방어 계층

1. ISP filter
2. Cloud scrubbing (Cloudflare, AWS Shield)
3. Application rate limit, captcha
4. Auto-scaling
- Anycast (분산 흡수)
- Tarpit (slow down)

## §25 Secret 관리

| Tool | 용도 |
|--|--|
| HashiCorp Vault | 일반 |
| AWS Secrets Manager | AWS |
| Azure Key Vault | Azure |
| Kubernetes Secrets | K8s |

Rotation: 90 day 또는 event-based.

## §26 STRIDE

| | 의미 |
|--|--|
| Spoofing | Identity 위조 |
| Tampering | 변조 |
| Repudiation | 부인 |
| Information disclosure | 노출 |
| Denial of service | 거부 |
| Elevation of privilege | 권한 상승 |

## §27 Post-quantum

**Quantum (Shor)**: RSA, ECC, DH 깨짐.

**NIST PQ 2024**:
- CRYSTALS-Kyber — key exchange
- CRYSTALS-Dilithium — signature
- FALCON — smaller signature
- SPHINCS+ — hash-based

**Symmetric (Grover)**: key 2x (AES-256).
**Hash**: SHA-384 / SHA-512.

## §28 Tool 모음

| Tool | 용도 |
|--|--|
| `openssl s_client` | TLS 분석 |
| `openssl x509` | Cert 분석 |
| `nmap --script ssl-enum-ciphers` | Cipher 협상 |
| `gpg` | PGP |
| `ssh-keygen` | SSH key |
| `fail2ban` | Brute force 방어 |
| `iptables`, `nftables` | Firewall |
| `tcpdump`, `wireshark` | Packet capture |
| `nikto`, `nmap` | Vuln scan |
| `OWASP ZAP` | Web app pen test |

## §29 자주 빠지는 함정

| 함정 | 실제 |
|--|--|
| HTTPS = secure | Cert validation + cipher strength 도 |
| VPN = privacy | Provider 가 봄 (Tor 가 진짜) |
| Sym vs Asym | Hybrid 가 표준 |
| RSA = 표준 | ECC, EdDSA 가 modern |
| Hash = encryption | One-way |
| MD5/SHA-1 = OK | Broken |
| WEP/WPA = security | WPA3 권장 |
| Firewall = sufficient | Defense-in-depth |
| ZT = no firewall | 둘 다 |
| Quantum = far future | 2030~ 시작 |

## §30 핵심 mindmap

```
Network Security
├── CIA + 1
├── Cryptography
│   ├── Symmetric (AES, ChaCha20) + AEAD
│   ├── Asymmetric (RSA, ECC, EdDSA)
│   └── Hybrid (TLS 의 표준)
├── Hash + MAC + Signature
│   ├── SHA-256, SHA-3
│   ├── HMAC
│   └── EdDSA (Ed25519)
├── PKI
│   ├── CA + Cert chain
│   ├── Revocation
│   └── Let's Encrypt
├── TLS
│   ├── 1.3 (1 RTT, AEAD only)
│   ├── 0 RTT resumption
│   └── HTTPS 95%+
├── IPsec + VPN
│   ├── Transport / Tunnel
│   └── WireGuard
├── Wireless (WPA3)
├── Firewall + IDS + DDoS
├── Zero Trust (BeyondCorp)
└── Future (Post-quantum)
```

## §31 1-line summary

> **Network security = CIA + non-repudiation + availability. Symmetric (AES-GCM) + Asymmetric (ECDH, EdDSA) 의 hybrid. TLS 1.3 가 web security 표준. IPsec + WireGuard 의 network layer 보안. Firewall + IDS + Zero Trust 의 defense in depth. Post-quantum 의 다가오는 변화.**
