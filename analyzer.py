from langchain_groq import ChatGroq
from schemas import VulnerabilityAnalysis


def analyze_vulnerability(finding_text: str) -> VulnerabilityAnalysis:

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    structured_llm = llm.with_structured_output(VulnerabilityAnalysis)

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

    return result