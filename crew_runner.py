#CrewAI is used to create agents with roles, goals, and tasks
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM #llm cause im not using langchain to invoke the model w lazem with groq to get the model
from rag import setup_rag

load_dotenv()

retriever = setup_rag()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0
)


def run_cyber_audit_crew(finding_text: str):
    docs = retriever.invoke(finding_text)

    retrieved_context = "\n".join(
        [doc.page_content for doc in docs]
    )

    vulnerability_analyst = Agent(
        role="Vulnerability Analyst",
        goal="Analyze cybersecurity vulnerabilities and explain their security impact.",
        backstory="You are a cybersecurity analyst specialized in vulnerability assessment.",
        llm=llm,
        verbose=True#Show what the agent is doing in the terminal
    )
    
    severity_agent = Agent(
    role="Severity Classification Analyst",
    goal="Classify vulnerability severity as Low, Medium, High, or Critical.",
    backstory="You specialize in risk scoring and vulnerability severity classification.",
    llm=llm,
    verbose=True
    )

    compliance_agent = Agent(
        role="Cybersecurity Compliance Analyst",
        goal="Compare vulnerability findings with cybersecurity guidelines.",
        backstory="You review findings against security best practices and internal guidelines.",
        llm=llm,
        verbose=True
    )

    remediation_agent = Agent(
        role="Remediation Specialist",
        goal="Suggest safe defensive remediation steps.",
        backstory="You specialize in secure configuration and defensive remediation.",
        llm=llm,
        verbose=True
    )

    report_writer = Agent(
        role="Audit Report Writer",
        goal="Write a professional cybersecurity audit report.",
        backstory="You write clear audit reports for security teams and managers.",
        llm=llm,
        verbose=True
    )

    task1 = Task(
        description=f"""
Analyze the following vulnerability finding.

Finding:
{finding_text}

Retrieved Cybersecurity Guideline:
{retrieved_context}

Explain:
- what the vulnerability is
- why it matters
- possible security impact

Do not provide offensive hacking steps.
Keep the answer concise. Maximum 120 words.
Do not repeat the same idea.
""",
        expected_output="A clear vulnerability analysis.",
        agent=vulnerability_analyst
    )
    
    task2 = Task(
        description=f"""
Classify the severity of this vulnerability.

Finding:
{finding_text}

Retrieved Cybersecurity Guideline:
{retrieved_context}

Use only one severity level:
Low, Medium, High, or Critical.

Briefly justify the severity in maximum 80 words.
""",
        expected_output="Severity level and short justification.",
        agent=severity_agent
    )

    task3 = Task(
        description=f"""
Compare the vulnerability with the retrieved cybersecurity guideline.

Retrieved Guideline:
{retrieved_context}

Explain which guideline applies and why.
Keep the answer concise. Maximum 120 words.
Do not repeat the same idea.
""",
        expected_output="A compliance/guideline mapping explanation.",
        agent=compliance_agent
    )

    task4 = Task(
        description=f"""
Suggest defensive remediation steps for this vulnerability.

Retrieved Cybersecurity Guideline:
{retrieved_context}

Use the vulnerability analysis and guideline mapping from previous tasks.
Focus only on safe defensive recommendations.
Keep the answer concise. Maximum 120 words.
Do not repeat the same idea.
""",
        expected_output="A list of safe remediation actions.",
        agent=remediation_agent
    )

    task5 = Task(
        description=f"""
Write a final cybersecurity audit report for this finding.

The report must include:
- Severity
- Category
- Risk
- Retrieved Guideline Used
- Remediation
- Audit Summary

Retrieved Guideline Used:
{retrieved_context}
Keep the final report under 250 words.
""",
        expected_output="A professional final audit report.",
        agent=report_writer
    )

    crew = Crew(
        agents=[
            vulnerability_analyst,
            severity_agent,
            compliance_agent,
            remediation_agent,
            report_writer
        ],
        tasks=[task1, task2, task3, task4, task5],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()#Begin the cyber audit process

    return result