# tpm-toolkit

# Enterprise LLM Gateway Proxy & Rate-Limiting Guardrail

## Overview for Reviewers
This repository contains a high-performance infrastructure asset simulating an enterprise AI Gateway. It represents a common, complex technical challenge managed by infrastructure Technical Program Managers: **how to scale corporate AI adoption across cross-functional teams while preventing unthrottled API cost overruns and system resource exhaustion.** 

This project showcases dual execution pathways to satisfy both local development testing and high-throughput production needs:
1. **`local_gateway_proxy.py`**: A synchronous CLI automation utility used by developers to run pre-packaged scenario suites against business unit token allocations.
2. **`scaled_gateway_proxy.py`**: An asynchronous, non-blocking REST API service built with FastAPI and Pydantic, engineered to handle high-concurrency request validation and token accounting at scale.

---

## The Problem Statement
Uncapped developer and product access to public LLM vendor APIs (e.g., OpenAI, Anthropic) introduces massive corporate vulnerabilities:
* **Financial Risk:** A single unoptimized recursive prompt loop or a massive batch data pipeline can exhaust an entire department's monthly financial budget in minutes.
* **Operational Stability:** Unregulated token traffic leads to rate-limiting or throttling from upstream model vendors, causing service outages for critical user-facing applications.
* **Governance Gaps:** Lack of precise request attribution prevents accurate cross-functional chargebacks, allows "Shadow IT" models to pull corporate data unmonitored, and leaves the organization blind to total usage metrics.

---

## Technical Architecture
The gateway acts as an intermediate reverse proxy layer between internal applications and external vendor APIs. Every payload must clear **four sequential, zero-trust validation gates** before it is approved for upstream routing:

```text
[Incoming Payload] 
       │
       ▼
 [ Gate 1: Governance Check ] ───► Invalid BU? ──► HTTP 401 Unauthorized
       │
       ▼
 [ Gate 2: Context Window ]   ───► Too Large?  ──► HTTP 413 Entity Too Large
       │
       ▼
 [ Gate 3: Budget Ceiling ]   ───► Cap Breached? ─► HTTP 429 Too Many Requests
       │
       ▼
 [ Gate 4: Input Length ]     ───► Empty Text? ──► HTTP 400 Bad Request
       │
       ▼
[ Approved Routing Telemetry ]
```

### Cross-Functional Allocation Matrix (`data/team_quota_registry.json`)
The configuration registry establishes clear operational boundaries tailored to specific business profiles:

| Business Unit | Monthly Token Budget | Single-Request Limit | Technical Profile / Rationale |
| :--- | :--- | :--- | :--- |
| **Research** | 25,000,000 | 256,000 | Deep-dive analytical tasks; handles massive document embeddings. |
| **Engineering** | 15,000,000 | 128,000 | Automated code refactoring and CI/CD pipeline automation integrations. |
| **Marketing** | 5,000,000 | 15,000 | High-frequency, low-context generative copywriting campaigns. |
| **Product** | 4,000,000 | 20,000 | Ticket generation engines and functional requirement parsing. |
| **Finance** | 3,000,000 | 30,000 | Quarterly ledger audits and bulk document ingestion streams. |
| **Security** | 2,000,000 | 50,000 | Continuous, automated SIEM production container log scanning. |

---

## Program Roadmap
To scale this architecture from a single-region proof-of-concept to a multi-region global deployment, the cross-functional roadmap targets the following milestones:
* **Phase 1: Distributed Cache Migration (Next Quarter):** Replace the local JSON/in-memory data registries with a distributed **Redis Enterprise Cluster**, utilizing atomic `INCRBY` actions to completely eliminate race conditions during high-volume parallel requests.
* **Phase 2: Streaming Token Counting (Current Half):** Integrate native runtime token counters (such as `tiktoken`) directly into the proxy stream to track actual incoming and outgoing tokens in real-time, eliminating the reliance on client-provided token estimates.
* **Phase 3: Automated Chargeback Dashboard (Future State):** Build an internal automated engineering ledger that translates token counts directly into real-time dollars, auto-exporting data to ERP systems for cross-department billing.

