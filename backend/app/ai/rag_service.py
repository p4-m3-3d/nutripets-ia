from app.ai.chroma_client import collection
from app.ai.embedding_service import create_embedding
from app.ai.llm_service import LLMService
from app.ai.toxic_detector import ToxicDetector

SPECIES = {
    1: "Perro",
    2: "Gato"
}

LIFE_STAGES = {
    1: "Cachorro",
    2: "Adulto",
    3: "Senior"
}

CATEGORIES = {
    1: "General",
    2: "Digestiva",
    3: "Energética"
}


class RagService:

    @staticmethod
    def ask(question: str):

        toxic_result = ToxicDetector.detect(question)

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
        unique_titles = set()

        for metadata in metadatas:

            if metadata is None:
                continue

            if metadata.get("type") != "recipe":
                continue

            title = metadata.get("title")

            if not title:
                continue

            if title in unique_titles:
                continue

            unique_titles.add(title)

            recommendations.append({
                "title": title,
                "type": metadata.get("type"),
                "species": SPECIES.get(
                    metadata.get("species_id")
                ),
                "life_stage": LIFE_STAGES.get(
                    metadata.get("life_stage_id")
                ),
                "category": CATEGORIES.get(
                    metadata.get("category_id")
                )
            })

        return {
            "question": question,
            "answer": answer,
            "recommendations": recommendations,
            "sources_found": len(docs)
        }