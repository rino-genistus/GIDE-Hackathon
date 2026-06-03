# Meridian Technologies — Information Security Policy
**Policy Number:** SEC-001  
**Version:** 3.1  
**Effective Date:** January 1, 2026  
**Review Date:** January 1, 2027  
**Owner:** Chief Information Security Officer  
**Classification:** Internal — All Employees

---

## 1. Purpose and Scope

This policy establishes the minimum security requirements for all information systems, data, and personnel at Meridian Technologies, Inc. ("Meridian"). It applies to all employees, contractors, consultants, temporary staff, and any third party with access to Meridian systems or data, regardless of location.

Failure to comply with this policy may result in disciplinary action up to and including termination of employment or contract, and may expose the individual and Meridian to legal liability.

---

## 2. Data Classification

All data created, received, or processed by Meridian must be classified into one of four tiers:

### Tier 1 — Public
Data intended for public consumption. No restrictions on distribution.  
Examples: marketing materials, published blog posts, job listings.

### Tier 2 — Internal
Data for internal use only. Should not be shared outside Meridian without approval.  
Examples: company policies, internal announcements, meeting notes, general business correspondence.

### Tier 3 — Confidential
Sensitive business data. Access restricted to employees with a legitimate business need.  
Examples: financial reports, customer contracts, employee compensation data, product roadmaps, source code.

### Tier 4 — Restricted
Highest sensitivity. Access requires explicit approval from the data owner and CISO.  
Examples: authentication credentials, encryption keys, PII subject to GDPR/CCPA, payment card data, M&A information, security vulnerability details.

Employees must label documents with their classification tier in the document header. Unlabeled documents default to Tier 3 (Confidential) until reviewed.

---

## 3. Access Control

### 3.1 Principle of Least Privilege
All access to systems and data must be granted on the basis of minimum necessary access to perform job responsibilities. Access must be explicitly requested and approved — it is never granted by default.

### 3.2 Account Management
- All employees receive a Meridian Google Workspace account upon hire.
- System access to production environments requires a separate request through the IT ticketing system (Jira Service Management, project: IT-ACCESS).
- Access reviews are conducted quarterly. Managers must certify their direct reports' access is still appropriate.
- Accounts must be deprovisioned within 4 hours of an employee's departure. Offboarding is initiated automatically by HR systems and enforced by the IT team.

### 3.3 Privileged Access
- Production system access (SSH, database consoles, cloud console) is restricted to the Platform Engineering and Security teams.
- All privileged access is logged via BeyondTrust Privileged Access Management (PAM). Logs are immutable and retained for 2 years.
- Break-glass access procedures exist for emergencies and require post-hoc review within 24 hours.

### 3.4 Multi-Factor Authentication
MFA is mandatory for:
- All Google Workspace accounts
- AWS console access
- GitHub
- VPN access
- Any system containing Tier 3 or Tier 4 data

Acceptable MFA methods: hardware security keys (YubiKey, preferred), TOTP authenticator apps (Google Authenticator, Authy). SMS-based MFA is not permitted due to SIM-swap risk.

---

## 4. Password Policy

Passwords must meet the following requirements:
- Minimum 16 characters
- No reuse of last 12 passwords
- No expiration (NIST 800-63B guidance — forced rotation is counterproductive)
- Must be changed immediately if compromise is suspected

Meridian uses 1Password Teams as the company password manager. All employees must use it for storing and generating credentials. Storing passwords in plaintext, spreadsheets, or browser password managers for work accounts is prohibited.

Service account passwords and API keys must be stored in HashiCorp Vault (self-hosted), not in code or environment files in source control.

---

## 5. Device Policy

### 5.1 Company Devices
All employees working with Tier 3 or Tier 4 data must use a company-issued device. Company devices are enrolled in Jamf (macOS) or Intune (Windows) for MDM.

Required device configuration:
- Full disk encryption enabled (FileVault on macOS, BitLocker on Windows)
- Auto-lock after 5 minutes of inactivity
- OS and security patches applied within 7 days of release (48 hours for critical patches)
- Endpoint detection and response (EDR) agent installed (CrowdStrike Falcon)

### 5.2 Personal Devices (BYOD)
Personal devices may access email and calendar via Meridian's Google Workspace mobile apps only. Personal devices must not be used to access source code, production systems, customer data, or Tier 3/4 documents.

### 5.3 Lost or Stolen Devices
Report a lost or stolen company device to the Security team immediately via security@meridian.com or Slack #security-alerts. Remote wipe will be initiated within 1 hour of notification.

---

## 6. Network Security

### 6.1 VPN
All access to internal systems (Jira, Confluence, internal dashboards, production infrastructure) must be over Meridian's VPN (Tailscale). VPN is always-on for corporate devices.

### 6.2 Wi-Fi
Employees should not use public Wi-Fi without VPN active. The Meridian office network is WPA3-Enterprise. Guest Wi-Fi is isolated from the corporate network.

### 6.3 Firewall and Network Segmentation
Production, staging, and development environments are in separate VPCs with no direct peering. Access between environments requires explicit approval and is logged.

---

## 7. Incident Response

### 7.1 Reporting
All suspected security incidents must be reported to the Security team immediately:
- Slack: #security-alerts
- Email: security@meridian.com
- Phone (P1 only): +1-800-MER-SEC1

A security incident includes (but is not limited to): suspected account compromise, phishing email clicked, malware on a device, unauthorized data access, exposed credentials in code or logs, lost device.

When in doubt, report it. There is no penalty for reporting a false alarm.

### 7.2 Incident Classification
- **P1 — Critical:** Active breach, ransomware, data exfiltration, production system compromise. Response: 15 minutes. CISO and CEO notified immediately.
- **P2 — High:** Credential compromise, unauthorized access detected, data exposure. Response: 1 hour.
- **P3 — Medium:** Phishing attempt (not successful), policy violation, suspicious activity. Response: 4 hours.
- **P4 — Low:** General security questions, non-urgent policy clarifications. Response: 24 hours.

### 7.3 Post-Incident Review
All P1 and P2 incidents require a written post-mortem within 5 business days, covering: timeline, root cause, impact, remediation steps, and preventive measures.

---

## 8. Third-Party and Vendor Risk

All software vendors and SaaS tools that will process Meridian data must be approved by the Security team before procurement. A vendor security review (VSR) is required for any tool handling Tier 3 or Tier 4 data.

The VSR process takes 5–10 business days. Do not sign up for or pilot a new tool with company data before VSR approval. The approved tools list is maintained in Confluence at Security > Approved Vendor List.

---

## 9. Security Training

All employees must complete:
- Security awareness training within 30 days of hire and annually thereafter (via KnowBe4)
- Phishing simulation participation — employees who fail 3 simulations in a year receive mandatory re-training
- Role-specific training for engineers (secure coding, OWASP Top 10) within 60 days of hire

Completion is tracked by the People team. Non-completion after deadline is escalated to the employee's manager.

---

## 10. Policy Violations and Exceptions

Exceptions to this policy must be requested in writing to the CISO, with a documented business justification and proposed compensating controls. Exceptions are temporary (maximum 90 days) and must be reviewed before expiry.

Violations of this policy will be handled through Meridian's standard disciplinary process. Intentional or malicious violations may result in immediate termination and referral to law enforcement.

Questions about this policy should be directed to the Security team at security@meridian.com.
