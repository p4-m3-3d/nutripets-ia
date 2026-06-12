from app.ai.chroma_client import collection
from app.ai.embedding_service import create_embedding

from app.core.database import SessionLocal

from app.models.recipe_model import Recipe
from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient


class VectorLoader:

    @staticmethod
    def load_all():

        db = SessionLocal()

        try:

            collection.delete(
                where={}
            )

        except:
            pass

        recipes = db.query(Recipe).all()

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

        advice_list = db.query(Advice).all()

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

        faq_list = db.query(FAQ).all()

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

        toxic_list = db.query(
            ToxicIngredient
        ).all()

        for toxic in toxic_list:

            text = f"""
            Ingrediente:
            {toxic.name}

            Síntomas:
            {toxic.symptoms}

            Acción:
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
                    "name": toxic.name
                }]
            )

        db.close()

        return {
            "message": "Base vectorial creada"
        }