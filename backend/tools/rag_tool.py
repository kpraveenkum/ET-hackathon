from langchain_core.tools import tool

from rag.pipeline import ask_question


@tool
def rag_search(question:str):
    """
    Search EPC project documents.
    """

    result = ask_question(question)

    return {
    "answer": result["answer"],
    "sources": result["sources"]
}