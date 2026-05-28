# Ch 8 Security — 퀴즈

> 12 문항 (개념 4 / 계산 4 / 디버그 2 / 면접 2).

### Q1. CIA + 1 의 5 요구

각 요구 + 해당 기술?

<details><summary>답</summary>

| 요구 | 의미 | 기술 |
|--|--|--|
| **Confidentiality** | 도청 방지 | AES, ChaCha20, RSA |
| **Integrity** | 변조 방지 | SHA-256, HMAC |
| **Authentication** | 누구인지 | Digital signature, certificate, password |
| **Availability** | DoS 방지 | Rate limit, redundancy, anycast |
| **Non-repudiation** | 부인 방지 | Digital signature only (HMAC 안 됨) |

**시사**:
- 모든 secure protocol = 5 요구 의 조합
- TLS = C + I + A + non-repudiation 일부
- HMAC = I + A, *non-repudiation 없음*
- Tor = C + privacy (anonymity)

</details>

### Q2. Symmetric vs Asymmetric

각 장단점 + 실제 protocol 의 사용 방식?

<details><summary>답</summary>

| | Symmetric | Asymmetric |
|--|--|--|
| Key | 같음 | Public + Private |
| Speed | 빠름 | 100~1000x 느림 |
| Key 분배 | 어려움 | 쉬움 |
| Scalability | $N(N-1)/2$ keys | $2N$ keys |
| Non-repudiation | X | O |

**실제 — Hybrid**:
1. Asymmetric 으로 random symmetric key 교환
2. Symmetric 으로 data encrypt

**TLS 의 예**:
- Handshake — ECDH ephemeral symmetric key
- Record — AES-GCM data

**왜 hybrid**: Asymmetric trust + Symmetric speed.

</details>

### Q3. AEAD 의 의미

AES-GCM 이 AEAD. *왜 중요*?

<details><summary>답</summary>

**AEAD** = Authenticated Encryption with Associated Data.

**기존 — encrypt + MAC 분리**:
- Encrypt-then-MAC vs MAC-then-encrypt vs Encrypt-and-MAC
- Order critical — *padding oracle attack* 등 implementation bug

**AEAD 통합**:
- Encryption + integrity 한 번에
- 잘못 사용 어려움
- AES-GCM, ChaCha20-Poly1305

**Associated data**:
- 암호화 안 되지만 integrity 보호
- TLS record header (sequence number, version)

**시사**:
- TLS 1.3 = AEAD only (CBC, RC4 폐지)
- Padding oracle 같은 implementation bug 근본 회피
- Modern crypto 표준

</details>

### Q4. Hash 의 4 property

각 property + 어겼을 때 영향?

<details><summary>답</summary>

**1. Fixed output**: Any size → fixed (256 bit). 어기면 큰 input 의 size 폭증.

**2. One-way**: $H(x) = y$ 의 $y$ → $x$ 복원 불가. 어기면 password hash 직접 복원.

**3. Collision resistant**: $H(x_1) = H(x_2)$ 어려움. 어기면 digital signature forge.
- MD5 collision (2004)
- SHA-1 collision (2017)

**4. Avalanche effect**: Input 1 bit → output 절반 변경. 어기면 correlation 으로 input 추정.

**산업 영향**:
- MD5 broken → Flame malware (2012) certificate 위조
- SHA-1 broken → Git collision (Google demo, 2017)
- SHA-256 + SHA-3 권장

</details>

### Q5. RSA vs ECC key size

같은 security 의 RSA / ECC?

<details><summary>답</summary>

| Symmetric | RSA | ECC | 용도 |
|--|--|--|--|
| 80 bit | 1024 | 160 | Deprecated |
| 112 bit | 2048 | 224 | Acceptable |
| 128 bit | 3072 | 256 | Modern 표준 |
| 192 bit | 7680 | 384 | High security |
| 256 bit | 15360 | 521 | Top secret |

**핵심**:
- RSA 2048 ≈ ECC 224 (≈ AES-112)
- RSA 3072 ≈ ECC 256 (≈ AES-128)

**Why ECC 작음**: Elliptic curve discrete log 가 factorization 보다 어려움.

**산업**:
- RSA → ECC 전환 (2010s ~ 현재)
- TLS 1.3 default — ECDH (X25519, P-256)
- 모바일/IoT 에 작은 key critical
- Quantum 위협 — 둘 다 깨질 위협 → post-quantum

</details>

### Q6. TLS handshake 시간

TLS 1.2 vs 1.3, RTT = 50 ms. Handshake + first byte 시간?

<details><summary>답</summary>

