from app.ai.chroma_client import get_collection
from app.ai.embedding_service import create_embedding
from sqlalchemy.orm import Session
from app.models.toxic_ingredient_model import ToxicIngredient

class ToxicSemanticDetector:

    @staticmethod
    def detect(question: str, db: Session):
        embedding = create_embedding(question)

        results = get_collection().query(
            query_embeddings=[embedding],
            n_results=1,  
            where={"type": "toxic"}
        )

        # Validación segura de contenido devuelto por ChromaDB
        if not results or not results.get("metadatas") or len(results["metadatas"][0]) == 0:
            return None

        distance = results["distances"][0][0]
        print(f"\n[DEBUG] DISTANCIA SEMÁNTICA TÓXICA: {distance}")

        # Umbral estricto para evitar falsos positivos pero capturar relaciones reales
        if distance > 0.65:
            print("[DEBUG] DESCARTADO POR BAJA CONFIANZA SEMÁNTICA")
            return None

        toxic_name = results["metadatas"][0][0].get("name")
        if not toxic_name:
            return None

        # Consumir la sesión db activa de SQLAlchemy pasada por parámetro
        toxic = db.query(ToxicIngredient).filter(ToxicIngredient.name == toxic_name).first()

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