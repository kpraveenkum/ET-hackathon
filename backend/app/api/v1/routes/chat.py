from fastapi import APIRouter

from backend.schemas.chat import ChatRequest, ChatResponse
from backend.agents.supervisor.router import route_question
from backend.agents.supervisor.executor import execute_agent


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    agent_name = route_question(
        request.question
    )

    result = execute_agent(
        agent_name,
        request.question
    )

    return ChatResponse(
        agent=result["agent"],
        answer=result["answer"],
        sources=result["sources"],
    )