import asyncio
import time
from typing import Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status

app = FastAPI(
    title="Enterprise LLM Gateway Proxy",
    description="High-performance rate-limiting and quota governance guardrail.",
    version="1.0.0"
)

# Production In-Memory Database State (In production, replace with Redis)
BUSINESS_UNIT_REGISTRY: Dict[str, Dict[str, int]] = {
    "Finance": {"budget": 3000000, "consumed": 850000, "max_per_request": 30000},
    "Marketing": {"budget": 5000000, "consumed": 4100000, "max_per_request": 15000},
    "Product": {"budget": 4000000, "consumed": 1200000, "max_per_request": 20000},
    "Engineering": {"budget": 15000000, "consumed": 6250000, "max_per_request": 128000},
    "Security": {"budget": 2000000, "consumed": 1950000, "max_per_request": 50000},
    "Research": {"budget": 25000000, "consumed": 18400000, "max_per_request": 256000}
}

class TokenRequest(BaseModel):
    business_unit: str = Field(..., description="The registered corporate business unit identifier")
    requested_tokens: int = Field(..., gt=0, description="Number of tokens estimated for the inference job")
    input_prompt: str = Field(..., min_length=5, description="The raw prompt string payload to evaluate")

@app.post("/v1/proxy/handshake", status_code=status.HTTP_200_OK)
async def execute_proxy_handshake(payload: TokenRequest) -> Dict[str, Any]:
    start_time = time.perf_counter()
    bu = payload.business_unit

    # Gate 1: Non-blocking Governance Check
    if bu not in BUSINESS_UNIT_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Access denied. Business Unit '{bu}' is not onboarded to the AI governance framework."
        )

    config = BUSINESS_UNIT_REGISTRY[bu]

    # Gate 2: Enforce Single-Request Payload Boundaries
    if payload.requested_tokens > config["max_per_request"]:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload blocked. Requested tokens ({payload.requested_tokens}) exceed maximum allowed window ({config['max_per_request']}) for {bu}."
        )

    # Gate 3: Enforce Atomic Macro Monthly Budget Constraints
    # Note: In production, use Redis INCRBY to avoid race conditions
    projected_total = config["consumed"] + payload.requested_tokens
    if projected_total > config["budget"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate-limit triggered. Request of {payload.requested_tokens} tokens breaches the remaining monthly budget ceiling for {bu}."
        )

    # Simulate highly optimized, non-blocking asymmetric network I/O or model routing overhead
    await asyncio.sleep(0.01)
    
    # Commit token consumption to registry state
    BUSINESS_UNIT_REGISTRY[bu]["consumed"] = projected_total
    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return {
        "status": "SUCCESS",
        "routing_telemetry": {
            "originating_business_unit": bu,
            "allocated_tokens_approved": payload.requested_tokens,
            "gateway_processing_latency_ms": latency_ms,
            "remaining_monthly_quota_tokens": config["budget"] - projected_total
        }
    }
