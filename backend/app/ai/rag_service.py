from app.ai.chroma_client import collection
from app.ai.embedding_service import create_embedding
from app.ai.llm_service import LLMService


class RagService:

    @staticmethod
    def ask(question: str):

        embedding = create_embedding(question)

        results = collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        docs = results["documents"][0]

        context = "\n\n".join(docs)

        answer = LLMService.generate(
            context=context,
            question=question
        )

        return {
            "question": question,
            "answer": answer,
            "sources_found": len(docs)
        }