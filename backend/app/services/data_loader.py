import json

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient
from app.models.recipe_model import Recipe
from app.models.catalog_models import Species
from app.models.catalog_models import LifeStage
from app.models.catalog_models import Category

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
                    species_id=item["species_id"],
                    life_stage_id=item["life_stage_id"],
                    category_id=item["category_id"]
                )

                db.add(recipe)

            db.commit()

            return {
                "message": "Recetas cargadas correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_species():

        db: Session = SessionLocal()

        try:

            db.query(Species).delete()
            db.commit()

            with open(
                "app/data/species.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                species = Species(
                    id=item["id"],
                    name=item["name"]
                )

                db.add(species)

            db.commit()

            return {
                "message": "Especies cargadas correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_life_stage():

        db: Session = SessionLocal()

        try:

            db.query(LifeStage).delete()
            db.commit()

            with open(
                "app/data/life_stage.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                stage = LifeStage(
                    id=item["id"],
                    stage_name=item["stage_name"]
                )

                db.add(stage)

            db.commit()

            return {
                "message": "Etapas cargadas correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_categories():

        db: Session = SessionLocal()

        try:

            db.query(Category).delete()
            db.commit()

            with open(
                "app/data/categories.json",
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for item in data:

                category = Category(
                    id=item["id"],
                    category_name=item["category_name"]
                )

                db.add(category)

            db.commit()

            return {
                "message": "Categorias cargadas correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def load_all():

        species_result = DataLoader.load_species()

        life_stage_result = DataLoader.load_life_stage()

        categories_result = DataLoader.load_categories()

        recipes_result = DataLoader.load_recipes()

        advice_result = DataLoader.load_advice()

        faq_result = DataLoader.load_faq()

        toxic_result = DataLoader.load_toxic_ingredients()

        return {
            "message": "Carga completa finalizada",
            "species": species_result,
            "life_stage": life_stage_result,
            "categories": categories_result,
            "recipes": recipes_result,
            "advice": advice_result,
            "faq": faq_result,
            "toxic": toxic_result
        }