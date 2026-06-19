from pathlib import Path

import chromadb

BACKEND_ROOT = Path(__file__).resolve().parents[2]
client = chromadb.PersistentClient(
    path=str(BACKEND_ROOT / "chroma_db")
)

COLLECTION_NAME = "nutripets_knowledge"


def get_collection():

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )