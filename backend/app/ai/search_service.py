from app.ai.chroma_client import get_collection
from app.ai.embedding_service import create_embedding


class SearchService:

    @staticmethod
    def search(query: str):

        embedding = create_embedding(query)

        results = get_collection().query(
            query_embeddings=[embedding],
            n_results=5
        )

        documents = results.get("documents", [[]])[0]
        metadata = results.get("metadatas", [[]])[0]

        response = []

        for doc, meta in zip(
            documents,
            metadata
        ):
            meta = meta or {}
            title = (
                meta.get("title")
                if "title" in meta and meta.get("title") is not None
                else meta.get("question")
                if "question" in meta and meta.get("question") is not None
                else meta.get("name")
                if "name" in meta and meta.get("name") is not None
                else "Sin título"
            )

            response.append({
                "type": meta.get("type", "unknown"),
                "title": title,
                "content": doc
            })

        return response