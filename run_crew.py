from crew_runner import run_cyber_audit_crew
import time

with open("sample_findings.txt", "r", encoding="utf-8") as file:
    content = file.read()


findings = [f.strip() for f in content.split("Finding") if f.strip()]

all_reports = []

for index, finding in enumerate(findings, start=1):
    print(f"\nRunning CrewAI audit for Vulnerability {index}...")

    try:
        result = run_cyber_audit_crew(finding)

    except Exception as e:
        print("Rate/API error happened. Waiting 20 seconds then retrying...")
        time.sleep(20)
        result = run_cyber_audit_crew(finding)

    section = f"""
==================================================
CREWAI AUDIT REPORT - VULNERABILITY {index}
==================================================

Original Finding:
{finding}

CrewAI Result:
{result}
"""

    all_reports.append(section)

    time.sleep(15)#Groq has time to reset token usage


final_report = "\n".join(all_reports)

with open("crewai_audit_report.txt", "w", encoding="utf-8") as file:
    file.write(final_report)


print("\nCrewAI audit report generated successfully!")