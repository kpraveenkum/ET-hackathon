import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="documents"
)

result = collection.get(
    limit=5,
    include=["metadatas","documents"]
)

print(result["metadatas"])

print("\n----CONTENT----")

for doc in result["documents"]:
    print(doc[:200])