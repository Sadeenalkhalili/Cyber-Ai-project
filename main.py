from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()


class VulnerabilityAnalysis(BaseModel):
    severity: str = Field(description="Severity level: Low, Medium, High, or Critical")
    category: str = Field(description="Security category of the vulnerability")
    risk: str = Field(description="Clear explanation of the security risk")
    remediation: str = Field(description="Safe recommended fix")
    audit_summary: str = Field(description="Professional audit-style summary")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(VulnerabilityAnalysis)


with open("sample_findings.txt", "r", encoding="utf-8") as file:
    finding_text = file.read()


prompt = f"""
You are a cybersecurity audit assistant.

Analyze this vulnerability finding:

{finding_text}

Rules:
- Classify severity as Low, Medium, High, or Critical.
- Explain the risk clearly.
- Suggest only defensive remediation.
- Do not provide hacking steps.
- Write a professional audit summary.
"""

result = structured_llm.invoke(prompt)


print("\n=== Vulnerability Analysis ===")
print("Severity:", result.severity)
print("Category:", result.category)
print("Risk:", result.risk)
print("Remediation:", result.remediation)
print("Audit Summary:", result.audit_summary)