---

## Cross-Functional Impact
This program solves critical operational pain points for stakeholders across the entire organization:
* **Engineering Leadership:** Protects system availability by gracefully dropping rogue or infinite-loop traffic before it triggers widespread vendor rate limits.
* **Finance & Procurement:** Enables transparent billing via hard consumption limits, ensuring no single business unit overruns shared corporate cloud budgets.
* **Security & Compliance:** Blocks unauthorized "Shadow IT" application integrations, enforcing audit trails on every payload targeting generative AI models.

---

## Tech Stack & Setup
* **Languages & Frameworks:** Python 3, FastAPI (Asynchronous Framework), Pydantic (Data Validation).
* **Server Runtime:** Uvicorn (ASGI Server).

### Environment Configuration
Navigate to the sub-project directory and verify that your Python virtual environment is active:
```bash
# Change to the gateway proxy directory
cd "/tpm-toolkit/llm-gateway-proxy"

# Activate the workspace environment
source ../venv/bin/activate

# Install required core framework components
pip install fastapi uvicorn pydantic
```

---

## Quick Start

### 1. Execute the Local Scenario Test Suite
Verify your core business unit logic instantly using the pre-configured local simulation script:
```bash
python3 src/local_gateway_proxy.py
```

### 2. Launch the High-Performance Production Proxy
Spin up the live asynchronous API gateway to handle actual HTTP network requests:
```bash
uvicorn src.scaled_gateway_proxy:app --reload --port 8000
```

### 3. Dispatch Live Test Payloads
With the server running on port `8000`, open a separate terminal window and dispatch test traffic via `curl`:

*   **Compliant Request Execution (Engineering):**
    ```bash
    curl -X POST "http://127.0.0" \
         -H "Content-Type: application/json" \
         -d '{"business_unit": "Engineering", "requested_tokens": 5000, "input_prompt": "Refactor API routing logic."}'
    ```

*   **Quota Exhaustion Rejection (Security):**
    ```bash
    curl -X POST "http://127.0.0" \
         -H "Content-Type: application/json" \
         -d '{"business_unit": "Security", "requested_tokens": 75000, "input_prompt": "Audit container activity logs."}'
    ```

---

## Sample Output

When running the live API proxy endpoints or local simulation suite, the system outputs structured telemetry tracking the transaction health:

```json
{
  "status": "SUCCESS",
  "routing_telemetry": {
    "originating_business_unit": "Engineering",
    "allocated_tokens_approved": 5000,
    "gateway_processing_latency_ms": 12,
    "remaining_monthly_quota_tokens": 8745000
  }
}
```

---

## How to Read This Output: A Walkthrough
When an application targets the proxy, the resulting JSON tells a clear technical story:
* `"status": "SUCCESS"`: Confirms that the incoming request cleared all four validation gates seamlessly. If it failed, this switches to `REJECTED` alongside an explanatory HTTP error code (e.g., `429 Too Many Requests`).
* `"allocated_tokens_approved": 5000`: The proxy has officially guaranteed and reserved this token slice out of the global organizational allowance for the request.
* `"gateway_processing_latency_ms": 12`: Demonstrates high-performance execution. The proxy evaluated rules, parsed JSON, and updated balances in just 12 milliseconds without blocking the engine.
* `"remaining_monthly_quota_tokens": 8745000`: Shows real-time ledger depletion. The requested tokens have been safely deducted, giving the team precise, live visibility into their remaining operational budget.

---

## TPM Core Competencies Demonstrated
This project demonstrates several advanced skills required for high-impact Technical Program Managers:
* **Operational Risk Management:** Proactively designs technical architectural guardrails to prevent devastating cloud cost overruns and system resource exhaustion before they occur.
* **Scalable Systems Governance:** Formulates clear, multi-tiered business rule frameworks that manage developer speed without compromising financial control.
* **Technical Architecture Fluency:** Bridges high-level business requirements (departmental budgets) with low-level engineering implementation choices (asynchronous network I/O, schema enforcement via Pydantic).
