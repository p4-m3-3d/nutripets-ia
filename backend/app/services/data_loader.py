import json

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient
from app.models.recipe_model import Recipe

class DataLoader:

    @staticmethod
    def load_advice():

        db: Session = SessionLocal()

        try:

            db.query(Advice).delete()
            db.commit()

            with open(
                "app/data/advice.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                advice = Advice(
                    title=item["title"],
                    content=item["content"]
                )

                db.add(advice)

            db.commit()

            return {
                "message": "Consejos cargados correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_faq():

        db: Session = SessionLocal()

        try:

            db.query(FAQ).delete()
            db.commit()

            with open(
                "app/data/faq.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                faq = FAQ(
                    question=item["question"],
                    answer=item["answer"]
                )

                db.add(faq)

            db.commit()

            return {
                "message": "FAQ cargado correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_toxic_ingredients():

        db: Session = SessionLocal()

        try:

            db.query(ToxicIngredient).delete()
            db.commit()

            with open(
                "app/data/toxic_ingredients.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                ingredient = ToxicIngredient(
                    name=item["name"],
                    danger_level=item["danger_level"],
                    symptoms=item["symptoms"],
                    action_required=item["action_required"]
                )

                db.add(ingredient)

            db.commit()

            return {
                "message": "Ingredientes tóxicos cargados correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_recipes():

        db: Session = SessionLocal()

        try:

            db.query(Recipe).delete()
            db.commit()

            with open(
                "app/data/recipes.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                recipe = Recipe(
                    title=item["title"],
                    description=item["description"],
                    preparation=item["preparation"],
                    preparation_time=item["preparation_time"],
                    difficulty=item["difficulty"],
                    calories=item["calories"],
                    species_id=1,
                    life_stage_id=1,
                    category_id=1
                )

                db.add(recipe)

            db.commit()

            return {
                "message": "Recetas cargadas correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_all():

        recipes_result = DataLoader.load_recipes()

        advice_result = DataLoader.load_advice()

        faq_result = DataLoader.load_faq()

        toxic_result = DataLoader.load_toxic_ingredients()

        return {
            "message": "Carga completa finalizada",
            "recipes": recipes_result,
            "advice": advice_result,
            "faq": faq_result,
            "toxic": toxic_result
        }