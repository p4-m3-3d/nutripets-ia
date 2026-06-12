from app.ai.chroma_client import collection
from app.ai.embedding_service import create_embedding
from app.ai.llm_service import LLMService
from app.ai.toxic_detector import ToxicDetector

class RagService:


    @staticmethod
    def ask(question: str):
        toxic_result = ToxicDetector.detect(
            question
            )

        if toxic_result["found"]:

            return {
                "question": question,
                "alert": True,
                "ingredient": toxic_result["ingredient"],
                "danger_level": toxic_result["danger_level"],
                "symptoms": toxic_result["symptoms"],
                "action_required": toxic_result["action_required"]
            }

        embedding = create_embedding(question)

        results = collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        docs = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(docs)

        answer = LLMService.generate(
            context=context,
            question=question
        )

        recommendations = []

        for metadata in metadatas:

            if metadata is None:
                continue

            recommendations.append(metadata)

        return {
            "question": question,
            "answer": answer,
            "recommendations": recommendations,
            "sources_found": len(docs)
        }
