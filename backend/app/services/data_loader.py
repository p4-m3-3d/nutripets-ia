import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient
from app.models.recipe_model import Recipe
from app.models.catalog_models import Species, LifeStage, Category

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class DataLoader:

    @staticmethod
    def load_advice(db: Session):
        db.query(Advice).delete()
        db.commit()

        with open(DATA_DIR / "advice.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            advice = Advice(title=item["title"], content=item["content"])
            db.add(advice)

        db.commit()
        return {"message": "Consejos cargados correctamente"}

    @staticmethod
    def load_faq(db: Session):
        db.query(FAQ).delete()
        db.commit()

        with open(DATA_DIR / "faq.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            faq = FAQ(question=item["question"], answer=item["answer"])
            db.add(faq)

        db.commit()
        return {"message": "FAQ cargado correctamente"}

    @staticmethod
    def load_toxic_ingredients(db: Session):
        db.query(ToxicIngredient).delete()
        db.commit()

        with open(DATA_DIR / "toxic_ingredients.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            ingredient = ToxicIngredient(
                name=item["name"],
                aliases=",".join(item.get("aliases", [])),
                danger_level=item["danger_level"],
                symptoms=item["symptoms"],
                action_required=item["action_required"],
            )
            db.add(ingredient)

        db.commit()
        return {"message": "Ingredientes tóxicos cargados correctamente"}

    @staticmethod
    def load_recipes(db: Session):
        db.query(Recipe).delete()
        db.commit()

        with open(DATA_DIR / "recipes.json", "r", encoding="utf-8") as file:
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
                category_id=item["category_id"],
            )
            db.add(recipe)

        db.commit()
        return {"message": "Recetas cargadas correctamente"}

    @staticmethod
    def load_species(db: Session):
        db.query(Species).delete()
        db.commit()

        with open(DATA_DIR / "species.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            species = Species(id=item["id"], name=item["name"])
            db.add(species)

        db.commit()
        return {"message": "Especies cargadas correctamente"}

    @staticmethod
    def load_life_stage(db: Session):
        db.query(LifeStage).delete()
        db.commit()

        with open(DATA_DIR / "life_stage.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            stage = LifeStage(id=item["id"], stage_name=item["stage_name"])
            db.add(stage)

        db.commit()
        return {"message": "Etapas cargadas correctamente"}

    @staticmethod
    def load_categories(db: Session):
        db.query(Category).delete()
        db.commit()

        with open(DATA_DIR / "categories.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            category = Category(id=item["id"], category_name=item["category_name"])
            db.add(category)

        db.commit()
        return {"message": "Categorias cargadas correctamente"}

    @staticmethod
    def load_all(db: Session):
        # Compartimos de forma segura la misma transacción activa 'db'
        species_result = DataLoader.load_species(db=db)
        life_stage_result = DataLoader.load_life_stage(db=db)
        categories_result = DataLoader.load_categories(db=db)
        recipes_result = DataLoader.load_recipes(db=db)
        advice_result = DataLoader.load_advice(db=db)
        faq_result = DataLoader.load_faq(db=db)
        toxic_result = DataLoader.load_toxic_ingredients(db=db)

        return {
            "message": "Carga completa finalizada con éxito",
            "species": species_result,
            "life_stage": life_stage_result,
            "categories": categories_result,
            "recipes": recipes_result,
            "advice": advice_result,
            "faq": faq_result,
            "toxic": toxic_result,
        }