import os
from typing import Optional

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm() -> ChatGroq:
    """Create and return the Groq chat model used for answer generation."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment.")

    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)
