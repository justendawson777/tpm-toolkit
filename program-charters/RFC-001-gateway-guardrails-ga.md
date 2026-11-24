# RFC-001: Enterprise GenAI Guardrail Proxy (`llm-gateway-proxy`) — Path to GA
**Status:** Proposed | **Author:** Justen Dawson (Staff/Principal TPM) | **Target GA:** Q1 2027 | **Repo Component:** `/llm-gateway-proxy`

## 1. Executive Summary (TL;DR)
To prevent PII leakage, prompt injection, and unbudgeted token spend across internal AI consumers, `llm-gateway-proxy` will enforce automated ingress/egress validation gates across all production LLM traffic. To reach General Availability (GA) without degrading developer velocity, we will separate synchronous policy checks (**<80ms p99 overhead**) from asynchronous semantic drift logging via `/llm-eval-orch`.

## 2. Explicit Non-Goals (Phase 1)
* **No synchronous heavy LLM-as-a-judge evaluation on ingress:** Deep semantic scoring remains asynchronous to protect real-time inference latency.
* **No air-gapped or on-premises model hosting support:** Phase 1 targets cloud-hosted foundation models and MCP agent endpoints only; air-gapped deployments are deferred to Phase 2 (Q2 2027).

## 3. Phased Rollout & Automated Exit Gates

| Phase | Target Cohort | Automated Exit Gate (Go / No-Go Criteria) |
| :--- | :--- | :--- |
| **Phase 1: Dogfood** | Internal platform & SRE workflows (`<500` RPS) | p99 proxy latency overhead **<65ms**; **100%** block rate on synthetic secret and PII test suite. |
| **Phase 2: Canary Beta** | 3 high-volume product orgs (`2,000+` engineers) | False-positive block rate **<2%**; developer override/bypass rate **<4%** over 14 consecutive days. |
| **Phase 3: General Availability** | All enterprise AI & MCP agent consumers | Sustained **99.99% proxy availability** at **5,000+ RPS** with **<80ms p99** overhead; **100%** SIEM audit log delivery with zero dropped telemetry events. |

## 4. Cross-Org RACI & Governance

| Workstream | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
| :--- | :--- | :--- | :--- | :--- |
| **Ingress Regex & PII Policy Rules** | Security Eng | Staff TPM (`Justen`) | Legal / Privacy | App Teams |
| **Fail-Open Circuit Breaker & SLOs** | Platform SRE | Eng Director | Security Eng | VP Eng |
| **FinOps Token Quotas & Chargeback** | FinOps / Cloud Eng | Staff TPM (`Justen`) | Finance / Procurement | Org Leads |

## 5. Risks & Automated Circuit-Breaker Mitigations

| Risk | Severity | Mitigation & Automated Rollback Trigger |
| :--- | :--- | :--- |
| **Guardrail Latency Spikes Degrade UX** | High | **Fail-open circuit breaker:** If proxy overhead exceeds **150ms p99 for >60s**, auto-bypass deep inspection and route payloads to an async audit queue. |
| **False Positives Block Valid Prompts** | Medium | Enforce structured bypass headers in staging; auto-quarantine any custom rule exceeding a **5% false-positive rate** within 24 hours. |
| **Unbounded Token Spend / Agent Loops** | High | **Automated rate-limit circuit breaker:** Enforce per-API-key token velocity caps; auto-throttle runaway agent loops exceeding **3x baseline hourly spend** and page on-call FinOps. |

