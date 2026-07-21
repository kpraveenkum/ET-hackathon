from rag.ingestion import ingest_project_data


count = ingest_project_data()

print("Indexed chunks:", count)