import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

try:
    client.delete_collection(
        name="nutripets_knowledge"
    )
    print("Colección eliminada")
except Exception as e:
    print(e)