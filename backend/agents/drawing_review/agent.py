from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage


from backend.services.vision_processor import pdf_to_images
from backend.services.vision_llm import analyze_drawing


from rag.llm import get_llm
from backend.tools.rag_tool import rag_search

from .prompts import DRAWING_REVIEW_SYSTEM_PROMPT


def drawing_review_logic(state):

    llm = get_llm()


    messages = state["messages"]

    question = (
        messages[-1]
        if isinstance(messages[-1], str)
        else messages[-1].content
    )


    print("DRAWING REVIEW QUESTION:", question)


    # Retrieve drawing documents
    rag_result = rag_search.invoke(question)


    print("DRAWING RAG RESULT:")
    print(rag_result)



    response = llm.invoke(
        [
            SystemMessage(
                content=DRAWING_REVIEW_SYSTEM_PROMPT
            ),

            HumanMessage(
                content=f"""
User Question:

{question}


Retrieved Drawing Documents:

{rag_result}


Generate the final drawing review report.

Include:

1. Drawing information
2. Missing details
3. Issues found
4. Compliance status
5. Recommendations

Use only the retrieved documents.
"""
            )
        ]
    )


    return {
        "messages":[response]
    }





drawing_review_agent = RunnableLambda(
    drawing_review_logic
)

drawing_review_agent = RunnableLambda(
    drawing_review_logic
)