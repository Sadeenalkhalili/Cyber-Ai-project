from dotenv import load_dotenv
from analyzer import analyze_vulnerability

load_dotenv()

with open("sample_findings.txt", "r", encoding="utf-8") as file:
    finding_text = file.read()

result = analyze_vulnerability(finding_text)

print("\n=== Vulnerability Analysis ===")
print("Severity:", result.severity)
print("Category:", result.category)
print("Risk:", result.risk)
print("Remediation:", result.remediation)
print("Audit Summary:", result.audit_summary)