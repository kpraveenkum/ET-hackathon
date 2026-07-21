from agents.qa.agent import qa_agent

question = "What is Linux?"

response = qa_agent(question)

print("=" * 60)
print(response)
print("=" * 60)