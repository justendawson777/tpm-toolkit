import json
import os
import sys
import time

def load_registry(file_path):
    if not os.path.exists(file_path):
        print(f"Configuration Error: Registry file '{file_path}' was not found.")
        sys.exit(1)
    with open(file_path, 'r') as f:
        return json.load(f)

def execute_proxy_handshake(team_id, requested_tokens, input_prompt, registry):
    start_time = time.time()
    
    # Validation Gate 1: Check Business Unit Authentication / Governance
    if team_id not in registry:
        return {
            "status": "REJECTED",
            "http_status_code": 401,
            "error_code": "UNAUTHORIZED_BUSINESS_UNIT",
            "message": f"Access denied. Business Unit '{team_id}' is not onboarded to the AI governance framework."
        }
    
    team_config = registry[team_id]
    
    # Validation Gate 2: Enforce Single-Request Payload Boundaries (Context Window Guards)
    if requested_tokens > team_config["max_tokens_per_request"]:
        return {
            "status": "REJECTED",
            "http_status_code": 413,
            "error_code": "REQUEST_TOKEN_LIMIT_EXCEEDED",
            "message": f"Payload blocked. Requested tokens ({requested_tokens}) exceed maximum allowed window ({team_config['max_tokens_per_request']}) for {team_id}."
        }
        
    # Validation Gate 3: Enforce Hard Macro Monthly Budget Constraints
    projected_total = team_config["tokens_consumed_to_date"] + requested_tokens
    if projected_total > team_config["assigned_monthly_token_budget"]:
        return {
            "status": "REJECTED",
            "http_status_code": 429,
            "error_code": "MONTHLY_QUOTA_EXHAUSTED",
            "message": f"Rate-limit triggered. Request of {requested_tokens} tokens breaches the remaining monthly budget ceiling for {team_id}."
        }
        
    # Validation Gate 4: System Input Sanitization and Prompt Length Check
    if len(input_prompt.strip()) < 5:
        return {
            "status": "REJECTED",
            "http_status_code": 400,
            "error_code": "MALFORMED_PROMPT_INPUT",
            "message": "Transaction aborted. Input payload contains insufficient semantic length."
        }

    # Simulate programmatic network routing processing overhead
    time.sleep(0.12) 
    execution_latency_ms = int((time.time() - start_time) * 1000)
    
    return {
        "status": "SUCCESS",
        "http_status_code": 200,
        "routing_telemetry": {
            "originating_business_unit": team_id,
            "allocated_tokens_approved": requested_tokens,
            "gateway_processing_latency_ms": execution_latency_ms,
            "remaining_monthly_quota_tokens": team_config["assigned_monthly_token_budget"] - projected_total
        }
    }

def run_simulation_suite():
    registry_path = "data/team_quota_registry.json"
    registry = load_registry(registry_path)
    
    print("======================================================================")
    print("RUNNING: Cross-Functional Enterprise LLM Gateway Proxy Simulator")
    print(f"TARGET REGISTRY CONFIGURATION: {registry_path}")
    print("======================================================================\n")
    
    # Scenario A: Successful Context Window Routing (Engineering)
    print("Scenario A: Processing compliant high-context payload from Engineering...")
    res_a = execute_proxy_handshake("Engineering", 85000, "Refactor core authentication middleware layers to use secure JWTs.", registry)
    print(json.dumps(res_a, indent=2))
    print("-" * 70)
    
    # Scenario B: Budget Quota Exhausted Violation (Security near its cap)
    print("\nScenario B: Processing continuous log parsing pipeline request from Security...")
    res_b = execute_proxy_handshake("Security", 75000, "Analyze production container logs for lateral movement patterns.", registry)
    print(json.dumps(res_b, indent=2))
    print("-" * 70)
    
    # Scenario C: Context Window Max Payload Size Violation (Marketing)
    print("\nScenario C: Processing heavy creative optimization payload from Marketing...")
    res_c = execute_proxy_handshake("Marketing", 20000, "Generate variant copy patterns for global distribution streams.", registry)
    print(json.dumps(res_c, indent=2))
    print("-" * 70)
    
    # Scenario D: Unauthorized Access / Shadow IT Tracking (Unregistered Unit)
    print("\nScenario D: Processing incoming request traffic from an untracked entity...")
    res_d = execute_proxy_handshake("Legal_Compliance", 2000, "Audit platform internal service definitions.", registry)
    print(json.dumps(res_d, indent=2))
    print("======================================================================")

if __name__ == "__main__":
    run_simulation_suite()
