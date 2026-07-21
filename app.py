from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.ingestion import process_uploaded_file
from rag.pipeline import ask_question

app = FastAPI(title="Data Center RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, object]:
    """Accept a document upload, save it, and index it into the vector store."""
    try:
        result = process_uploaded_file(file)
        return {"status": "success", "message": "Document uploaded successfully.", **result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc


@app.post("/ask")
async def ask(payload: AskRequest) -> dict[str, str]:
    """Answer a user question using the RAG pipeline."""
    try:
        answer = ask_question(payload.question)
        return {"answer": answer}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {exc}") from exc
