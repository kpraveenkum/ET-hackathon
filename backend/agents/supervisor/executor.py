from rag.pipeline import ask_question

from backend.agents.compliance.agent import compliance_agent
from backend.agents.schedule.agent import schedule_agent
from backend.agents.commissioning.agent import commissioning_agent
from backend.agents.supplychain.agent import supply_chain_agent
from backend.agents.drawing_review.agent import drawing_review_agent
from backend.agents.qms.agent import qms_agent

def execute_agent(agent_name: str, question: str):


    if agent_name == "qa":

        result = ask_question(question)

        return {
            "agent": "qa",
            "answer": result["answer"],
            "sources": result.get("sources", []),
        }



    AGENTS = {
        "compliance": compliance_agent,
        "schedule": schedule_agent,
        "commissioning": commissioning_agent,
        "supply_chain": supply_chain_agent,
        "drawing_review": drawing_review_agent,
        "qms": qms_agent,
    }


    agent = AGENTS.get(agent_name)


    if not agent:

        return {
            "agent": "none",
            "answer": "No suitable agent found.",
            "sources": [],
        }



    result = agent.invoke(
        {
            "messages": [
                question
            ],
            "sources": []
        }
    )


    print("\n========== AGENT RESULT ==========")
    print(result)



    answer = result["messages"][-1].content


    sources = result.get(
        "sources",
        []
    )


    print("\nFINAL AGENT SOURCES:")
    print(sources)



    return {

        "agent": agent_name,

        "answer": answer,

        "sources": sources,

    }