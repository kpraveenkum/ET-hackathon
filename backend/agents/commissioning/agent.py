from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage

from rag.llm import get_llm
from backend.tools.rag_tool import rag_search


def commissioning_logic(state):

    llm = get_llm()

    messages = state["messages"]

    question = (
        messages[-1]
        if isinstance(messages[-1], str)
        else messages[-1].content
    )


    print("COMMISSIONING QUESTION:", question)


    # ==========================
    # RAG SEARCH
    # ==========================

    rag_result = rag_search.invoke(question)


    print("\nRAG RESULT:")
    print(rag_result)



    # Extract answer + sources

    retrieved_answer = rag_result.get(
        "answer",
        ""
    )

    sources = rag_result.get(
        "sources",
        []
    )


    # ==========================
    # FINAL ENGINEERING RESPONSE
    # ==========================

    response = llm.invoke(
        [
            SystemMessage(
                content="""
You are a Commissioning Engineer AI Assistant.

Answer ONLY from the retrieved project documents.

Rules:
- Do not use outside knowledge.
- Do not hallucinate.
- Do not mention RAG or tools.
- Provide a clear engineering answer.
- If the information is unavailable, reply exactly:

The information is not available in the uploaded project documents.
"""
            ),

            HumanMessage(
                content=f"""
Question:

{question}


Retrieved Project Information:

{retrieved_answer}


Provide the final answer.
"""
            )
        ]
    )


    return {

        "messages": [
            response
        ],

        # Pass sources to API
        "sources": sources
    }



commissioning_agent = RunnableLambda(
    commissioning_logic
)