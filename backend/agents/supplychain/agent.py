from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage

from rag.llm import get_llm
from backend.tools.rag_tool import rag_search


def supply_chain_logic(state):

    llm = get_llm()

    question = state["messages"][-1]


    print("SUPPLY CHAIN QUESTION:")
    print(question)


    rag_result = rag_search.invoke(question)


    response = llm.invoke(
        [

SystemMessage(
content="""
You are a Supply Chain Risk Analyst for Data Center EPC projects.

Analyze only the retrieved project documents.

Identify:

- Equipment
- Supplier
- Delivery status
- Delay days
- Risk level
- Project impact
- Mitigation action

Do not use external knowledge.

If information is unavailable say:

The information is not available in the uploaded project documents.
"""
),


HumanMessage(
content=f"""

Question:

{question}


Documents:

{rag_result}

Generate Supply Chain Risk Report.

"""
)

        ]
    )


    return {
    "messages":[response],
    "sources": rag_result.get("sources", [])
}



supply_chain_agent = RunnableLambda(
    supply_chain_logic
)