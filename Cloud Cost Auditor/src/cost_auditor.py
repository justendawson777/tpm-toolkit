import pandas as pd
import json
import argparse
import sys
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Automated Enterprise Cloud Cost Auditor")
    parser.add_argument(
        "--file", 
        type=str, 
        default="data/aws_resource_inventory.csv", 
        help="Path to the cloud resource inventory CSV file"
    )
    return parser.parse_args()

def load_inventory(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The cloud data file '{file_path}' was not found.")
        sys.exit(1)
        
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

def audit_infrastructure_costs(df):
    remediation_log = []
    
    total_current_spend = df['Monthly_Cost'].sum()
    total_potential_savings = 0.0
    
    # Financial aggregation counters by category block
    leakage_by_service = {}
    leakage_by_env = {}
    
    for _, row in df.iterrows():
        resource_id = row['Resource_ID']
        service = row['Service']
        res_type = row['Resource_Type']
        state = row['State']
        cpu = row['CPU_Utilization']
        cost = row['Monthly_Cost']
        env = row['Environment']
        owner = row['Owner_Tag']
        
        is_waste = False
        finding_type = ""
        action_item = ""
        
        # Rule 1: Isolate Unattached Storage (Orphaned EBS Volumes)
        if service == 'EBS' and state == 'available':
            is_waste = True
            finding_type = "ORPHANED_STORAGE_VOLUME"
            action_item = "Immediate Snapshot and Deletion. Volume is unattached to any running compute instance."
            
        # Rule 2: Isolate Over-provisioned Compute (Idling EC2 / RDS Instances)
        elif service in ['EC2', 'RDS'] and state == 'running' and cpu < 5.0:
            is_waste = True
            finding_type = "UNDERUTILIZED_COMPUTE_NODE"
            action_item = "Downsize instance family profile or consolidate workloads. Node is idling under 5% CPU capacity."
            
        # Rule 3: Catch Governance Risk (Missing Metadata / Ownership Tags)
        elif owner == 'Unknown' and cost > 50.0:
            is_waste = True
            finding_type = "UNOWNED_COST_CENTER"
            action_item = "Restrict permissions or re-assign to an explicit cost center. Untagged asset generating leakage."
            
        if is_waste:
            cost_val = float(cost)
            total_potential_savings += cost_val
            
            # Aggregate stats across service metrics
            leakage_by_service[service] = leakage_by_service.get(service, 0.0) + cost_val
            leakage_by_env[env] = leakage_by_env.get(env, 0.0) + cost_val
            
            remediation_log.append({
                "resource_id": resource_id,
                "service_line": f"{service} ({res_type})",
                "finding_category": finding_type,
                "monthly_leakage_amount": cost_val,
                "environment_tier": env,
                "accountable_team": owner,
                "recommended_action": action_item
            })
            
    # Sort remediation findings by highest cost leakage first
    remediation_log = sorted(remediation_log, key=lambda x: x['monthly_leakage_amount'], reverse=True)
    
    # Slice arrays down to isolate exactly the top 10 primary targets
    top_10_leaks = remediation_log[:10]
    
    # Calculate performance metadata summaries
    optimized_run_rate = total_current_spend - total_potential_savings
    savings_percentage = (total_potential_savings / total_current_spend * 100) if total_current_spend > 0 else 0
    
    # Round aggregate data blocks for perfect string serialization formatting
    report_summary = {
        "financial_summary": {
            "gross_monthly_spend": round(float(total_current_spend), 2),
            "target_remediation_savings": round(float(total_potential_savings), 2),
            "optimized_monthly_run_rate": round(float(optimized_run_rate), 2),
            "program_efficiency_gain_pct": round(savings_percentage, 1),
            "total_detected_waste_nodes": len(remediation_log)
        },
        "breakdown_metrics": {
            "leakage_by_cloud_service": {k: round(v, 2) for k, v in leakage_by_service.items()},
            "leakage_by_environment_tier": {k: round(v, 2) for k, v in leakage_by_env.items()}
        },
        "top_10_critical_remediation_targets": top_10_leaks
    }
    
    return report_summary

def main():
    args = parse_arguments()
    df = load_inventory(args.file)
    
    print("======================================================================")
    print("RUNNING: Automated Cloud Infrastructure Cost Auditor")
    print(f"AUDIT TARGET: {args.file}")
    print("======================================================================\n")
    
    report = audit_infrastructure_costs(df)
    
    # Print clean formatted JSON report output directly to CLI dashboard
    print(json.dumps(report, indent=2))
    print("\n======================================================================")
    print("AUDIT EXECUTION COMPLETE: Financial telemetry successfully generated.")
    print("======================================================================")

if __name__ == "__main__":
    main()
