from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.recipe_model import Recipe


class RecipeService:

    @staticmethod
    def get_all_recipes():

        db: Session = SessionLocal()

        try:

            recipes = db.query(Recipe).all()

            result = []

            for recipe in recipes:

                result.append({
                    "id": recipe.id,
                    "title": recipe.title,
                    "description": recipe.description,
                    "preparation_time": recipe.preparation_time,
                    "difficulty": recipe.difficulty,
                    "calories": recipe.calories
                })

            return result

        finally:
            db.close()