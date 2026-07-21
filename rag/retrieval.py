from __future__ import annotations

from typing import Any, List

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag.ingestion import (
    DATA_DIR,
    PERSIST_DIR,
    get_embeddings,
    split_documents,
    load_documents_from_file,
)

load_dotenv()


def get_vectorstore() -> Chroma:
    embedding_model = get_embeddings()

    return Chroma(
        collection_name="data_center_rag",
        embedding_function=embedding_model,
        persist_directory=str(PERSIST_DIR),
        create_collection_if_not_exists=True,
    )


def add_documents_to_vectorstore(documents: List[Document]) -> int:

    vectorstore = get_vectorstore()

    vectorstore.add_documents(documents)

    return len(documents)


def initialize_seed_documents() -> int:

    vectorstore = get_vectorstore()

    if vectorstore._collection.count() > 0:
        return int(vectorstore._collection.count())

    if not DATA_DIR.exists():
        return 0

    all_chunks = []

    for file_path in DATA_DIR.rglob("*"):

        if file_path.suffix.lower() not in [".txt", ".pdf", ".docx"]:
            continue

        try:

            docs = load_documents_from_file(file_path)

            chunks = split_documents(docs)

            all_chunks.extend(chunks)

        except Exception:
            continue

    if all_chunks:

        add_documents_to_vectorstore(all_chunks)

    return len(all_chunks)


def build_retriever(
    k: int = 5,
    metadata_filter: dict | None = None,
) -> Any:

    vectorstore = get_vectorstore()

    search_kwargs = {
        "k": k,
    }

    if metadata_filter:

        search_kwargs["filter"] = metadata_filter

        print("\nUsing Metadata Filter")
        print(metadata_filter)

    return vectorstore.as_retriever(
        search_kwargs=search_kwargs
    )