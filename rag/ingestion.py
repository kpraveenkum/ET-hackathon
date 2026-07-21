from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, List

from dotenv import load_dotenv
from fastapi import UploadFile

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPLOAD_DIR = PROJECT_ROOT / "uploads"
PERSIST_DIR = PROJECT_ROOT / "chroma_db"

# Knowledge base folder
DATA_DIR = PROJECT_ROOT / "Data_center_RAG" / "data"

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def ensure_directories() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    PERSIST_DIR.mkdir(parents=True, exist_ok=True)



def validate_upload_file(file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("Missing filename")

    suffix = Path(file.filename).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type {suffix}"
        )

    return suffix



def save_upload_file(file: UploadFile) -> Path:

    ensure_directories()

    suffix = Path(file.filename or "upload").suffix.lower()

    filename = f"{uuid.uuid4().hex}{suffix}"

    destination = UPLOAD_DIR / filename


    with destination.open("wb") as buffer:

        while True:

            chunk = file.file.read(1024 * 1024)

            if not chunk:
                break

            buffer.write(chunk)


    return destination



def load_documents_from_file(file_path: Path) -> List[Document]:

    suffix = file_path.suffix.lower()


    if suffix == ".txt":

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )


    elif suffix == ".pdf":

        loader = PyPDFLoader(
            str(file_path)
        )


    elif suffix == ".docx":

        loader = Docx2txtLoader(
            str(file_path)
        )


    else:

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )


    documents = loader.load()


    if not documents:
        raise ValueError(
            "No content extracted"
        )


    return documents



def load_project_documents() -> List[Document]:
    """
    Load DataCenter-RAG knowledge base files
    """

    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8"
        }
    )


    documents = loader.load()


    if not documents:
        raise ValueError(
            "No project documents found"
        )


    return documents



def split_documents(
        documents: List[Document]
) -> List[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=[" "]
    )


    return splitter.split_documents(documents)



def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )



from backend.services.document_classifier import classify_document


def process_uploaded_file(
    file: UploadFile
) -> dict[str, Any]:

    validate_upload_file(file)

    saved_path = save_upload_file(file)

    documents = load_documents_from_file(saved_path)

    # -------------------------------
    # Classify document
    # -------------------------------
    metadata = classify_document(file.filename)

    # Attach metadata to every page
    for doc in documents:

        doc.metadata["document_type"] = metadata["document_type"]
        doc.metadata["discipline"] = metadata["discipline"]
        doc.metadata["project"] = metadata["project"]
        doc.metadata["filename"] = file.filename

    chunks = split_documents(documents)

    # Attach metadata to every chunk
    for chunk in chunks:

        chunk.metadata["document_type"] = metadata["document_type"]
        chunk.metadata["discipline"] = metadata["discipline"]
        chunk.metadata["project"] = metadata["project"]
        chunk.metadata["filename"] = file.filename

    from rag.retrieval import add_documents_to_vectorstore

    count = add_documents_to_vectorstore(chunks)

    return {

        "status": "success",

        "filename": saved_path.name,

        "original_filename": file.filename,

        "document_type": metadata["document_type"],

        "discipline": metadata["discipline"],

        "project": metadata["project"],

        "pages": len(documents),

        "chunks": len(chunks),

        "documents_added": count

    }


def ingest_project_data():

    """
    Build vector database from Data_center_RAG/data
    """


    documents = load_project_documents()


    chunks = split_documents(
        documents
    )


    from rag.retrieval import add_documents_to_vectorstore


    count = add_documents_to_vectorstore(
        chunks
    )


    return count