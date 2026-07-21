from pydantic import BaseModel, Field
from typing import Any


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    agent: str
    answer: str
    sources: list[Any] = Field(default_factory=list)