from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda

from rag.llm import get_llm
from backend.tools.rag_tool import rag_search



def schedule_logic(state):

    llm = get_llm()


    question = state["messages"][-1]


    print("SCHEDULE QUESTION:", question)



    rag_result = rag_search.invoke(question)


    print("SCHEDULE RAG:")
    print(rag_result)



    response = llm.invoke(
        [
            SystemMessage(
                content="""
You are an EPC Schedule Risk Analyst.

Analyze only retrieved schedule documents.

Find:
- delayed activities
- schedule risks
- project impact
- mitigation actions

Do not use outside knowledge.

Generate a professional schedule risk report.
"""
            ),


            HumanMessage(
                content=f"""

Question:

{question}


Schedule Data:

{rag_result["answer"]}


Generate final report.

"""
            )
        ]
    )


    return {
        "messages":[response],
        "sources":rag_result.get("sources",[])
    }



schedule_agent = RunnableLambda(
    schedule_logic
)