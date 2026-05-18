from dotenv import load_dotenv
from analyzer import analyze_vulnerability

load_dotenv()


with open("sample_findings.txt", "r", encoding="utf-8") as file:
    content = file.read()


findings = [f.strip() for f in content.split("Finding") if f.strip()]

report_lines = []

for index, finding in enumerate(findings, start=1):

    result = analyze_vulnerability(finding)

    section = f"""
==================================================
VULNERABILITY {index}
==================================================

Original Finding:
{finding}

Severity:
{result.severity}

Category:
{result.category}

Risk:
{result.risk}

Remediation:
{result.remediation}

Audit Summary:
{result.audit_summary}

"""

    report_lines.append(section)

    print(f"\nProcessed Vulnerability {index}")


final_report = "\n".join(report_lines)


with open("audit_report.txt", "w", encoding="utf-8") as report_file:
    report_file.write(final_report)


print("\nAudit report generated successfully!")