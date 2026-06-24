import pandas as pd
import json
import argparse
import sys
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Program Risk & Dependency Analyzer")
    parser.add_argument(
        "--file", 
        type=str, 
        default="data/mock_jira_data.csv", 
        help="Path to the Jira mock data CSV file"
    )
    return parser.parse_args()

def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The data file '{file_path}' was not found.")
        sys.exit(1)
    
    # Read CSV
    df = pd.read_csv(file_path)
    print("Detected CSV Columns are:", list(df.columns))

    
    # Force all column names to be clean, stripped of spaces, and consistent
    df.columns = df.columns.str.strip()
    
    # A mapping dictionary to fix common naming variations automatically
    column_mapping = {
        'ticket_id': 'Ticket_ID',
        'ticket id': 'Ticket_ID',
        'issue_type': 'Issue_Type',
        'issue type': 'Issue_Type',
        'linked_issues': 'Linked_issues',
        'linked issues': 'Linked_issues',
        'story_points': 'Story_Points',
        'story points': 'Story_Points'
    }
    
    # Standardize column headers by matching case-insensitively
    df = df.rename(columns=lambda x: column_mapping.get(x.lower(), x))
    
    # Clean up string values inside the cells
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
        
    return df


def analyze_program_dependencies(df):
    risk_report = []
    
    # Map each ticket to its respective Epic milestone context
    # Stories do not explicitly contain their parent Epic in this flat export,
    # so we group items by their blocks of IDs for mapping context
    def extract_milestone(ticket_id):
        try:
            id_num = int(ticket_id.split('-')[1])
            # Drop trailing digits to find the parent milestone block (e.g., 101 -> 100)
            milestone_id = f"WED-{(id_num // 100) * 100}"
            return milestone_id
        except:
            return "Unknown"

    # Build an inverse mapping dictionary to find what a target item blocks
    blocked_by_map = {}
    for _, row in df.iterrows():
        ticket = row['Ticket_ID']
        links = row['Linked_issues']
        
        if pd.notna(links) and "is blocked by" in links:
            # Extract target blocker ID (e.g., "is blocked by WED-101" -> "WED-101")
            upstream_blocker = links.replace("is blocked by", "").strip()
            if upstream_blocker not in blocked_by_map:
                blocked_by_map[upstream_blocker] = []
            blocked_by_map[upstream_blocker].append(ticket)

    # Core evaluation loop to catch high-impact nodes
    for _, row in df.iterrows():
        ticket_id = row['Ticket_ID']
        
        # Only evaluate actual execution stories for roadblock mapping
        if row['Issue_Type'] != 'Story':
            continue
            
        # Check if this item is a bottleneck node blocking downstream dependencies
        if ticket_id in blocked_by_map:
            downstream_tickets = blocked_by_map[ticket_id]
            impact_count = len(downstream_tickets)
            
            # Map out which distinct Milestones (Epics) are stalled by this single blocker
            impacted_milestones = sorted(list(set([extract_milestone(tid) for tid in downstream_tickets])))
            
            # Calculate total program risk saturation density metric
            total_stories = len(df[df['Issue_Type'] == 'Story'])
            saturation_pct = int((impact_count / total_stories) * 100) if total_stories > 0 else 0
            
            # Formulate the programmatic triage summary object
            risk_entry = {
                "ticket_id": ticket_id,
                "summary": row['Summary'],
                "risk_type": "CRITICAL_PATH_BOTTLENECK",
                "downstream_impact_count": impact_count,
                "impacted_milestones": impacted_milestones,
                "priority": row['Priority'],
                "mitigation_notes": f"Single point of failure. {saturation_pct}% of total program stories are directly bottlenecked by this task."
            }
            risk_report.append(risk_entry)
            
    # Sort reports by most impactful blocker node first
    risk_report = sorted(risk_report, key=lambda x: x['downstream_impact_count'], reverse=True)
    return risk_report

def main():
    args = parse_arguments()
    df = load_data(args.file)
    
    print("======================================================================")
    print("RUNNING: Automated Program Risk & Dependency Analyzer")
    print(f"TARGET DATA: {args.file}")
    print("======================================================================\n")
    
    results = analyze_program_dependencies(df)
    
    # Print clean formatted JSON report output directly to CLI dashboard
    print(json.dumps(results, indent=2))
    print("\n======================================================================")
    print("ANALYSIS COMPLETE: Dashboard JSON successfully generated for review.")
    print("======================================================================")

if __name__ == "__main__":
    main()
