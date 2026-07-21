from pathlib import Path

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from rag.llm import get_llm
from rag.retrieval import build_retriever



def detect_metadata_filter(question: str) -> dict:

    q = question.lower()

    filters = []


    # Document Type Detection

    if (
        "commission" in q
        or "procedure" in q
        or "testing" in q
    ):

        filters.append(
            {
                "$or": [
                    {
                        "document_type": {
                            "$eq": "Procedure"
                        }
                    },
                    {
                        "document_type": {
                            "$eq": "Commissioning"
                        }
                    }
                ]
            }
        )


    elif (
        "inspection" in q
        or "inspection report" in q
        or "quality" in q
        or "qms" in q
        or "finding" in q
        or "non-conformance" in q
    ):

        filters.append(
            {
                "document_type": {
                    "$eq": "Inspection Report"
                }
            }
        )


    elif (
        "specification" in q
        or "vendor" in q
        or "requirement" in q
        or "compliance" in q
    ):

        filters.append(
            {
                "document_type": {
                    "$eq": "Specification"
                }
            }
        )


    # Discipline Detection

    if (
        "electrical" in q
        or "ups" in q
        or "generator" in q
        or "switchgear" in q
        or "cable" in q
    ):

        filters.append(
            {
                "discipline": {
                    "$eq": "Electrical"
                }
            }
        )


    elif (
        "hvac" in q
        or "cooling" in q
    ):

        filters.append(
            {
                "discipline": {
                    "$eq": "HVAC"
                }
            }
        )



    if len(filters)==1:
        return filters[0]


    if len(filters)>1:
        return {
            "$and":filters
        }


    return {}




def get_rag_chain(question:str):

    llm=get_llm()


    metadata_filter=detect_metadata_filter(question)


    print("\n========== FILTER ==========")
    print(metadata_filter)



    retriever=build_retriever(
        k=5,
        metadata_filter=metadata_filter if metadata_filter else None
    )



    prompt=ChatPromptTemplate.from_messages(
        [

            (
                "system",
                """
You are an AI EPC Project Intelligence Assistant.

Answer ONLY using the retrieved project documents.

Rules:

- Do not use outside knowledge.
- Do not hallucinate.
- Mention only findings present in documents.
- If information is missing say:

The information is not available in the uploaded project documents.


Retrieved Context:

{context}

"""
            ),

            (
                "human",
                "{input}"
            )

        ]
    )



    document_chain=create_stuff_documents_chain(
        llm,
        prompt
    )



    return create_retrieval_chain(
        retriever,
        document_chain
    )





def ask_question(question:str):


    rag_chain=get_rag_chain(question)



    response=rag_chain.invoke(
        {
            "input":question
        }
    )


    sources=[]



    print("\n========== CONTEXT DEBUG ==========")

    print(
        "Number of docs:",
        len(response["context"])
    )



    for doc in response["context"]:


        print("\nTEXT:")
        print(doc.page_content[:150])


        print("\nMETADATA:")
        print(doc.metadata)



        filename = doc.metadata.get(
            "filename",
            Path(
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            ).name
        )


        if filename not in sources:
            sources.append(filename)



    print("\nRETRIEVED SOURCES:")
    print(sources)



    return {

        "answer":response["answer"],

        "sources":sources

    }