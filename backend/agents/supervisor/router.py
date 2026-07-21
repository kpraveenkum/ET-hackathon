from langchain_core.messages import HumanMessage, SystemMessage

from rag.llm import get_llm
from .prompts import SUPERVISOR_SYSTEM_PROMPT


llm = get_llm()


AVAILABLE_AGENTS = {
    "qa",
    "compliance",
    "schedule",
    "commissioning",
    "supply_chain",
    "drawing_review",
    "qms",
}


def route_question(question: str) -> str:

    response = llm.invoke(
        [
            SystemMessage(
                content=SUPERVISOR_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=question
            ),
        ]
    )


    output = response.content.strip().lower()

    print("LLM ROUTER OUTPUT:", output)


    output = (
        output
        .replace("'", "")
        .replace('"', "")
        .replace(".", "")
        .replace("`", "")
        .replace("\n", "")
        .strip()
    )


    # Exact match
    if output in AVAILABLE_AGENTS:
        return output


    # Handle space output
    if "drawing review" in output:
        return "drawing_review"


    # Keyword fallback

    if "drawing" in question.lower() or "diagram" in question.lower():
        return "drawing_review"


    if "supply" in output or "procurement" in output:
        return "supply_chain"


    if "commission" in output:
        return "commissioning"


    if "compliance" in output:
        return "compliance"


    if "schedule" in output or "delay" in output:
        return "schedule"


    return "qa"