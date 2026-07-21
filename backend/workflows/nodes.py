from langchain_core.messages import HumanMessage

from backend.agents.supervisor.router import route_question

from backend.agents.qa.agent import qa_agent
from backend.agents.compliance.agent import compliance_agent
from backend.agents.schedule.agent import schedule_agent
from backend.agents.commissioning.agent import commissioning_agent


def supervisor_node(state):
    question = state["messages"][-1].content

    next_agent = route_question(question)

    return {
        "next": next_agent,
    }


def qa_node(state):
    response = qa_agent.invoke(
        {
            "messages": state["messages"]
        }
    )

    return {
        "messages": response["messages"]
    }


def compliance_node(state):
    response = compliance_agent.invoke(
        {
            "messages": state["messages"]
        }
    )

    return {
        "messages": response["messages"]
    }


def schedule_node(state):
    response = schedule_agent.invoke(
        {
            "messages": state["messages"]
        }
    )

    return {
        "messages": response["messages"]
    }


def commissioning_node(state):
    response = commissioning_agent.invoke(
        {
            "messages": state["messages"]
        }
    )

    return {
        "messages": response["messages"]
    }