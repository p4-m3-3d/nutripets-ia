from app.ai.chroma_client import collection
from app.ai.embedding_service import create_embedding


class SearchService:

    @staticmethod
    def search(query: str):

        embedding = create_embedding(query)

        results = collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        response = []

        documents = results["documents"][0]
        metadata = results["metadatas"][0]

        for doc, meta in zip(
            documents,
            metadata
        ):

            response.append({
                "type": meta["type"],
                "title": meta["title"],
                "content": doc
            })

        return response