**TLS 1.2** (2 RTT):
- 2 × 50 = **100 ms** handshake
- + TCP handshake 50 ms
- = **150 ms before data**

**TLS 1.3** (1 RTT):
- 1 × 50 = **50 ms** handshake
- + TCP 50 ms
- = **100 ms before data**

**TLS 1.3 + 0 RTT resumption**:
- 0 RTT — handshake 와 함께 data
- = *TCP 1 RTT only*
- TCP Fast Open + 0 RTT — even less

**산업 시사**:
- Mobile, high RTT 에 큰 차이
- Cellular RTT 100+ ms → TLS 1.3 가 200 ms 절약
- QUIC — TCP + TLS 통합, 0 RTT 까지

</details>

### Q7. Password hash work factor

bcrypt cost 12 = 250 ms. Cost 14 의 시간?

<details><summary>답</summary>

**bcrypt cost factor**:
- Cost $c$ → $2^c$ iteration
- Cost 12 = 4096 iter
- Cost 14 = 16384 iter (4x)

**시간**:
- Cost 12 = 250 ms
- Cost 14 = **1000 ms** = 1 sec

**Best practice**:
- Hashing time = 100~300 ms
- Periodic upgrade
- Argon2 (2015) — memory-hard (GPU 회피)

**Trade-off**:
- 큰 cost = 안전 + slow login
- 250 ms = sweet spot

**2025 권장**:
- bcrypt cost 12 (250 ms)
- Argon2id memory 64 MB, iter 3
- PBKDF2 600000 iter (NIST 옛 권장)

</details>

### Q8. DDoS 흡수 capacity

CDN anycast 5 region, 각 200 Gbps. 1 region 의 1 Tbps 공격 시 동작?

<details><summary>답</summary>

**Anycast 분산**:
- Anycast IP = 5 region 모두 동일 IP
- BGP closest path 자동 라우팅
- 정상 시: traffic 이 5 region 분산

**DDoS 시**:
- 한 region 의 1 Tbps 공격
- *공격 traffic 도 5 region 분산*
- 각 region: 200 Gbps (= capacity 한계)

**Scrubbing**:
- 각 region 의 scrubbing 이 legitimate vs attack 분류
- Attack = drop
- Legitimate = origin server 전달

**한계**:
- 공격 2 Tbps → 400 Gbps/region → capacity 초과
- *Total capacity 1 Tbps 가 한계*

**실제**:
- AWS Shield Advanced — Tbps
- Cloudflare — 248 Tbps peak (2024)
- 2023 Google — 398M RPS attack 흡수

</details>

### Q9. 디버그 — TLS handshake 실패

`curl https://example.com` handshake fail. 진단 + 해결.

<details><summary>답</summary>

**Common 원인**:

**1. Certificate 문제**:
- Expired — `openssl x509 -in cert.pem -noout -enddate`
- Wrong domain — CN 불일치
- Self-signed — root CA trust 없음
- Chain incomplete — intermediate CA 누락

**2. Protocol/Cipher mismatch**:
- Server TLS 1.3 only, client 옛 TLS
- Cipher suite 공통 set 없음

**3. SNI 문제**:
- Server 여러 cert hosting
- Client SNI 없음 → default cert → mismatch

**4. Firewall / proxy**:
- TLS interception (회사 proxy MITM)
- Self-signed CA injection

**5. Time skew**:
- Client clock 오차
- Cert validity 범위 밖

**진단**:
```bash
# Verbose
curl -v https://example.com 2>&1 | grep -E "(SSL|TLS|cert)"

# Full chain
openssl s_client -connect example.com:443 -servername example.com

# Cipher 협상
nmap --script ssl-enum-ciphers -p 443 example.com

# Cert dates
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# CA trust
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.pem
```

**산업 시사**:
- Let's Encrypt 90 day → auto-renew fail = handshake 실패
- Monitor cert expiry — SSL Labs
- Health check on renewal pipeline

</details>

### Q10. 디버그 — Mysterious failed login

`/var/log/auth.log` 의 수천 failed login. 진단 + 대응.

<details><summary>답</summary>

**진단**:

```bash
# Top attacker IP
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -20

# Top username
grep "Failed password for" /var/log/auth.log | awk '{print $9}' | sort | uniq -c | sort -rn | head -20

# Time distribution
grep "Failed password" /var/log/auth.log | awk '{print $1, $2}' | uniq -c
```

**패턴**:
- Brute force — 같은 user, 다른 password
- Spray — 다른 user, 같은 password
- Targeted — admin, root

**즉시 대응**:

1. **SSH 강화**:
   - `PermitRootLogin no`
   - `PasswordAuthentication no` (key-based only)
   - `AllowUsers <whitelist>`
   - Port 변경 (marginal)

2. **fail2ban**:
   - 3 fail in 10 min → 1h ban

3. **Firewall**:
   - `iptables -A INPUT -p tcp --dport 22 -s <attacker> -j DROP`
   - 또는 VPN 안에서만 SSH

4. **Audit**:
   - `last -a`, `lastb`
   - Successful login 의 unusual source

5. **Notify**:
   - Logwatch, OSSEC, Wazuh
   - Slack/email threshold alert

**Long-term**:
- MFA (libpam-google-authenticator)
- Hardware key (YubiKey)
- Passkey (FIDO2)
- SIEM 통합 (Splunk, Wazuh)
- Zero Trust — bastion host, IAP

> Internet-facing SSH = 항상 brute force 대상. 수천 attempt 가 normal. 그러나 *successful login 의 unusual* = immediate flag.

</details>

### Q11. 면접 — Quantum 의 위협

"Quantum 이 RSA 깬다는데 *언제 대비*?"

<details><summary>답</summary>

**Quantum 위협**:

**Shor's algorithm** (1994):
- Factorization + discrete log 의 polynomial time
- RSA, ECC, DH *모두 깨짐*

**현재**:
- IBM Condor (2023): 1121 qubit
- RSA 2048 → ~4096 qubit + error correction
- Useful quantum 의 *5~15 년* 예상

**Symmetric**:
- Grover algorithm — sqrt time
- AES-128 → AES-64 security
- 해결: AES-256 (key size 2배)

**Hash**:
- SHA-256 → SHA-128 security
- 해결: SHA-384 또는 SHA-512

**언제 대비**:

**Now (2026)**:
- Sensitive data with long lifetime → 시작
- Harvest now, decrypt later — attacker 의 traffic 저장
- Critical infrastructure 우선

**Post-quantum (NIST 2024)**:
- **CRYSTALS-Kyber** — key exchange
- **CRYSTALS-Dilithium** — signature
- **FALCON** — smaller signature
- **SPHINCS+** — hash-based

**산업 진행**:
- Google Chrome 2023 — hybrid post-quantum
- Cloudflare 2024 — 모든 connection
- AWS KMS 2024 — hybrid mode

**Migration 전략**:
1. Hybrid (classical + PQ)
2. Crypto-agility
3. Inventory
4. Long-term data 우선

> Quantum 의 RSA/ECC 위협 실제. 5~15년 내. Sensitive long-life data now 시작. NIST PQ 표준. Symmetric = key 2x.

</details>

### Q12. 면접 — Zero Trust 의 *현실*?

"Zero Trust 가 trendy 한데 deploy 어렵지 않나?"

<details><summary>답</summary>

**원칙** (Forrester 2010):
- Never trust, always verify
- Identity-based (not network)
- Continuous verification
- Least privilege

**Deploy 어려움**:

**1. Application inventory**:
- 모든 app 의 identity-aware 통합
- Legacy (no SSO) — proxy wrapper 또는 재작성

**2. Identity foundation**:
- Single IdP (Okta, Azure AD)
- MFA universally
- Lifecycle management

**3. Device trust**:
- Managed device only (MDM)
- Endpoint security
- BYOD 어려움

**4. Network**:
- Identity-aware proxy (Cloudflare Access, IAP)
- Micro-segmentation
- East-west inspection

**5. Continuous verification**:
- Behavior analytics
- Risk-based auth
- Session monitoring

**Realistic timeline**:
- Full = 3~5 년 journey
- 부분부터:
  - Phase 1 (3~6m): IdP + MFA
  - Phase 2 (6~12m): IAP + device trust
  - Phase 3 (1~2y): Micro-segmentation
  - Phase 4 (2~3y): Continuous verification

**사례**:

**Google BeyondCorp** (2014):
- VPN 폐지
- IAP
- Device trust
- 결과 — VPN free + better security

**일반 enterprise**:
- M365 Conditional Access — entry-level
- Okta + CrowdStrike popular combo

**Hybrid 현실**:
- Pure ZT = drama
- Defense-in-depth + ZT principles = realistic
- Firewall + ZT 둘 다

**Trade-off**:
- Operations complexity ↑
- UX — MFA friction
- Cost — IdP, MDM, proxy licenses

> ZT 원칙 옳음 — perimeter 한계 명백. 그러나 deploy 3~5 년. 부분부터 — IdP + MFA + IAP. Google BeyondCorp = 본보기. 일반 enterprise = hybrid (firewall + ZT).

</details>
