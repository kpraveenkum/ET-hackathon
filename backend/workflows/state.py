from typing import Literal
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    next: Literal[
        "qa",
        "compliance",
        "schedule",
        "commissioning",
    ]