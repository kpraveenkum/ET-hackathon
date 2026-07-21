from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage

from rag.llm import get_llm
from backend.tools.rag_tool import rag_search

from .prompts import QMS_SYSTEM_PROMPT



def qms_logic(state):

    llm = get_llm()


    messages = state["messages"]

    question = (
        messages[-1]
        if isinstance(messages[-1], str)
        else messages[-1].content
    )


    print("QMS QUESTION:", question)


    rag_result = rag_search.invoke(question)


    print("QMS RAG RESULT:")
    print(rag_result)


    response = llm.invoke(
        [
            SystemMessage(
                content=QMS_SYSTEM_PROMPT
            ),

            HumanMessage(
                content=f"""

Question:

{question}


Retrieved Quality Documents:

{rag_result}


Generate final QMS report.

"""
            )
        ]
    )


    return {
        "messages":[response],
        "sources": rag_result.get("sources", [])
    }



qms_agent = RunnableLambda(qms_logic)