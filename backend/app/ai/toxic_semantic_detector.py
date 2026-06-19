from app.ai.chroma_client import get_collection
from app.ai.embedding_service import create_embedding

from app.core.database import SessionLocal
from app.models.toxic_ingredient_model import ToxicIngredient


class ToxicSemanticDetector:

    @staticmethod
    def detect(question: str):

        embedding = create_embedding(question)

        results = get_collection().query(
            query_embeddings=[embedding],
            n_results=3,
            where={
                "type": "toxic"
            }
        )

        print("\n===== CHROMA =====")
        print(results)
        print("==================\n")

        if not results["metadatas"][0]:
            return None

        distance = results["distances"][0][0]

        print(
            f"\nDISTANCIA TOXICA: {distance}\n"
        )

        # FILTRO DE CONFIANZA
        if distance > 1.0:

            print(
                "DESCARTADO POR BAJA CONFIANZA"
            )

            return None

        toxic_name = (
            results["metadatas"][0][0]
            .get("name")
        )

        db = SessionLocal()

        try:

            toxic = (
                db.query(ToxicIngredient)
                .filter(
                    ToxicIngredient.name == toxic_name
                )
                .first()
            )

            if not toxic:
                return None

            return {
                "type": "toxic",
                "name": toxic.name,
                "danger_level": toxic.danger_level,
                "symptoms": toxic.symptoms,
                "action_required": toxic.action_required,
                "distance": distance
            }

        finally:

            db.close()