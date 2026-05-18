from pydantic import BaseModel, Field


class VulnerabilityAnalysis(BaseModel):
    severity: str = Field(description="Severity level: Low, Medium, High, or Critical")
    category: str = Field(description="Security category of the vulnerability")
    risk: str = Field(description="Clear explanation of the security risk")
    remediation: str = Field(description="Safe recommended fix")
    audit_summary: str = Field(description="Professional audit-style summary")