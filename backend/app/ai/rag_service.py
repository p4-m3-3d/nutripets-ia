from app.ai.chroma_client import get_collection
from app.ai.embedding_service import create_embedding
from app.ai.llm_service import LLMService
from app.ai.toxic_detector import ToxicDetector
from app.ai.query_analyzer import QueryAnalyzer
from app.ai.toxic_semantic_detector import (
    ToxicSemanticDetector
)

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

            if toxic_result["match_type"] == "symptom":

                return {
                    "question": question,
                    "alert": True,
                    "match_type": "symptom",
                    "highest_risk": toxic_result.get(
                        "highest_risk"
                    ),
                    "possible_toxicities": toxic_result[
                        "possible_toxicities"
                    ]
                }

            return {
                "question": question,
                "alert": True,
                "match_type": toxic_result.get(
                    "match_type"
                ),
                "ingredient": toxic_result["ingredient"],
                "danger_level": toxic_result["danger_level"],
                "urgency": toxic_result.get(
                    "urgency"
                ),
                "recommended_action": toxic_result.get(
                    "recommended_action"
                ),
                "reason": toxic_result.get(
                    "reason"
                ),
                "symptoms": toxic_result["symptoms"],
                "action_required": toxic_result["action_required"]
            }

        # ==================================
        # DETECCION SEMANTICA DE TOXICOS
        # ==================================

        semantic_toxic = (
            ToxicSemanticDetector.detect(
                question
            )
        )

        if (
            semantic_toxic
            and semantic_toxic.get("type") == "toxic"
        ):

            return {
                "question": question,
                "alert": True,
                "match_type": "semantic",
                "ingredient": semantic_toxic.get(
                    "name"
                ),
                "danger_level": semantic_toxic.get(
                    "danger_level"
                ),
                "urgency": semantic_toxic.get(
                    "urgency"
                ),
                "recommended_action": semantic_toxic.get(
                    "recommended_action"
                ),
                "reason": (
                    f"Se encontró una coincidencia semántica "
                    f"con {semantic_toxic.get('name')}."
                ),
                "symptoms": semantic_toxic.get(
                    "symptoms"
                ),
                "action_required": semantic_toxic.get(
                    "action_required"
                )
            }

        embedding = create_embedding(question)

        results = get_collection().query(
            query_embeddings=[embedding],
            n_results=5
        )

        docs = results["documents"][0]
        metadatas = results["metadatas"][0]

        species_filter = QueryAnalyzer.detect_species(
            question
        )

        life_stage_filter = QueryAnalyzer.detect_life_stage(
            question
        )

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

            if (
                species_filter is not None
                and metadata.get("species_id") != species_filter
            ):
                continue

            if (
                life_stage_filter is not None
                and metadata.get("life_stage_id") != life_stage_filter
            ):
                continue

            title = metadata.get("title")

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