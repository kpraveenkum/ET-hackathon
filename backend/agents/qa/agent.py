from langgraph.prebuilt import create_react_agent

from rag.llm import get_llm
from backend.tools.rag_tool import rag_search
from .prompts import QA_SYSTEM_PROMPT

qa_agent = create_react_agent(
    model=get_llm(),
    tools=[rag_search],
    prompt=QA_SYSTEM_PROMPT,
    name="qa_agent",
)