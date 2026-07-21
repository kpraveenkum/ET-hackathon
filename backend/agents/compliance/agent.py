from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda

from rag.llm import get_llm
from backend.tools.rag_tool import rag_search



def compliance_logic(state):

    llm = get_llm()


    question = state["messages"][-1]


    rag_result = rag_search.invoke(question)



    response = llm.invoke(
        [
            SystemMessage(
content="""
You are an EPC Quality Compliance Engineer.

Generate a professional compliance report.

Format exactly:

## Compliance Report

| Parameter | Required Value | Vendor Value | Status |
|-----------|---------------|--------------|--------|

After table provide:

## Non-Conformances

List only failed items.

Rules:
- Use only retrieved documents.
- Never use external knowledge.
- If information is missing mark NOT FOUND.
"""
),

            HumanMessage(
                content=f"""
Question:

{question}


Documents:

{rag_result["answer"]}
"""
            )
        ]
    )


    return {
        "messages":[response],
        "sources":rag_result.get("sources",[])
    }



compliance_agent = RunnableLambda(
    compliance_logic
)