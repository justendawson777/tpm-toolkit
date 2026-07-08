# GenAI Evaluation Framework & Model Drift Tracker (`/llm_eval_orch`)

## Quick overview (Elevator Pitch)
An automated quality-gate pipeline built using vectorized array processing to evaluate LLM output validity. It operates seamlessly inside existing engineering CI/CD systems, preventing brand damage by systematically checking model revisions against static ground truths for semantic drift and hallucinations.

## The Problem Statement

### Pain Point
Engineering teams frequently modify system prompts or swap underlying model versions (e.g., upgrading from GPT-4o to a cheaper open-source variant) without standard, regression-tested baselines. This leads to silent production degradation, toxic outputs, and "hallucination liability" hitting real end-users.

### The Project Objective
To build a high-performance evaluation matrix that computes token-overlap and semantic consistency at scale, providing program managers with a hard pass/fail exit metric to approve or block code deployment.

## Program Roadmap (Phased Approach)
*   **Phase 1 (MVP):** Build a vectorized token-matrix similarity mathematical model utilizing NumPy to score 10,000+ text generations instantly.
*   **Phase 2 (Scalability):** Implement production telemetry ingestion to flag live model drift via Grafana alerts.
*   **Phase 3 (Enterprise):** Standardize testing across product families to formalize an enterprise-wide Model Reliability SLA.

## Cross-Functional Impact
*   **Product Management:** Delivers concrete, numerical data proving product quality before rollout.
*   **DevOps/Infra:** Acts as an automated release blocker, preventing broken prompt variants from hitting main branches.
*   **Customer Support:** Radically reduces user-reported incidents stemming from broken or nonsensical AI text completions.

## Tech Stack & Setup
*   **Tech Stack:** Python 3.11+, NumPy.
*   **Setup:** Install required matrix libraries: `python3 --version pip3 --version pip3 install numpy`

## Quick Start Instructions
1. Navigate to the directory: `cd tpm-toolkit/llm-eval-orch`
2. Run the evaluation baseline: `python3 eval_gate.py`

## Sample Output
```text
 Evaluating 10,000 test cases with vectorized NumPy matrix processing...
 Evaluation Complete in 0.08412 seconds.
 CI/CD Gate Metrics: {'pass_rate_percent': 100.0, 'avg_score': 0.875, 'execution_time_seconds': 0.08412}
```

## How to Read the Output
*   **`pass_rate_percent`**: The portion of current LLM responses clearing your quality threshold. A score under your target (e.g., 85%) means the engineering deployment fails.
*   **`execution_time_seconds`**: Proves the mathematical operations are optimized. Running 10,000 checks in under 0.1 seconds ensures the evaluation gate won't slow down the developer pipeline.
