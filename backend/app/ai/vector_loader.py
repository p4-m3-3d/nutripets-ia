from app.ai.embedding_service import create_embedding

from app.core.database import SessionLocal

from app.models.recipe_model import Recipe
from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient

from app.ai.chroma_client import (
    client,
    COLLECTION_NAME
)


class VectorLoader:

    @staticmethod
    def load_all():

        db = SessionLocal()

        try:

            # ==================================
            # ELIMINAR COLECCION ANTERIOR
            # ==================================

            try:

                client.delete_collection(
                    COLLECTION_NAME
                )

                print(
                    "COLECCION ANTERIOR ELIMINADA"
                )

            except Exception as e:

                print(
                    "NO EXISTIA COLECCION:",
                    e
                )

            # ==================================
            # CREAR NUEVA COLECCION
            # ==================================

            collection = client.get_or_create_collection(
                name=COLLECTION_NAME
            )

            print(
                "COLECCION RECREADA"
            )

            # ==================================
            # RECETAS
            # ==================================

            recipes = db.query(
                Recipe
            ).all()

            for recipe in recipes:

                text = f"""
                Receta:
                {recipe.title}

                {recipe.description}
                """

                collection.add(
                    ids=[f"recipe_{recipe.id}"],
                    documents=[text],
                    embeddings=[
                        create_embedding(text)
                    ],
                    metadatas=[{
                        "type": "recipe",
                        "title": recipe.title,
                        "species_id": recipe.species_id,
                        "life_stage_id": recipe.life_stage_id,
                        "category_id": recipe.category_id
                    }]
                )

            # ==================================
            # CONSEJOS
            # ==================================

            advice_list = db.query(
                Advice
            ).all()

            for advice in advice_list:

                text = f"""
                Consejo:
                {advice.title}

                {advice.content}
                """

                collection.add(
                    ids=[f"advice_{advice.id}"],
                    documents=[text],
                    embeddings=[
                        create_embedding(text)
                    ],
                    metadatas=[{
                        "type": "advice",
                        "title": advice.title
                    }]
                )

            # ==================================
            # FAQS
            # ==================================

            faq_list = db.query(
                FAQ
            ).all()

            for faq in faq_list:

                text = f"""
                Pregunta:
                {faq.question}

                Respuesta:
                {faq.answer}
                """

                collection.add(
                    ids=[f"faq_{faq.id}"],
                    documents=[text],
                    embeddings=[
                        create_embedding(text)
                    ],
                    metadatas=[{
                        "type": "faq",
                        "question": faq.question
                    }]
                )

            # ==================================
            # TOXICOS
            # ==================================

            toxic_list = db.query(
                ToxicIngredient
            ).all()

            for toxic in toxic_list:

                urgency = "PRECAUCIÓN"

                if toxic.danger_level == "Crítico":
                    urgency = "EMERGENCIA"

                elif toxic.danger_level == "Alto":
                    urgency = "URGENTE"

                recommended_action = (
                    "Observar síntomas y consultar a un veterinario si empeoran."
                )

                if urgency == "EMERGENCIA":

                    recommended_action = (
                        "Acudir inmediatamente a un veterinario o centro de emergencias."
                    )

                elif urgency == "URGENTE":

                    recommended_action = (
                        "Contactar a un veterinario lo antes posible y monitorear al animal."
                    )

                text = f"""
                Ingrediente tóxico:
                {toxic.name}

                Nivel de peligro:
                {toxic.danger_level}

                Nivel de urgencia:
                {urgency}

                Síntomas:
                {toxic.symptoms}

                Acción recomendada:
                {toxic.action_required}
                """

                collection.add(
                    ids=[f"toxic_{toxic.id}"],
                    documents=[text],
                    embeddings=[
                        create_embedding(text)
                    ],
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

            # ==================================
            # LOGS
            # ==================================

            print(
                f"RECETAS: {len(recipes)}"
            )

            print(
                f"CONSEJOS: {len(advice_list)}"
            )

            print(
                f"FAQS: {len(faq_list)}"
            )

            print(
                f"TOXICOS: {len(toxic_list)}"
            )

            print(
                "TOTAL EN CHROMA:",
                collection.count()
            )

            return {
                "message": "Base vectorial creada correctamente"
            }

        finally:

            db.close()