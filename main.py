from apex_orchestrator import ApexManager
from apex_queries import ApexAuditor


def run_engine():
    manager = ApexManager()
    auditor = ApexAuditor()

    print("--- Apex Engine: Intelligence Ingestion ---")
    fnd = manager.register_finding(
        subject="Persistent SQL Injection Attempt",
        context="Detected at edge firewall on port 443",
        impact="High",
        category_name="Web Security"
    )

    strat = manager.register_strategy(
        title="Sanitize Input Headers",
        methodology="Implement parameterized queries and WAF rules."
    )

    if fnd and strat:
        manager.link_finding_to_strategy(fnd.id, strat.id)
        manager.update_status(fnd.ref_code, "In-Progress")

    print("\n--- Apex Engine: High-Level Audit Report ---")
    report_data = auditor.generate_audit_report()
    for item in report_data:
        print(f"CODE:      {getattr(item, 'ref_code', 'MISSING')}")
        print(f"SUBJECT:   {getattr(item, 'subject', 'MISSING')}")
        print(f"IMPACT:    {getattr(item, 'impact_level', 'MISSING')} (Priority: {item.priority_score}/10)")

        strategy_titles = [str(s.title) for s in item.strategies if s.title]
        print(f"SOLUTIONS: {', '.join(strategy_titles) if strategy_titles else 'No strategies linked.'}")
        print("-" * 40)

    print("\n--- Current Active Workstream ---")
    active_tasks = auditor.get_findings_by_status("In-Progress")
    for task in active_tasks:
        print(f"[*] {task.ref_code}: {task.subject} | Status: {task.status}")


if __name__ == "__main__":
    run_engine()