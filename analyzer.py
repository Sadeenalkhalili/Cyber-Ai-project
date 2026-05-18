from langchain_groq import ChatGroq
from schemas import VulnerabilityAnalysis
from rag import setup_rag


retriever = setup_rag()


def analyze_vulnerability(finding_text: str):

    docs = retriever.invoke(finding_text)

    retrieved_context = "\n".join(
        [doc.page_content for doc in docs]
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    structured_llm = llm.with_structured_output(VulnerabilityAnalysis)

    prompt = f"""
You are a cybersecurity audit assistant.

Use the following cybersecurity guidelines while analyzing the vulnerability.

Cybersecurity Guidelines:
{retrieved_context}

Vulnerability Finding:
{finding_text}

Rules:
- Classify severity as Low, Medium, High, or Critical.
- Explain the risk clearly.
- Suggest only defensive remediation.
- Use the retrieved cybersecurity guidelines in your reasoning.
- Do not provide offensive hacking steps.
- Write a professional audit summary.
"""

    result = structured_llm.invoke(prompt)

    return result, retrieved_context