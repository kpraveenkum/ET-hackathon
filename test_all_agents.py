from backend.agents.qa.agent import qa_agent
from backend.agents.compliance.agent import compliance_agent
from backend.agents.schedule.agent import schedule_agent
from backend.agents.commissioning.agent import commissioning_agent

print("=" * 60)
print("QA AGENT")
print(qa_agent("What is Linux?"))

print("=" * 60)
print("COMPLIANCE AGENT")
print(compliance_agent("What are the safety standards?"))

print("=" * 60)
print("SCHEDULE AGENT")
print(schedule_agent("What is the project schedule?"))

print("=" * 60)
print("COMMISSIONING AGENT")
print(commissioning_agent("Explain FAT testing"))