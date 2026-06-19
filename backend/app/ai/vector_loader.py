from sqlalchemy.orm import Session
from app.ai.embedding_service import create_embedding
from app.models.recipe_model import Recipe
from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient
from app.ai.chroma_client import client, COLLECTION_NAME


class VectorLoader:

    @staticmethod
    def load_all(db: Session):
        # 1. ELIMINAR COLECCIÓN ANTERIOR
        try:
            client.delete_collection(COLLECTION_NAME)
            print("COLECCIÓN ANTERIOR ELIMINADA EN CHROMADB")
        except Exception as e:
            print(f"NO EXISTÍA COLECCIÓN PREVIA: {e}")

        # 2. CREAR NUEVA COLECCIÓN
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        print("COLECCIÓN RECREADA EXITOSAMENTE")

        # 3. PROCESAR RECETAS
        recipes = db.query(Recipe).all()
        for recipe in recipes:
            text = f"Receta:\n{recipe.title}\n\n{recipe.description or ''}"
            collection.add(
                ids=[f"recipe_{recipe.id}"],
                documents=[text],
                embeddings=[create_embedding(text)],
                metadatas=[{
                    "type": "recipe",
                    "title": recipe.title,
                    "species_id": recipe.species_id or 1,
                    "life_stage_id": recipe.life_stage_id or 1,
                    "category_id": recipe.category_id or 1
                }]
            )

        # 4. PROCESAR CONSEJOS
        advice_list = db.query(Advice).all()
        for advice in advice_list:
            text = f"Consejo:\n{advice.title}\n\n{advice.content}"
            collection.add(
                ids=[f"advice_{advice.id}"],
                documents=[text],
                embeddings=[create_embedding(text)],
                metadatas=[{"type": "advice", "title": advice.title}]
            )

        # 5. PROCESAR FAQS
        faq_list = db.query(FAQ).all()
        for faq in faq_list:
            text = f"Pregunta:\n{faq.question}\n\nRespuesta:\n{faq.answer}"
            collection.add(
                ids=[f"faq_{faq.id}"],
                documents=[text],
                embeddings=[create_embedding(text)],
                metadatas=[{"type": "faq", "question": faq.question}]
            )

        # 6. PROCESAR TÓXICOS
        toxic_list = db.query(ToxicIngredient).all()
        for toxic in toxic_list:
            urgency = "PRECAUCIÓN"
            if toxic.danger_level == "Crítico":
                urgency = "EMERGENCIA"
            elif toxic.danger_level == "Alto":
                urgency = "URGENTE"

            recommended_action = "Observar síntomas y consultar a un veterinario si empeoran."
            if urgency == "EMERGENCIA":
                recommended_action = "Acudir inmediatamente a un veterinario o centro de emergencias."
            elif urgency == "URGENTE":
                recommended_action = "Contactar a un veterinario lo antes posible y monitorear al animal."

            text = f"Ingrediente tóxico:\n{toxic.name}\n\nNivel de peligro:\n{toxic.danger_level}\n\nSíntomas:\n{toxic.symptoms}"
            collection.add(
                ids=[f"toxic_{toxic.id}"],
                documents=[text],
                embeddings=[create_embedding(text)],
                metadatas=[{
                    "type": "toxic",
                    "name": toxic.name,
                    "danger_level": toxic.danger_level,
                    "urgency": urgency,
                    "recommended_action": recommended_action,
                    "symptoms": toxic.symptoms,
                    "action_required": toxic.action_required
                }]
            )

        print(f"SINCRO FINALIZADA -> TOTAL EN CHROMA: {collection.count()}")
        return {"message": "Base vectorial sincronizada correctamente con MySQL"}